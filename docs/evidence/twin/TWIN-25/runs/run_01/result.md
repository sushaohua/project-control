# TWIN-25 AP端0x18调平网格解析与设备状态拓扑呈现交付自检报告 (Run 01)

| 属性 | 内容 |
| :--- | :--- |
| **任务卡片** | `TWIN-25` (AP端0x18调平网格解析与设备状态拓扑呈现) |
| **所属工作包** | `TASK-007` (实现 forward 协议与传输), `TASK-008` (实现整机状态和统一指令准入) |
| **执行角色** | `ENG-FWD` (Forward & Device Manager Engineer) |
| **当前轮次** | `run_01` (0x18调平网格解析与设备状态拓扑呈现闭环落地) |
| **前置依赖** | `TWIN-24` (`mcu-p3=9b017f186665c2c9226146cc0fdc34af3ad5242b`) |
| **候选 Commit** | `soc-ap: f2596517c8e7a53da6ff9623d948ec5e70bf6770` (`feat(twin): implement 0x18 bed leveling grid parsing and state topology presentation (TWIN-25)`) |
| **作者会话 ID** | `session-eng-fwd-twin-25` |
| **执行状态** | **Completed (AP端 0x18 52B 5×5 双线性网格编解码校验、设备状态拓扑呈现与全量单测 100% 验证通过)** |

---

## 1. 契约复核与核心实现 (Contract Alignment & Implementation)

依据首版调平特性（`MOT-002`）、用户指令 **U-D04**（“固件存量为 5×5 双线性网格，PM 目标要求 7×7 网格，未达成技术裁决，采用固件存量；当前开发功能以固件存量为主要参考”）以及前序任务 `TWIN-24` 导出的 0x18 协议规格，`ENG-FWD` 在上位机 `soc-ap` 侧完成了对下位机 5×5 双线性调平网格的消费与拓扑呈现闭环：

### 1.1 Wire 协议扩展 (`forward_protocol.h` / `forward_protocol.cpp`)
1. **0x18 常量与操作码定义**：
   - `MINIMC_CMD_LEVEL_GRID_QUERY = 0x18U`；
   - `MINIMC_LEVEL_GRID_POINTS_X = 5U`；
   - `MINIMC_LEVEL_GRID_POINTS_Y = 5U`；
   - `MINIMC_LEVEL_GRID_POINTS_NUM = 25U`；
   - `MINIMC_LEVEL_GRID_PAYLOAD_SIZE = 52U`；
2. **Wire 载荷排布与内存布局**：
   - 增加单字节紧凑对齐结构体 `minimc_level_grid_wire_payload_t`（52 字节：`grid_points_x: uint8_t`, `grid_points_y: uint8_t`, `z_offset_um: int16_t[25]`），编译期通过 `static_assert(sizeof(...) == 52)` 强校验；
   - 增加模型结构体 `dev_leveling_grid_t`（`points_x`, `points_y`, `z_offset_um[25]`, `updated_ns`, `valid`）；
3. **协议构建与校验函数**：
   - `fwd_proto_build_grid_query_frame(uint16_t seq, fwd_frame_buf_t* out_buf)`：构建目标为 MC（`MINIMC_DEV_MC = 0x02`）的 0x18 查询帧，头部 12B + 0B 载荷 + 2B CRC；
   - `fwd_proto_validate_grid_response(const minimc::FrameView* frame, uint16_t expected_seq, bool* out_valid)`：严格防御性校验响应标志位（`MINIMC_FLAG_IS_RESPONSE`）、源节点（`src_id == MINIMC_DEV_MC`）、报文序号（`seq == expected_seq`）、指令编号（`cmd_id == 0x18`）及载荷长度（`payload.size == 52`）；
   - `fwd_proto_parse_raw_grid(const uint8_t* payload, size_t len, dev_leveling_grid_t* out_grid)`：解析 52B 原始网格载荷并填入微米整型拓扑模型，注入主机单调纳秒时间戳。

