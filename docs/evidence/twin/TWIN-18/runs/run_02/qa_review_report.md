---
template_version: '2026-10-27'
review_id: TWIN-18-run02-QA-rereview
review_status: completed
reviewer_role: QA
reviewer_roles: [QA]
platform: codex
requested_model: gpt-6-luna
actual_model: gpt-6-luna
model_override_ref: null
planned_session_alias: codex-qa-twin-18-run02-rereview
actual_session: 01a18a85-5f09-7283-b4a5-321509554a35
author_session: null
task_id: TWIN-18
task_revision: 2
run_id: run_02
reviewed_artifact_version: 'project-control=7fc4f26078326f2c5381921dac82fc80c55db0aa; mcu-p3=1246ea9cb441d074ea444f53320f5632fefcd503; test_harness=210ddd1c3f6f59594836c91b68aae55fb7a35181; soc-ap=dd0eefb9e5e966908f1c5a96848fd92787592dd0'
reviewed_artifacts:
  - path: project-control/docs/specs/mcu_motion_leveling_filament_interface_survey_20261029.md
    sha256: 596b4e84252fd71332865663a31187d40e5826ab345712bec34d40eca1f2f4ea
    commit: 7fc4f26078326f2c5381921dac82fc80c55db0aa
  - path: project-control/docs/evidence/twin/TWIN-18/runs/run_02/result.md
    sha256: fcc4ad4e601c48b0e5a885110944243149df68bb50fe15984bf12cc639660fcc
    commit: 7fc4f26078326f2c5381921dac82fc80c55db0aa
  - path: mcu-p3 source baseline
    commit: 1246ea9cb441d074ea444f53320f5632fefcd503
  - path: test_harness candidate
    commit: 210ddd1c3f6f59594836c91b68aae55fb7a35181
  - path: soc-ap candidate
    commit: dd0eefb9e5e966908f1c5a96848fd92787592dd0
protocol_and_expectations:
  - 'TWIN-18 revision 2 scope, run_01 findings TWIN18-QA-01 through TWIN18-QA-04, and run_02's explicit COL-007 4-byte event_id + 4-byte timestamp_tick_ms check.'
  - 'Survey §5/§6 protocol reconciliation, including run_02 check criterion that COL-007 carries a 4-byte event_id and 4-byte timestamp_tick_ms; MC source facts at mcu-p3 1246ea9cb441d074ea444f53320f5632fefcd503.'
verification_environment: 'Fresh exact-SHA fetches to /tmp and read-only content inspection of those candidate files; supplied Docker server_qa evidence independently checked. This reviewer did not use the author worktree as source baseline.'
verification_scope: 'Independent document/source audit, run_01 finding re-review, server commit/ref check, supplied server QA record and task graph count check; no firmware build or hardware operation.'
required_evidence_level: document
review_time: '2026-10-30 Asia/Shanghai'
process_audit: completed-with-blockers
result_check: failed
decision: REJECTED
accepted_scope: 'Verified all four exact commits are fetchable from origin; survey SHA matches; The §5/§6 internal MOT-001/MOT-002/COL-007 contradictions are corrected; selected source anchors match pinned mcu-p3; task graph reports 108 canonical tasks and 66 microtasks. Formal acceptance is blocked by a COL-007 layout mismatch, recurring inaccurate ref metadata, and a writable sandbox mount.'
limitations:
  - 'No firmware build, automated firmware test, physical MCU operation, or HIL was executed or required for this document-level review.'
  - 'The sandbox evidence records /workspace as RW=true. It therefore does not establish the read-only candidate snapshot required by the governing QA rules.'
  - 'The review report itself still requires a separate non-author review. COORD must bind that review and this report hash before formal receipt.'
  - 'The survey spells the MOT-002 dimensions/array as grid_points_x, grid_points_y, and z_offset_um[25]; those names are internally consistent between §5 and §6, although they differ from the shorthand spellings in the review request.'
