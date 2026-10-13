# Manim Voiceover 使用入口

版本、角色、依赖与验证状态以 [catalog.json](../../catalog.json) 的 `manim-voiceover` 为准。

在本库根目录先执行：

```text
python scripts/toolbox.py show manim-voiceover
python scripts/toolbox.py doctor manim-voiceover
python scripts/toolbox.py fetch manim-voiceover
```

fetch 仅获取已采用 commit，不检查最新版本。要编辑或安装依赖时，复制固定源码到 work/ 或用户指定任务目录，保留来源。下面的原生命令在所述任务目录执行；Python/Node 依赖局部安装，不修改全局技能目录。

这是 Manim Community 的插件，不是 ManimGL 插件或独立场景生成器。先读固定源码 `docs/source/installation.rst` 与 `quickstart.rst`。

在任务虚拟环境中安装固定源码，并只选择所需语音服务。以 gTTS 示例为起点：
```text
python -m pip install "/absolute/path/to/pinned/manim-voiceover/source[gtts]"
python -m manim -ql examples/gtts-example.py GTTSExample --disable_caching
```

安装与渲染的 python 都使用任务虚拟环境；示例从固定源码副本读取，不能从远端 main 临时下载。场景继承 `VoiceoverScene`，设置 `GTTSService`，通过 `self.voiceover(...)` 的 tracker.duration 让动画匹配旁白。

gTTS 需要联网；其他服务的凭据、SoX、PortAudio 或语音识别依赖按具体服务补齐，不使用 all 一次安装全部。词级书签依赖相应时间数据，不等于任意语音都天然精确同步。渲染保留 `--disable_caching`，再检查音画时长。

上游：[官方仓库](https://github.com/ManimCommunity/manim-voiceover)。`show` 输出固定源码和许可链接；使用时读取该 commit 的资料。本次核对了入口文档与相关源码，尚未在本库运行完整制作流程；验证状态保持 `not-run`。
