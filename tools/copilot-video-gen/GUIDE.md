# Copilot Video Gen 使用入口

版本、角色、依赖与验证状态以 [catalog.json](../../catalog.json) 的 `copilot-video-gen` 为准。

在本库根目录先执行：

```text
python scripts/toolbox.py show copilot-video-gen
python scripts/toolbox.py doctor copilot-video-gen
python scripts/toolbox.py fetch copilot-video-gen
```

fetch 仅获取已采用 commit，不检查最新版本。使用输出目录中的上游文件；要写任务工程时复制到 work/ 或用户指定目录。以下命令工作目录是该固定源码/任务目录，不是本库根目录。

本库可直接读取固定源码的 skills/video-gen/SKILL.md，无须安装为全局 Copilot 插件。

先运行纯 Node 选择器：
```text
node skills/video-gen/scripts/recommend.mjs "explain a math proof" --json
```

选择具体工具后，在 Bash 中生成独立任务工程并渲染：
```text
bash skills/video-gen/scripts/scaffold.sh threejs my-globe --dir WORK --prompt "rotating globe"
bash skills/video-gen/scripts/preview.sh WORK/my-globe
bash skills/video-gen/scripts/render.sh WORK/my-globe --out WORK/out/globe.mp4
```

Windows 需要 Git Bash/WSL，不能把 .sh 直接当 PowerShell 命令。选择器的规则是初筛，最终仍根据用途、输出与环境判断。默认起步工程可能引用 CDN；为可复现任务锁定实际依赖。选择器检查成功只证明路由调用成功，不代表七条渲染链都已验证。

上游：[官方仓库](https://github.com/abhi-singhs/copilot-video-gen-plugin)。`show` 输出当前固定源码链接；使用时优先读该 commit 的资料。上面的调用形态用于指引，未通过本库执行检查的部分不标为已验证。