issues:
  - id: TWIN18-QA-02
    severity: blocker
    summary: 'The server lock still claims non-advertised refs/heads/<commit> instead of recording a valid advertised ref or a commit-addressed fetch.'
    evidence: 'For all four candidates, git ls-remote <origin> refs/heads/<full-SHA> returned no rows. Direct git fetch <origin> <full-SHA> succeeded and FETCH_HEAD equaled the requested SHA for each repository. The source commits are available, but the ref metadata remains inaccurate and repeats run_01 finding TWIN18-QA-02.'
    required_fix: 'COORD must pause ordinary author-retry per delivery_and_coord_gate.md §5.1(3), align ARCH and QA on an acceptable candidate locator, then record actual advertised refs or explicitly label each candidate as commit-addressed without claiming refs/heads/<SHA>. Keep the exact SHA values and run_01 history.'
  - id: TWIN18-QA-06
    severity: blocker
    summary: 'COL-007 does not use the 4-byte event_id field required by the run_02 review criterion.'
    evidence: 'The criterion supplied for this re-review specifies an 8-byte payload composed of a 4-byte event_id and a 4-byte timestamp_tick_ms. The pinned survey instead defines uint8_t alarm_level, uint8_t subsystem_id, uint16_t error_code, uint32_t timestamp_tick_ms. Although §5 and §6 agree with each other on that 8-byte layout, the first four bytes are not a single event_id field and have different semantics.'
    required_fix: 'ARCH/COORD must clarify whether event_id is an accepted alias for the three existing alarm metadata fields or revise the accepted criterion/protocol layout. Do not freeze downstream field names or semantics until the interpretation is explicit.'
  - id: TWIN18-QA-05
    severity: blocker
    summary: 'The recorded QA container mounted the candidate workspace read/write.'
    evidence: 'run_02 server_qa.json and runtime.log contain Docker Inspect mount Destination=/workspace, Mode=rw, RW=true. The container/image identity is present, but a writable source mount does not meet the read-only candidate snapshot and isolation requirement in delivery_and_coord_gate.md §3/§3.1.'
    required_fix: 'For formal server QA, use an independently fetched candidate snapshot mounted read-only (or another compliant controlled export), preserve new inspect/runtime evidence, and verify it is the same four locked commits.'
commands:
  - command: 'git fetch <origin> <full-commit-sha>; git rev-parse FETCH_HEAD (four repositories)'
    cwd: '/tmp/twin18_run02_{project-control,mcu-p3,test_harness,soc-ap}'
    tool_version: 'git'
    time: '2026-10-30'
    exit_code: 0
    output: 'Each FETCH_HEAD matched the requested commit exactly; transcript: docs/evidence/twin/TWIN-18/runs/run_02/qa_audit.log; sha256=663ac669e63e693f41e14c2661016ce3fe39652ce18980190fd50e9093cc057e.'
  - command: 'git ls-remote <origin> refs/heads/<full-commit-sha> (four repositories)'
    cwd: '/tmp'
    tool_version: 'git'
    time: '2026-10-30'
    exit_code: 0
    output: 'All four queries returned no advertised ref rows; transcript: docs/evidence/twin/TWIN-18/runs/run_02/qa_audit.log, sha256=663ac669e63e693f41e14c2661016ce3fe39652ce18980190fd50e9093cc057e.'
  - command: 'PYTHONDONTWRITEBYTECODE=1 python3 tools/check_task_graph.py --workspace ..'
    cwd: '/tmp/twin18_run02_workspace/project-control'
    tool_version: 'Python 3'
    time: '2026-10-30'
    exit_code: 0
    output: 'canonical_task_count=108; microtask_count=66; errors=[]; full output in docs/evidence/twin/TWIN-18/runs/run_02/qa_audit.log (sha256=663ac669e63e693f41e14c2661016ce3fe39652ce18980190fd50e9093cc057e).'
  - command: 'sha256sum survey, result, server_qa.json, server_lock.json, checkout.log, runtime.log, server_verdict.json'
    cwd: '/home/sushaohua/workspace/ai_soc_project'
    tool_version: 'sha256 via Python hashlib'
    time: '2026-10-30'
    exit_code: 0
    output: 'Survey and evidence digests are recorded in qa_audit.log; server_qa.json sha256=17f54a9964260e9770de2ba78ce54d4d1060080648555068436fa49c89889139; server_lock sha256=5aecd1e4d269e9beedd15708f41f22581937529f97d7e170057b6c2734cec892.'
  - command: 'Inspect pinned MCU source anchors for current_position, bed_level/G29, A_DET/PD2 and filament polling/debounce/event.'
    cwd: '/tmp/twin18_run02_mcu-p3'
    tool_version: 'rg / source line inspection'
    time: '2026-10-30'
    exit_code: 0
    output: 'Source observations summarized below; commit 1246ea9cb441d074ea444f53320f5632fefcd503.'
