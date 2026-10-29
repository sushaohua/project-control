---
template_version: '2026-10-27'
review_id: AUTO-02-r1-run_02-QA
review_status: completed
reviewer_role: QA
reviewer_roles: [QA]
platform: codex
requested_model: gpt-6-luna
actual_model: gpt-6-luna
model_override_ref: null
planned_session_alias: planned-qa-auto-02
actual_session: null
author_session: 0e0e4b90-2aeb-42d4-abc2-13ed9198e8f0
task_id: AUTO-02
task_revision: 1
reviewed_artifact_version: project-control=eb3de6a6d370a5bd069c72bcdebfafd4c207a50e; test_harness=210ddd1c3f6f59594836c91b68aae55fb7a35181; run_02 record sha256=7f036835b1357cc8fa9bbeaa7a6ae51540d36d9ef98ff63e387aa1163e9a2dfd
reviewed_artifacts:
  - path: project-control/docs/evidence/coord_automation/AUTO-02/runs/run_02/result.md
    sha256: 7f036835b1357cc8fa9bbeaa7a6ae51540d36d9ef98ff63e387aa1163e9a2dfd
  - path: project-control/docs/evidence/coord_automation/AUTO-02/runs/run_02/server_qa.json
    sha256: 48a0c82dda98bdfc3f008861b9ca94b4832a4b712dd9e917b33a6f24d9e40946
  - path: project-control/tools/coord_runner/__init__.py
    sha256: c1806f909a8c9c891c17c9f9a2824851a7a70d289ab087502794bff5796de7fa
  - path: project-control/tools/coord_runner/models.py
    sha256: e2db6126d84ef12a007f83a89ddd472e5569e0ca7ba28b0f20a09d5f4a18ce78
  - path: project-control/tools/coord_runner/errors.py
    sha256: 1407cc0ddd7dc5a954dc024f2be1e2689274a0735bef37d8e8effd22ccef07e3
  - path: project-control/tools/coord_runner/lease_manager.py
    sha256: e65e24a97af415303c7193e6c0c1d0264aac7aa9e90c43f4e0a657676680a96d
  - path: project-control/tools/coord_runner/state_machine.py
    sha256: 93150cac90cd9254f37306552900e14b6480382dad3648c5d7317e36a50d3c91
  - path: project-control/tools/coord_runner/checkpoint.py
    sha256: 5e38f357b573570a27cd718e296b694c8cb6671bacd5a67a834ff796b5f56ed6
  - path: project-control/tools/coord_runner/scheduler.py
    sha256: c015900d4ee81e421da333aec2b0e49d0066158c9dffa3f1c23037083095e884
  - path: project-control/tools/coord_runner/runner.py
    sha256: 468fd313e899a3788360d2e3d4b5c4e9197e2a26ec900e21f1216798f2c34f05
  - path: project-control/tools/coord_runner/codex_adapter.py
    sha256: 5e571fbd94cc38486d3b7ba892adf425d7ed0f750384e0e793827e63f948d9a0
  - path: project-control/config/coord_runner/coord_config.yaml
    sha256: 75d43276a3da0fab4640b1f516045bea0d77142638be0d2f47a85a50c86a54f2
  - path: project-control/tools/coord_queue.py
    sha256: cb803af84686e7b98e9e3818b7050cfb99427e1d3b0482e3213f8d98919fe995
  - path: test_harness candidate commit
    commit: 210ddd1c3f6f59594836c91b68aae55fb7a35181
protocol_and_expectations:
  - source: project-control/.agents/rules/codex_qa_review.md and project-control/.agents/rules/delivery_and_coord_gate.md
    version: current rules in candidate checkout
    expectation: independent Codex session and isolated sandbox; server-pinned candidate; trusted server/job and report evidence
  - source: project-control/.agents/rules/c_cpp_coding_standard.md
    version: approved-baseline 1.0
    expectation: self-authored Python functions at most 50 source lines and at most 4 parameters
  - source: project-control/.agents/kanban/microtasks/coord_automation/AUTO-02.md
    version: revision 1
    expectation: real agent launch/wait, QA handoff, delivery gating, recovery and resource exclusivity
