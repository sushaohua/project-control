# AI SoC V2 垂直切片执行账本 (`ledger.md`)

本账本由 `project-control/tools/workflow/run_slice_batch.py` 与 `tools/gates/slice_gate.py` 追加维护，作为断点幂等续跑与双态准出（`SW-Verified` / `HIL-Verified`）唯一状态记录。

## 1. 切片准出流水表

| 时间戳 (UTC+8) | 批次 ID | 切片 ID | 准出状态 | 锁定多仓 Commit 摘要 | Docker 容器 ID | Codex 会话 ID | Verdict SHA256 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |

## 2. 非阻断技术债登记表 (`MINOR` Findings)

| 时间戳 (UTC+8) | 切片 ID | 审计轴 | 代码位置 | 问题描述与后续收敛建议 |
| :--- | :--- | :--- | :--- | :--- |
