# OmniManim 使用入口

版本、角色、依赖与验证状态以 [catalog.json](../../catalog.json) 的 `omnimanim` 为准。

在本库根目录先执行：

```text
python scripts/toolbox.py show omnimanim
python scripts/toolbox.py doctor omnimanim
python scripts/toolbox.py fetch omnimanim
```

fetch 仅获取已采用 commit，不检查最新版本。要编辑或安装依赖时，复制固定源码到 work/ 或用户指定任务目录，保留来源。下面的原生命令在所述任务目录执行；Python/Node 依赖局部安装，不修改全局技能目录。

在固定源码的任务副本中建立 Python 3.10+ 虚拟环境；以下 python 使用该环境的解释器：
```text
python -m pip install -r requirements.txt
python -m agent_pipeline "用动画讲解神经网络前向传播"
```

运行前按 `.env.example` 设置本地 `.env`：`OPENAI_API_KEY`，按需设置 `OPENAI_BASE_URL` 与 `OPENAI_MODEL`。代码生成和视觉模型评测均会调用接口；凭据和生成资料不提交到本库。

输出在 `runs/` 的各轮目录、summary.json 与最终视频中。先查看模型生成的代码、渲染结果和报告，再决定是否采用。TTS、OCR 和音视频合成的额外依赖按实际功能补齐。

已有视频评测使用：
```text
python -m eval_pipeline path/to/video.mp4 --out-dir path/to/eval_output
```

固定版本 README 的许可证章节只有“按需自定”，未给出明确许可文本；分发或商业复用前需向作者确认。

上游：[官方仓库](https://github.com/AI4Learning-Club/OmniManim)。`show` 输出固定源码和许可链接；使用时读取该 commit 的资料。本次核对了入口文档与相关源码，尚未在本库运行完整制作流程；验证状态保持 `not-run`。
