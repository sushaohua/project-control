# C308L SDK 清单（`amc308l/manifests.git`）与 `printer-soc@b0ca37c0` 对齐实施方案

## 修订历史

| 版本 | 修订时间 | 修订人 | 变更摘要 | 审批状态 |
| :--- | :--- | :--- | :--- | :--- |
| v1.0 | 2026-11-17 14:48 | `AI (Antigravity-CLI)` | 初版方案：按“议题A：方式1”更新 `amc308l/manifests.git`、`sdk/c308l`、`project-control` 契约/配置与根工作区版本锁 | 已批准执行 |

---

## 1. 背景与目标

`printer-soc` 已快进至远端最新提交 `b0ca37c0f5fdb6c849a3da4a1393b3336e809b2f`（`feat(ui): vendor HelixScreen v1.0.9 sources`），其 [boards/c308l-aw419/sdk/manifest.lock.xml](file:///home/sushaohua/workspace/ai_soc_project/printer-soc/boards/c308l-aw419/sdk/manifest.lock.xml) 已将远端改为 `ssh://git@192.168.77.79:2222/software/soc/amc308l` 并移除 `craftdance/helixscreen`（56 项，SHA-256 为 `ea8f4eec4425f1624af05a2cfc529c621006f2feb40b6b0bc1fa254b3312e13e`）。

当前 `192.168.77.79` 上的 `software/soc/amc308l/manifests.git`（`0f37f765bdb963d129891e25dda549d6debd4931`）与本地 `sdk/c308l` 仍停留在 `192.168.77.113` 与 57 项（含 `craftdance/helixscreen`）。本方案按用户选定的 **议题A：方式1** 完成平台清单、本地 SDK、治理契约与根工作区版本锁的全链路对齐。

---

## 2. 经代码/Git 核实的影响范围与文件清单

1. **平台清单仓（`ssh://git@192.168.77.79:2222/software/soc/amc308l/manifests.git`，`master` 分支，权限已核实为 Group Owner level 50）**：
   - `default.xml`（L3, L84）：`<remote fetch>` 由 `192.168.77.113` 改为 `192.168.77.79`，移除 `<project name="helixscreen" path="craftdance/helixscreen" .../>`（其余 56 项项目与 `manifest.lock.xml` 100% 一致，已物理比对）。
   - `README.md`（L7, L10）：同步将 `192.168.77.113` 更新为 `192.168.77.79`。
2. **本地 SDK 客户端（[sdk/c308l](file:///home/sushaohua/workspace/ai_soc_project/sdk/c308l)）**：
   - 核对 [sdk/c308l/craftdance/helixscreen](file:///home/sushaohua/workspace/ai_soc_project/sdk/c308l/craftdance/helixscreen) 工作树完全干净且位于锁定基线 `910dba53c0ad2f833678bc226f6331242fb6bef0`（已实测）。
   - 更新 `.repo/local_manifests/workspace-lock.xml`（移除 `helixscreen` `<extend-project>` 项，保留 56 项）。
   - 通过 `repo init -u ssh://git@192.168.77.79:2222/software/soc/amc308l/manifests.git -b <NEW_MANIFEST_COMMIT> -m default.xml --manifest-upstream-branch master --depth=1 --no-clone-bundle --no-tags` 与 `repo sync` 对齐新清单，并确保 `sdk/c308l/craftdance/helixscreen` 残留目录已从工作树移除（避免触发 `sdk_workspace.py` `_check_unmanaged` 拒绝未登记文件）。
3. **跨仓治理仓（[project-control](file:///home/sushaohua/workspace/ai_soc_project/project-control)）**：
   - [project-control/config/qa_runner/default_config.yaml](file:///home/sushaohua/workspace/ai_soc_project/project-control/config/qa_runner/default_config.yaml)（L70, L75）：更新 `manifest_commit` 为新清单提交 SHA，`lock_sha256` 为 `ea8f4eec4425f1624af05a2cfc529c621006f2feb40b6b0bc1fa254b3312e13e`。
   - [project-control/contracts/c308l_platform_contract.yaml](file:///home/sushaohua/workspace/ai_soc_project/project-control/contracts/c308l_platform_contract.yaml)（L32）：移除已退出 SDK 的 `craftdance/helixscreen: ENG-AP` 条目，使 `project_owners` 与 56 项有效 SDK 路径保持一一对应。
   - 本方案原件归档。
4. **根工作区（`ai-soc-workspace`）**：
   - [workspace.json](file:///home/sushaohua/workspace/ai_soc_project/workspace.json)：更新 `repo_clients[0].manifest_commit` 与 `repo_clients[0].lock_sha256`，并通过 `python3 tools/workspace.py lock` 锁定 `printer-soc@b0ca37c0...` 与更新后的 `project-control` 提交。

---

## 3. 最小修改预算 (Diff Budget)

| 仓库 | 允许修改文件 | 预估行数 | 角色边界 |
| :--- | :--- | :--- | :--- |
| `amc308l/manifests.git` (`master`) | `default.xml`、`README.md` | ≤ 10 行 | `ENG-PLATFORM`（平台清单维护） |
| `project-control` (`main`) | `config/qa_runner/default_config.yaml`、`contracts/c308l_platform_contract.yaml`、本方案原件 | ≤ 15 行（不含本方案） | `COORD` |
| 根工作区 (`ai-soc-workspace`, `main`) | `workspace.json` | ≤ 10 行 | 工作区治理维护 |
| `printer-soc` / MCU / Boot / `agents` / `test_harness` | **0 修改** | 0 行 | 只读保持 |

---

## 4. 有序实施步骤与验收标准

1. **Slice-01（更新并推送 `amc308l/manifests.git`）**：
   - 在隔离工作目录（不引入到 `sdk/c308l` 或根工作区源码树）完整克隆 `ssh://git@192.168.77.79:2222/software/soc/amc308l/manifests.git`（`master`），修改 `default.xml` 与 `README.md`，提交 Conventional Commit 并推送 `master`，用 `git ls-remote` 确认 `<NEW_MANIFEST_COMMIT>`。
2. **Slice-02（对齐本地 `sdk/c308l`）**：
   - 复查 `sdk/c308l/craftdance/helixscreen` 无未提交修改后，更新 `.repo/local_manifests/workspace-lock.xml` 移除 `helixscreen`；执行 `repo init` 指向 `<NEW_MANIFEST_COMMIT>` 与 `repo sync`；确认 `sdk/c308l/craftdance/helixscreen` 已清理、56 项提交无变化、`AGENTS.md`/`.agents` 软链接完好。
3. **Slice-03（更新 `project-control` 配置与平台契约）**：
   - 更新 `default_config.yaml` 与 `c308l_platform_contract.yaml`，运行 `python3 -m pytest -o cache_dir=/tmp/pytest_v2_cache project-control/tools/test_qa_runner.py -v` 验证通过，本地提交 `project-control`。
4. **Slice-04（更新根工作区锁与全链校验）**：
   - 更新 `workspace.json` 中 `repo_clients[0]` 的 `manifest_commit` 与 `lock_sha256`，执行 `python3 tools/workspace.py lock`；
   - 执行以下验收命令并要求全部通过：
     - `python3 tools/workspace.py verify`（退出 0，7 仓 + 56 个 SDK 项全部 `dirty: false`）
     - `python3 test_harness/static_checks/platform/check_platform_inputs.py --workspace .`（输出 `"passed": true`, `"scope": "software-inputs"`）
     - `python3 -m unittest discover -s tools -p 'test_workspace.py' -v`（全部 `ok`）
   - 本地提交根仓 `workspace.json`。
5. **Slice-05（远端推送，可选）**：
   - 若用户一并批准远端发布，按顺序通过 SSH 推送 `project-control` 与根仓 `ai-soc-workspace` 至 `192.168.77.79` 并 `ls-remote` 核验。

### 回滚预案
- 任一步骤失败立即停机保留现场；`amc308l/manifests.git` 原提交 `0f37f765` 与 `printer-soc` 原锁定提交均保留在 Git 历史中，可通过重新锁定或回退未推送本地提交无损恢复，严禁 `--force` 推送。

---

## 5. 审批闸门

请审阅上述方案并确认：
1. 是否批准执行（含更新并推送 `amc308l/manifests.git` `master`、清理干净的 `sdk/c308l/craftdance/helixscreen`、更新 `project-control` 与根 `workspace.json`）；
2. 本地全链 `verify` 与 `check_platform_inputs.py` 全部通过后，是否**一并推送 `project-control` 与根仓 `ai-soc-workspace` 至 `192.168.77.79`**？

请回复 **“批准执行”**（及是否一并推送）以进入实施阶段。
