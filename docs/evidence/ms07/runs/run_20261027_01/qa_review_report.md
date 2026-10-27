# Independent QA Review Report: `MS-07` (`run_20261027_01`)

- **Milestone / Task ID**: `MS-07` (`实现主控版本查询`, Revision `5`)
- **Review Run ID**: `run_20261027_01`
- **Reviewer Role**: `QA` (`independent-qa-reviewer`)
- **Reviewer Session ID**: `663fcda3-b02b-4d3a-89f6-ffc1ef283810`
- **Author Role & Session ID**: `ENG-FWD` (`1c634be7-4be2-4743-af02-dc8ada31bad3`)
- **Review Timestamp**: `2026-10-27T10:37:12+08:00`
- **Decision**: **`APPROVED`** (`decision: accepted`)

---

## 1. Scope, Repository & Deliverable Hash Verification

| Check Item | Expected / Contract | Actual Observed | Verdict |
| :--- | :--- | :--- | :--- |
| `soc-ap` Base Commit | `3b474924f9f0079e77fb5fa01f56abff2e1fc2f5` | `3b474924f9f0079e77fb5fa01f56abff2e1fc2f5` | PASS |
| `soc-ap` Modified/Added Paths (`git status --porcelain=v1`) | Within `soc-ap/core/forward/transport/**`, `soc-ap/core/host/**`, `soc-ap/CMakeLists.txt` | `M CMakeLists.txt`, `A core/forward/transport/serial_posix.cpp`, `A core/forward/transport/serial_posix.h`, `M core/host/main.cpp` | PASS |
| Deliverable 1: `soc-ap/core/forward/transport/serial_posix.h` | `7071f089fc19b47e5179719da16cb4de23c5b0d4447c135e119276b96e425818` | `7071f089fc19b47e5179719da16cb4de23c5b0d4447c135e119276b96e425818` (`2138` bytes, `64` lines) | PASS |
| Deliverable 2: `soc-ap/core/forward/transport/serial_posix.cpp` | `e3254b399e09c146667e2f70af512857f3731feacceb193ae50d5602764e9f35` | `e3254b399e09c146667e2f70af512857f3731feacceb193ae50d5602764e9f35` (`4418` bytes, `177` lines) | PASS |
| Deliverable 3: `soc-ap/core/host/main.cpp` | `b990595eea8378cfcb0384e0f66adc145491d59e372a1ac123eeacb5618c40c8` | `b990595eea8378cfcb0384e0f66adc145491d59e372a1ac123eeacb5618c40c8` (`10814` bytes, `338` lines) | PASS |
| Deliverable 4: `soc-ap/CMakeLists.txt` | `9091fb625294c9e8213e8d38abb2df60e87a2ac01e9667cb72b374ed574fe11f` | `9091fb625294c9e8213e8d38abb2df60e87a2ac01e9667cb72b374ed574fe11f` (`2920` bytes, `86` lines) | PASS |
| Consumed `soc-ap/core/forward/minimc/parser.cpp` (`V2-P0506`) | `4b882ecaf454b564d93ce57b50bbba624b62d45902aa0cf85a937e6b1da4cc1b` | `4b882ecaf454b564d93ce57b50bbba624b62d45902aa0cf85a937e6b1da4cc1b` | PASS |
| Consumed `soc-ap/core/forward/minimc/codec.cpp` (`V2-P04D`) | `e943c3b6c991063a6a887b954ce9eef95dd2485ddf5901c9763052f97414b040` | `e943c3b6c991063a6a887b954ce9eef95dd2485ddf5901c9763052f97414b040` | PASS |
| `test_harness` (`5a2ebe49e26ffb76a55ab74de652142ce9961de7`) | Clean working tree | Clean | PASS |
| `mcu-p3` (`14b8057b04030bd659744c874c73ff8f09f29979`) | Clean working tree | Clean | PASS |

---

