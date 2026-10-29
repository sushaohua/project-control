# AUTO-02 单票实际执行记录 (run_01)

```yaml
template_version: '2026-10-27'
task_id: AUTO-02
task_revision: 1
actual_run_id: run_01
actor_role: INTEGRATOR
actor_model: inherit
model_override_ref: null
actor_session: 0e0e4b90-2aeb-42d4-abc2-13ed9198e8f0
lease_id: lease_auto-02_20261029_01
start_time: '2026-10-29T15:47:39+08:00'
end_time: '2026-10-29T16:25:00+08:00'
workspace: /home/sushaohua/workspace/ai_soc_project
branch: main
source_head: a5e4b5e97439cae4a7093d1d0a29c5dc9b3c7819
verification_environment: independent-codex-in-server-based-sandbox
verification_scope: coord-runner-and-recovery
required_evidence_level: server-sandbox-verified
commands:
  - command: PYTHONDONTWRITEBYTECODE=1 python3 -m unittest project-control/tools/test_coord_runner.py -v
    cwd: .
    exit_code: 0
    passed: true
  - command: PYTHONDONTWRITEBYTECODE=1 python3 -m unittest project-control/tools/test_qa_runner.py -v
    cwd: .
    exit_code: 0
    passed: true
  - command: PYTHONDONTWRITEBYTECODE=1 python3 -m unittest project-control/tools/test_delivery_checks.py -v
    cwd: .
    exit_code: 0
    passed: true
  - command: PYTHONDONTWRITEBYTECODE=1 python3 -m unittest project-control/tools/test_check_task_graph.py -v
    cwd: .
    exit_code: 0
    passed: true
  - command: PYTHONDONTWRITEBYTECODE=1 python3 project-control/tools/check_task_graph.py --workspace .
    cwd: .
    exit_code: 0
    passed: true
  - command: PYTHONDONTWRITEBYTECODE=1 python3 project-control/tools/coord_queue.py --workspace .
    cwd: .
    exit_code: 0
    passed: true
actual_result: passed
```

## 执行说明与专项重构总结

针对用户与独立 OpenAI Codex 审查员（`gpt-6-luna`）在 run_02 审查中指出的 5 项问题，INTEGRATOR 在白名单内完成了全面系统性修复与闭环验证：

1. **[P0 AUTO02-R2-01] 强制 `server_qa` 证据字典与 Commit 强绑定**：
   - 在 `state_machine.py:validate_qa_verdict` 中，将 `server_qa` 字典置为强制项（缺失或空即抛出 `GateValidationError`）。
   - 校验 `server_qa` 必须包含非空 `path` 与 `sha256`。
   - 校验 `server_qa.sandbox.kind` 必须为 `container` 或 `vm`。
   - 强校验 `verdict` 中的 `candidate_commit` 与任务记录完全一致，拒绝未匹配或缺失的判定。
   - 同步更新测试套件中的所有 mock QA 执行器，提供完整的 `server_qa` 证据与匹配的 Commit SHA。

2. **[P0 AUTO02-R2-06] 生产执行器接通 (`runner.py`)**：
   - 实现 `default_qa_executor(self, task_id, candidate_commit)`：调用 `qa_runner.py` 并解析输出中的 `[SERVER QA REF]` 与 `server_qa.json`，返回标准 QA 证据字典。
   - 实现 `default_review_executor(self, task_id, candidate_commit, record=None)`：调用 `CodexReviewAdapter`（模型 `gpt-6-luna`），执行独立审查并返回审查会话、决策与 Token 凭据。
   - 提供 `wire_production_executors(self)` 方法，在 `runner.py:main()` CLI 入口中默认接入生产执行器，使命令行工具完全具备实机运行能力。
   - 保留未配置执行器时的 Fail-Closed 机制，防止无执行器时静默放行。

3. **[P0 AUTO02-R2-02] Docker 容器 Inspect 真实物证捕获 (`qa_runner.py`)**：
   - 容器启动后立即执行 `docker inspect {cid}`，捕获容器 ID、镜像摘要、挂载卷及运行状态元数据。
   - 将 inspect 结果插入 `runtime.log` 首部，并在 `server_qa.json` 的 `sandbox.container_inspect` 中结构化留存，确保容器销毁后仍具备完整的硬件与环境审计溯源能力。

