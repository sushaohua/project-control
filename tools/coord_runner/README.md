# QA执行与独立审阅

当前默认链路为：Runner确定性执行已接受的沙箱测试 → 固化并校验客观物证 → 准备准确源码与Diff → 新建只读Codex审阅 → 校验正式报告 → 非作者复核QA报告 → COORD收件。

## 执行输入

- `default_qa_executor`读取当前任务卡准确revision，使用`verification.commands`的实际命令、`cwd`、`expected`、`availability`和可选`kind`（`build`或`test`，默认`test`）。缺失、计划中或零测试命令会阻塞，模型不会补写命令。
- `cwd`是沙箱根目录下的相对路径；构建输出须使用容器可写位置，例如`/tmp`。服务器源码快照仍只读挂载，不能依靠写作者目录或复制作者产物完成检查。
- 目标仓库取任务写入边界或显式`candidate_repository`；多仓边界无法唯一判断时阻塞。各仓`source_baseline`与候选锁定为完整提交，URL/ref取QA配置。Diff采用准确的`source_baseline`或本卡`base_commit`，缺少提交对象时要求补齐输入，不自行改用别的比较基线。
- Python直接运行`qa_runner.py`并传入命令列表和所有仓库锁。程序从固定输出目录读取`server_qa.json`，校验实际字节和关联证据，不从stdout中猜测JSON引用。

## 审阅

- 沙箱完成并通过物证完整性检查后，checkpoint保存`runtime_context.qa_result`，包含原始通过/失败事实、请求快照、准确候选和物证引用。失败事实同样交独立Codex审计以区分代码缺陷与环境问题，绝不改写为通过；有效拒绝沿用原任务退修，环境、来源或证据不足阻塞。审计不能批准已失败的客观检查。
- `default_review_executor`只消费已有物证，确定性生成准确候选的Diff、请求和审阅包。Codex不负责启动Docker或组织测试，不读取作者工作树作为受测源码。
- Codex以独立进程运行，显式`--sandbox read-only`，使用`--output-schema`与`--output-last-message`。进度JSONL、stderr与最终结果分别落盘；不拼接所有聊天文字当作JSON，也不靠字符串包含`APPROVED`判定。
- 程序核对报告字段、任务/revision、候选、角色、实际thread ID和批准范围；必测项未执行不能批准。整体JSON代码块可去除外层围栏后校验，其余非法最终输出阻塞，不能猜测或补造决定。
- 正式`review_report.md`、会话原始记录和哈希分别保存。QA报告由新的非作者审阅会话复核，独立复核报告与被审QA报告分别留痕。

## 阻塞与重试

单任务发生超时、鉴权失败、非法审阅输出或缺证据时，Runner记录错误物证及原阶段，将内部执行记录置为`Blocked`并保存checkpoint，继续处理其他可运行任务。环境阻塞不增加代码返工次数；有效`REJECTED`仍按原规则退修并累计返工。

`runtime_context`是兼容旧checkpoint的附加字段，不是Markdown任务卡的第二套正式状态。卡片、看板、资源和最终收件仍由唯一COORD按实际证据维护；旧checkpoint没有该字段时按空记录加载，缺物证不能直接审阅通过。

COORD确认阻塞原因已解除、输入revision未变、资源可重新占用后，可显式重试：

```bash
python3 project-control/tools/coord_runner/runner.py --resume-task <实际任务ID> --once
```

审阅阶段阻塞会复用已保存并重新核验的沙箱物证，从原阶段继续；不会重复跑测试或偷偷换模型。默认不在每次轮询自动重试阻塞项。输入变更必须修订任务并安排新的执行记录；不能将旧测试套到新候选。

如果修复的是沙箱环境而必须重新执行测试，可在输入revision和准确候选未变、COORD确认环境已恢复后显式加`--rerun-sandbox`。旧run及报告引用保存在`previous_qa_runs`，新run重新生成物证，不覆盖原文件。

单轮/有限执行模式输出JSON摘要；存在阻塞或升级任务时正常返回退出码2，便于上层区分“本轮已处理”与“任务通过”。常驻模式继续处理其他可运行任务，阻塞及原始错误保存在checkpoint和物证中。

## 当前边界

- 当前默认Docker配置没有真实USB设备映射/HIL执行器。要求`hardware-verified`的任务会保留软件物证并阻塞HIL接受，不能签成真实硬件通过。
- 现有作者默认执行器仍只定位候选，不代表已实现工程师Agent的自动派发。本改动聚焦QA执行、审阅和错误恢复，不宣称整个自动调度系统已部署。
- 本地模拟测试和假CLI协议测试只验证编排及失败处理。正式QA仍需服务器锁定候选、真实隔离环境、独立Codex会话和相应物理证据；本地文件及哈希检查不能单独证明服务器或硬件真实性。
- 本实现没有提交/推送、自动合入或改写历史报告的动作。
