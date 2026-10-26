# V2-P04D 独立 QA 审查报告（Revision 1 / `run_20261026_01`）

## 1. 审查身份与元数据

- **任务编号**：`V2-P04D`（实现完整帧校验与字段读取）
- **版本 / 轮次**：Revision `1`（`run_20261026_01`）
- **被审角色 / 会话**：`ENG-FWD`（Session ID: `1c634be7-4be2-4743-af02-dc8ada31bad3`）
- **独立 QA 审查角色 / 会话**：`QA`（Session ID: `663fcda3-b02b-4d3a-89f6-ffc1ef283810`）
- **父调度会话**：`COORD`（Session ID: `9e5411f4-acad-421e-b487-9e68b9483320`）
- **审查完成时间**：`2026-10-26T21:02:34+08:00`
- **审查结论**：**`APPROVED`**

---

## 2. 被审交付物与工作区基线核验

| 核验项 | 实测值 / 结论 | 状态 |
| --- | --- | --- |
| 被审主产物路径 | `soc-ap/core/forward/minimc/codec.cpp` | PASS |
| 被审主产物 SHA256 | `e943c3b6c991063a6a887b954ce9eef95dd2485ddf5901c9763052f97414b040` | PASS |
| 被审主产物大小 / 行数 | `6019` bytes / `162` lines | PASS |
| `soc-ap` Base Commit (`HEAD`) | `219597a3a85570515f21b13656979b31487da02a` | PASS |
| `soc-ap` 工作区状态 (`git status --porcelain=v1`) | ` M core/forward/minimc/codec.cpp`（严格单文件改动） | PASS |
| `test_harness` Base Commit (`HEAD`) | `5a2ebe49e26ffb76a55ab74de652142ce9961de7`（工作区干净） | PASS |
| 只读头文件 `soc-ap/core/forward/minimc/codec.h` | `733b589bf4ddb08c6108ffdc039acaab4992425bf1393a3dd94ae19f91fc0e75` | PASS |
| 只读解析器桩 `soc-ap/core/forward/minimc/parser.cpp` | `16a73b1105c78c85ca243f5a4b05d7f28875b4f29c39cb10b726c62ed2dda8d4` | PASS |
| 只读构建配置 `soc-ap/CMakeLists.txt` | `549df0a78f0baab9d6c3331c73cb590c3dd73a81d476c5b4aec7b8dfbb6053d8` | PASS |
| 只读探针源码 `soc-ap/tests/protocol/probe.cpp` | `2ebee129e4c1d35fa394d74d8b5daf66e4480cb5b4671c89055af29be554b42c` | PASS |
| 只读运行器 `test_harness/static_checks/minimcproto/run_codec_cases.py` | `e1384164c92078fe8dc71017d5128c0b0e610deb527f53d182efa6c5257f9cdf` | PASS |
| 只读样例集 `test_harness/test_cases/minimcproto/vectors.json` | `6d46bd05a4133e678611abe2ab1cb88db190c394f23151900009c0c077c8d995` | PASS |

---

## 3. 任务卡验收准则与代码逐项核查（`V2-P04D.md`）

1. **完整帧校验顺序与字段显式读取**：
   - 在 `V2-P04C` 长度/边界防御（`< 14B`、`> 1024B`、`!= 14 + L`）之后，依次执行：
     - **SOF 魔数校验**：`if (frame_bytes.data[0] != SOF_1 || frame_bytes.data[1] != SOF_2)` 返回 `Status::ERR_BAD_SOF`。
     - **协议版本位校验**：`if ((flags & FLAGS_PROTO_VERSION_MASK) != FLAGS_PROTO_VERSION_V2)` 返回 `Status::ERR_BAD_VERSION`。
     - **Flags 保留位校验**：`if ((flags & FLAGS_RESERVED_MASK) != 0)` 返回 `Status::ERR_BAD_FLAGS_RESERVED`。
     - **Route_Ctrl 互斥与保留位校验**：`if (((route_ctrl & 0x03) == 0x03) || ((route_ctrl & ROUTE_RESERVED_MASK) != 0))` 返回 `Status::ERR_BAD_ROUTE_CTRL`。
     - **显式小端 CRC-16 比对**：`wire_crc = frame_bytes.data[12 + L] | (frame_bytes.data[13 + L] << 8)` 与 `calc_crc16(Bytes(frame_bytes.data, 12 + L))` 显式比对（消除 `0x0000` 残差歧义），不匹配返回 `Status::ERR_CRC_MISMATCH`。
   - 校验全部通过后，通过显式字节偏移填充 `out_frame->header`、借用视图 `out_frame->payload`（`L > 0` 时指向 `frame_bytes.data + 12`，`L == 0` 时为 `Bytes(nullptr, 0)`）及 `out_frame->crc = wire_crc`，返回 `Status::OK`。
   - 对 `V04`（`DEC-005`）仅在物理帧结构层认定 `frame_valid: true`（`0 <= L <= 1024`），不执行急停业务动作，保持与 `OQ-01` 隔离裁决一致。
