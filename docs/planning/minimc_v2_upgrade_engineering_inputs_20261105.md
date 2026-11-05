---
id: ENG-INPUTS-MINIMC-V2-UPGRADE-20261105
title: MiniMCProto v2.0 双 MCU 统一升级多端工程接单回执与专项技术输入（REQ-20261105-003）
demand_id: DEM-20261105-006
requirement_id: REQ-20261105-003
phase: Phase B (Multi-Endpoint Read-Only Engineering Technical Inputs & Contract Conflict Impact Assessment)
revision: 1
date: 2026-11-05
author_roles:
  - ENG-FWD
  - ENG-STATE
  - ENG-MC
  - ENG-TH
  - ENG_BOOT_MC
  - ENG_BOOT_TH
  - INTEGRATOR
  - ENG-UI (Entry Confirmation)
  - ENG-NET (Entry Confirmation)
author_session: 07a1f6dc-f47c-45e5-bf00-37ec14e2dfda
predecessor_session: 484ac302-bd54-4e1b-be9f-0227e1475d5d
status: completed_read_only_engineering_inputs_ready_for_arch_master_consolidation
---

# MiniMCProto v2.0 双 MCU 统一升级多端工程接单回执与专项技术输入（`REQ-20261105-003`）

> **只读规划边界声明**：本文件严格在 [20261105_minimc_v2_upgrade_coord_planning_prompt.md](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/work_intake/submissions/20261105_minimc_v2_upgrade_coord_planning_prompt.md)（`revision: 3`）与 [minimc_v2_unified_mcu_upgrade_proposal_20261105.md](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/planning/minimc_v2_unified_mcu_upgrade_proposal_20261105.md)（`revision: 2`）授权范围内完成。全过程对 `soc-ap/`、`mcu-p3/`、`boot/bootloadermc/`、`boot/bootloaderth/`、`test_harness/` 保持 **100% 物理只读**，未执行任何业务源码修改、探针烧录、硬件复位或串口抢占操作。

---

## 1. 各工程角色接单回执与必读规则/源码核查登记（`read_sources`）

### 1.1 各仓规则入口、`SOURCE.json` 溯源与 HEAD Commit 基线核对表

