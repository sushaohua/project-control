# Independent QA Review Report: `V2-P05B` (`run_20261026_01`)

- **Microtask ID**: `V2-P05B` (`实现固定帧头累积与长度门禁`, Revision `2`)
- **Review Run ID**: `run_20261026_01`
- **Reviewer Role**: `QA` (Independent QA Reviewer)
- **Reviewer Session ID**: `663fcda3-b02b-4d3a-89f6-ffc1ef283810`
- **Author Role & Session ID**: `ENG-FWD` (`1c634be7-4be2-4743-af02-dc8ada31bad3`)
- **Review Timestamp**: `2026-10-26T21:23:28+08:00`
- **Decision**: **`APPROVED`**

---

## 1. Scope & Integrity Verification

| Check Item | Expected / Contract | Actual Observed | Verdict |
| :--- | :--- | :--- | :--- |
| Target Repository (`soc-ap`) Base Commit | `a3a2d9586402a3f00d8d95902087999478f9244a` | `a3a2d9586402a3f00d8d95902087999478f9244a` | PASS |
| Target Repository Dirty Path Boundary | Only `soc-ap/core/forward/minimc/parser.cpp` modified | ` M core/forward/minimc/parser.cpp` | PASS |
| Target Artifact SHA256 (`soc-ap/core/forward/minimc/parser.cpp`) | `4839634a52fc5f33bb7c06cb245ffe4b4b9228acfaeae79b9ef87a35c7491aba` | `4839634a52fc5f33bb7c06cb245ffe4b4b9228acfaeae79b9ef87a35c7491aba` (`4226` bytes, `130` lines) | PASS |
| Unmodified `soc-ap/core/forward/minimc/parser.h` | `a4397848a1c65b5a1e183b7a9e95283fb6908c4180b46701161de14b86575cbe` | `a4397848a1c65b5a1e183b7a9e95283fb6908c4180b46701161de14b86575cbe` | PASS |
| Unmodified `soc-ap/core/forward/minimc/codec.cpp` | `e943c3b6c991063a6a887b954ce9eef95dd2485ddf5901c9763052f97414b040` | `e943c3b6c991063a6a887b954ce9eef95dd2485ddf5901c9763052f97414b040` | PASS |
| Unmodified `soc-ap/core/forward/minimc/codec.h` | `733b589bf4ddb08c6108ffdc039acaab4992425bf1393a3dd94ae19f91fc0e75` | `733b589bf4ddb08c6108ffdc039acaab4992425bf1393a3dd94ae19f91fc0e75` | PASS |
| Unmodified `soc-ap/CMakeLists.txt` | `549df0a78f0baab9d6c3331c73cb590c3dd73a81d476c5b4aec7b8dfbb6053d8` | `549df0a78f0baab9d6c3331c73cb590c3dd73a81d476c5b4aec7b8dfbb6053d8` | PASS |
| Unmodified `soc-ap/tests/protocol/probe.cpp` | `2ebee129e4c1d35fa394d74d8b5daf66e4480cb5b4671c89055af29be554b42c` | `2ebee129e4c1d35fa394d74d8b5daf66e4480cb5b4671c89055af29be554b42c` | PASS |
| `test_harness` Repository Status (`5a2ebe49e26ffb76a55ab74de652142ce9961de7`) | Clean (`git status --porcelain=v1` empty) | Clean | PASS |

---

## 2. Code & Contract Semantic Review (`soc-ap/core/forward/minimc/parser.cpp`)

1. **`READ_HEADER` Fixed Header Accumulation (`rx_index` `2..11`)**:
   - For `parser->rx_index < 11` (offsets `2..10`): stores `parser->rx_buffer[parser->rx_index++] = byte`, updates `parser->last_byte_rx_ms = now_ms`, and returns `Status::OK`.
   - For `parser->rx_index == 11` (the 12th header byte, `Payload_Len` MSB): strictly executes `parser->rx_buffer[11] = byte; parser->rx_index = 12; parser->last_byte_rx_ms = now_ms;` before computing `payload_len`.
