---
id: TWIN-15
title: TWIN-15 MC温度契约复核与必要修订
revision: 1
plan_revision: vmware-soc-twin-20261029
task_kind: implementation
development_stage: vmware-twin
dispatchable: true
status: Done
blocked: false
planning_status: closed
owner: ENG-MC
proposed_owner: ENG-MC
executor:
  role: ENG-MC
  agent_id: 1aba53f3-e424-4e8c-926a-ddfc0d5e44c5
  run_id: run_01
reviewer:
- QA
- ARCH
verifier: null
integrator: INTEGRATOR
review_assignments:
  reviewer_sessions:
  - role: QA
    platform: codex
    model: gpt-6-luna
    planned_session_alias: planned-qa-twin-15
    session: 04e29db1-8492-7f9a-81cb-9a885e528802
    decision: APPROVED
    reviewed_task_revision: 1
    artifact_version: run_01
    evidence: docs/evidence/twin/TWIN-15/runs/run_01/qa_review_report.md
    report_sha256: 41b65b63be708e3100650d4eb0caefdd678d212ce71934c9c1e19488da154ab1
  - role: ARCH
    platform: codex
    model: gpt-6-luna
    planned_session_alias: planned-arch-twin-15
    session: 08bc71da-8831-7e8a-82dc-8a901f417715
    decision: APPROVED
    reviewed_task_revision: 1
    artifact_version: run_01
    evidence: docs/evidence/twin/TWIN-15/runs/run_01/arch_review_report.md
    report_sha256: 7d65c3bbec6147e0340156bbac8fe45722129c9225792376fcd8efbe68194f4d
  verifier_session: null
  integrator_session: null
primary_work_package: TASK-002
related_work_packages: []
depends_on:
- TWIN-02
- TWIN-03
- TEMP-03
dependency_conditions:
- task: TWIN-02
  accepted_version: 1.0.0
  acceptance_evidence: docs/evidence/twin/TWIN-02/runs/run_03/result.md
  required: 开工前绑定准确产物、必需接受及适用限制；历史Done不批准新契约
- task: TWIN-03
  accepted_version: 1.0.0
  acceptance_evidence: docs/evidence/twin/TWIN-03/runs/run_02/result.md
  required: 开工前绑定准确产物、必需接受及适用限制；历史Done不批准新契约
- task: TEMP-03
  accepted_version: 1.0.0
  acceptance_evidence: docs/evidence/temperature_increment/TEMP-03/runs/run_01/result.md
  required: 开工前绑定准确产物、必需接受及适用限制；历史Done不批准新契约
