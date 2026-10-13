"""Manual animation-tool discovery and commit maintenance; Python standard library only."""
from __future__ import annotations

import argparse
import copy
import fnmatch
import hashlib
import json
import os
import platform
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
ROLES = {"directory", "workflow", "workbench", "engine", "library"}
SHA = re.compile(r"[0-9a-f]{40}\Z")
ID = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")
REPOSITORY = re.compile(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+\Z")


def now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    handle, temporary = tempfile.mkstemp(dir=path.parent, prefix=".write-", suffix=".json")
    try:
        with os.fdopen(handle, "w", encoding="utf-8", newline="\n") as stream:
            json.dump(value, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def inside(base, relative):
    base = base.resolve()
    path = (base / relative).resolve()
    if not path.is_relative_to(base):
        raise ValueError(f"Path escapes its workspace: {relative}")
    return path


def load_catalog():
    return read_json(ROOT / "catalog.json")


def tool_by_id(catalog, identifier):
    for tool in catalog["tools"]:
        if tool["id"] == identifier:
            return tool
    raise ValueError(f"Unknown tool: {identifier}")


def url_for(tool):
    repository = tool["source"]["repository"]
    if not REPOSITORY.fullmatch(repository) or ".." in repository:
        raise ValueError("Invalid GitHub repository name")
    return f"https://github.com/{repository}.git"


def run(argv, cwd=None, timeout=180):
    environment = dict(os.environ, GIT_TERMINAL_PROMPT="0")
    return subprocess.run(argv, cwd=cwd, env=environment, capture_output=True,
                          text=True, encoding="utf-8", errors="replace", timeout=timeout)


def git(*args, cwd=None):
    result = run(["git", "-c", "core.quotepath=false", *map(str, args)], cwd=cwd)
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip() or "Git command failed")
    return result.stdout


def remote_tip(tool):
    branch = tool["source"].get("branch")
    ref = f"refs/heads/{branch}" if branch else "HEAD"
    if branch and (branch.startswith("-") or any(c.isspace() for c in branch)):
        raise ValueError("Invalid tracking branch")
    lines = git("ls-remote", "--symref", url_for(tool), ref).splitlines()
    resolved_branch = branch
    for line in lines:
        if line.startswith("ref: refs/heads/"):
            resolved_branch = line.split("\t", 1)[0].removeprefix("ref: refs/heads/")
        elif "\t" in line:
            sha, found_ref = line.split("\t", 1)
            if found_ref == ref and SHA.fullmatch(sha):
                return {"commit": sha, "resolved_branch": resolved_branch}
    raise RuntimeError(f"Tracking ref not found: {ref}")


def fetch_source(tool, commit):
    if not ID.fullmatch(tool["id"]) or not SHA.fullmatch(commit):
        raise ValueError("Invalid source identity or commit")
    destination = inside(ROOT, f".cache/sources/{tool['id']}/{commit}")
    if (destination / ".git").exists():
        if git("remote", "get-url", "origin", cwd=destination).strip() != url_for(tool):
            raise RuntimeError("Cached source origin does not match the catalog")
        result = run(["git", "rev-parse", "HEAD"], cwd=destination)
        if result.returncode == 0:
            if result.stdout.strip() != commit:
                raise RuntimeError("Cached source HEAD does not match its commit directory; refusing to overwrite it")
            if git("status", "--porcelain", cwd=destination).strip():
                raise RuntimeError("Cached source has edits; copy them to a task workspace before reusing it")
            return destination
    destination.mkdir(parents=True, exist_ok=True)
    if not (destination / ".git").exists():
        git("init", cwd=destination)
        git("remote", "add", "origin", url_for(tool), cwd=destination)
    git("fetch", "--depth=1", "origin", commit, cwd=destination)
    git("checkout", "--detach", "FETCH_HEAD", cwd=destination)
    if git("rev-parse", "HEAD", cwd=destination).strip() != commit:
        raise RuntimeError("Fetched source does not match the requested commit")
    return destination


def fingerprint(tool):
    entry = copy.deepcopy(tool)
    entry.pop("verification", None)
    for key in ("observed_commit", "checked_at", "check_error", "resolved_branch"):
        entry["source"].pop(key, None)
    digest = hashlib.sha256(json.dumps(entry, sort_keys=True, ensure_ascii=False).encode())
    digest.update(inside(ROOT, tool["guide"]).read_bytes())
    for path in sorted((ROOT / "scripts" / "adapters").glob(f"{tool['id']}.*")):
        digest.update(path.read_bytes())
    return digest.hexdigest()


def check_updates(catalog, identifiers):
    rows = []
    for identifier in identifiers:
        tool = tool_by_id(catalog, identifier)
        print(f"Checking {identifier}", file=sys.stderr, flush=True)
        source = tool["source"]
        row = {"id": identifier, "adopted_commit": source["adopted_commit"]}
        try:
            tip = remote_tip(tool)
            source.update(observed_commit=tip["commit"], resolved_branch=tip["resolved_branch"],
                          checked_at=now(), check_error=None)
            row.update(tip, status="changed" if tip["commit"] != source["adopted_commit"] else "unchanged")
        except (OSError, ValueError, RuntimeError, subprocess.TimeoutExpired) as error:
            source.update(checked_at=now(), check_error=str(error))
            row.update(status="check-failed", error=str(error))
        rows.append(row)
    write_json(ROOT / "catalog.json", catalog)
    return rows


def state_path(identifier):
    if not ID.fullmatch(identifier):
        raise ValueError("Invalid tool ID")
    return inside(ROOT, f".state/{identifier}.json")


def upstream_commits(tool, before, after):
    url_for(tool)
    endpoint = f"https://api.github.com/repos/{tool['source']['repository']}/compare/{before}...{after}"
    commits, page = [], 1
    while True:
        request = Request(f"{endpoint}?per_page=100&page={page}",
                          headers={"Accept": "application/vnd.github+json", "User-Agent": "animation-toolbox"})
        with urlopen(request, timeout=30) as response:
            data = json.load(response)
        if not isinstance(data, dict) or not isinstance(data.get("commits"), list):
            raise ValueError("Invalid upstream comparison response")
        total = data.get("total_commits")
        if not isinstance(total, int) or total < 0:
            raise ValueError("Invalid upstream commit count")
        for item in data["commits"]:
            commit = item.get("sha") if isinstance(item, dict) else None
            details = item.get("commit") if isinstance(item, dict) else None
            message = details.get("message") if isinstance(details, dict) else None
            if not isinstance(commit, str) or not SHA.fullmatch(commit) or not isinstance(message, str):
                raise ValueError("Invalid upstream commit entry")
            commits.append({"commit": commit, "subject": message.splitlines()[0] if message else ""})
        if len({row["commit"] for row in commits}) != len(commits) or len(commits) > total:
            raise ValueError("Inconsistent upstream commit pages")
        if len(commits) == total:
            return commits
        if not data["commits"]:
            raise ValueError("Incomplete upstream commit pages")
        page += 1


def prepare_update(tool):
    source = tool["source"]
    before, after = source["adopted_commit"], source.get("observed_commit")
    if source.get("check_error"):
        raise ValueError("The latest upstream check failed; do not treat a cached observation as current")
    if not after or before == after:
        return {"id": tool["id"], "status": "unchanged"}
    print(f"Preparing {tool['id']} {before[:8]} -> {after[:8]}", file=sys.stderr, flush=True)
    candidate = fetch_source(tool, after)
    git("fetch", "--depth=1", "origin", before, cwd=candidate)
    commits = upstream_commits(tool, before, after)
    files = git("diff", "--name-only", "-z", before, after, cwd=candidate).rstrip("\x00").split("\x00")
    files = [name for name in files if name]
    diff_path = inside(ROOT, f".state/diffs/{tool['id']}-{before}-{after}.diff")
    diff_path.parent.mkdir(parents=True, exist_ok=True)
    diff_path.write_text(git("diff", "--no-ext-diff", "--no-textconv", "--no-color", before, after,
                             cwd=candidate), encoding="utf-8")
    review_files = [name for name in files if any(fnmatch.fnmatchcase(name, pattern)
                    for pattern in tool["review_globs"])]
    # This is a change summary only, never a substitute for an execution check.
    documentation_only = bool(files) and not review_files and all(name.lower().endswith(".md") for name in files)
    state = {"id": tool["id"], "base_commit": before, "candidate_commit": after,
             "source_directory": str(candidate), "changed_files": files,
             "commits": commits, "diff_path": diff_path.relative_to(ROOT).as_posix(),
             "review_files": review_files, "documentation_only": documentation_only,
             "prepared_at": now(), "status": "prepared", "receipt": None}
    write_json(state_path(tool["id"]), state)
    return state


def load_pending(tool, allow_current=False):
    path = state_path(tool["id"])
    existing = read_json(path) if path.exists() else None
    if allow_current and (existing is None or existing.get("status") == "applied"):
        source = tool["source"]
        if source["adopted_commit"] != source.get("observed_commit"):
            raise ValueError("An update was observed; prepare it before candidate verification")
        return {"id": tool["id"], "base_commit": source["adopted_commit"],
                "candidate_commit": source["adopted_commit"], "changed_files": [],
                "review_files": [], "documentation_only": False, "receipt": None, "status": "prepared"}
    if existing is None:
        raise ValueError("No pending update; run prepare-update first")
    state = existing
    if state["base_commit"] != tool["source"]["adopted_commit"]:
        raise ValueError("This update plan is stale; prepare it again")
    if state["candidate_commit"] != tool["source"].get("observed_commit"):
        raise ValueError("A different upstream candidate was observed; prepare it again")
    return state


def verify(tool, state, checks, reviewed=False):
    source = fetch_source(tool, state["candidate_commit"])
    results = []
    if not checks:
        raise ValueError("A real execution check is required")
    for check in checks:
        argv = check["argv"]
        if not isinstance(argv, list) or not argv or not all(isinstance(a, str) and a for a in argv):
            raise ValueError("Check argv must be a non-empty string array")
        cwd = inside(source, check.get("cwd", "."))
        executable = shutil.which(argv[0]) or str(inside(cwd, argv[0]))
        try:
            result = run([executable, *argv[1:]], cwd=cwd)
            record = {"argv": argv, "cwd": str(cwd.relative_to(source)), "returncode": result.returncode,
                      "stdout": result.stdout[-12000:], "stderr": result.stderr[-12000:]}
        except (OSError, subprocess.TimeoutExpired) as error:
            record = {"argv": argv, "cwd": str(cwd.relative_to(source)), "returncode": -1, "stderr": str(error)}
        results.append(record)
        if record["returncode"] != 0:
            break
    state["receipt"] = {"commit": state["candidate_commit"], "fingerprint": fingerprint(tool),
                        "checked_at": now(), "reviewed": reviewed, "checks": results,
                        "environment": {"os": platform.system(), "release": platform.release(),
                                        "python": platform.python_version()},
                        "passed": len(results) == len(checks) and all(r["returncode"] == 0 for r in results)}
    state["status"] = "verified" if state["receipt"]["passed"] else "needs-ai"
    write_json(state_path(tool["id"]), state)
    return state


def apply_update(catalog, tool, state):
    directory = tool["role"] == "directory"
    receipt = state.get("receipt")
    if not directory:
        if not receipt or not receipt["passed"] or receipt["commit"] != state["candidate_commit"]:
            raise ValueError("Candidate has no successful execution check")
        if receipt["fingerprint"] != fingerprint(tool):
            raise ValueError("Guide, adapter, or catalog entry changed after verification; verify again")
        if state["review_files"] and not receipt.get("reviewed"):
            raise ValueError("Entrypoint/usage changes still require AI review; verify with --reviewed after adapting")
    tool["source"]["adopted_commit"] = state["candidate_commit"]
    if receipt and not directory:
        tool["verification"] = {"status": "command-passed", "commit": state["candidate_commit"],
                                "checked_at": receipt["checked_at"], "checks": receipt["checks"],
                                "environment": receipt.get("environment", {})}
    state.update(status="applied", applied_at=now())
    write_json(ROOT / "catalog.json", catalog)
    write_json(state_path(tool["id"]), state)
    return {"id": tool["id"], "status": "applied", "adopted_commit": state["candidate_commit"],
            "verification": tool["verification"]["status"]}


def sync(catalog, identifiers):
    observations = check_updates(catalog, identifiers)
    results = []
    for observation in observations:
        if observation["status"] != "changed":
            results.append(observation)
            continue
        tool = tool_by_id(catalog, observation["id"])
        try:
            state = prepare_update(tool)
            if tool["role"] == "directory":
                results.append(apply_update(catalog, tool, state))
                continue
            if not state["review_files"] and tool["automatic_checks"]:
                state = verify(tool, state, tool["automatic_checks"])
                if state["receipt"]["passed"]:
                    results.append(apply_update(catalog, tool, state))
                    continue
            reasons = []
            if state["review_files"]:
                reasons.append("Usage/entrypoint files changed; review only the listed files and this tool's GUIDE")
            if not tool["automatic_checks"]:
                reasons.append("No registered execution check; perform one real minimal call")
            if state.get("receipt") and not state["receipt"]["passed"]:
                reasons.append("Registered execution check failed; see the receipt")
            state.update(status="needs-ai", reasons=reasons)
            write_json(state_path(tool["id"]), state)
            results.append(state)
        except (OSError, ValueError, RuntimeError, subprocess.TimeoutExpired) as error:
            results.append({"id": tool["id"], "status": "prepare-failed", "error": str(error)})
    return results


def search(catalog, query, role=None, task=None, output=None):
    query = query.casefold()
    words = set(re.findall(r"[a-z0-9][a-z0-9.-]*", query))
    rows = []
    for tool in catalog["tools"]:
        if role and role != tool["role"] or task and task not in tool["tasks"] or output and output not in tool["outputs"]:
            continue
        terms = [tool["id"], tool["name"], *tool["aliases"], *tool["keywords"], *tool["tasks"], *tool["outputs"]]
        haystack = " ".join(terms + [tool["summary"]]).casefold()
        score = sum(3 for term in terms if len(term) > 1 and term.casefold() in query)
        score += sum(1 for word in words if word in haystack)
        if query and query in haystack:
            score += 5
        if not query or score:
            rows.append({"id": tool["id"], "role": tool["role"], "summary": tool["summary"],
                         "outputs": tool["outputs"], "guide": tool["guide"], "score": score,
                         "verification": tool["verification"]["status"]})
    return sorted(rows, key=lambda row: (-row["score"], row["id"]))


def doctor(tool):
    requirements = []
    for alternatives in tool["requirements"]:
        found = next((shutil.which(command) for command in alternatives if shutil.which(command)), None)
        requirements.append({"alternatives": alternatives, "found": found})
    return {"id": tool["id"], "requirements": requirements,
            "commands_available": all(r["found"] for r in requirements),
            "note": "Only checks command availability; browser, package dependencies and runtime remain tool-specific"}


def validate(catalog):
    if catalog.get("schema_version") != 1 or catalog.get("update_policy") != "manual-commit-only":
        raise ValueError("This catalog requires schema 1 and manual commit-only updates")
    seen = set()
    repositories = set()
    for tool in catalog["tools"]:
        if not ID.fullmatch(tool["id"]) or tool["id"] in seen:
            raise ValueError("Invalid/duplicate tool ID")
        seen.add(tool["id"])
        if tool["role"] not in ROLES:
            raise ValueError("Invalid role")
        url_for(tool)
        repository = tool["source"]["repository"].casefold()
        if repository in repositories:
            raise ValueError(f"Duplicate upstream: {repository}")
        repositories.add(repository)
        for key in ("adopted_commit", "observed_commit"):
            if not SHA.fullmatch(tool["source"][key]):
                raise ValueError(f"Invalid {key}: {tool['id']}")
        if not inside(ROOT, tool["guide"]).is_file():
            raise ValueError(f"Missing guide: {tool['id']}")
        for field in ("tasks", "outputs", "aliases", "keywords", "review_globs", "related", "requirements", "automatic_checks"):
            if not isinstance(tool[field], list):
                raise ValueError(f"Invalid list: {field}")
        for check in tool["automatic_checks"]:
            argv = check.get("argv")
            if not isinstance(argv, list) or not argv or not all(isinstance(a, str) and a for a in argv):
                raise ValueError("Automatic check argv must be a non-empty string array")
            inside(ROOT, check.get("cwd", "."))
    for tool in catalog["tools"]:
        if any(identifier not in seen for identifier in tool["related"]):
            raise ValueError(f"Unknown related tool: {tool['id']}")
        if tool["role"] == "directory" and tool["outputs"] != ["discovery"]:
            raise ValueError("Directories cannot claim executable output")
    return {"status": "passed", "tools": len(seen), "network_used": False}


def commit_updates():
    validate(load_catalog())
    if git("rev-parse", "--show-toplevel", cwd=ROOT).strip().casefold() != str(ROOT.resolve()).replace("\\", "/").casefold():
        raise ValueError("Initialize this toolbox as its own Git repository first")
    if run(["git", "diff", "--cached", "--quiet"], cwd=ROOT).returncode:
        raise ValueError("Existing staged changes found; refusing to include other work")
    paths = [p for p in ["catalog.json", "tools", "scripts", "references", "tests", "README.md",
                         "AGENTS.md", "SKILL.md", ".gitignore"] if (ROOT / p).exists()]
    git("add", "--", *paths, cwd=ROOT)
    if run(["git", "diff", "--cached", "--quiet"], cwd=ROOT).returncode == 0:
        return {"status": "unchanged"}
    identity = []
    for key, fallback in (("user.name", "Animation Toolbox Bot"), ("user.email", "animation-toolbox@example.invalid")):
        if not run(["git", "config", "--get", key], cwd=ROOT).stdout.strip():
            identity += ["-c", f"{key}={fallback}"]
    git(*identity, "commit", "-m", "Update animation tool catalog and usage entrypoints", cwd=ROOT)
    return {"status": "committed", "commit": git("rev-parse", "HEAD", cwd=ROOT).strip(), "pushed": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("list", "validate", "commit-updates"):
        sub.add_parser(name)
    find = sub.add_parser("search")
    find.add_argument("query", nargs="?", default="")
    find.add_argument("--role", choices=sorted(ROLES))
    find.add_argument("--task")
    find.add_argument("--output")
    for name in ("show", "doctor", "fetch", "prepare-update", "apply-update"):
        command = sub.add_parser(name)
        command.add_argument("id")
    for name in ("check-updates", "sync"):
        command = sub.add_parser(name)
        group = command.add_mutually_exclusive_group(required=True)
        group.add_argument("--all", action="store_true")
        group.add_argument("--id", action="append")
        if name == "sync":
            command.add_argument("--commit", action="store_true", help="Commit managed updates locally after synchronization; never push")
    check = sub.add_parser("verify")
    check.add_argument("id")
    check.add_argument("--cwd", default=".")
    check.add_argument("--reviewed", action="store_true")
    check.add_argument("--register", action="store_true", help="Save a passing command as this tool's future automatic check")
    arguments = sys.argv[1:]
    command_argv = []
    if arguments[:1] == ["verify"] and "--" in arguments:
        separator = arguments.index("--")
        command_argv = arguments[separator + 1:]
        arguments = arguments[:separator]
    args = parser.parse_args(arguments)
    catalog = load_catalog()
    validate(catalog)
    tool = tool_by_id(catalog, args.id) if args.command in {"show", "doctor", "fetch", "prepare-update", "apply-update", "verify"} else None
    if args.command == "validate":
        result = validate(catalog)
    elif args.command == "list":
        result = {role: [t["id"] for t in catalog["tools"] if t["role"] == role] for role in sorted(ROLES)}
    elif args.command == "search":
        result = search(catalog, args.query, args.role, args.task, args.output)
    elif args.command == "show":
        result = copy.deepcopy(tool)
        result["guide_path"] = str(inside(ROOT, tool["guide"]))
        result["pinned_source_url"] = f"https://github.com/{tool['source']['repository']}/tree/{tool['source']['adopted_commit']}"
    elif args.command == "doctor":
        result = doctor(tool)
    elif args.command == "fetch":
        result = {"id": tool["id"], "commit": tool["source"]["adopted_commit"],
                  "directory": str(fetch_source(tool, tool["source"]["adopted_commit"]))}
    elif args.command in {"check-updates", "sync"}:
        identifiers = [t["id"] for t in catalog["tools"]] if args.all else list(dict.fromkeys(args.id))
        for identifier in identifiers:
            tool_by_id(catalog, identifier)
        result = (sync if args.command == "sync" else check_updates)(catalog, identifiers)
        if args.command == "sync" and args.commit:
            committed = commit_updates()
            print(json.dumps({"local_commit": committed}, ensure_ascii=False), file=sys.stderr)
    elif args.command == "prepare-update":
        result = prepare_update(tool)
    elif args.command == "verify":
        checks = [{"argv": command_argv, "cwd": args.cwd}]
        result = verify(tool, load_pending(tool, allow_current=True), checks, args.reviewed)
        if args.register and result["receipt"]["passed"]:
            tool["automatic_checks"] = checks
            result["receipt"]["fingerprint"] = fingerprint(tool)
            write_json(ROOT / "catalog.json", catalog)
            write_json(state_path(tool["id"]), result)
    elif args.command == "apply-update":
        result = apply_update(catalog, tool, load_pending(tool))
    else:
        result = commit_updates()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if isinstance(result, list) and any(r.get("status") in {"check-failed", "prepare-failed"} for r in result):
        return 1
    if args.command == "verify" and not result["receipt"]["passed"]:
        return 1
    return 0


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    try:
        sys.exit(main())
    except (OSError, ValueError, KeyError, RuntimeError, subprocess.TimeoutExpired) as error:
        print(json.dumps({"status": "error", "error": str(error)}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)
