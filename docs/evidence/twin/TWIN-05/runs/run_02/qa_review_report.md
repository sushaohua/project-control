---
template_version: '2026-10-27'
review_id: TWIN-05-QA-run_02
review_status: completed
reviewer_role: QA
reviewer_roles: [QA]
platform: codex
requested_model: gpt-6-luna
actual_model: gpt-6-luna
model_override_ref: null
planned_session_alias: planned-qa-twin-05
actual_session: 01a18b79-11fa-7441-8792-21ae24c4e74b
author_session: 3fbe2d65-b1c3-4c69-8a2d-084bcc76a4c3
task_id: TWIN-05
task_revision: 2
reviewed_artifact_version:
  requested_candidates:
    soc-ap: 16ba69d29c93191731a13a1fa4c88f981677c4d5
    test_harness: 0b7497ba43158841eb3c4af7f16e477b9c30c2c5
    project-control: e549c9e3c45b34db11e74edfa8cb264cbd5508df
    mcu-p3: 1246ea9cb441d074ea444f53320f5632fefcd503
  server_qa_locked_candidates:
    soc-ap: 16ba69d29c93191731a13a1fa4c88f981677c4d5
    test_harness: 0b7497ba43158841eb3c4af7f16e477b9c30c2c5
    project-control: 7a3e344918a5682fe66dedff4914555edeaf93d7
    mcu-p3: 1246ea9cb441d074ea444f53320f5632fefcd503
reviewed_artifacts:
  - {path: soc-ap/config/dds/twin/DEFAULT_FASTRTPS_PROFILES.xml, sha256: 566a4893171c89fd976ce73dc61895215875d64c8d9d4f5b780caf6d11fe742d}
  - {path: soc-ap/middleware/dds/include/aisoc_dds.h, sha256: 3ca44e38eabb3ac69c2546d5fb517e51f733819405f97509f1b39c0f193c6ce0}
  - {path: soc-ap/middleware/dds/src/aisoc_dds.cpp, sha256: cc34be1ee06784ea38d5606dcae27ed38cc63382f5fdbf0be0ff071610ac3011}
  - {path: soc-ap/middleware/dds/src/aisoc_dds_common.cpp, sha256: 5c10e45eac063d82c5a1415a7787f83e0468e5f06d9815aa494d8eba282d3030}
  - {path: soc-ap/middleware/dds/src/aisoc_dds_internal.hpp, sha256: 029c977887de32e90a1e6c2e15e20aed2df85383af5bd09a18311a8883271233}
  - {path: soc-ap/middleware/dds/src/aisoc_dds_participant.cpp, sha256: 01137d727324188d3c4327b82dad51c227a67e5dfaa8e4fc3bd7b8a5c33a6a99}
  - {path: soc-ap/middleware/dds/src/aisoc_dds_pub.cpp, sha256: 689a9b62752bccf724ca7508bcffd5607242e736196e02ab62393667f888cefb}
  - {path: soc-ap/middleware/dds/src/aisoc_dds_sub.cpp, sha256: 19e72cdbd121f1ff4f9e5a90c1d9b8c5994a02c5706e55e48e0abbfa63ebd684}
  - {path: soc-ap/middleware/dds/src/aisoc_dds_types.cpp, sha256: 5d025812b81eb015b00366b69b8485ba9407f402cf393665590a11dbbaa00213}
  - {path: soc-ap/middleware/dds/src/aisoc_dds_types.hpp, sha256: d2d6dd8e7aafd067c0bdabced6101035002509c727b234f21358e357e5725ed3}
  - {path: soc-ap/middleware/dds/CMakeLists.txt, sha256: a5921ad4024328a1d0f0985670ae9fb979652049f15ac46ad777ea6f85c8cf18}
  - {path: soc-ap/middleware/dds/README.md, sha256: 0840c17dcf17c0184898c605d0c5409126cd7bf76fa03c70dc13c5c8c1786e51}
  - {path: soc-ap/middleware/dds/examples/CMakeLists.txt, sha256: c8d70445e4688a238319626f317a9e1fe14b618cd6e8cfa397eb1595e6c18fb8}
  - {path: soc-ap/middleware/dds/examples/publisher_example.cpp, sha256: 34b035b61ba1de90150ab3c19f382c5c31d62600886e03725e349c7a1dcbf4b6}
  - {path: soc-ap/middleware/dds/examples/subscriber_example.cpp, sha256: 47d230b9e7ad967c46c6601cfb2d34006606314b2b275c51e22662e6afd90c80}
  - {path: soc-ap/tests/dds/twin/CMakeLists.txt, sha256: 1dff2c0658c49f180a2deb0c6ac57271ce92c9e1eae123249bac3e60de54c775}
  - {path: soc-ap/tests/dds/twin/test_dds_pubsub.cpp, sha256: 86fa9c929e9802e8ec934fc1563a35cacf9829564af20827209b819079b5c7b2}
  - {path: soc-ap/third_party/dds/README.md, sha256: 3f523e14bfd21b00135cbaf0c0d841c87f1e37df0f7ad3e85f1b5acebf4cc525}
