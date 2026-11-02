---
name: coord-task-handoff
description: Prepare a task-specific dispatch handoff for COORD in the AI SoC workspace. Use when COORD needs to assemble or check a task assignment, its inputs, scope, readiness and acceptance; do not dispatch agents or change task state as part of this skill.
---

# COORD 派单准备

为指定任务准备可核对的派单草稿，供现有 COORD 使用。此 skill 只读取和整理，不启动或中断 Agent，不修改任务卡、看板、租约、源码或证据，不推送，也不代替 COORD 判定 Ready、派单或收件。

## 读取依据

从工作区根目录定位 `project-control/`，以其 `.agents/` 为权威。先读取当前任务卡的完整内容、相关运行记录和实际输入；再按需读取以下当前原件，而不是沿用本文中的规则快照：

- `project-control/.agents/rules/delivery_and_coord_gate.md` 和 `project-control/docs/planning/coord_autorun_tasklist_20261029.md`。
- `project-control/.agents/rules/templates/角色任务提示词.md`、`任务卡模板.md` 和任务卡引用的具体规则、契约及前置接受证据。
- 涉及独立 QA 时读取 `project-control/.agents/rules/codex_qa_review.md`；涉及代码时读取对应仓库指南及适用编码标准。

若未指定任务，依据 COORD 提供的上下文和实际队列提出候选；不把队列顺序或卡面状态单独当作派单授权。仅在必要时运行现有只读检查命令，说明其适用范围和实际结果；检查器不能证明服务器、会话或沙箱的真实性。

## 整理与交付

按实际任务和现行模板生成简洁派单草稿，包含：

1. 任务 ID、revision、目标、阶段及来源；本轮角色、实际执行者和 COORD 接收入口。未落实的会话标为待落实，计划别名不能冒充实际会话。
2. 已接受的前置产物、准确版本和接受依据；区分实际核实、文档记录和未知。调查任务与实现任务按现行规则分别处理。
3. 工作区、允许写入的仓库和路径、不可改动范围、资源及租约、授权、检查点和预算；未确认事项列出缺口，不自行补造。
4. 交付物、可执行的验证命令或步骤、正常及相关异常判据、证据级别、必需检查角色与反馈入口；尚未产生的候选和 QA 结果标为后续交付，不作为开工前既成事实。
5. 必要的服务器候选、独立沙箱、独立 Codex 审查、报告非作者复核及 COORD 收件要求，按当前权威规则和任务适用范围引用。

最后单列阻碍派单的缺口、需要 COORD 核实的事项及其来源。存在冲突时指出冲突和权威依据，不擅自改写历史记录或判定正式状态。草稿只发给当前请求者；后续派单和任何修改仍由有权执行者按既有流程处理。
