# Independent QA Review Report: `MCQ-0106` (`run_20261027_01`)

- **Microtask ID**: `MCQ-0106` (`主控MC实现至TH板间双向业务代理转发(USART6/USART1)`, Revision `1`)
- **Review Run ID**: `run_20261027_01`
- **Reviewer Role**: `QA` (`independent-qa-reviewer`)
- **Reviewer Session ID**: `8d0be5e4-88bb-41ac-873a-995bf3f9e0f9`
- **Author Role & Session ID**: `ENG-MC` (`57212b7d-c5d1-4968-9d05-45934bef927b`)
- **Target Repository & Branch**: `mcu-p3` (`feat/soc-debug`)
- **Base Commit**: `23e8d5c8c7f44c1849da0166109fb6e88aff4e77` (Short hash `23e8d5c8`; clerical note: task card recorded `23e8d5c8052f9a76d4981766627aa5aa1c7ee07c`)
- **Candidate Commit**: `a679133204ecbb81ad48694f5372c125db2e749f`
- **Review Timestamp**: `2026-10-27T14:15:00+08:00`
- **Decision**: **`APPROVED`** (`decision: accepted`)

---

## Track 1: Process & Engineering Standard Audit (`PA-1` ~ `PA-7`)

| Audit ID | Check Item | Expected / Gatekeeper Rule | Actual Observed | Verdict |
| :--- | :--- | :--- | :--- | :--- |
| **PA-1** | Scope & Contract Alignment | Conforms to `MCQ-0106.md`: route TH (`dst_id == 0x03`) queries, send `"M115"` probe on USART6, wait with timeout, package compliant MiniMCProto response (`src_id=0x03, dst_id=0x01, fw_ver=1.0`), and pack firmware `fw_mc.bin` | Full protocol forwarding state machine implemented in `minimc_proto.c`; builds cleanly into `fw_mc.bin` | **PASS** |
| **PA-2** | Repository & Path Boundaries | Changes restricted strictly to `mcu-p3/motion-controller-mcu/project/inc/**` and `mcu-p3/motion-controller-mcu/project/src/**`; forbidden paths untouched | `git -C mcu-p3 diff --stat HEAD~1 HEAD` shows only `project/inc/minimc_proto.h` (+1) and `project/src/minimc_proto.c` (+63/-11); all other paths untouched | **PASS** |
| **PA-3** | Function Length Gate (`<= 50` Lines) | All newly written/modified self-developed functions must strictly measure `<= 50` lines (excluding empty lines / headers) | All 15 functions in `minimc_proto.c` are between 5 and 37 lines (maximum 37 lines in `parse_body_step`) | **PASS** |
| **PA-4** | Parameter Count Gate (`<= 4` Params) | Self-developed functions must take `<= 4` parameters | All 15 functions take between 0 and 4 parameters (maximum 4 params in `build_version_resp_header`) | **PASS** |
| **PA-5** | Memory & Pointer Safety | Zero dynamic heap allocation (`malloc`/`free`/`new`/`delete`); explicit array indexing (`buf[i]`), no `*dst++ = *src++`; pointer depth `<= 2` | Static bounded buffers (`s_rx_buf`, `s_tx_buf`, `resp_buf[18]`); array indexing used everywhere; no pointer arithmetic | **PASS** |
| **PA-6** | Guard Clauses & Hardware Timeout Protection | Entry null-pointer guard clauses on all pointer-accepting functions; hardware polling loops must have timeout counter | Line 1 null-pointer guard on all 5 pointer-accepting functions; `handle_th_query` bounds USART6 response wait with `timeout = 200000U`; `minimc_proto_send` bounds `usart2_tx_busy` wait with `timeout = 100000U` | **PASS** |
| **PA-7** | Protocol Specification Adherence | MiniMCProto v2.0 frame structure: `SOF: 0x55 0xAA`, `src_id: 0x03`, `dst_id: 0x01`, `flags: 0x06`, `cmd_id: req_cmd`, `seq: req_seq`, payload `[0x02, 0x00, 0x01, 0x00]`, CRC-16/CCITT-FALSE | Compliant bit-for-bit with MiniMCProto v2.0 spec; verified via independent reference decoder and probe | **PASS** |

