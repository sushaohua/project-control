# AUTO-05 Execution Record (run_01, Rework 03)

## 任务信息
- **任务编号**: `AUTO-05`
- **任务标题**: `AUTO-05 M1与M2综合端到端独立实景验收门禁（P1-01~13, P1-15~20）`
- **任务修订号**: `1` (`plan_revision: coord-intake-dispatch-phase1-20261103-rev2`)
- **运行编号**: `run_01`
- **执行角色与会话**: `QA` (QA Automation Engineer, `model`: `gpt-6-luna`, `session`: `05bae949-06e3-40fa-828c-ce9818b335e2`)
- **唯一接收 COORD 会话**: `8d4e8b77-42a9-4bd3-bd5a-1b881e8d4bd5`
- **前置候选基线 (`source_baseline.project-control`)**: `4c58c46be12af0e4dcfc4ef6f40dd162c5b18c06`（AUTO-03 与 AUTO-04 均已通过独立 Docker 沙箱与独立 Codex 审签 Done）
- **前置依赖 `AUTO-04` 验收证据**: `project-control/docs/evidence/coord_automation/AUTO-04/runs/run_02/qa_review_report.md` (Done)
- **授权与协议输入绑定**:
  - 人工批准记录：`project-control/docs/work_intake/approvals/APPR-20261103-001.yaml` (`SHA256: b7ea9ac9bdefc719fc46263c50e3a893d693ad63ae5166bc9085e4c71cc3f96d`)
  - 确认单 `rev 2`：`project-control/docs/planning/coord_intake_dispatch_phase1_confirmation_20261103.md` (`SHA256: 63c1225d60c377a662bebaa0328f9bc95c19daccaa61d9f2766bc989f06f3f98`)
  - 第一阶段设计 `rev 2`：`project-control/docs/architecture/coord_intake_dispatch_phase1_design_20261103.md` (`SHA256: 8a2984c6bb4b868cc8e2d6742873527f448f27c7006d99c5ce322207b2941350`)
- **阶段边界与硬门禁声明**:
  1. 严格针对前置锁定候选 `4c58c46be12af0e4dcfc4ef6f40dd162c5b18c06` 编写并执行独立端到端自动化验收套件，覆盖 Phase 1 M1 和 M2 全量 19 项条款（`P1-01~13` 及 `P1-15~20`）。
  2. 严格排除 `P1-14`（单实例 `systemd --user` 定时服务，属 M3 `AUTO-06`）。
  3. **受测业务实现代码物理只读**：严禁修改 `project-control/tools/coord_runner/**`，QA 绝不修改受测代码促通过。
  4. **业务仓库物理只读**：零触碰 `soc-ap/`、`mcu-p3/`、`test_harness/`、`boot/bootloadermc/`、`boot/bootloaderth/` 及物理硬件外设。
  5. **自研函数规范**：所有新增 Python 函数 100% 保持 $\le 50$ 行且参数 $\le 4$ 个。
  6. **工作区保护**：严禁 `git add -A` 或 `git clean`，保护已有未跟踪与修改文件。

---

## 交付工件与 SHA256 清单

| 交付文件路径 | SHA256 | 说明 |
| --- | --- | --- |
| `project-control/tools/test_phase1_intake_acceptance.py` | `6837765d38d7d78c5a38a40cb8bb080c9084a6fc4767ac1d2d093c67be535d39` | Phase 1 M1与M2综合端到端独立验收套件，全量覆盖 19 项条款深层断言与 AST 规约自检 |
| `project-control/docs/evidence/coord_automation/AUTO-05/runs/run_01/result.md` | 本文档 | AUTO-05 运行结果与客观物证审计记录（包含 ARCH 8 项缺陷返工闭环） |

---

## 独立 ARCH 审查（01a1a0b2 会话）8 项缺陷纠正与实证对照表

针对独立 Host Codex ARCH（`01a1a0b2-f27e-7072-b150-2c008217c3f6`）在 `arch_review_report.md` 中指出的 8 项实质性覆盖与断言不足，已在 `tools/test_phase1_intake_acceptance.py` 中逐项纠正补齐，断言范围严格与测试代码实证对齐：

