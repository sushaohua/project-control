---
title: 独立 QA 与 QA 作者产物复核报告模板
status: current-template
template_version: '2026-10-27'
updated: '2026-10-27T20:16:05+08:00'
---

# 独立审查报告模板

本模板适用于独立QA，以及QA作者产物的独立ARCH复核；保留实际岗位。按[Codex QA规则](../codex_qa_review.md)运行，审阅者未参与本产物写作，不继承实现完整交互历史，只读业务源码。复制到新的授权run，不覆盖历史报告。

```yaml
template_version: '2026-10-27'
review_id: null
review_status: pending # pending / completed；不是正式任务status
reviewer_role: null # QA 或 QA作者产物的ARCH复核
platform: codex
requested_model: gpt-6-luna
actual_model: null # 实际运行后填写；偏离默认须关联任务卡批准记录
model_override_ref: null # 仅模型例外时，引用任务卡model_policy.approved_overrides条目
planned_session_alias: null
actual_session: null
author_session: null
task_id: null
task_revision: null
reviewed_artifact_version: null # 准确候选清单/文档/commit+diff/制品SHA256及其对象域
reviewed_artifacts: [] # 每项 path/commit或sha256/配置版本
protocol_and_expectations: [] # 正式来源/版本/哈希/已接受范围
verification_environment: null
verification_scope: null
required_evidence_level: null
review_time: null
process_audit: not-executed
result_check: not-executed
decision: null # 完成后仅APPROVED / REJECTED；不得预填通过
accepted_scope: null
limitations: []
unexecuted: []
not_applicable: [] # 检查项/理由/已接受依据；不适用不等于PASS
issues: []
commands: [] # 实际command/cwd/工具版本/时间/退出码/完整stdout-stderr路径与SHA256
case_results: [] # 独立预期版本、触发/输入、预期、观察、判定、原始证据及哈希
required_test_sets: []
executed_test_sets: []
missing_test_sets: []
raw_trace_files: [] # 真实HIL原始双向Hex/时间源/设备/方向/关联/丢失计数
supersedes_or_limits: [] # 追加旧结论适用变化，保留旧报告
handoff:
  receiver_session: null
  evidence_location: null
```

## 1. 身份、候选与过程核查

逐项写实际观察和证据；状态只能为“未执行/通过/失败/不适用（附理由）”，复制模板时不得预勾选：

| 检查项 | 要核对什么 | 实际结果 | 证据 |
| --- | --- | --- | --- |
| 输入/范围 | 任务revision、正式契约、前置能力、准确候选、授权路径 | 未执行 | 待实际填写 |
| 独立性 | 作者与各独立检查者分离，QA作者报告另有独立复核 | 未执行 | 待实际填写 |
| 原子步骤 | 先计划/前检、阶段边界、失败归因/熔断、保留用户改动 | 未执行 | 待实际填写 |
| 代码/构建 | 适用的函数/参数/内存/ISR/DMA及告警门禁，不弱化检查 | 未执行 | 待实际填写 |
| 证据真实 | 命令/cwd/退出码/原始输出/哈希/环境范围一致，未将模拟当HIL | 未执行 | 待实际填写 |

源码或任务不符合时报告REJECTED，不以结果绿灯抵消；环境或来源证据无法核验时按交付门禁§5.3记录阻塞及解除条件，缺条件不得APPROVED。保留未做项，不编造后续运行证据。文档审查用来源/链接/结构/准确差异，不机械要求固件构建或HIL。

## 2. 结果与正常/异常判据

每例列独立预期、输入/故障触发、实际观察、时间期限、退出码及证据。帧层校验、命令语义、事务匹配、端到端物理闭环分别核对；参考工具自身推算的command_valid不能冒充生产实现验证。必跑组/用例缺失或实际case=0时不得通过对应验收。

正常物理查询必须取得符合src/dst/flags/cmd/seq/精确载荷等正式契约的关联响应；零响应、线路噪声、请求回显或MC生成TH固定身份都不能通过。失联、超时、坏帧等负例按既定预期判定：坏CRC应按协议静默丢弃，不将标准NACK作为坏CRC的默认应答。

HIL必须明确真实设备、串口参数、AP/MC/TH实际部署版本与制品哈希，保留带UTC毫秒和单调时钟的逐帧双向原始Hex与关联。联合调试记录与最终独立验收分开；软件PTY/Mock可以验证主机行为，结果不提升为硬件通过。故障夹具先有独立接受、唯一目标绑定、快照/异常恢复/读回证据；写寄存器成功不等于链路恢复。

## 3. 问题、限制与结论

先列问题、缺失证据和未执行项，再给准确范围的APPROVED或REJECTED；待审/报告缺失/调用失败不填APPROVED。单板票只评价本票交付，最终组合才要求参与节点的全部制品和适用物理证据。文档APPROVED不等于源码实施批准、固件接受或HIL通过。

报告自身SHA256由收件者在文件写完后存入任务卡/交接清单，不在报告内容中嵌入自身哈希。新候选重新审核，旧报告和签署保留。审阅者提交结果，唯一COORD核对全部必需签署、同一候选、集成和收件条件后才更新正式status；REJECTED是报告决定，阻塞用blocked字段记录。


