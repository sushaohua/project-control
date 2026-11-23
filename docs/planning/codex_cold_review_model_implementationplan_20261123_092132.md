# 正式 Codex 冷审模型调整实施方案

## 修订历史

| 版本 | 修订时间（北京时间） | 修订人 | 变更摘要 | 审批状态 |
| --- | --- | --- | --- | --- |
| `v1.0` | `2026-11-23 09:21:32` | `AI (Codex)` | 归档正式冷审默认 Sol High 与按切片选择 Astra 的范围和验收 | 用户已明确批准按建议修改 |

## 1. 目标和现状

正式独立冷审的默认模型改为 `gpt-6.2-sol`，启动时明确传 `model_reasoning_effort=high`。遇到 Bootloader、跨板协议或复杂并发时，由任务负责人在获批切片填写 `codex_review_model: gpt-6.2-astra`。每个待交付候选仍只走现有一次正式冷审。保留已有 `CODEX_MODEL` 调用入口。选择优先级为切片显式值、现有环境覆盖、默认 Sol。审阅保持独立会话、只读、原输出 Schema 和现有裁决语义。回执记录请求的模型、推理档位与真实会话各自的来源。

实际调用链为 `tools/gates/slice_gate.py:execute_slice_funnel()` → `_run_codex_stage()` → `tools/gates/codex_review.py:run_codex_audit()` → `_build_codex_cmd()` → 本机 `codex exec`。当前默认 Luna，审查命令未显式配置推理档位。手动冷审入口继续接受单独的切片 ID。首轮只配置模型选型，不修改提示词的审查范围、QA 授权或工作流模型。

## 2. 实施和验收

| 步骤 | 路径与预算 | 验收 |
| --- | --- | --- |
| 配置接入 | `tools/gates/codex_review.py`、`tools/gates/slice_gate.py`、`tools/test_v2_gates.py`、`slices/TEMPLATE_SLICE.yaml`。只在现有入口传递选择、记录请求参数并加回归。总行数自检上限随本次必要增量微调，继续执行逐函数和反假状态门禁。 | 从工作区根运行 `python3 -B project-control/tools/test_v2_gates.py`。覆盖默认 Sol / High、Astra 选择优先于环境覆盖、旧切片兼容和坏参数失败，核对 CLI 只读与原裁决行为。 |
| 权威规则同步 | 修改 `.agents/rules/codex_qa_review.md`、`delivery_and_coord_gate.md`、`02_模块与Agent职责.md`、`04_公共看板与读写协议.md`、`qa_audit_checklist_guide_20261013_115611.md` 及 `.agents/rules/templates/` 中 `任务卡模板.md`、`角色任务提示词.md`、`QA审查报告模板.md` 的正式冷审引用。`.agents/skills/two-axis-qa-audit/SKILL.md` 改为引用权威规则。 | 核对规则、模板与代码的正式冷审默认和覆盖方式一致，历史证据、历史切片和旧调度实现不改。 |

限定 `project-control/`，最多 14 个文件（含本方案），增删合计最多 150 行。异常时可恢复原模型入口及规则引用，已签署候选和证据按原记录保存。
