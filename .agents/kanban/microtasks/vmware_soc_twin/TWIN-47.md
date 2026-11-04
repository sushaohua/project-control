---
id: TWIN-47
title: TWIN-47 MC固件(AT32F435)控制命令全集打通、Marlin队列桥接、0x1C级联转发与真机交叉编译
revision: 1
plan_revision: vmware-soc-twin-20261104
task_kind: implementation
development_stage: vmware-twin
dispatchable: true
status: Done
blocked: false
planning_status: closed
owner: 7812a1f6-5006-4971-a954-802f855cf20a
proposed_owner: ENG-MC
executor:
  role: ENG-MC
  agent_id: 7812a1f6-5006-4971-a954-802f855cf20a
  run_id: author_03
qa_policy: streamlined-v1
reviewer:
- QA
verifier: null
integrator: INTEGRATOR
feature_id: FEAT-20261104-001
confirmation_id: CONFIRM-DEBUG-BAUD-20261104
approval_id: APPR-20261104-001
accepted_scope: "C unit-test verification in Docker QA sandbox (gcc) of MC (AT32F435) MiniMCProto V2 control opcodes (0x10 SET_TEMP, 0x11 MOTION_HOME, 0x12 MOTION_MOVE, 0x13 JOB_CONTROL, 0x17 MOTION_STOP, 0x18 LEVEL_GRID_QUERY 0B/1B, 0x19 SLOT_SELECT local & TH cascade sync, 0x1A LEVEL_TRIGGER, 0x1C GCODE_EXEC & minimc_proto_send_th_gcode), Marlin queue/heater/quickStop bridging (with bare-board non-blocking strategy A), memu_gui.c 0x55 0xAA DWIN isolation, and genuine [MC-DBG] (USART1 115200) RX->STATE->TX ACK log emission without bypass calls. Cross-compiler ELF build and physical MCU USB/UART HIL are not applicable in qa-sandbox:20261029 (host arm-none-eabi-gcc build is verified in author_01 and physical HIL in TWIN-50): qa-sandbox:20261029 provides host GCC/Python only and no physical MCU hardware; all in-scope checks are executed in server_qa so unexecuted is empty when those checks pass."
review_assignments:
  reviewer_sessions:
  - role: QA
    platform: codex
    model: gpt-6-luna
    planned_session_alias: planned-qa-twin-47
    session: 01a1a61f-f579-7cd0-a857-cd21096242ac
    reviewer_session: 01a1a61f-f579-7cd0-a857-cd21096242ac
    commit_sha: d86041814689b2f353d6fe0b372d31689b826a98
    session_evidence:
      path: /home/sushaohua/workspace/ai_soc_project/project-control/docs/evidence/twin/TWIN-47/runs/qa_03/codex_events.jsonl
      sha256: 6fcf1b57e375c55c57e4ae0a1ad1239e03fd4145b88dd7cd0e53159f9f3f77f6
    decision: APPROVED
    reviewed_task_revision: 1
    artifact_version: project-control=17e0887da07ceb3b017623b791b6a6999e837c79; soc-ap=c2c5a228c81488bca2178488a4e8a109b0472d72; mcu-p3=d86041814689b2f353d6fe0b372d31689b826a98; test_harness=30c21f74e74179994eb475c38cc4afc2c1427a26
    report_path: /home/sushaohua/workspace/ai_soc_project/project-control/docs/evidence/twin/TWIN-47/runs/qa_03/qa_review_report.md
    evidence: docs/evidence/twin/TWIN-47/runs/qa_03/qa_review_report.md
    report_sha256: 91cb27f444234a1e87d17de1ccf0dd303c06b6036ce31a187671662d2832a78e
  verifier_session: null
  integrator_session: null
primary_work_package: TASK-002
related_work_packages:
- TASK-007
- TASK-010
depends_on:
- TWIN-26
- TWIN-44
dependency_conditions:
- task: TWIN-26
  accepted_version: mcu-p3=04231388c842c1ce3e5b71675d0dc118a65edf2e; project-control=37be0fe2cb7bc945c888aabbcb2bb7d8a8068dea; soc-ap=f2596517c8e7a53da6ff9623d948ec5e70bf6770; test_harness=0b7497ba43158841eb3c4af7f16e477b9c30c2c5
  acceptance_evidence: docs/evidence/twin/TWIN-26/runs/run_01/qa_review_report.md
  required: 继承TWIN-26 wk_usart.c与MC串口级联基线
