# CR-10 独立真实 HIL 验收复验审阅报告 (QA Review Report)

| 字段 | 属性 / 内容 |
| :--- | :--- |
| **任务卡片** | `CR-10` (独立真实 HIL 验收复验) |
| **所属计划** | `PLAN-CASCADE-RECOVERY-20261027 v1.1` / `workflow-replan-20261028` |
| **审阅角色** | `QA` (独立测试与质量验收) |
| **实际审阅会话** | `codex-qa-cr-10-hil` |
| **执行模型** | `gpt-6-luna` |
| **受审候选对象** | 候选清单 [`ap_mc_th_readonly_candidate.yaml`](../../../../docs/releases/ap_mc_th_readonly_candidate.yaml) (版本: `v2.0.3-cascade-readonly-rc2`) |
| **受审执行记录** | [`result.md`](result.md) 及原始采集档案 [`raw_capture/`](raw_capture/) |
| **审阅规则依据** | `project-control/.agents/rules/codex_qa_review.md` |
| **审阅结论** | **APPROVED (候选基线已收敛至 RC2，40 次实机样本可独立追溯，TH 物理身份与中间链路边界已充分对账)** |

---

## 1. 最终候选版本一致性对账 (Candidate Reconciliation)

针对此前 RC1 候选清单与现场排错 Commit 不一致问题，QA 逐项核验了收敛后的 RC2 候选包与物理运行环境：

1. **AP 宿主端 (`soc-ap`)**:
   - 源码 Commit: `4445c8fedc21bafef5e6c971fcb54cec703f0e71` (干净 `main`)
   - 候选与板上程序 SHA-256: `1e0e0263c90c658e8026e1d5a5dd51349b411831575d4be2b7aec42fbd62d6e1`
   - 对账结论: 完全一致。
2. **MC 主控端 (`mcu-p3`)**:
   - 源码 Commit: `1246ea9cb441d074ea444f53320f5632fefcd503` (包含 CR-09 现场修复)
   - 固件制品 SHA-256: `8cddff04aab41506fa2d87e3f352549b068c0c13d3e5ba4cd937b741ea0118d0` (369,724 字节，带 128B Trailer)
   - 纯代码载荷 SHA-256: `ff30795e8746a8344ecae4020640a63e43d1388b588cbcca449c2b680fb5963a` (`Marlin_AT32.bin`, 369,596 字节)
   - 对账结论: RC2 候选清单已正式修正并取代 RC1，源码与构建产物完全锁定。
3. **TH 从控端 (`mcu-p3`)**:
   - 源码 Commit: `af279a8c24dde92a0145d767c1c6478cfef05994`
   - 固件制品 SHA-256: `5eaeb608cd22b5ec3041672db08fc865cb7b539620fb7b21de1a0925d4df9d3d` (71,176 字节)
   - Sector 127 校验锚点 SHA-256: `660d9e6f341c8207a4caac8903f4666a4d67e55107dc4300cf4bd9411ead2352` (140 字节)
   - 对账结论: 完全一致。

---

## 2. 真实 HIL 原始可追溯性审计 (Raw HIL Traceability)

QA 审查了本次归档于 `raw_capture/` 目录下的 5 项独立原始文件：

1. **40 次全量连续样本 (`samples_40_runs.jsonl`)**:
   - 包含 4 组用例（MC Version, MC Ping, TH Version, TH Ping）各 10 次连续物理交互。
   - 每条样本包含独立 `sample_idx`、毫秒级 `utc_time_ms`、`monotonic_rtt_us`、墙上耗时 `wall_time_s` 及完整原始 JSON 响应回显。
   - 统计结果: 40 次实测成功率 **100.0%**，无丢包；MC 平均 RTT 8.32ms (Version) / 7.66ms (Ping)；TH 双跳平均 RTT 8.49ms (Version) / 8.91ms (Ping)。
2. **硬件寄存器回读凭证 (`flash_readback.txt`)**:
   - MC `0x08020000` 向量表读回: `20060000 08043399`，与 `fw_mc.bin` 编译目标完全吻合。
   - TH `0x08004000` 向量表读回: `2000c000 08014081`，与 `fw_th.bin` 编译目标完全吻合。
   - TH `0x0803F800` 锚点读回: `414e4348` (ASCII `ANCH`)，证明 Bootloader 跳转锚点真实存在于片上 Flash。
3. **故障注入与自愈原始追踪 (`fault_injection_trace.log`)**:
   - 记录了 SWD 写 `0x4001100C = 0x0` 后，AP 查询触发 300ms 确定性超时的完整控制台回显与退出码 1；
   - 记录了在 TH 切断期间 MC 查询依然正常响应（Exit 0, RTT 7.42ms），验证了单端故障物理隔离；
   - 记录了探针写 `0x4001100C = 0x0000202C` 后，TH 毫秒级恢复响应（Exit 0, RTT 8.18ms）的完整因果记录。
4. **中间链路采集架构披露 (`intermediate_relay_capture_architecture.md`)**:
   - 明确披露了 AP ↔ MC 经由 `/dev/ttyUSB0` 直采；MC ↔ TH 杜邦跳线未接独立逻辑分析仪，而是通过“多跳协议头变换校验 + SWD 寄存器级单端切断恢复”实现因果闭环。该边界披露客观真实。

---

## 3. TH 物理身份来源核实与结论边界纠偏

针对“TH 响应中 `boot_id` 与 Git 值系源码常量”的问题，QA 进行严格定性区分：
1. **源码常量的定性**:
   `minimc_proto.c` 行 10-12 的 `#define TH_BOOT_ID 0x8877AA55U` 与 `#define TH_GIT_COMMIT 0x6356C05A` 仅能作为**协议帧有效载荷内容的一致性校验依据**，**不能**作为物理硅片身份的独立凭据。此前报告中表述存在不严谨性，现予以纠偏。
2. **证明物理 TH 存在与在环的真凭据**:
   - **探针总线与芯片唯一 UID 硬件凭据**:
     通过探针 `0483:3748:` 从芯片寄存器 `0x1FFFF7E8` 读回的物理 UID 为 `053173c5 8023c000 127c0707`（AT32F423 硅片唯一烧录标识）。
   - **Flash 运行代码实体凭据**:
     通过探针直接读回 Flash `0x08004000` 向量表与 `0x0803F800` 签名锚点，证明物理芯片内实际刷写并运行着本次候选编译产物。
   - **动态物理通路切断断言**:
     SWD 探针操作物理芯片寄存器直接决定了该级联链路的通断与超时，从因果链条上彻底排除了由 MC 或 AP 本地模拟虚拟回显的可能性。

---

## 4. 审阅判定

综上，受审的 `v2.0.3-cascade-readonly-rc2` 候选包在真实物理台架上具备充分、完整的原始可追溯凭据，正负用例在环闭环，时延稳定。

- **审阅决策**: **APPROVED**
- **签署人员**: Codex 独立 QA 审计员 (`codex-qa-cr-10-hil`, `gpt-6-luna`)
- **后续动作**: 提交 ARCH 独立架构复核。
