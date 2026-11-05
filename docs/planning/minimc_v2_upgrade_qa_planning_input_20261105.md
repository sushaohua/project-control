---
title: MiniMCProto v2.0 双 MCU 统一升级 QA 规划输入
revision: 2
date: 2026-11-05
author: AI (Codex)，独立 QA 规划角色
requirement: REQ-20261105-003
demand: DEM-20261105-006
qa_policy: streamlined-v1
status: planning-input-not-executed-not-acceptance-report
---

# MiniMCProto v2.0 双 MCU 统一升级 QA 规划输入

## 修订历史

| revision | 日期 | 修订人 | 变更摘要 | 审批/执行状态 |
| --- | --- | --- | --- | --- |
| 1 | 2026-11-05 | AI (Codex)，独立 QA 规划作者 | 首版资产盘点、软件/HIL 验收矩阵、异常恢复、U盘回归、16KB/236KB 门禁及说明书核对 | 只读规划交付；非正式验收签署 |
| 2 | 2026-11-05 | AI (Codex)，独立 QA 补充规划作者 | 接收 submission revision 3；补齐检查器来源审计、主规范冲突、固定字节候选与协议/MTU 回归判据；保留 revision 1 全部验收范围 | 未执行、待非作者独立复核；统一契约未裁定，不冻结接口 |

revision 2 是用户本轮指定的补充只读规划。第 1～6 节保留首版覆盖与历史观察（新增来源见 §1.5），第 7～9 节补充协议专项；旧观察不冒充本轮重验。仅本文件可写，不修改业务代码、检查器、需求或状态，不运行构建、测试或硬件操作。统一契约由 ARCH 与相关 Owner 裁定并纳入同一完整方案，再由用户一次确认；本规划不替代该裁定或授权。

## 1. QA 规划角色接单回执（read_sources）

本会话按用户派单接单，关联 `REQ-20261105-003 / DEM-20261105-006`、U-D05、`PM:FEAT-OTA-001`。角色为独立 Codex QA **规划作者**，接收人为 COORD，技术汇总人为 ARCH。唯一写入路径为本文件；不更改需求、看板、其他规划、业务或测试代码，不提交或推送，不解除历史冻结。本次只做文件阅读、Git 身份/状态与本地历史查询、来源摘要核对及规划写作；未运行编译、测试、Docker、部署、烧录、复位、寄存器或串口操作，未占用 VMware/台架。

本文件中的编号是建议验收项，不是已创建实现任务或 `depends_on`。所有运行判据均供完整方案冻结及后续授权使用，**本轮执行结果一律为未执行**。本会话未获得可供归档的实际 Session UUID、运行审计或模型例外回执，不编造会话身份，不将本规划作者身份当成正式独立验收签署。

### 1.1 规则入口、来源与适用范围

以下为本轮 `read_sources` 回执。完整路径相对工作区根；同一行未重复仓名前缀的 `.repo-rules/` 路径相对该行仓库。公共原件取 `project-control/.agents/rules/`，没有依赖客户端自动继承。各仓只读检查前已核对其入口及所需规则来源。

| read_sources | 本轮读取版本/范围 | 适用说明 |
| --- | --- | --- |
| 根 `AGENTS.md`；`project-control/AGENTS.md` | 当前入口；管理仓 HEAD 见下表 | 用户本轮唯一输出白名单优先；不因规则创建额外回执文件 |
| `project-control/.agents/rules/repository_rule_sources.json` | schema 1，canonical 为 project-control | 分发入口；Boot 是两个独立仓 |
| `project-control/.agents/rules/repository_rule_boundaries.md` | 2026-11-04；头部对账基线 `7e826b89bdcfdd6048371205ce8cce1503f5e988` | 公共流程与本机硬件规则分别适用，该基线不冒充当前 HEAD |
| `project-control/.agents/rules/codex_qa_review.md` | updated 2026-11-04 | 独立会话、服务器候选、宿主机只读审阅、HW-G5～G7及 QA 作者产物非作者复核 |
| `project-control/.agents/rules/delivery_and_coord_gate.md` | 当前原件，重点 §3.1、§4.1～4.4、§5.1～5.4 | 软件/HIL 分层、同轮四方证据、程序预检及定向复验 |
| `project-control/.agents/rules/bootloader_role_boundaries.md` | revision 1，2026-11-03 | Boot Owner/分支边界；历史探针条款不覆盖本轮常规 App 部署禁令 |
| `test_harness/AGENTS.md`；`test_harness/.agents/rules/repository.md`；`test_harness/.agents/rules/shared/SOURCE.json` | SOURCE 的 `source_commit=17e0887da07ceb3b017623b791b6a6999e837c79`，`source_publication_at_capture=not-verified` | 独立预期与工具是受审资产；文件存在不证明 HIL 已执行 |
| `test_harness/.agents/rules/shared/` 下 `repository_rule_boundaries.md`、`code_documentation_standard.md`、`codex_qa_review.md`、`delivery_and_coord_gate.md`、`e2e_issue_verification_flow.md`、`c_cpp_coding_standard.md` | 本轮读取相关条款并与 canonical 逐文件字节比较，一致 | 不把规则分发快照自动当最新发布证明 |
| `soc-ap/AGENTS.md`；`soc-ap/.agents/rules/repository.md`；`soc-ap/.agents/rules/shared/SOURCE.json` | SOURCE 同为 `17e0887da07ceb3b017623b791b6a6999e837c79`，publication 为 not-verified | 本轮只核身份和规则，不代 AP 工程或实现审查 |
| `mcu-p3/.repo-rules/AGENTS.md`、`.repo-rules/AGENTS.legacy.md`、`.repo-rules/SOURCE.json`、`.repo-rules/.agents/rules/c_cpp_coding_standard.md` | SOURCE 公共来源同上；legacy SHA256 `2c0bdf6722429308ce569731a2766292554c55a69c5bf16d1b4fceb8386c4d54` | 只读核查旧 TH 调用、帧容量与 App 链接参数 |
| `boot/bootloadermc/.repo-rules/AGENTS.md`、`.repo-rules/AGENTS.legacy.md`、`.repo-rules/SOURCE.json`、`.repo-rules/.agents/rules/c_cpp_coding_standard.md` | SOURCE 公共来源同上；legacy SHA256 `47705eccd4c1fe7b7cc8470cba00607b3103880baef81e9aa40bfa0c7e63e086` | MC Boot 打包、校验与 U盘路径的源码观察 |
| `boot/bootloaderth/.repo-rules/AGENTS.md`、`.repo-rules/AGENTS.legacy.md`、`.repo-rules/SOURCE.json`、`.repo-rules/.agents/rules/c_cpp_coding_standard.md` | SOURCE 公共来源同上；legacy SHA256 `d66331914be260fa5ecf350a9e7ae4978bd3e1fc1d3a9c03eb6b18e294c01a24` | TH Boot 私有 IAP、Flash、打包与链接参数的源码观察 |

对 soc-ap 与三个 `.repo-rules` 仓，亦读取/比对其共享 `repository_rule_boundaries.md`、`code_documentation_standard.md`、`codex_qa_review.md`、`delivery_and_coord_gate.md`、`e2e_issue_verification_flow.md`、`c_cpp_coding_standard.md`；Boot 另核共享 `bootloader_role_boundaries.md`。本轮这些共享副本均与 canonical 字节一致。SOURCE 记录的是分发来源提交，不能用本轮相同比较推断服务器已发布或物理设备采用该版本。本机既有链接保留，未向链接目标以外探索。

### 1.2 六仓 revision 1 观察基线（revision 2 增量见 §1.5）

| 仓库 | 当前分支 | HEAD（完整 40 位） | 本轮工作树观察 |
| --- | --- | --- | --- |
| project-control | `main` | `5686e1931123650bb2251045353c18c8baa00f65` | 已有 intake 修改及本专项多份未跟踪材料；本文件为唯一新增交付 |
| soc-ap | `main` | `79932746d225bb115010c5545ef3f7499482e137` | 多项已有修改，涉及 HMI、device-manager、forward、ui-gateway 等；均保留 |
| mcu-p3 | `feat/soc-debug` | `891a8bb252814c83992a49b01fbe11ba83b92a1f` | 已有 MC CMakeLists、thermistor.c/.h 修改；均保留 |
| test_harness | `main` | `d14ed04321c6d4f5ddb35a8801604a8af53b5b60` | 观察时干净 |
| boot/bootloadermc | `soc_debug` | `4fc171ea61912561949b9a0cfc1da8975e4c39ba` | `.agents`、`AGENTS.md`、`docs` 为已有未跟踪本机入口 |
| boot/bootloaderth | `soc_debug` | `769fccbe52464ad7ceb856c5e89cb0d25abbbf87` | 同上 |

这些是本地观察值，未 fetch 或检查服务器，**不是冻结发布组合**；有工作树修改/未跟踪文件时 HEAD 不代表现场全部字节，更不代表片上 Boot/App 身份。正式验收须按第 6 节重建服务器候选链。

### 1.3 需求、协议与历史输入 read_sources

| 输入路径（project-control 内） | 版本与本轮用途 |
| --- | --- |
| `docs/work_intake/submissions/20261105_minimc_v2_upgrade_coord_planning_prompt.md` | 当前接收 revision 3；SHA256 `4699feade73d9e621b5ead2bade96ba195c488446de6e215bbb9b5276dcfcc80`，本轮文件字节摘要一致；重点 §2 先裁定协议冲突。首版读取 revision 2 / SHA256 `01687e475a1ca1bbdc7a884f5afe2e5f27b65f5018ed17c49fa2fbf59eb79d71` 的历史保留 |
| `docs/planning/minimc_v2_unified_mcu_upgrade_proposal_20261105.md` | revision 2；SHA256 `72c1a91a1487b7184ba371ea3ed653d038c741a7e8baf2eb98316e0d91e6dc2f`；助理讨论输入，未批准实现 |
| `docs/specs/ap_mc_formal_protocol_v2_0_multidevice_routing_draft_20261015.md` | `SPEC-PROTO-20261015-153000 / Rev 2.0.3`；SHA256 `9f8d4f9607cb3e76cc30b9ee2f971b23c3e0d936611188466a71f4aa15f3ce54`；帧、路由、会话与 OTA 的权威输入 |
| `docs/analysis/mcu_firmware_upgrade_design_20261031.md` | `ARCH-MCU-UPGRADE-DESIGN-20261031` revision 1；历史 MC 探针/TH 私有 IAP 方案，只作迁移对照 |
| `.agents/kanban/microtasks/vmware_soc_twin/TWIN-26.md`、`TWIN-27.md`、`TWIN-28.md` | 均 revision 1；读取原状态、范围、产物与历史接受，不改签署/冻结 |
| `docs/planning/qa_streamline_cutover_20261103.md` | revision 2，`coord-received-effective`；2026-11-04 正式收件段，消解规则页头“待切换”的历史提示，见第 6 节 |
| `docs/guides/minimc_v2_mcu_upgrade_and_hil_deployment_manual_20261105.md` | revision 1，草案，尚不可执行；核对说明书验收责任 |
| `docs/work_intake/requirements/REQ-20261105-003.yaml` | 只读核对关联；观察到其 source_refs 仍引用 submission revision 1/旧摘要，而上述 prompt 已 revision 2；由 COORD 对账，本轮不改 |

源码/工具的按需读取位置与事实见第 2 节；未运行这些脚本，也未 import 可能带串口/复位副作用的模块。

### 1.4 环境边界和当前未验证缺口

| 环境 | 后续允许证明的层级 | 本轮状态 |
| --- | --- | --- |
| 当前 Linux 文件工作区 | 文档与源码只读观察、验收规划 | 已读取；未验证服务器、容器或设备 |
| 独立 Linux Docker 软件沙箱 | 静态/交叉构建、镜像校验、协议/状态机及模拟故障的软件集成 | 尚未启动；不映射真实 USB/串口，不套用 Windows venv/COM 端口要求 |
| VMware AP + 真实 MC/TH 物理 HIL 台架 | 文件入口到真实双 MCU 升级、安全效果、启动身份及业务恢复 | 未连接、未申请租约、未实测；Windows/WSL 本机规则仅在对应获授权台架适用 |

当前缺口：完整架构方案及跨端字节契约尚待角色汇总接受；新 Boot 现场版本与首次迁移未核实；TH 16KB 实际体积、RAM/栈、236KB 全路径对齐未构建验证；新升级驱动、真实采集器与新用例尚未接受；设备/芯片准确型号、端口映射、波特率、时源、温度新鲜度阈值和安全恢复窗口未绑定。TH 仓使用 AT32A423 名称而旧 App/历史资料使用 AT32F423，须 Owner 用物理板身份、工具链/SDK 与制品映射核实，不能按 Board ID 相同自行抹平差异。

这些缺口不妨碍本轮规划交付，但阻断相应后续执行或通过声明。常规 App 部署不得用 probe-rs 或其他探针写入替代；首次 Boot 安装/特殊救援另交用户决定。读到的历史探针操作条款不构成本阶段操作授权。

### 1.5 revision 2 补充 read_sources 与身份回执

本轮角色仍为 QA 规划作者，交 COORD 收件、ARCH 汇总；没有以同会话改名自批，也没有启动子 Agent 或正式运行器。读取各目标仓入口、soc-ap/test_harness 的本仓规则及 SOURCE、MCU 的 `.repo-rules/AGENTS.legacy.md` / SOURCE；按需读取各仓共享边界、中文注释、C/C++、独立 QA、交付门禁与 E2E 条款，公共分发来源仍为 `17e0887da07ceb3b017623b791b6a6999e837c79`，publication 仍为 not-verified。canonical 原件为 project-control（manifest 标为 active-canonical）；本轮不重做首版 Boot 调查，不把首版规则比对或 Boot 观察描述为本轮重新验证。

