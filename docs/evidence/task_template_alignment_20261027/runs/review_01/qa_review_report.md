# 任务模板与流程文档独立审查：review_01

```yaml
review_id: task-template-alignment-20261027-review-01
review_status: completed
reviewer_role: ARCH # 对QA报告模板与QA规范产物进行独立复核；并核对整组文档一致性
platform: codex
actual_session: /root/task_template_review
author_session: /root
task_id: task_template_alignment_20261027 # 本轮文档工作标识，不冒充正式工程任务卡ID
task_revision: null # 派单未提供正式任务卡revision；以以下准确候选清单绑定本轮
reviewed_artifact_version:
  manifest: docs/evidence/task_template_alignment_20261027/runs/author_01/candidate_manifest.json
  sha256: a6a6de2540d806929b08f8fd1da03f7ccd1b427ccc1b0f3ec3578f33cb60b99d
verification_environment: local-host-document-review
verification_scope: 七份模板及流程文档；含QA作者模板独立复核
required_evidence_level: document
process_audit: passed-with-scope-limitations
result_check: failed
decision: REJECTED
accepted_scope: null
handoff:
  receiver_session: /root
  evidence_location: project-control/docs/evidence/task_template_alignment_20261027/runs/review_01/
```

本报告只审派单给定七份候选和必要的权威规则/字段依据，不修改候选、正式卡、看板或业务源码。审阅者由独立会话承担，未参与候选写作；收到的是任务、规范、候选与原始材料，未接收作者实现交互历史。作者在检查期间提示四个待核点；本报告均用实际文件和规则独立判断，未将提示视为审查结论。未另行委派。

## 1. 阻断项

| 编号 | 位置与实际观察 | 影响与修复要求 |
| --- | --- | --- |
| D1 | `.agents/rules/templates/任务卡模板.md:23` 起的生命周期/范围字段没有 `scope_status`。现有 `tools/check_task_graph.py:76` 将其列为必填，`:89` 要求为 `mapped`；通用卡和执行指南却未说明该字段如何从未映射转为已映射。 | 新建V2卡即使按当前模板填写范围，仍会因缺字段被现有结构检查拒绝。补安全的未映射默认值、实际映射与Ready的关系；不能默认mapped或声称新增自动检查已生效。现有工具另要求readiness_pending等V2字段，可明确通用模板仍需V2适配，不要求本次改工具或大规模迁移旧卡。 |
| D2 | `.agents/rules/qa_audit_checklist_guide_20261013_115611.md:73` 的PA-6“一票否决”仍写“缺乏 Exit Code 0 和 0 Warning”的终端日志。该文`:18`、运行记录模板及报告模板又允许按冻结预期接受非零退出/无响应负例。 | 合格的负例实际exit非零会被PA-6直接否决，过程否决与结果判定相互冲突。将PA-6改为核对真实命令、实际退出/告警与事先接受预期的一致性；构建exit0/零告警仍按适用构建门禁保持。 |
| D3 | `.agents/rules/codex_qa_review.md:56` 无限定地禁止中间路由节点“解包”。正式协议§2.2及§3.3明确中间节点必须检查DST、处理hop_limit/route_ctrl并重算CRC。 | “解包”可被理解为连必要帧头解析都禁止，使工程执行/QA判定无法一致。明确禁止业务payload解析、业务cmd转译和伪造下游成功，同时允许/要求正式契约规定的帧头校验与路由处理。无需改变正式协议或批准任何固件实施。 |

三项均属于本组模板/流程一致性修正；作者修复后必须提交新候选、新哈希并在新run复审，本结论不自动适用于后续内容。

## 2. 已完成核查

独立脚本核对七份候选与六份开工原件的SHA256，重建的七文件规范化差异与作者candidate.patch逐字符一致；新QA模板无before原件。准确路径、前后哈希、YAML块和行尾计数保存在`command_01.stdout.log`，七份候选原字节快照另存`reviewed_snapshot/`。

| 检查 | 实际结果与判定 |
| --- | --- |
| YAML及默认值 | 11份frontmatter/YAML块均可用PyYAML 5.3.1解析且无重复键；QA decision=null、pending/未执行，运行记录not-executed，未预勾选；检查通过不代替语义接受。 |
| 对象层级 | policy和卡片中的review_assignments.reviewer_sessions元素字段集合一致；verifier的候选/revision/决定/报告哈希字段位于review_assignments；独立运行记录使用independent_reviews数组。报告actual_session、reviewed_artifact_version是报告域，与卡片session、artifact_version对应，不要求不同文档对象同名。 |
| 必需岗位与空值 | 卡片正文明确逐项必需Reviewer、作者不能自批、不适用需说明、不可删岗位，且引用canonical 04 §4.3已有任务类型矩阵。因此空reviewer/verifier/integrator是待填写占位，不是额外独立阻断；建议换为明确可点击的相对链接并重申空值不能进入Ready，不必重复整张矩阵。 |
| Ready与后续阶段 | Ready要求输入能力、实际安排/范围/资源/租约，不要求本票未来候选与签署；Review/Verify/Done核同一候选、所有必需接受、适用运行/集成与COORD收件。未发现自引用开工条件。D1的字段缺口仍须修复。 |
| 能力及跨节点关联 | dependency_conditions明示与depends_on对应；父任务能力需落实；coordination仅关联目录；最终HIL不得反向作为单板实施前置。单板产物与最终组合产物范围分别说明。未建立实际任务图，也未宣称实际工程依赖已满足。 |
| 状态/决定/撤回 | status六态、blocked及恢复条件、APPROVED/REJECTED决定分开；历史accepted/旧报告保留；新版本重新审查；报告自身哈希在外部卡片/交接登记，避免自引用。 |
| HIL正常与负例 | 正常查询零有效关联响应失败；断链/坏帧按冻结无响应/错误预期判定；禁止Mock替代物理HIL。PA-6残留冲突列D2；路由措辞列D3。 |
| 链接/格式 | 26个标准Markdown相对链接目标存在；检查路径目标，不推断目标文档内容已被本次接受。两份原模板保持纯CRLF，其他文件纯LF；无行尾空格/tab；受限七路径git diff --check exit0（明确启用cr-at-eol识别原CRLF）。历史Obsidian wikilink保持原表示，不把它们伪称成标准Markdown解析检查结果。 |
| 工具与范围 | 候选明确文档规则、人工核对、现有工具能力三者边界，没有把模板修改称为自动门禁已部署。重建差异限准确七文件；并发卡/看板修改与以前未跟踪方案不纳入本候选、未回退或代签。 |

