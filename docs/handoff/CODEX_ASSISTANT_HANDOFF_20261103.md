---
title: Codex 助理交接：2026-11-03 讨论、执行状态与明日起步
revision: 1
date: 2026-11-03
timezone: Asia/Shanghai
observed_at: '2026-11-03T17:58:44+08:00'
intended_resume_date: 2026-11-04
status: assistant-handoff-not-execution-authorization
---

# Codex 助理交接

## 1. 明天先做什么

**先只读核实 COORD 和相关作业的最新状态，落实流程切换窗口；随后按明确授权简化 QA 门禁，再推进 Debug、921600 两项需求，最后执行独立真实环境验收。**

不要重讲整套方案或重新询问已确认的四项 QA 选择。先给用户一张简短状态表：在途任务、实际后台作业、写入占用、剩余条件和下一动作。本文是本地观察与会话交接，不能替代当前任务卡、服务器候选或新的执行授权。

用户明日可直接输入：

> 你继续作为我的 Codex 助理。读取 project-control/docs/handoff/CODEX_ASSISTANT_HANDOFF_20261103.md，先只读核查最新状态、COORD 停机交接和流程切换条件，简短汇报；保留既有成果，不自动启动开发或测试。

## 2. 助理身份、工作区与权限

- 用户是项目负责人。当前会话默认是**只读助理和架构建议者**，不是开发 COORD，不接管现有 Agent。已明确授权的本轮工作是需求/流程/交接文档编写和状态核查。
- 不把“如果让你改”“等 COORD 停了再改”等讨论自动当作代码修改、执行测试、暂停会话、部署、烧录、提交或推送授权。后续用户明确授权后按范围执行，已有有效授权不重复索要。
- 根目录：`/home/sushaohua/workspace/ai_soc_project`。`project-control/.agents/` 是规则原件；根 `.agents/` 为镜像。根 `AGENTS.md` 及目标仓本地规则仍须遵循，本文不覆盖现行门禁。
- 根仓与六个子 Git 仓独立；业务仓为 `soc-ap`、`mcu-p3`、`test_harness`，另有两个 `boot/` 仓。根 Git 操作使用 `bash tools/workspace_git.sh ...`，各子仓分别处理。
- 工作区有用户及其他 Agent 的在途/未提交改动。先核对差异与归属，禁止覆盖、批量清理、顺手合并提交或修改正式任务状态。实际会话/运行身份必须重新核实，历史 ID 不证明当前仍活跃。
- 本文及今日 QA 文档只完成作者文档检查，不是正式独立 QA 签署。没有执行的构建、测试、硬件动作须明确未执行。

## 3. 今日讨论和落地概览

| 事项 | 已完成/已确认 | 未完成/需继续 |
| --- | --- | --- |
| ENG_BOOT_MC / ENG_BOOT_TH | 角色与仓库边界、本机规则使用方式已整理；两仓本地 `soc_debug` 已建立、设置 upstream，并在前序操作中推送 | 首个开发目标稍后由 ARCH 分配；本轮未开发 Boot；部分角色规则和交接文档未提交 |
| 三类人工入口 | 人提交指令/MD；一条指令一个稳定需求，可拆多角色任务；AI 整理理解/概要，准确版本审批后实施；分类 YAML 由程序维护 | 单步、持续恢复、定时常驻分别验收，不能仅凭文档或代码声称整套自动化已部署 |
| 新需求一：MC/TH Debug | 原文及需求确认单 rev 1 已生成，目标是两路调试串口＋用户 UI 的双向链路对账 | 尚未查到这两项新需求的正式 intake/任务关联和实现交付；由 COORD 查重收件并安排概要 |
| 新需求二：921600 | VMware/AP↔MC 业务 UART 统一到 921600 的需求确认单 rev 1 已生成 | 两端配套实现、升级兼容和真实验收待执行；不自动改变 MC↔TH 或调试 UART |
| 独立 QA 闭环 | 主流程、27 个基础测试规格组、delta、Issue 模板、四张已回答问题卡及 COORD 提示词已形成 | 工具/环境、buildno 制品链、QA 自动发现收件适配、浏览器/HIL 运行尚未落实为本专项实际验收 |
| QA 简化 | 用户明确希望减少门禁，重点是代码符合要求、满足功能需求、Bug 少；已讨论修改范围及切换顺序 | 规则、Runner 和检查器尚未改成简化流程；相关正式实施与切换待处理 |
| 停机交接 | 已给用户一段发给 COORD 的准备切换提示词 | 未取得实际停机/无相关写入/检查点完整的核验结论；不能假定用户已发送提示词 |

