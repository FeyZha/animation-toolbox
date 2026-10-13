# edge-tts 使用入口

版本、角色、依赖与验证状态以 [catalog.json](../../catalog.json) 的 `edge-tts` 为准。

在本库根目录先执行：

```text
python scripts/toolbox.py show edge-tts
python scripts/toolbox.py doctor edge-tts
python scripts/toolbox.py fetch edge-tts
```

fetch 仅获取已采用 commit，不检查最新版本。要编辑或安装依赖时，复制固定源码到 work/ 或用户指定任务目录，保留来源。下面的原生命令在所述任务目录执行；Python/Node 依赖局部安装，不修改全局技能目录。

在任务虚拟环境中，用该环境解释器安装固定源码：
```text
python -m pip install /absolute/path/to/pinned/edge-tts/source
```

使用同一环境的 edge-tts 命令：
```text
edge-tts --list-voices
edge-tts --voice zh-CN-XiaoxiaoNeural --text "这是神经网络的输入。" --write-media narration.mp3 --write-subtitles narration.srt
```

这两条会请求 Microsoft 在线服务，不能当成离线测试。音色以实际返回的列表为准。旁白 MP3 和 SRT 是本工具原生输出，视频需由动画引擎与 FFmpeg 等另行合成。

先测量音频时长，再编排动画。字幕或同步事件的粒度以当前返回数据为准，不承诺所有语言和版本都提供逐词标记。该项目的 LGPL 许可与在线服务条款分别适用，见固定源码 LICENSE 与上游说明。

上游：[官方仓库](https://github.com/rany2/edge-tts)。`show` 输出固定源码和许可链接；使用时读取该 commit 的资料。本次核对了入口文档与相关源码，尚未在本库运行完整制作流程；验证状态保持 `not-run`。
