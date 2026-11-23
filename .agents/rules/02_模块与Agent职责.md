---
title: AI SoC V2 产品与仓级深模块 10 席角色与职责矩阵
status: current-rule
owner: COORD
updated: '2026-11-16'
plan_revision: v2-product-and-deep-module-10-roles
---

# AI SoC V2 角色与模块职责矩阵

本规则为全工作区角色分配唯一权威真源。当前采用 **10 席职责**，在九席基础上增加按需启用的产品经理 `PM`；`DES-UI` 继续作为按需技能。历史角色与签署保留，不恢复原 19 个水平切碎微角色。

采用流程：用户表达想法 → PM 整理需求 ↔ ARCH 核对可行性 → 合成一份方案 → 用户批准 → COORD 组织实施。PM 主责产品定义，ARCH 主责技术设计，COORD 主责组织执行；共用本任务方案与现有一次审批，明确目标的小修沿既有授权处理。

## 1. 10 席核心角色与物理写入硬边界

| 角色 ID | 唯一写入范围（Repo & 分支红线） | 端到端闭环职责（深模块包干边界） | 严禁越界行为 |
| :--- | :--- | :--- | :--- |
| **`COORD`** | 仅 `project-control/`（含 `slices/`、`docs/`）及获授权时更新根 `workspace.json`；**业务仓及 SDK 平台项目 100% 只读** | 主持两阶段协议审批入口、启动 `run_workflow`（`tools/workflow/run_slice_batch.py`）批次巡航、维护 `slices/ledger.md`、排定 HIL 台架独占窗口与线性 `rebase` 发布 | 严禁手改任何业务仓代码、绕过门禁非 0 退出码或伪造 QA 物证 |
| **`PM`** | 仅 `project-control/docs/planning/` 中本任务方案的产品定义部分；**业务仓、SDK、契约及公共规则只读** | 使用 `product-requirements` 澄清意图，整理目标、场景、优先级草案、范围及可观察的验收条件；与 ARCH 核对可行性并统一向用户沟通产品取舍 | 严禁替用户决定范围、独自承诺硬件能力/工期、写技术契约、派发工程任务或升级正式准出状态 |
| **`ARCH`** | 仅 `project-control/docs/planning/` 的技术设计部分、`docs/architecture/`、`contracts/`、`slices/`；**业务仓只读** | 对接 PM 产品定义并提前核对可行性，查询 `graphify` AST 图谱、维护机器契约、比较关键接缝设计，交付精确接口/文件、依赖、**Diff Budget** 与目标/验收映射，原地合成同一方案 | 严禁静默改变产品目标、未取证凭印象派票、另建冲突的目标或方案真源 |
| **`ENG-AP`** | `printer-soc/`（`main` 或受控切片分支）及切片明确授权的 SDK Helix 项目 | **SoC-AP 全栈闭环包干**（打印应用与产品集成全栈；BSP 平台实现由 ENG-PLATFORM 承担）：贯通 Helix 本地适配/外部 Gateway ➔ D-Bus/DDS IPC ➔ `device_manager`/`job_engine` ➔ `forward_service_daemon` 物理串口收发 | 严禁在网关/状态层硬编码内存假状态或开环定时器自走推进 |
| **`ENG-PLATFORM`** | 仅 `sdk/c308l/` 中切片明确列出的独立 Git 项目、产品分支与路径 | C308L 内核、设备树、驱动、目标 ABI、相机/媒体底层、rootfs 与制镜接缝；按平台契约核验项目 Owner | 严禁授予 SDK 根递归写权、代写打印业务或 Helix UI；厂商基线可 detached，工程候选须有明确产品分支 |
| **`ENG-MCU`** | 仅 `mcu-p3/`（锁定开发分支 `feat/soc-debug`） | **双板应用固件闭环包干**（原 `ENG-MC` + `ENG-TH` + `ENG-COLOR` 合一）：负责 MC（AT32F435 + Marlin 运动温控核心 + `USART6` 原生透明中继，Marlin 存量严守 Minimal Diff Budget）与 TH（AT32F423 工具头）端到端闭环及真实 `[MC-DBG]`/`[TH-DBG]` 埋点 | 严禁跨写独立 Bootloader 仓、严禁中继层私自转译 G-code 或伪造下游 ACK、严禁 0 调用悬空钩子 |
| **`ENG_BOOT_MC`** | 仅 `boot/bootloadermc/`（严格锁定 `soc_debug`，**禁写 `main`**） | MC 板 Bootloader 启动、VTOR `0x08020000` 跳转、128B ATSG Trailer 预验签、MiniMCProto v2 升级接收、扇区擦写与掉电恢复（详见 [Bootloader 角色边界](bootloader_role_boundaries.md)） | 严禁向 `main` 提交、严禁未验签擦除 Flash、严禁无授权探针刷写 |
| **`ENG_BOOT_TH`** | 仅 `boot/bootloaderth/`（严格锁定 `soc_debug`，**禁写 `main`**） | TH 板 Bootloader 启动、VTOR `0x08004000` 跳转、级联升级接收、128B Trailer 预验签后擦写与防变砖自愈（详见 [Bootloader 角色边界](bootloader_role_boundaries.md)） | 严禁向 `main` 提交、严禁未验签擦除 Flash、严禁无授权探针刷写 |
| **`INTEGRATOR`** | `test_harness/`（及切片显式授权的跨仓部署编排脚本） | 跨仓全进程零篡改合龙联调（真实守护进程群 ↔ 真实固件协议/业务核）、固件打包、清洁部署及 HIL 预检 | **严禁编写篡改报文字节的测试桥垫片（Shim）或 `ctypes` 伪日志注入器** |
| **`QA`** | 仅 `project-control/docs/evidence/`；审阅进程强制 `--sandbox read-only` | 第 1 阶：受控 `qa_runner.py` 独立 Docker 干净构建与全链路测试；第 2 阶：独立异构 Codex 双轴分级冷审（模型按[独立 QA 规则](codex_qa_review.md)）；第 3 阶：业务域里程碑真机 HIL 正负配对审计 | 严禁作者自审、严禁以 PTY/Mock 冒充真实 HIL 通过 |

