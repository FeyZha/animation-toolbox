# Three.js 使用入口

版本、角色、依赖与验证状态以 [catalog.json](../../catalog.json) 的 `three` 为准。

在本库根目录先执行：

```text
python scripts/toolbox.py show three
python scripts/toolbox.py doctor three
python scripts/toolbox.py fetch three
```

fetch 仅获取已采用 commit，不检查最新版本。使用输出目录中的上游文件；要写任务工程时复制到 work/ 或用户指定目录。以下命令工作目录是该固定源码/任务目录，不是本库根目录。

Three.js 负责浏览器三维画面。用固定源码 src/ 模块或该源码实际构建输出，嵌入自己的页面工程；使用发布包时明确锁定版本并确认来源。

```javascript
import * as THREE from 'three';
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(70, 16/9, 0.01, 10);
camera.position.z = 1;
const renderer = new THREE.WebGLRenderer();
renderer.setSize(640, 360);
document.body.appendChild(renderer.domElement);
const box = new THREE.Mesh(new THREE.BoxGeometry(0.2,0.2,0.2), new THREE.MeshNormalMaterial());
scene.add(box);
renderer.setAnimationLoop(t => { box.rotation.y = t / 1000; renderer.render(scene, camera); });
```

示例 import 指向任务工程中已固定的依赖。addons 与核心保持同版本。这个实时循环适合网页；视频需由宿主接管时间和导出。

上游：[官方仓库](https://github.com/mrdoob/three.js)。`show` 输出当前固定源码链接；使用时优先读该 commit 的资料。上面的调用形态用于指引，未通过本库执行检查的部分不标为已验证。
