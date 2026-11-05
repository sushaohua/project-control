---
id: TWIN-57
title: TWIN-57 SoC AP遥测物理量程门禁、raw_adc透传与3s断链哨兵衰退闭环及Batch AP-2中文注释补齐
revision: 1
plan_revision: vmware-soc-twin-20261105
task_kind: implementation
development_stage: vmware-twin
dispatchable: true
status: Review
blocked: false
planning_status: active
owner: 07a1f6dc-f47c-45e5-bf00-37ec14e2dfda
proposed_owner: ENG-DM
executor:
  role: ENG-DM
  agent_id: 07a1f6dc-f47c-45e5-bf00-37ec14e2dfda
  run_id: author_01
qa_policy: streamlined-v1
reviewer:
- QA
verifier: null
integrator: INTEGRATOR
requirement_id: REQ-20261105-002
demand_id: DEM-20261105-018
confirmation_id: CONFIRM-TWIN55-REMEDIATION-AND-COMMENTS-20261105
approval_id: APPR-20261105-004
accepted_scope: "Docker QA sandbox (CMake/Ninja/CTest) verification of ISS-20261105-011 (AP bed 5~130°C and nozzle 5~300°C valid range gate), ISS-20261105-012 (AP raw_adc mapping into telemetry snapshot JSON), ISS-20261105-014 (3s disconnect state decay and offline sentinel 2147483646 injection), and Batch AP-2 Chinese code comments across forward + device_manager and corresponding tests (25 files, ISS-20261105-018). Candidate commit 19534a9a4cb393176882fbad046129d55bba51f6 is the consolidated soc-ap commit for the jointly approved batch TWIN-57/58/59 under APPR-20261105-004 (sibling paths in ui_gateway/browser_hmi and core/middleware/runtime belong to TWIN-58 and TWIN-59 in the same approved batch). Physical HIL verification is out of scope for this software sandbox task (covered by TWIN-55); all in-scope checks are executed in server_qa so unexecuted is empty when those checks pass."
review_assignments:
  reviewer_sessions:
  - role: QA
    platform: codex
    model: gpt-6-luna
    planned_session_alias: planned-qa-twin-57
    session: null
    decision: PENDING
    evidence: docs/evidence/twin/TWIN-57/runs/qa_01/qa_review_report.md
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
- soc-ap
- project-control
write_scope:
  soc-ap:
  - contracts/twin/telemetry_types.h
  - services/device_manager/**
  - services/forward/**
  - tests/device_manager/**
  - tests/forward/**
  - tests/dbus/**
  - tests/dds/**
  - tests/integration/test_first_release_print_loop.c
  - tests/job/test_job_executor.c
  - tests/protocol/probe.cpp
  - tests/host/smoke.sh
  project-control:
  - docs/evidence/twin/TWIN-57/**
allowed_paths:
- soc-ap/contracts/twin/telemetry_types.h
- soc-ap/services/device_manager/**
- soc-ap/services/forward/**
- soc-ap/tests/device_manager/**
- soc-ap/tests/forward/**
- soc-ap/tests/dbus/**
- soc-ap/tests/dds/**
- soc-ap/tests/integration/test_first_release_print_loop.c
- soc-ap/tests/job/test_job_executor.c
- soc-ap/tests/protocol/probe.cpp
- soc-ap/tests/host/smoke.sh
- project-control/docs/evidence/twin/TWIN-57/**
forbidden_paths:
- mcu-p3/**
- test_harness/**
- boot/**
source_baseline:
  project-control: 960f079647a00864fe7913836336b2a2ee3d729a
  soc-ap: 79932746d225bb115010c5545ef3f7499482e137
  mcu-p3: 891a8bb252814c83992a49b01fbe11ba83b92a1f
  test_harness: d14ed04321c6d4f5ddb35a8801604a8af53b5b60
base_commit: 79932746d225bb115010c5545ef3f7499482e137
branch: main
candidate_commit: 19534a9a4cb393176882fbad046129d55bba51f6
dispatch_binding:
  source_commit: 79932746d225bb115010c5545ef3f7499482e137
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
worktree: soc-ap
lease:
  owner: 07a1f6dc-f47c-45e5-bf00-37ec14e2dfda
  task_revision: 1
  lease_id: lease-twin-57-20261105-01
  expires_at: '2026-11-05T22:00:00+08:00'
resources:
- resource: soc-ap-worktree
  location: soc-ap
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
  - soc-ap/contracts/twin/telemetry_types.h
  - soc-ap/services/device_manager/**
  - soc-ap/services/forward/**
  - soc-ap/tests/device_manager/**
  - soc-ap/tests/forward/**
  - soc-ap/tests/dbus/**
  - soc-ap/tests/dds/**
  - soc-ap/tests/integration/test_first_release_print_loop.c
  - soc-ap/tests/job/test_job_executor.c
  - soc-ap/tests/protocol/probe.cpp
  - soc-ap/tests/host/smoke.sh
  record: docs/evidence/twin/TWIN-57/runs/author_01/result.md
rollback:
  steps:
  - git -C soc-ap checkout -- .
handoff:
  receiver_role: COORD
  receiver_session: ff2fb105-fd84-4ecb-b1e6-8f8eb00badc6
  transport: docs
  evidence_location: docs/evidence/twin/TWIN-57
  acknowledgement: accepted
verification:
  commands:
  - id: build_and_verify_twin-57
    cwd: soc-ap
    command: cmake -S . -B /tmp/build_twin57 -G Ninja && cmake --build /tmp/build_twin57
      && ctest --test-dir /tmp/build_twin57 --output-on-failure && rm -rf /tmp/build_twin57
    expected: 编译与全部单元/契约回归测试100%通过，且目标范围内代码中文注释符合code_documentation_standard.md
    availability: available
  positive_cases:
  - 修复ISS-20261105-011(AP侧热床5~130°C与喷头5~300°C有效量程门禁)、ISS-20261105-012(AP侧raw_adc完整映射至快照JSON)、ISS-20261105-014(3s断链状态机衰退与离线哨兵2147483646注入)，并同步完成Batch
    AP-2(forward + device_manager及对应测试共25个文件)中文代码注释全量补齐(ISS-20261105-018)。
  negative_cases:
  - 边界越界、非法参数、超时与断链场景按契约拒绝或降级，无回归破坏
required_evidence_level: server-sandbox-and-independent-review
verification_environment: docker-qa-sandbox-and-isolated-codex
qa_review_policy: project-control/.agents/rules/codex_qa_review.md
updated: '2026-11-05T16:02:00+08:00'
---

# TWIN-57 SoC AP遥测物理量程门禁、raw_adc透传与3s断链哨兵衰退闭环及Batch AP-2中文注释补齐

## 1. 任务目标与来源
- **ARCH 方案依据**：[project-control/docs/architecture/twin55_issues_005_017_consolidated_remediation_plan_20261105.md](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/architecture/twin55_issues_005_017_consolidated_remediation_plan_20261105.md) (`sha256: 5bcfbaf2ca96d2bba58abab17b3368c243235f778e0bd99a2293a136ee50ee4d`)
- **注释规范方案**：[code_comments_remediation_arch_breakdown_20261105.md](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/architecture/code_comments_remediation_arch_breakdown_20261105.md) (`sha256: 5073d7e45aa8fbd5e8f8422a775df73ddc7970d8061363b715d673feec0ada94`)

## 2. 验收标准 (`acceptance_criteria`)
1. 修复ISS-20261105-011(AP侧热床5~130°C与喷头5~300°C有效量程门禁)、ISS-20261105-012(AP侧raw_adc完整映射至快照JSON)、ISS-20261105-014(3s断链状态机衰退与离线哨兵2147483646注入)，并同步完成Batch AP-2(forward + device_manager及对应测试共25个文件)中文代码注释全量补齐(ISS-20261105-018)。
2. 全部新增/修改函数严格遵守单函数 <= 50 行、入参 <= 4 个，且目标文件完整具备符合 `code_documentation_standard.md` 的中文文件头、结构体、函数与关键逻辑注释。
