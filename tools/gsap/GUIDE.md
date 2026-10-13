# GSAP 使用入口

版本、角色、依赖与验证状态以 [catalog.json](../../catalog.json) 的 `gsap` 为准。

在本库根目录先执行：

```text
python scripts/toolbox.py show gsap
python scripts/toolbox.py doctor gsap
python scripts/toolbox.py fetch gsap
```

fetch 仅获取已采用 commit，不检查最新版本。使用输出目录中的上游文件；要写任务工程时复制到 work/ 或用户指定目录。以下命令工作目录是该固定源码/任务目录，不是本库根目录。

使用固定源码中的构建文件，或在任务工程安装已确认对应的具体版本。GSAP 是运动控制库，不是视频导出器。

```javascript
import {gsap} from 'gsap';
const timeline = gsap.timeline({paused: true});
timeline.to('#box', {x: 200, duration: 1});
timeline.seek(0.5);
```

网页需要交互时按宿主播放 timeline；视频需要外部时钟逐帧 seek。使用 SVG/滚动等插件时明确 import 并 registerPlugin，先核对固定版本是否包含该插件。不要让独立的实时自动播放与视频时间轴同时控制同一元素。

上游：[官方仓库](https://github.com/greensock/GSAP)。`show` 输出当前固定源码链接；使用时优先读该 commit 的资料。上面的调用形态用于指引，未通过本库执行检查的部分不标为已验证。