## 服务器候选、独立沙箱与内容审计扩展（2026-10-29）

以下写入真实报告的YAML元数据，空值不表示通过。`reviewed_artifacts`逐项覆盖任务交付、准确路径与实际SHA256，所有必需岗位的报告分别绑定本卡revision与实际身份。一个报告承担多个非作者岗位时显式列`reviewer_roles`及各岗位接受范围。

```yaml
actual_session: null # 或actual_thread_id；必须与任务卡session及运行记录一致
reviewer_role: QA
reviewer_roles: [QA]
task_id: null
task_revision: null
reviewed_artifacts: [] # path / sha256，不能只写候选名称或verified
server_qa: null # {path, sha256}，引用下方实际服务器/沙箱记录
content_audit:
  fact_sources: {result: pending, basis: null}
  protocol_compatibility: {result: pending, basis: null}
  claim_scope: {result: pending, basis: null}
  architecture_completeness: {result: pending, basis: null}
# QA报告的非作者复核报告还必须填：
reviewed_qa_report_sha256: null
```

内容审计result仅可在实际核对后写passed；不适用写not-applicable并给依据。引用[交付内容审计表](交付内容审计表.md)，列出事实来源、协议变化兼容和修订任务、设计/代码/硬件等结论层级、架构验收逐项结果。

服务器/沙箱记录为实际runner导出的JSON，并作为证据锁定SHA256：

```json
{
  "task_id": null, "task_revision": null,
  "source": "server-pinned-commits", "fresh_checkout": false,
  "sandbox": {"kind": null, "id": null, "developer_mounts": []},
  "server_lock": {"path": null, "sha256": null},
  "checkout_log": {"path": null, "sha256": null},
  "runtime_log": {"path": null, "sha256": null},
  "server_verdict": {"path": null, "sha256": null}
}
```

`server_lock` JSON包含`repositories`数组，每仓有URL、ref、完整commit及所消费的准确版本；`checkout_log`记录从服务器fetch/checkout与clean检查；`runtime_log`记录镜像digest/VM快照、实际sandbox/会话、账户/挂载/隔离/命令/退出码/日志；`server_verdict`是可定位的可信服务端job/候选/会话与判定记录。源码来自服务器、沙箱隔离和结果真实性由AUTO-01的可信runner核实，不能用手写布尔值、作者目录或本地文件存在代替。离线检查工具只核记录结构/哈希，不提供真实性认证。

任务卡Reviewer的`session_evidence`引用实际Codex/运行器导出，内容可定位该session。QA条目`report_review`记录另一非作者的role/session/session_evidence/reviewed_task_revision/evidence/report_sha256；其报告元数据绑定`reviewed_qa_report_sha256`。保留所有旧报告，新候选新run，不覆写旧签署。

QA报告的非作者复核报告同样填写`server_qa`，在与原QA不同的独立沙箱中复核服务器候选及已发布报告；其沙箱ID必须不同。QA作者交付的预期/工具由ARCH复核时，也须有服务器基线和独立沙箱记录，但不递归要求再为这份ARCH复核无限增加检查层。

## 正常流程覆盖与Issue复验补充（2026-11-02）

适用报告按[交付门禁§4.1～4.3](../delivery_and_coord_gate.md#41-正常流程优先与正负成对验收2026-11-02)和[E2E与Issue规则](../e2e_issue_verification_flow.md)填写。本节补充人工收件核对项，不改变旧报告、原schema或既有决定枚举；文档/软件/HIL批准范围分别注明。

| 功能/用户入口及case ID | 正常/负向/恢复及配对ID | 前置、触发契约与期限来源 | 必需门禁/实际环境 | 实际结果 | 原始证据/哈希及Issue |
| --- | --- | --- | --- | --- | --- |
| 待实际填写，不预勾通过 | 待关联 | 待核实 | document/software/real-hil及实际身份 | 未执行 | 待实际产生 |

列出全量必测项及未实现/冻结的范围说明，分别汇总通过、失败、阻塞、未执行、不适用；不适用附理由及接受依据。页面正确显示未连接只记负例通过，正常连接时超时UNKNOWN记正例失败。真实HIL须将浏览器动作、后台触发、原始请求/响应、硬件效果与页面最终状态关联；纯界面或网络项按实际链路记录适用证据。

结论逐项说明软件门禁和HIL门禁是否必需、是否实际执行及其准确候选；单模块软件接受不外推组合HIL。任一范围内必测项缺失或无证据，不得给该功能/整体验收APPROVED。环境/来源阻塞按交付门禁§5.3记录；报告schema仅支持APPROVED/REJECTED时，缺条件保持待审并注明原因，不能填造APPROVED。

Issue复验逐项关联原失败case、新服务器候选、独立重跑、正常/故障/恢复及受影响回归证据。作者自检或仅不再显示报错不构成修复验收；QA给出实际结果，非作者复核报告后由COORD登记关闭。历史报告的限制或撤回追加到新记录。
