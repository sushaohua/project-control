---
id: TWIN-39
title: TWIN-39 browser_hmi硬件离线阻断视觉与双状态指示器
revision: 1
plan_revision: vmware-soc-twin-20261029
task_kind: implementation
development_stage: vmware-twin
dispatchable: true
status: Review
blocked: false
planning_status: planned
owner: ENG-UI
proposed_owner: ENG-UI
executor:
  role: ENG-UI
  agent_id: session-eng-ui
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
    planned_session_alias: planned-qa-twin-39
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
    planned_session_alias: planned-arch-twin-39
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
depends_on:
- TWIN-33
- TWIN-34
- TWIN-38
dependency_conditions:
- task: TWIN-33
  accepted_version: soc-ap=2e19a4242699e3a6a9be5c483d72b2260ffc3dd2; project-control=c6eb49339794cb150fbf9e6584be6e63dc366f60
  acceptance_evidence: docs/evidence/twin/TWIN-33/runs/run_01/qa_review_report.md
  required: 继承TWIN-33首发Web HMI框架
- task: TWIN-34
  accepted_version: soc-ap=2e19a4242699e3a6a9be5c483d72b2260ffc3dd2; project-control=c6eb49339794cb150fbf9e6584be6e63dc366f60
  acceptance_evidence: docs/evidence/twin/TWIN-34/runs/run_01/qa_review_report.md
  required: 继承TWIN-34调平与运控交互
- task: TWIN-38
  accepted_version: soc-ap=409846a5ce6c1b1d6115736e7129a71d85ebe875; project-control=afd525946602c973d52feedcf7364f77ab2d221c
  acceptance_evidence: docs/evidence/twin/TWIN-38/runs/run_01/qa_review_report.md
  required: 继承TWIN-38网关离线拦截与503语义
scope_status: mapped
allowed_repositories:
- soc-ap
- project-control
write_scope:
  soc-ap:
  - browser_hmi/first_release/**
  project-control:
  - docs/evidence/twin/TWIN-39/**
allowed_paths:
- soc-ap/browser_hmi/first_release/**
- project-control/docs/evidence/twin/TWIN-39/**
source_baseline:
  project-control: afd525946602c973d52feedcf7364f77ab2d221c
  soc-ap: 409846a5ce6c1b1d6115736e7129a71d85ebe875
  mcu-p3: 04231388c842c1ce3e5b71675d0dc118a65edf2e
  test_harness: 0b7497ba43158841eb3c4af7f16e477b9c30c2c5
base_commit: 409846a5ce6c1b1d6115736e7129a71d85ebe875
candidate_commit: 456aa72adb0def34dca448e9dafcdef4e7ab9d52
dispatch_binding:
  source_commit: 409846a5ce6c1b1d6115736e7129a71d85ebe875
  workspace_diff_sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
  consumed_artifact_versions: {}
protocol_input:
  path: project-control/docs/evidence/architecture/qa_review_hardware_realism_proposal.md
  sha256: df3db0adf20bb9cc240b1bf144ce050d3a77a5c0fb6e104b2578a5b936a91ae5
  revision: 1
read_sources:
- soc-ap/browser_hmi/first_release/index.html
- soc-ap/browser_hmi/first_release/app.js
- soc-ap/browser_hmi/first_release/styles.css
worktree: soc-ap
lease: null
resources:
- resource: ui-static-env
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
  - soc-ap/browser_hmi/first_release/test_hmi_contract.py
  record: docs/evidence/twin/TWIN-39/runs/<actual-run>/result.md
rollback:
  steps:
  - 仅回退本票候选；保存失败证据和原状态
handoff:
  receiver_role: COORD
  receiver_session: session-coord-autorun
  transport: docs
  evidence_location: docs/evidence/twin/TWIN-39
  acknowledgement: null
verification:
  commands:
  - id: check_graph
    cwd: .
    command: PYTHONDONTWRITEBYTECODE=1 python3 project-control/tools/check_task_graph.py --workspace .
    expected: 结构无错误
    availability: local
  positive_cases:
  - 界面区分网关服务与物理硬件双指示灯
  - 正确区分 0x7FFFFFFE 离线与 0x7FFFFFFF 故障哨兵值
  - 离线时操作区弹出黄色悬浮警告条
  - 离线时灰化所有运控轴操作、加热调节与启动作业按钮
  - 捕获 503 错误并进行透明友好的 UI 弹窗反馈
  negative_cases:
  - 严禁物理离线时显示假正常温度
  - 严禁物理离线时允许用户点击运控产生假请求
required_evidence_level: server-sandbox-and-independent-review
verification_environment: docker-qa-sandbox-and-isolated-codex
qa_review_policy: project-control/.agents/rules/codex_qa_review.md
updated: '2026-10-31T18:40:00+08:00'
---

# TWIN-39 browser_hmi硬件离线阻断视觉与双状态指示器

## 任务目标
由 ENG-UI 完善首发 Web HMI 界面中的离线透明感知与安全视觉。顶栏增加物理硬件指示灯 `#hw-conn-pill`；正确解析哨兵值（`0x7FFFFFFE` 显示 `--.- °C (离线)`）；在离线时弹出黄色告警条并锁定运控与作业启动按钮；统一拦截 HTTP 503 错误并提供弹窗反馈。
