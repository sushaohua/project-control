---
id: TWIN-44
title: TWIN-44 MC固件USART2 921600升级与USART1非阻塞[MC-DBG]结构化日志输出
revision: 1
plan_revision: vmware-soc-twin-20261104
task_kind: implementation
development_stage: vmware-twin
dispatchable: true
status: Done
blocked: false
planning_status: closed
owner: 8ca47c46-1cd8-4f82-955a-9742b6988ded
proposed_owner: ENG-MC
executor:
  role: ENG-MC
  agent_id: 8ca47c46-1cd8-4f82-955a-9742b6988ded
  run_id: author_06
qa_policy: streamlined-v1
reviewer:
- QA
verifier: null
integrator: INTEGRATOR
feature_id: FEAT-20261104-001
confirmation_id: CONFIRM-DEBUG-BAUD-20261104
approval_id: APPR-20261104-001
accepted_scope: "C unit-test verification in Docker QA sandbox (gcc) of MC USART2 921600 reconfiguration, USART1 2048B non-blocking [MC-DBG] ring logger, honest MiniMC V2 command dispatch (preserving NACK 0x04 for unimplemented opcodes), real-time state synchronization (including 0x18 level-grid [MC-DBG] state fields), TH cascade response correlation, minimc_proto_send and forward_uart_send_raw failure handling, and post-error recovery. Cross-compiler ELF build and physical MCU USB/UART HIL are not applicable: qa-sandbox:20261029 provides host GCC/Python only and no physical MCU hardware; all in-scope checks are executed in server_qa so unexecuted is empty when those checks pass."
review_assignments:
  reviewer_sessions:
  - role: QA
    platform: codex
    model: gpt-6-luna
    planned_session_alias: planned-qa-twin-44
    session: 01a1a4f2-21d9-7183-921c-7a4f5d5a3d18
    reviewer_session: 01a1a4f2-21d9-7183-921c-7a4f5d5a3d18
    commit_sha: f34a4b9d3ce03ec02824e1c54dd4dd3052386156
    session_evidence:
      path: /home/sushaohua/workspace/ai_soc_project/project-control/docs/evidence/twin/TWIN-44/runs/qa_06/codex_events.jsonl
      sha256: 47611e60c5abe46f8743235dd825fbf18f44520487c16cd2eba1cc207cfe8c89
    decision: APPROVED
    reviewed_task_revision: 1
    artifact_version: project-control=42b031efff970b01ee8cc8e5dd087387cdf9288f; soc-ap=427dd6d82caceebb7b4642e78f1dbfa96ff5fc84; mcu-p3=f34a4b9d3ce03ec02824e1c54dd4dd3052386156; test_harness=ccf1476a0b98cb55ca9ee7bd49d73ca5d4704414
    report_path: /home/sushaohua/workspace/ai_soc_project/project-control/docs/evidence/twin/TWIN-44/runs/qa_06/qa_review_report.md
    evidence: docs/evidence/twin/TWIN-44/runs/qa_06/qa_review_report.md
    report_sha256: dfbdcadb41b3e1d38a0d6f0d114986cd015907811815b5f6121c276537d6a656
  verifier_session: null
  integrator_session: null
primary_work_package: TASK-002
related_work_packages:
- TASK-007
- TASK-010
depends_on:
- TWIN-24
- TWIN-30
dependency_conditions:
- task: TWIN-24
  accepted_version: mcu-p3=04231388c842c1ce3e5b71675d0dc118a65edf2e
  acceptance_evidence: docs/evidence/twin/TWIN-24/runs/run_01/qa_review_report.md
  required: 继承TWIN-24 MC侧minimc_proto全功能指令处理与级联转发基线
- task: TWIN-30
  accepted_version: soc-ap=7bb05218c39d6852cac5e8d86db845dbbedd7064; project-control=f7d18c48774a8787f0dfa1d1cbe9dddea9309a40
  acceptance_evidence: docs/evidence/twin/TWIN-30/runs/run_01/qa_review_report.md
  required: 继承TWIN-30全流程闭环基线
