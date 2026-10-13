# 归藏 Product Video 使用入口

版本、角色、依赖与验证状态以 [catalog.json](../../catalog.json) 的 `guizang` 为准。

在本库根目录先执行：

```text
python scripts/toolbox.py show guizang
python scripts/toolbox.py doctor guizang
python scripts/toolbox.py fetch guizang
```

fetch 仅获取已采用 commit，不检查最新版本。使用输出目录中的上游文件；要写任务工程时复制到 work/ 或用户指定目录。以下命令工作目录是该固定源码/任务目录，不是本库根目录。

先读固定源码的 SKILL.md；确认产品范围与用户要展示的平台，概念试验要明确标注固定内容。源码目录记为 SOURCE，任务目录记为 VIDEO。

```text
python SOURCE/scripts/init_project.py --output VIDEO --style repo --repo PRODUCT_REPO
python SOURCE/scripts/check_environment.py --project VIDEO --engine browser
```

然后在 VIDEO 按起步工程 package.json 执行 npm install、npm run build、npm run preview。编辑 plan.json、DIRECTION.md 和镜头组件；npm run stills 检查关键画面；npm run render 导出。声音使用原 scripts/mix_audio.py，最终检查使用 scripts/check_delivery.py。Windows 注意 UTF-8 与浏览器路径，按环境检查报告处理，不把另一个引擎的结果冒充本工具。

最小集成检查可用 python -m unittest discover -s tests；这只检查上游工具脚本，不等于产品宣传片已经验收。制作时只加载 references/starter.md、component-pipeline.md 或当前需要的声音/渲染部分。

上游：[官方仓库](https://github.com/op7418/guizang-product-video-skill)。`show` 输出当前固定源码链接；使用时优先读该 commit 的资料。上面的调用形态用于指引，未通过本库执行检查的部分不标为已验证。
