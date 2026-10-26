# 工作区恢复与服务器同步

2026-10-26 起采用“轻量工作区总仓＋manifest＋同步脚本”。总仓管理根目录入口、
公共脚本和四仓准确恢复版本；工程规则、任务、协议与验收证据仍以本控制仓为权威。
完整步骤和环境限制见根目录 [WORKSPACE.md](../../../WORKSPACE.md)。

## 当前恢复方式

在空父目录执行：

```bash
git clone --branch main ssh://git@192.168.77.113:2222/sushaohua/ai-soc-workspace.git ai_soc_project
cd ai_soc_project
python3 tools/workspace.py restore
python3 tools/workspace.py verify
```

2026-10-26 已实际创建并上传总仓，完成五仓普通推送及 SSH 克隆、准确提交恢复。
执行记录、初次发现的问题及修正后核对结果见[服务器发布证据](../evidence/20261026_gitlab_publication/README.md)。
本机提交和离线 bundle 恢复通过不代表服务器已同步。若服务器不可达，按 WORKSPACE.md 从五仓
离线包恢复。未配置 SSH 的新机器先配置允许访问该服务器的 SSH 认证。

`workspace.json` 锁定恢复 commit；本仓 `manifest.yaml` 保留工程基线与验证状态，
不能把历史基线当作最新备份提交。恢复保留 `mcu-p3` 的 `feat/soc-debug` 分支。
已有子目录只有在分支、commit 和干净状态都一致时复用，脚本不覆盖本机修改。

总仓排除四个子仓、凭据、构建缓存与离线传输包。根目录旧 `.agents/` 不是正式状态来源；
新机器恢复后缺少该目录时创建到本仓 `.agents/` 的相对符号链接。

## 提交、锁定与推送

先审阅并分别提交各仓改动，再运行：

```bash
python3 tools/workspace.py lock
bash tools/workspace_git.sh add workspace.json
bash tools/workspace_git.sh commit -m 'chore(workspace): pin repository checkpoints'
python3 tools/workspace.py publish
```

推送使用环境变量 `GITLAB_TOKEN`。GitLab API 查询/创建项目后，通过 HTTP(S) Git
逐仓推送并检查远端 SHA，最后上传总仓；不强制推送、不自动合并或自动提交。
真实 GitLab HTTP 入口可通过 `GITLAB_URL` 或 `--gitlab-url` 提供，令牌不写入 URL/文件。
`project-control/tools/push_to_server.sh` 在总仓脚本存在时转交该流程，否则保留旧四仓 SSH 推送方式。

## 历史材料

`workspace-root/*.snapshot`、旧交接和 `artifacts/server_sync_20261019/` 是之前的恢复材料。
原件保持追溯，后续根目录入口由总仓保存，不再要求刷新多份导出快照。
旧 bundle 只覆盖当批版本，不能当作后续全部工作或服务器上传证据。

恢复后读取[本地协议](../specs/README.md)和[独立工作区运行说明](standalone_workspace.md)。
知识库不作为构建或运行输入；硬件与 MCU 证据要求保持原任务约定。