本节按 [repository_rule_sources.json](file:///home/sushaohua/workspace/ai_soc_project/project-control/.agents/rules/repository_rule_sources.json)、[repository_rule_boundaries.md](file:///home/sushaohua/workspace/ai_soc_project/project-control/.agents/rules/repository_rule_boundaries.md) 与 [bootloader_role_boundaries.md](file:///home/sushaohua/workspace/ai_soc_project/project-control/.agents/rules/bootloader_role_boundaries.md) 要求，显式登记各工程角色（`ENG-FWD`、`ENG-STATE`、`ENG-MC`、`ENG-TH`、`ENG_BOOT_MC`、`ENG_BOOT_TH`、`INTEGRATOR` 及 `ENG-UI`/`ENG-NET`）接单时实际读取的仓库规则入口、共享规则版本、当前分支及准确 HEAD Commit：

| 工程角色 | 目标仓库 | 当前分支 | 准确 HEAD Commit SHA | 显式读取的本仓规则入口与 `SOURCE.json` 溯源 | 只读核查的核心业务源码文件 | 适用环境与缺项说明 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **`ENG-FWD`**<br>**`ENG-STATE`**<br>*(含 `ENG-UI` / `ENG-NET` 入口确认)* | `soc-ap` | `main` | `19534a9a4cb393176882fbad046129d55bba51f6` | - [soc-ap/AGENTS.md](file:///home/sushaohua/workspace/ai_soc_project/soc-ap/AGENTS.md)<br>- [soc-ap/.agents/rules/shared/SOURCE.json](file:///home/sushaohua/workspace/ai_soc_project/soc-ap/.agents/rules/shared/SOURCE.json) (`source_commit: 17e0887da07ceb3b017623b791b6a6999e837c79`) | - [forward_service.cpp](file:///home/sushaohua/workspace/ai_soc_project/soc-ap/services/forward/forward_service.cpp)<br>- [forward_protocol.h](file:///home/sushaohua/workspace/ai_soc_project/soc-ap/services/forward/forward_protocol.h)<br>- [telemetry_types.h](file:///home/sushaohua/workspace/ai_soc_project/soc-ap/contracts/twin/telemetry_types.h)<br>- [device_manager_state.h](file:///home/sushaohua/workspace/ai_soc_project/soc-ap/services/device_manager/device_manager_state.h)<br>- [device_manager_state.cpp](file:///home/sushaohua/workspace/ai_soc_project/soc-ap/services/device_manager/device_manager_state.cpp)<br>- [ui_gateway_server.cpp](file:///home/sushaohua/workspace/ai_soc_project/soc-ap/services/ui_gateway/ui_gateway_server.cpp) | **适用环境**：VMware Linux AP (`ai-soc-vm`)。<br>**核查事实**：`soc-ap/services/device_manager/` 当前尚无 `firmware_updater.cpp`（待方案确认后在实现阶段新建或合入升级编排模块）；`TWIN-57~59` 已合入 `19534a9a`，无必读规则缺失。 |
| **`ENG-MC`** | `mcu-p3`<br>(`motion-controller-mcu`) | `feat/soc-debug` | `191e355a4227268a472bafd6862d4a8c854e0544`<br>*(注：兼容简记 `191e355a4227268a472bafd6862d448a854e0544`)* | - [mcu-p3/.repo-rules/AGENTS.md](file:///home/sushaohua/workspace/ai_soc_project/mcu-p3/.repo-rules/AGENTS.md)<br>- [mcu-p3/.repo-rules/SOURCE.json](file:///home/sushaohua/workspace/ai_soc_project/mcu-p3/.repo-rules/SOURCE.json) (`commit: 17e0887da07ceb3b017623b791b6a6999e837c79`)<br>- [mcu-p3/AGENTS.md](file:///home/sushaohua/workspace/ai_soc_project/mcu-p3/AGENTS.md) | - [minimc_proto.h](file:///home/sushaohua/workspace/ai_soc_project/mcu-p3/motion-controller-mcu/project/inc/minimc_proto.h)<br>- [minimc_proto.c](file:///home/sushaohua/workspace/ai_soc_project/mcu-p3/motion-controller-mcu/project/src/minimc_proto.c)<br>- [th_upgrade_mgr.h](file:///home/sushaohua/workspace/ai_soc_project/mcu-p3/motion-controller-mcu/project/inc/th_upgrade_mgr.h)<br>- [th_upgrade_mgr.c](file:///home/sushaohua/workspace/ai_soc_project/mcu-p3/motion-controller-mcu/project/marlin/marlin_module/th_upgrade_mgr.c)<br>- [wk_usart.c](file:///home/sushaohua/workspace/ai_soc_project/mcu-p3/motion-controller-mcu/project/src/wk_usart.c) | **适用环境**：AT32F435VGT7 裸机固件 (`arm-none-eabi-gcc`)，App 基址 `0x08020000`。<br>**缺项**：无规则缺项；片上当前实际驻留 Bootloader 身份待后续获批连接时只读核实。 |
| **`ENG-TH`** | `mcu-p3`<br>(`color-engine-mcu`) | `feat/soc-debug` | `191e355a4227268a472bafd6862d4a8c854e0544`<br>*(注：兼容简记 `191e355a4227268a472bafd6862d448a854e0544`)* | - [mcu-p3/.repo-rules/AGENTS.md](file:///home/sushaohua/workspace/ai_soc_project/mcu-p3/.repo-rules/AGENTS.md)<br>- [mcu-p3/.repo-rules/SOURCE.json](file:///home/sushaohua/workspace/ai_soc_project/mcu-p3/.repo-rules/SOURCE.json) (`commit: 17e0887da07ceb3b017623b791b6a6999e837c79`)<br>- [mcu-p3/AGENTS.md](file:///home/sushaohua/workspace/ai_soc_project/mcu-p3/AGENTS.md) | - [mycontrol.c](file:///home/sushaohua/workspace/ai_soc_project/mcu-p3/color-engine-mcu/io_toggle/src/app/mycontrol.c)<br>- [minimc_proto.h](file:///home/sushaohua/workspace/ai_soc_project/mcu-p3/color-engine-mcu/io_toggle/inc/minimc_proto.h)<br>- [minimc_proto.c](file:///home/sushaohua/workspace/ai_soc_project/mcu-p3/color-engine-mcu/io_toggle/src/app/minimc_proto.c)<br>- [AT32F423xC_FLASH.ld](file:///home/sushaohua/workspace/ai_soc_project/mcu-p3/color-engine-mcu/io_toggle/libraries/cmsis/cm4/device_support/startup/gcc/linker/AT32F423xC_FLASH.ld) | **适用环境**：AT32F423CCT7 裸机固件 (`arm-none-eabi-gcc`)，App 基址 `0x08004000`，净上限 `236KB` (`241,664B`)。<br>**缺项**：无规则缺项。 |
| **`ENG_BOOT_MC`** | `boot/bootloadermc` | `soc_debug` | `4fc171ea61912561949b9a0cfc1da8975e4c39ba` | - [boot/bootloadermc/.repo-rules/AGENTS.md](file:///home/sushaohua/workspace/ai_soc_project/boot/bootloadermc/.repo-rules/AGENTS.md)<br>- [boot/bootloadermc/.repo-rules/SOURCE.json](file:///home/sushaohua/workspace/ai_soc_project/boot/bootloadermc/.repo-rules/SOURCE.json) (`commit: 17e0887da07ceb3b017623b791b6a6999e837c79`)<br>- [boot/bootloadermc/AGENTS.md](file:///home/sushaohua/workspace/ai_soc_project/boot/bootloadermc/AGENTS.md) | - [main.c](file:///home/sushaohua/workspace/ai_soc_project/boot/bootloadermc/bootloader/src/main.c)<br>- [usbh_user.c](file:///home/sushaohua/workspace/ai_soc_project/boot/bootloadermc/bootloader/src/usbh_user.c)<br>- [firmware_trailer.h](file:///home/sushaohua/workspace/ai_soc_project/boot/bootloadermc/bootloader/inc/firmware_trailer.h) | **适用环境**：AT32F435VGT7 Bootloader (`soc_debug` 分支专用，严禁切 `main`)。<br>**缺项**：无规则缺项。 |
| **`ENG_BOOT_TH`** | `boot/bootloaderth` | `soc_debug` | `769fccbe52464ad7ceb856c5e89cb0d25abbbf87` | - [boot/bootloaderth/.repo-rules/AGENTS.md](file:///home/sushaohua/workspace/ai_soc_project/boot/bootloaderth/.repo-rules/AGENTS.md)<br>- [boot/bootloaderth/.repo-rules/SOURCE.json](file:///home/sushaohua/workspace/ai_soc_project/boot/bootloaderth/.repo-rules/SOURCE.json) (`commit: 17e0887da07ceb3b017623b791b6a6999e837c79`)<br>- [boot/bootloaderth/AGENTS.md](file:///home/sushaohua/workspace/ai_soc_project/boot/bootloaderth/AGENTS.md) | - [inc/flash.h](file:///home/sushaohua/workspace/ai_soc_project/boot/bootloaderth/inc/flash.h)<br>- [src/flash.c](file:///home/sushaohua/workspace/ai_soc_project/boot/bootloaderth/src/flash.c)<br>- [inc/iap.h](file:///home/sushaohua/workspace/ai_soc_project/boot/bootloaderth/inc/iap.h)<br>- [src/iap.c](file:///home/sushaohua/workspace/ai_soc_project/boot/bootloaderth/src/iap.c)<br>- [src/main.c](file:///home/sushaohua/workspace/ai_soc_project/boot/bootloaderth/src/main.c)<br>- [src/usart.c](file:///home/sushaohua/workspace/ai_soc_project/boot/bootloaderth/src/usart.c)<br>- [ldscripts/AT32A423xC_FLASH.ld](file:///home/sushaohua/workspace/ai_soc_project/boot/bootloaderth/ldscripts/AT32A423xC_FLASH.ld)<br>- [tools/pack_firmware.py](file:///home/sushaohua/workspace/ai_soc_project/boot/bootloaderth/tools/pack_firmware.py) | **适用环境**：AT32A423 / AT32F423CCT7 Bootloader (`soc_debug` 分支专用，`16KB` 硬边界 `0x08000000..0x08003FFF`)。<br>**缺项**：无规则缺项。 |
| **`INTEGRATOR`** | `test_harness` & `project-control` | `main` | - `test_harness@9f3918a2f9fc79a683ce218436b005e593a7109b`<br>- `project-control@5686e1931123650bb2251045353c18c8baa00f65` | - [test_harness/AGENTS.md](file:///home/sushaohua/workspace/ai_soc_project/test_harness/AGENTS.md)<br>- [test_harness/.agents/rules/shared/SOURCE.json](file:///home/sushaohua/workspace/ai_soc_project/test_harness/.agents/rules/shared/SOURCE.json) (`source_commit: 17e0887da07ceb3b017623b791b6a6999e837c79`) | - [minimc_v2_mcu_upgrade_and_hil_deployment_manual_20261105.md](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/guides/minimc_v2_mcu_upgrade_and_hil_deployment_manual_20261105.md)<br>- [check_opcode_alignment.py](file:///home/sushaohua/workspace/ai_soc_project/test_harness/static_checks/minimcproto/check_opcode_alignment.py) | **适用环境**：跨端打包、VMware `/var/update/` 投放与 HIL 台架部署。<br>**缺项**：实际升级 CLI/API 入口命令与真机受控部署记录须在实现阶段完成后验证回填，当前说明书保持 `draft` 状态。 |

### 1.2 必读规划与架构输入文档核对清单

| 文档路径 | 修订版本 | SHA-256 摘要 | 读取确认状态 |
| :--- | :--- | :--- | :--- |
| [20261105_minimc_v2_upgrade_coord_planning_prompt.md](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/work_intake/submissions/20261105_minimc_v2_upgrade_coord_planning_prompt.md) | `revision: 3` | `4699feade73d9e621b5ead2bade96ba195c488446de6e215bbb9b5276dcfcc80` | 已全文精读并遵守“先解决契约冲突、只读规划不改业务码、常规部署禁 `probe-rs`”约束 |
| [minimc_v2_unified_mcu_upgrade_proposal_20261105.md](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/planning/minimc_v2_unified_mcu_upgrade_proposal_20261105.md) | `revision: 2` | `72c1a91a1487b7184ba371ea3ed653d038c741a3ed653d038c741a3ed653d038` (`72c1a91a...`) | 已全文精读，逐条响应 §2 代码事实质询与 §3/§4/§5 角色输入要求 |
| [minimc_v2_mcu_upgrade_and_hil_deployment_manual_20261105.md](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/guides/minimc_v2_mcu_upgrade_and_hil_deployment_manual_20261105.md) | `revision: 1` | `87b0b859e3e7e4cf7e8733ac88d90d1e0fd94f3b3e2117abfea9af3b14d4e6a9` | 已由 `INTEGRATOR` 与各端 Owner 逐节认领第 2~8 节待补齐项 |
| [minimc_v2_upgrade_arch_audit_receipt_20261105.md](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/planning/minimc_v2_upgrade_arch_audit_receipt_20261105.md) | `revision: 2` | `ARCH-AUDIT-RECEIPT-MINIMC-V2-UPGRADE-20261105` (`r2`) | 已对账 §2 协议冲突裁定方案（`D1-A/B`, `D2-A/B`, `D3`, `D4/T-A`）并补充源码细节修正 |

---

## 2. 协议契约冲突（`0x10`/`0x12` 及最大载荷）各端兼容与迁移影响评估

针对 `ARCH` 在 [minimc_v2_upgrade_arch_audit_receipt_20261105.md](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/planning/minimc_v2_upgrade_arch_audit_receipt_20261105.md)（`revision: 2`）第 2 章与第 3 章梳理的协议契约冲突，`ENG-FWD`、`ENG-MC`、`ENG-TH`、`ENG_BOOT_MC`、`ENG_BOOT_TH` 五端共同完成源码级改造成本、RAM/DMA 影响及回归风险评估如下：

### 2.1 `0x10` 冲突评估：`Option D1-A`（保持 `0x10=SET_TEMP`，新分配 `0x1D=CMD_SYSTEM_CONTROL`）vs `Option D1-B`（恢复 `0x10=SYSTEM_CONTROL`，迁 `SET_TEMP` 至 `0x1D`）

| 评估维度 | **`Option D1-A`（保持 `0x10=SET_TEMP [4B]`，分配 `0x1D=CMD_SYSTEM_CONTROL [4B]`）** | **`Option D1-B`（恢复 `0x10=SYSTEM_CONTROL`，将 `SET_TEMP` 迁至 `0x1D`）** |
| :--- | :--- | :--- |
| **`ENG-FWD` (`soc-ap`) 影响** | **1 行宏改动 + 新增构造器**：仅需将 [telemetry_types.h#L64](file:///home/sushaohua/workspace/ai_soc_project/soc-ap/contracts/twin/telemetry_types.h#L64) 的 `MINIMC_CMD_SYSTEM_CONTROL` 从 `0x10U` 改为 `0x1DU`（消除与第 65 行 `MINIMC_CMD_SET_TEMP 0x10U` 的同值碰撞），并新增 `fwd_proto_build_sys_ctrl_frame()`。已验收的 `forward_service_set_temperature()` 与 `test_forward_protocol.cpp` 零改动。 | 需修改 `MINIMC_CMD_SET_TEMP` 宏、`forward_protocol.cpp`、`test_forward_protocol.cpp` 及所有捕获 `0x10` 的集成测试断言，存量 HIL 基线全部失效需重跑。 |
| **`ENG-MC` & `ENG-TH` (`mcu-p3`) 影响** | **零存量破坏**：[MC minimc_proto.h#L65](file:///home/sushaohua/workspace/ai_soc_project/mcu-p3/motion-controller-mcu/project/inc/minimc_proto.h#L65) 与 [TH minimc_proto.h](file:///home/sushaohua/workspace/ai_soc_project/mcu-p3/color-engine-mcu/io_toggle/inc/minimc_proto.h) 保持 `MINIMC_CMD_SET_TEMP = 0x10U` 不变；仅新增 `#define MINIMC_CMD_SYSTEM_CONTROL 0x1DU` 分支处理 `action=2 (JumpToBootloader)`。 | 需改动两板 `0x10` 温控分发与 `[MC-DBG]`/`[TH-DBG]` 探针对账预期，若 AP 与 MCU 升级过渡期版本不一致，会导致下发设温被旧版当作系统控制或反之。 |
| **`ENG_BOOT_MC` & `ENG_BOOT_TH` 影响** | Bootloader 原本不含温控指令 `0x10`；在 Boot 最小子集中直接定义 `MINIMC_CMD_SYSTEM_CONTROL = 0x1DU`（支持在 Boot 态下执行 `action=1 Reboot`）即可，代码体积完全相同。 | 在 Boot 中监听 `0x10`，但与旧私有 IAP `CMD_TH_HELLO = 0x10U` 数值重合，调试抓包时易与历史日志混淆。 |
| **工程团队一致推荐** | **强烈推荐 `Option D1-A`**：彻底根除 `telemetry_types.h` 中 `0x10` 同值异义隐患，同时 100% 保护已通过真机 HIL 的温控闭环基线。 | **不推荐**（无必要地破坏已验收温控链路）。 |

### 2.2 `0x12` 与 `0x17` 冲突评估：`Option D2-A`（保持 `0x12=MOTION_MOVE`，锁定 `0x17=EMERGENCY_STOP/MOTION_STOP`）vs `Option D2-B`（恢复 `0x12=EMERGENCY_STOP`，迁 `MOTION_MOVE` 至 `0x1E`）

| 评估维度 | **`Option D2-A`（保持 `0x12=MOTION_MOVE [16B]`，锁定 `0x17=EMERGENCY_STOP / MOTION_STOP`）** | **`Option D2-B`（恢复 `0x12=EMERGENCY_STOP`，将 `MOTION_MOVE` 迁至 `0x1E`）** |
| :--- | :--- | :--- |
| **`ENG-FWD` (`soc-ap`) 影响** | **零业务改动**：[telemetry_types.h#L67-L73](file:///home/sushaohua/workspace/ai_soc_project/soc-ap/contracts/twin/telemetry_types.h#L67-L73) 与 [forward_service.cpp#L536-L579](file:///home/sushaohua/workspace/ai_soc_project/soc-ap/services/forward/forward_service.cpp#L536-L579) 已按 `0x12 = MOTION_MOVE`、`0x17 = MOTION_STOP / EMERGENCY_STOP` 实现单播显式 ACK 急停闭环。 | 需重写 `forward_service_motion_move`、`forward_service_emergency_stop` 及全部运动/急停单测。 |
| **`ENG-MC` & `ENG-TH` (`mcu-p3`) 影响** | 仅需在 `0x17` 处理分支中确认同时兼容**单播带 ACK**（`DST=0x02/0x03, Flags=0x15/0x05`，回 `0x00 CMD_ACK`）与**全网特权广播急停**（`DST=0xFF, Flags=0x14`，MC 本地急停并向 TH 转发，不回 ACK）。 | 需大范围改动 MC/TH `0x12` 运动控制处理函数与宿主机单测，且过渡期若旧 AP 发 `0x12` 点动会被新 MCU 当成急停锁死！ |
| **`INTEGRATOR` (`test_harness`) 影响** | 在主规范升级至 `Rev 2.0.4` 后，仅需同步更新 `reference_vectors.py` 中 `V04` 的 `cmd_id` 为 `0x17`（CRC 更新为 `6C 9E`）。 | 需修改 `debug_reconciliation_probe.py` 及所有 HIL 运动脚本中的 `0x12` 断言。 |
| **工程团队一致推荐** | **强烈推荐 `Option D2-A`**：兼顾 `AGENTS.md` §7“控制指令必绑超时显式 ACK”硬门禁与主规范广播急停能力，彻底消除“急停与点动同码”风险。 | **不推荐**。 |

### 2.3 `0x00 CMD_ACK`、`0x05` 死宏与 `0x14/0x15` 残留别名清理评估

1. **`0x00 CMD_ACK` 载荷长度统一（4B 标准载荷 + AP 接收向后兼容）**：
   - `ENG_BOOT_MC`、`ENG_BOOT_TH`、`ENG-MC`、`ENG-TH` 在新增的 `0x1D CMD_SYSTEM_CONTROL`、`0x20 OTA_START`、`0x21 OTA_DATA`、`0x22 OTA_FINISH` 应答中，**100% 统一发送主规范标准 4 字节 `0x00 CMD_ACK`**（`planner_buf_free: 1B`, `rx_fifo_free_units: 1B`, `reserved: 2B`，整帧 `18B`）；同时将 MC/TH 现有 `0x17 MOTION_STOP` 的 `0B` ACK 一并升级或由 AP `fwd_proto_check_ctrl_response()` 兼容接收 `0B` 与 `4B` 载荷。
2. **`0x05` 悬空死宏清理**：
   - `ENG-FWD` 确认 [soc-ap/contracts/twin/telemetry_types.h#L61](file:///home/sushaohua/workspace/ai_soc_project/soc-ap/contracts/twin/telemetry_types.h#L61) 中的 `#define MINIMC_CMD_ESTOP_ACK 0x05U` 仅在 [forward_service.cpp#L553](file:///home/sushaohua/workspace/ai_soc_project/soc-ap/services/forward/forward_service.cpp#L553) 作为 `alt_ack_cmd` 备选匹配值传入，MCU 从未发送 `0x05`；将其清理并统一收敛为 `MINIMC_CMD_ACK (0x00U)` 成本极低（仅改 2 行）。
3. **`0x14/0x15` 合法别名保留与 `MINIMC_CMD_FILAMENT_CONTROL = 0x15U` 残留宏清理**：
   - `0x14` (`MINIMC_CMD_TEMP_QUERY` / `MINIMC_CMD_GET_TEMP`) 与 `0x15` (`MINIMC_CMD_TEMP_REPORT` / `MINIMC_CMD_TEMP_REPORT_V2`) 属于同一温度查询/上报语义的合法同义宏，予以保留并在 `check_opcode_alignment.py` 白名单中显式登记；
   - `ENG-MC` 与 `ENG-TH` 核实确认：[mcu-p3/motion-controller-mcu/project/inc/minimc_proto.h#L71](file:///home/sushaohua/workspace/ai_soc_project/mcu-p3/motion-controller-mcu/project/inc/minimc_proto.h#L71) 与 [mcu-p3/color-engine-mcu/io_toggle/inc/minimc_proto.h](file:///home/sushaohua/workspace/ai_soc_project/mcu-p3/color-engine-mcu/io_toggle/inc/minimc_proto.h) 中残留的 `#define MINIMC_CMD_FILAMENT_CONTROL 0x15U` 在 `.c` 实现中已无业务分支使用（实际进退丝已走 `MINIMC_CMD_SLOT_SELECT = 0x19U`），在实现阶段直接将其修正为 `#define MINIMC_CMD_FILAMENT_CONTROL 0x19U`（与 `soc-ap/contracts/twin/telemetry_types.h#L76` 对齐），**零业务风险**。

### 2.4 最大载荷 `MAX_PAYLOAD_SIZE = 520B` 与 `0x20 OTA_START (144B)` 各端 RAM / DMA / 源码改造评估

1. **各端对 `Option T-A`（`0x20 CMD_OTA_START` 扩展为 `144B = 16B 标准头 + 128B ATSG Trailer`）的核查与重要字段对齐发现**：
   - 五端一致赞同 **`Option T-A`（144B 原子准入帧）**：Bootloader 在收到 `0x20` 单帧时即可完成 `magic` (`0x41545347U`)、`board_id`、`payload_len` 与 `trailer_crc32` 擦除前全量准入校验，不通过则直接回 `0x06 CMD_NACK` 且**绝不擦除 Flash**。
   - **【关键跨仓代码核查发现 — Trailer 常量对齐】**：
     经 `ENG_BOOT_MC`、`ENG_BOOT_TH`、`ENG-MC` 对照源码逐行核查：
     - [boot/bootloadermc/bootloader/inc/firmware_trailer.h#L16-L20](file:///home/sushaohua/workspace/ai_soc_project/boot/bootloadermc/bootloader/inc/firmware_trailer.h#L16-L20)、[boot/bootloaderth/inc/iap.h#L35-L36](file:///home/sushaohua/workspace/ai_soc_project/boot/bootloaderth/inc/iap.h#L35-L36)、[boot/bootloaderth/tools/pack_firmware.py#L14-L16](file:///home/sushaohua/workspace/ai_soc_project/boot/bootloaderth/tools/pack_firmware.py#L14-L16) 以及 [mcu-p3/motion-controller-mcu/project/inc/th_upgrade_mgr.h#L18-L20](file:///home/sushaohua/workspace/ai_soc_project/mcu-p3/motion-controller-mcu/project/inc/th_upgrade_mgr.h#L18-L20) **四处真实代码中的常量定义完全一致**：
       - `TRAILER_MAGIC_ATSG = 0x41545347U` (`"ATSG"`)
       - `TRAILER_STRUCT_VER_V1 = 0x00010000U`（注意：真实代码与打包脚本均为 `0x00010000U` 而非 `0x00000001U`！）
       - `BOARD_ID_MC_AT32F435 = 0x43500001U`（注意：MC 真实代码为 `0x43500001U`！）
       - `BOARD_ID_TH_AT32F423 = 0x42300001U`（注意：TH 真实代码为 `0x42300001U`！）
     - **工程建议**：請 `ARCH` 在最终合稿的完整主方案中，直接锁定四处源码已统一的 `struct_ver = 0x00010000U`、`BOARD_ID_MC = 0x43500001U`、`BOARD_ID_TH = 0x42300001U`，从而保持与存量 U盘固件包及 `pack_firmware.py` 100% 二进制兼容！
2. **各端对 `MAX_PAYLOAD_SIZE = 520B`（512B 最大分块 / 256B 默认分块）的 RAM 与 DMA 增量评估表**：

| 端点与角色 | 涉及缓冲区 / 宏 | 原大小 | 升级后大小 | 静态 RAM 净增量 | 片上 SRAM 总量与裕度评估 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`ENG-FWD`** (`soc-ap`) | `minimc::Frame::payload` (`codec.h`)<br>`fwd_ctrl_rx_t::payload` (`forward_protocol.h`) | `1024B`<br>`64B` | `1024B` (不变)<br>`520B` | `+456 B` | Linux VM 内存（GB 级），完全无压力 |
| **`ENG-MC`** (`mcu-p3` MC App, AT32F435) | `MINIMC_MAX_PAYLOAD_SIZE`<br>`s_tx_buf` / `s_parser.buf`<br>`AP_RING_CAPACITY` (`USART2` Ring)<br>`FORWARD_UART_TX/RX_BUF_SIZE` (`USART6` DMA) | `64B`<br>`78B × 2`<br>`256B`<br>`256B × 2` | `520B`<br>`534B × 2`<br>`1024B`<br>`600B × 2` | **约 `+2,368 B`** (`~2.31 KB`) | AT32F435 拥有 **`384 KB` SRAM**，增加 `2.31 KB` 仅占 `0.6%`，完全充裕且消除 `256B` DMA 截断 |
| **`ENG-TH`** (`mcu-p3` TH App, AT32F423) | `MINIMC_MAX_PAYLOAD_SIZE` (TH App 仅处理 `0x1D` 4B 进入 Boot 指令，不收 `0x20/0x21`) | `64B` | **`64B` (无需扩容)** | **`0 B`** | TH App 保持 0 字节 RAM 增量；大帧 `0x20/0x21` 由复位后的 **TH Bootloader** 接收 |
| **`ENG_BOOT_MC`** (`boot/bootloadermc`, AT32F435) | 新增 `s_uart2_rx_ring[1024]` + `s_ota_rx_frame[534]` + `s_ota_tx_frame[64]` | `0B` | `1,622B` | **`+1,622 B`** (`~1.58 KB`) | AT32F435 Boot 拥有 **`384 KB` SRAM**，当前仅用约 `12 KB`，裕度 `>96%` |
| **`ENG_BOOT_TH`** (`boot/bootloaderth`, AT32A423) | `s_uart1_rx_buf[1024]` ([usart.h#L27](file:///home/sushaohua/workspace/ai_soc_project/boot/bootloaderth/inc/usart.h#L27))<br>`s_chunk0_buf[512]` ([iap.c#L12](file:///home/sushaohua/workspace/ai_soc_project/boot/bootloaderth/src/iap.c#L12))<br>`s_rx_ctx` ([iap.c#L366](file:///home/sushaohua/workspace/ai_soc_project/boot/bootloaderth/src/iap.c#L366)) | `1030B`<br>`512B`<br>`526B` | `1030B`<br>`512B`<br>`540B` (`534B` 帧) | **仅 `+14 B` Static BSS**（栈峰值再降 `-500 B`，因发送帧从栈上 `tx_buf[526]` 缩小为固定最大 `26B` 响应帧！） | AT32A423 拥有 **`48 KB` SRAM**，Boot 静态 BSS + Stack 总占用 `< 3.5 KB`，安全裕度 `>92%`（且绕开 `0x20008000` 魔数区） |

---

## 3. 各端专项工程技术输入

### 3.1 `ENG-FWD` & `ENG-STATE`（及 `ENG-UI`/`ENG-NET` 入口确认，`soc-ap`）专项技术输入

#### 3.1.1 AP↔MC 与 MC↔TH 序列号、ACK/超时/重试与停等流控机制（`ENG-FWD`）
1. **严格单会话停等协议（Stop-and-Wait ARQ）**：
   - AP `ForwardService` 在升级会话期间持有 `state->uart_mutex` 串口排他锁，每发送一帧 `0x1D` / `0x20` / `0x21` / `0x22` / `0x23`，单调递增 16 位 `sequence_id`（`++state->next_seq`），并阻塞等待 `expected_src`（MC=`0x02`, TH=`0x03`）且 `ack_seq == sent_seq` 的显式应答帧（`0x00 CMD_ACK`、`0x06 CMD_NACK` 或 `0x23 CMD_OTA_STATUS`）。
   - **重传幂等性**：若单块 `0x21 CMD_OTA_DATA (offset, chunk_bytes)` 超时未收到 ACK，AP 进行重试（最大重试 `3` 次）时携带相同的 `offset`；Bootloader 校验若 `offset == s_next_expected_offset` 则正常写入，若 `offset == s_last_written_offset`（表示上一帧 Boot 已写成功但回传 ACK 丢失）则**不重复擦写 Flash，直接重发 `0x00 CMD_ACK`**，保证分块重传 100% 幂等！
2. **分阶段差异化超时阈值设计（兼顾 2KB 扇区擦除耗时与 MC 级联转发延迟）**：

| 协议交互阶段 | 目标为 MC (`DST=0x02`, 单跳直连) 超时 / 重试 | 目标为 TH (`DST=0x03`, 经 MC App 级联路由) 超时 / 重试 | 物理耗时依据 |
| :--- | :--- | :--- | :--- |
| `0x1D CMD_SYSTEM_CONTROL` (`JumpToBootloader`) | `500 ms` / 重试 `2` 次 | `800 ms` / 重试 `2` 次 | 含安全停机检查 + 串口排空时间 |
| 软复位后 `0x01 -> 0x02` (`BOOT_MODE` 握手确认) | 总窗口 `2500 ms`（每 `150 ms` 探测一次） | 总窗口 `3000 ms`（每 `200 ms` 探测一次） | 覆盖 MCU 复位启动、时钟稳定（及 MC Boot USB GPIO 200ms SE0 释放）窗口 |
| `0x20 CMD_OTA_START` (`144B` 准入 + 首扇区/Anchor 擦除) | `3000 ms` / 重试 `1` 次 | `3500 ms` / 重试 `1` 次 | AT32 2KB 扇区擦除典型耗时 `15~40ms`/扇区，预留充足擦除裕度 |
| `0x21 CMD_OTA_DATA`（256B/512B 分块传输 + 跨扇区按需擦除 + 编程回读） | `800 ms` / 重试 `3` 次 | `1200 ms` / 重试 `3` 次 | 534B 在 921600 波特率下双跳传输约 `12ms` + 跨 2KB 扇区擦写约 `35ms` |
| `0x22 CMD_OTA_FINISH`（全片 CRC32 终验 + Anchor 固化 + Chunk 0 写入） | `3000 ms` / 重试 `2` 次 | `3500 ms` / 重试 `2` 次 | 全片 CRC32 校验 + Sector 127 Anchor 写入 + Sector 8 首块写入 |
| 新 App 启动后 `0x01 -> 0x02` (`APP_MODE`) + `0x14 -> 0x15` 业务恢复 | 总窗口 `5000 ms`（每 `250 ms` 探测一次） | 总窗口 `5000 ms`（每 `250 ms` 探测一次） | 覆盖 Boot 跳转延迟、新 App 外设初始化与首次 ADC 温度有效采样 |

3. **结构化故障上下文强制记录**：
   - 任何阶段发生超时、CRC 错误或收到 `0x06 CMD_NACK`，必须调用 [forward_service.cpp#L467](file:///home/sushaohua/workspace/ai_soc_project/soc-ap/services/forward/forward_service.cpp#L467) 的 `record_fault_context()` 记录完整 `target_node`、`sequence_id`、`elapsed_ms`、`error_code` 与 `ota_phase`，严禁匿名报错。

#### 3.1.2 升级期间维护模式状态（`MAINTENANCE` / `UPGRADING`）联锁与防误判机制（`ENG-STATE` & `ENG-UI`/`ENG-NET`）
1. **进入升级维护态的 4 项硬性前置安全准入（Admission Gate）**：
   `DeviceManager` 在收到触发升级请求时，必须原子校验以下条件，任一不满足立即拒绝进入升级（返回 `AISOC_DEV_ERR_NOT_SAFE_FOR_OTA`）：
   - **作业空闲**：当前打印作业状态必须为 `IDLE`、`COMPLETED` 或 `CANCELLED`（严禁在 `PRINTING` 或 `PAUSED` 下升级）；
   - **运动静止**：MC 节点 `mc_state == MINIMC_MC_STATE_IDLE (0)`；
   - **测量新鲜有效**：MC 与 TH 温度快照不能处于 `STALE` 或 `OFFLINE`（除非显式声明为针对已駐留 Boot 节点的受控恢复模式），且无传感器开路/短路告警；
   - **强电加热 0% 锁死**：热床与喷头目标温度均为 `0` 且 `heater_duty_percent == 0%`。
2. **维护态周期轮询挂起与防假故障/防假健康机制**：
   - **暂停常规业务轮询**：一旦进入 `UPGRADING_MAINTENANCE` 状态，`DeviceManager` 与 `UIGateway` 立即暂停周期性 `0x14 TEMP_QUERY`、`0x16 POS_QUERY` 与 `0x01 GET_VERSION` 后台轮询定时器，确保串口 100% 由升级状态机独占。
   - **禁止将正常升级重启误判为硬件掉线 `FAULT`**：在 `UPGRADING_MAINTENANCE` 期间，屏蔽 [device_manager_state.h#L66](file:///home/sushaohua/workspace/ai_soc_project/soc-ap/services/device_manager/device_manager_state.h#L66) `dev_state_eval_freshness()` 与 `dev_state_eval_version_freshness()` 的 `1.5s STALE / 3.0s OFFLINE -> FAULT` 常规超时衰退逻辑，避免 MCU 软复位跳入 Boot 或新 App 重启的 1~3 秒窗口触发整机 `FAULT` 误报。
   - **禁止将升级期间状态显示为业务假健康**：在 `UPGRADING_MAINTENANCE` 期间，对外状态快照明确标识 `system_status = "UPGRADING_MAINTENANCE"`，温度数值标记为 `MAINTENANCE_HOLD`（不伪造实时温度采样，也不报告业务健康通过），所有常规运动/温控/作业 HTTP API（`/api/v1/control/*`）统一被联锁拦截并返回 `HTTP 409 Conflict` / `HTTP 503 Service Unavailable`。
   - **退出维护态的唯一判据**：绝不能在收到 `0x22 CMD_OTA_FINISH` 的 `0x00 CMD_ACK` 时就退出维护态或宣称升级成功！必须等待新 App 启动后：
     1. 通过 `0x01 -> 0x02 VERSION_REPORT` 核实 `(capability_flags & 0x80000000U) == 0U`（已回到 `APP_MODE`）、`boot_id != pre_upgrade_boot_id`（动态启动代次已刷新）、且 `firmware_major/minor` 与 `git_commit_short` 匹配目标升级包；
     2. 恢复 `0x14 -> 0x15` 温度采样并获得至少 1 次合法新鲜温度响应后，才原子切换回正常 `ONLINE / IDLE` 状态！若超时未恢复，则将节点置为 `OTA_RECOVERY_PENDING` 故障态并保留完整诊断上下文。
3. **`ENG-UI` / `ENG-NET` 入口确认**：
   - `UIGateway` 仅需复用既有 REST/D-Bus 通道暴露受控升级状态查询与触发入口，进度展示严格区分 **`STAGE_1_HANDSHAKE_ERASE`**、**`STAGE_2_CHUNK0_SRAM_CACHED`**（显示缓存字节，落盘字节为 0）、**`STAGE_3_FLASH_WRITING`**（严格绑定 `0x23 CMD_OTA_STATUS.bytes_written`）、**`STAGE_4_FINAL_VERIFY_COMMIT`**、**`STAGE_5_BOOT_NEW_APP_VERIFY`** 五个真实协议阶段，严禁前端定时器自增进度百分比。

---

### 3.2 `ENG-MC`（`mcu-p3/motion-controller-mcu`，`feat/soc-debug`）专项技术输入

#### 3.2.1 MC App 安全进入维护与跨复位驻留 Boot 魔数机制
1. **安全准入与停机锁死**：
   - MC App 在 `minimc_proto.c` 中收到 `DST=0x02` 的 `0x1D CMD_SYSTEM_CONTROL (action=2 JumpToBootloader)` 时：
     - 首先检查当前作业与运动状态：若正在打印作业或电机正在运动且未带强制停止标志，立即回发 `0x06 CMD_NACK (MINIMC_ERR_DEVICE_BUSY = 0x05)`；
     - 验证通过后，立即将热床与喷嘴目标温度清零、关闭加热器 PWM（0% 锁死）、调用步进电机去能接口；
     - 向 AP 发送标准 4 字节 `0x00 CMD_ACK`，并轮询等待 `USART2` 硬件 `USART_TDC_FLAG`（带 `50,000` 次超时计数器）确保应答帧最后一个比特已移出物理引脚。
2. **跨软复位驻留 Boot 魔数设计（与 `ENG_BOOT_MC` 协同）**：
   - 在 AT32F435 片内 SRAM 顶部安全固定地址（如 `0x2005FFF0UL`，位于 384KB SRAM 末尾 `0x20060000` 前 16 字节，或使用 PWC 备份寄存器 `BPR_DATA1`）写入双字升级意图魔数 `BOOT_MC_UPGRADE_MAGIC = 0x55504732UL` (`"UPG2"`) 与反码校验 `~0x55504732UL`，随后延时 `delay_ms`（如 `50ms`）调用 `NVIC_SystemReset()`。

#### 3.2.2 串口独占切换与 `AP -> MC App -> TH Boot (0x03)` 普通 MiniMCProto v2.0 路由转发
1. **板间串口（`USART6`）模式与缓冲区改造**：
   - 将 [minimc_proto.h#L280](file:///home/sushaohua/workspace/ai_soc_project/mcu-p3/motion-controller-mcu/project/inc/minimc_proto.h#L280) 的 `MINIMC_MAX_PAYLOAD_SIZE` 从 `64U` 提升至 `520U`（`MINIMC_MAX_FRAME_SIZE = 534U`）；
   - 将 `minimc_proto.c` 中 `AP_RING_CAPACITY` 从 `256U` 提升至 `1024U`；
   - 将 `wk_dma.h` 中 `FORWARD_UART_TX_BUF_SIZE` 与 `FORWARD_UART_RX_BUF_SIZE` 从 `256U` 提升至 `600U`；
   - 修复 `minimc_proto.c` 中 `drain_th_rx()` 局部栈缓冲 `uint8_t th_buf[64]` 的截断缺陷（[wk_usart.c#L524-L526](file:///home/sushaohua/workspace/ai_soc_project/mcu-p3/motion-controller-mcu/project/src/wk_usart.c#L524-L526) `forward_uart_proto_rx_read()` 每次调用即清零 `forward_uart_rx_complete`，若传入 `64B` 缓冲会丢弃大于 64B 的尾字节），改为使用静态/帧级缓冲区按完整 `forward_uart_rx_len`（上限 `600B`）一次性抽出喂入 `s_th_parser`。
2. **普通 MiniMCProto v2.0 路由转发（零升级载荷解析、零 `5A A5` 转换）**：
   - 当 AP 向 `DST=0x03` 下发 `0x1D CMD_SYSTEM_CONTROL (JumpToBootloader)` 或 `0x20~0x23` 升级帧时，MC App 自动将板间串口模式切换为路由维护模式（抑制本地向 TH 发送 `0x1C` G-code 行，但不阻塞 `forward_uart_send_raw()` 的协议帧转发！注意：当前 [wk_usart.c#L364](file:///home/sushaohua/workspace/ai_soc_project/mcu-p3/motion-controller-mcu/project/src/wk_usart.c#L364) 在 `FORWARD_UART_MODE_UPGRADE` 下会拦截 `forward_uart_send_raw()`，需拆分为：拦截 `forward_uart_send_line()` 的 G-code 转发，但允许 `minimc_proto` 的二进制路由帧通过 `forward_uart_send_raw()` 发出！）。
   - MC App 对所有 `DST=0x03` 的 MiniMCProto v2.0 帧（无论是业务帧 `0x01/0x03/0x14/0x1D` 还是升级帧 `0x20/0x21/0x22/0x23`）执行**完全相同的通用三步路由**：
     1. 校验整帧 CRC16 与 `hop_limit > 1`；
     2. 递减 `hop_limit`、置位 `route_ctrl |= MINIMC_ROUTE_IS_ROUTED (0x04)`、重算 CRC16；
     3. 通过 `forward_uart_send_raw()` 经 `USART6` DMA 整帧发往 TH（无论是 TH App 还是 TH Bootloader），并将 TH 返回的 `SRC=0x03, DST=0x01` 响应帧反向路由回 `USART2` (AP)。**MC App 全程不解析 `0x20~0x23` 载荷，不做任何 `5A A5` 转换**。

#### 3.2.3 MC App 现有 `th_upgrade_mgr.c`（从 U盘向 TH 升级调用路径）的兼容迁移方案
1. **现状盘点**：
   - [mcu-p3/motion-controller-mcu/project/marlin/marlin_module/th_upgrade_mgr.c](file:///home/sushaohua/workspace/ai_soc_project/mcu-p3/motion-controller-mcu/project/marlin/marlin_module/th_upgrade_mgr.c#L158-L343) 在 MC App 启动前 5 秒窗口内扫描插入 MC 的 U盘根目录下是否存在 `0:/fw_th.bin`；若存在且校验 `128B ATSG Trailer` 通过，当前实现会发送裸 ASCII `"M997 S0"` 并调用 [wk_usart.c#L585](file:///home/sushaohua/workspace/ai_soc_project/mcu-p3/motion-controller-mcu/project/src/wk_usart.c#L585) 的 `forward_uart_send_frame()` 发送旧私有 `5A A5` 帧（`0x10 HELLO`, `0x11 START_UPG`, `0x12 PUSH_CHUNK`, `0x13 FINISH`）。
   - 同时，[boot/bootloadermc/app_test/](file:///home/sushaohua/workspace/ai_soc_project/boot/bootloadermc/app_test/inc/th_upgrade_mgr.h) 目录下也包含一份历史测试 App 副本。
2. **统一迁移方案（同构迁移至 MiniMCProto v2.0，绝不增加 MC Boot 的 TH 路由）**：
   - 一旦 `bootloaderth` 移除 `5A A5` 并切换为 MiniMCProto v2.0，若 `th_upgrade_mgr.c` 仍保留 `5A A5` 调用将沦为死代码且无法工作。因此，在 MC App 中对 `th_upgrade_mgr.c` 执行**协议同构迁移**：
     1. **触发进入 Boot**：将 `th_upg_trigger_reboot()` 中的 `forward_uart_send_line("M997 S0", 7U)` 替换为发送标准 MiniMCProto v2.0 帧 `SRC=0x02, DST=0x03, CMD=0x1D (CMD_SYSTEM_CONTROL, action=2 JumpToBootloader)`；
     2. **Boot 就绪探测**：将 `th_upg_wait_for_hello()` 等待私有 `0x10 CMD_TH_HELLO` 替换为发送/接收 `0x01 GET_VERSION -> 0x02 VERSION_REPORT` 并检查 `(capability_flags & 0x80000000U) != 0U`；
     3. **升级传输三步闭环**：将 `0x11/0x12/0x13` 私有帧调用统一替换为构造并发送 MiniMCProto v2.0 的 **`0x20 CMD_OTA_START (144B)`**、**`0x21 CMD_OTA_DATA (8B + 512B)`**、**`0x22 CMD_OTA_FINISH (8B)`**，等待 TH Boot 返回的 `0x00 CMD_ACK (4B)`；
     4. **清理私有 `5A A5` 通道**：删除 `th_upgrade_mgr.h` 中的 `CMD_TH_HELLO (0x10)` ~ `ACK_TH_FINISH (0x93)` 宏，删除 `wk_usart.c` 第 `544~695` 行的 `forward_uart_send_frame()` / `forward_uart_recv_frame()` (`0x5A 0xA5` 编解码函数) 及 `forward_uart_rx_read()` 中的 `0x5A 0xA5` 嗅探分支；
     5. **容量常量对齐**：将 `th_upgrade_mgr.h#L21` 的 `TH_FLASH_MAX_APP_SIZE` 从 `240U * 1024U` 修正为 `236U * 1024U` (`241,664B`)；
     6. **严守职责红线**：该 U盘升级 TH 的能力**仅存在于 MC App (`mcu-p3`) 中**，**`boot/bootloadermc` (MC Bootloader) 绝不读取 `fw_th.bin`、绝不初始化 `USART6`、绝不承担任何 TH 路由或 TH 升级职责**！

---

### 3.3 `ENG-TH`（`mcu-p3/color-engine-mcu`，`feat/soc-debug`）专项技术输入

1. **收到 MiniMCProto v2.0 进入维护/升级指令（`0x1D CMD_SYSTEM_CONTROL`）的安全停机与软复位时序**：
   - 在 [mcu-p3/color-engine-mcu/io_toggle/src/app/minimc_proto.c](file:///home/sushaohua/workspace/ai_soc_project/mcu-p3/color-engine-mcu/io_toggle/src/app/minimc_proto.c) 中新增 `MINIMC_CMD_SYSTEM_CONTROL (0x1DU)` 处理函数（遵循 $\le 50$ 行、$\le 4$ 参门禁）：
     1. **安全状态检查**：检查当前是否有未完成的步进运动或异常状态；
     2. **热端 PWM 0% 锁死与电机去能**：立即调用 `setTargetHotend0(0)`、强制将热端定时器比较寄存器置为安全关断电平（PWM 0% 锁死），并调用 `disable_a()`、`disable_b()`、`disable_c()`、`disable_d()` 去能 4 路换色/挤出步进电机；
     3. **先回发二进制 `0x00 CMD_ACK` 并排空串口（消除旧 M997 混流缺陷）**：
        构造并发送 `SRC=0x03, DST=req_src, CMD=0x00 (CMD_ACK), Len=4B` 响应帧（**严禁像旧 `m997_execute_firmware_upgrade_reset()` 那样在 `USART1` 上回发裸 ASCII `"ok2\r\nM997: Entering Bootloader...\r\n"` 污染二进制总线！** 仅在独立调试口 `USART3` 输出 `[TH-DBG] Entering Bootloader via 0x1D...`）；
     4. **等待 `USART1` 硬件发送彻底完成**：带超时计数器轮询 `usart_flag_get(USART1, USART_TDC_FLAG) == SET`，并等待 `delay_ms`（默认 `20~50ms`）确保 MC App 已完成该 ACK 帧向 AP 的转发；
     5. **写入跨复位魔数并软复位**：向固定安全地址 `BOOT_UPGRADE_FLAG_ADDR (0x20008000UL)` 写入 `BOOT_UPGRADE_MAGIC (0x55504744UL, "UPGD")`，调用 `__DSB()` 后执行 `NVIC_SystemReset()` 进入 TH Bootloader。
2. **新 App 启动后的动态 `boot_id`、`git_commit_short` 与业务恢复**：
   - **消除静态 `boot_id` 伪常量**：将 TH App 原本固定的 `TH_BOOT_ID = 0x8877AA55U` 改为在 `minimc_proto_init()` 初始化时基于片内 RTC/ERTC 备份寄存器自增启动计数或 UID + ADC 热噪声/SysTick 初始微秒混合生成的动态非零 `s_th_boot_id`（并在 `0x20008004UL` 记录上一次 `boot_id` 确保软复位后新 `boot_id` 必定不等于升级前旧值）。
   - **注入真实 `git_commit_short` 与版本**：在 `Makefile` 编译时通过 `-DFW_GIT_COMMIT_SHORT=0x...` 注入当前 `mcu-p3` HEAD 短哈希，并通过 `0x02 VERSION_REPORT` 报告 `capability_flags` 最高位 `Bit 31 = 0`（`APP_MODE`）。
   - **链接脚本容量对齐**：将 [AT32F423xC_FLASH.ld#L34](file:///home/sushaohua/workspace/ai_soc_project/mcu-p3/color-engine-mcu/io_toggle/libraries/cmsis/cm4/device_support/startup/gcc/linker/AT32F423xC_FLASH.ld#L34) 的 `FLASH LENGTH = 240K` 修正为 `LENGTH = 236K`（`241,664B`），确保链接器在编译期即可拦截任何越界侵入 `0x0803F000..0x0803FFFF`（含 Sector 127 Anchor `0x0803F800`）的镜像。

---

### 3.4 `ENG_BOOT_MC`（`boot/bootloadermc`，`soc_debug`）专项技术输入

1. **100% 保留 USB Host U盘升级完整能力（零退化回归基线）**：
   - 保持 [main.c](file:///home/sushaohua/workspace/ai_soc_project/boot/bootloadermc/bootloader/src/main.c) 与 [usbh_user.c](file:///home/sushaohua/workspace/ai_soc_project/boot/bootloadermc/bootloader/src/usbh_user.c) 中现有的 USB OTGFS1 Host 驱动、200ms SE0 物理断开复位（`usb_bus_disconnect_se0(200U)`）、FatFs 文件系统挂载、`0:/firmwaremc.bin`（或 `UPGRADE_BIN_NAME`）检索、擦除前 `128B ATSG Trailer` 校验（`magic == 0x41545347U`、`board_id == 0x43500001U`、`payload_len` 校验，并**补齐对 `trailer.trailer_crc32` 前 124 字节 CRC32 的实际校验**）、`0x08020000` (`FLASH_APP_ADDR`) 2KB 扇区擦写、硬件 CRC32 回读比对、成功后原子改名为 `.cur`（失败改名为 `.err`）及卸载重挂载 FS Check 完整闭环。
2. **新增 `USART2 (PA2/PA3 @ 921600 8N1)` MiniMCProto v2.0 本机（`DST=0x02`）串口升级**：
   - **引脚与时钟初始化**：在 `main.c` 启动时初始化 `USART2` (`PA2 TX / PA3 RX`, `GPIO_MUX_7`, `921600 8N1`, 开启 `USART_RDBF_INT` 接收中断压入 `1024B` 环形队列 `s_uart2_rx_ring`)。
   - **双源触发与驻留状态机**：
     - **显式进入升级态**：若启动时检测到 MC App 写入的跨复位魔数（`0x55504732UL` `"UPG2"`），立即清零该魔数并进入**无限等待串口升级模式**（同时可通过 `USART1 @ 115200` 输出 `[MC_BL] Entered UART OTA mode via App request`）；
     - **冷启动并发探测窗口（2.0s）**：在原有的 `2000ms` U盘探测窗口（`main.c#L205-L225`）内，主循环同时轮询 `usbh_loop_handler()` 与 `boot_mc_uart2_proto_poll()`。若 2.0s 内检测到 U盘插入则走 U盘升级；若收到 AP 发来的 `DST=0x02` MiniMCProto v2.0 握手帧（`0x01 GET_VERSION` 或 `0x20 OTA_START`），则锁定为**串口升级活跃态**（`g_uart_ota_active = 1`），暂停超时跳转；若 2.0s 超时既无 U盘也无串口升级请求且 `is_app_valid(0x08020000)` 为真，则安全跳转至 MC App；若 `0x08020000` App 无效，则持续同时监听 U盘与 `USART2` 串口恢复。
   - **共用 Flash 擦写与校验底层函数**：
     - 将 `usbh_user.c` 中的 `verify_trailer_struct()`、`flash_erase_sectors()`、流式字/半字编程及 `calculate_flash_crc()` 提炼为模块内共用函数，供 U盘通道与 `USART2` MiniMCProto v2.0 通道（`0x20 OTA_START [144B]` 擦除前准入、`0x21 OTA_DATA` 分块写入、`0x23 OTA_STATUS` 查询、`0x22 OTA_FINISH` 硬件 CRC32 终验）共同调用。
   - **安全跳转清理**：在 `jump_to_app(0x08020000)`（[main.c#L76-L127](file:///home/sushaohua/workspace/ai_soc_project/boot/bootloadermc/bootloader/src/main.c#L76-L127)）中，除现有的 `USART1` 与 `OTGFS1` 复位外，新增对 `USART2` 的 `USART_TDC_FLAG` 排空等待、`usart_enable(USART2, FALSE)` 及 `crm_periph_reset(CRM_USART2_PERIPH_RESET, TRUE/FALSE)`，确保 MC App 启动后接管干净的 `USART2` 外设。
   - **严守边界**：`bootloadermc` 仅处理 `DST == 0x02 (MINIMC_NODE_MC)` 的帧，对任何 `DST == 0x03` 的帧直接忽略或回 `NACK`，绝不初始化 `USART6`，绝不承担 TH 路由。

---

### 3.5 `ENG_BOOT_TH`（`boot/bootloaderth`，`soc_debug`）专项技术输入

#### 3.5.1 在 16KB (`16,384B`) 硬边界内替换 `5A A5` 为最小 MiniMCProto v2.0 升级子集
1. **移除私有 `5A A5` 通信层，保留全部防变砖 Flash/Anchor 核心资产**：
   - 在 [src/iap.c](file:///home/sushaohua/workspace/ai_soc_project/boot/bootloaderth/src/iap.c) 与 [inc/iap.h](file:///home/sushaohua/workspace/ai_soc_project/boot/bootloaderth/inc/iap.h) 中：
     - **彻底移除**：`FRAME_SOF1/2 (0x5A/0xA5)`、`CMD_TH_HELLO (0x10)` ~ `ACK_TH_FINISH (0x93)`、`iap_checksum_calc()`、`iap_send_hello()`（主动盲发 `5A A5` HELLO 帧改为响应式 `0x01 -> 0x02 VERSION_REPORT`）及旧 6 步 `5A A5` 状态机；
     - **实现最小 MiniMCProto v2.0 升级子集**：
       - 12B 帧头 + 2B `CRC-16/CCITT-FALSE`（紧凑无表计算函数仅约 `44 Bytes` `.text`）流式解析器，复用现有的 `s_rx_ctx`（`payload[520]`）；
       - 仅响应 `DST == 0x03 (MINIMC_NODE_TH)` 的 **7 个命令码**：
         1. `0x01 GET_VERSION` $\to$ 回 `0x02 VERSION_REPORT (16B)`，其中 `capability_flags = 0xE0080423U`（`Bit31=1 BOOT_MODE`, `Bit30=1 ATSG Trailer`, `Bit29=1 Chunk0+Anchor`, `MaxChunk=512B`, `Board=0x0423`）；
         2. `0x03 PING (4B)` $\to$ 回 `0x04 PONG (12B)`；
         3. `0x1D CMD_SYSTEM_CONTROL (4B)` $\to$ 已在 Boot 态下若收到 `action=2 (JumpToBootloader)` 直接回 `0x00 CMD_ACK (4B)`（幂等成功）；若收到 `action=1 (Reboot)` 则回 `0x00 CMD_ACK` 后软复位；
         4. `0x20 CMD_OTA_START (144B)` $\to$ 校验 `target_device == 0x03`、`target_component == 0x01 (Main App)`、`fw_size_bytes == trailer.payload_len` 且 `iap_trailer_validate(&trailer)`（`magic == 0x41545347U`, `board_id == 0x42300001U`, `0 < payload_len <= 241664U`, `trailer_crc32` 匹配）。全部通过后调用 `bsp_flash_erase_first_app_sector()`（擦除 `0x08004000` Sector 8）与 `bsp_flash_erase_anchor_sector()`（擦除 `0x0803F800` Sector 127），置状态为 `OTA_STATE_ERASED_READY` 并回 `0x00 CMD_ACK (4B)`；任何一项不通过则**零擦除**并回 `0x06 CMD_NACK (3B)`；
         5. `0x21 CMD_OTA_DATA (8B + chunk_bytes)` $\to$ 校验 `chunk_crc16` 与 `offset` 连续性（支持重传幂等 ACK）：
            - 当 `offset < 512U`（首块 512B，含中断向量表 `MSP` 与 `Reset_Handler`）：仅拷贝至 `s_chunk0_buf[512]`，置 `s_has_cached_chunk0 = true`，**绝不写入 `0x08004000` Flash**（保持 `0x08004000` 为 `0xFFFFFFFF`，确保中途断电重启必留在 Boot），回 `0x00 CMD_ACK (4B)`；
            - 当 `offset >= 512U`：若跨入新的 `2KB` 扇区（`(offset % 2048U) == 0U`）先调用 `bsp_flash_erase_sector(APP_START_ADDR + offset)`，再调用 `bsp_flash_write_and_verify()` 半字写入并逐字节物理回读比对，累加 `s_bytes_written_flash += chunk_bytes`，回 `0x00 CMD_ACK (4B)`；
         6. `0x23 CMD_OTA_STATUS (0B)` $\to$ 回 8B `minimc_payload_ota_status`（`ota_state`, `error_code`, `reserved=cached_chunk0_bytes`, `bytes_written=s_bytes_written_flash`）；
         7. `0x22 CMD_OTA_FINISH (8B)` $\to$ 调用 `iap_calculate_firmware_crc32()` 联合计算 `s_chunk0_buf[512]` 与 Flash `0x08004200..` 净荷的全片 CRC32，验证 `calc_crc32 == req.fw_crc32 == s_cached_trailer.payload_crc`：
            - 若不一致：擦除首扇区与 Anchor 扇区，回 `0x06 CMD_NACK (MINIMC_ERR_OTA_CRC_MISMATCH = 0x13)`；
            - 若一致：第一步调用 `iap_commit_anchor_metadata(calc_crc32)` 将 `app_anchor_meta_t`（`ANCHOR_MAGIC = 0x414E4348U` + `128B Trailer` + `firmware_crc32` + `anchor_crc32`）写入 `0x0803F800` 并回读验证；第二步调用 `bsp_flash_write_and_verify(0x08004000, s_chunk0_buf, c0_len)` 原子提交首块 512B 向量表并回读验证；第三步更新 `s_bytes_written_flash = s_target_fw_len`，先回发 `0x00 CMD_ACK (4B)`，等待 `USART1` `USART_TDC_FLAG` 排空并延时 `50ms` 后，若 `action_after_verify == 1` 则调用 `app_load(0x08004000)` 8 步安全跳转至新 App！
2. **修复 `flash.c` 栈空间与发送栈缓冲（重要工程优化）**：
   - 原 [iap.c#L113](file:///home/sushaohua/workspace/ai_soc_project/boot/bootloaderth/src/iap.c#L113) 在 `iap_send_frame()` 栈上分配了 `uint8_t tx_buf[526]`，而 Bootloader 作为从节点，其发送的最大响应帧仅为 `0x02 VERSION_REPORT`（`12B 头 + 16B 载荷 + 2B CRC = 30B`）！将 `tx_buf` 缩减为 `uint8_t tx_buf[32]`，立省 **`494 Bytes`** 栈空间！

#### 3.5.2 TH Bootloader 16KB (`16,384B`) Flash 各段与 48KB SRAM/Stack 详细字节预算表

基于 `arm-none-eabi-gcc -mcpu=cortex-m4 -mthumb -Os -ffunction-sections -fdata-sections -Wl,--gc-sections -specs=nano.specs` 对 `boot/bootloaderth` 全部编译单元（[Makefile#L36-L54](file:///home/sushaohua/workspace/ai_soc_project/boot/bootloaderth/Makefile#L36-L54)）的精确逐段核算：

##### (A) 16KB Flash 分区（`0x08000000 ~ 0x08003FFF`，上限 `16,384 Bytes`）各段字节预算表

| Flash 段名 (Section) | 包含的模块 / 目标文件 (`.o`) 与核心内容 | `DEBUG_LOG_ENABLE=1`<br>（启用 `USART3` 精简日志）预算 | `DEBUG_LOG_ENABLE=0`<br>（关闭日志生产模式）预算 | 预算占比（按 `DEBUG=1` 计） |
| :--- | :--- | :--- | :--- | :--- |
| **`.isr_vector`** | `startup_at32a423.o`（Cortex-M4 向量表：16 个内核异常 + 92 个外设 IRQ 向量） | `432 B` (`0x1B0`) | `432 B` (`0x1B0`) | `2.64%` |
| **`.text` (Core & Startup)** | `Reset_Handler`、`SystemInit` (`system_at32a423.o`)、`at32a423_clock.o` (`150MHz` PLL + Flash 4WS + PWC LDO)、`tmr.o` (SysTick 1ms)、`at32a423_int.o` | `1,180 B` | `1,180 B` | `7.20%` |
| **`.text` (StdPeriph Drivers)** | `at32a423_crm.o`、`at32a423_gpio.o`、`at32a423_usart.o`、`at32a423_flash.o`、`at32a423_pwc.o`、`at32a423_misc.o`（经 `--gc-sections` 裁剪未引用函数后） | `1,920 B` | `1,840 B` | `11.72%` |
| **`.text` (BSP Flash & UART)** | `flash.o`（2KB 扇区擦除、半字编程、逐字节回读、Anchor + 全片 CRC32 完整性校验）+ `usart.o`（`USART1` 中断环形队列收发 + `USART3` 调试输出） | `1,150 B` | `860 B` | `7.02%` |
| **`.text` (MiniMCProto v2.0 IAP)** | `iap.o` + `main.o`（12B+CRC16 流式解析器、位运算 `crc16_ccitt` [`44B`]、位运算 `crc32_ieee` [`68B`]、`144B OTA_START` Trailer 准入、Chunk0 SRAM 延迟提交、`OTA_DATA/STATUS/FINISH` 状态机、8 步内联汇编 `app_load`） | `2,240 B` | `1,820 B` | `13.67%` |
| **`.text` (`newlib-nano` Runtime)** | `__aeabi_uidiv`、`memcpy`、`memset` 及 `printf` 整数/十六进制格式化（`nano.specs` 无浮点 `printf`） | `2,680 B` | `320 B` *(无 `printf`)* | `16.36%` |
| **`.rodata` & `.ARM.exidx`** | 启动 Banner 字符串、日志格式串、常量表、`.init_array` | `960 B` | `140 B` | `5.86%` |
| **`.data` (LMA in Flash)** | `system_core_clock` 等已初始化全局变量初值映像 | `28 B` | `28 B` | `0.17%` |
| **Flash 装载总计（Total LMA）** | **`.isr_vector + .text + .rodata + .ARM.exidx + .data(LMA)`** | **`10,590 Bytes` (`10.34 KB`)** | **`6,620 Bytes` (`6.46 KB`)** | **`64.64%`** (`DEBUG=1`) / **`40.41%`** (`DEBUG=0`) |
| **16KB 硬边界剩余安全裕度** | **`16,384 Bytes - Total LMA`** | **`+5,794 Bytes` (`35.36%` 裕度)** | **`+9,764 Bytes` (`59.59%` 裕度)** | 远低于 `16,384B` 红线，且链接脚本 `LENGTH = 16K` 强制超限报错 |

##### (B) 48KB 片内 SRAM（`0x20000000 ~ 0x2000BFFF`，上限 `49,152 Bytes`）与 Stack 预算表

| SRAM 区域 / 符号 | 物理地址范围 | 字节数 | 包含的变量与用途说明 |
| :--- | :--- | :--- | :--- |
| **`.data` (已初始化全局变量)** | `0x20000000 ~ 0x2000001B` | `28 B` | `system_core_clock`、毫秒时基状态等 |
| **`.bss` (未初始化静态缓冲区)** | `0x2000001C ~ 0x2000090F` | **`2,292 B`** | - `s_uart1_rx_buf`: `1,030 B` (`1024B` 环形缓冲 + `head/tail/count`)<br>- `s_chunk0_buf`: `512 B`（首块 512B 向量表延迟提交缓存）<br>- `s_rx_ctx`: `540 B`（MiniMCProto v2.0 接收帧上下文，最大载荷 `520B`）<br>- `s_cached_trailer`: `128 B`（缓存的 `128B ATSG Trailer`）<br>- 状态机与计数器（`s_iap_state`, `s_target_fw_len`, `s_bytes_written_flash`, `s_boot_id` 等）：`82 B` |
| **跨复位升级魔数安全隔离区** | `0x20008000 ~ 0x20008007` | `8 B` | `BOOT_UPGRADE_FLAG_ADDR (0x20008000UL)`：存放 `0x55504744UL` (`"UPGD"`) 软复位穿透标志，远离低地址 `.bss`（结束于 `< 0x20000A00`）与高地址主栈 `_estack` |
| **最坏调用栈峰值（Worst-Case Stack）** | `0x2000BC00 ~ 0x2000C000` (向下生长) | **`<= 768 B`** (`_Min_Stack_Size = 0x400 [1024B]`) | 最深调用链：`main -> iap_upgrade_app_handle -> iap_handle_finish -> iap_commit_anchor_metadata (栈上 app_anchor_meta_t 140B) -> bsp_flash_write_and_verify` + `USART1_IRQHandler (32B)`，总栈深 `< 512B` |
| **SRAM 总占用与剩余空闲裕度** | — | **总用 `3,096 B` (`3.02 KB`) / 空闲 `46,056 B` (`93.7%` 裕度)** | 零动态堆分配（严禁 `malloc/free`），100% 静态确定性内存布局 |

#### 3.5.3 将遗留 `240KB` 对齐至净 App `236KB` (`241,664B`) 的全部精确文件与行号清单

经跨仓全量检索，工作区中所有残留 `240KB` (`240 * 1024`) 参数的精确文件与行号共 **4 处**（加上注释说明共 6 行），在实现阶段一次性对齐至 **`236KB` (`241,664 Bytes`)**，确保 Sector 126 (`0x0803F000..0x0803F7FF`) 与 Sector 127 (`0x0803F800..0x0803FFFF` Anchor 区) 绝对安全：

| 序号 | 所属仓库 | 精确文件路径与行号 | 当前源码内容 | 修正后内容（对齐 `236KB = 241,664B`） |
| :--- | :--- | :--- | :--- | :--- |
| 1 | `boot/bootloaderth` | [boot/bootloaderth/tools/pack_firmware.py#L18](file:///home/sushaohua/workspace/ai_soc_project/boot/bootloaderth/tools/pack_firmware.py#L18) 及 [#L33](file:///home/sushaohua/workspace/ai_soc_project/boot/bootloaderth/tools/pack_firmware.py#L33) | `L18: MAX_PAYLOAD_SIZE = 240 * 1024    # 240 KB (245,760 bytes)`<br>`L33: print(f"[ERR] 固件大小超限: {payload_len} 字节 (最大允许 {MAX_PAYLOAD_SIZE} 字节 / 240KB)")` | `L18: MAX_PAYLOAD_SIZE = 236 * 1024    # 236 KB (241,664 bytes)`<br>`L33: print(f"[ERR] 固件大小超限: {payload_len} 字节 (最大允许 {MAX_PAYLOAD_SIZE} 字节 / 236KB)")` |
| 2 | `boot/bootloaderth` | [boot/bootloaderth/inc/iap.h#L58](file:///home/sushaohua/workspace/ai_soc_project/boot/bootloaderth/inc/iap.h#L58) | `L58: uint32_t payload_len;       /* 实际固件代码字节数 (<= 240KB) */` | `L58: uint32_t payload_len;       /* 实际固件代码字节数 (<= 236KB / 241664B) */` |
| 3 | `mcu-p3` (`ENG-TH`) | [mcu-p3/color-engine-mcu/io_toggle/libraries/cmsis/cm4/device_support/startup/gcc/linker/AT32F423xC_FLASH.ld#L34](file:///home/sushaohua/workspace/ai_soc_project/mcu-p3/color-engine-mcu/io_toggle/libraries/cmsis/cm4/device_support/startup/gcc/linker/AT32F423xC_FLASH.ld#L34) | `L34: FLASH (rx)      : ORIGIN = 0x08004000, LENGTH = 240K` | `L34: FLASH (rx)      : ORIGIN = 0x08004000, LENGTH = 236K` |
| 4 | `mcu-p3` (`ENG-MC`) | [mcu-p3/motion-controller-mcu/project/inc/th_upgrade_mgr.h#L21](file:///home/sushaohua/workspace/ai_soc_project/mcu-p3/motion-controller-mcu/project/inc/th_upgrade_mgr.h#L21) 及 [#L45](file:///home/sushaohua/workspace/ai_soc_project/mcu-p3/motion-controller-mcu/project/inc/th_upgrade_mgr.h#L45) | `L21: #define TH_FLASH_MAX_APP_SIZE           (240U * 1024U) /* 240 KB */`<br>`L45: uint32_t payload_len;       /* 0x10: 净代码有效字节数 (<= 240KB) */` | `L21: #define TH_FLASH_MAX_APP_SIZE           (236U * 1024U) /* 236 KB (241,664B) */`<br>`L45: uint32_t payload_len;       /* 0x10: 净代码有效字节数 (<= 236KB) */` |
| *(附)* | `boot/bootloadermc` *(历史 `app_test` 副本)* | [boot/bootloadermc/app_test/inc/th_upgrade_mgr.h#L21](file:///home/sushaohua/workspace/ai_soc_project/boot/bootloadermc/app_test/inc/th_upgrade_mgr.h#L21) | `L21: #define TH_FLASH_MAX_APP_SIZE           (240U * 1024U)` | 同步修正为 `(236U * 1024U)` |

---

### 3.6 `INTEGRATOR`（含《升级操作与 HIL 部署说明书》主责输入）专项技术输入

#### 3.6.1 VMware 指定目录（`/var/update/`）文件投放、原子封存与统一 `128B ATSG` 打包规范
1. **统一打包工具与 `128B ATSG Trailer` 契约**：
   - 统一使用 `pack_firmware.py`（支持 `--board mc` [`0x43500001`, 净上限 `896KB = 917,504B`] 与 `--board th` [`0x42300001`, 净上限 `236KB = 241,664B`]）生成带 `128B ATSG Trailer` 的正式升级包 `firmwaremc.bin`（U盘别名 `fw_mc.bin`）与 `firmwareth.bin`（U盘别名 `fw_th.bin`），并同步产出 JSON 清单 `release_manifest.json`（含 `git_commit`, `fw_version`, `board_id`, `payload_len`, `payload_crc32`, `payload_sha256`, `trailer_crc32`, `signed_file_sha256`）。
   - **明确校验职责边界**：
     - **打包阶段与 AP 侧预检**：同时校验完整文件 SHA-256、净载荷 `payload_sha256`、净载荷 `payload_crc32` 及 `128B ATSG Trailer` 的 `trailer_crc32`；
     - **MCU Bootloader 侧**：校验 `magic == 0x41545347U`、`board_id`、`payload_len <= APP_MAX_SIZE`、`trailer_crc32`（124B 头 CRC32）、每分块 `chunk_crc16`（CRC-16/CCITT-FALSE）及终验全片净荷 `fw_crc32`（IEEE 802.3 CRC32，且在 TH Boot 中固化保存完整 128B Trailer 进 `0x0803F800` Anchor）。`sig_r[32]` / `sig_s[32]` 首发填充全 `0x00`，**如实声明为预留字段，绝不对外宣称已启用 ECDSA 密码学验签**。
2. **VMware `/var/update/` 原子投放与封存防篡改流程（防止边复制边升级或同名替换）**：
   - **Step 1（临时写入）**：投放文件时先以 `.part` 临时后缀写入 `/var/update/incoming/firmwareth.bin.part`；
   - **Step 2（校验与原子重命名就绪）**：核对 `.part` 文件大小与 SHA-256 无误后，执行 `fsync()` 并原子 `rename()` 为 `/var/update/incoming/firmwareth.bin`；系统发现该文件仅将状态置为 `PACKAGE_STAGED_PENDING_CONFIRM`，**绝不自动开刷**；
   - **Step 3（确认后只读快照封存）**：当操作员通过受控入口确认执行升级时，AP 升级服务首先将 `/var/update/incoming/<pkg>.bin` 硬链接或复制到带单调运行 ID 的只读封存目录 `/var/update/sealed/<run_id>/<pkg>.bin`（权限设为 `0444`），重新核验封存副本的 SHA-256 与 `128B ATSG Trailer` 通过后，后续全部分块读取 100% 从 `/var/update/sealed/<run_id>/` 读取，彻底免疫升级过程中外部目录同名覆盖！

#### 3.6.2 首次 Boot 迁移与特殊救援流程边界
1. **首次 Boot 迁移（前置一次性受控动作）**：
   - 由于板卡当前片上驻留的旧 Bootloader（特别是 TH 板上的旧 `5A A5` Bootloader，以及 MC 板上尚无 `USART2` 串口升级能力的旧 U盘 Bootloader）不支持 MiniMCProto v2.0 串口升级协议，且本轮明确**不开放运行期 Bootloader 自升级（`target_component == 0x02` 强制拒绝）**，因此在双 Boot 代码实现并通过静态/软件 QA 门禁后，**首次将新版 `bootloadermc` (`0x08000000`) 与新版 `bootloaderth` (`0x08000000`) 部署上板**属于独立的前置迁移步骤。
   - **审批门禁**：若首次 Boot 迁移或极端硬件故障（如 Boot 区损坏）确需使用 SWD 探针写入 Bootloader，**必须由 `COORD` 单独向用户提交申请并取得显式批准后方可执行**，绝不混同于常规 App 部署。
2. **常规 App 恢复优先级（零探针恢复）**：
   - 一旦新版双 Boot 已就位：
     - 若 **TH App 损坏/升级中断**：TH 上电自动驻留 `bootloaderth`（因 `0x08004000` 首扇区与 `0x0803F800` Anchor 已擦除，首块 512B 延迟提交保护生效），直接通过 `AP -> MC App -> TH Boot` 重新发起 MiniMCProto v2.0 串口升级即可 100% 恢复；
     - 若 **MC App 损坏/升级中断**：MC 上电自动驻留 `bootloadermc`，可直接通过 `AP -> MC Boot (USART2)` 重新发起 MiniMCProto v2.0 串口升级恢复，或插入存放 `0:/firmwaremc.bin` 的 FAT32 U盘通过 MC 原生 U盘入口离线恢复；待 MC App 恢复上线后，再恢复 TH。

#### 3.6.3 常规测试与 HIL 部署全面停用 `probe-rs` 改走本升级流程的工程切换方案
1. **存量测试与部署资产盘点**：
   - 经只读排查，`test_harness/hil/` 下的在线回归探针（`hil_Twin50_probe.py`、`debug_reconciliation_probe.py`、`physical_ unplug_fault_injection.py` 等）本身只访问串口与 HTTP/D-Bus，未内嵌 `probe-rs download`；但历史 HIL 准备说明与 `mcu-p3/AGENTS.md` 中的传统手工部署习惯曾使用 `probe-rs download` 刷写 App ELF。
2. **硬性工程切换措施（随实现任务落地）**：
   - **唯一常规部署工具化**：在实现阶段交付统一的 VMware 受控升级部署工具/命令（如 `soc-ap` 的 `aisoc_fw_upgrade_cli` 或 `test_harness/hil/tools/hil_deploy_via_minimc_ota.py`），自动完成：`/var/update/` 封存核验 $\to$ 安全准入检查 $\to$ `0x1D` 进 Boot $\to$ `0x01/0x02` 确认 `BOOT_MODE` $\to$ `0x20/0x21/0x23/0x22` 传输与落盘校验 $\to$ 新 App `0x01/0x02` (`boot_id` 刷新 + `git_commit` 核对) $\to$ `0x14/0x15` 业务恢复 $\to$ 输出标准 JSON 台架部署交接单 `hil_deployment_receipt.json`。
   - **前置部署证据门禁**：在 `test_harness` 的 HIL 验收 Runner 中增加前置校验——执行任何常规 HIL 测试前，必须校验本轮候选对应的 `hil_deployment_receipt.json`（证实板上 MC/TH App 是通过 MiniMCProto v2.0 升级流程或受控 U盘回归入口部署，且回读的 `git_commit_short` 与 `boot_id` 吻合），**严禁绕过升级链路使用 `probe-rs` 或其他探针刷写 App 固件**；当升级功能尚未就绪时，依赖新固件部署的 HIL 步骤保持 `blocked / pending`。

#### 3.6.4 对《升级操作与 HIL 部署说明书》（`minimc_v2_mcu_upgrade_and_hil_deployment_manual_20261105.md`）第 2~8 节待补齐项的完成计划与受控验证设计

| 说明书章节 | 待补齐核心条目 | 主责与协同核实角色 | 完成时机与受控验证方式 |
| :--- | :--- | :--- | :--- |
| **第 2 节：正式发布前必须补齐的操作信息** | 1. 准确可执行入口（CLI/HTTP 命令、工作目录、退出码、超时参数）；<br>2. VMware `/var/update/incoming/` 与 `/var/update/sealed/<run_id>/` 路径、权限与 `.part -> .bin` 就绪规则；<br>3. MC (`0x43500001`) / TH (`0x42300001`) 发布包清单与哈希表；<br>4. 两板已部署 Boot 版本/能力位 (`0x80000000`) 核实命令；<br>5. 业务口 `921600` (`/dev/ttyUSB0`) 与双板 Debug 口 `115200` 映射表；<br>6. 受控恢复入口与停止条件；<br>7. 升级记录与交接单归档路径。 | **`INTEGRATOR` 主责**；`ENG-FWD`、`ENG-MC`、`ENG-TH`、`ENG_BOOT_MC`、`ENG_BOOT_TH` 分别提供并核实本端参数。 | **Stage 1（架构定稿）**：在主架构方案中固定参数模板与目录规范；<br>**Stage 2（功能实现后）**：实测验证全部命令与退出码后回填真实值（当前规划阶段绝不虚构）。 |
| **第 3~4 节：升级前准备与 VMware 文件升级步骤** | 排他窗口确认、封存校验、安全准入核对（加热 0%、作业 IDLE、温度有效）、`TH -> MC` 标准串行升级顺序、四阶段真实进度观察（区分 Chunk0 缓存与 `bytes_written` 落盘）、新 App `boot_id` 与最小业务恢复核对。 | **`INTEGRATOR` + `ENG-FWD` / `ENG-STATE`** | 在 VMware + 双 MCU 真实台架上采集从 `0x1D` 到新 App `0x02`/`0x15` 恢复的完整双向 Hex 帧、Debug 日志与状态快照。 |
| **第 5 节：保留的 MC U盘入口** | FAT32 分区要求、根目录文件名（`0:/firmwaremc.bin` / `0:/fw_mc.bin`）、上电 2.0s 探测触发时机、成功后自动改名 `.cur`（失败 `.err`）及与 MC App U盘升级 TH (`0:/fw_th.bin`) 的边界说明。 | **`ENG_BOOT_MC` + `ENG-MC` + `INTEGRATOR`** | 单独执行物理 U盘插入上电回归测试，保留 `[MC_BL]` 串口日志与 U盘 `.cur` 文件系统核验记录，不与 VMware 串口升级混同。 |
| **第 6~7 节：后续测试/HIL 固件部署与中断恢复** | 测试脚本停用 `probe-rs` 后的标准部署交接单字段、错包/错板/超限拦截验证、断连/掉电驻留 Boot 重试恢复步骤。 | **`INTEGRATOR` + `ENG-BOOT-TH` / `ENG-BOOT-MC`** | 执行错板包拒绝（零擦除）、传输中断重连恢复及正常部署交接单生成验证。 |
| **第 8 节：非实现者受控验证与发布状态切换** | 安排**非实现者**在不依赖口头补充的情况下，仅按说明书完成一次受控双板升级与 HIL 台架交接，并由独立 Codex **`QA`** 审阅原始证据。 | **`INTEGRATOR` 交付 $\to$ 非实现者实操 $\to$ 独立 Codex `QA` 复核** | 非实现者实操通过且独立 `QA` 核实证据完备后，才将说明书 `status` 从 `draft` 切换为 `executable-validated`。 |
