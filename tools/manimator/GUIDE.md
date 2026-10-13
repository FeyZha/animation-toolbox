# Manimator 使用入口

版本、角色、依赖与验证状态以 [catalog.json](../../catalog.json) 的 `manimator` 为准。

在本库根目录先执行：

```text
python scripts/toolbox.py show manimator
python scripts/toolbox.py doctor manimator
python scripts/toolbox.py fetch manimator
```

fetch 仅获取已采用 commit，不检查最新版本。要编辑或安装依赖时，复制固定源码到 work/ 或用户指定任务目录，保留来源。下面的原生命令在所述任务目录执行；Python/Node 依赖局部安装，不修改全局技能目录。

先看固定源码 `pyproject.toml`、`.env.example` 与 `src/manimator/api/`。Python 要求 3.11+；在任务虚拟环境安装固定源码：
```text
python -m pip install -e .
```

配置任务本地凭据。固定源码部分模块会将 `OPENROUTER_API_KEY` 写入进程中的 `OPENAI_API_KEY`，并读取 `OPENAI_BASE_URL`；仅设置 OPENAI_API_KEY 可能不够。模型和语音后端以实际源码为准。

使用上游 FastAPI 对象在本机启动：
```text
python -m uvicorn manimator.api.app:app --host 127.0.0.1 --port 8042
```

在本机 `/docs` 查看 `POST /api/animation/generate` 的请求结构与结果；生成会调用模型并执行 Manim。根目录 main.py 是包含固定题目和模型的试验，不当成通用文本命令入口。环境成功启动也不等于生成链路通过。

固定版本未见 LICENSE，README 也未明确授权条件；复用或分发前需向作者确认。

上游：[官方仓库](https://github.com/nabin2004/Manimator)。`show` 输出固定源码和许可链接；使用时读取该 commit 的资料。本次核对了入口文档与相关源码，尚未在本库运行完整制作流程；验证状态保持 `not-run`。
