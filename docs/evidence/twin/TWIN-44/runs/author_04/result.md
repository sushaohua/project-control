# TWIN-44 Author Self-Check & Delivery Report (`author_04`)

- **task_id**: `TWIN-44`
- **revision**: `1`
- **run_id**: `author_04`
- **author_role**: `ENG-MC`
- **author_session_id**: `8ca47c46-1cd8-4f82-955a-9742b6988ded`
- **target_repo**: `mcu-p3`
- **branch**: `feat/soc-debug`
- **source_baseline**: `e051111e68dd61896ed42c0961153b167b8bca41`
- **previous_candidate_commit**: `d2e469559081616f6312ecbabf8d6b69a7e92e3a` (`author_03`)
- **candidate_commit**: `04a2e8d161e1a1a18efc0d41d0dad91d51d065e9`
- **arch_breakdown_ref**: `project-control/docs/architecture/debug_reconciliation_and_921600_arch_breakdown_20261104.md` (`revision: 9`, SHA-256: `13b5a69b92f8369457ed99c0dbea5b5756d6bb2d4b1c7308bcfa33732ab4dad7`, Section `1.3.5` item 2)
- **qa_remediation_ref**: `project-control/docs/evidence/twin/TWIN-44/runs/qa_03/qa_review_report.md` (Independent Codex session `01a1a4c3-87c2-7c43-b651-9d349664e841`)

---

## 1. Summary of Remediation in `author_04`

