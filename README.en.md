# Animation Toolbox

[简体中文](README.md) · [Agent entrypoint](SKILL.md) · [Contributing](CONTRIBUTING.md)

An agent-readable collection with 36 catalog entries: 28 animation production projects, 5 discovery directories, and 3 supporting tools. Each entry points to a different GitHub repository. Find a suitable tool, read its guide, fetch a pinned commit, and use the upstream workflow.

The catalog separates workflows, workbenches, rendering engines, graphics libraries, and discovery directories. It preserves each project's native commands and distinguishes documented capabilities from commands actually verified. Detailed tool guides are currently in Chinese; agents can translate the selected guide as needed.

ManimGL and Manim Community have separate entries, as do the iart hub and its Motion Design Skills pack. Supporting tools cover frontend design, speech/subtitles, and WebM duration repair; they are not standalone video production routes. The Anthropic entry covers only its frontend-design skill, and bundled subskills are not counted as separate repositories. See [the full catalog table](README.md#分类与收录范围).

## Install as a skill (recommended)

Run this from the project where you want to create animations. The installer requires Node.js / npx and Git:

```text
npx skills add FeyZha/animation-toolbox --skill animation-toolbox
```

Choose your assistant when prompted, or append `--agent codex`, `--agent claude-code`, or `--agent cursor` to target one. Installation is project-scoped by default. It installs one entrypoint with the complete catalog; production dependencies are installed only when needed.

In assistants that support `$skill-name`, invoke it directly:

```text
$animation-toolbox Make a 30-second narrated MP4 explaining neural-network forward propagation.
```

Other assistants can use a natural-language request such as “Use animation-toolbox to create…”. Start a new session if the current one has not discovered the skill. Running the toolbox requires Python 3.10+ and Git. The skill includes catalog, scripts, tool guides, and references; task projects and output belong in your project.

Installation uses the [Skills CLI](https://github.com/vercel-labs/skills). The root SKILL.md is the standard skill entrypoint.

## Copy this prompt to your AI assistant

If you have not installed the skill, use an assistant that can read files and run commands. Copy the entire prompt and replace the final request. A chat-only assistant can help select tools; production needs a local execution environment.

```text
Use https://github.com/FeyZha/animation-toolbox to complete the animation task below.

1. Reuse animation-toolbox if it already exists in the workspace; otherwise clone it into a separate directory. Read SKILL.md and AGENTS.md, then search catalog.json.
2. Choose one suitable production route and briefly explain why. Distinguish production tools, discovery directories, and supporting tools. Read only the selected tool guides and necessary dependency guides.
3. Check the environment, fetch the adopted_commit pinned in the catalog, install dependencies locally in the task workspace, and produce the result using the GUIDE and native upstream commands.
4. For narration, generate audio and measure its real duration before timing animations. Check visuals, audio, duration, and output files before delivery; state any unverified steps.
5. Complete a playable or interactive result and provide its file path, editable source, and reproduction instructions.
6. Do not check or upgrade upstream versions unless I explicitly ask. Do not install skills globally or install every tool.

My request: Make an approximately 30-second narrated MP4 explaining neural-network forward propagation with simple animation.
```

Other requests you can use:

- **Product video:** Create a 15-second MP4 showcasing three key features of my app, using the product materials I provide.
- **Explainer:** Explain the vector dot product in a 3Blue1Brown-inspired animation, around 45 seconds, with narration, exported to MP4.
- **Interactive art:** Build a particle flow field that responds to the mouse and deliver a browser-viewable page.
- **Compare results:** Use two visually different production routes to make an approximately 8-second sample of the same topic with each, then explain the differences.

## Manual quick start

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

Use `python3` if that is your system's Python command.

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

MathLens declares CC BY-NC 4.0, which restricts commercial use. The pinned OmniManim and Manimator sources do not provide clear license grants. Catalog inclusion does not grant permission to redistribute or commercially use upstream content.