| 缺陷项 | 条款 | ARCH 审查指出的不足 | Rework 1/2 补齐的实测断言 | 对应测试方法 |
| --- | --- | --- | --- | --- |
| 1 | `P1-09` | 仅写入伪造非法 PID 检查状态，未真实模拟崩溃/超时与对账五个源，未检验宿主 dispatch_key 查询 | 启动真实外部子进程并发送 `SIGKILL` 终止，在 mock `~/.codex/state_5.sqlite` 中插入匹配的 `[COORD_DISPATCH_KEY:...]` 记录，对账器检索 `/proc` 确认死亡、检索 SQLite threads 确认 `thread_id`，返回 `RECONCILE_REQUIRED`（派单待核实）；随后写入原子 `exit_status.json`，对账器确定性推进至 `COMPLETED` | `test_p1_09_timeout_and_crash_reconciliation_via_dispatch_key` |
| 2 | `P1-08` | 仅调用 `JobLauncher` 跑两个 sleep 进程，未检验外部角色/QA 调度器、就绪任务状态机推进及并发上限 2 | 基于 `CoordRunner.step()` 真实调度循环与异步外置子进程（`async_role_dispatch=True`），验证长耗时任务（`TASK-LONG` 0.6s）与快任务（`TASK-FAST` 0.05s）并发启动，第 3 张就绪卡 `TASK-THIRD` 被并发上限（2）拦截；FAST 完成后 THIRD 顺利派发，LONG 仍在途；LONG 完成后双任务闭环 | `test_p1_08_async_long_running_job_allows_second_task_advancement` |
| 3 | `P1-07` | 仅检查布尔值，未断言原版本绑定保留与防静默替换 | 注入任务 revision 1 为 InProgress 状态，对账器判定 revision 2 冲突返回 True；调用 `record_revision_conflict_referral` 记录审计线索，断言返回 `action: COORDINATOR_REFERRAL`, `active_revision: 1`, `incoming_revision: 2`；断言 sqlite 存储中 `referral:TASK-ACTIVE:rev2` 记录存在且新旧 revision 正确；任务持久化状态与原 revision 1 绑定完整保留 | `test_p1_07_higher_revision_in_flight_conflict_delegation` |
| 4 | `P1-11` | 仅检验空/零 commit，未检验“exit 0 缺交付物”与“QA 决议为 REJECTED”拦截写 Done | 补充 3 项硬门禁测试：(1) 角色返回 exit 0 但声明的 deliverable 不存在或为空，`_verify_implementation_outputs` 抛出 `GateValidationError: Exit 0 rejected: declared deliverable missing or empty`；(2) QA 评审决议为 `REJECTED` 时，`validate_done_acceptance` 坚决拦截写 Done 并抛出 `GateValidationError`；(3) QA 缺少必选非作者 `report_review` 时坚决拦截写 Done | `test_p1_11_exit_code_zero_without_evidence_or_qa_rejection_blocked` |
| 5 | `P1-12` | 仅检验 subagent 与同作者会话拦截，未检验未推远端候选与报告 SHA256 失配 | 补充 2 项硬门禁测试：(1) 候选 commit 未推送到远端服务器 origin 时，`_verify_remote_commit` 坚决抛出 `GateValidationError(P1-12)`；(2) QA 报告物理文件内容与 `report_sha256` 不匹配时，`validate_done_acceptance` 坚决抛出 `GateValidationError` 拦截伪造 Done | `test_p1_12_unpushed_candidate_and_fake_qa_subagent_rejected` |
| 6 | `P1-15` | 仅读取 summary 字段，未校验工件 SHA256 且未与锁定候选、服务器 QA 及独立审查记录绑定 | 强制无条件断言真实工件存在并核验具体 SHA256：(1) M1 drill summary (`cab642ada34ff4cd5484924059ccad011d2578dac8ebb6404f1b9c70f6376e97`)；(2) M1 manifest 真实物理文件 (`4866705b9b624387caace5315b1f5c031dec8ec77ce111a79b288b34f3acdf04`)；(3) M2 drill summary (`447f21ffacba271108c89bb2ad38905bde2f212664f49d48d69bfad4b4b87c22`)；(4) M2 QA 报告物理文件 (`d816d2c3e8c479eee317155c8acfebdb9bc515262eb93d2075812ed95400af8f`) 且包含候选提交 `4c58c46be12af0e4dcfc4ef6f40dd162c5b18c06`；(5) 验证 M2 演练 6 项核心能力标志位 | `test_p1_15_live_drill_end_to_end_verification` |
| 7 | `P1-20` | 仅检验调序不生成新文件，未检验实质变更触发升版与旧审批失效 | 补充实质变更升版测试：确认单内容发生实质修改后升至 revision 2，持旧版 revision 1 的 Approval 尝试释放需求执行时，`ApprovalGuard.require_implementation_approval` 坚决拦截并抛出 `ApprovalValidationError: STALE_CONFIRMATION_REVISION` | `test_p1_20_reordered_input_reuses_approvals_while_substantive_bump_requires_fresh` |
| 8 | `P1-16` | 仅检验 `enabled: false`，未真实删除文件并检验在途保护 | 补充真实物理删除测试：在 `scan2` 验证 `enabled: false` 触发 `IN_FLIGHT_PRESERVED_ON_INTAKE_DISABLED` 且任务保持 `InProgress` 后，执行 `Path(rec["_path"]).unlink()` 真实删除该 YAML 文件，`scan3` 证实已删除文件触发 `IN_FLIGHT_PRESERVED_ON_INTAKE_REMOVAL` 且在途卡依然坚决保持 `InProgress` | `test_p1_16_delete_or_disable_preserves_in_flight_and_blocks_shell_and_escape` |

