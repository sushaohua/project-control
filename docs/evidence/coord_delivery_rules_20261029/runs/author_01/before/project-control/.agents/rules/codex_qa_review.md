---
title: 独立 QA 统一使用 Codex 的执行规则
status: current-rule
owner: COORD
effective_date: 2026-10-26
updated: '2026-10-27T20:16:05+08:00'
authorization: 用户本轮明确要求“把所有的qa都独立成codex审查”
---

# 独立 QA 统一使用 Codex

本规则是后续 QA 审查与验收的执行方式原件，适用于所有未完成任务和新建任务。已经完成的评审及原始报告保留原会话、版本、结论；重新检查时另建 run，不将历史签署改名为 Codex 签署。

## 覆盖范围与职责

- `reviewer_sessions` 中岗位为 QA 的过程审计、契约审查和结果验收，统一由独立 Codex 会话执行。
- `verifier: QA` 的独立运行验证，统一由独立 Codex 会话承担。硬件使用条件、实际环境与原有 HW-G 门禁继续适用，缺少实测不能签署硬件通过。
- QA 作者交付的独立样例、测试工具和报告，由独立 Codex 会话承担其 ARCH 复核；岗位名称和其他必需工程师评审保留，不能以 Codex QA 替代 HUMAN 或真实 MCU Owner 的批准。
- 原实现者、QA 作者及其已登记 owner/租约不因本规则自动更换。作者不得在同一会话切换岗位后自批；AGY 实现团队内部的自检不能替代本规则要求的独立 Codex 审查。
- 工作包不直接派单，卡内引用本规则仅约束后续子任务的 QA 安排。

## 登记方式

每张适用任务卡引用 `qa_review_policy: project-control/.agents/rules/codex_qa_review.md`。Codex Reviewer 登记格式：

默认模型统一为 `gpt-6-luna`，包括独立 QA、QA 作者产物的独立 ARCH 复核以及 QA Verifier。派单/启动独立 Codex 时显式使用该模型；任务卡记录计划模型，报告记录实际模型。只有 COORD 在任务卡 `model_policy.approved_overrides` 中登记角色、会话、实际模型、原因及批准证据后，才允许该任务临时覆盖默认值。该条约束项目任务调度，不代表已修改工作区外的用户级 Codex 配置。

```yaml
review_assignments:
  reviewer_sessions:
  - role: QA # QA 作者产物的复核保留原 ARCH 岗位
    platform: codex
    model: gpt-6-luna
    planned_session_alias: codex-qa-<task-id>-review
    session: null
    decision: null
    reviewed_task_revision: null
    artifact_version: null
    evidence: null
    report_sha256: null
```

独立Verifier在`review_assignments`登记platform/计划别名、`verifier_model: gpt-6-luna`和空的`verifier_actual_model`；实际`verifier_session`落实后填写。提交时分别绑定`verifier_reviewed_task_revision`、`verifier_artifact_version`、`verifier_decision`、`verifier_evidence`、`verifier_report_sha256`及实际模型。模型例外必须引用`model_policy.approved_overrides`中含原因和COORD批准证据的对应记录。所有必需Reviewer逐项填写同等信息，单个报告不能默默覆盖其他岗位。

`planned_session_alias` 只是计划名称，不代表会话已创建或通过 Ready。尚未落实的实际 `session` 保持 null；COORD 实际安排独立 Codex 会话后，填写可定位的会话标识。用户已指定的 `codex-qa-session-01` 保留为 V2-P01C 的会话别名，不能据此宣称已经审核。通过 CLI 执行时，从真实运行事件记录 CLI 会话 ID 及其与别名的对应关系，不编造 ID。

## 硬件在环（HIL）零虚拟化与端到端协议原生审计铁律（HW-G5 / HW-G6）

1. **真实硬件回环绝对性（Zero Virtualization in HIL）**：
   凡任务定义中包含 `required_evidence_level: hardware-verified`、`verification_environment` 涉及真实物理板卡（如 `real-mcu-hil`、`/dev/ttyUSB0`）的，验收必须严格执行物理在环测试。**严禁以伪终端（PTY）、本地回环（Loopback）、Socket 模拟器或软件 Mock 代替物理单片机应答**。
2. **物理回包有效性底线（零响应即否决）**：
   正常物理查询必须验证真实双向闭环及目标响应关联。若仅收到线路噪声/旧外设报文，或符合正式契约的src/dst/flags/cmd/seq/精确载荷等有效关联响应为0，QA必须判定REJECTED并交COORD登记阻塞。失联、坏帧、超时等负例按事先接受的无响应/错误与恢复预期判断，不能把负例通过提升为正常闭环通过。**严禁以“AP 单向发包成功”或“AP 过滤了噪声未崩溃”等局部表现替代端到端成功**。
