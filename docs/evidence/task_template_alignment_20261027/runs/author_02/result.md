# 模板文档候选修订记录

作者：AI (Codex)，`/root`。七文件范围和用户授权不变。开工原字节仍为`../author_01/before/`；首轮候选、自检与独立报告原样保留。本run准确候选见`candidate_manifest.json`，相对开工原件的差异见`candidate.patch`。

首轮独立审查`../review_01/qa_review_report.md`结论REJECTED，报告SHA256为`304c0e8e89547042381be80dc579a09b9d055bcc9f29254660cc5699eeadcbff`。本次由作者针对三项问题修订：

- D1：任务卡增加`scope_status: unmapped`，说明Ready前必须映射真实范围；明确通用模板不等于旧V2专用schema，专用适配不能填造字段换绿灯。
- D2：QA指引PA-6改查真实命令/退出码/原始输出与独立预期是否一致；明确负例可预期非零/无响应，Exit0与零告警只用于适用构建/正常用例。
- D3：HW-G6区分路由帧头、Hop/routed/CRC等必要操作与被禁止的业务cmd/Payload解析、业务seq修改、文本降级和伪造下游应答。

同段补充公共规则§4.3可点击链接，空Reviewer/Verifier/Integrator只是Backlog占位，不能当免检；将指南中的20张卡明确为2026-10-27目录采样，实时数量/状态仍以准确卡为准。

实际重跑文档检查命令`PYTHONDONTWRITEBYTECODE=1 python3 /tmp/check_task_template_docs_20261027.py`，cwd为工作区根，exit0；输出与脚本副本存本run。未运行构建、正式任务Ready/Done验收、HIL或硬件操作。检查器代码保持未改，完整自动门禁仍是独立工具专项，不能把文档模板更新当作已部署。

当前候选交未参与写作的原独立审阅会话，以新`review_02`复审；不覆写首轮报告、候选或历史签署。同仓其他会话的卡片/看板/交接变更继续保留，不纳入本轮七文件交付。
