---
review_id: REV-ARCH-SOC-TEMP-ICD-20261028-QA01
reviewer_role: QA
platform: codex
actual_session: 01a18280-cb29-73c2-89e5-53facca8bf18
actual_model: "Codex / GPT-6; precise runtime model alias not exposed by session metadata"
required_default_model: gpt-6-luna
task_id: ARCH-SOC-TEMP-ICD-20261028
task_revision: 1
reviewed_artifact_version: revision-1
reviewed_artifact: project-control/docs/interfaces/soc_temperature_module_architecture_icd_draft_20261028.md
reviewed_artifact_sha256: 6753599ef5d8282cf876649359873c2daf0f40fbcc01c379a0aa7a2e5e250bf5
review_time_utc: 2026-10-28T12:35:24Z
decision: REJECTED
review_scope: document-only; no business source edits, builds, tests, or hardware operations
---

# SoC 温度架构草案独立 QA 审查报告

## 结论

**REJECTED**。候选准确识别了协议 flags、温度编码/范围及操作码等主要冲突，并正确将尚未接受的内容保留为提案；但温度 MUST 中的安全和编码要求没有全部落成明确的阶段放行条件，阶段 A→F 的交接门也不够明确。候选哈希为 6753599ef5d8282cf876649359873c2daf0f40fbcc01c379a0aa7a2e5e250bf5。

运行会话 ID 从 Codex TUI 会话列表取得：01a18280-cb29-73c2-89e5-53facca8bf18。策略默认模型是 gpt-6-luna，但会话元数据未暴露实际模型的精确别名；本报告如实记录可见信息，不把默认值冒充实际模型。该项是审计限制，也意味着无法核实本会话是否满足精确模型别名要求。

## 审阅输入及哈希

| 输入 | SHA256 |
| --- | --- |
| 候选架构 ICD revision 1 | 6753599ef5d8282cf876649359873c2daf0f40fbcc01c379a0aa7a2e5e250bf5 |
| TEMP-01 任务卡 revision 1 | 431063a22c84ae1c7955340119d811df7f395f1cd0f031cde1d70f545ca33aa4 |
| TEMP-01 板端 ICD | 74361f23ee27f513c0df195c796c42961a1d3c5fb352a72a91c7f70f23033a8d |
| PL-02 细粒度设计 | 75f3512b80a72266aa1bd0f53ee7fe1b523ac4179396f3261a307e85a18bd30a |
| PL-02 任务卡 | f5a0e4c1674f8e1bbba45b9644c259063862d6d5d04354a57ad9838fab2b322c |
| MiniMCProto v2.0 Rev 2.0.3 | 候选记载的 SHA256：9f8d4f9607cb3e76cc30b9ee2f971b23c3e0d936611188466a71f4aa15f3ce54 |
| 当前 Codex QA 规则 | 已读取 project-control/.agents/rules/codex_qa_review.md；本次未记录其 SHA256 |
| 角色职责规则 | 已读取 02_模块与Agent职责.md、06_通信工程师职责与接口边界.md 及派单五项所在公共读写协议 |

## 核查结果

### 协议、接口与版本冲突

1. **Flags：候选判断正确。** 正式协议规定 v2.0 必须叠加 PROTO_VERSION=0x04；请求 WANTS_ACK 应为 0x05，响应 IS_RESPONSE 应为 0x06。TEMP-01 ICD 写 0x01/0x02、PL-02 写 flags=0，确有冲突。候选将其列为 C1，并要求重算 CRC、复核路由字段和重做双向黄金帧，符合正式协议。
2. **温度编码与范围：冲突判断正确。** PL-02 的无符号 0.1°C 表示与 TEMP-01 的有符号 0.01°C 表示不一致；后者的 int16_t 无法表达 +35000，且 0x7FFF 被用作故障哨兵。候选 C2/C3 正确要求重新选择编码并验证边界与哨兵。
3. **操作码：冲突判断基本正确。** PL-01 对 0x10 有互相矛盾的表述；正式协议将 0x10 用于系统控制，将 0x40 定义为综合状态遥测。0x40 不能不经契约就替代查询命令。PL-02 与 TEMP-01 均提出 0x14，但候选没有擅自把它写成新分配，而是要求 Owner 接受，处理得当。
4. **状态码映射仍未闭合。** 候选内部模型列 ADC_TIMEOUT，TEMP-01 线缆状态码名为 TEMP_STATUS_TIMEOUT。候选要求映射基于已接受载荷，但没有要求列出每个数值状态码到内部状态的确定映射和未知码行为。纳入 A/B 阶段的接口接受表。
5. **路由及安全边界：方向正确但实现契约待定。** 候选把 FORWARD 定为唯一 UART 所有者、要求有效帧关联、保留 TH 端到端透明转发；职责与正式协议及 FWD 角色规则一致。应在接口接受项中保留 Hop、ROUTE_IS_ROUTED、CRC 重算和零业务解析约束，不以候选 SoC 模型取代 MCU ICD。

