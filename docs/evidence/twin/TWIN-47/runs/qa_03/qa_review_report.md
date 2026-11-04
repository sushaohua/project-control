```yaml
task_id: TWIN-47
task_revision: 1
candidate_commit: d86041814689b2f353d6fe0b372d31689b826a98
role: QA
decision: APPROVED
summary: 复验通过。已核对上一轮报告及其 SHA256，并聚焦审阅上一候选到本候选的增量差异；本轮修复阻止新的级联请求覆盖在途关联状态，冻结的宿主 GCC
  单测证据通过。
findings:
- 已确认新增保护覆盖 MC 本地级联与 AP→TH 转发：已有请求 pending 时拒绝后续转发；接收响应仍要求 pending、16 位序列号匹配且响应命令与原请求匹配。新增用例检查第二请求被拒、伪造序列号响应被拒、原响应完成后后续请求恢复；冻结运行日志显示测试命令退出码为
  0，9 个测试套件通过。
- 非阻断建议：冻结 GCC 日志仍有 CMSIS 整数到指针宽度告警；命令退出码为 0，告警不影响本轮接受范围判定。
accepted_scope: TWIN-47 revision 1：接受范围内六个 MCU 文件及冻结 GCC 单测所覆盖的 MiniMCProto 控制/查询、Marlin
  桥接、0x1C 封装、MC-DBG、负例和恢复证据。本轮重点复验上一候选 8d6b01059ed2ec6f405a5b6ec7859167f7045fec 的
  MC→TH 在途关联覆盖问题；本候选增量差异已检查，并核对相关响应校验、并发拒绝、原响应完成及恢复测试。交叉编译 ELF 构建和实体 MCU USB/UART
  HIL 属明确排除项，未视为已通过。
unexecuted: []
actual_session: 01a1a61f-f579-7cd0-a857-cd21096242ac
reviewer_role: QA
reviewer_roles:
- QA
reviewed_artifact_version: project-control=17e0887da07ceb3b017623b791b6a6999e837c79;
  soc-ap=c2c5a228c81488bca2178488a4e8a109b0472d72; mcu-p3=d86041814689b2f353d6fe0b372d31689b826a98;
  test_harness=30c21f74e74179994eb475c38cc4afc2c1427a26
server_qa:
  task_id: TWIN-47
  task_revision: 1
  source: server-pinned-commits
  fresh_checkout: true
  sandbox:
    kind: container
    container_id: 3fee157e3c3e
    id: TWIN-47_run_183322_20261104_103322
    image: qa-sandbox:20261029
    path: /tmp/qa_sandboxes/TWIN-47_run_183322_20261104_103322
    developer_mounts: []
    container_inspect:
      id: 3fee157e3c3e026500204afd498829716f1746f0d81b09b908751ad4c01de1c0
      image: qa-sandbox:20261029
      image_digest: sha256:acbab225932c3877fff37f4d9e5a21235e099182c198e4f4034064ea80cf544f
      created: '2026-11-04T10:34:31.082375411Z'
      state: exited
      mounts:
      - Type: bind
        Source: /tmp/qa_sandboxes/TWIN-47_run_183322_20261104_103322
        Destination: /workspace
        Mode: ro
        RW: false
        Propagation: rprivate
  server_lock:
    path: /tmp/qa_TWIN-47_pzjnfc3a/evidence/server_lock.json
    sha256: 00b25f163a8e012bcefa6cfb1169197acf8f75a6b1fe1df309e10d59dfe90803
  checkout_log:
    path: /tmp/qa_TWIN-47_pzjnfc3a/evidence/checkout.log
    sha256: 29a7caac64aa2e70416acfd69f6024e1b376a02e98d085c81bf8c6db2e133e76
  runtime_log:
    path: /tmp/qa_TWIN-47_pzjnfc3a/evidence/runtime.log
    sha256: 9a112e7b535cf81cb107250e92b337eefd0ce73e68c358866fa8da3112f8e75e
  server_verdict:
    path: /tmp/qa_TWIN-47_pzjnfc3a/evidence/server_verdict.json
    sha256: 66f1d30ffa681892da98c4b8bf9fe66828eacea57cffa74914c78d1b6000f148
  tool_versions:
    git: git version 2.25.1
    python: Python 3.8.10
  build_results: []
  test_results:
  - command: gcc -std=c11 -O2 -Wall -Wextra -no-pie -fno-pie -DAT32F435VGT7 -DUSE_STDPERIPH_DRIVER
      -I project/inc -I project/delay -I project/marlin -I project/marlin/marlin_core
      -I project/marlin/marlin_module -I libraries/drivers/inc -I libraries/cmsis/cm4/core_support
      -I libraries/cmsis/cm4/device_support project/src/minimc_proto.c project/src/test_twin44_mc_debug.c
      -o /tmp/test_twin47 && /tmp/test_twin47 && rm -f /tmp/test_twin47
    exit_code: '0'
    subpath: mcu-p3/motion-controller-mcu
    duration: 0.45s
    output: "========================================================================\n\
      TWIN-44 & TWIN-47 MC USART2 921600, Control Cmds & 0x1C Verification\n========================================================================\n\
      [RUN ] test_usart2_921600_reconfig\n[PASS] test_usart2_921600_reconfig\n[RUN\
      \ ] test_ring_buffer_trunc_drop_and_recovery\n[PASS] test_ring_buffer_trunc_drop_and_recovery\n\
      [RUN ] test_honest_minimc_v2_queries_and_nack\n[PASS] test_honest_minimc_v2_queries_and_nack\n\
      [RUN ] test_non_intrusive_notify_and_fault_sync\n[PASS] test_non_intrusive_notify_and_fault_sync\n\
      [RUN ] test_tx_fail_suppresses_ack_and_recovers\n[PASS] test_tx_fail_suppresses_ack_and_recovers\n\
      [RUN ] test_relay_timeout_crc_err_and_recovery\n[PASS] test_relay_timeout_crc_err_and_recovery\n\
      [RUN ] test_th_relay_correlation_and_nack\n[PASS] test_th_relay_correlation_and_nack\n\
      [RUN ] test_twin47_temp_home_move_stop\n[PASS] test_twin47_temp_home_move_stop\n\
      [RUN ] test_twin47_job_filament_level_gcode\n[PASS] test_twin47_job_filament_level_gcode\n\
      ------------------------------------------------------------------------\nAll\
      \ 9 TWIN-44/TWIN-47 test suites PASSED!\n========================================================================\n\
      \nIn file included from libraries/cmsis/cm4/device_support/at32f435_437.h:428,\n\
      \                 from project/inc/at32f435_437_wk_config.h:37,\n          \
      \       from project/inc/wk_dma.h:36,\n                 from project/src/minimc_proto.c:2:\n\
      libraries/cmsis/cm4/core_support/core_cm4.h: In function '__NVIC_SetVector':\n\
      libraries/cmsis/cm4/core_support/core_cm4.h:1913:23: warning: cast to pointer\
      \ from integer of different size [-Wint-to-pointer-cast]\n 1913 |   uint32_t\
      \ *vectors = (uint32_t *)SCB->VTOR;\n      |                       ^\nlibraries/cmsis/cm4/core_support/core_cm4.h:\
      \ In function '__NVIC_GetVector':\nlibraries/cmsis/cm4/core_support/core_cm4.h:1929:23:\
      \ warning: cast to pointer from integer of different size [-Wint-to-pointer-cast]\n\
      \ 1929 |   uint32_t *vectors = (uint32_t *)SCB->VTOR;\n      |             \
      \          ^\nIn file included from libraries/cmsis/cm4/device_support/at32f435_437.h:428,\n\
      \                 from project/marlin/configure.h:4,\n                 from\
      \ project/marlin/marlin_core/planner.h:28,\n                 from project/src/test_twin44_mc_debug.c:17:\n\
      libraries/cmsis/cm4/core_support/core_cm4.h: In function '__NVIC_SetVector':\n\
      libraries/cmsis/cm4/core_support/core_cm4.h:1913:23: warning: cast to pointer\
      \ from integer of different size [-Wint-to-pointer-cast]\n 1913 |   uint32_t\
      \ *vectors = (uint32_t *)SCB->VTOR;\n      |                       ^\nlibraries/cmsis/cm4/core_support/core_cm4.h:\
      \ In function '__NVIC_GetVector':\nlibraries/cmsis/cm4/core_support/core_cm4.h:1929:23:\
      \ warning: cast to pointer from integer of different size [-Wint-to-pointer-cast]\n\
      \ 1929 |   uint32_t *vectors = (uint32_t *)SCB->VTOR;\n      |             \
      \          ^"
  passed: true
  timestamp: '2026-11-04T10:34:34.145954+00:00'
  path: /tmp/qa_TWIN-47_pzjnfc3a/evidence/server_qa.json
  sha256: dc7dca29748480022c52c1d5cccbd0d847eb40daa38fd207b8c8ec0efe8460bc
platform: codex
model: gpt-6-luna
session_evidence:
  path: /tmp/qa_TWIN-47_pzjnfc3a/reviews/f279dce7f876426f80e2db5b39eed3e0/codex.jsonl
  sha256: 6fcf1b57e375c55c57e4ae0a1ad1239e03fd4145b88dd7cd0e53159f9f3f77f6
reviewed_artifacts:
- path: /tmp/qa_TWIN-47_pzjnfc3a/request.json
  sha256: 3a0607509534308a8f7713c87613362eb27221914fd0791cdb1809f161070c82
- path: /tmp/qa_TWIN-47_pzjnfc3a/diffs/project-control.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_TWIN-47_pzjnfc3a/diffs/soc-ap.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_TWIN-47_pzjnfc3a/diffs/mcu-p3.patch
  sha256: 052d22120892c86bc51d6524adbf0cd48ea2d30749f7d95dbd34308192a0ec1e
- path: /tmp/qa_TWIN-47_pzjnfc3a/diffs/test_harness.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_sandboxes/TWIN-47_run_183322_20261104_103322/mcu-p3/motion-controller-mcu/project/inc/minimc_proto.h
  sha256: 8bb15b3bc3957ccc88f9d9388bc8567e7b5da6e0ea31d8ed1d6c4efc1c2e9b3d
- path: /tmp/qa_sandboxes/TWIN-47_run_183322_20261104_103322/mcu-p3/motion-controller-mcu/project/src/minimc_proto.c
  sha256: 090b626d16f08976b7f514b1c5be0e3636552fd2390e68dd0d531e84ffde5307
- path: /tmp/qa_sandboxes/TWIN-47_run_183322_20261104_103322/mcu-p3/motion-controller-mcu/project/src/wk_usart.c
  sha256: 7ff0695de92c0d6094c49fda2ba910aed0b7f1e37d178cefa334a9636ced7aec
- path: /tmp/qa_sandboxes/TWIN-47_run_183322_20261104_103322/mcu-p3/motion-controller-mcu/project/marlin/marlin_core/Marlin_main.c
  sha256: 80719c3135211a8b8d85c38e0a4b96197f2b1cacb469542fff010781ba2f0c47
- path: /tmp/qa_sandboxes/TWIN-47_run_183322_20261104_103322/mcu-p3/motion-controller-mcu/project/marlin/marlin_lcd/memu_gui.c
  sha256: b7342e786c03e43f3f191a36cb5d59313400c16226ede3c849289a5b2838ffab
- path: /tmp/qa_sandboxes/TWIN-47_run_183322_20261104_103322/mcu-p3/motion-controller-mcu/project/src/test_twin44_mc_debug.c
  sha256: 7dd2be9da4df36c191e2176a359be4740dba87fc1d6759eb17f5e2beb8913b37
verification_scope: TWIN-47 revision 1：接受范围内六个 MCU 文件及冻结 GCC 单测所覆盖的 MiniMCProto 控制/查询、Marlin
  桥接、0x1C 封装、MC-DBG、负例和恢复证据。本轮重点复验上一候选 8d6b01059ed2ec6f405a5b6ec7859167f7045fec 的
  MC→TH 在途关联覆盖问题；本候选增量差异已检查，并核对相关响应校验、并发拒绝、原响应完成及恢复测试。交叉编译 ELF 构建和实体 MCU USB/UART
  HIL 属明确排除项，未视为已通过。
verification_environment: docker-sandbox-and-independent-codex-audit
```

复验通过。已核对上一轮报告及其 SHA256，并聚焦审阅上一候选到本候选的增量差异；本轮修复阻止新的级联请求覆盖在途关联状态，冻结的宿主 GCC 单测证据通过。
