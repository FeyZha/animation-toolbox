# teach-me 使用入口

版本、角色、依赖与验证状态以 [catalog.json](../../catalog.json) 的 `teach-me` 为准。

在本库根目录先执行：

```text
python scripts/toolbox.py show teach-me
python scripts/toolbox.py doctor teach-me
python scripts/toolbox.py fetch teach-me
```

fetch 仅获取已采用 commit，不检查最新版本。要编辑或安装依赖时，复制固定源码到 work/ 或用户指定任务目录，保留来源。下面的原生命令在所述任务目录执行；Python/Node 依赖局部安装，不修改全局技能目录。

在固定源码的任务副本中建立 Python 3.11+ 虚拟环境，用该环境解释器安装：
```text
python -m pip install -e .
```

先核对 `configs/default.yaml` 与 `src/teachme/config.py`。该固定版本默认模型后端为 Claude Code CLI，TTS 配置为本地 Kokoro；README 中仍有 macOS say 的描述，以实际配置为准。API 后端需要相应凭据。默认 macOS 通知在其他系统需关闭或调整，不能配置对外发送通知。

使用任务虚拟环境中的命令：
```text
teachme generate "讲解神经网络前向传播" --config configs/default.yaml --out output/neural-network
```

可用 `--sources` 指定用户资料；运行前用 `teachme generate --help` 核对其他参数。渲染、旁白与视觉审查会保留中间文件。确认真实 MP4 和审查结果后交付，不把流水线结束当作内容正确的证明。

上游：[官方仓库](https://github.com/wanxinwanxin/teach-me)。`show` 输出固定源码和许可链接；使用时读取该 commit 的资料。本次核对了入口文档与相关源码，尚未在本库运行完整制作流程；验证状态保持 `not-run`。
