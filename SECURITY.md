# Security policy / 安全政策

## Reporting

For a suspected vulnerability in this toolbox, use GitHub's private [Report a vulnerability](https://github.com/FeyZha/animation-toolbox/security/advisories/new) flow. Include the affected commit, a minimal reproduction, and the possible impact. Remove credentials and personal data from attachments.

Please do not publish exploit details or secrets in a public issue before the maintainer has assessed the report. Bugs in an upstream animation tool should be reported through that project's security policy.

The current `main` branch is maintained; older snapshots have no separate security maintenance commitment. Reports are handled on a best-effort basis without a guaranteed response time.

## 使用边界

- 本库是工具目录和执行入口，固定 commit 不代表第三方代码已经过安全审计。
- `fetch` 下载源码；`verify` 执行登记的命令。执行第三方代码前应确认其来源与本次任务授权，并使用适合该任务的隔离环境。
- 不把凭据、私人内容或全局配置写入目录、检查输出或提交中。
- 漏洞请走上面的私密报告入口；普通使用问题可以通过 Issues 提交。
