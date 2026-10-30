---
template_version: '2026-10-27'
review_id: TWIN-18-r1-run_01-QA
review_status: completed
reviewer_role: QA
reviewer_roles: [QA]
platform: codex
requested_model: gpt-6-luna
actual_model: gpt-6-luna
model_override_ref: null
planned_session_alias: planned-qa-twin-18
actual_session: null # 本运行接口未向审阅者暴露可核验的 Session UUID；未以作者会话记录代填
author_session: null
task_id: TWIN-18
task_revision: 1
reviewed_artifact_version: 'project-control=03dd0d1fef94545f844dbf70470958d783a6f2aa; test_harness=210ddd1c3f6f59594836c91b68aae55fb7a35181; mcu-p3 source=1246ea9cb441d074ea444f53320f5632fefcd503'
reviewed_artifacts:
  - path: project-control/docs/specs/mcu_motion_leveling_filament_interface_survey_20261029.md
    sha256: caffb64413d745e513ef5947e8d7c29c0f5ac70fa24e0523ebe7bed565629e38
    commit: 03dd0d1fef94545f844dbf70470958d783a6f2aa
  - path: project-control/docs/evidence/twin/TWIN-18/runs/run_01/result.md
    sha256: 46eaa6c157c5a1c2fbce1cebf3d824eb54ba9a3b1500f399f5b8c18f8a4e2eea
    commit: 03dd0d1fef94545f844dbf70470958d783a6f2aa
  - path: test_harness server candidate
    commit: 210ddd1c3f6f59594836c91b68aae55fb7a35181
  - path: mcu-p3 read-only source baseline
    commit: 1246ea9cb441d074ea444f53320f5632fefcd503
protocol_and_expectations:
  - 'TWIN-18 revision 1 acceptance: source-anchored X/Y/Z/E, 5x5 leveling grid, TH runout pin/debounce/event and software/HIL separation.'
  - 'TWIN-18 deliverable matrix: MOT-001 0x16, MOT-002 0x18, COL-007 0x50 / HMS 0x3001.'
verification_environment: 'Read-only host document/source audit; source inspected with git show at the remotely advertised mcu-p3 commit. Server-provided container evidence separately reviewed; no local build or HIL run.'
verification_scope: 'Independent content and evidence audit of TWIN-18 deliverables and supplied server QA record.'
required_evidence_level: document
review_time: '2026-10-30 Asia/Shanghai'
process_audit: completed-with-evidence-gaps
result_check: failed
decision: REJECTED
accepted_scope: 'Verified remote fetchability, artifact SHA, selected MCU source facts, presence of requested protocol IDs, and explicit software/HIL distinction. The protocol reconciliation is internally inconsistent and cannot be accepted as a downstream contract.'
limitations:
  - 'This review does not approve firmware changes, builds, physical motion/probing, filament sensor operation, or HIL acceptance.'
  - 'The Codex runtime did not expose a Session UUID or exportable reviewer execution record. actual_session remains null; this report must not be treated as satisfying session-binding or non-author report-review gates until COORD records actual evidence.'
  - 'The server_lock lists refs/heads/<commit>, but those refs are not advertised by origin. Fetching each exact commit SHA from origin succeeded. The MCU source commit is not in server_lock; its exact branch/commit was independently checked.'
unexecuted:
  - 'No firmware build or automated content tests were run; task evidence level is document. The supplied runner ran only graph validation and artifact-presence checks.'
  - 'No physical HIL, serial traffic, motion, probe, filament-removal, or end-to-end AP acceptance was executed; these belong to the separately defined physical bench stage.'
not_applicable:
  - item: firmware coding-standard/build review
    reason: 'This task delivers a source survey, not firmware changes.'
  - item: physical HIL
    reason: 'The deliverable expressly separates HIL from software/source survey; no physical run is claimed or required for this document-level review.'