| 本轮实际输入/路径（工作区相对路径） | revision 2 读取版本/摘要与用途 |
| --- | --- |
| `project-control/docs/work_intake/submissions/20261105_minimc_v2_upgrade_coord_planning_prompt.md` | revision 3；SHA256 `4699feade73d9e621b5ead2bade96ba195c488446de6e215bbb9b5276dcfcc80`；全文读取，重点 §2 的契约先行和检查器预期来源要求 |
| `project-control/docs/specs/ap_mc_formal_protocol_v2_0_multidevice_routing_draft_20261015.md` | `SPEC-PROTO-20261015-153000 / Rev 2.0.3`；SHA256 `9f8d4f9607cb3e76cc30b9ee2f971b23c3e0d936611188466a71f4aa15f3ce54`；§1～8 的帧、方向、载荷、CRC、错误、会话与 OTA |
| `project-control/docs/architecture/print_control_protocol_extension_design_20261031.md` | 当前文件及本地已跟踪同名路径未找到；不能证明扩展从未存在或未经接受。ARCH 须提供实际文件、准确版本/哈希及接受/替代关系，才能用其裁定冲突；不从源码反推接受 |
| 用户简写 `test_harness/static_checks/check_opcode_alignment.py` | 该路径不存在；实际资产是下行路径，不创建入口或移动文件 |
| `test_harness/static_checks/minimcproto/check_opcode_alignment.py` | SHA256 `bcc098de7793d08c79f391be82f55a1d3b099b9984f8db08952722ad8b1253e9`；全文只读及本地 `git log --follow` / `git show`，未运行/导入 |
| `soc-ap/core/forward/minimc/codec.h` | SHA256 `53fc801508e7cfdf1368d031b479b8f737317d21f20371949c2d49ce532434fa`；12B 头、Flags 与 `MAX_PAYLOAD_SIZE=1024`；该头本身没有业务命令表 |
| `soc-ap/contracts/twin/telemetry_types.h` | SHA256 `cb8fe4e894ea7c0857646432947ea93c95b1487aeae8353559e068e127da4381`；检查器实际 AP 输入，含系统控制/温控及急停/停止的同码定义，见 §7 |
| `mcu-p3/motion-controller-mcu/project/inc/minimc_proto.h` | SHA256 `21f66bf4446705e1a7afcbcf89166c60971d0347c45e7fdd4bf3f6f979e40e44`；命令、温控/运动布局、64B 上限 |
| `mcu-p3/color-engine-mcu/io_toggle/inc/minimc_proto.h` | SHA256 `3b4a8c44b8e054c2e9dbfcbd449d2aca498176d57c1b687108cc7f17c74487fe`；TH 子集、同码定义、64B 上限 |
| `project-control/docs/interfaces/ap_mc_th_readonly_cascade_icd.md` | 只读查阅其主规范/NACK 来源与作用域；只读级联 ICD 不能自动授权温控/运动重定义或 OTA 接口 |
| `project-control/docs/work_intake/requirements/REQ-20261105-003.yaml` | 本轮观察 requirement 自身 revision 4，source_refs 已绑定 submission revision 3 及本轮摘要，authorization_refs 保留 1/2/3；首版 §1.3、§6.4 的旧来源缺口在此更新，不修改需求文件。submission revision 3 与 requirement revision 4、本文件 revision 2 分别记录 |

| 本轮观察仓库 | 分支 / HEAD | 工作树及限制 |
| --- | --- | --- |
| project-control | `main` / `5686e1931123650bb2251045353c18c8baa00f65` | 已有 intake 修改及多份专项未跟踪文档，保留；只写本文件 |
| soc-ap | `main` / `19534a9a4cb393176882fbad046129d55bba51f6`（`19534a9`） | 本轮观察干净；替代首版 `7993274` 作为本轮源码观察基线，未 fetch、不作服务器或 HIL 通过声明 |
| mcu-p3 | `feat/soc-debug` / `191e355a4227268a472bafd6862d4a8c854e0544` | 观察到已有 `tools/diag/__pycache__/` 未跟踪目录，未触碰；非正式候选 |
| test_harness | `main` / `d14ed04321c6d4f5ddb35a8801604a8af53b5b60` | 检查器来源提交见 §7.1；未运行检查器，未改任何 QA 资产 |

## 2. 历史 TWIN-26～28 与现有资产盘点

### 2.1 冻结历史的实际范围

| 历史输入 | 观察事实 | 本轮可继承与限制 |
| --- | --- | --- |
| TWIN-26 | `Done` 且 `blocked: true`，人为冻结；候选 MC `04231388c842c1ce3e5b71675d0dc118a65edf2e`；卡内证据层级为 software-verified，旧命令 `0x10～0x13`、M997、升级透传 | 保留历史 QA/ENG-MC 签署及报告引用；可参考 UART 所有权交接意图。既非当前 MiniMC OTA 实现接受，也不证明当前真机升级 |
| TWIN-27 | Backlog/blocked；前置 TWIN-26 冻结，candidate null；计划 AP 扫描、Trailer 与准入 | 需求场景可参考，`firmware_updater.*` 是计划产物，不能据卡推断已实现或测试通过 |
| TWIN-28 | Backlog/blocked；candidate null；`test_mcu_firmware_upgrade.py` 为计划交付，验证命令还是 planned-not-runnable | 最终硬件目标保留；旧“0x01/0x02分别查 MC/TH”及 ST-Link 路线不能直接沿用 |
| 2026-10-31 设计 revision 1 | MC 首推探针直刷；TH `5A A5` 私有 IAP，512B 块及累加和；含 240KB、“预验签”“10秒恢复”等历史表述 | 新方案必须替换数据通道、容量与确认语义；时限、绝不变砖、签名和零 Boot 修改等说法不作为本轮既成保证 |

**指定脚本缺失事实：**本轮列举 `test_harness/hil/tests/`，并查询本地 `git log --all -- hil/tests/test_mcu_firmware_upgrade.py`，均未找到该文件或可见历史提交。因此不能列出它“已经实现”的旧通道分支；旧方案绑定来自上述历史卡/设计，不能补写成脚本实情。此查询仅覆盖本地可见 refs，未检查远端不可见历史。后续是否复用其他版本由 COORD/QA 提供准确来源；未提供前按新增升级用例/工具缺口处理。

### 2.2 test_harness 现存能力与改造边界

| 实际读取资产 | 可复用能力 | 必须新增/调整及证据限制 |
| --- | --- | --- |
| `static_checks/minimcproto/reference_vectors.py`、`run_codec_cases.py` | 独立 Python CRC16/帧解码/FSM参考；固定 V01～V04、超时恢复与逐例预期比对；拒绝空测试/未实现后端的思路 | 当前命令级参考限 GET_VERSION/VERSION_REPORT/PING/PONG，未覆盖 OTA/Flash。新增独立接受的 OTA 正负字节向量、Trailer 预期及状态断言；不能用打包器或生产 codec 同源生成输入与唯一预期 |
| `static_checks/minimcproto/check_opcode_alignment.py` | 跨端常量提取和一致性比较框架 | 现表含 SET_TEMP=0x10、MOTION_MOVE=0x12 等业务扩展，未列 OTA 0x20～0x23；与主规范 SYSTEM_CONTROL/ESTOP 存语义冲突，交 ARCH 冻结各模式命令表后针对升级扩展，不将现表直接当新协议裁决 |
| `static_checks/cascade/run_query_cases.py` | 原生帧 CRC、端到端 SRC/DST/响应与超时的独立比对结构 | 运行引擎用 PTY 模拟，适用于 Docker 软件层。新增真实 MC 路由与 Boot 升级测试，禁止将 PTY 的 TH 响应当硬件帧 |
| `hil/twin_capture/twin_capture_analyzer.py` | 12B 头、Raw Hex/CRC、采样节拍解析方法 | 现业务解码针对温度、部分关联按 seq；不构成 OTA 或动态代次验证。须扩展 OTA 字段、完整请求键、双向路由、时源与 Flash 事件；“physical”文件名不证明物理来源 |
| `hil/tools/debug_reconciliation_probe.py` | MC/TH Debug 基础解析与 AP 状态对账方法 | 有 fixture、自测及 PTY daemon 路径，不能进最终 HIL 证据链；需升级事件适配、原始帧和实际 Flash/测量证据，不能只改表格 passed。Boot 允许精简事件，不强制复制 App 全量 Debug 格式 |
| `hil/tools/device_discovery.py`、`probe_fault_injector.py`，`hil/tests/test_probe_tools.py` | 历史身份识别、防误操作及故障工具设计参考 | discovery/injector 可能读写寄存器/复位；本轮仅读。test_probe_tools 明确用 Mock/AST，不能证明设备。后续诊断/注入沿原授权独立核实，不能被用于替代新流程写 App |
| `hil/tests/test_qa_e2e_hotunplug.py`、`test_qa_e2e_oobe_browser.py`（相关身份断言检索） | 既有入口/断连回归场景参考 | 有固定提交标识断言，须绑定本轮候选；不得以历史固定短哈希证明新 App 身份 |

### 2.3 Boot 打包、校验与旧调用的源码观察

| 来源 | 实际能力/风险 | 规划处理 |
| --- | --- | --- |
| `boot/bootloadermc/scripts/pack_firmware.py`；`bootloader/inc/firmware_trailer.h` | 使用小端 `<IIIII32s32s32s8s`，前124B CRC32，尾部总128B；计算净荷 SHA256；sig_r/s 全零预留。打包器未见完整目标/容量准入门禁 | 布局、净荷摘要计算可复用；建立独立黄金包并补错板/空包/超限用例。128B Trailer 总长、净荷长度、文件哈希分别对账 |
| `boot/bootloaderth/tools/pack_firmware.py` | 同布局；计算 SHA256 与 CRC32，但 `MAX_PAYLOAD_SIZE=240*1024`，版本默认与 MC 工具不同 | 统一版本来源与236KB边界；现打包成功不能证明 TH Boot 会接受，不运行打包器生成本轮“通过” |
| MC `bootloader/src/usbh_user.c` 的 `verify_firmware_trailer` / `write_bin_to_flash` | 实查 magic、MC Board ID、净长度与文件关系，再查地址范围；随后按净荷擦写、Flash 与文件硬件 CRC 比对。该准入函数未见 Trailer CRC、SHA256 或密码学签名校验；CRC 末字按4B补齐口径与串口 IEEE CRC32 不能混称 | 保留 U盘完整能力，但须由 Owner 冻结本轮准入职责；在正确包及每项坏包上逐项核验，不沿用“预验签”日志名称夸大校验范围 |
| TH `inc/iap.h`、`src/iap.c`、`src/flash.c`、`inc/flash.h` | `5A A5`+CMD+LE长度+累加和；128B START Trailer 检查 magic/Board/长度/Trailer CRC，未见 SHA/签名验证。第0块512B缓存于 SRAM先 ACK；Finish 用缓存首块+Flash后续段计算 CRC，再提交锚点/首块；启动完整性校验有无锚点时仅向量校验的历史回退 | Flash 擦写回读、首块保护和锚点思路可由 Owner评估复用；协议解析/应答/偏移/计数须按 v2重构。首块缓存不能算 Flash写入；须验证提交失败、掉电和“无锚点”回退不会启动不完整新镜像 |
| TH `Makefile`、`ldscripts/AT32A423xC_FLASH.ld` | 已链接 FLASH=16K，`.data >RAM AT>FLASH`，输出 ELF/BIN/map/size；RAM=48K，保留 heap/stack 符号 | 这是现有链接约束，无新实现体积实测；不能凭 ELF文件大小或仅.text判16KB通过，见 S01 |
| `boot/bootloadermc/scripts/verify_mcu_p3_uboot_suite.py`、`verify_step1*.py`、`verify_step2*.py`、`verify_step3_dual.py` | 既有 happy/cross/corrupt/repeat/nodisk/relay 场景；硬编码 Windows探针/COM口并可复位；多数以日志关键词作判据，relay仍查旧HELLO/Chunk；某些脚本顶层即串口/复位 | 场景与采集思路可复用，执行器与判定需适配；日志中出现“erase aborted”不独立证明零擦除，关键词 Jumping不证明新App。禁止直接执行或import这些资产作为本轮检查 |
| `mcu-p3/motion-controller-mcu/project/inc/th_upgrade_mgr.h`、`project/marlin/marlin_module/th_upgrade_mgr.c`，`project/src/main.c`、`usbh_user.c` | TH调用仍为512B/旧CMD与240KB；main初始化/轮询管理器，U盘移除通知管理器；健康TH开机5秒后可永久停轮询。`project/inc/minimc_proto.h`载荷上限64B | 兼容回归须覆盖 U盘提供TH镜像、移除清理及开机窗口外主动升级；不保留5A A5转换层。MC Boot只升级MC，TH升级由MC App承担 |
| TH App `mcu-p3/color-engine-mcu/io_toggle/libraries/cmsis/cm4/device_support/startup/gcc/linker/AT32F423xC_FLASH.ld` | App基址0x08004000，FLASH长度仍240K | 链接、MC侧准入、TH打包与Boot一并对齐236KB，不能只修一处常量 |

