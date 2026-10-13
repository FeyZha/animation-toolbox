# iart Motion Design Skills 使用入口

版本、角色、依赖与验证状态以 [catalog.json](../../catalog.json) 的 `iart-motion-design` 为准。

在本库根目录先执行：

```text
python scripts/toolbox.py show iart-motion-design
python scripts/toolbox.py doctor iart-motion-design
python scripts/toolbox.py fetch iart-motion-design
```

fetch 仅获取已采用 commit，不检查最新版本。要编辑或安装依赖时，复制固定源码到 work/ 或用户指定任务目录，保留来源。下面的原生命令在所述任务目录执行；Python/Node 依赖局部安装，不修改全局技能目录。

本档案对应具体仓库 `iart-ai/motion-design-skills`；已有 `iart-motion-skills` 是技能集合总入口。两者的 commit 独立记录，不能用总入口的版本代表子包版本。

先看固定源码 README 的技能清单，再按需求读取一个或少数入口：
- `skills/motion-art-direction/SKILL.md`：整体动效语言、层次与节奏。
- `skills/animation-principles/SKILL.md`、`skills/shot-composition/SKILL.md`、`skills/color-motion/SKILL.md`：运动、构图与色彩。
- `skills/remotion-video/SKILL.md`：Remotion 制作与导出。

其余技能包含 After Effects、节拍剪辑、logo 和动态背景。子技能均位于同一固定仓库，本库不逐个重复计为 GitHub 项目，也不默认全量安装。

设计指导本身没有统一渲染命令。选定 Remotion、网页或 After Effects 后，再检查对应环境与实际输出；不要只读取指导文件就标记视频制作通过。

上游：[官方仓库](https://github.com/iart-ai/motion-design-skills)。`show` 输出固定源码和许可链接；使用时读取该 commit 的资料。本次核对了入口文档与相关源码，尚未在本库运行完整制作流程；验证状态保持 `not-run`。
