# TWIN-22 AP端温控倍数换算与故障哨兵防御性治理交付自检报告 (Run 01)

| 属性 | 内容 |
| :--- | :--- |
| **任务卡片** | `TWIN-22` (AP端温控倍数换算与故障哨兵防御性治理) |
| **所属工作包** | `TASK-008` (实现设备状态管理器权威快照) |
| **执行角色** | `ENG-FWD / ENG-STATE` (AP 转发与状态机工程师) |
| **当前轮次** | `run_01` (全功能首轮交付与自检闭环) |
| **前置依赖** | `TWIN-18` (`project-control=579fd108ee7f12b0daf90d8a1559b61b73c62bf3; soc-ap=532caecf3a146802969a49e73081400c2b32b25e`) |
| **代码基线** | `soc-ap: 19dd461b1959c170963ebd477aa29c36ea841f63` |
| **执行状态** | **Completed (100% 测试通过，无编译警告，符合 C/C++ 编码硬性门禁)** |

---

## 1. 任务背景与问题治理概述 (Problem & Solution Summary)

在 TWIN-12 验收与端到端调查中，暴露了上位机 AP 端两项关键隐患：
1. **温度倍数猜测逻辑污染**：在 `forward_protocol.cpp` 中存在 `else if (wire.current_temp_deci_c > 1000) millic = (int32_t)wire.current_temp_deci_c * 10;` 的临时猜测逻辑。该逻辑导致当热床或喷头真实温度超过 100.0℃（1000 deci_c）时被错误除以 10 处理（例如 1200 deci_c 变为 12000 millic 即 12.0℃），严重破坏温控准确性；
2. **故障哨兵泄露与浮点数值越界**：下位机断路/故障哨兵 `0x7FFF` 与离线哨兵 `0x7FFE` 在 `device_manager_state.cpp` 中未作浮点拦截，被直接除以 1000.0 作为 `temperature_c` 序列化输出为 `2147483.6℃`。同时，收到该样本时 `quality` 被无条件标记为 `FRESH`，未能降级为 `FAULT` 或 `STALE`；
3. **集成测试历史断言偏差**：`test_device_manager.cpp` 中 `test_dds_sync_and_signal` 原断言 `g_captured_snap_sig_gen == 10U`，未考虑遥测样本注入后触发快照递增的必然行为（初值 10 -> 更新后应为 11），导致测试失败。

本轮任务（`TWIN-22`）对上述问题进行了彻底治理。

---

## 2. 详细技术改造 (Implementation Details)

### 2.1 规范化协议解包与脏逻辑清理 (`soc-ap/services/forward/forward_protocol.cpp`)
- **彻底清除猜测逻辑**：删除 `else if (wire.current_temp_deci_c > 1000) ...` 代码分支；
- **规范化哨兵与量程转换**：
  - `wire.current_temp_deci_c == (int16_t)0x7FFF` (`MINIMC_TEMP_SENTINEL_FAULT`)：置 `millic = AISOC_TEMP_MILLIC_FAULT`；
  - `wire.current_temp_deci_c == (int16_t)0x7FFE` (`MINIMC_TEMP_SENTINEL_OFFLINE`)：置 `millic = AISOC_TEMP_MILLIC_OFFLINE`；
  - 正常区间严格调用规范函数 `telemetry_deci_to_millic(wire.current_temp_deci_c, &millic)`（0.1℃ 乘以 100 得到 milli_c，例如 245 deci_c -> 24500 milli_c 即 24.5℃）；若超量程则安全降级标记为 `AISOC_TEMP_MILLIC_FAULT`。

### 2.2 权威状态机质量评估与快照格式化治理 (`soc-ap/services/device_manager/device_manager_state.cpp`)
- **数据质量动态评估 (`eval_sample_quality`)**：
  - 当样本温度为 `AISOC_TEMP_MILLIC_FAULT` 或传感器状态非 `AISOC_SENSOR_OK` 时，`quality` 强制标记为 `AISOC_QUALITY_FAULT`，严禁标记为 `FRESH`；
  - 当样本温度为 `AISOC_TEMP_MILLIC_OFFLINE` 时，`quality` 标记为 `AISOC_QUALITY_STALE`；
- **系统状态智能降级 (`update_system_status_desc`)**：
  - 当任一传感器发生故障或处于退化状态时，`system_status` 判定为 `DEGRADED`（若设备已处于故障机态则保持 `FAULT` 语义）；
- **快照序列化格式化安全防线 (`format_temp_c_val`)**：
  - 对 `AISOC_TEMP_MILLIC_FAULT` 与 `AISOC_TEMP_MILLIC_OFFLINE` 哨兵，JSON 字段 `temperature_c` 严格格式化为 `null`，100% 杜绝输出 `2147483.6` 伪造读数；
  - 正常数值保持浮点一位小数输出（如 `24.5`）。

