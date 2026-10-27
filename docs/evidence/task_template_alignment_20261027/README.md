# 任务模板与派单/交付规范同步证据

用户授权：2026-10-27“那就直接来修改”，承接任务模板及相关流程规范修改。范围为6份已有文档和1份新增QA报告模板；源码、任务检查器、正式状态和旧签署不在本次交付内。

| run | 实际会话 | 内容 |
| --- | --- | --- |
| [author_01](runs/author_01/result.md) | `/root`，AI (Codex) | 开工原字节、七文件首轮候选/差异、格式与结构自检 |
| [review_01](runs/review_01/qa_review_report.md) | `/root/task_template_review`，独立Codex | 首轮REJECTED；原候选快照、命令/输出、外部哈希清单保留 |
| [author_02](runs/author_02/result.md) | `/root`，AI (Codex) | 修scope_status、PA-6负例语义和HW-G6业务/帧边界，保留新候选与自检 |
| [review_02](runs/review_02/qa_review_report.md) | `/root/task_template_review`，独立Codex | 修订候选APPROVED，仅准确七文件的文档接受；首轮报告保留 |

报告只针对准确文档候选，不能作为业务源码、设备部署或真实HIL通过。原两份CRLF模板保持CRLF；其他会话同期修改的任务卡、看板、交接等未被本次作者覆盖或代签。文档自检的exit0只证明其所列格式/结构检查通过，不代表正式任务准入或全部自动门禁已实现。
