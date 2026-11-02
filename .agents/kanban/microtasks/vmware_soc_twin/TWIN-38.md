---
id: TWIN-38
title: TWIN-38 ui_gateway链路感知、下线安全阻断与作业紧急挂起
revision: 1
plan_revision: vmware-soc-twin-20261029
task_kind: implementation
development_stage: vmware-twin
dispatchable: true
status: Review
blocked: false
planning_status: planned
owner: null
proposed_owner: ENG-STATE
executor:
  role: ENG-STATE
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
    planned_session_alias: planned-qa-twin-38
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
    planned_session_alias: planned-arch-twin-38
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
- TASK-008
- TASK-010
depends_on:
- TWIN-09
- TWIN-32
- TWIN-37
dependency_conditions:
- task: TWIN-09
  accepted_version: soc-ap=f2596515c0e1e92d6e4b85dae921d78ea15a9937; project-control=31818a7c2e35a1cb943d674cb2eeb1d36d3969fb
  acceptance_evidence: docs/evidence/twin/TWIN-09/runs/run_01/qa_review_report.md
  required: 继承TWIN-09 ui_gateway网关骨架
- task: TWIN-32
  accepted_version: soc-ap=2e19a4242699e3a6a9be5c483d72b2260ffc3dd2; project-control=c6eb49339794cb150fbf9e6584be6e63dc366f60
  acceptance_evidence: docs/evidence/twin/TWIN-32/runs/run_01/qa_review_report.md
  required: 继承TWIN-32首发作业引擎与运控快照
- task: TWIN-37
  accepted_version: soc-ap=409846a5ce6c1b1d6115736e7129a71d85ebe875; project-control=afd525946602c973d52feedcf7364f77ab2d221c
  acceptance_evidence: docs/evidence/twin/TWIN-37/runs/run_01/qa_review_report.md
  required: 继承TWIN-37真实硬件下线状态机
scope_status: mapped
allowed_repositories:
- soc-ap
- project-control
write_scope:
  soc-ap:
  - services/ui_gateway/**
  - tests/ui_gateway/**
  project-control:
  - docs/evidence/twin/TWIN-38/**
allowed_paths:
- soc-ap/services/ui_gateway/**
- soc-ap/tests/ui_gateway/**
- project-control/docs/evidence/twin/TWIN-38/**
source_baseline:
  project-control: afd525946602c973d52feedcf7364f77ab2d221c
  soc-ap: 409846a5ce6c1b1d6115736e7129a71d85ebe875
  mcu-p3: 04231388c842c1ce3e5b71675d0dc118a65edf2e
  test_harness: 0b7497ba43158841eb3c4af7f16e477b9c30c2c5
base_commit: 409846a5ce6c1b1d6115736e7129a71d85ebe875
candidate_commit: 5e46556f8fba3d52c42c9da32a39a2f2efd1ae7d
dispatch_binding:
  source_commit: 409846a5ce6c1b1d6115736e7129a71d85ebe875
  workspace_diff_sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
  consumed_artifact_versions: {}
protocol_input:
  path: project-control/docs/evidence/architecture/qa_review_hardware_realism_proposal.md
  sha256: df3db0adf20bb9cc240b1bf144ce050d3a77a5c0fb6e104b2578a5b936a91ae5
  revision: 1
read_sources:
- soc-ap/services/ui_gateway/ui_gateway_http.cpp
- soc-ap/services/ui_gateway/ui_gateway_job_ctrl.cpp
- soc-ap/services/ui_gateway/ui_gateway_server.cpp
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
  - soc-ap/services/ui_gateway/ui_gateway_http.cpp
  - soc-ap/services/ui_gateway/ui_gateway_job_ctrl.cpp
  - soc-ap/services/ui_gateway/ui_gateway_server.cpp
  - soc-ap/tests/ui_gateway/test_ui_gateway.cpp
  record: docs/evidence/twin/TWIN-38/runs/<actual-run>/result.md
rollback:
  steps:
  - 仅回退本票候选；保存失败证据和原状态
handoff:
  receiver_role: COORD
  receiver_session: session-coord-autorun
  transport: docs
  evidence_location: docs/evidence/twin/TWIN-38
  acknowledgement: null
verification:
  commands:
  - id: check_graph
    cwd: .
    command: PYTHONDONTWRITEBYTECODE=1 python3 project-control/tools/check_task_graph.py --workspace .
    expected: 结构无错误
    availability: local
  positive_cases:
  - 彻底移除 ui_gateway_http.cpp 中默认假 ONLINE 填充逻辑
  - 物理离线时拒绝 /api/v1/motion/jog, home, level 并返回 HTTP 503
  - 物理离线时拒绝 /api/v1/job/start 并返回 HTTP 503
  - 废除本地纯定时器空跑进度，作业推进必须依赖底层反馈，无ACK/超时立即暂停
  - 打印过程中若 MC 离线，作业在 1 tick 内进入 PAUSED 并记录 LINK_LOST_STOP_UNKNOWN
  negative_cases:
  - 严禁断线后继续输出假成功 200 OK
  - 严禁断网后作业在后台虚假推进进度
  - 严禁在未收到 MC ACK 的情况下推进打印行号与倒计时
required_evidence_level: server-sandbox-and-independent-review
verification_environment: docker-qa-sandbox-and-isolated-codex
qa_review_policy: project-control/.agents/rules/codex_qa_review.md
updated: '2026-10-31T18:40:00+08:00'
---

# TWIN-38 ui_gateway链路感知、下线安全阻断与作业紧急挂起

## 任务目标
由 ENG-STATE 落实网关层下线安全阻断。移除 `ui_gateway_http.cpp` 中默认假 `ONLINE`；当 MC 或 TH 处于离线状态时，所有轴移动、调平与作业启动请求严格返回 HTTP 503 Service Unavailable；当打印作业执行循环中发现硬件离线时，作业立即挂起为 `PAUSED`（子原因 `LINK_LOST / STOP_UNKNOWN`），停止后续指令投递。
