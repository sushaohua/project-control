---
id: ARCH-AUDIT-RECEIPT-MINIMC-V2-UPGRADE-20261105
title: MiniMCProto v2.0 双 MCU 统一升级 Phase A 接单回执与跨仓只读架构核查报告
demand_id: DEM-20261105-006
requirement_id: REQ-20261105-003
phase: Phase A (Read-Only Cross-Repository Architecture Audit & Protocol Contract Conflict Reconciliation)
revision: 2
date: 2026-11-05
author_role: ARCH
author_session: ef428595-f4d6-46a7-9d12-07e1fd215641
status: phase_a_r2_completed_ready_for_engineering_and_qa_inputs
---

# MiniMCProto v2.0 双 MCU 统一升级 Phase A 接单回执与跨仓只读架构核查报告

| 修订版本 | 日期 | 作者角色与会话 | 修订内容摘要 |
| :--- | :--- | :--- | :--- |
| `revision: 1` | 2026-11-05 | `ARCH` (`ef428595-f4d6-46a7-9d12-07e1fd215641`) | 初版跨仓只读架构核查回执（`sha256: 9f93becf1ae1b80eef29ed8b95cd6cb8d9ecf0873e0e126ffa9d3aca3d59dde7`）：登记六仓规则与基线、核查 `64B` 载荷上限与 `236KB` 遗留参数、起草升级协议与双 Boot/双 App 边界。 |
| `revision: 2` | 2026-11-05 | `ARCH` (`ef428595-f4d6-46a7-9d12-07e1fd215641`) | 响应收件单 `20261105_minimc_v2_upgrade_coord_planning_prompt.md` (`revision: 3`) 与 `REQ-20261105-003` (`revision: 4`)：<br>1. **新增第 2 章《全量协议契约冲突对账与裁定记录》**：逐项对账主规范 `SPEC-PROTO-20261015-153000` (`Rev 2.0.3`)、已批准扩展方案（`SPEC-ALIGN-20261102-01`、`PLAN-E2E-PHYSICAL-LINK-REMEDIATION-20261104`）与四端源码，完整列出 `0x00~0x50` 全量命令码，严格区分**完全一致**、**合法别名/扩展**、**功能子集**与**核心语义冲突**（重点剖析 `0x10 SYSTEM_CONTROL vs SET_TEMP`、`0x12 EMERGENCY_STOP vs MOTION_MOVE`、`0x00 CMD_ACK 4B vs 0B`、`MAX_PAYLOAD_SIZE 1024B vs 64B`）；<br>2. **专项审计 `check_opcode_alignment.py`**：核实其硬编码 `0x10=SET_TEMP`、`0x12=MOTION_MOVE` 的来源与三大结构性盲区（不防同值异义碰撞、未覆盖 Boot 与主规范、不检载荷尺寸）；<br>3. **校正升级状态与确认契约**：严格对齐主规范 `0x00 CMD_ACK (4B)`、`0x06 CMD_NACK (3B)` 与 `0x23 CMD_OTA_STATUS (8B)`，不占用 `0x05` 作为通用 ACK；<br>4. **新增第 6 章《升级操作与 HIL 部署说明书衔接及常规部署禁 `probe-rs` 门禁》**。 |

---

## 1. 接单回执、必读输入登记（`read_sources`）与六仓基线核查

### 1.1 规划输入、权威规范与历史文档显式读取登记（`read_sources`）

