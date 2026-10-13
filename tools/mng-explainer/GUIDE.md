# Mng Explainer Video 使用入口

版本、角色、依赖与验证状态以 [catalog.json](../../catalog.json) 的 `mng-explainer` 为准。

在本库根目录先执行：

```text
python scripts/toolbox.py show mng-explainer
python scripts/toolbox.py doctor mng-explainer
python scripts/toolbox.py fetch mng-explainer
```

fetch 仅获取已采用 commit，不检查最新版本。要编辑或安装依赖时，复制固定源码到 work/ 或用户指定任务目录，保留来源。下面的原生命令在所述任务目录执行；Python/Node 依赖局部安装，不修改全局技能目录。

先读固定源码根目录 `SKILL.md`。本流程绘制 HTML/CSS/GSAP 页面，与 PaulLemaistre 的 Manim 配音流程分别收录。

复制固定源码到任务目录，在 lib 中安装锁定依赖和浏览器：
```text
npm ci
npx playwright install chromium
```

以上两条的工作目录为任务副本 `lib/`。随后回到任务副本根目录，编写 page.html 和 config.json：
```json
{
  "title": "神经网络",
  "voice": "zh-CN-XiaoxiaoNeural",
  "html": "page.html",
  "scriptSegments": ["输入经过连接进入神经元。", "加权求和之后得到输出。"]
}
```
```text
node lib/pipeline.js --config config.json --out video.mp4
```

页面遵守上游契约：1280×720，读取 `window.__AUDIO_DURATION` 与按段注入的 `window.__SEGMENT_DURATIONS`，结束后设置 `window.__done = true`。先核对实际音频时长再编排场景。

配音通过在线 Edge 服务，页面示例还从 CDN 加载 GSAP；“本地运行”不代表无需联网。结果检查 MP4 声音、时长和录屏帧。

上游：[官方仓库](https://github.com/Mng-dev-ai/explainer-video)。`show` 输出固定源码和许可链接；使用时读取该 commit 的资料。本次核对了入口文档与相关源码，尚未在本库运行完整制作流程；验证状态保持 `not-run`。
