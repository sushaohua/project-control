# 去除 GitLab API 依赖（纯 Git/SSH 直连方案）与文档补齐实施方案

## 修订历史

| 版本 | 修订时间 | 修订人 | 变更摘要 | 审批状态 |
| :--- | :--- | :--- | :--- | :--- |
| v1.0 | 2026-11-17 15:45 | `AI (Antigravity-CLI)` | 初版方案：彻底移除 `tools/workspace.py` 与 `qa_runner.py` 对 GitLab REST API / `GITLAB_TOKEN` 的依赖，改用纯 Git/SSH 直连，并按分工补齐 `README.md` 与 `docs/WORKSPACE.md` | 已批准执行 |

---

## 1. 背景与目标

1. 在内网 GitLab 服务器变更 IP 或服务端 `external_url` 未同步更新时，依赖 `/api/v4/` REST API 的 `http_url_to_repo` 检查与 Token 鉴权反而导致 `publish` 失败或增加隐性耦合。
2. 根据用户最新要求：**彻底去掉对 GitLab API 的依赖，今后仅使用 GitLab 直连方案（Git SSH / 原生 Git 协议），不再允许使用 API**。
3. 同步按分工补齐工作区新建与运维文档：根 [README.md](file:///home/sushaohua/workspace/ai_soc_project/README.md) 补充精简“快速新建工作区”入口命令，[docs/WORKSPACE.md](file:///home/sushaohua/workspace/ai_soc_project/docs/WORKSPACE.md) 与 [docs/README.md](file:///home/sushaohua/workspace/ai_soc_project/docs/README.md) 补充完整范围与直连规范。

---

## 2. 经源码检索核实的修改清单

### A. 根工作区工具与配置（`ai-soc-workspace`）
1. [tools/workspace.py](file:///home/sushaohua/workspace/ai_soc_project/tools/workspace.py)：
   - 移除 `class GitLab`、`NoRedirect`、`urllib.request`、`urllib.error`、`redact`（`GITLAB_TOKEN`）、`GIT_ASKPASS`（`tools/gitlab_askpass.py`）与 `--gitlab-url` 参数。
   - 在 `load_manifest` 中支持并校验 `workspace_project.url`（使用 `safe_url`）；如旧清单未配置 `workspace_project.url`，在 `publish` 时回退读取根仓本地 `remote.origin.url`（拒绝猜测或调用 API）。
   - `publish(root, data)` 直接逐仓通过 `push_one` 推送至 `repo["url"]` 及 `repo.get("mirror_urls", [])` 并执行 `git ls-remote` SHA 核验；随后推送根入口仓至 `workspace_project` 的直连 URL（及可选 `mirror_urls`）并核验 SHA。不再读取 `GITLAB_TOKEN`、不再访问 `/api/v4/`、不再自动通过 API 创建缺失项目（目标项目需已在 GitLab 服务端存在且具备 SSH 推送权限）。
   - 若旧版 `workspace.json` 仍残留已废弃的 `gitlab_url` 字段，加载时允许忽略或直接从本工作区 `workspace.json` 移除。
2. [tools/gitlab_askpass.py](file:///home/sushaohua/workspace/ai_soc_project/tools/gitlab_askpass.py)：全仓检索仅被 `tools/workspace.py:284` 引用，一并删除（`git rm`）。
3. [workspace.json](file:///home/sushaohua/workspace/ai_soc_project/workspace.json)：移除顶层 `"gitlab_url"`，在 `"workspace_project"` 中显式登记 `"url": "ssh://git@192.168.77.79:2222/sushaohua/ai-soc-workspace.git"`。
4. [tools/test_workspace.py](file:///home/sushaohua/workspace/ai_soc_project/tools/test_workspace.py)：
   - 删除 `test_api_creates_private_project_in_exact_namespace` 与 `test_existing_project_is_reused_without_creation`（原 GitLab API 单测）；
   - 更新 `test_publish_pushes_to_gitlab_and_mirror_urls` 为纯 Git 直连推送测试（无 `GITLAB_TOKEN`、无 `GitLab` mock）；
   - 新增负向/边界校验用例：无 `GITLAB_TOKEN`、无 HTTP 服务时直连 `publish` 正常工作，且工具内不再存在任何 HTTP API 调用或 `gitlab_askpass` 依赖。
5. [README.md](file:///home/sushaohua/workspace/ai_soc_project/README.md)、[docs/WORKSPACE.md](file:///home/sushaohua/workspace/ai_soc_project/docs/WORKSPACE.md)、[docs/README.md](file:///home/sushaohua/workspace/ai_soc_project/docs/README.md)：
   - `README.md`：新增“快速新建工作区”小节（前置条件 + 4 行 `clone -> restore -> verify` 命令 + 指向 `docs/WORKSPACE.md`）。
   - `docs/WORKSPACE.md`：修正 L73（7 个普通仓 + `sdk/c308l` 56 项 SDK + 相对软链接）、明确 `repo` CLI 亦为 `status`/`verify`/`lock` 必需、补充 `restore` 后 `agents` 手动双推 GitHub 的 `pushurl` 配置方法、移除 `GITLAB_TOKEN`/`--gitlab-url`/API 自动建仓说明并改为纯 GitLab SSH 直连发布说明。
   - `docs/README.md`：更新 L13 描述（覆盖 7 仓与 C308L SDK）。

### B. 控制仓独立 QA 运行器（`project-control`）
1. [project-control/tools/qa_runner/qa_runner.py](file:///home/sushaohua/workspace/ai_soc_project/project-control/tools/qa_runner/qa_runner.py)：
   - 彻底移除 `class GitLabClient`、`verify_server_commit`（REST API v4）、`redact_token`（`GITLAB_TOKEN`）、`urllib.request` / `urllib.error` API 调用以及 `self.gitlab` / `self.gitlab_url` / `self.api_timeout`。
   - `verify_server_prerequisites()` 改为纯 SSH 连通性核验（`check_ssh_connection`，返回 `{"auth_mode": "ssh-git", "ssh_connected": ssh_ok}`）；
   - `verify_target_commits(targets)` 改为纯 Git/SSH 直连核验：先校验 SSH 连通性与每项目 SHA/URL，并通过 `git ls-remote <url> <ref>` 与随后 `checkout_remote_repository` 的真实服务端拉取校验目标提交可达（拒绝未推送的本地哈希，且全过程严格遵守函数 `≤50` 行、`≤4` 参数与中文文档字符串规范）。
2. [project-control/config/qa_runner/default_config.yaml](file:///home/sushaohua/workspace/ai_soc_project/project-control/config/qa_runner/default_config.yaml)：
   - 移除 `server.gitlab_url`、`server.api_timeout_seconds` 及各仓 `api_project_path` 字段，仅保留 `ssh_host`、`ssh_port`、`ssh_user` 与各仓 SSH `url`。
3. [project-control/tools/test_qa_runner.py](file:///home/sushaohua/workspace/ai_soc_project/project-control/tools/test_qa_runner.py)：
   - 将原 `GitLabClient` / `verify_server_commit` 测试替换为纯 SSH 与 `verify_target_commits`（`git ls-remote` / SSH 失败熔断）单元测试；保留 `MethodologicalInvariantsTest` AST 规模校验。

---

## 3. 最小修改预算 (Diff Budget)

| 仓库 | 修改文件 | 预估行数 | 角色边界 |
| :--- | :--- | :--- | :--- |
| 根仓 (`ai-soc-workspace`) | `tools/workspace.py`、`tools/test_workspace.py`、`tools/gitlab_askpass.py`（删除）、`workspace.json`、`README.md`、`docs/WORKSPACE.md`、`docs/README.md` | 增删合计 ≤ 180 行 | 工作区治理维护 |
| `project-control` | `tools/qa_runner/qa_runner.py`、`tools/test_qa_runner.py`、`config/qa_runner/default_config.yaml`、本方案原件 | 增删合计 ≤ 140 行（不含本方案） | `COORD` |
| 业务仓 / `agents` / `sdk/c308l` | **0 修改** | 0 行 | 只读保持 |

---

## 4. 验收标准与实施步骤

1. **Slice-01（`project-control` 去 API 化与单测）**：修改 `qa_runner.py`、`test_qa_runner.py`、`default_config.yaml`，运行 `python3 -m pytest -o cache_dir=/tmp/pytest_v2_cache project-control/tools/test_qa_runner.py -v` 要求全绿（含 AST 规模与入参门禁）。
2. **Slice-02（根仓去 API 化与文档更新）**：修改 `tools/workspace.py`、删除 `tools/gitlab_askpass.py`、更新 `tools/test_workspace.py`、`workspace.json`、`README.md`、`docs/WORKSPACE.md`、`docs/README.md`；运行 `python3 -m unittest discover -s tools -p 'test_workspace.py' -v` 全通。
3. **Slice-03（全工作区校验与代码审计）**：
   - 运行 `python3 tools/workspace.py verify` 与 `python3 test_harness/static_checks/platform/check_platform_inputs.py --workspace .` 全通；
   - `grep` 核验 `tools/`、`workspace.json`、`qa_runner.py`、`default_config.yaml` 中不再包含 `/api/v4`、`GitLabClient`、`GITLAB_TOKEN`、`gitlab_askpass`。
4. **Slice-04（线性对齐提交与推送）**：在 `project-control` 与根仓 `ai-soc-workspace` 分别 `fetch + rebase` 对齐 `origin/main` 后提交并直连推送 `192.168.77.79`（若一并批准推送）。

### 回滚预案
- 若任一单测或 AST 门禁报错立即 Fail-Fast 停机，通过 `git checkout` / `git rebase --abort` 无损保留现场与回退。

---

## 5. 审批闸门

请审阅上述方案并回复 **“批准执行”**（并确认是否在测试全通后直接提交并推送 `project-control` 与根仓至 `192.168.77.79`）。
