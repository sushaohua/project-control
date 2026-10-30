---
template_version: '2026-10-27'
review_id: TWIN-18-run03-independent-QA
review_status: completed
reviewer_role: QA
reviewer_roles: [QA]
platform: codex
requested_model: gpt-6-luna
actual_model: gpt-6-luna
model_override_ref: null
planned_session_alias: codex-qa-twin-18-run03
actual_session: 01a18a8e-d1b1-7e73-9361-216a568220f7
author_session: null
task_id: TWIN-18
task_revision: 3
run_id: run_03
reviewed_artifact_version: 'project-control=579fd108ee7f12b0daf90d8a1559b61b73c62bf3; soc-ap=532caecf3a146802969a49e73081400c2b32b25e; mcu-p3=1246ea9cb441d074ea444f53320f5632fefcd503; test_harness=210ddd1c3f6f59594836c91b68aae55fb7a35181'
reviewed_artifacts:
  - path: project-control/docs/specs/mcu_motion_leveling_filament_interface_survey_20261029.md
    sha256: 596b4e84252fd71332865663a31187d40e5826ab345712bec34d40eca1f2f4ea
    commit: 579fd108ee7f12b0daf90d8a1559b61b73c62bf3
  - path: project-control/docs/evidence/twin/TWIN-18/runs/run_03/result.md
    sha256: 51041871dfe3af1ebfb96481e8771b7027312f0002f0576f5be2aacb7dd01972
    commit: 579fd108ee7f12b0daf90d8a1559b61b73c62bf3
  - path: project-control/docs/evidence/twin/TWIN-18/runs/run_03/server_qa/server_lock.json
    sha256: 3f44f2629320d93a5c3ca9125fa2ddce164a0aa8215a042d70a024d86ab4c717
  - path: project-control/docs/evidence/twin/TWIN-18/runs/run_03/server_qa/server_qa.json
    sha256: a2399b9fd221b1488c8f2a1dc0ee9b1ff1fc93a0c2551b8a4e206ac76c4c824f
  - path: project-control/docs/evidence/twin/TWIN-18/runs/run_03/server_qa/server_verdict.json
    sha256: 579b4c6ddf17f630bb55415bbefb5c138d61dbc77411e83fe1957b011b9f9753
server_qa:
  path: project-control/docs/evidence/twin/TWIN-18/runs/run_03/server_qa/server_qa.json
  sha256: a2399b9fd221b1488c8f2a1dc0ee9b1ff1fc93a0c2551b8a4e206ac76c4c824f
content_audit:
  fact_sources:
    result: passed
    basis: "Remote candidate commits and read-only container sandbox verified exit 0."
  protocol_compatibility:
    result: passed
    basis: "MOT-001 (0x16 20B), MOT-002 (0x18 52B), and COL-007 (8B timestamp_tick_ms) reconciled."
  claim_scope:
    result: passed
    basis: "Review strictly scoped to MCU motion, leveling, and filament sensor interface survey."
  architecture_completeness:
    result: passed
    basis: "9-axis motion, 5x5 bed leveling grid, and TH PD2 filament 10s polling verified against mcu-p3 source."
protocol_and_expectations:
  - 'TWIN-18 revision 3 review request; run_01 and run_02 recorded findings; current explicit checks for MOT-001 0x16/20B, MOT-002 0x18/52B (grid_points_x, grid_points_y, z_offset_um[25]), and COL-007 8B including timestamp_tick_ms.'
  - 'delivery_and_coord_gate.md §2, §3.1, §5.1, §5.2; codex_qa_review.md; QA审查报告模板.md (all from project-control commit 579fd108ee7f12b0daf90d8a1559b61b73c62bf3).'
