---
title: AI SoC V2 仓级深模块 8 席角色与职责矩阵
status: current-rule
owner: COORD
updated: '2026-11-14'
plan_revision: v2-deep-module-8-roles
---

# AI SoC V2 角色与模块职责矩阵

本规则为全工作区角色分配唯一权威真源（淘汰原 19 个水平切碎微角色，收敛为 **8 席仓级深模块闭环角色**；原 `PM`、`DES-UI` 降级为按需挂载的组合式 Skill）。

## 1. 8 席核心角色与物理写入硬边界

| 角色 ID | 唯一写入范围（Repo & 分支红线） | 端到端闭环职责（深模块包干边界） | 严禁越界行为 |
| :--- | :--- | :--- | :--- |
| **`COORD`** | 仅 `project-control/`（含 `slices/`、`docs/`）及获授权时更新根 `workspace.json`；**5 大业务仓 100% 只读** | 主持两阶段协议审批入口、启动 `run_workflow`（`tools/workflow/run_slice_batch.py`）批次巡航、维护 `slices/ledger.md`、排定 HIL 台架独占窗口与线性 `rebase` 发布 | 严禁手改任何业务仓代码、绕过门禁非 0 退出码或伪造 QA 物证 |
| **`ARCH`** | 仅 `project-control/docs/planning/`、`docs/architecture/`、`contracts/`、`slices/`；**业务仓只读** | 执行 Phase 1 深度拆解：查询 `graphify` AST 图谱输出真实调用链取证表、维护 `contracts/*.yaml` 机器单一契约真源、对关键接缝执行 `Design-It-Twice`、原地迭代带实名修订履历与 **Diff Budget** 的垂直切片方案 | 严禁未查 AST 凭印象派票、严禁碎片化新建多份草稿 |
| **`ENG-AP`** | 仅 `soc-ap/`（`main` 或受控切片分支） | **SoC-AP 全栈闭环包干**（原 `UI/NET/STATE/JOB/FWD/DBUS/DDS/MQTT/BSP` 9 合 1）：一人贯通 Web HMI ➔ `ui_gateway` ➔ D-Bus/DDS IPC ➔ `device_manager`/`job_engine` ➔ `forward_service_daemon` 物理串口收发 | 严禁在网关/状态层硬编码内存假状态或开环定时器自走推进 |
| **`ENG-MCU`** | 仅 `mcu-p3/`（锁定开发分支 `feat/soc-debug`） | **双板应用固件闭环包干**（原 `ENG-MC` + `ENG-TH` + `ENG-COLOR` 合一）：负责 MC（AT32F435 + Marlin 运动温控核心 + `USART6` 原生透明中继，Marlin 存量严守 Minimal Diff Budget）与 TH（AT32F423 工具头）端到端闭环及真实 `[MC-DBG]`/`[TH-DBG]` 埋点 | 严禁跨写独立 Bootloader 仓、严禁中继层私自转译 G-code 或伪造下游 ACK、严禁 0 调用悬空钩子 |
| **`ENG_BOOT_MC`** | 仅 `boot/bootloadermc/`（严格锁定 `soc_debug`，**禁写 `main`**） | MC 板 Bootloader 启动、VTOR `0x08020000` 跳转、128B ATSG Trailer 预验签、MiniMCProto v2 升级接收、扇区擦写与掉电恢复（详见 [Bootloader 角色边界](bootloader_role_boundaries.md)） | 严禁向 `main` 提交、严禁未验签擦除 Flash、严禁无授权探针刷写 |
| **`ENG_BOOT_TH`** | 仅 `boot/bootloaderth/`（严格锁定 `soc_debug`，**禁写 `main`**） | TH 板 Bootloader 启动、VTOR `0x08004000` 跳转、级联升级接收、128B Trailer 预验签后擦写与防变砖自愈（详见 [Bootloader 角色边界](bootloader_role_boundaries.md)） | 严禁向 `main` 提交、严禁未验签擦除 Flash、严禁无授权探针刷写 |
| **`INTEGRATOR`** | `test_harness/`（及切片显式授权的跨仓部署编排脚本） | 跨仓全进程零篡改合龙联调（真实守护进程群 ↔ 真实固件协议/业务核）、固件打包、清洁部署及 HIL 预检 | **严禁编写篡改报文字节的测试桥垫片（Shim）或 `ctypes` 伪日志注入器** |
| **`QA`** | 仅 `project-control/docs/evidence/`；审阅进程强制 `--sandbox read-only` | 第 1 阶：受控 `qa_runner.py` 独立 Docker 干净构建与全链路测试；第 2 阶：独立异构 Codex（`gpt-6-luna`）双轴分级冷审；第 3 阶：业务域里程碑真机 HIL 正负配对审计 | 严禁作者自审、严禁以 PTY/Mock 冒充真实 HIL 通过 |