1. **Strict TH Relay Response Correlation (`handle_th_frame()` in `minimc_proto.c`)**:
   - Added `s_relay_seq16` to record the full 16-bit sequence number of the active pending TH relay request when `handle_ap_frame()` forwards a `dst == MINIMC_NODE_TH` request (`s_relay_pending = true`).
   - Added static helpers `is_valid_th_relay_cmd(uint8_t req_cmd, uint8_t resp_cmd, uint16_t plen)` (20 lines, 3 params) and `validate_th_relay_resp(const uint8_t *frame, uint8_t *out_err_code)` (32 lines, 2 params) to validate incoming TH frames before any state transition or AP forwarding:
     1. Must have an active pending relay request (`s_relay_pending == true`);
     2. Header fields must be a valid TH-to-AP response (`src == MINIMC_NODE_TH (0x03)`, `dst == MINIMC_NODE_AP (0x01)`, `(flags & MINIMC_FLAG_IS_RESPONSE) != 0U`, `hop_limit > 1U`);
     3. 16-bit sequence number `rx_seq16` must strictly equal `s_relay_seq16`;
     4. Response command `cmd_id` must match the pending request command (`0x01 -> 0x02`, `0x03 -> 0x04`, `0x14 -> 0x15`, or `MINIMC_CMD_NACK (0x06)` with payload length $\ge 1$).
   - When an unsolicited TH frame (`!s_relay_pending`), stale/mismatched sequence TH frame (`rx_seq16 != s_relay_seq16`), mismatched command TH frame, or invalid header/TTL TH frame is received:
     - `s_relay_pending` is **preserved** (never falsely disarmed, so the genuine pending request's timeout remains armed);
     - The invalid frame is **not** forwarded to AP over `USART2` and **never** emits `dir=RELAY_RX status=ACK`;
     - Instead, `handle_th_frame()` emits `[MC-DBG] ts=<ms> dir=ERR node=TH seq=<seq> cmd=0x<XX> status=BAD_FRAME err_code=0x07` (or `0x05` for `hop_limit <= 1U`).
   - Only when `validate_th_relay_resp()` succeeds does `handle_th_frame()` clear `s_relay_pending = false`, emit `dir=RELAY_RX node=TH ... status=ACK|NACK`, forward the frame to AP via `minimc_proto_send()`, and emit `dir=TX` or `dir=ERR status=TX_ERR` according to the actual send return value.

2. **Expanded Unit Test Coverage (`test_twin44_mc_debug.c`)**:
   - Added `inject_th_custom_frame()` and `test_th_relay_correlation_and_nack()` (Suite 7) verifying:
     1. Unsolicited TH frame with no pending relay logs `dir=ERR node=TH seq=50 cmd=0x02 status=BAD_FRAME err_code=0x07` and is not forwarded to AP;
     2. With pending relay (`seq=51, cmd=0x01`), injected mismatched-seq (`seq=99, cmd=0x02`) and mismatched-cmd (`seq=51, cmd=0x04`) frames both log `dir=ERR node=TH ... status=BAD_FRAME err_code=0x07`, do not forward to AP, and preserve `s_relay_pending`, followed by a valid matching TH response (`seq=51, cmd=0x02`) at `+20ms` that logs `dir=RELAY_RX node=TH seq=51 cmd=0x02 status=ACK elapsed_ms=20` and forwards to AP;
     3. With pending relay (`seq=52, cmd=0x01`), an injected mismatched-seq (`seq=88`) frame does not disarm the timeout, and advancing time `+250ms` triggers `dir=RELAY_RX node=TH seq=52 cmd=0x01 status=TIMEOUT elapsed_ms=250`;
     4. With pending relay (`seq=53, cmd=0x01`), a matching TH `NACK (0x06)` (`err_code=0x04`) logs `dir=RELAY_RX node=TH seq=53 cmd=0x06 status=NACK err_code=0x04 elapsed_ms=15` and `dir=TX node=TH seq=53 cmd=0x06 status=NACK err_code=0x04 elapsed_ms=15`.

---

## 2. Modified Files & Scope Audit (`e051111e...` -> `04a2e8d1...`)

`git -C mcu-p3 diff --name-only e051111e68dd61896ed42c0961153b167b8bca41 04a2e8d161e1a1a18efc0d41d0dad91d51d065e9`:
1. `motion-controller-mcu/project/inc/minimc_proto.h`
2. `motion-controller-mcu/project/src/minimc_proto.c`
3. `motion-controller-mcu/project/src/test_twin44_mc_debug.c`

Zero changes outside `allowed_paths` (`main.c`, `wk_usart.c`, `wk_usart.h`, `color-engine-mcu/**`, `marlin/**` untouched).

---

## 3. Coding Standard & Unit Test Evidence

- **Function Line & Parameter Gate**:
  - `minimc_proto.c`: max function length = `47` lines (`<= 50`), max parameters = `4` (`<= 4`).
  - `test_twin44_mc_debug.c`: max function length = `46` lines (`<= 50`), max parameters = `4` (`<= 4`).
  - Zero dynamic memory allocation (`malloc`/`free`/`new`/`delete` = 0).
- **Host / Docker Sandbox Test Execution**:
  - Command:
    ```bash
    gcc -std=c11 -O2 -Wall -Wextra -no-pie -fno-pie -DAT32F435VGT7 -DUSE_STDPERIPH_DRIVER \
      -I project/inc -I project/delay -I project/marlin -I project/marlin/marlin_core \
      -I project/marlin/marlin_module -I libraries/drivers/inc \
      -I libraries/cmsis/cm4/core_support -I libraries/cmsis/cm4/device_support \
      project/src/minimc_proto.c project/src/test_twin44_mc_debug.c \
      -o /tmp/test_twin44 && /tmp/test_twin44 && rm -f /tmp/test_twin44
    ```
  - Output:
    ```text
    [PASS] test_usart2_921600_reconfig
    [PASS] test_ring_buffer_trunc_drop_and_recovery
    [PASS] test_honest_minimc_v2_queries_and_nack
    [PASS] test_non_intrusive_notify_and_fault_sync
    [PASS] test_tx_fail_suppresses_ack_and_recovers
    [PASS] test_relay_timeout_crc_err_and_recovery
    [PASS] test_th_relay_correlation_and_nack
    All 7 TWIN-44 test suites (including TH relay correlation & recovery) PASSED!
    ```
