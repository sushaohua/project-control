# V2-P04A 独立 QA 审查报告（Revision 1 / `run_20261026_01`）

## 1. 审查身份与元数据

- **任务编号**：`V2-P04A`（实现CRC计算）
- **版本 / 轮次**：Revision `1`（`run_20261026_01`）
- **被审角色 / 会话**：`ENG-FWD`（Session ID: `1c634be7-4be2-4743-af02-dc8ada31bad3`）
- **独立 QA 审查角色 / 会话**：`QA`（Session ID: `663fcda3-b02b-4d3a-89f6-ffc1ef283810`）
- **父调度会话**：`COORD`（Session ID: `9e5411f4-acad-421e-b487-9e68b9483320`）
- **审查完成时间**：`2026-10-26T20:37:35+08:00`
- **审查结论**：**`APPROVED`**

---

## 2. 被审交付物与工作区基线核验

| 核验项 | 实测值 / 结论 | 状态 |
| --- | --- | --- |
| 被审主产物路径 | `soc-ap/core/forward/minimc/codec.cpp` | PASS |
| 被审主产物 SHA256 | `7cb49c0a6720f40055e9e24eaf9b30a5d8419ddfd6f89982c4d83bbef0218395` | PASS |
| 被审主产物大小 / 行数 | `1468` bytes / `50` lines | PASS |
| `soc-ap` Base Commit (`HEAD`) | `25d8f99faf338b2d324a9793b33deaa423a57f9e` | PASS |
| `soc-ap` 工作区状态 (`git status --porcelain=v1`) | ` M core/forward/minimc/codec.cpp`（严格单文件改动） | PASS |
| `test_harness` Base Commit (`HEAD`) | `5a2ebe49e26ffb76a55ab74de652142ce9961de7`（工作区干净） | PASS |
| 只读头文件 `soc-ap/core/forward/minimc/codec.h` | `733b589bf4ddb08c6108ffdc039acaab4992425bf1393a3dd94ae19f91fc0e75` | PASS |
| 只读构建配置 `soc-ap/CMakeLists.txt` | `549df0a78f0baab9d6c3331c73cb590c3dd73a81d476c5b4aec7b8dfbb6053d8` | PASS |
| 只读探针源码 `soc-ap/tests/protocol/probe.cpp` | `2ebee129e4c1d35fa394d74d8b5daf66e4480cb5b4671c89055af29be554b42c` | PASS |
| 只读运行器 `test_harness/static_checks/minimcproto/run_codec_cases.py` | `e1384164c92078fe8dc71017d5128c0b0e610deb527f53d182efa6c5257f9cdf` | PASS |
| 只读样例集 `test_harness/test_cases/minimcproto/vectors.json` | `6d46bd05a4133e678611abe2ab1cb88db190c394f23151900009c0c077c8d995` | PASS |

---

## 3. 任务卡验收准则与代码逐项核查（`V2-P04A.md`）

1. **算法与覆盖域一致性**：
   - `calc_crc16(Bytes data)` 严格按照 `CRC-16/CCITT-FALSE`（`Poly=0x1021`, `Init=0xFFFF`, `RefIn=false`, `RefOut=false`, `XorOut=0x0000`）实现逐字节、逐比特移位异或。
   - 空指针及空长度防御：`if (data.data == nullptr || data.size == 0) { return 0xFFFF; }`，绝不发生空指针解引用或越界访问。
   - 全部位运算均带显式 `static_cast<uint16_t>`，在 `-Wall -Wextra -Wpedantic -Werror` 下零告警通过。
2. **范围边界与未实现函数桩隔离**：
   - `encode_frame` 与 `decode_frame` 严格保持 `Status::ERR_NOT_IMPLEMENTED` 桩状态，未提前越界实现 `V2-P04B`/`V2-P04C`/`V2-P04D` 逻辑。
   - 针对尚未实现的 `encode` 分组独立执行 `run_codec_cases.py --case-set encode`，实测退出码为 `1`（精准拦截未实现桩，无伪造通过）。
