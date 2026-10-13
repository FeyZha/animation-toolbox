# MathLens 使用入口

版本、角色、依赖与验证状态以 [catalog.json](../../catalog.json) 的 `mathlens` 为准。

在本库根目录先执行：

```text
python scripts/toolbox.py show mathlens
python scripts/toolbox.py doctor mathlens
python scripts/toolbox.py fetch mathlens
```

fetch 仅获取已采用 commit，不检查最新版本。要编辑或安装依赖时，复制固定源码到 work/ 或用户指定任务目录，保留来源。下面的原生命令在所述任务目录执行；Python/Node 依赖局部安装，不修改全局技能目录。

先读固定源码的 `SKILL.md`，在任务目录建立 Python 虚拟环境，按 `requirements.txt` 补依赖。下列 python 均指该虚拟环境的解释器。

在固定源码的任务副本中初始化：
```text
python init.py ./my_math_problem
```

按上游八步流程准备题目分析、HTML/SVG 讲解、分镜、audio_list.csv 和 Manim 场景。进入初始化生成的项目目录后，依次使用：
```text
python scripts/generate_tts.py audio_list.csv ./audio --voice xiaoxiao
python scripts/validate_audio.py 分镜.md ./audio
python scripts/check.py
python scripts/render.py
```

配音依赖 Microsoft Edge 在线服务；先核对实际时长及返回的同步点，再安排动画。此前局部试做遇到渲染脚本质量参数问题时，使用任务虚拟环境的 `python -m manim` 直接渲染生成场景；不能据此声称完整 AI 流水线已通过。

README 声明 **CC BY-NC 4.0**；商业使用需要作者授权。

上游：[官方仓库](https://github.com/shuyicc/MathLens)。`show` 输出固定源码和许可链接；使用时读取该 commit 的资料。本次核对了入口文档与相关源码，尚未在本库运行完整制作流程；验证状态保持 `not-run`。
