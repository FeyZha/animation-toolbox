# XM Video Engine 使用入口

版本、角色、依赖与验证状态以 [catalog.json](../../catalog.json) 的 `xm` 为准。

在本库根目录先执行：

```text
python scripts/toolbox.py show xm
python scripts/toolbox.py doctor xm
python scripts/toolbox.py fetch xm
```

fetch 仅获取已采用 commit，不检查最新版本。使用输出目录中的上游文件；要写任务工程时复制到 work/ 或用户指定目录。以下命令工作目录是该固定源码/任务目录，不是本库根目录。

固定源码中的 app/ 是原生工程；需要 Bun、Chrome/Edge 和 FFmpeg。基线自带合成测试音频，不必先装音频分析大模型。

在 app/ 中执行：
```text
bun install
bunx vite
bun scripts/render-par.ts --from 0 --to 16 --samples 1 --out ../out/demo.mp4
```

先阅读 CLAUDE.md、docs/使用指南.md，写场景时再查 docs/引擎指南.md。场景在 app/src/scenes/，时间线在 app/src/timeline.ts，尺寸与音频设置在 app/src/config.ts。要创建独立工程，可先读 tools/new_project.py --help 再执行该上游脚本。

现成视觉练习可在预览 URL 传 ?ref=boot 等；导出使用 --query ref=boot 并指定场景真实时长。ref 练习不代表任意歌曲自动卡点。完成后使用上游 tools/check_video.py --help 获取本版本检查参数。只在用户确实提供新歌曲并要求分析时安装 analysis/ 所需模型。

上游：[官方仓库](https://github.com/xiaoming6680/xm-video-engine)。`show` 输出当前固定源码链接；使用时优先读该 commit 的资料。上面的调用形态用于指引，未通过本库执行检查的部分不标为已验证。
