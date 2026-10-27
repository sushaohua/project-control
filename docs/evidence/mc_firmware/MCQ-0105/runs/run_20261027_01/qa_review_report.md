# Independent QA Review Report: `MCQ-0105` (`run_20261027_01`)

- **Microtask ID**: `MCQ-0105` (`主控USART2接入MiniMCProto协议解析与版本查询响应`, Revision `1`)
- **Review Run ID**: `run_20261027_01`
- **Reviewer Role**: `QA` (`independent-qa-reviewer`)
- **Reviewer Session ID**: `663fcda3-b02b-4d3a-89f6-ffc1ef283810`
- **Author Role & Session ID**: `ENG-MC` (`57212b7d-c5d1-4968-9d05-45934bef927b`)
- **Target Repository & Branch**: `mcu-p3` (`feat/soc-debug`)
- **Base Commit**: `14b8057b04030bd659744c874c73ff8f09f29979`
- **Candidate Commit**: `23e8d5c8c7f44c1849da0166109fb6e88aff4e77` (short commit `23e8d5c8`)
- **Review Timestamp**: `2026-10-27T12:19:50+08:00`
- **Decision**: **`APPROVED`** (`decision: accepted`)

---

## Track 1: Process Audit (`PA-1` ~ `PA-7`)

| Audit ID | Check Item | Expected / Gatekeeper Rule | Actual Observed | Verdict |
| :--- | :--- | :--- | :--- | :--- |
| **PA-1** | Plan & Ticket Alignment | Matches `MCQ-0105.md` goals: bypass DWIN DGUS USART2 broadcast, attach MiniMCProto v2.0 parser to USART2 RX IDLE, reply to `CMD_VERSION_GET`, build `fw_mc.bin` | All 4 objectives implemented and evidenced in `result.md` and `01_precheck.log`..`04_git_diff.patch` | **PASS** |
| **PA-2** | Repository & Path Boundary | Only `mcu-p3/motion-controller-mcu/**` and `project-control/docs/evidence/mc_firmware/MCQ-0105/**` modified; `color-engine-mcu`, `bootloader`, `soc-ap`, `test_harness` untouched | `git -C mcu-p3 show --stat HEAD` shows 6 files exclusively under `motion-controller-mcu/`; `git status` clean across `mcu-p3` and `test_harness` | **PASS** |
| **PA-3** | Function Length Gate (`<= 50` Lines) | Every newly written function in `minimc_proto.c` must be `<= 50` lines | All 13 functions in `minimc_proto.c` are `5` to `37` lines (max `37` lines in `parse_body_step`) | **PASS** |
| **PA-4** | Parameter Count Gate (`<= 4` Params) | Every newly written function must take `<= 4` parameters | All 13 functions in `minimc_proto.c` take `0` to `3` parameters (max `3` params in `build_version_resp_header`) | **PASS** |
| **PA-5** | Memory & Pointer Safety | Zero dynamic heap allocation (`malloc`/`free`/`new`/`delete`); explicit array indexing (`buf[i]`), no `*dst++ = *src++` | Static bounded buffers (`s_rx_buf[78]`, `s_tx_buf[78]`, `resp_buf[18]`); all buffer writes use explicit array indices | **PASS** |
| **PA-6** | Guard Clauses & Hardware Polling Timeout | Entry null-pointer guard clauses on pointer-accepting functions; hardware polling loops must have timeout counter | All 5 pointer-accepting functions have `if (ptr == NULL)` guards on line 1; `minimc_proto_send` bounds `while (usart2_tx_busy != 0U)` with `timeout = 100000U` | **PASS** |
| **PA-7** | Legacy Code Minimal Diff Budget | Minimal, surgical bypass of DWIN DGUS screen broadcast without refactoring Marlin core | `dgus_t300spro.c` (`+4/-15`), `memu_gui.c` (`+11/-120`), `main.c` (`+2`), `CMakeLists.txt` (`+1`); Marlin motion/planner/PID untouched | **PASS** |

### Function-by-Function Audit Table (`mcu-p3/motion-controller-mcu/project/src/minimc_proto.c`)

