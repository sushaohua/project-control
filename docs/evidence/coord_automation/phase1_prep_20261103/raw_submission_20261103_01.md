---
submission_id: SUB-20261103-001
revision: 1
submitted_at: '2026-11-03T11:49:44+08:00'
reported_by: HUMAN
source_channel: antigravity-main-session
coord_session: 8d4e8b77-42a9-4bd3-bd5a-1b881e8d4bd5
status: archived-verbatim
---

# 原始人工指令归档（SUB-20261103-001 rev 1）

## 1. 用户原话（逐字保留，零删改）

```text
你现在的角色是coord。
推进“三类人工入口自动调度”第一阶段。读取 project-control/docs/planning/coord_intake_dispatch_phase1_handoff_20261103.md 及其关联设计，按 revision 2 执行。

已确认原则：人工提交一批指令或 MD；一条指令对应一条需求，可拆成多个角色的工程任务；AI 先形成需求理解和实施概要，人工批准准确版本后实施。分类 YAML、编号和关联由程序生成。

先安排 PM、ARCH 提交一页确认单，说明目标、范围、验收场景、实施概要及待决问题；安排 INTEGRATOR 核实真实 COORD 和角色调用、查询接口。已有有效批准直接引用，保护现有任务及成果。

将确认单交我批量审批。批准后，按“手动单步 → 持续推进与恢复 → 定时调度”分段实现并独立验收。第一阶段不接入 QA 自动生成 Issue，也不修改 MCU 或 Bootloader。普通技术问题由团队闭环
```

## 2. 关联输入原件与观察基线

| 输入原件 / 仓库 | 版本 / 分支 | Commit / SHA256 |
| --- | --- | --- |
| `project-control/docs/planning/coord_intake_dispatch_phase1_handoff_20261103.md` | `revision: 2` | `400e61311c726663c8645a6237ad1084b19fb7b2d3c8b1850b4e20e59a91ab06` |
| `project-control/docs/architecture/coord_intake_dispatch_phase1_design_20261103.md` | `revision: 2` | `8a2984c6bb4b868cc8e2d6742873527f448f27c7006d99c5ce322207b2941350` |
| `project-control/.agents/rules/delivery_and_coord_gate.md` | `revision: 5` | `c48f91e65766da74813cb85bb6e90b286ce27f0ac297c7e95a48e95af17590a6` |
| `project-control/.agents/rules/codex_qa_review.md` | `2026-11-02` | `b7dfa803382ca6b5d21a6bdb13d345bb0e149226fd0b4c15494be318dd4624f2` |
| `project-control/docs/planning/coord_autorun_tasklist_20261029.md` | `revision: 1` | `f42dec024d6aae9f0e5e63cc6f6b09f46bd82f045134078c960e30a3369706cd` |
| 总仓 (`workspace`) | `main` | `1e88c17a62bdcb63b4c0b78321eba3c44c3edc11` |
| `project-control` | `main` (含本地未提交规则/设计增量) | `b4af2d32601a07d448ac8d67a07c57f5b9ab36ac` |
| `soc-ap` | `main` | `427dd6d82caceebb7b4642e78f1dbfa96ff5fc84` |
| `mcu-p3` | `feat/soc-debug` | `e051111e68dd61896ed42c0961153b167b8bca41` |
| `test_harness` | `main` | `ccf1476a0b98cb55ca9ee7bd49d73ca5d4704414` |
| `boot/bootloadermc` | `soc_debug` | `01bfda29b82f0576cb255d0b4196aeda1edb8d2e` |
| `boot/bootloaderth` | `soc_debug` | `1e4f592feaf400e5d4a1932db5aa86e75e60832b` |
