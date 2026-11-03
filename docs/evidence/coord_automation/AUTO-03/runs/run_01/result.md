# AUTO-03 Execution Record (run_01)

## 任务信息
- **任务编号**: `AUTO-03`
- **任务标题**: `AUTO-03 M1手动单步：三类人工入口收件、版本审批防伪绑定与真实单步角色派发闭环`
- **任务修订号**: `1` (`plan_revision: coord-intake-dispatch-phase1-20261103-rev2`)
- **运行编号**: `run_01`
- **执行角色与会话**: `INTEGRATOR` (`actual_session`: `25b63893-2611-41ff-87d7-0b9f82cf0375`, `model`: `gpt-6-luna`)
- **唯一接收 COORD 会话**: `8d4e8b77-42a9-4bd3-bd5a-1b881e8d4bd5`
- **开工基线 (`source_baseline.project-control`)**: `b4af2d32601a07d448ac8d67a07c57f5b9ab36ac`
- **第一阶段规划与任务卡落仓基线提交 (`Commit B`)**: `b7a0a706b9d5683c69989faa4e6d4f6007826915`
- **授权与协议输入绑定**:
  - 人工批准记录：`project-control/docs/work_intake/approvals/APPR-20261103-001.yaml` (`SHA256: b7ea9ac9bdefc719fc46263c50e3a893d693ad63ae5166bc9085e4c71cc3f96d`)
  - 确认单 `rev 2`：`project-control/docs/planning/coord_intake_dispatch_phase1_confirmation_20261103.md` (`SHA256: 63c1225d60c377a662bebaa0328f9bc95c19daccaa61d9f2766bc989f06f3f98`)
  - 第一阶段设计 `rev 2`：`project-control/docs/architecture/coord_intake_dispatch_phase1_design_20261103.md` (`SHA256: 8a2984c6bb4b868cc8e2d6742873527f448f27c7006d99c5ce322207b2941350`)
  - 宿主机接口实测 `rev 2`：`project-control/docs/evidence/coord_automation/phase1_prep_20261103/integrator_host_interface_verification_20261103.md` (`SHA256: 3e9ebb7eb0992e3517abf1d802bec1fdad4c91a4a0e6d188e54f97d47b7db6d8`)
- **阶段边界声明**: 严格执行第一阶段第 1 步（**M1 手动单步**），**未安装任何 `systemd`/`cron` 后台服务**（属 M3 `AUTO-06`），**未修改 `AUTO-03.md` 为 `Done`**（待正式服务器 Docker 沙箱与独立 Codex QA/ARCH 双重审查通过后由唯一 COORD 收件推进），且 **零触碰** `soc-ap/`、`mcu-p3/`、`test_harness/`、`boot/bootloadermc/`、`boot/bootloaderth/` 及物理硬件。

---

## 交付工件与 SHA256 清单

