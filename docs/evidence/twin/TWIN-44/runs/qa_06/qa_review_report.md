```yaml
task_id: TWIN-44
task_revision: 1
candidate_commit: f34a4b9d3ce03ec02824e1c54dd4dd3052386156
role: QA
decision: APPROVED
summary: Pinned bundle hash and metadata match. The scoped diff and candidate source
  align with the contract, and the frozen server QA evidence records all seven test
  suites passing with exit code 0.
findings: []
accepted_scope: Host GCC unit-test audit of USART2 921600 reconfiguration; the USART1
  2048-byte non-blocking logger, truncation, full-buffer drop and recovery; honest
  MiniMC dispatch and NACK behavior; state notifications including 0x18 grid fields;
  TH relay response correlation, timeout, CRC and recovery; and send-failure suppression
  and recovery. Cross-compiler ELF builds and physical MCU USB/UART HIL are excluded
  by the contract and environment.
unexecuted: []
actual_session: 01a1a4f2-21d9-7183-921c-7a4f5d5a3d18
reviewer_role: QA
reviewer_roles:
- QA
reviewed_artifact_version: project-control=42b031efff970b01ee8cc8e5dd087387cdf9288f;
  soc-ap=427dd6d82caceebb7b4642e78f1dbfa96ff5fc84; mcu-p3=f34a4b9d3ce03ec02824e1c54dd4dd3052386156;
  test_harness=ccf1476a0b98cb55ca9ee7bd49d73ca5d4704414
server_qa:
  task_id: TWIN-44
  task_revision: 1
  source: server-pinned-commits
  fresh_checkout: true
  sandbox:
    kind: container
    container_id: 0e818f18692f
    id: TWIN-44_run_130428_20261104_050428
    image: qa-sandbox:20261029
    path: /tmp/qa_sandboxes/TWIN-44_run_130428_20261104_050428
    developer_mounts: []
    container_inspect:
      id: 0e818f18692f062af6e1b58df3b871df1997d515daa2d4fa716881a1214874b4
      image: qa-sandbox:20261029
      image_digest: sha256:acbab225932c3877fff37f4d9e5a21235e099182c198e4f4034064ea80cf544f
      created: '2026-11-04T05:04:50.671702919Z'
      state: exited
      mounts:
      - Type: bind
        Source: /tmp/qa_sandboxes/TWIN-44_run_130428_20261104_050428
        Destination: /workspace
        Mode: ro
        RW: false
        Propagation: rprivate
  server_lock:
    path: /tmp/qa_TWIN-44_sb4alei1/evidence/server_lock.json
    sha256: 862d65ef78bcfcb053302b6d2fdf7f44eaf2c5ea98b2e506c8c5b390c725da24
  checkout_log:
    path: /tmp/qa_TWIN-44_sb4alei1/evidence/checkout.log
    sha256: 9e69d8f42f8297ac52c33fe2614d09816016c4babb53e0498adf025d1df761da
  runtime_log:
    path: /tmp/qa_TWIN-44_sb4alei1/evidence/runtime.log
    sha256: ffdbb7b21eaad2839385b19ed4141b26174b774d3046b471d34f0c99ca436c75
  server_verdict:
    path: /tmp/qa_TWIN-44_sb4alei1/evidence/server_verdict.json
    sha256: 01a48b6aaedf918316c0f7f22ff7750d161b38be5bf5b70f0a1953e134362032
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
    duration: 0.36s
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
  timestamp: '2026-11-04T05:04:53.746051+00:00'
  path: /tmp/qa_TWIN-44_sb4alei1/evidence/server_qa.json
  sha256: 375efc5823373c5d9eb0bb66fbaa5676c077a7a66e59adff1626083de403f7bf
platform: codex
model: gpt-6-luna
session_evidence:
  path: /tmp/qa_TWIN-44_sb4alei1/reviews/74253d9c81224d95ba34ecd30fcf20e8/codex.jsonl
  sha256: 47611e60c5abe46f8743235dd825fbf18f44520487c16cd2eba1cc207cfe8c89
reviewed_artifacts:
- path: /tmp/qa_TWIN-44_sb4alei1/request.json
  sha256: 5ed950fab756bd78562fa24c33f20f63e446121b88d5c9aacaf9a5472fb7b0da
- path: /tmp/qa_TWIN-44_sb4alei1/diffs/project-control.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_TWIN-44_sb4alei1/diffs/soc-ap.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_TWIN-44_sb4alei1/diffs/mcu-p3.patch
  sha256: 7ff36b9ae1c3fc1ad49de5bce57d2519bb56ac328e9914719215d005815a8ddf
- path: /tmp/qa_TWIN-44_sb4alei1/diffs/test_harness.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_sandboxes/TWIN-44_run_130428_20261104_050428/mcu-p3/motion-controller-mcu/project/src/minimc_proto.c
  sha256: f64c223aa97e9b5efe1c7a5b428a0ea7da6da5bb44d8891870e6c75a028305c8
- path: /tmp/qa_sandboxes/TWIN-44_run_130428_20261104_050428/mcu-p3/motion-controller-mcu/project/inc/minimc_proto.h
  sha256: 7986230ecaa81e7bfc4d255bbfa9573968ac8bb0f5a55decd86b041320e45d5c
- path: /tmp/qa_sandboxes/TWIN-44_run_130428_20261104_050428/mcu-p3/motion-controller-mcu/project/src/test_twin44_mc_debug.c
  sha256: b8e5d609fbe95d5544089a2f3cef2a1edecda69abccaa126b89a68188ca2a834
verification_scope: Host GCC unit-test audit of USART2 921600 reconfiguration; the
  USART1 2048-byte non-blocking logger, truncation, full-buffer drop and recovery;
  honest MiniMC dispatch and NACK behavior; state notifications including 0x18 grid
  fields; TH relay response correlation, timeout, CRC and recovery; and send-failure
  suppression and recovery. Cross-compiler ELF builds and physical MCU USB/UART HIL
  are excluded by the contract and environment.
verification_environment: docker-sandbox-and-independent-codex-audit
```

Pinned bundle hash and metadata match. The scoped diff and candidate source align with the contract, and the frozen server QA evidence records all seven test suites passing with exit code 0.
