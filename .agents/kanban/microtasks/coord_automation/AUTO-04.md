---
id: AUTO-04
title: AUTO-04 M2持续推进与恢复：外置SQLite权威恢复源、长耗时异步并发与五源防重对账
revision: 1
plan_revision: coord-intake-dispatch-phase1-20261103-rev2
task_kind: implementation
development_stage: cross-stage
dispatchable: true
status: Backlog
blocked: false
blocked_reason: null
recovery_condition: null
planning_status: mapped-approved
demand_id: DEM-INTAKE-P1-001
feature: FEAT-INTAKE-20261103-001
owner: null
proposed_owner: INTEGRATOR
executor:
  role: INTEGRATOR
  model: gpt-6-luna
  actual_model: null
  agent_id: null
  run_id: null
authorization:
  evidence: project-control/docs/work_intake/approvals/APPR-20261103-001.yaml
  scope: CONFIRM-INTAKE-P1-20261103 rev 2 全部批准（M1 独立 QA 通过后启动 M2 持续推进与恢复）
model_policy:
  default: gpt-6-luna
  approved_overrides: []
reviewer:
  - QA
  - ARCH
verifier: null
integrator: INTEGRATOR
review_assignments:
  reviewer_sessions:
    - role: QA
      platform: codex
      model: gpt-6-luna
      planned_session_alias: codex-qa-auto-04-review
      session: null
      session_evidence:
        path: null
        sha256: null
      decision: null
      reviewed_task_revision: null
      artifact_version: null
      evidence: null
      report_sha256: null
      report_review:
        session: null
        role: ARCH
        decision: null
        reviewed_task_revision: null
        artifact_version: null
        evidence: null
        report_sha256: null
        session_evidence:
          path: null
          sha256: null
    - role: ARCH
      platform: codex
      model: gpt-6-luna
      planned_session_alias: codex-arch-auto-04-review
      session: null
      session_evidence:
        path: null
        sha256: null
      decision: null
      reviewed_task_revision: null
      artifact_version: null
      evidence: null
      report_sha256: null
  verifier_session: null
  integrator_session: null
primary_work_package: TASK-010
related_work_packages: []
depends_on:
  - AUTO-03
dependency_conditions:
  - task: AUTO-03
    accepted_version: null
    acceptance_evidence: docs/evidence/coord_automation/AUTO-03/runs/run_01/result.md
    required: AUTO-03（M1 手动单步）经服务器沙箱与独立 Codex QA、非作者 ARCH 报告复核全部通过并收件 Done 后方可启动 M2
scope_status: mapped
allowed_repositories:
  - project-control