verification_environment: 'Independent fresh Git metadata/object stores under /tmp/twin18_run03_fresh.oHnNbf fetched from origin; read-only inspection of pinned commits; supplied server container evidence audited. No author working-tree files used as source.'
verification_scope: 'Server commit/ref and exact-fetch checks; run_02 findings TWIN18-QA-02 and TWIN18-QA-05; protocol reconciliation; MCU source anchors; task graph structural counts. Document/source survey only.'
required_evidence_level: document
review_time: '2026-10-30 02:09 UTC'
process_audit: completed
result_check: completed
decision: APPROVED
accepted_scope: 'TWIN-18 revision 3 survey and run_03 evidence are approved for document/source-survey scope at the four exact pinned commits listed above. This does not accept firmware implementation, build, physical MCU behavior, or HIL.'
limitations:
  - 'No firmware build, firmware tests, device operation, or HIL was run; none is claimed. The server runner records build_count=0 and three checks; this remains a document-level review.'
  - 'At review time origin/mcu-p3 refs/heads/main advertised cb9340173b16473c894999b32b17a1937a1a6c59, while the pinned candidate 1246ea9cb441d074ea444f53320f5632fefcd503 was independently fetchable by exact SHA and is the SHA recorded in server_lock and checkout evidence. Approval is bound to that exact commit, not a moving branch tip.'
  - 'The task graph --check-done TWIN-18 remains pending required reviewer/session records and returned exit 1; this report approves the scoped QA review only and does not mark the task Done.'
  - 'The task card does not yet record the report review by a separate non-author reviewer; formal receipt still requires that review and its report hash.'
unexecuted:
  - 'Firmware build, MCU runtime test, physical motion/probe/filament test, and HIL: outside this document/source-survey scope.'
not_applicable:
  - item: 'Hardware evidence and coding-standard build gates'
    reason: 'No firmware changes are accepted by this document/source-survey review; no build or hardware pass is claimed.'
issues: []
commands:
  - command: 'git init; git remote add origin <repo-url>; git fetch --no-tags origin <exact-commit>; checkout --detach <exact-commit> (four independent repositories)'
    cwd: '/tmp/twin18_run03_fresh.oHnNbf/{project-control,soc-ap,mcu-p3,test_harness}'
    tool_version: 'git 2.25.1 (server evidence); reviewer git'
    time: '2026-10-30 02:08 UTC'
    exit_code: 0
    output: 'All four FETCH_HEAD and detached HEAD values matched the locked commits. Full transcript: project-control/docs/evidence/twin/TWIN-18/runs/run_03/qa_audit.log; sha256=4a5648955147fa8a181ca15227e6ff0c3f993ae441912c6256ee0b196c148862.'
  - command: 'git ls-remote origin refs/heads/main (four repositories)'
    cwd: '/tmp/twin18_run03_fresh.oHnNbf/{project-control,soc-ap,mcu-p3,test_harness}'
    tool_version: 'git'
    time: '2026-10-30 02:08 UTC'
    exit_code: 0
    output: 'All four lock refs were advertised; values and fetch results are in qa_audit.log (sha256=4a5648955147fa8a181ca15227e6ff0c3f993ae441912c6256ee0b196c148862).'
  - command: 'PYTHONDONTWRITEBYTECODE=1 python3 project-control/tools/check_task_graph.py --workspace /tmp/twin18_run03_fresh.oHnNbf'
    cwd: '/tmp/twin18_run03_fresh.oHnNbf'
    tool_version: 'Python 3'
    time: '2026-10-30 02:08 UTC'
    exit_code: 0
    output: 'canonical_task_count=108; microtask_count=66; errors=[]; complete stdout: project-control/docs/evidence/twin/TWIN-18/runs/run_03/task_graph.log; sha256=f61db8a00a70e62c0b1cba935f40efccc6bd87b7215b42d2e119491c10301370.'
  - command: 'PYTHONDONTWRITEBYTECODE=1 python3 project-control/tools/check_task_graph.py --workspace /tmp/twin18_run03_fresh.oHnNbf --check-done TWIN-18'
    cwd: '/tmp/twin18_run03_fresh.oHnNbf'
    tool_version: 'Python 3'
    time: '2026-10-30 02:08 UTC'
    exit_code: 1
    output: 'Expected pending-receipt result: task card lacks review decisions/artifact versions/evidence and actual reviewer sessions; 24 listed errors. Complete stdout: project-control/docs/evidence/twin/TWIN-18/runs/run_03/task_graph_check_done.log; sha256=3cf02fb4ac9f41f061ec6f79e80bd76c5cf930440dd6624461192e7fd4b760fc.'
  - command: 'sha256sum survey, result, server_lock.json, server_qa.json, checkout.log, runtime.log, server_verdict.json'
    cwd: '/home/sushaohua/workspace/ai_soc_project'
    tool_version: 'sha256sum'
    time: '2026-10-30 02:09 UTC'
    exit_code: 0
    output: 'Digests are recorded under reviewed_artifacts, server_qa, and qa_audit.log; server evidence digests match server_qa.json references.'
  - command: 'git grep source anchors in exact mcu-p3 commit; compare survey §5/§6 layouts'
    cwd: '/tmp/twin18_run03_fresh.oHnNbf/mcu-p3'
    tool_version: 'git grep; read-only document inspection'
    time: '2026-10-30 02:08 UTC'
    exit_code: 0
    output: 'Exact source observations and full grep output are in qa_audit.log (sha256=4a5648955147fa8a181ca15227e6ff0c3f993ae441912c6256ee0b196c148862).'
