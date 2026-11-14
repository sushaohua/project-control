---
id: TWIN-31
title: TWIN-31 Web HMI全流程打印交互原型规范与组件状态设计
revision: 1
plan_revision: vmware-soc-twin-20261029
task_kind: design
development_stage: vmware-twin
dispatchable: true
status: Backlog
blocked: false
planning_status: planned
owner: session-des-ui-twin-31
proposed_owner: DES-UI
executor:
  role: DES-UI
  agent_id: session-des-ui-twin-31
  run_id: run_01
reviewer:
- ARCH
- QA
verifier: null
integrator: INTEGRATOR
review_assignments:
  reviewer_sessions:
  - role: QA
    platform: codex
    model: gpt-6-luna
    planned_session_alias: planned-qa-twin-31
    session: null
    session_evidence: null
    decision: PENDING
    reviewed_task_revision: 1
    artifact_version: null
    evidence: null
    report_sha256: null
  - role: ARCH
    platform: codex
    model: gpt-6-luna
    planned_session_alias: planned-arch-twin-31
    session: null
    session_evidence: null
    decision: PENDING
    reviewed_task_revision: 1
    artifact_version: null
    evidence: null
    report_sha256: null
  verifier_session: null
  integrator_session: null
primary_work_package: TASK-009
related_work_packages:
- TASK-010
- TASK-011
depends_on:
- TWIN-20
- TWIN-23
- TWIN-25
- TWIN-30
dependency_conditions:
- task: TWIN-20
  accepted_version: soc-ap=cb70d59e949396f45aec94d33ae23cab75beb282; project-control=f0fe3948482adb71e5366006850fdb9dd36282bc
  acceptance_evidence: docs/evidence/twin/TWIN-20/runs/run_02/qa_review_report.md
  required: 继承TWIN-20 HMI样式与OOBE开箱向导规范
- task: TWIN-23
  accepted_version: soc-ap=674e7336f924c2f297c439417a0011adc12427fa; project-control=e097299f1483d5192f3319996fa3008901f27613
  acceptance_evidence: docs/evidence/twin/TWIN-23/runs/run_01/qa_review_report.md
  required: 继承TWIN-23离线作业流式执行与Option A强电锁死规范
- task: TWIN-25
  accepted_version: 04231388c842c1ce3e5b71675d0dc118a65edf2e
  acceptance_evidence: docs/evidence/twin/TWIN-25/runs/run_01/qa_review_report.md
  required: 继承TWIN-25 5x5调平网格高程数据模型
- task: TWIN-30
  accepted_version: soc-ap=7bb05218c39d6852cac5e8d86db845dbbedd7064; project-control=f7d18c48774a8787f0dfa1d1cbe9dddea9309a40
  acceptance_evidence: docs/evidence/twin/TWIN-30/runs/run_01/qa_review_report.md
  required: 继承TWIN-30闭环全流程基线
scope_status: mapped
allowed_repositories:
- project-control
write_scope:
  project-control:
  - docs/design/ui_ux/**
  - docs/design/checklists/**
  - docs/evidence/twin/TWIN-31/**
allowed_paths:
- project-control/docs/design/ui_ux/**
- project-control/docs/design/checklists/**
- project-control/docs/evidence/twin/TWIN-31/**
source_baseline:
  project-control: 2ee77a21ca48b84b24f3f66e572c56663ad69a12
  soc-ap: ca6c40b2fdfc421ef628100f8b2d40fe64869d85
  mcu-p3: 04231388c842c1ce3e5b71675d0dc118a65edf2e
  test_harness: 0b7497ba43158841eb3c4af7f16e477b9c30c2c5
base_commit: 2ee77a21ca48b84b24f3f66e572c56663ad69a12
candidate_commit: null
dispatch_binding:
  source_commit: 2ee77a21ca48b84b24f3f66e572c56663ad69a12
  workspace_diff_sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
  consumed_artifact_versions: {}
protocol_input:
  path: project-control/docs/planning/ui_ux_end_to_end_interaction_design_20261031.md
  sha256: bde64b69b88556659cee48c87d2e648ad51d60a76b88250cc8f317102ff5e7f2
  revision: 1
read_sources:
- project-control/docs/planning/product/first_release_scope_decision_20261029.md
- project-control/.agents/rules/07_UI交互设计师职责与交付规范.md
- project-control/.agents/rules/02_模块与Agent职责.md
worktree: project-control
lease:
  owner: session-des-ui-twin-31
  task_revision: 1
  lease_id: lease-twin-31-run-01
  expires_at: '2026-10-31T23:59:59+08:00'
resources:
- resource: design-workspace
  location: null
  exclusive: true
  pending: Ready前落实
budget:
  planned_checkpoint_minutes: 45
  max_evidence_based_corrections: 2
  on_limit: 保存证据交COORD
checkpoint: 开工前绑定；交互原型规范自检；双独立沙箱检查；收件
execution_contract: project-control/docs/planning/vmware_soc_twin_task_execution_20261029.md
readiness_pending: []
deliverables:
  artifacts:
  - project-control/docs/design/ui_ux/hmi_full_interaction_specification.md
  - project-control/docs/design/checklists/ux_audit_checklist.md
  record: docs/evidence/twin/TWIN-31/runs/<actual-run>/result.md
rollback:
  steps:
  - 仅回退本票候选；保存失败证据和原状态
handoff:
  receiver_role: COORD
  receiver_session: session-coord-autorun
  transport: docs
  evidence_location: docs/evidence/twin/TWIN-31
  acknowledgement: null
verification:
  commands:
  - id: check_graph
    cwd: .
    command: PYTHONDONTWRITEBYTECODE=1 python3 project-control/tools/check_task_graph.py --workspace .
    expected: 结构无错误
    availability: local
  positive_cases:
  - 完整规划打印工作台主航道：G-code上传拖拽区、内置样例选择、进度环、开始/暂停/恢复/取消按钮群
  - 完整规划手动轴控盘（X/Y 罗盘与 Z 轴升降、0.1~100mm 步长、一键 G28 归零）
  - 完整规划 5x5 调平网格 25 点彩色高程热力图渲染规范与标定操作流
  - 完整定义全局顶栏常驻红色 E-STOP 紧急急停按钮与 HMS 告警抽屉
  - 交付完备的 UX 体验验收清单 (UX Audit Checklist)
  negative_cases:
  - 严禁虚构不符合 Option A 强电 0% 锁死底线的危险硬件操作
  - 严禁违反触控热区 >= 48px 标准
required_evidence_level: server-sandbox-and-independent-review
verification_environment: docker-qa-sandbox-and-isolated-codex
qa_review_policy: project-control/.agents/rules/codex_qa_review.md
updated: '2026-10-31T17:30:00+08:00'
---

# TWIN-31 Web HMI全流程打印交互原型规范与组件状态设计

## 任务目标
由 DES-UI（UI/UX 交互设计专家）编制高保真 Web HMI 全流程交互原型规范与组件状态设计文档，作为后续 ENG-UI 与 ENG-NET 编码落地的唯一权威设计基准：
1. 规划首屏【🖨️ 打印工作台】：含 G-code 拖拽上传、内置模型选择、进度大环、开始/暂停/终止按钮与流式走线实时进度条；
2. 规划【🕹️ 轴控与调平】面板：含 X/Y 罗盘、Z 轴升降微调、一键 G28 归零与 5×5 调平网格彩色高程热力图；
3. 规范全局常驻顶栏：含红色 E-STOP 紧急急停大按钮、双温胶囊与全局 HMS 告警抽屉；
4. 交付独立 UX 体验验收清单（UX Audit Checklist）。
