# TWIN-02 双环境可执行通信契约与生成规则执行与验收报告

| 属性 | 内容 |
| :--- | :--- |
| **任务卡片** | `TWIN-02` (双环境可执行通信契约与生成规则) |
| **所属工作包** | `TASK-013` (冻结 DDS D-Bus MQTT 通信契约) |
| **所属计划** | `PLAN-TWIN-TASK-EXECUTION-20261029` (VMware与SoC两阶段任务执行与闭环总表) |
| **执行角色** | `ARCH` (系统架构师) |
| **基线输入** | `ICD-VMWARE-SOC-TWIN-20261029 revision 2` (`923d250ec36b2585120f70620f3a71572448496f0a3850c5d3f9594321959793`) |
| **前置条件绑定** | `TWIN-01` (`docs/evidence/twin/TWIN-01/runs/run_01/result.md`) |
| **执行日期** | 2026-10-30 |
| **执行状态** | **Completed / Delivered (契约原件齐备，语法与生成验证全通，等待独立 QA 与各岗位审查)** |

---

## 1. 交付物清单与 SHA256 校验码

本任务严格依照微任务卡片授权范围（`allowed_paths: soc-ap/contracts/twin/**`, `project-control/docs/evidence/twin/TWIN-02/**`）实施交付。所有产物均位于 `soc-ap/contracts/twin/` 目录，无越界写操作。

| 交付文件路径 | 文件类型与规范 | SHA256 校验码 | 状态 |
| :--- | :--- | :--- | :--- |
| [`soc-ap/contracts/twin/README.md`](../../../../../../soc-ap/contracts/twin/README.md) | 全链路协议映射、生成规则与兼容策略说明 | `09f869547f7e9b1b04b781177d261421cf956b927c2eb3ef3cf4b52ab73f650e` | **Delivered** |
| [`soc-ap/contracts/twin/telemetry.idl`](../../../../../../soc-ap/contracts/twin/telemetry.idl) | Fast DDS 权威 IDL 规范 (OMG IDL / Fast DDS 3.6.2) | `50987edd6419d7c4ac61a18b87f1f7f18638b9595db0c042dae0071d2a81b516` | **Delivered** |
| [`soc-ap/contracts/twin/dbus_interfaces.xml`](../../../../../../soc-ap/contracts/twin/dbus_interfaces.xml) | D-Bus 权威 Introspection XML 接口规范 | `cf1389ffd6d4f580865af6033abdaaf66e3d2d9072dda0ca00785e6bc7ac54ed` | **Delivered** |
| [`soc-ap/contracts/twin/http_sse_schema.json`](../../../../../../soc-ap/contracts/twin/http_sse_schema.json) | Web REST 与 SSE 实时事件流权威 JSON Schema (Draft-07) | `3df1e1e92e4499ecee7812d0c1dc9e82dc1a2b852270102d0d2e9d82dc3be5f7` | **Delivered** |
| [`soc-ap/contracts/twin/telemetry_types.h`](../../../../../../soc-ap/contracts/twin/telemetry_types.h) | C/C++ 权威二进制布局、线缆结构体、哨兵与转换内联函数 | `33e9d0c8dd78f59fd2ce7e303171ae54e5621ef936fbcebf4ada6740bea99f47` | **Delivered** |
| [`soc-ap/contracts/twin/services_manifest_schema.json`](../../../../../../soc-ap/contracts/twin/services_manifest_schema.json) | 运行时服务拓扑、IPC 通道、资源预算与 systemd Schema | `4d05014be794634ffd1bfcda95112f907daabf3a2be33ac5509660d37dde6dc8` | **Delivered** |
| [`project-control/docs/evidence/twin/TWIN-02/runs/run_01/result.md`](result.md) | 本执行与验收证据报告 | *当前文件* | **Delivered** |

---

## 2. 架构决策与 ICD 契约合规性核查 (ICD Compliance Audit)

对照 `project-control/docs/interfaces/vmware_soc_twin_architecture_icd_20261029.md` 逐项核验：