旧软件通过不能外推：旧候选、旧帧格式/Opcode/容量、Mock/PTY或主机桩的环境均与新原生 OTA 不同；没有物理 Flash、现场固件身份和安全测量证据。TWIN-26 的 software-verified 接受仅保留原范围；TWIN-27/28 的计划与冻结状态不构成通过记录。

## 3. 软件沙箱 vs 真实 HIL 分层验收矩阵

### 3.1 冻结判据前必须补齐的技术契约

下列是 QA 向 ARCH/对应 Owner 的输入缺口，不由 QA 自定义新线缆格式：

1. **擦除前 Trailer 与 START 对应**：Rev 2.0.3 的 OTA_START 固定16B，不能直接携带128B Trailer。冻结 Trailer 的传递/重组/绑定机制、何时准入/擦除、`fw_size_bytes`/offset/CRC 的净荷或整包口径，并保证各端一致；未收全必要元数据前不得擦除。若需调整规范，须准确 revision/哈希及各端接受，不能私加 START 后缀或私有帧。
2. **帧容量**：主规范 L≤1024，OTA_DATA 含8B头，常规块64～1016B；现MC L≤64时最多只余56B数据，不能承载64B最小常规块。若选64B块，至少 L=72、总帧86B；若选512B块，L=520、总帧534B；上限总帧1038B。冻结共同上限、末块不足64B及奇数净荷处理、DMA/环形/路由缓冲和栈预算，不盲目假设全端都可1024B。
3. **确认语义**：规范 DATA 文字要求写Flash成功再ACK，但旧首块策略先缓存。需统一缓存受理、实际持久写入、完整校验、首块/锚点提交、App启动各自确认方式；`OTA_STATUS.bytes_written` 8B载荷定义为实际Flash字节。若缓存首块改变ACK语义，须显式契约调整/接受，不能仅改UI文案或占用ACK保留字段。
4. **进入维护、身份与恢复**：冻结 App→Boot系统控制、Boot最小身份/能力、两板版本组合、超时/有限重试、会话代次及恢复准入。`GET_VERSION=0x01`/`VERSION_REPORT=0x02` 对两板相同，目标由DST=0x02/0x03区分。状态超时不能统一“豁免安全准入”。
5. **安全与校验职责**：ENG-STATE给出温度来源/validity/新鲜度、运动静止及维护互斥证据和期限；各Owner冻结CRC参数/范围、SHA在哪层实际核验、Flash/启动保护、首次Boot迁移与救援。恢复MC时无法从坏App取得温度，应提供独立可核实的安全隔离/测量准入，不能把未知温度当0°C。

### 3.2 静态/构建门禁（后续由独立 Docker Runner 执行）

| 编号 | 覆盖与通过判据 | 必须保存的证据 | 本轮 |
| --- | --- | --- | --- |
| S01 TH Boot16KB | Flash固定 `[0x08000000,0x08004000)`，16,384B。统计向量表、`.text`、`.rodata`、其他ALLOC装载段及 `.data` 的Flash LMA副本，纳入对齐/空隙，逐段与最高装载结束地址均不越界；不能只相加text或比较ELF文件大小。边界内成功，增加Flash占用越界须构建非零失败且不发布可用制品 | 准确源码/工具链/链接参数；BIN字节数、ELF文件大小与section/LMA占用分别报告；map、段地址清单、原始构建/失败日志及SHA256 | 未执行 |
| S02 RAM/栈 | TH48KB RAM内 `.data/.bss`、帧/首块缓存、环形/发送缓冲、最坏调用栈/ISR嵌套与保留升级标志地址不冲突；报告剩余量。链接脚本最小栈保留不等于最坏栈已证明；不足不得删安全校验促16KB达标 | map及栈使用/调用链分析；Owner明确预算。HIL补适用峰值证据；本轮无实测预算值 | 未执行 |
| S03 TH净App236KB | `payload_len≤241,664B`；App装载范围 `[0x08004000,0x0803F000)`，锚点仍0x0803F800，间隔与锚点保留区不挤占；不重划分区。链接LMA、打包器、AP/MC准入、THBoot、写地址与填充均同界。净荷241,663/241,664/241,665B及遗留240KB包覆盖；上限包加128B Trailer为241,792B，文件长度不与净荷上限混算 | 全路径参数对照、独立边界包预期、ELF/map/包清单；超限包“拒绝且零擦除”证据 | 未执行 |
| S04 最小子集/代码防御 | TH仅必要OTA/身份/ACK/NACK子集，无旧私有转换层或完整业务协议栈；对改动核函数≤50行、入参≤4、中文注释/文档、安全长度/溢出、定长内存、超时及强类型错误 | 差异、适用规则与静态结果；第三方/历史无关代码保持最小修改；不能单凭字符串未出现证明行为正确 | 未执行 |

### 3.3 Docker 软件集成层

受控Runner从服务器锁定候选，在不接硬件的独立Docker内运行真实编解码、路由、升级状态机和Flash适配层；可用明确标记的Flash模型/PTY故障夹具，不旁路生成成功日志。每项只能接受所声明软件范围。

| 编号 | 场景与判据 | 关键证据/对应负例 |
| --- | --- | --- |
| D01 包识别/准入 | 128B Trailer逐字段小端解析：magic、struct_ver、BoardID、版本、净长度、SHA256、保留字段策略、前124B CRC与末4B；文件长度=净荷+128，目标/组件/Start与包一致。按冻结职责校验完毕才允许擦除 | 独立固定包及字段偏移；magic数值0x41545347按现工具LE字节为`47 53 54 41`，不可凭“ATSG”标签直接写成ASCII顺序。错板/坏CRC/截断/附加字节/未知版本/空包/超限及不完整Trailer，Flash擦写调用计数0、原快照不变 |
| D02 文件就绪/输入锁定 | VMware目录的软件扫描链经过实际服务；复制未完成不触发升级，封存已确认文件身份，同名替换/重复发现不换包、不并发升级；发现文件与开始升级分开 | 文件事件、入口结果、封存哈希及事务ID；复制中/同名替换/重复点击/扫描重启的拒绝和恢复 |
| D03 四命令完整流程 | 按冻结契约执行0x20 START、0x21 DATA、0x22 FINISH、0x23 STATUS；请求/响应SRC/DST、flags版本位、seq、载荷精确长度及双CRC正确。每Peer可靠请求in-flight=1，响应回显seq | 固定正负字节向量、真实被测路径日志；错误版本/flags/长度/seq/无效目标、Boot/Config组件拒绝，不开放运行期Boot自升级 |
| D04 容量/边界 | 冻结共同MTU，验证最小常规块、选定最大块、末块、非整字/非整页长度、跨2KB扇区、越界offset和加法/乘法溢出；DMA发送期间独占副本不被下一帧覆写 | 源码/缓冲预算、边界帧及内存保护结果；超过选定MTU、1025B载荷、截断帧、粘包/拆包/50ms字节间超时后恢复，不越界写 |
| D05 首块与进度 | 同时记录接收/缓存量、实际Flash写入量、已验证量及启动结果（概念指标，不擅增线缆字段）。仅首块缓存后其持久写入量为0；后续块写回读成功才增量；首块最终提交后仅增加其真实有效长度一次 | Flash模型操作序列与STATUS逐步对账；丢ACK重传不重复加数；全量收齐但未FINISH不得显示持久完成/新App已生效；缓存首块丢失后的状态可识别 |
| D06 终验/启动保护 | 按明确范围CRC32：传输净荷/整包、末块填充、SRAM首块+Flash尾段的预提交校验与首块提交后Flash全净荷回读分别命名。全部成功才允许有效标记/锚点和启动 | 模型写失败、回读失败、锚点/首块提交各失败点；FINISH ACK仅证明已定义阶段，重连版本核对前不能作最终成功。无锚点回退也需坏镜像负例 |
| D07 TH透明路由 | AP→MC App→THBoot，业务cmd/payload/seq不改；Hop递减、routed置位、CRC重算、水平分割；MC本机应答不能冒充TH应答 | AP-MC与MC-TH双段输入/输出；非法route组合、TTL耗尽、拥塞/下游无响应不合成成功。MCBoot没有TH路由 |
| D08 AP维护互斥 | 安全准入与资源占用原子交接：打印/回零/调平/运动/加热/另一路升级互斥，AP单通信入口，MC App旧升级轮询与业务解析不争抢；未知/过期温度拒绝；升级中拒绝普通控制 | IDLE正例及忙/错误/断连/陈旧值/并发入口负例；锁持有、超时释放/恢复与上层状态轨迹。维护重启不显示业务健康 |

### 3.4 真实物理 HIL 最终出口

最终验收组合锁定AP、MC App、TH App与两Boot的准确版本/配置/制品；前置模块软件票可先按软件范围接受。以下顺序在后续获授权的排他台架窗口由受控HIL执行器/INTEGRATOR执行，Codex审阅席位只读审计证据。

| 编号/顺序 | 实际操作与通过判据 | 同轮必需证据 |
| --- | --- | --- |
| H01 台架前提 | 核对Boot已具备新协议且初始迁移有独立授权/记录，设备身份、AP/MC与MC/TH业务口、各Debug口、波特率及采集时源锁定；采集先于模式切换启动，不争抢串口 | 芯片/板卡清单、端口角色、实际波特率；Boot/旧App身份及源码→制品→部署映射。不能由历史COM8/COM6推定当前端口 |
| H02 VMware投放与准入 | 将封存fw_th/fw_mc包投放已确认的真实VMware目录，由实际用户入口确认；强电加热0%锁死、目标0、电机静止且去能、真实温度有效新鲜、作业空闲才进入维护 | 实际目录/包哈希、入口受理/拒绝与事务ID；同采样温度/有效性/新鲜度、相关MC/TH Debug、实际PWM/驱动使能测量或受控现场观察。仅软件变量=0不足；不为测试安全门禁开启加热/运动 |
| H03 先TH | AP以SRC0x01/DST0x03经MC App受控进入THBoot，完成START/DATA/FINISH/STATUS与校验；MC保持路由职责，无5A A5/ASCII转换 | 两段真实TX/RX Hex，匹配seq与时戳、Hop/Route/CRC变化；MC路由/App与THBoot事件；TH实际Flash写入/回读范围、首块和锚点提交 |
| H04 TH生效后再MC | TH新App重新握手、身份/业务恢复确认后，才以DST0x02让MC进入MCBoot并升级自身；MCBoot期间不尝试TH路由 | TH成功关口、MC模式交接与完整OTA帧、MCBoot写入/回读/启动事件；两升级阶段不重叠，TH失败不能继续宣称组合完成 |
| H05 新App与业务恢复 | 分别以GET_VERSION0x01收VERSION_REPORT0x02，核对proto、版本及git_commit_short映射到本轮完整commit/固件SHA256；记录动态boot_id变化与旧会话清理；完成两端真实PING、温度/状态查询及维护退出 | 升级前后Boot/App身份、实际原始应答；boot_id变化依据及冷启动/复位行为，不能用常量证明；真实新鲜温度与0%锁保持。范围内其他业务只按既有受控方案验证，不擅自加热/运动 |
| H06 非实现者说明书验证 | INTEGRATOR发布操作说明书准确revision/哈希，由非实现者按实际入口独立完成一轮受控部署与台架交接 | 操作者、工具/包、步骤/命令/cwd/超时/退出码或界面记录，原始证据及缺项；说明书草案不作为当前执行入口 |

每个H项都按**同一升级事务/请求或采样**关联：入口结果 → 真实业务请求/匹配响应 → 所涉及Boot/App Debug事件 → Flash校验/真实安全测量或物理效果。关联键至少含run、节点、升级事务、会话代次、cmd/seq与offset（若适用），记录时间源与跨日志对齐依据；仅seq不足以区分回绕/重启。原始双向Hex保留毫秒时戳、端口及波特率，不用解码摘要替代原始流。

Flash最终证据应列实际起止地址、有效长度、算法/填充、期望/实际摘要或CRC、回读来源；“缓存首块+Flash尾部”不冒充“Flash整镜像”。必要读回采用Owner批准的诊断机制，在后续具体授权内采集，不能在本规划阶段读寄存器/Flash。缺少真实回包的正常用例不能通过；PTY、Mock、旧烧录日志、文件复制、FINISH ACK及UI100%均不能单独证明最终升级成功。

## 4. 负例、异常注入与恢复验收设计

先完成健康台架正常路径，再按下表开展完整故障/恢复；安全前检始终在先。Docker层用可控夹具重复覆盖；标HIL的场景须在真正被测链路施加故障，另取受控窗口、供电/线路与恢复授权。每例注入前保存候选/包身份、节点状态、预期Flash范围与可恢复方式；异常后先采证再恢复，不先探针重刷抹去现场。

