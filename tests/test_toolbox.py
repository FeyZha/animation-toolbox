import contextlib
import copy
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("toolbox", REPOSITORY_ROOT / "scripts/toolbox.py")
tb = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tb)


class ToolboxTest(unittest.TestCase):
    def setUp(self):
        parent = REPOSITORY_ROOT / ".cache/tests"
        parent.mkdir(parents=True, exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(prefix="toolbox-", dir=parent)
        self.root = Path(self.temporary.name).resolve()
        self.assertTrue(self.root.is_relative_to(parent.resolve()))
        self.root_patch = patch.object(tb, "ROOT", self.root)
        self.root_patch.start()
        self.upstream = self.root / "upstream"
        self.upstream.mkdir()
        self.git("init", "-b", "main")
        (self.upstream / "README.md").write_text("Original usage\n", encoding="utf-8")
        (self.upstream / "run.py").write_text("print('old')\n", encoding="utf-8")
        self.old = self.commit()
        self.guide = self.root / "tools/demo/GUIDE.md"
        self.guide.parent.mkdir(parents=True)
        self.guide.write_text("Run the upstream entrypoint.\n", encoding="utf-8")
        self.tool = {"id":"demo", "name":"Demo", "role":"engine", "summary":"算法讲解工具",
                     "tasks":["explainer"], "outputs":["mp4"], "aliases":[], "keywords":["算法","讲解"],
                     "limits":"test", "requirements":[["python"]], "related":[], "guide":"tools/demo/GUIDE.md",
                     "source":{"repository":"example/demo", "branch":None, "adopted_commit":self.old,
                               "observed_commit":self.old, "check_error":None},
                     "review_globs":["README.md","SKILL.md","package.json"],
                     "automatic_checks":[{"argv":[sys.executable,"run.py"], "cwd":"."}],
                     "verification":{"status":"not-run", "checks":[]}}
        self.catalog = {"schema_version":1, "update_policy":"manual-commit-only", "tools":[self.tool]}
        tb.write_json(self.root / "catalog.json", self.catalog)
        self.url_patch = patch.object(tb, "url_for", return_value=self.upstream.as_uri())
        self.url_patch.start()
        self.http_patch = patch.object(tb, "urlopen", side_effect=self.local_comparison)
        self.http_patch.start()

    def tearDown(self):
        self.http_patch.stop()
        self.url_patch.stop()
        self.root_patch.stop()
        self.assertTrue(self.root.is_relative_to((REPOSITORY_ROOT / ".cache/tests").resolve()))
        self.temporary.cleanup()

    def git(self, *args):
        result = subprocess.run(["git", "-c", "user.name=Toolbox tests", "-c", "user.email=toolbox-tests@example.invalid", *args],
                                cwd=self.upstream, capture_output=True, text=True, encoding="utf-8", check=True)
        return result.stdout.strip()

    def commit(self):
        self.git("add", ".")
        self.git("commit", "-m", "Test fixture")
        return self.git("rev-parse", "HEAD")

    def change(self, filename="run.py", contents="print('new')\n"):
        path = self.upstream / filename
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(contents, encoding="utf-8")
        return self.commit()

    def local_comparison(self, request, timeout):
        before, after = request.full_url.split("/compare/", 1)[1].split("?", 1)[0].split("...")
        lines = self.git("log", "--reverse", "--format=%H%x09%s", f"{before}..{after}").splitlines()
        commits = [{"sha": line.split("\t", 1)[0], "commit": {"message": line.split("\t", 1)[1]}}
                   for line in lines]
        return io.BytesIO(json.dumps({"total_commits": len(commits), "commits": commits}).encode())

    def pending(self):
        self.tool["source"]["observed_commit"] = self.git("rev-parse", "HEAD")
        tb.write_json(self.root / "catalog.json", self.catalog)
        return tb.prepare_update(self.tool)

    def test_search_and_doctor_never_check_upstream(self):
        before = (self.root / "catalog.json").read_bytes()
        with patch.object(tb, "remote_tip", side_effect=AssertionError("Unexpected network")), \
             patch.object(tb, "urlopen", side_effect=AssertionError("Unexpected API call")):
            self.assertEqual(tb.search(self.catalog, "帮我讲解算法")[0]["id"], "demo")
            tb.doctor(self.tool)
            tb.validate(self.catalog)
        self.assertEqual(before, (self.root / "catalog.json").read_bytes())

    def test_fetch_uses_adopted_commit_without_latest_lookup(self):
        self.change()
        with patch.object(tb, "remote_tip", side_effect=AssertionError("Unexpected update check")):
            source = tb.fetch_source(self.tool, self.old)
        self.assertEqual((source / "run.py").read_text().strip(), "print('old')")

    def test_default_branch_detection_uses_actual_head(self):
        tip = tb.remote_tip(self.tool)
        self.assertEqual(tip["commit"], self.old)
        self.assertEqual(tip["resolved_branch"], "main")

    def test_check_discovers_without_adopting(self):
        candidate = self.change()
        result = tb.check_updates(self.catalog, ["demo"])
        self.assertEqual(result[0]["status"], "changed")
        self.assertEqual(self.tool["source"]["observed_commit"], candidate)
        self.assertEqual(self.tool["source"]["adopted_commit"], self.old)

    def test_check_failure_does_not_report_unchanged(self):
        with patch.object(tb, "remote_tip", side_effect=RuntimeError("offline")):
            result = tb.check_updates(self.catalog, ["demo"])
        self.assertEqual(result[0]["status"], "check-failed")
        self.assertEqual(self.tool["source"]["adopted_commit"], self.old)

    def test_compatible_code_change_is_automatically_adopted(self):
        candidate = self.change()
        result = tb.sync(self.catalog, ["demo"])
        self.assertEqual(result[0]["status"], "applied")
        self.assertEqual(self.tool["source"]["adopted_commit"], candidate)
        self.assertIn("new", self.tool["verification"]["checks"][0]["stdout"])

    def test_update_context_includes_intermediate_commits_and_text_diff(self):
        middle = self.change()
        latest = self.change("README.md", "Different installation\n")
        state = self.pending()
        self.assertEqual([row["commit"] for row in state["commits"]], [middle, latest])
        diff = tb.inside(self.root, state["diff_path"]).read_text(encoding="utf-8")
        self.assertIn("+Different installation", diff)
        self.assertIn("+print('new')", diff)
        self.assertEqual(self.tool["source"]["adopted_commit"], self.old)

    def test_upstream_commit_listing_reads_all_pages(self):
        entries = [{"sha": f"{number:040x}", "commit": {"message": f"Change {number}\nDetails"}}
                   for number in range(1, 102)]
        pages = [io.BytesIO(json.dumps({"total_commits": 101, "commits": batch}).encode())
                 for batch in (entries[:100], entries[100:])]
        with patch.object(tb, "urlopen", side_effect=pages) as fetch:
            commits = tb.upstream_commits(self.tool, self.old, "f" * 40)
        self.assertEqual(len(commits), 101)
        self.assertEqual(commits[-1], {"commit": entries[-1]["sha"], "subject": "Change 101"})
        self.assertIn("per_page=100&page=2", fetch.call_args.args[0].full_url)

    def test_incomplete_or_invalid_commit_responses_are_rejected(self):
        entry = {"sha": "e" * 40, "commit": {"message": "Change"}}
        cases = [{"total_commits": 1, "commits": []},
                 {"total_commits": 2, "commits": [entry, entry]},
                 {"total_commits": 1, "commits": [{"sha": "e" * 40, "commit": None}]}]
        for data in cases:
            with self.subTest(data=data), patch.object(tb, "urlopen", return_value=io.BytesIO(json.dumps(data).encode())):
                with self.assertRaises(ValueError):
                    tb.upstream_commits(self.tool, self.old, "f" * 40)

    def test_comparison_failure_preserves_adopted_version(self):
        candidate = self.change()
        with patch.object(tb, "urlopen", side_effect=OSError("comparison unavailable")):
            result = tb.sync(self.catalog, ["demo"])
        self.assertEqual(result[0]["status"], "prepare-failed")
        self.assertEqual(self.tool["source"]["adopted_commit"], self.old)
        self.assertEqual(self.tool["source"]["observed_commit"], candidate)

    def test_failed_execution_preserves_old_version_and_pending_candidate(self):
        candidate = self.change(contents="raise SystemExit(3)\n")
        result = tb.sync(self.catalog, ["demo"])
        self.assertEqual(result[0]["status"], "needs-ai")
        self.assertEqual(self.tool["source"]["adopted_commit"], self.old)
        self.assertEqual(self.tool["source"]["observed_commit"], candidate)
        self.assertEqual(tb.read_json(tb.state_path("demo"))["receipt"]["checks"][0]["returncode"], 3)

    def test_usage_change_requires_review_even_with_passing_call(self):
        self.change("README.md", "Different installation\n")
        state = self.pending()
        state = tb.verify(self.tool, state, self.tool["automatic_checks"])
        with self.assertRaisesRegex(ValueError, "require AI review"):
            tb.apply_update(self.catalog, self.tool, state)
        state = tb.verify(self.tool, state, self.tool["automatic_checks"], reviewed=True)
        self.assertEqual(tb.apply_update(self.catalog, self.tool, state)["status"], "applied")

    def test_guide_change_invalidates_successful_receipt(self):
        self.change()
        state = tb.verify(self.tool, self.pending(), self.tool["automatic_checks"])
        self.guide.write_text("Changed after checking", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "changed after verification"):
            tb.apply_update(self.catalog, self.tool, state)
        self.assertEqual(self.tool["source"]["adopted_commit"], self.old)

    def test_no_execution_check_requires_ai(self):
        self.change()
        self.tool["automatic_checks"] = []
        result = tb.sync(self.catalog, ["demo"])
        self.assertEqual(result[0]["status"], "needs-ai")
        self.assertEqual(self.tool["source"]["adopted_commit"], self.old)

    def test_directory_updates_without_executing_upstream(self):
        candidate = self.change("README.md", "New resource list\n")
        self.tool.update(role="directory", outputs=["discovery"], automatic_checks=[])
        with patch.object(tb, "verify", side_effect=AssertionError("Directory should not execute")):
            result = tb.sync(self.catalog, ["demo"])
        self.assertEqual(result[0]["status"], "applied")
        self.assertEqual(self.tool["source"]["adopted_commit"], candidate)

    def test_paths_and_duplicate_entries_are_rejected(self):
        with self.assertRaises(ValueError):
            tb.inside(self.root, "../outside")
        self.catalog["tools"].append(copy.deepcopy(self.tool))
        with self.assertRaisesRegex(ValueError, "duplicate"):
            tb.validate(self.catalog)

    def test_cached_user_edits_are_never_overwritten(self):
        source = tb.fetch_source(self.tool, self.old)
        (source / "run.py").write_text("print('keep me')", encoding="utf-8")
        with self.assertRaisesRegex(RuntimeError, "has edits"):
            tb.fetch_source(self.tool, self.old)
        self.assertEqual((source / "run.py").read_text(), "print('keep me')")

    def test_cached_wrong_head_is_not_reset(self):
        source = tb.fetch_source(self.tool, self.old)
        candidate = self.change()
        tb.git("fetch", "origin", candidate, cwd=source)
        tb.git("checkout", "--detach", candidate, cwd=source)
        with self.assertRaisesRegex(RuntimeError, "refusing to overwrite"):
            tb.fetch_source(self.tool, self.old)
        self.assertEqual(tb.git("rev-parse", "HEAD", cwd=source).strip(), candidate)

    def test_verify_cli_accepts_options_after_id(self):
        self.change("README.md", "New usage\n")
        self.pending()
        argv = ["toolbox.py", "verify", "demo", "--cwd", ".", "--reviewed", "--register", "--", sys.executable, "run.py"]
        with patch.object(sys, "argv", argv), contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(tb.main(), 0)
        self.assertTrue(tb.read_json(tb.state_path("demo"))["receipt"]["reviewed"])
        self.assertEqual(tb.load_catalog()["tools"][0]["automatic_checks"][0]["argv"], [sys.executable,"run.py"])

    def test_stale_candidate_is_rejected(self):
        self.change()
        self.pending()
        self.tool["source"]["observed_commit"] = "f" * 40
        with self.assertRaisesRegex(ValueError, "different upstream"):
            tb.load_pending(self.tool)

    def test_first_use_can_verify_current_version_without_update_check(self):
        with patch.object(tb, "remote_tip", side_effect=AssertionError("Unexpected update check")):
            state = tb.load_pending(self.tool, allow_current=True)
            state = tb.verify(self.tool, state, self.tool["automatic_checks"])
            result = tb.apply_update(self.catalog, self.tool, state)
        self.assertEqual(result["adopted_commit"], self.old)
        self.assertEqual(result["verification"], "command-passed")

    def test_directory_cannot_claim_video_output(self):
        self.tool["role"] = "directory"
        with self.assertRaisesRegex(ValueError, "Directories"):
            tb.validate(self.catalog)

    def test_shell_strings_cannot_be_execution_checks(self):
        self.tool["automatic_checks"] = [{"argv":"python run.py; echo wrong"}]
        with self.assertRaisesRegex(ValueError, "string array"):
            tb.validate(self.catalog)

    def test_documentation_change_does_not_skip_execution_verification(self):
        self.change("notes.md", "Some documentation can be runtime input\n")
        self.tool["automatic_checks"] = []
        self.assertEqual(tb.sync(self.catalog, ["demo"])[0]["status"], "needs-ai")
        self.assertEqual(self.tool["source"]["adopted_commit"], self.old)

    def test_current_version_can_be_rechecked_after_an_applied_update(self):
        self.change()
        tb.sync(self.catalog, ["demo"])
        state = tb.load_pending(self.tool, allow_current=True)
        self.assertEqual(state["candidate_commit"], self.tool["source"]["adopted_commit"])
        self.assertEqual(state["base_commit"], state["candidate_commit"])

    def test_atomic_save_preserves_previous_catalog_on_failure(self):
        path = self.root / "catalog.json"
        previous = path.read_bytes()
        with patch.object(tb.os, "replace", side_effect=OSError("disk failure")):
            with self.assertRaises(OSError):
                tb.write_json(path, {"broken":True})
        self.assertEqual(path.read_bytes(), previous)

    def test_commit_uses_bot_fallback_without_configuration_changes(self):
        tb.git("init", "-b", "main", cwd=self.root)
        (self.root / "personal.txt").write_text("unrelated work", encoding="utf-8")
        with patch.dict(os.environ, {"GIT_CONFIG_GLOBAL":os.devnull,"GIT_CONFIG_SYSTEM":os.devnull}):
            result = tb.commit_updates()
            self.assertEqual(result["status"], "committed")
            self.assertFalse(result["pushed"])
            self.assertEqual(tb.run(["git","config","--local","--get","user.name"],cwd=self.root).returncode, 1)
        files = tb.git("show", "--pretty=", "--name-only", "HEAD", cwd=self.root)
        self.assertIn("catalog.json", files)
        self.assertNotIn("personal.txt", files)

    def test_commit_preserves_preexisting_staged_work(self):
        tb.git("init", "-b", "main", cwd=self.root)
        (self.root / "personal.txt").write_text("keep staged", encoding="utf-8")
        tb.git("add", "personal.txt", cwd=self.root)
        with self.assertRaisesRegex(ValueError, "Existing staged"):
            tb.commit_updates()
        self.assertEqual(tb.git("diff","--cached","--name-only",cwd=self.root).strip(), "personal.txt")


if __name__ == "__main__":
    unittest.main()