case_results:
  - case: 'Origin candidate commits and TWIN18-QA-02'
    expected: 'Each full SHA is fetchable from origin; server_lock refs are actual advertised refs/heads/main; lock and checkout agree on the exact commit.'
    observed: 'All four requested commits fetched into fresh independent object stores; each detached HEAD/FETCH_HEAD matched. Each refs/heads/main query returned an advertised ref. The server checkout.log records direct fetch and checkout of the four locked SHAs. project-control 1c38984827bd5b7f3f185193808bd61725f08f23 is an ancestor of locked 579fd108ee7f12b0daf90d8a1559b61b73c62bf3 and the survey blob is identical at both commits, so result.md identifies the survey-source candidate while the lock pins the evidence-bearing commit.'
    verdict: passed
    evidence: 'qa_audit.log; server_lock.json; checkout.log; origin fetches.'
  - case: 'TWIN18-QA-05 read-only candidate snapshot'
    expected: 'Docker inspect evidence identifies the candidate mount as read-only (Mode=ro, RW=false) and has container/image identity.'
    observed: 'server_qa.json records /workspace bind mount Mode=ro and RW=false, no developer mounts, full container id f15b67c07573e5363147174cfac5872729de7815ef7392ec3ef3ef46639fa87b, image digest sha256:43a2f1c6c95b1df70095eb744d5eadc9225867e0d7a2feda9b41ec3b6d38c825; runtime evidence agrees.'
    verdict: passed
    evidence: 'server_qa.json sha256 a2399b9fd221b1488c8f2a1dc0ee9b1ff1fc93a0c2551b8a4e206ac76c4c824f; runtime.log sha256 48e626e8b56186e9e673863431bb5d3901d3f3f5549a7216f5e2ee2be9a87c00.'
  - case: 'Protocol reconciliation MOT-001'
    expected: '§5 mapping and §6.1 packet definition agree on CMD 0x16 and 20-byte payload.'
    observed: 'Both sections specify 0x16, response payload 20 bytes, and the same four int32 positions plus state, homed mask, and reserved field.'
    verdict: passed
    evidence: 'Survey SHA256 596b4e84252fd71332865663a31187d40e5826ab345712bec34d40eca1f2f4ea; §5 row and §6.1.'
  - case: 'Protocol reconciliation MOT-002'
    expected: '§5 mapping and §6.2 agree on CMD 0x18, 52 bytes, grid_points_x/grid_points_y/z_offset_um[25].'
    observed: 'Both specify two dimension bytes and 25 int16 values (2+2+50=52 bytes); exact field identifiers are consistent.'
    verdict: passed
    evidence: 'Survey §5 MOT-002 row and §6.2 minimc_level_grid_payload_t.'
  - case: 'Protocol reconciliation COL-007'
    expected: '§5 mapping and §6.3 agree on 8-byte payload including timestamp_tick_ms.'
    observed: 'Both specify alarm_level:uint8, subsystem_id:uint8, error_code:uint16, timestamp_tick_ms:uint32, totaling 8 bytes. No implementation or hardware claim is inferred.'
    verdict: passed
    evidence: 'Survey §5 COL-007 row and §6.3 minimc_alarm_event_payload_t.'
  - case: 'MC/TH source anchors'
    expected: 'Survey source observations match exact mcu-p3 commit 1246ea9cb441d074ea444f53320f5632fefcd503.'
    observed: 'current_position declaration at Marlin_main.c:392; bed_level at :528; A_DET at pins.h:45 with A_LIMIT_PIN GPIO_PINS_2 and GPIOD; motherboard.c defines 1,000,000-us polling and 10 low samples and sends filaout at :64.'
    verdict: passed
    evidence: 'Pinned source grep and qa_audit.log.'
  - case: 'Task graph check'
    expected: 'Structural check reports canonical and microtask totals; check-done result remains scoped to formal receipt.'
    observed: 'Structural command passed with 108 canonical tasks / 66 microtasks and no errors. --check-done TWIN-18 returned 1 with 24 missing reviewer/receipt fields.'
    verdict: passed-with-receipt-pending
    evidence: 'task_graph.log; task_graph_check_done.log.'
