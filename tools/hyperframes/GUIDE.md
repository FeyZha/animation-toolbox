# HyperFrames 使用入口

版本、角色、依赖与验证状态以 [catalog.json](../../catalog.json) 的 `hyperframes` 为准。

在本库根目录先执行：

```text
python scripts/toolbox.py show hyperframes
python scripts/toolbox.py doctor hyperframes
python scripts/toolbox.py fetch hyperframes
```

fetch 仅获取已采用 commit，不检查最新版本。使用输出目录中的上游文件；要写任务工程时复制到 work/ 或用户指定目录。以下命令工作目录是该固定源码/任务目录，不是本库根目录。

先读固定源码的 skills/hyperframes/SKILL.md 或该版本实际 router 位置，选中创建流程后再加载域技能。没有要求安装全局技能时，直接在会话中读取文件即可。

官方 CLI 用法如下；实施时使用固定源码构建出的本地 CLI，或先确认发布包对应版本，避免 npx 默默安装最新：
```text
hyperframes init my-video
hyperframes preview
hyperframes render
```

进入 my-video 后再 preview/render。可定位时间的动画、音视频片段时序和结构检查由该版本技能定义；不要把任意依赖实时墙钟的页面直接当成确定性视频。部分解释流程输出可导航页面，执行前先确认交付类型。

源码使用 Bun 工作区时遵守其 lockfile；不为了阅读技能就安装全部开发依赖或拉取全部 LFS 演示素材。

上游：[官方仓库](https://github.com/heygen-com/hyperframes)。`show` 输出当前固定源码链接；使用时优先读该 commit 的资料。上面的调用形态用于指引，未通过本库执行检查的部分不标为已验证。
