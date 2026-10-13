---
name: animation-toolbox
description: 根据需求选择工具并制作产品宣传、知识讲解、动效或交互视觉。用于比较动画路线、生成视频或网页动画，以及维护动画工具目录。仅在用户主动要求时检查或同步上游版本。
license: MIT
---

# Animation Toolbox

这是工具选用与运行入口。只按当前需求读取相关项目，不通读所有工具资料。

## 定位技能和任务目录

将本 SKILL.md 所在目录的绝对路径记为 TOOLBOX_DIR；catalog.json、scripts/、tools/、references/ 和 AGENTS.md 都相对于此目录。先读本目录的 [AGENTS.md](AGENTS.md)。

用户正在制作内容的项目是任务目录，可能与技能目录不同。通过脚本的绝对路径调用工具箱，保留用户项目作为工作目录。下方 TOOLBOX_DIR 占位符需替换为实际路径；GUIDE 中从“本库根目录”执行的工具箱命令也按此方式定位。

## 调用入口

```text
python "<TOOLBOX_DIR>/scripts/toolbox.py" search "讲解神经网络" --output mp4
python "<TOOLBOX_DIR>/scripts/toolbox.py" show manim
python "<TOOLBOX_DIR>/scripts/toolbox.py" doctor manim
python "<TOOLBOX_DIR>/scripts/toolbox.py" fetch manim
```

工具箱需要 Python 3.10+ 与 Git。Python 命令在部分系统中为 python3；具体制作工具的环境按需补齐。

## 检索和使用

1. 用 `search "需求"` 挑选路线。可用 `--role`、`--task`、`--output` 筛选；用 `list` 看职责分类。简短说明选用理由后继续制作。
2. 用 `show <id>` 读取候选的用途、限制、环境要求、关联工具和绝对 GUIDE 路径。directory 只用于发现；workbench 可能需要另一个 AI CLI；library 本身通常没有 MP4 导出功能。
3. 明确用户要视频还是可交互网页。优先选适用且有运行证据的工具，未知的能力不能当作已支持。多个路线按表达差异选择，不把同一流程的依赖当成独立方案。Frontend Design、edge-tts 和 fix-webm-duration 是设计、配音、录屏修复辅助入口，按需配合制作工具使用。
4. 运行 `doctor <id>` 检查本机命令，再读该工具 GUIDE。`fetch <id>` 将已采用 commit 的源码放在技能目录的 .cache 中；需要编辑或安装依赖时复制到用户任务目录，保留来源。安装位置只读时，先将完整工具箱复制到任务内的可写目录再调用。
5. 按 GUIDE 使用上游的原生命令，依赖局部安装。任务工程、素材和成品放在用户项目或其指定位置。需要配音时先生成音频并测量时长，再安排动画；检查实际输出后交付成品路径、可编辑源码与复现方法，并说明未验证环节。

## 用户主动要求更新时

读 [references/updates.md](references/updates.md)。安装副本通常不含 .git；需要维护和提交目录时，在独立的本库 Git 检出中执行，保留用户业务项目的 Git 状态。`sync` 自动完成版本发现、差异准备和可执行检查；遇到 `needs-ai` 时，只读取对应变更文件和 GUIDE，处理具体适配并继续验证、采用。不要停在转交清单而不继续已授权工作。

索引字段与状态见 [references/catalog.md](references/catalog.md)。本库没有效果配方或案例积累流程。