### 1. 任务卡 `deliverables.artifacts`（9 项核心交付物）
| 路径 | SHA256 | 说明 |
| --- | --- | --- |
| `project-control/tools/coord_runner/work_intake.py` | `531c71020a3c7a4437820396c3693b319de0bf235db18d6ce9700fe5e1352549` | 批量 MD 原文收件解析、1:1 稳定 `demand_id` 映射、唯一主分类 YAML 自动生成、同 `(id, rev)` 防篡改台账、错误隔离与在途生命周期保护 |
| `project-control/tools/coord_runner/approval_guard.py` | `6e709eab82285df50c133e1c7df6610ea5bf4e135a186a542fbcbfe406af4d61` | 真实 `HUMAN` 批准来源校验、确认单 `(confirmation_id, revision, sha256)` 磁盘字节重算绑定、部分批次与子范围审批分流、防模型自批与防自然语言“批准”误触发 |
| `project-control/tools/coord_runner/role_adapter.py` | `a6c051bdc1916e68b351d87eae30f96a77881f553e8b1d43f33bdac70fe98e1e` | 真实宿主 `/home/sushaohua/.local/bin/codex exec -m gpt-6-luna` 四接口（`coordinate`/`submit_role_task`/`query_role_job`/`collect_role_result`）、`NOOP` 零模型调用短路、`allowed_paths` 快照回滚审计、`state_5.sqlite` 只读对账、远端推送与防伪门禁 |
| `project-control/tools/coord_runner/cas_writer.py` | `438a9aa3668491aaa5b01c0121c51647b7ef9f602710dad48501f22a4f5dff66` | 物理字节级 SHA256 CAS 乐观锁（`read_with_digest`, `record_write_intent`, `write_cas`, `create_exclusive`），并发写冲突零覆盖保护 |
| `project-control/tools/coord_runner/runner.py` | `6aa94148750d1a79003f2d9fe4de73c077e54720a5ca0582a2a99767038cd06c` | 废除旧 `git rev-parse HEAD` 空壳 `default_agent_executor`，统一接入 `ApprovalGuard` + `CodexRoleAdapter`，支持 `--once` / `--intake-scan` / `--drill-dir` |
| `project-control/tools/coord_runner/scheduler.py` | `d8a58bb957110d84fb47c5ceb50dbcfc11985d63efb3336ff09dfa715c6a36a4` | 显式隔离旧队列 `coord_autorun_queue_20261029.yaml` 与 `TWIN-*`/`MS-*` 历史任务，补齐前置与自身 `Done` 卡 `done_acceptance_errors` 硬核验 |
| `project-control/config/coord_runner/coord_config.yaml` | `59a51cd659b1ec64f6dc175b9555e571e7116fea973394cd936fdba8137d62ad` | M1 配置：指向 `docs/work_intake/work_intake_queue.yaml`、`isolate_legacy_queue: true`、`/home/sushaohua/.local/bin/codex` 与 `default_model: gpt-6-luna` |
| `project-control/tools/test_work_intake.py` | `52123dee64114e533a86b571e27d912f8b601bec33a77e85ac72e5fcf76dc28b` | M1 全部 12 个正负向场景与真实演练物证确定性单测套件（15 项测试） |
| `project-control/tools/test_coord_runner.py` | `2cbe58169913e1efc6dd77b35e80f5dfb03c47ca3c884be49d6d2130fe3a8e19` | 运行器单步角色适配、前置 `Done` 门禁、旧队列隔离、状态机防伪与 AST 规范门禁单测套件（74 项测试） |

### 2. 配套模块、新队列与示例模板（白名单内）
- `project-control/tools/coord_runner/__init__.py` (`001e0f47cac4527d46cf8100779c5429a7a6b0769655c302a109d644e0e693fb`)
- `project-control/tools/coord_runner/__main__.py` (`6d3f54b9a24428c6e8d90678fdcf5e2b7d32200ce281f9b194daba00d2e03338`)
- `project-control/tools/coord_runner/m1_drill.py` (`9452bab73050922994a9fda71ffaa1f0719ba6efa1a3722771dffb78820be524`)
- `project-control/tools/coord_runner/errors.py` (`b3a353fca1e0cfabfc6a8f135c0cecdb5fe699fbaa3debd8be6c50d83352e155`)
- `project-control/tools/coord_runner/models.py` (`12ad1e16a263d4bd6673f6f92983dcacc8e5e086b2997a1a584f38a12677f9db`)
- `project-control/tools/coord_runner/state_machine.py` (`59baf36d1df4b4684d346dfc7defcce1dce2757e5deff093120a88cb0c154f06`)
- `project-control/tools/coord_queue.py` (`b6c4f918b7c20afd6c3bd23f37790f6555d408dd3143f8f195f4edd61c631b28`)
- `project-control/docs/work_intake/work_intake_queue.yaml` (`d2d148c633c113345c849ce282ec039d3d8acbd61f19265cc0038cf7a30067a0`)
- `project-control/docs/work_intake/examples/`（`README_template.md`, `example_batch_submission.md`, `issues/ISS-EXAMPLE-001.yaml`, `features/FEAT-EXAMPLE-001.yaml`, `requirements/REQ-EXAMPLE-001.yaml`；全部示例显式 `enabled: false`、`approval_refs: []`，与运行目录物理隔离）

---

## M1 覆盖场景（12 项）实现与测试映射