### 1.2 设备状态机与拓扑呈现 (`device_manager_state.h` / `device_manager_state.cpp`)
1. **网格模型绑定与维护**：
   - 采用定长绑定位表 `s_grid_bindings` 关联设备管理器状态实例，零动态堆内存分配；
   - 在 `dev_state_init_snapshot()` 中初始化网格模型，默认状态 `valid = false`, `points_x = 5`, `points_y = 5`, `updated_ns = 0`；
2. **状态更新与获取接口**：
   - `dev_state_update_leveling_grid(device_manager_state_t* state, const dev_leveling_grid_t* grid)`：校验入参边界（`points_x == 5 && points_y == 5`）后原子更新状态；
   - `dev_state_get_leveling_grid(const device_manager_state_t* state, dev_leveling_grid_t* out_grid)`：导出当前网格模型快照；
3. **JSON 序列化拓扑输出**：
   - `dev_state_get_leveling_grid_json(const device_manager_state_t* state, char* out_json, size_t cap)`：格式化输出符合 Web HMI 热力图与 D-Bus `GetLevelingGrid` 规范的紧凑 JSON 报文：
     `{"points_x":5,"points_y":5,"z_offset_um":[-180,-165,...],"valid":true,"updated_ns":987654321}`；
   - 内部拆解出辅助格式化函数 `format_grid_array_json`（<= 37 行），严禁压缩指针运算。

### 1.3 测试工程与单测用例扩展 (`CMakeLists.txt` & `test_device_manager.cpp`)
1. **构建配置更新**：
   - 在 `soc-ap/tests/device_manager/twin/CMakeLists.txt` 中引入 `${SOC_AP_ROOT}/services/forward`、`${SOC_AP_ROOT}/core/forward/minimc`、`${SOC_AP_ROOT}/core/forward/transport` 头文件目录及 `forward_protocol.cpp`、`codec.cpp` 编译源文件；
2. **正反例单测扩充**：
   - `test_unit_grid_proto_build_query`：0x18 查询帧正向组装与空指针校验防御；
   - `test_unit_grid_proto_validate_positive_and_negative`：正向校验，及反向非法序号、源节点不符、非响应帧、短载荷（51B）、长载荷（53B）丢弃防御；
   - `test_unit_grid_proto_parse_raw`：52B 载荷微米数值正向解析，及短载荷、非法维度反向防御；
   - `test_unit_state_leveling_grid_and_json`：初态默认 invalid、网格更新、JSON 拓扑输出及模型快照读取校验；
   - `test_unit_state_grid_defense`：更新与序列化空指针防御、非法维度防御、缓冲区容量不足防御。

---

## 2. 交付文件清单与 SHA-256 校验码

| 交付文件路径 | 类型与描述 | SHA-256 校验码 |
| :--- | :--- | :--- |
| `soc-ap/services/forward/forward_protocol.h` | 协议头文件，0x18 宏、载荷定义与接口声明 | `294106db669b0cad836035f14ed936a9330cc1d5c3137a6cda12eafad60d4bd9` |
| `soc-ap/services/forward/forward_protocol.cpp` | 协议实现，0x18 帧构建、响应校验与载荷解析 | `1b9553c59ca32970f402ab9962bc36b2068508c1ef6af48764680d554404e1fe` |
| `soc-ap/services/device_manager/device_manager_state.h` | 状态机头文件，网格结构体与状态管理接口声明 | `efbf59358aca74d2cfa9e3c6d1c42989365f43efc584dff0dee5d2e41d43398d` |
| `soc-ap/services/device_manager/device_manager_state.cpp` | 状态机实现，网格模型维护与 JSON 序列化拓扑 | `29c0656ea1591442c12af550828d936bc822510e053eb82cbc6516e17923560c` |
| `soc-ap/tests/device_manager/twin/CMakeLists.txt` | 构建脚本，引入 forward 协议库与 minimc 编解码器 | `f3c29c80b0433662d8db74a593ad55f0ec220de9b7cf4194b2e476d4803da6db` |
| `soc-ap/tests/device_manager/twin/test_device_manager.cpp` | 单元与集成测试套件，正反例与边界防御用例 | `73c8966fe3bea24fa5ca84136a41d002096b8ab50c8c86bb9f0141f3d13a3126` |

---

