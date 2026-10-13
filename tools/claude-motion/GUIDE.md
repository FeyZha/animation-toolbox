# Claude Motion 使用入口

版本、角色、依赖与验证状态以 [catalog.json](../../catalog.json) 的 `claude-motion` 为准。

在本库根目录先执行：

```text
python scripts/toolbox.py show claude-motion
python scripts/toolbox.py doctor claude-motion
python scripts/toolbox.py fetch claude-motion
```

fetch 仅获取已采用 commit，不检查最新版本。使用输出目录中的上游文件；要写任务工程时复制到 work/ 或用户指定目录。以下命令工作目录是该固定源码/任务目录，不是本库根目录。

从固定源码复制独立任务工程，先读 AGENTS.md 和相关 .claude/skills，不需要全局安装。

动态图形基线命令：
```text
npm install
npm run build
npm run studio
```

上游基线输出 out/effort.mp4。网页仿真路线先读 sims/README.md 与 web-sims 技能，再执行：
```text
npx playwright install chromium
npm run sims
npm run capture -- engine --size 1080x1350 --out out/engine.mp4
```

先选动态图形或网页仿真其中一条路线。声音生成器在 sfx/；跟随所选管线组织时间轴。安装只作用于任务目录，浏览器缺项按用户环境处理。

上游：[官方仓库](https://github.com/whaleyxbt/claude-motion)。`show` 输出当前固定源码链接；使用时优先读该 commit 的资料。上面的调用形态用于指引，未通过本库执行检查的部分不标为已验证。
