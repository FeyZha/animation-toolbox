# Code Explainer Film 使用入口

版本、角色、依赖与验证状态以 [catalog.json](../../catalog.json) 的 `code-explainer-film` 为准。

在本库根目录先执行：

```text
python scripts/toolbox.py show code-explainer-film
python scripts/toolbox.py doctor code-explainer-film
python scripts/toolbox.py fetch code-explainer-film
```

fetch 仅获取已采用 commit，不检查最新版本。要编辑或安装依赖时，复制固定源码到 work/ 或用户指定任务目录，保留来源。下面的原生命令在所述任务目录执行；Python/Node 依赖局部安装，不修改全局技能目录。

从固定源码的 `template/` 复制完整模板到任务目录，不直接修改缓存。在任务目录创建 Python 3.10+ 虚拟环境，并用该环境解释器执行：
```text
python -m pip install -r requirements.txt
python build.py
```

安装前需要 Manim 的文字渲染依赖、FFmpeg 与 ffprobe。完整输出为 `out/explainer.mp4`。

模板的三个修改入口是 SCRIPT.md 分镜、build.py 中实际使用的 NARR 旁白、scenes.py 场景。同步修改对应场景名，不能只改 SCRIPT.md 就认为交付旁白已改变。
```text
python build.py Flow
python build.py --concat
```

前者重建指定场景再拼接；后者只拼接已有片段。语音和画质可按上游使用 FILM_VOICE、FILM_QUALITY 环境变量配置。

配音需要在线 Edge 服务；构建会补齐较短音轨/画面，但过长停顿仍需调整场景节奏。检查缺失场景提示并核对整片，不把“拼出了文件”当成全部场景成功。

上游：[官方仓库](https://github.com/kobyal/code-explainer-film)。`show` 输出固定源码和许可链接；使用时读取该 commit 的资料。本次核对了入口文档与相关源码，尚未在本库运行完整制作流程；验证状态保持 `not-run`。
