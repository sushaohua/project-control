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
end_time: '2026-10-29T16:00:00+08:00'
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

## 执行说明与验证总结

1. **已交付组件与产物清单**：
   - `project-control/config/coord_runner/coord_config.yaml`: 默认调度运行器配置（队列路径、状态持久化文件、租约超时时长、重试上限 2 次、最大实现并发 2、排他设备配置）。
     - SHA256: `75d43276a3da0fab4640b1f516045bea0d77142638be0d2f47a85a50c86a54f2`
   - `project-control/tools/coord_runner/__init__.py`: 包导出入口。
     - SHA256: `66693b1f4cbb0cf7d9041b584ebd4791e84def091ae9e68ac03646f4f92d73b6`
   - `project-control/tools/coord_runner/models.py`: 核心数据模型（`TaskState`, `Lease`, `TaskExecutionRecord`, `CoordState`, `CoordRunnerConfig`）。
     - SHA256: `e2db6126d84ef12a007f83a89ddd472e5569e0ca7ba28b0f20a09d5f4a18ce78`
   - `project-control/tools/coord_runner/errors.py`: 专用异常体系（`CoordRunnerError`, `ResourceConflictError`, `RemediationLimitExceededError`, `GateValidationError` 等）。
     - SHA256: `1407cc0ddd7dc5a954dc024f2be1e2689274a0735bef37d8e8effd22ccef07e3`
   - `project-control/tools/coord_runner/lease_manager.py`: 租约与互斥管理（最大实现并发限制、设备排他锁如 UART/PTY、租约超时清理与续期）。
     - SHA256: `e65e24a97af415303c7193e6c0c1d0264aac7aa9e90c43f4e0a657676680a96d`
   - `project-control/tools/coord_runner/state_machine.py`: 状态流转机与门禁校验（`Backlog` -> `Ready` -> `InProgress` -> `CandidatePushed` -> `SandboxQA` -> `Review` -> `Done`，最多 2 次有证据纠正拦截、虚假 Done 拦截、作者自批拦截、沙箱逃逸拦截）。
     - SHA256: `3c591694b703b42fd230cc779f73c82c19c6f25e51f2bbed25304a6f09c8ac45`
   - `project-control/tools/coord_runner/checkpoint.py`: 原子状态保存与检查点恢复（防御损坏 JSON、状态快照与重启演练恢复）。
     - SHA256: `5e38f357b573570a27cd718e296b694c8cb6671bacd5a67a834ff796b5f56ed6`
   - `project-control/tools/coord_runner/scheduler.py`: 依赖感知选卡与调度器（优先处理 bootstrap、依赖满足判定、并发与资源互斥前置判定）。
     - SHA256: `c015900d4ee81e421da333aec2b0e49d0066158c9dffa3f1c23037083095e884`
   - `project-control/tools/coord_runner/runner.py`: COORD 主运行器（支持 `--once` 有限循环、`--max-tasks N` 有限执行、常驻守护模式带 SIGINT/SIGTERM 信号处理与安全退出快照）。
     - SHA256: `b8569038fbf6b7bfe5078e67bdb812274e45cfe5d06147128586a1072d2f9f24`
   - `project-control/tools/coord_queue.py`: 队列状态投影升级（兼容旧 `next_action`，增加部署状态与检查点感知）。
     - SHA256: `cb803af84686e7b98e9e3818b7050cfb99427e1d3b0482e3213f8d98919fe995`
   - `project-control/tools/test_coord_runner.py`: 全量单元与门禁测试套件（26 项测试 100% 通过）。
     - SHA256: `c97b248931de181004a47d33e1b5eb464d077d89563062e5738756b4dd6e3bc3`

2. **核心特性与门禁验证**：
   - **依赖感知选卡**：精确解析 `bootstrap` 与 `order`，未完成前置任务的卡片被严格阻断；已完成任务自动过滤。
   - **资源互斥与租约**：严格限定最多 2 张实现卡并行，对 UART/硬件串口等排他资源严格互斥，防止并发抢占冲突；租约过期自动剪除。
   - **状态流转与退修上限**：流转推进 `Backlog` -> `Ready` -> `InProgress` -> `CandidatePushed` -> `SandboxQA` -> `Review` -> `Done`。沙箱 QA 失败或审查拒绝进入退修；连续 2 次退修仍失败时，第 3 次触发 `RemediationLimitExceededError` 升级停止，坚决不无限重试或违规放行。
   - **负例硬拦截**：虚假 Done（缺少审查或未批准）、作者自批（审查人与作者会话相同）、服务端 QA 失败、并发设备抢占、重复派单均被 100% 拦截。
   - **崩溃与重启恢复演练**：支持原子写入检查点；恢复时已验证的 `Done` 任务不重复执行，在途任务保持会话 ID、退修计数与租约状态；损坏检查点安全防御不盲目执行。
   - **代码编写规范门禁**：通过 AST 静态扫描，所有自研函数严格执行 $\le 50$ 行、参数 $\le 4$ 个的硬性门禁（0 违规项）。