case_results:
  - case: TWIN18-QA-01 internal protocol matrix/detail alignment
    expected: '§5 reconciliation matrix and §6 packet layouts use identical command IDs, sizes and field meanings.'
    observed: 'The previous internal contradictions are removed: MOT-001 is 0x16/20 bytes; MOT-002 is 0x18/52 bytes with grid_points_x, grid_points_y, z_offset_um[25]; COL-007 is 0x50 with an 8-byte payload including timestamp_tick_ms.'
    verdict: passed
    evidence: 'Pinned survey SHA 596b4e84252fd71332865663a31187d40e5826ab345712bec34d40eca1f2f4ea, §5 and §6.'
  - case: run_02 COL-007 field layout criterion
    expected: '8-byte payload consists of a 4-byte event_id and a 4-byte timestamp_tick_ms.'
    observed: 'The document defines alarm_level:uint8_t, subsystem_id:uint8_t, error_code:uint16_t, timestamp_tick_ms:uint32_t. The first four bytes are three distinct alarm metadata fields; no event_id field is defined.'
    verdict: failed
    evidence: 'Pinned survey §5 COL-007 row and §6.3 minimc_alarm_event_payload_t.'
  - case: run_01 findings TWIN18-QA-02/03 candidate and runner evidence
    expected: 'All source repositories and their exact commits are pinned; graph output is non-empty and runner verdict is limited to recorded checks.'
    observed: 'server_lock lists project-control, mcu-p3, test_harness and soc-ap with full commits. All direct SHA fetches succeed; named refs are absent (TWIN18-QA-02 remains open). check_task_graph reports 108/66. Server runner records graph validation, artifact existence and survey SHA checks only; it has no build or content-test result.'
    verdict: failed
    evidence: 'server_qa.json sha256 17f54a9964260e9770de2ba78ce54d4d1060080648555068436fa49c89889139; server_lock.json; server_verdict.json; qa_audit.log.'
  - case: run_01 finding TWIN18-QA-04 reviewer identity
    expected: 'A distinct actual reviewer session and usable session evidence are bound to this report.'
    observed: 'This run has actual thread ID 01a18a85-5f09-7283-b4a5-321509554a35 in run_02/codex_session.jsonl. The pinned task card has not yet recorded this review assignment; author session identity was not provided in the reviewed run inputs.'
    verdict: passed-with-recording-follow-up
    evidence: 'docs/evidence/twin/TWIN-18/runs/run_02/codex_session.jsonl; task card reviewer assignments in candidate project-control commit.'
  - case: motion, bed leveling, and runout sensor source anchors
    expected: 'Survey facts are supported by exact mcu-p3 source at the pinned commit.'
    observed: 'current_position is at motion-controller Marlin_main.c:392; bed_level declaration is at Marlin_main.c:528 and G29 stores measured_z at :2737; TH A_LIMIT_PIN is GPIO_PINS_2 and A_LIMIT_GPIO_PORT is GPIOD in color-engine io_toggle/inc/pins.h:20-21, A_DET is :45; motherboard.c defines a 1,000,000-us poll and 10 low samples at :9-10 and sends filaout at :64.'
    verdict: passed
    evidence: 'mcu-p3 commit 1246ea9cb441d074ea444f53320f5632fefcd503; source paths/anchors above.'
  - case: sandbox source isolation
    expected: 'Container evidence shows controlled read-only candidate source mount and accurate inspect evidence.'
    observed: 'Container/image digest and full container ID are recorded; /workspace mount is RW=true.'
    verdict: failed
    evidence: 'run_02/server_qa/runtime.log and server_qa.json.'
required_test_sets: []
executed_test_sets:
  - 'Four direct origin SHA fetches and ref advertisement checks.'
  - 'Task graph static validation from exact archived commits: 108 canonical tasks / 66 microtasks.'
  - 'Read-only survey/source inspection and artifact SHA verification.'
missing_test_sets:
  - 'No build, firmware test, content-specific automated test, or HIL was run; no such result is claimed.'
raw_trace_files: []
supersedes_or_limits:
  - 'This report re-reviews only TWIN-18 task revision 2 run_02 documents and the listed server candidates. It does not approve firmware implementation, build, device behavior, or HIL.'
handoff:
  receiver_session: null
  evidence_location: project-control/docs/evidence/twin/TWIN-18/runs/run_02/
