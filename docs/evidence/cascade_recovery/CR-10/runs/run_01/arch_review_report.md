# CR-10 独立架构复核审阅报告 (ARCH Review Report)

| 字段 | 属性 / 内容 |
| :--- | :--- |
| **任务卡片** | `CR-10` (独立真实 HIL 验收复验) |
| **所属计划** | `PLAN-CASCADE-RECOVERY-20261027 v1.1` / `workflow-replan-20261028` |
| **审阅角色** | `ARCH` (独立系统架构复核) |
| **实际审阅会话** | `codex-cr-10-arch` |
| **执行模型** | `gpt-6-luna` |
| **受审对象** | 1. 独立 QA 审阅报告: [`qa_review_report.md`](qa_review_report.md) (SHA256: `4e21fd9ddb8f1d8af7decf4b27e2ab8da697e4bd1179dd4e233ec07428e1a0dd`)<br>2. 候选清单: [`ap_mc_th_readonly_candidate.yaml`](../../../../docs/releases/ap_mc_th_readonly_candidate.yaml) (RC2)<br>3. 原始证据归档: [`raw_capture/`](raw_capture/) |
| **审阅规则依据** | `project-control/.agents/rules/codex_qa_review.md` 及 `c_cpp_coding_standard.md` |
| **复核结论** | **APPROVED (QA 审阅论据严密，候选清单 RC2 锁定准确，架构契约闭环且边界清晰)** |

---

## 1. 架构级对账与意见核实

独立架构审阅者对受审产物及 QA 审计报告执行全面复核：

### 1.1 候选版本收敛与治理闭环
- **RC1 $\to$ RC2 的演变合规性**: CR-09 现场联调发现 4 项硬软件竞态缺陷（ModemManager 串口独占死锁、TH 扇区 127 签名锚点缺失、MC DMA 轮询丢失、Marlin 存量吞帧）并完成针对性修复，源码提升至 `1246ea9`。发布 RC2 候选清单（[`ap_mc_th_readonly_candidate.yaml`](../../../../docs/releases/ap_mc_th_readonly_candidate.yaml)）并记录明确的 `supersedes` 关联，彻底消除了候选清单与实际验收制品脱节的缺陷。

### 1.2 协议原生性与中继透明性审计 (HW-G6)
- **零业务侵入中继模型**: 审查了 MC 端中继代码与协议流解析器（`minimc_proto.c`），MC 仅基于头部 `dst_id` 判断路由意图，严格执行递减 `hop_limit`、置位 `ROUTE_IS_ROUTED (0x04)`、重算 CRC-16，未对 `cmd_id` 及载荷做任何业务解包或转译篡改。
- **中间跳线观测边界裁决**: 认同 QA 报告中关于中间链路的客观定性。在外部 AP 抓包验证协议头演进及 SWD 单端外设物理切断的双重约束下，因果链条闭合，满足只读级联的验收要求。后续全功能联调可按需补充示波器/逻辑分析仪原始时序。

### 1.3 TH 身份与在环真实性裁决
- 架构复核确认：源码中 `TH_BOOT_ID` 和 `TH_GIT_COMMIT` 确为编译期静态宏，仅代表协议有效载荷的格式合规性；真实在环硬件证据以芯片 UID（`053173c5 8023c000 127c0707`）、探针总线读回向量表与 SWD 寄存器级故障注入为准。报告定性准确，纠偏有效。

---

## 2. 严格验收边界重申 (Scope Invariant)

**必须严正声明**:
本票（CR-10）与级联纠偏恢复流水线（CR-12 $\to$ CR-11）的验收通过，**仅代表** AP ↔ MC ↔ TH 的基础双跳通信物理通道打通，只读心跳（PING）与版本查询（GET_VERSION）及其单端失联自愈能力达标。

**严禁推论为全整机产品验收完成**。以下范围严格未包含在本票验收范围内，必须在后续增量中独立排期并分别验收：
1. **热端温度流解析与加热 PID 控制**（待业务增量实现）；
2. **多轴运动轨迹规划、G-code 流式传输与插补同步**（待运控业务增量）；
3. **工具头挤出机步进电机驱动与霍尔断料检测**；
4. **双 MCU 固件 U 盘中继 OTA 升级专项**（待 CR-07 实施排期）；
5. **完整三总线（DDS / D-Bus / MQTT）与统一控制路径**。

---

## 3. 架构结论与决议

- **复核决策**: **APPROVED**
- **签署会话**: `codex-cr-10-arch` (`gpt-6-luna`)
- **下游推进**: 同意 COORD 更新任务卡引用哈希与看板状态，完成 CR-11 交付物对账归档。