本节按 [repository_rule_sources.json](file:///home/sushaohua/workspace/ai_soc_project/project-control/.agents/rules/repository_rule_sources.json) 与 [repository_rule_boundaries.md](file:///home/sushaohua/workspace/ai_soc_project/project-control/.agents/rules/repository_rule_boundaries.md) 要求，显式登记本次跨仓只读核查实际读取的全部规划输入、协议规范、已接受扩展方案、公共规则、静态检查器及历史任务卡精确版本与 SHA-256 摘要：

| 类别 | 文件路径 | 版本 / 修订标识 | SHA-256 摘要 |
| :--- | :--- | :--- | :--- |
| 收件指令（最新） | [20261105_minimc_v2_upgrade_coord_planning_prompt.md](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/work_intake/submissions/20261105_minimc_v2_upgrade_coord_planning_prompt.md) | `revision: 3` (`2026-11-05`)<br>*(历史 `rev 2`: `01687e47...`)* | `4699feade73d9e621b5ead2bade96ba195c488446de6e215bbb9b5276dcfcc80` |
| 归档需求记录 | [REQ-20261105-003.yaml](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/work_intake/requirements/REQ-20261105-003.yaml) | `revision: 4` (`DEM-20261105-006`) | `d9967df4be6b6334be41f5508c54c94e43498bcbb24070009b7b69e829088629` |
| 助理讨论稿 | [minimc_v2_unified_mcu_upgrade_proposal_20261105.md](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/planning/minimc_v2_unified_mcu_upgrade_proposal_20261105.md) | `revision: 2` (`2026-11-05`) | `72c1a91a1487b7184ba371ea3ed653d038c741a7e8baf2eb98316e0d91e6dc2f` |
| 规划委派表 | [minimc_v2_upgrade_planning_dispatch_register_20261105.md](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/planning/minimc_v2_upgrade_planning_dispatch_register_20261105.md) | `revision: 3` (`2026-11-05`) | `8a5b54af2228cabe69d259a9fa37691ad11d79f71a65d11592b547f13bc51f02` |
| QA 规划输入初稿 | [minimc_v2_upgrade_qa_planning_input_20261105.md](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/planning/minimc_v2_upgrade_qa_planning_input_20261105.md) | `revision: 1` (`2026-11-05`) | `97f53a4de98bd8f91c99a7f3d2512dc740471d6172a6f0aee16e654557882657` |
| 部署说明书草案 | [minimc_v2_mcu_upgrade_and_hil_deployment_manual_20261105.md](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/guides/minimc_v2_mcu_upgrade_and_hil_deployment_manual_20261105.md) | `revision: 1` (`2026-11-05`) | `87b0b859e3e7e4cf7e8733ac88d90d1e0fd94f3b3e2117abfea9af3b14d4e6a9` |
| 权威协议主规范 | [ap_mc_formal_protocol_v2_0_multidevice_routing_draft_20261015.md](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/specs/ap_mc_formal_protocol_v2_0_multidevice_routing_draft_20261015.md) | `SPEC-PROTO-20261015-153000` (`Rev 2.0.3`) | `9f8d4f9607cb3e76cc30b9ee2f971b23c3e0d936611188466a71f4aa15f3ce54` |
| ACK/NACK 对齐规范 | [minimcproto_ack_nack_contract_alignment_matrix_20261102.md](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/specs/minimcproto_ack_nack_contract_alignment_matrix_20261102.md) | `SPEC-ALIGN-20261102-01` (`APPROVED`) | `efa28a8dba708527a18309a0fb2956c233cd85f7009c91d8316bb7ff570ad683` |
| 已接受控制扩展方案 | [end_to_end_physical_link_remediation_plan_20261104.md](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/planning/end_to_end_physical_link_remediation_plan_20261104.md) | `PLAN-E2E-PHYSICAL-LINK-REMEDIATION-20261104` (`revision: 3`) | `21dd6cc16b9eb7d643662b6fba681e6360f4dcd98cdece55439c6f759c5b22cc` |
| 历史首发范围决议 | [first_release_scope_decision_20261029.md](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/planning/product/first_release_scope_decision_20261029.md) | `revision: 7` (`2026-11-03`) | `d7f7c0de96f8e3776090820e6633e67a78ec756577ebb27d977faf6539360802` |
| 历史升级设计稿 | [mcu_firmware_upgrade_design_20261031.md](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/analysis/mcu_firmware_upgrade_design_20261031.md) | `revision: 1` (`2026-10-31`) | `c5a79270ec6017a071944bbf314ebb11e345ec61d62fee6f5563336110c7505c` |
| 命令码静态检查器 | [check_opcode_alignment.py](file:///home/sushaohua/workspace/ai_soc_project/test_harness/static_checks/minimcproto/check_opcode_alignment.py) | `test_harness` `HEAD` | `bcc098de7793d08c79f391be82f55a1d3b099b9984f8db08952722ad8b1253e9` |
| 历史冻结任务卡 | [TWIN-26.md](file:///home/sushaohua/workspace/ai_soc_project/project-control/.agents/kanban/microtasks/vmware_soc_twin/TWIN-26.md) / [TWIN-27.md](file:///home/sushaohua/workspace/ai_soc_project/project-control/.agents/kanban/microtasks/vmware_soc_twin/TWIN-27.md) / [TWIN-28.md](file:///home/sushaohua/workspace/ai_soc_project/project-control/.agents/kanban/microtasks/vmware_soc_twin/TWIN-28.md) | 保持冻结不改写 | `ba7bd322...` / `4190ef89...` / `0b1097d7...` |
| 公共规则集 | [repository_rule_sources.json](file:///home/sushaohua/workspace/ai_soc_project/project-control/.agents/rules/repository_rule_sources.json)、[repository_rule_boundaries.md](file:///home/sushaohua/workspace/ai_soc_project/project-control/.agents/rules/repository_rule_boundaries.md)、[bootloader_role_boundaries.md](file:///home/sushaohua/workspace/ai_soc_project/project-control/.agents/rules/bootloader_role_boundaries.md)、[c_cpp_coding_standard.md](file:///home/sushaohua/workspace/ai_soc_project/project-control/.agents/rules/c_cpp_coding_standard.md)、[code_documentation_standard.md](file:///home/sushaohua/workspace/ai_soc_project/project-control/.agents/rules/code_documentation_standard.md)、[delivery_and_coord_gate.md](file:///home/sushaohua/workspace/ai_soc_project/project-control/.agents/rules/delivery_and_coord_gate.md)、[codex_qa_review.md](file:///home/sushaohua/workspace/ai_soc_project/project-control/.agents/rules/codex_qa_review.md) | `source_commit: 17e0887da07ceb3b017623b791b6a6999e837c79` | `e9bc40d4...` / `97c3112c...` / `c8ef3d78...` / `395c7c22...` / `a2ab273f...` / `90be6aa7...` / `4c992c3e...` |

### 1.2 六仓规则入口、当前分支、HEAD Commit 与工作树状态核查

| 仓库名称 | 当前分支 | 最新观察 HEAD Commit（括号内为 `r1` 初查时 HEAD） | 仓内规则入口文件与 SHA-256 | 共享规则副本 `SOURCE.json` 溯源 | 工作树状态说明 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `project-control` | `main` | `5686e1931123650bb2251045353c18c8baa00f65` | [project-control/AGENTS.md](file:///home/sushaohua/workspace/ai_soc_project/project-control/AGENTS.md)<br>`59781839d7ebbf977f71e4659c31bb6fbb1e4fa6793080c460cff65b7094ada5` | 权威源仓（`.agents/rules/`） | 含本轮收件与规划文档更新 |
| `soc-ap` | `main` | `19534a9a4cb393176882fbad046129d55bba51f6`<br>*(初查: `79932746d225bb115010c5545ef3f7499482e137`)* | [soc-ap/AGENTS.md](file:///home/sushaohua/workspace/ai_soc_project/soc-ap/AGENTS.md)<br>`c3ef0100585a22113466086a11e7e413369a2615ce3d8afc772848e86271c955` | [SOURCE.json](file:///home/sushaohua/workspace/ai_soc_project/soc-ap/.agents/rules/shared/SOURCE.json)<br>`17e0887da07ceb3b017623b791b6a6999e837c79` (`fd9c1d52...`) | 跟踪树已干净（并行任务 `TWIN-57~59` 已提交为 `19534a9a`）；全程保持只读 |
| `mcu-p3` | `feat/soc-debug` | `191e355a4227268a472bafd6862d4a8c854e0544`<br>*(初查: `891a8bb252814c83992a49b01fbe11ba83b92a1f`)* | [mcu-p3/.repo-rules/AGENTS.md](file:///home/sushaohua/workspace/ai_soc_project/mcu-p3/.repo-rules/AGENTS.md)<br>`69b1ca579d6c6cfec2e26d5ffe53097c25c0e2c695dc5c614d781dd66c3a8375` | [SOURCE.json](file:///home/sushaohua/workspace/ai_soc_project/mcu-p3/.repo-rules/SOURCE.json)<br>`17e0887da07ceb3b017623b791b6a6999e837c79` (`c91cf048...`) | 跟踪树已干净（并行任务 `TWIN-60` 已提交为 `191e355a`）；全程保持只读 |
| `boot/bootloadermc` | `soc_debug` | `4fc171ea61912561949b9a0cfc1da8975e4c39ba` | [boot/bootloadermc/.repo-rules/AGENTS.md](file:///home/sushaohua/workspace/ai_soc_project/boot/bootloadermc/.repo-rules/AGENTS.md)<br>`d14b4256e02944738afb9ccc06a5e674ccbb43c0adc3d81bb172f8642d4d76b4` | [SOURCE.json](file:///home/sushaohua/workspace/ai_soc_project/boot/bootloadermc/.repo-rules/SOURCE.json)<br>`17e0887da07ceb3b017623b791b6a6999e837c79` (`1a814694...`) | 跟踪树干净（仅保留未跟踪本机符号链接 `.agents`、`AGENTS.md`、`docs`）；分支为 `soc_debug` |
| `boot/bootloaderth` | `soc_debug` | `769fccbe52464ad7ceb856c5e89cb0d25abbbf87` | [boot/bootloaderth/.repo-rules/AGENTS.md](file:///home/sushaohua/workspace/ai_soc_project/boot/bootloaderth/.repo-rules/AGENTS.md)<br>`c5667a15afbbae4c22681414e4e75e798cb03514b0d09e7946aa20abefb6697c` | [SOURCE.json](file:///home/sushaohua/workspace/ai_soc_project/boot/bootloaderth/.repo-rules/SOURCE.json)<br>`17e0887da07ceb3b017623b791b6a6999e837c79` (`ccda3a94...`) | 跟踪树干净（仅保留未跟踪本机符号链接 `.agents`、`AGENTS.md`、`docs`）；分支为 `soc_debug` |
| `test_harness` | `main` | `d14ed04321c6d4f5ddb35a8801604a8af53b5b60` | [test_harness/AGENTS.md](file:///home/sushaohua/workspace/ai_soc_project/test_harness/AGENTS.md)<br>`b0e9dc4f66dee01b8741c3e9f16c26f627c49a57444d56094528d68bc5b0010a` | [SOURCE.json](file:///home/sushaohua/workspace/ai_soc_project/test_harness/.agents/rules/shared/SOURCE.json)<br>`17e0887da07ceb3b017623b791b6a6999e837c79` (`54d841ee...`) | 工作树干净；全程保持只读 |

---

## 2. 全量协议契约冲突对账与裁定记录（先解决契约冲突，再定型升级接口）

本章响应 `20261105_minimc_v2_upgrade_coord_planning_prompt.md` (`revision: 3`) 第 2 节硬性要求：在冻结升级接口前，首先对主规范 [SPEC-PROTO-20261015-153000 (`Rev 2.0.3`)](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/specs/ap_mc_formal_protocol_v2_0_multidevice_routing_draft_20261015.md)、已接受扩展方案（[SPEC-ALIGN-20261102-01](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/specs/minimcproto_ack_nack_contract_alignment_matrix_20261102.md) 与 [PLAN-E2E-PHYSICAL-LINK-REMEDIATION-20261104 (`rev 3`)](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/planning/end_to_end_physical_link_remediation_plan_20261104.md)）、以及四端源码（[soc-ap/contracts/twin/telemetry_types.h](file:///home/sushaohua/workspace/ai_soc_project/soc-ap/contracts/twin/telemetry_types.h)、[soc-ap/services/forward/forward_protocol.h](file:///home/sushaohua/workspace/ai_soc_project/soc-ap/services/forward/forward_protocol.h)、[mcu-p3 MC minimc_proto.h](file:///home/sushaohua/workspace/ai_soc_project/mcu-p3/motion-controller-mcu/project/inc/minimc_proto.h)、[mcu-p3 TH minimc_proto.h](file:///home/sushaohua/workspace/ai_soc_project/mcu-p3/color-engine-mcu/io_toggle/inc/minimc_proto.h)、[boot/bootloaderth/inc/iap.h](file:///home/sushaohua/workspace/ai_soc_project/boot/bootloaderth/inc/iap.h)）与检查器（[check_opcode_alignment.py](file:///home/sushaohua/workspace/ai_soc_project/test_harness/static_checks/minimcproto/check_opcode_alignment.py)）进行逐命令、逐字段全量核对。

### 2.1 全量命令码（`0x00 ~ 0x50`）跨源对账总表

| Cmd ID | 主规范 `Rev 2.0.3` 定义<br>(`SPEC-PROTO-20261015-153000`) | 已批准扩展方案定义<br>(`PLAN-E2E-20261104 rev 3`) | 当前源码实现状态<br>(`soc-ap` / `MC App` / `TH App` / `TH Boot`) | 传输方向与 Flags (`v2=0x04`) | 请求/响应载荷布局、长度與单位 | 差异分类与定性 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **`0x00`** | `CMD_ACK`<br>双向确认应答 | `CMD_ACK`<br>(`0x17` 急停应答) | - `soc-ap`: `MINIMC_CMD_ACK = 0x00U`<br>- `MC/TH App`: `MINIMC_CMD_ACK = 0x00U`<br>- `TH Boot`: 无 (`5A A5` 私有应答) | 从 $\to$ 主<br>`Flags=0x06` (`IS_RESPONSE \| VER_2`) | - **主规范 `Rev 2.0.3` §5.1**：固定 **4B** (`uint8_t planner_buf_free`, `uint8_t rx_fifo_free_units`, `uint16_t reserved`)；<br>- **当前 `MC/TH App` (`0x17` 急停应答)**：发送 **0B** 载荷（14B 整帧） | **[功能子集 / 载荷长度分歧]**<br>主规范要求固定 `4B`，现有 `0x17` 实现发 `0B` |
| **`0x01`** | `CMD_GET_VERSION`<br>查询固件版本与能力 | `GET_VERSION` | - `soc-ap` / `MC App` / `TH App`: `0x01U` 均已实现<br>- `MC/TH Boot`: 待接入 | 主 $\to$ 从<br>`Flags=0x05` (`WANTS_ACK \| VER_2`) | 请求：**0B**（14B 整帧）；<br>预期响应：`0x02 VERSION_REPORT`（16B） | **[完全一致]** |
| **`0x02`** | `CMD_VERSION_REPORT`<br>版本与能力回报 | `VERSION_REPORT` | - `soc-ap` / `MC App` / `TH App`: `0x02U` 均已实现<br>- `MC/TH Boot`: 待接入 | 从 $\to$ 主<br>`Flags=0x06` (`IS_RESPONSE \| VER_2`) | 响应：固定 **16B** (`proto_ver_major:1B`, `proto_ver_minor:1B`, `fw_major:1B`, `fw_minor:1B`, `boot_id:4B`, `git_commit:4B`, `capability_flags:4B`) | **[完全一致]**<br>*(注：MC/TH 结构体前 4B 用 2 个 `uint16_t` 小端编码，字节序与 AP 4 个 `uint8_t` 兼容)* |
| **`0x03`** | `CMD_PING`<br>链路心跳测量 | `PING` | - `soc-ap` / `MC App` / `TH App`: `0x03U` 均已实现 | 双向<br>`Flags=0x05` | 请求：固定 **4B** (`uint32_t t_originate_ms`, 毫秒)；<br>预期响应：`0x04 PONG`（12B） | **[完全一致]** |
| **`0x04`** | `CMD_PONG`<br>心跳应答与流控信用 | `PONG` | - `soc-ap` / `MC App` / `TH App`: `0x04U` 均已实现（12B 载荷） | 双向<br>`Flags=0x06` | 响应：固定 **12B** (`t_originate_ms:4B`, `t_receive_ms:4B`, `planner_buf_free:1B`, `rx_fifo_free_units:1B`, `reserved:2B`) | **[完全一致]**<br>*(注：`PLAN-E2E-20261104` 表中曾简写为 8B，但三端真实源码均为 12B，符合主规范)* |
| **`0x05`** | *(未分配 / 保留)* | *(未分配)* | - `soc-ap`: `telemetry_types.h#L61` 定义了悬空宏 `MINIMC_CMD_ESTOP_ACK = 0x05U`（无任何源码引用）<br>- `MC/TH App`: 未定义 | — | 无 | **[历史残留死宏]**<br>`0x05` 并非 `CMD_ACK`（`CMD_ACK` 为 `0x00`），应清理悬空宏 `MINIMC_CMD_ESTOP_ACK` |
| **`0x06`** | `CMD_NACK`<br>否定应答 | `CMD_NACK` | - `soc-ap` / `MC App` / `TH App`: `0x06U`（经 `SPEC-ALIGN-20261102-01` 纠偏后三端均为 3B 载荷） | 双向<br>`Flags=0x06` | 响应：固定 **3B** (`uint8_t error_code`, `uint16_t expected_seq` LE) | **[完全一致]** |
| **`0x07`** | `CMD_LOG_MESSAGE`<br>异步调试日志输出 | *(未启用，走独立物理 Debug 串口)* | - `soc-ap`: `telemetry_types.h#L63` 声明宏 `0x07U`（未调用）<br>- `MC/TH App`: 未实现（按用户确认走独立 `115200` 物理 Debug 口输出 `[MC-DBG]`/`[TH-DBG]`） | 从 $\to$ 主<br>`Flags=0x04` (单向) | 变长 **2~128B** (`level:1B`, `module_id:1B`, `message[]`) | **[功能子集 / 架构保留]**<br>首发采用独立物理 Debug 串口，线缆协议预留 `0x07` 不冲突 |
| **`0x10`** | **`CMD_SYSTEM_CONTROL`**<br>系统控制（Reboot / 跳入 Bootloader） | **`SET_TEMP`**<br>设定喷嘴/热床目标温度 | - `soc-ap`: `telemetry_types.h#L64-L65` **同时定义** `MINIMC_CMD_SYSTEM_CONTROL = 0x10U` 与 `MINIMC_CMD_SET_TEMP = 0x10U`；`forward_protocol.cpp` 按 `SET_TEMP (4B)` 发送<br>- `MC/TH App`: 定义 `MINIMC_CMD_SET_TEMP = 0x10U` (4B)，回 `0x15 TEMP_REPORT` (16B)<br>- `TH Boot`: 旧私有 `5A A5` 中 `0x10 = IAP_CMD_START` | 主 $\to$ 从<br>`Flags=0x05` | - **主规范 `Rev 2.0.3` §5.2.4**：固定 **3B** (`uint8_t action` [0=Noop, 1=Reboot, 2=JumpToBootloader], `uint16_t delay_ms`)，回 `0x00 CMD_ACK`<br>- **当前业务实现 (`SET_TEMP`)**：固定 **4B** (`int16_t nozzle_target_deci_c`, `int16_t bed_target_deci_c`, 单位 `0.1°C`)，回 `0x15` (16B) | **[核心语义冲突 D1]**<br>同一命令码 `0x10` 在主规范与已实现业务间存在**严重同码异义冲突**（详见 §2.3.1 裁定） |
| **`0x11`** | *(未定义)* | `MOTION_HOME`<br>轴归零控制 (`G28`) | - `soc-ap` / `MC App` / `TH App`: `MINIMC_CMD_MOTION_HOME = 0x11U` | 主 $\to$ 从<br>`Flags=0x05` | 请求：固定 **4B** (`axes_mask:1B`, `reserved:1B`, `feedrate_mm_s:2B`)；<br>响应：`0x16 POS_REPORT`（20B） | **[已批准业务扩展]**<br>主规范未占用 `0x11`，但需在主规范 `Rev 2.0.4` 正式登记（注：结构体字段名 `feedrate_mm_s` 注释写有 `mm/min 或 mm/s`，需统一明确单位为 `mm/s`） |
| **`0x12`** | **`CMD_EMERGENCY_STOP`**<br>全网特权广播急停 | **`MOTION_MOVE`**<br>点动/坐标直线移动 (`G0/G1`) | - `soc-ap`: `telemetry_types.h#L67` 定义 `MINIMC_CMD_MOTION_MOVE = 0x12U`（而将 `MINIMC_CMD_EMERGENCY_STOP` 改定义为 `0x17U`）<br>- `MC/TH App`: `MINIMC_CMD_MOTION_MOVE = 0x12U` (16B)<br>- `test_harness`: `reference_vectors.py` 黄金向量 `V04` 仍测试 `0x12 = EMERGENCY_STOP` (`DST=0xFF, Flags=0x14, Len=0`)！ | - 主规范：主 $\to$ `0xFF`, `Flags=0x14` (`IS_PRIORITY \| VER_2`), 无即时 ACK<br>- 现实现：主 $\to$ `0x02`, `Flags=0x05`, 回 `0x16` | - **主规范 `Rev 2.0.3` §5.2.4 / §7 V04**：固定 **2B** (`uint16_t reason_code`) 或 V04 **0B**，无即时 ACK<br>- **当前业务实现 (`MOTION_MOVE`)**：固定 **16B** (`axes_mask:1B`, `is_relative:1B`, `feedrate_mm_min:2B`, `x_um:4B`, `y_um:4B`, `z_um:4B`, 微米 `um`)，回 `0x16 POS_REPORT` (20B) | **[核心语义冲突 D2]**<br>同一命令码 `0x12` 在主规范（及 `V04` 黄金向量）中为**广播急停**，而在业务代码中被改作**点动移动**（详见 §2.3.2 裁定） |
| **`0x13`** | *(未定义)* | `JOB_CONTROL`<br>打印作业状态机控制 | - `soc-ap` / `MC App` / `TH App`: `MINIMC_CMD_JOB_CONTROL = 0x13U` | 主 $\to$ MC<br>`Flags=0x05` | 请求：固定 **4B** (`job_op:1B`, `reserved:1B`, `total_lines:2B`)；<br>响应：`0x13` 固定 **8B** (`job_state:1B`, `ack_seq:1B`, `progress_permille:2B`, `executed_lines:2B`, `total_lines:2B`) | **[已批准业务扩展]**<br>*(注：`telemetry_types.h#L260` 与 `MC minimc_proto.h#L230` 末尾为 2 个 `uint16_t` (`executed_lines + total_lines = 4B`)，而 `PLAN-E2E` 曾写为 `uint32_t executed_lines`，以代码一致的 `2B+2B` 锁定)* |
| **`0x14`** | *(未定义)* | `TEMP_QUERY`<br>单节点温度查询 | - `soc-ap`: `MINIMC_CMD_TEMP_QUERY = 0x14U`<br>- `MC App`: `MINIMC_CMD_TEMP_QUERY = 0x14U`（且定义别名 `MINIMC_CMD_GET_TEMP = 0x14U`）<br>- `TH App`: 定义 `MINIMC_CMD_GET_TEMP = 0x14U`（在 `minimc_telemetry.h`） | 主 $\to$ 从<br>`Flags=0x05` | 请求：固定 **0B**（14B 整帧）；<br>响应：`0x15 TEMP_REPORT`（16B） | **[合法别名 + 已批准扩展]**<br>`MINIMC_CMD_TEMP_QUERY` 与 `MINIMC_CMD_GET_TEMP` 均为 `0x14U` |
| **`0x15`** | *(未定义)* | `TEMP_REPORT`<br>单节点温度响应上报 | - `soc-ap`: `MINIMC_CMD_TEMP_REPORT = 0x15U`<br>- `MC App`: `MINIMC_CMD_TEMP_REPORT = 0x15U`，同时残留旧别名 `#define MINIMC_CMD_FILAMENT_CONTROL 0x15U`<br>- `TH App`: `MINIMC_CMD_TEMP_REPORT_V2 = 0x15U`（`minimc_telemetry.h` 含 `MINIMC_CMD_TEMP_REPORT = 0x15U`），同时残留 `#define MINIMC_CMD_FILAMENT_CONTROL 0x15U` | 从 $\to$ 主<br>`Flags=0x06` | 响应：固定 **16B** (`current_temp_deci_c:2B`, `target_temp_deci_c:2B`, `raw_adc_value:2B`, `sensor_status:1B`, `heater_duty_percent:1B`, `sample_timestamp_ms:4B`, `reserved:4B`) | **[合法别名 + 历史残留宏清理]**<br>`TEMP_REPORT` / `TEMP_REPORT_V2` 属合法同名；但 MC/TH 头文件中残留的 `MINIMC_CMD_FILAMENT_CONTROL = 0x15U` 应统一收敛至 `0x19U`（与 `telemetry_types.h#L76` 对齐） |
| **`0x16`** | *(未定义)* | `POS_QUERY` / `POS_REPORT`<br>坐标与归零状态查询 | - `soc-ap` / `MC App` / `TH App`: `MINIMC_CMD_POS_QUERY = 0x16U` | 主 $\leftrightarrow$ MC<br>`0x05` / `0x06` | 请求：**0B**；<br>响应：`0x16` 固定 **20B** (`x_um:4B`, `y_um:4B`, `z_um:4B`, `e_um:4B`, `mc_state:1B`, `homed_mask:1B`, `reserved:2B`) | **[已批准业务扩展]** |
| **`0x17`** | *(未定义)* | `MOTION_STOP`<br>紧急停止控制 | - `soc-ap`: `telemetry_types.h#L72-L73` 同时定义 `MINIMC_CMD_MOTION_STOP = 0x17U` 与 `MINIMC_CMD_EMERGENCY_STOP = 0x17U`<br>- `MC/TH App`: `MINIMC_CMD_MOTION_STOP = 0x17U` | 主 $\to$ 从<br>`Flags=0x05` (单播) 或 `0x15` (广播) | 请求：固定 **1B** (`uint8_t stop_mode`: `1=QuickStop/E-Stop, 0=Clear`)；<br>响应：单播回 `0x00 CMD_ACK` | **[与 `0x12` 联动的急停契约冲突]**<br>详见 §2.3.2 裁定 |
| **`0x18`** | *(未定义)* | `LEVEL_GRID_QUERY`<br>5×5 调平网格查询与上报 | - `soc-ap` / `MC App` / `TH App`: `MINIMC_CMD_LEVEL_GRID_QUERY = 0x18U` | 主 $\leftrightarrow$ MC<br>`0x05` / `0x06` | 请求：固定 **1B** (`uint8_t probe_idx = 7U`，MC 兼容 0B/1B)；<br>响应：`0x18` 固定 **52B** (`grid_x:1B=5`, `grid_y:1B=5`, `z_offset_um[25]:50B`, 微米 `um`) | **[已批准业务扩展]** |
| **`0x19`** | *(未定义)* | `SLOT_SELECT`<br>多色选槽与进退丝控制 | - `soc-ap`: `MINIMC_CMD_SLOT_SELECT = 0x19U`、`MINIMC_CMD_FILAMENT_CONTROL = 0x19U`<br>- `MC/TH App`: `MINIMC_CMD_SLOT_SELECT = 0x19U` | 主 $\leftrightarrow$ MC/TH<br>`0x05` / `0x06` | 请求：固定 **4B** (`slot_id:1B`, `action:1B` [0=SELECT, 1=LOAD, 2=UNLOAD], `length_mm:2B`)；<br>响应：`0x19` 固定 **4B** (`active_slot:1B`, `present_mask:1B`, `step_state:1B`, `status_code:1B`) | **[已批准业务扩展]** |
| **`0x1A`** | *(未定义)* | `LEVEL_TRIGGER`<br>触发 G29 自动调平 | - `soc-ap` / `MC App` / `TH App`: `MINIMC_CMD_LEVEL_TRIGGER = 0x1AU` | 主 $\to$ MC<br>`Flags=0x05` | 请求：**0B** 或 **1B** (`mode=1`)；<br>响应：`0x18 LEVEL_GRID_REPORT`（52B） | **[已批准业务扩展]** |
| **`0x1B`** | *(未定义)* | `FILAMENT_LEGACY`<br>历史兼容接收码 | - `soc-ap`: 已移除发送<br>- `MC/TH App`: `MINIMC_CMD_FILAMENT_LEGACY = 0x1BU`（仅接收侧兼容转发至 `0x19` 处理函数） | 仅接收兼容 | 同 `0x19`（4B） | **[合法向后兼容别名]**<br>发送端已统一为 `0x19` |
| **`0x1C`** | *(未定义)* | `GCODE_EXEC`<br>受控单行 G-code 执行 | - `soc-ap` / `MC App` / `TH App`: `MINIMC_CMD_GCODE_EXEC = 0x1CU` | 主/MC $\to$ MC/TH<br>`0x05` / `0x06` | 请求：变长 **2B + `line_len`**（最大 `62B`：`line_len:1B` [1..60], `exec_flags:1B`, `gcode[line_len]`）；<br>响应：`0x1C` 固定 **4B** (`status:1B`, `queue_free:1B`, `ack_seq:2B` LE) | **[已批准业务扩展]**<br>*(注：源码真实字段顺序为 `line_len(偏移0) + exec_flags(偏移1)`，响应末 2B 为 `uint16_t ack_seq`)* |
| **`0x20`** | **`CMD_OTA_START`**<br>固件升级开始握手 | *(未覆盖)* | - `soc-ap`: `telemetry_types.h#L79` 仅声明宏 `0x20U`，无结构体与实现<br>- `MC/TH App` & `Boot`: 未实现 | 主 $\to$ 从<br>`Flags=0x05` | - **主规范 `Rev 2.0.3` §5.2.5(1)**：固定 **16B** (`target_device:1B`, `target_component:1B`, `force_flag:1B`, `reserved:1B`, `fw_size_bytes:4B`, `fw_crc32:4B`, `new_version_raw:4B`)，回 `0x00 CMD_ACK`<br>- **Boot 准入需求**：擦除前必须校验 `128B ATSG Trailer` | **[待定型升级契约冲突 D3]**<br>16B `OTA_START` 与擦除前校验 128B `ATSG` Trailer 的衔接需在统一契约中裁定（见 §2.3.4） |
| **`0x21`** | **`CMD_OTA_DATA`**<br>固件分块数据传输 | *(未覆盖)* | - `soc-ap`: `telemetry_types.h#L80` 仅声明宏 `0x21U`<br>- `MC/TH App` & `Boot`: 未实现 | 主 $\to$ 从<br>`Flags=0x05` | **主规范 `Rev 2.0.3` §5.2.5(2)**：**8B 帧内头** (`offset:4B`, `chunk_bytes:2B`, `chunk_crc16:2B`) + `firmware_bytes[chunk_bytes]`（主规范写 `64~1016B`），回 `0x00 CMD_ACK` | **[待定型升级契约冲突 D3]**<br>与 MCU `MINIMC_MAX_PAYLOAD_SIZE = 64B` 及 TH 首块缓存 ACK 语义冲突（见 §2.3.3 & §4） |
| **`0x22`** | **`CMD_OTA_FINISH`**<br>固件传输结束与全量校验 | *(未覆盖)* | - `soc-ap`: `telemetry_types.h#L81` 仅声明宏 `0x22U`<br>- `MC/TH App` & `Boot`: 未实现 | 主 $\to$ 从<br>`Flags=0x05` | **主规范 `Rev 2.0.3` §5.2.5(3)**：固定 **8B** (`uint32_t fw_crc32`, `uint8_t action_after_verify`, `uint8_t reserved[3]`)，回 `0x00 CMD_ACK` | **[完全可复用主规范 8B 布局]**<br>`reserved[3]` 可扩展或结合 `0x23` 表达提交状态 |
| **`0x23`** | **`CMD_OTA_STATUS`**<br>升级进度与状态查询 | *(未覆盖)* | - `soc-ap`: `telemetry_types.h#L82` 仅声明宏 `0x23U`<br>- `MC/TH App` & `Boot`: 未实现 | 双向<br>`0x05` / `0x06` | **主规范 `Rev 2.0.3` §5.2.5(4)**：查询请求 **0B**（或带受控中止参数），响应固定 **8B** (`uint8_t ota_state`, `uint8_t error_code`, `uint16_t reserved`, `uint32_t bytes_written`) | **[完全可复用主规范 8B 布局]**<br>`bytes_written` 严格定义为**已物理写入 Flash 并读回校验通过的字节数** |
| **`0x31`** | `CMD_STREAM_CHUNK`<br>批量切片数据原子入队 | *(由 `0x1C` 替代单行，保留批量扩展)* | - `soc-ap`: `telemetry_types.h#L83` 仅声明宏 `0x31U`<br>- `MC/TH App`: 未实现 | AP $\to$ MC<br>`Flags=0x05` | **8B 事务头** (`job_id:2B`, `chunk_seq:2B`, `text_bytes:2B`, `chunk_flags:1B`, `reserved:1B`) + `gcode_text[]` | **[功能子集 / 预留未启用]**<br>与现有 `0x00~0x23` 无命令码冲突 |
| **`0x40`** | `CMD_TELEMETRY_REPORT`<br>36B 综合状态单向广播 | *(当前采用 `0x14/0x15` + `0x16` 轮询)* | - `soc-ap`: `telemetry_types.h#L84` 仅声明宏 `0x40U`<br>- `MC/TH App`: 未实现 | 从 $\to$ 主<br>`Flags=0x04` | 固定 **36B** (`minimc_payload_telemetry`) | **[功能子集 / 预留未启用]**<br>与现有 `0x14/0x15/0x16` 轮询模式无命令码冲突 |
| **`0x50`** | `CMD_ALARM_EVENT`<br>硬件告警与异常上报 | *(未启用)* | - `soc-ap`: `telemetry_types.h#L85` 仅声明宏 `0x50U`<br>- `MC/TH App`: 未实现 | 从 $\to$ 主<br>`Flags=0x05` | 固定 **8B** (`alarm_level:1B`, `subsystem_id:1B`, `error_code:2B`, `param:4B`) | **[功能子集 / 预留未启用]**<br>无命令码冲突 |

---

### 2.2 四大核心协议契约冲突深度剖析与裁定方案

#### 2.2.1 冲突 D1：`0x10` 主规范 `CMD_SYSTEM_CONTROL (3B)` vs 现有实现 `MINIMC_CMD_SET_TEMP (4B)`

1. **冲突根因与现状风险**：
   - 主规范 `Rev 2.0.3` §5.1 将 `0x10` 定义为 `CMD_SYSTEM_CONTROL`（3B 载荷：`uint8_t action` [`0=Noop, 1=Reboot, 2=JumpToBootloader`], `uint16_t delay_ms` LE，应答 `0x00 CMD_ACK`）。
   - `PLAN-E2E-PHYSICAL-LINK-REMEDIATION-20261104` 在补齐 Web UI 温控下发闭环时，未核对主规范 `0x10` 已被 `CMD_SYSTEM_CONTROL` 占用，将 `0x10` 分配给了 `MINIMC_CMD_SET_TEMP`（4B 载荷：`int16_t nozzle_target_deci_c`, `int16_t bed_target_deci_c`，应答 `0x15 TEMP_REPORT`）。
   - 当前 [soc-ap/contracts/twin/telemetry_types.h#L64-L65](file:///home/sushaohua/workspace/ai_soc_project/soc-ap/contracts/twin/telemetry_types.h#L64-L65) 中甚至出现了 `#define MINIMC_CMD_SYSTEM_CONTROL 0x10U` 与 `#define MINIMC_CMD_SET_TEMP 0x10U` **同值异义并存**的危险状态！一旦在升级方案中启用 `CMD_SYSTEM_CONTROL (JumpToBootloader)` 而继续使用 `0x10`，AP 或 MCU 极易因 3B vs 4B 载荷解析错位导致**设温请求被误判为重启/跳入 Bootloader，或跳入 Bootloader 指令被当作设定温度**！
2. **严禁同码混用原则**：
   **绝不允许通过“按 3B 还是 4B 载荷长度区分同一 `0x10` 命令是设温还是重启进 Boot”这种脆弱隐式约定来掩盖冲突！** `CMD_SYSTEM_CONTROL`（系统复位/进入 Bootloader）属于高危系统维护指令，必须拥有全局唯一、独立于 `SET_TEMP` 的专属 `cmd_id`。
3. **跨端兼容与迁移影响对比（供完整方案一次确认）**：

| 裁定候选方案 | 命令码分配规则 | 对已验收业务闭环（`TWIN-47~60`）的影响 | 需同步修改的具体文件清单 | 架构师推荐度 |
| :--- | :--- | :--- | :--- | :--- |
| **方案 D1-A（推荐：最小业务破坏 + 显式分配 `0x1D = CMD_SYSTEM_CONTROL`）** | - 保持 **`0x10 = MINIMC_CMD_SET_TEMP`**（4B，设温）；<br>- 将 **`CMD_SYSTEM_CONTROL`**（系统复位 / 跳入 Bootloader，4B 对齐载荷：`uint8_t action`, `uint8_t target_component`, `uint16_t delay_ms`）正式分配至未占用的 **`0x1D`**；<br>- 同步将主规范升级为 `Rev 2.0.4` 正式纳管 `0x10~0x1D`。 | **零破坏**：已通过真机 HIL 验收的 `0x10 -> 0x15` 设温链路、Web UI 温控 API、以及现有单元测试与抓包解码器 100% 免改动保持绿色。 | 1. `project-control/docs/specs/ap_mc_formal_protocol_v2_0...`（升级至 `Rev 2.0.4`，登记 `0x10=SET_TEMP`, `0x1D=SYSTEM_CONTROL`）；<br>2. `soc-ap/contracts/twin/telemetry_types.h#L64`（将 `MINIMC_CMD_SYSTEM_CONTROL` 从 `0x10U` 改为 `0x1DU`）；<br>3. `mcu-p3` MC/TH `minimc_proto.h` & `bootloadermc`/`bootloaderth`（新增 `MINIMC_CMD_SYSTEM_CONTROL = 0x1DU`）；<br>4. `test_harness/static_checks/minimcproto/check_opcode_alignment.py`（增加 `0x1D` 与唯一性检查）。 | **首选推荐**<br>（兼顾规范唯一性与存量 HIL 稳定性） |
| **方案 D1-B（备选：严格恢复 `Rev 2.0.3` 原号 `0x10 = SYSTEM_CONTROL`，将 `SET_TEMP` 迁至 `0x1D`）** | - 恢复 **`0x10 = MINIMC_CMD_SYSTEM_CONTROL`**（3B/4B，重启/进 Boot）；<br>- 将 **`MINIMC_CMD_SET_TEMP`**（4B，设温）整体迁移至 **`0x1D`**。 | 需同步修改 AP/MC/TH 三端设温常量、重编重刷两板 App 并全量更新设温单测与对账探针。 | 除方案 D1-A 的 4 处文件外，还需修改：<br>5. `soc-ap/tests/forward/twin/test_forward_protocol.cpp`；<br>6. `mcu-p3/motion-controller-mcu/tests/test_mc_proto_v2.c`；<br>7. `mcu-p3/color-engine-mcu/tests/test_th_proto_v2.c`；<br>8. `test_harness/hil/tools/debug_reconciliation_probe.py`（`cmd=0x10` 对账断言改为 `0x1D`）。 | 次选备选<br>（仅在不允许修订主规范 `0x10` 原号时采用） |

---

#### 2.2.2 冲突 D2：`0x12` 主规范 `CMD_EMERGENCY_STOP` vs 现有实现 `MINIMC_CMD_MOTION_MOVE (16B)` 与 `0x17 MOTION_STOP (1B)`

1. **冲突根因与现状风险**：
   - 主规范 `Rev 2.0.3` §5.1、§5.2.4 及 §7 黄金测试向量 `V04` 将 `0x12` 定义为全网特权广播急停 `CMD_EMERGENCY_STOP`（`DST=0xFF`, `Flags=0x14 [IS_PRIORITY | VER_2]`, `WANTS_ACK=0`，载荷 2B `uint16_t reason_code` 或 V04 的 0B，全网节点收到后立即切断加热与电机且不回即时 ACK）。
   - 而在 `PLAN-E2E-PHYSICAL-LINK-REMEDIATION-20261104` 及现有 `soc-ap` / `mcu-p3` 代码中：
     - `0x12` 被实现为 **`MINIMC_CMD_MOTION_MOVE`**（16B 点动/直线坐标移动请求，`DST=0x02`, `Flags=0x05`, 回 `0x16 POS_REPORT`）；
     - 急停被移到了 **`0x17`**（`telemetry_types.h#L72-L73` 同时定义 `MINIMC_CMD_MOTION_STOP = 0x17U` 与 `MINIMC_CMD_EMERGENCY_STOP = 0x17U`）；
     - 且 [soc-ap/services/forward/forward_protocol.cpp#L99-L129](file:///home/sushaohua/workspace/ai_soc_project/soc-ap/services/forward/forward_protocol.cpp#L99-L129) 中 `fwd_proto_build_estop_frame()` 构造的是 `DST=0xFF, Flags=0x15 (WANTS_ACK=1 | VER_2 | IS_PRIORITY), CMD=0x17, Len=1`，而 Web UI 实际急停路由调用的是单播 `fwd_proto_build_motion_stop_frame(dst_id, 0x01, seq, ...)`（`CMD=0x17, DST=0x02/0x03, Flags=0x05, Len=1`，期望 `0x00 CMD_ACK`）。
     - 与此同时，`test_harness/static_checks/minimcproto/reference_vectors.py` 中的 `V04` 黄金向量仅作为纯 Codec 编解码帧测试（不调业务分发），仍寫着 `55 AA 01 FF 14 12 04 00 00 00 00 00 3D C1` (`Cmd=0x12`)。
   - **安全风险警告**：若任何遵循主规范 `Rev 2.0.3` 的模块或测试工具向 MC 发送 `Cmd=0x12` 的广播急停帧，MC App 当前的 `handle_mc_motion_and_level()` 会将其当作 `MOTION_MOVE`（因 `plen < 16` 返回 `NACK 0x02`），**导致急停失效**！
2. **跨端兼容与迁移影响对比**：

| 裁定候选方案 | 命令码与急停语义分配规则 | 安全急停保障与跨端迁移成本分析 | 架构师推荐度 |
| :--- | :--- | :--- | :--- |
| **方案 D2-A（推荐：在 `Rev 2.0.4` 中正式锁定 `0x12 = MOTION_MOVE`、`0x17 = EMERGENCY_STOP / MOTION_STOP`，并修复广播/单播双重急停契约）** | - 锁定 **`0x12 = MINIMC_CMD_MOTION_MOVE`**（16B 单播坐标移动，`DST=0x02`）；<br>- 锁定 **`0x17 = MINIMC_CMD_EMERGENCY_STOP`（同义别名 `MINIMC_CMD_MOTION_STOP`）** 为全系统唯一急停指令码，支持两种寻址模式：<br>  1. **在线受控单播急停（主路径，符合 `AGENTS.md` §7 显式 ACK 门禁）**：`DST=0x02` / `0x03`, `Flags=0x15 (IS_PRIORITY \| VER_2 \| WANTS_ACK)`, `Len=1B/2B`，目标节点立即执行 `quickStop()` + 加热归零，并回发 `0x00 CMD_ACK`；<br>  2. **全网特权广播急停（`DST=0xFF`）**：`Flags=0x14 (IS_PRIORITY \| VER_2, WANTS_ACK=0)`, `Len=0B/2B`，MC 本地立即急停并向 TH 广播转发，不产生 ACK 风暴；<br>- 同步更新主规范 `Rev 2.0.4`（含黄金向量 `V04` 的 `Cmd=0x17` 新 CRC `55 AA 01 FF 14 17 04 00 00 00 00 00 6C 9E`）。 | 1. 彻底消除“发 `0x12` 急停却进入 `MOTION_MOVE` 分支”的安全隐患；<br>2. 既满足 `AGENTS.md` §7“凡下发控制指令必绑定超时显式 ACK 闭环”的硬性门禁（单播 `0x17`），又保留主规范广播急停能力；<br>3. 已验收的 `0x12 MOTION_MOVE` 与 `0x17 MOTION_STOP` 业务代码免受翻盘重改。 | **首选推荐** |
| **方案 D2-B（备选：恢复 `Rev 2.0.3` 原号 `0x12 = EMERGENCY_STOP`，将 `MOTION_MOVE` 迁至 `0x1E`）** | - 恢复 **`0x12 = MINIMC_CMD_EMERGENCY_STOP`**；<br>- 将 **`MINIMC_CMD_MOTION_MOVE` (16B)** 迁移至新命令码 **`0x1E`**；<br>- `0x17` 保留为单轴/普通运动停止或作为 `0x12` 的过渡兼容别名。 | 需同步修改 `soc-ap`、`mcu-p3` (MC/TH)、`test_harness` 中所有涉及 `0x12 MOTION_MOVE` 的宏、单测与 HIL 对账脚本。 | 次选备选 |

---

#### 2.2.3 冲突 D3：`0x00 CMD_ACK` 载荷长度分歧（主规范固定 `4B` vs 现有急停应答 `0B`）与升级确认语义

1. **分歧事实核查**：
   - 主规范 `Rev 2.0.3` §5.1 与 [minimcproto_ack_nack_contract_alignment_matrix_20261102.md](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/specs/minimcproto_ack_nack_contract_alignment_matrix_20261102.md#L56-L78) 明确规定：`CMD_ACK (0x00)` 载荷长度固定为 **4 字节** (`uint8_t planner_buf_free`, `uint8_t rx_fifo_free_units`, `uint16_t reserved`，整帧 18 字节）。
   - 而在 `mcu-p3` 现有 `0x17 MOTION_STOP` 应答实现中（[MC minimc_proto.c#L1687](file:///home/sushaohua/workspace/ai_soc_project/mcu-p3/motion-controller-mcu/project/src/minimc_proto.c#L1687)、[TH minimc_proto.c#L475](file:///home/sushaohua/workspace/ai_soc_project/mcu-p3/color-engine-mcu/io_toggle/src/app/minimc_proto.c#L475)），返回的 `0x00 CMD_ACK` 载荷为 **0 字节**（整帧 14 字节），且 `soc-ap` 的 `fwd_proto_check_ctrl_response()` 按 `expected_payload_len = 0` 接收。
   - 同时，在本报告 `revision: 1` 初稿中曾误将 `CMD_ACK` 写为 `0x05` 并拟定 8B 载荷——经与主规范 `Rev 2.0.3` 及 `SPEC-ALIGN-20261102-01` 对账，**`CMD_ACK` 必须严格锁定为 `0x00`，`CMD_NACK` 严格锁定为 `0x06`（3B），而 8 字节升级状态与实际写入字节数应由主规范原生的 `0x23 CMD_OTA_STATUS`（8B：`ota_state`, `error_code`, `reserved`, `bytes_written`）承载**！
2. **统一裁定**：
   - **`0x00 CMD_ACK`**：在 OTA 升级与主规范标准交互中，统一生成标准 **4 字节载荷** `minimc_payload_ack_t`（`planner_buf_free: 1B`, `rx_fifo_free_units: 1B`, `reserved: 2B`，整帧 18 字节）；AP 解析端对 `0x17 MOTION_STOP` 兼容接收 `0B` 或 `4B` 载荷的 `0x00 CMD_ACK`，后续可将 MCU 端 `0x17` 应答一并补齐为标准 4B `0x00 CMD_ACK`。
   - **`0x05` 悬空宏清理**：删除 `soc-ap/contracts/twin/telemetry_types.h#L61` 中从未使用的悬空宏 `#define MINIMC_CMD_ESTOP_ACK 0x05U`。

---

#### 2.2.4 冲突 D4：最大载荷（AP `1024B` vs MCU `64B`）与 `0x20 CMD_OTA_START`（主规范 `16B` vs `128B ATSG Trailer` 擦除前准入）

1. **最大载荷不一致裁定**：
   - 主规范 `Rev 2.0.3` 定义协议理论上限 `MAX_PAYLOAD_SIZE = 1024B`（`soc-ap/core/forward/minimc/codec.h#L21` 已按 `1024B` 实现），而 `mcu-p3` MC/TH App 因早期仅跑短控制帧被设为了 `MINIMC_MAX_PAYLOAD_SIZE = 64U`。
   - **分层 MTU 契约裁定**：
     - 协议规范层维持帧格式上限 `MAX_PAYLOAD_SIZE = 1024B`；
     - 嵌入式端点协商上限（Negotiated Endpoint MTU）按 `0x02 VERSION_REPORT.capability_flags` 声明并统一收敛至 **`520B` 载荷（`534B` 整帧，对应 `8B OTA_DATA 头 + 512B 净固件分块`，默认发送分块 `256B` 净荷即 `264B` 载荷）**；详情见第 3 章缓冲区核算。
2. **`0x20 CMD_OTA_START` 16B 与 `128B ATSG Trailer` 擦除前准入的两种规范化映射方案对比**：
   - **问题核心**：主规范 `Rev 2.0.3` §5.2.5(1) 定义 `CMD_OTA_START (0x20)` 载荷为固定 **16 字节**（仅含 `target_device`, `target_component`, `force_flag`, `reserved`, `fw_size_bytes`, `fw_crc32`, `new_version_raw`），不包含 `bootloadermc` / `bootloaderth` 所需的 **128 字节 `ATSG` `fw_trailer_t`**（含 `magic="ATSG"`, `board_id`, `load_addr`, `payload_sha256[32]`, `header_crc32` 等，且 TH Boot 在 `OTA_FINISH` 时需将完整 128B `fw_trailer_t` 写入 `0x0803F800` Sector 127 的 `app_anchor_meta_t`！）。若未收齐并校验 128B Trailer 就擦除 Flash，将违反“擦除前完成 Trailer 准入校验”的安全门禁。
   - **候选方案对比与推荐**：

| 候选方案 | `0x20 CMD_OTA_START` 载荷与擦除时机设计 | 优势 | 劣势 / 修改点 | 架构师推荐度 |
| :--- | :--- | :--- | :--- | :--- |
| **方案 T-A（推荐：`0x20 CMD_OTA_START` 扩展为 `16B 标准头 + 128B ATSG Trailer = 144B` 原子准入帧）** | 在 `Rev 2.0.4` 中将 `0x20 CMD_OTA_START` 正式定义为 **144 字节**（前 16B 完全保持 `Rev 2.0.3` `minimc_payload_ota_start` 字段偏移不变，紧随其后附加 `128B fw_trailer_t`）。Bootloader 收到 `0x20` 单帧后，立即完成 16B 与 128B Trailer 的交叉校验（`magic`、`board_id`、`fw_size_bytes == trailer.payload_size <= APP_MAX_SIZE`、`header_crc32`），**全部通过后才执行首扇区与 Anchor 预擦除并回 `0x00 CMD_ACK`**；校验失败直接回 `0x06 CMD_NACK`，**零 Flash 擦写**。 | 1. **擦除前准入最彻底、状态机最简洁**：单帧完成全量元数据校验，绝不存在“收了 16B `OTA_START` 却还没收到 Trailer 时擦不擦除 Flash”的中间态；<br>2. `144B` 远小于 `520B` MTU，无需分片；<br>3. 前 16B 与 `Rev 2.0.3` 100% 偏移兼容。 | 需在主规范 `Rev 2.0.4` 中将 `0x20` 载荷长度从 `16B` 更新为 `144B`（`16B + 128B Trailer`）。 | **首选推荐** |
| **方案 T-B（备选：保持 `0x20` 固定 `16B` 不擦除，由第一帧特殊 `OTA_DATA` 传递 128B Trailer 后再触发擦除）** | `0x20 CMD_OTA_START` 保持 `16B`（仅做长度与版本初筛，**不擦除 Flash**）；紧接着发送一帧携带 128B Trailer 的元数据帧，校验通过后才在写第一块数据前执行擦除。 | 字面保持 `0x20` 的 `16B` 长度。 | 违背主规范 §5.2.5(1)“收到 `OTA_START` 擦除目标扇区成功后回送 `CMD_ACK`”的时序定义，且 `OTA_DATA` `offset=0` 会产生“到底是 Trailer 还是固件首字节”的偏移语义混乱。 | 不推荐 |

---

### 2.3 对 `test_harness/static_checks/minimcproto/check_opcode_alignment.py` 的专项审计

经只读审阅 [test_harness/static_checks/minimcproto/check_opcode_alignment.py](file:///home/sushaohua/workspace/ai_soc_project/test_harness/static_checks/minimcproto/check_opcode_alignment.py#L1-L137)（`sha256: bcc098de7793d08c79f391be82f55a1d3b099b9984f8db08952722ad8b1253e9`），核实其真实行为与结构性局限如下：

1. **硬编码预期来源审计**：
   - 该脚本第 `10~28` 行的 `EXPECTED_OPCODES` 列表共硬编码了 **17 个命令码**（`0x00, 0x01, 0x02, 0x03, 0x04, 0x06, 0x10, 0x11, 0x12, 0x13, 0x15, 0x16, 0x17, 0x18, 0x19, 0x1A, 0x1C`），其中直接将 `0x10` 写死为 `("SET_TEMP", 0x10, ("MINIMC_CMD_SET_TEMP",))`，将 `0x12` 写死为 `("MOTION_MOVE", 0x12, ("MINIMC_CMD_MOTION_MOVE",))`。
   - **结论**：该脚本是在 `TWIN-49` 阶段根据当时 `PLAN-E2E-PHYSICAL-LINK-REMEDIATION-20261104` 的业务实现编写的**三端实现自洽性检查器**，而非源自 `SPEC-PROTO-20261015-153000` (`Rev 2.0.3`) 主规范的合规性门禁。因此，“`check_opcode_alignment.py` 输出 17 个命令码 100% aligned”**只能证明 `telemetry_types.h`、MC `minimc_proto.h`、TH `minimc_proto.h` 三个文件的这 17 个宏名数值相同，绝不能证明符合主规范 `Rev 2.0.3`**！
2. **三大检测盲区（即使存在严重协议冲突仍会误报 `[PASSED]`）**：
   - **盲区 1：不检测“同值异义碰撞（Opcode Value Collision）”**：
     `resolve_endpoint_opcode()`（第 49~65 行）仅正向查找 `aliases` 中指定的宏名（如 `MINIMC_CMD_SET_TEMP`）在单个头文件中是否等于 `0x10`；当 [telemetry_types.h#L64-L65](file:///home/sushaohua/workspace/ai_soc_project/soc-ap/contracts/twin/telemetry_types.h#L64-L65) 同时定义了 `MINIMC_CMD_SYSTEM_CONTROL = 0x10U` 和 `MINIMC_CMD_SET_TEMP = 0x10U`（或在 MC/TH `minimc_proto.h` 中同时定义了 `MINIMC_CMD_TEMP_REPORT = 0x15U` 和 `MINIMC_CMD_FILAMENT_CONTROL = 0x15U`）时，检查器完全不会报错！
   - **盲区 2：未覆盖 `0x14`、`0x1D`、`0x20~0x23` 及两个 Bootloader 仓库**：
     `EXPECTED_OPCODES` 甚至漏掉了 `0x14 (TEMP_QUERY)`，且完全未包含 `0x1D (SYSTEM_CONTROL)` 与 `0x20~0x23 (OTA_START/DATA/FINISH/STATUS)`；`load_endpoint_headers()`（第 88~103 行）也未将 `boot/bootloadermc` 与 `boot/bootloaderth` 的协议头文件纳入扫描。
   - **盲区 3：不检查最大载荷 `MAX_PAYLOAD_SIZE` 与结构体字节尺寸（`static_assert`）**：
     脚本只用正则匹配 `#define MINIMC_CMD_*`，对 AP `MAX_PAYLOAD_SIZE = 1024` vs MCU `MINIMC_MAX_PAYLOAD_SIZE = 64` 的 16 倍容量断层完全无感知。
3. **后续实现阶段的检查器改造要求（纳入完整方案，当前阶段保持只读不改）**：
   - 待用户确认统一协议契约后，在后续任务中升级 `check_opcode_alignment.py`：
     1. 补齐完整命令集（含 `0x14 TEMP_QUERY`、`0x1D SYSTEM_CONTROL`、`0x20 OTA_START`、`0x21 OTA_DATA`、`0x22 OTA_FINISH`、`0x23 OTA_STATUS`）；
     2. 增加**反向值唯一性断言**：扫描每个头文件内所有 `MINIMC_CMD_*` 宏，除白名单显式登记的合法同义别名（如 `MINIMC_CMD_TEMP_REPORT` / `MINIMC_CMD_TEMP_REPORT_V2`、`MINIMC_CMD_MOTION_STOP` / `MINIMC_CMD_EMERGENCY_STOP`、`MINIMC_CMD_SLOT_SELECT` / `MINIMC_CMD_FILAMENT_CONTROL`）外，**严禁两个不同业务语义的宏共享同一 `0xXX` 数值**；
     3. 将扫描范围从 3 个端点扩展至 **5 个端点**（`soc-ap`、`mcu-p3 MC`、`mcu-p3 TH`、`boot/bootloadermc`、`boot/bootloaderth`），并校验 `MINIMC_OTA_MAX_PAYLOAD_SIZE (520U)` 及关键载荷结构体 `sizeof` 对齐。

---

## 3. 帧长限制与缓冲区核查（`64B` 载荷上限 vs `OTA_DATA 0x21` 跨层扩容方案）

### 3.1 现有四层代码中的帧长、DMA 与 Ring Buffer 瓶颈精确定位

| 所在层级 / 仓库 | 关键源码位置与行号 | 当前宏 / 缓冲区定义 | 承载 `OTA_START (0x20)` 与 `OTA_DATA (0x21)` 的阻塞点分析 |
| :--- | :--- | :--- | :--- |
| **AP 协议编解码层**<br>(`soc-ap`) | [codec.h](file:///home/sushaohua/workspace/ai_soc_project/soc-ap/core/forward/minimc/codec.h#L21-L22)<br>[parser.h](file:///home/sushaohua/workspace/ai_soc_project/soc-ap/core/forward/minimc/parser.h#L27) | `MAX_PAYLOAD_SIZE = 1024`<br>`MAX_FRAME_SIZE = 1038` | 编解码器与流式解析器 `rx_buffer[1038]` 已原生支持最高 `1024B` 载荷，但 [forward_service.cpp](file:///home/sushaohua/workspace/ai_soc_project/soc-ap/services/forward/forward_service.cpp#L123) 局部栈缓冲 `tx_buf[64]` 与 [forward_protocol.h](file:///home/sushaohua/workspace/ai_soc_project/soc-ap/services/forward/forward_protocol.h#L265) `fwd_ctrl_rx_t.payload[64]` 仅按短指令分配，OTA 发送/接收需使用 `>= 534B` 帧缓冲。 |
| **MC App 协议解析与 AP 串口接收环**<br>(`mcu-p3`) | [minimc_proto.h](file:///home/sushaohua/workspace/ai_soc_project/mcu-p3/motion-controller-mcu/project/inc/minimc_proto.h#L236-L237)<br>[minimc_proto.c](file:///home/sushaohua/workspace/ai_soc_project/mcu-p3/motion-controller-mcu/project/src/minimc_proto.c#L96-L145) | `MINIMC_MAX_PAYLOAD_SIZE = 64U`<br>`MINIMC_MAX_FRAME_SIZE = 78U`<br>`AP_RING_CAPACITY = 256U`<br>`s_tx_buf[78]` | **阻断**：即使最小 `64B` 固件分块加上 8B `OTA_DATA` 帧内头也需 `72B` 载荷（`86B` 整帧），直接触发 `parser_step()` 超长丢弃；且 `AP_RING_CAPACITY = 256U` 无法缓存在主循环 1~2ms 抖动期间到达的 `>256B` 帧。 |
| **MC App 板间串口 (`USART6`) DMA 与接收抽取**<br>(`mcu-p3`) | [wk_dma.h](file:///home/sushaohua/workspace/ai_soc_project/mcu-p3/motion-controller-mcu/project/inc/wk_dma.h#L45-L46)<br>[wk_usart.c](file:///home/sushaohua/workspace/ai_soc_project/mcu-p3/motion-controller-mcu/project/src/wk_usart.c#L354)<br>[minimc_proto.c](file:///home/sushaohua/workspace/ai_soc_project/mcu-p3/motion-controller-mcu/project/src/minimc_proto.c#L2203) | `FORWARD_UART_TX_BUF_SIZE = 256`<br>`FORWARD_UART_RX_BUF_SIZE = 256`<br>`uint8_t th_buf[64]` (`drain_th_rx`)<br>`budget = 64U` (`drain_ap_rx`) | **阻断**：`forward_uart_send_raw()` 拒绝 `len > FORWARD_UART_TX_BUF_SIZE (256)` 的帧；`drain_th_rx()` 局部缓冲 `th_buf[64]` 会将超过 64B 的 TH 应答截断（且 `forward_uart_proto_rx_read()` 一次调用就会清零 `forward_uart_rx_complete`，导致 64B 之后的尾字节永久丢失！）。 |
| **TH App 协议解析层**<br>(`mcu-p3`) | [minimc_proto.h](file:///home/sushaohua/workspace/ai_soc_project/mcu-p3/color-engine-mcu/io_toggle/inc/minimc_proto.h#L58-L59)<br>[minimc_proto.c](file:///home/sushaohua/workspace/ai_soc_project/mcu-p3/color-engine-mcu/io_toggle/src/app/minimc_proto.c#L44) | `MINIMC_MAX_PAYLOAD_SIZE = 64U`<br>`MINIMC_MAX_FRAME_SIZE = 78U` | TH App 仅需在正常运行态接收 `0x01`（0B 载荷）、`0x03`（4B 载荷）与 `0x1D CMD_SYSTEM_CONTROL`（进入 Bootloader，4B 载荷），真正接收 `0x20/0x21/0x22/0x23` 大帧的是 **TH Bootloader**；因此 TH App 保持 `64B` 载荷上限即可，无需浪费业务态 SRAM。 |
| **TH Bootloader (`AT32F423`, 16KB Flash / 48KB SRAM)**<br>(`boot/bootloaderth`) | [inc/iap.h](file:///home/sushaohua/workspace/ai_soc_project/boot/bootloaderth/inc/iap.h#L45-L46)<br>[src/iap.c](file:///home/sushaohua/workspace/ai_soc_project/boot/bootloaderth/src/iap.c#L59-L80) | `CHUNK_MAX_SIZE = 512U`<br>`s_chunk0_buf[512]`<br>`s_rx_ctx.payload[520]` | **关键发现**：`bootloaderth` 现有静态 `.bss` 缓冲区**已经预留了 `512B` 分块缓存 `s_chunk0_buf[512]` 与 `520B` 载荷接收缓冲 `s_rx_ctx.payload[520]`**（恰好等于 `8B OTA_DATA 头 + 512B 净固件分块 = 520B`）！ |
| **MC Bootloader (`AT32F435`, 32KB Boot Flash / 384KB SRAM)**<br>(`boot/bootloadermc`) | [src/usbh_user.c](file:///home/sushaohua/workspace/ai_soc_project/boot/bootloadermc/bootloader/src/usbh_user.c#L26) | `read_buffer[4096]` (U 盘读取缓冲)<br>尚无 `USART2` 解析器 | `AT32F435` 拥有充裕的 `384KB` SRAM 与 `32KB` Bootloader Flash（当前 U 盘 Boot 仅占约 `18KB`），新增 `USART2` (`PA2/PA3`) MiniMCProto v2.0 接收缓冲完全无资源压力。 |

### 3.2 统一分块粒度与四层缓冲区协同设计方案

| 参数宏 / 缓冲区名称 | 统一设定值 | 字节数计算依据与安全裕度说明 | 涉及修改的仓库与源码位置 |
| :--- | :--- | :--- | :--- |
| `MINIMC_OTA_DATA_HDR_SIZE` | `8U` | `offset(4B) + chunk_bytes(2B) + chunk_crc16(2B)` | `soc-ap`, `mcu-p3`, `bootloadermc`, `bootloaderth` |
| `MINIMC_OTA_DEFAULT_CHUNK_SIZE` | `256U` | 默认推荐单帧净固件数据块大小（256B，整帧 `12 + 8 + 256 + 2 = 278B`） | `soc-ap` (`ForwardService`), `mcu-p3` (`th_upgrade_mgr`) |
| `MINIMC_OTA_MAX_CHUNK_SIZE` | `512U` | 协议单帧允许的最大净固件数据块大小（对齐 TH Boot `s_chunk0_buf[512]`） | `soc-ap`, `mcu-p3`, `bootloadermc`, `bootloaderth` |
| `MINIMC_MAX_PAYLOAD_SIZE` (MC App / MC Boot / TH Boot) | `520U` | `8B (OTA_DATA 头) + 512B (最大净数据块) = 520B`；同时兼容 `144B` 的 `OTA_START` 载荷 | `mcu-p3/motion-controller-mcu/project/inc/minimc_proto.h`<br>`boot/bootloadermc` & `boot/bootloaderth` |
| `MINIMC_MAX_FRAME_SIZE` (MC App / MC Boot / TH Boot) | `534U` | `12B (帧头) + 520B (最大载荷) + 2B (CRC16) = 534B` | 同上 |
| `AP_RING_CAPACITY` (MC App `USART2` RX Ring) | `1024U` | 从 `256U` 扩容至 `1024U`（可容纳近 2 个完整最大 OTA 帧，消除主循环轮询丢字节） | `mcu-p3/motion-controller-mcu/project/src/minimc_proto.c#L96` |
| `FORWARD_UART_TX_BUF_SIZE` / `RX_BUF_SIZE` (MC App `USART6` DMA) | `600U` | 从 `256U` 扩容至 `600U`（大于 `534B` 最大帧长，确保整帧单次 DMA 发送与 IDLE 判帧接收） | `mcu-p3/motion-controller-mcu/project/inc/wk_dma.h#L45-L46` |
| `drain_ap_rx()` 轮询预算与 `drain_th_rx()` 缓冲 | `budget = 600U`<br>`th_buf[128]` (或直接按帧读取) | 修复 `drain_th_rx()` 中 `th_buf[64]` 截断缺陷；升级路由态下单次 `minimc_proto_poll()` 可完整抽干一整帧 `534B` 数据 | `mcu-p3/motion-controller-mcu/project/src/minimc_proto.c#L2185-L2204` |

---

## 4. 统一 MiniMCProto v2.0 升级字节级协议契约草案（严格对齐主规范 `0x00/0x06/0x20~0x23`）

### 4.1 帧格式与路由寻址不变量

- **MC 升级寻址**：`SRC=0x01 (AP)` $\leftrightarrow$ `DST=0x02 (MC)`，物理链路为 `AP (/dev/ttyUSB0, 921600 8N1) <-> MC USART2 (PA2/PA3)`，由 **MC Bootloader** 直接终结并执行 Flash 擦写。
- **TH 升级寻址**：`SRC=0x01 (AP)` $\leftrightarrow$ `DST=0x03 (SCM-TH)`，物理链路为 `AP <-> MC USART2` 经 **MC App 存储转发路由（Store-and-Forward Router）** $\leftrightarrow$ `MC USART6 (PA4/PA5, 921600 8N1) <-> TH USART1 (PA9/PA10)`，由 **TH Bootloader** 终结并执行 Flash 擦写。
  - MC App 转发规则：收到 `DST=0x03` 请求帧并完成整帧 CRC16 校验后，检查 `hop_limit > 1`，递减 `hop_limit = frame[6] - 1`，置位 `route_ctrl |= 0x04 (IS_ROUTED)`，重新计算尾部 CRC16 并通过独立发送缓冲提交 `USART6` DMA 整帧发出；收到 TH Bootloader 返回的 `SRC=0x03, DST=0x01` 响应帧后，同样完成整帧 CRC16 校验、递减 `hop_limit`、置位 `IS_ROUTED`、重算 CRC16 后通过 `USART2` 回传 AP。**MC App 不解析或改写 `0x20~0x23` 业务载荷，MC Bootloader 严禁包含任何 `DST=0x03` 转发逻辑。**

### 4.2 节点运行态身份识别（`0x01 GET_VERSION` / `0x02 VERSION_REPORT`）与 Boot 信标

统一复用 `0x01 GET_VERSION`（0B 载荷）与 `0x02 VERSION_REPORT`（16B 载荷，`minimc_payload_version_report`），并对 `capability_flags` (`Offset 12..15`, `uint32_t` LE) 的高位标志位做出严格定义：

| 字节偏移 (Payload) | 字段名 | 类型 | App 业务态 (`APP_MODE`) 取值约定 | Bootloader 引导态 (`BOOT_MODE`) 取值约定 |
| :--- | :--- | :--- | :--- | :--- |
| `+0` | `proto_ver_major` | `uint8_t` | `2` (v2.0) | `2` (v2.0) |
| `+1` | `proto_ver_minor` | `uint8_t` | `0` (v2.0) | `0` (v2.0) |
| `+2` | `firmware_major` | `uint8_t` | App 主版本号 (`FW_VERSION_MAJOR`) | Boot 主版本号 (`BOOT_VERSION_MAJOR`, 如 `2`) |
| `+3` | `firmware_minor` | `uint8_t` | App 次版本号 (`FW_VERSION_MINOR`) | Boot 次版本号 (`BOOT_VERSION_MINOR`, 如 `0`) |
| `+4..7` | `boot_id` | `uint32_t` | 每次 App 冷启动或复位后单调变化或基于硬件计数生成的动态启动代次标识（Session Epoch） | Boot 会话标识（MC Boot: `0x4D43424C` `"MCBL"` ^ 复位计数；TH Boot: `0x5448424C` `"THBL"` ^ 复位计数） |
| `+8..11` | `git_commit_short` | `uint32_t` | App 编译注入的 32-bit Git Commit 短哈希 | Boot 编译注入的 32-bit Git Commit 短哈希 |
| `+12..15` | `capability_flags` | `uint32_t` | **`Bit 31 = 0` (`0x00000000`)**：标识当前运行于 **App 业务态**；低位保持既有能力位（MC=`0x03`, TH=`0x07`） | **`Bit 31 = 1` (`0x80000000`)**：标识当前运行于 **Bootloader 升级态**；<br>`Bit 30 = 1` (`0x40000000`)：支持 `128B ATSG Trailer` 准入校验；<br>`Bit 29 = 1` (`0x20000000`)：TH 首块 512B SRAM 延迟提交与 `0x0803F800` Anchor 保护；<br>`Bits 16..23`：最大支持分块字节数除以 64（`512B -> 8`）；<br>`Bits 0..15`：硬件 `board_id` 低 16 位（MC=`0x0435`, TH=`0x0423`） |

### 4.3 系统控制进入 Bootloader（`0x1D CMD_SYSTEM_CONTROL`）与升级命令（`0x20~0x23`）字节布局

#### (1) 系统控制进入升级引导态（`0x1D CMD_SYSTEM_CONTROL`，按 §2.2.1 方案 D1-A 定型）
```c
#pragma pack(push, 1)
/**
 * @brief 系统控制请求载荷 (CMD_SYSTEM_CONTROL, 固定 4 字节自然对齐，小端序)
 * @note  在方案 D1-A 下命令码为 0x1D (避免与 0x10 SET_TEMP 冲突)；若采用 D1-B 则为 0x10。
 */
typedef struct {
    uint8_t  action;           /* +0: 0=Noop, 1=Reboot, 2=JumpToBootloader */
    uint8_t  target_component; /* +1: 1=Main App (预检进入升级维护态), 0=通用复位 */
    uint16_t delay_ms;         /* +2..3: 回复 0x00 CMD_ACK 后的延迟复位毫秒数 (推荐 50~100ms) */
} minimc_payload_sys_ctrl_t;
#pragma pack(pop)
```
- **受控跳入 Bootloader 闭环时序**：
  1. AP 在确认整机空闲安全（作业 `IDLE`、热床/喷头 PWM 为 `0%`、步进电机静止、温度采样有效且新鲜）后，向目标节点（`DST=0x02` 或 `DST=0x03`）发送 `CMD_SYSTEM_CONTROL (action=2 JumpToBootloader, target_component=1, delay_ms=50)`；
  2. 目标节点 App 校验本地安全状态（无活跃打印、加热器已关闭、步进电机已去能）：
     - 若不安全：立即返回 `0x06 CMD_NACK`（`err_code = 0x05 MINIMC_ERR_DEVICE_BUSY` 或 `0x06 MINIMC_ERR_COMMAND_REJECTED`），**严禁复位**；
     - 若安全：先向 AP 回复标准 **`0x00 CMD_ACK`（4B 载荷）**，等待硬件串口 `USART_TDC_FLAG` 发送移位寄存器彻底排空，写入跨软复位驻留魔数（MC 写入 `0x55504732` `"UPG2"`；TH 向 `0x20008000` 写入 `0x55504744` `"UPGD"`），延迟 `delay_ms` 后执行 `NVIC_SystemReset()` 进入 Bootloader！
  3. AP 收到 `0x00 CMD_ACK` 后，等待 `100ms ~ 500ms` 并发送 `0x01 GET_VERSION`，验证收到 `0x02 VERSION_REPORT` 且 `(capability_flags & 0x80000000U) != 0U` (`BOOT_MODE`)，确认目标节点已成功驻留 Bootloader！

#### (2) 固件升级握手与擦除前 Trailer 准入（`0x20 CMD_OTA_START`，144B 载荷）
```c
#pragma pack(push, 1)
/**
 * @brief 128 字节统一固件尾部元数据描述符 (与 bootloadermc / bootloaderth pack_firmware.py 小端布局 <IIIII32s32s32s8s 严格一致)
 * @note  注意：pack_firmware.py 按 uint32_t LE 写入 magic = 0x41545347，物理字节序为 0x47('G'), 0x53('S'), 0x54('T'), 0x41('A')！
 */
typedef struct {
    uint32_t magic;              /* +0..3:   固定为 0x41545347U (LE 字节序: 47 53 54 41) */
    uint32_t struct_version;     /* +4..7:   结构体版本号 (固定为 0x00000001U) */
    uint32_t board_id;           /* +8..11:  目标板卡硬件 ID (MC=0x41543433U, TH=0x00000423U) */
    uint32_t version_code;       /* +12..15: 语义化版本号编码 (Major<<16 | Minor<<8 | Patch) */
    uint32_t payload_size;       /* +16..19: 净 App 固件字节数 (TH <= 241664B [236KB], MC <= 917504B) */
    uint8_t  payload_sha256[32]; /* +20..51: 净 App 固件 SHA-256 摘要 (由 AP 与打包器核验，MCU Boot 记录入 Anchor) */
    uint8_t  sig_r[32];          /* +52..83: 预留签名字段 R (首发全 0，不宣称密码学验签) */
    uint8_t  sig_s[32];          /* +84..115:预留签名字段 S (首发全 0) */
    uint8_t  reserved[8];        /* +116..123: 预留全 0 */
    uint32_t header_crc32;       /* +124..127: 前 124 字节的标准 IEEE 802.3 CRC32 */
} minimc_fw_trailer_t;

/**
 * @brief 0x20 CMD_OTA_START 请求载荷结构体 (16B 主规范标准头 + 128B ATSG Trailer = 144 字节)
 */
typedef struct {
    uint8_t             target_device;    /* +0: 目标节点 ID (0x02=MC, 0x03=TH) */
    uint8_t             target_component; /* +1: 目标组件 (0x01=Main App; 0x02=Bootloader 首发严禁并拒绝) */
    uint8_t             force_flag;       /* +2: 0=常规校验, 1=允许同版本重刷 (绝不允许跳过错板/超限/CRC 门禁) */
    uint8_t             reserved;         /* +3: 置 0 */
    uint32_t            fw_size_bytes;    /* +4..7: 净 App 固件字节数 (须严格等于 trailer.payload_size) */
    uint32_t            fw_crc32;         /* +8..11: 净 App 固件全量 IEEE 802.3 CRC32 */
    uint32_t            new_version_raw;  /* +12..15: 目标新版本号 (须等于 trailer.version_code) */
    minimc_fw_trailer_t trailer;          /* +16..143: 完整 128 字节固件尾部描述符 */
} minimc_payload_ota_start_t;
#pragma pack(pop)
```
> **重要字节布局修正说明**：经核对 [boot/bootloadermc/bootloader/inc/firmware_trailer.h](file:///home/sushaohua/workspace/ai_soc_project/boot/bootloadermc/bootloader/inc/firmware_trailer.h#L17-L29) 与 [boot/bootloaderth/tools/pack_firmware.py](file:///home/sushaohua/workspace/ai_soc_project/boot/bootloaderth/tools/pack_firmware.py#L46-L58)，两仓存量 `fw_trailer_t` 的真实二进制布局均为 `<IIIII32s32s32s8s` + `uint32_t header_crc32`（即 `magic[4B] + struct_version[4B] + board_id[4B] + version_code[4B] + payload_size[4B] + payload_sha256[32B] + sig_r[32B] + sig_s[32B] + reserved[8B] + header_crc32[4B] = 128B`），且 `magic = 0x41545347U` 按小端编码在字节流前 4 字节为 `47 53 54 41`！上方 `minimc_fw_trailer_t` 已 100% 精确对齐两仓真实代码定义（修正了 `r1` 中误引历史文档的字符串布局）。

#### (3) 固件数据分块传输（`0x21 CMD_OTA_DATA`）、结束终验（`0x22 CMD_OTA_FINISH`）与状态查询（`0x23 CMD_OTA_STATUS`）
100% 采用主规范 `Rev 2.0.3` §5.2.5(2)~(4) 的标准结构体定义：
- **`0x21 CMD_OTA_DATA`**：`offset (4B)` + `chunk_bytes (2B, 常规 256B/512B，末块允许 <64B 并由 Boot 按 4B 边界安全补 `0xFF` 写 Flash，但 CRC 计算严格按有效净荷长度 `fw_size_bytes` 对账)` + `chunk_crc16 (2B, CRC-16/CCITT-FALSE)` + `firmware_bytes[chunk_bytes]`；应答为 `0x00 CMD_ACK (4B)`。
- **`0x22 CMD_OTA_FINISH`**：`fw_crc32 (4B)` + `action_after_verify (1B: 1=立即重启加载新 App, 0=保持在 Boot)` + `reserved[3]`；应答为 `0x00 CMD_ACK (4B)`。
- **`0x23 CMD_OTA_STATUS`**：AP 发送 `0B` 查询请求（或 `4B` 中止控制），Boot 返回 **8 字节 `minimc_payload_ota_status`**：
  - `ota_state (1B)`：`0=IDLE`, `1=ERASED_READY`, `2=RECEIVING_CHUNK0_CACHED`（仅首块在 SRAM，尚未写 Flash）, `3=RECEIVING_FLASH_WRITING`, `4=VERIFYING`, `5=VERIFIED_COMMITTED`（Chunk 0 与 Anchor 均已落盘）, `6=ERROR_ABORTED`；
  - `error_code (1B)`：`0=OK`，其余对应标准 `MINIMC_ERR_OTA_*`（`0x10~0x14`）；
  - `reserved (2B)`：可回显已缓存但未落盘字节数（如 `512U`）；
  - `bytes_written (4B)`：**严格定义为已物理写入 Flash 并完成读回比对的持久字节数**（当仅收到首块 512B 缓存在 `s_chunk0_buf` 时，`bytes_written == 0`！直到后续块写入 Flash 才累加后续块字节，并在 `OTA_FINISH` 将首块 512B 真正写入 `0x08004000` 后才加上这 `512B`！）。

---

## 5. 双 Boot / 双 App 职责边界、Flash/RAM 预算核算与历史设计演进裁决

### 5.1 双 Bootloader 与双 App 改造边界矩阵

| 角色 / 仓库 / 分支 | 物理目标与资源约束 | 核心改造职责与代码落点 | 明确禁止事项（红线） |
| :--- | :--- | :--- | :--- |
| **`ENG_BOOT_MC`**<br>[boot/bootloadermc](file:///home/sushaohua/workspace/ai_soc_project/boot/bootloadermc)<br>(`soc_debug`) | `AT32F435` Bootloader<br>Flash: `0x08000000..0x08007FFF` (`32KB`)<br>App: `0x08020000` (或 `0x08008000` 按本仓 `usbh_user.c` `APPLICATION_ADDRESS` 统一) | 1. **完整保留既有 U 盘升级入口**（[usbh_user.c](file:///home/sushaohua/workspace/ai_soc_project/boot/bootloadermc/bootloader/src/usbh_user.c#L171-L263) `0:/fw_mc.bin`、`128B ATSG Trailer` 校验、Flash 擦写、改名 `.cur` 与 `0x080FF800` `UPGD` 防重刷标记），补齐 `verify_firmware_trailer()` 对 `header_crc32` 的实际核验；<br>2. **新增 `USART2` (`PA2/PA3`, `921600 8N1`) MiniMCProto v2.0 本机升级通道**：当检测到 App 软复位魔数 `0x55504732` (`"UPG2"`)、App 区无效或上电探测窗口握手请求时，驻留响应 `DST=0x02` 的 `0x01/0x02/0x03/0x04/0x1D/0x20/0x21/0x22/0x23`，完成 MC App 串口升级。 | **严禁在 `bootloadermc` 中引入 `USART6` 驱动或任何 `DST=0x03` TH 路由转发逻辑**；严禁破坏 U 盘离线恢复能力。 |
| **`ENG_BOOT_TH`**<br>[boot/bootloaderth](file:///home/sushaohua/workspace/ai_soc_project/boot/bootloaderth)<br>(`soc_debug`) | `AT32F423` / `AT32A423` Bootloader<br>Flash: `0x08000000..0x08003FFF` (**严守 `16KB` 硬上限**)<br>App: `0x08004000..0x0803EFFF` (**净载荷上限 `236KB` = `241,664B`**)<br>Anchor: `0x0803F800` | 1. **移除私有 `0x5A 0xA5` 协议栈**（[src/iap.c](file:///home/sushaohua/workspace/ai_soc_project/boot/bootloaderth/src/iap.c)），替换为 `USART1` (`PA9/PA10`, `921600 8N1`) **MiniMCProto v2.0 升级最小子集**（仅处理 `DST=0x03` 的 `0x01/0x02/0x03/0x04/0x1D/0x20/0x21/0x22/0x23` 及 `0x00/0x06` 应答）；<br>2. **100% 保留并加固断电防变砖机制**：首块 `512B` SRAM 延迟缓存（`s_chunk0_buf[512]`）、`0x0803F800`（Sector 127）`app_anchor_meta_t`（`0xA55A424C` + `128B ATSG Trailer` + 双 CRC32）、`0x20008000` (`0x55504744`) 软复位穿透魔数；修复 `flash_verify_app_integrity()` 在“无 Anchor 但首块向量存在”时的历史回退漏洞（强制校验 Anchor 或完整镜像有效性）；<br>3. **修正打包脚本上限**：将 [tools/pack_firmware.py](file:///home/sushaohua/workspace/ai_soc_project/boot/bootloaderth/tools/pack_firmware.py#L18) 中 `MAX_PAYLOAD_SIZE = 240 * 1024` 修正为 `236 * 1024` (`241,664B`)。 | **编译产出的全段 Flash 装载总占用（`.isr_vector + .text + .rodata + .data LMA`）严禁超过 `16,384` 字节**。 |
| **`ENG-MC`**<br>[mcu-p3/motion-controller-mcu](file:///home/sushaohua/workspace/ai_soc_project/mcu-p3/motion-controller-mcu)<br>(`feat/soc-debug`) | `AT32F435` MC App<br>Flash: `0x08020000`<br>SRAM: `384KB` | 1. **扩容协议与板间 DMA 缓冲区**：`MINIMC_MAX_PAYLOAD_SIZE = 520U`、`MINIMC_MAX_FRAME_SIZE = 534U`、`AP_RING_CAPACITY = 1024U`、`FORWARD_UART_TX/RX_BUF_SIZE = 600U`，修复 `drain_th_rx()` 64B 截断；<br>2. **升级维护态安全准入与锁止**：收到 `DST=0x02` 的 `0x1D CMD_SYSTEM_CONTROL (JumpToBootloader)` 时校验空闲安全态、回发 `0x00 CMD_ACK`、置位 `0x55504732` 并软复位；<br>3. **`DST=0x03` 升级帧存储转发路由**：在 TH 升级期间锁定 `USART6` 所有权（`FORWARD_UART_MODE_OTA_ROUTE`，静默暂停本地 G-code 与温度轮询），对 `DST=0x03` 的 `0x01/0x03/0x1D/0x20/0x21/0x22/0x23` 请求与 TH 响应执行完整 CRC 校验、TTL 递减与整帧独立缓冲 DMA 转发；<br>4. **MC App U 盘升级 TH (`th_upgrade_mgr.c`) 协议同构迁移**：将 [th_upgrade_mgr.c](file:///home/sushaohua/workspace/ai_soc_project/mcu-p3/motion-controller-mcu/project/marlin/marlin_module/th_upgrade_mgr.c) 从旧 `5A A5` 帧切换为发送相同的 MiniMCProto v2.0 `0x20~0x23` 帧，并将 `TH_FLASH_MAX_APP_SIZE` 从 `240KB` 修正为 `236KB`。 | 严禁在升级维护态下继续向 TH 混发 `0x1C` G-code 或 `0x14` 温度查询帧；严禁在 MC App 中保留 `5A A5` 死代码。 |
| **`ENG-TH`**<br>[mcu-p3/color-engine-mcu](file:///home/sushaohua/workspace/ai_soc_project/mcu-p3/color-engine-mcu)<br>(`feat/soc-debug`) | `AT32F423` TH App<br>Flash: `0x08004000..0x0803EFFF` (`236KB`)<br>SRAM: `48KB` | 1. **MiniMCProto v2.0 进入 Bootloader 支持**：在 [minimc_proto.c](file:///home/sushaohua/workspace/ai_soc_project/mcu-p3/color-engine-mcu/io_toggle/src/app/minimc_proto.c) 中支持收到 `0x1D CMD_SYSTEM_CONTROL (action=2)` 时，执行热端 PWM 归零、步进电机去能，先回发 `0x00 CMD_ACK`，等待 `USART1` 发送完成，再写 `0x20008000 = 0x55504744` 并触发 `NVIC_SystemReset()`；<br>2. **链接脚本容量对齐**：将 [AT32F423xC_FLASH.ld](file:///home/sushaohua/workspace/ai_soc_project/mcu-p3/color-engine-mcu/io_toggle/libraries/cmsis/cm4/device_support/startup/gcc/linker/AT32F423xC_FLASH.ld#L34) 中 `FLASH LENGTH = 240K` 修正为 **`LENGTH = 236K`**；<br>3. **动态 `boot_id` 生成**：替换常量 `TH_BOOT_ID = 0x8877AA55U`，基于启动计数或硬件熵生成每次复位变化的 `boot_id`。 | 严禁在未回发 MiniMCProto ACK 前直接裸复位导致 AP 超时误判。 |
| **`ENG-FWD` / `ENG-STATE` / `INTEGRATOR`**<br>[soc-ap](file:///home/sushaohua/workspace/ai_soc_project/soc-ap)<br>(`main`) | VMware Linux AP<br>(`forward_service`, `device_manager`, `ui_gateway`) | 1. **`ForwardService` 升级会话引擎**：实现 VMware 指定目录升级包原子就绪检测与哈希封存、`128B ATSG Trailer` 离线预检、串口排他锁获取（暂停周期温度轮询）、`0x1D -> 0x01/0x02 -> 0x20 -> 0x21 -> 0x23 -> 0x22` 停等重传状态机、以及复位后 `0x01 -> 0x02` 新 App 身份（动态 `boot_id` 变化 + `git_commit` 匹配 + `APP_MODE`）与 `0x14 -> 0x15` 业务恢复核验；<br>2. **`DeviceManager` & `UI Gateway`**：实现 `UPGRADING_MAINTENANCE` 状态互斥锁（核验强电加热 0%、运动静止、温度有效新鲜；升级期间拒绝普通控制并返回 HTTP 503/409），区分展示“缓存接收 / Flash 落盘（`bytes_written`） / 整包终验 / 新 App 在线确认”四阶段真实状态。 | 严禁使用开环定时器伪造升级进度条；严禁在收到 `0x22 FINISH ACK` 时提前宣布升级成功。 |

### 5.2 历史 `240KB` 遗留点全量修正清单（统一收敛至 `236KB = 241,664B`）

| 序号 | 仓库 | 文件路径与行号 | 当前遗留定义 | 统一修正目标 |
| :--- | :--- | :--- | :--- | :--- |
| 1 | `boot/bootloaderth` | [tools/pack_firmware.py#L18](file:///home/sushaohua/workspace/ai_soc_project/boot/bootloaderth/tools/pack_firmware.py#L18) | `MAX_PAYLOAD_SIZE = 240 * 1024` | `MAX_PAYLOAD_SIZE = 236 * 1024` (`241,664` 字节，与 [inc/flash.h#L30](file:///home/sushaohua/workspace/ai_soc_project/boot/bootloaderth/inc/flash.h#L30) `APP_MAX_SIZE` 严格一致) |
| 2 | `mcu-p3` | [AT32F423xC_FLASH.ld#L34](file:///home/sushaohua/workspace/ai_soc_project/mcu-p3/color-engine-mcu/io_toggle/libraries/cmsis/cm4/device_support/startup/gcc/linker/AT32F423xC_FLASH.ld#L34) | `FLASH (rx) : ORIGIN = 0x08004000, LENGTH = 240K` | `FLASH (rx) : ORIGIN = 0x08004000, LENGTH = 236K`（保护 `0x0803F000..0x0803FFFF` 的 Sector 126/127 不被 App 代码覆盖） |
| 3 | `mcu-p3` | [th_upgrade_mgr.h#L21](file:///home/sushaohua/workspace/ai_soc_project/mcu-p3/motion-controller-mcu/project/inc/th_upgrade_mgr.h#L21) | `#define TH_FLASH_MAX_APP_SIZE (240U * 1024U)` | `#define TH_FLASH_MAX_APP_SIZE (236U * 1024U)` |
| 4 | `boot/bootloadermc` | [app_test/inc/th_upgrade_mgr.h#L21](file:///home/sushaohua/workspace/ai_soc_project/boot/bootloadermc/app_test/inc/th_upgrade_mgr.h#L21) | `#define TH_FLASH_MAX_APP_SIZE (240U * 1024U)` | `#define TH_FLASH_MAX_APP_SIZE (236U * 1024U)` |

---

## 6. 《升级操作与 HIL 部署说明书》架构衔接与常规部署禁用 `probe-rs` 硬门禁

### 6.1 《升级操作与 HIL 部署说明书》正式交付责任链

[project-control/docs/guides/minimc_v2_mcu_upgrade_and_hil_deployment_manual_20261105.md](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/guides/minimc_v2_mcu_upgrade_and_hil_deployment_manual_20261105.md)（`revision: 1`, `sha256: 87b0b859e3e7e4cf7e8733ac88d90d1e0fd94f3b3e2117abfea9af3b14d4e6a9`）作为与主架构方案并列的正式受控交付物，其全生命周期责任绑定如下：
1. **规划阶段（当前）**：保持 `status: draft-procedure-not-executable-until-implementation-validated`，绝不编造尚未实现的 CLI 参数或成功日志；在主架构方案中明确其 7 类必填操作信息（准确入口、VMware 文件投放目录与原子就绪规则、发布包 `ATSG` 身份清单、已部署 Boot 能力核实依据、921600/115200 端口角色映射、受控恢复步骤、证据与交接单目录）的工程提供方。
2. **实现与集成阶段**：由 **`INTEGRATOR` 主责**维护，协同 `ENG-FWD`、`ENG-MC`、`ENG-TH`、`ENG_BOOT_MC`、`ENG_BOOT_TH` 填入经实测验证的可执行命令、工作目录、配置路径、超时与退出码。
3. **非实现者独立操作验证**：功能实现后，必须安排**非实现者**严格按照说明书步骤在真实 VMware + 双 MCU 台架上完成一次受控升级与台架交接验证，并由独立 Codex **`QA`** 对照原始双向帧 Hex、Boot/App Debug 与新 App 动态 `boot_id` 证据核对可执行性后，方可将说明书状态切换为正式可执行发布版。

### 6.2 常规测试与 HIL 台架部署禁用 `probe-rs` 架构门禁

1. **常规 MC/TH App 部署唯一通道**：
   后续所有功能测试、回归测试及 HIL 台架搭建中的常规 MC/TH App 固件部署，**100% 强制通过本方案实现的 VMware 文件 $\to$ MiniMCProto v2.0 升级流程（或 MC 原生 U 盘入口独立回归）执行，严禁使用 `probe-rs`、`st-flash`、`openocd` 或任何其他 SWD/JTAG 探针写入工具替代**！
2. **存量脚本与任务清理要求**：
   在完整方案确认后的工程任务拆分中，必须显式包含对 `test_harness` 与部署脚本中旧 `probe-rs download` App 烧录步骤的替换任务；**严禁只修改操作文档而让测试脚本后台继续调用探针刷写 App**。当升级链路或前置新 Boot 尚未就绪时，依赖该版本部署的 HIL 测试步骤必须保持 ` pending / blocked` 待完成状态，绝不允许“先用探针刷进去跑通测试再把记录写成升级部署完成”。
3. **首次 Boot 迁移与特殊砖机救援的严格审批隔离**：
   - 本方案不开放运行期 Bootloader 自升级（`target_component == 0x02` 在协议层强制拒绝）；
   - 将支持 MiniMCProto v2.0 的新版 `bootloadermc` / `bootloaderth` 首次烧入物理板卡，或因极端硬件故障导致 Bootloader 自身损坏需执行探针救援写入时，**必须单独向用户提交申请并取得显式授权**，记录独立的迁移/救援审计台账，**绝不自动视为常规测试/HIL 部署的默认例外**（不涉及 Flash 写入的只读诊断观察按既有授权边界处理）。
