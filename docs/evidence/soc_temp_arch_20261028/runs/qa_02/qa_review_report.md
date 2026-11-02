---
review_id: REV-ARCH-SOC-TEMP-ICD-20261028-QA02
reviewer_role: QA
platform: codex
actual_session: 01a18280-cb29-73c2-89e5-53facca8bf18
actual_model: "Codex / GPT-6; exact runtime model alias not exposed in session metadata"
required_default_model: gpt-6-luna
task_id: ARCH-SOC-TEMP-ICD-20261028
task_revision: 1
reviewed_artifact_version: revision-1-sha256-0c7b4ed64d7c388f3bc4075266e9bb80d05ec8243dff1d0719047ae4e5a751ae
reviewed_artifact: project-control/docs/interfaces/soc_temperature_module_architecture_icd_draft_20261028.md
reviewed_artifact_sha256: 0c7b4ed64d7c388f3bc4075266e9bb80d05ec8243dff1d0719047ae4e5a751ae
review_time_utc: 2026-10-28T12:38:51Z
decision: APPROVED
accepted_scope: document architecture proposal for owner review; not protocol freeze, implementation acceptance, or hardware verification
review_scope: document-only; no business source edits, builds, tests, or hardware operations
---

# SoC 温度架构草案独立 QA 复审报告

## 结论

**APPROVED（限本文档设计提案进入 Owner 评审）**。本次候选相对 QA01 增补了温度状态码逐值映射、A–F 阶段消费/放行条件、温度切片全生命周期断热要求、物理证据门、ADC 有界超时及代码规范门禁，也增加了 D-Bus XML 与 DDS IDL 草图。复核认为 QA01 中影响文档进入 Owner 评审的缺口已补齐，未发现新的阻断项。

该结论不代表各 Owner 已接受接口、不代表 TEMP-01 冲突已解决，也不代表构建、软件验收或任何硬件安全项目通过。候选仍明确标记为 draft，并把必要决定交给对应 Owner 与 COORD。

实际 Codex 会话 ID 为 01a18280-cb29-73c2-89e5-53facca8bf18。独立 QA 规则的默认模型是 gpt-6-luna，但会话元数据只提供 Codex/GPT-6 上下文，未暴露精确模型别名；本报告不推断或伪造实际别名。此为过程记录限制，需 COORD 在任务登记中按可获得的运行记录补齐。

## 受审版本及主要输入

| 文件 | SHA256 / 状态 |
| --- | --- |
| 候选架构 ICD revision 1 | 0c7b4ed64d7c388f3bc4075266e9bb80d05ec8243dff1d0719047ae4e5a751ae |
| TEMP-01 板端 ICD | 74361f23ee27f513c0df195c796c42961a1d3c5fb352a72a91c7f70f23033a8d |
| PL-02 细粒度设计 | 75f3512b80a72266aa1bd0f53ee7fe1b523ac4179396f3261a307e85a18bd30a |
| PL-01 范围 | 候选声明 fc95bd769829d629ebdb12ef1a2df3b3d420bfb8006a18975a20b50741c7ec89 |
| MiniMCProto v2.0 Rev 2.0.3 | 候选声明 9f8d4f9607cb3e76cc30b9ee2f971b23c3e0d936611188466a71f4aa15f3ce54 |
| QA01 历史报告 | e7edcb750d589bc21b8a822f4ab5dca94254c8ba8abad375931e4e775c9a0820（复审前后未变） |

已按指派读取根 AGENTS.md、project-control/.agents/rules/codex_qa_review.md、TEMP-01 卡、PL-02 设计、PL-01 范围、MiniMCProto 规范、编码标准、模块/通信角色规则及派单五项规则。未为未单独计算的规则文件编造哈希。

## QA01 问题复核