3. **不可伪造的硬件对账凭证**：
   HIL 验收证据必须包含物理串口设备路径、波特率设置、精确到毫秒的真实时戳，以及原始的双向收发十六进制报文（Raw Hex TX 与 Raw Hex RX 逐帧对账记录）。缺少物理硬件原始应答对账证据的，COORD 严禁采纳。
4. **反作弊与虚假结论作废**：
   QA 独立评审员严禁“替受测方写测试桩促成通过”。若发现任何使用 PTY/Mock 替身绕过物理硬件验证的行为，一律判定为严重违规，其签发的 `APPROVED` 结论自始无效，由唯一COORD追加撤回记录、保留历史签署，并在现有生命周期内修正状态、设置`blocked: true`与恢复条件；`REJECTED`是报告决定，不是任务status。

5. **端到端协议原生一致性（严禁转译伪造与拆单遗漏, HW-G6）**：
   凡规范定义为原生透明路由的链路，中继必须按正式协议识别路由头、校验完整帧，并处理Hop、ROUTE_IS_ROUTED与CRC；“零业务解析”不禁止这些帧级操作。**中继转发路径严禁解析cmd_id的业务语义、解包Payload、修改业务seq，严禁私自降级为G-code等旧文本或伪造下游应答**。本机业务及协议规定的本机广播消费按契约处理，与中继转发职责分开。跨节点工程必须落实“ARCH契约接受 → 各节点必要实现 → 工程联合调试 → 独立组合验收”，显式登记节点提供票及能力前置。单板微步按本票范围交付，不要求每张票产出双固件；最终MC＋TH组合必须锁定两端固件（fw_mc.bin＋fw_th.bin）及AP准确版本与实际部署证据。中间节点不得替未就绪的下游生成成功；缺少最终组合必需制品或物理证据时拒绝相应组合接受。

## 执行与签署

1. 作者完成本票后向 COORD 提交准确任务 revision、候选 commit/diff/产物 SHA256、执行记录、原始日志和检查判据。
2. COORD 安排新的 Codex 会话，或继续本票已登记且未参与写作的独立 Codex 审阅会话；不 resume/fork 实现会话，不复制实现者完整交互历史。传入任务卡、规则、正式输入与交付证据，由审阅者独立核查。
3. 审阅者对业务源码只读；构建输出、测试执行与证据写入按本卡授权的隔离位置进行。发现问题交回作者，不能自行修业务代码促通过，也不能修改正式任务状态。
4. 报告记录实际 Codex 会话/别名、任务与 revision、所审版本、过程审计、正常和异常判据、实际命令/cwd/退出码/日志、未执行项、问题与限制，并给出 `APPROVED` 或 `REJECTED`。证据不足不得签署 APPROVED。
5. 报告与原始输出保存在本票 `docs/evidence/.../runs/<run-id>/` 的独立位置，COORD 核对报告 SHA256 和候选 SHA256。首次约定可使用 `qa_review_report.md`；同名文件已存在时另建审核 run，保留历史。
6. CLI 退出码为 0、结构检查通过或报告文件存在，都不等于审核通过。调用失败、超时或报告缺失保持待审；REJECTED 交回作者修复，新候选重新审核，不沿用旧结论。
7. 只有唯一 COORD 在准确版本获得所有必需接受结果、收件及适用的集成验证后，才能推进 Review → Verify → Done 并释放下一微步。

本规则和卡内 `platform` 是调度要求，不能自行启动 Codex。当前结构检查工具不会调用审核服务；尚未接入实际调度脚本时，由 COORD 启动独立 Codex 会话或人工转交，不能声称后台自动审核已部署。


## 模板、阶段与工具边界（2026-10-27）

新建/修订任务使用[任务卡模板](templates/任务卡模板.md)、[派单提示词](templates/角色任务提示词.md)、[实际运行记录](../../docs/guides/templates/task_run_record.md)、[独立报告模板](templates/QA审查报告模板.md)。历史accepted等签署值按原版本保留，不批量改写；新报告decision使用APPROVED/REJECTED，未审为null。

Ready核输入、实际作者/检查安排、授权范围、资源和有效租约，不要求本票尚未产生的候选/签署。Review/Verify/Done按同一准确候选核全部必需接受、适用运行/集成与收件；blocked或未满足的能力条件不能通过新建子票绕过。报告自身SHA256在文件写完后存卡片/交接清单，避免自引用。

故障夹具/黄金预期/报告也是受审产物；先检查工具目标绑定、写失败传播、原状态快照、异常恢复和读回，才能用于所授权台架。寄存器操作、模拟测试、真实链路、部署启动证据分别记录。

本轮模板规范更新不表示`check_task_graph.py`的MCU任务发现、全生命周期、真实版本/报告、租约期限或范围交叠校验已经实现；这些项目仍需COORD人工核对，并在工具专项完成后另留验收证据。文件存在、exit0、CRC通过都不自动解除该责任。
