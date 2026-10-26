# V2-P04C 独立 QA 审查报告（Revision 1 / `run_20261026_01`）

## 1. 审查身份与元数据

- **任务编号**：`V2-P04C`（实现解码长度与边界防御）
- **版本 / 轮次**：Revision `1`（`run_20261026_01`）
- **被审角色 / 会话**：`ENG-FWD`（Session ID: `1c634be7-4be2-4743-af02-dc8ada31bad3`）
- **独立 QA 审查角色 / 会话**：`QA`（Session ID: `663fcda3-b02b-4d3a-89f6-ffc1ef283810`）
- **父调度会话**：`COORD`（Session ID: `9e5411f4-acad-421e-b487-9e68b9483320`）
- **审查完成时间**：`2026-10-26T20:54:17+08:00`
- **审查结论**：**`APPROVED`**

---

## 2. 被审交付物与工作区基线核验

| 核验项 | 实测值 / 结论 | 状态 |
| --- | --- | --- |
| 被审主产物路径 | `soc-ap/core/forward/minimc/codec.cpp` | PASS |
| 被审主产物 SHA256 | `84312fea95497444b58a3792139325e88e71465c6a2f7fcdf90cc1aac5fa2be7` | PASS |
| 被审主产物大小 / 行数 | `3752` bytes / `109` lines | PASS |
| `soc-ap` Base Commit (`HEAD`) | `830ef5a7a230deb720f26a144f921b2c96bebe18` | PASS |
| `soc-ap` 工作区状态 (`git status --porcelain=v1`) | ` M core/forward/minimc/codec.cpp`（严格单文件改动） | PASS |
| `test_harness` Base Commit (`HEAD`) | `5a2ebe49e26ffb76a55ab74de652142ce9961de7`（工作区干净） | PASS |
| 只读头文件 `soc-ap/core/forward/minimc/codec.h` | `733b589bf4ddb08c6108ffdc039acaab4992425bf1393a3dd94ae19f91fc0e75` | PASS |
| 只读构建配置 `soc-ap/CMakeLists.txt` | `549df0a78f0baab9d6c3331c73cb590c3dd73a81d476c5b4aec7b8dfbb6053d8` | PASS |
| 只读探针源码 `soc-ap/tests/protocol/probe.cpp` | `2ebee129e4c1d35fa394d74d8b5daf66e4480cb5b4671c89055af29be554b42c` | PASS |
| 只读运行器 `test_harness/static_checks/minimcproto/run_codec_cases.py` | `e1384164c92078fe8dc71017d5128c0b0e610deb527f53d182efa6c5257f9cdf` | PASS |
| 只读样例集 `test_harness/test_cases/minimcproto/vectors.json` | `6d46bd05a4133e678611abe2ab1cb88db190c394f23151900009c0c077c8d995` | PASS |

---

## 3. 任务卡验收准则与代码逐项核查（`V2-P04C.md`）

1. **解码长度与边界防御顺序核查**：
   - 入口先执行 `if (out_frame != nullptr) { *out_frame = {}; }`，确保任何失败或未实现返回均重置输出视图。
   - **最小帧长防御**：`if (frame_bytes.data == nullptr || frame_bytes.size < MIN_FRAME_SIZE)`（`< 14` 字节）在访问任何帧头字节前安全拒绝，返回 `Status::ERR_FRAME_TOO_SHORT`。
   - **显式单字节偏移提取 `payload_len`**：通过 `frame_bytes.data[10]` 与 `frame_bytes.data[11]` 小端拼装 `declared_payload_len`，无结构体指针强转或未对齐访问。
   - **MTU 边界防御**：`if (declared_payload_len > MAX_PAYLOAD_SIZE)`（`> 1024` 字节）在读取任何载荷或 CRC 字节前安全拒绝，返回 `Status::ERR_MTU_EXCEEDED`。
   - **总长度恒等式防御**：`const size_t expected_frame_size = HEADER_SIZE + declared_payload_len + CRC_SIZE; if (frame_bytes.size != expected_frame_size)` 安全拒绝截断或超长缓冲区，返回 `Status::ERR_LENGTH_MISMATCH`。
