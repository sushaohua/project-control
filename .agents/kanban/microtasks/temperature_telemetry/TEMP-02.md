---
id: TEMP-02
title: TEMP-02 TH 喷头温度驱动重构与应答实现
revision: 1
plan_revision: marlin-r2
task_kind: implementation
dispatchable: true
status: Done
blocked: false
planning_status: closed-done
owner: th-session-20261028
proposed_owner: ENG-TH
executor:
  role: ENG-TH
  agent_id: th-session-20261028
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
    planned_session_alias: codex-qa-temp02-review
    session: 7f1cda3e-d24d-40ed-92d7-c40afe3a440c
    decision: APPROVED
    reviewed_task_revision: 1
    artifact_version: 1.0.0
    evidence: docs/evidence/temperature_increment/TEMP-02/runs/run_01/qa_review_report.md
    report_sha256: 38e7ca500fb9ddf3e59f55163ca52477e6b1e16eebae28611625faae3841ba9c
  - role: ARCH
    session: arch-session-20261028
    decision: APPROVED
    reviewed_task_revision: 1
    artifact_version: 1.0.0
    evidence: docs/evidence/temperature_increment/TEMP-02/runs/run_01/result.md
  verifier_session: null
  integrator_session: null
primary_work_package: TASK-007
requirement:
- PILOT-REQ-01
- PILOT-REQ-04
depends_on:
- TEMP-01
dependency_conditions:
- task: TEMP-01
  accepted_version: 5675a50c07e8c908aa7da8b3ad90252bf53d253aad78fc26f0e246cb26243a4d
  acceptance_evidence: docs/evidence/temperature_increment/TEMP-01/runs/run_01/result.md
  required: 绑定温度遥测ICD与结构体头文件
scope_status: mapped
allowed_repositories:
- mcu-p3
- project-control
write_scope:
  mcu-p3:
  - color-engine-mcu/io_toggle/src/app/thermistor_adc.c
  - color-engine-mcu/io_toggle/src/app/minimc_proto.c
  - color-engine-mcu/io_toggle/inc/thermistor_adc.h
  project-control:
  - docs/evidence/temperature_increment/TEMP-02/**
allowed_paths:
- mcu-p3/color-engine-mcu/io_toggle/src/app/thermistor_adc.c
- mcu-p3/color-engine-mcu/io_toggle/src/app/minimc_proto.c
- mcu-p3/color-engine-mcu/io_toggle/inc/thermistor_adc.h
- project-control/docs/evidence/temperature_increment/TEMP-02/**
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
- resource: th-firmware
  location: null
  exclusive: false
  pending: TH固件工作区
lease:
  owner: th-session-20261028
  task_revision: 1
  lease_id: lease-temp02-th-20261028-01
  expires_at: '2026-10-28T22:30:00+08:00'
budget:
  planned_checkpoint_minutes: 30
  max_evidence_based_corrections: 2
  on_limit: 保存失败交COORD
checkpoint: 开工前；驱动重构完成；固件编译通过
execution_contract: project-control/docs/planning/product/next_increment_design_pl02.md
readiness_pending: []
deliverables:
  artifacts:
  - mcu-p3/color-engine-mcu/io_toggle/build/fw_th.bin
  record: docs/evidence/temperature_increment/TEMP-02/runs/run_01/result.md
rollback:
  steps:
  - 回退TH温度驱动与协议代码修改
handoff:
  receiver_role: COORD
  receiver_session: main
  transport: docs
  evidence_location: docs/evidence/temperature_increment/TEMP-02
  acknowledgement: accepted
verification:
  commands:
  - id: th_build
    cwd: mcu-p3/color-engine-mcu/io_toggle
    command: make -j4
    expected: 编译成功生成fw_th.bin，零警告
    availability: local
  positive_cases:
  - ADC带超时计数保护且响应0x14命令
  negative_cases:
  - 热敏开路短路准确置位0x7FFF
updated: '2026-10-28'
required_evidence_level: hardware-verified
verification_environment: ubuntu-host+real-mcu-hil
qa_review_policy: project-control/.agents/rules/codex_qa_review.md
---

# TEMP-02 TH 喷头温度驱动重构与应答实现

在 color-engine-mcu 中展开 while(!FLAG) 死等，实现带超时退出的 ADC 采样，实现 NTC 查表，并响应 0x14 温度查询。加热 PWM 占空比硬锁死为 0。
