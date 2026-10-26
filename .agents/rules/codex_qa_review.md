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

## 执行与签署

1. 作者完成本票后向 COORD 提交准确任务 revision、候选 commit/diff/产物 SHA256、执行记录、原始日志和检查判据。
2. COORD 安排新的 Codex 会话，或继续本票已登记且未参与写作的独立 Codex 审阅会话；不 resume/fork 实现会话，不复制实现者完整交互历史。传入任务卡、规则、正式输入与交付证据，由审阅者独立核查。
3. 审阅者对业务源码只读；构建输出、测试执行与证据写入按本卡授权的隔离位置进行。发现问题交回作者，不能自行修业务代码促通过，也不能修改正式任务状态。
4. 报告记录实际 Codex 会话/别名、任务与 revision、所审版本、过程审计、正常和异常判据、实际命令/cwd/退出码/日志、未执行项、问题与限制，并给出 `APPROVED` 或 `REJECTED`。证据不足不得签署 APPROVED。
5. 报告与原始输出保存在本票 `docs/evidence/.../runs/<run-id>/` 的独立位置，COORD 核对报告 SHA256 和候选 SHA256。首次约定可使用 `qa_review_report.md`；同名文件已存在时另建审核 run，保留历史。
6. CLI 退出码为 0、结构检查通过或报告文件存在，都不等于审核通过。调用失败、超时或报告缺失保持待审；REJECTED 交回作者修复，新候选重新审核，不沿用旧结论。
7. 只有唯一 COORD 在准确版本获得所有必需接受结果、收件及适用的集成验证后，才能推进 Review → Verify → Done 并释放下一微步。

本规则和卡内 `platform` 是调度要求，不能自行启动 Codex。当前结构检查工具不会调用审核服务；尚未接入实际调度脚本时，由 COORD 启动独立 Codex 会话或人工转交，不能声称后台自动审核已部署。
