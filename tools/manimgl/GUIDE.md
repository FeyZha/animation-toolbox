# ManimGL / 3Blue1Brown Manim 使用入口

版本、角色、依赖与验证状态以 [catalog.json](../../catalog.json) 的 `manimgl` 为准。

在本库根目录先执行：

```text
python scripts/toolbox.py show manimgl
python scripts/toolbox.py doctor manimgl
python scripts/toolbox.py fetch manimgl
```

fetch 仅获取已采用 commit，不检查最新版本。要编辑或安装依赖时，复制固定源码到 work/ 或用户指定任务目录，保留来源。下面的原生命令在所述任务目录执行；Python/Node 依赖局部安装，不修改全局技能目录。

这是 `3b1b/manim`，包名 `manimgl`、导入名 `manimlib`；现有 `manim` 档案对应 Manim Community，两者不能互换命令或场景代码。

在任务目录创建 Python 3.10+ 虚拟环境，使用该环境的解释器安装固定源码：
```text
python -m pip install /absolute/path/to/pinned/manimgl/source
```

使用虚拟环境中的 manimgl 命令，在固定源码的任务副本运行上游示例：
```text
manimgl example_scenes.py OpeningManimExample -w
```

`-w` 写出视频；不带写入参数时上游默认开启预览窗口。输出目录和画质从固定源码配置及 `custom_config.yml` 读取，不套用社区版 `python -m manim -ql` 参数。

系统需要 FFmpeg、可用的 OpenGL 环境与文字渲染依赖；包含公式的示例还需要 LaTeX。仅做基本图形测试时可选不含公式的场景。doctor 不会验证显卡、窗口或字体是否可用。

上游：[官方仓库](https://github.com/3b1b/manim)。`show` 输出固定源码和许可链接；使用时读取该 commit 的资料。本次核对了入口文档与相关源码，尚未在本库运行完整制作流程；验证状态保持 `not-run`。