write_scope:
  project-control:
    - tools/coord_runner/**
    - config/coord_runner/**
    - tools/coord_queue.py
    - tools/test_work_intake.py
    - tools/test_coord_runner.py
    - tools/test_coord_recovery.py
    - docs/work_intake/**
    - docs/evidence/coord_automation/AUTO-04/**
allowed_paths:
  - project-control/tools/coord_runner/**
  - project-control/config/coord_runner/**
  - project-control/tools/coord_queue.py
  - project-control/tools/test_work_intake.py
  - project-control/tools/test_coord_runner.py
  - project-control/tools/test_coord_recovery.py
  - project-control/docs/work_intake/**
  - project-control/docs/evidence/coord_automation/AUTO-04/**
forbidden_paths:
  - soc-ap/**
  - mcu-p3/**
  - test_harness/**
  - boot/bootloadermc/**
  - boot/bootloaderth/**
source_baseline:
  project-control: b4af2d32601a07d448ac8d67a07c57f5b9ab36ac
  soc-ap: 427dd6d82caceebb7b4642e78f1dbfa96ff5fc84
  mcu-p3: e051111e68dd61896ed42c0961153b167b8bca41
  test_harness: ccf1476a0b98cb55ca9ee7bd49d73ca5d4704414
base_commit: null
candidate_commit: null
dispatch_binding:
  source_commit: b4af2d32601a07d448ac8d67a07c57f5b9ab36ac
  workspace_diff_sha256: 736c674846d52dee8985cae0654388560199cb33f3041365bd62fae7d91710ad
  consumed_artifact_versions:
    confirmation_rev2: 63c1225d60c377a662bebaa0328f9bc95c19daccaa61d9f2766bc989f06f3f98
    approval_rev1: b7ea9ac9bdefc719fc46263c50e3a893d693ad63ae5166bc9085e4c71cc3f96d
protocol_input:
  path: project-control/docs/architecture/coord_intake_dispatch_phase1_design_20261103.md
  sha256: 8a2984c6bb4b868cc8e2d6742873527f448f27c7006d99c5ce322207b2941350
  revision: 2
read_sources:
  - project-control/.agents/rules/delivery_and_coord_gate.md
  - project-control/.agents/rules/codex_qa_review.md
  - project-control/docs/planning/coord_intake_dispatch_phase1_confirmation_20261103.md
  - project-control/docs/evidence/coord_automation/phase1_prep_20261103/integrator_host_interface_verification_20261103.md
worktree: /home/sushaohua/workspace/ai_soc_project
lease: null
resources:
  - resource: project-control-coord-runner-worktree
    location: /home/sushaohua/workspace/ai_soc_project/project-control
    exclusive: true
    pending: 待 AUTO-03 Done 后登记实际会话与有效租约
budget:
  planned_checkpoint_minutes: 30
  max_evidence_based_corrections: 2
  on_limit: 保存失败证据与检查点交唯一 COORD，仅回退本票差异
checkpoint: AUTO-03 收件核验；SQLite 单一恢复源与异步作业并发实现；超时/崩溃五源对账恢复自检；独立 QA
execution_contract: project-control/docs/planning/coord_intake_dispatch_phase1_confirmation_20261103.md
readiness_pending:
  - 等待前置 AUTO-03 正式独立 QA 通过并收件 Done 后绑定准确输入 commit、执行会话与租约
deliverables:
  artifacts:
    - project-control/tools/coord_runner/state_store.py
    - project-control/tools/coord_runner/job_launcher.py
    - project-control/tools/coord_runner/reconciler.py
    - project-control/tools/coord_runner/runner.py
    - project-control/tools/test_coord_recovery.py
  record: docs/evidence/coord_automation/AUTO-04/runs/run_01/result.md
rollback:
  steps:
    - 仅回退本票新增/修改文件并清理测试临时 SQLite 实例，保留工作区既有未提交修改
handoff:
  receiver_role: COORD
  receiver_session: 8d4e8b77-42a9-4bd3-bd5a-1b881e8d4bd5
  transport: tools.send_message
  evidence_location: docs/evidence/coord_automation/AUTO-04
  acknowledgement: null
verification:
  commands:
    - id: check_graph
      kind: test
      cwd: .
      command: PYTHONDONTWRITEBYTECODE=1 python3 project-control/tools/check_task_graph.py --workspace .
      expected: 任务图结构校验零错误
      availability: executable
    - id: test_coord_recovery_m2
      kind: test
      cwd: project-control
      command: PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tools -p 'test_coord_recovery.py' -v
      expected: 外置 SQLite 单一恢复源、异步双卡推进、重扫幂等、版本演进、超时/SIGKILL 五源对账、flock 单实例、租约活跃保护与 CAS 冲突用例全部通过
      availability: executable
    - id: test_m1_regression
      kind: test
      cwd: project-control
      command: PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tools -p 'test_work_intake.py' -v && PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tools -p 'test_coord_runner.py' -v
      expected: M1 与既有运行器回归测试全部通过
      availability: executable
  positive_cases:
    - P1-08/P1-09/P1-20：长耗时角色/QA 外置异步运行期间另一无冲突就绪任务真实启动推进；超时/崩溃后凭五源对账无缝续接；原文重排/局部未变项不重建需求并复用有效批准
  negative_cases:
    - P1-05/P1-07/P1-09/P1-10/P1-13/P1-20：重扫零重复作业；新 rev 遇旧版在途不静默换输入；无法确认从未启动标 RECONCILE_REQUIRED 禁盲重发；双实例被 flock 拦截且租约过期旧作业仍活跃禁抢占；并发手改触发 SHA256 CAS 拒覆盖
required_evidence_level: server-sandbox-verified
verification_environment: docker-qa-sandbox-and-isolated-host-codex
qa_review_policy: project-control/.agents/rules/codex_qa_review.md
delivery_gate_policy: project-control/.agents/rules/delivery_and_coord_gate.md
updated: '2026-11-03T13:25:00+08:00'
---

# AUTO-04 M2持续推进与恢复：外置SQLite权威恢复源、长耗时异步并发与五源防重对账

## 1. 目标与边界

在前置 `AUTO-03`（M1 手动单步）经独立 QA 验收通过后，交付第 2 步（**M2 持续推进与恢复**）：

1. 外置运行存储至 `/home/sushaohua/.local/share/ai_soc_coord_runner/state.sqlite3`（WAL 事务，确立唯一权威恢复源），配合 `coord_runner.lock`（`fcntl.flock(LOCK_EX | LOCK_NB)`）确保单写协调进程与唯一受控 `active_coord_thread_id`（`codex exec --sandbox read-only resume`）。
2. 将角色任务与 Docker/Codex QA 全面外置为异步非阻塞作业（`job_launcher.py`），支持一个长耗时作业等待期间另一无冲突就绪任务真实推进（最多 2 卡并行，`P1-08`）。
3. 实现五源确定性对账（`state.sqlite3` `dispatch_key` + `/proc/<pid>/stat` `starttime` + `codex_events.jsonl` + 只读 `~/.codex/state_5.sqlite` `first_user_message LIKE '[COORD_DISPATCH_KEY:...]'` / `rollout-*.jsonl` + `exit_status.json`），闭合 `P1-05, P1-07, P1-09, P1-10, P1-13, P1-20`。
4. 函数规模硬门禁：单函数 $\le 50$ 行、入参 $\le 4$ 个；未完成 M1/M2 独立验收前严禁安装后台服务。
