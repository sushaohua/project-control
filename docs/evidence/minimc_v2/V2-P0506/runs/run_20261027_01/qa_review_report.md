# Independent QA Review Report: `V2-P0506` (`run_20261027_01`)

- **Microtask ID**: `V2-P0506` (`流式解析器收尾、CTest集成与离线协议候选归档(包5包6合并)`, Revision `1`)
- **Review Run ID**: `run_20261027_01`
- **Reviewer Role**: `QA` (`independent-qa-reviewer`)
- **Reviewer Session ID**: `663fcda3-b02b-4d3a-89f6-ffc1ef283810`
- **Author Role & Session ID**: `ENG-FWD` (`1c634be7-4be2-4743-af02-dc8ada31bad3`)
- **Review Timestamp**: `2026-10-27T09:53:34+08:00`
- **Decision**: **`APPROVED`** (`decision: accepted`)

---

## 1. Scope, Repository & Deliverable Hash Verification

| Check Item | Expected / Contract | Actual Observed | Verdict |
| :--- | :--- | :--- | :--- |
| `soc-ap` Base Commit | `79be851016c62e31b041700b4cd200a488a8eade` | `79be851016c62e31b041700b4cd200a488a8eade` | PASS |
| `soc-ap` Modified Paths (`git status --porcelain=v1`) | Only `CMakeLists.txt` and `core/forward/minimc/parser.cpp` | ` M CMakeLists.txt`, ` M core/forward/minimc/parser.cpp` | PASS |
| Deliverable 1: `soc-ap/core/forward/minimc/parser.cpp` | `4b882ecaf454b564d93ce57b50bbba624b62d45902aa0cf85a937e6b1da4cc1b` | `4b882ecaf454b564d93ce57b50bbba624b62d45902aa0cf85a937e6b1da4cc1b` (`7466` bytes, `244` lines) | PASS |
| Deliverable 2: `soc-ap/CMakeLists.txt` | `acf7197951385bdc93d09b2b3a9928cf4d62675e4b3aba74d492cfaef6daaeac` | `acf7197951385bdc93d09b2b3a9928cf4d62675e4b3aba74d492cfaef6daaeac` (`2761` bytes, `83` lines) | PASS |
| Deliverable 3: `project-control/docs/releases/minimc_v2_offline_candidate.yaml` | `e5728fccdc5983c5761b481661d1fc72f6e4a879d40d7f142f1e4da5eca461ab` | `e5728fccdc5983c5761b481661d1fc72f6e4a879d40d7f142f1e4da5eca461ab` (`2436` bytes, `71` lines) | PASS |
| Unmodified `soc-ap/core/forward/minimc/parser.h` | `a4397848a1c65b5a1e183b7a9e95283fb6908c4180b46701161de14b86575cbe` | `a4397848a1c65b5a1e183b7a9e95283fb6908c4180b46701161de14b86575cbe` | PASS |
| Unmodified `soc-ap/core/forward/minimc/codec.cpp` | `e943c3b6c991063a6a887b954ce9eef95dd2485ddf5901c9763052f97414b040` | `e943c3b6c991063a6a887b954ce9eef95dd2485ddf5901c9763052f97414b040` | PASS |
| Unmodified `soc-ap/core/forward/minimc/codec.h` | `733b589bf4ddb08c6108ffdc039acaab4992425bf1393a3dd94ae19f91fc0e75` | `733b589bf4ddb08c6108ffdc039acaab4992425bf1393a3dd94ae19f91fc0e75` | PASS |
| Unmodified `soc-ap/tests/protocol/probe.cpp` | `2ebee129e4c1d35fa394d74d8b5daf66e4480cb5b4671c89055af29be554b42c` | `2ebee129e4c1d35fa394d74d8b5daf66e4480cb5b4671c89055af29be554b42c` | PASS |
| `test_harness` (`5a2ebe49e26ffb76a55ab74de652142ce9961de7`) | Clean working tree | Clean | PASS |
| `mcu-p3` (`14b8057b04030bd659744c874c73ff8f09f29979`) | Clean working tree (untouched) | Clean | PASS |

---

## 2. Coding Standard Gatekeeper Audit (`project-control/.agents/rules/c_cpp_coding_standard.md`)

### 2.1 Function Length (`<= 50` Lines) & Parameter Count (`<= 4` Parameters) Audit on `soc-ap/core/forward/minimc/parser.cpp`