2. **范围边界与未实现阶段隔离**：
   - `parser.cpp` 流式状态机保持未实现符号桩；针对 `stream_sync` 分组运行 `run_codec_cases.py --case-set stream_sync`，实测退出码为 `1`（精准拦截未实现流式解析桩，无伪造通过）。
3. **独立复跑构建与 `decode` / `crc` / `encode` / `decode_bounds` 全量验证**：
   - `cmake -S soc-ap -B /tmp/ai_soc_v2_build/V2-P04D_QA -G Ninja -DCMAKE_BUILD_TYPE=Debug`：退出码 `0`。
   - `cmake --build /tmp/ai_soc_v2_build/V2-P04D_QA --clean-first`：退出码 `0`，`-Wall -Wextra -Wpedantic -Werror` 下零警告编译通过。
   - `run_codec_cases.py --case-set decode`：退出码 `0`，`12/12` 用例全部通过：
     - `DEC-001`（`V01` 14B `CMD_GET_VERSION`）：PASS
     - `DEC-002`（`V02_INBOUND` 18B `CMD_PING`）：PASS
     - `DEC-003`（`V02_OUTBOUND` 18B `hop=3, route_ctrl=0x04`）：PASS
     - `DEC-004`（`V03` 25B `CMD_STREAM_CHUNK`）：PASS
     - `DEC-005`（`V04` 14B 帧结构有效 `frame_valid: true` + `command_valid: false, conflict_id: OQ-01`）：PASS
     - `DEC-006`（合法 `CRC == 0x0000` 显式比对通过）：PASS
     - `DEC-007`（最大 `1024B` 载荷帧 1038B 解码通过）：PASS
     - `DEC-008`（坏 SOF `0x55 0xAB` -> `bad_sof`）：PASS
     - `DEC-009`（坏 CRC -> `crc_mismatch`）：PASS
     - `DEC-010`（非法版本 `flags=0x01` -> `bad_version`）：PASS
     - `DEC-011`（非零保留位 `flags=0x25` -> `bad_flags_reserved`）：PASS
     - `DEC-012`（互斥路由控制 `route_ctrl=0x03` -> `bad_route_ctrl`）：PASS
   - 全量编解码回归：`crc` (`9/9`)、`encode` (`8/8`)、`decode_bounds` (`6/6`) 全部以退出码 `0` 通过（合计 35/35 编解码用例 100% 通过）。
   - `env -C /tmp/ai_soc_v2_build/V2-P04D_QA ctest --output-on-failure -R ^host_runtime_smoke$`：退出码 `0`（`1/1 Passed`）。
   - `python3 project-control/tools/check_task_graph.py --check-artifact V2-P04D`：退出码 `0`，`errors: []`。

---

## 4. 独立复跑原始输出摘要

```text
$ git -C soc-ap rev-parse HEAD && git -C soc-ap status --porcelain=v1
219597a3a85570515f21b13656979b31487da02a
 M core/forward/minimc/codec.cpp

$ sha256sum soc-ap/core/forward/minimc/codec.cpp
e943c3b6c991063a6a887b954ce9eef95dd2485ddf5901c9763052f97414b040  soc-ap/core/forward/minimc/codec.cpp

$ cmake -S soc-ap -B /tmp/ai_soc_v2_build/V2-P04D_QA -G Ninja -DCMAKE_BUILD_TYPE=Debug && cmake --build /tmp/ai_soc_v2_build/V2-P04D_QA --clean-first
[1/7] Building CXX object CMakeFiles/minimcproto.dir/core/forward/minimc/parser.cpp.o
[2/7] Building CXX object CMakeFiles/minimcproto.dir/core/forward/minimc/codec.cpp.o
[3/7] Linking CXX static library libminimcproto.a
[4/7] Building CXX object CMakeFiles/soc-ap.dir/core/host/main.cpp.o
[5/7] Linking CXX executable bin/soc-ap
[6/7] Building CXX object CMakeFiles/minimc-probe.dir/tests/protocol/probe.cpp.o
[7/7] Linking CXX executable bin/minimc-probe

$ python3 test_harness/static_checks/minimcproto/run_codec_cases.py --vectors test_harness/test_cases/minimcproto/vectors.json --probe /tmp/ai_soc_v2_build/V2-P04D_QA/bin/minimc-probe --case-set decode
"total_cases": 12, "passed_cases": 12, "failed_cases": 0, "status": "ok", "exit_code": 0

$ stream_sync_unimplemented_exit_code=1
$ 1/1 Test #1: host_runtime_smoke ...............   Passed    0.11 sec
```

---

## 5. 签名与最终结论

- **审查结论**：**`APPROVED`**
- **被审产物**：`soc-ap/core/forward/minimc/codec.cpp`（SHA256: `e943c3b6c991063a6a887b954ce9eef95dd2485ddf5901c9763052f97414b040`）
- **独立 QA 签名**：`QA (663fcda3-b02b-4d3a-89f6-ffc1ef283810)` @ `2026-10-26T21:02:34+08:00`
