# VMware→SoC两阶段孪生开发文档记录

本次依据用户2026-10-29明确指令更新开发方向：第一阶段在VMware尽量1:1运行应用模块、进程管理、真实IPC和可见交互，第二阶段同源迁移SoC。用户方向与具体技术提案的接受分开；本轮不修改业务代码、正式任务状态或设备。

## 候选与原状态

- [原状态清单](runs/author_01/before_manifest.json)及`before/`内5份逐字节快照保留既有内容。
- [首次候选](runs/author_01/candidate_manifest.json)：6份文档；历史审阅范围表述存在缺口。
- [修订候选v2](runs/author_01/candidate_manifest_v2.json)：修正历史QA/ARCH报告各自的对象/哈希范围，其余5份文件不变。
- [作者文档自检](runs/author_01/document_checks.json)：相对链接存在；不构成独立验收。

## 独立审阅

| 环节 | 实际会话 | 结论 / 报告 / SHA256 |
| --- | --- | --- |
| QA首轮 | `01a1861b-bc97-7052-bbfd-668cb2d90db0` | REJECTED；[qa_01](runs/qa_01/qa_review_report.md)，`c4da7c0dac3bc8596c6939d619be66771ba2f273a2922661db380bed5714220f` |
| 非作者QA差异复核 | 同一QA会话，符合继续独立审阅规则 | APPROVED，限v2文档内容；[qa_02](runs/qa_02/qa_review_report.md)，`6c60e56be0f65cb29821ea267296b00eac40f0571a142a0d0348bc707eead237` |
| QA产物非作者ARCH复核 | `01a18626-a3a1-7be0-bace-cfc17da78f12` | APPROVED，限文档评审；[report_arch_01](runs/report_arch_01/qa_report_arch_review.md)，`4927af20c2d7556d3f9e3059443f09d55d96fa5deaddef00a8c3ae357540c6ea` |

启动两个独立线程时均请求`gpt-6-luna`。运行时实际模型别名按报告可见性如实记录，未核实部分不能冒称满足正式模型登记；COORD正式收件时核对适用性。所有结果限文档评审，不批准尚未实现的服务、总线、显示或硬件能力。旧历史报告保持原件和原适用范围。
