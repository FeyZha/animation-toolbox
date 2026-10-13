# Code2Video (lixingit) 使用入口

版本、角色、依赖与验证状态以 [catalog.json](../../catalog.json) 的 `code2video` 为准。

在本库根目录先执行：

```text
python scripts/toolbox.py show code2video
python scripts/toolbox.py doctor code2video
python scripts/toolbox.py fetch code2video
```

fetch 仅获取已采用 commit，不检查最新版本。要编辑或安装依赖时，复制固定源码到 work/ 或用户指定任务目录，保留来源。下面的原生命令在所述任务目录执行；Python/Node 依赖局部安装，不修改全局技能目录。

本入口固定 `lixingit/code2video`。README 引用了 Show Lab 的研究项目，不能因此把另一个仓库当作本档案已采用的源码。

在固定源码任务副本的 `src/` 中，用 Python 3.12 局部环境安装：
```text
python -m pip install -r requirements.txt
```

按 `src/api_config.example.json` 建立任务本地的 api_config.json；核对 `src/gpt_request.py` 中实际支持的模型与配置字段。视觉反馈和素材获取可能另需接口；不将凭据文件提交或输出。

单题入口是 `src/run_agent_single.sh`。该固定版本脚本设置 `PY=python3.12`、`API=deepseek`，复制到任务目录后按所建环境和配置调整，再从 src 执行：
```text
sh run_agent_single.sh --knowledge_point "Linear transformations and matrices"
```

只运行单题，不默认运行完整基准 `run_agent.sh`。输出查看 `src/CASES/` 对应目录；Windows 需可用的 Shell、字体和 Manim 系统依赖。

上游：[官方仓库](https://github.com/lixingit/code2video)。`show` 输出固定源码和许可链接；使用时读取该 commit 的资料。本次核对了入口文档与相关源码，尚未在本库运行完整制作流程；验证状态保持 `not-run`。
