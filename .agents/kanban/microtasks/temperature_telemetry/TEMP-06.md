---
id: TEMP-06
title: TEMP-06 独立真实 HIL 验收复验与安全断线测试
revision: 1
plan_revision: marlin-r2
task_kind: verification
dispatchable: true
status: Done
blocked: false
planning_status: closed-done
owner: 7f1cda3e-d24d-40ed-92d7-c40afe3a440c
proposed_owner: QA
executor:
  role: QA
  agent_id: 7f1cda3e-d24d-40ed-92d7-c40afe3a440c
  run_id: run_01
reviewer:
- ARCH
verifier: null
integrator: null
review_assignments:
  reviewer_sessions:
  - role: ARCH
    platform: codex
    model: gpt-6-luna
    planned_session_alias: codex-arch-temp06-review
    session: 212d83ba-56f8-4c1b-9b5a-46e87a340671
    decision: APPROVED
    reviewed_task_revision: 1
    artifact_version: 1.0.0
    evidence: docs/evidence/temperature_increment/TEMP-06/runs/run_01/arch_review_report.md
    report_sha256: 72df8d31d3e95458115616a4baeaf6c334609af604ca31ebf0e8bacbb02cac4b
  verifier_session: null
  integrator_session: null
primary_work_package: TASK-010
requirement:
- PILOT-REQ-01
- PILOT-REQ-04
depends_on:
- TEMP-05
dependency_conditions:
- task: TEMP-05
  accepted_version: dd5acaf0df09bcbed48ac092f62441171240f8b9410842df84f0a783ff67868a
  acceptance_evidence: docs/evidence/temperature_increment/TEMP-05/runs/run_01/result.md
  required: 绑定联调稳定的RC3候选清单与台架环境
scope_status: mapped
allowed_repositories:
- project-control
write_scope:
  project-control:
  - docs/evidence/temperature_increment/TEMP-06/**
allowed_paths:
- project-control/docs/evidence/temperature_increment/TEMP-06/**
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
    TEMP-05: dd5acaf0df09bcbed48ac092f62441171240f8b9410842df84f0a783ff67868a
protocol_input:
  path: project-control/docs/specs/ap_mc_formal_protocol_v2_0_multidevice_routing_draft_20261015.md
  sha256: 9f8d4f9607cb3e76cc30b9ee2f971b23c3e0d936611188466a71f4aa15f3ce54
  revision: 2.0.3
read_sources:
- project-control/docs/planning/product/next_increment_design_pl02.md
- project-control/docs/operations/ap_mc_th_joint_debug.md
worktree: /home/sushaohua/workspace/ai_soc_project
resources:
- resource: physical-hil-bench
  location: VMware Ubuntu + /dev/ttyUSB0 + AT32F435 MC + AT32F423 TH
  exclusive: true
  pending: null
lease:
  owner: 7f1cda3e-d24d-40ed-92d7-c40afe3a440c
  task_revision: 1
  lease_id: lease-temp06-qa-20261029-01
  expires_at: '2026-10-29T18:00:00+08:00'
budget:
  planned_checkpoint_minutes: 30
  max_evidence_based_corrections: 2
  on_limit: 保存失败交COORD
checkpoint: 开工前；40轮实测完成；断线开路故障注入完成；独立ARCH复核闭环
execution_contract: project-control/docs/planning/product/next_increment_design_pl02.md
readiness_pending: []
deliverables:
  artifacts:
  - project-control/docs/evidence/temperature_increment/TEMP-06/result.md
  record: docs/evidence/temperature_increment/TEMP-06/runs/run_01/result.md
rollback:
  steps:
  - 仅回退HIL测试证据记录
handoff:
  receiver_role: COORD
  receiver_session: main
  transport: docs
  evidence_location: docs/evidence/temperature_increment/TEMP-06
  acknowledgement: null
verification:
  commands:
  - id: hil_bench_mc
    cwd: .
    command: ssh vmware "~/soc-ap --port /dev/ttyUSB0 --target mc --cmd temp --json"
    expected: 40轮实测双端室温读数精准返回，加热PWM实测为0
    availability: local
  - id: hil_bench_th
    cwd: .
    command: ssh vmware "~/soc-ap --port /dev/ttyUSB0 --target th --cmd temp --json"
    expected: TH喷头温度读数穿透返回，双跳时延稳定
    availability: local
  positive_cases:
  - 40轮实测双端室温读数精准返回，RTT稳定，加热占空比实测为0
  negative_cases:
  - 模拟NTC开路断线或短路，固件精准上报0x7FFF与错误状态码
updated: '2026-10-28'
required_evidence_level: hardware-verified
verification_environment: ubuntu-host+real-mcu-hil
qa_review_policy: project-control/.agents/rules/codex_qa_review.md
---

# TEMP-06 独立真实 HIL 验收复验与安全断线测试

独立 Codex QA 在真实台架上执行 40 轮温度压测，验证 HW-G1~HW-G6 零虚拟化，执行开路短路故障注入，验证加热 PWM 绝对为 0，出具独立 QA 报告与 ARCH 架构复核报告。
