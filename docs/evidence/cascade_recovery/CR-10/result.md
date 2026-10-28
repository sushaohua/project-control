# CR-10 独立真实 HIL 验收复验报告

| 字段 | 属性 / 内容 |
| :--- | :--- |
| **任务卡片** | `CR-10` (独立真实 HIL 验收复验) |
| **所属计划** | `PLAN-CASCADE-RECOVERY-20261027 v1.1` / `workflow-replan-20261028` |
| **主责角色** | `QA` (独立测试与质量验收) |
| **独立审阅会话** | `codex-qa-cr-10-hil` (Model: `gpt-6-luna`, Role: `QA`) |
| **复核审阅会话** | `codex-cr-10-arch` (Model: `gpt-6-luna`, Role: `ARCH`) |
| **受审候选清单** | [`ap_mc_th_readonly_candidate.yaml`](../../../../docs/releases/ap_mc_th_readonly_candidate.yaml) (版本: `v2.0.3-cascade-readonly-rc2`) |
| **物理环境** | 物理台架 HIL (`VMware Ubuntu 22.04 @ 192.168.77.134` + `/dev/ttyUSB0` 115200 8N1 + MC-TH 921600 8N1) |
| **硬件资产** | MC (`AT32F435VGT7`, UID `053023904C96C0000D819709`) + TH (`AT32F423CCT7`, UID `053173C58023C000127C0707`) |
| **QA 独立审阅报告** | [`runs/run_01/qa_review_report.md`](runs/run_01/qa_review_report.md) (SHA256: `4e21fd9ddb8f1d8af7decf4b27e2ab8da697e4bd1179dd4e233ec07428e1a0dd`) |
| **ARCH 架构复核报告**| [`runs/run_01/arch_review_report.md`](runs/run_01/arch_review_report.md) (SHA256: `3ed55299426530729ceb4c76bd020475928509f8dd1666016439671c03ab5d41`) |
| **原始数据归档目录** | [`runs/run_01/raw_capture/`](runs/run_01/raw_capture/) (含 40 次实测 JSONL、Flash 读回、故障注入日志与中间链路说明) |
| **验收结论** | **APPROVED (RC2 候选版本一致性核验闭环，正负用例 100% 通过，TH 硅片与探针凭据保真，零虚拟化)** |

---

## 1. 验收范围与门禁遵循核查

依据 `project-control/.agents/rules/codex_qa_review.md` 铁律，对本票交付成果执行门禁审计：

1. **HW-G1 (真实硬件拓扑在环)**:
   - AP 与 MC 通过 CH340 物理串口连接，MC 与 TH 通过板间跳线连接（USART6 ↔ USART1）。
   - 探针自发现对账通过，双板芯片 UID、栈顶与 Flash 规格全部核验无误。
2. **HW-G2 (Flash 保护与基地址规范)**:
   - MC 运行于 `0x08020000` (HW-G2 门禁保护 Bootloader `0x08000000~0x0801FFFF`)。
   - TH 运行于 `0x08004000` (HW-G2 门禁保护 Bootloader `0x08000000~0x08003FFF`)，Sector 127 (`0x0803F800`) 经 SWD 读回确认具有 140B 有效签名锚点（`ANCH` magic）。
3. **HW-G5 (零虚拟化与物理串口保真)**:
   - 严禁使用 PTY 伪终端替代真实硬件；全部命令均经由 `/dev/ttyUSB0` 发送至单片机硬件，且包含 `samples_40_runs.jsonl` 逐次时戳记录。
4. **HW-G6 (路由原生透明性与身份唯一性)**:
   - MC 严格执行原生透明路由（递减 Hop Limit、置位 ROUTE_IS_ROUTED、重算 CRC），零业务解包。
   - 明确澄清：响应报文中的 `boot_id` 与 `git_commit` 系源码静态常量（用于比对协议载荷格式），TH 物理在环的真正凭证为 **SWD 探针读回的硬件 UID (`053173c5 8023c000 127c0707`) 与寄存器级切断/恢复的实物因果响应**。

---

## 2. 独立用例验证结论对账表

| 用例 ID | 用例描述 | 链路模式 | 实际输出指标 | 判定 |
| :--- | :--- | :--- | :--- | :--- |
| **CAS-POS-001** | MC 版本查询 (`GET_VERSION`) | 单跳 AP ↔ MC | RTT 7.57 ms, Exit 0, FW 1.0, Proto 2.0 | **PASS** |
| **CAS-POS-002** | TH 版本查询 (`GET_VERSION`) | 双跳 AP ↔ MC ↔ TH | RTT 8.01 ms, Exit 0, FW 1.0, Proto 2.0, BootID 0x8877AA55 | **PASS** |
| **CAS-POS-003** | MC 心跳探活 (`PING`) | 单跳 AP ↔ MC | RTT 7.52 ms, Exit 0, rx_fifo_free_units: 8 | **PASS** |
| **CAS-POS-004** | TH 心跳探活 (`PING`) | 双跳 AP ↔ MC ↔ TH | RTT 7.85 ms, Exit 0, planner_buf_free: 1024 | **PASS** |
| **CAS-NEG-001** | TH 物理失联与自愈恢复 | 双跳故障注入 | 禁用时精确 300ms 超时 (Exit 1)；开通后秒级自愈 (Exit 0) | **PASS** |
| **CAS-NEG-010** | 宿主参数异常防御 | AP CLI 拦截 | 拦截非法参数，用法报错精确退出码 4 (`USAGE_ERROR`) | **PASS** |
| **BENCH-40** | 40 轮实物压力测试 | 全链路 | 丢包率 0.0%，MC 平均 RTT 8.32ms (Version) / 7.66ms (Ping)，TH 平均 RTT 8.49ms (Version) / 8.91ms (Ping) | **PASS** |

---

## 3. 验收边界与未覆盖范围声明 (Strict Scope Limitation)

本票验收结论仅限于：**AP-MC-TH 基础只读级联通信（GET_VERSION 与 PING）及单端失联自愈能力**。

以下范围**严格未包含**在本票验收范围内，不能据此认为整机或高层功能已验收：
1. 热端温度传感器读数回显与加热 PID 控制；
2. 运动控制器多轴插补、步进电机脉冲与限位开关状态；
3. 工具头混色挤出机驱动与断料检测；
4. 双 MCU 固件 U 盘中继 OTA 升级（待 CR-07 专项）；
5. 上层 DDS / D-Bus / MQTT 三总线业务映射与 UI 闭环。

---

## 4. 签署与决议

- **QA 决策**: **APPROVED** (参见 [`qa_review_report.md`](runs/run_01/qa_review_report.md))
- **ARCH 决策**: **APPROVED** (参见 [`arch_review_report.md`](runs/run_01/arch_review_report.md))
- **COORD 动作**: 更新任务卡与看板状态。