Boot 仓分别为 `boot/bootloadermc`、`boot/bootloaderth`，仅允许 `soc_debug` 开发，不能在 main 开发。各自 `AGENTS.md`、`.agents`、`docs` 是本机未入 Git 的软链接，用户已选择**暂时仅本机使用**，不迁移或上传这些规则。详见 [Boot 角色交接](../planning/bootloader_role_onboarding_20261103.md)。

## 4. 自动调度任务的最新观察

以下按 17:58 本地任务卡观察，明日必须重新核对。COORD 在今日讨论期间持续提交和更新，状态可能继续变化。

| 任务 | 观察状态 | 候选及证据线索 |
| --- | --- | --- |
| [AUTO-03](../../.agents/kanban/microtasks/coord_automation/AUTO-03.md) M1 手动单步 | Done | 候选 `4411a1d72643c8153587c1bc814f84b5ee04c74a`；`run_04` QA 和 ARCH 报告记录 APPROVED |
| [AUTO-04](../../.agents/kanban/microtasks/coord_automation/AUTO-04.md) M2 异步推进与恢复 | Done | 候选 `4c58c46be12af0e4dcfc4ef6f40dd162c5b18c06`；`run_02` QA 和 ARCH 报告记录 APPROVED |
| [AUTO-05](../../.agents/kanban/microtasks/coord_automation/AUTO-05.md) M1/M2 综合验收 | InProgress | 最新卡面候选 `8a203cadab38a3f1233c27090321dc77b2fcfa75`；存在早期 REJECTED 和后续返修，尚未观察到最终收件 |
| [AUTO-06](../../.agents/kanban/microtasks/coord_automation/AUTO-06.md) M3 定时服务 | Backlog | 候选为空，未完成常驻部署验收 |

最后观察 `project-control` HEAD 为 `ec300ef`，标题 `chore(kanban): update AUTO-05 candidate_commit to 8a203ca`。这里只是本地观察，不是服务器正式锁。

此前给用户解释过 AUTO-03 `run_01` 的 BLOCKED；**后续 `run_04` 已记录通过，不能沿用早期阻塞结论描述现在的 AUTO-03。**同样不能用早期 AUTO-04 REJECTED 覆盖后续 `run_02`。这次助理核查未重新执行测试或完整审计这些接受。

三类入口原专项已有 `APPR-20261103-001` 对确认单 rev 2 的“全部批准”记录，不能因确认单旧头部仍写 pending 就要求用户重新批整个专项。批准范围明确排除了 QA 自动 Issue、buildno/HIL 及业务/Boot 改动；新专项不能套用该批准扩大执行范围。

## 5. QA 简化：方向与最小修改范围

拟采用普通任务默认流程：

**作者实现与自检 → 锁定候选 → 一轮独立 QA（代码 Review＋功能/回归测试）→ COORD 收件。**

保留需求验收、Diff 及必要上下文的代码审查、相关异常/恢复、必要基础回归、硬件功能真实 HIL、作者与独立 QA 分离，以及准确候选/结果的机器校验。取消普通任务默认重复 Docker 测试、重复 ARCH 审查和逐份 QA 报告二次复核；跨模块契约、协议、升级/硬件安全等特殊变更按开工时明确范围追加审查。QA 自编工具/预期仍需有效非作者检查，不允许自证替代独立性。

审批防伪、去重、崩溃恢复、CAS、异步并发属于**调度器自身功能需求**；涉及这些能力的任务仍验收，不将其每次重复加到无关业务任务上，也不因减少流程删除真实可靠性要求。

**当前旧门禁仍生效。**核查到需同步处理的层面：

1. 权威规则：根 `AGENTS.md`；`.agents/rules/codex_qa_review.md`、`delivery_and_coord_gate.md`，以及公共协议/Issue 规则中相关强制复核条款。
2. 执行代码：`tools/coord_runner/runner.py` 的 `_ensure_qa_report_review()` 和审查阶段；复用同一候选的有效沙箱事实，不重复运行相同测试。
3. 收件检查：`tools/coord_runner/state_machine.py`、`tools/delivery_checks.py`；`tools/check_task_graph.py` 引用后者。只改 Runner 会留下收件冲突。
4. 任务/角色/QA 模板、未完成任务明确迁移记录、相应测试和当前流程文档。历史 Done、报告及签署原样保留，不批量删除 Reviewer。

实现应尽量统一一处审查策略，供调度和校验共用。`scheduler.py` 主要选任务，不是唯一修改点；此次只做有界 QA 流程简化，不扩大为整套自动调度重写。

需注意：今日生成的独立 QA 流程仍引用当时有效的报告非作者复核要求，正式切换时同步修订；不能将这些旧条款无条件带入新流程。提出简化方案不等于已经发布新规则或允许旧卡直接跳过当前门禁。

## 6. 两项产品需求的交接

