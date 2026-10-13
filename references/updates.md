# 手动 commit 更新流程

只有用户主动要求检查/同步时执行。没有 cron、后台服务、使用前自动更新或定时 GitHub Actions。

通过技能安装器得到的副本通常不含 .git。需要维护并提交目录时，先在用户指定位置或独立任务目录克隆本库，在该 Git 检出的根目录执行下列命令；安装副本仍按已安装内容调用。上游工具版本同步与重新安装本技能是两个操作，不自动覆盖安装副本。

## 机械流程

```text
python scripts/toolbox.py check-updates --all
python scripts/toolbox.py sync --all --commit
```

check-updates 只查询指定分支/default HEAD 的 commit，并记录 observed_commit 与检查错误，不修改 adopted_commit。失败不是“无更新”。无变化不拉取源码。

sync 执行检查并为变更工具获取新旧固定源码、完整文件差异，写入 .state/<id>.json。目录集合可机械更新；可执行项目在相关 GUIDE/接口资料未变化且 automatic_checks 通过时采用。其他情况写明确 needs-ai 原因，保留旧采用版本。--commit 自动提交已经完成的本地变更，不 push。AI 适配完待处理项目后再运行 commit-updates。

更新记录包含新增提交的 commit/标题和全部变更文件；`diff_path` 指向新旧版本的文本差异，二进制文件只标记变化。提交列表使用 GitHub 官方 Compare API 分页获取，避免浅克隆漏掉中间提交；文本差异使用本地 Git 生成，不受 API 的变更文件数量上限影响。公开仓库不需要凭据；API 限流或差异准备失败时保留旧采用版本并报错。这些请求只在主动更新流程中发生。

## AI 只处理这些事情

- 安装方式、CLI、接口或能力描述改变：检查差异，修改 tools/<id>/GUIDE.md、对应目录字段或本库封装。
- 自动检查失败：读取错误、定位缺依赖或兼容性问题，不重读其他工具。
- 没有可用自动检查：为这一次候选版本执行一次与用途有关的最小调用。值得复用时，把经过验证的命令加入 automatic_checks；不要用“文件存在”冒充运行验证。

候选源码位置与文件差异通过 `prepare-update <id>` 获取。可用 `verify` 在候选源码目录运行真实命令并保存返回码、输出摘要及 commit：

```text
python scripts/toolbox.py verify <id> --cwd . --reviewed -- python -m unittest discover -s tests
python scripts/toolbox.py apply-update <id>
```

--cwd 必须在候选源码内。适配 GUIDE/目录后再 verify；记录绑定候选 commit 和当前使用说明，之后又改说明需重新验证。apply-update 仅在待适配记录与当前 adopted_commit 一致、检查成功时采用，并保留实际验证范围。directory 类型无运行检查要求。

第一次使用尚无待更新计划时，verify 会验证当前采用 commit，不查询上游。通过后用 apply-update 把这一次调用的范围记入目录。加 --register 可将通过的命令保存成以后更新时的自动检查，脚本不会自行编造测试命令。

脚本不会调用付费模型。当前 AI 会话就是适配执行者，脚本生成的 needs-ai 清单提供上下文。

最后运行 `validate` 和本库测试，再提交本次目录、使用说明及必要封装的改动。`commit-updates` 自动暂存受管理的改动并创建本地提交；检测到已有暂存内容会拒绝，以免夹带其他工作。不自动 push、不创建/合并远端 PR。

尊重已有 Git 提交身份；未设置时只在这一次提交命令使用 Animation Toolbox Bot / animation-toolbox@example.invalid，不修改本地或全局 Git 身份配置。

上游源码放在 .cache；候选按完整 commit 分目录，旧版保留，不覆盖正在使用的工程。临时网络问题可在下次用户主动要求时重试；失败项目不阻塞其他工具的检查。
