# 独立 QA 黑盒发现与 COORD Issue 交接模板

> **切换补丁待接受：** 本文的 `streamlined-v1` 是候选策略定义，尚未正式发布。本次变更须先按 legacy 门禁接受，由 COORD 登记准确生效版本后启用；此前保持停机，旧任务按原门禁处理。切换与逐卡迁移见 `project-control/docs/planning/qa_streamline_cutover_20261103.md`。

配套[独立 QA 执行流程](../../planning/independent_qa_vmware_execution_flow_20261103.md)。本模板对齐[现行 Issue 字段](../../../.agents/rules/e2e_issue_verification_flow.md)，扩展发现、buildno 和耐久交接信息；扩展 schema 是待实现/接受的合同，不声称现有 HUMAN 入口可以消费。模板不是实际 Issue，也不携带执行授权。

发现者保存一个稳定 `finding_id` 的发现包，追加证据另有事件/版本，不覆盖已封存文件。同一事件重投复用 `event_id`；新观察用新事件。COORD 收件后分配正式 `issue_id` 并单写正式 Issue，回执指向发现包和准确哈希。空字段必须说明未知原因，尤其不能假造会话、构建号或硬件物证。

以下 YAML 供正式发现记录的机器头使用，正文保留可直接复现的用户步骤。数字 buildno 必须填实际整数，时间为实际 UTC；源码/制品/配置及证据使用完整哈希。

```yaml
schema_version: qa-finding-proposal-v1
finding_id: null # QA 实际分配的稳定发现标识
event_id: null # 本次交接事件，重投不变
finding_revision: 1
issue_id: null # COORD 收件后分配/关联，QA 不抢占正式 ID
summary: null
issue_type: null # functional / usability / requirement / environment / tooling
resolution: open # open / fixed / duplicate / not-a-defect；不是任务status
reported_by:
  actor_type: QA
  actor_id: null # 实际执行者/操作者，不伪装 HUMAN
  session_or_job: null
reported_at_utc: null
source_task: null # 实际 task_id/revision/run；尚无正式任务如实说明
feature_and_case_ids: []
requirement_refs: [] # 正式需求准确版本、接受记录及相关手册章节
case_ref:
  suite: null # base / delta
  case_id: null
  revision: null
  tools_commit: null
release_series: null
found_buildno: null
source_candidate_ref: null # QA 重建来源候选，如适用
candidate_manifest:
  path: null
  sha256: null
affected_versions: {} # 各仓完整commit/ref、配置、制品和实际固件身份；可引用不可变清单
run_id: null
attempt: null
environment_ref: null # VM UUID/快照、浏览器、串口/探针/板卡、台架窗口及环境清单哈希
preconditions: []
reproduction_steps: [] # 页面入口→点击/输入→观察，保留失败发生的步骤
expected:
  behavior: null
  deadline_or_tolerance: null
  source_ref: null # 需求/契约版本；不拿当前实现当预期
observed: null # 事实；推断放 root_cause_hypothesis
evidence: [] # 受控路径/URI、SHA256、类型、采集区间和来源；缺证据明确列出
missing_evidence: []
impact: null
severity_hint: null # QA 提议；COORD 决定正式优先级
priority: null
root_cause: null # 未查明保持 null
root_cause_hypothesis: null # 明确待验证，不写成事实
blocked_cases: []
blocker_and_recovery: null
linked_tasks: [] # COORD 登记的实际任务/Owner/revision
fix_commits: [] # 开发/INTEGRATOR 提供各受影响仓库完整提交及依赖
fix_available_buildno: null # INTEGRATOR 首次发布修复组合，非 QA 通过
fix_candidates: []
verified_buildno: null # QA 真实复验并完成所需接受后才填
verification_runs: [] # 原失败例、正负/恢复、必要base、实际候选/证据/审阅，失败也保留
duplicate_of_or_disposition: null
receipt_ref: null # COORD 实际回执/正式 Issue 关联
closure: null # COORD 核验接受后填；不能凭修复声明关闭
```

每个 `evidence` 条目至少为 `{path, sha256, kind, captured_at_utc, producer}`；引用外部环境/build 清单时，该清单同样不可变且有哈希。报文原始文件和 UI 轨迹互补，截图不是实际设备响应的替代。

发现记录正文顺序：现象和影响 → 前置/用户入口 → 精确步骤及失败点 → 预期/依据 → 实际 → 证据和缺口 → 依赖/恢复。黑盒观察成立即可提交，根因和源码位置未知不阻止收件。

## COORD 实际收件回执字段

```yaml
receipt_id: null
event_id: null
finding_id: null
received_at_utc: null
receiver_session: null
issue_id: null
disposition: null # received / linked-duplicate / rejected-input（说明输入错误；不是忽略产品失败）
owner_or_next_role: null
linked_tasks: []
next_action: null
reason: null
```

发现→收件→派单→修复就绪→独立复验→关闭各自留记录。发送失败保持待投递；收到重复事件返回原回执，不重复创建任务。正式 Issue/任务关联由 COORD 查重；不能仅凭相似标题合并不同根因。

`verified_buildno >= fix_available_buildno` 不是关闭判据；必须核对同一发布序列、有效修复/依赖、原失败与必要回归结果、独立审阅及所用qa_policy的必需接受（streamlined-v1不默认二次审报告，legacy保留）。环境/证据不足保留阻塞，真实失败保留 FAIL，不能为填字段预签 APPROVED。