---

## 综合端到端验收矩阵执行结果（19/19 条款全量覆盖）

| 编号 | 验收条款主题 | 验收场景与验证机制 | 对应测试用例 / 证据落点 | 结果 |
| --- | --- | --- | --- | --- |
| `P1-01` | 单 MD 批次三类指令输入与契约映射 | 单 MD 包含 issue/feature/requirement，逐条映射唯一主分类 YAML，保留公共约束 SHA256，需求 1:1 稳定映射，零人工手写 YAML | `test_p1_01_batch_markdown_generates_unique_yamls_and_preserves_contracts` | **PASSED** |
| `P1-02` | requirement 目标不清澄清拉起 | 需求不清（`clarify`）时自动路由 PM/ARCH 澄清方案，执行沙箱为 `read-only`，实现标记挂起，不阻塞其他就绪任务 | `test_p1_02_ambiguous_requirement_triggers_pm_arch_clarification` | **PASSED** |
| `P1-03` | feature 范围受控派发与未批拦截 | 仅释放已获批 feature 切片（`implementation_summary_approved=True`），未批子范围（`SUBSCOPE_UNAPPROVED`）硬性拦截开工 | `test_p1_03_approved_feature_scope_dispatches_while_unapproved_blocked` | **PASSED** |
| `P1-04` | issue 根因分流与直派 Owner | 根因未知先拉起 `read-only` 调查；根因明确直派特定 Owner（如 `ENG-FWD`），确保修改前留痕 | `test_p1_04_issue_root_cause_triage_routing_to_owner` | **PASSED** |
| `P1-05` | 同一记录重扫与重通知幂等 | 相同 `(id, rev, content_sha256)` 重扫返回既有记录，生成文件数为 0，权威 SQLite 存储摘要防重生效，零新增工程作业 | `test_p1_05_intake_rescan_and_renotify_idempotence` + M2 drill | **PASSED** |
| `P1-06` | 同版篡改与坏 Schema 隔离 | 同 `(id, rev)` 内容篡改报 `TAMPERED_SAME_REVISION`；错 `schema_version`（如 99）隔离报错，其余有效记录继续处理 | `test_p1_06_tampered_content_and_schema_version_isolated_from_valid_items` | **PASSED** |
| `P1-07` | 新 revision 遇到在途冲突移交 | 运行中任务遭遇新 revision 输入，对账器判定冲突并记录 audit referral 留痕（action: COORDINATOR_REFERRAL，保留新旧版本绑定），持久化保持原 revision 1 绑定转 COORD 裁决 | `test_p1_07_higher_revision_in_flight_conflict_delegation` | **PASSED** |
| `P1-08` | 长耗时外置异步与无冲突就绪票并发 | 基于真实 step() 调度循环与异步子进程推进，并发上限严格为 2（第 3 张卡拦截），FAST 完成后 THIRD 推进，LONG 仍在途，最终全闭环 | `test_p1_08_async_long_running_job_allows_second_task_advancement` + M2 drill | **PASSED** |
| `P1-09` | 派单超时/崩溃后凭 dispatch_key 五源对账 | 进程被 SIGKILL 终止且缺失退出状态时，对账器检索 `/proc` 与 SQLite threads，判定 `RECONCILE_REQUIRED`（“派单待核实”），严格禁止盲目重发；原子写入 `exit_status.json` 后推进至 `COMPLETED` | `test_p1_09_timeout_and_crash_reconciliation_via_dispatch_key` | **PASSED** |
| `P1-10` | flock 互斥锁与底层活跃租约保护 | `coord_runner.lock` 拦截第二实例双启动；纸面上租约超时但底层 `/proc` 进程存活时，对账器自动续期拦截资源抢占 | `test_p1_10_single_instance_flock_and_active_lease_protection` + M2 drill | **PASSED** |
| `P1-11` | exit 0 无候选/证据或 QA 拒绝拦截写 Done | (1) 退出码 0 缺失 40 位 commit 拒绝推进；(2) 退出码 0 缺失声明交付物坚决抛错拦截；(3) QA 决议为 `REJECTED` 坚决拦截写 Done；(4) QA 缺失非作者 `report_review` 坚决拦截写 Done；(5) 达返工上限触发升级 | `test_p1_11_exit_code_zero_without_evidence_or_qa_rejection_blocked` | **PASSED** |
| `P1-12` | 伪造 QA 子 Agent 与虚假 Session 拦截 | (1) `platform='subagent'` 冒充 Codex 硬拒；(2) 独立审阅人与实现作者 session 相同（自审自签）硬拒；(3) 候选 commit 未推送到远端服务器 origin 硬拒；(4) 报告物理 SHA256 失配硬拒 | `test_p1_12_unpushed_candidate_and_fake_qa_subagent_rejected` | **PASSED** |
| `P1-13` | 写前 SHA256 CAS 乐观锁防覆写 | 写入前比较文件 SHA256 摘要；遭遇外部/人工并发修改时抛出 `CasConflictError` 拒绝覆盖，完整保留用户现场 | `test_p1_13_cas_optimistic_concurrency_blocks_user_overwrite` | **PASSED** |
| `P1-15` | 真实小范围软件任务端到端演练闭环 | 获批微任务全流程实跑物证审计：强制无条件断言 M1/M2 演练 summary、manifest 及 M2 QA 报告物理存在并核验具体 SHA256，绑定候选 `4c58c46be12af0e4dcfc4ef6f40dd162c5b18c06`，业务仓库零触碰 | `test_p1_15_live_drill_end_to_end_verification` + AUTO-03/04 物证 | **PASSED** |
| `P1-16` | 删入口/改 disabled 保护在途与防注入 | 删入口（真实 `unlink()`）或改 disabled 不撤销在途任务；原文包含恶意 Shell 命令不直接执行；跨界越权路径访问（如 `soc-ap/core/**`）触发 `BoundaryViolationError` | `test_p1_16_delete_or_disable_preserves_in_flight_and_blocks_shell_and_escape` | **PASSED** |
| `P1-17` | 单指令多角色切片共享 demand_id | 单一稳定需求拆分 `ARCH`、`INTEGRATOR` 等多角色任务卡，保持唯一 `demand_id` 与确认单哈希血缘绑定，路径白名单互斥隔离 | `test_p1_17_single_demand_multi_role_split_preserves_demand_id` | **PASSED** |
| `P1-18` | 批次部分批准与“仅确认需求未批方案”分流 | 批次中仅部分需求获准时仅释放获准项；若 `demand_confirmed=True` 但 `implementation_summary_approved=False` 判定 `DEMAND_CONFIRMED_ONLY` 禁开工 | `test_p1_18_partial_batch_approval_and_demand_only_confirmation` | **PASSED** |
| `P1-19` | 审批防伪（非人类来源/过期/模型自填拦截） | 审批人非 `HUMAN` 拒收；确认单版本/哈希过期拒收；自然语言模糊字样或模型自填 `approved: true` 拒绝作为开工依据 | `test_p1_19_anti_forgery_rejects_bogus_actors_stale_rev_and_fuzzy_prose` | **PASSED** |
| `P1-20` | 原文重排复用有效批准与实质变更升版 | 原文指令调序保留指令摘要哈希，复用既有批准零重复生成；实质变更导致确认单升版后，旧审批文件被坚决拒绝作为有效凭据 | `test_p1_20_reordered_input_reuses_approvals_while_substantive_bump_requires_fresh` | **PASSED** |

