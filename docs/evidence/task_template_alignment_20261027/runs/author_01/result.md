# 模板与派单/交付规范同步记录

本轮用户明确要求“那就直接来修改”，范围承接任务模板及相关派单、运行与QA报告规范。作者：AI (Codex)，主会话`/root`。本记录不表示新建工程实施票已派单或旧候选已被接受。

本次修改6份已有文档并新增1份QA报告模板，准确路径和前后SHA256见`candidate_manifest.json`，字节级开工原件在`before/`，内容差异在`candidate.patch`。两份原CRLF模板保持CRLF，其他文档保持LF。

主要变化：补齐父任务能力门和准确接受版本、模板版本、逐项Reviewer/Verifier报告哈希与所审候选、跨节点实施/工程联调/独立验收关联、逐命令与逐例实际结果、正常/故障预期区别、必跑测试组/非零case、证据撤回、候选适用范围及状态/决定区分。QA模板未预填PASS或APPROVED；文档任务、单板任务和最终组合分别按范围检查。旧V2执行指南中的当前会话/实时审核叙述改为由卡片和真实交接记录读取，说明superseded及V2-P0506的关系。

自检命令（cwd为工作区根）：`PYTHONDONTWRITEBYTECODE=1 python3 /tmp/check_task_template_docs_20261027.py`，最终exit0，输出见`document_checks.json`。脚本副本为`check_template_docs.py`，验证所有YAML frontmatter/代码块可解析且无重复键、内部Markdown链接存在、模板默认待审/未执行且无预勾选、活动V2数量、原CRLF保留、无尾随空格/tab，以及7文件范围的Git差异格式。

首次自检使用默认`git diff --check`，把原有CRLF的CR识别为尾随空白，exit1；查明两份旧模板原件全为CRLF后，单次命令明确使用`core.whitespace=blank-at-eol,blank-at-eof,space-before-tab,cr-at-eol`识别合法行尾，同时另检查每行尾部无空格/tab。后者又发现QA指引中4行存量Mermaid空白行，已只去除这些行的空格。两项格式失败保留在实际工具事件中，没有声称首次检查即通过，也没有修改编译/协议检查开关。

当前`check_task_graph.py`未改；模板字段不自动成为机器门禁，完整MCU任务/生命周期/真实版本/租约及作用域校验仍需对应工具专项。所有文档明确目前的人工核对责任，不将结构检查exit0当成QA通过。

同仓其他会话在本轮期间修改了看板、MS-07/MS-14/MCQ-0106、复盘和交接文件；这些不在本轮7文件候选中，未回退、提交或代签。此前完整纠偏方案与审查证据也保留原件。本轮未修改AP/MC/TH源码、测试实现或任务检查器，未执行构建/HIL/硬件/服务器推送；未更新正式任务状态或历史签署。文档候选交独立Codex复核，报告在新的独立run保存。
