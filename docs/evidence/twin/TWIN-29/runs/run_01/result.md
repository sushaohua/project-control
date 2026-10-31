# TWIN-29 AP端双MCU真实固件版本查询链路与时序衰退状态机实现交付自检报告 (Run 01)

| 属性 | 内容 |
| :--- | :--- |
| **任务卡片** | `TWIN-29` (AP端双MCU真实固件版本查询链路与时序衰退状态机实现) |
| **所属工作包** | `TASK-007` (实现 forward 协议与传输), `TASK-008` (实现整机状态和统一指令准入) |
| **执行角色** | `ENG-FWD` (Forward & Device Manager Engineer) |
| **当前轮次** | `run_01` (双MCU真实固件版本查询、校验、四态衰退状态机与D-Bus接口闭环落地) |
| **前置依赖** | `TWIN-25` (`soc-ap: f2596517c8e7a53da6ff9623d948ec5e70bf6770`) |
| **候选 Commit** | `soc-ap: 594ffab12902ac5b38a6f1a6dd869da0942c8dbb` (`feat(twin): implement dual MCU firmware version telemetry and freshness decay state machine (TWIN-29)`) |
| **作者会话 ID** | `session-eng-fwd-twin-29` |
| **执行状态** | **Completed (0x01查询组帧、0x02响应校验与解析、MC/TH双端版本时序衰退状态机及D-Bus GetVersionInfo 100% 通过验证)** |

---

## 1. 契约复核与核心实现 (Contract Alignment & Implementation)

依据 MiniMCProto v2.0 规约（`SPEC-PROTO-20261015-153000`）、`v2-commands.md` 以及任务卡片 `TWIN-29.md` 明确的需求与红线约束，`ENG-FWD` 在上位机 `soc-ap` 完成了双 MCU 真实固件版本查询与衰退状态机的完整实现：

### 1.1 Wire 协议扩展 (`forward_protocol.h` / `forward_protocol.cpp`)
1. **指令与载荷常量定义**：
   - `MINIMC_CMD_GET_VERSION = 0x01U`（查询版本与能力，无载荷，帧总长 14B）；
   - `MINIMC_CMD_VERSION_REPORT = 0x02U`（版本回报，载荷 16B，帧总长 30B）；
   - `MINIMC_VERSION_PAYLOAD_SIZE = 16U`；
   - `MINIMC_VERSION_FRAME_SIZE = 30U`；
2. **Wire 载荷排布与内存布局**：
   - 定义紧凑对齐结构体 `aisoc_fwd_version_info_t`（`#pragma pack(push, 1)`）：
     `uint8_t proto_ver_major`, `uint8_t proto_ver_minor`, `uint8_t firmware_major`, `uint8_t firmware_minor`, `uint32_t boot_id`, `uint32_t git_commit_short`, `uint32_t capability_flags`（总共 16 字节）；
3. **协议构建、校验与解析函数**：
   - `fwd_proto_build_version_query_frame(const char* target, uint16_t seq, fwd_frame_buf_t* out_buf)`：
     构建 MiniMCProto v2.0 `CMD_GET_VERSION` (0x01) 帧：`target "MC"` 寻址 `dst_id = 0x02`；`target "TH"` 寻址 `dst_id = 0x03`。控制位 `flags = 0x05`（`IS_RESPONSE=0, WANTS_ACK=1, PROTO_V2=0x04`），载荷长度 0，CRC-16 覆盖 12B 头；
   - `fwd_proto_validate_version_response(const uint8_t* frame, size_t len, uint8_t expected_src, uint16_t expected_seq)`：
     严格校验总长 `len == 30`，SOF 校验（兼容 `0x5A 0xA5` 与 MiniMC 标准 `0x55 0xAA`），校验 `src_id == expected_src`、`dst_id == 0x01`（AP）、`cmd_id == 0x02`（`CMD_VERSION_REPORT`）、`seq == expected_seq`、`payload_len == 16`，并对前 28 字节执行 `calc_crc16` 比对帧尾 CRC-16；
   - `fwd_proto_parse_raw_version(const uint8_t* payload, size_t len, aisoc_fwd_version_info_t* out_info)`：
     以确定性小端序逐字段显式提取 16B 载荷（禁止指针压缩黑魔法，无任何堆内存分配）。

### 1.2 设备状态机与四态时序衰退 (`device_manager_state.h` / `device_manager_state.cpp`)
1. **状态枚举与模型拓扑**：
   - 增加状态枚举 `aisoc_dev_ver_status_t`：`DEV_VER_STATUS_UNKNOWN (0)`, `DEV_VER_STATUS_ONLINE (1)`, `DEV_VER_STATUS_STALE (2)`, `DEV_VER_STATUS_OFFLINE (3)`, `DEV_VER_STATUS_QUERY_FAILED (4)`；
   - 增加版本结构体 `aisoc_dev_mcu_version_t`（包含 `is_valid`, `proto_major/minor`, `firmware_major/minor`, `boot_id`, `git_commit`, `capability_flags`, `last_update_ns`, `status`）；
   - 使用静态绑定表 `s_version_bindings` 分配 MC 与 TH 双节点版本插槽，零动态堆内存；