---

## 宿主机真实物证核查（P1-15 闭环验证）

依据 `test_p1_15_live_drill_end_to_end_verification` 与现场物证审计：
1. **M1 单步受控演练物证 (`AUTO-03`)**:
   - `project-control/docs/evidence/coord_automation/AUTO-03/runs/run_01/live_drill/drill_summary.json`
   - 物理交付物文件：`project-control/docs/evidence/coord_automation/AUTO-03/runs/run_01/live_drill/deliverables/drill_intake_manifest.json`
   - 证明 `gpt-6-luna` 真实角色执行，产出物真实存在且磁盘 SHA256 精确等于 `4866705b9b624387caace5315b1f5c031dec8ec77ce111a79b288b34f3acdf04`，生命周期如实停驻在 `AWAITING_SERVER_CANDIDATE_AND_INDEPENDENT_QA`，未伪造自动写 `Done`。
2. **M2 持续推进与恢复物证 (`AUTO-04`)**:
   - `project-control/docs/evidence/coord_automation/AUTO-04/runs/run_01/live_drill/drill_summary.json`
   - 证明 SQLite 权威恢复源、`coord_runner.lock` 进程互斥 (`flock_mutual_exclusion_verified: true`)、双任务异步非阻塞推进 (`fast_done_while_long_active: true`, `step3_both_tasks_completed: true`)、Intake 重扫幂等与 CAS 乐观锁防覆写真实通过。
