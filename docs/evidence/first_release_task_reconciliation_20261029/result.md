# 首版范围与任务对账文档审查收件记录

状态：文档候选 QA 与 QA 报告非作者复核均通过。准确候选：`e9f98cdac044cb518ab6fd871ce7871361329ebf`。

用户已确认本地可正常打印目标、按 PM 建议分期及七项首版子范围，并要求 MC、TH 工程师参与。本次交付范围是三份规划文档及其中任务对账草案，不含新正式任务卡生成、业务实现或硬件验收。

源文档最初以 `5b27106a08212b7d1e5d0f3be615a9f600d930e7` 推送。qa_01 返回 APPROVED，但 report_review_01 发现其“全部链接有效”的断言不成立：一份 TEMP 历史证据未随候选提供，两处源码是另仓路径。作者在新候选中明确记录证据限制并修正引用方式，原报告保留。qa_02 定向复验通过，report_review_02 对其报告复核通过。

## 实际独立运行

每次启动独立 Codex CLI，显式 `-m gpt-6-luna --sandbox read-only`，使用服务器全新克隆并锁定的源码检出。会话模型来自本次实际会话 turn_context 的最小字段提取，不依据模型自述。启动命令、候选与远端核对、会话 JSONL、退出码、模型记录和报告分别保存。

| 运行 | 会话 ID | 实际记录模型 | 结论 | 报告及 SHA256 |
| --- | --- | --- | --- | --- |
| qa_01 | `01a1878a-efb6-7272-be24-57936dca6e56` | `gpt-6-luna` | APPROVED | [qa_01 报告](runs/qa_01/qa_review_report.md)；`9157a0a8093f977fba1ce3c6126d7a91e153b2ada08bcf80888563e72f30da76` |
| report_review_01 | `01a1878c-9a85-7791-9c4c-a47b616caa11` | `gpt-6-luna` | REJECTED | [report_review_01 报告](runs/report_review_01/qa_report_arch_review.md)；`16e4eb569f4ca488cc0f000d17967b064df5ee4ba2b21851578461c28aaecc27` |
| qa_02 | `01a1878f-48d3-7642-b5e5-eb922e7f7f23` | `gpt-6-luna` | APPROVED | [qa_02 报告](runs/qa_02/qa_review_report.md)；`3ca64685d5e947a8082a29d7d43e7ae1776131a4cf5b45b202eaceb3cf69c02b` |
| report_review_02 | `01a18790-65c5-7461-9b34-dace691af446` | `gpt-6-luna` | APPROVED | [report_review_02 报告](runs/report_review_02/qa_report_arch_review.md)；`c72731bb43d37d1a357560c508729701c64dd64cc4f20c3b4b3caf1d3e13fee1` |

## 适用范围与后续

核对了44项功能编号和七项子范围、产品决定分期、MC/TH参与分工、现有任务映射及候选文件中49个相对链接。构建和自动化测试不适用于本次文档变更，未执行；本次不声明温度历史实测、SoC代码或整机产品经过复验。相关来源限制已在候选正文写明。

下一项由 ARCH 牵头把已确认范围变成需求、接口、验收和正式任务卡；MC、TH及软件模块负责人补各端范围和条件，PM核对产品范围，COORD负责版本、依赖、派单、独立QA与收件。TASK-011等长期工作包和TWIN现有卡先对账复用，未覆盖子范围再补卡，不将本行政收件记录当成正式实现任务完成。
