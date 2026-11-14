---
name: slice-batch-orchestrator
description: "AI SoC V2 COORD 角色专属批次巡航编排技能：基于 run_workflow (run_slice_batch.py) 与 slices/ledger.md 执行垂直切片幂等续跑、稀疏四文件指针派单、四阶门禁拦截与 2 轮保活返修熔断。"
---

# COORD 垂直切片批次巡航编排技能 (`slice-batch-orchestrator`)

本技能约束 `COORD` 在 **Phase 2（获批后的有界执行）** 中高效编排跨仓研发闭环，彻底替代旧版 `coord_runner`。

## 核心执行铁律

1. **业务仓 100% 只读**：`COORD` 仅允许写入 `project-control/`（及获授权时更新 `workspace.json`），严禁直接手改 5 大业务仓源码。
2. **前置审批硬闸门（Human Gate #1）**：确认对应批次 SSoT 方案已获用户明确批准（`Approved` / `批准执行`），且 `project-control/slices/SLICE-XX.yaml` 与 `contracts/*.yaml` 已就位。
3. **启动代码化批次巡航**：
   - 使用内置 `run_workflow` 工具执行 `project-control/tools/workflow/run_slice_batch.py`：
     ```json
     {
       "ScriptPath": "/home/sushaohua/workspace/ai_soc_project/project-control/tools/workflow/run_slice_batch.py",
       "Description": "Cruise approved vertical slice batch",
       "Args": {
         "plan_path": "project-control/docs/planning/<approved_plan>.md",
         "slice_files": ["project-control/slices/SLICE-01.yaml", "project-control/slices/SLICE-02.yaml"]
       }
     }
     ```
   - 根工作区 `.gitignore` 忽略 7 个子仓，因此跨子仓并发工程 Agent 统一使用 `workspace="inherit"`（物理目录正交），由 `fast_gate.py` 强校验路径不越界。
4. **稀疏指针传参与幂等续跑**：
   - 每次派发子 Agent 仅传 4 个文件路径指针（SSoT 方案、本切片 YAML、契约真源、自检输出路径），禁止塞入历史对话长文。
   - 重跑前自动读取 `project-control/slices/ledger.md`，已标 `SW-Verified` / `HIL-Verified` 的切片毫秒级跳过。
5. **2 轮保活返修熔断与 Human Gate #2**：
   - `fast_gate.py`、跨仓合龙或独立 Codex 报 `BLOCKER` 时，在同一保活 `ENG-*` 会话内定向返修，**最多 2 轮**；第 3 次失败立即 Fail-Fast 停机升级人类。
   - 批次全部 `SW-Verified` 或触及 `requires_hil_immediately: true` / 远端 `publish` / `git rebase` 冲突时，立即停机请求 **Human Gate #2**。
