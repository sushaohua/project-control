# V2-P03C 独立 QA 审查报告 (`run_20261026_01`)

## 1. 审查元数据

- **Task ID**: `V2-P03C` (`接入协议库构建目标`, Revision `1`)
- **Run ID**: `run_20261026_01`
- **被审角色与会话 (`Executor`)**: `INTEGRATOR` (`1c634be7-4be2-4743-af02-dc8ada31bad3`)
- **独立审查角色与会话 (`Reviewer`)**: `QA` (`663fcda3-b02b-4d3a-89f6-ffc1ef283810`)
- **审查策略依据**: `project-control/.agents/rules/codex_qa_review.md`
- **审查时间**: `2026-10-26T19:42:10+08:00`
- **被审交付物及版本哈希**:
  - `soc-ap/CMakeLists.txt`:
    - **SHA256**: `1915f23ae45bcb8104cfe776687f84b518ddbc2041dd7bf5f573fc4d095f2a56` (`992` bytes, `35` lines)
  - 关联执行记录与日志:
    - `project-control/docs/evidence/minimc_v2/V2-P03C/runs/run_20261026_01/result.md`
    - `project-control/docs/evidence/minimc_v2/V2-P03C/runs/run_20261026_01/01_precheck.log`
    - `project-control/docs/evidence/minimc_v2/V2-P03C/runs/run_20261026_01/02_configure.log`
    - `project-control/docs/evidence/minimc_v2/V2-P03C/runs/run_20261026_01/03_build.log`
    - `project-control/docs/evidence/minimc_v2/V2-P03C/runs/run_20261026_01/04_library.log`
    - `project-control/docs/evidence/minimc_v2/V2-P03C/runs/run_20261026_01/05_host_regression.log`
- **前置依赖版本绑定核验**:
  - `V2-P03A` (`soc-ap/core/forward/minimc/codec.cpp`): `sha256:5a35421cbf2e9d816db3dac7242b6878fa17de9e63a81e25facb4acb0fc3d8d3`
  - `V2-P03B` (`soc-ap/core/forward/minimc/parser.cpp`): `sha256:16a73b1105c78c85ca243f5a4b05d7f28875b4f29c39cb10b726c62ed2dda8d4`
  - `MiniMCProto v2.0 Rev 2.0.3`: `sha256:9f8d4f9607cb3e76cc30b9ee2f971b23c3e0d936611188466a71f4aa15f3ce54`
- **独立审查结论 (`Decision`)**: **`APPROVED`**

---

## 2. 审查核查项逐条对账

| 核查项 | 任务卡 `V2-P03C` 判据要求 | `soc-ap/CMakeLists.txt` 实测实现与构建核验 | 结论 |
| :--- | :--- | :--- | :--- |
| 新增 `minimcproto` 静态库目标 | 显式列出 `codec.cpp`/`parser.cpp` 源文件与公共 include 路径 | L10-16 定义 `add_library(minimcproto STATIC core/forward/minimc/codec.cpp core/forward/minimc/parser.cpp)` 及 `target_include_directories(minimcproto PUBLIC "${CMAKE_CURRENT_SOURCE_DIR}/core/forward/minimc")` | **PASS** |
| 编译告警配置 | 启用 `-Wall -Wextra -Wpedantic -Werror`，保留既有告警与 C++17 标准 | L5-7 保留 C++17 标准；L17-19 为 `minimcproto` 配置 `$<$<CXX_COMPILER_ID:GNU,Clang>:-Wall;-Wextra;-Wpedantic;-Werror>`；L21-25 保留 `soc-ap` 既有目标与编译配置 | **PASS** |
| 构建与 `host_runtime_smoke` 回归 | 构建 `libminimcproto.a` 零告警退出码 0；既有 `host_runtime_smoke` 非零测试且通过 | 全量 clean 构建与 `--target minimcproto` 均退出码 `0`、零告警，成功生成 `libminimcproto.a`（含 `codec.cpp.o` 与 `parser.cpp.o`）；`ctest -R ^host_runtime_smoke$` `1/1 Passed` | **PASS** |
| 负向防作弊红线 | 不把桩链接成功标成协议实现通过；不修改任何 `.c`/`.cpp`/`.h` 业务文件 | `codec.h`、`codec.cpp`、`parser.h`、`parser.cpp` SHA256 均未变化；仅注册既有 `host_runtime_smoke`，未宣称未实现的协议功能组通过 | **PASS** |

---

## 3. 独立复现验证日志

### 3.1 Precheck、CMake 配置、静态库符号与 `check_task_graph.py`

