# p5.js 使用入口

版本、角色、依赖与验证状态以 [catalog.json](../../catalog.json) 的 `p5` 为准。

在本库根目录先执行：

```text
python scripts/toolbox.py show p5
python scripts/toolbox.py doctor p5
python scripts/toolbox.py fetch p5
```

fetch 仅获取已采用 commit，不检查最新版本。使用输出目录中的上游文件；要写任务工程时复制到 work/ 或用户指定目录。以下命令工作目录是该固定源码/任务目录，不是本库根目录。

这是浏览器绘图库。先读取固定源码 package.json 与开发说明，使用其构建输出或在任务工程安装对应明确版本；不直接写 npm install p5@latest。

在页面加载已固定版本的 p5 构建后，最小场景为：
```javascript
function setup() { createCanvas(640, 360); }
function draw() { background(20); circle(mouseX, mouseY, 60); }
```

若源仓库版本尚未发布到 npm，不把 package.json 中版本号当作该 commit 的等价发布包；使用源码构建。当前 API 与示例优先看固定源码的 README、src/ 和 test/，以及官方 reference。视频任务另外选导出工程；交互网页直接交付 HTML 工程。

上游：[官方仓库](https://github.com/processing/p5.js)。`show` 输出当前固定源码链接；使用时优先读该 commit 的资料。上面的调用形态用于指引，未通过本库执行检查的部分不标为已验证。