| Function Name | Linkage | Line Range | Raw Lines (Incl. Signature/Braces) | Effective Code Lines (Excl. Blank/Comments) | Parameter Count | Guard Clause at Entry | Verdict |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `parser_init` | Public | L10–L15 | 6 | 6 | 1 (`StreamParser*`) | Yes (`if (!parser)`) | PASS |
| `parser_reset` | Public | L17–L27 | 11 | 9 | 1 (`StreamParser*`) | Yes (`if (!parser)`) | PASS |
| `feed_wait_sof1` | `static` | L29–L45 | 17 | 17 | 3 (`parser`, `byte`, `now_ms`) | Yes (`if (!parser)`) | PASS |
| `feed_wait_sof2` | `static` | L47–L75 | 29 | 27 | 3 (`parser`, `byte`, `now_ms`) | Yes (`if (!parser)`) | PASS |
| `feed_read_header` | `static` | L77–L115 | 39 | 34 | 3 (`parser`, `byte`, `now_ms`) | Yes (`if (!parser)`) | PASS |
| `feed_read_payload` | `static` | L117–L130 | 14 | 14 | 3 (`parser`, `byte`, `now_ms`) | Yes (`if (!parser)`) | PASS |
| `feed_read_crc` | `static` | L132–L177 | 46 | 39 | 4 (`parser`, `byte`, `now_ms`, `DispatchSink*`) | Yes (`if (!parser \|\| !sink \|\| !sink->out_ready)`) | PASS |
| `parser_feed_byte` | Public (Frozen ABI) | L179–L222 | 44 | 36 | 5 (Frozen in `V2-P02B` `parser.h`; delegates to `<= 4`-param `static` helpers per §1.3) | Yes (`if (!parser \|\| !out_frame_ready)`) | PASS |
| `parser_poll_timeout` | Public | L224–L241 | 18 | 18 | 2 (`parser`, `now_ms`) | Yes (`if (!parser)`) | PASS |

### 2.2 Memory, Pointer & Control-Flow Safety Audit
- **Zero Dynamic Heap Allocation (§3.4)**: Confirmed zero occurrences of `new`, `delete`, `malloc`, `free`, or dynamic STL containers (`std::vector`, `std::string`, etc.).
- **Explicit Pointer & Index Operations (§3.1)**: Confirmed zero compressed pointer/index increments (such as `*dst++ = *src++` or `rx_buffer[rx_index++] = byte`); all buffer writes and `rx_index++` increments are separated onto distinct lines. Pointer indirection depth is `<= 1`.
- **Control Flow Flattening & Guard Clauses (§2.2, §3.2)**: All public and internal functions validate pointers on their first executable line; maximum block nesting depth is `<= 2` levels (`<= 3` limit).

---

## 3. Protocol State Machine, Timeout, Self-Healing & CTest Audit

1. **Payload Accumulation & CRC Completion (`feed_read_payload`, `feed_read_crc`)**:
   - Accumulates `L` payload bytes in `READ_PAYLOAD` and transitions to `READ_CRC` when `rx_index == expected_len - 2`.
   - In `READ_CRC`, stores the low CRC byte at `rx_index == expected_len - 2` without dispatching, and stores the high CRC byte at `rx_index == expected_len - 1` before calling `decode_frame(Bytes(parser->rx_buffer, parser->expected_len), sink->out_frame)`.
   - On `Status::OK`: sets `*(sink->out_ready) = true` and increments `parser->dispatched_frames++`.
   - On error: increments `parser->err_crc++` and sets `*(sink->out_ready) = false`.
   - In both cases, resets `state = WAIT_SOF1`, `rx_index = 0`, `expected_len = 0` while preserving diagnostic counters.
2. **Inter-Byte 50ms Timeout & `uint32_t` Wraparound (`parser_feed_byte`, `parser_poll_timeout`)**:
   - Strictly implements the **Check-Before-Refresh** rule: when `parser->state != ParserState::WAIT_SOF1`, computes `const uint32_t elapsed_ms = now_ms - parser->last_byte_rx_ms;` using unsigned `uint32_t` modular arithmetic (handling `0xFFFFFFE0 -> 0x00000010` wraparound).
   - When `elapsed_ms > 50`, increments `parser->err_timeout++` and resets `state = WAIT_SOF1`, `rx_index = 0`, `expected_len = 0` prior to dispatching the current byte to `feed_wait_sof1`.
   - `parser_poll_timeout` is idempotent in `WAIT_SOF1` (`returns false`) and resets + increments `err_timeout++` (`returns true`) when `state != WAIT_SOF1 && elapsed_ms > 50`.
3. **CMake & CTest Suite Registration (`soc-ap/CMakeLists.txt`)**:
   - Preserves `host_runtime_smoke` and registers `minimc_reference` plus 9 functional test targets (`minimc_crc`, `minimc_encode`, `minimc_decode_bounds`, `minimc_decode`, `minimc_stream_sync`, `minimc_stream_header`, `minimc_stream_payload`, `minimc_timeout`, `minimc_recovery`) when `-DMINIMC_QA_ROOT` is set.
   - Fails configuration with `FATAL_ERROR` if `-DMINIMC_QA_ROOT` points to a path missing required runner/vector files (verified via negative CMake test: `bad_qa_root_exit_code=1`).
