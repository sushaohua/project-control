```yaml
task_id: TWIN-44
task_revision: 1
candidate_commit: 04a2e8d161e1a1a18efc0d41d0dad91d51d065e9
role: QA
decision: REJECTED
summary: The pinned bundle hash matches, and the frozen server evidence ties a passing
  seven-suite GCC run to the candidate commit. The audited diff stays within the allowed
  MCU files. However, required negative-path and business-state logging coverage is
  incomplete.
findings:
- The contract calls for failure handling when either minimc_proto_send or forward_uart_send_raw
  fails, including recovery. The test stub has s_forward_send_ok, but no test sets
  it false or verifies the relay failure log, pending-state behavior, and recovery.
  The passing test therefore does not establish this required path.
- The test exercises a level-grid query but asserts only the response command and
  frame size. It does not assert the corresponding [MC-DBG] level/grid state fields,
  leaving that business-state logging path unverified.
accepted_scope: C unit-test verification in the Docker QA sandbox of USART2 921600
  reconfiguration, USART1 2048-byte non-blocking logging, honest MiniMC V2 dispatch
  and NACK handling, runtime-state logging, TH cascade response correlation, send-failure
  handling, and post-error recovery.
unexecuted:
- No hardware-in-the-loop verification of actual USART baud rates, pins, non-blocking
  behavior, or MC↔TH cascade operation.
- No embedded-target firmware build is present in the frozen evidence; the recorded
  command is a host GCC unit-test build.
actual_session: 01a1a4d8-3b88-7113-ab17-6f40c3ce71a3
reviewer_role: QA
reviewer_roles:
- QA
reviewed_artifact_version: project-control=42b031efff970b01ee8cc8e5dd087387cdf9288f;
  soc-ap=427dd6d82caceebb7b4642e78f1dbfa96ff5fc84; mcu-p3=04a2e8d161e1a1a18efc0d41d0dad91d51d065e9;
  test_harness=ccf1476a0b98cb55ca9ee7bd49d73ca5d4704414
server_qa:
  task_id: TWIN-44
  task_revision: 1
  source: server-pinned-commits
  fresh_checkout: true
  sandbox:
    kind: container
    container_id: 7a92aa5da2d4
    id: TWIN-44_run_123611_20261104_043611
    image: qa-sandbox:20261029
    path: /tmp/qa_sandboxes/TWIN-44_run_123611_20261104_043611
    developer_mounts: []
    container_inspect:
      id: 7a92aa5da2d4b231b6bbaa0cdfeff719bd04d4edaecc2fba3701bc125f6e296d
      image: qa-sandbox:20261029
      image_digest: sha256:acbab225932c3877fff37f4d9e5a21235e099182c198e4f4034064ea80cf544f
      created: '2026-11-04T04:36:33.18976326Z'
      state: exited
      mounts:
      - Type: bind
        Source: /tmp/qa_sandboxes/TWIN-44_run_123611_20261104_043611
        Destination: /workspace
        Mode: ro
        RW: false
        Propagation: rprivate
  server_lock:
    path: /tmp/qa_TWIN-44_wmxiv09u/evidence/server_lock.json
    sha256: 17154ad8b24a974b0a255218a2e68f98c024f886cb7fc38e95f7e3fa5beaa5ea
  checkout_log:
    path: /tmp/qa_TWIN-44_wmxiv09u/evidence/checkout.log
    sha256: fd9f9f5449ef80bc0cd648b3fa51e0d5c66dcb15ea37dd5fcd0b39db5f473920
  runtime_log:
    path: /tmp/qa_TWIN-44_wmxiv09u/evidence/runtime.log
    sha256: 675441f48fdacc037575c2e5f7372aa1fc7f817f607dca74180efde576e1689e
  server_verdict:
    path: /tmp/qa_TWIN-44_wmxiv09u/evidence/server_verdict.json
    sha256: 7716c2ad197f3fe11dfee78d99d7d1f7d288cbfbdae1a715578a59d17f6f22e5
  tool_versions:
    git: git version 2.25.1
    python: Python 3.8.10
  build_results: []
  test_results:
  - command: gcc -std=c11 -O2 -Wall -Wextra -no-pie -fno-pie -DAT32F435VGT7 -DUSE_STDPERIPH_DRIVER
      -I project/inc -I project/delay -I project/marlin -I project/marlin/marlin_core
      -I project/marlin/marlin_module -I libraries/drivers/inc -I libraries/cmsis/cm4/core_support
      -I libraries/cmsis/cm4/device_support project/src/minimc_proto.c project/src/test_twin44_mc_debug.c
      -o /tmp/test_twin44 && /tmp/test_twin44 && rm -f /tmp/test_twin44
    exit_code: '0'
    subpath: mcu-p3/motion-controller-mcu
    duration: 0.35s
    output: "========================================================================\n\
      TWIN-44 MC USART2 921600 & USART1 Non-Blocking [MC-DBG] Verification\n========================================================================\n\
      [RUN ] test_usart2_921600_reconfig\n[PASS] test_usart2_921600_reconfig\n[RUN\
      \ ] test_ring_buffer_trunc_drop_and_recovery\n[PASS] test_ring_buffer_trunc_drop_and_recovery\n\
      [RUN ] test_honest_minimc_v2_queries_and_nack\n[PASS] test_honest_minimc_v2_queries_and_nack\n\
      [RUN ] test_non_intrusive_notify_and_fault_sync\n[PASS] test_non_intrusive_notify_and_fault_sync\n\
      [RUN ] test_tx_fail_suppresses_ack_and_recovers\n[PASS] test_tx_fail_suppresses_ack_and_recovers\n\
      [RUN ] test_relay_timeout_crc_err_and_recovery\n[PASS] test_relay_timeout_crc_err_and_recovery\n\
      [RUN ] test_th_relay_correlation_and_nack\n[PASS] test_th_relay_correlation_and_nack\n\
      ------------------------------------------------------------------------\nAll\
      \ 7 TWIN-44 test suites (including TH relay correlation & recovery) PASSED!\n\
      ========================================================================\n\n\
      In file included from libraries/cmsis/cm4/device_support/at32f435_437.h:428,\n\
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
  timestamp: '2026-11-04T04:36:36.191774+00:00'
  path: /tmp/qa_TWIN-44_wmxiv09u/evidence/server_qa.json
  sha256: 6c3e13868cc0b52cf3db0a43f9b7a34338c2358686cef08c19c2dff8eb946c12
platform: codex
model: gpt-6-luna
session_evidence:
  path: /tmp/qa_TWIN-44_wmxiv09u/reviews/e92d0d353f4c4c6eb8d257b5b4037165/codex.jsonl
  sha256: 2400c82075b0fdef123bc35d743133e4a87dcc8e279dbab19e189dc937c40071
reviewed_artifacts:
- path: /tmp/qa_TWIN-44_wmxiv09u/request.json
  sha256: 76d0b496b66cdb0225ade51091e546644c857067e99102ac2aa4b8a82c782a75
- path: /tmp/qa_TWIN-44_wmxiv09u/diffs/project-control.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_TWIN-44_wmxiv09u/diffs/soc-ap.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_TWIN-44_wmxiv09u/diffs/mcu-p3.patch
  sha256: f3d465e5e450123fbdd24d3df666058d2ca985a4c8e408443c5e23fa3fa7ef62
- path: /tmp/qa_TWIN-44_wmxiv09u/diffs/test_harness.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_sandboxes/TWIN-44_run_123611_20261104_043611/mcu-p3/motion-controller-mcu/project/src/minimc_proto.c
  sha256: f64c223aa97e9b5efe1c7a5b428a0ea7da6da5bb44d8891870e6c75a028305c8
- path: /tmp/qa_sandboxes/TWIN-44_run_123611_20261104_043611/mcu-p3/motion-controller-mcu/project/inc/minimc_proto.h
  sha256: 7986230ecaa81e7bfc4d255bbfa9573968ac8bb0f5a55decd86b041320e45d5c
- path: /tmp/qa_sandboxes/TWIN-44_run_123611_20261104_043611/mcu-p3/motion-controller-mcu/project/src/test_twin44_mc_debug.c
  sha256: cd9b21da9631498aaad2182b333c3b51e5215dbe3e3cbd6e8bd8667d433ba0b6
verification_scope: C unit-test verification in the Docker QA sandbox of USART2 921600
  reconfiguration, USART1 2048-byte non-blocking logging, honest MiniMC V2 dispatch
  and NACK handling, runtime-state logging, TH cascade response correlation, send-failure
  handling, and post-error recovery.
verification_environment: docker-sandbox-and-independent-codex-audit
```

The pinned bundle hash matches, and the frozen server evidence ties a passing seven-suite GCC run to the candidate commit. The audited diff stays within the allowed MCU files. However, required negative-path and business-state logging coverage is incomplete.