### 用户要求的五项 MUST

| PL-01 MUST | 结果 | 依据 |
| --- | --- | --- |
| 双端温度统一查询及真实测量数据 | 部分满足 | 第 3–4 节给出 MC/TH 来源、查询请求和状态模型；真实传感器及独立基准对照留到 HIL 阶段。 |
| 操作码避让与分层寻址 | 部分满足 | C4 指明 0x10 禁用及 0x40 语义，保留 0x14 接受流程；阶段 A 完成前不应进入依赖该字段的实现。 |
| 加热 PWM 全周期锁定 0、PID 旁路 | 未形成明确放行门 | 候选提及不能以 duty=0 遥测证明物理断热，并要求记录物理隔离/检测方案；但阶段 D/E 没有明确要求验收“MC/TH 整个固件生命周期 PWM 为 0 且 PID 禁用/旁路”。应将该不变量及物理证据写入验收门。 |
| 开路/短路与采样异常明确报错 | 部分满足 | 状态模型包含 OPEN/SHORT/TIMEOUT/UNKNOWN，并禁止由断链推断传感器开路；精确阈值、极性、状态码与传感器依据仍待硬件/端侧 Owner 接受。 |
| ADC 轮询超时及代码门禁 | 部分满足 | C 阶段含超时用例；没有明确要求 TH ADC 轮询必须有界退出，也未把项目编码门禁（函数 ≤50 行、参数 ≤4 个、零动态堆分配等）列入实现验收检查。 |

### 阶段前置、角色与安全

- 阶段 A 要解决 C1–C6，B 要接受 SoC 最小契约，C 使用已接受端点预期，D 绑定 AP 与双固件，E 做独立 HIL；主序列合理。第 9 节也要求 COORD 协调当前 TEMP-02/04 的消费限制，且不声称已通知。
- 表格没有显式写出各阶段的“前阶段接受后由 COORD 放行”条件，以及新 ICD/头文件的准确版本、必要 Owner 签署、候选哈希与下游消费绑定。TEMP-01 当前 Done 和其下游卡记录的 accepted version 不能自动消除文档已指出的冲突。需明确依赖关系与暂停/恢复判据，避免仅凭表格排列推进。
- 角色职责大体符合规则：ARCH 维护公共接口，ENG-FWD 独占串口，STATE 拥有状态，MC/TH Owner 对固件与硬件事实负责，INTEGRATOR 装配，QA 独立验收；HUMAN/真实 MCU Owner 的确认没有被 QA 替代。
- 候选将 max_age、刷新周期、超时和资源预算留为配置待定是恰当的；它也正确区分主机接收年龄和 MCU 采样时钟，不宣称硬实时。

## 需修订后重新审查

1. 将全生命周期断热/PID 旁路写成温度切片不可变安全条件，并规定由适当硬件 Owner 提供的物理检测证据和阶段门。
2. 在编码/实现验收中明确 ADC 有界超时及项目编码门禁，并写出 TEMP 状态码到 SoC 状态的逐值映射、未知码处理。
3. 给 A–F 阶段补上明确的前置接受、COORD 放行、准确候选版本/哈希和阻塞时的消费规则。
4. 由 COORD/Owner 处理会话模型登记限制；重新审查时绑定修订后文件的新 SHA256。

## 执行记录与限制

- 只读检查了根 AGENTS.md、project-control/.agents/rules/codex_qa_review.md、目标架构 ICD、TEMP-01 卡及交付 ICD、PL-02 设计/卡、PL-01 范围、协议规范和相关角色规则。
- 执行的读取/核对操作包括 cat、sed -n、nl -ba、rg -n、rg --files、sha256sum，工作目录 /home/sushaohua/workspace/ai_soc_project。
- 未执行构建、测试、源码检查或硬件操作；本结论仅评审文档，不评审源码、固件或硬件安全状态。
- 实际模型的精确运行时别名无法从本会话工具元数据读取；会话 ID 可从 TUI 会话列表确认。
- 报告仅写入本轮指定路径。历史 TEMP-01 状态及签名未修改。
