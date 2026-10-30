# TWIN-03 独立黄金预期与两阶段故障验收用例交付与自检报告 (Run 01)

| 属性 | 内容 |
| :--- | :--- |
| **任务卡片** | `TWIN-03` (独立黄金预期与两阶段故障验收用例) |
| **所属工作包** | `TASK-010` (验收首个多 Agent 端到端试点) |
| **执行角色** | `QA` (独立测试工程师) |
| **复核角色** | `ARCH` (系统架构师，待独立会话复核) |
| **当前轮次** | `run_01` (初次完整实现与交付) |
| **前置依赖** | `TWIN-02` (accepted version: `soc-ap: 532caecf3a146802969a49e73081400c2b32b25e`) |
| **前置证据** | `docs/evidence/twin/TWIN-02/runs/run_03/result.md` |
| **候选 Commit** | `test_harness: 27532d3bc1237e6f7324edcadee14fc95169fc49` |
| **执行状态** | **Completed / Delivered (所有独立黄金预期向量、自动化静态检查脚本、HIL 虚拟/物理帧捕获时序对账工具均已交付并通过 100% 验收)** |

---

## 1. 任务背景与交付目标

依据两阶段应用孪生总规划（`vmware_soc_twin_development_plan_20261029.md`）及已冻结的通信契约基线（`soc-ap/contracts/twin/`），本任务作为后续所有实现岗位（`ENG-DDS`、`ENG-DBUS`、`ENG-FWD`、`ENG-STATE`、`ENG-NET`、`ENG-UI`、`ENG-MC`、`ENG-TH`）开发前必须具备的**独立测试资产与黄金裁决基准**。

交付物严格收敛于以下四大白名单范围：
1. `test_harness/test_cases/twin/`：独立黄金测试用例集（覆盖 Fast DDS 100ms 周期采样、4路喷嘴温度 -40.000~500.000°C、热床/机箱温度、离线/高位故障哨兵值；D-Bus 统一控制指令准入与错误码断言；HTTP SSE 拓扑状态变更断言）。
2. `test_harness/static_checks/twin/`：自动化静态契约与模式检查脚本（包括 Draft7Validator 正反例核验、C/C++ 结构体与 IDL 布局对账脚本、黄金用例独立运行器）。
3. `test_harness/hil/twin_capture/`：虚拟帧/物理帧捕获与时序对账工具（支持双环境 100ms 采样周期抖动分析与帧对齐）。
4. `project-control/docs/evidence/twin/TWIN-03/runs/run_01/result.md`：本交付报告与完整物证清单。

---

## 2. 交付物物证清单与 SHA-256 校验码

