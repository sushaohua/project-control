# V2-P05A 独立 QA 审查报告（Revision 1 / `run_20261026_01`）

## 1. 审查身份与元数据

- **任务编号**：`V2-P05A`（实现解析器复位和同步）
- **版本 / 轮次**：Revision `1`（`run_20261026_01`）
- **被审角色 / 会话**：`ENG-FWD`（Session ID: `1c634be7-4be2-4743-af02-dc8ada31bad3`）
- **独立 QA 审查角色 / 会话**：`QA`（Session ID: `663fcda3-b02b-4d3a-89f6-ffc1ef283810`）
- **父调度会话**：`COORD`（Session ID: `9e5411f4-acad-421e-b487-9e68b9483320`）
- **审查完成时间**：`2026-10-26T21:14:03+08:00`
- **审查结论**：**`APPROVED`** (`decision: APPROVED`)

---

## 2. 被审交付物与工作区基线核验

| 核验项 | 实测值 / 结论 | 状态 |
| --- | --- | --- |
| 被审主产物路径 | `soc-ap/core/forward/minimc/parser.cpp` | PASS |
| 被审主产物 SHA256 | `573901547d37813fe42dade25459948096886c82baf1866387b065858daf3f33` | PASS |
| 被审主产物大小 / 行数 | `3018` bytes / `96` lines | PASS |
| `soc-ap` Base Commit (`HEAD`) | `bc2506049c1c4947b32e8d59055b146ff9e4fac4` | PASS |
| `soc-ap` 工作区状态 (`git status --porcelain=v1`) | ` M core/forward/minimc/parser.cpp`（严格单文件改动） | PASS |
| `test_harness` Base Commit (`HEAD`) | `5a2ebe49e26ffb76a55ab74de652142ce9961de7`（工作区干净） | PASS |
| 只读头文件 `soc-ap/core/forward/minimc/parser.h` | `a4397848a1c65b5a1e183b7a9e95283fb6908c4180b46701161de14b86575cbe` | PASS |
| 只读编解码器 `soc-ap/core/forward/minimc/codec.cpp` | `e943c3b6c991063a6a887b954ce9eef95dd2485ddf5901c9763052f97414b040` | PASS |
| 只读头文件 `soc-ap/core/forward/minimc/codec.h` | `733b589bf4ddb08c6108ffdc039acaab4992425bf1393a3dd94ae19f91fc0e75` | PASS |
| 只读构建配置 `soc-ap/CMakeLists.txt` | `549df0a78f0baab9d6c3331c73cb590c3dd73a81d476c5b4aec7b8dfbb6053d8` | PASS |
| 只读探针源码 `soc-ap/tests/protocol/probe.cpp` | `2ebee129e4c1d35fa394d74d8b5daf66e4480cb5b4671c89055af29be554b42c` | PASS |
| 只读运行器 `test_harness/static_checks/minimcproto/run_codec_cases.py` | `e1384164c92078fe8dc71017d5128c0b0e610deb527f53d182efa6c5257f9cdf` | PASS |
| 只读样例集 `test_harness/test_cases/minimcproto/vectors.json` | `6d46bd05a4133e678611abe2ab1cb88db190c394f23151900009c0c077c8d995` | PASS |

---

## 3. 任务卡验收准则与代码逐项核查（`V2-P05A.md`）

1. **`parser_init` 与 `parser_reset` 契约审查**：
   - `parser_init(StreamParser* parser)`：空指针防御后执行 `*parser = StreamParser{};`，将状态机置为 `WAIT_SOF1`，并清空 `rx_buffer`、索引及全部统计计数器。
   - `parser_reset(StreamParser* parser)`：空指针防御后将 `state` 置回 `WAIT_SOF1`，清零 `rx_index`、`expected_len`、`last_byte_rx_ms`，并保留诊断错误计数（`err_sof`, `err_header`, `err_mtu`, `err_crc`, `err_timeout`, `dispatched_frames`），满足幂等复位要求。
2. **`parser_feed_byte` 前导同步与噪声丢弃审查**：
   - 入口校验 `if (!parser || !out_frame_ready) return Status::ERR_INVALID_ARGUMENT;`，并初始化 `*out_frame_ready = false;` 与 `*out_frame = FrameView{};`。
   - `WAIT_SOF1`：
     - `byte == 0x55` (`SOF_1`)：写入 `rx_buffer[0] = SOF_1`，`rx_index = 1`，转移至 `WAIT_SOF2`，更新 `last_byte_rx_ms = now_ms`，返回 `Status::OK`。
     - `byte != 0x55`：累加 `err_sof++`，更新 `last_byte_rx_ms = now_ms`，保持 `WAIT_SOF1`，返回 `Status::OK`。
   - `WAIT_SOF2`：
     - `byte == 0xAA` (`SOF_2`)：写入 `rx_buffer[1] = SOF_2`，`rx_index = 2`，转移至 `READ_HEADER`，更新 `last_byte_rx_ms = now_ms`，返回 `Status::OK`。
     - `byte == 0x55` (`SOF_1`)：连续 `0x55 0x55` 维持同步前导，`rx_buffer[0] = SOF_1`，`rx_index = 1`，保持在 `WAIT_SOF2`，更新 `last_byte_rx_ms = now_ms`，返回 `Status::OK`。
     - 其余字节：累加 `err_sof++`，复位回 `WAIT_SOF1`（`rx_index = 0, expected_len = 0`），更新 `last_byte_rx_ms = now_ms`，返回 `Status::OK`。