4. **[P1 AUTO02-R2-03] 真实崩溃-落盘-重启恢复演练 (`test_coord_runner.py`)**：
   - 新增 `test_crash_and_restart_recovery_drill_from_disk_sandbox_qa` 测试：
     - Runner 1 启动任务并推进入 `SandboxQA` 状态，将快照写入磁盘检查点文件后终止（模拟进程崩溃）。
     - Runner 2 从磁盘检查点恢复，验证处于 `SandboxQA` 状态，接通执行器继续流转完成 Review 与 Done。
     - 验证任务成功进入 `completed_tasks` 并落盘保存最终状态。

5. **[P1 AUTO02-R2-04] 函数入参重构 (`check_task_graph.py`)**：
   - 将 `check_task_graph.py:done_acceptance_errors` 重构为 `(task_id, card, cards, workspace=None)`，严格 $\le 4$ 参数。

7. **[P0 AUTO02-R3-01 / AUTO02-R5-01] 生产环境 Agent 执行器接通与服务端远端推送核验 (`runner.py`)**：
   - 实现 `default_agent_executor(self, task_id, record)`：通过 `_resolve_task_repo` 定位任务所属仓库（`soc-ap`、`mcu-p3`、`test_harness` 或 `project-control`），调用 `git rev-parse HEAD` 获取候选 Commit。
   - 实现 `_verify_server_commit(self, repo_dir, commit)`：通过 `git branch -r --contains <commit>` 及 `git ls-remote origin <commit>` 核验候选 Commit 是否真实推送至 GitLab 远端服务器；若为本地未推送 Commit 则抛出 `CoordRunnerError` 拦截。
   - 在 `wire_production_executors(self)` 中同步组装 `self.agent_executor = self.default_agent_executor`，保证生产运行环境下三类执行器（Agent、QA、Review）全量自动接通。

8. **[P1 AUTO02-R3-02] 进程级崩溃与跨进程重启恢复真实演练 (`test_coord_runner.py`)**：
   - 实现 `test_process_level_kill_and_restart_recovery_drill`：
     - 子进程通过 `subprocess.Popen([sys.executable, "-c", ...])` 启动 `CoordRunner`，将任务置入 `SandboxQA` 状态并持久化落盘至 `coord_state_proc.json`。
     - 子进程紧接着触发硬杀死（`os.kill(os.getpid(), signal.SIGKILL)`）模拟真实进程意外崩溃。
     - 父进程验证子进程非正常退出（`returncode == -SIGKILL`），随后在父进程中拉起全新的 `CoordRunner` 实例并调用 `restore_from_checkpoint`。
     - 验证任务自 `SandboxQA` 状态成功恢复，接通 QA 和 Review 判定后无缝推进至 `Done` 状态，最终持久化落盘。

9. **[AUTO02-R5-02] 多角色评审门禁与闭环验收 (`runner.py` 与 `state_machine.py`)**：
   - 在 `runner.py:_execute_review_phase` 中：读取 `card.get("reviewer", ["QA"])`，循环每个必需角色；未完成评审的角色调用 `review_executor` 并记录结果；所有声明的评审角色均 APPROVED 后方流转至 DONE。
   - 在 `state_machine.py:validate_done_acceptance` 中：校验任务卡声明的所有 reviewer 角色均存在于 `reviewer_sessions` 且判定全为 APPROVED；若包含 QA 且附带 QA 报告复审则递归校验复审 APPROVED，任一缺失或拒绝立即抛出 `GateValidationError` 拒绝虚假 Done。

10. **[AUTO02-R6-01 / R6-02 / R6-03] run_06 审查三大阻断项闭环修复**：
    - **QA 报告复核强制门禁与自动衔接**：在 `state_machine.py:validate_done_acceptance` 中，当 `required_roles` 包含 QA 时，强制要求 QA 审阅条目必须包含独立的 `report_review` 字典且必须为 APPROVED；其评审人必须存在且严禁为 QA 本人或任务作者（严格非作者独立复核），缺失或未通过立即抛出 `GateValidationError("Fake Done rejected: QA reviewer missing mandatory non-author report_review")`；在 `runner.py:_execute_review_phase` 中实现 `_ensure_qa_report_review`，在 QA 审阅通过后自动通过非作者角色（如 ARCH）完成对 QA 报告的复审并注入 `report_review`。
    - **有证据纠正硬性门禁落实**：在 `state_machine.py:handle_remediation` 中将 `evidence` 参数置为强制必需项，严禁为 None 或空；必须为包含有效非空 `path` 与 `sha256` 的字典，否则立即抛出 `GateValidationError("Remediation requires mandatory evidence dict with non-empty path and sha256")`；在 `validate_qa_verdict` 与 `validate_review_verdict` 中均实现证据结构提取与哈希化绑定，保证每次纠正 100% 具备可审计凭证。
    - **沙箱证据任务修订号严格一致**：在 `models.py:TaskExecutionRecord` 中增加 `task_revision` 字段；在 `runner.py:dispatch_task` 中自任务卡严格继承 `revision`；在 `runner.py:default_qa_executor` 中透传 `--revision`；在 `state_machine.py:validate_qa_verdict` 中强校验 `server_qa.task_revision == record.task_revision`，不一致立即拒绝。