verification_environment: Reviewer process ran in workspace session; candidate files also inspected in run_02 fresh-checkout directory; Docker presence and reviewer-in-container binding not verified
verification_scope: locked commits and hashes; five prior findings; state/recovery/lease behavior; test records; Python function limits; server and Docker proof
required_evidence_level: server-sandbox-verified
review_time: 2026-10-29T08:33:38Z
process_audit: failed
result_check: failed
decision: REJECTED
accepted_scope: Exact run_02 source files were reviewed read-only; origin/main refs match both locked commits and listed source hashes. This report does not accept deployment, trusted server QA, isolated Codex execution or restart recovery as verified.
limitations:
  - Current review session ID is not available in the execution record; task-card reviewer session has no session_evidence and cannot be tied to this report.
  - Docker inspect from the reviewer environment returned No such object. This cannot disprove a transient container existed during the recorded run, but submitted logs do not independently establish its identity or configuration.
  - Reviewer command log is from the workspace session, not a Codex process shown to be running inside the QA container.
unexecuted:
  - Tests were not rerun by this reviewer inside a confirmed isolated container; runtime.log results were checked as submitted evidence only.
  - No actual process termination/restart recovery drill was observed.
  - No independent server-side job lookup or authenticated verdict query was available.
not_applicable:
  - item: HIL and firmware build
    reason: AUTO-02 is coordination infrastructure and has no firmware or HIL deliverable.
issues:
  - id: AUTO02-R2-01
    severity: P0
    status: open
    finding: QA verdict does not require or bind server_qa evidence. validate_qa_verdict accepts passed is True with no server_qa; if present it only checks sandbox.kind when the value is a truthy dict. The committed SandboxQA test uses passed=true without server_qa and can advance to Done.
    evidence: project-control/tools/coord_runner/state_machine.py lines 85-104; project-control/tools/test_coord_runner.py lines 292-293 and 334-345
  - id: AUTO02-R2-02
    severity: P0
    status: open
    finding: Server/container evidence is not independently established. server_qa.json declares kind=container, image=qa-sandbox:20261029 and container_id=32da38cfe4c6; runtime.log contains test command output only, and server_verdict.json is an unsigned summary without server job identity or authenticated query binding. Reviewer-side docker inspect found no such object. The evidence proves the claim files match their hashes, not a trusted job or actual container configuration.
    evidence: run_02 server_qa.json, runtime.log, server_verdict.json and qa_review_commands.log
  - id: AUTO02-R2-03
    severity: P1
    status: open
    finding: SandboxQA resumption branch exists, but crash/restart coverage is not demonstrated. The test injects an in-memory SandboxQA record and directly calls process_task; it does not checkpoint, terminate a process, restore a new process, or verify leases and waiting events.
    evidence: project-control/tools/coord_runner/runner.py lines 51-59 and 145-162; test_coord_runner.py lines 334-345
  - id: AUTO02-R2-04
    severity: P1
    status: open
    finding: Strict candidate-wide Python scan found one function over four parameters when *args and **kwargs are counted, namely done_acceptance_errors(task_id, card, cards, *args, **kw). Its signature predates this candidate and was not newly authored, so this is a standards-scope caveat; the execution record's unqualified all-functions claim is too broad.
    evidence: project-control/tools/check_task_graph.py line 304; signature predates AUTO-02; qa_review_commands.log
  - id: AUTO02-R2-05
    severity: P1
    status: open
    finding: Required independent-session and sandbox provenance is incomplete. The AUTO-02 QA assignment has session_evidence=null and this review has no externally verifiable session ID or runner-to-container binding. Policy requires the Codex reviewer itself to run inside the isolated environment.
    evidence: AUTO-02 card reviewer_sessions; delivery_and_coord_gate.md section 3; qa_review_commands.log
  - id: AUTO02-R2-06
    severity: P0
    status: open
    finding: The shipped runner has no concrete executor wiring. CoordRunner initializes all three executor callbacks to None, and the CLI constructs it without installing implementations. CodexReviewAdapter is never called outside tests. Therefore the CLI can fail closed, but cannot launch/wait for an agent, invoke QA, or request independent review as required by AUTO-02.
    evidence: project-control/tools/coord_runner/runner.py lines 47-49 and 232-252; project-control/tools/coord_runner/codex_adapter.py; qa_review_commands.log call-site search