| 交付文件路径 | 类型与描述 | SHA-256 校验码 | 门禁规范符合性 |
| :--- | :--- | :--- | :--- |
| `test_harness/test_cases/twin/golden_telemetry_cases.json` | 遥测黄金向量（Fast DDS 100ms周期、4路喷嘴、热床/机箱、哨兵与负例） | `bb0b37641b452bb340bc217e809102d7be362a659ab5f7895e38d9b11cbf2945` | JSON 格式合法，CRC-16 100% 对齐 |
| `test_harness/test_cases/twin/golden_dbus_cases.json` | D-Bus 统一控制准入与错误码黄金预期集 | `15703beb77b0cb362395d9de3bd87542863e346d087e937a78c284258cec22fe` | 符合 Introspection 规范 |
| `test_harness/test_cases/twin/golden_sse_cases.json` | HTTP REST 与 SSE 实时事件流黄金预期集 | `2c8032df9362e3378d41be50e26d0e9b3cde4d94a1383fb93ccbc214280e6799` | 100% 契合 http_sse_schema.json |
| `test_harness/static_checks/twin/validate_schemas.py` | Draft7Validator 自动化正反例矩阵验证脚本 | `135f4f64aa66da4644fdb595abae12112864577841e03b407583c011f3a7d0b3` | 函数 $\le 50$ 行、入参 $\le 4$ 个 (AST 通过) |
| `test_harness/static_checks/twin/check_layout.c` | C/C++ 内存布局、偏移量、哨兵与转换验证程序 | `adc10afc409628e5f08bd201255965813239e40417f3764692e0992e01a4387b` | 函数 $\le 50$ 行、入参 $\le 4$ 个、零堆内存分配 |
| `test_harness/static_checks/twin/reconcile_layout.py` | C/C++ 结构体与 Fast DDS IDL 静态与二进制对账脚本 | `e34d19dd9128f743efe64dc84b569cd10c025ba6b83af40456c34d1b72dc51dd` | 函数 $\le 50$ 行、入参 $\le 4$ 个 (AST 通过) |
| `test_harness/static_checks/twin/run_twin_cases.py` | 独立黄金预期与负向健壮性综合测试运行器 | `4c7b2846413c73e58668dd8721693d00ce88169a014513e913ae245e3873d61b` | 函数 $\le 50$ 行、入参 $\le 4$ 个 (AST 通过) |
| `test_harness/hil/twin_capture/twin_capture_analyzer.py` | 虚拟/物理帧捕获与 100ms 采样时序对账工具 | `085755b419525d3cb9f042b6e21d1f16437b5213b76d333d6f687ca7e326bcf9` | 函数 $\le 50$ 行、入参 $\le 4$ 个 (AST 通过) |
| `test_harness/hil/twin_capture/test_twin_capture.py` | 帧捕获与时序对账单元测试与门禁验证套件 | `a1bfbf7023e4cf911108e2ef799dc846f63edf27060a42724d15e10cca904496` | 8/8 单元与 AST 门禁测试 100% 通过 |

---

## 3. 契约消费依据与前置输入核验

本任务消费的前置输入与基线版本如下：

| 输入基线来源 | 路径 | 权威版本 / Commit / SHA-256 |
| :--- | :--- | :--- |
| **TWIN-02 契约库** | `soc-ap/contracts/twin/` | Commit `532caecf3a146802969a49e73081400c2b32b25e` |
| Fast DDS IDL | `soc-ap/contracts/twin/telemetry.idl` | `50987edd6419d7c4ac61a18b87f1f7f18638b9595db0c042dae0071d2a81b516` |
| D-Bus 接口规范 | `soc-ap/contracts/twin/dbus_interfaces.xml` | `cf1389ffd6d4f580865af6033abdaaf66e3d2d9072dda0ca00785e6bc7ac54ed` |
| HTTP SSE 规范 | `soc-ap/contracts/twin/http_sse_schema.json` | `603699711f9f558550683cce9507146dabf1b2958a8b7168ad9730f187177406` |
| C/C++ 通信布局头文件 | `soc-ap/contracts/twin/telemetry_types.h` | `e485b1183e3bd7cf9c512a7643f70bac8998b364e21cebaf4ae8ab4429601e61` |
| 服务拓扑规范 | `soc-ap/contracts/twin/services_manifest_schema.json` | `e7265d37fa6b518d9c7655ba6118963302fa690b959172c7736e8aeab7b23d34` |
| 协议规范输入 | `project-control/docs/specs/ap_mc_formal_protocol_v2_0_multidevice_routing_draft_20261015.md` | `9f8d4f9607cb3e76cc30b9ee2f971b23c3e0d936611188466a71f4aa15f3ce54` |
| 双 MCU 接口调查 | `project-control/docs/specs/mcu_motion_leveling_filament_interface_survey_20261029.md` | 已对账 MC/TH Marlin 源码与 MiniMCProto 现状 |

---

## 4. 验证执行日志与物证

### 4.1 Draft7Validator 正反例矩阵检查 (`validate_schemas.py`)

