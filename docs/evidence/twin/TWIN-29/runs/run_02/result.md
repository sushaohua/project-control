# TWIN-29 AP端双MCU真实固件版本查询链路与时序衰退状态机实现交付自检报告 (Run 02)

| 属性 | 内容 |
| :--- | :--- |
| **任务卡片** | `TWIN-29` (AP端双MCU真实固件版本查询链路与时序衰退状态机实现) |
| **所属工作包** | `TASK-007` (实现 forward 协议与传输), `TASK-008` (实现整机状态和统一指令准入) |
| **执行角色** | `ENG-FWD` (Forward & Device Manager Engineer) |
| **当前轮次** | `run_02` (针对 Run 01 QA 驳回意见的专项缺陷修复与门禁强化) |
| **前置依赖** | `TWIN-25` (`soc-ap: f2596517c8e7a53da6ff9623d948ec5e70bf6770`) |
| **Run 01 被驳回 Commit** | `soc-ap: 594ffab12902ac5b38a6f1a6dd869da0942c8dbb` |
| **Run 02 候选 Commit** | `soc-ap: 86f5e17ead0971ca1a1eb20c07ca345924e24454` (`fix(twin): address QA review findings for dual MCU version telemetry (TWIN-29 run_02)`) |
| **作者会话 ID** | `session-eng-fwd-twin-29` |
| **执行状态** | **Completed (QA 5 项驳回意见 100% 修复，全量 23 项单元与集成测试套件 100% 通过)** |

---

## 1. QA 驳回意见整改复核 (QA Review Findings Resolution)

对照 QA 驳回报告 `project-control/docs/evidence/twin/TWIN-29/runs/run_01/qa_review_report.md`，执行角色 `ENG-FWD` 在 `run_02` 中完成如下专项闭环修复：

### 1.1 修复 SOF 容差缺陷 (Defect 1)
- **QA 意见**：`fwd_proto_validate_version_response` 接受了非标 `0x5A 0xA5`，违反 MiniMCProto v2.0 规范（魔数必须为 `0x55 0xAA`）。
- **整改落实**：
  - 在 `soc-ap/services/forward/forward_protocol.cpp` 中彻底移除对 `0x5A 0xA5` 的宽松容差逻辑；
  - 严格校验 `frame[0] == MINIMC_SOF_1 && frame[1] == MINIMC_SOF_2`（`0x55U` 与 `0xAAU`）；
  - 生产代码中彻底清除所有 `0x5AU / 0xA5U` 裸字面量；
  - 在 `test_device_manager.cpp` 中新增反向测试用例 `Negative 1`，明确断言传入 `0x5A 0xA5` SOF 帧必须被拒绝并返回 `AISOC_FWD_ERR_INVALID_ARG`。

### 1.2 消除裸魔数字面量 (Defect 2)
- **QA 意见**：状态衰退阈值裸写 `5000000000ULL` / `15000000000ULL`；请求 flags 裸写 `0x05U`；hop limit 裸写 `10U`。
- **整改落实**：
  - 在 `soc-ap/services/device_manager/device_manager_state.h` 增加具名常量宏：
    - `#define AISOC_DEV_VER_ONLINE_TIMEOUT_NS 5000000000ULL` (5s 在线衰退门限)
    - `#define AISOC_DEV_VER_STALE_TIMEOUT_NS 15000000000ULL` (15s 离线衰退门限)
  - 在 `soc-ap/services/forward/forward_protocol.h` 增加具名常量宏：
    - `#define MINIMC_DEFAULT_HOP_LIMIT 10U`
  - 使用 `MINIMC_REQ_FLAGS_V2`（`0x05U`，即 `MINIMC_FLAG_VERSION_2 | MINIMC_FLAG_WANTS_ACK`）与 `MINIMC_RESP_FLAGS_V2`（`0x06U`）；
  - 全工程消除上述所有裸魔数。