commands:
  - command: git ls-remote for project-control and test_harness refs/heads/main
    cwd: /home/sushaohua/workspace/ai_soc_project
    tool_version: git version 2.25.1
    time: 2026-10-29T08:33Z
    exit_code: 0
    stdout_stderr: project-control/docs/evidence/coord_automation/AUTO-02/runs/run_02/qa_review_commands.log
    log_sha256: 4540ed3343e4f98a4bea9c3a0249793058ae1a126ff0913ed9c6b4c13edb70a1
  - command: docker inspect 32da38cfe4c6
    cwd: /home/sushaohua/workspace/ai_soc_project
    tool_version: Docker CLI; daemon returned no such object
    time: 2026-10-29T08:33Z
    exit_code: 1
    stdout_stderr: project-control/docs/evidence/coord_automation/AUTO-02/runs/run_02/qa_review_commands.log
    log_sha256: 4540ed3343e4f98a4bea9c3a0249793058ae1a126ff0913ed9c6b4c13edb70a1
  - command: AST scan of changed Python files; sha256sum run evidence and 11 deliverable files
    cwd: /home/sushaohua/workspace/ai_soc_project
    tool_version: Python 3.8.10 and git 2.25.1
    time: 2026-10-29T08:33Z
    exit_code: 0
    stdout_stderr: project-control/docs/evidence/coord_automation/AUTO-02/runs/run_02/qa_review_commands.log
    log_sha256: 4540ed3343e4f98a4bea9c3a0249793058ae1a126ff0913ed9c6b4c13edb70a1
  - command: rg call-site search for executor initialization and CodexReviewAdapter usage
    cwd: /home/sushaohua/workspace/ai_soc_project
    tool_version: ripgrep
    time: 2026-10-29T08:36Z
    exit_code: 0
    stdout_stderr: project-control/docs/evidence/coord_automation/AUTO-02/runs/run_02/qa_review_commands.log
    log_sha256: 4540ed3343e4f98a4bea9c3a0249793058ae1a126ff0913ed9c6b4c13edb70a1
case_results:
  - case: Missing executors
    independent_expectation: Missing agent_executor, qa_executor or review_executor must fail closed.
    observation: runner.py raises CoordRunnerError for each missing executor.
    result: pass
    evidence: runner.py source hash and test_missing_executor_fails_closed
  - case: Production executor wiring
    independent_expectation: Shipped runner/CLI must connect real agent launch, server QA and independent review executors.
    observation: All executor hooks default to None; CLI creates CoordRunner without installing any; CodexReviewAdapter has no production call site.
    result: fail
    evidence: runner.py lines 47-49 and 232-252; source call-site search
  - case: QA boolean and server evidence binding
    independent_expectation: Boolean true plus valid server_qa bound to task, revision, sandbox, candidate and server job is required.
    observation: Strict is-True check exists; server_qa is optional and no candidate/job binding is checked.
    result: fail
    evidence: state_machine.py lines 85-104; SandboxQA success test supplies no server_qa
  - case: SandboxQA restart
    independent_expectation: Fresh process restores checkpointed SandboxQA and advances safely.
    observation: process_task handles the state, but test supplies an in-memory record; no restart drill or evidence.
    result: incomplete
    evidence: runner.py recovery and process_task paths; test_coord_runner.py lines 334-345
  - case: UART lease rollback
    independent_expectation: UART conflict after implementation lease acquisition leaves no implementation lease.
    observation: Exception handler releases acquired leases; regression test asserts zero active implementation leases.
    result: pass
    evidence: runner.py lines 79-99; test_coord_runner.py lines 323-332
  - case: Docker sandbox proof
    independent_expectation: Runtime evidence confirms container kind, image digest/id, mounts and bound server job.
    observation: JSON declares kind/image/id and no developer mounts; logs do not attest the runtime settings or job; inspect unavailable in reviewer environment.
    result: fail
    evidence: server_qa.json, runtime.log, server_verdict.json and qa_review_commands.log
  - case: Required automated test sets
    independent_expectation: Four specified Python suites and full QA harness pass against locked commits.
    observation: All five are reported exit 0 in runtime.log and server_qa.json; reviewer did not reproduce inside a confirmed sandbox.
    result: reported-pass, unverified
    evidence: run_02 runtime.log and server_qa.json
  - case: Python function scale
    independent_expectation: New Python functions have at most 50 lines and 4 parameters.
    observation: 18 changed Python files and 249 functions scanned; none exceed 50 lines. One legacy variadic function is 5 parameters under strict counting.
    result: partial; execution-record claim needs scope qualification
    evidence: check_task_graph.py line 304 and qa_review_commands.log
required_test_sets:
  - project-control/tools/test_coord_runner.py (35 tests)
  - project-control/tools/test_qa_runner.py (20 tests)
  - project-control/tools/test_delivery_checks.py (20 tests)
  - project-control/tools/test_check_task_graph.py (12 tests)
  - test_harness/runner/qa_entrypoint.sh --suite all
