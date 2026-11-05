---
id: ARCH-BREAKDOWN-COORD-INTAKE-CHECKPOINT-20261105
revision: 1
author_role: ARCH
author_session: ef428595-f4d6-46a7-9d12-07e1fd215641
status: Approved
qa_policy: streamlined-v1
submission_id: 20261105_coord_intake_trigger_gap
issue_ids:
  - ISS-20261105-004
demand_ids:
  - DEM-20261105-004
source_baseline:
  project-control: 491158cd4f183a01517c36fb093821db54a8a6dd
  soc-ap: 68b926e4376185a4979869a4787b90c8623a9164
  mcu-p3: 016e1236af75f6f19282d6b000f4b1b68bd96cc3
  test_harness: d14ed04321c6d4f5ddb35a8801604a8af53b5b60
  bootloadermc: 4fc171ea61912561949b9a0cfc1da8975e4c39ba
  bootloaderth: 769fccbe52464ad7ceb856c5e89cb0d25abbbf87
read_sources:
  - project-control/docs/work_intake/submissions/20261105_coord_intake_trigger_gap.md
  - project-control/docs/work_intake/issues/ISS-20261105-004.yaml
  - project-control/tools/coord_runner/runner.py
  - project-control/tools/coord_runner/work_intake.py
  - project-control/tools/test_coord_runner.py
  - project-control/tools/test_work_intake.py
  - project-control/tools/test_coord_systemd_service.py
  - project-control/.agents/kanban/microtasks/coord_automation/AUTO-03.md
  - project-control/.agents/kanban/microtasks/coord_automation/AUTO-04.md
  - project-control/.agents/kanban/microtasks/coord_automation/AUTO-05.md
  - project-control/.agents/kanban/microtasks/coord_automation/AUTO-06.md
  - project-control/docs/work_intake/.intake_digests.json
  - project-control/docs/work_intake/features/FEAT-20261104-001.yaml
  - project-control/docs/work_intake/features/FEAT-20261104-002.yaml
  - project-control/.agents/rules/c_cpp_coding_standard.md
  - project-control/.agents/rules/code_documentation_standard.md
  - project-control/.agents/rules/delivery_and_coord_gate.md
  - project-control/.agents/rules/codex_qa_review.md
created_at: '2026-11-05T11:32:00+08:00'
---

# `ISS-20261105-004` (`DEM-20261105-004`) COORD 人工收件检查点接通与摘要账本一致性修复架构拆解 (`2026-11-05`)

## 1. 只读事实核查与根因定位

### 1.1 收件单与关联源码只读核实
针对收件原件 [`project-control/docs/work_intake/submissions/20261105_coord_intake_trigger_gap.md`](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/work_intake/submissions/20261105_coord_intake_trigger_gap.md)（`sha256: 4e353ffb5450bd7af66f022ce0b0634baeb0987e9261797afcccae56ec57749a`）及已归档 [`project-control/docs/work_intake/issues/ISS-20261105-004.yaml`](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/work_intake/issues/ISS-20261105-004.yaml)，只读核实以下三项核心事实：

