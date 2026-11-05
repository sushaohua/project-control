---
id: TWIN-45
title: TWIN-45 TH固件USART3非阻塞[TH-DBG]全操作结构化日志输出
revision: 1
plan_revision: vmware-soc-twin-20261104
task_kind: implementation
development_stage: vmware-twin
dispatchable: true
status: Done
blocked: false
planning_status: closed
owner: d5309433-d257-4397-b0b5-ef72e5d66d55
proposed_owner: ENG-TH
executor:
  role: ENG-TH
  agent_id: d5309433-d257-4397-b0b5-ef72e5d66d55
  run_id: author_03
qa_policy: streamlined-v1
reviewer:
- QA
verifier: null
integrator: INTEGRATOR
feature_id: FEAT-20261104-001
confirmation_id: CONFIRM-DEBUG-BAUD-20261104
approval_id: APPR-20261104-001
accepted_scope: "C unit-test verification in Docker QA sandbox (gcc) of TH USART1 921600 cascade observation and USART3 115200 2048B non-blocking [TH-DBG] ring logger, real-time sensor/filament state synchronization, 2Hz periodic state summary, and error/overflow recovery. Cross-compiler ELF build and physical MCU USB/UART HIL are not applicable: qa-sandbox:20261029 provides host GCC/Python only and no physical MCU hardware; all in-scope checks are executed in server_qa so unexecuted is empty when those checks pass."
review_assignments:
  reviewer_sessions:
  - role: QA
    platform: codex
    model: gpt-6-luna
    planned_session_alias: planned-qa-twin-45
    session: 01a1a4fd-5e6a-7b91-832a-9d0eb3871d4b
    reviewer_session: 01a1a4fd-5e6a-7b91-832a-9d0eb3871d4b
    commit_sha: 29d62ef1bb7cf33e334f7e58aae81717cd26c54f
    session_evidence:
      path: /home/sushaohua/workspace/ai_soc_project/project-control/docs/evidence/twin/TWIN-45/runs/qa_01/codex_events.jsonl
      sha256: 6dc9ad1f2e67d49be9a9ce1dbff5b5e6f0ca4e36eab71abfbabe8d7258b5ee64
    decision: APPROVED
    reviewed_task_revision: 1
    artifact_version: project-control=42b031efff970b01ee8cc8e5dd087387cdf9288f; soc-ap=426d604e9ddcfdb3e95e94ecff4f699ae976fc95; mcu-p3=29d62ef1bb7cf33e334f7e58aae81717cd26c54f; test_harness=ccf1476a0b98cb55ca9ee7bd49d73ca5d4704414
    report_path: /home/sushaohua/workspace/ai_soc_project/project-control/docs/evidence/twin/TWIN-45/runs/qa_01/qa_review_report.md
    evidence: docs/evidence/twin/TWIN-45/runs/qa_01/qa_review_report.md
    report_sha256: 715a02ee768543db49fd4171147b5ca79e1f80ed954430680d4c06e02ffd48eb
  verifier_session: null
  integrator_session: null
primary_work_package: TASK-002
related_work_packages:
- TASK-007
- TASK-010
depends_on:
- TWIN-16
- TWIN-30
dependency_conditions:
- task: TWIN-16
  accepted_version: mcu-p3=run_01
  acceptance_evidence: docs/evidence/twin/TWIN-16/runs/run_01/qa_review_report.md
  required: 继承TWIN-16及TEMP-02 TH侧温度传感器ADC与协议基线
- task: TWIN-30
  accepted_version: soc-ap=7bb05218c39d6852cac5e8d86db845dbbedd7064; project-control=f7d18c48774a8787f0dfa1d1cbe9dddea9309a40
  acceptance_evidence: docs/evidence/twin/TWIN-30/runs/run_01/qa_review_report.md
  required: 继承TWIN-30及CR-06 TH侧USART1级联收发与USART3非阻塞DMA环形缓冲基线
