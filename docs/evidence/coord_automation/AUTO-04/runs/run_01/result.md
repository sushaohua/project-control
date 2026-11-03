# AUTO-04 Execution Record (run_01)

## 任务信息
- **任务编号**: `AUTO-04`
- **任务标题**: `AUTO-04 M2持续推进与恢复：外置SQLite权威恢复源、长耗时异步并发与五源防重对账`
- **任务修订号**: `1` (`plan_revision: coord-intake-dispatch-phase1-20261103-rev2`)
- **运行编号**: `run_01`
- **执行角色与会话**: `INTEGRATOR` (`actual_session`: `482f7dba-d6ce-4ecc-92d4-29608bc1ffd4`, `model`: `gpt-6-luna`)
- **唯一接收 COORD 会话**: `8d4e8b77-42a9-4bd3-bd5a-1b881e8d4bd5`
- **开工基线 (`source_baseline.project-control`)**: `4411a1d72643c8153587c1bc814f84b5ee04c74a`
- **前置依赖 `AUTO-03` 验收证据**: `project-control/docs/evidence/coord_automation/AUTO-03/runs/run_04/qa_review_report.md` (Done)
- **授权与协议输入绑定**:
  - 人工批准记录：`project-control/docs/work_intake/approvals/APPR-20261103-001.yaml` (`SHA256: b7ea9ac9bdefc719fc46263c50e3a893d693ad63ae5166bc9085e4c71cc3f96d`)
  - 确认单 `rev 2`：`project-control/docs/planning/coord_intake_dispatch_phase1_confirmation_20261103.md` (`SHA256: 63c1225d60c377a662bebaa0328f9bc95c19daccaa61d9f2766bc989f06f3f98`)
  - 第一阶段设计 `rev 2`：`project-control/docs/architecture/coord_intake_dispatch_phase1_design_20261103.md` (`SHA256: 8a2984c6bb4b868cc8e2d6742873527f448f27c7006d99c5ce322207b2941350`)
- **阶段边界声明**: 严格执行第一阶段第 2 步（**M2 持续推进与恢复**），**未安装任何 `systemd`/`cron` 后台服务**（属 M3 `AUTO-06`），**未修改 `AUTO-04.md` 为 `Done`**（待正式服务器 Docker 沙箱与独立 Codex QA/ARCH 双重审查通过后由唯一 COORD 收件推进），且 **零触碰** `soc-ap/`、`mcu-p3/`、`test_harness/`、`boot/bootloadermc/`、`boot/bootloaderth/` 及物理硬件。

---

## 交付工件与 SHA256 清单

### 1. 任务卡 `deliverables.artifacts`（5 项核心交付物）
| 路径 | SHA256 | 说明 |
| --- | --- | --- |
| `project-control/tools/coord_runner/state_store.py` | `d8858738f06a94c77c131ec3c497e5b600954785ee1689866e4485cc962fc637` | 外置 WAL SQLite 权威恢复源；支持配置覆盖隔离单测；实现 `fcntl.flock(LOCK_EX \| LOCK_NB)` 进程互斥锁与 `active_coord_thread_id` 状态持久化 |
| `project-control/tools/coord_runner/job_launcher.py` | `9463a4daa5f25dbfdef4316294b77638170e3b3e961ab95919d9bd3bbb07e429` | 非阻塞异步作业拉起（`start_new_session=True`）；落盘包含 `/proc/<pid>/stat` 字段 22 `starttime` 的 `pid.json`（防 PID 重用误判）；原子落盘 `exit_status.json` |
| `project-control/tools/coord_runner/reconciler.py` | `90289fed609ea8b5bc6b45c9a77bc2b7f3e2063976771feb7aa3afa7775d8602` | 五源防重对账机制（对齐 SQLite、/proc、本地事件流、宿主 `state_5.sqlite` 及 `exit_status.json`）；实现孤儿进程收割、超时标记、断点恢复与租约活跃保护 |
| `project-control/tools/coord_runner/runner.py` | `7081e498370601acd05817c5570cdb7a5f13d030415378d7ac5a1f063f150e61` | 接入 `StateStore` 作为单一权威恢复源；集成 `JobLauncher` 与 `FiveSourceReconciler`；支持外置异步非阻塞调度与断电续接推进 |
| `project-control/tools/test_coord_recovery.py` | `641d49979e8917c10e2da7ff403916f2e2979e01a70d2e2546ed25898848ab4f` | 覆盖 WAL 单一恢复源、异步双卡并发推进、重扫幂等、新版冲突保护、超时/孤儿五源对账、flock 单实例锁、租约活跃保护及 AST 门禁（16 项测试） |