| 编号 | 注入位置/方法（后续执行） | 预期与恢复判据 | 层级 |
| --- | --- | --- | --- |
| N01 超时/无响应 | START、DATA、FINISH、STATUS及App重连分别延迟/阻断真实响应；软件层用时钟/链路夹具 | 有界等待/有限重试；上抛强类型错误与`target_node, sequence_id, elapsed_ms, error_code`。无ACK不增进度、不报成功；重连身份/代次核对后按已冻结机制重新开始 | Docker + HIL |
| N02 丢ACK | 对已实际受理/写入块仅丢其返回ACK，再以同seq重发；分别测试首块/普通块/FINISH | 幂等回显已接受终态，不二次擦除、写入或重复加计数；ACK须来自目标节点。过期缓存/跨boot_id旧ACK拒绝；FINISH响应丢失先查真实启动身份，不盲目重新擦写 | Docker + 受控物理链路HIL |
| N03 多级CRC损坏 | 分别破坏外帧CRC16、重算外帧后破坏chunk_crc16、Trailer CRC、净荷SHA、Finish全量CRC | 帧CRC按规范静默丢弃加计数，由发送侧超时报错，不期待坏帧一定NACK；内块/镜像校验按冻结错误契约失败。准入失败零擦除，终验失败不得启动坏App | Docker；相关HIL回读与拒绝 |
| N04 重复/冲突块 | 同seq同内容重传；同offset不同内容；更旧seq、窗口超前及半周期歧义、65535→0回绕 | 最近重复请求幂等；冲突数据不静默接受；乱序/过时按标准NACK/期望seq，offset不连续/越界拒绝；Flash未越界，恢复后正确包可重刷 | Docker + 关键HIL |
| N05 非法目标/错板/超限 | DST=0/未支持节点/广播、多播；START目标与DST/Trailer Board不一致；TH包伪装MC文件名；组件Boot/Config；TH净荷241,665B、240KB及溢出长度 | 擦除前明确拒绝，App/Boot/锚点前后不变；正确236KB边界正例配对。不通过force跳过硬安全、错板或容量门禁 | Docker + 关键HIL零擦除对账 |
| N06 维护互斥/失效测量 | 作业忙、运动未停、PWM非零的状态输入；温度validity无效/哨兵/过期、单板失联；两个升级入口并发 | 拒绝且未擦除；不为构造负例实际启动强电/运动。故障解除并取得真实新鲜采样后重新准入；恢复态不无条件免安全门禁 | Docker + HIL安全采集 |
| N07 断连/热拔线 | 分别断AP-MC物理串口、MC-TH链路与Debug采集链；对软件层对应错误注入 | 停止推进、通信丢ACK即挂起为PAUSED/明确升级失败且不报完成；AP物理ttyUSB拔除后CPU≤2%，3s内降级及温度哨兵，上层控制HTTP503/504（依冻结入口）。Debug丢失标证据缺口，不虚称业务断连。重接后重建会话/核身份/安全再升级 | Docker + 必需真实HIL |
| N08 复位/掉电 | 擦除后、仅首块已缓存、传输中、校验中、锚点/首块提交前后分别受控切断/复位；MC/TH分别覆盖 | 已破坏App时应留在可识别Boot恢复入口，不跳部分镜像；完整有效App按冻结规则启动。记录电源时刻与事件/Flash状态；重上电用新会话与完整包重新开始，成功后重新证明身份与业务 | Docker故障点模型 + 授权物理HIL |
| N09 Flash/文件失败 | 模型擦除/编程/回读错误、U盘读取/目录/改名失败；真实HIL只使用Owner接受且可恢复的故障方法 | 错误传播、无错误成功标记、保护Boot及保留区；恢复条件和文件处置明确。若无安全可用的实物Flash故障注入机制，声明软件覆盖及HIL缺口，不能伪造实际Flash失败 | Docker；适用受控HIL |
| N10 部分升级 | TH已成功后MC升级失败，或TH失败但MC仍健康 | 报实际混合版本、失败节点及影响，维护锁/恢复策略符合兼容矩阵；不自动宣称整组成功或两板都回旧版。恢复后重核双板身份 | Docker + HIL |

N07 CPU须由执行器记录被测AP相关进程集合、采样窗口、核数归一化口径、负载及拔线时点，窗口/算法在正式计划冻结；不以瞬时截图代替≤2%结论，不自行扩大MCU CPU指标。3s从物理断连时点核对状态/温度/入口锁定的真实时序。

N05“拒绝擦除”不能只依据没有日志：Docker观察真实Flash适配层擦写调用与前后快照；HIL结合目标拒绝帧、Boot准入/擦写事件及Owner批准的App/锚点/Boot保护范围摘要或读回核对。缺少可验证的无副作用证据时保留该项待验证。

### 4.1 MC App 不可用时的完整恢复路线

1. 分别构造“MC App不能运行但MCBoot可用、THBoot待恢复”和“MC App故障、THApp仍健康”两例；由后续授权方式进入故障态，不在本轮制造坏固件或复位。
2. AP识别MC App无响应，不对TH产生成功应答，不尝试让MCBoot路由TH；保留TH真实当前版本/未知状态。
3. 核对MCBoot身份/能力、MC安全隔离及新鲜测量或Owner批准的独立安全证据。若无法验证加热0%/运动静止，则保持阻塞，不能用丢心跳当作安全。
4. 用MCBoot自身MiniMCProto串口通道恢复MC，或按已保留的MC U盘恢复SOP恢复MC。完整核对Trailer、擦写、终验、App启动与新boot_id/版本/commit映射。U盘成功只记U盘恢复，不冒充VMware串口通过。
5. MC App真实启动后恢复维护路由；重新检查TH身份与安全，从AP→MC App→THBoot完整重刷TH。再完成双端身份、真实温度/心跳、维护退出及错误清理核对。
6. 若MCBoot本身无新入口、损坏或无法恢复，停止自动尝试并交COORD/对应Owner；首次Boot迁移或特殊探针救援须用户另行决定，不作为常规App部署例外。

不承诺断点续传、自动回滚、A/B、密码学签名验签或历史“10秒复苏”。STATUS有bytes_written不等于断电后持久恢复能力；只有统一契约、持久元数据与实际掉电证据支持时才另验续传。当前恢复验收以**重新准入、重新握手、完整镜像重传**为规划基线，并要求Owner落实可用路径。CRC/哈希仅按实际职责说明完整性，不将预留sig_r/s称为真实性认证。

## 5. MC 原有 U盘升级完整回归方案

U盘入口是独立必验能力。软件层覆盖文件/USB状态机及Flash适配层；真实物理USB Host枚举、持久改名、Flash写入和跳转必须回到真实MC。测试人员不得以探针部署App代替该入口，也不能因新串口通过而删掉以下回归。

| 编号 | 正例/异常与恢复 | 验收证据与判据 |
| --- | --- | --- |
| U01 USB Host枚举 | 冷启动有盘、无盘有效App、无盘无效App、枚举后拔盘/再插及文件系统挂载失败 | 真实USB事件/MCBoot Debug；有效App按冻结探测窗口启动，无有效App保持可恢复；不照搬历史2s作为未接受的新性能保证 |
| U02 文件识别 | FAT/文件系统与标准8.3文件名按Owner确认；正确fw_mc.bin、大小写、仅fw_th.bin、两文件并存、无包、截断/复制未完成 | 目标依据Trailer与BoardID而非文件名；MCBoot只处理MC，不把fw_th当MC刷；两包并存后App可重新枚举处理TH调用 |
| U03 128B准入 | 合法包、缺Trailer/128B空净荷、坏magic/Board/结构版本/长度/CRC、payload损坏、超MC边界 | 本轮冻结哪些层实际验证CRC/SHA后逐项断言；未实现校验作为缺口而非套用“预验签通过”。准入拒绝前后Flash不变；错误文件处置有证据 |
| U04 擦写/终验 | 正常大小、末字1/2/3B及跨2KB边界、MC允许净荷边界；读取中断、拔盘、编程/校验失败 | 记录地址0x08020000起的准确净荷、补齐与硬件CRC口径，源文件/Flash对账；不写Trailer入App，不越Boot/Flash端界。失败不误报新App启动 |
| U05 跳转生效 | 正常写入后启动MC App；Boot→App外设/中断/VTOR/栈及USB状态交接 | 启动实际应答、动态boot_id、版本/短commit与全commit/制品映射、真实查询恢复；仅Marlin Banner或Jumping关键词不足 |
| U06 防重复刷写 | 成功改fw_mc.cur，重上电/拔插不重复擦写；旧.cur存在、只读盘、改名/卸载/重挂载/FS check失败，失败包.err | 在物理盘独立确认旧.bin消失、新文件存在、长度/哈希一致并持久；后续启动擦写次数为0。改名失败有可操作错误/保护策略，不因前面Flash成功就虚报防重能力通过 |
| U07 新串口与U盘共存 | 同时提供串口请求与U盘包、恢复中切换入口、失败后重新枚举 | 按冻结仲裁仅一个写入所有者，拒绝冲突且有界释放；不交错擦写或提前跳App。MCBoot仍无TH路由 |
| U08 MC App调用TH升级 | 从物理U盘提供fw_th.bin、MCBoot跳入App后USB重新枚举、MC App五秒窗口内/外、TH健康/Boot待恢复、传输中拔盘及恢复、两包串行 | 现有th_upgrade_mgr初始化/轮询/移除通知调用兼容；替换为统一MiniMCProto原生OTA，无旧私有帧/ASCII旁路。核TH Trailer236KB与末块、真实双段帧/Flash终验/启动身份、fw_th.cur防重；失败状态清理、UART所有权及AP维护互斥均核对 |

U08的保留/复用方式须在ARCH完整方案中明确，不能仅保留USB驱动或把旧调用留在不可达分支。实际源码存在开机五秒后停轮询策略，须由Owner说明主动升级和既有启动窗口各自行为；QA按接受后的契约验证，不自行要求永远自动扫盘。MCBoot升级MC与MC App升级TH职责始终分开。

## 6. 独立 QA 流程与非作者复核要求

### 6.1 本轮规划与后续策略

本轮按`qa_policy: streamlined-v1`规划。规则页头仍有候选提示，但`qa_streamline_cutover_20261103.md` revision 2已记录2026-11-04 COORD正式生效：管理仓源码`cec9b34f8284f7b2580a7d219536d32b7b1ee849`，根仓`e5b7ec6d80259976b8a38e4164b5596311fed15f`，证据归档`613f3cbc9a58283ff085cee241de9810895cfdb4`。本轮读取该接受记录，不重新执行其196项检查，不声称本会话重新审定历史证据。

后续新任务由COORD显式登记该策略；TWIN-26～28无策略迁移记录，继续保留legacy及冻结要求，不仅改标记套用旧报告。必要Owner接受与显式额外Reviewer均保留；本升级涉及跨端协议、启动/Flash安全，ARCH及相关App/Boot/FWD/STATE Owner先核实各自契约与专业输入，不据此默认每份结果报告再审一轮。

### 6.2 后续确定性执行与只读独立审阅

1. **输入与资产冻结**：完整方案由用户确认后，ARCH提供唯一字节/镜像/状态契约、技术拆分与路径；COORD登记任务revision、策略、验收编号、作者/非作者、准确服务器组合、必要Owner接受及资源。测试计划/预期/工具版本也锁定，未知超时/温度新鲜度/恢复策略先补契约，不由测试默许。
2. **QA作者资产非作者检查**：后续新增或修改的OTA用例、固定正负字节向量、Trailer黄金包、预期状态/错误/计数、Flash模型、故障夹具、采集器、对账/证据工具均属QA作者产物。按规则由**未参与作者工作的独立Codex会话承担ARCH检查**，核需求推导、预期独立性、故障真实落点、目标绑定/写失败传播、状态快照与恢复边界。QA作者不能切换角色自批；实现者自测也不能替代。本规划及其编号预期在正式采用/冻结前亦须非作者独立核对；本轮未执行该复核，不将文件交付当作复核已完成。
3. **程序预检**：复用现有校验器检查任务revision、候选commit、run、所有输入引用/哈希、制品和证据完整性。必要材料缺失/摘要不符保持待审，不因机械错误开启无关构建或改写结论；本轮没有运行这些检查器。
4. **Runner软件执行**：受控Python Runner从服务器fetch准确各仓commit，在独立Docker沙箱检出、确定性构建和执行适用测试；不共享作者Git对象库、可写工作树、构建输出或不可信缓存，不把宿主Docker socket挂入容器。记录job/远端ref/commit、容器ID/镜像digest、实际inspect挂载/状态、工具链/配置/依赖、命令/cwd/退出码、原始输出与制品SHA256，归档`server_qa.json`、`runtime.log`等客观物证。
5. **HIL执行与证据接收**：由COORD分配唯一VMware/真实台架排他窗口，实际授权到设备/端口/供电故障点/恢复条件。受控HIL执行器或INTEGRATOR按H01～H06、异常/恢复及U盘清单采证；常规App部署走正式升级流程。Docker profile若无真实HIL执行器、双段帧采集或Flash证据入口，先落实工具与接收路径，不能只填hardware-verified。工程联调不能替代正式接受。
6. **宿主机独立Codex审阅**：Runner客观证据固化并校验后启动独立Reviewer，读取容器受控导出或独立取得的**同一服务器候选只读快照**及证据；完整commit、快照/证据摘要必须一致。不得读取作者可写工作树作正式基线，不在宿主机补跑受审代码构建/测试，不让Reviewer启动Docker或补写计划。Reviewer无需也不得依赖直连USB，核齐客观物证即可审计；不以只读席位无法碰硬件为阻塞理由。
7. **会话与模型真实登记**：后续按规则显式请求`gpt-6-luna`，其他模型须COORD登记实际角色/会话/原因/批准证据。保存真实Session UUID、实际模型、启动/运行审计及可用token用量；计划别名、普通子Agent名或CLI exit0不能代替独立会话和APPROVED，不归档API token或凭据。
8. **报告与收件**：逐例记录通过/失败/未执行/阻塞/不适用及依据，分别说明静态/软件/HIL接受范围；绑定源码、设备/固件、包、工具/预期、run、会话及原始证据。报告完成后从文件字节重算SHA256，绑定在外部收件记录，避免自引用。本轮输出只有规划，不预填APPROVED或任务Done；正式收件/关闭仅COORD有权进行。

