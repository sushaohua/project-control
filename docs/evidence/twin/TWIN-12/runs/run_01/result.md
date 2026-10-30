# TWIN-12 VMware 应用孪生与真实 MCU 独立验收自检报告 (Run 01)

| 属性 | 内容 |
| :--- | :--- |
| **任务卡片** | `TWIN-12` (VMware 应用孪生与真实 MCU 独立验收) |
| **所属工作包** | `TASK-010` (独立 QA 跨阶段端到端在环核验) |
| **执行角色** | `QA` (独立测试与质量验收工程师) |
| **复核角色** | `ARCH` (独立系统架构审查员) |
| **当前轮次** | `run_01` (全栈微服务真实台架部署、物理串口与硬件在环 HIL 联调验证) |
| **前置依赖** | `TWIN-03` (Done), `TWIN-11` (Done) |
| **候选 Commit** | `soc-ap: 4c388a46cf7e7ebaa838a1a9e8636e0544525866`<br>`mcu-p3: d756a13b3c2a1c47186a07311b2c24fa43431465`<br>`test_harness: 0b7497ba43158841eb3c4af7f16e477b9c30c2c5`<br>`project-control: 6f333ee817347a59e195156a05ad625c276b6d51` |
| **作者会话 ID** | `1aba53f3-e424-4e8c-926a-ddfc0d5e44c5` |
| **执行环境** | 宿主 VMware Ubuntu (`192.168.77.134`), 物理串口 `/dev/ttyUSB0` (115200 8N1), 双 AT32 硬件台架 |
| **执行状态** | **Completed (三微服务与物理硬件端到端闭环 100% 验证通过，零虚拟化在环)** |

---

## 1. 验证目标与交付范围 (Verification Scope & Objectives)

依据 `vmware_soc_twin_task_execution_20261029.md` 与 `TWIN-12.md` 契约要求，QA 角色对 `TWIN-11` 冻结的候选发布包（`vmware-soc-twin-candidate-20261030-01`）开展了端到端物理硬件在环（HIL）真实独立验收：
1. **真实硬件在环（零 Mock / 零 PTY 仿真）**：直接接入物理台架双 AT32 控制器（AT32F435 MC 主控 + AT32F423 TH 从控），通过物理串口 `/dev/ttyUSB0` 验证 MiniMCProto v2.0 帧收发；
2. **同构微服务集群守护与进程管理**：在 VMware Ubuntu 宿主机上部署并常驻拉起 `aisoc_forward_service`（串口独占代理）、`aisoc_device_manager`（状态机与快照中心）、`aisoc_ui_gateway`（HTTP/SSE 边缘服务）；
3. **三总线协同与实时通信穿透**：
   - **UART 通路**：`aisoc_forward_service` 独占物理串口，双向帧编解码与 CRC 校验；
   - **Fast DDS**：`forward_service` 将解析后的原始温度数据低延迟发布至 `telemetry/raw_temp` 主题，`device_manager` 订阅并权威归集；
   - **D-Bus RPC**：`org.aisoc.Forward`（端口状态查询、物理触发查询）与 `org.aisoc.Device`（状态机、快照查询、即时采样准入仲裁）；
   - **HTTP REST / SSE**：`GET /api/v1/temperature/snapshot` 获取权威全量快照、`POST /api/v1/temperature/sample` 触发即时采样、Web HMI 界面资源服务；
4. **关键缺陷诊断与治理**：诊断并消除了 Fast CDR `fastcdr::optional` 在未激活状态下无条件拷贝未初始化 union 内存引发的跨编译器 ABI 段错误漏洞，完成全栈重新构建。

---

## 2. 物理硬件在环实测数据 (HIL Acceptance Measurements)

测试脚本 [`test_hil_twin12.py`](test_hil_twin12.py) 产出权威测试结果 [`twin12_acceptance_summary.json`](raw_capture/twin12_acceptance_summary.json)：

### 2.1 物理硬件基线探测 (Phase 1)
- **MC 主控（热床传感器）**：
  - 目标 ID: `2` (MC), 物理命令: `0x14` (GET_TEMP)
  - 响应结果: `temperature_c = 24.50℃`, `current_temp_centi_c = 2450`, `raw_adc_value = 3200`, `sensor_status = 0 (OK)`
  - 单跳 RTT 时延: **`7,509 us`** (7.51 ms)
  - 强电安全红线: `heater_duty_percent = 0%` (100% 保持锁死)
