---
id: TWIN-64
title: TWIN-64 MC/TH App 520B载荷扩容、0x1D受控进Boot、MC维护透明路由与th_upgrade_mgr同构迁移
revision: 1
plan_revision: vmware-soc-twin-20261106
task_kind: implementation
development_stage: vmware-twin
dispatchable: true
status: Review
blocked: false
planning_status: active
owner: 07a1f6dc-f47c-45e5-bf00-37ec14e2dfda
proposed_owner: ENG-MC
executor:
  role: ENG-MC
  agent_id: 07a1f6dc-f47c-45e5-bf00-37ec14e2dfda
  run_id: author_01
qa_policy: streamlined-v1
reviewer:
- QA
verifier: null
integrator: INTEGRATOR
requirement_id: REQ-20261105-003
demand_id: DEM-20261105-006
confirmation_id: CONFIRM-MINIMC-V2-UNIFIED-UPGRADE-20261106
approval_id: APPR-20261106-001
accepted_scope: "Docker QA sandbox (gcc + python3) verification of MC/TH App Rev 2.0.4 alignment (520B max payload, 0x17 EMERGENCY_STOP, 0x19 FILAMENT_CONTROL, 0x1D SYSTEM_CONTROL, 0x20~0x23 OTA macros), MC App DST=0x03 maintenance transparent routing (600B UART buffers, drain_th_rx 534B fix, proxy_active & 5000ms timeout recovery), 0x1D safe heater-off/stepper-disable + 4B CMD_ACK + magic word + reset, dynamic TH boot_id, th_upgrade_mgr.c migration to MiniMCProto v2.0 with 236K linker limit, TWIN-44/45/60 regressions, and S04 function length (<=50), params (<=4) & Chinese comment checks. Cross-compiler arm-none-eabi-gcc ELF/bin build and physical HIL verification (covered by TWIN-67) are out of scope for qa-sandbox:20261029; all in-scope checks are executed in server_qa so unexecuted is empty when those checks pass."
review_assignments:
  reviewer_sessions:
  - role: QA
    platform: codex
    model: gpt-6-luna
    planned_session_alias: planned-qa-twin-64
    session: null
    decision: PENDING
    evidence: docs/evidence/twin/TWIN-64/runs/qa_01/qa_review_report.md
  verifier_session: null
  integrator_session: null
primary_work_package: TASK-009
related_work_packages:
- TASK-007
- TASK-012
depends_on:
- TWIN-60
dependency_conditions:
- task: TWIN-60
  accepted_version: project-control=960f079647a00864fe7913836336b2a2ee3d729a; soc-ap=79932746d225bb115010c5545ef3f7499482e137;
    mcu-p3=57674d8b07d6c75a4d20b3fcd52c23df964aa7a7; test_harness=d14ed04321c6d4f5ddb35a8801604a8af53b5b60
  acceptance_evidence: docs/evidence/twin/TWIN-60/runs/qa_02/qa_review_report.md
  required: 继承TWIN-60 mcu-p3双端固件基线