streamlined-v1只有一轮独立QA（代码Review＋功能/必要回归证据），**不默认逐份二次复核QA执行报告**，不为审报告重复同候选Docker测试；QA作者资产的非作者ARCH检查是作者分离门禁，不递归审其检查报告。legacy未迁移卡继续原报告复核，不能删除历史签名或已显式指定岗位。

### 6.3 复验、结论与证据限制

同一任务revision、完整候选、测试计划、工具/配置/依赖与证据哈希一致时可复用已验证沙箱事实；变化时说明影响并重验受影响部分。新候选需新独立接受，不拼接不同候选冒充全套通过。首审尽量列齐已知阻断/恢复路径；复验聚焦原finding、整改差异及必要回归；保留原run、失败现场与整改映射，不用换run清零返工预算。

REJECTED须绑定已接受条款或有位置/复现证据的功能、安全、协议/真实性风险；措辞排版和无行为影响建议可随批准保留。服务器/会话/容器/设备或证据来源缺失记BLOCKED/INCONCLUSIVE或按schema保留待审，不计无关代码退修。所接受范围内必测项缺失不签相应APPROVED，软件通过不替HIL通过，负例通过不抵消正常升级未完成。

### 6.4 交 ARCH/COORD 的规划缺口清单

| 缺口 | 补齐责任/解除条件 | 影响 |
| --- | --- | --- |
| START/Trailer擦除前绑定、共同MTU/末块、缓存ACK/Flash计数与CRC范围 | ARCH牵头FWD、MC/TH App与双Boot Owner，交准确契约及独立可推导预期 | 正式用例/工具冻结及升级安全接受 |
| TH16KB实际预算、236KB全端一致、芯片名称/板身份冲突 | ENG_BOOT_TH、ENG-TH/MC、INTEGRATOR提供源码/配置/板身份依据；后续Docker构建证据 | Boot/App边界与现场制品映射 |
| 新软件工具/真实HIL双段采集、Flash证据及可恢复故障方案 | QA作者/INTEGRATOR交工具与接收入口，经非作者独立检查 | 软件与硬件执行可行性，尤其零擦除/首块提交/掉电恢复 |
| 已部署Boot和首次迁移、恢复时独立安全准入 | 双Boot/App Owner及ENG-STATE提供SOP/准入；必要首次迁移另获用户决定 | 真实升级及MC不可用恢复；不以探针临时部署绕过 |
| 操作说明书可执行性与U盘TH调用兼容 | INTEGRATOR主责、各端Owner核实；功能交付时非实现者完成实际受控操作 | 后续常规测试/HIL部署入口 |
| 新旧需求来源revision/哈希与历史冻结衔接 | COORD核对prompt revision2与REQ来源字段，按现有流程收件；不在本轮改需求/卡 | 专项范围追溯，不能自动解冻TWIN-26～28 |

本轮已完成的是上述只读资产核查与验收设计。所有构建、软件运行、真实升级、故障注入、U盘回归与说明书实操均未执行；本文件供ARCH汇总完整方案、COORD收件，不能单独授权实现或硬件操作。

## 7. check_opcode_alignment.py 预期来源审计与规范符合性缺口

### 7.1 可追溯来源与不能推定的接受

本轮只读定位到实际脚本 `test_harness/static_checks/minimcproto/check_opcode_alignment.py`，未执行它。其本地可见历史为：

| 来源提交（test_harness） | 可核对的变更 | 结论边界 |
| --- | --- | --- |
| `dccf2de1ec680cbf7456c76d70970b0338710e8e`，2026-11-02 | 新建脚本，头注引用主规范及 `SPEC-ALIGN-20261102-01 §5.2`；原功能是 NACK=0x06、3B 载荷、17B CAS-NEG-008 的六项防漂移检查 | 此处“17”原指 NACK 整帧字节数，不是当前 17 个命令；历史引用不能替后来新增命令提供规范授权 |
| `2812f60f5250d777d38a55537d9d5018cb603692`，2026-11-04 | 改写为当前 `EXPECTED_OPCODES` 17 项硬编码矩阵及三端宏比较；删除原规范/矩阵来源说明与原 CRC/ICD/案例检查 | 当前 17 项表的直接代码来源已定位；脚本没有逐项契约条款、版本/哈希或扩展接受引用 |
| 本轮 HEAD `d14ed04321c6d4f5ddb35a8801604a8af53b5b60` | 脚本仍是上述 17 项表，文件 SHA256 见 §1.5 | 仅本地观察；没有取得服务器锁定、当前执行结果或新接受 |

脚本注释把表称为“权威”，但执行路径只读 AP 的 `contracts/twin/telemetry_types.h` 和 MCU 两份 `minimc_proto.h`，用正则提取宏/constexpr 数值，再逐端比较硬编码值；它**没有读取主规范、版本化注册表、扩展接受记录或协议配置清单**。本轮找不到指定扩展设计文件，故不能判定该表来自某个已接受扩展；能够证明的是代码引入来源与当前业务表一致，不能把“与源码一致”倒置为“从主规范独立推导”。AP 本地历史可见 `cd87958` / `333178c` 引入/调整业务表，但也不凭提交标题认定规范替代已获接受。

### 7.2 当前 17 项与 Rev 2.0.3 的逐项差异

主规范依据为 §5.1、§5.2 和 §8，不从实现取唯一预期。

| 当前检查器语义=数值 | 主规范 Rev 2.0.3 | 分类/当前检查遗漏 |
| --- | --- | --- |
| ACK=0x00 | ACK=0x00，响应，4B | 数值相符；未查响应 Flags、信用/保留字段 |
| GET_VERSION=0x01 | 主→从，0B，回 0x02 | 数值相符；未查方向/空载/会话 |
| VERSION_REPORT=0x02 | 从→主，响应，16B | 数值相符；未查字节布局与 boot_id |
| PING=0x03 | 双向，4B，回 0x04 | 数值相符；未查应答关联 |
| PONG=0x04 | 双向响应，12B | 数值相符；未查时间戳/信用 |
| NACK=0x06 | 响应，3B，错误码+LE expected_seq | 数值相符；不再覆盖原案例的 CRC/长度 |
| SET_TEMP=0x10 | **SYSTEM_CONTROL=0x10**，3B action+LE delay_ms | **语义冲突**；实现温控请求是4B、两个 int16 温度，非系统控制别名 |
| MOTION_HOME=0x11 | 主表未登记 | 扩展来源/接受待提供；不是主规范已定义命令 |
| MOTION_MOVE=0x12 | **EMERGENCY_STOP=0x12**，广播、priority、禁止 WANTS_ACK、2B reason | **语义冲突**；MC move 是16B axes/relative/feed/x/y/z，非急停子集 |
| JOB_CONTROL=0x13 | 主表未登记 | 扩展来源/布局/响应待裁定 |
| TEMP_REPORT=0x15（允许 TEMP_REPORT_V2 名称） | 主表未登记 | 两个名称仅在语义、方向、单位和布局完全相同且获接受时可作合法别名；同码 FILAMENT_CONTROL 不能仅凭宏名放行 |
| POS_QUERY=0x16 | 主表未登记 | 扩展来源/20B 布局待裁定 |
| MOTION_STOP=0x17 | 主表急停在0x12 | 普通停止与全网锁存急停不能自动互作别名；AP 的 EMERGENCY_STOP=0x17 未被检查 |
| LEVEL_GRID_QUERY=0x18 | 主表未登记 | 扩展来源/52B 布局待裁定 |
| SLOT_SELECT=0x19 | 主表未登记 | 扩展来源/别名及方向待裁定 |
| LEVEL_TRIGGER=0x1A | 主表未登记 | 扩展来源/响应待裁定 |
| GCODE_EXEC=0x1C | 主表为 STREAM_CHUNK=0x31 事务通道 | 扩展来源/兼容影响待裁定，不能等价替代0x31 |

另有确定的漏检：

- AP 同时声明 SYSTEM_CONTROL=SET_TEMP=0x10；声明 EMERGENCY_STOP=MOTION_STOP=0x17。脚本只挑已列别名，不遍历剩余定义查语义冲突，故即使 17 项全通过也不会揭示这些冲突。
- OTA_START/DATA/FINISH/STATUS=0x20～0x23、SYSTEM_CONTROL、规范急停、LOG_MESSAGE、STREAM_CHUNK、TELEMETRY_REPORT、ALARM_EVENT 均未作为本轮规范符合性集合检查。TH Boot 可以是经接受的最小功能子集，但“未支持”必须按节点/模式显式登记并拒绝，不能用所有端都没有该命令作为符合性依据。
- AP `codec.h` 的 MAX_PAYLOAD_SIZE=1024、MC/TH 头的 MINIMC_MAX_PAYLOAD_SIZE=64 不在检查范围；Flags/载荷长度、端序、CRC、响应错误、路由、Flash/ACK 语义也未覆盖。
- AP 还定义 ESTOP_ACK=0x05；主规范 §5.1 / §8 定义的是 ACK=0x00、NACK=0x06，未登记0x05。本次补充要求中的“0x05/0x06”应分别审计，**不能写成主规范 ACK=0x05**。广播急停明确禁止即时 ACK，不能以 ESTOP_ACK 名称覆盖该规则。

因此，“17 个命令码对齐通过”至多说明 **AP、MC、TH 头文件中被选中的宏，在脚本自定义表上数值一致**，不证明编译采用的定义/实际分发一致，更**不能证明符合主规范 Rev 2.0.3**。三端共享同一错误表完全可能一起通过。真实 HIL 若也共享该表，能证明相应实机行为发生，仍不能证明命令语义、版本与规范相符；**规范符合性、端间一致性和真实物理闭环分别必需，互不替代**。本轮不撤销或改写历史报告，差异交 ARCH/COORD 按准确候选和原批准范围处理。

### 7.3 后续检查器如何绑定唯一权威契约

以下仅为后续资产要求，本轮不修改脚本：

1. ARCH 会同 FWD、MC/TH App、双 Boot Owner 交付唯一版本化契约及裁定/迁移记录，写清主规范条款、接受扩展、优先/替代关系、各节点 App/Boot 能力子集；冲突不得由 QA/COORD 猜测改号。每项登记命令数值/唯一语义、合法别名、方向、Flags、载荷字段偏移/类型/长度/单位/端序、响应/错误、MTU、OTA 块/末块、CRC 与确认阶段。
2. 静态工具从该准确契约数据加载预期，绑定契约 ID/revision、管理仓完整 commit、原始文件 SHA256、schema 和必要 Owner 接受引用；本轮候选尚无这些接受，不能把本文候选向量当作已发布注册表。缺失、摘要不符、未知 revision 或未裁定条目须阻断相关范围，禁止退回硬编码表/从实现自动学习预期。
3. 分开报告“对权威契约符合性”与“端间一致性”；枚举所有有效定义和消费入口，捕获未声明扩展、同码异义、非法别名、错误节点/模式、遗漏的 OTA 子集。数值/布局静态核对之外，软件层还须以固定字节检查生产编解码及分发、副作用、路由与错误路径，不能靠正则证明行为。
4. QA 依据已接受条款独立维护固定输入/期望，生产 codec/打包器不得同时成为输入与唯一预期来源。规范数据可以共享，推导与审计须独立；记录每向量→条款/裁定、夹具前提、字节、校验值及版本。工具改动加入故意冲突的负样例：三端同时改成旧码仍应失败；删除/篡改契约、额外冲突宏和隐藏别名也应失败。
5. 检查器、协议静态检查器、用例及预期均为 QA 作者资产，正式冻结/消费前由未参与写作的**独立 Codex 会话承担非作者 ARCH 检查**，绑定准确候选、计划/工具/预期摘要及实际会话证据，检查期望来源、完整性、拒绝路径与不自证。沿用 streamlined-v1，不因此新增默认 QA 报告复核轮次或重复同候选 Docker 运行。

## 8. 从主规范独立推导的 Golden Wire Vectors（统一契约候选）

### 8.1 冻结状态、依据与夹具

**当前尚无已接受的统一契约，不能声称已经“从已裁定契约”推导完成。** 本节交付可审阅的完整固定字节候选，以 SHA256 已锁定的 Rev 2.0.3 §1～5 为起点；采用 §5.1/§5.2 的系统控制、2B 急停、ACK=0x00/NACK=0x06 定义。其与源码的差异及主规范 §7 旧 V04（空载急停14B）和 §5.1/§5.2（2B急停16B）的内部冲突一并交 ARCH 裁定。旧 V04 不直接删除或冒充合规正例。若裁定改变任一命令/Flags/字段/错误/边界，须修订关联向量和迁移用例、重新非作者接受后才能冻结；不能在执行中临时选择“更容易通过”的版本。

帧排列严格为 `55 AA SRC DST FLAGS CMD HOP ROUTE SEQ_LE16 L_LE16 PAYLOAD CRC_LE16`，总长 L+14。所有多字节载荷小端；CRC16-CCITT-FALSE 参数为 poly=0x1021、init=0xFFFF、RefIn/RefOut=false、xorout=0，覆盖 SOF 起至载荷尾，**不含自身**，低字节先发。OTA 内块 CRC 只覆盖 firmware_bytes；全量 CRC32 为 IEEE 802.3（本节夹具采用反射多项式0xEDB88320、init/xorout=0xFFFFFFFF）。本轮仅在文档写作过程中按这些数学参数计算字节和校验值，不导入、执行或调用任何仓库 codec、检查器、构建/测试程序，不构成编解码测试通过或独立复核。

