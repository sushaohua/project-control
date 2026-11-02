# VMware→SoC两阶段孪生开发接续

> **历史交接快照（2026-10-29）：**下文的Backlog、未启动和下一任务描述记录交接当时的情况，不代表当前状态。请从[主看板](../../.agents/kanban/KANBAN.md)、各任务卡和[总控执行清单](../planning/coord_autorun_tasklist_20261029.md)接续；正式状态及候选消费限制仍由COORD按证据核对。

用户已确认两阶段，且要求VMware阶段尽量1:1覆盖功能模块、进程/进程管理、实际IPC与可见交互。浏览器是独立显示模块，消费真实后台数据。目标是复用同一业务源码、契约和UI资源迁移SoC；不保证无需BSP/驱动/ABI/显示适配。

已更新18个工作包、未完成旧任务接续关系、主看板、规则/模板、架构/输入/交接/使用入口，新增TWIN-01～16能力任务。全部新票Backlog，未启动开发会话、未实现服务、未操作硬件，历史Done与签署保留原范围。

下一张交ARCH：[TWIN-01](../../.agents/kanban/microtasks/vmware_soc_twin/TWIN-01.md)。COORD先落实实际作者/非作者检查会话、输入版本、worktree/写范围/输出、资源、租约，再推进Ready。01接受整体服务拓扑、完整模块状态/切片及C1～C6影响和处理；02形成可执行契约，其后按依赖分发。

完整分工、依赖、验收和全部旧卡覆盖：[执行总表](../planning/vmware_soc_twin_task_execution_20261029.md)。最新输入缺口：[输入登记](../planning/soc_system_architecture_input_register_20261029.md)。交付填写：[软硬件交接规范](../operations/ap_mc_th_software_hardware_handover.md)第9节。文档调整证据：[本轮记录](../evidence/twin_task_alignment_20261029/README.md)。

优先澄清C1～C6涉及的字段消费，未知目标SoC/BSP/sysroot/屏幕和目标数值预算留待真实资料，不阻止VM目标无关工作。MC/TH仍为真实硬件，严禁中继伪造下游应答；VMware可验应用语义，SoC板级/性能只能实板接受。MS-22团队演练仍Verify，未因本轮产品规划而关闭。
