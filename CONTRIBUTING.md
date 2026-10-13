# Contributing / 贡献指南

欢迎修正工具入口、补充相关工具和改进检索或手动维护流程。提交前请读 [AGENTS.md](AGENTS.md) 与 [SKILL.md](SKILL.md)。

## 新增或修改工具

1. 先查 `catalog.json` 的 repository 和 aliases，避免重复收录同一上游。
2. 在 `catalog.json` 增加或修改工具档案，使用完整 commit，明确 role、tasks、outputs、requirements、limits 和关联工具。字段见 [目录说明](references/catalog.md)。
3. 在 `tools/<id>/GUIDE.md` 写清固定源码的获取、局部安装、最小调用及预览/导出入口；优先复用上游方法。
4. 保留来源及对应版本的许可引用；导航集合登记为 directory，不递归收录或安装其所有下游。
5. 没执行过的工具标为 `not-run`。通过 `verify` 和 `apply-update` 记录实际执行结果，不能把文件存在或文档核对写成成功运行。记录不包含凭据、个人路径或私人任务内容。

更新既有上游版本时，遵循 [手动更新流程](references/updates.md)，在 PR 中说明触发原因、旧/新 commit、调用变化及验证范围。不要添加定时上游检查、使用前自动更新、付费 API 调用或全局安装步骤。

## 本地检查

```text
python scripts/toolbox.py validate
python -m unittest discover -s tests -v
git diff --check
```

核心代码保持 Python 3.10+ 标准库实现。修复行为问题时增加小而有意义的测试；避免为简单文案修改制造测试。测试使用本地临时仓库和模拟 API，不能访问上游、依赖私人账号或修改全局配置。

PR 应说明改了什么、为何需要、如何验证及仍未验证的部分。不要提交 `.cache/`、`.state/`、`work/`、虚拟环境、第三方依赖、渲染媒体或任何凭据。

## English quick guide

- Read AGENTS.md and SKILL.md; keep the catalog's role distinctions and manual-only update policy.
- Update the catalog entry and `tools/<id>/GUIDE.md` together. Pin an exact upstream commit and retain source/license references.
- Leave unexecuted tools as `not-run`; record only the actual scope of successful commands.
- Run the three checks above. Tests must remain local and independent of personal accounts.
- Explain the change, evidence, and limitations in the PR. Do not vendor upstream projects or commit local state, media, or credentials.

Contributions to original toolbox code and documentation are provided under this repository's MIT license; third-party material must retain its applicable license and attribution.
