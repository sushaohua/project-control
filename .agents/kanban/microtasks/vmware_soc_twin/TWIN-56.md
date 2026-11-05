---
id: TWIN-56
title: TWIN-56 MC/TH串口调试日志[MC-DBG]/[TH-DBG] 16-bit seq截断修复与MC本地级联号段隔离
revision: 1
plan_revision: vmware-soc-twin-20261105
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
  run_id: author_01
qa_policy: streamlined-v1
reviewer:
  - QA
verifier: null
integrator: INTEGRATOR
requirement_id: REQ-20261105-001
demand_id: DEM-20261105-005
confirmation_id: CONFIRM-WEB-HMI-FULL-QA-BUILD-DEPLOY-20261105
approval_id: APPR-20261105-003
accepted_scope: "C unit-test verification in Docker QA sandbox (gcc) of MC (AT32F435) and TH (AT32F423) 16-bit sequence number logging in [MC-DBG] (minimc_proto.h/c) and [TH-DBG] (usart.c), MC local cascade initial sequence offset s_mc_th_seq = 0x0100U in minimc_proto_init(), and debug_reconciliation_probe.py --self-test compatibility. Cross-compiler ELF build and physical MCU USB/UART HIL are not applicable in qa-sandbox:20261029 (host arm-none-eabi-gcc build is verified in author_01 and physical HIL in TWIN-55): qa-sandbox:20261029 provides host GCC/Python only and no physical MCU hardware; all in-scope checks are executed in server_qa so unexecuted is empty when those checks pass."
review_assignments:
  reviewer_sessions:
    - role: QA
      platform: codex
      model: gpt-6-luna
      planned_session_alias: planned-qa-twin-56
      session: 01a1aa28-b5a7-70b1-901d-74be17e64077
      reviewer_session: 01a1aa28-b5a7-70b1-901d-74be17e64077
      commit_sha: 891a8bb252814c83992a49b01fbe11ba83b92a1f
      session_evidence:
        path: /home/sushaohua/workspace/ai_soc_project/project-control/docs/evidence/twin/TWIN-56/runs/qa_03/codex_events.jsonl
        sha256: cae4a4424acfe324a0af77f16e8acf019c44129881cec51912eb5f6d710e3050
      decision: APPROVED
      reviewed_task_revision: 1
      artifact_version: project-control=99cd83bb40b4ecf53e8f9dd996ad61ecb653f6f0; soc-ap=79932746d225bb115010c5545ef3f7499482e137; mcu-p3=891a8bb252814c83992a49b01fbe11ba83b92a1f; test_harness=d14ed04321c6d4f5ddb35a8801604a8af53b5b60
      report_path: /home/sushaohua/workspace/ai_soc_project/project-control/docs/evidence/twin/TWIN-56/runs/qa_03/qa_review_report.md
      evidence: docs/evidence/twin/TWIN-56/runs/qa_03/qa_review_report.md
      report_sha256: 3766b355264f0259f2c4bb665a4a714dc896bd692eaa45fda9ddb2bafce0b377
  verifier_session: null
  integrator_session: null
primary_work_package: TASK-002
related_work_packages:
  - TASK-007
  - TASK-010
depends_on:
  - TWIN-47
  - TWIN-48
dependency_conditions:
  - task: TWIN-47
    accepted_version: project-control=17e0887da07ceb3b017623b791b6a6999e837c79; soc-ap=c2c5a228c81488bca2178488a4e8a109b0472d72; mcu-p3=d86041814689b2f353d6fe0b372d31689b826a98; test_harness=30c21f74e74179994eb475c38cc4afc2c1427a26
    acceptance_evidence: docs/evidence/twin/TWIN-47/runs/qa_03/qa_review_report.md
    required: 继承TWIN-47 MC端控制命令结构与[MC-DBG]日志基线
  - task: TWIN-48
    accepted_version: project-control=17e0887da07ceb3b017623b791b6a6999e837c79; soc-ap=c2c5a228c81488bca2178488a4e8a109b0472d72; mcu-p3=016e1236af75f6f19282d6b000f4b1b68bd96cc3; test_harness=30c21f74e74179994eb475c38cc4afc2c1427a26
    acceptance_evidence: docs/evidence/twin/TWIN-48/runs/qa_01/qa_review_report.md
    required: 继承TWIN-48 TH端级联控制与[TH-DBG]日志基线
scope_status: mapped
allowed_repositories:
  - mcu-p3
  - project-control