issues:
  - id: TWIN18-QA-01
    severity: blocker
    summary: 'Protocol matrix and detailed wire definitions conflict.'
    evidence: 'Specification §5 table row MOT-002 calls the 0x18 response payload 52 bytes and lists only grid_size_x, grid_size_y, z_offsets_um[25]. §6.2 defines 54 bytes and adds two plane coefficients. §5 row COL-007 describes the final four bytes as param=0, while §6.3 defines them as timestamp_tick_ms. §5 also presents 0x40 or 0x16 for MOT-001, while §6.1 only defines the 0x16 query. These choices change payload semantics/length or leave command selection ambiguous.'
    required_fix: 'Choose and consistently document one payload length/layout and field meaning for each command; resolve whether 0x40 is a separate telemetry push or remove it from the MOT-001 query mapping. Bind the resulting accepted contract revision before downstream implementation.'
  - id: TWIN18-QA-02
    severity: major
    summary: 'Candidate reference metadata does not match advertised server refs.'
    evidence: 'server_lock.json labels refs/heads/03dd0d1... and refs/heads/210ddd1..., but git ls-remote for both exact refs returned no rows. The exact SHA fetches succeeded, so commit objects were reachable, but the recorded refs are not verified refs. server_lock also omits the mcu-p3 source commit used by this survey.'
    required_fix: 'Record an actually advertised candidate ref or identify the candidate as a commit-addressed fetch without claiming a nonexistent branch; include the exact mcu-p3 source repository/ref/commit in the source lock.'
  - id: TWIN18-QA-03
    severity: major
    summary: 'Server runner success does not evidence substantive survey validation.'
    evidence: 'server_qa.json test_results contain only check_task_graph.py and test -f. The graph check reports canonical_task_count=0 and microtask_count=0 in that runner workspace. No source/content check was run there. Independent source review was therefore necessary; server_verdict PASSED is limited to those two checks.'
    required_fix: 'Scope the server verdict to its actual checks and bind the source versions consumed by the survey; do not describe the runner result as substantive content acceptance.'
  - id: TWIN18-QA-04
    severity: process-evidence
    summary: 'Reviewer session evidence is not available in the supplied or exposed run context.'
    evidence: 'Task card reviewer session is null, and this review runtime exposes no Session UUID/exportable execution record. The author codex_session.jsonl cannot establish this reviewer session.'
    required_fix: 'COORD must bind the actual independent reviewer session and available run evidence, then arrange non-author review of this report and record its SHA256.'
commands:
  - command: 'git -C project-control fetch origin 03dd0d1fef94545f844dbf70470958d783a6f2aa; git -C test_harness fetch origin 210ddd1c3f6f59594836c91b68aae55fb7a35181'
    cwd: /home/sushaohua/workspace/ai_soc_project
    tool_version: 'git (host version not recorded); server checkout log records git 2.25.1'
    time: '2026-10-30'
    exit_code: 0
    output: 'Exact commits fetched successfully from origin; detailed transcript: project-control/docs/evidence/twin/TWIN-18/runs/run_01/qa_audit.log; sha256=966391fd6e2af408e05cc76adbc312214e77a8ddc0a6533b7600a4b6366d2f7e'
  - command: 'git -C mcu-p3 ls-remote origin refs/heads/feat/soc-debug'
    cwd: /home/sushaohua/workspace/ai_soc_project
    tool_version: git
    time: '2026-10-30'
    exit_code: 0
    output: 'Remote advertised 1246ea9cb441d074ea444f53320f5632fefcd503; transcript in qa_audit.log above.'
  - command: 'sha256sum <survey> <result.md> <server QA evidence files>'
    cwd: /home/sushaohua/workspace/ai_soc_project
    tool_version: coreutils sha256sum
    time: '2026-10-30'
    exit_code: 0
    output: 'Survey matched requested SHA256; all computed values in qa_audit.log (SHA256 966391fd6e2af408e05cc76adbc312214e77a8ddc0a6533b7600a4b6366d2f7e).'
  - command: 'git -C mcu-p3 show 1246ea9cb441d074ea444f53320f5632fefcd503:<source path> | nl -ba | sed -n <reviewed range>'
    cwd: /home/sushaohua/workspace/ai_soc_project
    tool_version: git show / nl / sed
    time: '2026-10-30'
    exit_code: 0
    output: 'Read-only source excerpts and line numbers retained in qa_audit.log; SHA256 966391fd6e2af408e05cc76adbc312214e77a8ddc0a6533b7600a4b6366d2f7e.'
