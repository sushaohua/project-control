# AUTO-05 Execution Record (run_01)

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
| `project-control/tools/test_phase1_intake_acceptance.py` | `7b1510a43897d59a7da9739b621aa86143770b587673d99ac69fca3fd7e5b36a` | Phase 1 M1与M2综合端到端独立验收套件，覆盖全部 19 项条款正反例与 AST 自检 |
| `project-control/docs/evidence/coord_automation/AUTO-05/runs/run_01/result.md` | 本文档 | AUTO-05 运行结果与客观物证审计记录 |

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
| `P1-07` | 新 revision 遇到在途冲突移交 | 运行中任务遭遇新 revision 输入，对账器确定性判定 `IN_FLIGHT_REVISION_CONFLICT`，不静默换候选或盲目重派，留存转 COORD 裁决 | `test_p1_07_higher_revision_in_flight_conflict_delegation` | **PASSED** |
| `P1-08` | 长耗时外置异步与无冲突就绪票并发 | 长耗时角色任务通过 `JobLauncher` 外置异步推进，另一无冲突就绪任务并发拉起并优先完成，双任务皆具真实独立 PID/starttime | `test_p1_08_async_long_running_job_allows_second_task_advancement` + M2 drill | **PASSED** |
| `P1-09` | 派单超时/崩溃后凭 dispatch_key 五源对账 | 进程被 kill/异常终止且缺失退出状态时，对账器判定 `RECONCILE_REQUIRED`（“派单待核实”），严格禁止盲目重发 | `test_p1_09_timeout_and_crash_reconciliation_via_dispatch_key` | **PASSED** |
| `P1-10` | flock 互斥锁与底层活跃租约保护 | `coord_runner.lock` 拦截第二实例双启动；纸面上租约超时但底层 `/proc` 进程存活时，对账器自动续期拦截资源抢占 | `test_p1_10_single_instance_flock_and_active_lease_protection` + M2 drill | **PASSED** |
| `P1-11` | exit 0 无候选/证据或 QA 拒绝拦截写 Done | 退出码 0 缺失 40 位 commit 拒绝推进；QA 拒绝/失败时拦截写 Done，进入返工治理（`rework_count` 递增，达上限触发升级） | `test_p1_11_exit_code_zero_without_evidence_or_qa_rejection_blocked` | **PASSED** |
| `P1-12` | 伪造 QA 子 Agent 与虚假 Session 拦截 | `platform='subagent'` 冒充 Codex 硬拒；独立审阅人与实现作者 session 相同（自审自签）硬拒；报告哈希不匹配硬拒 | `test_p1_12_unpushed_candidate_and_fake_qa_subagent_rejected` | **PASSED** |
| `P1-13` | 写前 SHA256 CAS 乐观锁防覆写 | 写入前比较文件 SHA256 摘要；遭遇外部/人工并发修改时抛出 `CasConflictError` 拒绝覆盖，完整保留用户现场 | `test_p1_13_cas_optimistic_concurrency_blocks_user_overwrite` | **PASSED** |
| `P1-15` | 真实小范围软件任务端到端演练闭环 | 获批微任务全流程实跑物证审计：锁定服务器候选 `4c58c46be12af0e4dcfc4ef6f40dd162c5b18c06`，Docker 沙箱测试、独立 Codex 只读审签与 ARCH 报告复核全合规闭环，业务仓库零触碰 | `test_p1_15_live_drill_end_to_end_verification` + AUTO-03/04 物证 | **PASSED** |
| `P1-16` | 删入口/改 disabled 保护在途与防注入 | 删入口或改 disabled 不撤销在途任务；原文包含恶意 Shell 命令不直接执行；跨界越权路径访问（如 `soc-ap/core/**`）触发 `BoundaryViolationError` | `test_p1_16_delete_or_disable_preserves_in_flight_and_blocks_shell_and_escape` | **PASSED** |
| `P1-17` | 单指令多角色切片共享 demand_id | 单一稳定需求拆分 `ARCH`、`INTEGRATOR` 等多角色任务卡，保持唯一 `demand_id` 与确认单哈希血缘绑定，路径白名单互斥隔离 | `test_p1_17_single_demand_multi_role_split_preserves_demand_id` | **PASSED** |
| `P1-18` | 批次部分批准与“仅确认需求未批方案”分流 | 批次中仅部分需求获准时仅释放获准项；若 `demand_confirmed=True` 但 `implementation_summary_approved=False` 判定 `DEMAND_CONFIRMED_ONLY` 禁开工 | `test_p1_18_partial_batch_approval_and_demand_only_confirmation` | **PASSED** |
| `P1-19` | 审批防伪（非人类来源/过期/模型自填拦截） | 审批人非 `HUMAN` 拒收；确认单版本/哈希过期拒收；自然语言模糊字样或模型自填 `approved: true` 拒绝作为开工依据 | `test_p1_19_anti_forgery_rejects_bogus_actors_stale_rev_and_fuzzy_prose` | **PASSED** |
| `P1-20` | 原文重排复用有效批准与实质变更升版 | 原文指令调序保留指令摘要哈希，复用既有批准零重复生成；实质变更导致哈希变化必须升版确认 | `test_p1_20_reordered_input_reuses_approvals_while_substantive_bump_requires_fresh` | **PASSED** |

