---
id: TWIN-48
title: TWIN-48 TH固件(AT32F423)新协议控制与0x1C G-code全功能打通、温度误锁死修复与真机交叉编译
revision: 1
plan_revision: vmware-soc-twin-20261104
task_kind: implementation
development_stage: vmware-twin
dispatchable: true
status: Done
blocked: false
planning_status: closed
owner: 7812a1f6-5006-4971-a954-802f855cf20a
proposed_owner: ENG-TH
executor:
  role: ENG-TH
  agent_id: 7812a1f6-5006-4971-a954-802f855cf20a
  run_id: author_01
qa_policy: streamlined-v1
reviewer:
- QA
verifier: null
integrator: INTEGRATOR
feature_id: FEAT-20261104-001
confirmation_id: CONFIRM-DEBUG-BAUD-20261104
approval_id: APPR-20261104-001
accepted_scope: "C unit-test verification in Docker QA sandbox (gcc) of TH (AT32F423) MiniMCProto V2 control opcodes (0x10 SET_TEMP, 0x15/0x19 SLOT_SELECT & FILAMENT_CONTROL, 0x17 MOTION_STOP, 0x1C GCODE_EXEC), mycontrol.c G/M/T queue bridging (th_control_enqueue_gcode & th_control_poll_once), thermistor_adc.c false safety-lock fix, USART1 raw ASCII suppression, and genuine [TH-DBG] (USART3 115200) RX->STATE->TX ACK log emission. Cross-compiler ELF build and physical MCU USB/UART HIL are not applicable in qa-sandbox:20261029 (host arm-none-eabi-gcc build is verified in author_01 and physical HIL in TWIN-50): qa-sandbox:20261029 provides host GCC/Python only and no physical MCU hardware; all in-scope checks are executed in server_qa so unexecuted is empty when those checks pass."
review_assignments:
  reviewer_sessions:
  - role: QA
    platform: codex
    model: gpt-6-luna
    planned_session_alias: planned-qa-twin-48
    session: 01a1a639-77f0-7f01-a9ae-b5d814dcfae1
    reviewer_session: 01a1a639-77f0-7f01-a9ae-b5d814dcfae1
    commit_sha: 016e1236af75f6f19282d6b000f4b1b68bd96cc3
    session_evidence:
      path: /home/sushaohua/workspace/ai_soc_project/project-control/docs/evidence/twin/TWIN-48/runs/qa_01/codex_events.jsonl
      sha256: 860cb9bfb805db5f0a50de29512e4d2eac5f037fce58d3c632661246403e3632
    decision: APPROVED
    reviewed_task_revision: 1
    artifact_version: project-control=17e0887da07ceb3b017623b791b6a6999e837c79; soc-ap=c2c5a228c81488bca2178488a4e8a109b0472d72; mcu-p3=016e1236af75f6f19282d6b000f4b1b68bd96cc3; test_harness=30c21f74e74179994eb475c38cc4afc2c1427a26
    report_path: /home/sushaohua/workspace/ai_soc_project/project-control/docs/evidence/twin/TWIN-48/runs/qa_01/qa_review_report.md
    evidence: docs/evidence/twin/TWIN-48/runs/qa_01/qa_review_report.md
    report_sha256: 2ce43f4c546d1a8617b0103e5ce92f3b7d7756a95ffebf09e649c89341283b83
  verifier_session: null
  integrator_session: null
primary_work_package: TASK-002
related_work_packages:
- TASK-007
- TASK-010
depends_on:
- TWIN-45
- TWIN-47
dependency_conditions:
- task: TWIN-45
  accepted_version: project-control=42b031efff970b01ee8cc8e5dd087387cdf9288f; soc-ap=426d604e9ddcfdb3e95e94ecff4f699ae976fc95; mcu-p3=29d62ef1bb7cf33e334f7e58aae81717cd26c54f; test_harness=ccf1476a0b98cb55ca9ee7bd49d73ca5d4704414
  acceptance_evidence: docs/evidence/twin/TWIN-45/runs/qa_01/qa_review_report.md
  required: 继承TWIN-45 TH USART1 921600级联收发与USART3 [TH-DBG]非阻塞日志基线
- task: TWIN-47
  accepted_version: project-control=17e0887da07ceb3b017623b791b6a6999e837c79; soc-ap=c2c5a228c81488bca2178488a4e8a109b0472d72; mcu-p3=d86041814689b2f353d6fe0b372d31689b826a98; test_harness=30c21f74e74179994eb475c38cc4afc2c1427a26
  acceptance_evidence: docs/evidence/twin/TWIN-47/runs/qa_03/qa_review_report.md
  required: 继承TWIN-47 MC端控制命令结构与0x1C级联二进制协议基线