case_results:
  - case: remote commits and requested deliverable digest
    expected: 'Both locked commits fetch from origin; survey SHA256 equals caffb64413d745e513ef5947e8d7c29c0f5ac70fa24e0523ebe7bed565629e38.'
    observed: 'Both exact SHA fetches exit 0; survey digest matches. Advertised refs in server_lock do not exist.'
    verdict: 'passed with reference-metadata issue'
    evidence: qa_audit.log
  - case: container inspect and server verdict
    expected: 'Inspect evidence is present; runner verdict exit status is 0.'
    observed: 'server_qa.json contains full container ID, image digest sha256:43a2f1c6c95b1df70095eb744d5eadc9225867e0d7a2feda9b41ec3b6d38c825, exited state, and rw bind mount; server_verdict.json exit_code=0. Inspect object itself has no exit_status field.'
    verdict: passed
    evidence: 'server_qa.json sha256 56eb09a247794be9ed8f4c4b25922d7326e4e3a32bf6dee1060ecd694b6f4788; server_verdict.json sha256 b4749049302eb2ea0ce3f62aa75f6d89ce967efb8579eb60ed21c6593a3b0ab3'
  - case: MC AT32F435 coordinates and ABL grid
    expected: 'X/Y/Z/E source anchors and a 5x5 ABL grid match mcu-p3 source.'
    observed: 'NUM_AXIS=9, COREXY, grid points=5, bed bounds 20..220, bed_level writes in G29 loop, and adjust_delta source are present at pinned commit 1246ea9cb441d074ea444f53320f5632fefcd503.'
    verdict: passed
    evidence: 'qa_audit.log; survey §§2-3'
  - case: TH filament runout
    expected: 'GPIOD pin 2, 1s polling, 10-count debounce, filaout string match source.'
    observed: 'A_LIMIT_PIN=GPIO_PINS_2 and port GPIOD; timer period=1000000us, FILAMENT_LOW_SAMPLES=10U, Board_manage polls, Board_pauseFilament sends filaout.'
    verdict: passed
    evidence: 'qa_audit.log; survey §4'
  - case: protocol reconciliation matrix
    expected: 'MOT-001 0x16, MOT-002 0x18, COL-007 0x50 / HMS 0x3001 reconciled consistently.'
    observed: 'IDs and HMS code appear, but payload length/field conflicts and alternate 0x40 command remain unresolved.'
    verdict: failed
    evidence: 'survey §§5-6; TWIN18-QA-01'
  - case: software survey vs physical HIL acceptance
    expected: 'Software/source checks are explicitly separated from physical device acceptance.'
    observed: 'Survey §§1 and 8 define distinct isolated software and physical bench evidence; no HIL result is claimed by this review.'
    verdict: passed
    evidence: 'survey §§1, 8'
required_test_sets: []
executed_test_sets:
  - 'Read-only exact-commit source inspections and artifact SHA verification; see qa_audit.log.'
missing_test_sets:
  - 'No firmware build, automated source-content test, or HIL run; none is claimed as performed.'
raw_trace_files: []
supersedes_or_limits:
  - 'This report reviews only the listed TWIN-18 revision 1 artifacts and does not accept future firmware implementation or physical HIL.'
handoff:
  receiver_session: null
  evidence_location: project-control/docs/evidence/twin/TWIN-18/runs/run_01/
server_qa:
  path: project-control/docs/evidence/twin/TWIN-18/runs/run_01/server_qa/server_qa.json
  sha256: 56eb09a247794be9ed8f4c4b25922d7326e4e3a32bf6dee1060ecd694b6f4788
  server_verdict_path: project-control/docs/evidence/twin/TWIN-18/runs/run_01/server_qa/server_verdict.json
  server_verdict_sha256: b4749049302eb2ea0ce3f62aa75f6d89ce967efb8579eb60ed21c6593a3b0ab3
content_audit:
  fact_sources: {result: passed, basis: 'Checked source facts against mcu-p3 commit 1246ea9cb441d074ea444f53320f5632fefcd503; see qa_audit.log.'}
  protocol_compatibility: {result: failed, basis: 'Conflicting 0x18 payload size and 0x50 payload fields; ambiguous 0x40/0x16 mapping.'}
  claim_scope: {result: passed, basis: 'Software/source review is distinguished from physical HIL acceptance.'}
  architecture_completeness: {result: not-applicable, basis: 'This task is a source-interface survey; no runtime architecture implementation is under acceptance.'}
---

# TWIN-18 独立 QA 审查报告

## 1. 身份、候选与过程核查

| 检查项 | 实际结果 | 证据 |
| --- | --- | --- |
| 输入/范围 | 通过。审核 TWIN-18 revision 1；project-control、test_harness 候选完整 SHA 与交付规格 SHA 均已核对。 | `qa_audit.log`；服务器证据 `server_qa.json`、`server_lock.json` |
| 独立性 | 部分未满足。此审查由独立 Codex QA 回合执行，未使用作者改动作为源码基线；但运行环境未暴露可核验的 reviewer Session UUID，任务卡的 QA session 仍为空。 | 本报告元数据；任务卡 `TWIN-18.md` |
| 原子步骤 | 通过。依次核验提交/哈希、sandbox 证据、源码锚点、协议矩阵和 HIL 边界；未修改业务源码。 | `qa_audit.log` |
| 代码/构建 | 不适用。受审对象是文档调查，没有固件改动；本次没有运行固件构建。 | 任务类型为 design；无 build claim |
| 证据真实 | 部分通过。提交 SHA 可从服务器 fetch，交付哈希相符，容器 inspect 和 runner exit 0 记录存在；锁定 ref 元数据和 runner 内容覆盖范围有限。 | 本报告 issues TWIN18-QA-02/03 |