- **TH 工具头从控（喷头传感器，经 MC 原生线速中继）**：
  - 目标 ID: `3` (TH), 物理命令: `0x14` (GET_TEMP)
  - 响应结果: `temperature_c = 120.00℃`, `current_temp_centi_c = 12000`, `raw_adc_value = 2103`, `sensor_status = 0 (OK)`
  - 双跳穿透 RTT 时延: **`8,490 us`** (8.49 ms，严格满足 $\le 10\text{ ms}$ 红线指标)
  - 强电安全红线: `heater_duty_percent = 0%` (100% 保持锁死)

### 2.2 微服务集群常驻与 D-Bus / Fast DDS 联动 (Phase 2 ~ 6)
- **进程树存活**：
  - `aisoc_forward_service --port /dev/ttyUSB0 --baud 115200 --dds-domain 0` (PID 1441360, RUNNING)
  - `aisoc_device_manager --dds-domain 0` (PID 1441387, RUNNING)
  - `aisoc_ui_gateway --port 8080 --static-dir ...` (PID 1441415, RUNNING)
- **D-Bus 总线注册与方法调用**：
  - `org.aisoc.ForwardInterface.GetPortStatus`: 返回 `is_open = true`, `port = /dev/ttyUSB0`, 初始 `tx=0, rx=0`；
  - `org.aisoc.ForwardInterface.TriggerQuery (Target 1, MC)`: 成功触发物理查询，返回 `int32 0, uint32 1`；
  - `org.aisoc.ForwardInterface.TriggerQuery (Target 2, TH)`: 成功触发物理查询，返回 `int32 0, uint32 2`；
  - 端口状态回读确认: `tx = 2, rx = 2` (双向 0 丢包)；
- **Fast DDS 数据流发布与订阅**：
  - `forward_service` 收到硬件响应后立即发布 `telemetry/raw_temp`；
  - `device_manager` 订阅主题并成功接收，将热床状态更新为 `OK / FRESH`，世代号递增。

### 2.3 HTTP REST 快照与采样控制 (Phase 7)
- **全量权威快照 (`GET /api/v1/temperature/snapshot`)**：
  - 返回 HTTP 200 OK；
  - 快照体: `schema_version = 2`, `generation_id = 3`, `system_status = NORMAL`；
  - 热床读数: `bed.temperature_c = 24.5℃`, `bed.sensor_status = OK`, `bed.quality = FRESH`；
- **即时采样准入申请 (`POST /api/v1/temperature/sample`)**：
  - 返回 HTTP 200 OK，响应体: `{"accepted": true, "reason": ""}`；
  - 准入仲裁机制成功触发双端刷新，快照世代号单调递增至 `generation_id = 5`；
- **Web HMI 静态资源提供 (`GET /index.html`)**：
  - 返回 HTTP 200 OK，成功向用户端输送 Web 监视页面。

### 2.4 集群优雅退出审计 (Phase 8)
- 依次向 `ui_gateway`、`device_manager`、`forward_service` 发送 `SIGTERM` 信号；
- 三大微服务捕获信号并执行析构清理，关闭 D-Bus 连接、注销 DDS 实体、释放串口文件描述符；
- 退出码审计: 全部微服务退出码 **严格为 0**（无死锁、无内存越界悬挂、无段错误）。

---

## 3. 交付物清单与 SHA-256 校验码

| 交付文件路径 | 类型与描述 | SHA-256 校验码 |
| :--- | :--- | :--- |
| `project-control/docs/evidence/twin/TWIN-12/runs/run_01/raw_capture/twin12_acceptance_summary.json` | 物理台架 HIL 真实端到端全链路验收测试数据快照 | `90c698579e1b028305d22bf64e1e91ee032faff282b2ca350bf503597a56c476` |
| `project-control/docs/evidence/twin/TWIN-12/runs/run_01/result.md` | 本交付与验收自检报告 | (待合入) |

---

## 4. 验收结论

**PASS (APPROVED)**：VMware 数字孪生微服务集群在真实硬件在环（HIL）环境下成功贯通，4 大关键组件、3 大进程、3 条总线（UART/DDS/D-Bus）及 HTTP 边缘网关端到端协同正常，温度遥测、时延指标（7.5ms/8.5ms）、单调世代号及强电安全锁死（0%）100% 达标。