## 2. Coding Standard Gatekeeper Audit (`project-control/.agents/rules/c_cpp_coding_standard.md`)

### 2.1 Function-by-Function Audit of `soc-ap/core/forward/transport/serial_posix.cpp`

| Function Name | Linkage | Line Range | Raw Lines (Incl. Braces) | Parameter Count | Guard Clause at Entry | Verdict |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `baud_to_speed` | `static` | L11–L28 | 18 (`<= 50`) | 1 (`uint32_t baud`) | N/A (value param) | PASS |
| `configure_termios` | `static` | L30–L56 | 27 (`<= 50`) | 2 (`int fd`, `speed_t speed`) | `tcgetattr(fd, &tty) != 0` | PASS |
| `serial_open` | Public | L58–L81 | 24 (`<= 50`) | 2 (`const SerialConfig*`, `SerialContext*`) | Yes (`if (!config \|\| !ctx \|\| !config->device_path)`) | PASS |
| `serial_close` | Public | L83–L92 | 10 (`<= 50`) | 1 (`SerialContext*`) | Yes (`if (!ctx)`) | PASS |
| `serial_write` | Public | L94–L132 | 39 (`<= 50`) | 4 (`ctx`, `data`, `size`, `bytes_written`) | Yes (`if (!ctx \|\| !ctx->is_open \|\| ctx->fd < 0)`) | PASS |
| `serial_read` | Public | L134–L174 | 41 (`<= 50`) | 4 (`ctx`, `buf`, `timeout_ms`, `bytes_read`) | Yes (`if (!ctx \|\| !ctx->is_open \|\| ... \|\| !buf)`) | PASS |

- **POSIX `termios` & Non-Blocking I/O Review**:
  - Opens device with `O_RDWR | O_NOCTTY | O_NONBLOCK`.
  - `configure_termios` configures raw 8N1 mode (`~PARENB`, `~CSTOPB`, `~CSIZE`, `CS8`, `~CRTSCTS`, `CLOCAL | CREAD`), disables canonical mode/echo/signals (`~(ICANON | ECHO | ECHOE | ISIG)`), disables software flow control (`~(IXON | IXOFF | IXANY)`), disables CR/LF translation and output post-processing (`~OPOST`), sets `VMIN = 0`, `VTIME = 0`, and flushes I/O queues (`tcflush(fd, TCIOFLUSH)`).
  - `serial_read` uses `poll()` with explicit `timeout_ms` and handles `POLLERR | POLLHUP | POLLNVAL` and `EINTR`/`EAGAIN` cleanly.
  - Zero dynamic heap allocation (`new`, `delete`, `malloc`, `free`, or dynamic STL containers are completely absent in `serial_posix.*`).

### 2.2 Function-by-Function Audit of `soc-ap/core/host/main.cpp`