### 2. 配套模块与物证演练（白名单内）
- `project-control/tools/coord_runner/m2_drill.py` (`7f3fa5ed04fb334f421dc38b83eef65a9b5a3fd1d003e25c1db2ecbc171cf4f8`): 宿主机 M2 恢复与并发演练执行器
- `project-control/tools/coord_runner/models.py` (`3cb73f482c966da352138de24f83396fda733d19a9a6c10f97dbdcd430871f42`): 补充 `state_db_file` 与 `lock_file` 解析及自动测试隔离
- `project-control/tools/coord_runner/role_adapter.py` (`9461dfebb2ec64840f6c4ca3fec8fa6368d2c9117017437cec2f7794230193a2`): 补充 `submit_role_task_async` 异步外置调度接口
- `project-control/tools/coord_runner/__init__.py` (`f0443a336bb2420fffb35b54e54eaf8fc00c71283053e86c254dafb405a7492e`): 导出 M2 新增模块与方法
- `project-control/docs/evidence/coord_automation/AUTO-04/runs/run_01/live_drill/drill_summary.json` (`f2d06885475152f21485d0a080f9595006f6c71070cff2018c092c6083d8563b`): 宿主机 M2 真实演练物证汇总

---

## M2 覆盖场景（7 项）实现与验证映射

| 场景编号 | 设计要求摘要 | 实现落点 | 验证用例 / 实测证据 |
| --- | --- | --- | --- |
| `P1-05` | 同一记录 `(id, rev, content_sha256)` 重复扫描或重通知返回已有回执，零新增工程作业 | `reconciler.py:check_intake_idempotence`, `state_store.py:set_meta/get_meta` | `test_coord_recovery.py:test_rescan_idempotence_p1_05` |
| `P1-07` | 新 `revision` 遇到旧版在途任务不静默换输入或盲目重发，明确新旧绑定和影响交 COORD 裁决 | `reconciler.py:check_in_flight_revision`, `runner.py:dispatch_task` | `test_coord_recovery.py:test_in_flight_revision_conflict_p1_07` |
| `P1-08` | 长耗时角色任务外置异步运行期间，另一条无冲突就绪任务真实推进（最多 2 卡并行） | `job_launcher.py:JobLauncher.launch_async` (`start_new_session=True`), `runner.py:step` (`max_parallel_implementation=2`) | `test_coord_recovery.py:test_max_parallel_implementation_allows_two_concurrent_tasks` + `live_drill` |
| `P1-09` | 派单超时或崩溃后凭五源对账（SQLite, /proc, events, host DB, exit_status）续接；无法确认“从未启动”标 `RECONCILE_REQUIRED` 禁盲重发 | `reconciler.py:reconcile_job`, `_handle_orphan_job`, `_lookup_host_thread` | `test_coord_recovery.py:test_reconcile_orphan_killed_process_flags_reconcile_required_p1_09` + `test_reconcile_completed_job_from_exit_status` |
| `P1-10` | `coord_runner.lock` 拦截多实例；租约在纸面上超时但底层 `/proc` 进程仍活跃时保护租约禁被抢占重派 | `state_store.py:acquire_process_lock`, `reconciler.py:protect_active_leases`, `runner.py:step` | `test_coord_recovery.py:test_single_instance_flock_mutual_exclusion` + `test_protect_active_leases_for_running_processes_p1_10` + `live_drill` |
| `P1-13` | 写任务卡或状态前校验字节级 SHA256 CAS；遇人工或其他并发修改拒覆盖，保留操作意图 | `cas_writer.py:write_cas`, `reconciler.py:verify_cas_write` | `test_coord_recovery.py:test_cas_conflict_detection_p1_13` + `live_drill` |
| `P1-20` | 原文重排或非关键说明修订不重建需求；未实质变化项复用既有有效人工批准 | `work_intake.py:_reconcile_in_flight_notices`, `approval_guard.py:verify_demand_approval` | `test_work_intake.py:test_p1_03_and_p1_18_partial_batch_subscope_and_demand_only_split` + `test_coord_recovery.py` |