### Function-by-Function Audit Table (`mcu-p3/motion-controller-mcu/project/src/minimc_proto.c`)

| Function Name | Linkage | Line Range | Lines (Raw) | Params | Guard Clause / Protection Mechanism | Verdict |
| :--- | :--- | :--- | :---: | :---: | :--- | :---: |
| `minimc_crc16` | Public | L20–L43 | 24 (`<= 50`) | 2 | `if (data == NULL) return 0xFFFFU;` | **PASS** |
| `parser_reset` | `static` | L45–L50 | 6 (`<= 50`) | 0 | Flat state reset | **PASS** |
| `is_header_valid` | `static` | L52–L75 | 24 (`<= 50`) | 0 | Validates `PROTO_V2`, `dst_id` in `{MC, TH, Broadcast}`, `payload_len <= 64` | **PASS** |
| `build_version_resp_header` | `static` | L77–L95 | 19 (`<= 50`) | 4 | `if (buf == NULL) return;` | **PASS** |
| `build_version_resp_payload` | `static` | L97–L111 | 15 (`<= 50`) | 2 | `if (buf == NULL) return;` | **PASS** |
| `handle_mc_query` | `static` | L113–L119 | 7 (`<= 50`) | 2 | Encapsulates MC response (`fw_ver=1.9`) | **PASS** |
| `handle_th_query` | `static` | L121–L142 | 22 (`<= 50`) | 2 | USART6 send `"M115"`, wait with `timeout = 200000U`; silent return on timeout (no spoofing) | **PASS** |
| `handle_rx_frame` | `static` | L144–L168 | 25 (`<= 50`) | 0 | Dispatcher by `dst_id` (`0x02` -> MC, `0x03` -> TH) | **PASS** |
| `process_crc_and_dispatch` | `static` | L170–L184 | 15 (`<= 50`) | 0 | CRC-16 verification before dispatching | **PASS** |
| `parse_sof_step` | `static` | L186–L213 | 28 (`<= 50`) | 1 | Flat SOF1 (`0x55`) / SOF2 (`0xAA`) stream sync | **PASS** |
| `parse_body_step` | `static` | L215–L251 | 37 (`<= 50`) | 1 | Stream header/payload/CRC collection state machine | **PASS** |
| `parse_rx_byte` | `static` | L253–L260 | 8 (`<= 50`) | 1 | Composition helper delegating to SOF/Body steps | **PASS** |
| `minimc_proto_process_rx` | Public | L262–L272 | 11 (`<= 50`) | 2 | `if (data == NULL \|\| len == 0U) return;` | **PASS** |
| `minimc_proto_send` | Public | L274–L299 | 26 (`<= 50`) | 2 | Pointer/len guard + `timeout = 100000U` on `usart2_tx_busy` | **PASS** |
| `minimc_proto_init` | Public | L301–L305 | 5 (`<= 50`) | 0 | Explicit state initialization | **PASS** |

---

## Track 2: Objective Verification (`RV-1` ~ `RV-5`)

