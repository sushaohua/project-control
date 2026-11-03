---
receipt_id: COORD-PREP-RECEIPT-INTAKE-P1-20261103
revision: 2
previous_revision: 1
previous_sha256: 9143af68c502ad8210d93d3551117a8eb74ed344c82cf4e0a11061336e6c3f8a
date: '2026-11-03'
coord_session: 8d4e8b77-42a9-4bd3-bd5a-1b881e8d4bd5
demand_id: DEM-INTAKE-P1-001
confirmation_id: CONFIRM-INTAKE-P1-20261103
confirmation_revision: 2
confirmation_sha256: 63c1225d60c377a662bebaa0328f9bc95c19daccaa61d9f2766bc989f06f3f98
model_overrides_required: false
status: awaiting-human-batch-approval
---

# COORD 收件台账：三类人工入口自动调度第一阶段前置确认包（rev 2）

## 1. 真实角色执行与产物哈希绑定

| 角色 / 任务 | 真实会话 ID (`conversationId`) | 产物路径（相对 `project-control/`） | 版本 | 磁盘重算 SHA256 |
| --- | --- | --- | --- | --- |
| `COORD` 原文归档 | `8d4e8b77-42a9-4bd3-bd5a-1b881e8d4bd5` | `docs/evidence/coord_automation/phase1_prep_20261103/raw_submission_20261103_01.md` | `rev 1` (`SUB-20261103-001`) | `f740af045cd3f6dc7d91bc05603849c8c12924e67c9e8e4e0eb4d7e585e944ac` |
| `PM` (`PREP-INTAKE-P1-PM`) | `4eb5c2eb-b365-45bf-b6a2-2dbf0aa86a08` | `docs/evidence/coord_automation/phase1_prep_20261103/pm_demand_understanding_20261103.md` | `rev 1` (`PM-DEMAND-INTAKE-P1-20261103`) | `fb762ed4e0075d94392d21cc96ad64de3e1f6076ac6163759fde0e74e7650a1a` |
| `INTEGRATOR` (`PREP-INTAKE-P1-INT` / `run_02`) | `25b63893-2611-41ff-87d7-0b9f82cf0375` | `docs/evidence/coord_automation/phase1_prep_20261103/integrator_host_interface_verification_20261103.md` | `rev 2` (`PREP-INTAKE-P1-INT-VERIFY-20261103`) | `3e9ebb7eb0992e3517abf1d802bec1fdad4c91a4a0e6d188e54f97d47b7db6d8` |
| `ARCH` (`PREP-INTAKE-P1-ARCH` / `run_02`) | `de6e7ac5-adc5-4382-b0d5-442f63e175ac` | `docs/planning/coord_intake_dispatch_phase1_confirmation_20261103.md` | `rev 2` (`CONFIRM-INTAKE-P1-20261103`) | `63c1225d60c377a662bebaa0328f9bc95c19daccaa61d9f2766bc989f06f3f98` |

## 2. `rev 2` 修正记录

- 修正 `rev 1` 将后台角色 CLI 误绑定至 `agy -p` 的错误：经宿主机历史溯源与 3 组 CLI 冒烟实测，确认 `COORD`、`PM`、`ARCH`、`ENG-*`、`INTEGRATOR`、`QA` 全角色均可直接通过 `/home/sushaohua/.local/bin/codex exec -m gpt-6-luna` 统一调用（`model_overrides_required: false`，零模型覆盖）。
- 删除确认单原第 ② 项模型覆盖申请，并将验收演练与第 3 步 `enable-linger` 授权说明改为通俗中文表述。

## 3. 代码库只读与存量保护核验结果

- 业务代码与双 Bootloader 仓库零写入：`soc-ap`、`mcu-p3`、`test_harness` 干净，`boot/bootloadermc`、`boot/bootloaderth` 仅保留既有本机未跟踪软链接。
- 静态任务图门禁：`python3 project-control/tools/check_task_graph.py` 退出码 `0`（`errors: []`）。
- 获批前保护边界：尚未创建 `project-control/docs/work_intake/`，尚未新建 `AUTO-03`～`AUTO-06` 正式任务卡，尚未修改 `tools/coord_runner/` 代码，尚未配置任何定时服务。