3. **独立复跑构建与 `crc` 用例集全量验证**：
   - `cmake -S soc-ap -B /tmp/ai_soc_v2_build/V2-P04A_QA -G Ninja -DCMAKE_BUILD_TYPE=Debug`：退出码 `0`。
   - `cmake --build /tmp/ai_soc_v2_build/V2-P04A_QA --clean-first`：退出码 `0`，零警告编译生成 `libminimcproto.a`、`bin/soc-ap`、`bin/minimc-probe`。
   - `python3 test_harness/static_checks/minimcproto/run_codec_cases.py --vectors test_harness/test_cases/minimcproto/vectors.json --probe /tmp/ai_soc_v2_build/V2-P04A_QA/bin/minimc-probe --case-set crc`：退出码 `0`，`9/9` 用例全部通过：
     - `CRC-001`（`"123456789"` -> `0x29B1` / `B129`）：PASS
     - `CRC-002`（空输入 `""` -> `0xFFFF` / `FFFF`）：PASS
     - `CRC-003`（`V01` 12B -> `0x1EF9` / `F91E`）：PASS
     - `CRC-004`（`V02_INBOUND` 16B -> `0xB066` / `66B0`）：PASS
     - `CRC-005`（`V02_OUTBOUND` 16B -> `0x3073` / `7330`）：PASS
     - `CRC-006`（`V03` 23B -> `0xDAA0` / `A0DA`）：PASS
     - `CRC-007`（`V04` 12B -> `0xC13D` / `3DC1`）：PASS
     - `CRC-008`（合法帧 `CRC == 0x0000` -> `0x0000` / `0000`）：PASS
     - `CRC-009`（`nullptr` 且 `len=4` 拒绝 -> `status: error, error_code: invalid_argument`）：PASS
   - `env -C /tmp/ai_soc_v2_build/V2-P04A_QA ctest --output-on-failure -R ^host_runtime_smoke$`：退出码 `0`（`1/1 Passed`）。
   - `python3 project-control/tools/check_task_graph.py --check-artifact V2-P04A`：退出码 `0`，`errors: []`。

---

## 4. 独立复跑原始输出摘要

```text
$ git -C soc-ap rev-parse HEAD && git -C soc-ap status --porcelain=v1
25d8f99faf338b2d324a9793b33deaa423a57f9e
 M core/forward/minimc/codec.cpp

$ sha256sum soc-ap/core/forward/minimc/codec.cpp
7cb49c0a6720f40055e9e24eaf9b30a5d8419ddfd6f89982c4d83bbef0218395  soc-ap/core/forward/minimc/codec.cpp

$ cmake -S soc-ap -B /tmp/ai_soc_v2_build/V2-P04A_QA -G Ninja -DCMAKE_BUILD_TYPE=Debug && cmake --build /tmp/ai_soc_v2_build/V2-P04A_QA --clean-first
[1/7] Building CXX object CMakeFiles/minimcproto.dir/core/forward/minimc/parser.cpp.o
[2/7] Building CXX object CMakeFiles/minimcproto.dir/core/forward/minimc/codec.cpp.o
[3/7] Linking CXX static library libminimcproto.a
[4/7] Building CXX object CMakeFiles/soc-ap.dir/core/host/main.cpp.o
[5/7] Linking CXX executable bin/soc-ap
[6/7] Building CXX object CMakeFiles/minimc-probe.dir/tests/protocol/probe.cpp.o
[7/7] Linking CXX executable bin/minimc-probe

$ python3 test_harness/static_checks/minimcproto/run_codec_cases.py --vectors test_harness/test_cases/minimcproto/vectors.json --probe /tmp/ai_soc_v2_build/V2-P04A_QA/bin/minimc-probe --case-set crc
"total_cases": 9, "passed_cases": 9, "failed_cases": 0, "status": "ok", "exit_code": 0

$ encode_unimplemented_exit_code=1
$ 1/1 Test #1: host_runtime_smoke ...............   Passed    0.11 sec
```

---

## 5. 签名与最终结论

- **审查结论**：**`APPROVED`**
- **被审产物**：`soc-ap/core/forward/minimc/codec.cpp`（SHA256: `7cb49c0a6720f40055e9e24eaf9b30a5d8419ddfd6f89982c4d83bbef0218395`）
- **独立 QA 签名**：`QA (663fcda3-b02b-4d3a-89f6-ffc1ef283810)` @ `2026-10-26T20:37:35+08:00`