---

## 宿主机真实 M2 演练物证（`live_drill`）

通过命令 `python3 -m tools.coord_runner --drill-m2-dir docs/evidence/coord_automation/AUTO-04/runs/run_01/live_drill` 在宿主机执行 M2 真实演练：
- **演练物证汇总**: `project-control/docs/evidence/coord_automation/AUTO-04/runs/run_01/live_drill/drill_summary.json` (`SHA256: f2d06885475152f21485d0a080f9595006f6c71070cff2018c092c6083d8563b`)
- **单一权威恢复源 SQLite**:
  - 文件：`docs/evidence/coord_automation/AUTO-04/runs/run_01/live_drill/state.sqlite3` (`SHA256: da222962026b7924d381cc29bdb7476b80aa1fd0078dc6e29d1908122ad74674`)
  - 验证 WAL 模式及 `role_jobs`、`coord_meta`、`leases` 表事务读写完整性。
- **flock 进程排他锁**:
  - 文件：`docs/evidence/coord_automation/AUTO-04/runs/run_01/live_drill/coord_runner.lock`
  - 验证首实例持有锁期间，第二实例调用 `acquire_process_lock()` 100% 触发 `ResourceConflictError`。
- **异步双任务并发拉起与对账（P1-08 / P1-09）**:
  - `task_a` 与 `task_b` 以独立 session (`start_new_session=True`) 并发拉起；
  - 各种各自落盘 `/proc/<pid>/stat` 字段 22 `starttime` 绑定的 `pid.json`；
  - 进程结束时原子落盘 `exit_status.json`（`task_a`: `0e111493...`, `task_b`: `e3626761...`），五源对账器确认双双为 `COMPLETED`。
- **活跃租约保护（P1-10）**:
  - `DRILL-ACTIVE` 任务在纸面上租约已过期（`expires_at = time.time() - 10.0`），但对账器核验底层 `/proc/<pid>` 仍然存活且 starttime 一致，确定性自动续展租约，拦截抢占。
- **CAS 并发修改冲突拦截（P1-13）**:
  - `cas_test.md` 注入人工并发手改后，CAS 校验拦截覆盖并抛出 `CasConflictError`。

---

## 本地自检与门禁命令验证结果

1. **`check_graph`**:
   - 命令：`PYTHONDONTWRITEBYTECODE=1 python3 project-control/tools/check_task_graph.py --workspace . --check-artifact AUTO-04`
   - 结果：`exit_code: 0`，`errors: []`，`dependency_cycles: []`，5 项核心工件哈希核验全部匹配。
2. **`test_coord_recovery_m2`**:
   - 命令：`PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s project-control/tools -p 'test_coord_recovery.py' -v`
   - 结果：`Ran 16 tests` — **OK (exit 0)**。
3. **`test_work_intake_m1`**:
   - 命令：`PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s project-control/tools -p 'test_work_intake.py' -v`
   - 结果：`Ran 15 tests` — **OK (exit 0)**。
4. **`test_coord_runner_m1`**:
   - 命令：`PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s project-control/tools -p 'test_coord_runner.py' -v`
   - 结果：`Ran 74 tests` — **OK (exit 0)**。
5. **`test_existing_qa_and_delivery`**:
   - 命令：`PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s project-control/tools -p 'test_qa_runner.py' -v && PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s project-control/tools -p 'test_delivery_checks.py' -v`
   - 结果：`test_qa_runner.py` 22 tests **OK** + `test_delivery_checks.py` 20 tests **OK (exit 0)**。
6. **`check_ast_coding_standard`**:
   - 命令：AST 函数规模（$\le 50$ 行）与参数个数（$\le 4$ 参）扫描全量自研模块（`coord_runner/*.py`、`test_coord_recovery.py`、`test_coord_runner.py`、`test_work_intake.py`）
   - 结果：`AST violations: []` — **exit 0**（100% 零违规通过）。