scope_status: mapped
allowed_repositories:
- mcu-p3
- project-control
write_scope:
  mcu-p3:
  - color-engine-mcu/io_toggle/src/bsp/usart.c
  - color-engine-mcu/io_toggle/inc/usart.h
  - color-engine-mcu/io_toggle/src/user/test_twin45_th_debug.c
  project-control:
  - docs/evidence/twin/TWIN-45/**
allowed_paths:
- mcu-p3/color-engine-mcu/io_toggle/src/bsp/usart.c
- mcu-p3/color-engine-mcu/io_toggle/inc/usart.h
- mcu-p3/color-engine-mcu/io_toggle/src/user/test_twin45_th_debug.c
- project-control/docs/evidence/twin/TWIN-45/**
forbidden_paths:
- mcu-p3/color-engine-mcu/io_toggle/src/user/main.c
- mcu-p3/color-engine-mcu/io_toggle/src/app/minimc_proto.c
- mcu-p3/color-engine-mcu/io_toggle/inc/minimc_proto.h
- mcu-p3/color-engine-mcu/io_toggle/src/app/thermistor_adc.c
- mcu-p3/color-engine-mcu/io_toggle/inc/thermistor_adc.h
- mcu-p3/motion-controller-mcu/**
- soc-ap/**
- test_harness/**
- boot/**
source_baseline:
  project-control: 42b031efff970b01ee8cc8e5dd087387cdf9288f
  soc-ap: 426d604e9ddcfdb3e95e94ecff4f699ae976fc95
  mcu-p3: f34a4b9d3ce03ec02824e1c54dd4dd3052386156
  test_harness: ccf1476a0b98cb55ca9ee7bd49d73ca5d4704414
base_commit: f34a4b9d3ce03ec02824e1c54dd4dd3052386156
branch: feat/soc-debug
candidate_commit: 29d62ef1bb7cf33e334f7e58aae81717cd26c54f
dispatch_binding:
  source_commit: f34a4b9d3ce03ec02824e1c54dd4dd3052386156
  workspace_diff_sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
  consumed_artifact_versions:
    arch_breakdown: 9e66c080771a98ed2e87043c369841dcea0140f0270ae1ebab0d811c613cf5b3
    merged_summary: c469fcd058b8607f454d661a69c07bf8a483e5763d9d231a574d71ee14cd69ec
protocol_input:
  path: project-control/docs/planning/debug_and_921600_merged_implementation_summary_20261104.md
  sha256: c469fcd058b8607f454d661a69c07bf8a483e5763d9d231a574d71ee14cd69ec
  revision: 2
icd_versions:
- path: project-control/docs/architecture/debug_reconciliation_and_921600_arch_breakdown_20261104.md
  version: 10
read_sources:
- project-control/docs/architecture/debug_reconciliation_and_921600_arch_breakdown_20261104.md
- project-control/docs/planning/mc_th_debug_mode_requirement_confirmation_20261103.md
- project-control/.agents/rules/c_cpp_coding_standard.md
- mcu-p3/color-engine-mcu/io_toggle/src/bsp/usart.c
- mcu-p3/color-engine-mcu/io_toggle/inc/usart.h
- mcu-p3/color-engine-mcu/io_toggle/src/user/main.c
- mcu-p3/color-engine-mcu/io_toggle/src/app/minimc_proto.c
worktree: mcu-p3
lease:
  owner: d5309433-d257-4397-b0b5-ef72e5d66d55
  task_revision: 1
  lease_id: lease-twin-45-20261104-01
  expires_at: '2026-11-04T15:00:00+08:00'
resources:
- resource: th-host-gcc-test-env
  location: mcu-p3/color-engine-mcu/io_toggle
  exclusive: true
  pending: null
budget:
  planned_checkpoint_minutes: 60
  max_evidence_based_corrections: 2
  on_limit: 保存证据交COORD
checkpoint: 开工前绑定；C模块单测与静态规范自检；独立沙箱与QA审查；收件
execution_contract: project-control/docs/planning/vmware_soc_twin_task_execution_20261029.md
readiness_pending: []
deliverables:
  artifacts:
  - mcu-p3/color-engine-mcu/io_toggle/src/bsp/usart.c
  - mcu-p3/color-engine-mcu/io_toggle/inc/usart.h
  - mcu-p3/color-engine-mcu/io_toggle/src/user/test_twin45_th_debug.c
  record: docs/evidence/twin/TWIN-45/runs/author_03/result.md
rollback:
  steps:
  - git -C mcu-p3 checkout -- color-engine-mcu/io_toggle/src/bsp/usart.c color-engine-mcu/io_toggle/inc/usart.h && rm -f mcu-p3/color-engine-mcu/io_toggle/src/user/test_twin45_th_debug.c
handoff:
  receiver_role: COORD
  receiver_session: ff2fb105-fd84-4ecb-b1e6-8f8eb00badc6
  transport: docs
  evidence_location: docs/evidence/twin/TWIN-45
  acknowledgement: received-author_03-29d62ef1bb7cf33e334f7e58aae81717cd26c54f
verification:
  commands:
  - id: build_and_test_th_debug_and_cascade
    cwd: mcu-p3/color-engine-mcu/io_toggle
    command: gcc -std=c11 -O2 -Wall -Wextra -no-pie -fno-pie -DAT32F423CCT7 -DUSE_STDPERIPH_DRIVER -DAT_START_F423_V1 -I inc -I inc/temperature_control -I at32f423_board -I src -I src/app -I libraries/cmsis/cm4/core_support -I libraries/cmsis/cm4/device_support -I libraries/drivers/inc src/bsp/usart.c src/app/minimc_proto.c src/user/test_twin45_th_debug.c -o /tmp/test_twin45 && /tmp/test_twin45 && rm -f /tmp/test_twin45
    expected: 容器/宿主gcc编译usart.c、minimc_proto.c与test_twin45_th_debug.c 0错误，全部正例（USART1 921600与USART3 115200初始化、RX/TX/STATE日志与实时传感器/料槽状态同步、2Hz周期摘要）与反例及恢复（USART3 2048B环形缓冲满丢包不阻塞级联响应与排空恢复、>192B截断、CRC_ERR/BAD_FRAME错误日志与DMA恢复）单测PASS
    availability: available
  positive_cases:
  - 保持USART1(PB6/PB7，TH↔MC级联921600)与USART3(PC4/PC5，TH Debug 115200 DMA非阻塞环形缓冲)波特率不变
  - 在usart.c(usart1_rx_pop_raw_byte/usart1_send_raw)中自包含通过USART3_write非阻塞输出[TH-DBG]结构化日志（保持main.c零改动），覆盖dir=RX|TX|STATE|ERR、级联帧命令/seq、喷嘴温度/ADC原始值/挡位及进退丝/料槽操作状态
  - 暴露并携带usart3_tx_drop_count与trunc_count统计字段，周期性温度/状态摘要限频<=2Hz
  negative_cases:
  - 收到非法级联帧或CRC校验失败时，输出[TH-DBG] dir=ERR status=CRC_ERR|BAD_FRAME结构化错误日志且不影响后续USART1级联DMA正常帧恢复
  - 高频打印日志压测下USART3 DMA环形缓冲满时仅递增drop计数，不阻塞USART1级联帧响应；缓冲排空后恢复正常日志输出
required_evidence_level: server-sandbox-and-independent-review
verification_environment: docker-qa-sandbox-and-isolated-codex
qa_review_policy: project-control/.agents/rules/codex_qa_review.md
updated: '2026-11-04T10:40:00+08:00'
---

# TWIN-45 TH固件USART3非阻塞[TH-DBG]全操作结构化日志输出

## 1. 任务目标与来源
- **ARCH 拆分依据**：[debug_reconciliation_and_921600_arch_breakdown_20261104.md](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/architecture/debug_reconciliation_and_921600_arch_breakdown_20261104.md) (`revision: 10`, SHA-256 `9e66c080771a98ed2e87043c369841dcea0140f0270ae1ebab0d811c613cf5b3`, ARCH Session `433026bf-a1ff-4863-8f3e-7a5f43b016ff`)
- **需求与批准绑定**：`FEAT-20261104-001` / `CONFIRM-DEBUG-BAUD-20261104` (`rev 2`) / `APPR-20261104-001` (`rev 1`)

## 2. 验收标准 (`acceptance_criteria`)
1. 保持 TH `USART1` (`PB6`/`PB7` 板间级联 `921600`) 与 `USART3` (`PC4`/`PC5` Debug `115200` DMA 非阻塞) 波特率配置不变。
2. 在 `color-engine-mcu/io_toggle/src/bsp/usart.c` 与 `inc/usart.h` 中自包含完善非阻塞丢包/截断只读计数查询接口，并实现 `TH_DEBUG_MODE_ENABLE` 宏控制下的 `[TH-DBG]` 结构化日志输出（不触碰 `src/user/main.c` 与 `src/app/minimc_proto.c`）。
3. `[TH-DBG]` 完整覆盖级联请求接收 (`dir=RX`)、级联响应发送 (`dir=TX`)、喷嘴温度/ADC/挡位与进退丝/料槽状态变更 (`dir=STATE`，周期限频 $\le 2\text{ Hz}$) 及校验/格式异常 (`dir=ERR`)，并附带 `drop=<u32> trunc=<u32>`。
4. 所有新增/修改 C 函数严格满足 $\le 50$ 行、$\le 4$ 个入参、零动态堆分配门禁，容器 `gcc` 编译与 `test_twin45_th_debug.c` 单元测试零错误。
