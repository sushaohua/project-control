---
name: arch-deep-spec
description: "本项目 ARCH 技术架构技能：与 PM 往返核对产品目标的可行性，结合 graphify AST、单一协议契约、Design-It-Twice 接缝比选及 Diff Budget，将目标落实为同一份可执行、可验证的实施方案。"
---

# ARCH 深度架构拆解与垂直切片规范 (`arch-deep-spec`)

本技能用于 `ARCH` 在 **Phase 1（实施方案先行）** 产出穿透式、零漏链的跨仓垂直切片执行方案。**未经用户明确批准（Human Gate #1），严禁修改任何业务代码**。

## 产品目标输入与可行性往返

采用流程：用户表达想法 → [PM 整理需求](../product-requirements/SKILL.md) ↔ ARCH 核对可行性 → 合成一份方案 → 用户批准 → COORD 组织实施。

- 先读本任务方案中的产品目标、范围、用户流程及完成条件；有关键技术未知时提前参与，不要求 PM 先给出完整技术规格或保证可实现。
- 对照当前源码/图谱、协议、SDK 和资源核实已有能力、缺口、依赖与风险，明确现阶段可实施、须先验证的前提或当前条件下不能承诺的部分，给出依据和可选的阶段范围。
- 技术事实和一般实现选择由 ARCH 处理；影响产品结果的歧义、范围缩减和优先级取舍反馈 PM，由 PM 统一与用户沟通，不将技术提议当作用户决定。
- 用户目标已明确的小修或技术维护可沿既有授权进入设计，不强制经过 PM。已有产品决定不反复确认。
- PM 主责同一方案的产品定义，ARCH 主责技术设计，按章节串行交接；技术方案逐项对应目标和验收场景，不另立第二份目标真源。
- 接口不仅说明参数和返回值，还要明确调用前提、资源所有者、时序、错误与超时等真实约束；优先复用现有调用链，在关键接缝比较不同设计，不堆叠无真实调用点的抽象。
- 实施切片列出精确文件、Consumes/Produces 签名、依赖、修改预算、验收命令及 Pass Criteria；自检目标覆盖、跨任务接口一致性和异常路径，未实现的设计接口明确标注。
- 产品与技术内容合成后复用一次方案审批，再交 COORD 组织实施，不新增固定的 PM/ARCH 双重审批；复杂度不应使方案退化为实现代码逐行转录。

## 强制四步拆解流水线

### 1. `graphify` AST 物理取证（消灭凭印象派单）
- 对涉及的每个业务仓（`printer-soc`、`mcu-p3`、`boot/*`、`test_harness`）优先查询本地 `graphify-out/` 图谱：
  ```bash
  (cd printer-soc && ~/.local/bin/graphify path "<入口符号>" "<串口收发符号>")
  (cd mcu-p3 && ~/.local/bin/graphify explain "<目标模块或中断函数>")
  ```
- 方案中必须输出 **《端到端真实符号调用链与现状断点核实表》**，列明精确 `仓:文件路径:函数名` 与 `EXTRACTED` 调用边；无法核实的外部硬件事实必须显式标注 `[UNVERIFIED]`。

### 2. 复杂接缝 `Design-It-Twice` 与单一机器契约源锁定
- 凡涉及跨芯片状态同步、串口吞吐流控、Bootloader 擦写跳转或异常恢复的接缝，先用 5～8 行简要对比至少两种完全不同的边界设计（窄接口深模块优先），说明取舍依据。
- 涉及 MiniMCProto v2 协议变更时，必须先更新唯一真源 `project-control/contracts/minimc_v2_contract.yaml` 与黄金字节向量，严禁让各端手抄 Markdown 表格。

### 3. 软硬件契约推演与最小修改预算（Diff Budget）
- 显式推演：波特率/吞吐、指令-ACK 超时预算、中断优先级、RAM 静态缓冲上限（零堆分配）及 Flash 分区/VTOR（MC App `0x08020000`，TH App `0x08004000`）。
- 为每个切片子任务设定刚性 **`diff_budget`**（`max_files` 上限，以及存量模块如 `Marlin_main.c` 的 `protected_globs` 与 `max_protected_lines` 最小改动红线）。

### 4. 单一真相源（SSoT）原地迭代与垂直切片定义
- 初次创建命名：`project-control/docs/planning/{task_summary}_implementationplan_{YYYYMMDD_HHMMSS}.md`；同任务后续讨论评审**强制原地更新**，严禁新建碎片草稿。
- 方案头部必须维护**实名修订履历表**，修订人显式写明具体 AI 客户端/引擎实体（如 `AI (Antigravity-CLI)`），禁填模糊 `"AI"`。
- 按窄纵向业务链拆解为拓扑有序的 `project-control/slices/SLICE-XX.yaml`（严禁拆出纯局部接口或空钩子横向微票），每个切片列明 `Consumes/Produces` 签名、正负配对验收判据与回滚预案。

## C308L 平台输入取证

应用主线为 printer-soc，平台为 sdk/c308l。SDK 的 AST 只覆盖实际可解析源码；Makefile、设备树、工具链、预编译库和 manifest 派生规则另外做依赖取证。图谱必须绑定当前候选，旧 soc-ap 图谱不能代签新仓。逐 project 登记 Owner、源提交、分支与写路径，Helix归ENG-AP，平台实现归ENG-PLATFORM；禁止横向微票或整个SDK递归写权。
