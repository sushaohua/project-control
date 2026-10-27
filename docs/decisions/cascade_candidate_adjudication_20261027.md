# AP-MC-TH 级联候选与历史结论裁决与限制登记

| 字段 | 属性 / 内容 |
| :--- | :--- |
| **文档 ID** | `DECISION-CASCADE-ADJUDICATION-20261027` |
| **生效时间** | 2026-10-27T17:05:00+08:00 |
| **裁决角色** | 唯一项目协调员（COORD） |
| **依据方案** | [`PLAN-CASCADE-RECOVERY-20261027` v1.1](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/planning/ap_mc_th_cascade_recovery_implementationplan_20261027_162003.md) |
| **复核报告** | [`PLAN-CASCADE-RECOVERY-20261027-review-02`](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/evidence/cascade_recovery_plan_20261027/runs/plan_review_02/qa_review_report.md) |
| **裁决状态** | **EFFECTIVE (已生效执行)** |

---

## 1. 裁决背景与执行授权

根据工程复盘与多方独立 Codex 审查证据，当前级联验证链路中存在“任务拆解遗漏、伪造从控响应、命令与协议定义冲突、测试工具存在防御漏洞”等多维缺陷。
方案 [`PLAN-CASCADE-RECOVERY-20261027` v1.1](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/planning/ap_mc_th_cascade_recovery_implementationplan_20261027_162003.md) 已经独立审查会话签发 `APPROVED`，本裁决作为 `CR-01` 的核心产物，由 COORD 依法对受影响的候选制品、历史结论及测试工装追加明确的撤回与限制标记。

---

## 2. 核心裁决与撤回清单