3. **前置服务器锁定候选 (`4c58c46be12af0e4dcfc4ef6f40dd162c5b18c06`)**:
   - 经 `git diff 4411a1d72643c8153587c1bc814f84b5ee04c74a 4c58c46be12af0e4dcfc4ef6f40dd162c5b18c06` 确认：代码修改严格受限在 `project-control/` 白名单内，**零触碰** `soc-ap/`、`mcu-p3/`、`test_harness/` 及双 Bootloader。
   - `qa-sandbox:20261029` 独立 Docker 容器内构建与测试通过（18 项 recovery 测试全绿）。
   - 宿主机与服务器审签记录：版本库永久固化记录了 AUTO-04 独立 QA 审查报告（`AUTO-04/runs/run_02/qa_review_report.md`，SHA256: `d816d2c3e8c479eee317155c8acfebdb9bc515262eb93d2075812ed95400af8f`，包含候选提交 `4c58c46be12af0e4dcfc4ef6f40dd162c5b18c06` 与 APPROVED 决议），由验收套件强制无条件断言存在与内容校验。

---

## 本地自检命令与测试运行实测

1. **`check_task_graph`**:
   - 命令：`PYTHONDONTWRITEBYTECODE=1 python3 project-control/tools/check_task_graph.py --workspace .`
   - 结果：`exit_code: 0`，`errors: []`，任务图零错误。
2. **`run_phase1_m1_m2_acceptance`**:
   - 命令：`PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tools -p 'test_phase1_intake_acceptance.py' -v`
   - 结果：`Ran 20 tests in 1.426s` — **OK (exit 0)**。
3. **既有单元测试全量回归**:
   - `test_coord_recovery.py`: `Ran 18 tests` — **OK (exit 0)**
   - `test_work_intake.py`: `Ran 15 tests` — **OK (exit 0)**
   - `test_qa_runner.py`: `Ran 22 tests` — **OK (exit 0)**
   - `test_delivery_checks.py`: `Ran 20 tests` — **OK (exit 0)**
4. **自研函数规范门禁 (AST Audit)**:
   - 针对新增工件 `project-control/tools/test_phase1_intake_acceptance.py` 执行 AST 扫描：
   - 结果：`Violations count: 0`（所有函数与方法行数 $\le 50$ 且参数 $\le 4$）。

---

## 结论

针对独立非作者 Host Codex ARCH 审查报告提出的意见及 run_02 审阅反馈，本轮返工（Rework 03）已在 `project-control/tools/test_phase1_intake_acceptance.py` 与本文档中 100% 纠正补实：
1. P1-07 完整断言 `COORDINATOR_REFERRAL` 及 SQLite audit referral 留痕（新旧 revision 绑定）；
2. P1-08 基于真实的 `step()` 循环与长耗时异步子进程推进，完整验证并发上限（2）拦截与就绪票释放；
3. P1-15 强制无条件断言真实演练工件（`m1_sum`, `m1_manifest`, `m2_sum`, `m2_rep_p`）物理存在与具体 SHA256，绑定候选 `4c58c46be12af0e4dcfc4ef6f40dd162c5b18c06`。

全量 19 项条款在锁定基线上客观实测 100% 通过，具备提请独立非作者 Codex ARCH 进行复核审签的完整前置条件。