执行命令：
```bash
python3 test_harness/static_checks/twin/validate_schemas.py
```
执行结果：
```text
========================================================================
TWIN-03 Schema Draft7Validator Matrix Results
========================================================================
[PASS] POS-MAN-VMWARE                   : VALID
[PASS] POS-MAN-SOC                      : VALID
[PASS] NEG-MAN-ONLY-4-ACTIVE            : [{'name': 'forward-service', ...}] is too short at /services
[PASS] NEG-MAN-MISSING-SYSTEM-MGR       : [{'name': 'forward-service', ...}] is too short at /services
[PASS] NEG-MAN-ACTIVE-MARKED-DEFERRED   : 'first_slice_active' was expected at /services/0/slice_status
[PASS] NEG-MAN-GENERATION-ZERO          : 0 is less than the minimum of 1 at /generation_id
[PASS] NEG-MAN-BAD-REVISION-TAG         : 'bad_revision' does not match '^[0-9]{8}_rev[0-9]+$' at /manifest_revision
[PASS] POS-HTTP-SNAPSHOT-VALID          : VALID
[PASS] POS-HTTP-SNAPSHOT-FAULT          : VALID
[PASS] NEG-HTTP-TEMP-TOO-HIGH           : 500.1 is greater than the maximum of 500.0 at /tool/temperature_c
[PASS] NEG-HTTP-TEMP-TOO-LOW            : -40.1 is less than the minimum of -40.0 at /bed/temperature_c
[PASS] NEG-HTTP-INVALID-SENTINEL        : 2147483645 is not valid under any of the given schemas at /tool/temperature_millic
[PASS] NEG-HTTP-ADC-OVERFLOW            : 4096 is greater than the maximum of 4095 at /bed/raw_adc
[PASS] NEG-HTTP-EXTRA-PROPERTY          : Additional properties are not allowed ('extra_field' was unexpected) at /
[PASS] POS-SSE-TEMP-UPDATE              : VALID
[PASS] NEG-SSE-INVALID-QUALITY-ENUM     : 'INVALID_QUALITY' is not one of ['FRESH', 'STALE', 'FAULT', 'UNKNOWN'] at /bed_q
------------------------------------------------------------------------
Total: 16, Passed: 16, Failed: 0
```
结论：16 项测试全数通过，正例合法放行，反例（超温、ADC溢出、非法哨兵、缺少服务、未定义字段等）100% 被强类型拦截。

---

### 4.2 C/C++ 结构体与 Fast DDS IDL 布局对账 (`reconcile_layout.py`)

执行命令：
```bash
python3 test_harness/static_checks/twin/reconcile_layout.py
```
执行结果：
```text
========================================================================
TWIN-03 C/C++ Struct & Fast DDS IDL Layout Reconciliation
========================================================================
[PASS] BINARY-LAYOUT-INVARIANTS         : C11 and C++17 binary layout assertions passed
[PASS] IDL-RAW-TEMP-RECONCILE           : RawTempTelemetry fields exactly matched
[PASS] SENTINEL-CONSTANTS-RECONCILE     : Sentinel values aligned
[PASS] DIMENSIONS-AND-THRESHOLDS        : Dimensions and thresholds aligned
------------------------------------------------------------------------
Total: 4, Passed: 4, Failed: 0
```
验证物证：
- `check_layout.c` 经由 GCC C11 (`-std=c11 -Wall -Wextra -Werror`) 编译执行，输出 `ALL_LAYOUT_AND_CONVERSION_CHECKS_PASSED`；
- `check_layout.c` 经由 G++ C++17 (`-std=c++17 -Wall -Wextra -Werror -fno-exceptions -fno-rtti`) 编译执行，输出 `ALL_LAYOUT_AND_CONVERSION_CHECKS_PASSED`；
- 结构体尺寸（`minimc_header_t` 12字节、`minimc_temp_wire_payload_t` 16字节）与各字段字节偏移（`sof_1=0`, `sof_2=1`, `flags=4`, `current_temp=0`, `raw_adc=4`, `status=6`, `tick=8`）经编译期 `_Static_assert` 严格断言通过；
- Fast DDS IDL `RawTempTelemetry` 字段与 C 语言结构体 100% 逐字段对齐。

---

### 4.3 独立黄金预期与负向健壮性运行器 (`run_twin_cases.py`)

