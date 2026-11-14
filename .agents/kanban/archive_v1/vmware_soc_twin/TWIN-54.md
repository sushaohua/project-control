---
id: TWIN-54
title: TWIN-54 Web HMI完整basecase与增量闭环编译部署封存及提测交接准备
revision: 1
plan_revision: vmware-soc-twin-20261105
task_kind: integration
development_stage: vmware-twin
dispatchable: true
status: Backlog
blocked: false
planning_status: planned
owner: 7812a1f6-5006-4971-a954-802f855cf20a
proposed_owner: INTEGRATOR
executor:
  role: INTEGRATOR
  agent_id: 7812a1f6-5006-4971-a954-802f855cf20a
  run_id: author_01
qa_policy: streamlined-v1
reviewer:
  - QA
verifier: null
integrator: INTEGRATOR
requirement_id: REQ-20261105-001
demand_id: DEM-20261105-005
confirmation_id: CONFIRM-WEB-HMI-FULL-QA-BUILD-DEPLOY-20261105
approval_id: APPR-20261105-003
review_assignments:
  reviewer_sessions:
    - role: QA
      platform: codex
      model: gpt-6-luna
      planned_session_alias: planned-qa-twin-54
  verifier_session: null
  integrator_session: null
primary_work_package: TASK-010
related_work_packages:
  - TASK-004
  - TASK-009
depends_on:
  - TWIN-50
  - TWIN-51
  - TWIN-52
  - TWIN-53
dependency_conditions:
  - task: TWIN-50
    accepted_version: project-control=17e0887da07ceb3b017623b791b6a6999e837c79; soc-ap=333178c66280e785ae1a5c089a6e2a05075cc926; mcu-p3=016e1236af75f6f19282d6b000f4b1b68bd96cc3; test_harness=d14ed04321c6d4f5ddb35a8801604a8af53b5b60
    acceptance_evidence: docs/evidence/twin/TWIN-50/runs/qa_03/qa_review_report.md
    required: 继承TWIN-50双路Debug对账探针与软件/PTY基线
  - task: TWIN-51
    accepted_version: soc-ap=75f8a1a670edabb21c8d3dfc79243e06f73099af
    acceptance_evidence: docs/evidence/twin/TWIN-51/runs/qa_02/qa_review_report.md
    required: 继承TWIN-51 GCC 15 test_backoff编译修复
  - task: TWIN-52
    accepted_version: soc-ap=ad2538ae7f4834cac98be97e08b055f80eb81cfc
    acceptance_evidence: docs/evidence/twin/TWIN-52/runs/qa_03/qa_review_report.md
    required: 继承TWIN-52 Fast-CDR optional补丁固化
  - task: TWIN-53
    accepted_version: soc-ap=87c3bd31b1adc9f17fcc75aa5d7ea26beb44e59a
    acceptance_evidence: docs/evidence/twin/TWIN-53/runs/qa_02/qa_review_report.md
    required: 继承TWIN-53 deploy_twin.sh四进程存活与SIGHUP加固
scope_status: mapped
allowed_repositories:
  - project-control
