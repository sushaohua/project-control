# 独立文档/任务QA请求

按 project-control/.agents/rules/codex_qa_review.md 执行本轮独立QA。你未参与本轮写作；这是新候选，旧报告不复用。本轮依据用户已确认VMware→SoC两阶段尽量1:1：阶段一真实模块、进程管理、实际IPC、可见浏览器与真实MC/TH；阶段二共用源码/契约/UI平台适配并实板验收。用户明确要求update所有task相关文档。

读取本目录candidate_manifest.json，核对所列当前文件哈希，逐项审查执行总表、16新卡、18工作包、未完成旧卡接续、看板、规则/模板、架构/输入/软硬件交接/README等一致性。before/与before_manifest保留本轮前像；input_inventory保留86原卡，task_coverage记录102卡处理。46原Done卡须字节不变，原status/blocked不得伪改；旧签署不得跨revision复用。新TWIN全Backlog，不伪造会话/租约/接受。检查Scope/依赖覆盖C1~C6、MC/TH节点提供票、UI/API/IPC与进程管理、SoC输入缺口不无谓阻断VM、独立QA/QA产物ARCH复核和最终收件是否可执行。

可运行只读结构工具和隔离工具回归；不得改业务、卡、正式状态或作者文档，不操作硬件/网络/系统安装。证据与报告只写 docs/evidence/twin_task_alignment_20261029/runs/qa_01/。自行运行实际检查，保存命令/cwd/退出码/日志；检查新增工具TWIN识别与自审测试消息修正的合理性。作者的baseline_tool_tests_final.log证明原11项套件有1项失败（消息插入作者标识导致旧断言失配），当前12项通过；不要把测试字样修改当业务安全门已改变。

报告记录真实thread/session标识、请求gpt-6-luna，实际模型能核则核不能核明确unknown，不把请求值当实际值；标明准确manifest SHA256、审阅文件哈希、发现/限制/未执行、APPROVED或REJECTED（仅规划文档和小工具，不是实现/硬件通过）。报告本身SHA256另存，不自引用。报告文件名qa_review_report.md。之后主协调会安排非作者ARCH复核你的报告。