独立执行命令：
```bash
git -C soc-ap rev-parse HEAD && git -C soc-ap status --porcelain=v1 && git -C test_harness rev-parse HEAD && git -C test_harness status --porcelain=v1 && cmake -S soc-ap -B /tmp/ai_soc_v2_build/V2-P03C -G Ninja -DCMAKE_BUILD_TYPE=Debug && nm -C --defined-only /tmp/ai_soc_v2_build/V2-P03C/libminimcproto.a && sha256sum soc-ap/CMakeLists.txt soc-ap/core/forward/minimc/codec.h soc-ap/core/forward/minimc/codec.cpp soc-ap/core/forward/minimc/parser.h soc-ap/core/forward/minimc/parser.cpp && wc -c soc-ap/CMakeLists.txt && python3 project-control/tools/check_task_graph.py --check-artifact V2-P03C && date -Iseconds
```
- **退出码**: `0`
- **实际输出摘录**:
```text
60e8f567750510f5b4daf575266ca734b925ac8b
 M CMakeLists.txt
59d2320663dd7ef4a080272d624f831684935c34
-- Configuring done
-- Generating done
-- Build files have been written to: /tmp/ai_soc_v2_build/V2-P03C

codec.cpp.o:
0000000000000000 T minimc::calc_crc16(minimc::Bytes)
000000000000006b T minimc::decode_frame(minimc::Bytes, minimc::FrameView*)
0000000000000020 T minimc::encode_frame(minimc::FrameHeader const&, minimc::Bytes, minimc::MutableBytes, unsigned long*)
...
parser.cpp.o:
0000000000000000 T minimc::parser_init(minimc::StreamParser*)
0000000000000032 T minimc::parser_reset(minimc::StreamParser*)
0000000000000081 T minimc::parser_feed_byte(minimc::StreamParser*, unsigned char, unsigned int, minimc::FrameView*, bool*)
0000000000000174 T minimc::parser_poll_timeout(minimc::StreamParser*, unsigned int)
...
1915f23ae45bcb8104cfe776687f84b518ddbc2041dd7bf5f573fc4d095f2a56  soc-ap/CMakeLists.txt
733b589bf4ddb08c6108ffdc039acaab4992425bf1393a3dd94ae19f91fc0e75  soc-ap/core/forward/minimc/codec.h
5a35421cbf2e9d816db3dac7242b6878fa17de9e63a81e25facb4acb0fc3d8d3  soc-ap/core/forward/minimc/codec.cpp
a4397848a1c65b5a1e183b7a9e95283fb6908c4180b46701161de14b86575cbe  soc-ap/core/forward/minimc/parser.h
16a73b1105c78c85ca243f5a4b05d7f28875b4f29c39cb10b726c62ed2dda8d4  soc-ap/core/forward/minimc/parser.cpp
992 soc-ap/CMakeLists.txt
...
  "selected_artifacts": {
    "errors": [],
    "artifact_hashes": {
      "soc-ap/CMakeLists.txt": "1915f23ae45bcb8104cfe776687f84b518ddbc2041dd7bf5f573fc4d095f2a56"
    },
    "scope": "presence/hash only; independent content review is still required"
  },
  "exit_code": 0
```

### 3.2 Clean 全量构建、`--target minimcproto` 与 `host_runtime_smoke` CTest 独立复现

独立执行命令：
```bash
cmake --build /tmp/ai_soc_v2_build/V2-P03C --clean-first && cmake --build /tmp/ai_soc_v2_build/V2-P03C --target minimcproto && env -C /tmp/ai_soc_v2_build/V2-P03C ctest --output-on-failure -R ^host_runtime_smoke$ && date -Iseconds
```
- **退出码**: `0`
- **实际输出**:
```text
[1/1] Cleaning all built files...
Cleaning... 5 files.
[1/5] Building CXX object CMakeFiles/minimcproto.dir/core/forward/minimc/codec.cpp.o
[2/5] Building CXX object CMakeFiles/minimcproto.dir/core/forward/minimc/parser.cpp.o
[3/5] Linking CXX static library libminimcproto.a
[4/5] Building CXX object CMakeFiles/soc-ap.dir/core/host/main.cpp.o
[5/5] Linking CXX executable bin/soc-ap
ninja: no work to do.
Test project /tmp/ai_soc_v2_build/V2-P03C
    Start 1: host_runtime_smoke
1/1 Test #1: host_runtime_smoke ...............   Passed    0.11 sec

100% tests passed, 0 tests failed out of 1

Total Test time (real) =   0.11 sec
2026-10-26T19:42:10+08:00
```

---

## 4. 最终独立审查结论与签署

- **审查结论 (`Decision`)**: **`APPROVED`**
- **核准交付物版本**:
  - `soc-ap/CMakeLists.txt`: `sha256:1915f23ae45bcb8104cfe776687f84b518ddbc2041dd7bf5f573fc4d095f2a56`
- **独立审查签名**:
  - Reviewer Role: `QA`
  - Reviewer Session: `663fcda3-b02b-4d3a-89f6-ffc1ef283810`
  - Timestamp: `2026-10-26T19:42:10+08:00`