## 3. 编码硬门禁符合性声明 (Coding Standards Compliance)

本任务实现完全遵守 `project-control/.agents/rules/c_cpp_coding_standard.md`：
1. **函数规模硬性门禁（$\le 50$ 行）**：
   - `forward_protocol.cpp` 新增函数：
     - `fwd_proto_build_grid_query_frame()`: 28 行
     - `fwd_proto_validate_grid_response()`: 20 行
     - `fwd_proto_parse_raw_grid()`: 27 行
   - `device_manager_state.cpp` 新增/更新函数：
     - `find_or_create_grid_binding()`: 29 行
     - `find_grid_binding()`: 12 行
     - `dev_state_init_snapshot()`: 28 行
     - `dev_state_update_leveling_grid()`: 19 行
     - `dev_state_get_leveling_grid()`: 18 行
     - `format_grid_array_json()`: 37 行
     - `dev_state_get_leveling_grid_json()`: 47 行
   - `test_device_manager.cpp` 新增单测辅助与用例函数：
     - `init_mock_grid_frame()`: 18 行
     - `test_unit_grid_proto_build_query()`: 23 行
     - `test_unit_grid_proto_validate_positive_and_negative()`: 39 行
     - `test_unit_grid_proto_parse_raw()`: 30 行
     - `test_unit_state_leveling_grid_and_json()`: 42 行
     - `test_unit_state_grid_defense()`: 27 行
   - **结论**：所有自研函数均严格保持单一职责且 $\le 50$ 行，**100% 达标**。
2. **入参个数硬性门禁（$\le 4$ 个）**：
   - 所有自研新增函数参数均在 2~4 个以内（超出配置均通过结构体指针如 `mock_grid_cfg_t*` 传入），**100% 达标**。
3. **指针与内存安全**：
   - 零动态堆内存分配（严禁 `malloc` / `free` / `new` / `delete` 及动态 STL 容器）；
   - 指针显式化，严禁压缩指针运算黑魔法（无 `*dst++ = *src++`，统一采用显式下标递增）；
   - 指针解引用与取地址操作独立成行，无多重指针（无 `***`）。
4. **控制流与接口防御**：
   - 对外公开函数入口第一行统一执行 Guard Clause 空指针与边界检查；
   - 状态返回值统一度量（`aisoc_fwd_status_t`, `aisoc_dev_status_t`）；
   - 函数嵌套深度 $\le 2$ 层，无嵌套三元运算符。
5. **编译期静态断言**：
   - 采用 `static_assert(sizeof(minimc_level_grid_wire_payload_t) == 52)` 强校验 52B 紧凑载荷尺寸。

---

## 4. 验证与测试执行记录 (Verification Results)

### 4.1 任务规划图校验 (check_task_graph.py)
```bash
PYTHONDONTWRITEBYTECODE=1 python3 project-control/tools/check_task_graph.py --workspace .
```
**输出**：Exit code 0, 115 个规范任务无循环依赖、无配置错误。

### 4.2 编译与单测全集执行 (test_device_manager)
```bash
cmake -B soc-ap/tests/device_manager/twin/build -S soc-ap/tests/device_manager/twin && \
cmake --build soc-ap/tests/device_manager/twin/build && \
./soc-ap/tests/device_manager/twin/build/test_device_manager
```

**编译输出**：
`-Wall -Wextra -Wpedantic` 零 Warning，零 Error。

**运行输出**：
```text
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
[RUN ] test_unit_grid_proto_build_query
[PASS] test_unit_grid_proto_build_query
[RUN ] test_unit_grid_proto_validate_positive_and_negative
[PASS] test_unit_grid_proto_validate_positive_and_negative
[RUN ] test_unit_grid_proto_parse_raw
[PASS] test_unit_grid_proto_parse_raw
[RUN ] test_unit_state_leveling_grid_and_json
[PASS] test_unit_state_leveling_grid_and_json
[RUN ] test_unit_state_grid_defense
[PASS] test_unit_state_grid_defense
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
Total: Passed=16, Failed=0
========================================================================
```

**结论**：全部 16 个测试套件 100% 通过（0 failed）。
