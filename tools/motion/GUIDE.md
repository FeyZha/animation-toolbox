# Motion 使用入口

版本、角色、依赖与验证状态以 [catalog.json](../../catalog.json) 的 `motion` 为准。

在本库根目录先执行：

```text
python scripts/toolbox.py show motion
python scripts/toolbox.py doctor motion
python scripts/toolbox.py fetch motion
```

fetch 仅获取已采用 commit，不检查最新版本。使用输出目录中的上游文件；要写任务工程时复制到 work/ 或用户指定目录。以下命令工作目录是该固定源码/任务目录，不是本库根目录。

Motion 与旧名称 Framer Motion 归为同一条目。先选 JavaScript、React 或 Vue 入口，使用固定源码构建出的同版本包，或确认对应发布版本后局部安装。

```javascript
import {animate} from 'motion';
animate('#box', {x: 100});
```

React 入口为 motion/react，Vue 常用 motion-v；不要混用不同平台 API。官方 README 指向 motion.dev/llms.txt 与文档工具，按当前选中 API 查阅即可。网页交互和手势不是原生 MP4；需要视频时交给 Remotion/其他宿主并使用可控时间。

上游：[官方仓库](https://github.com/motiondivision/motion)。`show` 输出当前固定源码链接；使用时优先读该 commit 的资料。上面的调用形态用于指引，未通过本库执行检查的部分不标为已验证。