protocol_and_expectations:
  - {source: project-control/.agents/rules/delivery_and_coord_gate.md, revision: 1}
  - {source: project-control/.agents/rules/codex_qa_review.md, revision: current at review}
  - {source: project-control/.agents/rules/c_cpp_coding_standard.md, version: 1.0}
  - {source: project-control/.agents/rules/templates/QA审查报告模板.md, template_version: '2026-10-27'}
  - {source: project-control/.agents/kanban/microtasks/vmware_soc_twin/TWIN-05.md, revision: 2}
verification_environment:
  reviewer: host Codex session 01a18b79-11fa-7441-8792-21ae24c4e74b; read-only source/evidence inspection; no reviewer-side build/test run
  server_sandbox: {kind: Docker, id: TWIN-05_run_141932_20261030_061932, container_id: 866090ef344c47bf7ce35e54a7ec6c94b3c399ab6b52cbbb34a2abbc8b7a084d, image_digest: 'sha256:acbab225932c3877fff37f4d9e5a21235e099182c198e4f4034064ea80cf544f', mounts: 'fresh server checkout mounted read-only; developer_mounts empty'}
verification_scope: TWIN-05 revision 2 DDS SDK, server evidence, supplied deliverable hashes, bounded QoS and public API checks
required_evidence_level: server-sandbox-verified
review_time: '2026-10-30 Asia/Shanghai'
process_audit: completed-with-blockers
result_check: partial; all recorded test groups pass on sandbox lock, but project-control requested candidate is not the locked commit and strict quota guarantees are not established
decision: REJECTED
accepted_scope: null
limitations:
  - Sandbox evidence supports Linux container build and cross-process software IPC only; no SoC board, MCU HIL, restart/recovery cycle, or CPU/memory measurements are evidenced.
  - The task card still has null reviewer_sessions entries; this report records this actual reviewer session and the author session binding, but does not update formal task state.
  - The server test command compiles and runs the suite in one invocation; reviewer did not rerun it.
unexecuted:
  - Reviewer-side build and test execution; recorded server sandbox output was independently inspected instead.
  - Strict participant and subscriber quota overflow/recovery tests and concurrent quota stress tests.
  - TWIN-05 restart/recovery test and CPU/memory measurements required by the task acceptance text.
not_applicable:
  - {item: physical MCU/SoC HIL, reason: TWIN-05 run_02 evidence is a software container run; no physical pass is claimed}
issues:
  - id: TWIN05-QA-01
    severity: blocker
    finding: The requested candidate tuple is not the tuple tested by the run_02 server sandbox. The requested project-control commit e549c9e3c45b34db11e74edfa8cb264cbd5508df is fetchable from origin/main, but server_lock.json and checkout.log pin/fetch project-control 7a3e344918a5682fe66dedff4914555edeaf93d7. The other three requested commits match the lock and were confirmed fetchable from their listed remotes. The run therefore cannot be attributed to the complete requested candidate tuple.
    evidence: project-control/docs/evidence/twin/TWIN-05/runs/run_02/server_qa/server_lock.json (sha256 ff28e53f55a4042a7c153b0c89b183bacbfb6864ffa92e5b4015653fbaf5c56f); checkout.log (sha256 4cfdc35566e520b2965945017cd6541cdd4fd8b3f8deb903241a48b3ccebe47c); remote ls-remote showed project-control main=e549c9e3c45b34db11e74edfa8cb264cbd5508df.
    required_action: Regenerate and publish the candidate lock for the requested four commits, then rerun the server sandbox against that exact lock; preserve the existing run_02 evidence.
  - id: TWIN05-QA-03
    severity: blocker
    finding: The three quota macros and AISOC_DDS_ERR_RESOURCE_LIMIT exist, and test_quota_limits verifies the publisher count reaches 16, rejects the 17th, then accepts a replacement after destroy. However, each create path performs atomic count.load() followed later by entity creation and fetch_add(); the check and reservation are not atomic, so concurrent creators can all pass the bound and exceed the configured maximum. The test does not exercise participant or subscriber overflow/recovery boundaries. Thus the requested strict limits are not established.
    evidence: soc-ap/middleware/dds/src/aisoc_dds_participant.cpp:80-116; soc-ap/middleware/dds/src/aisoc_dds_pub.cpp:41-71; soc-ap/middleware/dds/src/aisoc_dds_sub.cpp:41-72; soc-ap/tests/dds/twin/test_dds_pubsub.cpp:67-100.
    required_action: Implement an atomic bounded reservation/release for each entity class, with rollback on creation failure; add boundary and recovery tests for participants, publishers, and subscribers, plus a concurrency test that proves the cap cannot be exceeded.
  - id: TWIN-05-ACC-01
    severity: major
    finding: Required task evidence is incomplete: the acceptance text asks for restart/recovery reproduction and locked CPU/memory measurements, but the recorded test suite covers guard clauses, one publisher quota boundary, E2E, transient-local late joiner, KEEP_LAST depth, and fork/exec IPC only. No restart/recovery test or CPU/memory values are recorded.
    evidence: project-control/.agents/kanban/microtasks/vmware_soc_twin/TWIN-05.md positive_cases and required_evidence_level; run_02/server_qa/runtime.log and server_qa.json.
    required_action: Add/re-run the task acceptance cases and record measured values, or obtain a formally accepted scope revision that explicitly removes them before acceptance.
  - id: TWIN05-QA-02
    severity: passed
    finding: The author session UUID 3fbe2d65-b1c3-4c69-8a2d-084bcc76a4c3 is identified in the task executor record and run_02 result.md; this review ran in actual Codex session 01a18b79-11fa-7441-8792-21ae24c4e74b, a distinct session. The task card reviewer assignment fields remain unfilled; this report records the independent reviewer identity for this run.
    evidence: project-control/.agents/kanban/microtasks/vmware_soc_twin/TWIN-05.md executor.agent_id; project-control/docs/evidence/twin/TWIN-05/runs/run_02/result.md; run_02/codex_session.jsonl.