| Function Name | Linkage | Line Range | Raw Lines (Incl. Braces) | Parameter Count | Guard Clause / Timeout Protection | Verdict |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `minimc_crc16` | Public | L19–L42 | 24 (`<= 50`) | 2 (`data`, `len`) | `if (data == NULL) return 0xFFFFU;` | PASS |
| `parser_reset` | `static` | L44–L49 | 6 (`<= 50`) | 0 | State reset | PASS |
| `is_header_valid` | `static` | L51–L72 | 22 (`<= 50`) | 0 | Validates `PROTO_V2`, `dst_id`, `payload_len <= 64` | PASS |
| `build_version_resp_header` | `static` | L74–L92 | 19 (`<= 50`) | 3 (`cmd_id`, `req_seq`, `buf`) | `if (buf == NULL) return;` | PASS |
| `build_version_resp_payload` | `static` | L94–L108 | 15 (`<= 50`) | 1 (`buf`) | `if (buf == NULL) return;` | PASS |
| `handle_rx_frame` | `static` | L110–L127 | 18 (`<= 50`) | 0 | Dispatches `0x03` / `0x01` queries | PASS |
| `process_crc_and_dispatch` | `static` | L129–L143 | 15 (`<= 50`) | 0 | Verifies little-endian CRC-16 before dispatch | PASS |
| `parse_sof_step` | `static` | L145–L172 | 28 (`<= 50`) | 1 (`byte`) | Handles `0x55` -> `0xAA` and repeated `0x55` sync | PASS |
| `parse_body_step` | `static` | L174–L210 | 37 (`<= 50`) | 1 (`byte`) | Header/payload/CRC accumulation | PASS |
| `parse_rx_byte` | `static` | L212–L219 | 8 (`<= 50`) | 1 (`byte`) | Delegates to `parse_sof_step` / `parse_body_step` | PASS |
| `minimc_proto_process_rx` | Public | L221–L231 | 11 (`<= 50`) | 2 (`data`, `len`) | `if (data == NULL \|\| len == 0U) return;` | PASS |
| `minimc_proto_send` | Public | L233–L258 | 26 (`<= 50`) | 2 (`data`, `len`) | Null/bounds guard + `timeout = 100000U` on `usart2_tx_busy` | PASS |
| `minimc_proto_init` | Public | L260–L264 | 5 (`<= 50`) | 0 | Explicit initialization | PASS |

---

## Track 2: Objective Verification (`RV-1` ~ `RV-4`)

| Verification ID | Check Item | Command / Method | Observed Output | Verdict |
| :--- | :--- | :--- | :--- | :--- |
| **RV-1** | Pre-Existing Firmware & Source Hash Verification | `sha256sum fw_mc.bin Marlin_AT32.bin minimc_proto.h minimc_proto.c` | `minimc_proto.h`: `83bb64807d9066babaf83cfb1fd07dbd63b13d96461824eec7afa32b5605164e`<br>`minimc_proto.c`: `c548b027426cae80248eaac6d1968ae5d1b4fc1e93bf67521b08ab31ab291f4e`<br>Author `fw_mc.bin`: `227474befa1659c9bdbab785bd546dc287d5498f518c2ba9d6e5fe936f4bcbef` (`367,668` B) | **PASS** |
| **RV-2** | Independent Clean Build & Pack Reproduction | `make -C mcu-p3/motion-controller-mcu clean && make -C mcu-p3/motion-controller-mcu pack` | Exit code `0`; `minimc_proto.c.obj` built with `0` warnings; `FLASH: 367540 B (40.06%)`, `RAM: 26424 B (6.72%)`; `build/fw_mc.bin` generated (`367,668` B, SHA256 `ce5855562dec727d3cf5dddc734b4b073e63f5c26cc160ed4e26b60a1670f308` with build timestamp `1793074723`) | **PASS** |
| **RV-3** | Protocol Frame Layout & CRC-16/CCITT-FALSE Verification | Host unit test compiling `minimc_proto.c` (`gcc -std=c99 -Wall -Wextra -Wpedantic -Werror`) | Feeding DGUS noise + `55AA01020503040001000000AE08` emits 18B response `55AA0201060304000100040002000109162D`; bad-CRC frame is rejected (`0` bytes TX); subsequent `cmd_id=0x01, seq=2` frame recovers and emits `55AA0201060104000200040002000109D045` | **PASS** |
| **RV-4** | Cross-Verification with `soc-ap` `minimc-probe` (`decode` & `feed`) | `/tmp/ai_soc_ms07_qa_build/bin/minimc-probe decode/feed --hex 55AA0201060304000100040002000109162D` | `status: ok`, `frame_valid: true`, `src_id: 2`, `dst_id: 1`, `flags: 0x06`, `cmd_id: 0x03`, `seq: 1`, `payload_len: 4`, `payload_hex: "02000109"`, `crc16_hex: 0x2D16`, `dispatched_frames: 1`, `err_crc: 0` | **PASS** |

---

## QA Signature

- **Reviewer**: `QA` (`663fcda3-b02b-4d3a-89f6-ffc1ef283810`)
- **Verified Commit (`mcu-p3`)**: `23e8d5c8c7f44c1849da0166109fb6e88aff4e77` (`feat/soc-debug`)
- **Verified Source Hashes**:
  - `mcu-p3/motion-controller-mcu/project/inc/minimc_proto.h`: `sha256:83bb64807d9066babaf83cfb1fd07dbd63b13d96461824eec7afa32b5605164e`
  - `mcu-p3/motion-controller-mcu/project/src/minimc_proto.c`: `sha256:c548b027426cae80248eaac6d1968ae5d1b4fc1e93bf67521b08ab31ab291f4e`
- **Verified Firmware Binary (`mcu-p3/motion-controller-mcu/build/fw_mc.bin`)**:
  - Author build (`result.md`): `sha256:227474befa1659c9bdbab785bd546dc287d5498f518c2ba9d6e5fe936f4bcbef` (`367,668` bytes)
  - QA clean rebuild (`make clean && make pack`): `sha256:ce5855562dec727d3cf5dddc734b4b073e63f5c26cc160ed4e26b60a1670f308` (`367,668` bytes)
- **Review Outcome**: **`APPROVED`** (`decision: accepted`)
- **Signed At**: `2026-10-27T12:19:50+08:00`
