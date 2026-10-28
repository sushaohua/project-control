# CR-10 独立真实 HIL 验收复验报告

| 字段 | 属性 / 内容 |
| :--- | :--- |
| **任务卡片** | `CR-10` (独立真实 HIL 验收复验) |
| **所属计划** | `PLAN-CASCADE-RECOVERY-20261027 v1.1` / `workflow-replan-20261028` |
| **主责角色** | `QA` (独立测试与质量验收) |
| **独立审阅会话** | `codex-qa-cr-10-hil` (Model: `gpt-6-luna`, Role: `QA`) |
| **复核审阅会话** | `codex-cr-10-arch` (Model: `gpt-6-luna`, Role: `ARCH`) |
| **物理环境** | 物理台架 HIL (`VMware Ubuntu 22.04 @ 192.168.77.134` + `/dev/ttyUSB0` 921600/115200 真实串口) |
| **硬件资产** | MC (`AT32F435VGT7`, UID `053023904C96C0000D819709`) + TH (`AT32F423CCT7`, UID `053173C58023C000127C0707`) |
| **详细运行记录** | [`runs/run_01/result.md`](runs/run_01/result.md) (SHA256: `ed6b0f5824c781de84acbc7d19fd3c6deb929371d1bfd16b2df3ef9e4713647d`) |
| **验收结论** | **APPROVED (双端物理在环验证 100% 通过，四正用例与两负用例全部闭环，零模拟零虚拟化)** |

---

## 1. 验收范围与门禁遵循核查

依据 `project-control/.agents/rules/codex_qa_review.md` 铁律，对本票交付成果执行门禁审计：

1. **HW-G1 (真实硬件拓扑在环)**:
   - AP 与 MC 通过 CH340 物理串口连接，MC 与 TH 通过板间跳线连接（USART6 ↔ USART1）。
   - 探针自发现对账通过，双板芯片 UID、栈顶与 Flash 规格全部核验无误。
2. **HW-G2 (Flash 保护与基地址规范)**:
   - MC 运行于 `0x08020000` (HW-G2 门禁保护 Bootloader `0x08000000~0x0801FFFF`)。
   - TH 运行于 `0x08004000` (HW-G2 门禁保护 Bootloader `0x08000000~0x08003FFF`)，Sector 127 具有有效签名锚点。
3. **HW-G5 (零虚拟化与物理串口保真)**:
   - 严禁使用 PTY 伪终端替代真实硬件；全部命令均经由 `/dev/ttyUSB0` 发送至单片机硬件，且包含原始 Raw Hex TX/RX 帧对账。
4. **HW-G6 (路由原生透明性与身份唯一性)**:
   - MC 严格执行原生透明路由（递减 Hop Limit、置位 ROUTE_IS_ROUTED、重算 CRC），零业务解包。
   - TH 真实自报其唯一硬件身份（`boot_id: 0x8877AA55`，`git_commit: 0x6356C05A`），杜绝伪造。

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
| **BENCH-40** | 40 轮实物压力测试 | 全链路 | 丢包率 0.0%，MC 平均 RTT 7.59ms，TH 平均 RTT 8.44ms | **PASS** |

---

## 3. ARCH 复核审查意见

独立 ARCH 审阅者对 QA 验收记录 [`runs/run_01/result.md`](runs/run_01/result.md) 进行复核：
1. **真实性确认**：QA 提交的 40 轮测试数据、SWD 寄存器切断/恢复现场均来自物理台架真实采集，时戳和时延符合物理波特率和 DMA 传输延迟模型。
2. **契约闭环**：完全满足 `ICD-CASCADE-READONLY-20261027` 与 `CONTRACT-CASCADE-QUERY-20261027` 契约定义。
3. **架构决议**：同意签署 `APPROVED`，允许解锁任务流向 `CR-11`（按范围接受、交接与版本锁定）。

---

## 4. 下游交付动作

- 任务卡 `CR-10.md` 标记完成（`Done`）。
- 主看板 `KANBAN.md` 投影状态更新。
- 移交下一卡 `CR-11` 开展版本锁定与交接工作。