server_qa:
  path: project-control/docs/evidence/twin/TWIN-18/runs/run_02/server_qa/server_qa.json
  sha256: 17f54a9964260e9770de2ba78ce54d4d1060080648555068436fa49c89889139
  server_verdict_path: project-control/docs/evidence/twin/TWIN-18/runs/run_02/server_qa/server_verdict.json
  server_verdict_sha256: b8235b5215d8f7591c045ef82c33df161ce7a79c2cea827dcde5bd14372237e1
  container_id: c566ca46b28f375972ed0f5f11469b1a1dce499674896bbd746535e1222691f7
  image_digest: sha256:43a2f1c6c95b1df70095eb744d5eadc9225867e0d7a2feda9b41ec3b6d38c825
content_audit:
  fact_sources: {result: passed, basis: 'Checked exact motion/leveling/runout anchors against mcu-p3 commit 1246ea9cb441d074ea444f53320f5632fefcd503.'}
  protocol_compatibility: {result: failed, basis: '§5 and §6 are internally consistent, but COL-007 does not meet the run_02 review criterion of a 4-byte event_id plus a 4-byte timestamp_tick_ms: the first four bytes are alarm_level, subsystem_id, and uint16_t error_code.'}
  claim_scope: {result: passed, basis: 'Survey separates document/software proposals from physical HIL; this review claims no build or hardware acceptance.'}
  architecture_completeness: {result: not-applicable, basis: 'This is an interface/source survey, not a runtime architecture implementation acceptance.'}
reviewer_session_evidence: 'project-control/docs/evidence/twin/TWIN-18/runs/run_02/codex_session.jsonl (thread.started ID matches actual_session)'
reviewed_qa_report_sha256: null # This report requires separate non-author review; not self-reviewed.
---

# TWIN-18 run_02 独立 QA 复审报告

## 1. 身份、候选与过程核查

本次审核仅使用从 origin 精确 fetch 的四仓提交，不采用作者工作树作为源码基线：project-control `7fc4f26078326f2c5381921dac82fc80c55db0aa`、mcu-p3 `1246ea9cb441d074ea444f53320f5632fefcd503`、test_harness `210ddd1c3f6f59594836c91b68aae55fb7a35181`、soc-ap `dd0eefb9e5e966908f1c5a96848fd92787592dd0`。四个对象均直接从 origin fetch 成功，`FETCH_HEAD` 与锁定 SHA 完全一致；但锁内 `refs/heads/<SHA>` 均未由 `git ls-remote` 公布。此前 TWIN18-QA-02 要求将其改为真实远端 ref 或明确写为 commit-addressed fetch，本 run 仍未修正，属于同一阻断根因复发。

实际审阅 thread ID 为 `01a18a85-5f09-7283-b4a5-321509554a35`，记录在 `codex_session.jsonl`。候选任务卡尚未登记本次 reviewer assignment，输入中也没有可核对的作者 session 标识；因此本报告将 review session 明确绑定，但不声称完成作者/Reviewer 的任务卡登记。报告仍需另一非作者复核并由 COORD 收件。

服务器证据容器 ID 为 `c566ca46b28f375972ed0f5f11469b1a1dce499674896bbd746535e1222691f7`，镜像 digest 为 `sha256:43a2f1c6c95b1df70095eb744d5eadc9225867e0d7a2feda9b41ec3b6d38c825`；二者与运行记录一致。但 Docker Inspect 显示 `/workspace` bind mount `Mode=rw`, `RW=true`。这不满足规则要求的只读候选快照。server_qa 仅记录三项检查：任务图结构验证、目标文件存在及文档 SHA 校验；`build_count=0`，没有自动化协议内容测试。任务图输出范围明确为静态计划验证，并报告 108 个 canonical tasks、66 个 microtasks。本次也从四个准确提交归档重跑，得到相同的 108/66 计数。

检查命令与证据摘要见 `qa_audit.log`（SHA256：`663ac669e63e693f41e14c2661016ce3fe39652ce18980190fd50e9093cc057e`）。服务器 `server_qa.json` SHA256 为 `17f54a9964260e9770de2ba78ce54d4d1060080648555068436fa49c89889139`；其锁文件 SHA256 为 `5aecd1e4d269e9beedd15708f41f22581937529f97d7e170057b6c2734cec892`。

## 2. 结果与正常/异常判据

### 已通过

