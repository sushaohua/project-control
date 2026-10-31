---
id: TWIN-33
title: TWIN-33 Web HMI核心打印工作台与G-code上传流式监视面板实现
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
    planned_session_alias: planned-qa-twin-33
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
    planned_session_alias: planned-arch-twin-33
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
- TWIN-10
- TWIN-20
- TWIN-31
- TWIN-32
dependency_conditions:
- task: TWIN-10
  accepted_version: soc-ap=33e23b74175b916b262d73b9901b106c4fb18f14; project-control=cd3b09d4dc2cb247347c98e9b1daf46bcb08ff6b
  acceptance_evidence: docs/evidence/twin/TWIN-10/runs/run_01/qa_review_report.md
  required: 继承TWIN-10 Web HMI初代样式与结构
- task: TWIN-20
  accepted_version: soc-ap=cb70d59e949396f45aec94d33ae23cab75beb282; project-control=f0fe3948482adb71e5366006850fdb9dd36282bc
  acceptance_evidence: docs/evidence/twin/TWIN-20/runs/run_02/qa_review_report.md
  required: 继承TWIN-20料槽映射与OOBE开箱向导规范
- task: TWIN-31
  accepted_version: project-control=2ee77a21ca48b84b24f3f66e572c56663ad69a12
  acceptance_evidence: docs/evidence/twin/TWIN-31/runs/run_01/qa_review_report.md
  required: 继承TWIN-31交互原型规范与组件定义
- task: TWIN-32
  accepted_version: soc-ap=ca6c40b2fdfc421ef628100f8b2d40fe64869d85
  acceptance_evidence: docs/evidence/twin/TWIN-32/runs/run_01/qa_review_report.md
  required: 继承TWIN-32作业管理与REST端点
scope_status: mapped
allowed_repositories:
- soc-ap
- project-control
write_scope:
  soc-ap:
  - browser_hmi/first_release/**
  - tests/ui/**
  project-control:
  - docs/evidence/twin/TWIN-33/**
allowed_paths:
- soc-ap/browser_hmi/first_release/**
- soc-ap/tests/ui/**
- project-control/docs/evidence/twin/TWIN-33/**
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
  - soc-ap/browser_hmi/first_release/styles.css
  record: docs/evidence/twin/TWIN-33/runs/<actual-run>/result.md
rollback:
  steps:
  - 仅回退本票候选；保存失败证据和原状态
handoff:
  receiver_role: COORD
  receiver_session: session-coord-autorun
  transport: docs
  evidence_location: docs/evidence/twin/TWIN-33
  acknowledgement: null
verification:
  commands:
  - id: check_graph
    cwd: .
    command: PYTHONDONTWRITEBYTECODE=1 python3 project-control/tools/check_task_graph.py --workspace .
    expected: 结构无错误
    availability: local
  positive_cases:
  - 实现默认首屏【🖨️ 打印工作台】
  - 实现 G-code 外部文件拖拽上传区与内置经典样例（3DBenchy、Cube）一键载入
  - 实现大进度环、当前层高/总层数、剩余时间倒计时卡片
  - 实现开始打印、暂停、恢复、取消按钮组与当前 G-code 指令行流式刷新
  - 实现全局顶栏红色 E-STOP 紧急急停大按钮
  negative_cases:
  - 严禁违背触控热区规范
  - 离线空跑期间严禁伪造高温报警
required_evidence_level: server-sandbox-and-independent-review
verification_environment: docker-qa-sandbox-and-isolated-codex
qa_review_policy: project-control/.agents/rules/codex_qa_review.md
updated: '2026-10-31T17:30:00+08:00'
---

# TWIN-33 Web HMI核心打印工作台与G-code上传流式监视面板实现

## 任务目标
由 ENG-UI（界面工程师）依据 DES-UI 的交互规范，在 Web 前端落地核心首屏【🖨️ 打印工作台】与全局常驻红色 E-STOP 急停按钮。