正常请求 Flags=0x05（版本0x04+WANTS_ACK），响应 Flags=0x06（版本+IS_RESPONSE，禁止再请求 ACK）；急停广播 Flags=0x14。普通发起 Hop=4、Route=0；MC 每次转发 Hop减1、Route置0x04并重算 CRC，SRC/DST/seq/cmd/载荷不变。响应交换端地址、回显 seq，不能误把响应 Flags 的0x06 当 NACK 命令字。下列每个代码块标签是向量 ID，标签不进入线上字节；换行/空格无含义，所有块都完整列出，无省略号。

软件夹具前提（非设备事实）：

- 版本夹具：proto=2.0、firmware major/minor=1/2、boot_id=0x12345678、git_commit_short=0x89ABCDEF、capability_flags=0。只检字段排列，不据此证明真实固件或赋予未定义能力位含义。TH 版本回复与 MC 使用同一字段格式、以 SRC 区分。
- ACK 夹具：planner_buf_free=32、rx_fifo_free_units=2、reserved=0。实际目标信用可变，固定回复字节只对该受控软件状态有效；最大块正例发送前另设信用至少17单位（1088B）。响应中的信用为处理后的快照。
- OTA 软件镜像夹具 I64：64B，即00～3F；chunk_crc16=0xFD2F，fw_crc32=0x100ECE8C；START 的 new_version_raw=0x01020304仅核小端，不裁定版本数值打包规则。它不是可启动固件，不可用于实机刷写。模型预置合法目标、维护联锁/必要元数据已接受、足够 Flash、写入/回读成功；START/Trailer 尚待统一的线上交互不能靠这些预置冒充实现。
- G01～G08 的逻辑序列：版本seq0、系统控制seq1、START seq2、DATA seq3、FINISH seq4、STATUS seq5。实际 App→Boot 后必须重建身份/代次并同步序号，不能直接沿用旧 App 的 seq；此处各行是在指定模式/会话中独立设置期望 seq 的软件夹具，并非省略握手的真实升级脚本。G07 action=0不重启，方便核对 G08。
- 负例各自独立重置夹具，expected_seq固定等于该行请求seq（业务拒绝未受理），不与正常序列串跑。可疑响应不能推进 pending 事务；精确错误码/拒绝后序号策略、内块 CRC 失败映射、非法急停回复策略须随统一契约显式接受，下面相应字节为候选预期。

### 8.2 身份、方向、系统控制及急停

G01：AP→MC GET_VERSION；响应16B载荷的 boot_id、commit 小端字段必须逐字节相符，不接收 ACK 替代 VERSION_REPORT。

G01-Q（14B）：

```text
55 AA 01 02 05 01 04 00 00 00 00 00 F9 1E
```

G01-R（30B）：

```text
55 AA 02 01 06 02 04 00 00 00 10 00 02 00 01 02
78 56 34 12 EF CD AB 89 00 00 00 00 8E 3E
```

G02：AP→TH 同一查询的两段物理链路，以及 TH 回复的两段物理链路。Q0=AP→MC、Q1=MC→TH；R0=TH→MC、R1=MC→AP。MC 不能返回 SRC=0x02 冒充 TH。

G02-Q0（14B）：

```text
55 AA 01 03 05 01 04 00 00 00 00 00 DA F5
```

G02-Q1（14B）：

```text
55 AA 01 03 05 01 03 04 00 00 00 00 9D B4
```

G02-R0（30B）：

```text
55 AA 03 01 06 02 04 00 00 00 10 00 02 00 01 02
78 56 34 12 EF CD AB 89 00 00 00 00 EF 92
```

G02-R1（30B）：

```text
55 AA 03 01 06 02 03 04 00 00 10 00 02 00 01 02
78 56 34 12 EF CD AB 89 00 00 00 00 7D E4
```

G03：主规范 SYSTEM_CONTROL，action=2（JumpToBootloader）、delay_ms=1000；维护许可已在夹具满足。只允许系统控制分发，温度设定/运动副作用为0。ACK 不是 Boot 已启动的证明，切换后另需身份与新代次核对。

G03-Q（17B）：

```text
55 AA 01 02 05 10 04 00 01 00 03 00 02 E8 03 43
9B
```

G03-R（18B）：

```text
55 AA 02 01 06 00 04 00 01 00 04 00 20 02 00 00
B2 43
```

G04：按主规范 §5.1/§5.2 的2B reason=0x0001 全网急停；预期即时响应字节串为**空串（0B）**，不得造 ACK/NACK。安全停机/KILLED 由后续独立状态/物理证据确认，不以无回包当动作完成。旧空载 V04 的处理须先裁定，当前不作为正例。

G04-Q（16B）：

```text
55 AA 01 FF 14 12 04 00 00 00 02 00 01 00 C2 1C
```


### 8.3 OTA 四命令与进度的完整请求/响应

G05：START：target=MC(2)、component=App(1)、force/reserved=0、size=64、CRC32=0x100ECE8C、version_raw=0x01020304。模型擦除成功才允许此 ACK；真实 START/Trailer 绑定未裁定前不能把这一模型前提当成准入已实现。

G05-Q（30B）：

```text
55 AA 01 02 05 20 04 00 02 00 10 00 02 01 00 00
40 00 00 00 8C CE 0E 10 04 03 02 01 13 B0
```

G05-R（18B）：

```text
55 AA 02 01 06 00 04 00 02 00 04 00 20 02 00 00
C7 8B
```

G06：DATA：offset=0、chunk_bytes=64、内块CRC=0xFD2F，L=72。模型持久写入64B并回读成功后才允许此 ACK；若采用缓存首块策略须由统一契约另行裁定，不能沿用此 ACK 字节却偷换确认含义。

G06-Q（86B）：

```text
55 AA 01 02 05 21 04 00 03 00 48 00 00 00 00 00
40 00 2F FD 00 01 02 03 04 05 06 07 08 09 0A 0B
0C 0D 0E 0F 10 11 12 13 14 15 16 17 18 19 1A 1B
1C 1D 1E 1F 20 21 22 23 24 25 26 27 28 29 2A 2B
2C 2D 2E 2F 30 31 32 33 34 35 36 37 38 39 3A 3B
3C 3D 3E 3F 33 1B
```

G06-R（18B）：

```text
55 AA 02 01 06 00 04 00 03 00 04 00 20 02 00 00
14 CC
```

G07：FINISH：CRC32=0x100ECE8C、action=0、reserved[3]=0；模型回读全量一致并完成有效标记后 ACK。真实重启 action=1 的100ms后复位及新App握手另按 H04/H05，不在本例虚称启动完成。

G07-Q（22B）：

```text
55 AA 01 02 05 22 04 00 04 00 08 00 8C CE 0E 10
00 00 00 00 0D B2
```

G07-R（18B）：

```text
55 AA 02 01 06 00 04 00 04 00 04 00 20 02 00 00
0C 0B
```

G08：STATUS：请求0B，响应8B，SUCCESS=4、error=0、reserved=0、bytes_written=64。响应 Flags=0x06、cmd仍0x23、seq=5；不把 STATUS 响应再当请求回 ACK，亦不把“接收64B”偷换为“Flash已写64B”。

G08-Q（14B）：

```text
55 AA 01 02 05 23 04 00 05 00 00 00 A9 AC
```

G08-R（22B）：

```text
55 AA 02 01 06 23 04 00 05 00 08 00 04 00 00 00
40 00 00 00 3E 8B
```


### 8.4 命令冲突、NACK、内外 CRC 与故障码候选

G09：cmd=0x05 的请求在**主规范注册集合夹具**中未登记，候选响应 NACK(cmd0x06)、ERR_UNKNOWN_CMD=0x04、expected_seq=1。0x05 不是主规范通用 ACK；AP 现有 ESTOP_ACK 扩展的接受/迁移另行裁定。该例不把请求未知码与收到伪 ACK 混为同一行为。

G09-Q（14B）：

```text
55 AA 01 02 05 05 04 00 01 00 00 00 8B A9
```

G09-R（17B）：

```text
55 AA 02 01 06 06 04 00 01 00 03 00 04 01 00 43
E6
```

G10：旧 SET_TEMP=0x10 的4B载荷（nozzle=200.0℃、bed=60.0℃），送入按主规范裁定后的接收端必须拒绝，候选 NACK ERR_COMMAND_REJECTED=0x06。不能取前3B执行系统控制、忽略末字节、设置温度或生成成功 ACK。

G10-Q（18B）：

```text
55 AA 01 02 05 10 04 00 01 00 04 00 D0 07 58 02
FF 82
```

G10-R（17B）：

```text
55 AA 02 01 06 06 04 00 01 00 03 00 06 01 00 23
88
```

G11：旧 MOTION_MOVE=0x12 的16B单播请求（X相对移动1mm、feed=300mm/min），按主规范急停定义不合法。候选对该可靠单播回 ERR_COMMAND_REJECTED（非法急停回复策略仍须接受）；必须不移动、不按长度猜测旧协议、不得误触全网急停。无论最终选择何种拒绝响应，不能视为成功控制。

G11-Q（30B）：

```text
55 AA 01 02 05 12 04 00 01 00 10 00 01 01 2C 01
E8 03 00 00 00 00 00 00 00 00 00 00 86 3C
```

G11-R（17B）：

```text
55 AA 02 01 06 06 04 00 01 00 03 00 06 01 00 23
88
```

G12：DATA offset=64，而模型期望offset=0且size=64；外层CRC及内块CRC均正确，独立触发 ERR_OTA_INVALID_OFFSET=0x13。拒绝后Flash、写入计数及expected_seq不变。

G12-Q（86B）：

```text
55 AA 01 02 05 21 04 00 03 00 48 00 40 00 00 00
40 00 2F FD 00 01 02 03 04 05 06 07 08 09 0A 0B
0C 0D 0E 0F 10 11 12 13 14 15 16 17 18 19 1A 1B
1C 1D 1E 1F 20 21 22 23 24 25 26 27 28 29 2A 2B
2C 2D 2E 2F 30 31 32 33 34 35 36 37 38 39 3A 3B
3C 3D 3E 3F 3B 3A
```

G12-R（17B）：

```text
55 AA 02 01 06 06 04 00 03 00 03 00 13 03 00 31
26
```

G13：TH START size=241665（LE `01 B0 03 00`），比236KB上限多1B；其他元数据/联锁均预置合法。期望 ERR_OTA_IMAGE_OVERSIZE=0x14、零擦除，不能先核无关镜像内容掩盖尺寸门禁。Q=AP→MC、Q1=MC→TH；R=TH→MC、R1=MC→AP，四帧完整列出。

G13-Q（30B）：

```text
55 AA 01 03 05 20 04 00 02 00 10 00 03 01 00 00
01 B0 03 00 8C CE 0E 10 04 03 02 01 94 44
```

G13-Q1（30B）：

```text
55 AA 01 03 05 20 03 04 02 00 10 00 03 01 00 00
01 B0 03 00 8C CE 0E 10 04 03 02 01 06 32
```

G13-R（17B）：

```text
55 AA 03 01 06 06 04 00 02 00 03 00 14 02 00 92
6D
```

G13-R1（17B）：

```text
55 AA 03 01 06 06 03 04 02 00 03 00 14 02 00 54
D3
```

G14：FINISH 声称 CRC32=0，但已写 I64 CRC为0x100ECE8C；外层CRC有效。期望 ERR_OTA_CRC_MISMATCH=0x12，拒绝有效标记/跳转。

G14-Q（22B）：

```text
55 AA 01 02 05 22 04 00 04 00 08 00 00 00 00 00
00 00 00 00 5F 9E
```

G14-R（17B）：

```text
55 AA 02 01 06 06 04 00 04 00 03 00 12 04 00 D2
91
```

G15：内块CRC由0xFD2F改为0xFD2E，**外层CRC已经重算且有效**，以隔离内块检查；预期零编程/计数不变。主规范对内块CRC错误未明确单独错误映射，下面 ERR_COMMAND_REJECTED=0x06 是待裁定候选，不能冒充规范已明定；不得误用“全量CRC32不匹配0x12”掩盖两层职责，也不得因外帧有效而接受数据。

G15-Q（86B）：

```text
55 AA 01 02 05 21 04 00 03 00 48 00 00 00 00 00
40 00 2E FD 00 01 02 03 04 05 06 07 08 09 0A 0B
0C 0D 0E 0F 10 11 12 13 14 15 16 17 18 19 1A 1B
1C 1D 1E 1F 20 21 22 23 24 25 26 27 28 29 2A 2B
2C 2D 2E 2F 30 31 32 33 34 35 36 37 38 39 3A 3B
3C 3D 3E 3F AC 57
```

G15-R（17B）：

```text
55 AA 02 01 06 06 04 00 03 00 03 00 06 03 00 A2
8E
```

G24/G25：分别重用 G05-Q / G06-Q 的完整请求，模型仅注入擦除失败/编程失败；响应分别为0x10/0x11错误码，绝不能生成 ACK。这是后续软件故障夹具预期，不是本轮实际注入。

G24-R（17B）：

```text
55 AA 02 01 06 06 04 00 02 00 03 00 10 02 00 31
F4
```

G25-R（17B）：

```text
55 AA 02 01 06 06 04 00 03 00 03 00 11 03 00 51
48
```


### 8.5 最大载荷边界完整字节与64B断点