### 2.1 MCQ-0106 / MS-14 候选撤回裁决
* **涉及对象**：
  * 微任务：[`MCQ-0106`](file:///home/sushaohua/workspace/ai_soc_project/project-control/.agents/kanban/microtasks/mc_firmware/MCQ-0106.md)
  * 里程碑：[`MS-14`](file:///home/sushaohua/workspace/ai_soc_project/project-control/.agents/kanban/milestones/marlin_ms14_20261007_214108.md)
  * 产物版本：`mcu-p3` commit `a679133204ecbb81ad48694f5372c125db2e749f`（`fw_mc.bin` SHA256: `c11067d9e3fcc082ffff701a7041aeafcc81dfdfb2a18e32be6ccf6dd2d7eab5`）
* **撤回原因**：
  * **伪造从机响应**：在 `handle_th_query` 中，仅判断 USART6 收到任意文本或接收完成事件，即在 MC 本地硬编码伪造构造包含 `proto_ver: 2.0, fw_ver: 1.0` 的 MiniMCProto 应答帧，违反 `SPEC-PROTO-20261015-153000` §2.2 原生双向透明路由协议规定。
  * **中断死等风险**：在 USART2 IRQ 处理链路中忙等 USART6 完成，且抢占优先级同为 2，存在死锁隐患。
* **裁决决定**：
  1. **撤回该制品作为级联转发候选的有效性**，严禁下游任务（MS-15、MS-17、MS-21）消费该候选。
  2. **保留历史记录**：保留该 commit 及 QA 审查报告 `docs/evidence/mc_firmware/MCQ-0106/runs/run_20261027_01/qa_review_report.md` 作为工程过程证据。
  3. **替代任务挂接**：由后续治理票 **CR-05（MC 原生双向路由与中断解耦）** 与 **CR-06（TH 原生 MiniMCProto 响应）** 重新实现。

### 2.2 MS-07 物理闭环结论限制与待复验登记
* **涉及对象**：
  * 里程碑：[`MS-07`](file:///home/sushaohua/workspace/ai_soc_project/project-control/.agents/kanban/milestones/marlin_ms07_20261007_214108.md)
  * 产物版本：`soc-ap` commit `8d6c446cd3b0bac57054723ba7da9cd797ab4131`（`bin/minimc_host`）
* **限制原因**：
  * **命令定义冲突**：使用了非标准的 `0x03/L0` 作为主控版本查询，与规范命令定义存在歧义。
  * **主机校验漏洞**：经 8 组负例测试，AP 宿主程序对非预期帧存在容忍误报 SUCCESS 漏洞（F02）。
* **裁决决定**：
  1. **保留物理链路连通性事实**（真实台架 10/10 帧收发与 RTT 6.14ms 证据有效）。
  2. **对其协议合规性追加限制标记（Restricted）**，待 **CR-04（AP 健壮查询改造）** 与 **CR-05** 完成后，在 **CR-10** 中统一复验。

### 2.3 HIL 测试夹具（`device_discovery.py` & `probe_fault_injector.py`）使用限制
* **涉及对象**：
  * 仓库：`test_harness` commit `1d0861f199b92f9eac7c2103dfe80b207dbe4838`
  * 文件：[`test_harness/hil/tools/device_discovery.py`](file:///home/sushaohua/workspace/ai_soc_project/test_harness/hil/tools/device_discovery.py)、[`test_harness/hil/tools/probe_fault_injector.py`](file:///home/sushaohua/workspace/ai_soc_project/test_harness/hil/tools/probe_fault_injector.py)
* **限制原因**：
  * 经软件隔离反例测试（F23~F26），工具存在探针冲突判定不严谨、读原值失败仍写 0、异常未走 finally 恢复、写入失败未校验等防御漏洞。
* **裁决决定**：
  1. **保留工具代码与实操指南**，肯定其基于 SWD 寄存器控制物理接口与指纹自发现的工程方向。
  2. **追加门禁限制**：在完成治理子票 **CR-02T（HIL 工具防御漏洞治理与隔离软件负例验证）** 并获独立 QA 签署前，**严禁将该版本作为 CR-09/CR-10 正式物理验收的已接受夹具**。

---

## 3. 任务分类管控清单（保留、暂停、修复、复验）

依据上述裁决，当前工程任务状态全面重构如下：

### 3.1 保留的任务与资产（Retained - 证据有效，不受波及）
* **TASK-001 ~ TASK-005 已有前期需求与调研结论**：方案基线 B0、历史分析报告保留。
* **MiniMCProto 基础编解码（V2-P01 ~ V2-P04 系列已闭环单测）**：帧层编解码（`codec.cpp`、`parser.cpp` 基础帧格式）保留，参考向量库保留。
* **硬件连通性与实物台架接线状态**：双 ST-Link SWD 链路与 VMware USB 串口直通物理接线保持。

### 3.2 暂停的任务（Paused / Blocked - 阻断下游，等待前置修复）
* **MS-14（接通 MC 到 TH 双向业务代理）**：状态置为 `Blocked`，等待 CR-02 契约与 CR-05/06 产出。
* **MS-15（接入经 MC 返回的 TH 状态）**：状态置为 `Blocked`，等待 MS-14 真正闭环。
* **MS-16（提供 TH 单端故障场景）**：状态置为 `Blocked`，等待 CR-02T 测试工具治理完成。
* **MS-21（准备真实双端验收候选）**：状态置为 `Blocked`，等待双端固件与 AP 均就绪。
* **MS-17（验收真实双 MCU 查询闭环）**：状态置为 `Blocked`，等待 CR-10 执行。

### 3.3 修复的任务（Fix / Governance - 当前启动的恢复票序列）
* **CR-00**：基线固化与已有成果保护【已完成】
* **CR-01**：结论撤回、限制登记与卡片语法修复【本票，执行中】
* **CR-02 / CR-02Q**：最小级联只读 ICD 冻结与 QA 独立黄金预期构建
* **CR-02T**：HIL 测试夹具与发现工具缺陷治理（F23~F26）
* **CR-03A~E**：任务管理工具检查项补齐与规则基线一致性保障
* **CR-04A~E**：AP 宿主健壮查询与反例防御改造（解决 F01~F07）
* **CR-05A~E**：MC 原生双向透明路由转发与中断解耦（解决 F08~F11）
* **CR-06A~D**：TH 原生 MiniMCProto 固件支持（解决 TH 端真实响应缺失问题）
* **CR-07A~C**：MC-TH 中继升级管理器缺陷专项治理（解决 F12~F14，F22）

### 3.4 复验的任务（Re-verification - 联合联调与真实 HIL）
* **CR-08**：装配真实 AP + MC + TH 双固件协同候选清单（Candidate Bundle）
* **CR-09**：三端物理台架工程联合调试（带完整四向轨迹记录）
* **CR-10**：独立真实 HIL 验收（覆盖正常查询、TH 故障注入与自恢复，重新复验 MS-07 与 MS-17）
* **CR-11**：最终验收评审、全流程交接与仓库版本锁文件更新

---

## 4. 签署与生效

* **裁决人**：唯一 COORD (`9e5411f4-acad-421e-b487-9e68b9483320`)
* **执行状态**：立即生效，全面应用至看板、任务卡及交接文档。