commands:
  - {command: 'sha256sum over all 18 supplied deliverables', cwd: workspace root, exit_code: 0, purpose: supplied artifact digest verification; 18/18 matched}
  - {command: 'git ls-remote origin refs/heads/main (soc-ap, test_harness, project-control) and refs/heads/feat/soc-debug (mcu-p3)', cwd: each repository, exit_code: 0, purpose: remote candidate reachability; project-control lock mismatch remains}
  - {command: 'inspect server_qa.json, server_lock.json, checkout.log, runtime.log and server_verdict.json; recompute evidence SHA-256', cwd: workspace root, exit_code: 0, purpose: evidence integrity and recorded result audit}
  - {command: 'inline source scan for C++ function body lengths and parameter counts in DDS sources, examples, and test file', cwd: workspace root, exit_code: 0, purpose: function gate scan; max body 39 nonblank code lines; no detected >50-line or >4-parameter functions}
case_results:
  - {case: GuardClause, expected: public API rejects null required pointers, observed: recorded test group reports 100% PASS, verdict: recorded pass on sandbox-locked soc-ap commit}
  - {case: QuotaLimits, expected: strict bounded participant/publisher/subscriber creation, observed: publisher-only single-thread boundary/recovery passes; other classes and concurrent creation untested, verdict: partial; finding TWIN05-QA-03 remains open}
  - {case: E2E, expected: raw telemetry and temperature snapshot delivery, observed: both recorded groups report 100% PASS, verdict: recorded pass on sandbox-locked soc-ap commit}
  - {case: TransientLocal, expected: late subscriber retrieves gen=42 snapshot, observed: recorded pass, verdict: recorded pass on sandbox-locked soc-ap commit}
  - {case: KeepLastDepth, expected: KEEP_LAST(5) retains newest five of ten, observed: received sequences 6..10, verdict: recorded pass on sandbox-locked soc-ap commit}
  - {case: CrossProcessIPC, expected: separate fork+exec child exchanges sample and exits zero, observed: recorded pass, child exit=0, verdict: recorded pass on sandbox-locked soc-ap commit}
required_test_sets: [GuardClause, QuotaLimits, E2E, TransientLocal, KeepLastDepth, CrossProcessIPC]
executed_test_sets: [GuardClause, QuotaLimits, E2E, TransientLocal, KeepLastDepth, CrossProcessIPC]
missing_test_sets: [ParticipantQuotaBoundary, SubscriberQuotaBoundary, ConcurrentQuotaLimit, RestartRecovery, CpuMemoryMeasurements]
raw_trace_files: []
supersedes_or_limits:
  - Run 01 findings TWIN05-QA-01 and TWIN05-QA-03 are not fully resolved for this review: candidate mismatch remains for project-control and strict quota behavior is not established.
handoff:
  receiver_session: COORD
  evidence_location: project-control/docs/evidence/twin/TWIN-05/runs/run_02/qa_review_report.md
