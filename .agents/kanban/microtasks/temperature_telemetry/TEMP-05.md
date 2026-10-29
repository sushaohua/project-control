---
id: TEMP-05
title: TEMP-05 物理台架三端工程联调与消缺
revision: 1
plan_revision: marlin-r2
task_kind: verification
dispatchable: true
status: Done
blocked: false
planning_status: closed-done
owner: integrator-session-20261028
proposed_owner: INTEGRATOR
executor:
  role: INTEGRATOR
  agent_id: integrator-session-20261028
  run_id: run_01
reviewer:
- QA
- ARCH
verifier: null
integrator: null
review_assignments:
  reviewer_sessions:
  - role: QA
    platform: codex
    model: gpt-6-luna
    planned_session_alias: codex-qa-temp05-review
    session: 7f1cda3e-d24d-40ed-92d7-c40afe3a440c
    decision: APPROVED
    reviewed_task_revision: 1
    artifact_version: 1.0.0
    evidence: docs/evidence/temperature_increment/TEMP-05/runs/run_01/qa_review_report.md
    report_sha256: 5ff096da80980be6e765a77959fa3bdcd354aadb09e2e1b9314b835aecfc40c6
  - role: ARCH
    session: arch-session-20261028
    decision: APPROVED
    reviewed_task_revision: 1
    artifact_version: 1.0.0
    evidence: docs/evidence/temperature_increment/TEMP-05/runs/run_01/result.md
  verifier_session: null
  integrator_session: null
primary_work_package: TASK-012
requirement:
- PILOT-REQ-01
- PILOT-REQ-04
depends_on:
- TEMP-02
- TEMP-03
- TEMP-04
dependency_conditions:
- task: TEMP-02
  accepted_version: 16e145e19649e1294e68f15da449405da744680cd1fcc4929d4aa5763a5e446c
  acceptance_evidence: docs/evidence/temperature_increment/TEMP-02/runs/run_01/result.md
  required: 绑定TH温度固件制品
- task: TEMP-03
  accepted_version: 4bbd7f6321f55f029ae257338f9ef30bf8af4b179dd323e7113e9a2f59ca49b8
  acceptance_evidence: docs/evidence/temperature_increment/TEMP-03/runs/run_01/result.md
  required: 绑定MC温度固件制品
- task: TEMP-04
  accepted_version: 5a1e31eb34ea6b2d36c6cac2abe6c10d0da37daeb5474ce8236a664f95d22776
  acceptance_evidence: docs/evidence/temperature_increment/TEMP-04/runs/run_01/result.md
  required: 绑定AP温度CLI程序
scope_status: mapped
allowed_repositories:
- project-control
write_scope:
  project-control:
  - docs/evidence/temperature_increment/TEMP-05/**
  - docs/releases/ap_mc_th_temperature_candidate.yaml
allowed_paths:
- project-control/docs/evidence/temperature_increment/TEMP-05/**
- project-control/docs/releases/ap_mc_th_temperature_candidate.yaml
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
    TEMP-02: 16e145e19649e1294e68f15da449405da744680cd1fcc4929d4aa5763a5e446c
    TEMP-03: 4bbd7f6321f55f029ae257338f9ef30bf8af4b179dd323e7113e9a2f59ca49b8
    TEMP-04: 5a1e31eb34ea6b2d36c6cac2abe6c10d0da37daeb5474ce8236a664f95d22776
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
  owner: integrator-session-20261028
  task_revision: 1
  lease_id: lease-temp05-integrator-20261028-01
  expires_at: '2026-10-29T18:00:00+08:00'
budget:
  planned_checkpoint_minutes: 30
  max_evidence_based_corrections: 2
  on_limit: 保存失败交COORD
checkpoint: 开工前；固件刷写完成；在环双端温度穿透成功
execution_contract: project-control/docs/planning/product/next_increment_design_pl02.md
readiness_pending: []
deliverables:
  artifacts:
  - project-control/docs/evidence/temperature_increment/TEMP-05/result.md
  - project-control/docs/releases/ap_mc_th_temperature_candidate.yaml
  record: docs/evidence/temperature_increment/TEMP-05/runs/run_01/result.md
rollback:
  steps:
  - 仅回退联调测试日志与候选描述
handoff:
  receiver_role: COORD
  receiver_session: main
  transport: docs
  evidence_location: docs/evidence/temperature_increment/TEMP-05
  acknowledgement: null
verification:
  commands:
  - id: mc_temp
    cwd: .
    command: ssh vmware "~/soc-ap --port /dev/ttyUSB0 --target mc --cmd temp --json"
    expected: 成功返回MC热床当前室温读数
    availability: local
  - id: th_temp
    cwd: .
    command: ssh vmware "~/soc-ap --port /dev/ttyUSB0 --target th --cmd temp --json"
    expected: 成功返回TH喷头当前室温读数，双跳穿透RTT<=10ms
    availability: local
  positive_cases:
  - MC热床与TH喷头温度读数在环正常返回
  negative_cases:
  - TH离线时触发超时，不返回假数据
updated: '2026-10-28'
required_evidence_level: hardware-verified
verification_environment: ubuntu-host+real-mcu-hil
qa_review_policy: project-control/.agents/rules/codex_qa_review.md
---

# TEMP-05 物理台架三端工程联调与消缺

在真实物理台架上执行 AP ↔ MC ↔ TH 温度遥测穿透联调，采集分段与全链路数据，排除现场兼容性缺陷，装配发布 RC3 候选清单。