11. **[AUTO02-R7-01 / R7-02 / R7-03] run_07 审查阻断项彻底加固**：
    - **沙箱任务修订号无条件严格强校验**：将 `state_machine.py:_validate_server_qa_proof` 改为无条件 fail-closed 强校验：`qa_rev is None or qa_rev != record.task_revision` 均立即抛出 `GateValidationError`，彻底杜绝缺失字段绕过门禁的隐患；并在 `test_coord_runner.py` 中新增缺失字段与不匹配的专项拦截测试。
    - **QA 报告复核强制绑定报告路径与 SHA256**：在 `runner.py:_ensure_qa_report_review` 中，通过 `_resolve_qa_report_ref` 显式解析并绑定 QA 报告物理路径 `report_path` 与真实 `report_sha256`；在 `state_machine.py:_validate_qa_report_review` 中增加强校验：`report_review` 必须包含非空 `report_path` 与 `report_sha256`，且若 QA 自身声明了 `report_sha256` 则必须严格一致，否则立即拒绝。
    - **故障物证优先使用真实磁盘文件**：重构 `state_machine.py:_extract_qa_failure_evidence` 与 `_extract_review_failure_evidence`，实现 `_find_or_create_evidence`，优先检索并读取 `server_qa.json`、`runtime.log`、`server_verdict.json` 等真实物理文件计算 SHA256；若不存在则持久化落盘至真实文件，杜绝内存虚构路径。

12. **[AUTO02-R8-01 / R8-02] run_08 审查阻断项彻底加固（QA 报告真实物理落盘与物理字节 SHA256 强校验）**：
    - **物理文件存在性与物理字节重算强门禁 (`state_machine.py`)**：在 `_validate_qa_report_review(self, entry, author, workspace)` 中，通过 `workspace / r_path`（或绝对路径）物理核查文件是否存在，不存在即抛出 `GateValidationError(f"Fake Done rejected: QA report file not found on disk at {r_path}")`；强制从磁盘读取物理字节重算 `real_sha = hashlib.sha256(p.read_bytes()).hexdigest()`，与 `report_review.get("report_sha256")` 比对，不一致直接拦截拒绝；若 QA 条目自报 `report_sha256` 也必须与物理字节重算的 `real_sha` 绝对一致。
    - **生产 Runner 杜绝假数据兜底并校验 Prefill (`runner.py`)**：在 `_resolve_qa_report_ref(self, record, qa_entry)` 中，严禁使用 `json.dumps` 内存伪造哈希；优先按规范路径检索物理文件并核查物理存在性，缺失立即抛出 `CoordRunnerError` 拦截；若 `qa_entry` 中预填了 `report_sha256`，强制要求与物理读取字节计算的真实 SHA 比对，不一致立即抛错拦截。
    - **全方位负例测试与覆盖率闭环 (`test_coord_runner.py`)**：新增 `test_done_rejected_when_qa_report_file_not_found_on_disk`、`test_done_rejected_when_qa_report_file_tampered_or_sha_mismatch`、`test_runner_resolve_qa_report_missing_file_rejected` 及 `test_runner_resolve_qa_report_prefill_mismatch_rejected` 专项负例测试。