2. **范围边界与未实现阶段隔离**：
   - 通过上述长度与边界检查的候选帧，在本阶段严格返回 `Status::ERR_NOT_IMPLEMENTED`，未提前实现 `V2-P04D` 的帧头字段合法性校验与 CRC 比对。
   - 针对完整 `decode` 分组独立执行 `run_codec_cases.py --case-set decode`，实测退出码为 `1`（精准拦截未实现桩，无伪造通过）。
   - `calc_crc16` 与 `encode_frame` 代码保持只读未变。
3. **独立复跑构建与 `decode_bounds` / `crc` / `encode` 全量验证**：
   - `cmake -S soc-ap -B /tmp/ai_soc_v2_build/V2-P04C_QA -G Ninja -DCMAKE_BUILD_TYPE=Debug`：退出码 `0`。
   - `cmake --build /tmp/ai_soc_v2_build/V2-P04C_QA --clean-first`：退出码 `0`，`-Wall -Wextra -Wpedantic -Werror` 下零警告编译通过。
   - `run_codec_cases.py --case-set decode_bounds`：退出码 `0`，`6/6` 用例全部通过：
     - `DBND-001`（0B 空输入 -> `frame_too_short`）：PASS
     - `DBND-002`（11B 残缺帧头 -> `frame_too_short`）：PASS
     - `DBND-003`（13B 截断空载帧 -> `frame_too_short`）：PASS
     - `DBND-004`（声明 `L=1025` 超 MTU -> `mtu_exceeded`）：PASS
     - `DBND-005`（声明 `L=4` 应为 18B 实为 17B -> `length_mismatch`）：PASS
     - `DBND-006`（声明 `L=0` 应为 14B 实为 15B -> `length_mismatch`）：PASS
   - `run_codec_cases.py --case-set crc`：退出码 `0`，`9/9` 用例回归通过。
   - `run_codec_cases.py --case-set encode`：退出码 `0`，`8/8` 用例回归通过。
   - `env -C /tmp/ai_soc_v2_build/V2-P04C_QA ctest --output-on-failure -R ^host_runtime_smoke$`：退出码 `0`（`1/1 Passed`）。
   - `python3 project-control/tools/check_task_graph.py --check-artifact V2-P04C`：退出码 `0`，`errors: []`。

---

## 4. 独立复跑原始输出摘要

```text
$ git -C soc-ap rev-parse HEAD && git -C soc-ap status --porcelain=v1
830ef5a7a230deb720f26a144f921b2c96bebe18
 M core/forward/minimc/codec.cpp

$ sha256sum soc-ap/core/forward/minimc/codec.cpp
84312fea95497444b58a3792139325e88e71465c6a2f7fcdf90cc1aac5fa2be7  soc-ap/core/forward/minimc/codec.cpp

$ cmake -S soc-ap -B /tmp/ai_soc_v2_build/V2-P04C_QA -G Ninja -DCMAKE_BUILD_TYPE=Debug && cmake --build /tmp/ai_soc_v2_build/V2-P04C_QA --clean-first
[1/7] Building CXX object CMakeFiles/minimcproto.dir/core/forward/minimc/parser.cpp.o
[2/7] Building CXX object CMakeFiles/minimcproto.dir/core/forward/minimc/codec.cpp.o
[3/7] Linking CXX static library libminimcproto.a
[4/7] Building CXX object CMakeFiles/soc-ap.dir/core/host/main.cpp.o
[5/7] Linking CXX executable bin/soc-ap
[6/7] Building CXX object CMakeFiles/minimc-probe.dir/tests/protocol/probe.cpp.o
[7/7] Linking CXX executable bin/minimc-probe

$ python3 test_harness/static_checks/minimcproto/run_codec_cases.py --vectors test_harness/test_cases/minimcproto/vectors.json --probe /tmp/ai_soc_v2_build/V2-P04C_QA/bin/minimc-probe --case-set decode_bounds
"total_cases": 6, "passed_cases": 6, "failed_cases": 0, "status": "ok", "exit_code": 0

$ decode_unimplemented_exit_code=1
$ 1/1 Test #1: host_runtime_smoke ...............   Passed    0.11 sec
```

---

## 5. 签名与最终结论

- **审查结论**：**`APPROVED`**
- **被审产物**：`soc-ap/core/forward/minimc/codec.cpp`（SHA256: `84312fea95497444b58a3792139325e88e71465c6a2f7fcdf90cc1aac5fa2be7`）
- **独立 QA 签名**：`QA (663fcda3-b02b-4d3a-89f6-ffc1ef283810)` @ `2026-10-26T20:54:17+08:00`
