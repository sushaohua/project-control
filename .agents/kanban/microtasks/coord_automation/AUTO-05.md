---
id: AUTO-05
title: AUTO-05 M1与M2综合端到端独立实景验收门禁（P1-01~13, P1-15~20）
revision: 1
plan_revision: coord-intake-dispatch-phase1-20261103-rev2
task_kind: verification
development_stage: cross-stage
dispatchable: true
status: InProgress
blocked: false
blocked_reason: null
recovery_condition: null
planning_status: mapped-approved
demand_id: DEM-INTAKE-P1-001
feature: FEAT-INTAKE-20261103-001
owner: 05bae949-06e3-40fa-828c-ce9818b335e2
proposed_owner: QA
executor:
  role: QA
  model: gpt-6-luna
  actual_model: null
  agent_id: 05bae949-06e3-40fa-828c-ce9818b335e2
  run_id: run_02
  rework_count: 1/2
authorization:
  evidence: project-control/docs/work_intake/approvals/APPR-20261103-001.yaml
  scope: CONFIRM-INTAKE-P1-20261103 rev 2 全部批准（进入 M3 装服务前完成 M1/M2 19 项端到端独立验收）
model_policy:
  default: gpt-6-luna
  approved_overrides: []
reviewer:
  - ARCH
verifier: null
integrator: INTEGRATOR
review_assignments:
  reviewer_sessions:
    - role: ARCH
      platform: codex
      model: gpt-6-luna
      planned_session_alias: codex-arch-auto-05-review
      session: 01a1a0b2-f27e-7072-b150-2c008217c3f6
      session_evidence:
        path: docs/evidence/coord_automation/AUTO-05/runs/run_01/arch_session.jsonl
        sha256: 9cb7071e9c691002511e9c764016a6a4b73568574e4eef17515b027ca8428fe9
      decision: REJECTED
      reviewed_task_revision: 1
      artifact_version: a49b986dbe98df3bb2dcd19da01c34777f8e19ae
      evidence: docs/evidence/coord_automation/AUTO-05/runs/run_01/arch_review_report.md
      report_sha256: 555c47881fffe22f03f8c54101ca9b3d00a168bcb4a0e47261c737dfdfcfafef
  verifier_session: null
  integrator_session: null
primary_work_package: TASK-010
related_work_packages: []
depends_on:
  - AUTO-04
dependency_conditions:
  - task: AUTO-04
    accepted_version: 1
    acceptance_evidence: docs/evidence/coord_automation/AUTO-04/runs/run_02/qa_review_report.md
    required: AUTO-03 与 AUTO-04 均已完成独立 QA 并收件 Done，锁定服务器候选后执行 M1/M2 19 项端到端验收
scope_status: mapped
allowed_repositories:
  - project-control
write_scope:
  project-control:
    - tools/test_phase1_intake_acceptance.py
    - docs/evidence/coord_automation/AUTO-05/**
allowed_paths:
  - project-control/tools/test_phase1_intake_acceptance.py
  - project-control/docs/evidence/coord_automation/AUTO-05/**
forbidden_paths:
  - project-control/tools/coord_runner/**
  - soc-ap/**
  - mcu-p3/**
  - test_harness/**
  - boot/bootloadermc/**
  - boot/bootloaderth/**
source_baseline:
  project-control: 4c58c46be12af0e4dcfc4ef6f40dd162c5b18c06
  soc-ap: 427dd6d82caceebb7b4642e78f1dbfa96ff5fc84
  mcu-p3: e051111e68dd61896ed42c0961153b167b8bca41
  test_harness: ccf1476a0b98cb55ca9ee7bd49d73ca5d4704414
base_commit: 4c58c46be12af0e4dcfc4ef6f40dd162c5b18c06
candidate_commit: ac820925bf14f5d2b4864dd1f01b9784939a453e
dispatch_binding:
  source_commit: 4c58c46be12af0e4dcfc4ef6f40dd162c5b18c06
  workspace_diff_sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
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
  owner: 05bae949-06e3-40fa-828c-ce9818b335e2
  task_revision: 1
  lease_id: lease_auto-05_20261103_01
  expires_at: '2026-11-03T21:00:00+08:00'
resources:
  - resource: project-control-qa-acceptance-suite
    location: /home/sushaohua/workspace/ai_soc_project/project-control
    exclusive: true
    pending: 待 AUTO-04 Done 后安排非实现作者的独立 QA 会话与非作者 ARCH 复核会话
budget:
  planned_checkpoint_minutes: 30
  max_evidence_based_corrections: 2
  on_limit: 保存证据交唯一 COORD，不修改受测实现代码促通过
checkpoint: AUTO-04 候选冻结；独立验收套件与宿主机实景演练验证；独立 ARCH 复核报告；收件放行 M3
execution_contract: project-control/docs/planning/coord_intake_dispatch_phase1_confirmation_20261103.md
readiness_pending: []
deliverables:
  artifacts:
    - project-control/tools/test_phase1_intake_acceptance.py
  record: docs/evidence/coord_automation/AUTO-05/runs/run_01/result.md
rollback:
  steps:
    - 仅回退本票新增独立验收脚本与报告草稿，严禁改动 coord_runner 受测代码
handoff:
  receiver_role: COORD
  receiver_session: 8d4e8b77-42a9-4bd3-bd5a-1b881e8d4bd5
  transport: tools.send_message
  evidence_location: docs/evidence/coord_automation/AUTO-05
  acknowledgement: null
verification:
  commands:
    - id: check_graph
      kind: test
      cwd: .
      command: PYTHONDONTWRITEBYTECODE=1 python3 project-control/tools/check_task_graph.py --workspace .
      expected: 任务图零错误
      availability: executable
    - id: run_phase1_m1_m2_acceptance
      kind: test
      cwd: project-control
      command: PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tools -p 'test_phase1_intake_acceptance.py' -v
      expected: 独立端到端验收矩阵 P1-01~13 及 P1-15~20 共 19 项正反例全部通过
      availability: executable
  positive_cases:
    - 独立验证服务器锁定候选在三类人工输入、多角色拆单、长任务并行推进、超时/崩溃恢复与演练闭环共 19 项条款的正向预期
  negative_cases:
    - 独立验证伪造审批、同版本篡改、重扫、双实例、租约活跃抢占、并发写冲突、exit 0 无证与未推远端拦截全部生效；QA 作者产物经独立非作者 Codex ARCH 复核通过
required_evidence_level: server-sandbox-verified
verification_environment: docker-qa-sandbox-and-isolated-host-codex
qa_review_policy: project-control/.agents/rules/codex_qa_review.md
delivery_gate_policy: project-control/.agents/rules/delivery_and_coord_gate.md
updated: '2026-11-03T13:25:00+08:00'
---

# AUTO-05 M1与M2综合端到端独立实景验收门禁（P1-01~13, P1-15~20）

## 1. 目标与边界

由未参与 `AUTO-03`/`AUTO-04` 实现的独立 QA 针对服务器锁定候选编写并执行 M1+M2 综合验收测试与宿主机实景核验（覆盖 `P1-01~13, P1-15~20` 共 19 项），其独立验收产物与报告由另一独立非作者 Codex `ARCH` 会话结合独立 Docker 沙箱复核通过后，方可释放 M3（`AUTO-06`）服务部署。