| 场景编号 | 设计要求摘要 | 实现落点 | 验证用例 / 实测证据 |
| --- | --- | --- | --- |
| `P1-01` | 单份批量 MD 指令 1:1 稳定映射 `demand_id`，保留逐字原话与公共约束哈希，自动生成唯一主分类 YAML，零人工手写 YAML | `work_intake.py:parse_submission_markdown`, `WorkIntakeManager.scan_and_sync`, `link_tasks_to_category_yaml` | `test_p1_01_batch_md_generates_unique_three_category_yamls_and_links` + `live_drill` |
| `P1-02` | `requirement` 目标不清时先拉起 `PM`/`ARCH` 只读澄清（`--sandbox read-only`），不擅自起实现卡 | `role_adapter.py:route_intake_demand` (`CLARIFY_PM_ARCH`, `read-only`) | `test_p1_02_p1_04_p1_17_routing_and_multi_role_split` + `live_drill` (`DEM-20261103-002`) |
| `P1-03` | 精确绑定人工批准的 `(confirmation_id, revision, sha256)` 后才放行实施派发 | `approval_guard.py:ApprovalGuard.verify_demand_approval`, `runner.py:_verify_card_human_approval` | `test_p1_03_and_p1_18_partial_batch_subscope_and_demand_only_split`, `test_default_agent_executor_invokes_role_adapter_with_approval` |
| `P1-04` | `issue` 根因未知先只读调查，根因明确且获批直派对应 Owner | `role_adapter.py:route_intake_demand` (`INVESTIGATE_ISSUE_READONLY` vs `DISPATCH_KNOWN_ISSUE_OWNER`) | `test_p1_02_p1_04_p1_17_routing_and_multi_role_split` |
| `P1-06` | 同 `(id, revision)` 篡改、未知 `schema_version`、目录与 `kind` 冲突、损坏/半截 YAML 确定性隔离，不阻塞其他有效项 | `work_intake.py:_check_and_bind_digest`, `_validate_single_category_file`, `_verify_submission_against_records` | `test_p1_06_tampered_same_revision_and_corrupt_records_isolated` |
| `P1-11` | `codex exec` 退出码 `0` 但缺 `candidate_commit` 或缺约定交付物时拒写 `Done` / 拒进入 QA | `role_adapter.py:collect_role_result`, `_verify_deliverables` | `test_p1_11_p1_12_p1_15_candidate_remote_reconcile_and_codex_reviewer_gates` |
| `P1-12` | 未推送远端、缺非作者报告复核、证据哈希失配或普通子 Agent/计划别名冒充独立 Codex 一律拒收件 | `role_adapter.py:_verify_git_commit_and_remote`, `verify_independent_codex_review_entry`, `state_machine.py:_validate_single_reviewer_entry` | `test_p1_11_p1_12_p1_15_candidate_remote_reconcile_and_codex_reviewer_gates`, `test_subagent_platform_and_planned_alias_rejected_in_state_machine` |
| `P1-15` | `project-control` 受控白名单内真实演练小任务走通收件 -> 审批 -> `codex exec -m gpt-6-luna` 单步派发与结果回收 | `m1_drill.py:execute_m1_live_drill`, `runner.py:main --drill-dir` | `live_drill/drill_summary.json` + `test_committed_m1_live_drill_evidence_verified` |
| `P1-16` | 删入口文件或 `enabled: false` 不自动撤已派在途任务；越界路径自动还原报错；原文含 shell 片段仅作被动数据 | `work_intake.py:_reconcile_in_flight_notices`, `role_adapter.py:_audit_and_revert_violations`, `_validate_write_whitelist` | `test_p1_16_disabled_or_deleted_preserves_in_flight_and_blocks_shell_or_forbidden_scope`, `test_p1_16_boundary_revert_and_forbidden_repo_block` |
| `P1-17` | 单一获批需求拆多角色工程卡时保持唯一 `demand_id`，各角色边界独立受控 | `role_adapter.py:build_multi_role_requests` | `test_p1_02_p1_04_p1_17_routing_and_multi_role_split` |
| `P1-18` | 批次部分批准及“仅确认需求、未批实施概要”分流：仅放行已获批子项，未批项挂起不阻塞其他就绪工作 | `approval_guard.py:ApprovalGuard.evaluate_batch_records`, `_evaluate_demand_entry` | `test_p1_03_and_p1_18_partial_batch_subscope_and_demand_only_split` + `live_drill` |
| `P1-19` | 100% 拦截无真实人工源、旧版本批准套新版确认单、模型自填 `approved: true`、仅凭 `enabled: true` 或自然语言“批准”字样 | `approval_guard.py:_verify_human_actor`, `_verify_bound_confirmation`, `work_intake.py:_check_category_record_fields` | `test_p1_19_rejects_forged_actor_stale_rev_tampered_hash_and_prose_keywords` |

---

## 宿主机真实单步演练证据（`P1-15`）

