---
confirmation_id: CONFIRM-INTAKE-P1-20261103
revision: 2
previous_revision: 1
previous_sha256: 3b92a397ef7687adcca9e808ce4fa9644a994e1289a3b5e77f05519a86c5192d
date: '2026-11-03'
demand_id: DEM-INTAKE-P1-001
task_id: PREP-INTAKE-P1-ARCH
run_id: run_02
status: pending-human-batch-approval
coord_session: 8d4e8b77-42a9-4bd3-bd5a-1b881e8d4bd5
prepared_by:
  pm_session: 4eb5c2eb-b365-45bf-b6a2-2dbf0aa86a08
  integrator_session: 25b63893-2611-41ff-87d7-0b9f82cf0375
  arch_session: de6e7ac5-adc5-4382-b0d5-442f63e175ac
consumed_inputs:
  raw_submission:
    id: SUB-20261103-001
    revision: 1
    path: ../evidence/coord_automation/phase1_prep_20261103/raw_submission_20261103_01.md
    sha256: f740af045cd3f6dc7d91bc05603849c8c12924e67c9e8e4e0eb4d7e585e944ac
  pm_understanding:
    id: PM-DEMAND-INTAKE-P1-20261103
    revision: 1
    path: ../evidence/coord_automation/phase1_prep_20261103/pm_demand_understanding_20261103.md
    sha256: fb762ed4e0075d94392d21cc96ad64de3e1f6076ac6163759fde0e74e7650a1a
  integrator_probe:
    id: PREP-INTAKE-P1-INT-VERIFY-20261103
    revision: 2
    path: ../evidence/coord_automation/phase1_prep_20261103/integrator_host_interface_verification_20261103.md
    sha256: 3e9ebb7eb0992e3517abf1d802bec1fdad4c91a4a0e6d188e54f97d47b7db6d8
  handoff_rev2:
    path: coord_intake_dispatch_phase1_handoff_20261103.md
    sha256: 400e61311c726663c8645a6237ad1084b19fb7b2d3c8b1850b4e20e59a91ab06
  design_rev2:
    path: ../architecture/coord_intake_dispatch_phase1_design_20261103.md
    sha256: 8a2984c6bb4b868cc8e2d6742873527f448f27c7006d99c5ce322207b2941350
---

# 三类人工入口自动调度第一阶段：一页确认单与实施概要（rev 2）

> **定位与升版说明**：本单由唯一 `COORD`（`8d4e8b77-42a9-4bd3-bd5a-1b881e8d4bd5`）汇总 [PM 需求理解底稿](../evidence/coord_automation/phase1_prep_20261103/pm_demand_understanding_20261103.md)（`fb762ed4...`）与 [INTEGRATOR 宿主机接口实测报告 rev 2](../evidence/coord_automation/phase1_prep_20261103/integrator_host_interface_verification_20261103.md)（`3e9ebb7e...`）形成，交 HUMAN 批量审批。`rev 2` 修正 `rev 1` 执行器误判：全角色 100% 统一使用 `/home/sushaohua/.local/bin/codex exec -m gpt-6-luna`（零模型覆盖），并通俗化实操授权说明。获批前不建 `docs/work_intake/`、不立实现卡、不装后台服务。

## 1. 原文锚定与核心原则

- **原文与基线锚定**：原始指令 [raw_submission_20261103_01.md](../evidence/coord_automation/phase1_prep_20261103/raw_submission_20261103_01.md)（`SUB-20261103-001` rev 1, SHA256 `f740af045cd3f6dc7d91bc05603849c8c12924e67c9e8e4e0eb4d7e585e944ac`）1:1 锚定稳定需求 **`DEM-INTAKE-P1-001`**（正式 ID 待程序/COORD 查重分配），绑定[交接单 rev 2](coord_intake_dispatch_phase1_handoff_20261103.md)（`400e6131...`）与[第一阶段设计 rev 2](../architecture/coord_intake_dispatch_phase1_design_20261103.md)（`8a2984c6...`）。
- **1 条指令 = 1 条稳定需求（可拆多角色工程任务）**：逐字保留用户原话与公共约束哈希，单需求维持统一用户验收目标，获批后由 `COORD` 拆解关联多张有明确仓库/路径白名单的角色卡；原文重排或局部修订仅做增量核对，不重复建需求。
- **AI 先出理解+实施概要 → 人工按准确版本批复后实施**：默认将 PM 理解与 ARCH 概要合并为单次待审批包；未绑定真实人工对准确 `(revision, sha256)` 批准前 **100% 严禁启动新增实现**（禁凭 `enabled: true`、模型自填 `approved: true` 或自然语言模糊匹配“批准”放行）。
- **人工零 YAML 负担**：人工仅提交自然语言或 MD；程序自动生成唯一主分类 YAML（`issues/`、`features/`、`requirements/` 三选一，不重复复制）、唯一编号去重及与 `.agents/kanban/` 正式任务卡的双向哈希关联，无需逐票手工转贴提示词。

