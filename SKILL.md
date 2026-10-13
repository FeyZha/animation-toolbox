---
name: animation-toolbox
description: 从分类目录检索并使用动画、视频、创意编码工具；仅在用户主动要求时检查和同步上游 commit。用于挑选动画工具、比较工具路线、按现有工具制作内容或维护此工具目录。
---

# Animation Toolbox

这是工具选用与运行入口。只按当前需求读取相关项目，不通读所有工具资料。

## 检索和使用

1. 在仓库根目录运行 `python scripts/toolbox.py search "需求"`。可用 `--role`、`--task`、`--output` 筛选；用 `list` 看职责分类。
2. 用 `show <id>` 读取候选的用途、限制、环境要求、关联工具和 GUIDE 路径。directory 只用于发现；workbench 可能需要另一个 AI CLI；library 本身通常没有 MP4 导出功能。
3. 明确用户要视频还是可交互网页。优先选适用且有运行证据的工具，未知的能力不能当作已支持。多个路线按表达差异选择，不把同一流程的依赖当成独立方案。Frontend Design、edge-tts 和 fix-webm-duration 是设计、配音、录屏修复辅助入口，按需配合制作工具使用。
4. 运行 `doctor <id>` 检查本机命令，再读该工具 GUIDE。`fetch <id>` 获取已采用 commit 的独立源码；需要改写时复制到任务目录，保留来源。不要切换到远端最新版本。
5. 按 GUIDE 使用上游的原生命令，局部补依赖，完成用户的成果并核对实际输出。缺环境不等于工具本身失败。

## 用户主动要求更新时

读 [references/updates.md](references/updates.md)。`sync` 自动完成版本发现、差异准备和可执行检查；遇到 `needs-ai` 时，只读取对应变更文件和 GUIDE，处理具体适配并继续验证、采用。不要停在转交清单而不继续已授权工作。

索引字段与状态见 [references/catalog.md](references/catalog.md)。本库没有效果配方或案例积累流程。