执行命令：
```bash
python3 test_harness/static_checks/twin/run_twin_cases.py
```
执行结果：
```text
========================================================================
TWIN-03 Independent Golden Expectation Test Suite Execution
========================================================================
[PASS] PERIODIC-100MS-SAMPLING          : Verified 10 periodic samples with 100ms cadence
[PASS] NOZZLE-4CH-AND-BED-TEMPS         : Verified 4 nozzles and 4 beds
[PASS] SENTINELS-AND-FRESHNESS          : Sentinels and freshness rules verified
[PASS] NEGATIVE-ROBUSTNESS-CASES        : Verified 9 negative telemetry cases
[PASS] DBUS-CONTROL-AND-ERRORS          : Verified 27 D-Bus method and signal test cases
[PASS] HTTP-REST-AND-SSE-EVENTS         : Verified 11 HTTP REST and SSE golden cases
------------------------------------------------------------------------
Total Suites: 6, Passed: 6, Failed: 0
```
核心预期验证覆盖：
1. **Fast DDS 100ms 周期采样**：10 组连贯递增帧验证序列号单调递增、tick 严格按 100ms 推进、物理帧 CRC-16/CCITT-FALSE 校验无误；
2. **4路喷嘴温度覆盖**：
   - 喷嘴通道 1（低温极限）：-40.000°C (-400 deci_c / -40000 milli_c, raw_adc=15)
   - 喷嘴通道 2（室温常温）：25.000°C (+250 deci_c / +25000 milli_c, raw_adc=1850)
   - 喷嘴通道 3（标准工况）：210.000°C (+2100 deci_c / +210000 milli_c, raw_adc=3200)
   - 喷嘴通道 4（高温上限）：500.000°C (+5000 deci_c / +500000 milli_c, raw_adc=4080)
3. **热床与机箱温度**：25°C、60°C、100°C、机箱 45°C 与 65°C 正例及转换断言；
4. **离线/高位故障哨兵**：
   - 开路故障：wire `0x7FFF` (+32767), DDS `2147483647` (`AISOC_TEMP_MILLIC_FAULT`), REST/SSE `null` + `STATUS_OPEN` + `QUALITY_FAULT`
   - 短路故障：wire `0x7FFF` (+32767), DDS `2147483647` (`AISOC_TEMP_MILLIC_FAULT`), REST/SSE `null` + `STATUS_SHORT` + `QUALITY_FAULT`
   - 离线/超时：wire `0x7FFE` (+32766), DDS `2147483646` (`AISOC_TEMP_MILLIC_OFFLINE`), REST/SSE `null` + `STATUS_TIMEOUT` + `QUALITY_FAULT`
5. **D-Bus 统一控制准入与错误码**：27 组测试断言，覆盖 ForwardInterface（`TriggerQuery`、`GetPortStatus`、`EmergencyStop`、`ResetLink`）、DeviceInterface（`GetSnapshot`、`RequestImmediateSample`、`GetDeviceState`、`EmergencyStop`）及 HmsInterface（`GetActiveAlarms`、`ClearAlarm`），强校验错误码（`InvalidArgument`, `Timeout`, `DeviceBusy`, `EmergencyStopped`）；
6. **HTTP REST 与 SSE 事件流**：11 组端点与推流断言，强类型检验 `temp_update`, `motion_update`, `status_change`, `alarm_event`。

---

### 4.4 帧捕获与时序对账工具单元测试 (`test_twin_capture.py`)

执行命令：
```bash
python3 -m unittest test_harness/hil/twin_capture/test_twin_capture.py
```
执行结果：
```text
........
----------------------------------------------------------------------
Ran 8 tests in 0.006s

OK
```
功能与防御能力覆盖：
- 流式连续报文多帧拆解与截断保护；
- 噪声字节丢弃与 SOF 同步头自动锁定；
- 100ms 周期采样抖动统计（mean, min, max, std_dev, jitter spread）与超限判定（>15ms 判定为 violation）；
- 虚拟环境帧（VMware Twin）与物理台架帧（HIL Physical Bench）基于序列号的多维度比对，包括漏帧、乱序与温度差异对账；
- 全脚本函数规模（$\le 50$ 行）与参数个数（$\le 4$ 个）AST 自动化静态审查。

