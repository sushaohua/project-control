# 任务模板与流程文档独立复审：review_02

```yaml
review_id: task-template-alignment-20261027-review-02
review_status: completed
reviewer_role: ARCH # QA作者报告模板/流程产物的独立复核，含整组文档差量一致性
platform: codex
actual_session: /root/task_template_review
author_session: /root
task_id: task_template_alignment_20261027 # 文档工作标识，不冒充正式工程卡ID
task_revision: null # 未提供正式任务卡revision；准确版本以下列清单绑定
reviewed_artifact_version:
  manifest: docs/evidence/task_template_alignment_20261027/runs/author_02/candidate_manifest.json
  sha256: 1d5727d812df7f02bf6eb796c3780f98e13f4bd880790f185afe9228ed80744c
verification_environment: local-host-document-review
verification_scope: 七份模板及流程文档的新候选；对review_01问题做差量复审
required_evidence_level: document
process_audit: passed
result_check: passed
decision: APPROVED
accepted_scope: 准确七文件的文档一致性与三项修复；不接受任何源码/固件/HIL/正式任务状态
issues: []
supersedes_or_limits:
  - review_01仍仅对其原候选为REJECTED；本结论仅用于author_02新候选，不改写历史报告
handoff:
  receiver_session: /root
  evidence_location: project-control/docs/evidence/task_template_alignment_20261027/runs/review_02/
```

结论：**APPROVED，仅文档接受**。D1–D3均已修复，未发现本次差量引入新的文档阻断。审阅者仍为未参与写作的原独立Codex会话，仅写本run证据，未更改候选、工程源码、正式卡片或看板；未另行委派。

## 差量复核结果

逐项对照review_01原字节快照与本次实际源文件，差异保存在`revision_delta.patch`及`command_08.stdout.log`。只变化任务卡、QA指引、Codex规则、V2执行指南四份；另三份候选逐字节哈希保持不变。未扩大七文件候选范围。

| 项目 | 本次实际观察 | 决定 |
| --- | --- | --- |
| D1：范围映射字段 | 卡片新增`scope_status: unmapped`，明确Backlog可未映射、Ready前需mapped且落实真实范围。另说明通用卡不等于现有V2专用schema；readiness_pending、case组和证据目录按实际适配，禁止填造字段换绿灯。没有声称工具逻辑被本轮实现。 | 已修复 |
| D2：PA-6负例退出语义 | PA-6改查实际command/cwd/退出码、原始日志与事先接受预期，明确负例可预期非零/无响应；Exit0和零告警限明确要求的构建/正常用例。既有适用构建门禁保留，未放宽编译检查。 | 已修复 |
| D3：中继帧与业务边界 | HW-G6明确允许/要求正式契约规定的路由头、完整帧校验、Hop、ROUTE_IS_ROUTED和CRC处理；禁止中继路径解析cmd业务、解包Payload、修改业务seq、降级文本或伪造下游应答。本机业务/广播消费单独按契约处理，与原生路由依据一致。 | 已修复 |
| 空检查字段/链接 | 新段明确空Reviewer/Verifier/Integrator仅为Backlog占位，派单前按公共规则§4.3矩阵落实，非适用需理由与依据。新增相对链接目标文件及实际标题存在，GitHub标题锚点`43-按任务类型安排检查`对应`4.3 按任务类型安排检查`。 | 通过 |
| 时间化描述 | 执行指南把20张有效V2卡表述为2026-10-27目录采样，后续数量/状态/替代关系回到准确卡，不把指南充当实时投影。本次未重审并发卡片或核定其当前状态。 | 通过 |
| 通用安全要求回归 | YAML默认仍待填/未执行；status、blocked、报告decision分开；Ready不要求本票未来签署；能力前置、跨节点关联不引入反向循环；HIL正常零响应与故障负例分开；历史签署保留、自身报告哈希外置。首轮通过项没有被本次差量撤销。 | 通过 |

