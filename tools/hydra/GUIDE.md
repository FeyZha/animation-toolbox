# Hydra 使用入口

版本、角色、依赖与验证状态以 [catalog.json](../../catalog.json) 的 `hydra` 为准。

在本库根目录先执行：

```text
python scripts/toolbox.py show hydra
python scripts/toolbox.py doctor hydra
python scripts/toolbox.py fetch hydra
```

fetch 仅获取已采用 commit，不检查最新版本。使用输出目录中的上游文件；要写任务工程时复制到 work/ 或用户指定目录。以下命令工作目录是该固定源码/任务目录，不是本库根目录。

用于实时合成画面。固定源码包含编辑器前端，启动前读取 package.json 的 scripts；上游 README 的 npm dev 是简写/笔误，不直接执行。

```text
npm install
npm run dev
```

在浏览器编辑器运行最小调用：
```javascript
osc(20, 0.1, 0.8).rotate(0.8).out()
```

初次调用无需摄像头、麦克风或远端流。用户要求音频响应时再接音频输入。嵌入宿主页面时使用对应 hydra-synth 模块，并记录实际包版本；MP4 需要单独的可控录制/导出流程，不能承诺库原生输出视频。

上游：[官方仓库](https://github.com/hydra-synth/hydra)。`show` 输出当前固定源码链接；使用时优先读该 commit 的资料。上面的调用形态用于指引，未通过本库执行检查的部分不标为已验证。
