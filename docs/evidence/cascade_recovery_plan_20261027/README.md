# AP—MC—TH 纠偏方案的独立排查证据

对应方案：[文件、操作、顺序与验收](../../planning/ap_mc_th_cascade_recovery_implementationplan_20261027_162003.md)。本目录证明本轮进行了哪些排查，不是源码修复或真实硬件验收通过材料。

| 位置 | 实际执行会话 | 内容与证据层级 |
| --- | --- | --- |
| [host审查](host/cascade_host_gap_audit_20261027.md) | `/root/independent_host_review` | 源码复核、PTY、系统调用故障注入、默认CTest实际运行 |
| [流程工具审查](workflow/cascade_workflow_gap_audit_20261027.md) | `/root/workflow_gap_audit` | 正式结构检查失败原件、只在/tmp修改副本的绕过反例 |
| [MCU审查](firmware/cascade_firmware_gap_audit_20261027.md) | `/root/independent_cascade_review` | 源码/文档和磁盘制品检查；没有构建/板卡操作 |
| [新增HIL工具补审](hil_tools/cascade_new_hil_tools_audit_20261027.md) | `/root/workflow_gap_audit` | 对并发新提交1d0861f做AST＋假硬件函数软件反例；未运行脚本入口或真实探针 |
| [首轮方案审查](runs/plan_review_01/qa_review_report.md) | `/root/cascade_plan_review` | v1.0内容审查REJECTED，保留原报告和准确受审副本 |
| `runs/plan_review_02/` | `/root/cascade_plan_review` | 对首轮R1/R2修正及新增HIL工具范围复审；结论以准确候选报告为准 |

审查会话互相独立，未继承实现交互历史。上表排查报告均未自签正式任务APPROVED。完整方案另交未参与写作的独立Codex审查；文档审查通过不表示实施批准、固件接受或HIL通过。

`source_evidence_manifest.json` 记录从原始/tmp位置复制的文件及SHA256，副本按字节保持不变。`repository_snapshot.json` 记录归档时四个子仓提交/分支/工作树；本方案和本证据目录为本次新增。历史报告里的/tmp路径保留，阅读时使用本目录同名副本；复现脚本中的临时路径需由后续执行者在隔离环境检查，不直接当作生产命令。

host目录保留初次8例脚本，初次stdout原件在真实工具事件中，未另造日志。新增host完整输出、transport探针和CTest LastTest.log已归档。workflow目录保留实际失败JSON、stdout、隔离反例脚本与输出。firmware报告中的向量/Trailer结果只证明磁盘文件自洽，不证明它们已装入芯片。

没有连接硬件、执行刷写/复位、改变正式卡片状态或推送服务器。已有飞书指南和缓存未纳入本次交付。

首轮方案v1.0的独立审查为REJECTED，报告和准确文档副本原样保留；作者修正后的同一原件为v1.1。初始快照与16:27:25归档快照之间，其他会话新增测试仓HIL工具并更新入口锁文件，版本与范围说明见方案§1.2；不能把归档快照冒充原始采样，也不能将新工具自动视为已接受。