### 1.3 补充响应控制位 `IS_RESPONSE` 校验 (Defect 3)
- **QA 意见**：`fwd_proto_validate_version_response` 未校验响应帧的 `IS_RESPONSE` 标志位。
- **整改落实**：
  - 在 `fwd_proto_validate_version_response` 校验逻辑中增加：
    `if ((frame[4] & MINIMC_FLAG_IS_RESPONSE) == 0U) { return AISOC_FWD_ERR_INVALID_ARG; }`；
  - 在 `test_device_manager.cpp` 中新增反向测试用例 `Negative 2`，断言缺失 `IS_RESPONSE` 标志位的响应帧必须被拒绝并返回 `AISOC_FWD_ERR_INVALID_ARG`。

### 1.4 修复版本绑定槽满静默覆盖槽位 0 缺陷 (Defect 4)
- **QA 意见**：`find_or_create_version_binding` 和 `find_or_create_grid_binding` 在槽满时静默覆盖槽位 0，破坏了正在运行状态的完整性。
- **整改落实**：
  - 修改 `find_or_create_version_binding` 与 `find_or_create_grid_binding`，在槽位耗尽时严禁覆盖槽位 0，统一返回 `nullptr`；
  - 上层调用者 `dev_state_update_mcu_version`、`dev_state_record_mcu_query_failed` 检测到 `nullptr` 时返回 `AISOC_DEV_ERR_BUSY`；
  - 增加公共接口 `void dev_state_reset_bindings(void)`，便于单元测试隔离与生命周期管理；
  - 在 `test_device_manager.cpp` 中新增 `test_unit_state_version_binding_exhaustion` 单元测试，严密断言：
    - 前 16 个状态成功绑定槽位；
    - 第 17 个状态返回 `AISOC_DEV_ERR_BUSY`；
    - 验证槽位 0 的状态与 JSON 数据未被破坏或覆盖（Slot 0 ONLINE 保持完整）。

### 1.5 消除节点别名重复解析代码 (Defect 5)
- **QA 意见**：`dev_state_update_mcu_version` 和 `dev_state_record_mcu_query_failed` 存在重复的字符串节点解析逻辑。
- **整改落实**：
  - 提取静态辅助函数 `resolve_mcu_version_slot(dev_state_version_binding_t* binding, const char* node, aisoc_dev_mcu_version_t** out_slot)`；
  - 辅助函数控制在 20 行以内、3 个入参，两处公共调用点统一复用该解析函数。

---

## 2. 交付文件清单与 SHA-256 校验码

| 交付文件路径 | 类型与描述 | SHA-256 校验码 |
| :--- | :--- | :--- |
| `soc-ap/services/forward/forward_protocol.h` | 协议头文件，新增 `MINIMC_DEFAULT_HOP_LIMIT` 具名常量 | `188de250ecbd4a06a44ebcf8909c956cd2878cda16dd3128610718919684ede2` |
| `soc-ap/services/forward/forward_protocol.cpp` | 协议实现，严格校验标准 SOF 0x55 0xAA、校验 IS_RESPONSE 标志位、消除魔数 | `07abba5cd85a849f2385ef8a8ace4ac6876abde61cacbb926ab95ec15c9a5e96` |
| `soc-ap/services/device_manager/device_manager_state.h` | 状态机头文件，新增时序衰退具名常量宏与 `dev_state_reset_bindings` | `0d569c52160f032fd7f78592b36c45f77b439b94146c2c8970bace58a07aba76` |
| `soc-ap/services/device_manager/device_manager_state.cpp` | 状态机实现，槽满拒绝返回 nullptr/BUSY、提取节点解析公共函数、消除魔数 | `77b8cabfa23c26543efe5f787d9757a381c26aa9c3c01cbda246a85c0c9ce942` |
| `soc-ap/services/device_manager/device_manager_dbus.h` | D-Bus 服务头文件 | `d782e7d2707c7102c87219ddbfca88c1bd3e711955b68752f486405f0b753d9a` |
| `soc-ap/services/device_manager/device_manager_dbus.cpp` | D-Bus 服务实现，注册并处理 GetVersionInfo RPC | `c501a72527ac23abda9e4f26b0f3eac0c7faaee46731242c3d4ae4cac776964b` |
| `soc-ap/tests/device_manager/twin/test_device_manager.cpp` | 单元与集成测试套件，补充坏 SOF 拒绝、缺失响应标志拒绝、槽满防破坏用例 | `8d1875896acdeca1d1f2c40d7ae77c78587c0b4d1131e847fe30581f9762d54b` |