- task: TWIN-44
  accepted_version: project-control=42b031efff970b01ee8cc8e5dd087387cdf9288f; soc-ap=427dd6d82caceebb7b4642e78f1dbfa96ff5fc84; mcu-p3=f34a4b9d3ce03ec02824e1c54dd4dd3052386156; test_harness=ccf1476a0b98cb55ca9ee7bd49d73ca5d4704414
  acceptance_evidence: docs/evidence/twin/TWIN-44/runs/qa_06/qa_review_report.md
  required: 继承TWIN-44 MC USART2 921600与USART1非阻塞[MC-DBG]环形缓冲日志基线
scope_status: mapped
allowed_repositories:
- mcu-p3
- project-control
write_scope:
  mcu-p3:
  - motion-controller-mcu/project/inc/minimc_proto.h
  - motion-controller-mcu/project/src/minimc_proto.c
  - motion-controller-mcu/project/src/wk_usart.c
  - motion-controller-mcu/project/marlin/marlin_core/Marlin_main.c
  - motion-controller-mcu/project/marlin/marlin_lcd/memu_gui.c
  - motion-controller-mcu/project/src/test_twin44_mc_debug.c
  project-control:
  - docs/evidence/twin/TWIN-47/**
allowed_paths:
- mcu-p3/motion-controller-mcu/project/inc/minimc_proto.h
- mcu-p3/motion-controller-mcu/project/src/minimc_proto.c
- mcu-p3/motion-controller-mcu/project/src/wk_usart.c
- mcu-p3/motion-controller-mcu/project/marlin/marlin_core/Marlin_main.c
- mcu-p3/motion-controller-mcu/project/marlin/marlin_lcd/memu_gui.c
- mcu-p3/motion-controller-mcu/project/src/test_twin44_mc_debug.c
- project-control/docs/evidence/twin/TWIN-47/**
forbidden_paths:
- mcu-p3/color-engine-mcu/**
- soc-ap/**
- test_harness/**
- boot/**
source_baseline:
  project-control: 17e0887da07ceb3b017623b791b6a6999e837c79
  soc-ap: c2c5a228c81488bca2178488a4e8a109b0472d72
  mcu-p3: 02ec2da65e38ffa3931026d961f685551981abd9
  test_harness: 30c21f74e74179994eb475c38cc4afc2c1427a26
base_commit: 02ec2da65e38ffa3931026d961f685551981abd9
branch: feat/soc-debug
candidate_commit: d86041814689b2f353d6fe0b372d31689b826a98
dispatch_binding:
  source_commit: 02ec2da65e38ffa3931026d961f685551981abd9
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
  lease_id: lease-twin-47-20261104-01
  expires_at: '2026-11-04T21:00:00+08:00'
resources:
- resource: mcu-host-gcc-test-env
  location: mcu-p3/motion-controller-mcu
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
  - mcu-p3/motion-controller-mcu/project/inc/minimc_proto.h
  - mcu-p3/motion-controller-mcu/project/src/minimc_proto.c
  - mcu-p3/motion-controller-mcu/project/src/wk_usart.c
  - mcu-p3/motion-controller-mcu/project/marlin/marlin_core/Marlin_main.c
  - mcu-p3/motion-controller-mcu/project/marlin/marlin_lcd/memu_gui.c
  - mcu-p3/motion-controller-mcu/project/src/test_twin44_mc_debug.c
  record: docs/evidence/twin/TWIN-47/runs/author_03/result.md
rollback:
  steps:
  - git -C mcu-p3 checkout -- motion-controller-mcu/
handoff:
  receiver_role: COORD
  receiver_session: ff2fb105-fd84-4ecb-b1e6-8f8eb00badc6
  transport: docs
  evidence_location: docs/evidence/twin/TWIN-47
  acknowledgement: received-author_03-d86041814689b2f353d6fe0b372d31689b826a98
verification:
  commands:
  - id: build_and_test_mc_control_and_debug
    cwd: mcu-p3/motion-controller-mcu
    command: gcc -std=c11 -O2 -Wall -Wextra -no-pie -fno-pie -DAT32F435VGT7 -DUSE_STDPERIPH_DRIVER -I project/inc -I project/delay -I project/marlin -I project/marlin/marlin_core -I project/marlin/marlin_module -I libraries/drivers/inc -I libraries/cmsis/cm4/core_support -I libraries/cmsis/cm4/device_support project/src/minimc_proto.c project/src/test_twin44_mc_debug.c -o /tmp/test_twin47 && /tmp/test_twin47 && rm -f /tmp/test_twin47
    expected: 容器/宿主gcc编译minimc_proto.c与test_twin44_mc_debug.c 0错误，全部正例（0x01/0x03/0x10/0x11/0x12/0x13/0x14/0x16/0x17/0x18(0B&1B)/0x19/0x1A/0x1C二进制控制与查询帧驱动Marlin桥接并自动触发[MC-DBG] RX->STATE->TX ACK、TH级联控制响应0x10->0x15/0x19->0x19/0x1C->0x1C关联同步、minimc_proto_send_th_gcode二进制封装）与反例及恢复（未知命令0xFE返回NACK 0x04、非法长度NACK 0x02、CRC错误与恢复、环形缓冲满丢包与恢复、非预期TH帧拦截与恢复、底层发送失败抑制伪ACK与恢复）单测PASS
    availability: available
  positive_cases:
  - minimc_proto.h与minimc_proto.c完整实现0x10(SET_TEMP)、0x11(MOTION_HOME)、0x12(MOTION_MOVE)、0x13(JOB_CONTROL)、0x17(MOTION_STOP)、0x18(LEVEL_GRID_QUERY 0B/1B)、0x19(SLOT_SELECT)、0x1A(LEVEL_TRIGGER)、0x1C(GCODE_EXEC)控制分支，真实调用Marlin桥接并触发mc_debug_notify_*输出[MC-DBG]
  - wk_usart.c的forward_uart_send_line升级为调用minimc_proto_send_th_gcode发送0x1C二进制级联帧，memu_gui.c隔离0x55 0xAA避免污染迪文屏状态机
  negative_cases:
  - 收到未知命令(如0xFE)、载荷长度不足或CRC错误帧时返回对应NACK/ERR日志且不破坏状态，后续合法帧立即恢复
  - 环形缓冲满或底层发送失败时不阻塞业务且不伪造ACK，排空或恢复后正常闭环
required_evidence_level: server-sandbox-and-independent-review
verification_environment: docker-qa-sandbox-and-isolated-codex
qa_review_policy: project-control/.agents/rules/codex_qa_review.md
updated: '2026-11-04T17:45:00+08:00'
---

# TWIN-47 MC固件(AT32F435)控制命令全集打通、Marlin队列桥接、0x1C级联转发与真机交叉编译

## 1. 任务目标与来源
- **ARCH 方案依据**：[end_to_end_physical_link_remediation_plan_20261104.md](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/planning/end_to_end_physical_link_remediation_plan_20261104.md) (`revision: 3`, SHA-256 `21dd6cc16b9eb7d643662b6fba681e6360f4dcd98cdece55439c6f759c5b22cc`)
- **执行模式**：单工程 Agent（`7812a1f6-5006-4971-a954-802f855cf20a`）顺序垂直贯穿阶段 1/4。

## 2. 验收标准 (`acceptance_criteria`)
1. 在 `minimc_proto.h` 与 `minimc_proto.c` 中补齐 `0x10`/`0x11`/`0x12`/`0x13`/`0x17`/`0x18`/`0x19`/`0x1A`/`0x1C` 全部控制命令处理、Marlin 桥接及真实 `[MC-DBG]` 触发（兼容裸板/半挂载防阻塞策略 A）。
2. 将 `wk_usart.c:forward_uart_send_line()` 升级为 `minimc_proto_send_th_gcode()` (`0x1C` 二进制帧)，消除 `USART6` 裸 ASCII 发送；在 `memu_gui.c` 隔离 `0x55 0xAA` 帧。
3. 完成宿主机 GCC 单测与 `arm-none-eabi-gcc` 真机固件 `.elf`/`.bin` 交叉编译校验，全部自研函数满足 $\le 50$ 行、$\le 4$ 入参、中文注释门禁。