### 2.3 测试套件修复与哨兵单测全覆盖 (`soc-ap/tests/device_manager/twin/test_device_manager.cpp`)
- **修复世代断言**：修正 `test_dds_sync_and_signal` 中 `g_captured_snap_sig_gen == 11U` 断言，端到端验证通过；
- **新增 3 组针对性单元测试**：
  - `test_unit_temp_conversion_and_json`：验证 `245 deci_c` 正确解析为 `24500 milli_c`，并在 JSON 快照中输出为 `24.5`；
  - `test_unit_fault_sentinel_defense`：验证 `0x7FFF` 故障哨兵解析为 `AISOC_TEMP_MILLIC_FAULT`，quality 正确标记为 `FAULT`，JSON 快照字段为 `null` 且绝不包含 `2147483.6`；
  - `test_unit_offline_sentinel_defense`：验证 `0x7FFE` 离线哨兵解析为 `AISOC_TEMP_MILLIC_OFFLINE`，quality 正确标记为 `STALE`，JSON 快照字段为 `null`。
- **重构治理超长测试函数**：将原超 50 行的 `setup_dev_test_env` 及 `test_rpc_device_state_and_estop` 拆解为单一职责的内部静态子函数，确保全文件所有函数行数均严格控制在 50 行以内。

---

## 3. 交付清单与 SHA-256 校验码

| 交付文件路径 | 类型与描述 | SHA-256 校验码 |
| :--- | :--- | :--- |
| `soc-ap/services/forward/forward_protocol.cpp` | 协议解析与哨兵转换逻辑治理 | `5bccbfb4d95ee025628f3299705341a6a60ff30d3b1932e1adabfa2dc009e415` |
| `soc-ap/services/device_manager/device_manager_state.cpp` | 权威状态机质量评估与快照 null 格式化 | `678892d4da5a81fa7bf03fd2781d184885f33cc25d89d545f1298299b12e965b` |
| `soc-ap/tests/device_manager/twin/test_device_manager.cpp` | 世代修复、哨兵与倍数单元测试集 | `b2be13ba63431f9935878b72e1cbdcf389dd56b95c934b69e5c4b08e1acc7bfc` |

---

## 4. 编码规范硬性门禁核查 (Coding Standards Gatekeeper)

严格依照 `project-control/.agents/rules/c_cpp_coding_standard.md` 进行审查：

| 门禁规则 | 要求 | 审查结果 | 备注 |
| :--- | :--- | :---: | :--- |
| **函数规模** | 严禁编写超 50 行的自研非结构体函数 | **100% 达标** | 所有新增及修改函数均 $\le 41$ 行 |
| **入参个数** | 函数入参严禁超过 4 个 | **100% 达标** | 所有自研函数参数 $\le 4$ 个 |
| **防御性空指针检查** | 函数入口第一行显式空指针校验 | **100% 达标** | 指针入参均在首行校验并返回错误码 |
| **零动态堆分配** | 严禁 malloc/free/new，禁用堆容器 | **100% 达标** | 纯静态数组与栈对象操作 |
| **指针运算显式化** | 严禁 `*dst++ = *src++`，禁止三级指针 | **100% 达标** | 扁平数组与指针独立操作 |
| **嵌套深度** | 严禁超过 3 层嵌套，卫语句优先 | **100% 达标** | 条件判断均通过 guard clause 提前返回 |

---

## 5. 本地验证证据 (Verification Evidence)

### 5.1 构建与测试执行
执行目录：`soc-ap/tests/device_manager/twin`  
执行命令：
```bash
cmake -B build -S . && cmake --build build && ./build/test_device_manager
```

