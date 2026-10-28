# 软硬件交接文档审阅记录

本轮为用户要求的交接文档编写及独立文档审阅，不是CR-08执行或硬件接受；不修改正式任务状态、作者、租约或历史签署。

审阅对象：`project-control/docs/operations/ap_mc_th_software_hardware_handover.md` 与工作区 `README.md` 的新增交接入口。原联合调试SOP在本次编写期间有其他修改，保留其内容；交接规范要求按准确版本核对SOP，不替其签署或宣称可执行。

实际报告及准确文件哈希保存在独立run。文档审阅通过不代表候选已锁定、真人已签收、固件已部署或HIL已通过。

## 实际审阅结果

| 检查 | 实际结果 | 报告 / SHA256 |
| --- | --- | --- |
| 独立QA首轮 / gpt-6-luna / `/root/handover_document_qa` | REJECTED；原表格部署前后条件存在歧义，历史保留 | [qa_01报告](runs/qa_01/qa_review_report.md) / `9b590e27ce09c81dc8d2acfe21d528bd095d981cac5ba89626c0054fde0e0ebc` |
| 独立QA定向复核 / 同一非作者会话 | APPROVED，仅修订文档及README入口；两行明确区分部署前静态检查和部署后收发核验 | [qa_02报告](runs/qa_02/qa_review_report.md) / `737cda79984730b1f9c2ba14cb1320d0307b80cd666c6d6d6e082235bdf09bce` |
| QA报告独立ARCH首轮 / gpt-6-luna / `/root/handover_report_arch` | REJECTED；读取了QA报告尚未完成的中间版本，不能用于最终报告 | [report_arch_01](runs/report_arch_01/qa_report_arch_review.md) / `081013d013b4e09a9c910bc2a2f672908bac7d42138dfeddc9acd4abb66102f7` |
| QA报告独立ARCH复核 / 同一非作者会话 | APPROVED；核对最终提交的QA报告及其日志哈希；仅文档/报告范围 | [report_arch_02](runs/report_arch_02/qa_report_arch_review.md) / `3e126431d0d5f4dd594165a214099babe44554752cd95dde08a870666a7c4001` |

接受的正文SHA256：`04bc8bb1c9403981f475398020bcfa7ead56ae573dd068e15c5ced5eaaad30d2`；根README SHA256：`a0db8f72c752dbdac9763fee475aa64bcde152afa972bc7b60f77f75cc0b40f0`。报告原始检查输出各在相应run内。QA最终报告已由非作者Codex作ARCH复核；首轮读取的中间QA报告哈希为 `78effda9875482d00e0e08f5a02cb19b85993c88cf8dabe93fef68458957cb1e`，与最终报告不同，该首轮意见只适用该中间版本，历史保留。

作者检查了新增文档的相对链接与README入口（无缺失链接，入口一处）。没有运行构建、固件测试、串口、部署或硬件HIL，不据此推进CR任务状态。
