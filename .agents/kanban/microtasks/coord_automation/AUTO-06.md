---
id: AUTO-06
title: AUTO-06 M3定时调度：单实例systemd用户服务部署与P1-14零空耗及重启恢复独立验收
revision: 1
plan_revision: coord-intake-dispatch-phase1-20261103-rev2
task_kind: integration
development_stage: cross-stage
dispatchable: true
status: InProgress
blocked: false
blocked_reason: null
recovery_condition: null
planning_status: mapped-approved
demand_id: DEM-INTAKE-P1-001
feature: FEAT-INTAKE-20261103-001
owner: 482f7dba-d6ce-4ecc-92d4-29608bc1ffd4
proposed_owner: INTEGRATOR
executor:
  role: INTEGRATOR
  model: gpt-6-luna
  actual_model: null
  agent_id: 482f7dba-d6ce-4ecc-92d4-29608bc1ffd4
  run_id: run_01
authorization:
  evidence: project-control/docs/work_intake/approvals/APPR-20261103-001.yaml
  scope: CONFIRM-INTAKE-P1-20261103 rev 2 全部批准（AUTO-05 通过后部署单个 systemd --user 服务并开启 enable-linger）
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
      planned_session_alias: codex-qa-auto-06-review
      session: codex-qa-auto-06-review-s1
      session_evidence:
        path: null
        sha256: null
      decision: null
      reviewed_task_revision: null
      artifact_version: null
      evidence: null
      report_sha256: null
      report_review:
        session: codex-arch-auto-06-review-s1
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
      planned_session_alias: codex-arch-auto-06-review
      session: codex-arch-auto-06-review-s1
      session_evidence:
        path: null
        sha256: null
      decision: null
      reviewed_task_revision: null
      artifact_version: null
      evidence: null
      report_sha256: null
  verifier_session: null
  integrator_session: 482f7dba-d6ce-4ecc-92d4-29608bc1ffd4
primary_work_package: TASK-010
related_work_packages: []
depends_on:
  - AUTO-05
dependency_conditions:
  - task: AUTO-05
    accepted_version: 1
    acceptance_evidence: docs/evidence/coord_automation/AUTO-05/runs/run_04/arch_review_report.md
    required: AUTO-05（M1/M2 19 项综合端到端独立验收）通过并收件 Done 后方可安装和启用 M3 后台服务
scope_status: mapped
allowed_repositories:
  - project-control
write_scope:
  project-control:
    - tools/coord_runner/**
    - config/coord_runner/**
    - tools/test_coord_systemd_service.py
    - docs/operations/coord_runner_systemd_service_20261103.md
    - docs/evidence/coord_automation/AUTO-06/**
allowed_paths:
  - project-control/tools/coord_runner/**
  - project-control/config/coord_runner/**
  - project-control/tools/test_coord_systemd_service.py
  - project-control/docs/operations/coord_runner_systemd_service_20261103.md
  - project-control/docs/evidence/coord_automation/AUTO-06/**
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
base_commit: 0acb940e79782490eb7781b0a6b7d5fbb53c69c6
candidate_commit: null
dispatch_binding:
  source_commit: 0acb940e79782490eb7781b0a6b7d5fbb53c69c6
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
worktree: /home/sushaohua/workspace/ai_soc_project
lease:
  owner: 482f7dba-d6ce-4ecc-92d4-29608bc1ffd4
  task_revision: 1
  lease_id: lease_auto-06_20261103_01
  expires_at: '2026-11-03T23:59:59+08:00'
resources:
  - resource: host-systemd-user-coord-runner-service
    location: /home/sushaohua/.config/systemd/user/ai-soc-coord-runner.service
    exclusive: true
    pending: 待 AUTO-05 Done 后登记实际部署会话、保护既有 crontab 并开启 linger
budget:
  planned_checkpoint_minutes: 30
  max_evidence_based_corrections: 2
  on_limit: 停止/卸载新增用户态 service 并保存证据交唯一 COORD
checkpoint: AUTO-05 收件核验；单实例 systemd --user 服务部署与回退脚本；零空耗与 stop/restart 恢复实测；独立 QA
execution_contract: project-control/docs/planning/coord_intake_dispatch_phase1_confirmation_20261103.md
readiness_pending: []
deliverables:
  artifacts:
    - project-control/config/coord_runner/ai-soc-coord-runner.service
    - project-control/tools/coord_runner/service_ctl.py
    - project-control/tools/test_coord_systemd_service.py
    - project-control/docs/operations/coord_runner_systemd_service_20261103.md
  record: docs/evidence/coord_automation/AUTO-06/runs/run_01/result.md
rollback:
  steps:
    - 执行 systemctl --user disable --now ai-soc-coord-runner.service 并移除该 unit 文件；严禁触碰用户既有 sync_md.sh crontab
handoff:
  receiver_role: COORD
  receiver_session: 8d4e8b77-42a9-4bd3-bd5a-1b881e8d4bd5
  transport: tools.send_message
  evidence_location: docs/evidence/coord_automation/AUTO-06
  acknowledgement: null
verification:
  commands:
    - id: check_graph
      kind: test
      cwd: .
      command: PYTHONDONTWRITEBYTECODE=1 python3 project-control/tools/check_task_graph.py --workspace .
      expected: 任务图零错误
      availability: executable
    - id: test_systemd_service_and_idle_noop
      kind: test
      cwd: project-control
      command: PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tools -p 'test_coord_systemd_service.py' -v
      expected: 单实例 systemd 单元生成/校验、无变化零模型调用断言、stop/restart 恢复及全套 P1-01~20 回归通过
      availability: executable
  positive_cases:
    - P1-14：单个 systemd --user 服务复用同一入口自动接收推进；enable-linger 开启且既有 sync_md.sh crontab 原封未动；stop/start/restart 不丢在途与锁
  negative_cases:
    - P1-14：无新输入、无版本变化、无回执、无到期动作的连续多个轮询周期内模型调用次数严格为 0；严禁仅凭 systemctl active 签通过；严禁干扰或换版在途 QA
required_evidence_level: server-sandbox-verified
verification_environment: docker-qa-sandbox-and-isolated-host-codex
qa_review_policy: project-control/.agents/rules/codex_qa_review.md
delivery_gate_policy: project-control/.agents/rules/delivery_and_coord_gate.md
updated: '2026-11-03T13:25:00+08:00'
---

# AUTO-06 M3定时调度：单实例systemd用户服务部署与P1-14零空耗及重启恢复独立验收

## 1. 目标与边界

在前置 `AUTO-05`（M1/M2 综合独立验收）正式通过并收件 `Done` 后，由 `INTEGRATOR` 部署单个用户态 `systemd --user` 服务（`ai-soc-coord-runner.service`），执行获批 `sudo loginctl enable-linger sushaohua`（如实记录 WSL2 宿主休眠客观边界，零改动既有 `sync_md.sh` crontab），完成自动唤醒收件推进、`stop/start/restart` 在途恢复与**空闲零模型调用**实测，并经服务器沙箱 + 宿主机独立 Codex QA + 非作者 ARCH 报告复核验收关闭 `P1-14`。
