---
id: TWIN-37
title: TWIN-37 device_manager新鲜度老化激活与真实下线状态机
revision: 1
plan_revision: vmware-soc-twin-20261029
task_kind: implementation
development_stage: vmware-twin
dispatchable: true
status: Review
blocked: false
planning_status: planned
owner: null
proposed_owner: ENG-DEVICE
executor:
  role: ENG-DEVICE
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
    planned_session_alias: planned-qa-twin-37
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
    planned_session_alias: planned-arch-twin-37
    session: null
    session_evidence: null
    decision: PENDING
    reviewed_task_revision: 1
    artifact_version: null
    evidence: null
    report_sha256: null
  verifier_session: null
  integrator_session: null
primary_work_package: TASK-008
related_work_packages:
- TASK-007
- TASK-010
depends_on:
- TWIN-08
- TWIN-18
- TWIN-36
dependency_conditions:
- task: TWIN-08
  accepted_version: soc-ap=f2596515c0e1e92d6e4b85dae921d78ea15a9937; project-control=31818a7c2e35a1cb943d674cb2eeb1d36d3969fb
  acceptance_evidence: docs/evidence/twin/TWIN-08/runs/run_01/qa_review_report.md
  required: 继承TWIN-08 device_manager状态机骨架
- task: TWIN-18
  accepted_version: soc-ap=cb70d59e949396f45aec94d33ae23cab75beb282; project-control=f0fe3948482adb71e5366006850fdb9dd36282bc
  acceptance_evidence: docs/evidence/twin/TWIN-18/runs/run_01/qa_review_report.md
  required: 继承TWIN-18遥测汇聚与D-Bus快照
- task: TWIN-36
  accepted_version: soc-ap=409846a5ce6c1b1d6115736e7129a71d85ebe875; project-control=afd525946602c973d52feedcf7364f77ab2d221c
  acceptance_evidence: docs/evidence/twin/TWIN-36/runs/run_01/qa_review_report.md
  required: 继承TWIN-36串口链路挂起信号
scope_status: mapped
allowed_repositories:
- soc-ap
- project-control
write_scope:
  soc-ap:
  - services/device_manager/**
  - tests/device_manager/**
  project-control:
  - docs/evidence/twin/TWIN-37/**
allowed_paths:
- soc-ap/services/device_manager/**
- soc-ap/tests/device_manager/**
- project-control/docs/evidence/twin/TWIN-37/**
source_baseline:
  project-control: afd525946602c973d52feedcf7364f77ab2d221c
  soc-ap: 409846a5ce6c1b1d6115736e7129a71d85ebe875
  mcu-p3: 04231388c842c1ce3e5b71675d0dc118a65edf2e
  test_harness: 0b7497ba43158841eb3c4af7f16e477b9c30c2c5
base_commit: 409846a5ce6c1b1d6115736e7129a71d85ebe875
candidate_commit: b373fe02f741584dbf35542dd7a393961efd4d42
dispatch_binding:
  source_commit: 409846a5ce6c1b1d6115736e7129a71d85ebe875
  workspace_diff_sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
  consumed_artifact_versions: {}
protocol_input:
  path: project-control/docs/evidence/architecture/qa_review_hardware_realism_proposal.md
  sha256: df3db0adf20bb9cc240b1bf144ce050d3a77a5c0fb6e104b2578a5b936a91ae5
  revision: 1
read_sources:
- soc-ap/services/device_manager/device_manager_service.cpp
- soc-ap/services/device_manager/device_manager_state.cpp
- soc-ap/services/device_manager/device_manager_dbus.cpp
worktree: soc-ap
lease: null
resources:
- resource: device-build-env
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
  - soc-ap/services/device_manager/device_manager_service.cpp
  - soc-ap/services/device_manager/device_manager_state.cpp
  - soc-ap/tests/device_manager/twin/test_device_manager.cpp
  record: docs/evidence/twin/TWIN-37/runs/<actual-run>/result.md
rollback:
  steps:
  - 仅回退本票候选；保存失败证据和原状态
handoff:
  receiver_role: COORD
  receiver_session: session-coord-autorun
  transport: docs
  evidence_location: docs/evidence/twin/TWIN-37
  acknowledgement: null
verification:
  commands:
  - id: check_graph
    cwd: .
    command: PYTHONDONTWRITEBYTECODE=1 python3 project-control/tools/check_task_graph.py --workspace .
    expected: 结构无错误
    availability: local
  positive_cases:
  - 废除开机时默认预设 MC/TH 为 ONLINE 的假在线逻辑
  - 在主分发循环中强制调度 dev_state_eval_version_freshness (5s/15s)
  - 收到断开信号或超时后，温度数值覆盖为 SENTINEL_OFFLINE，整机与节点切为 OFFLINE
  - 广播 D-Bus SnapshotUpdated 信号
  negative_cases:
  - 严禁断线后继续输出最后一次历史正常温度
  - 严禁覆盖更高优先级的锁存故障
required_evidence_level: server-sandbox-and-independent-review
verification_environment: docker-qa-sandbox-and-isolated-codex
qa_review_policy: project-control/.agents/rules/codex_qa_review.md
updated: '2026-10-31T18:40:00+08:00'
---

# TWIN-37 device_manager新鲜度老化激活与真实下线状态机

## 任务目标
由 ENG-DEVICE 废除 `init_default_mcu_versions` 中默认 `ONLINE` 的假在线初态；在主调度循环中强制激活 `dev_state_eval_version_freshness`，并在接收到物理拔线或心跳超时时，将温度打入 `SENTINEL_OFFLINE`，设备状态置为 `OFFLINE`，广播更新快照。