scope_status: mapped
allowed_repositories:
- mcu-p3
- project-control
write_scope:
  mcu-p3:
  - motion-controller-mcu/project/src/minimc_proto.c
  - motion-controller-mcu/project/inc/minimc_proto.h
  - motion-controller-mcu/project/src/test_twin44_mc_debug.c
  project-control:
  - docs/evidence/twin/TWIN-44/**
allowed_paths:
- mcu-p3/motion-controller-mcu/project/src/minimc_proto.c
- mcu-p3/motion-controller-mcu/project/inc/minimc_proto.h
- mcu-p3/motion-controller-mcu/project/src/test_twin44_mc_debug.c
- project-control/docs/evidence/twin/TWIN-44/**
forbidden_paths:
- mcu-p3/motion-controller-mcu/project/src/main.c
- mcu-p3/motion-controller-mcu/project/src/wk_usart.c
- mcu-p3/motion-controller-mcu/project/inc/wk_usart.h
- mcu-p3/color-engine-mcu/**
- mcu-p3/motion-controller-mcu/project/marlin/**
- soc-ap/**
- test_harness/**
- boot/**
source_baseline:
  project-control: 42b031efff970b01ee8cc8e5dd087387cdf9288f
  soc-ap: 427dd6d82caceebb7b4642e78f1dbfa96ff5fc84
  mcu-p3: e051111e68dd61896ed42c0961153b167b8bca41
  test_harness: ccf1476a0b98cb55ca9ee7bd49d73ca5d4704414
base_commit: e051111e68dd61896ed42c0961153b167b8bca41
branch: feat/soc-debug
candidate_commit: f34a4b9d3ce03ec02824e1c54dd4dd3052386156
dispatch_binding:
  source_commit: e051111e68dd61896ed42c0961153b167b8bca41
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
- project-control/docs/planning/vmware_mc_921600_requirement_confirmation_20261103.md
- project-control/.agents/rules/c_cpp_coding_standard.md
- mcu-p3/motion-controller-mcu/project/src/wk_usart.c
- mcu-p3/motion-controller-mcu/project/src/minimc_proto.c
- mcu-p3/motion-controller-mcu/project/src/main.c
worktree: mcu-p3
lease:
  owner: 8ca47c46-1cd8-4f82-955a-9742b6988ded
  task_revision: 1
  lease_id: lease-twin-44-20261104-01
  expires_at: '2026-11-04T15:00:00+08:00'
resources:
- resource: mcu-host-gcc-test-env
  location: mcu-p3/motion-controller-mcu
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
  - mcu-p3/motion-controller-mcu/project/src/minimc_proto.c
  - mcu-p3/motion-controller-mcu/project/inc/minimc_proto.h
  - mcu-p3/motion-controller-mcu/project/src/test_twin44_mc_debug.c
  record: docs/evidence/twin/TWIN-44/runs/author_06/result.md
rollback:
  steps:
  - git -C mcu-p3 checkout -- motion-controller-mcu/project/src/minimc_proto.c motion-controller-mcu/project/inc/minimc_proto.h && rm -f mcu-p3/motion-controller-mcu/project/src/test_twin44_mc_debug.c
handoff:
  receiver_role: COORD
  receiver_session: ff2fb105-fd84-4ecb-b1e6-8f8eb00badc6
  transport: docs
  evidence_location: docs/evidence/twin/TWIN-44
  acknowledgement: received-author_06-f34a4b9d3ce03ec02824e1c54dd4dd3052386156
verification:
  commands:
  - id: build_and_test_mc_debug_and_921600
    cwd: mcu-p3/motion-controller-mcu
    command: gcc -std=c11 -O2 -Wall -Wextra -no-pie -fno-pie -DAT32F435VGT7 -DUSE_STDPERIPH_DRIVER -I project/inc -I project/delay -I project/marlin -I project/marlin/marlin_core -I project/marlin/marlin_module -I libraries/drivers/inc -I libraries/cmsis/cm4/core_support -I libraries/cmsis/cm4/device_support project/src/minimc_proto.c project/src/test_twin44_mc_debug.c -o /tmp/test_twin44 && /tmp/test_twin44 && rm -f /tmp/test_twin44
    expected: 容器/宿主gcc编译minimc_proto.c与test_twin44_mc_debug.c 0错误，全部正例（USART2 921600初始化、保持真实MiniMC命令集与未知命令NACK 0x04、含0x18调平网格在内的五类业务实时状态字段断言、TH级联响应严格关联校验、send成功发射STATE+TX ACK）与反例及恢复（2048B环形缓冲满丢包与排空恢复、>192B截断、CRC错误与恢复、非预期/不匹配seq或cmd的TH帧拦截且不清除挂起超时及后续合法响应恢复、TH级联超时与恢复、minimc_proto_send与forward_uart_send_raw失败抑制伪ACK/挂起状态并恢复）单测PASS
    availability: available
  positive_cases:
  - minimc_proto_init将USART2(PA2/PA3，AP↔MC业务链路)波特率重配置为AP_USART_BAUDRATE(921600U)，保持USART6(PA4/PA5，MC↔TH级联921600)与USART1(PA9/PA10，MC Debug 115200)不变
  - 在minimc_proto.c中自包含实现USART1 2048B静态环形缓冲+mc_debug_poll_drain非阻塞排空（保持main.c零改动），具备drop_count与trunc_count统计
  - 严格保持minimc_proto.c既有真实命令响应（0x01/0x03/0x14/0x16/0x18及TH级联转发，不伪造未实现命令的假ACK），通过运行态全局变量同步与非侵入式mc_debug_notify_*接口输出并断言[MC-DBG]五类业务字段（含0x18调平网格查询对应的dir=STATE/TX调平状态字段）
  - handle_th_frame严格校验挂起请求关联性（s_relay_pending、src==TH、dst==AP、IS_RESPONSE、hop_limit>1、seq匹配及请求/响应cmd对应），且所有minimc_proto_send与forward_uart_send_raw调用均严格检查返回值，仅在底层发送成功时输出STATE与TX status=ACK|NACK
  negative_cases:
  - 当Debug环形缓冲满时，mc_debug_write立即丢弃当前日志并递增drop_count，绝不阻塞USART2/USART6业务收发；调用mc_debug_poll_drain排空后再次写入新日志立即恢复正常输出
  - 收到未知/未实现命令码（返回NACK 0x04）、CRC错误帧、TH级联超时、无挂起请求的非预期TH帧或序列号/命令码不匹配的TH帧时，输出对应[MC-DBG] dir=ERR/NACK/TIMEOUT日志；非预期或不匹配TH帧绝不清除当前有效挂起请求的s_relay_pending超时状态且不向AP转发，随后到达的匹配TH响应帧（或后续正常查询与级联请求）立即恢复成功
  - 当minimc_proto_send或forward_uart_send_raw（s_forward_send_ok=false）底层发送超时/失败时，严禁输出伪阳性TX status=ACK或置位s_relay_pending，必须输出[MC-DBG] dir=ERR node=MC|TH status=TX_ERR err_code=0x06；当usart2_tx_busy或s_forward_send_ok恢复后再次发送立即恢复正常ACK与级联转发闭环
required_evidence_level: server-sandbox-and-independent-review
verification_environment: docker-qa-sandbox-and-isolated-codex
qa_review_policy: project-control/.agents/rules/codex_qa_review.md
updated: '2026-11-04T12:42:00+08:00'
---

# TWIN-44 MC固件USART2 921600升级与USART1非阻塞[MC-DBG]结构化日志输出

## 1. 任务目标与来源
- **ARCH 拆分依据**：[debug_reconciliation_and_921600_arch_breakdown_20261104.md](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/architecture/debug_reconciliation_and_921600_arch_breakdown_20261104.md) (`revision: 10`, SHA-256 `9e66c080771a98ed2e87043c369841dcea0140f0270ae1ebab0d811c613cf5b3`, ARCH Session `433026bf-a1ff-4863-8f3e-7a5f43b016ff`)
- **需求与批准绑定**：`FEAT-20261104-001`, `FEAT-20261104-002` / `CONFIRM-DEBUG-BAUD-20261104` (`rev 2`) / `APPR-20261104-001` (`rev 1`)

## 2. 验收标准 (`acceptance_criteria`)
1. 在 `minimc_proto_init()` 中将 `USART2` (`PA2`/`PA3` AP↔MC 业务口) 波特率重配为 `AP_USART_BAUDRATE` (`921600U`)；保持 `USART6` (`921600`) 与 `USART1` (`115200`) 波特率不变，且不触碰 `wk_usart.{c,h}` 与 `main.c`。
2. 在 `minimc_proto.c` 中自包含实现基于静态环形缓冲 `s_mc_dbg_ring[2048]` 的非阻塞写入 + `minimc_proto_poll()` 内 `mc_debug_poll_drain()` 非阻塞定额排空，并提供 `drop_count` 与 `trunc_count` 统计。
3. 在 `minimc_proto.c` 中实现 `MC_DEBUG_MODE_ENABLE` 控制下的 `[MC-DBG]` 结构化日志输出，完整覆盖 `dir=RX|TX|RELAY_TX|RELAY_RX|STATE|ERR` 与五类业务状态（温度、归零/运动、调平、进退丝/料槽、作业状态），周期性状态日志限频 $\le 2\text{ Hz}$。
4. 所有新增/修改 C 函数严格满足 $\le 50$ 行、$\le 4$ 个入参、零动态堆分配（无 `malloc`/`free`）门禁，容器 `gcc` 编译与 `test_twin44_mc_debug.c` 单元测试零错误。