| Function Name | Linkage | Line Range | Raw Lines (Incl. Braces) | Parameter Count | Guard Clause at Entry | Verdict |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `request_shutdown` | Anonymous NS | L19–L21 | 3 (`<= 50`) | 1 (`int`) | N/A | PASS |
| `print_usage` | Anonymous NS | L31–L36 | 6 (`<= 50`) | 1 (`const char*`) | N/A | PASS |
| `print_hex_stream` | Anonymous NS | L38–L48 | 11 (`<= 50`) | 3 (`label`, `data`, `len`) | Yes (`if (!label)`) | PASS |
| `parse_arg_item` | Anonymous NS | L50–L90 | 41 (`<= 50`) | 4 (`arg`, `next_arg`, `opts`, `advance`) | Yes (`if (!arg \|\| !opts \|\| !advance)`) | PASS |
| `parse_arguments` | Anonymous NS | L92–L122 | 31 (`<= 50`) | 3 (`argc`, `argv`, `opts`) | Yes (`if (!opts)`) | PASS |
| `send_version_query` | Anonymous NS | L124–L148 | 25 (`<= 50`) | 3 (`ctx`, `cmd_id`, `tx_len`) | Yes (`if (!ctx \|\| !tx_len)`) | PASS |
| `print_frame_report` | Anonymous NS | L150–L167 | 18 (`<= 50`) | 1 (`const FrameView*`) | Yes (`if (!frame)`) | PASS |
| `print_query_diagnostics` | Anonymous NS | L169–L187 | 19 (`<= 50`) | 4 (`total_rx`, `rx_log`, `rx_log_len`, `parser`) | Yes (`if (!parser)`) | PASS |
| `record_raw_capture` | `static` | L194–L203 | 10 (`<= 50`) | 3 (`cap`, `src`, `count`) | Yes (`if (!cap \|\| !src \|\| count == 0)`) | PASS |
| `current_time_ms` | `static` | L205–L212 | 8 (`<= 50`) | 0 | N/A | PASS |
| `feed_rx_bytes` | `static` | L220–L232 | 13 (`<= 50`) | 4 (`src`, `count`, `target`, `now_ms`) | Yes (`if (!src \|\| !target \|\| !target->parser \|\| !target->received)`) | PASS |
| `poll_and_parse` | Anonymous NS | L234–L273 | 40 (`<= 50`) | 4 (`ctx`, `timeout_ms`, `out_frame`, `received`) | Yes (`if (!ctx \|\| !out_frame \|\| !received)`) | PASS |
| `execute_query_version` | Anonymous NS | L275–L300 | 26 (`<= 50`) | 1 (`const HostOptions*`) | Yes (`if (!opts)`) | PASS |
| `run_host_daemon` | Anonymous NS | L302–L316 | 15 (`<= 50`) | 1 (`const HostOptions*`) | Yes (`if (!opts)`) | PASS |
| `main` | Public | L320–L337 | 18 (`<= 50`) | 2 (`argc`, `argv`) | N/A | PASS |

- All 15 functions in `main.cpp` are `<= 41` lines (`<= 50` hard gate) and take `<= 4` parameters (using `HostOptions`, `RxCapture`, and `FeedTarget` context structures).
- All TX/RX buffers (`tx_buf[MAX_FRAME_SIZE]`, `rx_buf[64]`, `RxCapture::buffer[512]`, `StreamParser`) are statically sized on the stack with zero `new`/`malloc`.

---

## 3. Independent Reproduction, PTY Closed-Loop Verification & HIL Evidence Audit

### 3.1 Local Build & Full CTest Regression (`/tmp/ai_soc_ms07_qa_build`)
- **Configure & Build**:
  - `cmake -S soc-ap -B /tmp/ai_soc_ms07_qa_build -G Ninja -DCMAKE_BUILD_TYPE=Release -DMINIMC_QA_ROOT="$PWD/test_harness"` -> exit code `0`.
  - `cmake --build /tmp/ai_soc_ms07_qa_build --clean-first` -> exit code `0`, `0` warnings/errors under `-Wall -Wextra -Wpedantic -Werror` across `minimcproto`, `soc-ap`, and `minimc-probe`.
- **CTest 11/11 Suite (`env -C /tmp/ai_soc_ms07_qa_build ctest --output-on-failure`)**:
  - `100% tests passed, 0 tests failed out of 11` (`0.40 sec`): `host_runtime_smoke`, `minimc_reference`, `minimc_crc`, `minimc_encode`, `minimc_decode_bounds`, `minimc_decode`, `minimc_stream_sync`, `minimc_stream_header`, `minimc_stream_payload`, `minimc_timeout`, `minimc_recovery`.

### 3.2 Independent Host PTY Loopback Verification (Positive & Negative Paths)
1. **Negative Device Path**:
   - `/tmp/ai_soc_ms07_qa_build/bin/soc-ap --query-version --device /dev/nonexistent_tty_ms07 --timeout-ms 50` -> exited with code `1` (`error: failed to open serial device ...`).