write_scope:
  project-control:
    - docs/planning/web_hmi_full_qa_build_deploy_confirmation_20261105.md
    - docs/evidence/twin/TWIN-54/**
allowed_paths:
  - project-control/docs/planning/web_hmi_full_qa_build_deploy_confirmation_20261105.md
  - project-control/docs/evidence/twin/TWIN-54/**
forbidden_paths:
  - soc-ap/**
  - mcu-p3/**
  - test_harness/**
  - boot/**
  - boot/**
source_baseline:
  project-control: 77c679616a09d9c82906ff9bdf27fefc6d6c343f
  soc-ap: 79932746d225bb115010c5545ef3f7499482e137
  mcu-p3: 016e1236af75f6f19282d6b000f4b1b68bd96cc3
  test_harness: d14ed04321c6d4f5ddb35a8801604a8af53b5b60
base_commit: d14ed04321c6d4f5ddb35a8801604a8af53b5b60
branch: main
candidate_commit: null
dispatch_binding:
  source_commit: d14ed04321c6d4f5ddb35a8801604a8af53b5b60
  workspace_diff_sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
  consumed_artifact_versions:
    build_deploy_confirmation: 7e92f1093ea1ba1f27fe4b0159bad926e6b0f44130f55d06ae223c730ddffd89
protocol_input:
  path: project-control/docs/planning/web_hmi_full_qa_build_deploy_confirmation_20261105.md
  sha256: 7e92f1093ea1ba1f27fe4b0159bad926e6b0f44130f55d06ae223c730ddffd89
  revision: 2
icd_versions:
  - path: project-control/docs/planning/web_hmi_full_qa_build_deploy_confirmation_20261105.md
    version: 2
read_sources:
  - project-control/.agents/rules/repository_rule_sources.json
  - project-control/.agents/rules/repository_rule_boundaries.md
  - test_harness/AGENTS.md
  - test_harness/.agents/rules/shared/SOURCE.json
  - project-control/.agents/rules/c_cpp_coding_standard.md
  - project-control/.agents/rules/code_documentation_standard.md
  - project-control/docs/planning/web_hmi_full_qa_build_deploy_confirmation_20261105.md
  - project-control/docs/planning/qa_web_hmi_basecases_20261103.md
worktree: test_harness
lease:
  owner: 7812a1f6-5006-4971-a954-802f855cf20a
  task_revision: 1
  lease_id: lease-twin-54-20261105-01
  expires_at: '2026-11-05T18:00:00+08:00'
resources:
  - resource: integrator-qa-prep
    location: test_harness
    exclusive: true
    pending: null
budget:
  planned_checkpoint_minutes: 45
  max_evidence_based_corrections: 2
  on_limit: 保存证据交COORD
checkpoint: Step1-4干净构建与build_manifest.yaml封存；Step5烧录授权呈报；提测交接与BASE/DELTA自动化套件准备
execution_contract: project-control/docs/planning/vmware_soc_twin_task_execution_20261029.md
readiness_pending: []
deliverables:
  artifacts:
    - project-control/docs/planning/web_hmi_full_qa_build_deploy_confirmation_20261105.md
  record: docs/evidence/twin/TWIN-54/runs/author_01/result.md
rollback:
  steps:
    - git -C test_harness checkout -- hil/
handoff:
  receiver_role: COORD
  receiver_session: ff2fb105-fd84-4ecb-b1e6-8f8eb00badc6
  transport: docs
  evidence_location: docs/evidence/twin/TWIN-54
  acknowledgement: pending
verification:
  commands:
    - id: verify_twin54_manifest_and_qa_handoff
      cwd: project-control
      command: 'test -f docs/planning/web_hmi_full_qa_build_deploy_confirmation_20261105.md && test -f docs/evidence/twin/TWIN-54/runs/author_01/build_manifest.yaml'
      expected: 编译部署确认单及本轮锁定候选build_manifest.yaml、SHA256SUMS与轻量提测交接清单齐全且哈希一致
      availability: available
  positive_cases:
    - 完成Step 1-4从服务器准确版本检出、AP/UI（Docker与VMware）及MC/TH双固件干净构建，生成build_manifest.yaml与SHA256SUMS
    - 汇总完整轻量提测交接单并补齐BASE-01~27、J-01及DELTA-DBG/BAUD/COMB自动化执行与四方对账脚本
  negative_cases:
    - 未取得Step 5具体固件烧录授权前严禁执行probe-rs download烧录动作
required_evidence_level: server-sandbox-and-independent-review
verification_environment: docker-qa-sandbox-and-isolated-codex
qa_review_policy: project-control/.agents/rules/codex_qa_review.md
updated: '2026-11-05T11:57:30+08:00'
---

# TWIN-54 Web HMI完整basecase与增量闭环编译部署封存及提测交接准备

## 1. 任务目标与来源
- **关联收件**：[`REQ-20261105-001.yaml`](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/work_intake/requirements/REQ-20261105-001.yaml) / `DEM-20261105-005`
- **已确认编译部署流程**：[web_hmi_full_qa_build_deploy_confirmation_20261105.md](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/planning/web_hmi_full_qa_build_deploy_confirmation_20261105.md) (`revision: 2`, SHA-256 `7e92f1093ea1ba1f27fe4b0159bad926e6b0f44130f55d06ae223c730ddffd89`)
