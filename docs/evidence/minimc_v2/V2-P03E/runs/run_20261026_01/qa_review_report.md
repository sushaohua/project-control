# V2-P03E 独立 QA 审查报告（Revision 1 / `run_20261026_01`）

## 1. 审查身份与元数据

- **任务编号**：`V2-P03E`（接入探针构建目标）
- **版本 / 轮次**：Revision `1`（`run_20261026_01`）
- **被审角色 / 会话**：`INTEGRATOR`（Session ID: `1c634be7-4be2-4743-af02-dc8ada31bad3`）
- **独立 QA 审查角色 / 会话**：`QA`（Session ID: `663fcda3-b02b-4d3a-89f6-ffc1ef283810`）
- **父调度会话**：`COORD`（Session ID: `9e5411f4-acad-421e-b487-9e68b9483320`）
- **审查完成时间**：`2026-10-26T20:10:29+08:00`
- **审查结论**：**`APPROVED`**

---

## 2. 被审交付物与工作区基线核验

| 核验项 | 实测值 / 结论 | 状态 |
| --- | --- | --- |
| 被审主产物路径 | `soc-ap/CMakeLists.txt` | PASS |
| 被审主产物 SHA256 | `549df0a78f0baab9d6c3331c73cb590c3dd73a81d476c5b4aec7b8dfbb6053d8` | PASS |
| 被审主产物大小 / 行数 | `1218` bytes / `41` lines | PASS |
| `soc-ap` Base Commit (`HEAD`) | `b1bb83b422e92c8b4cf6ea24e75ee6c912448351` | PASS |
| `soc-ap` 工作区状态 (`git status --porcelain=v1`) | ` M CMakeLists.txt`（仅单文件修改，无越界写入） | PASS |
| `test_harness` Base Commit (`HEAD`) | `59d2320663dd7ef4a080272d624f831684935c34`（工作区干净） | PASS |
| 上游只读输入 `soc-ap/tests/protocol/probe.cpp` | `2ebee129e4c1d35fa394d74d8b5daf66e4480cb5b4671c89055af29be554b42c` | PASS |
| 上游只读输入 `soc-ap/core/forward/minimc/codec.h` | `733b589bf4ddb08c6108ffdc039acaab4992425bf1393a3dd94ae19f91fc0e75` | PASS |
| 上游只读输入 `soc-ap/core/forward/minimc/codec.cpp` | `5a35421cbf2e9d816db3dac7242b6878fa17de9e63a81e25facb4acb0fc3d8d3` | PASS |
| 上游只读输入 `soc-ap/core/forward/minimc/parser.h` | `a4397848a1c65b5a1e183b7a9e95283fb6908c4180b46701161de14b86575cbe` | PASS |
| 上游只读输入 `soc-ap/core/forward/minimc/parser.cpp` | `16a73b1105c78c85ca243f5a4b05d7f28875b4f29c39cb10b726c62ed2dda8d4` | PASS |

---

## 3. 任务卡验收准则逐项核查（`V2-P03E.md`）

1. **单文件写边界与上游只读边界**：
   - `git -C soc-ap status --porcelain=v1` 输出仅为 ` M CMakeLists.txt`，未触碰 `soc-ap/tests/protocol/probe.cpp`、`soc-ap/core/forward/minimc/*` 或任何其他文件。
2. **`minimc-probe` 目标定义与链接**：
   - `soc-ap/CMakeLists.txt` 第 27–31 行新增：
     ```cmake
     add_executable(minimc-probe tests/protocol/probe.cpp)
     target_link_libraries(minimc-probe PRIVATE minimcproto)
     target_compile_options(minimc-probe PRIVATE
         $<$<CXX_COMPILER_ID:GNU,Clang>:-Wall;-Wextra;-Wpedantic;-Werror>
     )
     ```
   - 继承全局 `CMAKE_RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin"`，产物输出在 `<build_dir>/bin/minimc-probe`。
   - 保持 `minimcproto` 静态库、`soc-ap` 主程序及 `host_runtime_smoke` CTest 目标完整无损。