executed_test_sets:
  - command: python3 tools/test_coord_runner.py
    result: exit 0; 35 tests reported by run_02 runtime.log; not independently rerun by reviewer
  - command: python3 tools/test_qa_runner.py
    result: exit 0; 20 tests reported by run_02 runtime.log; not independently rerun by reviewer
  - command: python3 tools/test_delivery_checks.py
    result: exit 0; 20 tests reported by run_02 runtime.log; not independently rerun by reviewer
  - command: python3 tools/test_check_task_graph.py
    result: exit 0; 12 tests reported by run_02 runtime.log; not independently rerun by reviewer
  - command: ./runner/qa_entrypoint.sh --suite all
    result: exit 0; cascade_vectors and hil_unit reported passed; not independently rerun by reviewer
missing_test_sets:
  - Independent execution of all named suites by reviewer Codex in a confirmed isolated container.
  - Actual process exit and restart recovery for checkpointed SandboxQA.
raw_trace_files: []
supersedes_or_limits:
  - Supersedes no prior decision; run_01 remains REJECTED for its exact candidate.
  - This report reviews only the run_02 commits; both origin/main refs matched at review time.
handoff:
  receiver_session: afd0a8cd-67b3-47cc-9cd2-a61f2973f496
  evidence_location: project-control/docs/evidence/coord_automation/AUTO-02/runs/run_02
server_qa:
  path: project-control/docs/evidence/coord_automation/AUTO-02/runs/run_02/server_qa.json
  sha256: 48a0c82dda98bdfc3f008861b9ca94b4832a4b712dd9e917b33a6f24d9e40946
content_audit:
  fact_sources:
    result: passed
    basis: Reviewer ls-remote returned both locked commits for origin/main; listed source hashes match local and fresh-checkout files.
  protocol_compatibility:
    result: not-applicable
    basis: AUTO-02 does not alter MCU/AP wire protocol fields.
  claim_scope:
    result: failed
    basis: Submitted materials claim server-bound QA, proven Docker execution and restart recovery, but do not establish a trusted job/container or actual process restart. Server evidence remains optional in code.
  architecture_completeness:
    result: failed
    basis: Fail-closed executors and lease rollback exist; server binding and isolated reviewer/restart evidence gates remain unproven.
reviewed_qa_report_sha256: null
---

# AUTO-02 独立 QA 审查报告（run_02）

## 1. 决定

**决定：REJECTED。** 候选 project-control=eb3de6a6d370a5bd069c72bcdebfafd4c207a50e、test_harness=210ddd1c3f6f59594836c91b68aae55fb7a35181 与 run_02 锁定对象一致；本次服务器 refs 查询也解析到这两个 commit。11 项交付文件摘要与提交清单相符。五项整改中，缺省执行器 fail-closed、严格布尔判断、SandboxQA 状态分支和租约回滚已落实；但 QA verdict 仍可在没有 server_qa 证据时通过，故此前第二项阻断问题没有完全关闭。Docker 和恢复验收证据不足，不能批准。

本报告只评价上述候选。任务卡仍为 InProgress；本报告不修改卡片状态，不接受部署或常驻服务能力。

## 2. 候选、范围与过程审计

| 检查项 | 结果 | 证据与说明 |
| --- | --- | --- |
| 输入与范围 | 通过 | AUTO-02 revision 1、run_02 执行记录、候选 commits、QA规则、交付门禁和编码标准已核对。 |
| 服务器候选 | 通过 | 实际 git ls-remote 返回 project-control eb3de6a6d370a5bd069c72bcdebfafd4c207a50e 和 test_harness 210ddd1c3f6f59594836c91b68aae55fb7a35181。沙箱仓库 .git/HEAD 也分别指向这两个完整 commit。 |
| 交付哈希 | 通过 | 用户列出的 11 项源文件哈希逐项匹配；run_02 result.md 和 server_qa.json 哈希也匹配。 |
| 独立 Codex 与沙箱过程 | 失败 | 本次执行事件没有可核验的 Codex session ID 或 runner-to-container 绑定；AUTO-02 卡片的 QA session_evidence 为空。QA 规则要求审阅 Codex 本身在隔离沙箱运行。 |
| Docker 运行环境 | 未证实 | proof 声明 kind=container、镜像 qa-sandbox:20261029、容器 32da38cfe4c6，但 runtime log 不含容器启动或 inspect 结果；server verdict 没有 job ID 或可信服务端查询依据。当前环境 docker inspect 返回 No such object。该结果不能否定一个已经结束的容器，但材料不足以确认其真实性和配置。 |
| 代码与恢复范围 | 失败 | server evidence 未绑定任务 revision、候选 commit、sandbox/job 和哈希；恢复测试没有演练进程退出和新进程恢复。 |

