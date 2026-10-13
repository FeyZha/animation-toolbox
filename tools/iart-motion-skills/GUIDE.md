# iart Motion Skills 使用入口

版本、角色、依赖与验证状态以 [catalog.json](../../catalog.json) 的 `iart-motion-skills` 为准。

在本库根目录先执行：

```text
python scripts/toolbox.py show iart-motion-skills
python scripts/toolbox.py doctor iart-motion-skills
python scripts/toolbox.py fetch iart-motion-skills
```

fetch 仅获取已采用 commit，不检查最新版本。使用输出目录中的上游文件；要写任务工程时复制到 work/ 或用户指定目录。以下命令工作目录是该固定源码/任务目录，不是本库根目录。

这是多个技能包的总入口，先看固定源码 README 的 packs 分类，选与任务相关的一个子仓库。

具体的 [Motion Design Skills](../iart-motion-design/GUIDE.md) 已单独建档，可按其固定 commit 读取 motion-art-direction 等技能；该版本独立于总入口。

只读取该子包的 SKILL.md 与当前需要的 references/。原始 npx skills add 命令会修改技能安装目录，本库默认不执行全局安装；会话里直接读取子包说明即可。真正制作前确认所选子包需要 Remotion、Manim、网页工程还是其他运行环境。

如要长期收录某个子包，为它单独登记上游 repository 和 commit，再提供 GUIDE 与检查；不能把总目录已固定的 commit 当成所有子包也已固定。

上游：[官方仓库](https://github.com/iart-ai/motion-skills)。`show` 输出当前固定源码链接；使用时优先读该 commit 的资料。上面的调用形态用于指引，未通过本库执行检查的部分不标为已验证。
