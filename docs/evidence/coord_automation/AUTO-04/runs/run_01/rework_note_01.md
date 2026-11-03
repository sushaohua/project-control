# AUTO-04 Rework Note 01

## 缺陷标识与审计背景
- **任务编号**: AUTO-04 (M2 持续推进与恢复：外置SQLite权威恢复源、长耗时异步并发与五源防重对账)
- **审查轮次**: run_01 独立 Host Codex QA 审计 (会话 `01a1a07e-749c-7721-810a-9b3675cdc769`)
- **审计决议**: REJECTED
- **缺陷项**:
  1. **F-01**: P1-08 异步作业调度未接入生产生命周期
  2. **F-02**: P1-05 幂等防护未接入 Intake 重扫流程

---

## 根因分析 (Root Cause Analysis)

### 1. F-01 根因
- 在首版实现中，`CoordRunner.step()` 依赖 `_process_task_safely()` → `process_task()` → `_execute_agent_phase()` 同步调用 `agent_executor`，即使定义了 `dispatch_async_role_task()` 也未在 `runner.py` 正常的生产生命周期中被触发。
- 长耗时角色执行阻塞了调度线程，导致队列中下一张就绪且无冲突的任务无法并发推进。
- 原演练脚本 `m2_drill.py` 仅直接调用底层的 `JobLauncher` 运行 sleep 进程并对账，未驱动实际 `CoordRunner` 双任务生命周期推进流。

### 2. F-02 根因
- `FiveSourceReconciler.check_intake_idempotence()` 虽在对账器中实现了基于 SQLite 的摘要检查，但未被 `WorkIntakeManager` 或 `CoordRunner.scan_work_intake()` 调用。
- 缺少在 Intake 扫描和重扫流程中将 demand digest 登记到权威 SQLite 存储并在重扫相同 `(id, revision, content_sha256)` 时返回既有关联而不新增任务或作业的闭环。

---

## 修复对策与工程实施 (Engineering Fixes)

### 1. F-01 修复：异步作业调度与生命周期完整接入
- **`runner.py`**:
  - 在 `_execute_agent_phase()` 中接入 `self.dispatch_async_role_task()`，当处于异步派发模式（`self.async_role_dispatch = True` 或 `wire_production_executors()`）时，通过 `job_launcher.launch_async()` 启动非阻塞后台进程，记录 `async_job_id`，立即返回而不阻塞调度器。
  - 在 `_check_async_job_completions()` 中轮询收集各在途任务对应的外置作业状态；当作业变为 `COMPLETED` 时自动收集交付物、验证候选 commit 并推进至 `CANDIDATE_PUSHED`。
  - 在 `step()` 循环中，当长耗时任务在后台运行（`async_job_id` 存在）时快速返回，调度器继续推进并发上限内（最大 2 个实现任务）的下一张无冲突任务。
- **`m2_drill.py`**:
  - 重构演练执行器，实例化真实的 `CoordRunner`，配置 `DRILL-LONG`（耗时 1.2s）与 `DRILL-FAST`（耗时 0.05s）双任务。
  - 演练客观物证证明：在 `DRILL-LONG` 后台持续运行期间，`DRILL-FAST` 成功推进并通过 QA 与 Review 率先达到 `Done`；随后 `DRILL-LONG` 完成并推进至 `Done`。

### 2. F-02 修复：Intake 重扫幂等防护闭环
- **`reconciler.py`**:
  - 增加 `record_intake_digest(demand_id, rev, content_sha)` 并在 `check_intake_idempotence()` 中实现自动首录与幂等匹配。
- **`work_intake.py`**:
  - `WorkIntakeManager` 接入 `reconciler`，在解析与入库时向权威 SQLite 登记 digest；重扫已有指令时执行防重校验。
- **`runner.py`**:
  - `scan_work_intake()` 对扫描记录执行 `reconciler.check_intake_idempotence()` 对账，准确统计并返回 `idempotent_records_count`；对于已收录且哈希一致的需求，直接返回既有记录，不新增任何文件、任务卡或角色作业。

---

## 客观验证结果 (Objective Verification Evidence)

1. **单元测试全量通过**:
   - `python3 -m unittest discover -s project-control/tools -p 'test_coord_recovery.py'`: 18/18 PASS
     - 包含新增 `test_async_task_advances_while_long_job_running_p1_08`
     - 包含新增 `test_intake_rescan_idempotence_guard_p1_05`
   - `python3 -m unittest discover -s project-control/tools -p 'test_coord_runner.py'`: 74/74 PASS
   - `python3 -m unittest discover -s project-control/tools -p 'test_work_intake.py'`: 15/15 PASS
   - `python3 -m unittest discover -s project-control/tools -p 'test_qa_runner.py'`: 22/22 PASS
   - `python3 -m unittest discover -s project-control/tools -p 'test_delivery_checks.py'`: 20/20 PASS
   - 总计 149 项自动化测试 100% 通过。
2. **AST 编码规范门禁**:
   - 所有新增与修改的自研 Python 函数 100% 满足行数 $\le 50$ 且参数 $\le 4$。
3. **宿主演练客观物证**:
   - `docs/evidence/coord_automation/AUTO-04/runs/run_01/live_drill/drill_summary.json`:
     - `fast_done_while_long_active`: `true`
     - `long_job_active_in_flight`: `true`
     - `step3_both_tasks_completed`: `true`
     - `idempotence_verified`: `true`
     - `flock_mutual_exclusion_verified`: `true`