## 2. 目标、三步分段范围与明确排除项

- **第一阶段目标**：在不触碰业务代码与双 Bootloader、不降级既有正式独立 QA 门禁的前提下，于 `project-control` 实证“MD 批量输入 → 1:1 稳定需求与确认包 → 准确版本人工审批防伪绑定 → 自动生成三类主分类 YAML 与关联 → 唯一 COORD 多角色真实异步派单、恢复对账与受控定时巡检”闭环。

| 分段里程碑 | 核心交付范围（逐段独立实现、独立 QA 验收通过后方可进入下一段） | 阶段准出判据与覆盖条款 |
| --- | --- | --- |
| **M1 手动单步** | 建立原文收件、确认包与版本化审批防伪绑定、唯一主分类 YAML 自动生成与关联；接入真实宿主角色执行（废除仅查 HEAD 的旧默认执行器），单命令完成拆单派发与门禁收件。 | 零手写 YAML、未批范围 100% 不开工、真实角色会话可核验；通过 `P1-01~04, 06, 11~12, 15~19`（12 项）。 |
| **M2 持续推进与恢复** | 启用外置 SQLite 单一权威恢复源；长耗时角色/QA 异步化（最多 2 卡并行推进无冲突就绪票）；闭合重扫幂等、版本演进对账、超时查重、崩溃恢复、单实例锁、租约活跃保护与 CAS 写防冲。 | 零盲重发、零双 COORD、零覆盖人工改动、零无证写 `Done`；通过 `P1-05, 07~10, 13, 20`（7 项）。 |
| **M3 定时调度** | M1/M2 均获独立 QA 接受且宿主条件登记齐备后，部署**单个** `systemd --user` 服务复用同一入口自动巡检（禁叠加 cron/timer），实现脏检查静默。 | 自动收件推进、`stop/restart` 续接在途、**无变化时模型调用严格为 0**；通过 `P1-14`（1 项）及回归。 |

- **6 大明确排除项**：
  1. **不接入 QA 自动提单**：第一阶段原始指令 100% 来自人工（HUMAN），独立 QA 自动生成 Issue 属《QA 方案 v2》第二阶段。
  2. **不接入 QA 固定轮次换版与 `buildno` 体系**：定时唤醒仅驱动开发 `COORD`，严禁重启在途 QA 或改写 QA 锁定的服务器候选。
  3. **不修改 `soc-ap/` 与 `mcu-p3/` 业务代码**：SoC 微服务、Web HMI 与 MC/TH 应用固件物理只读封锁。
  4. **不修改双 Bootloader**：`boot/bootloadermc/`、`boot/bootloaderth/` 物理只读封锁，严守首版升级不改 Bootloader 约束。
  5. **不做真实 MCU 烧录或物理硬件动作**：零操作 `/dev/ttyUSB*`、SWD 探针（`probe-rs`）、物理 U 盘及加热/运动外设。
  6. **不批量迁移历史卡，不降级正式 QA 门禁**：一切代码与演练任务仍须满足“服务器锁定候选 + 独立 Docker 容器测试 + 宿主机独立 Codex 只读审阅 + 非作者报告复核 + 必要 Owner 接受”。

## 3. 验收场景紧凑矩阵（`P1-01` ～ `P1-20` 20/20 全覆盖）

