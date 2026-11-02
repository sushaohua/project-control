---
task_id: TEMP-04
run_id: run_01
author_role: ENG-FWD
author_session: fwd-session-20261028
timestamp: '2026-10-28T20:33:00+08:00'
task_revision: 1
status: completed
deliverables:
- path: soc-ap/CMakeLists.txt
  sha256: 22b6f4f102e4e26da29bbd1a67cf058309e1706da5f3049ea45666133e308742
- path: soc-ap/core/host/main.cpp
  sha256: 9c8ef1a3e14527d11bc9ef1a2840e89e0a86cc62a37503ab562d296957a02e7a
- path: soc-ap/core/host/query.cpp
  sha256: 29eafce7b8d71ce8ae5c7ea093f56fac1a0165580b5ae88a0c7f704ee4c2a652
- path: soc-ap/core/host/query.h
  sha256: 764ec8ef5d539d4008439c8b19770f2145f3b1064a8ff0206de81c2f4bc03aee
- path: soc-ap/core/forward/minimc/codec.cpp
  sha256: e5ff9ea0736f727978a671be718f890a9a4dce526bfe886e75da9904bcd7ae33
- path: soc-ap/core/forward/minimc/codec.h
  sha256: c51e7d2a1fa0d4deed798f1536f1ea7f72e27696b7a4971fc9c2f9aab7433698
- path: soc-ap/tests/protocol/test_telemetry.cpp
  sha256: 4e8a03e0fb55263840873ef788b4e7070ac058f0678d8f378c3e87a7a33e0659
- path: soc-ap/build/host/bin/soc-ap
  sha256: 5a1e31eb34ea6b2d36c6cac2abe6c10d0da37daeb5474ce8236a664f95d22776
- path: soc-ap/build/host/bin/test_telemetry
  sha256: c6e6d5bb7692f31166706ff5db35590c2276bced30b3ef9b1f3ebc93adf94f2b
verification:
  commands:
  - id: ap_build
    cwd: /home/sushaohua/workspace/ai_soc_project/soc-ap
    command: cmake --build build/host -j4
    exit_code: 0
    result: PASS
  - id: ap_test
    cwd: /home/sushaohua/workspace/ai_soc_project/soc-ap
    command: ./build/host/bin/test_telemetry
    exit_code: 0
    result: PASS
  - id: ctest_suite
    cwd: /home/sushaohua/workspace/ai_soc_project/soc-ap/build/host
    command: ctest --output-on-failure
    exit_code: 0
    result: PASS
  - id: check_graph
    cwd: /home/sushaohua/workspace/ai_soc_project
    command: python3 project-control/tools/check_task_graph.py
    exit_code: 0
    result: PASS
---

# TEMP-04 AP 宿主端温度查询与 CLI 呈现执行报告

## 1. 任务完成摘要

ENG-FWD 已完成微任务 `TEMP-04`（AP 宿主端温度查询与 CLI 呈现）的全部研发与单测工作：
1. **CLI 查询参数扩展**：
   - 扩展支持 `--cmd temp`（同时兼容 `temp`, `get_temp`, `temperature`）；
   - 扩展支持 `--target mc|th`（发往 `0x02` MC 热床或 `0x03` TH 喷头）；
   - 扩展支持 `--json` 结构化输出。
2. **请求帧构造与分发**：
   - 在 `query_build_request` 中实现温度查询帧构造：`cmd_id = 0x14` (`MINIMC_CMD_GET_TEMP`), `payload_len = 0`, `flags = 0x05` (`MINIMC_FLAG_WANTS_ACK | MINIMC_FLAG_PROTO_VERSION_V2`)；
   - 默认序列号分配：MC 为 4，TH 为 5，支持 `--seq` 自定义覆盖。
3. **16 字节温度载荷编解码与校验**：
   - 在 `codec.cpp` / `codec.h` 中实现 `decode_temp_report_payload` 与 `encode_temp_report_payload`，严格按显式小端字节偏移安全解包，杜绝非对齐访问；
   - 摄氏度浮点转换：`current_temp_centi_c / 100.0f`；
   - 传感器状态码诊断：支持 `0x00` (OK)、`0x01` (OPEN_CIRCUIT)、`0x02` (SHORT_CIRCUIT)、`0x03` (TIMEOUT)。当状态码非 0 时，返回 `EXIT_CODE_SENSOR_ERROR` (5) 并输出错误信息；
   - 强电安全占空比锁死校验：严格校验 `heater_duty_percent == 0`，若大于 0 立即判定为 `EXIT_CODE_SAFETY_FAULT` (6) 并输出安全违规告警。
