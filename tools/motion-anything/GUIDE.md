# Motion Anything 使用入口

版本、角色、依赖与验证状态以 [catalog.json](../../catalog.json) 的 `motion-anything` 为准。

在本库根目录先执行：

```text
python scripts/toolbox.py show motion-anything
python scripts/toolbox.py doctor motion-anything
python scripts/toolbox.py fetch motion-anything
```

fetch 仅获取已采用 commit，不检查最新版本。使用输出目录中的上游文件；要写任务工程时复制到 work/ 或用户指定目录。以下命令工作目录是该固定源码/任务目录，不是本库根目录。

这是本地工作台。需要 Node，以及至少一个可用的外部 AI CLI；仅打开工作台不代表已经有模型调用能力。

在固定源码复制出的任务工程运行：
```text
node cli/bin/motion.js serve 4399
```

浏览器打开终端给出的 localhost 地址；根据需求选择网页动效或视频编辑流程。选中配方后再读对应 recipes/ 条目与 MOTION-SPEC.md。源码 README 声明运行入口不需要 npm install；若本库固定版本的实际文件要求改变，以该版本文件为准，并走适配。

AI CLI 凭据继续由原工具管理，不写入本库。项目里所说的多个 engines 指 AI 调用端，不是多种视频渲染引擎。导出前确认当前页面/视频管线实际支持的格式。

上游：[官方仓库](https://github.com/nexu-io/motion-anything)。`show` 输出当前固定源码链接；使用时优先读该 commit 的资料。上面的调用形态用于指引，未通过本库执行检查的部分不标为已验证。
