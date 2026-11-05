```yaml
task_id: TWIN-45
task_revision: 1
candidate_commit: 29d62ef1bb7cf33e334f7e58aae81717cd26c54f
role: QA
decision: APPROVED
summary: Pinned candidate and frozen evidence match the bundle. The bounded host GCC
  verification passed, and the audited positive, negative, and recovery cases cover
  the accepted scope.
findings: []
accepted_scope: Host GCC unit-test verification of USART1 921600 cascade observation
  and USART3 115200 non-blocking [TH-DBG] logging, runtime sensor and filament state
  synchronization, summaries limited to 2 Hz, and error, truncation, USART1 TX failure,
  and ring overflow recovery. The MCU diff is limited to the three allowed mcu-p3
  paths; other repository diffs are empty. Bundle SHA256 and recorded evidence/diff
  hashes match. Cross-compiler ELF builds and physical MCU USB/UART HIL are excluded
  by the contract and are not treated as missing required checks. source_report is
  empty, so there is no report or report SHA256 to audit.
unexecuted: []
actual_session: 01a1a4fd-5e6a-7b91-832a-9d0eb3871d4b
reviewer_role: QA
reviewer_roles:
- QA
reviewed_artifact_version: project-control=42b031efff970b01ee8cc8e5dd087387cdf9288f;
  soc-ap=426d604e9ddcfdb3e95e94ecff4f699ae976fc95; mcu-p3=29d62ef1bb7cf33e334f7e58aae81717cd26c54f;
  test_harness=ccf1476a0b98cb55ca9ee7bd49d73ca5d4704414
server_qa:
  task_id: TWIN-45
  task_revision: 1
  source: server-pinned-commits
  fresh_checkout: true
  sandbox:
    kind: container
    container_id: 30a49b8cabc3
    id: TWIN-45_run_131643_20261104_051643
    image: qa-sandbox:20261029
    path: /tmp/qa_sandboxes/TWIN-45_run_131643_20261104_051643
    developer_mounts: []
    container_inspect:
      id: 30a49b8cabc35963f23c86b6e376af5f1c869440508629b526ee9429548aaecf
      image: qa-sandbox:20261029
      image_digest: sha256:acbab225932c3877fff37f4d9e5a21235e099182c198e4f4034064ea80cf544f
      created: '2026-11-04T05:17:07.042104434Z'
      state: exited
      mounts:
      - Type: bind
        Source: /tmp/qa_sandboxes/TWIN-45_run_131643_20261104_051643
        Destination: /workspace
        Mode: ro
        RW: false
        Propagation: rprivate
  server_lock:
    path: /tmp/qa_TWIN-45_oaer0sm7/evidence/server_lock.json
    sha256: 27e93d4df79e6f2725a0c97e546ff568fbc0fb12d040634a7daa9e00ce16a7d5
  checkout_log:
    path: /tmp/qa_TWIN-45_oaer0sm7/evidence/checkout.log
    sha256: 31b1369ca00035543e1e3d0c42fda86e90070ff92eb0becf2b1ec3efff2dc3e8
  runtime_log:
    path: /tmp/qa_TWIN-45_oaer0sm7/evidence/runtime.log
    sha256: d8c9b335d3e245f7a1f1b8a2e2e1b530a3080663d90472271abb2bc5a0e20be6
  server_verdict:
    path: /tmp/qa_TWIN-45_oaer0sm7/evidence/server_verdict.json
    sha256: b305462cfc3895ed2a2828ad4a34fe980fb2e86db36540d395046c3b6fc96ef4
  tool_versions:
    git: git version 2.25.1
    python: Python 3.8.10
  build_results: []
  test_results:
  - command: gcc -std=c11 -O2 -Wall -Wextra -no-pie -fno-pie -DAT32F423CCT7 -DUSE_STDPERIPH_DRIVER
      -DAT_START_F423_V1 -I inc -I inc/temperature_control -I at32f423_board -I src
      -I src/app -I libraries/cmsis/cm4/core_support -I libraries/cmsis/cm4/device_support
      -I libraries/drivers/inc src/bsp/usart.c src/app/minimc_proto.c src/user/test_twin45_th_debug.c
      -o /tmp/test_twin45 && /tmp/test_twin45 && rm -f /tmp/test_twin45
    exit_code: '0'
    subpath: mcu-p3/color-engine-mcu/io_toggle
    duration: 0.36s
    output: "========================================================================\n\
      TWIN-45 TH USART1 921600 Cascade & USART3 Non-Blocking [TH-DBG] Suite\n========================================================================\n\
      [RUN ] test_usart1_921600_and_usart3_115200_init\n[PASS] test_usart1_921600_and_usart3_115200_init\n\
      [RUN ] test_cascade_rx_and_tx_logging\n[PASS] test_cascade_rx_and_tx_logging\n\
      [RUN ] test_periodic_state_and_dynamic_sync\n[PASS] test_periodic_state_and_dynamic_sync\n\
      [RUN ] test_negative_crc_err_bad_frame_and_recovery\n[PASS] test_negative_crc_err_bad_frame_and_recovery\n\
      [RUN ] test_negative_usart1_send_raw_fail_and_recovery\n[PASS] test_negative_usart1_send_raw_fail_and_recovery\n\
      [RUN ] test_negative_usart3_trunc_and_recovery\n[PASS] test_negative_usart3_trunc_and_recovery\n\
      [RUN ] test_negative_usart3_ring_full_drop_and_recovery\n[PASS] test_negative_usart3_ring_full_drop_and_recovery\n\
      ------------------------------------------------------------------------\nAll\
      \ 7 TWIN-45 test suites PASSED!\n========================================================================\n\
      \nIn file included from libraries/cmsis/cm4/device_support/at32f423.h:275,\n\
      \                 from libraries/drivers/inc/at32f423_adc.h:36,\n          \
      \       from inc/thermistor_adc.h:10,\n                 from src/app/minimc_proto.c:3:\n\
      libraries/cmsis/cm4/core_support/core_cm4.h: In function '__NVIC_SetVector':\n\
      libraries/cmsis/cm4/core_support/core_cm4.h:1913:23: warning: cast to pointer\
      \ from integer of different size [-Wint-to-pointer-cast]\n 1913 |   uint32_t\
      \ *vectors = (uint32_t *)SCB->VTOR;\n      |                       ^\nlibraries/cmsis/cm4/core_support/core_cm4.h:\
      \ In function '__NVIC_GetVector':\nlibraries/cmsis/cm4/core_support/core_cm4.h:1929:23:\
      \ warning: cast to pointer from integer of different size [-Wint-to-pointer-cast]\n\
      \ 1929 |   uint32_t *vectors = (uint32_t *)SCB->VTOR;\n      |             \
      \          ^"
  passed: true
  timestamp: '2026-11-04T05:17:10.062324+00:00'
  path: /tmp/qa_TWIN-45_oaer0sm7/evidence/server_qa.json
  sha256: cfa0484ca8f92bee10f7995151259384c68470b0eedd446faf4f8a05c0167d78
platform: codex
model: gpt-6-luna
session_evidence:
  path: /tmp/qa_TWIN-45_oaer0sm7/reviews/4dbbf3a8150b44b786f603058b7d05b5/codex.jsonl
  sha256: 6dc9ad1f2e67d49be9a9ce1dbff5b5e6f0ca4e36eab71abfbabe8d7258b5ee64
reviewed_artifacts:
- path: /tmp/qa_TWIN-45_oaer0sm7/request.json
  sha256: 777255a11ec682035a21ac567186d78a2723ae22cdf12ad640268720a4879aa7
- path: /tmp/qa_TWIN-45_oaer0sm7/diffs/project-control.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_TWIN-45_oaer0sm7/diffs/soc-ap.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_TWIN-45_oaer0sm7/diffs/mcu-p3.patch
  sha256: 79191f9e17cb43261b891913e43f935cda58bc5e80923a9f844408ee72f6f7bc
- path: /tmp/qa_TWIN-45_oaer0sm7/diffs/test_harness.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_sandboxes/TWIN-45_run_131643_20261104_051643/mcu-p3/color-engine-mcu/io_toggle/src/bsp/usart.c
  sha256: c394473d5a17c79dcea7f341efced73aae639def41a69ac3832eb2687388e239
- path: /tmp/qa_sandboxes/TWIN-45_run_131643_20261104_051643/mcu-p3/color-engine-mcu/io_toggle/inc/usart.h
  sha256: 700d48e2d9dc13b1fa1bffa20cc7b74fb8bbc0986a5c26ee27f7b35247bd9cb4
- path: /tmp/qa_sandboxes/TWIN-45_run_131643_20261104_051643/mcu-p3/color-engine-mcu/io_toggle/src/user/test_twin45_th_debug.c
  sha256: 724d0278531f81484d722be7e32e0d8c749f077292bb1848a4bf8ad1a31b9689
verification_scope: Host GCC unit-test verification of USART1 921600 cascade observation
  and USART3 115200 non-blocking [TH-DBG] logging, runtime sensor and filament state
  synchronization, summaries limited to 2 Hz, and error, truncation, USART1 TX failure,
  and ring overflow recovery. The MCU diff is limited to the three allowed mcu-p3
  paths; other repository diffs are empty. Bundle SHA256 and recorded evidence/diff
  hashes match. Cross-compiler ELF builds and physical MCU USB/UART HIL are excluded
  by the contract and are not treated as missing required checks. source_report is
  empty, so there is no report or report SHA256 to audit.
verification_environment: docker-sandbox-and-independent-codex-audit
```

Pinned candidate and frozen evidence match the bundle. The bounded host GCC verification passed, and the audited positive, negative, and recovery cases cover the accepted scope.