scope_status: mapped
allowed_repositories:
- mcu-p3
- project-control
write_scope:
  mcu-p3:
  - motion-controller-mcu/project/src/minimc*
  - motion-controller-mcu/project/inc/minimc*
  - motion-controller-mcu/project/src/thermistor*
  - motion-controller-mcu/project/inc/thermistor*
  project-control:
  - docs/evidence/twin/TWIN-15/**
allowed_paths:
- mcu-p3/motion-controller-mcu/project/src/minimc*
- mcu-p3/motion-controller-mcu/project/inc/minimc*
- mcu-p3/motion-controller-mcu/project/src/thermistor*
- mcu-p3/motion-controller-mcu/project/inc/thermistor*
- project-control/docs/evidence/twin/TWIN-15/**
source_baseline:
  project-control: 6207499476986989df3a82848510cbaa68e1435e
  soc-ap: 9d671be3c6eacd90169a56718e8e139c85ed9513
  mcu-p3: 0ba7769fe60a032f765deada1e112c360e08b3cd
  test_harness: 0b7497ba43158841eb3c4af7f16e477b9c30c2c5
base_commit: 1246ea9cb441d074ea444f53320f5632fefcd503
candidate_commit: 0ba7769fe60a032f765deada1e112c360e08b3cd
dispatch_binding:
  source_commit: null
  workspace_diff_sha256: null
  consumed_artifact_versions: {}
protocol_input:
  path: project-control/docs/specs/ap_mc_formal_protocol_v2_0_multidevice_routing_draft_20261015.md
  sha256: 9f8d4f9607cb3e76cc30b9ee2f971b23c3e0d936611188466a71f4aa15f3ce54
  revision: 2.0.3
read_sources:
- project-control/docs/planning/vmware_soc_twin_task_execution_20261029.md
- project-control/docs/planning/vmware_soc_twin_development_plan_20261029.md
- project-control/docs/interfaces/soc_temperature_module_architecture_icd_draft_20261028.md
- project-control/.agents/rules/c_cpp_coding_standard.md
worktree: null
lease: null
resources:
- resource: isolated-worktree-and-build-output
  location: null
  exclusive: true
  pending: Ready前按实际会话登记；最多两张实现票并行
- resource: physical-uart-probe-bench
  location: null
  exclusive: true
  pending: 只有涉及实际操作才按单一操作者预约；未预约不触碰硬件
budget:
  planned_checkpoint_minutes: 30
  max_evidence_based_corrections: 2
  on_limit: 保存证据交COORD
checkpoint: 开工前绑定；接口/实现自检；准确候选独立检查；收件
execution_contract: project-control/docs/planning/vmware_soc_twin_task_execution_20261029.md
readiness_pending:
- 真实作者、全部必需检查会话、有效租约和隔离worktree/输出待登记
- 开工时重取实际commit/dirty diff及SHA256；前置准确接受版本/证据待绑定
- 验证命令须在已实现入口上具体化并核资源/权限，不运行占位命令
deliverables:
  artifacts:
  - mcu-p3/motion-controller-mcu/project/src/minimc*
  - mcu-p3/motion-controller-mcu/project/inc/minimc*
  - mcu-p3/motion-controller-mcu/project/src/thermistor*
  - mcu-p3/motion-controller-mcu/project/inc/thermistor*
  record: docs/evidence/twin/TWIN-15/runs/<actual-run>/result.md
rollback:
  steps:
  - 仅回退本票候选；保存失败证据和原状态；硬件恢复须按实际SOP及授权执行
handoff:
  receiver_role: COORD
  receiver_session: null
  transport: docs
  evidence_location: docs/evidence/twin/TWIN-15
  acknowledgement: null
verification:
  commands:
  - id: check_graph
    cwd: .
    command: PYTHONDONTWRITEBYTECODE=1 python3 project-control/tools/check_task_graph.py --workspace .
    expected: 结构无错误；不等于任务/运行/硬件接受
    availability: local
  - id: planned_build_and_acceptance
    cwd: .
    command: Ready前由Owner绑定本票实际构建与正反例运行入口
    expected: 按新接受契约核MC温度表示/flags/命令/传感依据与透明路由；仅必要最小修订，或交付有证据的不改实现复用结论及准确固件
    availability: planned-not-runnable
  positive_cases:
  - 按新接受契约核MC温度表示/flags/命令/传感依据与透明路由；仅必要最小修订，或交付有证据的不改实现复用结论及准确固件
  negative_cases:
  - 边界温度/故障哨兵/错误flags/源目标或seq不符按独立预期；不从duty字段推定物理关断，不伪造TH应答
required_evidence_level: software-verified
verification_environment: isolated-host-or-document
qa_review_policy: project-control/.agents/rules/codex_qa_review.md
updated: '2026-10-29T13:52:16+08:00'
---

# TWIN-15 MC温度契约复核与必要修订

## 范围与交付

按新接受契约核MC温度表示/flags/命令/传感依据与透明路由；仅必要最小修订，或交付有证据的不改实现复用结论及准确固件。

首条业务采用现有温度只读切片；只读刷新表示请求采样，不增加加热、运动、OTA或打印控制。完整模块登记实现/未实现/后续状态，不为未实现模块启动空进程后声称功能完成。

## 正反验收与边界

正例：按新接受契约核MC温度表示/flags/命令/传感依据与透明路由；仅必要最小修订，或交付有证据的不改实现复用结论及准确固件。

负例：边界温度/故障哨兵/错误flags/源目标或seq不符按独立预期；不从duty字段推定物理关断，不伪造TH应答。

所有运行证据须绑定源码commit与dirty diff、构建日志、制品/配置/契约哈希及实际环境。VM真实应用、隔离测试替身、真实MC/TH HIL、SoC实板四类分别登记。

## 开工与闭环

本卡为Backlog计划，未登记真实作者/检查会话、有效租约和候选输入；当前不是开工许可。Ready前按输入版本、写范围、独立检查、工作区/输出目录、资源排他及可执行验证命令逐项落实。

依赖卡Done只表示其原范围，消费时须绑定准确接受版本、证据和限制；不继承被撤回或超范围签署。若无须改旧实现，也须提交准确复用矩阵及适用验证，不以空实现自动关闭。

实现Owner负责本范围及卡内函数拆分；新增函数≤50行、≤4参。共享CMake/配置/生成输出由既定Owner串行改动并登记精确白名单，其他卡提交接口需求，不并发抢写。

作者提交候选 → COORD安排必需独立检查（QA、ARCH）→ 必要真实环境验证 → COORD核对报告/制品哈希与收件 → 按实际范围推进状态。QA作者的预期、工具、报告必须由非作者ARCH独立复核；角色和计划别名不是已启动会话。

硬件使用和操作授权沿用现行HW-G及软硬件交接规范；此文档更新不执行串口、探针、烧录或加热操作。连续两次有证据修正仍失败，保存候选/失败日志交COORD重新裁决，不修改判据促通过。

[执行总表](../../../../docs/planning/vmware_soc_twin_task_execution_20261029.md) · [两阶段方案](../../../../docs/planning/vmware_soc_twin_development_plan_20261029.md)
