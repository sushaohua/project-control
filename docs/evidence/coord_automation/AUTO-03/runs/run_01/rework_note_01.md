# AUTO-03 Rework Note 01

## 1. 缺陷信息 (Defect Information)
- **Defect ID**: `QA-AUTO03-R3-01`
- **Associated Run**: `run_03` (QA Review Session: `01a1a048-0ecd-7660-9ecc-93d1432c3b16`)
- **Review Decision**: `REJECTED`
- **Rejection Basis**: 候选相对基线的差异中包含 12 项不在任务卡 `allowed_paths`/`write_scope` 白名单内的文件。

## 2. 根因分析 (Root Cause Analysis)
任务卡 `project-control/.agents/kanban/microtasks/coord_automation/AUTO-03.md` 中原配置的开工基线与 `base_commit` 错误地指向了规划前的初始提交 `b4af2d32601a07d448ac8d67a07c57f5b9ab36ac`（pre-planning commit），而非已批准的第一阶段规划与任务卡落仓基线提交 `b7a0a706b9d5683c69989faa4e6d4f6007826915`（Commit B: Phase 1 Planning & Task Cards Baseline）。

导致 QA 在比对 `b4af2d32601a07d448ac8d67a07c57f5b9ab36ac..HEAD` 时，差异中混入了由前置提交 `b7a0a706` 合入的 12 个第一阶段规划、架构设计与任务卡文件：
- `.agents/kanban/microtasks/coord_automation/AUTO-03.md`
- `.agents/kanban/microtasks/coord_automation/AUTO-04.md`
- `.agents/kanban/microtasks/coord_automation/AUTO-05.md`
- `.agents/kanban/microtasks/coord_automation/AUTO-06.md`
- `docs/architecture/coord_intake_dispatch_phase1_design_20261103.md`
- `docs/evidence/coord_automation/phase1_prep_20261103/coord_prep_receipt_20261103.md`
- `docs/evidence/coord_automation/phase1_prep_20261103/integrator_host_interface_verification_20261103.md`
- `docs/evidence/coord_automation/phase1_prep_20261103/pm_demand_understanding_20261103.md`
- `docs/evidence/coord_automation/phase1_prep_20261103/raw_submission_20261103_01.md`
- `docs/planning/coord_intake_dispatch_phase1_confirmation_20261103.md`
- `docs/planning/coord_intake_dispatch_phase1_handoff_20261103.md`
- `docs/planning/work_packages/TASK-010_验收首个多 Agent 端到端试点.md`

## 3. 修复措施与范围核验 (Fix & Scope Verification)
1. **基线对齐**：
   在 `project-control/.agents/kanban/microtasks/coord_automation/AUTO-03.md` 中将 `base_commit`、`source_baseline.project-control` 及 `dispatch_binding.source_commit` 对齐至第一阶段规划已批准基线 `b7a0a706b9d5683c69989faa4e6d4f6007826915`。
2. **范围门禁重核**：
   以 `b7a0a706b9d5683c69989faa4e6d4f6007826915` 为基准核验变更范围：
   `git diff --name-only b7a0a706b9d5683c69989faa4e6d4f6007826915..HEAD` 包含确切 46 个文件。经比对，100% 均严格落在 `AUTO-03.md` 的 `allowed_paths` 白名单定义内：
   - `project-control/tools/coord_runner/**` (11 个文件)
   - `project-control/config/coord_runner/**` (1 个文件)
   - `project-control/tools/coord_queue.py` (1 个文件)
   - `project-control/tools/test_work_intake.py` (1 个文件)
   - `project-control/tools/test_coord_runner.py` (1 个文件)
   - `project-control/docs/work_intake/**` (6 个文件)
   - `project-control/docs/evidence/coord_automation/AUTO-03/**` (25 个文件)
3. **零业务仓库触碰**：
   `soc-ap/`、`mcu-p3/`、`test_harness/`、`boot/bootloadermc/`、`boot/bootloaderth/` 保持零变更。
4. **功能测试与规范自检**：
   所有单元测试（`test_work_intake.py` 15 项、`test_coord_runner.py` 74 项）、回归测试、真实宿主演练物证及 AST 规范（230 个函数 0 违规）均保持 100% 通过。
