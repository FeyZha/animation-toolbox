# Motion Studio 使用入口

版本、角色、依赖与验证状态以 [catalog.json](../../catalog.json) 的 `motion-studio` 为准。

在本库根目录先执行：

```text
python scripts/toolbox.py show motion-studio
python scripts/toolbox.py doctor motion-studio
python scripts/toolbox.py fetch motion-studio
```

fetch 仅获取已采用 commit，不检查最新版本。要编辑或安装依赖时，复制固定源码到 work/ 或用户指定任务目录，保留来源。下面的原生命令在所述任务目录执行；Python/Node 依赖局部安装，不修改全局技能目录。

读取固定源码根目录 `SKILL.md`，然后只加载本任务需要的 `references/`。按“需求 → 分镜 → 资产 → 场景代码 → 渲染 → 检查输出”工作；默认 Remotion 路线的安装和导出见本库 Remotion GUIDE。

这是工作流技能，不是独立渲染器。仓库 `creative/` 中附带 p5js、manim-video、ascii-video、excalidraw、popular-web-designs 五个可选技能，按需读取，不作为五个独立 GitHub 项目重复计数或全部安装。

本库使用已固定的本地资料：不执行 `scripts/sync.sh pull/capture/log/stats/update`，不配置 capture hook 或社区服务器。上游这些命令可能自动更新技能或回传修改；用户明确要求对应操作时另行处理，不让普通制作触发更新。

在任务目录创建动画工程，按实际渲染引擎的原生命令生成 MP4，再核对画面、声音和时长。固定版本 README 声明 MIT，并提及附带技能的独立来源说明；复用子技能时也应保留相关说明。

上游：[官方仓库](https://github.com/Altrym/motion-studio)。`show` 输出固定源码和许可链接；使用时读取该 commit 的资料。本次核对了入口文档与相关源码，尚未在本库运行完整制作流程；验证状态保持 `not-run`。