server_qa:
  path: project-control/docs/evidence/twin/TWIN-05/runs/run_02/server_qa/server_qa.json
  sha256: 7b0fc1314d98986f9bd09fb1bb2791f0d736491ecb9f3c7b4468ab19bfe3faa8
content_audit:
  fact_sources: {result: passed, basis: candidate refs, task card, sandbox lock, checkout/runtime logs and supplied artifacts were cross-checked; tuple mismatch is recorded as a blocker}
  protocol_compatibility: {result: passed, basis: DDS type/API sources and XML QoS profiles inspected; no wire schema change found within reviewed artifact set}
  claim_scope: {result: passed, basis: server evidence is reported only as container build/test/IPC; no hardware, restart, or resource measurement pass is claimed}
  architecture_completeness: {result: not-applicable, basis: task asks for a DDS SDK slice; this report checks task-specific deliverables and records missing restart/resource cases, not the system-wide module inventory}
reviewed_qa_report_sha256: null
---

# TWIN-05 独立 QA 复审（run_02）

## 结论

**REJECTED**。本报告审阅 revision 2，拒绝对用户请求的候选组合签发 APPROVED。候选仓库、交付文件和沙箱结果已核对；server 记录的 6 组测试均通过，但完整候选组合与锁定候选不一致，且实体数量上限在并发创建下没有严格保证。

## 前次问题复核

| 发现 | 结果 | 证据与判断 |
| --- | --- | --- |
| TWIN05-QA-01 候选绑定/可取回 | 部分通过 | soc-ap、test_harness、mcu-p3 与请求候选匹配并可从 origin 查询；project-control 请求值为 `e549c9e…`，run_02 锁定并 fetch 的是 `7a3e344…`。 |
| TWIN05-QA-02 作者会话绑定/独立 | 通过 | 作者 `3fbe2d65-b1c3-4c69-8a2d-084bcc76a4c3` 与本 Reviewer 会话 `01a18b79-11fa-7441-8792-21ae24c4e74b` 不同。 |
| TWIN05-QA-03 SDK 实体上限 | 未通过 | 宏和错误码存在，publisher 单线程边界/销毁恢复测试通过；participant/subscriber 上限未测，且 `load()` 后创建、再 `fetch_add()` 的分离步骤允许竞争越限。 |

## 源码、哈希及服务器证据

18 项交付文件均与用户提供的 SHA-256 一致。三个被请求的候选仓库提交和 mcu-p3 提交在远端 ref 可定位；project-control 的请求候选可达，但与 run_02 `server_lock.json` 不同。server QA 元数据 SHA-256 为 `7b0fc1314d98986f9bd09fb1bb2791f0d736491ecb9f3c7b4468ab19bfe3faa8`。其容器为 `866090ef344c47bf7ce35e54a7ec6c94b3c399ab6b52cbbb34a2abbc8b7a084d`，镜像 digest 为 `sha256:acbab225932c3877fff37f4d9e5a21235e099182c198e4f4034064ea80cf544f`，开发者挂载为空，源码 checkout 只读。

运行记录中的编译命令退出码为 0；GuardClause、QuotaLimits、E2E、TransientLocal、KeepLastDepth、CrossProcessIPC 六组均报告 PASS。它们只能归属于 lock 中实际检出的源码组合。此次 Reviewer 未在宿主机重跑测试。

代码审阅确认配额宏为 Participant=4、Publisher=16、Subscriber=16，错误码为 `AISOC_DDS_ERR_RESOURCE_LIMIT`。创建入口在 `load()` 与实体创建成功后的 `fetch_add()` 之间没有原子预留操作，因此多个并发创建请求可同时通过上限检查。现有 `test_quota_limits` 只测 Publisher 边界与释放后再创建。

## 编码规范与范围

对所列新增 DDS C++ 源码、示例和测试执行函数定义扫描，最大函数体为 39 行，未检出超过 50 行或超过 4 个参数的函数；公开 SDK 指针入口具有空指针防御。该静态审阅不替代沙箱构建证据。任务验收还要求 restart/recovery 与 CPU/memory 实测锁定，本次 server 记录没有提供这些结果。无真实 SoC/MCU HIL 证据，本结论不作相关通过声明。

## 整改后复审要求

1. 用完全匹配的四仓候选重新生成 server lock 并复跑独立容器验收。
2. 对各类实体使用原子有界 reserve/release，并在构建失败时回滚预留；补齐 Participant、Publisher、Subscriber 的上限和销毁恢复测试及并发越限测试。
3. 补充任务卡要求的 restart/recovery 与 CPU/memory 记录，或先完成正式范围修订，再按修订后的判据验收。

本决定只针对 TWIN-05 revision 2 的本次 run_02 请求候选，不自动改变任务卡状态或其余仓库验收结论。
