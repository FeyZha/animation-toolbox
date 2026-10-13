# Sources and third-party licenses / 来源与第三方许可

This repository's MIT license covers its original catalog, guides, tests, and maintenance scripts. It does not relicense the tools referenced by the catalog or any code, fonts, music, images, models, or other assets fetched while using them.

`catalog.json` records each tool's upstream repository, pinned commit, and license reference. Read the upstream license and any asset-specific notices at that commit before reusing or distributing its contents. Local upstream checkouts are excluded from this repository under `.cache/`.

The toolbox's selection and documentation approach draws on these public resources:

- [Copilot Video Gen Plugin](https://github.com/abhi-singhs/copilot-video-gen-plugin): separate registry, tool selection, and per-tool usage guides.
- [Agent Skills specification](https://agentskills.io/specification): progressively load an entrypoint and only the relevant supporting references.
- [Git documentation](https://git-scm.com/docs) and [GitHub REST documentation](https://docs.github.com/en/rest): native commit queries, file comparisons, and paginated commit summaries.

本仓库没有把上游项目打包或重新授权。第三方项目及其素材继续适用各自许可；工具的来源、固定版本和许可入口以 `catalog.json` 为准。