4. **Offline Candidate Manifest (`project-control/docs/releases/minimc_v2_offline_candidate.yaml`)**:
   - Complete YAML structure with `candidate_id`, `scope`, `repositories`, `protocol` (`sha256: 9f8d4f9607cb3e76cc30b9ee2f971b23c3e0d936611188466a71f4aa15f3ce54`), `verification`, `limitations`, and `handoff`.

---

## 4. Independent Reproduction & Verification Commands

All verification commands were independently executed in an isolated QA build directory (`/tmp/ai_soc_v2_build/V2-P0506_QA`):

| Step ID | Command Executed | Exit Code | Observed Result |
| :--- | :--- | :--- | :--- |
| `precheck` | `git -C soc-ap rev-parse HEAD && git -C soc-ap status --porcelain=v1 && git -C test_harness rev-parse HEAD && git -C test_harness status --porcelain=v1` | `0` | `soc-ap` at `79be851016c62e31b041700b4cd200a488a8eade` (`M CMakeLists.txt`, `M core/forward/minimc/parser.cpp`); `test_harness` at `5a2ebe49e26ffb76a55ab74de652142ce9961de7` (clean) |
| `configure` | `cmake -S soc-ap -B /tmp/ai_soc_v2_build/V2-P0506_QA -G Ninja -DCMAKE_BUILD_TYPE=Debug -DMINIMC_QA_ROOT="$PWD/test_harness"` | `0` | Configured cleanly with Python 3.8.10 and Ninja |
| `build` | `cmake --build /tmp/ai_soc_v2_build/V2-P0506_QA --clean-first` | `0` | `[7/7] Linking CXX executable bin/minimc-probe`; `0` warnings under `-Wall -Wextra -Wpedantic -Werror` |
| `focused_recovery` | `python3 test_harness/static_checks/minimcproto/run_codec_cases.py --vectors test_harness/test_cases/minimcproto/vectors.json --probe /tmp/ai_soc_v2_build/V2-P0506_QA/bin/minimc-probe --case-set recovery` | `0` | `total_cases: 4`, `passed_cases: 4`, `failed_cases: 0` (`REC-001`..`REC-004` all passed) |
| `focused_timeout` | `python3 test_harness/static_checks/minimcproto/run_codec_cases.py --vectors test_harness/test_cases/minimcproto/vectors.json --probe /tmp/ai_soc_v2_build/V2-P0506_QA/bin/minimc-probe --case-set timeout` | `0` | `total_cases: 6`, `passed_cases: 6`, `failed_cases: 0` (`TMO-001`..`TMO-006` all passed) |
| `run_all_cases` | `python3 test_harness/static_checks/minimcproto/run_codec_cases.py --vectors test_harness/test_cases/minimcproto/vectors.json --probe /tmp/ai_soc_v2_build/V2-P0506_QA/bin/minimc-probe --case-set all` | `0` | `total_cases: 60`, `passed_cases: 60`, `failed_cases: 0` across all 9 functional groups |
| `ctest_list` | `env -C /tmp/ai_soc_v2_build/V2-P0506_QA ctest -N` | `0` | `Total Tests: 11` (`host_runtime_smoke`, `minimc_reference`, and 9 `minimc_<group>` targets) |
| `ctest_all` | `env -C /tmp/ai_soc_v2_build/V2-P0506_QA ctest --output-on-failure` | `0` | `100% tests passed, 0 tests failed out of 11` (`0.41 sec`) |
| `cmake_bad_root` | `cmake -S soc-ap -B /tmp/ai_soc_v2_build/V2-P0506_QA_bad_root -G Ninja -DCMAKE_BUILD_TYPE=Debug -DMINIMC_QA_ROOT="/tmp/nonexistent_qa_root_dir"` | `1` (Expected failure) | Rejected missing QA root with `FATAL_ERROR` |
| `check_task_graph` | `python3 project-control/tools/check_task_graph.py --workspace . --check-artifact V2-P0506` | `0` | `errors: []`, all 3 deliverable hashes verified |

---

## 5. QA Signature

- **Reviewer**: `QA` (`663fcda3-b02b-4d3a-89f6-ffc1ef283810`)
- **Verified Deliverables**:
  - `soc-ap/core/forward/minimc/parser.cpp` (`sha256:4b882ecaf454b564d93ce57b50bbba624b62d45902aa0cf85a937e6b1da4cc1b`)
  - `soc-ap/CMakeLists.txt` (`sha256:acf7197951385bdc93d09b2b3a9928cf4d62675e4b3aba74d492cfaef6daaeac`)
  - `project-control/docs/releases/minimc_v2_offline_candidate.yaml` (`sha256:e5728fccdc5983c5761b481661d1fc72f6e4a879d40d7f142f1e4da5eca461ab`)
- **Review Outcome**: **`APPROVED`** (`decision: accepted`)
- **Signed At**: `2026-10-27T09:53:34+08:00`
