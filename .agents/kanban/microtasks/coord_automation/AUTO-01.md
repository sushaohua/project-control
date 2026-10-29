---
id: AUTO-01
title: AUTO-01 服务器候选与独立Codex沙箱QA运行器
revision: 1
plan_revision: coord-server-sandbox-20261029
task_kind: implementation
development_stage: cross-stage
dispatchable: true
status: InProgress
blocked: false
planning_status: in-progress
owner: fad98376-ae68-4254-a199-e4d2983d21c5
proposed_owner: INTEGRATOR
executor:
  role: INTEGRATOR
  agent_id: fad98376-ae68-4254-a199-e4d2983d21c5
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
    planned_session_alias: planned-qa-auto-01
    session: planned-qa-auto-01
    session_evidence: null
    decision: null
    reviewed_task_revision: null
    artifact_version: null
    evidence: null
    report_sha256: null
  - role: ARCH
    platform: codex
    model: gpt-6-luna
    planned_session_alias: planned-arch-auto-01
    session: planned-arch-auto-01
    session_evidence: null
    decision: null
    reviewed_task_revision: null
    artifact_version: null
    evidence: null
    report_sha256: null
  verifier_session: null
  integrator_session: null
primary_work_package: TASK-004
related_work_packages: []
depends_on:
- CR-03
dependency_conditions:
- task: CR-03
  accepted_version: verified
  acceptance_evidence: docs/evidence/cascade_recovery_plan_20261027/README.md
  required: 工具历史基线与原范围仅作输入对账；新服务器沙箱能力另验，不继承历史通过
scope_status: mapped
allowed_repositories:
- project-control
- test_harness
write_scope:
  project-control:
  - tools/qa_runner/**
  - config/qa_runner/**
  - tools/delivery_checks.py
  - docs/evidence/coord_automation/AUTO-01/**
  test_harness:
  - runner/**
allowed_paths:
- project-control/tools/qa_runner/**
- project-control/config/qa_runner/**
- project-control/tools/delivery_checks.py
- project-control/docs/evidence/coord_automation/AUTO-01/**
- test_harness/runner/**
source_baseline:
  project-control: a5e4b5e97439cae4a7093d1d0a29c5dc9b3c7819
  soc-ap: 4445c8fedc21bafef5e6c971fcb54cec703f0e71
  mcu-p3: 1246ea9cb441d074ea444f53320f5632fefcd503
  test_harness: 6c61ce6e51cf83d7fb58d319c23cb91bf95786cb
base_commit: f48b21907ffbc7b24caf4d8e8afe994e7aeb9913
candidate_commit: null
dispatch_binding:
  source_commit: f48b21907ffbc7b24caf4d8e8afe994e7aeb9913
  workspace_diff_sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
  consumed_artifact_versions: {}
protocol_input:
  path: project-control/docs/specs/ap_mc_formal_protocol_v2_0_multidevice_routing_draft_20261015.md
  sha256: 9f8d4f9607cb3e76cc30b9ee2f971b23c3e0d936611188466a71f4aa15f3ce54
  revision: 2.0.3
read_sources:
- project-control/.agents/rules/delivery_and_coord_gate.md
- project-control/docs/planning/coord_autorun_tasklist_20261029.md
- project-control/.agents/rules/c_cpp_coding_standard.md
worktree: /home/sushaohua/workspace/ai_soc_project
lease:
  owner: fad98376-ae68-4254-a199-e4d2983d21c5
  task_revision: 1
  lease_id: lease_auto-01_20261029_01
  expires_at: '2026-10-29T18:00:00+08:00'
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
execution_contract: project-control/docs/planning/coord_autorun_tasklist_20261029.md
readiness_pending:
- 真实作者/独立检查者、有效租约、白名单工作区与输出待落实
- 服务器认证及实际runner/隔离/沙箱内Codex启动能力待核实，不把客户端名字当实现
- 开工时重新绑定准确候选、可执行命令及既有授权；不提交其他会话未审阅改动
deliverables:
  artifacts:
  - project-control/tools/qa_runner/**
  - project-control/config/qa_runner/**
  - project-control/tools/delivery_checks.py
  - test_harness/runner/**
  record: docs/evidence/coord_automation/AUTO-01/runs/<actual-run>/result.md
rollback:
  steps:
  - 仅回退本票候选；保存失败证据和原状态；硬件恢复须按实际SOP及授权执行
handoff:
  receiver_role: COORD
  receiver_session: afd0a8cd-67b3-47cc-9cd2-a61f2973f496
  transport: tools.invoke_subagent
  evidence_location: docs/evidence/coord_automation/AUTO-01
  acknowledgement: null
verification:
  commands:
  - id: check_graph
    cwd: .
    command: PYTHONDONTWRITEBYTECODE=1 python3 project-control/tools/check_task_graph.py --workspace .
    expected: 结构无错误，不代表运行器接受
    availability: local
  - id: planned_build_and_runner_acceptance
    cwd: .
    command: Ready前绑定实际运行器构建与正反例命令
    expected: 新沙箱从服务器锁定源码/工具/契约提交并重建；Codex实际在沙箱内运行；可信job/会话/源代码/隔离/日志绑定可复核
    availability: planned-not-runnable
  positive_cases:
  - 新沙箱从服务器锁定源码/工具/契约提交并重建；Codex实际在沙箱内运行；可信job/会话/源代码/隔离/日志绑定可复核
  negative_cases:
  - 未推送/缺commit、作者目录挂载、共享Git对象、脏覆盖、伪会话、沙箱逃逸或缺真实job必须拒绝；只按适用授权授予HIL设备
required_evidence_level: server-sandbox-verified
verification_environment: independent-codex-in-server-based-sandbox
qa_review_policy: project-control/.agents/rules/codex_qa_review.md
updated: '2026-10-29T15:03:42+08:00'
delivery_gate_policy: project-control/.agents/rules/delivery_and_coord_gate.md
---

# AUTO-01 服务器候选与独立Codex沙箱QA运行器

## 交付与验收

新沙箱从服务器锁定源码/工具/契约提交并重建；Codex实际在沙箱内运行；可信job/会话/源代码/隔离/日志绑定可复核。

负例：未推送/缺commit、作者目录挂载、共享Git对象、脏覆盖、伪会话、沙箱逃逸或缺真实job必须拒绝；只按适用授权授予HIL设备。

本卡Backlog，未启动作者/QA或分配租约；实际服务器、凭据和现有发布授权先核实。新增自研函数≤50行、≤4参；依赖/生成/共享配置由单一Owner管理，禁止提交别人未审阅改动。当前检查工具只是读记录，可信服务端判定和实际隔离能力由本卡实现验证。

独立QA实际在新沙箱消费服务器锁定候选，QA报告由另一非作者复核；COORD核实真实服务端job和同一候选，收件后才推进。初次AUTO-01用可信系统工具独立准备QA环境，不以未受审启动器自证。失败保留原日志，回原作者，最多两次有证据纠正；HIL设备/固件操作按既有专项门禁，本文不授予额外权限。

[总控执行清单](../../../../docs/planning/coord_autorun_tasklist_20261029.md)