独立检查器复跑得到：七候选及六份开工原件SHA256全部匹配；从开工原件重建的完整七文件diff与author_02/candidate.patch完全相同；11份YAML/frontmatter无重复键且解析成功；27个标准Markdown相对链接目标存在；原两模板CRLF及其余LF保持，无行尾空格/tab。限定七路径的`git diff --check`实际exit0；明确使用cr-at-eol识别原CRLF。没有以这些exit0替代本报告独立语义判定。

## 本次准确候选

路径相对于project-control；实际源文件与`reviewed_snapshot/`原字节快照均绑定以下哈希。收件清单副本为`reviewed_candidate_manifest.json`。

| 路径 | SHA256 |
| --- | --- |
| `.agents/rules/templates/任务卡模板.md` | `6121c4a99a5e155b5bf56c25115f67bc61e56274e431390bc1c8ba0ddc486ce6` |
| `.agents/rules/templates/角色任务提示词.md` | `aa2a3f07753bf90dc20ea4aca749b974514b2ddd9dc6844c7aa422e42fe1eda9` |
| `docs/guides/templates/task_run_record.md` | `79b7132f1732ac453d690ba3450e5082f935e1d6be3d42d364f4e379383ed6c2` |
| `.agents/rules/qa_audit_checklist_guide_20261013_115611.md` | `747a464dcacaa4e5f342b0875e49de972b2dcbcb6abc6208204f037d93c34aa7` |
| `.agents/rules/codex_qa_review.md` | `90d41e689ea9bf7d6943f987d6a54440141b2775033fbcd66a79895976ba4f4c` |
| `docs/guides/minimc_v2_task_execution.md` | `1b0d51ba17f18369965e70f03caa71246bb27d07c13eee12df94c21ce3d67559` |
| `.agents/rules/templates/QA审查报告模板.md` | `9f8687eb89eb2ad4b4a304709fbcfed47488b06073656204c841b559cbefbba6` |

## 实际命令、原始证据与限制

`commands.json`记录下列实际argv、cwd、UTC起止、退出码、完整stdout/stderr路径及SHA256。全部cwd为`/home/sushaohua/workspace/ai_soc_project/project-control`；Python 3.8.10、PyYAML 5.3.1。每项原始输出为`command_01`至`command_08`的`.stdout.log`/`.stderr.log`，没有覆写review_01。

| 编号 | 实际命令或准确用途 | exit |
| --- | --- | --- |
| 01 | `python3 -B .../review_02/independent_checks.py`；本审阅会话原独立检查器针对新候选复跑，额外核unmapped默认 | 0 |
| 02 | `git -c core.whitespace=blank-at-eol,blank-at-eof,space-before-tab,cr-at-eol diff --check -- <准确七路径>` | 0 |
| 03 | `cat ../AGENTS.md manifest.yaml .agents/rules/codex_qa_review.md`；重新核独立规范及canonical位置 | 0 |
| 04 | `cat <准确七路径>`；收件原文保存 | 0 |
| 05 | `sed -n 68,96p tools/check_task_graph.py`；现有字段要求原文，仅只读 | 0 |
| 06 | `sed -n 80,119p .agents/rules/04_公共看板与读写协议.md`；岗位矩阵依据 | 0 |
| 07 | `sed -n '124,155p;176,181p' docs/specs/ap_mc_formal_protocol_v2_0_multidevice_routing_draft_20261015.md`；帧路由正式依据 | 0 |
| 08 | `cat .../review_02/revision_delta.patch`；实际首轮/次轮差量原文 | 0 |

未运行工程构建、业务/正式任务验收、全图任务检查器、HIL、硬件操作、部署或推送；未宣称任何真实链路、固件、能力门或工具自动化已经验证。检查脚本只是本次文档证据，未修改项目工具。初始探查、差量生成、快照/锚点核对操作的工具事件保留于本独立会话，相关原文和输出另存本run。

本次授权仅差量复核及必要结构回归；未提供正式工程任务卡revision，因此本报告不接受任何正式卡Ready/Done，也不重审并发看板、此前方案或已完成历史签署。普通文档接受不等于源码实施授权、MCU Owner/HUMAN批准、固件接受或HIL通过。COORD需另行核对并收件；报告本身不推进正式状态。报告自身SHA256在写完后存本run外部交接清单，避免自引用。
