# 首版可验收需求分解与任务卡规划收件记录

- **状态**：需求分解与新增 4 张首版微任务卡通过独立 QA 审查与非作者 ARCH 复核，COORD 正式收件。
- **日期**：2026-10-29
- **收件人**：COORD

## 1. 交付物汇总与核查

| 交付文件 | 类型 | 核心内容 | 关联工作包 / 角色 |
| :--- | :--- | :--- | :--- |
| `docs/planning/product/first_release_requirements_and_task_decomposition_20261029.md` | 规范文档 | 首版 5 大必做能力与 7 项子范围的可验收需求、接口定义、MC/TH 对账及门禁标准 | ARCH 牵头，MC/TH 及各软件角色参与 |
| `.agents/kanban/microtasks/vmware_soc_twin/TWIN-17.md` | 任务卡 | 本地离线作业引擎与基础混色执行规划 (COL-001) | `TASK-011` / `ENG-STATE` (协力 `JOB`) |
| `.agents/kanban/microtasks/vmware_soc_twin/TWIN-18.md` | 任务卡 | 双MCU运动/调平/断料状态接口调查与协议对账 (MOT-001, MOT-002, COL-007) | `TASK-002` / `ENG-MC` (协力 `ENG-TH`, `ARCH`) |
| `.agents/kanban/microtasks/vmware_soc_twin/TWIN-19.md` | 任务卡 | 全机HMS错误码体系、双级急停联动与脱敏诊断导出 (SAF-001, SAF-002, SAF-005, MFG-003) | `TASK-008` / `ENG-STATE` (协力 `ENG-FWD`, `INTEGRATOR`) |
| `.agents/kanban/microtasks/vmware_soc_twin/TWIN-20.md` | 任务卡 | HMI料槽映射、新机检查引导、国际化与局域网发现 (HMI-003, HMI-004, HMI-005, NET-001) | `TASK-009` / `ENG-UI` (协力 `ENG-NET`, `ENG-STATE`) |
| `docs/planning/work_packages/TASK-011_...` 等 4 份工作包 | 父节点 | `child_tasks` 1:1 对称绑定 | 各主工作包 |
| `docs/planning/vmware_soc_twin_task_execution_20261029.md` | 执行总表 | 纳入 TWIN-17~20 执行流与依赖图 | COORD |
| `.agents/kanban/KANBAN.md` | 看板 | TWIN 增至 20 张 (19 Backlog, 1 Done)，有效卡总计 106 张 | COORD |
| `docs/planning/coord_autorun_queue_20261029.yaml` | 执行队列 | 纳入 TWIN-17~20 排序 | COORD |

## 2. 静态与依赖门禁结果

- `PYTHONDONTWRITEBYTECODE=1 python3 project-control/tools/check_task_graph.py --workspace .`
  - Canonical Tasks: 108
  - Microtasks: 66
  - Errors: 0
  - Dependency Cycles: 0
  - Exit Code: 0
- `PYTHONDONTWRITEBYTECODE=1 python3 project-control/tools/coord_queue.py --workspace .`
  - Queue next: `TWIN-02`

## 3. 独立审查与复核结论

- `qa_review_report.md`：独立 QA（`gpt-6-luna` 规则核查）签发 `APPROVED`；
- `arch_review_report.md`：非作者 ARCH 复核签发 `APPROVED`；
- COORD 正式签署收件，解除对首版范围与任务卡的未决状态。
