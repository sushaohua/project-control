# 给用户指定独立会话的审阅说明

用户已选择“由我另行指定独立会话，人工转交检查”。请将本说明交给该实际会话；当前文件不表示会话已运行或评审已通过。

## 审阅对象与版本

对象是当前独立项目中 **v2.0 首个离线协议增量的任务编排**，不是生产协议实现、硬件通信或整机验收。规划作者/本轮收件方为 Codex 主对话 `/root`，你应使用独立上下文审查。

先读取当前工作区根目录 `AGENTS.md`。然后读取：

1. [本轮协调与用户选择](COORD_20261020.md)。
2. [首轮开发安排](../planning/minimc_v2_first_increment_20261020.md)、[25 张任务卡索引](../../.agents/kanban/microtasks/minimc_v2/README.md)及所有卡原件。
3. [逐票执行约定](../guides/minimc_v2_task_execution.md)、[真实 run 模板](../guides/templates/task_run_record.md)、[04 状态与独立性规则](../../.agents/rules/04_公共看板与读写协议.md)。
4. 本地 [Rev 2.0.3 采用记录](../specs/protocol_selection_20261020.md)、[协议原文](../specs/ap_mc_formal_protocol_v2_0_multidevice_routing_draft_20261015.md)。知识库不是必需输入，原文 V04 长度冲突仍是已知未决项。
5. TASK-004/005/007/010 的子任务清单和 MS-05/06/07 的新依赖，见[公共看板](../../.agents/kanban/KANBAN.md)及卡链接。
6. [本批检查与哈希记录](../evidence/20261020_task_orchestration/README.md)，以及 `project-control/tools/check_task_graph.py` 的实际实现。

先记录 `git -C project-control rev-parse HEAD`、`git -C project-control status --porcelain=v1`，核对 `card_hash_manifest.json` 中的输入哈希。若工作区有差异，明确本次所审的是哪个 commit＋差异/文件哈希组合；不能只写“最新版本”。

## 权限与可运行检查

对任务卡、规则、协议、业务源码、管理工具只读；发现问题列缺陷，不直接改原件以促通过。不运行未来协议任务中的计划命令，不打开串口、不联网拉取、不安装依赖、不操作硬件、不更改正式任务状态。

你可以重新运行静态检查并查看原始输入：

```bash
# 从工作区根目录执行；这是已存在的管理工具。
python3 project-control/tools/check_task_graph.py --workspace .
python3 project-control/tools/check_task_graph.py --workspace . --check-ready V2-P01A
```

第二条在实际作者/检查/输入/占用未登记时应退出 **2** 并列出缺口，这是正确拒绝，不能改任务制造 Ready。第一条当前结构预期为 67 张任务、其中 25 张本批微步；依赖无缺失/循环，共享写入有先后顺序。已有合成反例检查验证工具拒绝错误输入，但工具通过不能代替你的内容审阅。

如需保存自己的报告/日志，只写入 `project-control/docs/evidence/20261020_task_orchestration/independent/<实际会话或真实run标识>/`，避免覆盖作者日志及其他审阅者原件。报告文件应署名实际会话和时间，不使用模板示例 PASS。

## 需要独立回答的问题

- 粒度是否落实到一个结果/接口层，是否仍有应继续分离的函数、构建或测试预期变更？每卡的白名单能否支撑其目标且不越界？
- 输入/前置/产物/能力条件是否形成有向、可执行的关系？设计是否错误等待实测，是否有未在字段图体现的循环？
- 每票的正常/异常判据、命令与其可用时点是否相符？桩、空测试、只跑 host smoke 是否可能误报成协议通过？
- 独立预期是否在实现前接受，作者/QA/状态写入/收件是否区分，失败重试与回退是否保留用户差异？
- 单票记录能否绑定输入、diff/候选、命令、原始日志、失败/修正、独立结论及收件？历史旧卡/旧计划是否确实保留原哈希？
- 正式状态是否如实保持 Backlog，哪些真实派单条件仍待补？不要把计划结构接受变成“25 张开发任务已经验收”。

## 回交内容

请提供实际审阅会话、所审 commit/差异及文件哈希、方法/实际命令和退出码、按任务 ID/文件定位的缺陷与严重性，以及本次结论：

- `plan_structure_accepted_pending_dispatch`：本批编排结构可接受，实际派单字段仍需逐票登记。
- `changes_requested`：有必须修订的编排缺口，列明复核条件。

这两个结论都不是协议实现通过或原 MS HIL 完成。由用户人工转交报告位置给当前主对话；本主对话读取后记录收到/修订，再核对原件更新相应状态。没有报告前继续保留检查会话/结论空值。
