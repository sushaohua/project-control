# GitLab IP 迁移（192.168.77.113 → 192.168.77.79）、`agents` 双 Git 同步与子项目对齐实施方案

## 修订历史

| 版本 | 修订时间 | 修订人 | 变更摘要 | 审批状态 |
| :--- | :--- | :--- | :--- | :--- |
| v1.0 | 2026-11-17 11:44 | `AI (Antigravity-CLI)` | 初版方案：覆盖全工作区 GitLab 地址迁移、`agents` 双 Git 配置与双端同步、`printer-soc` / `sdk/c308l` 对齐决策及验收回滚方案 | 已批准执行（采用选项 B） |

---

## 1. 背景与目标

1. 内网 GitLab 服务器地址已从 `192.168.77.113` 变更为 `192.168.77.79`（已实测 `http://192.168.77.79/api/v4/version` 与 `/api/v4/user` 返回 HTTP 200，SSH 2222 端口 `git ls-remote` 正常）。
2. `agents` 仓库需要落地**双 Git 维护**并在 GitLab（`ssh://git@192.168.77.79:2222/sushaohua/agents.git`）与 GitHub（`git@github.com:sushaohua/agents.git`）之间完成双向同步。
3. 需要检查并更新工作区（`ai-soc-workspace`）下涉及旧 GitLab 地址的所有现役配置文件、规则、文档、脚本、测试与本地 Git remote URL，同时对齐各子项目状态并确保 `python3 tools/workspace.py verify` 与单元测试全部通过。

---

## 2. 物理核查现状（已实测）

### 2.1 远端与本地各仓版本对比（相对 `192.168.77.79`）

| 仓库 / 客户端 | 分支 | 本地 `HEAD` | GitLab (`192.168.77.79`) | GitHub 镜像 | 状态与差异说明 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 根仓 (`ai-soc-workspace`) | `main` | `227254a250` | `227254a250` | — | 一致；`.workspace-git/config` `origin` 仍指向 `77.113` |
| `project-control` | `main` | `5385510356` | `5385510356` | — | 一致；`.git/config` `origin` 仍指向 `77.113` |
| `agents` | `main` | `30ecc6586a` | `19894de480` | `30ecc6586a` | 本轮已从 GitHub 快进本地 `b8c1c6d -> 30ecc65`；GitLab 落后 2 个提交（`b8c1c6d`、`30ecc65`）；`agents/.git/config` 仅配 `origin=github`，缺 GitLab 远端 |
| `printer-soc` | `main` | `d9278c5269` | `b0ca37c0f5` | — | **GitLab 领先 1 个提交** `b0ca37c0`（`feat(ui): vendor HelixScreen v1.0.9 sources`）；本地未快进 |
| `mcu-p3` | `feat/soc-debug` | `b865222c5e` | `b865222c5e` | — | 一致；仅本地 `origin` URL 为 `77.113` 且跟踪引用滞后 |
| `test_harness` | `main` | `3eef26a98a` | `3eef26a98a` | — | 一致；仅本地 `origin` URL 为 `77.113` |
| `boot/bootloadermc` | `soc_debug` | `3e01c00ce4` | `3e01c00ce4` | — | 一致；仅本地 `origin` URL 为 `77.113` 且跟踪引用滞后 |
| `boot/bootloaderth` | `soc_debug` | `c56ae6fa36` | `c56ae6fa36` | — | 一致；仅本地 `origin` URL 为 `77.113` 且跟踪引用滞后 |
| `sdk/c308l` (Repo 客户端) | — | 57 项干净 | `manifests.git` @ `0f37f765` | — | 缺 `AGENTS.md` / `.agents` 软链接；57 个子项目及 `.repo/manifests` `origin` 均为 `77.113`；`default.xml` 仍为 `77.113` + 57 项（含 `helixscreen`） |

### 2.2 涉及 `192.168.77.113` 的文件精确清单