3. **独立复跑构建与 CLI 契约验证**：
   - `cmake -S soc-ap -B /tmp/ai_soc_v2_build/V2-P03E -G Ninja -DCMAKE_BUILD_TYPE=Debug`：退出码 `0`。
   - `cmake --build /tmp/ai_soc_v2_build/V2-P03E --clean-first`：退出码 `0`，零警告编译生成 `libminimcproto.a`、`bin/soc-ap`、`bin/minimc-probe`。
   - `/tmp/ai_soc_v2_build/V2-P03E/bin/minimc-probe --help`：退出码 `0`，输出 `protocol_version: 2.0.3`、`supported_subcommands: crc, encode, decode, feed, poll, reset`、`status: ok`。
   - `/tmp/ai_soc_v2_build/V2-P03E/bin/minimc-probe --self-check`：退出码 `0`，输出 `self_check: ok`、`backend_state: stub_not_implemented`、`status: ok`。
   - `env -C /tmp/ai_soc_v2_build/V2-P03E ctest --output-on-failure -R ^host_runtime_smoke$`：退出码 `0`（`1/1 Test #1: host_runtime_smoke Passed`）。
   - `python3 project-control/tools/check_task_graph.py --check-artifact V2-P03E`：退出码 `0`，`errors: []`，`artifact_hashes["soc-ap/CMakeLists.txt"] == "549df0a78f0baab9d6c3331c73cb590c3dd73a81d476c5b4aec7b8dfbb6053d8"`。
4. **证据链完整性**：
   - 作者落盘的 `result.md` 及 `01_precheck.log`、`02_configure.log`、`03_build.log`、`04_probe_cli.log`、`05_host_regression.log` 真实完备，与 QA 独立复跑输出完全一致。

---

## 4. 独立复跑原始输出摘要

```text
$ cmake -S soc-ap -B /tmp/ai_soc_v2_build/V2-P03E -G Ninja -DCMAKE_BUILD_TYPE=Debug
-- Configuring done
-- Generating done
-- Build files have been written to: /tmp/ai_soc_v2_build/V2-P03E

$ cmake --build /tmp/ai_soc_v2_build/V2-P03E --clean-first
[1/1] Cleaning all built files...
Cleaning... 7 files.
[1/7] Building CXX object CMakeFiles/minimcproto.dir/core/forward/minimc/codec.cpp.o
[2/7] Building CXX object CMakeFiles/minimcproto.dir/core/forward/minimc/parser.cpp.o
[3/7] Linking CXX static library libminimcproto.a
[4/7] Building CXX object CMakeFiles/soc-ap.dir/core/host/main.cpp.o
[5/7] Linking CXX executable bin/soc-ap
[6/7] Building CXX object CMakeFiles/minimc-probe.dir/tests/protocol/probe.cpp.o
[7/7] Linking CXX executable bin/minimc-probe

$ /tmp/ai_soc_v2_build/V2-P03E/bin/minimc-probe --help
minimc_probe: MiniMCProto v2.0 Test Probe Adapter
protocol_version: 2.0.3
supported_subcommands: crc, encode, decode, feed, poll, reset
status: ok

$ /tmp/ai_soc_v2_build/V2-P03E/bin/minimc-probe --self-check
minimc_probe: MiniMCProto v2.0 Test Probe Adapter
protocol_version: 2.0.3
supported_subcommands: crc, encode, decode, feed, poll, reset
self_check: ok
backend_state: stub_not_implemented
status: ok

$ env -C /tmp/ai_soc_v2_build/V2-P03E ctest --output-on-failure -R ^host_runtime_smoke$
Test project /tmp/ai_soc_v2_build/V2-P03E
    Start 1: host_runtime_smoke
1/1 Test #1: host_runtime_smoke ...............   Passed    0.11 sec
100% tests passed, 0 tests failed out of 1

$ sha256sum soc-ap/CMakeLists.txt
549df0a78f0baab9d6c3331c73cb590c3dd73a81d476c5b4aec7b8dfbb6053d8  soc-ap/CMakeLists.txt
```

---

## 5. 签名与最终结论

- **审查结论**：**`APPROVED`**
- **被审产物**：`soc-ap/CMakeLists.txt`（SHA256: `549df0a78f0baab9d6c3331c73cb590c3dd73a81d476c5b4aec7b8dfbb6053d8`）
- **独立 QA 签名**：`QA (663fcda3-b02b-4d3a-89f6-ffc1ef283810)` @ `2026-10-26T20:10:29+08:00`
