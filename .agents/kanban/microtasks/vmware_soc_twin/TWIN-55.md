---
id: TWIN-55
title: TWIN-55 Web HMI完整basecase(BASE-01~27/J-01)与三组增量(DELTA-DBG/BAUD/COMB)真实闭环验收
revision: 1
plan_revision: vmware-soc-twin-20261105
task_kind: verification
development_stage: vmware-twin
dispatchable: false
status: Backlog
blocked: true
blocked_reason: 等待TWIN-54完成Step 1-4制品封存并由用户确认Step 5具体固件烧录清单与排他台架窗口
recovery_condition: TWIN-54完成且用户批准Step 5具体固件烧录清单后解封执行
planning_status: planned
owner: null
proposed_owner: QA
executor:
  role: QA
  agent_id: null
  run_id: null
qa_policy: streamlined-v1
reviewer:
  - QA
verifier: QA
integrator: INTEGRATOR
requirement_id: REQ-20261105-001
demand_id: DEM-20261105-005
confirmation_id: CONFIRM-WEB-HMI-FULL-QA-BUILD-DEPLOY-20261105
approval_id: APPR-20261105-003
review_assignments:
  reviewer_sessions: []
  verifier_session: null
  integrator_session: null
primary_work_package: TASK-010
related_work_packages:
  - TASK-009
depends_on:
  - TWIN-54
dependency_conditions:
  - task: TWIN-54
    accepted_version: pending
    acceptance_evidence: docs/evidence/twin/TWIN-54/runs/author_01/result.md
    required: 消费TWIN-54封存的build_manifest.yaml、提测交接单及经非作者独立复核的QA测试工具
scope_status: mapped
allowed_repositories:
  - project-control
write_scope:
  project-control:
    - docs/evidence/twin/TWIN-55/**
    - docs/evidence/hil/**
allowed_paths:
  - project-control/docs/evidence/twin/TWIN-55/**
  - project-control/docs/evidence/hil/**
forbidden_paths:
  - soc-ap/**
  - mcu-p3/**
  - test_harness/**
  - boot/**
source_baseline:
  project-control: 77c679616a09d9c82906ff9bdf27fefc6d6c343f
  soc-ap: 79932746d225bb115010c5545ef3f7499482e137
  mcu-p3: 016e1236af75f6f19282d6b000f4b1b68bd96cc3
  test_harness: d14ed04321c6d4f5ddb35a8801604a8af53b5b60
base_commit: 77c679616a09d9c82906ff9bdf27fefc6d6c343f
branch: main
candidate_commit: null
dispatch_binding:
  source_commit: 77c679616a09d9c82906ff9bdf27fefc6d6c343f
  workspace_diff_sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
  consumed_artifact_versions:
    build_deploy_confirmation: 7e92f1093ea1ba1f27fe4b0159bad926e6b0f44130f55d06ae223c730ddffd89
    basecases_rev4: 67a2c1df609ce14773361a83b803ca414f13bf243be87961f97700ef798ff929
protocol_input:
  path: project-control/docs/planning/qa_web_hmi_basecases_20261103.md
  sha256: 67a2c1df609ce14773361a83b803ca414f13bf243be87961f97700ef798ff929
  revision: 4
icd_versions:
  - path: project-control/docs/planning/qa_web_hmi_basecases_20261103.md
    version: 4
read_sources:
  - project-control/.agents/rules/repository_rule_sources.json
  - project-control/.agents/rules/repository_rule_boundaries.md
  - project-control/.agents/rules/delivery_and_coord_gate.md
  - project-control/.agents/rules/codex_qa_review.md
  - project-control/docs/planning/qa_web_hmi_basecases_20261103.md
  - project-control/docs/planning/web_hmi_full_qa_build_deploy_confirmation_20261105.md
worktree: project-control
lease: null
resources:
  - resource: vmware-and-physical-mcu-bench
    location: 192.168.77.134+COM12+COM13+STLink
    exclusive: true
    pending: TWIN-54
budget:
  planned_checkpoint_minutes: 90
  max_evidence_based_corrections: 2
  on_limit: 保存证据交COORD
checkpoint: 第一阶段全自动批次(BASE/J-01/DELTA)；第二阶段人工物理配合窗口(BASE-24等)；独立Codex QA审阅
execution_contract: project-control/docs/planning/vmware_soc_twin_task_execution_20261029.md
readiness_pending:
  - TWIN-54
deliverables:
  artifacts:
    - project-control/docs/evidence/twin/TWIN-55/runs/qa_01/qa_review_report.md
  record: docs/evidence/twin/TWIN-55/runs/qa_01/qa_review_report.md
rollback:
  steps:
    - ssh sushaohua@192.168.77.134 "cd /home/sushaohua/tmp/ai_soc_project/soc-ap && bash tools/deploy_twin.sh --stop --port 8080"
handoff:
  receiver_role: COORD
  receiver_session: ff2fb105-fd84-4ecb-b1e6-8f8eb00badc6
  transport: docs
  evidence_location: docs/evidence/twin/TWIN-55
  acknowledgement: pending
verification:
  commands:
    - id: verify_full_web_hmi_closed_loop_evidence
      cwd: project-control
      command: 'test -f docs/evidence/twin/TWIN-55/runs/qa_01/qa_review_report.md'
      expected: 产出逐例结果、BASE-01~27/J-01/DELTA-DBG/DELTA-BAUD/DELTA-COMB正负与恢复覆盖统计、准确候选与部署身份、软件与真实HIL分范围结论及原始证据索引
      availability: available
  positive_cases:
    - 覆盖BASE-01~27全部适用断言、J-01及DELTA-DBG/BAUD/COMB三组增量，Web/API结果与[MC-DBG]/[TH-DBG]原始日志四方对账一致
  negative_cases:
    - 负例与恢复用例独立展开计数并核验；缺失物理传感器或未满足前置条件的子例按实记录BLOCKED，绝不伪造日志或以Mock/PTY冒充硬件通过
required_evidence_level: hardware-and-collaboration-verified
verification_environment: vmware-and-physical-hil-with-isolated-codex
qa_review_policy: project-control/.agents/rules/codex_qa_review.md
updated: '2026-11-05T11:57:30+08:00'
---

# TWIN-55 Web HMI完整basecase(BASE-01~27/J-01)与三组增量(DELTA-DBG/BAUD/COMB)真实闭环验收
