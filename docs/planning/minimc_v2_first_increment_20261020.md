# MiniMCProto v2.0 首轮开发安排

本轮计划：`marlin-r2-v2-offline-1`。2026-10-20 按用户“继续”将之前六个分组细化落地为 **25 张实际微步卡**。作者/本轮编排收件入口：Codex 主对话 `/root`。这是首个本地离线增量，远期 MCU/串口/HIL 仍按原 MS 范围逐步细化。

## 权威任务与状态

实际任务原件在 [v2.0 微步目录](../../.agents/kanban/microtasks/minimc_v2/README.md)，该目录每票有唯一 ID/revision、输入、写范围、命令与正反判据、证据根目录、失败处理、检查/收件条件。此前 V2-P01～06 只作为分组名，不再派发整组。

结构已映射不等于实际执行闭环。当前新卡均 Backlog，未安排的作者/检查会话、未产生的上游接受版本和实际租约保持空值；必须按[逐票执行约定](../guides/minimc_v2_task_execution.md)补齐后才能 Ready。当前只落实编排，未实现生产协议库或部署自动调度。

## 首批任务清单

| ID | 单一结果 | 直接前置 | 主工作包 |
| --- | --- | --- | --- |
| [V2-P01A](../../.agents/kanban/microtasks/minimc_v2/V2-P01A.md) | 提取帧格式最小契约 | 已选本地协议 | TASK-005 |
| [V2-P01B](../../.agents/kanban/microtasks/minimc_v2/V2-P01B.md) | 提取版本与心跳命令契约 | V2-P01A | TASK-005 |
| [V2-P01C](../../.agents/kanban/microtasks/minimc_v2/V2-P01C.md) | 准备独立正常与异常样例 | V2-P01A, V2-P01B | TASK-005 |
| [V2-P01D](../../.agents/kanban/microtasks/minimc_v2/V2-P01D.md) | 实现独立样例参考校验器 | V2-P01C | TASK-005 |
| [V2-P02A](../../.agents/kanban/microtasks/minimc_v2/V2-P02A.md) | 定义无堆分配编解码接口 | V2-P01A, V2-P01B, V2-P01D | TASK-007 |
| [V2-P02B](../../.agents/kanban/microtasks/minimc_v2/V2-P02B.md) | 定义有界流式解析接口 | V2-P02A | TASK-007 |
| [V2-P02C](../../.agents/kanban/microtasks/minimc_v2/V2-P02C.md) | 冻结测试探针与运行器接口 | V2-P02A, V2-P02B, V2-P01D | TASK-005 |
| [V2-P03A](../../.agents/kanban/microtasks/minimc_v2/V2-P03A.md) | 提供编解码符号桩 | V2-P02A | TASK-007 |
| [V2-P03B](../../.agents/kanban/microtasks/minimc_v2/V2-P03B.md) | 提供解析器符号桩 | V2-P02B, V2-P03A | TASK-007 |
| [V2-P03C](../../.agents/kanban/microtasks/minimc_v2/V2-P03C.md) | 接入协议库构建目标 | V2-P03A, V2-P03B | TASK-007 |
| [V2-P03D](../../.agents/kanban/microtasks/minimc_v2/V2-P03D.md) | 实现独立命令行探针适配器 | V2-P03C, V2-P02C | TASK-007 |
| [V2-P03E](../../.agents/kanban/microtasks/minimc_v2/V2-P03E.md) | 接入探针构建目标 | V2-P03D | TASK-007 |
| [V2-P03F](../../.agents/kanban/microtasks/minimc_v2/V2-P03F.md) | 实现独立预期比较运行器 | V2-P01D, V2-P02C, V2-P03E | TASK-007 |
| [V2-P04A](../../.agents/kanban/microtasks/minimc_v2/V2-P04A.md) | 实现CRC计算 | V2-P03F | TASK-007 |
| [V2-P04B](../../.agents/kanban/microtasks/minimc_v2/V2-P04B.md) | 实现有界帧编码 | V2-P04A | TASK-007 |
| [V2-P04C](../../.agents/kanban/microtasks/minimc_v2/V2-P04C.md) | 实现解码长度与边界防御 | V2-P04B | TASK-007 |
| [V2-P04D](../../.agents/kanban/microtasks/minimc_v2/V2-P04D.md) | 实现完整帧校验与字段读取 | V2-P04C | TASK-007 |
| [V2-P05A](../../.agents/kanban/microtasks/minimc_v2/V2-P05A.md) | 实现解析器复位和同步 | V2-P04D | TASK-007 |
| [V2-P05B](../../.agents/kanban/microtasks/minimc_v2/V2-P05B.md) | 实现固定帧头累积与长度门禁 | V2-P05A | TASK-007 |
| [V2-P05C](../../.agents/kanban/microtasks/minimc_v2/V2-P05C.md) | 实现载荷和CRC收尾分发 | V2-P05B | TASK-007 |
| [V2-P05D](../../.agents/kanban/microtasks/minimc_v2/V2-P05D.md) | 实现字节超时和计时回绕 | V2-P05C | TASK-007 |
| [V2-P05E](../../.agents/kanban/microtasks/minimc_v2/V2-P05E.md) | 验证并修复坏帧后的同步恢复 | V2-P05D | TASK-007 |
| [V2-P06A](../../.agents/kanban/microtasks/minimc_v2/V2-P06A.md) | 将离线协议组注册到CTest | V2-P05E | TASK-007 |
| [V2-P06B](../../.agents/kanban/microtasks/minimc_v2/V2-P06B.md) | 独立复现协议离线候选 | V2-P06A | TASK-010 |
| [V2-P06C](../../.agents/kanban/microtasks/minimc_v2/V2-P06C.md) | 归档准确离线集成候选与收件 | V2-P06B | TASK-004 |