- [MC/TH Debug 需求 rev 1](../planning/mc_th_debug_mode_requirement_confirmation_20261103.md)：用户原文“TF”按同句上下文暂理解为 TH。记录两板实际收发、处理结果/状态及 MC 中继，区分接收、ACK、执行完成。日志不能阻塞业务；丢失/截断必须显式可见，不能用缺日志证明设备未收到。默认不改 Bootloader、不新增 UI 控制页；启停/关联/资源预算由 ARCH 与 Owner 核实。
- [VMware–MC 921600 需求 rev 1](../planning/vmware_mc_921600_requirement_confirmation_20261103.md)：明确两端配置、USB/驱动/透传及 MCU 能力，运行/升级模式兼容；不全局替换所有 115200。ENG-FWD、ENG-MC、INTEGRATOR 按边界实施。

原计划为两项合并提交简短实施概要供用户一次确认，已有有效批准直接引用，再拆多角色任务。用户数值和目标不重复询问。今日最后建议为**先落实切换窗口并简化流程，再按新流程实施两项需求**；只读调查和方案准备可先行，未开的业务实现不必先走完旧流程。

## 7. 独立 QA 闭环与已回答问题

用户已在当前对话逐项回答，准确选择如下：

| 问题 | 用户确认 |
| --- | --- |
| VMware 环境 | C：使用现有 VMware，划定 QA 独占窗口并冻结快照 |
| 首轮时机 | B：等待 Debug、921600 两项功能交付，再进行首次完整验收 |
| 物理台架 | A：已有 MC、TH 和完整机械/传感器，可安排受控运动测试 |
| 固件部署 | A：自动生成制品和烧录计划，授权人员确认并烧录，随后自动测试 |

实际 VM/账户/窗口、串口和 ST-Link 唯一身份、时钟/限位、工具链等由团队核实，别把工程细节全转问用户。0% 加热不代表电机不动，不授权解除保护或实加热；VM 快照也不恢复 MCU Flash 和机械现场。

资料入口：

- [QA 主流程](../planning/independent_qa_vmware_execution_flow_20261103.md)：服务器独立拉取各仓准确 commit，Docker 编译 AP/UI、MC、TH，封存带 `release_series + buildno` 的测试组合；人工烧录后在 VMware＋真机通过 Chrome 执行黑盒验收。
- [base/delta 草案](../planning/qa_web_hmi_basecases_20261103.md)：参考[用户手册](../guides/web_hmi_user_manual_and_workflow_guide.md)形成 27 个基础规格组及 Debug/921600/组合 delta；它们仍需接受并展开脚本，不是 27 项已跑通过。
- [四张问题卡及原选项](../planning/qa_environment_decision_cards_20261103.md)：已答，不重复提问。
- [QA Issue 模板](../guides/templates/qa_blackbox_issue_template.md)：需求/用例、复现、预期/实际、候选/buildno、环境与证据、收件回执及修复复验映射。

黑盒预期优先来自已接受功能需求。手册与门禁存在待澄清项，如断线 CPU ≤1% 与现行 ≤2%、重连期限、匀速进度描述与硬件执行依据；不凭实现输出反推正确答案。发现问题立即输出给 COORD，其他独立用例继续；根因未知可提交。

**接入缺口**：第一阶段 MD 收件器要求 HUMAN，QA 自动发现不能伪装成人。QA→COORD 的真实接收适配、幂等和回执需要另行落实；仅写 Issue 文件不代表已收件。

QA 一轮固定候选，通知随时入队；到本轮结束、空闲或整轮阻塞且无独立例可测、现场可交接时再换版并新建 run。`buildno >= 修复提供编号` 且实际包含有效修复/依赖，只是复验资格，实测通过后才能关闭。软件/HIL/UI 人工执行范围分别记录。

## 8. 切换、提交与明日交付

建议请现有 COORD：暂停领取新任务；让相关已启动动作完成有界步骤；保存候选、原始证据、检查点与未提交修改；只剩复核的任务保留待审；汇总真实后台作业及写入占用。**停 COORD 主会话不等于子 Agent 或后台 QA 已停止。**不必为此中断无关独立工作，也不要求先跑完 AUTO-06 或整个旧队列。

切换窗口核实后，取得明确实施授权，再完成有界规则/代码/检查器同步修改及适用验证，交独立 QA 审查该变更；避免用刚改的门禁自批。恢复 COORD 时明确生效版本和未完成任务的衔接方式。

今日自动调度代码已有多次提交；Boot 角色规则、两项需求和 QA 流程/模板等仍有未提交/未跟踪文件，尚未整体提交推送。明日重新检查各仓状态和文件归属；未经审阅不顺带提交他人改动，本文也不新增推送授权。

明日首轮助理交付应很短：**最新 AUTO-05/06 状态、是否实际停稳、未提交改动归属、可执行的最小下一步及真正需要用户决定的事项。**其他内容沿本文继续，不从头再讨论。
