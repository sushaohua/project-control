---
title: MiniMCProto v2.0 双 MCU 统一升级专项只读规划委派与接单登记表
revision: 5
date: 2026-11-05
owner: COORD
coord_session: ff2fb105-fd84-4ecb-b1e6-8f8eb00badc6
requirement_id: REQ-20261105-003
demand_id: DEM-20261105-006
status: master-plan-ready-pending-user-confirmation
---

# MiniMCProto v2.0 双 MCU 统一升级专项只读规划委派与接单登记表

| 修订 | 日期 | 修订内容 |
| --- | --- | --- |
| 1 | 2026-11-05 | 初始收件 `20261105_minimc_v2_upgrade_coord_planning_prompt.md` (`revision: 1`)，关联 `U-D05`/`PM:FEAT-OTA-001` 与 `TWIN-26~28`，登记只读规划角色实际委派 |
| 2 | 2026-11-05 | 同步收件 `revision: 2` 与讨论稿 `revision: 2`：关联原需求 `REQ-20261105-003` (`revision: 3`) 更新范围（不重复派单），将《升级操作与 HIL 部署说明书》纳入正式交付，并登记“后续测试/HIL 常规 MC/TH App 部署统一走本升级流程、禁止用 probe-rs 或其他探针写入替代”硬约束 |
| 3 | 2026-11-05 | 同步收件 `revision: 3` 至 `REQ-20261105-003` (`revision: 4`)：增加“先解决协议契约冲突，再继续升级方案接口定型”前置条件 |
| 4 | 2026-11-05 | 登记 `ARCH` (`revision: 2`)、独立 Codex `QA` (`revision: 2`) 与 `eng-vertical` 工程多端合并输入 (`revision: 1`) 全部收件完成及准确 SHA-256；推进 `ARCH` 进入 Phase B 合稿生成完整主方案 `minimc_v2_unified_mcu_upgrade_architecture_20261105.md` |
| 5 | 2026-11-05 | `ARCH`（会话 `3a7ad206-fef7-4d28-b3c8-1ee5bce395a5` 接力 `ef428595-f4d6-46a7-9d12-07e1fd215641`）完成完整主方案 `project-control/docs/architecture/minimc_v2_unified_mcu_upgrade_architecture_20261105.md` (`revision: 1`, `sha256: 6c0e672c50bc526d8b4e662c2c354114ef5c8c0180d4a3dd5563908726584c7a`)；更新 `REQ-20261105-003.yaml` (`revision: 5`) 并提交用户一次性确认 |

## 1. 收件关联与查重结论