通过命令 `PYTHONDONTWRITEBYTECODE=1 python3 -m tools.coord_runner --drill-dir docs/evidence/coord_automation/AUTO-03/runs/run_01/live_drill` 在宿主机真实调用 `/home/sushaohua/.local/bin/codex exec -m gpt-6-luna` 完成闭环（零模型覆盖）：
- **演练汇总文件**: `project-control/docs/evidence/coord_automation/AUTO-03/runs/run_01/live_drill/drill_summary.json` (`SHA256: cab642ada34ff4cd5484924059ccad011d2578dac8ebb6404f1b9c70f6376e97`)
- **批量收件与部分批准分流**:
  - 自动从 `SUB-DRILL-20261103-001.md` 解析并生成 2 份唯一主分类 YAML（`FEAT-20261103-001.yaml` 与 `REQ-20261103-001.yaml`），`intake_errors: []`；
  - `DEM-20261103-001` 经锚定 `APPR-20261103-001` 的精确确认单 SHA256 校验通过，路由为 `DISPATCH_APPROVED_FEATURE` (`INTEGRATOR`, `workspace-write`)；
  - `DEM-20261103-002`（目标不清 `requirement`）确定性挂起为 `CLARIFY_PM_ARCH` (`read-only`, `implementation_released: false`)，不阻塞已获准项。
- **真实 `COORD` 决策会话与 `NOOP` 短路验证**:
  - 首次 `coordinate()` 真实拉起 `/home/sushaohua/.local/bin/codex exec --sandbox read-only -m gpt-6-luna`：`thread_id = 01a19ff8-7fe0-7d52-8e4c-2f38dad3a7f4`，`actual_model = gpt-6-luna`（经 `~/.codex/sessions/` rollout `turn_context.model` 核实），`tokens = 13843`，事件流 `jobs/coord_521929f68511/codex_events.jsonl` (`SHA256: 0e58f6f34034ae80469254b27add833c8d39f2079891ec4d5471cc44ac5af095`)；
  - 同摘要二次 `coordinate()` 返回 `action = "NOOP"`、`model_invoked = false`（0 模型调用）。
- **真实 `INTEGRATOR` 单步角色派发、状态查询与交付物回收**:
  - `dispatch_key = "AUTO-03-DRILL-01:rev1:INTEGRATOR:implement:1"`，`job_id = "job_AUTO-03-DRILL-01_8f2d267410"`；
  - 真实角色会话 `thread_id = 01a19ff8-92e3-7703-be3a-977a1dc4d835`，`actual_model = gpt-6-luna`，`tokens = 34037`，事件流 `jobs/job_AUTO-03-DRILL-01_8f2d267410/codex_events.jsonl` (`SHA256: 83e611e0a66513c0854ff4ff5cfbe34c8bdecfa13eed6ccf62e213f287acd921`)；
  - `boundary_audit.json` 核验仅写入白名单内 `deliverables/drill_intake_manifest.json`（`SHA256: 4866705b9b624387caace5315b1f5c031dec8ec77ce111a79b288b34f3acdf04`，`violating_paths: []`）；
  - 角色退出后生命周期停留在 `AWAITING_SERVER_CANDIDATE_AND_INDEPENDENT_QA`（`auto_done_written: false`）。

---

## 本地自检与门禁命令验证结果

1. **`check_graph`**:
   - 命令：`PYTHONDONTWRITEBYTECODE=1 python3 project-control/tools/check_task_graph.py --workspace .`
   - 结果：`exit_code: 0`，`errors: []`，`dependency_cycles: []`（同时通过 `--check-artifact AUTO-03` 校验）。
2. **`test_work_intake_m1`**:
   - 命令：`PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tools -p 'test_work_intake.py' -v`（`cwd: project-control`）
   - 结果：`Ran 15 tests` — **OK (exit 0)**。
3. **`test_coord_runner_m1`**:
   - 命令：`PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tools -p 'test_coord_runner.py' -v`（`cwd: project-control`）
   - 结果：`Ran 74 tests` — **OK (exit 0)**。
4. **`test_existing_qa_and_delivery`**:
   - 命令：`PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tools -p 'test_qa_runner.py' -v && PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tools -p 'test_delivery_checks.py' -v`（`cwd: project-control`）
   - 结果：`test_qa_runner.py` 22 tests **OK** + `test_delivery_checks.py` 20 tests **OK (exit 0)**。
5. **`check_ast_coding_standard`**:
   - 命令：`AUTO-03.md` 定义的 AST 函数行数（$\le 50$ 行）与参数个数（$\le 4$ 参）扫描
   - 结果：`AST violations: []` — **exit 0**（100% 合规）。
