---
id: TWIN-10
title: TWIN-10 浏览器交互屏幕接入真实业务接口
revision: 1
plan_revision: vmware-soc-twin-20261029
task_kind: implementation
development_stage: vmware-twin
dispatchable: true
status: Done
blocked: false
planning_status: closed
owner: ENG-UI
proposed_owner: ENG-UI
executor:
  role: ENG-UI
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
    planned_session_alias: planned-qa-twin-10
    session: 4d92a14b-741a-4d29-a1b7-95ec10e30155
    decision: APPROVED
    reviewed_task_revision: 1
    artifact_version: run_01
    evidence: docs/evidence/twin/TWIN-10/runs/run_01/qa_review_report.md
    report_sha256: 79493097250f2eb08789616fe8b5634bf08809c0cc5a29e7f941e08d8de58cc0
  - role: ARCH
    platform: codex
    model: gpt-6-luna
    planned_session_alias: planned-arch-twin-10
    session: 6b81729b-8831-7e8a-82dc-8a901f417753
    decision: APPROVED
    reviewed_task_revision: 1
    artifact_version: run_01
    evidence: docs/evidence/twin/TWIN-10/runs/run_01/arch_review_report.md
    report_sha256: 1dd8b836f0d9ea818c568ad3a03e72af3a574e70df2ce6ef77fe74b88bc2c6f6
  verifier_session: null
  integrator_session: null
primary_work_package: TASK-009
related_work_packages: []
depends_on:
- TWIN-02
- TWIN-03
- TWIN-09
dependency_conditions:
- task: TWIN-02
  accepted_version: 1.0.0
  acceptance_evidence: docs/evidence/twin/TWIN-02/runs/run_03/result.md
  required: 开工前绑定准确产物、必需接受及适用限制；历史Done不批准新契约
- task: TWIN-03
  accepted_version: 1.0.0
  acceptance_evidence: docs/evidence/twin/TWIN-03/runs/run_02/result.md
  required: 开工前绑定准确产物、必需接受及适用限制；历史Done不批准新契约
- task: TWIN-09
  accepted_version: 1.0.0
  acceptance_evidence: docs/evidence/twin/TWIN-09/runs/run_01/result.md
  required: 开工前绑定准确产物、必需接受及适用限制；历史Done不批准新契约
scope_status: mapped
allowed_repositories:
- soc-ap
- project-control
write_scope:
  soc-ap:
  - ui/twin/**
  - tests/ui/twin/**
  project-control:
  - docs/evidence/twin/TWIN-10/**
allowed_paths:
- soc-ap/ui/twin/**
- soc-ap/tests/ui/twin/**
- project-control/docs/evidence/twin/TWIN-10/**
source_baseline:
  project-control: cd3b09d4dc2cb247347c98e9b1daf46bcb08ff6b
  soc-ap: 33e23b74175b916b262d73b9901b106c4fb18f14
  mcu-p3: d756a13b3c2a1c47186a07311b2c24fa43431465
  test_harness: 0b7497ba43158841eb3c4af7f16e477b9c30c2c5
base_commit: 4445c8fedc21bafef5e6c971fcb54cec703f0e71
candidate_commit: 33e23b74175b916b262d73b9901b106c4fb18f14
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
  - soc-ap/ui/twin/**
  - soc-ap/tests/ui/twin/**
  record: docs/evidence/twin/TWIN-10/runs/<actual-run>/result.md
rollback:
  steps:
  - 仅回退本票候选；保存失败证据和原状态；硬件恢复须按实际SOP及授权执行
handoff:
  receiver_role: COORD
  receiver_session: null
  transport: docs
  evidence_location: docs/evidence/twin/TWIN-10
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
    expected: 可见浏览器界面显示MC/TH温度、来源、有效性、服务状态与故障；刷新等只读交互走真实API；同份资源适配目标屏尺寸
    availability: planned-not-runnable
  positive_cases:
  - 可见浏览器界面显示MC/TH温度、来源、有效性、服务状态与故障；刷新等只读交互走真实API；同份资源适配目标屏尺寸
  negative_cases:
  - HTTP/SSE断线、过期、UNKNOWN、服务重启、重复点击与小屏布局可复核；无随机数或本地定时器生成设备温度
required_evidence_level: software-verified
verification_environment: isolated-host-or-document
qa_review_policy: project-control/.agents/rules/codex_qa_review.md
updated: '2026-10-29T13:52:16+08:00'
---

# TWIN-10 浏览器交互屏幕接入真实业务接口

## 范围与交付

可见浏览器界面显示MC/TH温度、来源、有效性、服务状态与故障；刷新等只读交互走真实API；同份资源适配目标屏尺寸。

首条业务采用现有温度只读切片；只读刷新表示请求采样，不增加加热、运动、OTA或打印控制。完整模块登记实现/未实现/后续状态，不为未实现模块启动空进程后声称功能完成。

## 正反验收与边界

正例：可见浏览器界面显示MC/TH温度、来源、有效性、服务状态与故障；刷新等只读交互走真实API；同份资源适配目标屏尺寸。

负例：HTTP/SSE断线、过期、UNKNOWN、服务重启、重复点击与小屏布局可复核；无随机数或本地定时器生成设备温度。

所有运行证据须绑定源码commit与dirty diff、构建日志、制品/配置/契约哈希及实际环境。VM真实应用、隔离测试替身、真实MC/TH HIL、SoC实板四类分别登记。

## 开工与闭环

本卡为Backlog计划，未登记真实作者/检查会话、有效租约和候选输入；当前不是开工许可。Ready前按输入版本、写范围、独立检查、工作区/输出目录、资源排他及可执行验证命令逐项落实。

依赖卡Done只表示其原范围，消费时须绑定准确接受版本、证据和限制；不继承被撤回或超范围签署。若无须改旧实现，也须提交准确复用矩阵及适用验证，不以空实现自动关闭。

实现Owner负责本范围及卡内函数拆分；新增函数≤50行、≤4参。共享CMake/配置/生成输出由既定Owner串行改动并登记精确白名单，其他卡提交接口需求，不并发抢写。

作者提交候选 → COORD安排必需独立检查（QA、ARCH）→ 必要真实环境验证 → COORD核对报告/制品哈希与收件 → 按实际范围推进状态。QA作者的预期、工具、报告必须由非作者ARCH独立复核；角色和计划别名不是已启动会话。

硬件使用和操作授权沿用现行HW-G及软硬件交接规范；此文档更新不执行串口、探针、烧录或加热操作。连续两次有证据修正仍失败，保存候选/失败日志交COORD重新裁决，不修改判据促通过。

[执行总表](../../../../docs/planning/vmware_soc_twin_task_execution_20261029.md) · [两阶段方案](../../../../docs/planning/vmware_soc_twin_development_plan_20261029.md)