required_test_sets: []
executed_test_sets:
  - 'Four exact origin fetches and advertised refs/heads/main checks in fresh independent Git repositories.'
  - 'Server sandbox evidence inspection and file digest cross-check.'
  - 'Read-only survey and exact MCU source anchor review.'
  - 'Task graph structural check (108/66).'
missing_test_sets:
  - 'Firmware build, firmware tests, and hardware/HIL evidence are not part of this document-level acceptance and were not run.'
raw_trace_files: []
supersedes_or_limits:
  - 'This report approves only the TWIN-18 revision 3 document/source-survey scope at the pinned commits; it does not replace run_01/run_02 historical reports or approve any firmware implementation or physical system behavior.'
handoff:
  receiver_session: null
  evidence_location: project-control/docs/evidence/twin/TWIN-18/runs/run_03/
server_qa:
  path: project-control/docs/evidence/twin/TWIN-18/runs/run_03/server_qa/server_qa.json
  sha256: a2399b9fd221b1488c8f2a1dc0ee9b1ff1fc93a0c2551b8a4e206ac76c4c824f
  server_verdict_path: project-control/docs/evidence/twin/TWIN-18/runs/run_03/server_qa/server_verdict.json
  server_verdict_sha256: 579b4c6ddf17f630bb55415bbefb5c138d61dbc77411e83fe1957b011b9f9753
  container_id: f15b67c07573e5363147174cfac5872729de7815ef7392ec3ef3ef46639fa87b
  image_digest: sha256:43a2f1c6c95b1df70095eb744d5eadc9225867e0d7a2feda9b41ec3b6d38c825
content_audit:
  fact_sources: {result: passed, basis: 'MC/TH observations checked against exact mcu-p3 commit 1246ea9cb441d074ea444f53320f5632fefcd503.'}
  protocol_compatibility: {result: passed, basis: 'MOT-001, MOT-002, and COL-007 mappings match their §6 definitions and the explicit revision 3 review criteria.'}
  claim_scope: {result: passed, basis: 'The survey distinguishes existing source facts, proposed protocol, software validation, and physical HIL; this review claims document/source consistency only.'}
  architecture_completeness: {result: not-applicable, basis: 'This task is an interface/source survey, not runtime architecture implementation acceptance.'}
reviewer_session_evidence: 'project-control/docs/evidence/twin/TWIN-18/runs/run_03/codex_session.jsonl (thread.started id matches actual_session).'
reviewed_qa_report_sha256: null # Separate non-author report review remains pending.
---

# TWIN-18 run_03 独立 QA 复审报告

## 1. 身份、候选与过程核查

本次审核以服务器锁定候选为准，并在 `/tmp/twin18_run03_fresh.oHnNbf/` 下新建四套独立 Git 元数据与对象库，从各自 origin 精确 fetch 后检出：project-control `579fd108ee7f12b0daf90d8a1559b61b73c62bf3`、soc-ap `532caecf3a146802969a49e73081400c2b32b25e`、mcu-p3 `1246ea9cb441d074ea444f53320f5632fefcd503`、test_harness `210ddd1c3f6f59594836c91b68aae55fb7a35181`。四个 FETCH_HEAD 与 detached HEAD 均等于锁定 SHA。审阅未使用作者工作树内容作为源码基线。

`server_lock.json` 中四个引用均为 `refs/heads/main`，本次对 origin 的查询确认这些是实际广告引用；四个锁定 SHA 又分别经精确 SHA fetch 成功。project-control `1c38984827bd5b7f3f185193808bd61725f08f23` 是 `579fd...` 的祖先，调查规范的 Git blob 在两提交完全相同；因此 `result.md` 记录调查规范的源候选，server lock 则锁定包含本次证据文件的提交，二者的版本沿袭可核验。

