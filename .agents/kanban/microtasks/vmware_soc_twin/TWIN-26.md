---
id: TWIN-26
title: TWIN-26 双MCU固件升级通道与Bootloader IAP协议复用对账
revision: 1
plan_revision: vmware-soc-twin-20261029
task_kind: implementation
development_stage: vmware-twin
dispatchable: true
status: Backlog
blocked: false
planning_status: planned
owner: null
proposed_owner: ARCH
executor:
  role: ARCH
  agent_id: null
  run_id: null
reviewer:
- QA
- ENG-MC
verifier: null
integrator: INTEGRATOR
review_assignments:
  reviewer_sessions:
  - role: QA
    platform: codex
    model: gpt-6-luna
    planned_session_alias: planned-qa-twin-26
    session: null
    session_evidence: null
    decision: null
    reviewed_task_revision: null
    artifact_version: null
    evidence: null
    report_sha256: null
  - role: ENG-MC
    platform: codex
    model: gpt-6-luna
    planned_session_alias: planned-mc-twin-26
    session: null
    session_evidence: null
    decision: null
    reviewed_task_revision: null
    artifact_version: null
    evidence: null
    report_sha256: null
  verifier_session: null
  integrator_session: null
primary_work_package: TASK-002
related_work_packages:
- TASK-007
- TASK-012
depends_on:
- TWIN-24
dependency_conditions:
- task: TWIN-24
  accepted_version: mcu-p3=9b017f186665c2c9226146cc0fdc34af3ad5242b
  acceptance_evidence: docs/evidence/twin/TWIN-24/runs/run_01/qa_review_report.md
  required: 开工前继承TWIN-24 0x18网格导出与MC固件基线
scope_status: mapped
allowed_repositories:
- mcu-p3
- project-control
write_scope:
  mcu-p3:
  - motion-controller-mcu/project/src/wk_usart.c
  - motion-controller-mcu/project/inc/wk_usart.h
  project-control:
  - docs/evidence/twin/TWIN-26/**
allowed_paths:
- mcu-p3/motion-controller-mcu/project/src/wk_usart.c
- mcu-p3/motion-controller-mcu/project/inc/wk_usart.h
- project-control/docs/evidence/twin/TWIN-26/**
source_baseline:
  project-control: 8ea89b9d1e442894be6bc1f92e4aa1a4c954f9a0
  soc-ap: 6850cc553d405b5e7e511ff181d985fdee8e221f
  mcu-p3: 9b017f186665c2c9226146cc0fdc34af3ad5242b
  test_harness: 0b7497ba43158841eb3c4af7f16e477b9c30c2c5
base_commit: 9b017f186665c2c9226146cc0fdc34af3ad5242b
candidate_commit: null
dispatch_binding:
  source_commit: 9b017f186665c2c9226146cc0fdc34af3ad5242b
  workspace_diff_sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
  consumed_artifact_versions: {}
protocol_input:
  path: project-control/docs/analysis/mcu_firmware_upgrade_design_20261031.md
  sha256: c5a79270ec6017a071944bbf314ebb11e345ec61d62fee6f5563336110c7505c
  revision: 1
read_sources:
- project-control/docs/planning/product/first_release_scope_decision_20261029.md
- project-control/docs/planning/product/first_release_requirements_and_task_decomposition_20261029.md
- project-control/docs/analysis/mcu_firmware_upgrade_design_20261031.md
- project-control/.agents/rules/c_cpp_coding_standard.md
worktree: mcu-p3
lease:
  owner: null
  task_revision: 1
  lease_id: null
  expires_at: null
resources:
- resource: isolated-worktree-and-build-output
  location: null
  exclusive: true
  pending: null
budget:
  planned_checkpoint_minutes: 30
  max_evidence_based_corrections: 2
  on_limit: 保存证据交COORD
checkpoint: 开工前绑定；通道对账与IAP握手自检；准确候选独立检查；收件
execution_contract: project-control/docs/planning/vmware_soc_twin_task_execution_20261029.md
readiness_pending: []
deliverables:
  artifacts:
  - mcu-p3/motion-controller-mcu/project/src/wk_usart.c
  - mcu-p3/motion-controller-mcu/project/inc/wk_usart.h
  record: docs/evidence/twin/TWIN-26/runs/<actual-run>/result.md
rollback:
  steps:
  - 仅回退本票候选；保存失败证据和原状态；硬件恢复须按实际SOP及授权执行
handoff:
  receiver_role: COORD
  receiver_session: session-coord-main
  transport: docs
  evidence_location: docs/evidence/twin/TWIN-26
  acknowledgement: null
verification:
  commands:
  - id: check_graph
    cwd: .
    command: PYTHONDONTWRITEBYTECODE=1 python3 project-control/tools/check_task_graph.py
      --workspace .
    expected: 结构无错误；不等于任务/运行/硬件接受
    availability: local
  - id: planned_build_and_acceptance
    cwd: .
    command: Ready前由Owner绑定本票实际构建与正反例运行入口
    expected: 遵守避免修改Bootloader原则；TH IAP 0x10~0x13时序与MC透传模式验证；函数<=50行
    availability: planned-not-runnable
  positive_cases:
  - 依据ARCH-MCU-UPGRADE-DESIGN-20261031，TH UART IAP握手（0x10~0x13）与MC透传模式满足契约
  negative_cases:
  - 校验失败立即中止，强电加热占空比恒为0%锁死
required_evidence_level: software-verified
verification_environment: isolated-host-or-document
qa_review_policy: project-control/.agents/rules/codex_qa_review.md
updated: '2026-10-31T11:30:00+08:00'
---

# TWIN-26 双MCU固件升级通道与Bootloader IAP协议复用对账

## 1. 目标与依据

根据系统决定 **U-D05**（首版纳入 VMware 指定目录真实双 MCU 固件升级），本任务落实双 MCU 升级通道契约与 Bootloader IAP 协议复用：
1. 恪守“避免修改 Bootloader”绝对优先原则：TH 100% 沿用存量 `bootloader423.bin`（Base `0x08000000`）；MC 评估并冻结硬件探针通道/透传通道；
2. 规范化 TH 921600 波特率 UART IAP 分块协议（`CMD_TH_HELLO 0x10`, `CMD_TH_START_UPG 0x11`, `CMD_TH_PUSH_CHUNK 0x12`, `CMD_TH_FINISH 0x13`）与 `M997 S0` 软复位时序；
3. 在 MC 固件 `wk_usart.c` 中完善 `FORWARD_UART_MODE_UPGRADE` 升级透传控制；
4. 严格遵守 C/C++ 编码规范（函数 $\le 50$ 行、参数 $\le 4$ 个，零堆分配，加热占空比恒为 0%）。

参考文档：
- [ARCH-MCU-UPGRADE-DESIGN-20261031.md](../../../../docs/analysis/mcu_firmware_upgrade_design_20261031.md)
