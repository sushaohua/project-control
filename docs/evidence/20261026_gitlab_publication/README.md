# 2026-10-26 GitLab 工作区发布与服务器恢复执行记录

本记录是用户授权的仓库发布与恢复操作证据，不是工程任务 QA 签署。既有独立审查记录、任务状态、MCU/HIL 门禁均保留；没有启动或冒充新的独立 QA 会话。

## 结果与版本

- 工作区：`/home/sushaohua/workspace/ai_soc_project`；开始时五仓均干净，总仓为 `a772a4880ac2d2e8cedfe34af29c1d28576b6843`。
- API：`http://192.168.77.113/api/v4/user`，使用环境变量 `GITLAB_TOKEN` 的 `PRIVATE-TOKEN` 请求头，实际 HTTP 200，用户 `sushaohua`。
- 首次发布创建 private 总仓 `sushaohua/ai-soc-workspace`，复用四个现有子仓。原有 `mcu-p3` 可见性为 internal，其他四仓为 private，未调整现有项目可见性。
- 推送前通过真实 HTTP Git fetch 核对远端历史，四个目标远端提交均为本地检查点的祖先或相同提交。全部采用普通推送，无强制推送、变基或覆盖远端分支。
- 总仓经 SSH `192.168.77.113:2222` 克隆到新的临时目录，`restore` 使用清单中的 SSH URL 下载四仓，没有使用本地 bundle。
- 修正后的服务器候选：总仓 `a7f4f33c185c8aa4334628c2a6229f0fe377b3b3`；实际恢复目录 `/tmp/ai-soc-gitlab-publication-20261026T164656/fixed-restored`。
- `restore`、`verify` 退出 0；补充比对五仓 commit/tree、分支及工作区干净状态，API 远端分支 SHA、总仓入口文件、57 个权威 `.agents` 文件 SHA256 均匹配。
- 根目录 `.agents` 为相对链接 `project-control/.agents`；`V2-P01D` 内容哈希一致且仍为 `InProgress`。没有把保存代码变成任务验收。

| 项目 | 分支 | 本记录实际验证提交 |
| --- | --- | --- |
| [ai-soc-workspace](http://192.168.77.113/sushaohua/ai-soc-workspace) | main | a7f4f33c185c8aa4334628c2a6229f0fe377b3b3 |
| [project-control](http://192.168.77.113/sushaohua/project-control) | main | 2b84bbfefca513973bb13726f45d2102d45e9bce |
| [soc-ap](http://192.168.77.113/sushaohua/soc-ap) | main | 849135ee69500e7e96ee75eed73c245e1ac94851 |
| [mcu-p3](http://192.168.77.113/sushaohua/mcu-p3) | feat/soc-debug | 14b8057b04030bd659744c874c73ff8f09f29979 |
| [test_harness](http://192.168.77.113/sushaohua/test_harness) | main | 59d2320663dd7ef4a080272d624f831684935c34 |

## 执行证据与问题

JSON 日志包含实际 cwd、命令、开始/结束时间、退出码、stdout/stderr。令牌不写入 URL、参数或记录，捕获器额外脱敏令牌值。`SHA256SUMS` 用于核对本目录归档文件，不代表独立审核。

- `01-preflight.json`：认证、五仓原始状态、真实远端 fetch 和祖先关系。
- `02-verify.json`、`03-publish.json`：首次本地清单检查与实际五仓发布。
- `04-clone-ssh.json`、`05-restore-ssh.json`、`06-restored-verify.json`：首次服务器 SSH 克隆与四仓准确恢复，均退出 0。
- `07-server-audit.json`：补充检查发现总仓存在未跟踪 `.agents` 链接；原 `.gitignore` 的 `/.agents/` 只匹配目录，未忽略生成的符号链接。
- 总仓提交 `a7f4f33` 将规则改为 `/.agents`，保留已有本地目录及恢复时的链接；同时更新 HTTP 入口的已验证状态。
- `08-publish-ignore-fix.json`：普通推送修正后的总仓，逐仓核对远端 SHA。
- `09-fixed-server-roundtrip.json`：重新 SSH 克隆、restore、verify 均退出 0；临时补充检查器因 Python 3.8 无 `Path.readlink` 而失败。
- `10-fixed-server-audit.json`：补充检查器处理 Git 引号包裹的中文路径失败；修为 `os.readlink` 及 `git ls-files -z`。这两项属于本次临时取证脚本，不是仓库发布脚本或恢复实现失败。
- `11-fixed-server-audit.json`：修正后的补充检查退出 0，记录五仓远端 SHA、57 个权威文件哈希及 InProgress 状态。
- 同步实现 `tools/workspace.py` 未修改，已有 8 项工具测试沿用历史原始记录，本轮没有冒称重新运行。此次针对忽略规则修正实际进行了服务器克隆与恢复复查。

## 归档后的检查点与边界

本文绑定上表已经真实恢复的候选。将本记录提交到控制仓后，会更新根目录 `workspace.json`，再次普通发布，并在新的临时目录对归档后的最终检查点执行完整服务器克隆、restore、verify 和补充核对。
最终发布及恢复的原始回执保存在工作区 `artifacts/gitlab_publication_20261026/` 和本轮 `/tmp/ai-soc-gitlab-publication-20261026T164656/`；总仓忽略 artifacts。最终 HEAD 以当前已提交的 `workspace.json` 及这些回执为准，不能将本表的较早候选当成最终控制仓记录提交。

本轮没有执行 MCU 构建、AP 协议功能测试、VMware/HIL 或新的工程独立 QA，没有推进正式任务状态。历史网络失败证据保留，已由本次真实服务器成功记录补充。
