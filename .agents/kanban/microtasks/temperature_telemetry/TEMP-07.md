---
id: TEMP-07
title: TEMP-07 全流程验收、交接与版本锁同步
revision: 1
plan_revision: marlin-r2
task_kind: design
dispatchable: true
status: Done
blocked: false
planning_status: closed-done
owner: coord-session-20261029
proposed_owner: COORD
executor:
  role: COORD
  agent_id: coord-session-20261029
  run_id: run_01
reviewer:
- QA
verifier: null
integrator: null
review_assignments:
  reviewer_sessions:
  - role: QA
    platform: codex
    model: gpt-6-luna
    planned_session_alias: codex-qa-temp07-review
    session: 7f1cda3e-d24d-40ed-92d7-c40afe3a440c
    decision: APPROVED
    reviewed_task_revision: 1
    artifact_version: 1.0.0
    evidence: docs/evidence/temperature_increment/TEMP-07/runs/run_01/qa_review_report.md
    report_sha256: b028d784fb3c517bd8a57d93bb112a3771f58d84514e2086b191970799b093c0
  verifier_session: null
  integrator_session: null
primary_work_package: TASK-010
requirement:
- PILOT-REQ-01
- PILOT-REQ-04
depends_on:
- TEMP-06
dependency_conditions:
- task: TEMP-06
  accepted_version: 246f7b2c1d366e4dcd9a485b946a735ff0adacc67510c2fb5a9e9b1e5fc47a2f
  acceptance_evidence: docs/evidence/temperature_increment/TEMP-06/runs/run_01/result.md
  required: 绑定独立HIL验收报告与双审签署，经主管审核核准放行
scope_status: mapped
allowed_repositories:
- project-control
write_scope:
  project-control:
  - docs/evidence/temperature_increment/TEMP-07/**
  - docs/handoff/**
  - .agents/kanban/**
allowed_paths:
- project-control/docs/evidence/temperature_increment/TEMP-07/**
- project-control/docs/handoff/**
- project-control/.agents/kanban/**
source_baseline:
  project-control: a5e4b5e97439cae4a7093d1d0a29c5dc9b3c7819
  soc-ap: 4445c8fedc21bafef5e6c971fcb54cec703f0e71
  mcu-p3: 1246ea9cb441d074ea444f53320f5632fefcd503
  test_harness: 6c61ce6e51cf83d7fb58d319c23cb91bf95786cb
base_commit: a5e4b5e97439cae4a7093d1d0a29c5dc9b3c7819
dispatch_binding:
  source_commit: a5e4b5e97439cae4a7093d1d0a29c5dc9b3c7819
  workspace_diff_sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
  consumed_artifact_versions:
    TEMP-06: 246f7b2c1d366e4dcd9a485b946a735ff0adacc67510c2fb5a9e9b1e5fc47a2f
protocol_input:
  path: project-control/docs/specs/ap_mc_formal_protocol_v2_0_multidevice_routing_draft_20261015.md
  sha256: 9f8d4f9607cb3e76cc30b9ee2f971b23c3e0d936611188466a71f4aa15f3ce54
  revision: 2.0.3
read_sources:
- project-control/docs/planning/product/next_increment_design_pl02.md
- project-control/docs/operations/ap_mc_th_software_hardware_handover.md
worktree: /home/sushaohua/workspace/ai_soc_project
resources:
- resource: coord-workspace
  location: null
  exclusive: false
  pending: null
lease:
  owner: coord-session-20261029
  task_revision: 1
  lease_id: lease-temp07-coord-20261029-01
  expires_at: '2026-10-29T18:00:00+08:00'
budget:
  planned_checkpoint_minutes: 30
  max_evidence_based_corrections: 2
  on_limit: 保存失败交COORD
checkpoint: 开工前；里程碑核销对账完成；锁文件同步完成
execution_contract: project-control/docs/planning/product/next_increment_design_pl02.md
readiness_pending: []
deliverables:
  artifacts:
  - project-control/docs/evidence/temperature_increment/TEMP-07/result.md
  - project-control/docs/handoff/HANDOFF_TEMP_INCREMENT.md
  record: docs/evidence/temperature_increment/TEMP-07/runs/<actual-run-id>/result.md
rollback:
  steps:
  - 回退交接报告与锁文件修改
handoff:
  receiver_role: COORD
  receiver_session: main
  transport: docs
  evidence_location: docs/evidence/temperature_increment/TEMP-07
  acknowledgement: null
verification:
  commands:
  - id: check_graph
    cwd: .
    command: PYTHONDONTWRITEBYTECODE=1 python3 project-control/tools/check_task_graph.py --workspace .
    expected: 全图无错误，无孤立卡
    availability: local
  positive_cases:
  - 增量全部任务按序验收，MS-07/15/21温度范围准确核销，五仓提交同步锁定
  negative_cases:
  - 缺少必需独立报告时拒绝提升状态
updated: '2026-10-28'
required_evidence_level: document
verification_environment: planning
qa_review_policy: project-control/.agents/rules/codex_qa_review.md
---

# TEMP-07 全流程验收、交接与版本锁同步

由 COORD 组织全增量验收对账，发布交接文档，核销 MS 里程碑温度范围，更新 workspace.json 锁定五仓提交。