## 3. 准确候选哈希

以下路径均相对于project-control；原件与候选清单SHA256经过独立检查。

| 路径 | 本次候选SHA256 |
| --- | --- |
| `.agents/rules/templates/任务卡模板.md` | `0a290d6e8ddc2ea19b7313677b6ea39da8924083f389d96f6ea04de424e4a1ab` |
| `.agents/rules/templates/角色任务提示词.md` | `aa2a3f07753bf90dc20ea4aca749b974514b2ddd9dc6844c7aa422e42fe1eda9` |
| `docs/guides/templates/task_run_record.md` | `79b7132f1732ac453d690ba3450e5082f935e1d6be3d42d364f4e379383ed6c2` |
| `.agents/rules/qa_audit_checklist_guide_20261013_115611.md` | `4a405e1e06dedc13a857d82e6838cdb9eeebf4eb77d7bd7c62a6960d91ce0ee8` |
| `.agents/rules/codex_qa_review.md` | `7f8723fa9ec8da48e7d9e7b4e6a2628299cce83732bd72aefd77772f128c90fa` |
| `docs/guides/minimc_v2_task_execution.md` | `7eb733f76e9a846d0bcab5f58fba9377f911e3654ce00c02599a1f1943b61990` |
| `.agents/rules/templates/QA审查报告模板.md` | `9f8687eb89eb2ad4b4a304709fbcfed47488b06073656204c841b559cbefbba6` |

## 4. 实际命令及证据

所有下表命令cwd均为`/home/sushaohua/workspace/ai_soc_project/project-control`，实际起止UTC时间、完整argv、退出码、完整stdout/stderr路径及SHA256在`commands.json`。运行器`run_commands.py`和独立检查器`independent_checks.py`保留原件；没有执行作者自检脚本来代替独立检查。

| 编号 | 实际命令/用途 | 实际退出码 | 原始输出 |
| --- | --- | --- | --- |
| 01 | `python3 -B .../review_01/independent_checks.py`：准确哈希、YAML/重复键、空默认、层级、链接、行尾与差异重建 | 0 | `command_01.stdout.log` / `.stderr.log` |
| 02 | `git -c core.whitespace=blank-at-eol,blank-at-eof,space-before-tab,cr-at-eol diff --check -- <准确七路径>`：格式核对 | 0 | `command_02.stdout.log` / `.stderr.log` |
| 03 | `cat ../AGENTS.md manifest.yaml .agents/rules/codex_qa_review.md`：权限、canonical及独立规则 | 0 | `command_03.stdout.log` / `.stderr.log` |
| 04 | `cat <准确七路径>`：独立全文检查与原始收件文本 | 0 | `command_04.stdout.log` / `.stderr.log` |
| 05 | `sed -n 68,96p tools/check_task_graph.py`：核对现有必填字段依据 | 0 | `command_05.stdout.log` / `.stderr.log` |
| 06 | `sed -n 80,119p .agents/rules/04_公共看板与读写协议.md`：岗位/不适用与任务类型规则 | 0 | `command_06.stdout.log` / `.stderr.log` |
| 07 | `sed -n '124,155p;176,181p' docs/specs/ap_mc_formal_protocol_v2_0_multidevice_routing_draft_20261015.md`：路由帧处理权威依据 | 0 | `command_07.stdout.log` / `.stderr.log` |

结构类11块YAML、26链接及7文件哈希检查均实际执行，语义判定以本报告逐项独立审阅为准；未靠exit0给出APPROVED。初始只读探查工具事件保留于本会话；必要文件内容与判断依据随后通过03–07重新读取并持久保存，未将历史未记录命令当作工程验证证据。

## 5. 限制、未执行及交接

- 未运行工程构建、生产测试、任务全图检查器、HIL、硬件/寄存器操作、部署或推送；这些均不属于本次文档QA授权范围。没有工程正常/负例case通过结论。
- 正式任务卡revision未提供；本报告仅绑定精确七文件清单哈希和原字节快照，不签署任何现有正式工程票Ready、Done或能力条件已满足。
- 以作者开工原字节与候选精确差异审查范围；没有审计工作区所有并发修改，也没有复核链接所指历史方案的全部内容。
- 本次是QA作者模板及流程规范的独立文档复核，结论REJECTED，交回作者修复D1–D3；不会修改正式status。报告自身SHA256应在写完后由收件/外部交接清单登记，不嵌入本报告。