2. **状态更新、失败记录与时序衰退**：
   - `dev_state_update_mcu_version(device_manager_state_t* state, const char* node, const aisoc_dev_mcu_version_t* ver, uint64_t now_ns)`：成功查询时更新对应 MC/TH 节点版本并置 `ONLINE` 态与纳秒时间戳；
   - `dev_state_record_mcu_query_failed(device_manager_state_t* state, const char* node, uint64_t now_ns)`：查询失败/校验错误时标记 `QUERY_FAILED`；
   - `dev_state_eval_version_freshness(device_manager_state_t* state, uint64_t now_ns)`：评估时间差 $\Delta t = \text{now\_ns} - \text{last\_update\_ns}$：
     - $\Delta t < 5\text{s}$（5,000,000,000 ns）$\to$ `DEV_VER_STATUS_ONLINE`；
     - $5\text{s} \le \Delta t < 15\text{s}$（15,000,000,000 ns）$\to$ `DEV_VER_STATUS_STALE`；
     - $\Delta t \ge 15\text{s}$ 或 `!is_valid` $\to$ `DEV_VER_STATUS_OFFLINE`；
3. **JSON 拓扑导出与快照集成**：
   - `dev_state_get_version_json(const device_manager_state_t* state, char* out_json, size_t cap)`：序列化输出符合 REST 规约的 `{"devices":{"mc":{...},"th":{...}}}` 拓扑；
   - 在 `dev_state_get_snapshot_json()` 中原子集成 `"devices"` 区块，使全局整机快照具备权威 MCU 版本呈现能力。

### 1.3 D-Bus 接口扩展 (`device_manager_dbus.h` / `device_manager_dbus.cpp`)
- 在 D-Bus 接口 `org.aisoc.DeviceInterface` 注册方法 `GetVersionInfo`；
- 处理函数 `handle_get_version_info` 互斥保护提取双 MCU 版本 JSON 并回复 D-Bus 客户端，提供权威 RPC 数据源。

---

## 2. 交付文件清单与 SHA-256 校验码

| 交付文件路径 | 类型与描述 | SHA-256 校验码 |
| :--- | :--- | :--- |
| `soc-ap/services/forward/forward_protocol.h` | 协议头文件，0x01/0x02 宏、16B 版本载荷定义与接口声明 | `0a791af452324ea37f6a1be0bbfdd5b14020323d2e30b6c63c30bd233e7c5d36` |
| `soc-ap/services/forward/forward_protocol.cpp` | 协议实现，版本查询帧构建、30B 响应校验、小端载荷解析 | `ab806b46306955815fb18becfb2b9dbe1d1f2daba4d96379bcc58607205bbfc7` |
| `soc-ap/services/device_manager/device_manager_state.h` | 状态机头文件，4态衰退枚举、MCU版本结构体与管理接口 | `244b9ef35b51f565ff04f609d9208f99b4f7ff3fe4702b9a3cd107eb30b5d435` |
| `soc-ap/services/device_manager/device_manager_state.cpp` | 状态机实现，双端版本拓扑维护、时序衰退状态机与快照集成 | `378796b1fc91cfb85e3bd462d0fd0d40a84c0a8cb2041f040c0637f450be7154` |
| `soc-ap/services/device_manager/device_manager_dbus.h` | D-Bus 服务头文件 | `d782e7d2707c7102c87219ddbfca88c1bd3e711955b68752f486405f0b753d9a` |
| `soc-ap/services/device_manager/device_manager_dbus.cpp` | D-Bus 服务实现，注册并处理 GetVersionInfo RPC | `c501a72527ac23abda9e4f26b0f3eac0c7faaee46731242c3d4ae4cac776964b` |
| `soc-ap/tests/device_manager/twin/test_device_manager.cpp` | 单元与集成测试套件，正反例与衰退状态机全集用例 | `419c9082ee983ae57045e005fbe16f3068ad2474d735addfa07331e36f450174` |

---

## 3. 编码硬门禁符合性自检表 (Coding Standards Compliance)

对照 `project-control/.agents/rules/c_cpp_coding_standard.md` 进行 100% 逐项自检：

| 门禁规则 | 要求 | 落地核查情况 | 结果 |
| :--- | :--- | :--- | :--- |
| **函数规模门禁** | 自研非结构体函数必须 $\le 50$ 行 | `forward_protocol.cpp`: 36行, 38行, 36行<br/>`device_manager_state.cpp`: 28行, 14行, 34行, 9行, 23行, 21行, 35行, 28行, 25行, 20行, 16行, 17行<br/>`device_manager_dbus.cpp`: 18行, 44行<br/>`test_device_manager.cpp`: 23行, 15行, 41行, 22行, 49行, 37行, 22行, 41行 | **PASS** (100% $\le 50$ 行) |
| **函数参数门禁** | 自研非结构体函数参数必须 $\le 4$ 个 | 所有新增函数参数均控制在 0 ~ 4 个；配置均通过结构体（如 `mock_version_cfg_t*`）传入 | **PASS** (100% $\le 4$ 参数) |
| **防御性空指针校验** | 公开函数首行执行 Guard Clause 校验 | 所有对外公开函数首行均包含 `if (... == nullptr) return ...;` 防御判断 | **PASS** |
| **内存与指针安全** | 零动态堆内存，禁用指针压缩黑魔法 | 无 `malloc/free/new/delete`，无动态 STL 容器；无 `*dst++ = *src++`，均采用显式拆步与下标 | **PASS** |
| **控制流安全** | 大括号嵌套层级 $\le 3$ 层，禁用嵌套三元 | 卫语句优先，控制流完全扁平化 | **PASS** |