2. **Little-Endian `Payload_Len` Extraction & `MAX_PAYLOAD_SIZE` Gate**:
   - Extracts `payload_len = static_cast<uint16_t>(static_cast<uint16_t>(parser->rx_buffer[10]) | (static_cast<uint16_t>(byte) << 8U))`.
   - When `payload_len > MAX_PAYLOAD_SIZE` (`1024`): increments `parser->err_mtu++`, resets `parser->state = ParserState::WAIT_SOF1`, `parser->rx_index = 0`, `parser->expected_len = 0`, and returns `Status::OK` without invoking any frame callback.
   - When `payload_len <= MAX_PAYLOAD_SIZE`: sets `parser->expected_len = static_cast<uint16_t>(MIN_FRAME_SIZE + payload_len)`, transitions `parser->state` to `ParserState::READ_CRC` if `payload_len == 0` or `ParserState::READ_PAYLOAD` if `payload_len > 0`, and returns `Status::OK`.
3. **Task Boundary & Embedded C++17 Discipline**:
   - `ParserState::READ_PAYLOAD` and `ParserState::READ_CRC` remain unimplemented (`return Status::ERR_NOT_IMPLEMENTED;`), and `parser_poll_timeout` remains a stub (`return false;`), respecting the boundary between `V2-P05B`, `V2-P05C`, and `V2-P05D`.
   - No dynamic memory allocation, no exceptions, no RTTI, and no STL containers are used.

---

## 3. Independent Reproduction & Verification Results

All verification commands were independently executed in an isolated build directory (`/tmp/ai_soc_v2_build/V2-P05B_qa`):

1. **Clean Build (`cmake -S soc-ap -B /tmp/ai_soc_v2_build/V2-P05B_qa -G Ninja -DCMAKE_BUILD_TYPE=Debug && cmake --build /tmp/ai_soc_v2_build/V2-P05B_qa --clean-first`)**:
   - Succeeded (`[7/7] Linking CXX executable bin/minimc-probe`, exit code `0`, zero warnings).
2. **Primary Acceptance Suite (`--case-set stream_header`)**:
   - Command: `python3 test_harness/static_checks/minimcproto/run_codec_cases.py --vectors test_harness/test_cases/minimcproto/vectors.json --probe /tmp/ai_soc_v2_build/V2-P05B_qa/bin/minimc-probe --case-set stream_header`
   - Result: `total_cases: 5`, `passed_cases: 5`, `failed_cases: 0`, `status: "ok"`, `exit_code: 0` (`SHDR-001` through `SHDR-005` all passed).
3. **Anti-Gaming Boundary Check (`--case-set stream_payload`)**:
   - Command: `(python3 test_harness/static_checks/minimcproto/run_codec_cases.py --vectors test_harness/test_cases/minimcproto/vectors.json --probe /tmp/ai_soc_v2_build/V2-P05B_qa/bin/minimc-probe --case-set stream_payload >/dev/null 2>&1; rc=$?; echo "stream_payload_unimplemented_exit_code=$rc"; test $rc -eq 1)`
   - Result: `stream_payload_unimplemented_exit_code=1` (exit code `0`), confirming `READ_PAYLOAD`/`READ_CRC` are not prematurely implemented.
4. **Regression Checks (`stream_sync` & `host_runtime_smoke`)**:
   - `--case-set stream_sync`: `total_cases: 5`, `passed_cases: 5`, `failed_cases: 0`, `exit_code: 0`.
   - `env -C /tmp/ai_soc_v2_build/V2-P05B_qa ctest --output-on-failure -R ^host_runtime_smoke$`: `1/1 Test #1: host_runtime_smoke ...............   Passed`, `exit_code: 0`.
5. **Task Graph & Artifact Registration Check**:
   - Command: `python3 project-control/tools/check_task_graph.py --check-artifact V2-P05B`
   - Result: `status: "ok"`, `errors: []`, `artifact_hashes: {"soc-ap/core/forward/minimc/parser.cpp": "4839634a52fc5f33bb7c06cb245ffe4b4b9228acfaeae79b9ef87a35c7491aba"}`, `exit_code: 0`.

---

## 4. QA Signature

- **Reviewer**: `QA` (`663fcda3-b02b-4d3a-89f6-ffc1ef283810`)
- **Verified Deliverable**: `soc-ap/core/forward/minimc/parser.cpp` (`sha256:4839634a52fc5f33bb7c06cb245ffe4b4b9228acfaeae79b9ef87a35c7491aba`)
- **Review Outcome**: **`APPROVED`**
- **Signed At**: `2026-10-26T21:23:28+08:00`