#### A. 根工作区（`ai-soc-workspace`，现役配置与文档）
- [workspace.json](file:///home/sushaohua/workspace/ai_soc_project/workspace.json)（L8, L13, L19, L28, L35, L43, L50, L58, L68）：`gitlab_url`、7 个普通仓 `url`、`repo_clients[0].manifest_url`（以及对应仓库的最新锁定 `commit` / `lock_sha256`）。
- [docs/WORKSPACE.md](file:///home/sushaohua/workspace/ai_soc_project/docs/WORKSPACE.md)（L4, L28, L76）：工作区总仓、`manifest_url` 与恢复克隆示例地址。
- 注：[docs/HANDOFF_20261116.md](file:///home/sushaohua/workspace/ai_soc_project/docs/HANDOFF_20261116.md)（L22）属于 2026-11-16 已结项会话交接历史记录，保持原样不篡改。

#### B. `project-control/`（现役配置、规则、运行器与测试）
- [project-control/config/qa_runner/default_config.yaml](file:///home/sushaohua/workspace/ai_soc_project/project-control/config/qa_runner/default_config.yaml)（L3, L4, L19, L23, L27, L31, L35, L39, L43, L69）：`gitlab_url`、`ssh_host`、7 仓 `url` 及 `repo_clients[0].manifest_url`。
- [project-control/tools/qa_runner/qa_runner.py](file:///home/sushaohua/workspace/ai_soc_project/project-control/tools/qa_runner/qa_runner.py)（L694, L695）：`gitlab_url` 与 `ssh_host` 默认兜底值。
- [project-control/tools/test_qa_runner.py](file:///home/sushaohua/workspace/ai_soc_project/project-control/tools/test_qa_runner.py)（L86, L87, L98, L99, L112, L135, L226, L252）：单元测试夹具与断言 URL/主机名（保持与运行器一致）。
- [project-control/manifest.yaml](file:///home/sushaohua/workspace/ai_soc_project/project-control/manifest.yaml)（L8, L15, L21, L54, L67, L80, L87）：各受管仓远端 URL。
- [project-control/.agents/rules/bootloader_role_boundaries.md](file:///home/sushaohua/workspace/ai_soc_project/project-control/.agents/rules/bootloader_role_boundaries.md)（L18, L19）：Bootloader 远端仓库地址。
- 注：`project-control/docs/` 下的历史验收证据与既有规划方案保持历史原样不篡改。

#### C. `agents/`
- 现役规则与技能（`agents/AGENTS.md` 及六个活动 `agents_subdir` 的 `.agents/` 与 `AGENTS.md`）中 **0 处**引用 `192.168.77.113`；历史交接/归档文档（`agents/*/docs/`）保持原样。
- 需要更新的是本地仓库 `agents/.git/config` 的双远端配置（见 §3.1）。

#### D. `boot/bootloadermc/`
- [boot/bootloadermc/README.md](file:///home/sushaohua/workspace/ai_soc_project/boot/bootloadermc/README.md)（L65, L71）包含历史名 `bootloader435.git` 的克隆命令示例。按角色边界，`COORD` 不直接修改业务仓；若需同步更新，须由 `ENG_BOOT_MC` 在 `soc_debug` 分支小改（可在本轮决定是否纳入）。

#### E. 本地 Git 元数据（`.git/config` / `.workspace-git/config`，不入库但决定日常 `git fetch/push`）
- 根仓 `.workspace-git/config` 及 6 个 GitLab 托管子仓（`project-control`、`printer-soc`、`mcu-p3`、`test_harness`、`boot/bootloadermc`、`boot/bootloaderth`）的 `remote.origin.url` 需从 `192.168.77.113` 更新为 `192.168.77.79` 并执行 `git fetch origin`。
- `sdk/c308l/.repo/manifests` 及 `sdk/c308l/.repo/projects/**`（57 项）的 `remote.origin.url` 也全部指向 `192.168.77.113`。

---

## 3. 关键技术推演与待确认决策点

### 3.1 `agents` 双 Git 维护方案
当前 `workspace.json` 为 `agents` 定义了：
- 主地址 `url`: `ssh://git@192.168.77.79:2222/sushaohua/agents.git`
- 镜像 `mirror_urls`: `["git@github.com:sushaohua/agents.git"]`

为使本地直接在 `agents/` 内操作与 `workspace.py publish` 行为完全一致，拟将 `agents/.git/config` 配置为双远端：
- `origin`: `ssh://git@192.168.77.79:2222/sushaohua/agents.git`（作为主拉取源，并保留/配置双 `pushurl`：`ssh://git@192.168.77.79:2222/sushaohua/agents.git` 与 `git@github.com:sushaohua/agents.git`，同时另设独立 remote `github` 指向 `git@github.com:sushaohua/agents.git` 便于单独 `fetch github`）；
- 先 `git -C agents fetch origin` 验证 GitLab `19894de` 是本地 `30ecc65` 的严格祖先（无分叉），再推送 `30ecc65` 至 GitLab `main`，并双向 `git ls-remote` 校验 GitLab 与 GitHub 均停在 `30ecc6586a861c1543a97804cfe0600bb4778efb`。

### 3.2 `printer-soc@b0ca37c0` 与 `sdk/c308l` 门禁一致性冲突（⚠️ 需拍板）
实测 `printer-soc` 远端最新提交 `b0ca37c0`（`feat(ui): vendor HelixScreen v1.0.9 sources`）中：
1. `boards/c308l-aw419/sdk/manifest.lock.xml` 已把 `<remote fetch=...>` 改为 `192.168.77.79`，且移除了 `<project name="helixscreen" .../>`（56 项，`SHA256 = ea8f4eec4425f1624af05a2cfc529c621006f2feb40b6b0bc1fa254b3312e13e`）。
2. 但远端 `ssh://git@192.168.77.79:2222/software/soc/amc308l/manifests.git` 仍停在 `0f37f765`（其 `default.xml` 仍写 `192.168.77.113` 且含 `helixscreen` 57 项）；且 [sdk_workspace.py](file:///home/sushaohua/workspace/ai_soc_project/tools/sdk_workspace.py) 的 `verify_sdk` 会执行 `repo manifest -r` 严格比对 `remotes` 与 56/57 项清单。

因此存在两种处置方式，请确认选型：
- **选项 A（同步 `printer-soc` 到 `b0ca37c0` 并先更新清单与软链接，暂保持 `sdk/c308l` 等待平台更新 `amc308l/manifests.git`）**：
  - 将本地 `printer-soc` 快进至 `b0ca37c0`，同步更新 `workspace.json` 与 `project-control/config/qa_runner/default_config.yaml` 中的 `lock_sha256` 为 `ea8f4eec...`，同时批量更新 `sdk/c308l` 本地 57 项 `.git/config` 远端为 `192.168.77.79` 并补齐 `sdk/c308l/AGENTS.md`、`.agents` 软链接。
  - **注意**：在 `software/soc/amc308l/manifests.git` 尚未更新提交以移除 `helixscreen` 并改 `192.168.77.79` 前，`python3 tools/workspace.py verify` 对 `sdk/c308l` 校验会报 `SDK 有效 manifest 与产品锁不一致`（`tools/workspace.py lock` 也会因此拒绝写锁，需直接编辑 `workspace.json` 对应字段）。若您有权限并希望我方一并更新 `sdk/c308l/.repo/manifests`（需单独授权 `ENG-PLATFORM` 变更 `amc308l/manifests.git`）则可一次性让 `verify` 全绿。
- **选项 B（仅迁移 IP 与同步 `agents`，`printer-soc` 暂保留在 `d9278c5`）**：
  - 先把所有 `192.168.77.113` 迁至 `192.168.77.79`、完成 `agents` 双端同步并锁定 `agents` 为 `30ecc65`，`printer-soc` 暂不快进到 `b0ca37c0`。
  - 但因远端 `amc308l/manifests.git@0f37f765` 的 `default.xml` 仍含 `192.168.77.113`，且 `printer-soc@d9278c5` 的 `manifest.lock.xml` 也含 `192.168.77.113`，`workspace.json` 内 `manifest_url` 改为 `77.79` 后，只要 `sdk/c308l/.repo/manifests` 的 `remote.origin.url` 同步改为 `77.79`，`verify_sdk` 即可通过（仅 `default.xml` 内 `<remote fetch>` 与 `manifest.lock.xml` 仍同为 `77.113` 保持自洽）。

---

## 4. 最小修改预算 (Diff Budget)

| 仓库 / 范围 | 允许修改文件 | 预估行数 | 角色边界 |
| :--- | :--- | :--- | :--- |
| 根仓 (`ai-soc-workspace`) | `workspace.json`、`docs/WORKSPACE.md` | ≤ 40 行 | 工作区治理维护 |
| `project-control` | `config/qa_runner/default_config.yaml`、`manifest.yaml`、`tools/qa_runner/qa_runner.py`、`tools/test_qa_runner.py`、`.agents/rules/bootloader_role_boundaries.md`、本方案原件 | ≤ 80 行（不含本方案） | `COORD` |
| `agents` | 仅 Git remote 配置与同步推送，**0 代码/文档文件改动** | 0 行 | 仓级 Git 同步 |
| `printer-soc`（若选方案 A） | 仅 fast-forward 至 `b0ca37c0`，**0 手工文件改动** | 0 行 | 仓级 Git 同步 |
| 各仓本地 `.git/config` | 更新 `remote.origin.url`（含根仓及可选 `sdk/c308l`）；补齐 `sdk/c308l` 缺失软链接 | 非跟踪本地配置 | 环境对齐 |
| `boot/bootloadermc`（可选） | `README.md` L65, L71（仅在明确授权时委派 `ENG_BOOT_MC` 修改） | 2 行 | `ENG_BOOT_MC` |

---

## 5. 有序实施步骤与验收标准

1. **Slice-01（GitLab `agents` 双远端配置与双端同步）**：
   - 配置 `agents` 远端：`origin` = `ssh://git@192.168.77.79:2222/sushaohua/agents.git`（双 `pushurl` 同时指向 GitLab 与 GitHub）+ `github` = `git@github.com:sushaohua/agents.git`。
   - `git -C agents fetch origin` 核对线性祖先关系并推送 `30ecc65` 至 GitLab `main`；`git ls-remote` 验证两端均为 `30ecc6586a861c1543a97804cfe0600bb4778efb`。
2. **Slice-02（全工作区本地 Git remote 迁移与上游对齐）**：
   - 将根仓 `.workspace-git` 及 6 个 GitLab 子仓 `remote.origin.url` 全部切换为 `192.168.77.79` 并 `fetch origin` 刷新跟踪引用；按选定方案处理 `printer-soc`（保留 `d9278c5` 或快进 `b0ca37c0`）与 `sdk/c308l` 软链接 / remote URL。
3. **Slice-03（`project-control` 现役 IP 替换与校验）**：
   - 将 §2.2.B 列出的 5 个文件内 `192.168.77.113` 更新为 `192.168.77.79`（若选方案 A 同步更新 `default_config.yaml` 中 `lock_sha256`）。
   - 执行 `python3 -m pytest -o cache_dir=/tmp/pytest_v2_cache project-control/tools/test_qa_runner.py project-control/tools/test_v2_gates.py -q` 验证全通。
4. **Slice-04（根仓 `workspace.json` 与 `docs/WORKSPACE.md` 更新及单测）**：
   - 更新 [workspace.json](file:///home/sushaohua/workspace/ai_soc_project/workspace.json) 与 [docs/WORKSPACE.md](file:///home/sushaohua/workspace/ai_soc_project/docs/WORKSPACE.md) 中的 GitLab 地址及 `agents` 锁定 SHA（`30ecc65...`）。
   - 执行 `python3 -m unittest discover -s tools -p 'test_workspace.py' -v` 与 `python3 tools/workspace.py verify`（按所选方案确认状态）。
5. **Slice-05（可选提交与远端推送）**：
   - 仅在用户明确要求提交推送时，按线性历史提交 `project-control` 与根仓改动并执行 `python3 tools/workspace.py publish`。

### 回滚预案
- 任一步骤失败（如变基冲突、SHA 不匹配或测试失败）立即 Fail-Fast 停机保留现场；
- 未提交前可通过 `git checkout -- <file>` 及恢复原 `remote.origin.url` 无损回滚，不执行任何强制覆盖或 `--force` 推送。

---

## 6. 审批闸门

请用户确认以下两项后回复 **“批准执行”**：
1. 对 `printer-soc@b0ca37c0` 与 `sdk/c308l` 选用 **选项 A**（同步 `printer-soc` 到 `b0ca37c0`，同时确认是否授权一并处理 `amc308l/manifests.git`）还是 **选项 B**（`printer-soc` 暂留 `d9278c5` 保持 `verify` 绿灯，仅完成 IP 迁移与 `agents` 双 Git 同步）；
2. 是否需要委派 `ENG_BOOT_MC` 一并修改 [boot/bootloadermc/README.md](file:///home/sushaohua/workspace/ai_soc_project/boot/bootloadermc/README.md) 中的旧地址，以及是否在本地修改并验证通过后直接提交并推送远端。