---

## 宿主机真实物证核查（P1-15 闭环验证）

依据 `test_p1_15_live_drill_end_to_end_verification` 与现场物证审计：
1. **M1 单步受控演练物证 (`AUTO-03`)**:
   - `project-control/docs/evidence/coord_automation/AUTO-03/runs/run_01/live_drill/drill_summary.json`
   - 证明 `gpt-6-luna` 真实角色执行，产出 `drill_intake_manifest.json` (`SHA256: 4866705b...`)，生命周期如实停驻在 `AWAITING_SERVER_CANDIDATE_AND_INDEPENDENT_QA`，未伪造自动写 `Done`。
2. **M2 持续推进与恢复物证 (`AUTO-04`)**:
   - `project-control/docs/evidence/coord_automation/AUTO-04/runs/run_01/live_drill/drill_summary.json`
   - 证明 SQLite 权威恢复源、`coord_runner.lock` 进程互斥 (`flock_mutual_exclusion_verified: true`)、双任务异步非阻塞推进 (`fast_done_while_long_active: true`, `step3_both_tasks_completed: true`)、Intake 重扫幂等与 CAS 乐观锁防覆写真实通过。
3. **前置服务器锁定候选 (`4c58c46be12af0e4dcfc4ef6f40dd162c5b18c06`)**:
   - 经 `git diff 4411a1d72643c8153587c1bc814f84b5ee04c74a 4c58c46be12af0e4dcfc4ef6f40dd162c5b18c06` 确认：代码修改严格受限在 `project-control/` 白名单内，**零触碰** `soc-ap/`、`mcu-p3/`、`test_harness/` 及双 Bootloader。
   - `qa-sandbox:20261029` 独立 Docker 容器内构建与测试通过（18 项 recovery 测试全绿）。
   - 宿主机独立 Codex 只读会话（`01a1a09b-5910-7301-8e8f-d14286c47cf1`）出具 `APPROVED` 审签。

---

## 本地自检命令与测试运行实测

1. **`check_task_graph`**:
   - 命令：`PYTHONDONTWRITEBYTECODE=1 python3 project-control/tools/check_task_graph.py --workspace .`
   - 结果：`exit_code: 0`，`errors: []`，任务图零错误。
2. **`run_phase1_m1_m2_acceptance`**:
   - 命令：`PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tools -p 'test_phase1_intake_acceptance.py' -v`
   - 结果：`Ran 20 tests in 1.226s` — **OK (exit 0)**。
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

微任务 `AUTO-05` 独立端到端自动化验收套件与实景物证全部完成，Phase 1 M1 和 M2 涉及的全部 19 项条款（`P1-01~13` 及 `P1-15~20`）在锁定基线上客观实测 100% 通过，已具备提请独立非作者 Codex ARCH 进行复核审签的完整前置条件。
