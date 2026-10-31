---
id: TWIN-35
title: TWIN-35 VMware宿主机端到端Web界面操作打印闭环综合验收
revision: 1
plan_revision: vmware-soc-twin-20261029
task_kind: integration
development_stage: vmware-twin
dispatchable: true
status: Backlog
blocked: false
planning_status: planned
owner: null
proposed_owner: INTEGRATOR
executor:
  role: INTEGRATOR
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
    planned_session_alias: planned-qa-twin-35
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
    planned_session_alias: planned-arch-twin-35
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
- TASK-009
- TASK-011
depends_on:
- TWIN-33
- TWIN-34
dependency_conditions:
- task: TWIN-33
  accepted_version: soc-ap=ca6c40b2fdfc421ef628100f8b2d40fe64869d85
  acceptance_evidence: docs/evidence/twin/TWIN-33/runs/run_01/qa_review_report.md
  required: 继承TWIN-33打印工作台组件
- task: TWIN-34
  accepted_version: soc-ap=ca6c40b2fdfc421ef628100f8b2d40fe64869d85
  acceptance_evidence: docs/evidence/twin/TWIN-34/runs/run_01/qa_review_report.md
  required: 继承TWIN-34轴控与调平网格组件
scope_status: mapped
allowed_repositories:
- soc-ap
- project-control
write_scope:
  soc-ap:
  - tests/integration/**
  project-control:
  - docs/evidence/twin/TWIN-35/**
allowed_paths:
- soc-ap/tests/integration/**
- project-control/docs/evidence/twin/TWIN-35/**
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
- soc-ap/tests/integration/test_first_release_print_loop.c
worktree: soc-ap
lease: null
resources:
- resource: vmware-cluster-8080
  location: 192.168.77.134:8080
  exclusive: true
  pending: Ready前落实
budget:
  planned_checkpoint_minutes: 60
  max_evidence_based_corrections: 2
  on_limit: 保存证据交COORD
checkpoint: 开工前绑定；端到端集成测试自检；双独立沙箱检查；收件
execution_contract: project-control/docs/planning/vmware_soc_twin_task_execution_20261029.md
readiness_pending: []
deliverables:
  artifacts:
  - soc-ap/tests/integration/test_web_print_loop.py
  record: docs/evidence/twin/TWIN-35/runs/<actual-run>/result.md
rollback:
  steps:
  - 仅回退本票候选；保存失败证据和原状态
handoff:
  receiver_role: COORD
  receiver_session: session-coord-autorun
  transport: docs
  evidence_location: docs/evidence/twin/TWIN-35
  acknowledgement: null
verification:
  commands:
  - id: check_graph
    cwd: .
    command: PYTHONDONTWRITEBYTECODE=1 python3 project-control/tools/check_task_graph.py --workspace .
    expected: 结构无错误
    availability: local
  positive_cases:
  - 在 VMware 环境通过 Web 页面完整闭环执行一次本地打印（选模型->G28回零->流式空跑->监视->完成）
  - 验证网页端开始/暂停/继续/取消按钮与后台状态机同步
  - 验证网页端红色 E-STOP 紧急急停按钮即时熔断
  - 验证 5x5 调平热力图与手动轴控响应
  - 严格保持 Option A 强电 0% 锁死安全基线
  negative_cases:
  - 任何升温命令严禁输出到物理发热元件
required_evidence_level: server-sandbox-and-independent-review
verification_environment: docker-qa-sandbox-and-isolated-codex
qa_review_policy: project-control/.agents/rules/codex_qa_review.md
updated: '2026-10-31T17:30:00+08:00'
---

# TWIN-35 VMware宿主机端到端Web界面操作打印闭环综合验收

## 任务目标
由 INTEGRATOR 联合 QA，在 VMware 真实运行环境（`192.168.77.134:8080`）完成端到端 Web 界面操作打印闭环综合验收。