| 字段 | 登记值 | 说明 |
| --- | --- | --- |
| 原始收件路径 | `project-control/docs/work_intake/submissions/20261105_minimc_v2_upgrade_coord_planning_prompt.md` | `revision: 3`, `sha256: 4699feade73d9e621b5ead2bade96ba195c488446de6e215bbb9b5276dcfcc80`（关联 `revision: 1/2` 原需求更新范围，不重复派单） |
| 分类收件记录 | `project-control/docs/work_intake/requirements/REQ-20261105-003.yaml` | `revision: 5`, `sha256: 2acb7142415198ab042de85a4df7d117554a7c3b06f3ad34b30e5d754ee58d00`, `demand_id: DEM-20261105-006` |
| 关联产品决定与功能 | `U-D05` / `PM:FEAT-OTA-001` | 见 `project-control/docs/planning/product/first_release_scope_decision_20261029.md` (`revision: 7`)；原“避免修改 Bootloader、MC 探针透传、TH 5A A5 私有 IAP”路线因用户本轮明确统一为 **MiniMCProto v2.0** 而进入架构重规划 |
| 关联历史任务（查重） | `TWIN-26` (`Done/Blocked`)、`TWIN-27` (`Backlog/Blocked`)、`TWIN-28` (`Backlog/Blocked`) | 保持人为冻结状态与历史签署记录不变；本单处于只读规划阶段，**不自动解冻历史任务、不提前新建或改写实现任务卡** |
| 关联历史设计输入 | `project-control/docs/analysis/mcu_firmware_upgrade_design_20261031.md` (`sha256: c5a79270ec6017a071944bbf314ebb11e345ec61d62fee6f5563336110c7505c`) | 128B `ATSG` Trailer 布局与安全前置条件等可复用部分由完整方案盘点迁移；旧探针执行器与 TH `5A A5` 私有 IAP 不作为新方案最终通道 |
| 助理讨论稿输入 | `project-control/docs/planning/minimc_v2_unified_mcu_upgrade_proposal_20261105.md` | `revision: 2`, `sha256: 72c1a91a1487b7184ba371ea3ed653d038c741a7e8baf2eb98316e0d91e6dc2f`（仅作规划输入，非 ARCH 正式交付） |
| 升级操作与 HIL 部署说明书输入 | `project-control/docs/guides/minimc_v2_mcu_upgrade_and_hil_deployment_manual_20261105.md` | `revision: 1`, `sha256: 87b0b859e3e7e4cf7e8733ac88d90d1e0fd94f3b3e2117abfea9af3b14d4e6a9`（正式交付物草案；由 `INTEGRATOR` 主责、各端 Owner 核实、`QA` 核对可执行性，随功能实现后验证发布） |
| 权威协议规范 | `project-control/docs/specs/ap_mc_formal_protocol_v2_0_multidevice_routing_draft_20261015.md` | `SPEC-PROTO-20261015-153000`, `Rev 2.0.3`, `sha256: 9f8d4f9607cb3e76cc30b9ee2f971b23c3e0d936611188466a71f4aa15f3ce54` |
| 协议契约冲突裁定前置要求 | **先解决主规范 `Rev 2.0.3` 与现有实现的命令/载荷冲突，再定型升级接口** | 核对主规范 `0x10=SYSTEM_CONTROL`、`0x12=EMERGENCY_STOP` 与现有业务实现及 `check_opcode_alignment.py` 中 `0x10=SET_TEMP`、`0x12=MOTION_MOVE` 的语义冲突，以及 AP (`1024B`) 与 MCU (`64B`) 最大载荷差异；区分合法别名、功能子集与语义冲突，明确兼容及迁移影响；QA 补齐从统一契约独立推导的固定字节用例、冲突回归判据及 `check_opcode_alignment.py` 预期来源审计 |
| 常规测试/HIL 部署门禁 | **禁止使用 `probe-rs` 或其他探针写入工具替代常规 MC/TH App 部署** | 后续测试及搭建 HIL 台架时，常规 MC/TH App 部署必须走本 MiniMCProto v2.0 升级流程；升级未就绪时保持对应部署步骤待完成，不绕回旧刷写路径；首次 Boot 安装或特殊救援若确需探针写入，须单独提交用户决定 |

## 2. 目标仓库只读观察基线与规则入口

| 仓库 | 分支 | 观察 HEAD 提交 | 仓内规则入口 | 公共规则快照来源 (`SOURCE.json`) | 当前工作树备注 |
| --- | --- | --- | --- | --- | --- |
| `project-control` | `main` | `5686e1931123650bb2251045353c18c8baa00f65` | `AGENTS.md` + `.agents/rules/` | Canonical (`project-control`) | 含本轮收件、规划产物与 `TWIN-61` 注释修改 |
| `soc-ap` | `main` | `19534a9a4cb393176882fbad046129d55bba51f6` | `AGENTS.md` + `.agents/rules/` | `17e0887da07ceb3b017623b791b6a6999e837c79` | 干净工作树（`TWIN-57~59` 已提交推送） |
| `mcu-p3` | `feat/soc-debug` | `191e355a4227268a472bafd6862d448a854e0544` | `.repo-rules/AGENTS.md` + 本机链接 `AGENTS.md` | `17e0887da07ceb3b017623b791b6a6999e837c79` | 干净工作树（`TWIN-60` 已提交推送） |
| `boot/bootloadermc` | `soc_debug` | `4fc171ea61912561949b9a0cfc1da8975e4c39ba` | `.repo-rules/AGENTS.md` + 本机链接 `AGENTS.md` | `17e0887da07ceb3b017623b791b6a6999e837c79` | 干净工作树（只读核查） |
| `boot/bootloaderth` | `soc_debug` | `769fccbe52464ad7ceb856c5e89cb0d25abbbf87` | `.repo-rules/AGENTS.md` + 本机链接 `AGENTS.md` | `17e0887da07ceb3b017623b791b6a6999e837c79` | 干净工作树（只读核查） |
| `test_harness` | `main` | `9f3918a`（初查时 `d14ed04321c6d4f5ddb35a8801604a8af53b5b60`） | `AGENTS.md` + `.agents/rules/` | `17e0887da07ceb3b017623b791b6a6999e837c79` | 干净工作树（`TWIN-61` 已提交推送） |

