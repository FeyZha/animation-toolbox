# Remotion 使用入口

版本、角色、依赖与验证状态以 [catalog.json](../../catalog.json) 的 `remotion` 为准。

在本库根目录先执行：

```text
python scripts/toolbox.py show remotion
python scripts/toolbox.py doctor remotion
python scripts/toolbox.py fetch remotion
```

fetch 仅获取已采用 commit，不检查最新版本。使用输出目录中的上游文件；要写任务工程时复制到 work/ 或用户指定目录。以下命令工作目录是该固定源码/任务目录，不是本库根目录。

视频工程使用 React 与帧驱动动画。固定源码是工具单仓，不把它直接当视频模板，也不直接执行 create-video@latest。

在任务工程使用已确认对应的 Remotion 包版本；如固定 commit 未发布，按源码的开发说明构建并链接相应 packages。视频工程常用 CLI：
```text
remotion studio
remotion render src/index.tsx CompositionId out/video.mp4
```

入口需注册 Composition，明确 fps、durationInFrames、width、height；场景从 useCurrentFrame 取时间。依赖包保持同一 Remotion 版本。先渲染一帧再导出；当前许可说明读上游对应版本文件，不替用户作商业许可保证。

上游：[官方仓库](https://github.com/remotion-dev/remotion)。`show` 输出当前固定源码链接；使用时优先读该 commit 的资料。上面的调用形态用于指引，未通过本库执行检查的部分不标为已验证。