scope_status: mapped
allowed_repositories:
- mcu-p3
- project-control
write_scope:
  mcu-p3:
  - color-engine-mcu/io_toggle/inc/minimc_proto.h
  - color-engine-mcu/io_toggle/src/app/minimc_proto.c
  - color-engine-mcu/io_toggle/src/app/mycontrol.c
  - color-engine-mcu/io_toggle/src/app/thermistor_adc.c
  - color-engine-mcu/io_toggle/src/app/stepper.c
  - color-engine-mcu/io_toggle/src/user/main.c
  - color-engine-mcu/io_toggle/inc/usart.h
  - color-engine-mcu/io_toggle/src/bsp/usart.c
  - color-engine-mcu/io_toggle/src/user/test_twin45_th_debug.c
  project-control:
  - docs/evidence/twin/TWIN-48/**
allowed_paths:
- mcu-p3/color-engine-mcu/io_toggle/inc/minimc_proto.h
- mcu-p3/color-engine-mcu/io_toggle/src/app/minimc_proto.c
- mcu-p3/color-engine-mcu/io_toggle/src/app/mycontrol.c
- mcu-p3/color-engine-mcu/io_toggle/src/app/thermistor_adc.c
- mcu-p3/color-engine-mcu/io_toggle/src/app/stepper.c
- mcu-p3/color-engine-mcu/io_toggle/src/user/main.c
- mcu-p3/color-engine-mcu/io_toggle/inc/usart.h
- mcu-p3/color-engine-mcu/io_toggle/src/bsp/usart.c
- mcu-p3/color-engine-mcu/io_toggle/src/user/test_twin45_th_debug.c
- project-control/docs/evidence/twin/TWIN-48/**
forbidden_paths:
- mcu-p3/motion-controller-mcu/**
- soc-ap/**
- test_harness/**
- boot/**
source_baseline:
  project-control: 17e0887da07ceb3b017623b791b6a6999e837c79
  soc-ap: c2c5a228c81488bca2178488a4e8a109b0472d72
  mcu-p3: d86041814689b2f353d6fe0b372d31689b826a98
  test_harness: 30c21f74e74179994eb475c38cc4afc2c1427a26
base_commit: d86041814689b2f353d6fe0b372d31689b826a98
branch: feat/soc-debug
candidate_commit: 016e1236af75f6f19282d6b000f4b1b68bd96cc3
dispatch_binding:
  source_commit: d86041814689b2f353d6fe0b372d31689b826a98
  workspace_diff_sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
  consumed_artifact_versions:
    remediation_plan: 21dd6cc16b9eb7d643662b6fba681e6360f4dcd98cdece55439c6f759c5b22cc
protocol_input:
  path: project-control/docs/planning/end_to_end_physical_link_remediation_plan_20261104.md
  sha256: 21dd6cc16b9eb7d643662b6fba681e6360f4dcd98cdece55439c6f759c5b22cc
  revision: 3
icd_versions:
- path: project-control/docs/planning/end_to_end_physical_link_remediation_plan_20261104.md
  version: 3
read_sources:
- project-control/.agents/rules/repository_rule_sources.json
- project-control/.agents/rules/repository_rule_boundaries.md
- mcu-p3/.repo-rules/AGENTS.md
- mcu-p3/.repo-rules/SOURCE.json
- project-control/.agents/rules/c_cpp_coding_standard.md
- project-control/.agents/rules/code_documentation_standard.md
- project-control/docs/planning/end_to_end_physical_link_remediation_plan_20261104.md
worktree: mcu-p3
lease:
  owner: 7812a1f6-5006-4971-a954-802f855cf20a
  task_revision: 1
  lease_id: lease-twin-48-20261104-01
  expires_at: '2026-11-04T21:00:00+08:00'
resources:
- resource: th-host-gcc-test-env
  location: mcu-p3/color-engine-mcu/io_toggle
  exclusive: true
  pending: null
budget:
  planned_checkpoint_minutes: 60
  max_evidence_based_corrections: 2
  on_limit: 保存证据交COORD
checkpoint: 开工前绑定；C模块单测与交叉编译自检；独立沙箱与QA审查；收件
execution_contract: project-control/docs/planning/vmware_soc_twin_task_execution_20261029.md
readiness_pending: []
deliverables:
  artifacts:
  - mcu-p3/color-engine-mcu/io_toggle/inc/minimc_proto.h
  - mcu-p3/color-engine-mcu/io_toggle/inc/usart.h
  - mcu-p3/color-engine-mcu/io_toggle/src/app/minimc_proto.c
  - mcu-p3/color-engine-mcu/io_toggle/src/app/mycontrol.c
  - mcu-p3/color-engine-mcu/io_toggle/src/app/stepper.c
  - mcu-p3/color-engine-mcu/io_toggle/src/app/thermistor_adc.c
  - mcu-p3/color-engine-mcu/io_toggle/src/bsp/usart.c
  - mcu-p3/color-engine-mcu/io_toggle/src/user/main.c
  - mcu-p3/color-engine-mcu/io_toggle/src/user/test_twin45_th_debug.c
  record: docs/evidence/twin/TWIN-48/runs/author_01/result.md
rollback:
  steps:
  - git -C mcu-p3 checkout -- color-engine-mcu/io_toggle/
handoff:
  receiver_role: COORD
  receiver_session: ff2fb105-fd84-4ecb-b1e6-8f8eb00badc6
  transport: docs
  evidence_location: docs/evidence/twin/TWIN-48
  acknowledgement: received-author_01-016e1236af75f6f19282d6b000f4b1b68bd96cc3
verification:
  commands:
  - id: build_and_test_th_control_and_debug
    cwd: mcu-p3/color-engine-mcu/io_toggle
    command: gcc -std=c11 -O2 -Wall -Wextra -no-pie -fno-pie -DAT32F423CCT7 -DUSE_STDPERIPH_DRIVER -DAT_START_F423_V1 -I inc -I inc/temperature_control -I at32f423_board -I src -I src/app -I libraries/cmsis/cm4/core_support -I libraries/cmsis/cm4/device_support -I libraries/drivers/inc src/bsp/usart.c src/app/minimc_proto.c src/user/test_twin45_th_debug.c -o /tmp/test_twin48 && /tmp/test_twin48 && rm -f /tmp/test_twin48
    expected: 容器/宿主gcc编译usart.c、minimc_proto.c与test_twin45_th_debug.c 0错误，全部正例（USART1 921600接收0x01/0x03/0x10/0x14/0x15/0x17/0x19/0x1C级联二进制帧、更新目标温度/激活挤出槽位/队列并真实触发[TH-DBG] RX->STATE->TX ACK）与反例及恢复（未知命令NACK 0x04、非法长度NACK 0x02、CRC_ERR/BAD_FRAME错误日志与恢复、USART3 2048B环形缓冲满丢包与恢复）单测PASS
    availability: available
  positive_cases:
  - TH minimc_proto.c完整支持0x10(SET_TEMP)、0x15/0x19(SLOT_SELECT & FILAMENT_CONTROL)、0x17(MOTION_STOP)、0x1C(GCODE_EXEC)，真实调用th_debug_notify_filament输出[TH-DBG]
  - 修复thermistor_adc.c正常采样误调thermistor_safety_lock问题，解封mycontrol.c M104并静默USART1裸ASCII send_quick输出
  negative_cases:
  - 收到非法级联帧、CRC错误或未知命令时输出[TH-DBG] dir=ERR或NACK且不阻塞后续级联帧恢复
required_evidence_level: server-sandbox-and-independent-review
verification_environment: docker-qa-sandbox-and-isolated-codex
qa_review_policy: project-control/.agents/rules/codex_qa_review.md
updated: '2026-11-04T17:45:00+08:00'
---

# TWIN-48 TH固件(AT32F423)新协议控制与0x1C G-code全功能打通、温度误锁死修复与真机交叉编译

## 1. 任务目标与来源
- **ARCH 方案依据**：[end_to_end_physical_link_remediation_plan_20261104.md](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/planning/end_to_end_physical_link_remediation_plan_20261104.md) (`revision: 3`, SHA-256 `21dd6cc16b9eb7d643662b6fba681e6360f4dcd98cdece55439c6f759c5b22cc`)
- **执行模式**：单工程 Agent（`7812a1f6-5006-4971-a954-802f855cf20a`）顺序垂直贯穿阶段 2/4。

## 2. 验收标准 (`acceptance_criteria`)
1. 在 TH `minimc_proto.{h,c}` 中补齐 `0x10`/`0x15`/`0x17`/`0x19`/`0x1C` 级联控制命令与 G-code 隧道处理，真实触发 `th_debug_notify_filament()` 输出 `[TH-DBG]`。
2. 修复 `thermistor_adc.c` 正常采样误调 `thermistor_safety_lock()` 导致目标温度归零的 Bug；解封 `mycontrol.c` `M104`，暴露 `th_control_enqueue_gcode()` / `th_control_poll_once()`，静默 `USART1` 裸 ASCII。
3. 完成宿主机 GCC 单测与 `arm-none-eabi-gcc` 真机固件 `.elf`/`.bin` 交叉编译校验，全部自研函数满足 $\le 50$ 行、$\le 4$ 入参、中文注释门禁。
