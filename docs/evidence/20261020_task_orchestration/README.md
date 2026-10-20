# 首批 v2.0 任务编排检查与交接证据

本批作者：AI (Codex)，当前主对话 `/root`。用户要求继续落实任务细化/闭环/回溯，并选择“由我另行指定独立会话，人工转交检查”。当前独立会话身份和结论尚未提供；本目录作者检查不是独立 QA 签署。

## 当前落地结果

原有 42 张任务卡继续保留，首个离线协议增量新增 **25 张实际微步卡**，共 67 张规范任务原件。新卡接入 TASK-004/005/007/010，MS-05/06/07 增加相应离线输入/候选前置，并保留原硬件条件。代码/硬件开发尚未执行，新卡均 Backlog。

所有新卡已映射仓库和写范围，逐项定义计划命令、正常/异常判据、有限检查点和两次有依据纠正后的停止条件、唯一证据根目录和收件路径。实际作者、检查会话、消费版本和占用尚未登记的字段保留空值，工具会明确拒绝派单 Ready。

## 实际检查记录

| 文件 | 结果及边界 |
| --- | --- |
| [structure_check.json](structure_check.json) | 规范任务原件 67、新卡 25；结构无错误、依赖无缺失/循环；28 对共享写路径均有依赖顺序。不是每张卡已执行或已接受的证明。 |
| [first_ticket_readiness.json](first_ticket_readiness.json) | 对首票 V2-P01A 检查派单条件，预期且实际退出 2，列出实际会话/工作区/输入绑定/租约缺口；正确拒绝未就绪，不改状态。 |
| [guardrail_checks.json](guardrail_checks.json) | 当前管理工具 11/11 合成检查按预期通过：正常结构、缺失依赖、循环、越界写路径、提前改 Ready、缺派单字段、协议哈希变化、共享写入无顺序、缺异常判据、缺交付文件、候选协议字段错误。错误输入只在 `/tmp` 副本中构造，规范任务未被测试篡改。 |
| [card_hash_manifest.json](card_hash_manifest.json) | 当前卡片、修订工作包/消费者、关键计划/指南/本地协议/工具的内容摘要；审阅时再与实际 Git commit/工作区差异核对。 |
| [validation_record.json](validation_record.json) | 本轮管理检查的实际命令、cwd、退出码、工具摘要和未执行范围。 |
| [runs/toolcheck_01/guardrail_checks.json](runs/toolcheck_01/guardrail_checks.json) | 初次工具 9 项检查的原始报告，保留当时工具源文件及 67 张输入快照；不以新结果覆盖它。 |
| [runs/toolcheck_02/guardrail_checks.json](runs/toolcheck_02/guardrail_checks.json) | 修正候选字段错误处理并增加交付/候选反例后，11 项检查的原始报告，另存当时工具和输入快照。 |
| [runs/final_validation_01/failure_and_correction.json](runs/final_validation_01/failure_and_correction.json) | 最终差异检查实际发现七份本轮编辑的旧卡 CRLF 被报告为尾随空白；保留原始失败日志和更正前快照，仅将这些文件换行统一成 LF，未放宽 Git 检查规则。后续重验另存 run。 |
| [SHA256SUMS](SHA256SUMS) | 本目录当前顶层证据文件的 SHA256，供内容复核；不是签名或审批证明。 |

两次合成检查的完整日志在各自 run 目录，`.snapshot` 是当时只读输入，不是正式卡或当前工具。根目录平铺的 `guard_*.log` 是最新检查副本，旧 run 保留原字节。工具只做静态结构和字段检查，不推定身份/签署真实性、依赖能力或代码正确性。

## 历史证据与使用限制

修订前核查的 42 张原卡及旧首轮计划已按原哈希保存在 `docs/evidence/20261020_task_audit/inputs/`，原 `task_audit.json` 保留不改。旧审计描述“没有实际新卡”等状态仍只对当时有效；当前状态由规范卡和本批结构记录读取，不能用改写历史来制造闭环。

本批没有执行未来协议编解码器测试，没有 AP 串口操作、MCU 构建/烧录、真实 RTT 或独立验收。将来任务中十个协议检查＋host smoke 的十一项 CTest 尚未产生；它们与本目录管理工具的十一项合成检查是两类不同对象。

本批资料由包含它们的控制仓本地 Git 提交标识；读取 `git -C project-control rev-parse HEAD` 并检查工作区差异。服务器同步没有新验证结果。独立会话请使用[审阅说明](../../handoff/MINIMC_V2_PLANNING_REVIEW.md)，由用户人工转交实际报告位置。

## 入库空白检查的范围

完整暂存差异检查会报告协议原稿、历史输入快照和两份原始网络失败日志中的既有尾随空白/CRLF；这些材料必须保留原字节。详见 [暂存检查记录](runs/staged_validation_01/record.json) 和原始日志。本轮新写/修订的有效任务、指南和工具仍执行 Git 空白检查；只对记录中明确列出的原稿、历史输入目录及三份原始日志使用路径排除，并逐文件记录 SHA256、核对暂存字节与磁盘一致。没有修改 Git 空白规则，也未把历史材料的原始格式问题记作通过。
