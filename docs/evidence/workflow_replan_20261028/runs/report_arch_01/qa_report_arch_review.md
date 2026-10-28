---
review_id: workflow-replan-report-arch-01
reviewer_role: ARCH
platform: codex
actual_session: /root/review_report_arch
actual_model: gpt-6-luna
reviewed_reports:
  - path: project-control/docs/evidence/workflow_replan_20261028/runs/review_01/qa_review_report.md
    sha256: 3e10e4d6af5e6f0accc092564346f9825adda141062ff3b3f3409d0095ac2785
    decision: REJECTED
  - path: project-control/docs/evidence/workflow_replan_20261028/runs/review_02/qa_review_report.md
    sha256: f8a734155581176029de3bec184d5c8bfaad92e8e5862f6a5b84c1ede8e824c6
    decision: APPROVED
  - path: project-control/docs/evidence/workflow_replan_20261028/runs/review_03/qa_review_report.md
    sha256: 79cff3918119e519540a3e5819e8ab883a182ba098623ef507490b1dce28ca8c
    decision: APPROVED
candidate_manifests:
  - path: project-control/docs/evidence/workflow_replan_20261028/candidate_manifest.json
    sha256: f101fef32726fda4717298259e6cbd97e2edbf050e39c86b6f7c8cc1f950914b
  - path: project-control/docs/evidence/workflow_replan_20261028/candidate_manifest_v2.json
    sha256: bcb25b180e67fbabbacffe717e55cf759be0a9600282f0c32fd80a0a85c5174f
  - path: project-control/docs/evidence/workflow_replan_20261028/candidate_manifest_v3.json
    sha256: ee83351d6a4e9f569a78c896e21a189ad88d86f620b82bf37d723d50fa508c08
review_time: 2026-10-28
process_audit: completed
result_check: completed
decision: APPROVED
accepted_scope: Evidence and conclusion integrity of the three listed QA reports, bound to their listed candidates only.
limitations:
  - No business source, firmware, build, deployment, or hardware/HIL acceptance was reviewed or performed.
---

# QA 报告 ARCH 复核

## 核查结果

- **review_01** 报告记录实际入口 `/root/workflow_review`、模型 `gpt-6-luna`，绑定 v1 manifest `f101fef32726fda4717298259e6cbd97e2edbf050e39c86b6f7c8cc1f950914b`。其 4 条断链清单与 `link_and_manifest_check.txt` 一致，结论 `REJECTED` 限定于 v1。报告称当时 34 项 hash 匹配；这是 review_01 检查时的候选状态。修订后当前文件已变化，v1 manifest 现有 6 项哈希不再匹配，不能把历史检查解释为当前文件校验。
- **review_02** 报告记录实际入口 `/root/workflow_review`、模型 `gpt-6-luna`，绑定 v2 manifest `bcb25b180e67fbabbacffe717e55cf759be0a9600282f0c32fd80a0a85c5174f`。报告 SHA 与交接值一致。`independent_checks.txt` 支持 34 项当时 hash 匹配、91 条相对链接无缺失和 frontmatter 检查通过；四处修复位置与 review_01 问题对应。报告的 `APPROVED` 明确只适用于 v2 文档候选，不声称业务或硬件验收。当前 v2 manifest 文件本身仍保持该哈希；README 已进入 v3 修订，因此以当前工作树重算时仅 README 与 v2 清单不同。这不推翻 v2 的历史签署范围。
- **review_03** 报告记录实际入口 `/root/workflow_review`、模型 `gpt-6-luna`，报告 SHA 与交接值一致。`delta_checks.txt` 显示 v2/v3 路径集合相同、仅 README 变化、其余 33 项无 hash 错误，README 实际 hash 与 v3 一致，25 条相对链接无缺失。独立重算 v3 manifest SHA 为 `ee83351d6a4e9f569a78c896e21a189ad88d86f620b82bf37d723d50fa508c08`；34 项当前文件均与 v3 manifest 匹配。报告的 `APPROVED` 限于 v3 文档候选及 README 差异。

四处断链修复由 v2 的候选文件哈希绑定及链接扫描证据支持；review_03 的单文件差异审查继承 review_02 对未变 33 项的核查。结构检查只支持报告所述任务图结构结果，不代表任务执行或验收。三份报告的决定均准确限定在各自 manifest 哈希：v1 为 `REJECTED`，v2、v3 为 `APPROVED`；后续版本不改写前版结论。

## 结论与限制

**ARCH 决定：APPROVED。** 本复核只确认上述 QA 报告的身份、候选绑定、证据与结论范围相互一致。未审阅业务代码、未运行构建或硬件/HIL，也未据此接受任何工程任务或正式状态。