---

## 4. 自动化构建与测试执行记录 (Verification Execution Log)

### 4.1 任务图依赖与静态规划检查
```bash
$ PYTHONDONTWRITEBYTECODE=1 python3 project-control/tools/check_task_graph.py --workspace .
```
```json
{
  "scope": "static planning validation, not execution/approval/QA acceptance",
  "canonical_task_count": 116,
  "microtask_count": 74,
  "errors": [],
  "dependency_cycles": [],
  "exit_code": 0
}
```

### 4.2 编译与单元/集成全量测试
```bash
$ cmake -B soc-ap/tests/device_manager/twin/build -S soc-ap/tests/device_manager/twin && cmake --build soc-ap/tests/device_manager/twin/build
$ ./soc-ap/tests/device_manager/twin/build/test_device_manager
```
**输出日志**：
```
========================================================================
TWIN-08 / TWIN-29 Device Manager Verification & Integration Test Suite
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
[RUN ] test_unit_version_proto_build_query
[PASS] test_unit_version_proto_build_query
[RUN ] test_unit_version_proto_validate_positive_and_negative
[PASS] test_unit_version_proto_validate_positive_and_negative
[RUN ] test_unit_version_proto_parse_raw
[PASS] test_unit_version_proto_parse_raw
[RUN ] test_unit_state_version_tracking_and_decay
[PASS] test_unit_state_version_tracking_and_decay
[RUN ] test_unit_state_version_json_and_snapshot
[PASS] test_unit_state_version_json_and_snapshot
[RUN ] [&]() { return test_rpc_get_snapshot(&env.cli_conn); }
[PASS] [&]() { return test_rpc_get_snapshot(&env.cli_conn); }
[RUN ] [&]() { return test_dds_sync_and_signal(&env); }
[DEVICE_MGR DEBUG] DDS RX: node=1, temp=62000 millic (62.0 C) -> Snapshot GEN=11 (DEGRADED)
[PASS] [&]() { return test_dds_sync_and_signal(&env); }
[RUN ] [&]() { return test_rpc_request_sample(&env.cli_conn); }
[PASS] [&]() { return test_rpc_request_sample(&env.cli_conn); }
[RUN ] [&]() { return test_rpc_device_state_and_estop(&env.cli_conn); }
[PASS] [&]() { return test_rpc_device_state_and_estop(&env.cli_conn); }
[RUN ] [&]() { return test_rpc_get_version_info(&env.cli_conn); }
[PASS] [&]() { return test_rpc_get_version_info(&env.cli_conn); }
========================================================================
Total: Passed=22, Failed=0
========================================================================
```

### 4.3 前向转发服务现有测试兼容性验证
```bash
$ cmake -B soc-ap/tests/forward/twin/build -S soc-ap/tests/forward/twin && cmake --build soc-ap/tests/forward/twin/build && ./soc-ap/tests/forward/twin/build/test_forward_service
```
**输出日志**：
```
========================================================================
TWIN-07 FORWARD Service Verification & Integration Test Suite
========================================================================
[RUN ] test_proto_target_mapping
[PASS] test_proto_target_mapping
[RUN ] test_proto_build_frames
[PASS] test_proto_build_frames
[RUN ] test_proto_parse_raw_temp
[PASS] test_proto_parse_raw_temp
[RUN ] [&]() { return test_fwd_full_pipeline(&env.fwd_state, &env.cli_conn); }
[FORWARD DEBUG] TX Query: target=1, seq=1 -> /dev/ttyUSB0
[FORWARD DEBUG] RX Response: node=1, temp_millic=60000 (60.0 C) -> Fast DDS Pub
[FORWARD DEBUG] TX Query: target=2, seq=2 -> /dev/ttyUSB0
[FORWARD DEBUG] RX Response: node=2, temp_millic=210000 (210.0 C) -> Fast DDS Pub
[PASS] [&]() { return test_fwd_full_pipeline(&env.fwd_state, &env.cli_conn); }
========================================================================
Total: Passed=4, Failed=0
========================================================================
```

---

## 5. 结论与移交提议 (Conclusion & Handoff)

`ENG-FWD` 已圆满完成 `TWIN-29` 研发工作，所有交付物均在严格的写权限与代码规范红线约束下完成，全量单测与集成测试通过率 100%。

- **候选提交 (Candidate Commit)**：`soc-ap: 594ffab12902ac5b38a6f1a6dd869da0942c8dbb`
- **提议移交对象**：`COORD` 与独立审查 `QA` (`session-qa-twin-29`) 进行独立验证。