2. **Positive End-to-End PTY Loopback with Leading DGUS Noise + Valid MCU Version Reply**:
   - Opened a real POSIX pseudo-terminal (`pty.openpty()`) and ran `soc-ap --query-version --device <pts> --timeout-ms 1000 --cmd-id 3`.
   - Verified `soc-ap` transmitted the exact 14-byte MiniMCProto v2.0 frame: `55 AA 01 02 05 03 04 00 01 00 00 00 AE 08`.
   - Injected 4 bytes of DGUS noise (`5A A5 07 82`) followed by a valid 18-byte MCU response frame (`55 AA 02 01 04 03 04 00 01 00 04 00 02 00 01 04 51 FA`).
   - `soc-ap` filtered the noise, validated the frame (`crc16: 0xFA51`), printed `SUCCESS: Valid response frame received from MCU!` with `proto_ver: 2.0` and `firmware_ver: 1.4`, and exited with code `0`.

### 3.3 VMware Physical Hardware-in-the-Loop (HIL) Evidence Audit
1. **`05_vmware_hil_query_cmd03.log` (`sha256:fab0019b117c3c10d64910eb6f5e0c36b7377fa0b2e6365e2d6583ed6e1c100d`)**:
   - Executed on VMware Ubuntu guest connected to physical `/dev/ttyUSB0` (`115200 8N1`, `timeout=2000ms`).
   - Transmitted `TX Query Frame (14 bytes): 55 AA 01 02 05 03 04 00 01 00 00 00 AE 08` (valid CRC-16/CCITT-FALSE `0x08AE`).
   - Captured `22,281` bytes from the AT32 MC board over the 2000ms window (~11.1 KB/s continuous 115200 baud stream).
   - Stream parser rejected all `22,281` non-`0x55` DGUS bytes (`5A A5 07 82 ...`) into `err_sof: 22281` with `dispatched_frames: 0`, confirming noise immunity and zero false-positive frame completion.
2. **`06_vmware_hil_query_cmd01.log` (`sha256:b4aae6b8543214e197a9c1ebb5c0fb8410f8a919fa8d9ad86d7895f9048920f8`)**:
   - Transmitted `TX Query Frame (14 bytes): 55 AA 01 02 05 01 04 00 01 00 00 00 4D 68` (`cmd_id=0x01`, valid CRC-16/CCITT-FALSE `0x684D`).
   - Captured `22,346` bytes over 2000ms, safely recording `err_sof: 22346` and `dispatched_frames: 0`.
3. **Hardware Baseline Consistency**:
   - Raw captured stream (`5A A5 07 82 10 09 01 2C 88 91 5A A5 07 82 21 87 00 00 E6 0B ...`) matches DWIN DGUS variable write frames (`0x5A 0xA5` header, command `0x82`) emitted by the existing AT32 MC firmware on USART2 (`PA2/PA3` at `115200` baud), consistent with `project-control/docs/baseline/serial_links.md` and `manifest.yaml`.

---

## 4. QA Signature

- **Reviewer**: `QA` (`663fcda3-b02b-4d3a-89f6-ffc1ef283810`)
- **Verified Deliverables**:
  - `soc-ap/core/forward/transport/serial_posix.h` (`sha256:7071f089fc19b47e5179719da16cb4de23c5b0d4447c135e119276b96e425818`)
  - `soc-ap/core/forward/transport/serial_posix.cpp` (`sha256:e3254b399e09c146667e2f70af512857f3731feacceb193ae50d5602764e9f35`)
  - `soc-ap/core/host/main.cpp` (`sha256:b990595eea8378cfcb0384e0f66adc145491d59e372a1ac123eeacb5618c40c8`)
  - `soc-ap/CMakeLists.txt` (`sha256:9091fb625294c9e8213e8d38abb2df60e87a2ac01e9667cb72b374ed574fe11f`)
- **Review Outcome**: **`APPROVED`** (`decision: accepted`)
- **Signed At**: `2026-10-27T10:37:12+08:00`
