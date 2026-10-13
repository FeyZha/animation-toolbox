# Motion Canvas 使用入口

版本、角色、依赖与验证状态以 [catalog.json](../../catalog.json) 的 `motion-canvas` 为准。

在本库根目录先执行：

```text
python scripts/toolbox.py show motion-canvas
python scripts/toolbox.py doctor motion-canvas
python scripts/toolbox.py fetch motion-canvas
```

fetch 仅获取已采用 commit，不检查最新版本。使用输出目录中的上游文件；要写任务工程时复制到 work/ 或用户指定目录。以下命令工作目录是该固定源码/任务目录，不是本库根目录。

先读固定源码 README 的 Using / Developing 区分：本库获取的是工具源码，不是用户视频工程。

使用固定源码自带模板预览：
```text
npm install
npx lerna run build
npm run template:dev
```

独立创作工程应使用同版本的 core、2d、vite-plugin；可按 README 的 file: 本地链接方式指向固定源码 packages/，避免 create 命令默默获取最新版本。场景使用生成器编排图形；旁白同步按官方 docs/getting-started 对应版本资料处理。

需要 MP4 时选定对应版本的 FFmpeg 导出插件并确认实际配置；仅预览成功不能标记视频导出成功。

上游：[官方仓库](https://github.com/motion-canvas/motion-canvas)。`show` 输出当前固定源码链接；使用时优先读该 commit 的资料。上面的调用形态用于指引，未通过本库执行检查的部分不标为已验证。
