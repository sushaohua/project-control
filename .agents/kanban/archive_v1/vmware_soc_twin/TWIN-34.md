---
id: TWIN-34
title: TWIN-34 Web HMI手动轴控盘与5×5调平网格热力图组件实现
revision: 1
plan_revision: vmware-soc-twin-20261029
task_kind: implementation
development_stage: vmware-twin
dispatchable: true
status: Backlog
blocked: false
planning_status: planned
owner: null
proposed_owner: ENG-UI
executor:
  role: ENG-UI
  agent_id: null
  run_id: null
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
    planned_session_alias: planned-qa-twin-34
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
    planned_session_alias: planned-arch-twin-34
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
- TWIN-33
dependency_conditions:
- task: TWIN-33
  accepted_version: soc-ap=ca6c40b2fdfc421ef628100f8b2d40fe64869d85
  acceptance_evidence: docs/evidence/twin/TWIN-33/runs/run_01/qa_review_report.md
  required: 继承TWIN-33打印工作台HMI基础
scope_status: mapped
allowed_repositories:
- soc-ap
- project-control
write_scope:
  soc-ap:
  - browser_hmi/first_release/**
  - tests/ui/**
  project-control:
  - docs/evidence/twin/TWIN-34/**
allowed_paths:
- soc-ap/browser_hmi/first_release/**
- soc-ap/tests/ui/**
- project-control/docs/evidence/twin/TWIN-34/**
source_baseline:
  project-control: 2ee77a21ca48b84b24f3f66e572c56663ad69a12
  soc-ap: ca6c40b2fdfc421ef628100f8b2d40fe64869d85
  mcu-p3: 04231388c842c1ce3e5b71675d0dc118a65edf2e
  test_harness: 0b7497ba43158841eb3c4af7f16e477b9c30c2c5
base_commit: ca6c40b2fdfc421ef628100f8b2d40fe64869d85
candidate_commit: null
dispatch_binding:
  source_commit: ca6c40b2fdfc421ef628100f8b2d40fe64869d85
  workspace_diff_sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
  consumed_artifact_versions: {}
protocol_input:
  path: project-control/docs/planning/ui_ux_end_to_end_interaction_design_20261031.md
  sha256: bde64b69b88556659cee48c87d2e648ad51d60a76b88250cc8f317102ff5e7f2
  revision: 1
read_sources:
- project-control/docs/planning/product/first_release_scope_decision_20261029.md
- soc-ap/browser_hmi/first_release/index.html
- soc-ap/browser_hmi/first_release/app.js
worktree: soc-ap
lease: null
resources:
- resource: ui-build-env
  location: null
  exclusive: true
  pending: Ready前落实
budget:
  planned_checkpoint_minutes: 60
  max_evidence_based_corrections: 2
  on_limit: 保存证据交COORD
checkpoint: 开工前绑定；组件自检；双独立沙箱检查；收件
execution_contract: project-control/docs/planning/vmware_soc_twin_task_execution_20261029.md
readiness_pending: []
deliverables:
  artifacts:
  - soc-ap/browser_hmi/first_release/index.html
  - soc-ap/browser_hmi/first_release/app.js
  record: docs/evidence/twin/TWIN-34/runs/<actual-run>/result.md
rollback:
  steps:
  - 仅回退本票候选；保存失败证据和原状态
handoff:
  receiver_role: COORD
  receiver_session: session-coord-autorun
  transport: docs
  evidence_location: docs/evidence/twin/TWIN-34
  acknowledgement: null
verification:
  commands:
  - id: check_graph
    cwd: .
    command: PYTHONDONTWRITEBYTECODE=1 python3 project-control/tools/check_task_graph.py --workspace .
    expected: 结构无错误
    availability: local
  positive_cases:
  - 实现【🕹️ 轴控与调平】主标签页面板
  - 实现 X/Y 四向触控罗盘与 Z 轴升降微调控件（0.1/1/10/100mm 步长）
  - 实现一键全局归零 G28 与独立分轴归零
  - 实现 5x5 调平网格 25 点彩色高程热力图（绿色平整、蓝色低、橙红高）
  - 实现一键重新触发自动调平校准按钮
  negative_cases:
  - 严禁违背触控热区规范
  - 处于急停状态下轴控指令严禁动作
required_evidence_level: server-sandbox-and-independent-review
verification_environment: docker-qa-sandbox-and-isolated-codex
qa_review_policy: project-control/.agents/rules/codex_qa_review.md
updated: '2026-10-31T17:30:00+08:00'
---

# TWIN-34 Web HMI手动轴控盘与5×5调平网格热力图组件实现

## 任务目标
由 ENG-UI（界面工程师）依据 DES-UI 的交互规范，在 Web 前端落地【🕹️ 轴控与调平】面板，包含三轴触控罗盘、G28 归零与 25 点调平网格高程彩色热力图。
