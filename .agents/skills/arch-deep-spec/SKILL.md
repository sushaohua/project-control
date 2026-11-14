---
name: arch-deep-spec
description: "AI SoC V2 ARCH 角色专属深度拆解技能：强制结合本地 graphify AST 图谱取证、单一协议契约源 (contracts/*.yaml)、Design-It-Twice 接缝比选与两阶段 SSoT 垂直切片方案编写（含实名修订履历与 Diff Budget）。"
---

# ARCH 深度架构拆解与垂直切片规范 (`arch-deep-spec`)

本技能用于 `ARCH` 在 **Phase 1（实施方案先行）** 产出穿透式、零漏链的跨仓垂直切片执行方案。**未经用户明确批准（Human Gate #1），严禁修改任何业务代码**。

## 强制四步拆解流水线

### 1. `graphify` AST 物理取证（消灭凭印象派单）
- 对涉及的每个业务仓（`soc-ap`、`mcu-p3`、`boot/*`、`test_harness`）优先查询本地 `graphify-out/` 图谱：
  ```bash
  (cd soc-ap && ~/.local/bin/graphify path "<入口符号>" "<串口收发符号>")
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
