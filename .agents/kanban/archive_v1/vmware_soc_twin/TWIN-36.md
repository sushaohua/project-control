---
id: TWIN-36
title: TWIN-36 forward_service串口挂起感知与优雅关闭
revision: 1
plan_revision: vmware-soc-twin-20261029
task_kind: implementation
development_stage: vmware-twin
dispatchable: true
status: Review
blocked: false
planning_status: planned
owner: null
proposed_owner: ENG-FWD
executor:
  role: ENG-FWD
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
    planned_session_alias: planned-qa-twin-36
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
    planned_session_alias: planned-arch-twin-36
    session: null
    session_evidence: null
    decision: PENDING
    reviewed_task_revision: 1
    artifact_version: null
    evidence: null
    report_sha256: null
  verifier_session: null
  integrator_session: null
primary_work_package: TASK-007
related_work_packages:
- TASK-008
- TASK-010
depends_on:
- TWIN-07
- TWIN-27
- TWIN-29
dependency_conditions:
- task: TWIN-07
  accepted_version: soc-ap=f2596515c0e1e92d6e4b85dae921d78ea15a9937; project-control=31818a7c2e35a1cb943d674cb2eeb1d36d3969fb
  acceptance_evidence: docs/evidence/twin/TWIN-07/runs/run_01/qa_review_report.md
  required: 继承TWIN-07 forward_service串口基础
- task: TWIN-27
  accepted_version: soc-ap=c0f75727e4e11cb93d395a1ee5aa7dc34c2ae2b1; project-control=ef0f40d4187f5492d5cfa3fbf9100407a1649983
  acceptance_evidence: docs/evidence/twin/TWIN-27/runs/run_01/qa_review_report.md
  required: 继承TWIN-27真实串口通信闭环
- task: TWIN-29
  accepted_version: soc-ap=5bf71be8d5d4d38e217d83296c039dbfb3ba5c67; project-control=15ff7c9c0543e06e7887ef4668b577317b9b1689
  acceptance_evidence: docs/evidence/twin/TWIN-29/runs/run_02/qa_review_report.md
  required: 继承TWIN-29固件版本与状态协议
scope_status: mapped
allowed_repositories:
- soc-ap
- project-control
write_scope:
  soc-ap:
  - services/forward/**
  - tests/forward/**
  project-control:
  - docs/evidence/twin/TWIN-36/**
allowed_paths:
- soc-ap/services/forward/**
- soc-ap/tests/forward/**
- project-control/docs/evidence/twin/TWIN-36/**
source_baseline:
  project-control: afd525946602c973d52feedcf7364f77ab2d221c
  soc-ap: 409846a5ce6c1b1d6115736e7129a71d85ebe875
  mcu-p3: 04231388c842c1ce3e5b71675d0dc118a65edf2e
  test_harness: 0b7497ba43158841eb3c4af7f16e477b9c30c2c5
base_commit: 409846a5ce6c1b1d6115736e7129a71d85ebe875
candidate_commit: 3ff4b144ef4d8c695b5f56d0996524adad0e644c
dispatch_binding:
  source_commit: 409846a5ce6c1b1d6115736e7129a71d85ebe875
  workspace_diff_sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
  consumed_artifact_versions: {}
protocol_input:
  path: project-control/docs/evidence/architecture/qa_review_hardware_realism_proposal.md
  sha256: df3db0adf20bb9cc240b1bf144ce050d3a77a5c0fb6e104b2578a5b936a91ae5
  revision: 1
read_sources:
- soc-ap/core/forward/transport/serial_posix.cpp
- soc-ap/services/forward/forward_uart.cpp
- soc-ap/services/forward/forward_service.cpp
worktree: soc-ap
lease: null
resources:
- resource: forward-build-env
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
  - soc-ap/services/forward/forward_uart.cpp
  - soc-ap/services/forward/forward_service.cpp
  - soc-ap/tests/forward/twin/test_forward_service.cpp
  record: docs/evidence/twin/TWIN-36/runs/<actual-run>/result.md
rollback:
  steps:
  - 仅回退本票候选；保存失败证据和原状态
handoff:
  receiver_role: COORD
  receiver_session: session-coord-autorun
  transport: docs
  evidence_location: docs/evidence/twin/TWIN-36
  acknowledgement: null
verification:
  commands:
  - id: check_graph
    cwd: .
    command: PYTHONDONTWRITEBYTECODE=1 python3 project-control/tools/check_task_graph.py --workspace .
    expected: 结构无错误
    availability: local
  positive_cases:
  - 捕获 serial_read 返回 false 与 POLLHUP 状态
  - 立即优雅关闭失效 fd 并设置 is_open = false
  - 消除 100% CPU 忙循环
  - 凡发指令必有对应 ACK 校验，超时未收 ACK 严格报错返回
  - 广播 D-Bus LinkStateChanged(node_id, is_connected=false)
  negative_cases:
  - 严禁忽略 read 错误码继续重试
  - 严禁多线程并发 close/open
  - 严禁下发指令后未收到 MC ACK 假定成功或静默丢弃
required_evidence_level: server-sandbox-and-independent-review
verification_environment: docker-qa-sandbox-and-isolated-codex
qa_review_policy: project-control/.agents/rules/codex_qa_review.md
updated: '2026-10-31T18:40:00+08:00'
---

# TWIN-36 forward_service串口挂起感知与优雅关闭

## 任务目标
由 ENG-FWD 修复 `forward_uart.cpp` 中的忙循环缺陷。严格检查 `serial_read` 返回值，捕获 `POLLHUP | POLLERR` 时立即关闭失效文件描述符，将 `is_open` 设为 `false`，彻底消灭 CPU 100% 忙循环，并通过 D-Bus 广播链路断开信号。