---

### 4.5 存量回归测试与任务依赖图检查

1. **存量级联查询用例与探针工具测试**：
   ```bash
   python3 test_harness/static_checks/cascade/run_query_cases.py --check-vectors
   python3 -m unittest test_harness/hil/tests/test_probe_tools.py
   ```
   结果：100% PASS，存量测试未受任何破坏。

2. **全局任务拓扑图无损验证**：
   ```bash
   PYTHONDONTWRITEBYTECODE=1 python3 project-control/tools/check_task_graph.py --workspace .
   ```
   结果：`canonical_task_count: 108, errors: []`, 退出码 0，无任何依赖环或死锁。

---

## 5. 硬性门禁与编码规范符合性证明

根据 `project-control/.agents/rules/c_cpp_coding_standard.md`，对本次新增的所有自研交付代码进行了全维度自检：

| 规范条目 | 门禁约束 | 执行证据与实测数据 | 结论 |
| :--- | :--- | :--- | :--- |
| **函数规模** | 严禁编写 $>50$ 行的非结构体函数 | 通过 `ast.parse` 静态分析所有 Python 函数（最大函数 47 行）；`check_layout.c` 最大函数 40 行，均 $\le 50$ 行 | **100% 达标** |
| **入参个数** | 严禁编写 $>4$ 个入参的非结构体函数 | 所有函数入参数量 $\le 4$ 个（多数为 1~2 个参数） | **100% 达标** |
| **零动态堆分配** | C/C++ 禁用 `new`, `delete`, `malloc`, `free` 及动态 STL 容器 | `check_layout.c` 完全使用栈变量与静态常量，零动态内存调用 | **100% 达标** |
| **现代 C++ 规范** | `-fno-exceptions -fno-rtti`，显式两阶段初始化 | 经 G++ C++17 编译，完全禁用异常与 RTTI，零告警 | **100% 达标** |
| **指针防御与安全** | 入参在前出参在后，只读加 `const`，入口防御性校验 | 所有指针入参均有 Guard Clause 校验；解引用分步执行 | **100% 达标** |
| **硬件/外设超时** | 严禁 `while(!FLAG)` 空死等循环 | `twin_capture_analyzer.py` 与 C 验证程序均设定有界步长与显式终止条件 | **100% 达标** |

---

## 6. 两阶段验收能力分账

按照项目要求，本任务资产明确区分软件仿真与硬件在环，不将离线向量冒充实板实测：
- **纯软件/离线断言（Stage 1 孪生开发）**：`golden_telemetry_cases.json`, `golden_dbus_cases.json`, `golden_sse_cases.json`, `validate_schemas.py`, `run_twin_cases.py`。由各模块在 VMware 或宿主环境中用于单元测试、中间件通信契约测试与 CI 门禁；
- **双环境时序对账（Stage 1/2 对账工具）**：`twin_capture_analyzer.py`。既支持读取 VMware 虚拟串口/PTY 捕获流，也支持读取真实板卡物理 UART 捕获流，并输出两阶段 100ms 周期抖动偏差与一致性报告；
- **后续硬件台架验收（Stage 2 实板实物）**：保留给 `TWIN-12`（VMware + 真实 MC/TH）与 `TWIN-14`（SoC 实板实屏）。

---

## 7. 结论与转交

TWIN-03 独立黄金预期与两阶段故障验收用例已全部开发完成，自检 100% 通过。
测试资产已成功冻结，具备为 `TWIN-05` (ENG-DDS), `TWIN-06` (ENG-DBUS), `TWIN-07` (ENG-FWD), `TWIN-08` (ENG-STATE), `TWIN-09` (ENG-NET), `TWIN-10` (ENG-UI), `TWIN-15` (ENG-MC), `TWIN-16` (ENG-TH) 提供权威前置裁决输入的能力。

提请系统架构师（`ARCH`）启动独立会话复核，并交由协调员（`COORD`）进行后续任务派单流转。
