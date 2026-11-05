---
id: TWIN-60
title: TWIN-60 双MCU固件热床量程/ADC透传、[MC-DBG]消截断去裸打印、动态boot_id/版本绑定及feat/soc-debug中文注释补齐
revision: 1
plan_revision: vmware-soc-twin-20261105
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
requirement_id: REQ-20261105-002
demand_id: DEM-20261105-018
confirmation_id: CONFIRM-TWIN55-REMEDIATION-AND-COMMENTS-20261105
approval_id: APPR-20261105-004
accepted_scope: "C unit-test verification in Docker QA sandbox (gcc) on mcu-p3 (feat/soc-debug, candidate 191e355a4227268a472bafd6862d4a8c854e0544) of ISS-20261105-010 (MC 0x19 slot/action out-of-range NACK 0x03), ISS-20261105-011/012 (MC bed g_last_bed_adc_raw passthrough and 5~130°C/ADC out-of-range 0x7FFF fault sentinel), ISS-20261105-015 (removal of thermistor.c bare printf(\"adc SS_ADC_BUSY\") and expansion of MC_DBG_LINE_MAX_LEN to 256U / RING_CAPACITY to 4096U), ISS-20261105-016 (MC/TH dynamic boot_id generation and FW_GIT_COMMIT_SHORT binding), and Batch MCU-MC & MCU-TH Chinese code comments across the 26 modified files (ISS-20261105-018). Cross-compiler ELF build and physical MCU HIL are not applicable in qa-sandbox:20261029 (host arm-none-eabi-gcc build is verified in author_01 and physical HIL in TWIN-55); all in-scope checks are executed in server_qa so unexecuted is empty when those checks pass."
review_assignments:
  reviewer_sessions:
  - role: QA
    platform: codex
    model: gpt-6-luna
    planned_session_alias: planned-qa-twin-60
    session: null
    decision: PENDING
    evidence: docs/evidence/twin/TWIN-60/runs/qa_01/qa_review_report.md
  verifier_session: null
  integrator_session: null
primary_work_package: TASK-009
related_work_packages:
- TASK-007
- TASK-010
depends_on:
- TWIN-56
dependency_conditions:
- task: TWIN-56
  accepted_version: project-control=99cd83bb40b4ecf53e8f9dd996ad61ecb653f6f0; soc-ap=79932746d225bb115010c5545ef3f7499482e137;
    mcu-p3=891a8bb252814c83992a49b01fbe11ba83b92a1f; test_harness=d14ed04321c6d4f5ddb35a8801604a8af53b5b60
  acceptance_evidence: docs/evidence/twin/TWIN-56/runs/qa_03/qa_review_report.md
  required: 继承TWIN-56 16-bit seq日志与三仓锁定基线