| 架构核查项 | ICD 规定标准 | TWIN-02 实现事实 | 审计结论 |
| :--- | :--- | :--- | :--- |
| **C1 协议 Flags** | 请求帧为 `0x05` (`V2_FLAG_VERSION_2 \| V2_FLAG_WANTS_ACK`)；响应帧为 `0x06` (`V2_FLAG_VERSION_2 \| V2_FLAG_IS_RESPONSE`) | `telemetry_types.h` 定义 `MINIMC_REQ_FLAGS_V2 (0x05U)` 与 `MINIMC_RESP_FLAGS_V2 (0x06U)`，且 `telemetry_validate_header` 强校验版本位 `0x04` | **PASS** |
| **C2 温度数据表示** | MCU 线缆层采用有符号 `int16_t`，分辨率 0.1°C (`deci_c`)；AP 内部标准化为有符号 `int32_t` 毫摄氏度 (0.001°C) | `minimc_temp_wire_payload_t` 字段 `current_temp_deci_c` (int16_t)；IDL 与内部类型使用 `temperature_millic` (int32_t)；提供转换函数 `telemetry_deci_to_millic` | **PASS** |
| **C3 量程与哨兵** | 物理有效量程 $-40.0^\circ\text{C} \sim +500.0^\circ\text{C}$ (数值 -400 ~ 5000)；故障哨兵 `0x7FFF` (+32767)，离线哨兵 `0x7FFE` (+32766) | `MINIMC_TEMP_SENTINEL_FAULT = 0x7FFF`，`MINIMC_TEMP_SENTINEL_OFFLINE = 0x7FFE`；内部映射为 `0x7FFFFFFF` 与 `0x7FFFFFFE` | **PASS** |
| **C4 指令码分配** | 温度主动查询指令固定为 `0x14` (`CMD_TEMP_QUERY` / `CMD_TEMP_REPORT`) | `telemetry_types.h` 中 `MINIMC_CMD_TEMP_QUERY = 0x14U`，`MINIMC_CMD_TEMP_REPORT = 0x14U` | **PASS** |
| **C5 传感器状态映射** | `0x00`=OK, `0x01`=OPEN, `0x02`=SHORT, `0x03`=ADC_TIMEOUT, `0xFF`=UNKNOWN | `telemetry_types.h` 与 `telemetry.idl` 逐字对齐定义 `SensorStatus` 枚举并提供 `telemetry_map_sensor_status` 转换函数 | **PASS** |
| **服务拓扑与进程划分** | 4 个独立真实进程：`forward-service`, `device-manager`, `ui-gateway`, `Browser HMI`；6 个未就绪模块暂缓不启动空进程 | `services_manifest_schema.json` 严格枚举 10 个标准模块，锁定首切片 4 个常驻进程及资源边界，标记其余为 `deferred` | **PASS** |
| **DDS 数据流模型** | `telemetry/raw_temp` (RELIABLE, VOLATILE, KEEP_LAST(5))；`state/temperature_snapshot` (BEST_EFFORT, TRANSIENT_LOCAL, KEEP_LAST(1)) | `telemetry.idl` 与 `README.md` 中完整定义数据结构、QoS 策略与映射关系 | **PASS** |
| **D-Bus 控制模型** | `org.aisoc.ForwardInterface` (/org/aisoc/forward), `org.aisoc.DeviceInterface` (/org/aisoc/device), `org.aisoc.HmsInterface` (/org/aisoc/hms) | `dbus_interfaces.xml` 完整定义三组标准接口，包含输入输出参数类型与信号定义 | **PASS** |
| **HTTP/SSE 契约** | REST `/api/v1/temperature/snapshot` (schema_version=2), `/api/v1/motion/status`, `/api/v1/hms/active`；SSE `/api/v1/events/stream` | `http_sse_schema.json` 使用 JSON Schema Draft-07 形式化锁定全量端点输入输出结构 | **PASS** |

---

## 3. C/C++ 编码规范硬门禁审查 (Coding Standard Hard Gate Audit)

对照 `project-control/.agents/rules/c_cpp_coding_standard.md` 逐条核验 `soc-ap/contracts/twin/telemetry_types.h`：

| 规范门禁要求 | 约束指标 | `telemetry_types.h` 实测值 | 审计结论 |
| :--- | :--- | :--- | :--- |
| **硬门禁 1：函数规模** | 严禁编写超 50 行的自研非结构体函数 | 最长函数为 `telemetry_deci_to_millic` 与 `telemetry_millic_to_deci` (均仅 25 行)，远低于 50 行上限 | **PASS** |
| **硬门禁 2：入参个数** | 严禁编写超 4 个入参的自研非结构体函数 | 所有函数入参均为 1~3 个 (无任何函数超过 3 个参数) | **PASS** |
| **防御性空指针校验** | 所有接收指针参数的函数入口第一行必须进行空指针 Guard Clause | 所有接收指针的函数首行均为 `if (... == NULL) return TELEMETRY_ERR_NULL_PTR;` | **PASS** |
| **参数顺序与只读修饰** | 入参在前加 `const`，出参在后 | 所有只读入参均标 `const`，数据输出均由末尾出参指针传出 | **PASS** |
| **返回值统一度量** | 返回强类型枚举错误码或布尔值 | 易错函数统一返回强类型 `telemetry_status_t` 状态码 | **PASS** |
| **内存与指针安全** | 零动态堆内存分配；严禁指针黑魔法 (`*dst++ = *src++`)；指针解引用独立成行；禁止多重指针 (`***ptr`) | 零动态堆内存；指针运算扁平清晰，分步解引用独立成行；无二级以上多重指针 | **PASS** |
| **控制流扁平化** | 禁用嵌套三元运算符；嵌套层级严禁超 3 层；复合逻辑拆解为具名临时布尔变量 | 无嵌套三元运算符；大括号最大嵌套深度仅 2 层；布尔条件具名拆解 (如 `is_fault`, `is_offline`, `below_min`, `above_max`) | **PASS** |
| **头文件防重入与声明** | 标准 Header Guard，`extern "C"` 守卫，无全局变量实体定义 | 包含 `#ifndef AISOC_TELEMETRY_TYPES_H` 与 `#ifdef __cplusplus extern "C"`，函数全为 `static inline` | **PASS** |
| **结构体布局与静态断言** | 严禁魔数；通信帧对齐与尺寸编译期断言 | 使用 `static_assert` / `_Static_assert` 严格断言 `minimc_header_t` (12B) 与 `minimc_temp_wire_payload_t` (16B) | **PASS** |

