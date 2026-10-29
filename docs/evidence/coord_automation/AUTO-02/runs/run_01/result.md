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

6. **方法论硬性门禁 100% 达标**：
   - 经 AST 静态扫描，所有 18 个白名单及工具文件（包括 `runner.py`、`state_machine.py`、`qa_runner.py`、`delivery_checks.py`、`check_task_graph.py`、各测试套件等）中的自研函数**行数全部严格 $\le 50$ 行**，**入参全部严格 $\le 4$ 个**，违规数为 0。
   - 运行 92 项单元测试 100% 通过（`test_coord_runner.py` 40 项、`test_qa_runner.py` 20 项、`test_delivery_checks.py` 20 项、`test_check_task_graph.py` 12 项）。

---

### 已交付产物路径与 SHA256 清单

| 产物路径 | SHA256 |
| :--- | :--- |
| `project-control/config/coord_runner/coord_config.yaml` | `75d43276a3da0fab4640b1f516045bea0d77142638be0d2f47a85a50c86a54f2` |
| `project-control/tools/coord_runner/__init__.py` | `c1806f909a8c9c891c17c9f9a2824851a7a70d289ab087502794bff5796de7fa` |
| `project-control/tools/coord_runner/models.py` | `e2db6126d84ef12a007f83a89ddd472e5569e0ca7ba28b0f20a09d5f4a18ce78` |
| `project-control/tools/coord_runner/errors.py` | `1407cc0ddd7dc5a954dc024f2be1e2689274a0735bef37d8e8effd22ccef07e3` |
| `project-control/tools/coord_runner/lease_manager.py` | `e65e24a97af415303c7193e6c0c1d0264aac7aa9e90c43f4e0a657676680a96d` |
| `project-control/tools/coord_runner/state_machine.py` | `36631c9b1e30ad454b093ed2c9be1059f98e672d3ba5806b2b920b76fdc5d88f` |
| `project-control/tools/coord_runner/checkpoint.py` | `5e38f357b573570a27cd718e296b694c8cb6671bacd5a67a834ff796b5f56ed6` |
| `project-control/tools/coord_runner/scheduler.py` | `c015900d4ee81e421da333aec2b0e49d0066158c9dffa3f1c23037083095e884` |
| `project-control/tools/coord_runner/runner.py` | `32e73dc4f8a46e71b425829f8bd2be879612777c31e7a21d4844f3333beb51a0` |
| `project-control/tools/coord_runner/codex_adapter.py` | `5e571fbd94cc38486d3b7ba892adf425d7ed0f750384e0e793827e63f948d9a0` |
| `project-control/tools/coord_queue.py` | `cb803af84686e7b98e9e3818b7050cfb99427e1d3b0482e3213f8d98919fe995` |
| `project-control/tools/delivery_checks.py` | `7c72354037f0a5e3fdbf6e8bed5522f8029b1ec5f957842bba06645ef32ecc0e` |
| `project-control/tools/check_task_graph.py` | `4fdb9b6fc7f4eac35c7ef0cf65aa7636c7ba4075e52f9f335a25f2273162e11e` |
| `project-control/tools/qa_runner/qa_runner.py` | `dc03452ee672e82eabc06ce2fb9c77adc9b079bdbd8c7723293bec6461b795c9` |
| `project-control/tools/test_coord_runner.py` | `2c23ba1bea87aa7ef92121ac1ca2b8963a7767b05d71a14a626df282401b0fe9` |
