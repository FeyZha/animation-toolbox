# fix-webm-duration 使用入口

版本、角色、依赖与验证状态以 [catalog.json](../../catalog.json) 的 `fix-webm-duration` 为准。

在本库根目录先执行：

```text
python scripts/toolbox.py show fix-webm-duration
python scripts/toolbox.py doctor fix-webm-duration
python scripts/toolbox.py fetch fix-webm-duration
```

fetch 仅获取已采用 commit，不检查最新版本。要编辑或安装依赖时，复制固定源码到 work/ 或用户指定任务目录，保留来源。下面的原生命令在所述任务目录执行；Python/Node 依赖局部安装，不修改全局技能目录。

先读固定源码 README。当前接口来自包 `@fix-webm-duration/fix`，不要套用旧版 `ysFixWebmDuration` 回调示例。

这是 Nx 多包仓库，根包是私有工作区，不是可直接安装的修复库。在固定源码的任务副本中按锁文件构建：
```text
npm ci
npm run build
```

生成包在 `dist/packages/parser` 与 `dist/packages/fix`；将两者一起作为本地依赖接入录制工程，避免 fix 的 parser 依赖从远端浮动获取。真正接入前核对构建产物的 package.json 和该工程的打包配置。

浏览器调用形态：
```typescript
import { fixWebmDuration } from "@fix-webm-duration/fix";

const fixedBlob = await fixWebmDuration(recordedBlob, durationMs);
```

durationMs 必须是录制时测得的毫秒时长。已有有效时长的文件通常保留原样。该工具不转码、不修复任意损坏文件，也不保证所有播放器的拖动行为；检查处理后的 WebM 时长与播放结果。

上游：[官方仓库](https://github.com/yusitnikov/fix-webm-duration)。`show` 输出固定源码和许可链接；使用时读取该 commit 的资料。本次核对了入口文档与相关源码，尚未在本库运行完整制作流程；验证状态保持 `not-run`。
