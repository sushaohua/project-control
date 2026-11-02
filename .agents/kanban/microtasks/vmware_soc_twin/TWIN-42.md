---
id: TWIN-42
title: TWIN-42 多模块系统集成阶段单功能穿透梳理与级联验证
revision: 1
plan_revision: vmware-soc-twin-20261029
task_kind: integration
development_stage: vmware-twin
dispatchable: true
status: Review
blocked: false
planning_status: planned
owner: INTEGRATOR
proposed_owner: INTEGRATOR
executor:
  role: INTEGRATOR
  agent_id: session-integrator-twin-42
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
    planned_session_alias: planned-qa-twin-42
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
    planned_session_alias: planned-arch-twin-42
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
- TASK-005
- TASK-009
depends_on:
- TWIN-35
- TWIN-40
- TWIN-41
dependency_conditions:
- task: TWIN-35
  accepted_version: soc-ap=2e19a4242699e3a6a9be5c483d72b2260ffc3dd2; project-control=c6eb49339794cb150fbf9e6584be6e63dc366f60
  acceptance_evidence: docs/evidence/twin/TWIN-35/runs/run_01/qa_review_report.md
  required: 继承TWIN-35端到端打印闭环基础
- task: TWIN-40
  accepted_version: soc-ap=3ff4b144ef4d8c695b5f56d0996524adad0e644c; project-control=afd525946602c973d52feedcf7364f77ab2d221c
  acceptance_evidence: docs/evidence/twin/TWIN-40/runs/run_01/qa_review_report.md
  required: 继承TWIN-40热插拔集成闭环基线
- task: TWIN-41
  accepted_version: project-control=afd525946602c973d52feedcf7364f77ab2d221c
  acceptance_evidence: docs/evidence/twin/TWIN-41/runs/run_01/qa_review_report.md
  required: 消费TWIN-41单功能全流程时序闭环与协议映射
scope_status: mapped
allowed_repositories:
- project-control
- soc-ap
write_scope:
  project-control:
  - docs/evidence/twin/TWIN-42/**
allowed_paths:
- project-control/docs/evidence/twin/TWIN-42/**
source_baseline:
  project-control: afd525946602c973d52feedcf7364f77ab2d221c
  soc-ap: 3ff4b144ef4d8c695b5f56d0996524adad0e644c
  mcu-p3: 04231388c842c1ce3e5b71675d0dc118a65edf2e
  test_harness: 0b7497ba43158841eb3c4af7f16e477b9c30c2c5
base_commit: afd525946602c973d52feedcf7364f77ab2d221c
candidate_commit: cb59514a74ccbde68832b12f4340114bc6645b55
dispatch_binding:
  source_commit: afd525946602c973d52feedcf7364f77ab2d221c
  workspace_diff_sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
  consumed_artifact_versions: {}
protocol_input:
  path: project-control/docs/evidence/architecture/qa_review_hardware_realism_proposal.md
  sha256: df3db0adf20bb9cc240b1bf144ce050d3a77a5c0fb6e104b2578a5b936a91ae5
  revision: 1
read_sources:
- soc-ap/tests/integration/test_first_release_print_loop.c
worktree: project-control
lease: null
resources:
- resource: integrator-twin-env
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
  - project-control/docs/evidence/twin/TWIN-42/runs/author_01/feature_by_feature_penetration_matrix.md
  record: docs/evidence/twin/TWIN-42/runs/author_01/result.md
rollback:
  steps:
  - 仅回退本票候选；保存失败证据和原状态
handoff:
  receiver_role: COORD
  receiver_session: session-coord-autorun
  transport: docs
  evidence_location: docs/evidence/twin/TWIN-42
  acknowledgement: null
verification:
  commands:
  - id: check_graph
    cwd: .
    command: PYTHONDONTWRITEBYTECODE=1 python3 project-control/tools/check_task_graph.py --workspace .
    expected: 结构无错误
    availability: local
  positive_cases:
  - 按单功能维度逐个执行端到端穿透验证，产出 10 大功能的穿透验证闭环矩阵
  - 每个功能均通过正向闭环、无 ACK 超时阻断、带 Sequence 报错核实
  - 关键运控功能在执行中经受物理拔线测试，CPU 保持正常（<= 2%），UI 准确阻断
  - 热插拔恢复后具备自愈重连验证记录
  negative_cases:
  - 严禁采用全系统一次性总装黑盒测试替代单功能垂直穿透
  - 严禁忽略任何功能的无 ACK 超时与断线测试
required_evidence_level: server-sandbox-and-independent-review
verification_environment: vmware-twin-and-docker-sandbox
qa_review_policy: project-control/.agents/rules/codex_qa_review.md
updated: '2026-10-31T19:30:00+08:00'
---

# TWIN-42 多模块系统集成阶段单功能穿透梳理与级联验证

## 1. 任务背景与目标
针对传统“多模块一次性集成导致故障原因互相掩盖”的弊端，由 INTEGRATOR 依据 `TWIN-41` 架构时序规范，在真实环境（VMware Twin / SoC 台架）实施**按“单功能”逐个穿透梳理与级联集成验证**：
1. **一个功能一个功能地梳理验证**：
   - 不再将所有子服务混在一起一把抓，而是按 Feature 切片依次验证；
   - 依次穿透：遥测心跳 -> Jog轴动 -> 归零 -> 调平 -> 打印流控 -> 混色 -> E-STOP -> HMS告警 -> OOBE -> mDNS。
2. **四维立体测试判据（每个功能必须经历 4 关）**：
   - 关卡 1【正向闭环】：Web 操作 -> 下行到 MCU -> 真实执行 -> ACK 逐级回传 -> 前端状态更新；
   - 关卡 2【无 ACK 拦截】：模拟 MCU 丢 ACK，验证系统是否准确在超时窗口内阻断，并向前端抛出带 `Sequence ID` 的错误弹窗；
   - 关卡 3【物理热插拔破坏性测试】：在该功能执行期间拔除物理串口，验证 CPU 保持平稳（$\le 2\%$），系统在 3s 内衰退至 `OFFLINE`，前端锁定按钮；
   - 关卡 4【自愈与断点恢复】：插回串口后，系统能否正确重新握手，作业是否保持 `PAUSED` 可继续状态。

## 2. 交付成果
- 交付文档：[`project-control/docs/evidence/twin/TWIN-42/runs/author_01/feature_by_feature_penetration_matrix.md`](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/evidence/twin/TWIN-42/runs/author_01/feature_by_feature_penetration_matrix.md)
- 包含每个功能的穿透测试记录、波形抓包/日志抓取物证及 QA 签署。