4. **独立单元测试套件**：
   - 在 `soc-ap/tests/protocol/test_telemetry.cpp` 中编写 12 个单元测试用例，覆盖结构体布局、正常正负温解析、开路/短路/超时诊断、零占空比硬件安全守卫校验、入参安全边界防御、编码/解码往返回环、请求帧构造以及全帧校验；
   - 在 `soc-ap/CMakeLists.txt` 中注册 `test_telemetry` 可执行目标与 CTest 测试项。
5. **编码规范硬门禁 100% 遵从**：
   - 所有自研新增/修改函数严格控制在 50 行以内；
   - 所有函数入参控制在 4 个以内；
   - 函数首行均设防御性空指针校验（Guard Clause）；
   - 零动态堆内存分配；扁平控制流，无嵌套三元运算符。

---

## 2. 编译与单元测试验证记录

### 2.1 构建命令输出 (`cmake --build build/host -j4`)

```text
[0/1] Re-running CMake...
-- MiniMC QA test suite not enabled (MINIMC_QA_ROOT not set)
-- Configuring done
-- Generating done
-- Build files have been written to: /home/sushaohua/workspace/ai_soc_project/soc-ap/build/host
[1/12] Building CXX object CMakeFiles/test_telemetry.dir/tests/protocol/test_telemetry.cpp.o
[2/12] Building CXX object CMakeFiles/soc-ap.dir/core/host/main.cpp.o
[3/12] Building CXX object CMakeFiles/minimcproto.dir/core/forward/minimc/codec.cpp.o
[4/12] Building CXX object CMakeFiles/minimcproto.dir/core/forward/minimc/parser.cpp.o
[5/12] Building CXX object CMakeFiles/test_telemetry.dir/core/host/query.cpp.o
[6/12] Building CXX object CMakeFiles/minimcproto.dir/core/forward/transport/serial_posix.cpp.o
[7/12] Linking CXX static library libminimcproto.a
[8/12] Linking CXX executable bin/test_telemetry
[9/12] Building CXX object CMakeFiles/soc-ap.dir/core/host/query.cpp.o
[10/12] Linking CXX executable bin/soc-ap
[11/12] Building CXX object CMakeFiles/minimc-probe.dir/tests/protocol/probe.cpp.o
[12/12] Linking CXX executable bin/minimc-probe
```

### 2.2 单元测试输出 (`./build/host/bin/test_telemetry`)

```text
Running 12 telemetry unit tests...
  [PASS] payload_size
  [PASS] decode_normal
  [PASS] decode_negative
  [PASS] decode_open_circuit
  [PASS] decode_short_circuit
  [PASS] decode_timeout
  [PASS] decode_bounds_and_null
  [PASS] encode_and_roundtrip
  [PASS] build_request_mc_and_th
  [PASS] validate_frame_normal
  [PASS] validate_frame_sensor_errors
  [PASS] validate_frame_duty_violation

Telemetry test summary: 12 / 12 passed
All telemetry unit tests PASSED (100%).
```

### 2.3 CTest 自动化测试套件输出 (`ctest --output-on-failure`)

```text
Test project /home/sushaohua/workspace/ai_soc_project/soc-ap/build/host
    Start 1: test_telemetry
1/3 Test #1: test_telemetry ...................   Passed    0.00 sec
    Start 2: host_runtime_smoke
2/3 Test #2: host_runtime_smoke ...............   Passed    0.11 sec
    Start 3: cascade_query_cases
3/3 Test #3: cascade_query_cases ..............   Passed    2.32 sec

100% tests passed, 0 tests failed out of 3

Total Test time (real) =   2.44 sec
```

### 2.4 任务图依赖校验 (`python3 project-control/tools/check_task_graph.py`)

- 全图任务与依赖闭环校验通过，退出码为 0，无任何孤岛或循环依赖错误。
