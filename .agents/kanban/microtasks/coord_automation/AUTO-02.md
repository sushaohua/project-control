---
id: AUTO-02
title: AUTO-02 COORD逐卡执行循环与恢复适配
revision: 1
plan_revision: coord-server-sandbox-20261029
task_kind: implementation
development_stage: cross-stage
dispatchable: true
status: InProgress
blocked: false
planning_status: in-progress
owner: 0e0e4b90-2aeb-42d4-abc2-13ed9198e8f0
proposed_owner: INTEGRATOR
executor:
  role: INTEGRATOR
  agent_id: 0e0e4b90-2aeb-42d4-abc2-13ed9198e8f0
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
    planned_session_alias: planned-qa-auto-02
    session: 3118e0b6-e82d-4f88-8b22-512cd6451293
    session_evidence: null
    decision: null
    reviewed_task_revision: null
    artifact_version: null
    evidence: null
    report_sha256: null
  - role: ARCH
    platform: codex
    model: gpt-6-luna
    planned_session_alias: planned-arch-auto-02
    session: f559672c-e3ca-4bb1-8b4a-a87d321a1a27
    session_evidence: null
    decision: null
    reviewed_task_revision: null
    artifact_version: null
    evidence: null
    report_sha256: null
  verifier_session: null
  integrator_session: null
primary_work_package: TASK-010
related_work_packages: []
depends_on:
- AUTO-01
dependency_conditions:
- task: AUTO-01
  accepted_version: 1
  acceptance_evidence: docs/evidence/coord_automation/AUTO-01/runs/run_01/result.md
  required: 绑定准确服务器候选、真实运行器与独立接受
scope_status: mapped
allowed_repositories:
- project-control
write_scope:
  project-control:
  - tools/coord_runner/**
  - config/coord_runner/**
  - tools/coord_queue.py
  - docs/evidence/coord_automation/AUTO-02/**
allowed_paths:
- project-control/tools/coord_runner/**
- project-control/config/coord_runner/**
- project-control/tools/coord_queue.py
- project-control/docs/evidence/coord_automation/AUTO-02/**
source_baseline:
  project-control: a5e4b5e97439cae4a7093d1d0a29c5dc9b3c7819
  soc-ap: 4445c8fedc21bafef5e6c971fcb54cec703f0e71
  mcu-p3: 1246ea9cb441d074ea444f53320f5632fefcd503
  test_harness: 6c61ce6e51cf83d7fb58d319c23cb91bf95786cb
base_commit: 896024edec58a8a6552bb776766d3a95bb849206
candidate_commit: null
dispatch_binding:
  source_commit: 896024edec58a8a6552bb776766d3a95bb849206
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
  owner: 0e0e4b90-2aeb-42d4-abc2-13ed9198e8f0
  task_revision: 1
  lease_id: lease_auto-02_20261029_01
  expires_at: '2026-10-29T20:00:00+08:00'
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
  - project-control/tools/coord_runner/**
  - project-control/config/coord_runner/**
  - project-control/tools/coord_queue.py
  record: docs/evidence/coord_automation/AUTO-02/runs/<actual-run>/result.md
rollback:
  steps:
  - 仅回退本票候选；保存失败证据和原状态；硬件恢复须按实际SOP及授权执行
handoff:
  receiver_role: COORD
  receiver_session: afd0a8cd-67b3-47cc-9cd2-a61f2973f496
  transport: tools.invoke_subagent
  evidence_location: docs/evidence/coord_automation/AUTO-02
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
    expected: 按依赖和实际资源拉起角色Agent，等待实际回执并调用AUTO-01独立QA；门禁通过收件后继续；保存游标并演练重启恢复
    availability: planned-not-runnable
  positive_cases:
  - 按依赖和实际资源拉起角色Agent，等待实际回执并调用AUTO-01独立QA；门禁通过收件后继续；保存游标并演练重启恢复
  negative_cases:
  - 虚假Done、同作者自批、服务端QA失败、并发抢UART、重复派单、会话中断或两次纠正仍失败时不得错误放行；未部署常驻模式不宣称后台续跑
required_evidence_level: server-sandbox-verified
verification_environment: independent-codex-in-server-based-sandbox
qa_review_policy: project-control/.agents/rules/codex_qa_review.md
updated: '2026-10-29T15:03:42+08:00'
delivery_gate_policy: project-control/.agents/rules/delivery_and_coord_gate.md
---

# AUTO-02 COORD逐卡执行循环与恢复适配

## 交付与验收

按依赖和实际资源拉起角色Agent，等待实际回执并调用AUTO-01独立QA；门禁通过收件后继续；保存游标并演练重启恢复。

负例：虚假Done、同作者自批、服务端QA失败、并发抢UART、重复派单、会话中断或两次纠正仍失败时不得错误放行；未部署常驻模式不宣称后台续跑。

本卡Backlog，未启动作者/QA或分配租约；实际服务器、凭据和现有发布授权先核实。新增自研函数≤50行、≤4参；依赖/生成/共享配置由单一Owner管理，禁止提交别人未审阅改动。当前检查工具只是读记录，可信服务端判定和实际隔离能力由本卡实现验证。

独立QA实际在新沙箱消费服务器锁定候选，QA报告由另一非作者复核；COORD核实真实服务端job和同一候选，收件后才推进。初次AUTO-01用可信系统工具独立准备QA环境，不以未受审启动器自证。失败保留原日志，回原作者，最多两次有证据纠正；HIL设备/固件操作按既有专项门禁，本文不授予额外权限。

[总控执行清单](../../../../docs/planning/coord_autorun_tasklist_20261029.md)