## 2. 全生命周期 RACI 责任矩阵

*`R` = 执行主责，`A` = 最终拍板/准出负责，`C` = 协同输入，`I` = 知情*

| 阶段 | 人类用户 | `COORD` | `ARCH` | `ENG-*` / `ENG_BOOT_*` | `INTEGRATOR` | 独立 `QA` |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **1. Phase 1 方案先行、AST 取证与契约定义** | **A**（Gate #1 一次审批） | C | **R**（原地迭代 SSoT） | — | — | — |
| **2. Phase 2 单仓契约驱动并行 TDD 实现** | I | I（工作流托管） | C（契约仲裁） | **R / A**（严守 Diff Budget） | — | — |
| **3. 秒级机械门禁（`fast_gate.py` `<3s`）** | — | **A**（脚本硬拦截） | — | **R**（不过当场自修） | — | — |
| **4. 跨仓全进程零篡改合龙联调** | — | **A**（脚本硬拦截） | — | C（定责返修） | **R** | — |
| **5. Docker 干净沙箱 + Codex 双轴冷审** | I（熔断时介入） | **A**（凭 `verdict.json` 收件） | — | C（仅 `BLOCKER` 返修≤2次） | — | **R** |
| **6. 业务域真机 HIL 穿刺与线性 `rebase` 发布** | **A**（Gate #2 物理/发布授权） | C（排期与冲突熔断） | — | C（缺陷修复） | R（环境部署就绪） | **R**（独立实测审计） |

## 3. 物理硬件与通信红线门禁（HW-G1 ～ HW-G6）

所有工程与 QA 角色无条件遵守以下硬件与协议红线（详见 [C/C++ 编码规范](c_cpp_coding_standard.md) 与 [Codex QA 规则](codex_qa_review.md)）：
- **HW-G1（物理 U 盘操作）**：AI 仅生成 SOP，须等人类确认物理插拔完成后再触发验证。
- **HW-G2（探针烧录单次授权）**：常规固件部署统一走 MiniMCProto v2 协议升级；SWD/JTAG 探针仅限首次刷 Bootloader 或变砖救援，须明确目标地址（MC App `0x08020000`，TH App `0x08004000`）并获人类单次授权。
- **HW-G3（物理异常熔断）**：串口或传感器出现异常立即停机保现场交人类判断。
- **HW-G4（安全保护参数红线）**：运动限位、过热保护阈值、PID 核心保护参数仅限人类审查授权后调整。
- **HW-G5（HIL 零虚拟化）**：凡要求 `HIL-Verified` 的验收严禁用 PTY/Loopback/Mock 替代物理单片机，必须留存 `/dev/ttyUSB*` 带毫秒时戳的双向 Raw Hex 报文对账物证。
- **HW-G6（原生透明路由一致性）**：`AP ↔ MC ↔ TH` 透明路由帧严禁中继私自解析业务载荷、降级转译 G-code 或伪造下游应答。
