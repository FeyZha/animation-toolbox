# Paul Explainer Video 使用入口

版本、角色、依赖与验证状态以 [catalog.json](../../catalog.json) 的 `paul-explainer` 为准。

在本库根目录先执行：

```text
python scripts/toolbox.py show paul-explainer
python scripts/toolbox.py doctor paul-explainer
python scripts/toolbox.py fetch paul-explainer
```

fetch 仅获取已采用 commit，不检查最新版本。要编辑或安装依赖时，复制固定源码到 work/ 或用户指定任务目录，保留来源。下面的原生命令在所述任务目录执行；Python/Node 依赖局部安装，不修改全局技能目录。

入口是 `skills/explainer-video/SKILL.md`，并非根目录同名技能。与 Mng 的 explainer-video 是两个独立仓库。

先阅读该目录的 README/说明，检查 Python 3.11+、FFmpeg、Cairo、Pango 和字体。上游 setup.sh 默认把环境放到用户数据目录；本库使用时将 `EXPLAINER_VENV` 指向任务内的 `.venv`，避免全局安装。setup.sh 是 Bash 脚本，上游仅声明 macOS/Linux 支持；Windows 需另行适配。

`<skill-dir>` 表示固定源码中的 `skills/explainer-video`：
```text
python <skill-dir>/scripts/check_env.py
python <skill-dir>/scripts/venv_path.py --python
python <skill-dir>/scripts/tts.py script.txt out/
python <skill-dir>/scripts/beats.py out/word_times.json beats.tsv beats.json
```

TTS 默认使用 `SPEECHIFY_API_KEY`，会发送旁白文本并可能计费。beats.tsv 的键和提示词之间必须是真正的 TAB；替换配音服务仍需满足逐词时间契约，不能只提供音频。

将 `assets/style.py` 复制到任务目录，编写读取 beats.json 的场景，再用 venv_path.py 返回的解释器渲染：
```text
python -m manim -qm --disable_caching scene.py SceneName
bash <skill-dir>/scripts/mux.sh media/videos/scene/720p30/SceneName.mp4 out/narration.wav final.mp4
```

关闭 Manim 缓存是该流程的同步要求；实际视频和旁白时长仍需检查。

上游：[官方仓库](https://github.com/PaulLemaistre/explainer-video)。`show` 输出固定源码和许可链接；使用时读取该 commit 的资料。本次核对了入口文档与相关源码，尚未在本库运行完整制作流程；验证状态保持 `not-run`。