### 5.2 终端执行输出
```
-- The CXX compiler identification is GNU 9.4.0
-- Detecting CXX compiler ABI info
-- Detecting CXX compiler ABI info - done
-- Check for working CXX compiler: /usr/bin/c++ - skipped
-- Detecting CXX compile features
-- Detecting CXX compile features - done
-- Configuring done (0.4s)
-- Generating done (0.0s)
-- Build files have been written to: /home/sushaohua/workspace/ai_soc_project/soc-ap/tests/device_manager/twin/build
[  6%] Building CXX object CMakeFiles/test_device_manager.dir/test_device_manager.cpp.o
[ 13%] Building CXX object CMakeFiles/test_device_manager.dir/home/sushaohua/workspace/ai_soc_project/soc-ap/services/device_manager/device_manager_state.cpp.o
[ 20%] Building CXX object CMakeFiles/test_device_manager.dir/home/sushaohua/workspace/ai_soc_project/soc-ap/services/device_manager/device_manager_dbus.cpp.o
[ 26%] Building CXX object CMakeFiles/test_device_manager.dir/home/sushaohua/workspace/ai_soc_project/soc-ap/services/device_manager/device_manager_service.cpp.o
[ 33%] Building CXX object CMakeFiles/test_device_manager.dir/home/sushaohua/workspace/ai_soc_project/soc-ap/middleware/dbus/src/aisoc_dbus_msg.cpp.o
[ 40%] Building CXX object CMakeFiles/test_device_manager.dir/home/sushaohua/workspace/ai_soc_project/soc-ap/middleware/dbus/src/aisoc_dbus_core.cpp.o
[ 46%] Building CXX object CMakeFiles/test_device_manager.dir/home/sushaohua/workspace/ai_soc_project/soc-ap/middleware/dbus/src/aisoc_dbus_client.cpp.o
[ 53%] Building CXX object CMakeFiles/test_device_manager.dir/home/sushaohua/workspace/ai_soc_project/soc-ap/middleware/dbus/src/aisoc_dbus_server.cpp.o
[ 60%] Building CXX object CMakeFiles/test_device_manager.dir/home/sushaohua/workspace/ai_soc_project/soc-ap/middleware/dds/src/aisoc_dds_types.cpp.o
[ 66%] Building CXX object CMakeFiles/test_device_manager.dir/home/sushaohua/workspace/ai_soc_project/soc-ap/middleware/dds/src/aisoc_dds_common.cpp.o
[ 73%] Building CXX object CMakeFiles/test_device_manager.dir/home/sushaohua/workspace/ai_soc_project/soc-ap/middleware/dds/src/aisoc_dds_participant.cpp.o
[ 80%] Building CXX object CMakeFiles/test_device_manager.dir/home/sushaohua/workspace/ai_soc_project/soc-ap/middleware/dds/src/aisoc_dds_pub.cpp.o
[ 86%] Building CXX object CMakeFiles/test_device_manager.dir/home/sushaohua/workspace/ai_soc_project/soc-ap/middleware/dds/src/aisoc_dds_sub.cpp.o
[ 93%] Building CXX object CMakeFiles/test_device_manager.dir/home/sushaohua/workspace/ai_soc_project/soc-ap/middleware/dds/src/aisoc_dds.cpp.o
[100%] Linking CXX executable test_device_manager
[100%] Built target test_device_manager
========================================================================
TWIN-08 Device Manager Verification & Integration Test Suite
========================================================================
[RUN ] test_unit_state_init
[PASS] test_unit_state_init
[RUN ] test_unit_state_sample_update
[PASS] test_unit_state_sample_update
[RUN ] test_unit_state_admission
[PASS] test_unit_state_admission
[RUN ] test_unit_state_json
[PASS] test_unit_state_json
[RUN ] test_unit_temp_conversion_and_json
[PASS] test_unit_temp_conversion_and_json
[RUN ] test_unit_fault_sentinel_defense
[PASS] test_unit_fault_sentinel_defense
[RUN ] test_unit_offline_sentinel_defense
[PASS] test_unit_offline_sentinel_defense
[RUN ] [&]() { return test_rpc_get_snapshot(&env.cli_conn); }
[PASS] [&]() { return test_rpc_get_snapshot(&env.cli_conn); }
[RUN ] [&]() { return test_dds_sync_and_signal(&env); }
[DEVICE_MGR DEBUG] DDS RX: node=1, temp=62000 millic (62.0 C) -> Snapshot GEN=11 (DEGRADED)
[PASS] [&]() { return test_dds_sync_and_signal(&env); }
[RUN ] [&]() { return test_rpc_request_sample(&env.cli_conn); }
[PASS] [&]() { return test_rpc_request_sample(&env.cli_conn); }
[RUN ] [&]() { return test_rpc_device_state_and_estop(&env.cli_conn); }
[PASS] [&]() { return test_rpc_device_state_and_estop(&env.cli_conn); }
========================================================================
Total: Passed=11, Failed=0
========================================================================
```
测试退出码：`0`（11 项单元测试与集成测试 100% PASS）。
构建产物清理：测试完成后已彻底清理 `soc-ap/tests/device_manager/twin/build` 目录，工作区无残留中间构建产物。

---

## 6. 自检结论

TWIN-22 微任务卡所要求的协议解包脏逻辑清理、数据质量评估治理、快照序列化哨兵防御（输出 `null` 杜绝 `2147483.6`）、测试修复与覆盖用例增加均已高标准完成，代码严格满足项目 C/C++ 硬性编码门禁，全套测试 100% 通过，具备交付条件。