13. **[AUTO02-R10-01 / R10-02 / R10-03] run_10 审查三大阻断项彻底加固**：
    - **Runner 入口严禁补写缺省 report_sha256 (`runner.py`)**：在 `_resolve_qa_report_ref` 中，若 `qa_entry` 中缺失 `report_path` 或缺失 `report_sha256`，严禁 runner 自动补写，强制抛出 `CoordRunnerError("QA review entry missing mandatory report_path or report_sha256")`；若物理文件不存在或磁盘重算哈希与 prefill 不一致，严格拦截。新增专项负例测试 `test_runner_resolve_qa_report_missing_entry_sha_rejected` 与 `test_runner_resolve_qa_report_missing_entry_path_rejected`。
    - **ARCH QA 报告复审专属独立会话调用 (`runner.py`)**：在 `_ensure_qa_report_review` 中，彻底移除复用代码审查 session 的假批准逻辑；通过 `_invoke_report_reviewer` 单独调用审阅执行器执行对 QA 报告的专属独立复核（传递 `review_kind="qa_report"`、`report_path` 与 `report_sha256`），仅当返回独立 session 且 `decision == "APPROVED"` 时才注入 `qa_entry["report_review"]`；若被拒绝则立刻触发 `handle_remediation` fail-closed 退出。新增专项测试 `test_execute_review_phase_qa_report_review_rejected`。
    - **保留 Docker 容器沙箱 inspect 物证 (`qa_runner.py`)**：在 `stop_docker_sandbox` 中，改为执行 `docker stop -t 2 {container_id}`，严禁直接执行 `docker rm -f`，确保容器保留在 Docker daemon 的 exited 状态，供独立审阅会话执行 `docker inspect` 验证运行物证真实性。新增测试 `test_stop_docker_sandbox_preserves_container_state`。

14. **方法论硬性门禁 100% 达标**：
    - 经 AST 静态扫描，所有 18 个白名单及工具文件（包括 `runner.py`、`state_machine.py`、`qa_runner.py`、`delivery_checks.py`、`check_task_graph.py`、各测试套件等）中的自研函数**行数全部严格 $\le 50$ 行**，**入参全部严格 $\le 4$ 个**，违规数为 0。
    - 运行 117 项单元测试 100% 通过（`test_coord_runner.py` 64 项、`test_qa_runner.py` 21 项、`test_delivery_checks.py` 20 项、`test_check_task_graph.py` 12 项）。

---

### 已交付产物路径与 SHA256 清单

| 产物路径 | SHA256 |
| :--- | :--- |
| `project-control/config/coord_runner/coord_config.yaml` | `75d43276a3da0fab4640b1f516045bea0d77142638be0d2f47a85a50c86a54f2` |
| `project-control/tools/coord_runner/__init__.py` | `c1806f909a8c9c891c17c9f9a2824851a7a70d289ab087502794bff5796de7fa` |
| `project-control/tools/coord_runner/models.py` | `6624e3bf13099f0c59085c72d99262ee9f88920ae87c7e8e26fa846126fc9bc5` |
| `project-control/tools/coord_runner/errors.py` | `1407cc0ddd7dc5a954dc024f2be1e2689274a0735bef37d8e8effd22ccef07e3` |
| `project-control/tools/coord_runner/lease_manager.py` | `e65e24a97af415303c7193e6c0c1d0264aac7aa9e90c43f4e0a657676680a96d` |
| `project-control/tools/coord_runner/state_machine.py` | `23d01b6473e6a1672f39b1ce623c5d6cc37574fd2f82850a094e3039c55e202a` |
| `project-control/tools/coord_runner/checkpoint.py` | `5e38f357b573570a27cd718e296b694c8cb6671bacd5a67a834ff796b5f56ed6` |
| `project-control/tools/coord_runner/scheduler.py` | `c015900d4ee81e421da333aec2b0e49d0066158c9dffa3f1c23037083095e884` |
| `project-control/tools/coord_runner/runner.py` | `07b6f9b051346212829cc4921c6ee490c4fd49eaff8a02754c8e8362518ae33c` |
| `project-control/tools/coord_runner/codex_adapter.py` | `5e571fbd94cc38486d3b7ba892adf425d7ed0f750384e0e793827e63f948d9a0` |
| `project-control/tools/coord_queue.py` | `cb803af84686e7b98e9e3818b7050cfb99427e1d3b0482e3213f8d98919fe995` |
| `project-control/tools/delivery_checks.py` | `7c72354037f0a5e3fdbf6e8bed5522f8029b1ec5f957842bba06645ef32ecc0e` |
| `project-control/tools/check_task_graph.py` | `4fdb9b6fc7f4eac35c7ef0cf65aa7636c7ba4075e52f9f335a25f2273162e11e` |
| `project-control/tools/qa_runner/qa_runner.py` | `6918544993dedf479bb60ff857e05e5dc331542bbeb11fc1d892274b363da69c` |
| `project-control/tools/test_coord_runner.py` | `3278ddd7902f1a5f673c644d7de7c2109c78e5b0e54f04a48608fef8b5fe9432` |
| `project-control/tools/test_qa_runner.py` | `b580269e53884994168dbc37b17d0abf95d34e4c7efbe711600a5eb67fbcf16a` |
