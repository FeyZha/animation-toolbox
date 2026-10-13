# Awesome Claude Video Skills 使用入口

版本、角色、依赖与验证状态以 [catalog.json](../../catalog.json) 的 `awesome-video-skills` 为准。

在本库根目录先执行：

```text
python scripts/toolbox.py show awesome-video-skills
python scripts/toolbox.py doctor awesome-video-skills
python scripts/toolbox.py fetch awesome-video-skills
```

fetch 仅获取已采用 commit，不检查最新版本。使用输出目录中的上游文件；要写任务工程时复制到 work/ 或用户指定目录。以下命令工作目录是该固定源码/任务目录，不是本库根目录。

此项是资源目录，不运行制作、预览或渲染命令。读取固定 commit 下的 README，按用户用途查找候选，再核对候选自己的官方仓库。不要递归安装整个目录，不继承第三方评级为本库验证结果。

下游工具已经在本库登记时，返回其唯一工具 ID；未登记时按当前任务调查，长期收录再补 catalog 条目和 GUIDE。此目录上游更新可机械同步固定 commit，不需要运行动画检查。

上游：[官方仓库](https://github.com/zhuyansen/awesome-claude-video-skills)。`show` 输出当前固定源码链接；使用时优先读该 commit 的资料。上面的调用形态用于指引，未通过本库执行检查的部分不标为已验证。
