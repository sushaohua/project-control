# v2.0 首批微步任务卡

后续独立 QA 统一由独立 Codex 会话执行，含 QA 作者产物的 ARCH 复核，见 [Codex QA 规则](../../../rules/codex_qa_review.md)。各未完成卡已登记执行平台及计划别名；实际会话须逐票落实，不能用计划名冒充已启动或已通过。P01A/P01B 的历史签署保留原记录。

当前由 20 张有效活跃任务卡组成（历史初版拆解 25 张，其中 V2-P05C～P06C 6 张卡已废弃并归档入 [`superseded/`](superseded/)，由统一收敛票 [`V2-P0506`](V2-P0506.md) 承接）；本表只索引，状态/范围/验收以卡内 frontmatter 为准。旧 V2-P01～06 是分组名，不另作为可派发任务。

| ID | 单一目标 | 直接前置 | 主工作包 | 状态 |
| --- | --- | --- | --- | --- |
| [V2-P01A](V2-P01A.md) | 提取帧格式最小契约 | 本地已选协议 | TASK-005 | Done |
| [V2-P01B](V2-P01B.md) | 提取版本与心跳命令契约 | V2-P01A | TASK-005 | Done |
| [V2-P01C](V2-P01C.md) | 准备独立正常与异常样例 | V2-P01A, V2-P01B | TASK-005 | Done |
| [V2-P01D](V2-P01D.md) | 实现独立样例参考校验器 | V2-P01C | TASK-005 | Done |
| [V2-P02A](V2-P02A.md) | 定义无堆分配编解码接口 | V2-P01A, V2-P01B, V2-P01D | TASK-007 | Done |
| [V2-P02B](V2-P02B.md) | 定义有界流式解析接口 | V2-P02A | TASK-007 | Done |
| [V2-P02C](V2-P02C.md) | 冻结测试探针与运行器接口 | V2-P02A, V2-P02B, V2-P01D | TASK-005 | Done |
| [V2-P03A](V2-P03A.md) | 提供编解码符号桩 | V2-P02A | TASK-007 | Done |
| [V2-P03B](V2-P03B.md) | 提供解析器符号桩 | V2-P02B, V2-P03A | TASK-007 | Done |
| [V2-P03C](V2-P03C.md) | 接入协议库构建目标 | V2-P03A, V2-P03B | TASK-007 | Done |
| [V2-P03D](V2-P03D.md) | 实现独立命令行探针适配器 | V2-P03C, V2-P02C | TASK-007 | Done |
| [V2-P03E](V2-P03E.md) | 接入探针构建目标 | V2-P03D | TASK-007 | Done |
| [V2-P03F](V2-P03F.md) | 实现独立预期比较运行器 | V2-P01D, V2-P02C, V2-P03E | TASK-007 | Done |
| [V2-P04A](V2-P04A.md) | 实现CRC计算 | V2-P03F | TASK-007 | Done |
| [V2-P04B](V2-P04B.md) | 实现有界帧编码 | V2-P04A | TASK-007 | Done |
| [V2-P04C](V2-P04C.md) | 实现解码长度与边界防御 | V2-P04B | TASK-007 | Done |
| [V2-P04D](V2-P04D.md) | 实现完整帧校验与字段读取 | V2-P04C | TASK-007 | Done |
| [V2-P05A](V2-P05A.md) | 实现解析器复位和同步 | V2-P04D | TASK-007 | Done |
| [V2-P05B](V2-P05B.md) | 实现固定帧头累积与长度门禁 | V2-P05A | TASK-007 | Done |
| [V2-P0506](V2-P0506.md) | **收敛集成离线协议库与测试套件（最终离线候选）** | V2-P05B | TASK-007 | Done |

## 历史废弃与收敛卡 (Superseded)
* [V2-P05C](superseded/V2-P05C.md)：载荷和CRC收尾（已被 V2-P0506 吸收合并）
* [V2-P05D](superseded/V2-P05D.md)：字节超时和计时回绕（已被 V2-P0506 吸收合并）
* [V2-P05E](superseded/V2-P05E.md)：验证并修复坏帧后同步恢复（已被 V2-P0506 吸收合并）
* [V2-P06A](superseded/V2-P06A.md)：注册 CTest 离线组（已被 V2-P0506 吸收合并）
* [V2-P06B](superseded/V2-P06B.md)：独立复现协议离线候选（已被 V2-P0506 吸收合并）
* [V2-P06C](superseded/V2-P06C.md)：归档离线候选（已被 V2-P0506 吸收合并）

首张 V2-P01A 无内部任务前置，但实际作者/独立检查安排仍需登记。其余票逐项消费已接受的前置产物，不能靠任务名或Done状态推定内容可用。

完整闭环与原始证据约定见[执行指南](../../../../docs/guides/minimc_v2_task_execution.md)。离线最终候选为 **V2-P0506**（锁定制品 `minimc_v2_offline_candidate.yaml`），不替代原 MS 硬件出口。
