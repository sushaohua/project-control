```yaml
task_id: TWIN-44
task_revision: 1
candidate_commit: d2e469559081616f6312ecbabf8d6b69a7e92e3a
role: QA
decision: REJECTED
summary: The pinned bundle hash and candidate identity match the request. Frozen server
  evidence records a successful run of all six C test suites, but the implementation
  incorrectly treats any TH frame as the response to the outstanding relay request
  and reports it as ACK. This violates honest relay status handling.
findings:
- In minimc_proto.c handle_th_frame, every parsed TH frame clears s_relay_pending
  before checking destination, sequence, or command, and is logged as RELAY_RX status=ACK.
  A delayed or unrelated TH frame can therefore cancel a valid request's timeout and
  be reported as its successful response. The recovery test covers only a matching
  response and does not exercise mismatched or unsolicited TH frames. Correlate a
  response with the outstanding request before clearing it or emitting ACK; add negative
  and recovery coverage.
- 'The frozen server evidence is internally consistent: the bundle SHA256 matches,
  the candidate commit matches the requested commit, and the Docker run reports exit
  code 0 with all six suites passing. The test evidence does not cover the relay-correlation
  defect identified above.'
- No source_report was supplied; there was no report body or report SHA256 to audit.
accepted_scope: Bounded software and C unit-test verification in the Docker QA sandbox
  for USART2 921600 reconfiguration, the USART1 2048B non-blocking debug ring, honest
  MiniMC command handling, state logging, send failure handling, and recovery. Physical
  MCU flashing and hardware HIL are excluded.
unexecuted:
- Physical MCU board flashing and hardware HIL, excluded by the contract.
- Coverage of mismatched, delayed, or unsolicited TH responses against an outstanding
  relay request.
actual_session: 01a1a4c3-87c2-7c43-b651-9d349664e841
reviewer_role: QA
reviewer_roles:
- QA
reviewed_artifact_version: project-control=42b031efff970b01ee8cc8e5dd087387cdf9288f;
  soc-ap=427dd6d82caceebb7b4642e78f1dbfa96ff5fc84; mcu-p3=d2e469559081616f6312ecbabf8d6b69a7e92e3a;
  test_harness=ccf1476a0b98cb55ca9ee7bd49d73ca5d4704414
server_qa:
  task_id: TWIN-44
  task_revision: 1
  source: server-pinned-commits
  fresh_checkout: true
  sandbox:
    kind: container
    container_id: cbeedce3bfb8
    id: TWIN-44_run_121338_20261104_041338
    image: qa-sandbox:20261029
    path: /tmp/qa_sandboxes/TWIN-44_run_121338_20261104_041338
    developer_mounts: []
    container_inspect:
      id: cbeedce3bfb88e9790c14687b0ea2cc02cefad844a7a8e68c37509b3ca3bc1d4
      image: qa-sandbox:20261029
      image_digest: sha256:acbab225932c3877fff37f4d9e5a21235e099182c198e4f4034064ea80cf544f
      created: '2026-11-04T04:13:56.582806633Z'
      state: exited
      mounts:
      - Type: bind
        Source: /tmp/qa_sandboxes/TWIN-44_run_121338_20261104_041338
        Destination: /workspace
        Mode: ro
        RW: false
        Propagation: rprivate
  server_lock:
    path: /tmp/qa_TWIN-44_2_rub7jg/evidence/server_lock.json
    sha256: fac978d481548420274c3e69fa14fd115f30a222fb2847c07ad23327d243f369
  checkout_log:
    path: /tmp/qa_TWIN-44_2_rub7jg/evidence/checkout.log
    sha256: 5c76f8887ab6a21f75b731d1b19567b4264d2312090667eb050ad0e3ceedd63c
  runtime_log:
    path: /tmp/qa_TWIN-44_2_rub7jg/evidence/runtime.log
    sha256: 40da06b256c6f14e259110009580052a3346d4204223b8cd0a2ad4df68fd175f
  server_verdict:
    path: /tmp/qa_TWIN-44_2_rub7jg/evidence/server_verdict.json
    sha256: 936af90d6dd8259fee24ae6eb268955b33a1e367732aa39a5242cd05cff1a49e
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
    duration: 0.31s
    output: "========================================================================\n\
      TWIN-44 MC USART2 921600 & USART1 Non-Blocking [MC-DBG] Verification\n========================================================================\n\
      [RUN ] test_usart2_921600_reconfig\n[PASS] test_usart2_921600_reconfig\n[RUN\
      \ ] test_ring_buffer_trunc_drop_and_recovery\n[PASS] test_ring_buffer_trunc_drop_and_recovery\n\
      [RUN ] test_honest_minimc_v2_queries_and_nack\n[PASS] test_honest_minimc_v2_queries_and_nack\n\
      [RUN ] test_non_intrusive_notify_and_fault_sync\n[PASS] test_non_intrusive_notify_and_fault_sync\n\
      [RUN ] test_tx_fail_suppresses_ack_and_recovers\n[PASS] test_tx_fail_suppresses_ack_and_recovers\n\
      [RUN ] test_relay_timeout_crc_err_and_recovery\n[PASS] test_relay_timeout_crc_err_and_recovery\n\
      ------------------------------------------------------------------------\nAll\
      \ 6 TWIN-44 test suites (including post-error recovery) PASSED!\n========================================================================\n\
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
  timestamp: '2026-11-04T04:13:59.602049+00:00'
  path: /tmp/qa_TWIN-44_2_rub7jg/evidence/server_qa.json
  sha256: 18f166b33112dfd7b2a0027c7f3c74825d05a55a09b9e1752018cc150a711ae2
platform: codex
model: gpt-6-luna
session_evidence:
  path: /tmp/qa_TWIN-44_2_rub7jg/reviews/6006992cdc4e431aab9071a6107e09d2/codex.jsonl
  sha256: b4080843bac8553b37b790aa9f4233de138f41785c2166042bfdb974bb3a02ae
reviewed_artifacts:
- path: /tmp/qa_TWIN-44_2_rub7jg/request.json
  sha256: 37f6897254c448b6911286b497a6f23f820fbd2fc43cd9f8b118a8330c6cf8a0
- path: /tmp/qa_TWIN-44_2_rub7jg/diffs/project-control.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_TWIN-44_2_rub7jg/diffs/soc-ap.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_TWIN-44_2_rub7jg/diffs/mcu-p3.patch
  sha256: db113d33f9cf37f441e7547e5bd1f571ed510534496665b9128d3776546a9671
- path: /tmp/qa_TWIN-44_2_rub7jg/diffs/test_harness.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_sandboxes/TWIN-44_run_121338_20261104_041338/mcu-p3/motion-controller-mcu/project/src/minimc_proto.c
  sha256: 38a7c4842356d13c3870567ae4fc8284b64e108c2bae8588411fb9e0ccf008e4
- path: /tmp/qa_sandboxes/TWIN-44_run_121338_20261104_041338/mcu-p3/motion-controller-mcu/project/inc/minimc_proto.h
  sha256: 7986230ecaa81e7bfc4d255bbfa9573968ac8bb0f5a55decd86b041320e45d5c
- path: /tmp/qa_sandboxes/TWIN-44_run_121338_20261104_041338/mcu-p3/motion-controller-mcu/project/src/test_twin44_mc_debug.c
  sha256: fb4a08300a7b6d4239bb1eeaf58c9dbfa1257dedc493e1fb62b43e305dc24188
verification_scope: Bounded software and C unit-test verification in the Docker QA
  sandbox for USART2 921600 reconfiguration, the USART1 2048B non-blocking debug ring,
  honest MiniMC command handling, state logging, send failure handling, and recovery.
  Physical MCU flashing and hardware HIL are excluded.
verification_environment: docker-sandbox-and-independent-codex-audit
```

The pinned bundle hash and candidate identity match the request. Frozen server evidence records a successful run of all six C test suites, but the implementation incorrectly treats any TH frame as the response to the outstanding relay request and reports it as ACK. This violates honest relay status handling.
