# V2-P04B 独立 QA 审查报告（Revision 1 / `run_20261026_01`）

## 1. 审查身份与元数据

- **任务编号**：`V2-P04B`（实现有界帧编码）
- **版本 / 轮次**：Revision `1`（`run_20261026_01`）
- **被审角色 / 会话**：`ENG-FWD`（Session ID: `1c634be7-4be2-4743-af02-dc8ada31bad3`）
- **独立 QA 审查角色 / 会话**：`QA`（Session ID: `663fcda3-b02b-4d3a-89f6-ffc1ef283810`）
- **父调度会话**：`COORD`（Session ID: `9e5411f4-acad-421e-b487-9e68b9483320`）
- **审查完成时间**：`2026-10-26T20:46:29+08:00`
- **审查结论**：**`APPROVED`**

---

## 2. 被审交付物与工作区基线核验

| 核验项 | 实测值 / 结论 | 状态 |
| --- | --- | --- |
| 被审主产物路径 | `soc-ap/core/forward/minimc/codec.cpp` | PASS |
| 被审主产物 SHA256 | `a659515a549b4ffe6e444aa2648e4984288df1fd225fea8356a7cc6a1a1608c7` | PASS |
| 被审主产物大小 / 行数 | `3063` bytes / `90` lines | PASS |
| `soc-ap` Base Commit (`HEAD`) | `e3215c449421ba0898004012ece1a7d329ea4cf0` | PASS |
| `soc-ap` 工作区状态 (`git status --porcelain=v1`) | ` M core/forward/minimc/codec.cpp`（严格单文件改动） | PASS |
| `test_harness` Base Commit (`HEAD`) | `5a2ebe49e26ffb76a55ab74de652142ce9961de7`（工作区干净） | PASS |
| 只读头文件 `soc-ap/core/forward/minimc/codec.h` | `733b589bf4ddb08c6108ffdc039acaab4992425bf1393a3dd94ae19f91fc0e75` | PASS |
| 只读构建配置 `soc-ap/CMakeLists.txt` | `549df0a78f0baab9d6c3331c73cb590c3dd73a81d476c5b4aec7b8dfbb6053d8` | PASS |
| 只读探针源码 `soc-ap/tests/protocol/probe.cpp` | `2ebee129e4c1d35fa394d74d8b5daf66e4480cb5b4671c89055af29be554b42c` | PASS |
| 只读运行器 `test_harness/static_checks/minimcproto/run_codec_cases.py` | `e1384164c92078fe8dc71017d5128c0b0e610deb527f53d182efa6c5257f9cdf` | PASS |
| 只读样例集 `test_harness/test_cases/minimcproto/vectors.json` | `6d46bd05a4133e678611abe2ab1cb88db190c394f23151900009c0c077c8d995` | PASS |

---

## 3. 任务卡验收准则与代码逐项核查（`V2-P04B.md`）

1. **有界编码与内存安全序列化**：
   - 入口先执行 `if (out_written != nullptr) { *out_written = 0; }`，确保任何失败分支均不会泄露旧有效长度。
   - MTU 边界检查：`if (payload.size > MAX_PAYLOAD_SIZE || header.payload_len > MAX_PAYLOAD_SIZE)` 返回 `Status::ERR_MTU_EXCEEDED`。
   - 空指针检查：`if (payload.data == nullptr && (payload.size > 0 || header.payload_len > 0))` 返回 `Status::ERR_INVALID_ARGUMENT`。
   - 缓冲区容量检查：`const size_t total_frame_size = HEADER_SIZE + payload.size + CRC_SIZE; if (out_buffer.data == nullptr || out_buffer.size < total_frame_size)` 返回 `Status::ERR_BUFFER_TOO_SMALL`。
   - 12 字节帧头采用显式单字节偏移写入 `out_buffer.data[0..11]`（含固定魔数 `SOF_1=0x55`, `SOF_2=0xAA`、小端 `seq` 与小端 `payload.size`），无结构体指针强转或未对齐访问风险。
   - 载荷拷贝至 `out_buffer.data[12 .. 12 + payload.size - 1]`，随后对前 `12 + payload.size` 字节调用已验收的 `calc_crc16`，并以小端序（LSB 在 `crc_coverage`，MSB 在 `crc_coverage + 1`）写入尾部 2 字节。
2. **范围边界与未实现函数桩隔离**：
   - `decode_frame` 严格保持 `Status::ERR_NOT_IMPLEMENTED` 桩状态，未提前越界实现 `V2-P04C`/`V2-P04D` 逻辑。
   - 针对尚未实现的 `decode` 分组独立执行 `run_codec_cases.py --case-set decode`，实测退出码为 `1`（精准拦截未实现桩，无伪造通过）。
