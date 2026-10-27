---
title: 独立 QA 与 QA 作者产物复核报告模板
status: current-template
template_version: '2026-10-27'
updated: '2026-10-27T17:07:21+08:00'
---

# 独立审查报告模板

本模板适用于独立QA，以及QA作者产物的独立ARCH复核；保留实际岗位。按[Codex QA规则](../codex_qa_review.md)运行，审阅者未参与本产物写作，不继承实现完整交互历史，只读业务源码。复制到新的授权run，不覆盖历史报告。

```yaml
template_version: '2026-10-27'
review_id: null
review_status: pending # pending / completed；不是正式任务status
reviewer_role: null # QA 或 QA作者产物的ARCH复核
platform: codex
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

有过程阻断则报告REJECTED，不以结果绿灯抵消；保留未做项，不编造后续运行证据。文档审查用来源/链接/结构/准确差异，不机械要求固件构建或HIL。

## 2. 结果与正常/异常判据

每例列独立预期、输入/故障触发、实际观察、时间期限、退出码及证据。帧层校验、命令语义、事务匹配、端到端物理闭环分别核对；参考工具自身推算的command_valid不能冒充生产实现验证。必跑组/用例缺失或实际case=0时不得通过对应验收。

正常物理查询必须取得符合src/dst/flags/cmd/seq/精确载荷等正式契约的关联响应；零响应、线路噪声、请求回显或MC生成TH固定身份都不能通过。失联、超时、坏帧等负例按既定预期判定：坏CRC应按协议静默丢弃，不将标准NACK作为坏CRC的默认应答。

HIL必须明确真实设备、串口参数、AP/MC/TH实际部署版本与制品哈希，保留带UTC毫秒和单调时钟的逐帧双向原始Hex与关联。联合调试记录与最终独立验收分开；软件PTY/Mock可以验证主机行为，结果不提升为硬件通过。故障夹具先有独立接受、唯一目标绑定、快照/异常恢复/读回证据；写寄存器成功不等于链路恢复。

## 3. 问题、限制与结论

先列问题、缺失证据和未执行项，再给准确范围的APPROVED或REJECTED；待审/报告缺失/调用失败不填APPROVED。单板票只评价本票交付，最终组合才要求参与节点的全部制品和适用物理证据。文档APPROVED不等于源码实施批准、固件接受或HIL通过。

报告自身SHA256由收件者在文件写完后存入任务卡/交接清单，不在报告内容中嵌入自身哈希。新候选重新审核，旧报告和签署保留。审阅者提交结果，唯一COORD核对全部必需签署、同一候选、集成和收件条件后才更新正式status；REJECTED是报告决定，阻塞用blocked字段记录。
