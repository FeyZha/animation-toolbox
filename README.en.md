# Animation Toolbox

[简体中文](README.md) · [Agent entrypoint](SKILL.md) · [Contributing](CONTRIBUTING.md)

An agent-readable catalog of 21 animation, video, and creative coding tools. Find a suitable tool, read its guide, fetch a pinned commit, and use the upstream workflow.

The catalog separates workflows, workbenches, rendering engines, graphics libraries, and discovery directories. It preserves each project's native commands and distinguishes documented capabilities from commands actually verified. Detailed tool guides are currently in Chinese; agents can translate the selected guide as needed.

## Get started

Requires Python 3.10+ and Git. The toolbox itself has no third-party Python dependencies.

```text
git clone https://github.com/FeyZha/animation-toolbox.git
cd animation-toolbox
python scripts/toolbox.py validate
python scripts/toolbox.py list
python scripts/toolbox.py search "" --task explainer --output mp4
python scripts/toolbox.py show xm
python scripts/toolbox.py doctor xm
python scripts/toolbox.py fetch xm
```

Use `python3` if that is your system's Python command. Give an agent the repository URL and ask:

> Read SKILL.md, select a suitable tool for my request, check its environment, and follow its GUIDE. Do not check or update upstream versions unless I explicitly request it.

`fetch` downloads only the adopted commit into `.cache/sources/<id>/<commit>`. It does not look up the latest version. Install tool-specific dependencies locally when needed; put editable task projects in `work/` or a separate directory. Discovery directories cannot produce animations themselves. Browser libraries do not automatically provide native MP4 export.

## Manual upstream updates

Run these commands only when the user explicitly asks to check or synchronize updates:

```text
python scripts/toolbox.py check-updates --all
python scripts/toolbox.py sync --id xm --commit
```

The observed and adopted commits are tracked separately. Scripts prepare commit summaries and file diffs, then run registered checks. Compatible updates can be adopted automatically; entrypoint changes, missing checks, or failures require targeted agent adaptation. Failed updates preserve the adopted version. Local commits never automatically push to GitHub.

There are no scheduled update jobs and no update checks during ordinary tool selection or use. See [the update workflow](references/updates.md) and [catalog fields](references/catalog.md).

## Validate and contribute

```text
python scripts/toolbox.py validate
python -m unittest discover -s tests -v
```

Tests use temporary local Git repositories and mocked API responses. CI checks Windows and Linux with Python 3.10 and 3.14; it does not query upstream projects or run their production workflows. A successful toolbox test is not evidence that every third-party tool has been fully exercised.

See [CONTRIBUTING.md](CONTRIBUTING.md), [the code of conduct](CODE_OF_CONDUCT.md), [security reporting](SECURITY.md), and [the changelog](CHANGELOG.md).

## License and sources

Original toolbox code and documentation are [MIT licensed](LICENSE). Upstream projects retain their own licenses; see [third-party notices](THIRD_PARTY_NOTICES.md). The repository contains catalog metadata, guides, and maintenance scripts. It does not vendor upstream source code, credentials, rendered media, or local caches.