## 拆解与闭环落实

- 独立样例数据、独立参考校验器分票；编解码/解析接口与测试工具接口分别冻结。
- 符号桩、构建接入、测试探针实现、探针接入和独立比较运行器分别成票。桩只返回明确未实现，不制造协议成功。
- CRC、编码、解码长度防御、解码完整校验分票；流式同步、头部、载荷CRC、超时、坏帧恢复分票。每票只填对应函数/状态分支，不同时回改已冻结接口或独立预期。
- 每票的计划命令标注依赖将来产物，正常/异常判据明确；该票完成需有自己的实际检查，不能全部推迟到最终 QA。
- 最终显式启用十个协议检查（reference＋九个功能组）及原 host smoke，合计十一项；每组必须非零 case。stub 不进入最终正常测试，all 不重复充当覆盖。
- 一卡一证据根目录、一次运行一个真实 run 目录；命令/cwd/退出码、失败及更正、准确候选、独立检查和收件逐项绑定版本。范围变更修订卡，不覆盖旧证据。

当前所有输入都使用项目内副本，不依赖知识库。[协议 Rev 2.0.3](../specs/README.md) 的 SHA256 为 `9f8d4f9607cb3e76cc30b9ee2f971b23c3e0d936611188466a71f4aa15f3ce54`；派单前按卡内 `dispatch_binding` 解析实际源码/前置版本，不能把规划时 HEAD 当成未来实现的消费版本。

## 与既有计划的连接

契约/样例任务挂 TASK-005；协议库与测试工具实现挂 TASK-007；独立复验挂 TASK-010；准确候选归档挂 TASK-004，均只有一个主工作包。MS-05 增加最小命令契约的消费前置，MS-06 消费独立参考预期，MS-07 消费本离线候选；原 MS-03/04/05/06/18 等硬件/固件条件保留，没有反向要求离线设计先等待硬件样例。

第一票 V2-P01A 仅依赖本地已选协议，不等尚未产生的实现；其独立 Reviewer、作者和占用仍须真实登记。后续按每条依赖的接受版本及可使用条件放行；“前置 Done”不能替代产物可用性检查。

后续另行细化 AP 会话/串口、MC/TH 构建与 USART2 迁移、MC↔TH 路由和真实 RTT。当前 socket 限制影响网络/HIL，不妨碍本地离线能力建设；本增量不执行 OTA、运动、加热或急停，也不自动完成 MS-11/17 的业务验收。

## 已有证据与历史保留

[协议算术预核对](../evidence/20261020_protocol_preflight/protocol_preflight.json)已对五个原稿帧 CRC/长度/版本位和 256 项 CRC 表核对匹配；V04 载荷长度语义冲突仍未解决，不能据此执行急停。该核对不是生产编解码测试或独立 QA 签署。

[上轮编排核查](task_orchestration_audit_20261020.md)保留为修订前快照。其 42 张旧卡和本计划旧版已按原哈希归档到 `docs/evidence/20261020_task_audit/inputs/`；结构化旧审计记录不覆盖。当前编排检查和真实独立评审（如发生）单独保存到 `docs/evidence/20261020_task_orchestration/`。