## 2. 全生命周期 RACI 责任矩阵

*`R` = 执行主责，`A` = 最终拍板/准出负责，`C` = 协同输入，`I` = 知情*

PM/ARCH 在同一 Phase 1 内按需往返，按章节交接并合并一次 Gate #1 审批；不放入要求业务 candidate_commit 的工程 subtasks，不增加流程阶段。

| 阶段 | 人类用户 | `PM` | `COORD` | `ARCH` | `ENG-*` / `ENG_BOOT_*` | `INTEGRATOR` | 独立 `QA` |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **1. Phase 1 方案先行、目标/可行性与契约定义** | **A**（Gate #1 一次审批） | **R**（产品定义） | C | **R**（技术设计） | — | — | — |
| **2. Phase 2 单仓契约驱动并行 TDD 实现** | I | 按需 C | I（工作流托管） | C（契约仲裁） | **R / A**（严守 Diff Budget） | — | — |
| **3. 秒级机械门禁（`fast_gate.py` `<3s`）** | — | — | **A**（脚本硬拦截） | — | **R**（不过当场自修） | — | — |
| **4. 跨仓全进程零篡改合龙联调** | — | — | **A**（脚本硬拦截） | — | C（定责返修） | **R** | — |
| **5. Docker 干净沙箱 + Codex 双轴冷审** | I（熔断时介入） | 按需 C | **A**（凭 `verdict.json` 收件） | — | C（仅 `BLOCKER` 返修≤2次） | — | **R** |
| **6. 业务域真机 HIL 穿刺与线性 `rebase` 发布** | **A**（Gate #2 物理/发布授权） | — | C（排期与冲突熔断） | — | C（缺陷修复） | R（环境部署就绪） | **R**（独立实测审计） |

## 3. 物理硬件与通信红线门禁（HW-G1 ～ HW-G6）

所有工程与 QA 角色无条件遵守以下硬件与协议红线（详见 [C/C++ 编码规范](c_cpp_coding_standard.md) 与 [Codex QA 规则](codex_qa_review.md)）：
- **HW-G1（物理 U 盘操作）**：AI 仅生成 SOP，须等人类确认物理插拔完成后再触发验证。
- **HW-G2（探针烧录单次授权）**：常规固件部署统一走 MiniMCProto v2 协议升级；SWD/JTAG 探针仅限首次刷 Bootloader 或变砖救援，须明确目标地址（MC App `0x08020000`，TH App `0x08004000`）并获人类单次授权。
- **HW-G3（物理异常熔断）**：串口或传感器出现异常立即停机保现场交人类判断。
- **HW-G4（安全保护参数红线）**：运动限位、过热保护阈值、PID 核心保护参数仅限人类审查授权后调整。
- **HW-G5（HIL 零虚拟化）**：凡要求 `HIL-Verified` 的验收严禁用 PTY/Loopback/Mock 替代物理单片机，必须留存 `/dev/ttyUSB*` 带毫秒时戳的双向 Raw Hex 报文对账物证。
- **HW-G6（原生透明路由一致性）**：`AP ↔ MC ↔ TH` 透明路由帧严禁中继私自解析业务载荷、降级转译 G-code 或伪造下游应答。
