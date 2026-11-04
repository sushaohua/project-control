```yaml
task_id: TWIN-47
task_revision: 1
candidate_commit: 8d6b01059ed2ec6f405a5b6ec7859167f7045fec
role: QA
decision: REJECTED
summary: 已核对校验通过的证据索引、request、上一轮 QA 报告及其 SHA256，并审阅上一候选到本候选的定向差异。增量实现了 MC→TH 级联路径，但仍有已证实的关联同步缺陷。冻结的
  GCC 单测通过。
findings:
- 阻断：新增 trigger_mc_to_th_cascade 在 s_relay_pending 为真且 s_relay_from_mc_local 为真时仍允许发起级联，并覆盖待处理命令的序列号、命令码和计时信息。若前一
  MC→TH 请求尚未收到响应，后一请求会覆盖其关联状态，导致响应可能被错误匹配；这不满足接受条款要求的 TH 级联控制响应关联同步（0x10→0x15、0x19→0x19、0x1C→0x1C）。本轮新增测试仅验证单个请求的顺序闭环，没有覆盖并发待处理及恢复。
- 非阻断建议：宿主 GCC 输出 CMSIS 的整数到指针宽度告警；冻结证据显示命令退出码为 0，单测通过。
accepted_scope: 审阅 TWIN-47 revision 1 六个 MCU 候选文件及冻结 GCC 单测覆盖的 MiniMCProto 控制/查询、Marlin
  桥接、0x1C 封装、MC-DBG 输出、负例和恢复证据；复验重点为上一轮 MC→TH 级联阻断项的整改。交叉编译 ELF 构建和实体 MCU USB/UART
  HIL 明确排除，未将其视为已通过。
unexecuted: []
actual_session: 01a1a61a-c6a8-77d0-a1d5-21e66be35cb5
reviewer_role: QA
reviewer_roles:
- QA
reviewed_artifact_version: project-control=17e0887da07ceb3b017623b791b6a6999e837c79;
  soc-ap=c2c5a228c81488bca2178488a4e8a109b0472d72; mcu-p3=8d6b01059ed2ec6f405a5b6ec7859167f7045fec;
  test_harness=30c21f74e74179994eb475c38cc4afc2c1427a26
server_qa:
  task_id: TWIN-47
  task_revision: 1
  source: server-pinned-commits
  fresh_checkout: true
  sandbox:
    kind: container
    container_id: c64370f43e6b
    id: TWIN-47_run_182830_20261104_102830
    image: qa-sandbox:20261029
    path: /tmp/qa_sandboxes/TWIN-47_run_182830_20261104_102830
    developer_mounts: []
    container_inspect:
      id: c64370f43e6b1c8532291602d7bd670bc271b9cf8425cafb2a305c5f3ba16cf9
      image: qa-sandbox:20261029
      image_digest: sha256:acbab225932c3877fff37f4d9e5a21235e099182c198e4f4034064ea80cf544f
      created: '2026-11-04T10:28:50.612648573Z'
      state: exited
      mounts:
      - Type: bind
        Source: /tmp/qa_sandboxes/TWIN-47_run_182830_20261104_102830
        Destination: /workspace
        Mode: ro
        RW: false
        Propagation: rprivate
  server_lock:
    path: /tmp/qa_TWIN-47_ksdwr2ji/evidence/server_lock.json
    sha256: 3081143fb36bd7b0f575bcf208a3ffb2ed6deb0d69f98bf7c7629e3f88bd4aed
  checkout_log:
    path: /tmp/qa_TWIN-47_ksdwr2ji/evidence/checkout.log
    sha256: 3f50be09e37cd8de98316242e4058997bdb6346f1b25c7581fa3036af62e9474
  runtime_log:
    path: /tmp/qa_TWIN-47_ksdwr2ji/evidence/runtime.log
    sha256: 5bd4880c436730ef83752ae53d4b1349b1a968375d3bf3fbf0ecd4d8f367daee
  server_verdict:
    path: /tmp/qa_TWIN-47_ksdwr2ji/evidence/server_verdict.json
    sha256: 3c88993a59e3a9e9429ad49a7cdcbed0b1564f607896cd471501262ae55bc872
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
  timestamp: '2026-11-04T10:28:53.739263+00:00'
  path: /tmp/qa_TWIN-47_ksdwr2ji/evidence/server_qa.json
  sha256: 7abffc075897bb6e37e9e7b0ce07654561e8954d25c8faeb661b8ba9984e44c9
platform: codex
model: gpt-6-luna
session_evidence:
  path: /tmp/qa_TWIN-47_ksdwr2ji/reviews/9f31df05eccd463cba56c31bf4e534f0/codex.jsonl
  sha256: 1751d35c1a014362c6c0a17b29321db8b59a517a4c1e50e8e52f550cccf3f244
reviewed_artifacts:
- path: /tmp/qa_TWIN-47_ksdwr2ji/request.json
  sha256: 21c60bc11b54f40fa666623ac4d7087d614c8aefeba598ea45c1109623f45579
- path: /tmp/qa_TWIN-47_ksdwr2ji/diffs/project-control.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_TWIN-47_ksdwr2ji/diffs/soc-ap.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_TWIN-47_ksdwr2ji/diffs/mcu-p3.patch
  sha256: b83ae6fa06426c3b71bd3c9d1a6d2f3efa43e6bd5fc9dbdb6c50ae2794abc3e5
- path: /tmp/qa_TWIN-47_ksdwr2ji/diffs/test_harness.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_sandboxes/TWIN-47_run_182830_20261104_102830/mcu-p3/motion-controller-mcu/project/inc/minimc_proto.h
  sha256: 8bb15b3bc3957ccc88f9d9388bc8567e7b5da6e0ea31d8ed1d6c4efc1c2e9b3d
- path: /tmp/qa_sandboxes/TWIN-47_run_182830_20261104_102830/mcu-p3/motion-controller-mcu/project/src/minimc_proto.c
  sha256: e92eaf06b61ab18a712606f91fed6f8b398037f77b3f75e363c7b9e10078d943
- path: /tmp/qa_sandboxes/TWIN-47_run_182830_20261104_102830/mcu-p3/motion-controller-mcu/project/src/wk_usart.c
  sha256: 7ff0695de92c0d6094c49fda2ba910aed0b7f1e37d178cefa334a9636ced7aec
- path: /tmp/qa_sandboxes/TWIN-47_run_182830_20261104_102830/mcu-p3/motion-controller-mcu/project/marlin/marlin_core/Marlin_main.c
  sha256: 80719c3135211a8b8d85c38e0a4b96197f2b1cacb469542fff010781ba2f0c47
- path: /tmp/qa_sandboxes/TWIN-47_run_182830_20261104_102830/mcu-p3/motion-controller-mcu/project/marlin/marlin_lcd/memu_gui.c
  sha256: b7342e786c03e43f3f191a36cb5d59313400c16226ede3c849289a5b2838ffab
- path: /tmp/qa_sandboxes/TWIN-47_run_182830_20261104_102830/mcu-p3/motion-controller-mcu/project/src/test_twin44_mc_debug.c
  sha256: 7d01ac21c70ca6a0b32f210ea06e07ae2393689396d109e6739e34f0494bbaed
verification_scope: 审阅 TWIN-47 revision 1 六个 MCU 候选文件及冻结 GCC 单测覆盖的 MiniMCProto 控制/查询、Marlin
  桥接、0x1C 封装、MC-DBG 输出、负例和恢复证据；复验重点为上一轮 MC→TH 级联阻断项的整改。交叉编译 ELF 构建和实体 MCU USB/UART
  HIL 明确排除，未将其视为已通过。
verification_environment: docker-sandbox-and-independent-codex-audit
```

已核对校验通过的证据索引、request、上一轮 QA 报告及其 SHA256，并审阅上一候选到本候选的定向差异。增量实现了 MC→TH 级联路径，但仍有已证实的关联同步缺陷。冻结的 GCC 单测通过。
