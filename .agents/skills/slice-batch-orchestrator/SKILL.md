---
name: slice-batch-orchestrator
description: "AI SoC V2 COORD 角色专属批次巡航编排技能：基于 run_workflow (run_slice_batch.py) 与 slices/ledger.md 执行垂直切片幂等续跑、稀疏四文件指针派单、四阶门禁拦截与 2 轮保活返修熔断。"
---

# COORD 垂直切片批次巡航编排技能 (`slice-batch-orchestrator`)

本技能约束 `COORD` 在 **Phase 2（获批后的有界执行）** 中高效编排跨仓研发闭环，彻底替代旧版 `coord_runner`。

## 规划到执行的交接

采用流程：用户表达想法 → PM 整理需求 ↔ ARCH 核对可行性 → 合成一份方案 → 用户批准 → COORD 组织实施。PM 使用 `product-requirements`，ARCH 使用 `arch-deep-spec`，产品定义和技术设计在同一方案原地维护。

COORD 按已批准方案核对目标、范围、接口、依赖、预算和验收映射，不替 PM 补产品含义或替 ARCH 设计。PM/ARCH 是规划职责，不放入要求业务 candidate_commit 的工程 subtasks；明确目标的小修沿既有授权处理，不增加 PM 签字环节。

## 核心执行铁律

1. **业务仓 100% 只读**：`COORD` 仅允许写入 `project-control/`（根治理文件仅按获批方案精确白名单维护），严禁直接手改 业务仓及 SDK 平台项目源码。
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
   - 重跑前读取 `project-control/slices/ledger.md`，仅在切片 revision、完整输入及关联证据均匹配时复用已验证结果，不能凭旧 slice_id 跳过。
5. **2 轮保活返修熔断与 Human Gate #2**：
   - `fast_gate.py`、跨仓合龙或独立 Codex 报 `BLOCKER` 时，在同一保活 `ENG-*` 会话内定向返修，**最多 2 轮**；第 3 次失败立即 Fail-Fast 停机升级人类。
   - 批次全部 `SW-Verified` 或触及 `requires_hil_immediately: true` / 远端 `publish` / `git rebase` 冲突时，立即停机请求 **Human Gate #2**。

## 当前 C308L 编排约束

当前十席包含 PM 与 ENG-PLATFORM，按任务启用；SDK 按 project 隔离写入与构建输出。切片声明 revision/profile，续跑核对准确候选与产品 SDK 锁的输入摘要，不凭旧 slice_id 跳过。调用门禁后核验退出状态及真实 verdict；厂商 SDK 不变的应用任务不全量构建BSP。

启动前核对 run_workflow 的 agent/parallel/phase/log/call_tool 原语实际可用；缺少时报告自动巡航未演练，当前客户端可按批准边界继续委派独立任务，但不冒充 run_workflow 成功。
