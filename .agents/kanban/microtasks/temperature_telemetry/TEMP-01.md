---
id: TEMP-01
title: TEMP-01 温度遥测 ICD 契约冻结与数据结构定义
revision: 1
plan_revision: marlin-r2
task_kind: design
dispatchable: true
status: Done
blocked: false
planning_status: closed-done
owner: arch-session-20261028
proposed_owner: ARCH
executor:
  role: ARCH
  agent_id: arch-session-20261028
  run_id: run_01
reviewer:
- QA
- ENG-FWD
- ENG-MC
- ENG-TH
verifier: null
integrator: null
review_assignments:
  reviewer_sessions:
  - role: QA
    platform: codex
    model: gpt-6-luna
    planned_session_alias: codex-qa-temp01-review
    session: 7f1cda3e-d24d-40ed-92d7-c40afe3a440c
    decision: APPROVED
    reviewed_task_revision: 1
    artifact_version: 1.0.0
    evidence: docs/evidence/temperature_increment/TEMP-01/runs/run_01/qa_review_report.md
    report_sha256: e772df7c839e57ec9cafeeb4fcd9ec98d8b50cf7e5d497906741fca22a8b0d8b
  - role: ENG-FWD
    session: fwd-session-20261028
    decision: APPROVED
    reviewed_task_revision: 1
    artifact_version: 1.0.0
    evidence: docs/evidence/temperature_increment/TEMP-01/runs/run_01/result.md
  - role: ENG-MC
    session: mc-session-20261028
    decision: APPROVED
    reviewed_task_revision: 1
    artifact_version: 1.0.0
    evidence: docs/evidence/temperature_increment/TEMP-01/runs/run_01/result.md
  - role: ENG-TH
    session: th-session-20261028
    decision: APPROVED
    reviewed_task_revision: 1
    artifact_version: 1.0.0
    evidence: docs/evidence/temperature_increment/TEMP-01/runs/run_01/result.md
  verifier_session: null
  integrator_session: null
primary_work_package: TASK-005
requirement:
- PILOT-REQ-01
- PILOT-REQ-04
depends_on:
- PL-02
- CR-11
dependency_conditions:
- task: PL-02
  accepted_version: 75f3512b80a72266aa1bd0f53ee7fe1b523ac4179396f3261a307e85a18bd30a
  acceptance_evidence: docs/planning/product/next_increment_design_pl02.md
  required: 绑定增量架构设计与操作码纠偏基线
- task: CR-11
  accepted_version: commit f859487
  acceptance_evidence: docs/evidence/cascade_recovery/CR-11/result.md
  required: 绑定级联恢复闭环与锁文件基线
scope_status: mapped
allowed_repositories:
- project-control
- soc-ap
- mcu-p3
write_scope:
  project-control:
  - docs/interfaces/ap_mc_th_telemetry_icd.md
  - docs/evidence/temperature_increment/TEMP-01/**
  soc-ap:
  - contracts/minimcproto/minimc_telemetry.h
  mcu-p3:
  - motion-controller-mcu/project/inc/minimc_telemetry.h
  - color-engine-mcu/io_toggle/inc/minimc_telemetry.h
allowed_paths:
- project-control/docs/interfaces/ap_mc_th_telemetry_icd.md
- project-control/docs/evidence/temperature_increment/TEMP-01/**
- soc-ap/contracts/minimcproto/minimc_telemetry.h
- mcu-p3/motion-controller-mcu/project/inc/minimc_telemetry.h
- mcu-p3/color-engine-mcu/io_toggle/inc/minimc_telemetry.h
source_baseline:
  project-control: a5e4b5e97439cae4a7093d1d0a29c5dc9b3c7819
  soc-ap: 4445c8fedc21bafef5e6c971fcb54cec703f0e71
  mcu-p3: 1246ea9cb441d074ea444f53320f5632fefcd503
  test_harness: 6c61ce6e51cf83d7fb58d319c23cb91bf95786cb
base_commit: a5e4b5e97439cae4a7093d1d0a29c5dc9b3c7819
dispatch_binding:
  source_commit: a5e4b5e97439cae4a7093d1d0a29c5dc9b3c7819
  workspace_diff_sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
  consumed_artifact_versions: {}
protocol_input:
  path: project-control/docs/specs/ap_mc_formal_protocol_v2_0_multidevice_routing_draft_20261015.md
  sha256: 9f8d4f9607cb3e76cc30b9ee2f971b23c3e0d936611188466a71f4aa15f3ce54
  revision: 2.0.3
read_sources:
- project-control/docs/planning/product/next_increment_design_pl02.md
- project-control/.agents/rules/c_cpp_coding_standard.md
worktree: /home/sushaohua/workspace/ai_soc_project
resources:
- resource: contract-definition
  location: null
  exclusive: false
  pending: 契约冻结
lease:
  owner: arch-session-20261028
  task_revision: 1
  lease_id: lease-temp01-arch-20261028-01
  expires_at: '2026-10-28T22:00:00+08:00'
budget:
  planned_checkpoint_minutes: 30
  max_evidence_based_corrections: 2
  on_limit: 保存失败交COORD
checkpoint: 开工前；契约完成；独立审查完成
execution_contract: project-control/docs/planning/product/next_increment_design_pl02.md
readiness_pending: []
deliverables:
  artifacts:
  - project-control/docs/interfaces/ap_mc_th_telemetry_icd.md
  - soc-ap/contracts/minimcproto/minimc_telemetry.h
  - mcu-p3/motion-controller-mcu/project/inc/minimc_telemetry.h
  - mcu-p3/color-engine-mcu/io_toggle/inc/minimc_telemetry.h
  record: docs/evidence/temperature_increment/TEMP-01/runs/run_01/result.md
rollback:
  steps:
  - 只回退本票修改的头文件与ICD文档
handoff:
  receiver_role: COORD
  receiver_session: main
  transport: docs
  evidence_location: docs/evidence/temperature_increment/TEMP-01
  acknowledgement: accepted
verification:
  commands:
  - id: check_graph
    cwd: .
    command: PYTHONDONTWRITEBYTECODE=1 python3 project-control/tools/check_task_graph.py --workspace .
    expected: 结构无错误
    availability: local
  - id: header_compile
    cwd: soc-ap
    command: gcc -fsyntax-only -I contracts/minimcproto contracts/minimcproto/minimc_telemetry.h
    expected: 语法检查通过，静态断言成功
    availability: local
  positive_cases:
  - 16字节载荷结构体静态对齐且各端头文件一致
  negative_cases:
  - 结构体尺寸偏离16字节触发编译期断言报错
updated: '2026-10-28'
required_evidence_level: document
verification_environment: planning
qa_review_policy: project-control/.agents/rules/codex_qa_review.md
---

# TEMP-01 温度遥测 ICD 契约冻结与数据结构定义

定义 MiniMCProto v2.0 温度遥测增补规范与数据结构。
操作码：`MINIMC_CMD_GET_TEMP = 0x14`。
16 字节对齐结构体 `minimc_temp_report_payload_t` 及状态码定义。
