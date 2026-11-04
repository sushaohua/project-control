```yaml
task_id: TWIN-47
task_revision: 1
candidate_commit: 0e70203b55a97cf73084c65b60f6ac48c28b10ff
role: QA
decision: REJECTED
summary: 已校验 bundle、request、服务器判定、runtime log、MCU 定向补丁及六个候选文件的 SHA256。冻结的 GCC 单测全部通过，但源码未满足接受范围内的
  TH 级联控制要求。
findings:
- 阻断：接受范围要求 0x19 本地槽位选择与 TH 级联同步。minimc_proto.c 的 handle_mc_filament 只更新 MC 的 active_extruder
  并发送本地响应，没有向 TH 转发；测试覆盖的是 TH 发起请求后经 MC 中继的反向路径，不能证明 MC→TH 级联。
- 阻断：接受范围要求 TH 级联控制响应的关联同步（0x10→0x15、0x19→0x19、0x1C→0x1C）。0x10 的 handle_mc_set_temp
  只调用 MC 本地加热器并发本地响应，0x1C 的 handle_mc_gcode_exec 仅入 Marlin 队列并发本地 ACK；队列标记还会使 forward_uart_send_line
  跳过该命令的 TH 转发。因此这些 MC 收到的控制命令没有实现所要求的 MC→TH 闭环。现有单测通过不足以覆盖该接受条款。
- 非阻断建议：主机 GCC 编译产生 CMSIS 指针宽度告警；本轮接受标准要求零错误且单测通过，证据显示退出码为 0。
accepted_scope: 审阅 TWIN-47 revision 1 的六个 MCU 候选文件，以及服务器 GCC 单测所覆盖的 MiniMCProto 控制/查询、Marlin
  桥接、0x1C 帧封装、MC-DBG 输出、负例和恢复证据。交叉编译 ELF 构建与实体 MCU USB/UART HIL 明确排除；未将其视为已通过。
unexecuted: []
actual_session: 01a1a60b-ce09-77d2-8066-c6b7c95a7512
reviewer_role: QA
reviewer_roles:
- QA
reviewed_artifact_version: project-control=17e0887da07ceb3b017623b791b6a6999e837c79;
  soc-ap=c2c5a228c81488bca2178488a4e8a109b0472d72; mcu-p3=0e70203b55a97cf73084c65b60f6ac48c28b10ff;
  test_harness=30c21f74e74179994eb475c38cc4afc2c1427a26
server_qa:
  task_id: TWIN-47
  task_revision: 1
  source: server-pinned-commits
  fresh_checkout: true
  sandbox:
    kind: container
    container_id: dfbad33b60aa
    id: TWIN-47_run_181209_20261104_101209
    image: qa-sandbox:20261029
    path: /tmp/qa_sandboxes/TWIN-47_run_181209_20261104_101209
    developer_mounts: []
    container_inspect:
      id: dfbad33b60aa43f637acee715e8d8bec1591236bf3230d969e11189962662e5f
      image: qa-sandbox:20261029
      image_digest: sha256:acbab225932c3877fff37f4d9e5a21235e099182c198e4f4034064ea80cf544f
      created: '2026-11-04T10:12:29.245742711Z'
      state: exited
      mounts:
      - Type: bind
        Source: /tmp/qa_sandboxes/TWIN-47_run_181209_20261104_101209
        Destination: /workspace
        Mode: ro
        RW: false
        Propagation: rprivate
  server_lock:
    path: /tmp/qa_TWIN-47_co6ypesz/evidence/server_lock.json
    sha256: 5f87eb221f25257d8581abbdf69286199037faeadd2e0ae9e7b4edea5c34cb1e
  checkout_log:
    path: /tmp/qa_TWIN-47_co6ypesz/evidence/checkout.log
    sha256: 8b6c8665bd2580efcb95df661545561bd72a619d1ffa7fb7821546e45a694d65
  runtime_log:
    path: /tmp/qa_TWIN-47_co6ypesz/evidence/runtime.log
    sha256: 73fb93017e548bc7c65ddfd7b4d916504b32d6e256ccc2a6945b652568cbe6f0
  server_verdict:
    path: /tmp/qa_TWIN-47_co6ypesz/evidence/server_verdict.json
    sha256: f4aa6fb783282a4a90cf186e0ecd489c3ea920c68741304f734b13a003ae0ac9
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
    duration: 0.48s
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
  timestamp: '2026-11-04T10:12:33.139256+00:00'
  path: /tmp/qa_TWIN-47_co6ypesz/evidence/server_qa.json
  sha256: 6055e3dea58500210c4fe2a49e85db806d7e7c6afed41e089ccce138b222eef6
platform: codex
model: gpt-6-luna
session_evidence:
  path: /tmp/qa_TWIN-47_co6ypesz/reviews/70b4d29364944990b03b351e621a4e0f/codex.jsonl
  sha256: dcc1394a8468965a7f14b7a86328f9267641f7a83e8e029cf422a3b745531c69
reviewed_artifacts:
- path: /tmp/qa_TWIN-47_co6ypesz/request.json
  sha256: 56d0572370a2641ca7bf16e90f530bea45b779318117dd45f152fbf45665070b
- path: /tmp/qa_TWIN-47_co6ypesz/diffs/project-control.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_TWIN-47_co6ypesz/diffs/soc-ap.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_TWIN-47_co6ypesz/diffs/mcu-p3.patch
  sha256: 64786b640645667f0ff67ffd2f3b8cc47d1d802c7e424b7e37488e170dcc27c0
- path: /tmp/qa_TWIN-47_co6ypesz/diffs/test_harness.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_sandboxes/TWIN-47_run_181209_20261104_101209/mcu-p3/motion-controller-mcu/project/inc/minimc_proto.h
  sha256: 8bb15b3bc3957ccc88f9d9388bc8567e7b5da6e0ea31d8ed1d6c4efc1c2e9b3d
- path: /tmp/qa_sandboxes/TWIN-47_run_181209_20261104_101209/mcu-p3/motion-controller-mcu/project/src/minimc_proto.c
  sha256: c60c658314d0b3a178e9da1fbc0bab2b58f50c1245b8f6af249530ad755a4561
- path: /tmp/qa_sandboxes/TWIN-47_run_181209_20261104_101209/mcu-p3/motion-controller-mcu/project/src/wk_usart.c
  sha256: 351f7acb861e7d3112afc665cdf2d8adda6eae59c779a289a65523a364212dd5
- path: /tmp/qa_sandboxes/TWIN-47_run_181209_20261104_101209/mcu-p3/motion-controller-mcu/project/marlin/marlin_core/Marlin_main.c
  sha256: 1b621c0b9a6c4ef5febd9836167d78e6ec8f8efd0cff0190a33ea75f4d722d64
- path: /tmp/qa_sandboxes/TWIN-47_run_181209_20261104_101209/mcu-p3/motion-controller-mcu/project/marlin/marlin_lcd/memu_gui.c
  sha256: b7342e786c03e43f3f191a36cb5d59313400c16226ede3c849289a5b2838ffab
- path: /tmp/qa_sandboxes/TWIN-47_run_181209_20261104_101209/mcu-p3/motion-controller-mcu/project/src/test_twin44_mc_debug.c
  sha256: e6238ec8dfb47f7ce17b5330bb1f1d6979f73df3703d1d2064a74a87431f466c
verification_scope: 审阅 TWIN-47 revision 1 的六个 MCU 候选文件，以及服务器 GCC 单测所覆盖的 MiniMCProto
  控制/查询、Marlin 桥接、0x1C 帧封装、MC-DBG 输出、负例和恢复证据。交叉编译 ELF 构建与实体 MCU USB/UART HIL 明确排除；未将其视为已通过。
verification_environment: docker-sandbox-and-independent-codex-audit
```

已校验 bundle、request、服务器判定、runtime log、MCU 定向补丁及六个候选文件的 SHA256。冻结的 GCC 单测全部通过，但源码未满足接受范围内的 TH 级联控制要求。