远端 `git fetch` 对 `03dd0d1fef94545f844dbf70470958d783a6f2aa` 与 `210ddd1c3f6f59594836c91b68aae55fb7a35181` 均返回 0；两者工作目录 HEAD 与目标 SHA 相同。规格文件 SHA256 为请求值 `caffb644…629e38`。`server_qa.json` 中容器 inspect 给出完整容器 ID、镜像 digest、`exited` 状态和 `/workspace` 的 rw bind mount；`server_verdict.json` 的 `exit_code` 为 0。inspect 对象本身未记录容器 `exit_status` 字段。

服务器锁定文件把两个 SHA 写成 `refs/heads/<sha>`，但对这两个精确 ref 的 `git ls-remote` 查询均无输出；按 SHA 从服务器 fetch 成功，故提交对象已验证可取，但 ref 声明不准确。源码调查依赖的 mcu-p3 `1246ea9cb441d074ea444f53320f5632fefcd503` 在服务器分支 `feat/soc-debug` 上可见；该 MCU 源码版本未列入 `server_lock.json`。

容器 runner 仅执行任务图检查和交付文件存在检查。任务图工具输出 `canonical_task_count=0`、`microtask_count=0`，这不验证调查内容。runner 的 0 退出码仅代表上述两个命令成功，不能作为技术内容审查通过依据。

## 2. 结果与正常/异常判据

### 通过项

- **MC 坐标和 ABL：** 在 mcu-p3 commit `1246ea9…` 中确认 `NUM_AXIS 9`、CoreXY、5 个网格点/维度、探测边界 20–220，以及 G29 将测量值写入 `bed_level` 并调用 QR 平面拟合；`adjust_delta` 从网格读取四邻点并执行插值。规格的 5×5/25 点、位置变量及网格接口缺失结论均有相应源码锚点。
- **TH 断料：** 确认 `A_LIMIT_PIN=GPIO_PINS_2`、`A_LIMIT_GPIO_PORT=GPIOD`；采样间隔 `1000000UL`，门限 `FILAMENT_LOW_SAMPLES=10U`，主循环 `Board_manage()` 到期采样，暂停路径调用 `send_quick("filaout\r\n")`。这支持用户指定的引脚、1 秒轮询、10 次计数和字符串事实。
- **HIL 边界：** 规格 §1、§8 将源码/软件孪生检查与真实 CoreXY、探针和断料台架分开描述。本报告未将软件检查或文档审查提升为物理通过。

### 阻断项

1. **TWIN18-QA-01：协议矩阵尚未对账一致。** §5 的 MOT-002 行定义 52 字节载荷，仅含 2 个网格维度字节和 25 个 `int16_t` 点；§6.2 定义 54 字节并添加两个平面系数。§5 的 COL-007 行把载荷末尾描述为 `param=0`，§6.3 则定义为 `timestamp_tick_ms`。MOT-001 矩阵还写 `0x40 或 0x16`，详细查询帧只定义 `0x16`。需要选定唯一布局/长度与字段语义，并明确 `0x40` 是否是独立遥测推送命令。
2. **TWIN18-QA-02：服务器 ref/source lock 不完整。** 两个 `refs/heads/<sha>` 未被服务器公布，虽然按 SHA fetch 成功；mcu-p3 作为主要事实来源也未绑定在 `server_lock.json`。修正记录后才能把服务器证据作为精确、可重复的源锁。
3. **TWIN18-QA-03：sandbox runner 未做内容审计。** 只有结构检查和文件存在性检查，没有执行源码事实或协议矩阵核验。其 `PASSED` 不能表述为本交付的实质技术验收。
4. **TWIN18-QA-04：审阅会话证据缺失。** 当前可用运行上下文未给出 reviewer UUID 或会话导出；不得用作者的 `codex_session.jsonl` 代替。COORD 仍需登记实际 reviewer 会话并安排非作者复核本报告。

未执行项：未构建固件、未运行 MCU 自动化内容测试、未接物理设备，也未进行串口协议闭环。本票是文档级调查；这些未执行项不构成 HIL 通过，也不改变上述协议文档拒绝结论。

## 3. 问题、限制与结论

**决定：REJECTED。** 源码事实的主要调查锚点、提交可取性、规格哈希和软件/HIL 边界通过；但协议矩阵与详细载荷定义存在直接冲突，不能作为一致的后续协议对账交付而批准。另有 ref 锁定和 reviewer 会话证据缺口，需由 COORD 补齐。此决定只针对列出的 TWIN-18 revision 1 文件，不表示固件或实机验收失败；物理 HIL 仍为独立阶段。

本报告 SHA256 应由收件者在写完后计算并记录；报告本身不嵌入自哈希。