scope_status: mapped
allowed_repositories:
- mcu-p3
- project-control
write_scope:
  mcu-p3:
  - motion-controller-mcu/**
  - color-engine-mcu/io_toggle/**
  project-control:
  - docs/evidence/twin/TWIN-60/**
allowed_paths:
- mcu-p3/motion-controller-mcu/**
- mcu-p3/color-engine-mcu/io_toggle/**
- project-control/docs/evidence/twin/TWIN-60/**
forbidden_paths:
- soc-ap/**
- test_harness/**
- boot/**
source_baseline:
  project-control: 960f079647a00864fe7913836336b2a2ee3d729a
  soc-ap: 79932746d225bb115010c5545ef3f7499482e137
  mcu-p3: 891a8bb252814c83992a49b01fbe11ba83b92a1f
  test_harness: d14ed04321c6d4f5ddb35a8801604a8af53b5b60
base_commit: 891a8bb252814c83992a49b01fbe11ba83b92a1f
branch: feat/soc-debug
candidate_commit: 191e355a4227268a472bafd6862d4a8c854e0544
dispatch_binding:
  source_commit: 891a8bb252814c83992a49b01fbe11ba83b92a1f
  workspace_diff_sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
  consumed_artifact_versions:
    arch_breakdown: 5bcfbaf2ca96d2bba58abab17b3368c243235f778e0bd99a2293a136ee50ee4d
protocol_input:
  path: project-control/docs/architecture/twin55_issues_005_017_consolidated_remediation_plan_20261105.md
  sha256: 5bcfbaf2ca96d2bba58abab17b3368c243235f778e0bd99a2293a136ee50ee4d
  revision: 1
icd_versions:
- path: project-control/docs/architecture/twin55_issues_005_017_consolidated_remediation_plan_20261105.md
  version: 1
read_sources:
- project-control/.agents/rules/repository_rule_sources.json
- project-control/.agents/rules/repository_rule_boundaries.md
- project-control/.agents/rules/c_cpp_coding_standard.md
- project-control/.agents/rules/web_ui_coding_standard.md
- project-control/.agents/rules/code_documentation_standard.md
- project-control/docs/architecture/twin55_issues_005_017_consolidated_remediation_plan_20261105.md
- project-control/docs/architecture/code_comments_remediation_arch_breakdown_20261105.md
worktree: mcu-p3
lease:
  owner: 07a1f6dc-f47c-45e5-bf00-37ec14e2dfda
  task_revision: 1
  lease_id: lease-twin-60-20261105-01
  expires_at: '2026-11-05T22:00:00+08:00'
resources:
- resource: mcu-p3-worktree
  location: mcu-p3
  exclusive: false
  pending: null
budget:
  planned_checkpoint_minutes: 45
  max_evidence_based_corrections: 2
  on_limit: 保存证据交COORD
checkpoint: 开工前绑定；自检单测与注释规范检查；独立沙箱与QA审查；收件
execution_contract: project-control/docs/planning/vmware_soc_twin_task_execution_20261029.md
readiness_pending: []
deliverables:
  artifacts:
  - mcu-p3/color-engine-mcu/io_toggle/Makefile
  - mcu-p3/color-engine-mcu/io_toggle/inc/minimc_proto.h
  - mcu-p3/color-engine-mcu/io_toggle/inc/minimc_telemetry.h
  - mcu-p3/color-engine-mcu/io_toggle/inc/thermistor_adc.h
  - mcu-p3/color-engine-mcu/io_toggle/inc/usart.h
  - mcu-p3/color-engine-mcu/io_toggle/src/app/minimc_proto.c
  - mcu-p3/color-engine-mcu/io_toggle/src/app/mycontrol.c
  - mcu-p3/color-engine-mcu/io_toggle/src/app/stepper.c
  - mcu-p3/color-engine-mcu/io_toggle/src/app/thermistor_adc.c
  - mcu-p3/color-engine-mcu/io_toggle/src/bsp/usart.c
  - mcu-p3/color-engine-mcu/io_toggle/src/user/main.c
  - mcu-p3/color-engine-mcu/io_toggle/src/user/test_twin45_th_debug.c
  - mcu-p3/motion-controller-mcu/CMakeLists.txt
  - mcu-p3/motion-controller-mcu/project/inc/minimc_proto.h
  - mcu-p3/motion-controller-mcu/project/inc/minimc_telemetry.h
  - mcu-p3/motion-controller-mcu/project/inc/wk_usart.h
  - mcu-p3/motion-controller-mcu/project/marlin/configure.h
  - mcu-p3/motion-controller-mcu/project/marlin/marlin_core/Marlin_main.c
  - mcu-p3/motion-controller-mcu/project/marlin/marlin_lcd/dgus_t300spro.c
  - mcu-p3/motion-controller-mcu/project/marlin/marlin_lcd/memu_gui.c
  - mcu-p3/motion-controller-mcu/project/marlin/marlin_module/thermistor.c
  - mcu-p3/motion-controller-mcu/project/marlin/marlin_module/thermistor.h
  - mcu-p3/motion-controller-mcu/project/src/main.c
  - mcu-p3/motion-controller-mcu/project/src/minimc_proto.c
  - mcu-p3/motion-controller-mcu/project/src/test_twin44_mc_debug.c
  - mcu-p3/motion-controller-mcu/project/src/wk_usart.c
  record: docs/evidence/twin/TWIN-60/runs/author_01/result.md
rollback:
  steps:
  - git -C mcu-p3 checkout -- .
handoff:
  receiver_role: COORD
  receiver_session: ff2fb105-fd84-4ecb-b1e6-8f8eb00badc6
  transport: docs
  evidence_location: docs/evidence/twin/TWIN-60
  acknowledgement: accepted
verification:
  commands:
  - id: verify_twin-60
    cwd: mcu-p3
    command: gcc -std=c11 -O2 -Wall -Wextra -no-pie -fno-pie -DAT32F435VGT7 -DUSE_STDPERIPH_DRIVER
      -I motion-controller-mcu/project/inc -I motion-controller-mcu/project/delay
      -I motion-controller-mcu/project/marlin -I motion-controller-mcu/project/marlin/marlin_core
      -I motion-controller-mcu/project/marlin/marlin_module -I motion-controller-mcu/libraries/drivers/inc
      -I motion-controller-mcu/libraries/cmsis/cm4/core_support -I motion-controller-mcu/libraries/cmsis/cm4/device_support
      motion-controller-mcu/project/src/minimc_proto.c motion-controller-mcu/project/src/test_twin44_mc_debug.c
      -o /tmp/test_twin60_mc && /tmp/test_twin60_mc && rm -f /tmp/test_twin60_mc &&
      gcc -std=c11 -O2 -Wall -Wextra -no-pie -fno-pie -DAT32F423CCT7 -DUSE_STDPERIPH_DRIVER
      -DAT_START_F423_V1 -I color-engine-mcu/io_toggle/inc -I color-engine-mcu/io_toggle/inc/temperature_control
      -I color-engine-mcu/io_toggle/at32f423_board -I color-engine-mcu/io_toggle/src
      -I color-engine-mcu/io_toggle/src/app -I color-engine-mcu/io_toggle/libraries/cmsis/cm4/core_support
      -I color-engine-mcu/io_toggle/libraries/cmsis/cm4/device_support -I color-engine-mcu/io_toggle/libraries/drivers/inc
      color-engine-mcu/io_toggle/src/bsp/usart.c color-engine-mcu/io_toggle/src/app/minimc_proto.c
      color-engine-mcu/io_toggle/src/user/test_twin45_th_debug.c -o /tmp/test_twin60_th
      && /tmp/test_twin60_th && rm -f /tmp/test_twin60_th
    expected: 编译与全部单元/契约回归测试100%通过，且目标范围内代码中文注释符合code_documentation_standard.md
    availability: available
  positive_cases:
  - 在mcu-p3仓库feat/soc-debug分支修复ISS-20261105-010(MC 0x19槽位/动作越界返回NACK 0x03)、ISS-20261105-011/012(MC热床真实ADC
    g_last_bed_adc_raw透传与5~130°C/ADC超界0x7FFF故障哨兵判定)、ISS-20261105-015(移除thermistor.c裸printf("adc
    SS_ADC_BUSY")并将MC_DBG_LINE_MAX_LEN扩容至256U、RING_CAPACITY扩容至4096U)、ISS-20261105-016(MC/TH动态boot_id生成与FW_GIT_COMMIT_SHORT绑定)，并同步完成Batch
    MCU-MC & MCU-TH共24个文件的中文注释补齐(ISS-20261105-018)。
  negative_cases:
  - 边界越界、非法参数、超时与断链场景按契约拒绝或降级，无回归破坏
required_evidence_level: server-sandbox-and-independent-review
verification_environment: docker-qa-sandbox-and-isolated-codex
qa_review_policy: project-control/.agents/rules/codex_qa_review.md
updated: '2026-11-05T16:02:00+08:00'
---

# TWIN-60 双MCU固件热床量程/ADC透传、[MC-DBG]消截断去裸打印、动态boot_id/版本绑定及feat/soc-debug中文注释补齐

## 1. 任务目标与来源
- **ARCH 方案依据**：[project-control/docs/architecture/twin55_issues_005_017_consolidated_remediation_plan_20261105.md](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/architecture/twin55_issues_005_017_consolidated_remediation_plan_20261105.md) (`sha256: 5bcfbaf2ca96d2bba58abab17b3368c243235f778e0bd99a2293a136ee50ee4d`)
- **注释规范方案**：[code_comments_remediation_arch_breakdown_20261105.md](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/architecture/code_comments_remediation_arch_breakdown_20261105.md) (`sha256: 5073d7e45aa8fbd5e8f8422a775df73ddc7970d8061363b715d673feec0ada94`)

## 2. 验收标准 (`acceptance_criteria`)
1. 在mcu-p3仓库feat/soc-debug分支修复ISS-20261105-010(MC 0x19槽位/动作越界返回NACK 0x03)、ISS-20261105-011/012(MC热床真实ADC g_last_bed_adc_raw透传与5~130°C/ADC超界0x7FFF故障哨兵判定)、ISS-20261105-015(移除thermistor.c裸printf("adc SS_ADC_BUSY")并将MC_DBG_LINE_MAX_LEN扩容至256U、RING_CAPACITY扩容至4096U)、ISS-20261105-016(MC/TH动态boot_id生成与FW_GIT_COMMIT_SHORT绑定)，并同步完成Batch MCU-MC & MCU-TH共24个文件的中文注释补齐(ISS-20261105-018)。
2. 全部新增/修改函数严格遵守单函数 <= 50 行、入参 <= 4 个，且目标文件完整具备符合 `code_documentation_standard.md` 的中文文件头、结构体、函数与关键逻辑注释。
