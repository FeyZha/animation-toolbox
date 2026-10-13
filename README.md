# Animation Toolbox

[English](README.en.md) · [AI 使用入口](SKILL.md) · [贡献指南](CONTRIBUTING.md)

[![Tests](https://github.com/FeyZha/animation-toolbox/actions/workflows/tests.yml/badge.svg)](https://github.com/FeyZha/animation-toolbox/actions/workflows/tests.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

给 AI 使用的动画工具目录：按需求找到工具，读取对应使用说明，获取固定 commit 的源码，再按上游方法执行。

**AI 从 [SKILL.md](SKILL.md) 开始。** 工作边界见 [AGENTS.md](AGENTS.md)，工具事实与版本状态以 [catalog.json](catalog.json) 为准。

核心脚本只需要 **Python 3.10+ 与 Git**。具体工具的 Node、Bun、FFmpeg、浏览器等环境按需补齐；本库不会一次安装所有工具，也不全局安装技能。

## 快速开始

```text
git clone https://github.com/FeyZha/animation-toolbox.git
cd animation-toolbox
python scripts/toolbox.py validate
python scripts/toolbox.py search "讲解神经网络" --output mp4
```

把这个仓库链接交给 AI，并告诉它：

> 先读 animation-toolbox 的 SKILL.md，根据我的需求选择工具，检查环境，再按对应 GUIDE 制作。除非我明确要求，否则不要检查或更新上游版本。

Python 命令在部分系统上是 `python3`。此仓库可直接克隆使用，无须安装 Python 包或全局技能。首次获取具体工具源码需要联网；检索和本库测试可离线执行。

## 查找与使用

在本库根目录执行：

```text
python scripts/toolbox.py list
python scripts/toolbox.py search "讲解神经网络" --output mp4
python scripts/toolbox.py search "字符音乐"
python scripts/toolbox.py search "" --role library --task interactive
python scripts/toolbox.py show xm
python scripts/toolbox.py doctor xm
python scripts/toolbox.py fetch xm
```

`show` 给出完整档案、GUIDE 路径与固定源码链接；`doctor` 只检查本机命令可用性；`fetch` 只获取已采用 commit，**不查询最新版本**。下载的源码在 `.cache/sources/<id>/<commit>`；任务工程写到 `work/` 或用户指定目录。

浏览器/包依赖是否齐全、工具是否能完成本次具体任务，继续按对应 GUIDE 检查。角色为 directory 的条目用于发现其他项目，不执行制作。library 原生网页输出不等于原生视频输出。

## 分类与收录范围

| 职责 | 工具入口 |
|---|---|
| 选用工作台 | [Copilot Video Gen](tools/copilot-video-gen/GUIDE.md)、[Motion Anything](tools/motion-anything/GUIDE.md) |
| 制作流程 | [归藏](tools/guizang/GUIDE.md)、[Claude Motion](tools/claude-motion/GUIDE.md)、[iart Motion Skills](tools/iart-motion-skills/GUIDE.md) |
| 动画与视频工程 | [XM](tools/xm/GUIDE.md)、[Motion Canvas](tools/motion-canvas/GUIDE.md)、[HyperFrames](tools/hyperframes/GUIDE.md)、[Remotion](tools/remotion/GUIDE.md)、[Manim](tools/manim/GUIDE.md) |
| 基础画面库 | [p5.js](tools/p5/GUIDE.md)、[Hydra](tools/hydra/GUIDE.md)、[Three.js](tools/three/GUIDE.md)、[GSAP](tools/gsap/GUIDE.md)、[Motion / Framer Motion](tools/motion/GUIDE.md)、[Theatre.js](tools/theatre/GUIDE.md) |
| 资源发现 | [AI 视频技能](tools/awesome-video-skills/GUIDE.md)、[Creative Agentic Coding](tools/awesome-creative-agentic/GUIDE.md)、[Creative Coding](tools/awesome-creative-coding/GUIDE.md)、[Creative Intelligence](tools/awesome-creative-intelligence/GUIDE.md)、[Generative Art](tools/awesome-generative-art/GUIDE.md) |

共 21 项。集合的下游资源保留为发现入口，不自动展开或全部安装。用途筛选值为 `product`、`explainer`、`music`、`data`、`interactive`、`generative`；输出筛选使用目录中的 `mp4`、`html`、`gif`、`svg`、`lottie`、`discovery`。

## 只有用户主动要求才更新

没有定时检查、后台服务、自动运行的更新工作流或使用前检查。初始化记录 commit 不代表开启监控。

```text
# 只发现上游 commit 变化，不切换采用版本
python scripts/toolbox.py check-updates --all

# 机械同步可处理的更新，并创建本地提交
python scripts/toolbox.py sync --all --commit

# 只处理一个工具
python scripts/toolbox.py sync --id xm --commit
```

更新通过 Git 查询上游指定分支，未指定时跟随默认分支；不按 release、star、issue 或仓库更新时间判断。`observed_commit` 与 `adopted_commit` 分开保存。

脚本准备完整文件差异，运行已经登记的最小调用，检查成功后更新入口版本。涉及使用说明/接口资料的变化，或检查失败、尚无执行检查时，输出对应工具的 `needs-ai` 记录；AI 只处理该工具所需适配。详细步骤见 [手动更新说明](references/updates.md)。网络失败记作检查失败，其他工具继续处理，旧采用版本保留。

`sync --commit` 只创建本地 Git 提交；AI 完成待适配项后用 `commit-updates` 提交剩余改动。已有暂存内容时拒绝夹带提交；不自动 push 或发布。

## 验证范围

```text
python scripts/toolbox.py validate
python -m unittest discover -s tests -v
```

本库测试使用局部临时 Git 仓库，覆盖固定版本获取、手动更新、自动采用、失败保留、AI 适配、检查记录失效和路径边界，不查询上游更新。

工具的 `verification` 仅表示记录中那条真实命令的结果。归藏的工具脚本自检、Copilot 的选择器调用等，都不能扩大成整条视频制作流程已通过验证；其他未运行工具标为 `not-run`。

GitHub Actions 在提交和拉取请求中检查目录及本库测试，覆盖 Windows / Linux 和 Python 3.10 / 3.14。它不查询上游 commit、不运行第三方制作工具，也不包含定时任务。

## 维护边界

本库维护索引、使用入口和必要脚本；第三方源码按固定 commit 下载到被忽略的缓存，来源及许可证链接保留在目录。能力描述和调用方式需要适配时才由 AI 修改。

不建设效果配方库、样片积累或审美评价。没有付费模型调用代码；AI 适配由使用本库的当前会话完成。

参考做法：[Copilot Video Gen](https://github.com/abhi-singhs/copilot-video-gen-plugin) 的目录与路由分离、[Agent Skills](https://agentskills.io/specification) 的按需阅读，以及 Git 原生的 [ls-remote](https://git-scm.com/docs/git-ls-remote) / [diff](https://git-scm.com/docs/git-diff)。本场景只做手动 commit 同步，因此没有引入常驻更新机器人。

## 参与和许可

新增工具或修正入口请按 [贡献指南](CONTRIBUTING.md) 提交；问题与建议使用 [Issues](https://github.com/FeyZha/animation-toolbox/issues)。社区约定见 [行为准则](CODE_OF_CONDUCT.md)，漏洞报告见 [安全政策](SECURITY.md)，版本变化见 [更新记录](CHANGELOG.md)。

本库原创代码与文档使用 [MIT 许可](LICENSE)。第三方项目各自保留其许可，详见 [来源与许可说明](THIRD_PARTY_NOTICES.md)；缓存、第三方源码、凭据和任务成果均不包含在发布内容中。
