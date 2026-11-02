---
id: TWIN-41
title: TWIN-41 架构拆解阶段端到端单功能全流程闭环梳理与协议映射
revision: 1
plan_revision: vmware-soc-twin-20261029
task_kind: architecture
development_stage: vmware-twin
dispatchable: true
status: Review
blocked: false
planning_status: planned
owner: ARCH
proposed_owner: ARCH
executor:
  role: ARCH
  agent_id: session-arch-twin-41
  run_id: author_01
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
    planned_session_alias: planned-qa-twin-41
    session: session-qa-twin-41
    session_evidence: docs/evidence/twin/TWIN-41/runs/qa_01/qa_review_report.md
    decision: APPROVED
    reviewed_task_revision: 1
    artifact_version: project-control=001bef072dc5195ab64ef51099b0027ca6e5e413
    evidence: docs/evidence/twin/TWIN-41/runs/qa_01/qa_review_report.md
    report_sha256: e83ccfe82869ec550acda5e43efc8964fccb4b40a3eb550bf278b694a1cda2e4
  - role: ARCH
    platform: codex
    model: gpt-6-luna
    planned_session_alias: planned-arch-twin-41
    session: null
    session_evidence: null
    decision: PENDING
    reviewed_task_revision: 1
    artifact_version: null
    evidence: null
    report_sha256: null
  verifier_session: null
  integrator_session: null
primary_work_package: TASK-005
related_work_packages:
- TASK-008
- TASK-010
depends_on:
- TWIN-01
- TWIN-08
- TWIN-20
dependency_conditions:
- task: TWIN-01
  accepted_version: soc-ap=f2596515c0e1e92d6e4b85dae921d78ea15a9937; project-control=31818a7c2e35a1cb943d674cb2eeb1d36d3969fb
  acceptance_evidence: docs/evidence/twin/TWIN-01/runs/run_01/qa_review_report.md
  required: 继承TWIN-01 AP-MCU通信协议基线
- task: TWIN-08
  accepted_version: soc-ap=f2596515c0e1e92d6e4b85dae921d78ea15a9937; project-control=31818a7c2e35a1cb943d674cb2eeb1d36d3969fb
  acceptance_evidence: docs/evidence/twin/TWIN-08/runs/run_01/qa_review_report.md
  required: 继承TWIN-08状态机骨架
- task: TWIN-20
  accepted_version: soc-ap=409846a5ce6c1b1d6115736e7129a71d85ebe875; project-control=afd525946602c973d52feedcf7364f77ab2d221c
  acceptance_evidence: docs/evidence/twin/TWIN-20/runs/run_01/qa_review_report.md
  required: 继承TWIN-20前端HMI功能骨架
scope_status: mapped
allowed_repositories:
- project-control
write_scope:
  project-control:
  - docs/architecture/**
  - docs/evidence/twin/TWIN-41/**
allowed_paths:
- project-control/docs/architecture/**
- project-control/docs/evidence/twin/TWIN-41/**
source_baseline:
  project-control: afd525946602c973d52feedcf7364f77ab2d221c
  soc-ap: 3ff4b144ef4d8c695b5f56d0996524adad0e644c
  mcu-p3: 04231388c842c1ce3e5b71675d0dc118a65edf2e
  test_harness: 0b7497ba43158841eb3c4af7f16e477b9c30c2c5
base_commit: afd525946602c973d52feedcf7364f77ab2d221c
candidate_commit: 001bef072dc5195ab64ef51099b0027ca6e5e413
dispatch_binding:
  source_commit: afd525946602c973d52feedcf7364f77ab2d221c
  workspace_diff_sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
  consumed_artifact_versions: {}
protocol_input:
  path: project-control/docs/evidence/architecture/qa_review_hardware_realism_proposal.md
  sha256: df3db0adf20bb9cc240b1bf144ce050d3a77a5c0fb6e104b2578a5b936a91ae5
  revision: 1
read_sources:
- soc-ap/contracts/twin/telemetry_types.h
- soc-ap/contracts/twin/job/job_types.h
worktree: project-control
lease: null
resources:
- resource: arch-doc-env
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
  - project-control/docs/architecture/end_to_end_feature_flow_closed_loop_matrix.md
  record: docs/evidence/twin/TWIN-41/runs/<actual-run>/result.md
rollback:
  steps:
  - 仅回退本票候选；保存失败证据和原状态
handoff:
  receiver_role: COORD
  receiver_session: session-coord-autorun
  transport: docs
  evidence_location: docs/evidence/twin/TWIN-41
  acknowledgement: null
verification:
  commands:
  - id: check_graph
    cwd: .
    command: PYTHONDONTWRITEBYTECODE=1 python3 project-control/tools/check_task_graph.py --workspace .
    expected: 结构无错误
    availability: local
  positive_cases:
  - 逐一梳理 10 大核心功能的端到端时序流（L5 Web -> L4 UI Gateway -> L3 Device Manager -> L2 Forward -> L1 MCU）
  - 明确每个功能的下行请求帧、上行 ACK 帧配对与序列号校验规则
  - 定义每个功能的超时预算、丢包重试策略与带 Sequence ID 结构化报错机制
  - 规范物理断连时的降级状态机流转与自愈同步机制
  negative_cases:
  - 严禁存在无 ACK 绑定的“发后即忘”开环功能
  - 严禁存在由本地定时器假跑的空跑时钟业务流
required_evidence_level: document-review
verification_environment: local-and-independent-codex
qa_review_policy: project-control/.agents/rules/codex_qa_review.md
updated: '2026-10-31T19:30:00+08:00'
---

# TWIN-41 架构拆解阶段端到端单功能全流程闭环梳理与协议映射

## 1. 任务背景与目标
针对多模块系统集成时容易出现的“各模块自说自话、开环假跑、异常吃报错”的系统性顽疾，由系统架构师（ARCH）在架构拆解阶段建立**以“单功能”为维度的端到端全流程闭环时序与映射规范**：
1. 抛弃以往“按模块静态罗列”的传统文档结构，改为按“用户核心业务功能（Feature Slice）”逐个垂直切片梳理；
2. 逐一梳理 10 大核心功能：
   - 功能 1：喷嘴/热床双温遥测与固件心跳
   - 功能 2：CoreXY 触控微步 Jog 运动
   - 功能 3：全轴归零 G28
   - 功能 4：5x5 自动调平网格校准 G29
   - 功能 5：打印作业流流式下发与执行推进
   - 功能 6：4 通道混色配置与权重校验
   - 功能 7：紧急急停 E-STOP 注入与硬锁存
   - 功能 8：全机 HMS 错误码上报与严重度分级
   - 功能 9：开箱引导向导 OOBE 硬件状态读取
   - 功能 10：mDNS 局域网服务发现与直连
3. 对每个功能明确标定：
   - 下行数据流与 Sequence ID 规则；
   - 物理 MCU 执行与显式 ACK 配对帧；
   - 超时计时器门限（Timeout Budget）；
   - 无 ACK / 校验失败时的异常抛出链条（带 Sequence ID）；
   - 物理拔线/通信中断时的降级阻断与自愈同步机制。

## 2. 交付成果
- 交付文档：[`project-control/docs/architecture/end_to_end_feature_flow_closed_loop_matrix.md`](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/architecture/end_to_end_feature_flow_closed_loop_matrix.md)
- 包含 10 大功能的 Mermaid 端到端时序图与字段映射表。