---

## 4. 自动化验证命令与执行输出实录

### 4.1 C++17 语法与编译门禁检查
```bash
g++ -std=c++17 -Wall -Wextra -Werror -fsyntax-only soc-ap/contracts/twin/telemetry_types.h
```
**输出**：Exit code `0` (零警告、零错误，编译期静态断言 `sizeof == 12` 与 `sizeof == 16` 顺利通过)。

### 4.2 C11 语法与纯 C 兼容性检查
```bash
gcc -std=c11 -Wall -Wextra -Werror -fsyntax-only soc-ap/contracts/twin/telemetry_types.h
```
**输出**：Exit code `0` (零警告、零错误，`_Static_assert` 兼容性通过)。

### 4.3 D-Bus Introspection XML 语法与代码生成验证
```bash
gdbus-codegen --generate-c-code /tmp/test_codegen --c-namespace Aisoc soc-ap/contracts/twin/dbus_interfaces.xml
```
**输出**：Exit code `0`，成功生成标准 GDBus C 代码骨架，证明 XML 格式完全符合 freedesktop D-Bus 规范。

### 4.4 JSON Schema 合法性校验
```bash
python3 -m json.tool soc-ap/contracts/twin/http_sse_schema.json > /dev/null
python3 -m json.tool soc-ap/contracts/twin/services_manifest_schema.json > /dev/null
```
**输出**：Exit code `0`，两份 JSON 文件语法均合规，无任何格式错误。

### 4.5 任务依赖图无损静态检查
```bash
PYTHONDONTWRITEBYTECODE=1 python3 project-control/tools/check_task_graph.py --workspace .
```
**输出**：
```json
{
  "scope": "static planning validation, not execution/approval/QA acceptance",
  "canonical_task_count": 108,
  "microtask_count": 66,
  "errors": [],
  "dependency_cycles": [],
  "exit_code": 0
}
```
**结论**：全局任务依赖关系完全完好，无循环依赖，无结构性破损。

---

## 5. 后续任务交接与通信工程师消费边界

依照 `project-control/docs/planning/communication_modules_ownership_20261029.md`：
1. **`TWIN-05` (ENG-DDS)**：消费 `soc-ap/contracts/twin/telemetry.idl`，使用 `fastddsgen` 接入 `soc-ap/middleware/dds/`，实现 Fast DDS 通信底座与统一发布订阅 SDK；
2. **`TWIN-06` (ENG-DBUS)**：消费 `soc-ap/contracts/twin/dbus_interfaces.xml`，使用 `gdbus-codegen` 接入 `soc-ap/middleware/dbus/`，实现 D-Bus 通信底座与客户端/服务端统一 SDK；
3. **`TWIN-07` (ENG-FWD)**：消费 `telemetry_types.h` 与 `telemetry.idl`，实现 `forward-service` 串口 MiniMCProto 0.1°C 报文编解码与 DDS 发布；
4. **`TWIN-08` (ENG-STATE)**：消费 `telemetry.idl` 与 `http_sse_schema.json`，实现 `device-manager` 0.001°C 归一化聚合与权威快照维护；
5. **`TWIN-15` (ENG-MC) / `TWIN-16` (ENG-TH)**：按 0.1°C `deci_c` 规范分别在 `mcu-p3/motion-controller-mcu/` 与 `mcu-p3/color-engine-mcu/io_toggle/` 实施固件修改；
6. **独立审阅移交**：本票已完成交付物编写与自检，移交 `COORD` 安排独立 `QA`（Codex 会话）与各工程角色进行独立审查。