G16：最大合法帧候选，DATA offset=0、chunk_bytes=1016、firmware_bytes为 `i mod 256`（i=0..1015），内块CRC=0xF13D；L=1024、整帧1038B、外层CRC=0x1F09。模型先置合法 size≥1016、预期offset=0、seq=3和足够信用/缓冲；成功持久写入才回 G16-R。**只有统一契约接受该节点/模式的1024B MTU后才是端到端正例**；目前 MCU64B 定义不足，不能预填通过或把安全拒绝当该正例已满足。

G16-Q（1038B）：

```text
55 AA 01 02 05 21 04 00 03 00 00 04 00 00 00 00
F8 03 3D F1 00 01 02 03 04 05 06 07 08 09 0A 0B
0C 0D 0E 0F 10 11 12 13 14 15 16 17 18 19 1A 1B
1C 1D 1E 1F 20 21 22 23 24 25 26 27 28 29 2A 2B
2C 2D 2E 2F 30 31 32 33 34 35 36 37 38 39 3A 3B
3C 3D 3E 3F 40 41 42 43 44 45 46 47 48 49 4A 4B
4C 4D 4E 4F 50 51 52 53 54 55 56 57 58 59 5A 5B
5C 5D 5E 5F 60 61 62 63 64 65 66 67 68 69 6A 6B
6C 6D 6E 6F 70 71 72 73 74 75 76 77 78 79 7A 7B
7C 7D 7E 7F 80 81 82 83 84 85 86 87 88 89 8A 8B
8C 8D 8E 8F 90 91 92 93 94 95 96 97 98 99 9A 9B
9C 9D 9E 9F A0 A1 A2 A3 A4 A5 A6 A7 A8 A9 AA AB
AC AD AE AF B0 B1 B2 B3 B4 B5 B6 B7 B8 B9 BA BB
BC BD BE BF C0 C1 C2 C3 C4 C5 C6 C7 C8 C9 CA CB
CC CD CE CF D0 D1 D2 D3 D4 D5 D6 D7 D8 D9 DA DB
DC DD DE DF E0 E1 E2 E3 E4 E5 E6 E7 E8 E9 EA EB
EC ED EE EF F0 F1 F2 F3 F4 F5 F6 F7 F8 F9 FA FB
FC FD FE FF 00 01 02 03 04 05 06 07 08 09 0A 0B
0C 0D 0E 0F 10 11 12 13 14 15 16 17 18 19 1A 1B
1C 1D 1E 1F 20 21 22 23 24 25 26 27 28 29 2A 2B
2C 2D 2E 2F 30 31 32 33 34 35 36 37 38 39 3A 3B
3C 3D 3E 3F 40 41 42 43 44 45 46 47 48 49 4A 4B
4C 4D 4E 4F 50 51 52 53 54 55 56 57 58 59 5A 5B
5C 5D 5E 5F 60 61 62 63 64 65 66 67 68 69 6A 6B
6C 6D 6E 6F 70 71 72 73 74 75 76 77 78 79 7A 7B
7C 7D 7E 7F 80 81 82 83 84 85 86 87 88 89 8A 8B
8C 8D 8E 8F 90 91 92 93 94 95 96 97 98 99 9A 9B
9C 9D 9E 9F A0 A1 A2 A3 A4 A5 A6 A7 A8 A9 AA AB
AC AD AE AF B0 B1 B2 B3 B4 B5 B6 B7 B8 B9 BA BB
BC BD BE BF C0 C1 C2 C3 C4 C5 C6 C7 C8 C9 CA CB
CC CD CE CF D0 D1 D2 D3 D4 D5 D6 D7 D8 D9 DA DB
DC DD DE DF E0 E1 E2 E3 E4 E5 E6 E7 E8 E9 EA EB
EC ED EE EF F0 F1 F2 F3 F4 F5 F6 F7 F8 F9 FA FB
FC FD FE FF 00 01 02 03 04 05 06 07 08 09 0A 0B
0C 0D 0E 0F 10 11 12 13 14 15 16 17 18 19 1A 1B
1C 1D 1E 1F 20 21 22 23 24 25 26 27 28 29 2A 2B
2C 2D 2E 2F 30 31 32 33 34 35 36 37 38 39 3A 3B
3C 3D 3E 3F 40 41 42 43 44 45 46 47 48 49 4A 4B
4C 4D 4E 4F 50 51 52 53 54 55 56 57 58 59 5A 5B
5C 5D 5E 5F 60 61 62 63 64 65 66 67 68 69 6A 6B
6C 6D 6E 6F 70 71 72 73 74 75 76 77 78 79 7A 7B
7C 7D 7E 7F 80 81 82 83 84 85 86 87 88 89 8A 8B
8C 8D 8E 8F 90 91 92 93 94 95 96 97 98 99 9A 9B
9C 9D 9E 9F A0 A1 A2 A3 A4 A5 A6 A7 A8 A9 AA AB
AC AD AE AF B0 B1 B2 B3 B4 B5 B6 B7 B8 B9 BA BB
BC BD BE BF C0 C1 C2 C3 C4 C5 C6 C7 C8 C9 CA CB
CC CD CE CF D0 D1 D2 D3 D4 D5 D6 D7 D8 D9 DA DB
DC DD DE DF E0 E1 E2 E3 E4 E5 E6 E7 E8 E9 EA EB
EC ED EE EF F0 F1 F2 F3 F4 F5 F6 F7 F8 F9 FA FB
FC FD FE FF 00 01 02 03 04 05 06 07 08 09 0A 0B
0C 0D 0E 0F 10 11 12 13 14 15 16 17 18 19 1A 1B
1C 1D 1E 1F 20 21 22 23 24 25 26 27 28 29 2A 2B
2C 2D 2E 2F 30 31 32 33 34 35 36 37 38 39 3A 3B
3C 3D 3E 3F 40 41 42 43 44 45 46 47 48 49 4A 4B
4C 4D 4E 4F 50 51 52 53 54 55 56 57 58 59 5A 5B
5C 5D 5E 5F 60 61 62 63 64 65 66 67 68 69 6A 6B
6C 6D 6E 6F 70 71 72 73 74 75 76 77 78 79 7A 7B
7C 7D 7E 7F 80 81 82 83 84 85 86 87 88 89 8A 8B
8C 8D 8E 8F 90 91 92 93 94 95 96 97 98 99 9A 9B
9C 9D 9E 9F A0 A1 A2 A3 A4 A5 A6 A7 A8 A9 AA AB
AC AD AE AF B0 B1 B2 B3 B4 B5 B6 B7 B8 B9 BA BB
BC BD BE BF C0 C1 C2 C3 C4 C5 C6 C7 C8 C9 CA CB
CC CD CE CF D0 D1 D2 D3 D4 D5 D6 D7 D8 D9 DA DB
DC DD DE DF E0 E1 E2 E3 E4 E5 E6 E7 E8 E9 EA EB
EC ED EE EF F0 F1 F2 F3 F4 F5 F6 F7 09 1F
```

G16-R（18B）：

```text
55 AA 02 01 06 00 04 00 03 00 04 00 20 02 00 00
14 CC
```

G17：L=64、数据56B；G18：L=65、数据57B。二者帧CRC/内块CRC有效，但按 Rev 2.0.3 的常规块最小64B，均不是合法常规 OTA_DATA。模型镜像size≥128以排除末块；若共同MTU允许到达业务层，候选响应均复用 G15-R（ERR_COMMAND_REJECTED，expected_seq=3）。当前MCU64B时 G17可到帧级边界但应在业务层拒绝，G18已超当前帧容量，应安全拒收；不能以“G17帧能解码”证明64B固件块可传输。末块豁免须另有裁定与独立用例。

G17-Q（78B）：

```text
55 AA 01 02 05 21 04 00 03 00 40 00 00 00 00 00
38 00 9E 83 00 01 02 03 04 05 06 07 08 09 0A 0B
0C 0D 0E 0F 10 11 12 13 14 15 16 17 18 19 1A 1B
1C 1D 1E 1F 20 21 22 23 24 25 26 27 28 29 2A 2B
2C 2D 2E 2F 30 31 32 33 34 35 36 37 9D 4B
```

G18-Q（79B）：

```text
55 AA 01 02 05 21 04 00 03 00 41 00 00 00 00 00
39 00 B0 88 00 01 02 03 04 05 06 07 08 09 0A 0B
0C 0D 0E 0F 10 11 12 13 14 15 16 17 18 19 1A 1B
1C 1D 1E 1F 20 21 22 23 24 25 26 27 28 29 2A 2B
2C 2D 2E 2F 30 31 32 33 34 35 36 37 38 64 A3
```

G19：L=1025（LE `01 04`）、chunk=1017，完整1039B固定过长输入如下，CRC按数学参数计算有效但**不使帧合法**。规范 §6 在头部收全即因L>1024拒收、err_mtu增加，不等待/缓存1025B、不分发、不擦写，预期响应为空串；不能凭错误表存在 ERR_MTU_EXCEEDED=0x02 就擅加线上 NACK。流式和整帧接口分别检验；随后按已接受超时/重新同步规则输入 G01-Q，应恢复正常。

G19-Q（1039B）：

```text
55 AA 01 02 05 21 04 00 03 00 01 04 00 00 00 00
F9 03 29 AC 00 01 02 03 04 05 06 07 08 09 0A 0B
0C 0D 0E 0F 10 11 12 13 14 15 16 17 18 19 1A 1B
1C 1D 1E 1F 20 21 22 23 24 25 26 27 28 29 2A 2B
2C 2D 2E 2F 30 31 32 33 34 35 36 37 38 39 3A 3B
3C 3D 3E 3F 40 41 42 43 44 45 46 47 48 49 4A 4B
4C 4D 4E 4F 50 51 52 53 54 55 56 57 58 59 5A 5B
5C 5D 5E 5F 60 61 62 63 64 65 66 67 68 69 6A 6B
6C 6D 6E 6F 70 71 72 73 74 75 76 77 78 79 7A 7B
7C 7D 7E 7F 80 81 82 83 84 85 86 87 88 89 8A 8B
8C 8D 8E 8F 90 91 92 93 94 95 96 97 98 99 9A 9B
9C 9D 9E 9F A0 A1 A2 A3 A4 A5 A6 A7 A8 A9 AA AB
AC AD AE AF B0 B1 B2 B3 B4 B5 B6 B7 B8 B9 BA BB
BC BD BE BF C0 C1 C2 C3 C4 C5 C6 C7 C8 C9 CA CB
CC CD CE CF D0 D1 D2 D3 D4 D5 D6 D7 D8 D9 DA DB
DC DD DE DF E0 E1 E2 E3 E4 E5 E6 E7 E8 E9 EA EB
EC ED EE EF F0 F1 F2 F3 F4 F5 F6 F7 F8 F9 FA FB
FC FD FE FF 00 01 02 03 04 05 06 07 08 09 0A 0B
0C 0D 0E 0F 10 11 12 13 14 15 16 17 18 19 1A 1B
1C 1D 1E 1F 20 21 22 23 24 25 26 27 28 29 2A 2B
2C 2D 2E 2F 30 31 32 33 34 35 36 37 38 39 3A 3B
3C 3D 3E 3F 40 41 42 43 44 45 46 47 48 49 4A 4B
4C 4D 4E 4F 50 51 52 53 54 55 56 57 58 59 5A 5B
5C 5D 5E 5F 60 61 62 63 64 65 66 67 68 69 6A 6B
6C 6D 6E 6F 70 71 72 73 74 75 76 77 78 79 7A 7B
7C 7D 7E 7F 80 81 82 83 84 85 86 87 88 89 8A 8B
8C 8D 8E 8F 90 91 92 93 94 95 96 97 98 99 9A 9B
9C 9D 9E 9F A0 A1 A2 A3 A4 A5 A6 A7 A8 A9 AA AB
AC AD AE AF B0 B1 B2 B3 B4 B5 B6 B7 B8 B9 BA BB
BC BD BE BF C0 C1 C2 C3 C4 C5 C6 C7 C8 C9 CA CB
CC CD CE CF D0 D1 D2 D3 D4 D5 D6 D7 D8 D9 DA DB
DC DD DE DF E0 E1 E2 E3 E4 E5 E6 E7 E8 E9 EA EB
EC ED EE EF F0 F1 F2 F3 F4 F5 F6 F7 F8 F9 FA FB
FC FD FE FF 00 01 02 03 04 05 06 07 08 09 0A 0B
0C 0D 0E 0F 10 11 12 13 14 15 16 17 18 19 1A 1B
1C 1D 1E 1F 20 21 22 23 24 25 26 27 28 29 2A 2B
2C 2D 2E 2F 30 31 32 33 34 35 36 37 38 39 3A 3B
3C 3D 3E 3F 40 41 42 43 44 45 46 47 48 49 4A 4B
4C 4D 4E 4F 50 51 52 53 54 55 56 57 58 59 5A 5B
5C 5D 5E 5F 60 61 62 63 64 65 66 67 68 69 6A 6B
6C 6D 6E 6F 70 71 72 73 74 75 76 77 78 79 7A 7B
7C 7D 7E 7F 80 81 82 83 84 85 86 87 88 89 8A 8B
8C 8D 8E 8F 90 91 92 93 94 95 96 97 98 99 9A 9B
9C 9D 9E 9F A0 A1 A2 A3 A4 A5 A6 A7 A8 A9 AA AB
AC AD AE AF B0 B1 B2 B3 B4 B5 B6 B7 B8 B9 BA BB
BC BD BE BF C0 C1 C2 C3 C4 C5 C6 C7 C8 C9 CA CB
CC CD CE CF D0 D1 D2 D3 D4 D5 D6 D7 D8 D9 DA DB
DC DD DE DF E0 E1 E2 E3 E4 E5 E6 E7 E8 E9 EA EB
EC ED EE EF F0 F1 F2 F3 F4 F5 F6 F7 F8 F9 FA FB
FC FD FE FF 00 01 02 03 04 05 06 07 08 09 0A 0B
0C 0D 0E 0F 10 11 12 13 14 15 16 17 18 19 1A 1B
1C 1D 1E 1F 20 21 22 23 24 25 26 27 28 29 2A 2B
2C 2D 2E 2F 30 31 32 33 34 35 36 37 38 39 3A 3B
3C 3D 3E 3F 40 41 42 43 44 45 46 47 48 49 4A 4B
4C 4D 4E 4F 50 51 52 53 54 55 56 57 58 59 5A 5B
5C 5D 5E 5F 60 61 62 63 64 65 66 67 68 69 6A 6B
6C 6D 6E 6F 70 71 72 73 74 75 76 77 78 79 7A 7B
7C 7D 7E 7F 80 81 82 83 84 85 86 87 88 89 8A 8B
8C 8D 8E 8F 90 91 92 93 94 95 96 97 98 99 9A 9B
9C 9D 9E 9F A0 A1 A2 A3 A4 A5 A6 A7 A8 A9 AA AB
AC AD AE AF B0 B1 B2 B3 B4 B5 B6 B7 B8 B9 BA BB
BC BD BE BF C0 C1 C2 C3 C4 C5 C6 C7 C8 C9 CA CB
CC CD CE CF D0 D1 D2 D3 D4 D5 D6 D7 D8 D9 DA DB
DC DD DE DF E0 E1 E2 E3 E4 E5 E6 E7 E8 E9 EA EB
EC ED EE EF F0 F1 F2 F3 F4 F5 F6 F7 F8 B0 95
```