scope_status: mapped
allowed_repositories:
- mcu-p3
- project-control
write_scope:
  mcu-p3:
  - motion-controller-mcu/project/inc/minimc_proto.h
  - motion-controller-mcu/project/src/minimc_proto.c
  - motion-controller-mcu/project/inc/wk_dma.h
  - motion-controller-mcu/project/src/wk_usart.c
  - motion-controller-mcu/project/inc/th_upgrade_mgr.h
  - motion-controller-mcu/project/marlin/marlin_module/th_upgrade_mgr.c
  - motion-controller-mcu/tests/**
  - color-engine-mcu/io_toggle/inc/minimc_proto.h
  - color-engine-mcu/io_toggle/src/app/minimc_proto.c
  - color-engine-mcu/io_toggle/src/app/mycontrol.c
  - color-engine-mcu/io_toggle/libraries/cmsis/cm4/device_support/startup/gcc/linker/AT32F423xC_FLASH.ld
  - color-engine-mcu/tests/**
  project-control:
  - docs/evidence/twin/TWIN-64/**
allowed_paths:
- mcu-p3/motion-controller-mcu/project/inc/minimc_proto.h
- mcu-p3/motion-controller-mcu/project/src/minimc_proto.c
- mcu-p3/motion-controller-mcu/project/inc/wk_dma.h
- mcu-p3/motion-controller-mcu/project/src/wk_usart.c
- mcu-p3/motion-controller-mcu/project/inc/th_upgrade_mgr.h
- mcu-p3/motion-controller-mcu/project/marlin/marlin_module/th_upgrade_mgr.c
- mcu-p3/motion-controller-mcu/tests/**
- mcu-p3/color-engine-mcu/io_toggle/inc/minimc_proto.h
- mcu-p3/color-engine-mcu/io_toggle/src/app/minimc_proto.c
- mcu-p3/color-engine-mcu/io_toggle/src/app/mycontrol.c
- mcu-p3/color-engine-mcu/io_toggle/libraries/cmsis/cm4/device_support/startup/gcc/linker/AT32F423xC_FLASH.ld
- mcu-p3/color-engine-mcu/tests/**
- project-control/docs/evidence/twin/TWIN-64/**
forbidden_paths:
- soc-ap/**
- boot/**
- test_harness/**
- mcu-p3/.repo-rules/**
source_baseline:
  project-control: c1d2c461aa65e6497c295843a2735d0d02ee2e2d
  soc-ap: c6692b244e0aa09d04e7051293f9fef3c67535dd
  mcu-p3: 57674d8b07d6c75a4d20b3fcd52c23df964aa7a7
  test_harness: 19c12bfeeac852670e8bdcb65ce0abcd1de121c1
  boot/bootloadermc: 4fc171ea61912561949b9a0cfc1da8975e4c39ba
  boot/bootloaderth: 769fccbe52464ad7ceb856c5e89cb0d25abbbf87
base_commit: 57674d8b07d6c75a4d20b3fcd52c23df964aa7a7
branch: feat/soc-debug
candidate_commit: 5c8aa04366231cbf8115ecf1c00db1ce43ecd664
dispatch_binding:
  source_commit: 57674d8b07d6c75a4d20b3fcd52c23df964aa7a7
  workspace_diff_sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
  consumed_artifact_versions:
    master_upgrade_architecture: b2b6d047500180c9f4d67d72c94794cbe5080caa52901ba262aa089bc1543223
    protocol_v2_0_4: ec874cab3f8f98fec6412b2da2b4f1fa52bfd8a33601da21e908b0ffaeb0522c
protocol_input:
  path: project-control/docs/specs/ap_mc_formal_protocol_v2_0_4_unified_ota_20261106.md
  sha256: ec874cab3f8f98fec6412b2da2b4f1fa52bfd8a33601da21e908b0ffaeb0522c
  revision: Rev 2.0.4
icd_versions:
- path: project-control/docs/architecture/minimc_v2_unified_mcu_upgrade_architecture_20261105.md
  version: 2
- path: project-control/docs/specs/ap_mc_formal_protocol_v2_0_4_unified_ota_20261106.md
  version: Rev 2.0.4
read_sources:
- project-control/.agents/rules/repository_rule_sources.json
- project-control/.agents/rules/repository_rule_boundaries.md
- project-control/.agents/rules/bootloader_role_boundaries.md
- project-control/.agents/rules/c_cpp_coding_standard.md
- project-control/.agents/rules/code_documentation_standard.md
- project-control/docs/architecture/minimc_v2_unified_mcu_upgrade_architecture_20261105.md
- project-control/docs/specs/ap_mc_formal_protocol_v2_0_4_unified_ota_20261106.md
- project-control/docs/planning/minimc_v2_upgrade_engineering_inputs_20261105.md
- project-control/docs/planning/minimc_v2_upgrade_qa_planning_input_20261105.md
- project-control/docs/guides/minimc_v2_mcu_upgrade_and_hil_deployment_manual_20261105.md
worktree: mcu-p3
lease:
  owner: 07a1f6dc-f47c-45e5-bf00-37ec14e2dfda
  task_revision: 1
  lease_id: lease-twin-64-20261106-01
  expires_at: '2026-11-07T22:00:00+08:00'
resources:
- resource: mcu-p3-worktree
  location: mcu-p3
  exclusive: false
  pending: null
budget:
  planned_checkpoint_minutes: 60
  max_evidence_based_corrections: 2
  on_limit: 保存证据交COORD
checkpoint: 开工前绑定；自检单测与注释规范检查；独立沙箱与QA审查；收件
execution_contract: project-control/docs/planning/vmware_soc_twin_task_execution_20261029.md
readiness_pending: []
deliverables:
  artifacts:
  - mcu-p3/motion-controller-mcu/project/inc/minimc_proto.h
  - mcu-p3/motion-controller-mcu/project/src/minimc_proto.c
  - mcu-p3/motion-controller-mcu/project/inc/th_upgrade_mgr.h
  - mcu-p3/motion-controller-mcu/project/marlin/marlin_module/th_upgrade_mgr.c
  - mcu-p3/color-engine-mcu/io_toggle/inc/minimc_proto.h
  - mcu-p3/color-engine-mcu/io_toggle/src/app/minimc_proto.c
  - mcu-p3/color-engine-mcu/io_toggle/libraries/cmsis/cm4/device_support/startup/gcc/linker/AT32F423xC_FLASH.ld
  record: docs/evidence/twin/TWIN-64/runs/author_01/result.md
rollback:
  steps:
  - git -C mcu-p3 checkout -- .
handoff:
  receiver_role: COORD
  receiver_session: ff2fb105-fd84-4ecb-b1e6-8f8eb00badc6
  transport: docs
  evidence_location: docs/evidence/twin/TWIN-64
  acknowledgement: accepted
verification:
  commands:
  - id: build_and_test_twin-64
    cwd: mcu-p3
    command: rm -rf /tmp/qa_twin64 && cp -r . /tmp/qa_twin64 && cd /tmp/qa_twin64/motion-controller-mcu/tests
      && sh run_tests.sh && cd /tmp/qa_twin64/color-engine-mcu/tests && sh run_tests.sh
      && rm -rf /tmp/qa_twin64
    expected: MC与TH宿主机协议、534B路由、0x1D受控进Boot及th_upgrade_mgr v2.0单元测试100%通过
    availability: available
  positive_cases:
  - MC/TH App扩容至MINIMC_MAX_PAYLOAD_SIZE=520B，对齐Rev 2.0.4命令表，实现0x1D安全停机回4B CMD_ACK置魔数软复位、MC维护态DST=0x03
    534B大帧透明路由、TH动态boot_id及th_upgrade_mgr.c同构v2.0升级
  negative_cases:
  - 非空闲安全态拒绝0x1D回NACK 0x05；严禁在业务串口发送M997或5A A5私有帧；AT32F423xC_FLASH.ld限制FLASH LENGTH
    = 236K
required_evidence_level: server-sandbox-and-independent-review
verification_environment: docker-qa-sandbox-and-isolated-codex
qa_review_policy: project-control/.agents/rules/codex_qa_review.md
updated: '2026-11-06T09:55:00+08:00'
---

# TWIN-64 MC/TH App 520B载荷扩容、0x1D受控进Boot、MC维护透明路由与th_upgrade_mgr同构迁移

## 1. 权威架构与协议契约依据
- **主架构方案（`revision: 2`）**：[project-control/docs/architecture/minimc_v2_unified_mcu_upgrade_architecture_20261105.md](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/architecture/minimc_v2_unified_mcu_upgrade_architecture_20261105.md) (`sha256: b2b6d047500180c9f4d67d72c94794cbe5080caa52901ba262aa089bc1543223`)
- **协议主规范（`Rev 2.0.4`）**：[project-control/docs/specs/ap_mc_formal_protocol_v2_0_4_unified_ota_20261106.md](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/specs/ap_mc_formal_protocol_v2_0_4_unified_ota_20261106.md) (`sha256: ec874cab3f8f98fec6412b2da2b4f1fa52bfd8a33601da21e908b0ffaeb0522c`)

## 2. 验收标准 (`acceptance_criteria`)
1. MC/TH App扩容至MINIMC_MAX_PAYLOAD_SIZE=520B，对齐Rev 2.0.4命令表，实现0x1D安全停机回4B CMD_ACK置魔数软复位、MC维护态DST=0x03 534B大帧透明路由、TH动态boot_id及th_upgrade_mgr.c同构v2.0升级
2. 非空闲安全态拒绝0x1D回NACK 0x05；严禁在业务串口发送M997或5A A5私有帧；AT32F423xC_FLASH.ld限制FLASH LENGTH = 236K
3. 全部新增/修改自研函数 100% 满足单函数 <= 50 行、入参 <= 4 个、零动态堆分配，且具备符合 `code_documentation_standard.md` 的中文说明注释。