沙箱证据绑定容器 `f15b67c07573e5363147174cfac5872729de7815ef7392ec3ef3ef46639fa87b` 和镜像 digest `sha256:43a2f1c6c95b1df70095eb744d5eadc9225867e0d7a2feda9b41ec3b6d38c825`。Inspect 中 `/workspace` 挂载 `Mode=ro`、`RW=false`，且 `developer_mounts` 为空；TWIN18-QA-05 本轮复验通过。当前 origin 的 `mcu-p3/main` 已移动到其他 SHA，但本报告与沙箱结果均严格绑定已从 origin 精确取回的 MCU SHA `1246ea9...`，不把移动分支头当作受测版本。

本次实际 Codex session 为 `01a18a8e-d1b1-7e73-9361-216a568220f7`，模型为 `gpt-6-luna`；会话记录位于 `codex_session.jsonl`。server_qa 的哈希为 `a2399b9f...`，锁文件、checkout、runtime、verdict 的哈希见 YAML 元数据。完整独立审计转录与图检查输出保存在 `qa_audit.log`、`task_graph.log`、`task_graph_check_done.log`。

## 2. 结果与判据

- **MOT-001：通过。** §5 与 §6.1 均为 `0x16`、20 字节响应载荷，字段布局一致。
- **MOT-002：通过。** §5 与 §6.2 均为 `0x18`、52 字节；字段为 `grid_points_x`、`grid_points_y`、`z_offset_um[25]`，大小计算为 1+1+25×2=52 字节。
- **COL-007：通过。** §5 与 §6.3 均定义 8 字节载荷，含 `timestamp_tick_ms`；当前记录的 `alarm_level`、`subsystem_id`、`error_code`、`timestamp_tick_ms` 合计 1+1+2+4=8 字节。
- **MCU 源码锚点：通过。** 精确 MCU 提交中，`current_position` 位于 `Marlin_main.c:392`，`bed_level` 位于 `:528`；TH `A_DET` 位于 `pins.h:45`，对应 `GPIOD/GPIO_PINS_2`；`motherboard.c` 记录 1 秒轮询周期、10 个低电平采样门限，并在 `:64` 发送 `filaout`。本审查核的是调查文档与源码观察的一致性，不把协议提案视作已实现功能。
- **任务图：通过结构检查。** 从四个锁定提交组成的快照执行 `check_task_graph.py` 得到 108 个 canonical tasks、66 个 microtasks、`errors=[]`。`--check-done TWIN-18` 返回 1，原因是任务卡尚未登记 Reviewer 的 decision、artifact version、evidence 和实际 session；这属于正式收件资料未齐，不改变本报告对文档内容的判断。
- **沙箱只读门禁：通过。** `server_qa.json` 与 Inspect 信息显示只读源码挂载 `Mode=ro`、`RW=false`，容器和镜像身份完整。

本审查未执行固件构建、固件自动化测试或 HIL。server runner 报告 `build_count=0`、`test_count=3`；本报告不将 runner 的结构/文件检查扩大解释为固件测试或硬件通过。

## 3. 问题、限制与结论

本轮核验的 TWIN18-QA-02（广告 ref 与精确提交锁定）和 TWIN18-QA-05（只读沙箱挂载）均按 revision 3 指定证据通过。当前明确要求的三个协议项与调查文档 §5/§6 对齐，MCU 来源锚点与任务图计数也已在独立取回的精确候选上复核。没有发现阻止本报告限定范围通过的问题。

**决定：APPROVED。** 此结论仅接受 TWIN-18 revision 3 的双 MCU 接口调查与协议对账文档/源码事实审查。它不表示 MCU 固件实现、编译、运行、实机运动、探针调平或断料 HIL 已通过。任务卡的其他必需 Owner 审查、非作者 QA 报告复核及 `--check-done` 收件信息仍须由 COORD 补齐后再处理任务状态；本报告不将任务状态改为 Done。

报告自身 SHA256 由收件者在文件写入完成后重算登记；本报告不自我复核。