### 8.6 Flags、外层CRC与伪响应

G20：GET_VERSION 的 Flags=0x01，缺版本位，外层CRC正确；按 §1.4 硬拒绝，不分发，响应空串。

G20-Q（14B）：

```text
55 AA 01 02 01 01 04 00 00 00 00 00 94 11
```

G21：急停广播错误置WANTS_ACK（Flags=0x15），外层CRC正确；不得产生任何即时 ACK 风暴，也不得按 MOTION_MOVE 分发。非法急停是否仍执行安全锁停须 ARCH/STATE 明确，本候选仅冻结“无即时响应、不运动、不当普通可靠请求”三个安全断言。

G21-Q（16B）：

```text
55 AA 01 FF 15 12 04 00 00 00 02 00 01 00 87 73
```

G22：G01-Q 仅改CRC低字节F9→F8；CRC坏，按 §6 静默丢弃、err_crc增加，预期响应空串。发送侧有界超时报错，不把诊断用 ERR_CRC=0x01 当必须线缆 NACK。

G22-Q（14B）：

```text
55 AA 01 02 05 01 04 00 00 00 00 00 F8 1E
```

G23：G03-Q 的未决事务收到 cmd=0x05 的“伪 ACK”完整帧；即使SRC/DST/seq、响应Flags及CRC都匹配，也不得把它当规范 cmd=0x00 ACK，pending不能推进、不能启动升级。按最终裁定的扩展/未知响应规则记录并有界超时；不向响应再回 NACK制造循环。规范正例回复仍为 G03-R。

G23-R（18B）：

```text
55 AA 02 01 06 05 04 00 01 00 04 00 20 02 00 00
BC CA
```


## 9. 协议冲突与 MAX_PAYLOAD_SIZE 专项正/负例回归判据

本节与 D03/D04/D07、N01～N05、H03～H05 关联，原软件/HIL、U盘、16KB/236KB及说明书范围全部保留。以下是统一契约裁定后的必测计划，**本轮全部未执行**。静态规范核对与软件用例先行，HIL随后在受控授权窗口用真实合法制品执行；I64/I1016 仅作软件编解码/Flash模型输入，不刷入真机。

### 9.1 0x10 / 0x12 语义隔离与混版本阻断

| 编号 | 正/负例与前提 | 通过/拒绝判据 |
| --- | --- | --- |
| C01 系统控制正例 | 按最终裁定的主规范语义，G03-Q→G03-R；分别覆盖 MC App、TH App 中实际支持的入口 | 仅命中 action/delay 系统控制；温控设置、Marlin移动/队列和其他业务副作用均0；Boot实际启动另核身份。受控模型测试 Noop/Reboot/Jump及非法action，真实操作另授权 |
| C02 温控旧义负例 | G10-Q 及4B旧温控中前3B可恰好解释成合法action/delay的变体，输入统一契约端；新系统控制3B输入旧温控端的软件夹具，方向对换 | **先验完整长度/契约身份，再读取任何业务字段**。不能截4B为3B、给3B补零为4B、按温度数值“猜协议”；无温控、复位、跳Boot或移动副作用，无成功ACK；混版本发送端须在业务发送前阻断 |
| C03 急停正例 | G04 的2B广播、Flags=0x14，按裁定急停定义消费与转发 | 进入安全锁停/KILLED、清队列、加热及驱动去能，不产生任何运动；无即时ACK，Hop/Route/CRC/水平分割正确。软件状态断言与真实安全测量分别出证 |
| C04 运动旧义负例 | G11-Q，及16B旧move改成广播/priority的CRC有效变体；G04输入旧move分发的软件夹具 | 不能以0x12同码受理错误语义；全长/方向/Flags不符按冻结错误策略拒绝，旧move不得被截成2B reason触发急停，规范急停不得补零/读越界变运动；不能仅因该错误负例“未运动”省略C03 |
| C05 长度精确性 | 0x10的L=0/2/3/4/5；0x12的L=0/1/2/3/16；CRC均有效并控制seq/模式 | 只接受最终契约规定的精确长度/方向；空载旧V04、任何额外尾字节/前缀合法长度伪装不得自动放行。若主规范裁定修改空载急停，须明确替代关系并重写受影响向量，不能两个预期随意切换 |
| C06 Flags与方向 | G20/G21；请求误置IS_RESPONSE、响应误置WANTS_ACK、错误版本/保留位；请求与响应地址互换/错误DST | 非法输入不触业务副作用；广播不造即时并发ACK。0x01/0x02不能按“查询MC/查询TH”分配，目标由DST、回复由SRC区分；无方向/模式权限的同码不得受理 |
| C07 伪响应/旧事务 | G23-R，错cmd/长度/错误码/seq/节点/boot_id回复、上一代延迟ACK、同seq异内容重发 | 仅最终契约允许的对应终态响应推进事务；0x05扩展不自动等于0x00 ACK；STATUS、VERSION_REPORT、NACK不得被泛化成成功。pending有界等待/错误传播；过期/歧义/窗口异常按规范错误表，不重复擦写或加进度 |
| C08 混版本准入 | 新AP+旧MC/TH、新MC+旧TH、旧AP+新MC/TH；App/Boot不同组合以及切换后旧应答 | 仅“帧头55AA、版本位0x04、proto=2.0”不足以证明同一语义契约。ARCH须明确可验证的契约身份/能力组合/发布映射及不兼容检测与拒绝时点；未证明兼容前禁止危险控制和OTA，不允许按长度、响应超时或观察到动作自动降级/试探。不能由QA私占保留位/扩16B版本响应 |
| C09 中继与本机消费 | TH目标的0x10/0x12及OTA经MC App；本机与广播路径分别验证 | 非本机单播业务字节不得因MC自己的命令定义被消费/改写；只处理帧级Hop/Route/CRC。TH源回复不能由MC合成；广播本机消费仍须按准确契约，MCBoot不承担TH路由 |

若统一裁定保留业务扩展，新增温控/运动的最终命令及载荷也须各有完整正向字节与响应，且与上述旧/新交叉负例成对；当前不能未经影响分析机械改号，亦不能让同一未区分会话在0x10/0x12同时接受两种语义。双方行为“碰巧可互通”但不符合裁定的版本，仍属符合性失败。任何无法区分且同码同布局异义的组合都必须由准入/迁移策略排除，不能承诺靠解析器猜测安全兼容。

### 9.2 共同 MTU、块长与长度/内存安全

主规范帧载荷上限1024B；当前AP1024B、MC/TH64B。必须同时区分三层限制：**物理帧L上限、OTA_DATA的8B头后可用固件字节、目标分区净镜像上限**。64B帧最多承载56B固件数据，低于主规范常规最小64B；64B固件块需要L=72/总长86B，512B块需要L=520/总长534B，1016B块需要L=1024/总长1038B。236KB是净镜像容量，不是单帧MTU。

| 编号 | 正/负边界 | 通过/拒绝及恢复判据 |
| --- | --- | --- |
| M01 三端/模式与缓冲静态一致 | AP、MC App本机/路由、MCBoot、TH App/Boot，含RX/DMA/环形/中继发送池/栈及codec边界 | 各段实际容量均≥最终选定L+14与必要在途开销，声明与消费一致；能力子集/模式拒绝显式登记。不能只改宏、只扩AP、静默取MIN(1024,64)或以64B帧替代64B数据块 |
| M02 当前64B断点 | G17 L64/56B、G18 L65/57B；另列帧级L63/64/65及L71/72/73 | 先分帧合法性与命令合法性。G17不是常规OTA正例；当前64B端应安全拒绝超限，但该拒绝不抵消它无法传G06的符合性缺口。共同契约确定后按其准确上限重定正负结果，不削小块长使旧端“通过” |
| M03 最小常规块 | G06 L72/chunk64，offset0及跨页/扇区边界；不足64的非末块 | 合法64B须完整保留包括末字节且双CRC相符，持久写入后才按冻结语义确认；非末块56/57/63等不能因外帧≤MTU而受理。末块1/2/3/63B的允许范围/填充/CRC须先裁定，再配独立向量，不自创例外 |
| M04 最大及所选最大块 | G16 L1024/chunk1016；若最终采用512B则另覆盖L520；L1023/1024/1025及所选上限±1 | 帧层/支持的块大小层分别判定。G16作为规范帧容量正例，只有支持该MTU的目标才是OTA端到端正例；缩小功能子集需显式接受，不能宣称完整1024B支持。G19超限头立即拒绝，禁止截成1024/64、绕回小长度或写越界 |
| M05 帧长与字段自洽 | 声明L≠实际物理长度、L<8的DATA、chunk_bytes≠L-8、L=0xFFFF、chunk=0/1017/0xFFFF、附加字节 | 先核长度、再核CRC/内块/业务，再产生副作用；不读不足字段，不将尾部CRC当固件数据，不把尾字节另作成功帧。流式先收帧与整帧decode对额外数据的边界各按接口契约验证 |
| M06 算术/目标越界 | offset=fw_size、offset=0xFFFFFFF0并加64、offset+chunk跨size/分区末端、目标地址加法溢出，TH241663/241664/241665及240KB旧包 | 宽度/溢出检查在擦写前，错误定位明确。G13=241665负例必须零擦除，合法236KB与末字节正例成对；不写Boot、间隙或锚点。净荷与128B Trailer按S03分别计长，不能以包总长误判净荷 |
| M07 不截断、不溢出 | 完整G06/G16/G19经逐字节/随机分片/粘包输入，至少两帧连续、DMA仍在途时复用接收缓冲 | 收发有效长度、CRC、最后数据字节、offset及Flash回读一致；拒绝任何“只取前64B/1024B仍ACK”。软件层用边界哨兵/适用内存检查、DMA所有权观察验证，不仅看进程未崩溃 |
| M08 拒绝后恢复 | 只发12B超限头、超长/截断/内含55AA、字节间超过50ms，随后正常G01/G06 | 超限头即拒收且内存状态完整；超时先检查再刷新、恢复同步，不忙轮询、不死锁/混入旧残帧。CRC错静默+计数、发送侧有界超时；帧拒收没有ACK不能误报升级成功 |

### 9.3 正式采用前的缺口及收件条件

| 缺口/当前状态 | 解除条件与责任 |
| --- | --- |
| 尚无唯一版本化契约与命令迁移结论；指定扩展设计文件未找到 | ARCH取得真实扩展/修复接受来源，联合相关Owner裁定0x10/0x12、0x05/0x00/0x06、主规范旧V04、方向/Flags/布局/错误、MTU/分块、兼容身份及迁移；纳入同一完整方案供用户确认，不新增逐端用户审批 |
| START/Trailer、安全准入、缓存/写Flash/生效ACK仍未定型 | 沿用§3.1/§6.4要求；候选向量的预置状态只能用于软件字段核对，不能授权真实擦除、改变分区或补造元数据传输接口 |
| 内块CRC错误映射、非法急停回复、失败expected_seq与末块策略尚待裁定 | Owner在唯一契约显式落字；QA依据裁定更新相关固定字节及状态断言，不能凭本文候选直接冻结 |
| 固定向量/工具尚无非作者接受，无任何执行证据 | 本文含字节也是QA作者预期，必须由未参与作者工作的独立Codex承担ARCH检查；后续准确服务器候选、工具/计划与哈希锁定后，由受控Docker Runner执行软件验证、受控HIL采证，再由独立Codex只读审阅 |
| 本轮仅完成文档与源码来源核对 | 不修改检查器/业务仓/其他文件、不创建实现任务、不运行任何测试/硬件操作；历史接受/冻结保留，全部运行项仍未执行 |

交付结论为 **revision 2 补充规划输入已形成，统一契约/预期仍待裁定与非作者独立接受**。本文件不签发规范符合性、软件、HIL或整机 APPROVED，也不表示可以进入实现拆分或开发。