3. **独立复跑构建与 `encode` / `crc` 用例集全量验证**：
   - `cmake -S soc-ap -B /tmp/ai_soc_v2_build/V2-P04B_QA -G Ninja -DCMAKE_BUILD_TYPE=Debug`：退出码 `0`。
   - `cmake --build /tmp/ai_soc_v2_build/V2-P04B_QA --clean-first`：退出码 `0`，`-Wall -Wextra -Wpedantic -Werror` 下零警告编译通过。
   - `run_codec_cases.py --case-set encode`：退出码 `0`，`8/8` 用例全部通过：
     - `ENC-001`（`V01` 0B 载荷，14B 恰好容量 -> `55AA01020501040000000000F91E`）：PASS
     - `ENC-002`（`V02_INBOUND` 4B 载荷，18B -> `55AA010305030400010004007856341266B0`）：PASS
     - `ENC-003`（`CMD_PONG` 12B 载荷，26B -> `55AA03010604040001000C007856341280563412100800007F2B`）：PASS
     - `ENC-004`（`CMD_VERSION_REPORT` 16B 载荷，30B -> `55AA020106020400000010000200010001000000A1B2C3D407000000780C`）：PASS
     - `ENC-005`（最大 `1024B` 载荷，1038B 恰好容量 -> `encoded_len: 1038`, `crc16_hex: 0x1021`, `crc16_le_hex: 2110` 及完整 1038B 字节比对）：PASS
     - `ENC-006`（`payload_len=1025` 超 MTU -> `status: error, error_code: mtu_exceeded, encoded_len: 0`）：PASS
     - `ENC-007`（输出容量 13B 差 1B -> `status: error, error_code: buffer_too_small, encoded_len: 0`）：PASS
     - `ENC-008`（空载荷指针且 `payload_len=4` -> `status: error, error_code: invalid_argument, encoded_len: 0`）：PASS
   - `run_codec_cases.py --case-set crc`：退出码 `0`，`9/9` 用例回归全部通过。
   - `env -C /tmp/ai_soc_v2_build/V2-P04B_QA ctest --output-on-failure -R ^host_runtime_smoke$`：退出码 `0`（`1/1 Passed`）。
   - `python3 project-control/tools/check_task_graph.py --check-artifact V2-P04B`：退出码 `0`，`errors: []`。

---

## 4. 独立复跑原始输出摘要

```text
$ git -C soc-ap rev-parse HEAD && git -C soc-ap status --porcelain=v1
e3215c449421ba0898004012ece1a7d329ea4cf0
 M core/forward/minimc/codec.cpp

$ sha256sum soc-ap/core/forward/minimc/codec.cpp
a659515a549b4ffe6e444aa2648e4984288df1fd225fea8356a7cc6a1a1608c7  soc-ap/core/forward/minimc/codec.cpp

$ cmake -S soc-ap -B /tmp/ai_soc_v2_build/V2-P04B_QA -G Ninja -DCMAKE_BUILD_TYPE=Debug && cmake --build /tmp/ai_soc_v2_build/V2-P04B_QA --clean-first
[1/7] Building CXX object CMakeFiles/minimcproto.dir/core/forward/minimc/parser.cpp.o
[2/7] Building CXX object CMakeFiles/minimcproto.dir/core/forward/minimc/codec.cpp.o
[3/7] Linking CXX static library libminimcproto.a
[4/7] Building CXX object CMakeFiles/soc-ap.dir/core/host/main.cpp.o
[5/7] Linking CXX executable bin/soc-ap
[6/7] Building CXX object CMakeFiles/minimc-probe.dir/tests/protocol/probe.cpp.o
[7/7] Linking CXX executable bin/minimc-probe

$ python3 test_harness/static_checks/minimcproto/run_codec_cases.py --vectors test_harness/test_cases/minimcproto/vectors.json --probe /tmp/ai_soc_v2_build/V2-P04B_QA/bin/minimc-probe --case-set encode
"total_cases": 8, "passed_cases": 8, "failed_cases": 0, "status": "ok", "exit_code": 0

$ python3 test_harness/static_checks/minimcproto/run_codec_cases.py --vectors test_harness/test_cases/minimcproto/vectors.json --probe /tmp/ai_soc_v2_build/V2-P04B_QA/bin/minimc-probe --case-set crc
"total_cases": 9, "passed_cases": 9, "failed_cases": 0, "status": "ok", "exit_code": 0

$ decode_unimplemented_exit_code=1
$ 1/1 Test #1: host_runtime_smoke ...............   Passed    0.11 sec
```

---

## 5. 签名与最终结论

- **审查结论**：**`APPROVED`**
- **被审产物**：`soc-ap/core/forward/minimc/codec.cpp`（SHA256: `a659515a549b4ffe6e444aa2648e4984288df1fd225fea8356a7cc6a1a1608c7`）
- **独立 QA 签名**：`QA (663fcda3-b02b-4d3a-89f6-ffc1ef283810)` @ `2026-10-26T20:46:29+08:00`
