---
title: 独立 QA 统一使用 Codex 的执行规则
status: current-rule
owner: COORD
effective_date: 2026-10-26
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

```yaml
review_assignments:
  reviewer_sessions:
  - role: QA # QA 作者产物的复核保留原 ARCH 岗位
    platform: codex
    planned_session_alias: codex-qa-<task-id>-review
    session: null
    decision: null
    artifact_version: null
    evidence: null
```

独立 Verifier 在 `review_assignments` 中登记 `verifier_platform: codex`、`verifier_planned_session_alias: codex-qa-<task-id>-verify`，实际 `verifier_session` 在落实会话后填写。

`planned_session_alias` 只是计划名称，不代表会话已创建或通过 Ready。尚未落实的实际 `session` 保持 null；COORD 实际安排独立 Codex 会话后，填写可定位的会话标识。用户已指定的 `codex-qa-session-01` 保留为 V2-P01C 的会话别名，不能据此宣称已经审核。通过 CLI 执行时，从真实运行事件记录 CLI 会话 ID 及其与别名的对应关系，不编造 ID。

## 硬件在环（HIL）零虚拟化与端到端协议原生审计铁律（HW-G5 / HW-G6）

1. **真实硬件回环绝对性（Zero Virtualization in HIL）**：
   凡任务定义中包含 `required_evidence_level: hardware-verified`、`verification_environment` 涉及真实物理板卡（如 `real-mcu-hil`、`/dev/ttyUSB0`）的，验收必须严格执行物理在环测试。**严禁以伪终端（PTY）、本地回环（Loopback）、Socket 模拟器或软件 Mock 代替物理单片机应答**。
2. **物理回包有效性底线（零响应即否决）**：
   物理串口通讯测试必须验证真实的物理双向闭环。若物理链路仅收到线路噪声、未迁移外设旧报文（如迪文屏 DGUS 数据）或合法协议响应帧数（Valid Response Frames）为 0，QA **必须无条件判定为 `REJECTED`**，开具硬阻塞单（Blocker Issue），挂起任务并交还协调员。**严禁以“AP 单向发包成功”或“AP 过滤了噪声未崩溃”等局部表现替代端到端成功**。
3. **不可伪造的硬件对账凭证**：
   HIL 验收证据必须包含物理串口设备路径、波特率设置、精确到毫秒的真实时戳，以及原始的双向收发十六进制报文（Raw Hex TX 与 Raw Hex RX 逐帧对账记录）。缺少物理硬件原始应答对账证据的，COORD 严禁采纳。
4. **反作弊与虚假结论作废**：
   QA 独立评审员严禁“替受测方写测试桩促成通过”。若发现任何使用 PTY/Mock 替身绕过物理硬件验证的行为，一律判定为严重违规，其签发的 `APPROVED` 结论自始无效，任务状态强制回退至 `Blocked / Rejected`。

5. **端到端协议原生一致性（严禁转译伪造与拆单遗漏, HW-G6）**：
   凡规范定义为原生透明路由的跨节点链路，**中间路由节点严禁解包或将协议私自降级为旧文本协议（如 G-code），严禁在中间节点伪造下游应答**。跨物理节点工程必须强制采用“ARCH 契约冻结 → 双端并行实施 → 联合调试验收”三段式拆解；若发现仅由单板工程师单边兜底造假或未配对交付双固件（`fw_mc.bin` + `fw_th.bin`）的，QA 必须直接判定为 `REJECTED`。

## 执行与签署

1. 作者完成本票后向 COORD 提交准确任务 revision、候选 commit/diff/产物 SHA256、执行记录、原始日志和检查判据。
2. COORD 安排新的 Codex 会话，或继续本票已登记且未参与写作的独立 Codex 审阅会话；不 resume/fork 实现会话，不复制实现者完整交互历史。传入任务卡、规则、正式输入与交付证据，由审阅者独立核查。
3. 审阅者对业务源码只读；构建输出、测试执行与证据写入按本卡授权的隔离位置进行。发现问题交回作者，不能自行修业务代码促通过，也不能修改正式任务状态。
4. 报告记录实际 Codex 会话/别名、任务与 revision、所审版本、过程审计、正常和异常判据、实际命令/cwd/退出码/日志、未执行项、问题与限制，并给出 `APPROVED` 或 `REJECTED`。证据不足不得签署 APPROVED。
5. 报告与原始输出保存在本票 `docs/evidence/.../runs/<run-id>/` 的独立位置，COORD 核对报告 SHA256 和候选 SHA256。首次约定可使用 `qa_review_report.md`；同名文件已存在时另建审核 run，保留历史。
6. CLI 退出码为 0、结构检查通过或报告文件存在，都不等于审核通过。调用失败、超时或报告缺失保持待审；REJECTED 交回作者修复，新候选重新审核，不沿用旧结论。
7. 只有唯一 COORD 在准确版本获得所有必需接受结果、收件及适用的集成验证后，才能推进 Review → Verify → Done 并释放下一微步。

本规则和卡内 `platform` 是调度要求，不能自行启动 Codex。当前结构检查工具不会调用审核服务；尚未接入实际调度脚本时，由 COORD 启动独立 Codex 会话或人工转交，不能声称后台自动审核已部署。