---

## 3. 编码硬门禁符合性自检表 (Coding Standards Compliance)

对照 `project-control/.agents/rules/c_cpp_coding_standard.md` 进行 100% 逐项自检：

| 门禁规则 | 要求 | 落地核查情况 | 结果 |
| :--- | :--- | :--- | :--- |
| **函数规模门禁** | 自研非结构体函数必须 $\le 50$ 行 | `forward_protocol.cpp`: 17行, 36行, 31行, 21行, 39行, 29行, 20行, 30行, 39行, 36行, 36行<br/>`device_manager_state.cpp`: 6行, 35行, 26行, 36行, 36行, 17行, 34行, 15行, 20行, 18行, 48行, 26行, 23行, 15行, 20行<br/>`device_manager_dbus.cpp`: 22行, 24行, 43行, 11行<br/>`test_device_manager.cpp`: 所有测试函数及 main 均 $\le 50$ 行 (main 为 39 行) | **PASS** (100% $\le 50$ 行) |
| **函数参数门禁** | 自研非结构体函数参数必须 $\le 4$ 个 | 全量函数参数均为 0 ~ 4 个；配置均通过结构体指针传入 | **PASS** (100% $\le 4$ 参数) |
| **防御性空指针校验** | 公开函数首行执行 Guard Clause 校验 | 所有对外公开函数首行均包含防御性空指针判断并返回对应错误码 | **PASS** |
| **内存与指针安全** | 零动态堆内存，禁用指针压缩黑魔法 | 无 `malloc/free/new/delete`，无动态 STL 容器；无 `*dst++ = *src++` | **PASS** |
| **控制流安全** | 大括号嵌套层级 $\le 3$ 层，禁用嵌套三元 | 卫语句优先，控制流完全扁平化 | **PASS** |
| **魔数彻底杜绝** | 严禁裸常量 | 所有衰退阈值、协议标志位、跳数限制均采用具名宏定义 | **PASS** |

---

## 4. 自动化构建与测试执行记录 (Verification Execution Log)

### 4.1 Device Manager 单元与集成全集测试 (TWIN-08 / TWIN-29)
```bash
$ cmake -B soc-ap/tests/device_manager/twin/build -S soc-ap/tests/device_manager/twin && cmake --build soc-ap/tests/device_manager/twin/build
$ ./soc-ap/tests/device_manager/twin/build/test_device_manager
```
执行输出：
```text
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
[RUN ] test_unit_state_version_binding_exhaustion
[PASS] test_unit_state_version_binding_exhaustion
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
Total: Passed=23, Failed=0
========================================================================
```

### 4.2 Forward 服务测试 (TWIN-07)
```bash
$ cmake -B soc-ap/tests/forward/twin/build -S soc-ap/tests/forward/twin && cmake --build soc-ap/tests/forward/twin/build
$ ./soc-ap/tests/forward/twin/build/test_forward_service
```
执行输出：
```text
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

## 5. 候选提交与推送证明 (Commit & Remote Push Evidence)

### 5.1 本地提交记录
```bash
$ git -C soc-ap log -n 1 --stat
commit 86f5e17ead0971ca1a1eb20c07ca345924e24454
Author: sushaohua <sushaohua@example.com>
Date:   Sat Oct 31 14:24:18 2026 +0800

    fix(twin): address QA review findings for dual MCU version telemetry (TWIN-29 run_02)
    
     services/device_manager/device_manager_state.cpp   | 51 ++++++++++++++++++------------
     services/device_manager/device_manager_state.h     |  5 +++
     services/forward/forward_protocol.cpp              | 20 ++++++------
     services/forward/forward_protocol.h                |  1 +
     tests/device_manager/twin/test_device_manager.cpp  | 75 +++++++++++++++++++++++++++------------------
     5 files changed, 103 insertions(+), 49 deletions(-)
```

### 5.2 远端推送记录
```text
To ssh://192.168.77.113:2222/sushaohua/soc-ap.git
   594ffab..86f5e17  main -> main
```

**候选提交 SHA**: `soc-ap: 86f5e17ead0971ca1a1eb20c07ca345924e24454`
