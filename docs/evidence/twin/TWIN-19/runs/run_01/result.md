# TWIN-19 全机 HMS 错误码体系、双级急停联动与脱敏诊断导出交付自检报告 (Run 01)

| 属性 | 内容 |
| :--- | :--- |
| **任务卡片** | `TWIN-19` (全机 HMS 错误码体系、双级急停联动与脱敏诊断导出) |
| **所属工作包** | `TASK-008` (实现整机状态和统一指令准入) |
| **执行角色** | `ENG-STATE` (协力 `ENG-FWD`, `INTEGRATOR`) |
| **当前轮次** | `run_01` (HMS 分层错误码、状态机双级急停联动与一键脱敏导出工具) |
| **前置依赖** | `TWIN-02` (Done) |
| **执行状态** | **Completed (HMS 模型、状态机双级急停联动、脱敏导出工具及全量正反用例 100% 验证通过)** |

---

## 1. 核心架构与功能实现 (Architecture & Implementation)

依据 `PM:FEAT-SAF-001`（双级急停）、`PM:FEAT-SAF-002`（HMS 统一错误码）与 `PM:FEAT-MFG-003`（脱敏诊断导出）规划，完成了全机健康监控与安全保护系统交付：
1. **统一整机分层 HMS 错误码体系 (`hms_types.h`)**：
   - 按照 16-bit `0xSSEE` 规范分层定义全机故障代码：
     - `0x1000` 串口与协议通信故障 (`COMM_UART_DISCONNECT`, `COMM_CRC_FAIL`, `COMM_TIMEOUT`)；
     - `0x2000` 热床与工具头温控故障 (`TH_SENSOR_OPEN/SHORT`, `BED_SENSOR_OPEN/SHORT`, `OVERTEMP`, `THERMAL_RUNAWAY`)；
     - `0x3000` 供料与挤出故障，严格继承 [`TWIN-18`](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/specs/mcu_motion_leveling_filament_interface_survey_20261029.md) 的断料告警 **`0x3001`** (`HMS_ERR_FILAMENT_RUNOUT`)；
     - `0x4000` 运动控制与回零故障 (`HOMING_FAILED_X/Y/Z`, `DRIVER_FAULT_STEPPER`)；
     - `0x5000` 系统安全与急停事件 (`HARD_ESTOP_ACTIVE`, `SOFT_ABORT_ACTIVE`)；
   - 4 级严重度评级：`INFO` (1), `WARNING` (2), `ERROR` (3), `FATAL` (4)。
2. **双级急停联动状态机管理 (`hms_manager.c`, `hms_manager.h`)**：
   - **一级软级急停（Level 1 Soft Pause / Abort）**：
     - 触发条件：断料、用户非破坏性请求、轻度超时；
     - 行为：受控降速停车，停转挤出机，维持加热与通信；
   - **二级硬级急停（Level 2 Hard E-stop / Kill）**：
     - 触发条件：过温、热失控、强电急停指令；
     - 行为：瞬间切断加热占空比为 0% (`heater_duty_percent = 0U`)，断电步进电机，状态机永久锁死熔断；
     - **安全互锁保护**：未排除致命故障（`FATAL`）时，严禁普通复位急停，除非人工发起带强制标记的特权复位。
3. **一键脱敏诊断包导出工具 (`export_diag_pack.py`)**：
   - 自动化收集系统运行环境元数据、微服务日志与遥测快照；
   - **硬性安全防泄露过滤机制**：内置多层正则表达式，100% 自动脱敏抹除 Wi-Fi 密码（`psk=`, `wpa_passphrase=`）、Bearer/Token 凭据、私钥证书（`-----BEGIN RSA PRIVATE KEY-----`）以及各类口令敏感字段；
   - 自动生成打包清单 `manifest.json` 与 SHA-256 防篡改摘要，压缩为 `.tar.gz` 诊断包。
4. **硬性编码规范合规**：
   - 所有自研 C 函数长度 $\le 39$ 行（远优于 $\le 50$ 行门禁）；
   - 函数入参 $\le 3$ 个；
   - 零动态堆内存分配（静态固定 16 容量告警表 `hms_alarm_entry_t alarms[16]`）。

---

## 2. 交付物清单与 SHA-256 校验码

| 交付文件路径 | 类型与描述 | SHA-256 校验码 |
| :--- | :--- | :--- |
| `soc-ap/core/state/hms/hms_types.h` | 结构体与常量定义（静态断言校验尺寸） | `0112412f5b1a6800e2b5c855f72ceb8f6999a24936e9c9a7d6645852aa0ee354` |
| `soc-ap/core/state/hms/hms_manager.h` | HMS 管理与双级急停联动 API 声明 | `68f4c915add5d53b9380b412ca4376e70f4c2da2be120b5947b5a8544a6f7bb4` |
| `soc-ap/core/state/hms/hms_manager.c` | 状态机核心管理实现与安全互锁逻辑 | `abf68f9a144842ebec851b229b4fec7570c7c1022b586f2531544fd3af878bed` |
| `soc-ap/core/state/hms/test_hms_manager.c` | C/C++ 状态机及急停互锁单元测试 | `c791499a09302748dd30ec933ac9137aea48364da2d4e96518e2e2c0f1fb3a47` |
| `soc-ap/tools/diag/export_diag_pack.py` | 一键脱敏诊断导出工具脚本 | `349bcf19f38b49bc4a1d2e59eddc2ce085605fd8be4f20daf610fb7221f3721d` |
| `soc-ap/tools/diag/test_diag_export.py` | 诊断包打包与敏感凭据脱敏断言测试 | `91732d1f4ba5d3d470b1d84dd051cc74f5efa6069f35320582ddd26a5964c67d` |

---

## 3. 正反用例与验证实测结果

### 3.1 HMS 状态机测试输出 (C11 与 C++17 双标准全通)
```
=== Starting TWIN-19 HMS System Acceptance Tests ===
[PASS] test_init_and_raise_alarm (告警去重、严重度等级晋升及软急停联动通过)
[PASS] test_fatal_and_hard_estop_escalation (过温硬急停升格、致命故障防盲复位互锁通过)
[PASS] test_clear_alarms (告警针对性清除与最高严重度动态重算通过)
[PASS] test_clear_all_preserves_fatal (批量清除普通告警并锁定保留致命告警通过)
[PASS] test_manual_trigger_estop (手动触发一级软急停与二级硬急停状态通过)
[PASS] test_table_full_protection (16项定长静态表溢出防御通过)
[PASS] test_json_summary (JSON 摘要序列化通过)
=== ALL TWIN-19 TESTS PASSED SUCCESSFULLY (7/7 Suites) ===
```

### 3.2 诊断导出与脱敏断言实测输出
```
=== Starting TWIN-19 Diagnostic Export & Security Tests ===
[PASS] Positive export and manifest verified (归档结构、manifest.json 及 SHA-256 完整性生成通过)
[PASS] Negative security credentials redaction assertion verified (Wi-Fi 密码、Token、私钥证书注入后 100% 被替换脱敏，零明文泄露)
=== ALL TWIN-19 DIAGNOSTIC TESTS PASSED SUCCESSFULLY ===
```