write_scope:
  mcu-p3:
    - motion-controller-mcu/project/inc/minimc_proto.h
    - motion-controller-mcu/project/src/minimc_proto.c
    - motion-controller-mcu/project/src/test_twin44_mc_debug.c
    - color-engine-mcu/io_toggle/src/bsp/usart.c
    - color-engine-mcu/io_toggle/src/user/test_twin45_th_debug.c
  project-control:
    - docs/evidence/twin/TWIN-56/**
allowed_paths:
  - mcu-p3/motion-controller-mcu/project/inc/minimc_proto.h
  - mcu-p3/motion-controller-mcu/project/src/minimc_proto.c
  - mcu-p3/motion-controller-mcu/project/src/test_twin44_mc_debug.c
  - mcu-p3/color-engine-mcu/io_toggle/src/bsp/usart.c
  - mcu-p3/color-engine-mcu/io_toggle/src/user/test_twin45_th_debug.c
  - project-control/docs/evidence/twin/TWIN-56/**
forbidden_paths:
  - soc-ap/**
  - test_harness/**
  - boot/**
source_baseline:
  project-control: 99cd83bb40b4ecf53e8f9dd996ad61ecb653f6f0
  soc-ap: 79932746d225bb115010c5545ef3f7499482e137
  mcu-p3: 016e1236af75f6f19282d6b000f4b1b68bd96cc3
  test_harness: d14ed04321c6d4f5ddb35a8801604a8af53b5b60
base_commit: 016e1236af75f6f19282d6b000f4b1b68bd96cc3
branch: feat/soc-debug
candidate_commit: 891a8bb252814c83992a49b01fbe11ba83b92a1f
dispatch_binding:
  source_commit: 016e1236af75f6f19282d6b000f4b1b68bd96cc3
  workspace_diff_sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
  consumed_artifact_versions:
    arch_breakdown: 842d813e60688e081279b83e539a2aee8a10885817233db0e7c734b84fa1380a
protocol_input:
  path: project-control/docs/architecture/mcu_dbg_seq_u16_fix_arch_breakdown_20261105.md
  sha256: 842d813e60688e081279b83e539a2aee8a10885817233db0e7c734b84fa1380a
  revision: 1
icd_versions:
  - path: project-control/docs/architecture/mcu_dbg_seq_u16_fix_arch_breakdown_20261105.md
    version: 1
read_sources:
  - project-control/.agents/rules/repository_rule_sources.json
  - project-control/.agents/rules/repository_rule_boundaries.md
  - mcu-p3/.repo-rules/AGENTS.md
  - mcu-p3/.repo-rules/SOURCE.json
  - project-control/.agents/rules/c_cpp_coding_standard.md
  - project-control/.agents/rules/code_documentation_standard.md
  - project-control/docs/architecture/mcu_dbg_seq_u16_fix_arch_breakdown_20261105.md
worktree: mcu-p3
lease:
  owner: 7812a1f6-5006-4971-a954-802f855cf20a
  task_revision: 1
  lease_id: lease-twin-56-20261105-01
  expires_at: '2026-11-05T20:00:00+08:00'
resources:
  - resource: mcu-host-gcc-test-env
    location: mcu-p3
    exclusive: true
    pending: null
budget:
  planned_checkpoint_minutes: 30
  max_evidence_based_corrections: 2
  on_limit: 保存证据交COORD
checkpoint: 开工前绑定；C模块单测与交叉编译自检；独立沙箱与QA审查；收件
execution_contract: project-control/docs/planning/vmware_soc_twin_task_execution_20261029.md
readiness_pending: []
deliverables:
  artifacts:
    - mcu-p3/motion-controller-mcu/project/inc/minimc_proto.h
    - mcu-p3/motion-controller-mcu/project/src/minimc_proto.c
    - mcu-p3/motion-controller-mcu/project/src/test_twin44_mc_debug.c
    - mcu-p3/color-engine-mcu/io_toggle/src/bsp/usart.c
    - mcu-p3/color-engine-mcu/io_toggle/src/user/test_twin45_th_debug.c
  record: docs/evidence/twin/TWIN-56/runs/author_01/result.md
rollback:
  steps:
    - git -C mcu-p3 checkout -- motion-controller-mcu/ color-engine-mcu/io_toggle/
handoff:
  receiver_role: COORD
  receiver_session: ff2fb105-fd84-4ecb-b1e6-8f8eb00badc6
  transport: docs
  evidence_location: docs/evidence/twin/TWIN-56
  acknowledgement: accepted
verification:
  commands:
    - id: build_and_test_mc_and_th_u16_seq_debug
      cwd: mcu-p3
      command: 'gcc -std=c11 -O2 -Wall -Wextra -no-pie -fno-pie -DAT32F435VGT7 -DUSE_STDPERIPH_DRIVER -I motion-controller-mcu/project/inc -I motion-controller-mcu/project/delay -I motion-controller-mcu/project/marlin -I motion-controller-mcu/project/marlin/marlin_core -I motion-controller-mcu/project/marlin/marlin_module -I motion-controller-mcu/libraries/drivers/inc -I motion-controller-mcu/libraries/cmsis/cm4/core_support -I motion-controller-mcu/libraries/cmsis/cm4/device_support motion-controller-mcu/project/src/minimc_proto.c motion-controller-mcu/project/src/test_twin44_mc_debug.c -o /tmp/test_twin47 && /tmp/test_twin47 && rm -f /tmp/test_twin47 && gcc -std=c11 -O2 -Wall -Wextra -no-pie -fno-pie -DAT32F423CCT7 -DUSE_STDPERIPH_DRIVER -DAT_START_F423_V1 -I color-engine-mcu/io_toggle/inc -I color-engine-mcu/io_toggle/inc/temperature_control -I color-engine-mcu/io_toggle/at32f423_board -I color-engine-mcu/io_toggle/src -I color-engine-mcu/io_toggle/src/app -I color-engine-mcu/io_toggle/libraries/cmsis/cm4/core_support -I color-engine-mcu/io_toggle/libraries/cmsis/cm4/device_support -I color-engine-mcu/io_toggle/libraries/drivers/inc color-engine-mcu/io_toggle/src/bsp/usart.c color-engine-mcu/io_toggle/src/app/minimc_proto.c color-engine-mcu/io_toggle/src/user/test_twin45_th_debug.c -o /tmp/test_twin48 && /tmp/test_twin48 && rm -f /tmp/test_twin48 && python3 ../test_harness/hil/tools/debug_reconciliation_probe.py --self-test'
      expected: 容器/宿主gcc编译minimc_proto.c、test_twin44_mc_debug.c、usart.c、test_twin45_th_debug.c 0错误；验证MC本地minimc_proto_send_th_gcode首帧seq=257(0x0101U)及AP请求seq>255(如seq=301)在[MC-DBG]与[TH-DBG]中原样输出16-bit完整十进制数值无8-bit截断；全部正反例与debug_reconciliation_probe.py --self-test 100% PASS
      availability: available
  positive_cases:
    - MC minimc_proto.c与TH usart.c将[MC-DBG]/[TH-DBG]中的seq、ack_seq、last_seq、s_relay_seq升位为uint16_t，完整提取frame[8] | (frame[9] << 8U)，seq > 255原样输出无模256截断
    - minimc_proto_init()恢复s_mc_th_seq = 0x0100U，使MC本地发起的0x1C级联G-code帧从seq=257(0x0101U)起步，与AP序列号清晰区分
  negative_cases:
    - 收到高位16-bit seq(>255)的CRC错误帧或未知命令帧时，输出[MC-DBG]/[TH-DBG] ERR或NACK日志且其中的16-bit seq保持完整无截断，后续合法帧立即恢复
    - 调试环形缓冲满时非阻塞拒绝写入并累加丢包计数，排空后恢复正常16-bit seq输出
required_evidence_level: server-sandbox-and-independent-review
verification_environment: docker-qa-sandbox-and-isolated-codex
qa_review_policy: project-control/.agents/rules/codex_qa_review.md
updated: '2026-11-05T12:53:40+08:00'
---

# TWIN-56 MC/TH串口调试日志[MC-DBG]/[TH-DBG] 16-bit seq截断修复与MC本地级联号段隔离

## 1. 任务目标与来源
- **ARCH 方案依据**：[mcu_dbg_seq_u16_fix_arch_breakdown_20261105.md](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/architecture/mcu_dbg_seq_u16_fix_arch_breakdown_20261105.md) (`revision: 1`, SHA-256 `842d813e60688e081279b83e539a2aee8a10885817233db0e7c734b84fa1380a`)

## 2. 验收标准 (`acceptance_criteria`)
1. 将 MC `minimc_proto.{h,c}` 与 TH `usart.c` 中的调试日志 `seq` / `ack_seq` / `last_seq` / `s_relay_seq` 从 `uint8_t` 升位为 `uint16_t`，完整输出 16-bit 帧序列号（`0..65535`）。
2. 在 `minimc_proto_init()` 中恢复 `s_mc_th_seq = 0x0100U`，使 MC 本地发起的 `0x1C` 级联帧从 `257 (0x0101U)` 起步。
3. 通过宿主机/沙箱 GCC 单测（含 `seq=257` 与 `seq=301` 无截断断言）并完成宿主机 ARM 交叉编译。
