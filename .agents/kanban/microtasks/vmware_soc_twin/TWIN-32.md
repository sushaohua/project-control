---
id: TWIN-32
title: TWIN-32 ui_gateway作业管理与手动运控REST API扩展
revision: 1
plan_revision: vmware-soc-twin-20261029
task_kind: implementation
development_stage: vmware-twin
dispatchable: true
status: Backlog
blocked: false
planning_status: planned
owner: null
proposed_owner: ENG-NET
executor:
  role: ENG-NET
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
    planned_session_alias: planned-qa-twin-32
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
    planned_session_alias: planned-arch-twin-32
    session: null
    session_evidence: null
    decision: PENDING
    reviewed_task_revision: 1
    artifact_version: null
    evidence: null
    report_sha256: null
  verifier_session: null
  integrator_session: null
primary_work_package: TASK-011
related_work_packages:
- TASK-009
- TASK-010
depends_on:
- TWIN-09
- TWIN-23
- TWIN-30
dependency_conditions:
- task: TWIN-09
  accepted_version: soc-ap=d214ded82447502944a41d2b27194245b0f96b19; project-control=754b188b312ac79e2873ea97075b8a2a74937ecc
  acceptance_evidence: docs/evidence/twin/TWIN-09/runs/run_01/qa_review_report.md
  required: 继承TWIN-09 ui_gateway HTTP/SSE服务骨架
- task: TWIN-23
  accepted_version: soc-ap=674e7336f924c2f297c439417a0011adc12427fa; project-control=e097299f1483d5192f3319996fa3008901f27613
  acceptance_evidence: docs/evidence/twin/TWIN-23/runs/run_01/qa_review_report.md
  required: 继承TWIN-23作业执行器与快照规范
- task: TWIN-30
  accepted_version: soc-ap=7bb05218c39d6852cac5e8d86db845dbbedd7064; project-control=f7d18c48774a8787f0dfa1d1cbe9dddea9309a40
  acceptance_evidence: docs/evidence/twin/TWIN-30/runs/run_01/qa_review_report.md
  required: 继承TWIN-30集成基线与选项A安全门禁
scope_status: mapped
allowed_repositories:
- soc-ap
- project-control
write_scope:
  soc-ap:
  - services/ui_gateway/**
  - tests/ui_gateway/**
  project-control:
  - docs/evidence/twin/TWIN-32/**
allowed_paths:
- soc-ap/services/ui_gateway/**
- soc-ap/tests/ui_gateway/**
- project-control/docs/evidence/twin/TWIN-32/**
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
- soc-ap/contracts/twin/job/job_executor.h
- project-control/.agents/rules/c_cpp_coding_standard.md
worktree: soc-ap
lease: null
resources:
- resource: gateway-build-env
  location: null
  exclusive: true
  pending: Ready前落实
budget:
  planned_checkpoint_minutes: 60
  max_evidence_based_corrections: 2
  on_limit: 保存证据交COORD
checkpoint: 开工前绑定；接口自检；双独立沙箱检查；收件
execution_contract: project-control/docs/planning/vmware_soc_twin_task_execution_20261029.md
readiness_pending: []
deliverables:
  artifacts:
  - soc-ap/services/ui_gateway/ui_gateway_server.cpp
  - soc-ap/tests/ui_gateway/twin/test_ui_gateway.cpp
  record: docs/evidence/twin/TWIN-32/runs/<actual-run>/result.md
rollback:
  steps:
  - 仅回退本票候选；保存失败证据和原状态
handoff:
  receiver_role: COORD
  receiver_session: session-coord-autorun
  transport: docs
  evidence_location: docs/evidence/twin/TWIN-32
  acknowledgement: null
verification:
  commands:
  - id: check_graph
    cwd: .
    command: PYTHONDONTWRITEBYTECODE=1 python3 project-control/tools/check_task_graph.py --workspace .
    expected: 结构无错误
    availability: local
  positive_cases:
  - 实现 POST /api/v1/jobs/upload 接收 G-code 文件流并落盘
  - 实现 GET /api/v1/jobs/list 导出模型列表及内置样例
  - 实现 POST /api/v1/jobs/start, pause, resume, cancel 生命周期控制
  - 实现 GET /api/v1/jobs/status 导出 128B 快照
  - 实现 POST /api/v1/motion/jog 与 /api/v1/motion/home 运控接口
  - 严格遵守 C/C++ 规范：函数 <= 50 行，参数 <= 4，Guard Clause 首行
  negative_cases:
  - 严禁违背 Option A 强电锁死
  - 非法路径穿越上传必须防御拒绝
required_evidence_level: server-sandbox-and-independent-review
verification_environment: docker-qa-sandbox-and-isolated-codex
qa_review_policy: project-control/.agents/rules/codex_qa_review.md
updated: '2026-10-31T17:30:00+08:00'
---

# TWIN-32 ui_gateway作业管理与手动运控REST API扩展

## 任务目标
由 ENG-NET（网络与文件接入工程师）为 `ui_gateway` 扩展作业控制、模型文件上传与手动运控 REST API，为前端 HMI 提供完整的数据通道。