日志和摘要与本地对象内容一致，但这不构成可信 server job 身份认证。本次 refs、Docker 检查、哈希核对、AST 扫描和 executor 调用点搜索的命令输出保存在 qa_review_commands.log，SHA256 为 4540ed3343e4f98a4bea9c3a0249793058ae1a126ff0913ed9c6b4c13edb70a1。

## 3. run_01 阻断项复核

| run_01 问题 | run_02 观察 | 判定 |
| --- | --- | --- |
| 默认假执行器可能推进完成 | runner.py 对缺少 agent、QA 或 review executor 均抛出 CoordRunnerError；测试覆盖缺省执行器。 | 已修复 |
| QA verdict 类型和服务端证据绑定 | passed is True 严格检查已实现，字符串 false 不会通过。但 server_qa 可缺省；存在时仅检查 truthy dict 的 sandbox.kind，不检查证据摘要、任务/revision、job、sandbox ID 或候选 commit。成功测试的 verdict 不提供 server_qa 仍可进 DONE。 | **未修复，P0** |
| SandboxQA 崩溃恢复 | process_task 会处理恢复后仍为 SandboxQA 的任务。但测试直接造内存记录并调用 process_task，没有保存 checkpoint、终止原进程、恢复新进程或核对 lease/waiting event。 | 代码分支已修复；演练未证明 |
| UART lease 冲突回滚 | _acquire_task_leases 异常路径释放已获 lease；回归测试断言实现 lease 数为 0。 | 已修复 |
| Docker 沙箱证据 | proof 字段与用户给的 kind/image/container_id 相同；日志不独立证明对应容器实际创建、挂载和运行了命令，也没有可信服务端 job 绑定。 | 未证实，门禁失败 |

## 4. 测试结果与编码门禁

run_02 的 runtime.log 声称以下命令全部 exit 0：test_coord_runner.py（35 tests）、test_qa_runner.py（20）、test_delivery_checks.py（20）、test_check_task_graph.py（12），以及 qa_entrypoint.sh --suite all。它们与 server_qa.json 的 test_results 一致。本审查未在可确认的独立容器中重跑，记录为“提交记录通过，未独立复现”，不能替代沙箱过程门禁。

对任务基线到候选的 18 个 Python 文件做 AST 扫描，共 249 个函数。没有函数超过 50 行。严格将 *args、**kwargs 计为参数时，tools/check_task_graph.py:304 的历史函数 done_acceptance_errors(task_id, card, cards, *args, **kw) 有 5 个参数；签名早于 AUTO-02，候选扩展的是函数体。按历史代码最小修改原则，这里记录为范围偏差，不称为候选新增函数。执行记录笼统声称“所有 Python 函数”均不超过 4 参数，未说明口径，应改成新增函数范围或明确这个既有例外。

## 5. 发现与修复要求

1. **P0：强制并绑定 server_qa。** 缺少证据、错误类型/摘要、任务/revision、candidate commit、job ID、sandbox ID 或 server verdict 不匹配时必须 fail closed。passed 是布尔真不等于服务端已接受该候选。
2. **P0：补齐可信沙箱和服务端证明。** 提供独立检查者可验证的 job/container 记录，包含容器 ID、镜像 digest、挂载、隔离配置、命令和退出码，并绑定准确 commits。QA Codex session 需有证据表明审阅者本身在隔离环境运行。
3. **P1：进行真实重启恢复演练。** checkpoint SandboxQA 任务，终止原进程，启动新进程并恢复；核验任务推进、租约、游标、等待事件和失败路径，保留原始日志。
4. **P1：说明函数扫描范围。** 对新增函数给出可复现的 AST 口径；对遗留 variadic 函数明确豁免依据，不能泛化成所有 Python 函数无超限。
5. **P0：交付真实执行器接线。** 将 agent 启动/等待、AUTO-01 服务端 QA 与独立 reviewer 接入 runner/CLI，或明确提供受控的外部注入入口和实装；只留 None 默认值和 callback 测试桩不构成可执行调度器。

## 6. 结论范围

本报告拒绝 run_02 的准确候选。修复后的 executor fail-closed 和 lease rollback 不抵消 server evidence optional 的 P0 缺陷；测试绿色也不能代替独立 Codex 沙箱和服务端 job 证明。原作者修复后应生成新候选和新 run，重新独立审查。本报告不覆盖 AUTO-01、物理 HIL、部署常驻能力或任务卡正式状态。
