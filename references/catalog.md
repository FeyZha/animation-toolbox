# 目录说明

catalog.json 是工具事实和版本状态的唯一来源，GUIDE 只写使用过程，不重复维护版本号。

## 职责 role

- directory：发现项目的导航集合，不能直接制作。
- workflow：分镜、动画、声音、审片等制作流程/技能包。
- workbench：统一编辑或选工具的入口，可能依赖外部 AI CLI。
- engine：场景、时间线、预览、渲染工程。
- library：绘图、三维、运动或合成能力，通常要嵌入一个工程。

tasks 按产品宣传、知识讲解、音乐视觉、数据叙事、交互、生成艺术检索；outputs 仅记录原生支持的交付形式，网页库不会因能录屏就自动被标为原生视频工具。

source.repository 采用 owner/repo；adopted_commit 是固定使用基准；observed_commit 是最后发现的版本；branch=null 表示跟随上游默认分支，而不是假设所有仓库都用 main。

verification.status=not-run 表示未通过本库执行验证。verification.checks 记录实际命令与范围；首次运行和后续版本升级共用此记录，不能把文档核对当作成功运行。

review_globs 指使用入口或能力说明变化时应交给 AI 的文件，不是能忽略其余代码的白名单。

automatic_checks 是本库已审阅的最小运行检查列表，包含 argv 和相对工作目录 cwd。空列表表示暂没有可自动执行的检查。源码发生功能变化且无检查时，进入 needs-ai；不能自动假定兼容。

目录集合的下游项目保留为来源关系，不自动递归安装。增加新工具需填写角色、用途、限制、需求、GUIDE、固定 commit；运行 `validate` 检查引用和重复项。