1. **事实一：`CoordRunner` 仅在 `--intake-scan` CLI 分支调用 `scan_work_intake()`，未接入启动/恢复与 `step()` 调度检查点**：
   - 在 [`project-control/tools/coord_runner/runner.py#L551-L568`](file:///home/sushaohua/workspace/ai_soc_project/project-control/tools/coord_runner/runner.py#L551-L568) 中，`CoordRunner.scan_work_intake(self, persist_ledger: bool = True) -> dict` 已完整实现，内部调用 `self.intake_mgr.scan_and_sync(persist_ledger=persist_ledger, active_cards=self.load_cards())` 并结合 `FiveSourceReconciler.check_intake_idempotence()` 做五源幂等对账。
   - 然而，在 [`runner.py#L818-L821`](file:///home/sushaohua/workspace/ai_soc_project/project-control/tools/coord_runner/runner.py#L818-L821) 中，`scan_work_intake()` 仅在显式传入 `--intake-scan` 时被调用（且传入了 `persist_ledger=False`）。
   - 在 [`runner.py#L118-L129`](file:///home/sushaohua/workspace/ai_soc_project/project-control/tools/coord_runner/runner.py#L118-L129) 的 `restore_from_checkpoint()`、[`runner.py#L689-L724`](file:///home/sushaohua/workspace/ai_soc_project/project-control/tools/coord_runner/runner.py#L689-L724) 的 `step()`、以及循环调用 `step()` 的 `run_once()` / `run_tasks()` / `run_daemon()`（[`runner.py#L726-L770`](file:///home/sushaohua/workspace/ai_soc_project/project-control/tools/coord_runner/runner.py#L726-L770)）中，**均未调用 `scan_work_intake()`**。
   - 结果：即便运行 `CoordRunner.step()` 或 `--once` / `--daemon`，放入 `docs/work_intake/submissions/` 的新提交也不会在启动、恢复或每轮调度检查点被自动扫描建档。

2. **事实二：`FEAT-20261104-001.yaml` 与 `FEAT-20261104-002.yaml` 在 `r3` 关联 `arch_breakdown` 时未递增 revision 并同步 `.intake_digests.json`，触发 `TAMPERED_SAME_REVISION`**：
   - 只读执行 `python3 -m tools.coord_runner --intake-scan` 返回退出码 `1`，报错如下：
     - `FEAT-20261104-001.yaml`（`revision: 3`）：[`project-control/docs/work_intake/.intake_digests.json#L5`](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/work_intake/.intake_digests.json#L5) 记录 `FEAT-20261104-001@r3` 为 `4602706f1d362b16a5c20373363a9f864e84f007fb36357ace949fcd1eb2ec9b`，而磁盘文件实际 SHA-256 为 `823e7d1e8064a38254ad94f566f67993070b00afc8fb49b0c98f5ab435d7eac3`。
     - `FEAT-20261104-002.yaml`（`revision: 3`）：[`.intake_digests.json#L8`](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/work_intake/.intake_digests.json#L8) 记录 `FEAT-20261104-002@r3` 为 `30745d7453b9a54e3beb663854c55c861b4c2efcf6ecdc93f01071be927dd08a`，而磁盘文件实际 SHA-256 为 `b7ddc92bb447c1f6e21e7165e6d140bc1d392772df03f2aec8702fba3fc4cc31`。
   - **根因**：[`project-control/tools/coord_runner/work_intake.py#L91-L99`](file:///home/sushaohua/workspace/ai_soc_project/project-control/tools/coord_runner/work_intake.py#L91-L99) 的 `TaskLinkUpdate` 与 [`#L587-L627`](file:///home/sushaohua/workspace/ai_soc_project/project-control/tools/coord_runner/work_intake.py#L587-L627) 的 `link_tasks_to_category_yaml()` 仅支持更新 `task_ids`、`demand_ref_updates`、`approval_refs`、`requested_action`，缺少对 `related_ids.arch_breakdown` 等关联元数据更新的原子字段支持；后续在向 [`FEAT-20261104-001.yaml#L63-L68`](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/work_intake/features/FEAT-20261104-001.yaml#L63-L68) 与 [`FEAT-20261104-002.yaml#L63-L68`](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/work_intake/features/FEAT-20261104-002.yaml#L63-L68) 写入 `related_ids.arch_breakdown` 时直接原地修改了 `r3` 文件而未递增至 `revision: 4` 并更新 `.intake_digests.json`。

3. **事实三：宿主机运行态边界与 `AUTO-06` 历史证据保留**：
   - [`AUTO-06.md`](file:///home/sushaohua/workspace/ai_soc_project/project-control/.agents/kanban/microtasks/coord_automation/AUTO-06.md)（M3 定时调度：单实例 systemd 用户服务部署与 P1-14 零空耗及重启恢复独立验收）已处于 `status: Done`，其历史证据与审阅记录保持完整不变。
   - 当前宿主机未开启后台 `ai-soc-coord-runner.service` 常驻进程，而是由唯一交互式 COORD 会话（`ff2fb105-fd84-4ecb-b1e6-8f8eb00badc6`）配合会话内定时 `/schedule` 承担唯一调度者。
   - **架构边界铁律**：本轮修复仅在代码与检查点层面打通 `CoordRunner` 的启动/恢复/`step()` 收件扫描与账本同步，**严禁在验收或测试中在宿主机真实启动常驻 `ai-soc-coord-runner.service` 与当前唯一交互式 COORD 会话抢锁**；报告与验收口径必须明确区分“代码检查点接通验证通过”与“宿主机后台 systemd 服务当前未启用”。

---

## 2. 技术修复方案与安全/零空耗不变量设计

### 2.1 `CoordRunner` 启动/恢复与 `step()` 检查点最小改动接通（`runner.py`）
1. **优化 `scan_work_intake()` 签名以避免单步内重复扫描看板**：
   - 将 [`runner.py#L551`](file:///home/sushaohua/workspace/ai_soc_project/project-control/tools/coord_runner/runner.py#L551) 的 `scan_work_intake` 扩展为：
     ```python
     def scan_work_intake(self, persist_ledger: bool = True, active_cards: Optional[dict] = None) -> dict:
     ```
     当调用方（如 `step()`）已持有 `cards = self.load_cards()` 时直接传入 `active_cards=cards`，避免在同一 `step()` 内重复执行耗时的 `check_task_graph.check()`；若 `active_cards is None` 则按原逻辑调用 `self.load_cards()`。
   - 将最新扫描结果缓存在 `self.last_intake_summary: Optional[dict] = None`，便于启动/恢复后核查收件回执与错误隔离状态。
2. **在 `restore_from_checkpoint()` 恢复检查点接通收件扫描**：
   - 在 [`runner.py#L118-L129`](file:///home/sushaohua/workspace/ai_soc_project/project-control/tools/coord_runner/runner.py#L118-L129) 的 `restore_from_checkpoint()` 完成 SQLite / JSON 状态与租约恢复后，调用 `self.scan_work_intake(persist_ledger=True)`，确保 Runner 在启动或崩溃恢复检查点立即同步期间到达的人工提交，同时保持已恢复的 `in_flight_tasks`、`completed_tasks`、`cursor` 与 `leases` 100% 不变。
3. **在 `step()` 调度检查点接通收件扫描并返回结构化回执**：
   - 在 [`runner.py#L689-L724`](file:///home/sushaohua/workspace/ai_soc_project/project-control/tools/coord_runner/runner.py#L689-L724) 的 `step()` 中：
     ```python
     cards = self.load_cards()
     intake_summary = self.scan_work_intake(persist_ledger=True, active_cards=cards)
     ```
   - 在 `step()` 返回字典中新增 `"intake": intake_summary` 字段（保留原有 `"cursor"`、`"dispatched"`、`"in_flight"`、`"completed"`、`"blocked"`、`"escalated"` 全部字段不变）。
4. **保持 CLI `--intake-scan` 行为兼容**：
   - `--intake-scan` 继续调用 `runner.scan_work_intake(persist_ledger=False)` 做只读扫描校验，当 `summary["errors"]` 非空时返回退出码 `1`，为空时返回 `0`。

### 2.2 零空耗、坏文件隔离与不绕过审批/前置/租约门禁保证
1. **无变化时零模型调用（P1-14）与零无效磁盘写入**：
   - `scan_work_intake()` 纯由确定性 Python 解析与 SHA-256 摘要校验组成，**不论是否有新提交，均不调用任何大模型（`agent_executor` / `qa_executor` / `review_executor` 调用次数为 `0`）**。
   - 在 [`work_intake.py#L338-L346`](file:///home/sushaohua/workspace/ai_soc_project/project-control/tools/coord_runner/work_intake.py#L338-L346) 的 `_save_ledger(self, ledger: dict)` 中增加幂等短路：
     - 若 `self.ledger_path.is_file()` 且现有文件内容与序列化后的 `payload` 完全一致（`snap.text == payload`），直接 `return` 跳过 `write_cas`，确保空闲 `step()` 轮询时零磁盘覆写；
     - 若 `self.ledger_path` 尚不存在、且 `ledger` 三个桶均为空、且 `self.intake_root / "submissions"` 目录不存在（如轻量单测临时目录），直接 `return` 不创建空账本文件。
2. **单份坏文件故障隔离**：
   - `WorkIntakeManager._scan_category_files()` 与 `_ingest_single_submission()` 已经对单文件 `IntakeValidationError` / `YAMLError` / `OSError` 进行捕获并写入 `result.errors`，不会中断其他合法 Markdown 提交单的建档，也不会抛异常中断 `CoordRunner.step()` 对在途任务的推进。
3. **严禁绕过批准、技术前置或台架租约**：
   - `scan_work_intake()` 仅将 `submissions/*.md` 转换为 `issues/`、`features/`、`requirements/` 下的分类 YAML（初始 `requested_action` 为 `triage` 或 `clarify`，`approval_refs: []`），**绝不自动改写任务队列 `work_intake_queue.yaml`、绝不自动将任何微任务卡置为 `Ready`、绝不绕过 `ApprovalGuard.require_implementation_approval()`、绝不绕过 `CoordScheduler` 前置 `Done` 检查或 `LeaseManager` 独占设备租约**。

### 2.3 `link_tasks_to_category_yaml()` 扩展与 `FEAT-20261104-001/002` 账本对齐（`work_intake.py` & `docs/work_intake/`）
1. **扩展 `TaskLinkUpdate` 与 `link_tasks_to_category_yaml()`**：
   - 在 [`work_intake.py#L91-L99`](file:///home/sushaohua/workspace/ai_soc_project/project-control/tools/coord_runner/work_intake.py#L91-L99) 的 `TaskLinkUpdate` 中新增可选字段 `arch_breakdown: Optional[dict] = None`。
   - 为遵守“单个函数 $\le 50$ 行、入参 $\le 4$ 个”的 AST 硬门禁，将 `link_tasks_to_category_yaml()` 中的字典字段合并逻辑拆分为内部辅助函数 `_apply_task_link_updates(data: dict, update: TaskLinkUpdate) -> None`（中文 docstring/注释）：
     - 支持原子写入 `related_ids["arch_breakdown"] = dict(update.arch_breakdown)`；
     - 当内容发生变更时自动将 `data["revision"]` 递增 `+1`，通过 `write_cas` 落盘后**无条件更新并保存 `.intake_digests.json`**（移除原有的 `if self.ledger_path.is_file():` 限制，确保任何通过 `link_tasks_to_category_yaml()` 的元数据修订都 100% 同步登记 `f"{data['id']}@r{data['revision']}"` 摘要）。
2. **修复 `FEAT-20261104-001.yaml` 与 `FEAT-20261104-002.yaml` 的 `TAMPERED_SAME_REVISION`**：
   - 保留 `.intake_digests.json` 中已登记的 `FEAT-20261104-001@r1..r3` 与 `FEAT-20261104-002@r1..r3` 历史摘要不篡改；
   - 将包含了 `related_ids.arch_breakdown` 的 [`FEAT-20261104-001.yaml#L3`](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/work_intake/features/FEAT-20261104-001.yaml#L3) 与 [`FEAT-20261104-002.yaml#L3`](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/work_intake/features/FEAT-20261104-002.yaml#L3) 的 `revision` 从 `3` 递增为 `4`；
   - 将递增 `revision: 4` 后的两个文件精确 SHA-256 写入 [`project-control/docs/work_intake/.intake_digests.json`](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/work_intake/.intake_digests.json) 的 `categories["FEAT-20261104-001@r4"]` 与 `categories["FEAT-20261104-002@r4"]`，使 `python3 -m tools.coord_runner --intake-scan` 恢复 `errors: []` 且退出码为 `0`。

---

## 3. 微任务定义：`AUTO-07`（`INTEGRATOR`）

### 3.1 任务卡元数据契约
- **`id`**: `AUTO-07`
- **`title`**: `AUTO-07 接通CoordRunner启动/恢复与step人工收件检查点并修复分类账本摘要同步`
- **`owner` / `proposed_owner` / `executor.role`**: `INTEGRATOR`
- **`primary_work_package`**: `TASK-010`（需将 `AUTO-07` 登记入 `project-control/docs/planning/work_packages/TASK-010.md` 的 `child_tasks`）
- **`related_work_packages`**: `[]`
- **`task_kind`**: `implementation`
- **`development_stage`**: `cross-stage`
- **`qa_policy`**: `streamlined-v1`
- **`reviewer`**: `['QA']`
- **`issue`**: `ISS-20261105-004`
- **`demand_id`**: `DEM-20261105-004`
- **`depends_on`**:
  - `AUTO-06`
- **`dependency_conditions`**:
  ```yaml
  - task: AUTO-06
    accepted_version: e6e4291a9608473cae2604dceb521c930d0c341f
    acceptance_evidence: docs/evidence/coord_automation/AUTO-06/runs/run_03/qa_review_report.md
    required: 继承AUTO-06已验收的CoordRunner单实例锁、SQLite恢复源与WorkIntakeManager收件底座（保留AUTO-06 Done状态与历史证据）
  ```
- **`allowed_repositories`**:
  - `project-control`
- **`write_scope`**:
  ```yaml
  project-control:
    - tools/coord_runner/runner.py
    - tools/coord_runner/work_intake.py
    - tools/test_coord_runner.py
    - tools/test_work_intake.py
    - docs/work_intake/features/FEAT-20261104-001.yaml
    - docs/work_intake/features/FEAT-20261104-002.yaml
    - docs/work_intake/.intake_digests.json
    - docs/evidence/coord_automation/AUTO-07/**
  ```
- **`allowed_paths`**:
  ```yaml
  - project-control/tools/coord_runner/runner.py
  - project-control/tools/coord_runner/work_intake.py
  - project-control/tools/test_coord_runner.py
  - project-control/tools/test_work_intake.py
  - project-control/docs/work_intake/features/FEAT-20261104-001.yaml
  - project-control/docs/work_intake/features/FEAT-20261104-002.yaml
  - project-control/docs/work_intake/.intake_digests.json
  - project-control/docs/evidence/coord_automation/AUTO-07/**
  ```
- **`forbidden_paths`**:
  ```yaml
  - soc-ap/**
  - mcu-p3/**
  - test_harness/**
  - boot/bootloadermc/**
  - boot/bootloaderth/**
  - project-control/.agents/kanban/microtasks/coord_automation/AUTO-03.md
  - project-control/.agents/kanban/microtasks/coord_automation/AUTO-04.md
  - project-control/.agents/kanban/microtasks/coord_automation/AUTO-05.md
  - project-control/.agents/kanban/microtasks/coord_automation/AUTO-06.md
  ```
- **`deliverables`**:
  ```yaml
  artifacts:
    - project-control/tools/coord_runner/runner.py
    - project-control/tools/coord_runner/work_intake.py
    - project-control/tools/test_coord_runner.py
    - project-control/tools/test_work_intake.py
    - project-control/docs/work_intake/features/FEAT-20261104-001.yaml
    - project-control/docs/work_intake/features/FEAT-20261104-002.yaml
    - project-control/docs/work_intake/.intake_digests.json
  record: docs/evidence/coord_automation/AUTO-07/runs/author_01/result.md
  ```

### 3.2 新增与更新单测要求（`test_coord_runner.py` & `test_work_intake.py`）
1. 在 [`project-control/tools/test_coord_runner.py`](file:///home/sushaohua/workspace/ai_soc_project/project-control/tools/test_coord_runner.py) 中新增测试方法（每个函数 $\le 50$ 行、入参 $\le 4$ 个，中文注释/docstring）：
   - `test_step_and_restore_checkpoints_auto_scan_intake_idempotently()`：
     - 验证在 `intake/submissions/` 放入合法 Markdown 提交单后，直接调用 `runner.step()`（或 `runner.restore_from_checkpoint()`）会自动识别并生成对应分类 YAML，`step()` 返回结果中的 `res["intake"]["generated_files"]` 非空（首次为 `1`）；
     - 连续第二次调用 `runner.step()` 时，`res["intake"]["generated_files"]` 为 `[]`，不会重复生成需求或重复派单；
     - 全程在途任务（`in_flight_tasks`）与恢复记录（`completed_tasks`、`cursor`）保持一致，且未配置可执行 `Ready` 任务时模型调用次数为 `0`（不绕过批准/前置/租约自动派单）。
   - `test_step_isolates_corrupt_submission_without_blocking_valid_intake_or_inflight()`：
     - 同时放入一份损坏/篡改的提交或分类 YAML 与一份合法 Markdown 提交单，调用 `runner.step()`，验证合法提交单正常生成分类 YAML，坏文件被记录在 `res["intake"]["errors"]` 中，且在途任务状态推进不受影响。
2. 在 [`project-control/tools/test_work_intake.py`](file:///home/sushaohua/workspace/ai_soc_project/project-control/tools/test_work_intake.py) 中新增测试方法：
   - 验证 `WorkIntakeManager.link_tasks_to_category_yaml(TaskLinkUpdate(..., arch_breakdown={...}))` 会自动递增 `revision` 并同步更新 `.intake_digests.json`，随后的 `scan_and_sync()` 零 `TAMPERED_SAME_REVISION` 报错。

### 3.3 验收命令契约（`verification`）
```yaml
verification:
  commands:
    - id: test_coord_intake_checkpoint_wiring_and_ledger_consistency
      cwd: project-control
      command: 'python3 -m tools.coord_runner --intake-scan && python3 -m unittest tools/test_work_intake.py tools/test_coord_runner.py tools/test_coord_recovery.py tools/test_coord_systemd_service.py -v'
      expected: coord_runner --intake-scan返回0且errors为空（FEAT-20261104-001@r4与FEAT-20261104-002@r4账本摘要一致）；test_work_intake、test_coord_runner（含step/restore检查点自动收件、重复检查幂等、坏文件隔离、AST函数<=50行且<=4参门禁）、test_coord_recovery与test_coord_systemd_service（含P1-14连续空闲轮询零模型调用）全部100% OK
      availability: available
  positive_cases:
    - CoordRunner在restore_from_checkpoint与step检查点自动调用scan_work_intake，新增Markdown提交单被识别一次并生成分类YAML，重复step不重复建单或调用模型
    - TaskLinkUpdate支持关联arch_breakdown并自动递增revision同步更新.intake_digests.json；FEAT-20261104-001/002升级为revision 4后--intake-scan零错误通过
    - 在途任务(in_flight_tasks)、恢复记录与单实例锁保持一致，收件扫描不绕过ApprovalGuard批准、技术前置或LeaseManager租约
  negative_cases:
    - 单份坏文件（格式损坏或同revision篡改）被隔离在intake.errors中，不阻断其他合法提交单收件，也不破坏在途任务恢复
    - 空闲轮询或未获批准的收件项严禁触发任何大模型调用或未授权派单；严禁将代码测试通过伪造为宿主机后台systemd服务已启用运行
```
