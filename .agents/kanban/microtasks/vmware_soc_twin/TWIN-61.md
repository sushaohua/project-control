---
id: TWIN-61
title: TWIN-61 全量HIL主测试计划与290帧/5类复合脚本固化(ISS-005)及project-control/tools Batch PC-1中文注释补齐(ISS-018)
revision: 1
plan_revision: vmware-soc-twin-20261105
task_kind: implementation
development_stage: vmware-twin
dispatchable: true
status: Review
blocked: false
planning_status: active
owner: 07a1f6dc-f47c-45e5-bf00-37ec14e2dfda
proposed_owner: QA
executor:
  role: QA
  agent_id: 07a1f6dc-f47c-45e5-bf00-37ec14e2dfda
  run_id: author_01
qa_policy: streamlined-v1
reviewer:
- QA
- ARCH
verifier: null
integrator: INTEGRATOR
requirement_id: REQ-20261105-002
demand_id: DEM-20261105-018
confirmation_id: CONFIRM-TWIN55-REMEDIATION-AND-COMMENTS-20261105
approval_id: APPR-20261105-004
accepted_scope: "Docker QA sandbox verification and independent non-author review (QA + ARCH) of ISS-20261105-005 full HIL acceptance master plan (project-control/docs/planning/hil_full_acceptance_master_plan_20261105.md), test_harness/hil/tests/test_290_frame_burst_stress.py & test_composite_lifecycle_sequences.py (test_harness candidate 9f3918a2f9fc79a683ce218436b005e593a7109b), and ISS-20261105-018 Batch PC-1 Chinese code comments across project-control/tools/** (41 files, committed in project-control at c1d2c461aa65e6497c295843a2735d0d02ee2e2d, diffable via git -C ../project-control diff 5686e1931123650bb2251045353c18c8baa00f65..c1d2c461aa65e6497c295843a2735d0d02ee2e2d). Live workspace intake scan of 20261105_twin55_codex_hil_issues.md (which intentionally preserves reported_by.actor_type: MODEL per its line 17 constraint) and physical HIL bench execution (covered by TWIN-55) are out of scope for this software sandbox run; all in-scope checks are executed in server_qa so unexecuted is empty when those checks pass."
review_assignments:
  reviewer_sessions:
  - role: QA
    platform: codex
    model: gpt-6-luna
    planned_session_alias: planned-qa-twin-61
    session: null
    decision: PENDING
    evidence: docs/evidence/twin/TWIN-61/runs/qa_01/qa_review_report.md
  - role: ARCH
    platform: codex
    model: gpt-6-luna
    planned_session_alias: planned-arch-twin-61
    session: null
    decision: PENDING
    evidence: docs/evidence/twin/TWIN-61/runs/qa_01/arch_review_report.md
  verifier_session: null
  integrator_session: null
primary_work_package: TASK-009
related_work_packages:
- TASK-007
- TASK-010
depends_on:
- TWIN-56
dependency_conditions:
- task: TWIN-56
  accepted_version: project-control=99cd83bb40b4ecf53e8f9dd996ad61ecb653f6f0; soc-ap=79932746d225bb115010c5545ef3f7499482e137;
    mcu-p3=891a8bb252814c83992a49b01fbe11ba83b92a1f; test_harness=d14ed04321c6d4f5ddb35a8801604a8af53b5b60
  acceptance_evidence: docs/evidence/twin/TWIN-56/runs/qa_03/qa_review_report.md
  required: 继承TWIN-56 16-bit seq日志与三仓锁定基线