| Verification ID | Check Item | Command / Test Harness | Observed Output | Verdict |
| :--- | :--- | :--- | :--- | :--- |
| **RV-1** | Source Hash Verification | `sha256sum minimc_proto.h minimc_proto.c` | `minimc_proto.h`: `235436443000f8d33d1dd7b6082a2907a1c4d7d4c3aaf3d32730623e43fb03f2`<br>`minimc_proto.c`: `b1b6c99b1d8008ba4da70b5c88a90cb9a230361a0bf10adba772a489c7e8e4bd`<br>Matches `result.md` exactly. | **PASS** |
| **RV-2** | Independent Clean Build & Pack Reproduction | `make -C mcu-p3/motion-controller-mcu pack` | Exit code `0`; `FLASH: 367796 B (40.09%)`, `RAM: 26424 B (6.72%)`<br>Artifact: `build/fw_mc.bin` (367,924 B)<br>Packaging prepended 128-byte firmware header with board ID `0x43500001` [MC (AT32F435)] and version `0x010951FF`. | **PASS** |
| **RV-3** | Host Unit Test with Mock USART/DMA | Host harness compiled via `gcc -std=c99 -Wall -Wextra -Werror` | 1. MC query (`dst_id=2`) -> emits MC response (`fw_ver=1.9`).<br>2. TH query (`dst_id=3`) -> calls `forward_uart_send_line("M115", 4U)` on USART6, receives TH response, and emits TH response frame (`src_id=3, dst_id=1, fw_ver=1.0, crc=0xC75E`).<br>3. TH timeout simulation -> exits silently after `200000U` countdown, emitting 0 bytes (no fake frames).<br>4. Corrupt CRC frame -> discarded, next valid frame recovers cleanly. All tests PASS. | **PASS** |
| **RV-4** | Independent Reference Vector Validation | `python3 test_harness/static_checks/minimcproto/reference_vectors.py` | Validated decoded structures and CRC-16/CCITT-FALSE on both MC and TH query/response frames:<br>- TH Query: `55AA010305030400010000008DE3` -> `status: ok`, CRC `0xE38D`<br>- TH Resp: `55AA03010603040001000400020001005EC7` -> `status: ok`, `src_id=3`, `dst_id=1`, `seq=1`, `payload_len=4`, CRC `0xC75E`. | **PASS** |
| **RV-5** | `soc-ap` `minimc-probe` Cross-Verification | `soc-ap/build/host/bin/minimc-probe decode --hex` & `feed --stream-hex` | Decoded: `src_id: 3`, `dst_id: 1`, `flags: 0x06`, `cmd_id: 0x03`, `seq: 1`, `payload_hex: "02000100"`, `crc16_hex: 0xC75E`. Stream feed dispatched 1 frame with 0 CRC/MTU errors. | **PASS** |

---

## Track 3: Clerical & Task Card Consistency Note

- In task card `MCQ-0106.md` line 67 and `result.md` line 13, `base_commit` was written as `23e8d5c8052f9a76d4981766627aa5aa1c7ee07c`.
- The actual git commit in repository `mcu-p3` is `23e8d5c8c7f44c1849da0166109fb6e88aff4e77` (the short commit `23e8d5c8` is identical).
- As previously documented in `MCQ-0105` QA report, this is a harmless historical clerical string transposition originating from `MCQ-0105.md`. The git DAG relationship `23e8d5c8 -> a679133` is fully verified and clean.

---

## QA Signature

- **Reviewer**: `QA` (`8d0be5e4-88bb-41ac-873a-995bf3f9e0f9`)
- **Verified Commit (`mcu-p3`)**: `a679133204ecbb81ad48694f5372c125db2e749f` (`feat/soc-debug`)
- **Verified Parent Commit (`mcu-p3`)**: `23e8d5c8c7f44c1849da0166109fb6e88aff4e77`
- **Verified Source Hashes**:
  - `mcu-p3/motion-controller-mcu/project/inc/minimc_proto.h`: `sha256:235436443000f8d33d1dd7b6082a2907a1c4d7d4c3aaf3d32730623e43fb03f2`
  - `mcu-p3/motion-controller-mcu/project/src/minimc_proto.c`: `sha256:b1b6c99b1d8008ba4da70b5c88a90cb9a230361a0bf10adba772a489c7e8e4bd`
- **Verified Firmware Binary (`mcu-p3/motion-controller-mcu/build/fw_mc.bin`)**:
  - Author build (`result.md`): `sha256:c11067d9e3fcc082ffff701a7041aeafcc81dfdfb2a18e32be6ccf6dd2d7eab5` (`367,924` bytes)
  - QA reproduction build: `sha256:1a0181514a9fb581f06d9a3cfca360a9bb650f8f13b9a876aa8aa95cdce983e7` (`367,924` bytes, timestamp injected)
- **Review Outcome**: **`APPROVED`** (`decision: accepted`)
- **Signed At**: `2026-10-27T14:15:00+08:00`
