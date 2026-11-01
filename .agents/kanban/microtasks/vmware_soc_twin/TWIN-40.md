---
id: TWIN-40
title: TWIN-40 VMware虚拟机台架热插拔与状态闭环集成验证
revision: 1
plan_revision: vmware-soc-twin-20261029
task_kind: integration
development_stage: vmware-twin
dispatchable: true
status: Backlog
blocked: false
planning_status: planned
owner: INTEGRATOR
proposed_owner: INTEGRATOR
executor:
  role: INTEGRATOR
  agent_id: session-integrator
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
    planned_session_alias: planned-qa-twin-40
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
    planned_session_alias: planned-arch-twin-40
    session: null
    session_evidence: null
    decision: PENDING
    reviewed_task_revision: 1
    artifact_version: null
    evidence: null
    report_sha256: null
  verifier_session: null
  integrator_session: null
primary_work_package: TASK-010
related_work_packages:
- TASK-007
- TASK-008
- TASK-009
depends_on:
- TWIN-35
- TWIN-36
- TWIN-37
- TWIN-38
- TWIN-39
dependency_conditions:
- task: TWIN-35
  accepted_version: soc-ap=2e19a4242699e3a6a9be5c483d72b2260ffc3dd2; project-control=c6eb49339794cb150fbf9e6584be6e63dc366f60
  acceptance_evidence: docs/evidence/twin/TWIN-35/runs/run_01/qa_review_report.md
  required: 继承TWIN-35台架端到端打印闭环基础
- task: TWIN-36
  accepted_version: soc-ap=409846a5ce6c1b1d6115736e7129a71d85ebe875; project-control=afd525946602c973d52feedcf7364f77ab2d221c
  acceptance_evidence: docs/evidence/twin/TWIN-36/runs/run_01/qa_review_report.md
  required: 继承TWIN-36串口挂起感知
- task: TWIN-37
  accepted_version: soc-ap=409846a5ce6c1b1d6115736e7129a71d85ebe875; project-control=afd525946602c973d52feedcf7364f77ab2d221c
  acceptance_evidence: docs/evidence/twin/TWIN-37/runs/run_01/qa_review_report.md
  required: 继承TWIN-37状态机新鲜度老化
- task: TWIN-38
  accepted_version: soc-ap=409846a5ce6c1b1d6115736e7129a71d85ebe875; project-control=afd525946602c973d52feedcf7364f77ab2d221c
  acceptance_evidence: docs/evidence/twin/TWIN-38/runs/run_01/qa_review_report.md
  required: 继承TWIN-38网关离线拦截与503语义
- task: TWIN-39
  accepted_version: soc-ap=409846a5ce6c1b1d6115736e7129a71d85ebe875; project-control=afd525946602c973d52feedcf7364f77ab2d221c
  acceptance_evidence: docs/evidence/twin/TWIN-39/runs/run_01/qa_review_report.md
  required: 继承TWIN-39前端双状态指示与悬浮告警
scope_status: mapped
allowed_repositories:
- soc-ap
- project-control
write_scope:
  soc-ap:
  - tests/**
  project-control:
  - docs/evidence/twin/TWIN-40/**
allowed_paths:
- soc-ap/tests/**
- project-control/docs/evidence/twin/TWIN-40/**
source_baseline:
  project-control: afd525946602c973d52feedcf7364f77ab2d221c
  soc-ap: 409846a5ce6c1b1d6115736e7129a71d85ebe875
  mcu-p3: 04231388c842c1ce3e5b71675d0dc118a65edf2e
  test_harness: 0b7497ba43158841eb3c4af7f16e477b9c30c2c5
base_commit: 409846a5ce6c1b1d6115736e7129a71d85ebe875
candidate_commit: 5955fa57c9be6b90ff34156a1a6b183717f9a3a6
dispatch_binding:
  source_commit: 409846a5ce6c1b1d6115736e7129a71d85ebe875
  workspace_diff_sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
  consumed_artifact_versions: {}
protocol_input:
  path: project-control/docs/evidence/architecture/qa_review_hardware_realism_proposal.md
  sha256: df3db0adf20bb9cc240b1bf144ce050d3a77a5c0fb6e104b2578a5b936a91ae5
  revision: 1
read_sources:
- soc-ap/tests/integration/test_first_release_print_loop.c
worktree: soc-ap
lease: null
resources:
- resource: twin-integration-env
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
  - soc-ap/tests/integration/test_first_release_print_loop.c
  record: docs/evidence/twin/TWIN-40/runs/run_01/result.md
rollback:
  steps:
  - 仅回退本票候选；保存失败证据和原状态
handoff:
  receiver_role: COORD
  receiver_session: session-coord-autorun
  transport: docs
  evidence_location: docs/evidence/twin/TWIN-40
  acknowledgement: null
verification:
  commands:
  - id: check_graph
    cwd: .
    command: PYTHONDONTWRITEBYTECODE=1 python3 project-control/tools/check_task_graph.py --workspace .
    expected: 结构无错误
    availability: local
  positive_cases:
  - 拔出 /dev/ttyUSB 串口后 forward-service CPU 不超 2%
  - 3 秒内 device-manager 将硬件状态转为 OFFLINE
  - 运行中的作业立即进入 PAUSED 状态
  - Web HMI 界面显示黄色断开悬浮条并禁用运控按钮
  - 恢复连接后能够自愈恢复
  negative_cases:
  - 严禁出现 CPU 100% 忙循环
  - 严禁在硬件下线后界面继续空跑虚假打印进度
required_evidence_level: server-sandbox-and-independent-review
verification_environment: docker-qa-sandbox-and-isolated-codex
qa_review_policy: project-control/.agents/rules/codex_qa_review.md
updated: '2026-10-31T18:40:00+08:00'
---

# TWIN-40 VMware虚拟机台架热插拔与状态闭环集成验证

## 任务目标
由 INTEGRATOR 在 VMware SoC Twin 台架环境（`192.168.77.134:8080`）实施端到端热插拔全链路验证。验证物理拔除 `/dev/ttyUSB0` / `/dev/ttyUSB1` 串口后，`forward-service` 优雅关闭、CPU 平稳（$\le 2\%$）；`device-manager` 3 秒内新鲜度老化切入 `OFFLINE`；作业执行引擎立即挂起 (`PAUSED`)；Web HMI 及时呈现双状态与告警，彻底解决拔出串口后界面还在跑的系统级架构缺陷。