## 3. 只读规划角色实际委派与已收件产物

| 规划角色范围 | 实际执行通道 / 会话 ID | 状态 | 已收件产物路径与 SHA-256 | 职责与只读边界 |
| --- | --- | --- | --- | --- |
| `ARCH`（主方案牵头人） | Subagent `arch` (`ef428595-f4d6-46a7-9d12-07e1fd215641` & `3a7ad206-fef7-4d28-b3c8-1ee5bce395a5`) | **已收件 (`Phase A rev 2` & `Master Plan rev 1`)** | 1. 架构核查与协议冲突对账回执 (`revision: 2`)：`project-control/docs/planning/minimc_v2_upgrade_arch_audit_receipt_20261105.md`（`sha256: 05308b35432bb483c2600130133b6105922159f3e3e763646d6468af15d9a6c0`）<br>2. 完整主方案 (`revision: 1`)：`project-control/docs/architecture/minimc_v2_unified_mcu_upgrade_architecture_20261105.md`（`sha256: 6c0e672c50bc526d8b4e662c2c354114ef5c8c0180d4a3dd5563908726584c7a`） | 牵头核对 `Rev 2.0.3`、已接受扩展方案与各端源码的协议契约冲突，汇总工程多端与独立 `QA` 输入形成完整版本化主方案 |
| `QA`（独立验收规划角色） | 独立 Codex 会话 (`01a1aafd-f2d4-7b91-a422-04ef47aefeb6` & `01a1ab34-f811-7ce2-b9d2-ae177ab18aef`) | **已收件 (`revision: 2`)** | 1. QA 规划输入与回执 (`revision: 2`)：`project-control/docs/planning/minimc_v2_upgrade_qa_planning_input_20261105.md`（`sha256: f41d27c2214cacd1113397f20eb50038a404df94781f4bfdb18239d5d6f246d9`）<br>2. 会话证据：`qa_planning_session.jsonl` (`sha256: ada0318fc9b5200aef011b25e28ddb5c4e77d40e084ec0c7fb091ce78639e4b6`)、`qa_planning_session_r2.jsonl` (`sha256: 663df69ff13da49509557a265912eadd989e68358c105cc74ff9f7a77fcdcdb9`) | 完成 `test_harness` 能力盘点、从统一契约独立推导固定字节用例、`0x10`/`0x12` 冲突回归判据、`check_opcode_alignment.py` 预期来源审计、U盘回归与说明书可执行性核对 |
| `ENG-FWD` / `ENG-STATE` / `ENG-MC` / `ENG-TH` / `ENG_BOOT_MC` / `ENG_BOOT_TH` / `INTEGRATOR`（含 `ENG-UI`/`ENG-NET` 入口核对） | 唯一工程 Subagent `eng-vertical` (`07a1f6dc-f47c-45e5-bf00-37ec14e2dfda`，接替 `484ac302-bd54-4e1b-be9f-0227e1475d5d`) | **已收件 (`revision: 1`)** | 工程多端合并技术输入与接单回执 (`revision: 1`)：`project-control/docs/planning/minimc_v2_upgrade_engineering_inputs_20261105.md`（`sha256: c79477a0b9bfa2b18d1451b91b2a6188aa4b50f72bc742a8640aa0a696a1610b`） | 显式读取各仓规则入口与源码，交付协议冲突（`0x10`/`0x12` 及最大载荷）各端兼容与迁移影响、帧容量（64B vs 520B）、维护互斥、U盘保留与 TH U盘升级兼容、16KB Flash/RAM 预算、236KB 对齐、打包/迁移/救援及《升级操作与 HIL 部署说明书》补齐计划 |

## 4. 阶段准入与当前推进状态

1. **所有前置角色专业输入与完整主方案均已收齐**：`ARCH`、`ENG-*`/`ENG_BOOT_*`/`INTEGRATOR` 与独立 Codex `QA` 的实际规划产物及主方案 `minimc_v2_unified_mcu_upgrade_architecture_20261105.md` (`revision: 1`, `sha256: 6c0e672c50bc526d8b4e662c2c354114ef5c8c0180d4a3dd5563908726584c7a`) 均已落盘并校验 SHA-256。
2. **当前等待动作**：已将完整主方案及 §9 实质待决事项（`D1~D4`）一次性呈交用户确认；**在用户确认前，保持规划/审阅阶段，绝不提前创建实现任务卡、不登记实现 `depends_on`、不修改任何业务源码**。
