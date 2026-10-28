# CR-08 交付与验收记录：装配协同候选清单与部署SOP

| 字段 | 属性 / 内容 |
| :--- | :--- |
| **任务卡片** | `CR-08` |
| **所属计划** | `PLAN-CASCADE-RECOVERY-20261027 v1.1` / `workflow-replan-20261028` |
| **执行者 / 角色** | `INTEGRATOR` (Session: INTEGRATOR-SESSION-20261028) |
| **独立审查角色** | `ARCH` / `QA` 联合复核 |
| **核心产出物** | 1. 候选清单: [`docs/releases/ap_mc_th_readonly_candidate.yaml`](../../../releases/ap_mc_th_readonly_candidate.yaml)<br>2. 联调SOP: [`docs/operations/ap_mc_th_joint_debug.md`](../../../operations/ap_mc_th_joint_debug.md) |
| **涉及仓库** | `project-control`, `soc-ap`, `mcu-p3`, `test_harness` |
| **验收结论** | **APPROVED (三端制品精确锁定，部署SOP严密就绪，直接解锁 CR-09 物理联调)** |

---

## 1. 候选装配内容与版本锁定

依据 CR-12 集中对账结论，INTEGRATOR 完成了 AP-MC-TH 三端协同候选清单的装配与版本锁定：

### 1.1 核心制品版本与 SHA-256 锁定
1. **AP 宿主可执行程序 (`soc-ap`)**：
   - 路径: `soc-ap/build/host/bin/soc-ap`
   - SHA-256: `1e0e0263c90c658e8026e1d5a5dd51349b411831575d4be2b7aec42fbd62d6e1`
   - 源码 Commit: `4445c8fedc21bafef5e6c971fcb54cec703f0e71` on `main`
2. **MC 主控固件 (`mcu-p3`)**：
   - 路径: `mcu-p3/motion-controller-mcu/build/fw_mc.bin`
   - SHA-256: `74ad2bd0861cebf7f6964ca81f83cf41ac850e8adfa21379073f51e218d78f99`
   - 芯片型号: `AT32F435VGT7`，基地址: `0x08020000` (HW-G2 强校验)
   - 源码 Commit: `af279a8c24dde92a0145d767c1c6478cfef05994` on `feat/soc-debug`
3. **TH 从控固件 (`mcu-p3`)**：
   - 路径: `mcu-p3/color-engine-mcu/io_toggle/build/fw_th.bin`
   - SHA-256: `5eaeb608cd22b5ec3041672db08fc865cb7b539620fb7b21de1a0925d4df9d3d`
   - 芯片型号: `AT32F423CCT7`，基地址: `0x08004000` (HW-G2 强校验)
   - 源码 Commit: `af279a8c24dde92a0145d767c1c6478cfef05994` on `feat/soc-debug`
4. **黄金用例与测试夹具 (`test_harness`)**：
   - 用例文件: `test_harness/test_cases/cascade/query_cases.json` (`18f7d9d5...`)
   - 探针故障注入器: `test_harness/hil/tools/probe_fault_injector.py`
   - 源码 Commit: `6c61ce6e51cf83d7fb58d319c23cb91bf95786cb` on `main`

---

## 2. 部署路径与安全门禁裁决

- **部署路径选定**：正式选定通过 `probe-rs` SWD 硬件烧录路径直接将 `fw_mc.bin` 与 `fw_th.bin` 烧录入板卡 Flash，完全规避 U 盘固件中继升级风险。
- **CR-07 解耦确认**：CR-07（升级管理器治理专项）不作为当前只读级联联调的阻断前置。
- **物理联调 SOP 输出**：输出了五阶段标准调试步骤（环境检查 $\to$ 固件烧录 $\to$ 单跳 AP-MC 连通 $\to$ 双跳 AP-MC-TH 级联穿透与 RTT 度量 $\to$ 异常故障注入），明确规定了 HW-G1 至 HW-G6 门禁条款。

---

## 3. 直接下游动作

- **解锁任务**：`CR-09`（物理台架三端工程联合调试）进入 `Ready` 状态，待台架操作员开展现场刷写与抓包验证。
