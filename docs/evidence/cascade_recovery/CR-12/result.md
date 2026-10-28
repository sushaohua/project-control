# CR-12 交付与验收记录：已有产物与接受证据集中对账

| 字段 | 属性 / 内容 |
| :--- | :--- |
| **任务卡片** | `CR-12` |
| **所属计划** | `PLAN-CASCADE-RECOVERY-20261027 v1.1` / `workflow-replan-20261028` |
| **执行者 / 角色** | `ARCH` (Session: 当前主架构会话) |
| **独立审查角色** | `QA` / `ARCH` 独立复核 |
| **产出物** | [`reuse_matrix.md`](reuse_matrix.md) |
| **涉及仓库** | `project-control`, `soc-ap`, `mcu-p3`, `test_harness` |
| **验收结论** | **APPROVED (五大核心资产全量对账闭环，全部评定为【可复用】，明确下游消费约束)** |

---

## 1. 对账执行总结

依据用户指令及 `workflow_replan_20261028.md` 规约，ARCH 角色对 AP、MC、TH、测试向量集以及探针故障注入工具展开了逐行代码与二进制对账，产出了权威的 [《核心资产与证据集中对账复用矩阵》](reuse_matrix.md)。

### 1.1 核心成果与指标达成
1. **源码版本固化**：
   - `soc-ap`: `4445c8fedc21bafef5e6c971fcb54cec703f0e71` on `main` (clean)
   - `mcu-p3`: `af279a8c24dde92a0145d767c1c6478cfef05994` on `feat/soc-debug` (clean)
   - `test_harness`: `6c61ce6e51cf83d7fb58d319c23cb91bf95786cb` on `main` (clean)
   - `project-control`: `2b4d592f587e474d416fde316db782ff2cd1f35a` on `main` (clean)
2. **已有制品校验**：
   - AP 宿主程序 `soc-ap/build/host/bin/soc-ap` SHA256 为 `1e0e0263...`，14/14 黄金用例及 60/60 编解码用例全通；
   - TH 从控固件 `fw_th.bin` (71,176 B) SHA256 为 `5eaeb608...`，与 CR-06 交付报告 100% 严格一致；
   - MC 主控固件 `fw_mc.bin` (369,516 B) SHA256 为 `74ad2bd0...`，查明与原报告 `054b83d8...` 的差异由 `version_autogen.h` 中编译时间戳动态生成所致，源码逻辑无任何漂移，已锁定当前二进制版本；
   - 探针故障注入工具 10/10 单元测试全通，CR-02T 四项安全缺陷（F23~F26）治理有效。
3. **撤回与限制边界明晰**：
   - 严格落实 HW-G5 约束：PTY 仿真仅限主机软件回归，严禁用于硬件放行；
   - 严格落实 HW-G6 约束：MC 不得伪造 TH 响应，TH 原生自报真实版本。

---

## 2. 交付物与索引

- **对账复用矩阵原件**: [`docs/evidence/cascade_recovery/CR-12/runs/run_01/reuse_matrix.md`](reuse_matrix.md)
- **直接下游任务**: 解锁 `CR-08`（装配候选清单与台架部署 SOP）
