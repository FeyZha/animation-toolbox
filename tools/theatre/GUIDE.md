# Theatre.js 使用入口

版本、角色、依赖与验证状态以 [catalog.json](../../catalog.json) 的 `theatre` 为准。

在本库根目录先执行：

```text
python scripts/toolbox.py show theatre
python scripts/toolbox.py doctor theatre
python scripts/toolbox.py fetch theatre
```

fetch 仅获取已采用 commit，不检查最新版本。使用输出目录中的上游文件；要写任务工程时复制到 work/ 或用户指定目录。以下命令工作目录是该固定源码/任务目录，不是本库根目录。

这是供宿主使用的运动编排库，原生交付为网页。

从固定源码构建/链接对应 packages/core 和 packages/studio，或在任务工程使用已确认对应的发布版本。基本调用形态：
```javascript
import {getProject} from '@theatre/core';
const sheet = getProject('Demo').sheet('Scene');
const object = sheet.object('Box', {x: 0});
object.onValuesChange(({x}) => { box.position.x = x; });
```

可视化编辑再接 @theatre/studio，三维场景由 Three.js 等宿主提供。只读取当前集成需要的官方 docs/教程；需要 MP4 时另选导出链路。上游 README 对未发布开发状态的说明不当作已经可安装的版本。

上游：[官方仓库](https://github.com/theatre-js/theatre)。`show` 输出当前固定源码链接；使用时优先读该 commit 的资料。上面的调用形态用于指引，未通过本库执行检查的部分不标为已验证。