3. **范围边界与未实现阶段隔离**：
   - `READ_HEADER`、`READ_PAYLOAD`、`READ_CRC` 状态分支严格返回 `Status::ERR_NOT_IMPLEMENTED`，`parser_poll_timeout` 保持符号桩返回 `false`，未提前越界实现 `V2-P05B`~`V2-P05E` 逻辑。
   - 针对尚未实现的 `stream_header` 分组独立执行 `run_codec_cases.py --case-set stream_header`，实测 `5/5` 全部因 `exit_code=126 / not_implemented` 被运行器拦截，整体退出码为 `1`。
4. **独立复跑构建与 `stream_sync` 及前置分组全量验证**：
   - `cmake -S soc-ap -B /tmp/ai_soc_v2_build/V2-P05A_qa -G Ninja -DCMAKE_BUILD_TYPE=Debug`：退出码 `0`。
   - `cmake --build /tmp/ai_soc_v2_build/V2-P05A_qa --clean-first`：退出码 `0`，`-Wall -Wextra -Wpedantic -Werror` 下零警告编译通过。
   - `run_codec_cases.py --case-set stream_sync`：退出码 `0`，`5/5` 用例全部通过：
     - `SYNC-001`（丢弃噪声 `00FF12` 保持 `WAIT_SOF1`, `dispatched_frames=0`）：PASS
     - `SYNC-002`（单字节 `55` 进入 `WAIT_SOF2`, `dispatched_frames=0`）：PASS
     - `SYNC-003`（`5555AA` 保持前导同步并进入 `READ_HEADER`, `header_bytes_collected=0, dispatched_frames=0`）：PASS
     - `SYNC-004`（`5501` 复位回 `WAIT_SOF1`, `dispatched_frames=0`）：PASS
     - `SYNC-005`（`WAIT_SOF2` 显式 `parser_reset` 幂等返回 `WAIT_SOF1`, `dispatched_frames=0`）：PASS
   - 前置编解码分组回归：`crc` (`9/9`)、`encode` (`8/8`)、`decode_bounds` (`6/6`)、`decode` (`12/12`) 均以退出码 `0` 全部通过。
   - `env -C /tmp/ai_soc_v2_build/V2-P05A_qa ctest --output-on-failure -R ^host_runtime_smoke$`：退出码 `0`（`1/1 Passed`）。
   - `python3 project-control/tools/check_task_graph.py --check-artifact V2-P05A`：退出码 `0`，`errors: []`。

---

## 4. 独立复跑原始输出摘要

```text
$ git -C soc-ap rev-parse HEAD && git -C soc-ap status --porcelain=v1
bc2506049c1c4947b32e8d59055b146ff9e4fac4
 M core/forward/minimc/parser.cpp

$ sha256sum soc-ap/core/forward/minimc/parser.cpp
573901547d37813fe42dade25459948096886c82baf1866387b065858daf3f33  soc-ap/core/forward/minimc/parser.cpp

$ cmake -S soc-ap -B /tmp/ai_soc_v2_build/V2-P05A_qa -G Ninja -DCMAKE_BUILD_TYPE=Debug && cmake --build /tmp/ai_soc_v2_build/V2-P05A_qa --clean-first
[1/7] Building CXX object CMakeFiles/minimcproto.dir/core/forward/minimc/parser.cpp.o
[2/7] Building CXX object CMakeFiles/minimcproto.dir/core/forward/minimc/codec.cpp.o
[3/7] Linking CXX static library libminimcproto.a
[4/7] Building CXX object CMakeFiles/soc-ap.dir/core/host/main.cpp.o
[5/7] Linking CXX executable bin/soc-ap
[6/7] Building CXX object CMakeFiles/minimc-probe.dir/tests/protocol/probe.cpp.o
[7/7] Linking CXX executable bin/minimc-probe

$ python3 test_harness/static_checks/minimcproto/run_codec_cases.py --vectors test_harness/test_cases/minimcproto/vectors.json --probe /tmp/ai_soc_v2_build/V2-P05A_qa/bin/minimc-probe --case-set stream_sync
"total_cases": 5, "passed_cases": 5, "failed_cases": 0, "status": "ok", "exit_code": 0

$ stream_header_unimplemented_exit_code=1
$ 1/1 Test #1: host_runtime_smoke ...............   Passed    0.11 sec
```

---

## 5. 签名与最终结论

- **审查结论**：**`APPROVED`** (`decision: APPROVED`)
- **被审产物**：`soc-ap/core/forward/minimc/parser.cpp`（SHA256: `573901547d37813fe42dade25459948096886c82baf1866387b065858daf3f33`）
- **独立 QA 签名**：`QA (663fcda3-b02b-4d3a-89f6-ffc1ef283810)` @ `2026-10-26T21:14:03+08:00`