scope_status: mapped
allowed_repositories:
- test_harness
- project-control
write_scope:
  test_harness:
  - hil/**
  project-control:
  - docs/planning/hil_full_acceptance_master_plan_20261105.md
  - tools/**
  - docs/evidence/twin/TWIN-61/**
allowed_paths:
- test_harness/hil/**
- project-control/docs/planning/hil_full_acceptance_master_plan_20261105.md
- project-control/tools/**
- project-control/docs/evidence/twin/TWIN-61/**
forbidden_paths:
- soc-ap/**
- mcu-p3/**
- boot/**
source_baseline:
  project-control: c1d2c461aa65e6497c295843a2735d0d02ee2e2d
  soc-ap: 19534a9a4cb393176882fbad046129d55bba51f6
  mcu-p3: 191e355a4227268a472bafd6862d4a8c854e0544
  test_harness: d14ed04321c6d4f5ddb35a8801604a8af53b5b60
base_commit: d14ed04321c6d4f5ddb35a8801604a8af53b5b60
branch: main
candidate_commit: 9f3918a2f9fc79a683ce218436b005e593a7109b
dispatch_binding:
  source_commit: d14ed04321c6d4f5ddb35a8801604a8af53b5b60
  workspace_diff_sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
  consumed_artifact_versions:
    arch_breakdown: 5bcfbaf2ca96d2bba58abab17b3368c243235f778e0bd99a2293a136ee50ee4d
protocol_input:
  path: project-control/docs/architecture/twin55_issues_005_017_consolidated_remediation_plan_20261105.md
  sha256: 5bcfbaf2ca96d2bba58abab17b3368c243235f778e0bd99a2293a136ee50ee4d
  revision: 1
icd_versions:
- path: project-control/docs/architecture/twin55_issues_005_017_consolidated_remediation_plan_20261105.md
  version: 1
read_sources:
- project-control/.agents/rules/repository_rule_sources.json
- project-control/.agents/rules/repository_rule_boundaries.md
- project-control/.agents/rules/c_cpp_coding_standard.md
- project-control/.agents/rules/web_ui_coding_standard.md
- project-control/.agents/rules/code_documentation_standard.md
- project-control/docs/architecture/twin55_issues_005_017_consolidated_remediation_plan_20261105.md
- project-control/docs/architecture/code_comments_remediation_arch_breakdown_20261105.md
worktree: test_harness
lease:
  owner: 07a1f6dc-f47c-45e5-bf00-37ec14e2dfda
  task_revision: 1
  lease_id: lease-twin-61-20261105-01
  expires_at: '2026-11-05T22:00:00+08:00'
resources:
- resource: test_harness-worktree
  location: test_harness
  exclusive: false
  pending: null
budget:
  planned_checkpoint_minutes: 45
  max_evidence_based_corrections: 2
  on_limit: 保存证据交COORD
checkpoint: 开工前绑定；自检单测与注释规范检查；独立沙箱与QA审查；收件
execution_contract: project-control/docs/planning/vmware_soc_twin_task_execution_20261029.md
readiness_pending: []
deliverables:
  artifacts:
  - test_harness/hil/**
  - project-control/docs/planning/hil_full_acceptance_master_plan_20261105.md
  - project-control/tools/**
  record: docs/evidence/twin/TWIN-61/runs/author_01/result.md
rollback:
  steps:
  - git -C test_harness checkout -- .
handoff:
  receiver_role: COORD
  receiver_session: ff2fb105-fd84-4ecb-b1e6-8f8eb00badc6
  transport: docs
  evidence_location: docs/evidence/twin/TWIN-61
  acknowledgement: accepted
verification:
  commands:
  - id: verify_twin-61
    cwd: test_harness
    command: python3 -m unittest ../project-control/tools/test_check_task_graph.py ../project-control/tools/test_delivery_checks.py ../project-control/tools/test_qa_runner.py ../project-control/tools/test_qa_pipeline.py ../project-control/tools/test_review_policy.py ../project-control/tools/test_coord_recovery.py ../project-control/tools/test_coord_systemd_service.py && python3 hil/tools/debug_reconciliation_probe.py --self-test && python3 hil/tests/test_290_frame_burst_stress.py --self-test && python3 hil/tests/test_composite_lifecycle_sequences.py --self-test
    expected: 编译与全部单元/契约回归测试及290帧/5类复合序列自测100%通过，且目标范围内代码中文注释符合code_documentation_standard.md
    availability: available
  positive_cases:
  - 完成ISS-20261105-005全量HIL主测试计划(project-control/docs/planning/hil_full_acceptance_master_plan_20261105.md)与test_harness/hil/下290帧高频突发及5类复合序列自动化测试脚本固化，并完成ISS-20261105-018
    Batch PC-1(project-control/tools/**共41个文件)中文代码注释全量补齐。
  negative_cases:
  - 边界越界、非法参数、超时与断链场景按契约拒绝或降级，无回归破坏
required_evidence_level: server-sandbox-and-independent-review
verification_environment: docker-qa-sandbox-and-isolated-codex
qa_review_policy: project-control/.agents/rules/codex_qa_review.md
updated: '2026-11-05T16:02:00+08:00'
---

# TWIN-61 全量HIL主测试计划与290帧/5类复合脚本固化(ISS-005)及project-control/tools Batch PC-1中文注释补齐(ISS-018)

## 1. 任务目标与来源
- **ARCH 方案依据**：[project-control/docs/architecture/twin55_issues_005_017_consolidated_remediation_plan_20261105.md](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/architecture/twin55_issues_005_017_consolidated_remediation_plan_20261105.md) (`sha256: 5bcfbaf2ca96d2bba58abab17b3368c243235f778e0bd99a2293a136ee50ee4d`)
- **注释规范方案**：[code_comments_remediation_arch_breakdown_20261105.md](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/architecture/code_comments_remediation_arch_breakdown_20261105.md) (`sha256: 5073d7e45aa8fbd5e8f8422a775df73ddc7970d8061363b715d673feec0ada94`)

## 2. 验收标准 (`acceptance_criteria`)
1. 完成ISS-20261105-005全量HIL主测试计划(project-control/docs/planning/hil_full_acceptance_master_plan_20261105.md)与test_harness/hil/下290帧高频突发及5类复合序列自动化测试脚本固化，并完成ISS-20261105-018 Batch PC-1(project-control/tools/**共41个文件)中文代码注释全量补齐。
2. 全部新增/修改函数严格遵守单函数 <= 50 行、入参 <= 4 个，且目标文件完整具备符合 `code_documentation_standard.md` 的中文文件头、结构体、函数与关键逻辑注释。