| QA01 事项 | 复核 |
| --- | --- |
| 状态码逐值映射及未知值处理 | 已补。候选 0x00–0x03 分别映射 OK/OPEN/SHORT/ADC_TIMEOUT，未知值成为 UNKNOWN + BAD_RESPONSE，不作为有效温度；第 93 行区分端侧采样超时与链路超时，并要求新 ICD、Owner、QA 确认反例。 |
| A–E 阶段及准确版本的放行条件 | 已补。第 183 行要求前置接受、精确 revision/SHA256、COORD 收件/放行、版本漂移停止消费，并声明历史 Done 不自动放行新版本；F 阶段依赖单列。 |
| 全生命周期断热及 PID 旁路 | 已补。第 185 行明确启动、复位、异常恢复期间 PWM=0 且 PID 禁用/旁路，并把 D/E 物理隔离或输出观测的范围及适用授权列为证据门；不能证明全生命周期则不签该项。 |
| ADC 轮询超时及代码门禁 | 已补。第 185 行要求适用 ADC 等待有界退出并验证超时/恢复，新增代码检查不超过 50 行、不超过 4 参数、零动态堆及指针/寄存器规范，存量按最小修改预算。 |
| D-Bus / DDS 草图 | 已补且仍是候选。第 108–141 行标明未经接受，不直接生成绑定；对 tuple 字段和 DDS 类型有说明，也明确 last_error 的 D-Bus/DDS 对齐是发布前待办。 |

## 交叉核查

- **MiniMCProto flags**：候选仍正确将正式 v2 版本位 0x04 与 WANTS_ACK / IS_RESPONSE 合成 0x05 / 0x06，要求重算 CRC 和复核路由字段。
- **温度表示/范围**：仍把 PL-02 的无符号 0.1°C 与 TEMP-01 的有符号 0.01°C、int16_t 上限和 0x7FFF 哨兵冲突作为待对账项，没有冒充已解决。
- **命令空间**：仍禁止把 0x10 当温度命令；区分 0x40 单向综合遥测和查询请求，0x14 仍待协议 Owner、相关端与 QA 接受。
- **角色与授权**：FORWARD 的 UART 唯一所有权、STATE 状态归属、MC/TH 对固件与硬件事实的责任、INTEGRATOR 装配和独立 QA/HUMAN 边界与角色规则一致。文档没有宣称已通知作者、已暂停实现或已操作硬件。
- **五项 PL-01 MUST**：双端只读查询在目标范围内；操作码冲突明确等待接受；加热关闭/PID 旁路现有硬门已增补；传感器异常状态仍需硬件与板端 Owner 定阈值；ADC 超时及编码限制已映射到实现验收。
- **安全与版本**：将候选 SoC 语义与 MCU 线缆布局分开；DDS/D-Bus、权限、资源及兼容性明确为后续候选，不宣称现有实现。通信转发继续要求遵从正式 Hop、ROUTE_IS_ROUTED、CRC 与透明业务边界。

## 尚待 Owner/COORD 处理（非本文件本轮阻断项）

1. A 阶段仍须真正生成并接受准确新 ICD/头文件、帧向量和传感器依据；该文档本身不代替这些产物或签署。
2. 状态码和内部字段单位需在新 MCU ICD 中落定；候选映射目前只是修订参考。
3. 真实板卡、输出极性、温度精度、物理断热检测和故障注入授权仍未验证。本文没有声称硬件通过。
4. D-Bus tuple 尚未包含 last_error，候选明确要求发布前统一 DDS/D-Bus 语义；IDL/XML、权限、QoS、目标预算仍待接受。
5. 文件正文 revision 字段仍为 1；本轮以新的文件 SHA256 精确区分该候选。后续正式基线应由作者/COORD 按项目版本约定更新。

## 执行与限制

- 工作目录：/home/sushaohua/workspace/ai_soc_project。
- 只读操作：读取规则和契约、nl -ba/sed -n 查看候选、rg -n 搜索状态码/放行/安全/IDL 内容、sha256sum 绑定候选及 QA01 历史报告。
- 未运行构建、测试或硬件操作；本报告只接受文档提案供 Owner 评审，不评源码、固件或物理安全状态。
- 曾尝试 git diff，但当前工作目录返回“不是 Git 仓库”；审阅按新 SHA 与正文逐项核对完成，未将该命令当成通过证据。
- 仅新建本轮指定的 qa_02/qa_review_report.md；QA01 历史报告哈希保持不变。