- **TWIN18-QA-01 的原始矩阵/布局冲突已修正：** §5 与 §6.1-§6.3 均将 MOT-001 定为 `0x16`、20 字节响应；MOT-002 定为 `0x18`、52 字节响应，布局为两个维度字节及 25 个 `int16_t`；COL-007 均以 8 字节载荷结束于 `uint32_t timestamp_tick_ms`。上一版的 `0x40/0x16` 歧义、MOT-002 54 字节布局及 COL-007 尾字段冲突均不再出现。文件中的 MOT-002 字段原文是 `grid_points_x`、`grid_points_y`、`z_offset_um[25]`。但 COL-007 前四字节与本轮明列的 4 字节 `event_id` 预期不相符，见新阻断项 TWIN18-QA-06。
- **TWIN18-QA-03 任务图与 runner 范围：** 任务图在锁定快照中报告 108/66。runner 结果实际限于任务图、文件存在和 SHA256 三项；本报告不将其当作协议内容测试或固件验收。mcu-p3 源码现已纳入四仓 `server_lock`。
- **MC 运动与调平锚点：** 在 mcu-p3 锁定提交中确认 `current_position` 声明于 `motion-controller-mcu/project/marlin/marlin_core/Marlin_main.c:392`；`bed_level` 声明于同文件 `:528`，G29 测点写入 `measured_z` 于 `:2737`。配置中 `NUM_AXIS=9` 与 `COREXY` 分别位于 `configure.h:22`、`:39`。
- **TH 断料传感器锚点：** `color-engine-mcu/io_toggle/inc/pins.h:20-21` 将 `A_LIMIT_PIN` 定义为 GPIO_PINS_2、端口定义为 GPIOD；`:45` 的 `A_DET` 使用该输入。`motherboard.c:9-10` 为 1 秒轮询与 10 次低电平门限，`:64` 发送既有 ASCII `filaout\r\n`。这些事实支持“当前代码现状”调查；新 `0x50` 二进制报文仍是拟议接口，未被误报为现有固件实现。
- **范围边界：** 本票是文档/源码调查。没有固件构建、MCU 运行、物理运动、探针或断料 HIL 证据，本报告不将文档审查提升为硬件通过。

### 未通过及需升级

1. **TWIN18-QA-06 COL-007 字段定义不满足本轮明确判据（阻断）：** 虽然 §5/§6 内部一致，指定的 4 字节 event_id 在定义中不存在。需由 ARCH/COORD 澄清该字段与 alarm_level/subsystem_id/error_code 的语义关系，或修订正式验收判据；澄清前不得冻结下游接口。
2. **TWIN18-QA-02 同因复发（阻断）：** 四个提交 SHA 均可直接 fetch，但 server_lock 仍将非广告 ref `refs/heads/<SHA>` 写成候选引用。由于 run_01 已指出同一问题，依据 delivery_and_coord_gate.md §5.1(3)，COORD 应先暂停常规作者重试，组织 ARCH 与 QA 冻结准确、可执行的候选定位判据，再决定是否修订锁文件/新候选。
3. **Sandbox 只读隔离不合规（阻断）：** 容器 `/workspace` 是 RW bind mount。所给证据不能证明只读候选快照，不能作为符合规则的正式隔离 QA 证据。需要以只读候选重新运行并保留新的 inspect/runtime 物证。
4. **MOT-002 字段标识差异记录：** 请求中的字段简称是 `grid_size_x/grid_size_y/z_offsets_um[25]`；受审文件实际采用 `grid_points_x/grid_points_y/z_offset_um[25]`。两处文档内部一致、总大小都是 52 字节；如字段名需逐字冻结，应由 ARCH 明确采用名称。

## 3. 问题、限制与结论

**决定：REJECTED。** 文档已修正 §5/§6 的内部布局冲突，源码锚点与静态任务图数量也得到验证；但 COL-007 未满足本轮明确的 `event_id` 字段判据。正式通过另被重复出现的 server ref 元数据缺陷和可写容器挂载阻断；其中 TWIN18-QA-02 是 run_01 同根因复发，必须按 §5.1(3) 升级并先冻结验收判据，不能直接开始又一轮无差异返工。此报告仅审查列出的 TWIN-18 revision 2 文档和服务器提交，不接受固件实现、构建、物理 MCU 或 HIL。

报告自身 SHA256 由 COORD 收件时从文件字节计算并登记；此报告未自我复核。QA 报告还需一位非作者 Reviewer 复核后方可完成正式收件。