> 逐项展开详表锚定 [PM 底稿 §3](../evidence/coord_automation/phase1_prep_20261103/pm_demand_understanding_20261103.md#L106-L150)（`fb762ed4...`）与[设计 rev 2 §9](../architecture/coord_intake_dispatch_phase1_design_20261103.md#L222-L252)（`8a2984c6...`）；真实调度验收须基于实际宿主与服务器锁定候选，禁止用纯 Mock 或进程存活替代。

| 分段 | 功能配对组 | 正向通过判据（Normal / Recovery） | 负向拦截与故障隔离判据（Negative / Isolation） |
| --- | --- | --- | --- |
| **M1** | **收件与安全防错**<br>`P1-01, P1-06, P1-16` | **`P1-01`**：单 MD 含 `issue`/`feature`/`requirement` 多指令及公共约束，逐条稳映需求并自动生成唯一主分类 YAML，获准确批准后关联正式任务，零人工写 YAML。 | **`P1-06`**：同 `(id,rev)` 篡改、错 `schema_version` 或目录冲突确定性拒收且隔离坏项；**`P1-16`**：删文件/改 `disabled` 不自动撤在途，禁扩权、禁直接执行原文 shell。 |
| **M1** | **版本审批与防伪**<br>`P1-03, P1-18, P1-19` | **`P1-03`**：按架构输入拆分并真实派发已获批 `feature` 范围；**`P1-18`**：批次部分批准仅释放获准项，其余挂起不阻塞已准工作。 | **`P1-03/P1-18`**：未批子范围及“仅确认需求未批概要”项严禁启动实现；**`P1-19`**：无真实人工源、旧版套新版、模型自填 `approved:true`、`enabled:true` 或模糊“批准”字样 100% 拦截。 |
| **M1** | **拆单与根因分流**<br>`P1-17, P1-02, P1-04` | **`P1-17`**：单指令多角色协作保持唯一 `demand_id` 关联多张有界任务卡；**`P1-02`**：`requirement` 不清真实拉起 PM/ARCH 澄清；**`P1-04`**：`issue` 根因未知先只读调查、明确直派 Owner 并留痕。 | **`P1-02/P1-04/P1-17`**：澄清等待或子任务阻塞期间，其他无依赖就绪任务正常推进，不猜需求盲写代码、不强压错误模块改代码。 |
| **M1** | **真实执行与门禁**<br>`P1-15, P1-11, P1-12` | **`P1-15`**：获批小范围真实软件任务由真实工程师执行提交，经服务器锁定、Docker 沙箱、独立 Codex 审阅与非作者复核全 `APPROVED` 后收件 `Done`（待审/阻塞如实停驻）。 | **`P1-11`**：退出码 `0` 无候选/无证或 QA `REJECTED`/`BLOCKED` 拒写 `Done`（区分 2 次返工预算与环境阻塞，不堵他票）；**`P1-12`**：未推远端、缺复核/哈希失配或子 Agent 冒充 Codex 硬拒收件。 |
| **M2** | **异步与版本幂等**<br>`P1-08, P1-05, P1-07, P1-20` | **`P1-08`**：长耗时角色/QA 外置异步查询，另一无冲突就绪票真实启动并产出会话记录（非仅标题改 `InProgress`）；**`P1-20`**：原文重排/未变项不重建需求并复用原有效批准。 | **`P1-05`**：同 `(id,rev,sha256)` 重扫/重通知零新增任务与作业；**`P1-07`**：新 `rev` 遇旧版在途不静默换输入或重派，交 COORD 裁决留痕；**`P1-20`**：实质变更升新 `rev` 禁套旧批。 |
| **M2** | **对账、单主与 CAS**<br>`P1-09, P1-10, P1-13` | **`P1-09`**：派单超时或崩溃重启后，先凭 `dispatch_key` 向真实宿主对账；确认状态后无缝续接，无关就绪票继续推进。 | **`P1-09`**：无法确认“从未启动”禁盲重发（标“派单待核实”）；**`P1-10`**：双启动被锁拦截保唯一 COORD，租约过期但旧作业仍活跃禁抢占重派；**`P1-13`**：写前核对 SHA256，遇人工修改拒覆盖并留意图。 |
| **M3** | **定时巡检与静默**<br>`P1-14` | **`P1-14`**：M1/M2 通过后单后台服务无人工命令自动接收推进；`stop/start/restart` 后在途作业、恢复源与单实例锁完整续接。 | **`P1-14`**：无新输入、无版本变化、无回执、无到期动作时**模型调用次数严格为 0**；严禁仅凭 `systemctl active` 签通过，严禁定时干扰/换版在途 QA。 |

- **完整性核对**：M1（`P1-01, P1-02, P1-03, P1-04, P1-06, P1-11, P1-12, P1-15, P1-16, P1-17, P1-18, P1-19` 共 12 项）+ M2（`P1-05, P1-07, P1-08, P1-09, P1-10, P1-13, P1-20` 共 7 项）+ M3（`P1-14` 共 1 项）= **20 / 20 项全覆盖**。

## 4. 实施概要与真实宿主架构方案（融合 INTEGRATOR rev 2 实测事实）

依据 [INTEGRATOR 宿主机实测报告 rev 2](../evidence/coord_automation/phase1_prep_20261103/integrator_host_interface_verification_20261103.md)（`3e9ebb7e...`：`WSL2 6.18.33.2`，`codex-cli 0.166.0` 全局默认 `gpt-6-luna` 且 `~/.codex/state_5.sqlite` 已有 66 次 `exec` 实跑记录，本轮新建只读、`--sandbox read-only resume`、受控 `--sandbox workspace-write` 三项冒烟全 `exit 0`；`Docker 26.1.3`；`sqlite3 3.31.1`），**`COORD`、`PM`、`ARCH`、`ENG-*`、`INTEGRATOR`、`QA` 全角色 100% 统一使用 `/home/sushaohua/.local/bin/codex exec -m gpt-6-luna`，零 `model_policy.approved_overrides` 模型覆盖**（`agy` 仅作人工交互 TUI 前端，与 `coord_runner` 底层 `~/.codex/` 会话及锁零冲突）：

### 4.1 收件与机器索引结构

- 获批后启用 `project-control/docs/work_intake/{submissions,confirmations,approvals,issues,features,requirements}`（原文存意图、确认单存解释、审批存版本化人工来源、三类 YAML 存唯一主分类机器索引、`.agents/kanban/` 存正式任务生命周期）。
- 全量写入强制执行**文件级字节 SHA256 CAS 乐观锁回写**；新入口队列与旧 [coord_autorun_queue_20261029.yaml](coord_autorun_queue_20261029.yaml)（`819fed4f...`）**显式隔离**（禁止默认遍历历史 `TWIN-*` 或干扰在途 `MS-22`/`TWIN-36..40`，并补齐前置 `Done` 卡 `done_acceptance_errors` 校验）。

### 4.2 四大宿主适配接口与外置运行态契约

运行存储外置至非 Git 持久化目录 `/home/sushaohua/.local/share/ai_soc_coord_runner/state.sqlite3`（WAL 事务，确立与既有阶段状态机衔接的**唯一权威恢复源**）：

1. **单写排他锁与唯一 COORD 血缘衔接**：`coord_runner` 启动获取 `coord_runner.lock` 内核锁 `fcntl.flock(LOCK_EX | LOCK_NB)` 防双实例；在 SQLite 记录来源交互会话 `8d4e8b77-42a9-4bd3-bd5a-1b881e8d4bd5` 血缘并维护唯一受控 `active_coord_thread_id`，与人工 `agy` TUI `presence/*.lock` 零锁冲突，辅以写前 SHA256 CAS 防人工并发改卡被覆盖。
2. **`coordinate(request)`（空闲零调用短路 + 只读线程延续）**：先对比输入/审批/回执/到期动作摘要，**无变化直接短路 `NOOP`（0 次模型调用）**；有变化时调 `codex exec --skip-git-repo-check --sandbox read-only -c 'approval_policy="never"' -m gpt-6-luna --json --output-schema`（后续轮次执行 `codex exec --sandbox read-only resume <active_coord_thread_id> ...`，`--sandbox read-only` 置于 `resume` 前物理锁死只读），程序硬校验 `revision`、`approval_refs` 与路径白名单。
3. **`submit_role_task(request, dispatch_key)`**：替代仅查 `git rev-parse HEAD` 的旧 `default_agent_executor`；派发前在 `state.sqlite3` 预写唯一 `dispatch_key` WAL 意图并在 `prompt.txt` 首行固定嵌入 `[COORD_DISPATCH_KEY:<dispatch_key>]`，由独立会话包装器异步派生 `codex exec -m gpt-6-luna --json --output-schema -o <job_dir>/final.json`：`PM`/`ARCH` 用 `--sandbox read-only`；获批 `ENG-*`/`INTEGRATOR` 新建独立线程用 `--sandbox workspace-write -C <target_repo>`（原生保护 `.git`/`.agents` 只读，控制器审计 `allowed_paths` 后受控提交推送远端）；正式独立 QA 与非作者报告复核复用 `Docker 26.1.3`（`qa_runner.py`）+ **全新独立 `thread_id`** 的 `codex exec --sandbox read-only -m gpt-6-luna`（强制校验作者、QA、报告复核三方 `thread_id` 互异隔离），全部异步外置解除主循环阻塞。
4. **`query_role_job` & `collect_role_result`（五源对账闭合 `LAUNCH_UNKNOWN`）**：联合核对 ① `state.sqlite3` `role_jobs` WAL、② `/proc/<pid>/stat` 第 22 字段 `starttime`（防 PID 回绕）、③ `<job_dir>/codex_events.jsonl`（`thread_id`/`usage`）、④ 只读 `~/.codex/state_5.sqlite`（会话启动瞬间即落盘 `first_user_message`）与 `~/.codex/sessions/.../rollout-*-<thread_id>.jsonl`（核验 `turn_context.model == 'gpt-6-luna'`）、⑤ 原子 `<job_dir>/exit_status.json`。超时或 `SIGKILL` 未写 `pid.json` 时，按 `first_user_message LIKE '[COORD_DISPATCH_KEY:<key>]%'` 只读查询 `state_5.sqlite` 找回或证伪线程，无法确认“从未启动”标 `RECONCILE_REQUIRED` 禁盲重发；退出码 `0` 仍须核验 `actual_model == 'gpt-6-luna'`、远端 40 位 commit 与物证齐备方可转正式 QA。

### 4.3 获批后拟拆解正式工程任务序列

默认实施仓为 `project-control`；`tools/coord_runner/` 共享路径由单 Owner `INTEGRATOR` 主控，按路径/依赖受控串并行；新增 Python 自研函数严格遵守 **$\le 50$ 行、$\le 4$ 个入参**硬门禁：

| 拟定任务 ID | 阶段 | 主责 / 独立审阅 | 前置依赖 | 交付焦点与白名单边界 |
| --- | --- | --- | --- | --- |
| **`AUTO-03`** | M1 收件层 | `INTEGRATOR` / 独立 `QA`+`ARCH` | `AUTO-02` | `work_intake` 原文解析、稳定需求映射、唯一主分类 YAML 生成、版本化人工审批防伪绑定与 CAS 回写。 |
| **`AUTO-04`** | M1 派发+M2 恢复 | `INTEGRATOR` / 独立 `QA`+`ARCH` | `AUTO-03` | 全角色 `codex exec -m gpt-6-luna` + `Docker` 异步作业适配、外置 `state.sqlite3` 单一恢复源、`flock` 单实例锁与五源对账防重控制器。 |
| **`AUTO-05`** | M1/M2 独立验收 | 独立 `QA` / 非作者 `ARCH` | `AUTO-04` | 服务器锁定候选独立 Docker 沙箱与宿主实景端到端验收，闭环验证 `P1-01~13, 15~20`。 |
| **`AUTO-06`** | M3 服务与验收 | `INTEGRATOR` / 独立 `QA`+`ARCH` | `AUTO-05` | M1/M2 接受后部署单实例 `systemd --user` 定时服务（保护既有 `sync_md.sh` crontab），完成零空耗与重启恢复 `P1-14` 验收。 |

## 5. 已有有效批准直接引用与存量保护

- **直接复用既有有效授权（免重复索批）**：直接引用 `SUB-20261103-001` rev 1（`f740af04...`，输入/审批总原则、三步顺序、排除边界与技术细节团队闭环）、[delivery_and_coord_gate.md](../../.agents/rules/delivery_and_coord_gate.md) rev 5（`c48f91e6...`，唯一 COORD 代码只读封锁、服务器候选正式门禁及受控任务内常规 Git 提交/推送授权复用）、[codex_qa_review.md](../../.agents/rules/codex_qa_review.md)（`b7dfa803...`）与[总控清单](coord_autorun_tasklist_20261029.md) rev 1（`f42dec02...`，独立 Codex `gpt-6-luna` 审阅、最多 2 卡并行、同票最多 2 次返工预算）及 [bootloader_role_boundaries.md](../../.agents/rules/bootloader_role_boundaries.md) rev 1（`c688f16a...`，双 Bootloader 角色与 `soc_debug` 隔离边界）。
- **存量成果与本地未提交增量物理保护**：
  1. 原封保留 `AUTO-01`（`38064f1f...`）与 `AUTO-02`（`0a3b1a4c...`, `run_13` 已批软件基线）原卡 `Done` 与历史签署，不重开、不夸大既有范围。
  2. 原封保留 `ISSUE-20261102-01~06` 已闭环文档/证据/提交（`soc-ap=427dd6d8...`, `mcu-p3=e051111e...`, `test_harness=ccf1476a...`），以及在途卡 `MS-22`（`Verify`）、`TWIN-36..40`（`Review`）和旧队列 `TWIN-15..12` 待对账状态。
  3. **严禁 `git checkout --` / `git reset --hard` / `git clean`**，完整保护 `workspace`、`project-control`（本地未提交规则/规划修改及未跟踪设计/交接/确认单/证据增量）与 `boot/*` 本机软链接（进入 M1 正式 QA 前由 `INTEGRATOR` 按单逻辑审阅固化已定稿规则/设计服务器基线）。

## 6. 待决事项与批量审批确认表

- **普通技术细节 100% 团队内部闭环（不打扰 HUMAN）**：Markdown/YAML Schema 与编号序列规则、`state.sqlite3` 表结构与既有 checkpoint 单一恢复源衔接、`dispatch_key` 五源对账与 CAS 冲突日志细节、`tools/coord_runner/` 单 Owner 排期与 $\le 50$ 行/$\le 4$ 参 AST 门禁、容器故障注入夹具及 `project-control` 定稿基线受控同步。
- **提请 HUMAN 批量审批的 2 个通俗勾选项**（支持**整批批准**、**部分批准**或**“仅确认需求、方案继续讨论”**；批复后由唯一 COORD 绑定本单 `CONFIRM-INTAKE-P1-20261103` rev 2 准确哈希登记生效）：

| 勾选 | 审批项编号与主题 | 具体待批内容与通俗说明 |
| --- | --- | --- |
| `[ ]` | **① 确认单主体与三步分段实施放行** | 批准本确认单 `CONFIRM-INTAKE-P1-20261103` `rev 2`（需求 `DEM-INTAKE-P1-001`）的目标、M1→M2→M3 分段范围、6 大排除项、`P1-01~20` 验收场景及 `AUTO-03~06` 实施概要（全角色统一使用 `codex exec -m gpt-6-luna`，无需任何模型覆盖），授权拆单实施。（若选“仅确认需求、方案继续讨论”，则仅锁定 §1～§3 需求边界，暂不启动代码实现。） |
| `[ ]` | **② 验收演练与第 3 步后台保活两项实操授权** | **(a) 跑一次安全的“全流程真枪实弹演习”（对应 `P1-15`）**：因为第一阶段严禁触碰 `soc-ap`/`mcu-p3`/`boot/*` 业务代码和真实硬件，但验收又要求不能只跑假模拟，必须真让 AI 工程师接单写一个小改动、推送到服务器、过 Docker 测试和独立 QA 审完收件——所以申请允许只在 `project-control` 文档/辅助小脚本范围内出 1～2 道无害的“演习小题”，把整条自动流水线真跑通一遍；<br>**(b) 第 3 步开启 Linux 用户后台常驻开关（`sudo loginctl enable-linger sushaohua`）**：Linux 默认在您关掉 SSH/终端窗口退出登录时，顺手把您名下的后台服务全关掉；开启这个开关只是为了让第 3 步的定时调度服务在您关掉终端窗口后还能继续在后台自动巡检（但若整个 Windows 电脑睡眠或 WSL2 虚拟机被系统彻底挂起休眠，服务会随虚拟机一起暂停，唤醒后自动恢复）。 |
