# Anthropic Frontend Design 使用入口

版本、角色、依赖与验证状态以 [catalog.json](../../catalog.json) 的 `frontend-design` 为准。

在本库根目录先执行：

```text
python scripts/toolbox.py show frontend-design
python scripts/toolbox.py doctor frontend-design
python scripts/toolbox.py fetch frontend-design
```

fetch 仅获取已采用 commit，不检查最新版本。要编辑或安装依赖时，复制固定源码到 work/ 或用户指定任务目录，保留来源。下面的原生命令在所述任务目录执行；Python/Node 依赖局部安装，不修改全局技能目录。

本档案只对应 `anthropics/skills` 仓库中的 `skills/frontend-design/SKILL.md`，不代表安装或收录整个 Anthropic 技能集合。

直接阅读该固定文件，按主题和使用场景明确视觉方向、字体、配色、版式，再在用户的网页工程中实施。所需 Node、浏览器或前端框架由实际工程决定，本技能没有统一构建命令。

这是辅助设计入口，可以与网页动画或视频流程配合使用；自身不生成 MP4、旁白或字幕。需要视频时仍须选择渲染工具。

许可读取同目录的 `LICENSE.txt`，该固定版本为 Apache-2.0；不能套用本库的 MIT 许可。

上游：[官方仓库](https://github.com/anthropics/skills)。`show` 输出固定源码和许可链接；使用时读取该 commit 的资料。本次核对了入口文档与相关源码，尚未在本库运行完整制作流程；验证状态保持 `not-run`。
