# Manim Community 使用入口

版本、角色、依赖与验证状态以 [catalog.json](../../catalog.json) 的 `manim` 为准。

本入口是 Manim Community；3Blue1Brown 原始引擎见 [ManimGL](../manimgl/GUIDE.md)。两者的安装、导入和渲染命令不同。

在本库根目录先执行：

```text
python scripts/toolbox.py show manim
python scripts/toolbox.py doctor manim
python scripts/toolbox.py fetch manim
```

fetch 仅获取已采用 commit，不检查最新版本。使用输出目录中的上游文件；要写任务工程时复制到 work/ 或用户指定目录。以下命令工作目录是该固定源码/任务目录，不是本库根目录。

创建任务目录的局部虚拟环境，并安装本库固定源码路径；不用系统全局 pip install。

```text
python -m venv .venv
python -m pip install /absolute/path/to/pinned/manim/source
python -m manim -ql example.py SquareToCircle
```

上面后两条中的 python 必须是该任务 .venv 的解释器（Windows 为 .venv/Scripts/python.exe）。最小 example.py：
```python
from manim import Scene, Square, Circle, Create, Transform
class SquareToCircle(Scene):
    def construct(self):
        square = Square()
        self.play(Create(square))
        self.play(Transform(square, Circle()))
```

基础图形不需要 TeX；使用公式时再补对应环境。渲染结果在 media/。新版本的 Python 与系统依赖要求以固定源码 pyproject.toml 和安装文档为准。

上游：[官方仓库](https://github.com/ManimCommunity/manim)。`show` 输出当前固定源码链接；使用时优先读该 commit 的资料。上面的调用形态用于指引，未通过本库执行检查的部分不标为已验证。
