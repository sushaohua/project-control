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

针对用户与独立 OpenAI Codex 审查员（`gpt-6-luna`，Session `01a186b5-3e2c-7762-8e97-d260e7820ea4`）对 AUTO-02 的深度复审意见，INTEGRATOR 在白名单内完成了全面系统性重构与修复：

1. **真实 Docker 容器沙箱改造 (`qa_runner.py` 与 `delivery_checks.py`)**：
   - 彻底废止使用 `/tmp` 纯目录冒充沙箱隔离的做法。
   - `qa_runner.py` 接入真实 Docker 容器隔离（`start_docker_sandbox`、`stop_docker_sandbox`），使用 `ubuntu:20.04` 容器作为隔离运行基座，并在 `try...finally` 中确保容器生命周期安全销毁。
   - 在 `server_qa.json` 中真实写入 `"sandbox": {"kind": "container", "container_id": "...", "image": "ubuntu:20.04", "developer_mounts": []}`。
   - `delivery_checks.py:check_server_qa` 强化硬性门禁：非 `container` 或 `vm` 沙箱直接抛出异常，杜绝任何目录级替身逃逸。

2. **真实 Codex CLI 审查适配与证据绑定 (`codex_adapter.py`)**：
   - 实现 `CodexReviewAdapter`，非交互式调用真实宿主机 `/home/sushaohua/.local/bin/codex exec --skip-git-repo-check -m gpt-6-luna -C <workdir> --json <prompt>`。
   - 精确解析 OpenAI Codex 输出中的 `thread.started`（实际 Session ID / UUID）、`turn.completed`（Token 消耗量）及原始执行日志。
   - **Fail-Closed 严格执行**：Codex 二进制缺失、认证失败或退出码非 0 时直接报错阻断，严禁任何形式的静默回退或替代。

3. **修复 `coord_runner` 核心机制缺陷**：
   - **Fail-Closed 原则彻底落实**：在 `runner.py` 中，当 `agent_executor`、`qa_executor` 或 `review_executor` 为 None 时，严禁伪造 Commit、严禁伪造 `passed: True`、严禁伪造 `APPROVED`，直接抛出 `CoordRunnerError("Missing ...: fail-closed enforced")`。
   - **严格布尔类型校验**：在 `state_machine.py:validate_qa_verdict` 中，严格要求 `verdict.get("passed") is True`，坚决拦截字符串 `"false"` 等假值转真漏洞；强制校验沙箱类型必须为 `container` 或 `vm`。
   - **`SandboxQA` 重启恢复流转**：在 `runner.py:process_task` 中补齐 `SandboxQA` 状态分支，恢复到该状态的在途任务可继续推进。
   - **排他设备锁争用自动回滚**：在 `runner.py:_acquire_task_leases` 中，申请 UART 等排他设备锁冲突时，立即自动回滚已申请的 implementation 租约，避免并发额度泄漏。
   - **有证据纠错校验**：`handle_remediation` 强校验纠错证据字典，必须具备非空 `path` 与 `sha256`。
   - **CLI 命令行入口交付**：`runner.py` 交付完整 `main()` CLI 入口，支持 `--once`, `--max-tasks N`, `--daemon`, `--config PATH`。

4. **方法论硬性门禁 100% 达标**：
   - 经 AST 静态扫描所有修改与新增自研函数，**函数行数全部严格 $\le 50$ 行**，**参数个数全部严格 $\le 4$ 个**，违规数为 0。

---

### 已交付产物路径与 SHA256 清单

| 产物路径 | SHA256 |
| :--- | :--- |
| `project-control/config/coord_runner/coord_config.yaml` | `75d43276a3da0fab4640b1f516045bea0d77142638be0d2f47a85a50c86a54f2` |
| `project-control/tools/coord_runner/__init__.py` | `c1806f909a8c9c891c17c9f9a2824851a7a70d289ab087502794bff5796de7fa` |
| `project-control/tools/coord_runner/models.py` | `e2db6126d84ef12a007f83a89ddd472e5569e0ca7ba28b0f20a09d5f4a18ce78` |
| `project-control/tools/coord_runner/errors.py` | `1407cc0ddd7dc5a954dc024f2be1e2689274a0735bef37d8e8effd22ccef07e3` |
| `project-control/tools/coord_runner/lease_manager.py` | `e65e24a97af415303c7193e6c0c1d0264aac7aa9e90c43f4e0a657676680a96d` |
| `project-control/tools/coord_runner/state_machine.py` | `93150cac90cd9254f37306552900e14b6480382dad3648c5d7317e36a50d3c91` |
| `project-control/tools/coord_runner/checkpoint.py` | `5e38f357b573570a27cd718e296b694c8cb6671bacd5a67a834ff796b5f56ed6` |
| `project-control/tools/coord_runner/scheduler.py` | `c015900d4ee81e421da333aec2b0e49d0066158c9dffa3f1c23037083095e884` |
| `project-control/tools/coord_runner/runner.py` | `468fd313e899a3788360d2e3d4b5c4e9197e2a26ec900e21f1216798f2c34f05` |
| `project-control/tools/coord_runner/codex_adapter.py` | `5e571fbd94cc38486d3b7ba892adf425d7ed0f750384e0e793827e63f948d9a0` |
| `project-control/tools/coord_queue.py` | `cb803af84686e7b98e9e3818b7050cfb99427e1d3b0482e3213f8d98919fe995` |
| `project-control/tools/delivery_checks.py` | `289c3f4504fc80c48f1121e9e83b15ee11d5df2c53c8024b02999dce11d2e5ad` |
| `project-control/tools/qa_runner/qa_runner.py` | `82924af7ca226cce87b84ed1a55d117843fdad194d47e84612c9caeef0d5151d` |
| `project-control/tools/test_coord_runner.py` | `ddacdbafac5354288c3be70576bcc9ead694d7974057e6921890fdf31488f18c` |
