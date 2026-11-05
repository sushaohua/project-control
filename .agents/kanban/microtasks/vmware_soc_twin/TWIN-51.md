---
id: TWIN-51
title: TWIN-51 修复test_backoff.cpp在GCC15下的-Werror=maybe-uninitialized编译阻断
revision: 1
plan_revision: vmware-soc-twin-20261105
task_kind: implementation
development_stage: vmware-twin
dispatchable: true
status: Done
blocked: false
planning_status: closed
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
issue_id: ISS-20261105-001
demand_id: DEM-20261105-001
confirmation_id: CONFIRM-SOC-AP-ISSUES-20261105
approval_id: APPR-20261105-001
accepted_scope: "Software and C++17 strict-warning (-O2 -Wall -Wextra -Werror -Wmaybe-uninitialized) sandbox verification of soc-ap/runtime/build/tests/test_backoff.cpp explicit zero-initialization of backoff_state_t and backoff_config_t and runtime/build CTest suite. Cross-compiler ELF build and physical MCU USB/UART HIL are not applicable in qa-sandbox:20261029: qa-sandbox:20261029 provides host GCC/Python only and no physical MCU hardware; all in-scope checks are executed in server_qa so unexecuted is empty when those checks pass."
review_assignments:
  reviewer_sessions:
  - role: QA
    platform: codex
    model: gpt-6-luna
    planned_session_alias: planned-qa-twin-51
    session: 01a1a999-e8d7-7cb3-ad5e-61e0dd08e72c
    reviewer_session: 01a1a999-e8d7-7cb3-ad5e-61e0dd08e72c
    commit_sha: 75f8a1a670edabb21c8d3dfc79243e06f73099af
    session_evidence:
      path: /home/sushaohua/workspace/ai_soc_project/project-control/docs/evidence/twin/TWIN-51/runs/qa_02/codex_events.jsonl
      sha256: 105a7b81b5e1b772e7dc9c08036775bf3fe5372927c3660dd66a852e6407c5b0
    decision: APPROVED
    reviewed_task_revision: 1
    artifact_version: project-control=491158cd4f183a01517c36fb093821db54a8a6dd; soc-ap=75f8a1a670edabb21c8d3dfc79243e06f73099af; mcu-p3=016e1236af75f6f19282d6b000f4b1b68bd96cc3; test_harness=d14ed04321c6d4f5ddb35a8801604a8af53b5b60
    report_path: /home/sushaohua/workspace/ai_soc_project/project-control/docs/evidence/twin/TWIN-51/runs/qa_02/qa_review_report.md
    evidence: docs/evidence/twin/TWIN-51/runs/qa_02/qa_review_report.md
    report_sha256: d182fbc7150715bd5f6c0f05493ae3282cd7d3bf6732d37fe35b9f46f6c460c3
  verifier_session: null
  integrator_session: null
primary_work_package: TASK-004
related_work_packages:
- TASK-010
depends_on:
- TWIN-04
dependency_conditions:
- task: TWIN-04
  accepted_version: soc-ap=8f05b7396bb11fb011b0279c6a38f26a194507be; project-control=6b3556fb52002833ce57bc28ca236630bd8e907be
  acceptance_evidence: docs/evidence/twin/TWIN-04/runs/run_01/qa_review_report.md
  required: 继承TWIN-04 runtime/build与test_backoff单测构建基线
scope_status: mapped
allowed_repositories:
- soc-ap
- project-control
write_scope:
  soc-ap:
  - runtime/build/tests/test_backoff.cpp
  project-control:
  - docs/evidence/twin/TWIN-51/**
allowed_paths:
- soc-ap/runtime/build/tests/test_backoff.cpp
- project-control/docs/evidence/twin/TWIN-51/**
forbidden_paths:
- mcu-p3/**
- test_harness/**
- boot/**
- soc-ap/services/**
- soc-ap/middleware/**
- soc-ap/tools/**
source_baseline:
  project-control: 491158cd4f183a01517c36fb093821db54a8a6dd
  soc-ap: 7c1f35091850b39f4ba3ff9b242043a62f3e5b74
  mcu-p3: 016e1236af75f6f19282d6b000f4b1b68bd96cc3
  test_harness: d14ed04321c6d4f5ddb35a8801604a8af53b5b60
base_commit: 7c1f35091850b39f4ba3ff9b242043a62f3e5b74
branch: main
candidate_commit: 75f8a1a670edabb21c8d3dfc79243e06f73099af
dispatch_binding:
  source_commit: 7c1f35091850b39f4ba3ff9b242043a62f3e5b74
  workspace_diff_sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
  consumed_artifact_versions:
    arch_breakdown: 2c3bba7cb6037cb8f89a6231008eafaa8bd4b8fcf90e81a7560742bafb8b200c
protocol_input:
  path: project-control/docs/architecture/soc_ap_build_and_startup_issues_arch_breakdown_20261105.md
  sha256: 2c3bba7cb6037cb8f89a6231008eafaa8bd4b8fcf90e81a7560742bafb8b200c
  revision: 4
icd_versions:
- path: project-control/docs/architecture/soc_ap_build_and_startup_issues_arch_breakdown_20261105.md
  version: 4
read_sources:
- project-control/.agents/rules/repository_rule_sources.json
- project-control/.agents/rules/repository_rule_boundaries.md
- soc-ap/AGENTS.md
- soc-ap/.agents/rules/shared/SOURCE.json
- project-control/.agents/rules/c_cpp_coding_standard.md
- project-control/.agents/rules/code_documentation_standard.md
- project-control/docs/architecture/soc_ap_build_and_startup_issues_arch_breakdown_20261105.md
worktree: soc-ap
lease:
  owner: 7812a1f6-5006-4971-a954-802f855cf20a
  task_revision: 1
  lease_id: lease-twin-51-20261105-01
  expires_at: '2026-11-05T16:00:00+08:00'
resources:
- resource: integrator-build-env
  location: soc-ap
  exclusive: true
  pending: null
budget:
  planned_checkpoint_minutes: 30
  max_evidence_based_corrections: 2
  on_limit: 保存证据交COORD
checkpoint: 开工前绑定；-O2 -Wall -Wextra -Werror -Wmaybe-uninitialized编译与CTest自检；独立沙箱与QA审查；收件
execution_contract: project-control/docs/planning/vmware_soc_twin_task_execution_20261029.md
readiness_pending: []
deliverables:
  artifacts:
  - soc-ap/runtime/build/tests/test_backoff.cpp
  record: docs/evidence/twin/TWIN-51/runs/author_01/result.md
rollback:
  steps:
  - git -C soc-ap checkout -- runtime/build/tests/test_backoff.cpp
handoff:
  receiver_role: COORD
  receiver_session: ff2fb105-fd84-4ecb-b1e6-8f8eb00badc6
  transport: docs
  evidence_location: docs/evidence/twin/TWIN-51
  acknowledgement: received-author_01-75f8a1a670edabb21c8d3dfc79243e06f73099af
verification:
  commands:
  - id: build_and_test_backoff_werror_uninitialized
    cwd: soc-ap
    command: 'rm -rf /tmp/qa_twin51 && mkdir -p /tmp/qa_twin51 && (! grep -En "backoff_(state|config)_t[[:space:]]+(st|cfg)[[:space:]]*;" runtime/build/tests/test_backoff.cpp) && g++ -std=c++17 -O2 -Wall -Wextra -Werror -Wpedantic -Wmaybe-uninitialized -fno-exceptions -fno-rtti -Iruntime/common runtime/build/tests/test_backoff.cpp runtime/common/service_lifecycle.cpp -o /tmp/qa_twin51/test_backoff_strict && /tmp/qa_twin51/test_backoff_strict && cmake -S runtime/build -B /tmp/qa_twin51/build -DCMAKE_BUILD_TYPE=Release -DCMAKE_CXX_FLAGS_RELEASE="-O2" && cmake --build /tmp/qa_twin51/build --parallel && ctest --test-dir /tmp/qa_twin51/build --output-on-failure && rm -rf /tmp/qa_twin51'
    expected: 源码静态扫描确认无未初始化的backoff_state_t/backoff_config_t局部变量，g++ -O2 -Wall -Wextra -Werror -Wmaybe-uninitialized严格编译零告警通过，且runtime/build全套Release CTest（test_service_lifecycle、test_backoff、test_supervisor_topology）100% PASS
    availability: available
  positive_cases:
  - test_backoff.cpp中所有栈上backoff_state_t与backoff_config_t结构体均显式零初始化，在-O2 -Wall -Wextra -Werror -Wmaybe-uninitialized下零告警编译通过
  - test_backoff_null_guards、test_backoff_progression、test_backoff_reset全部断言100%通过
  negative_cases:
  - 严禁通过移除-Werror或添加-Wno-maybe-uninitialized掩盖未初始化告警；静态检查发现未初始化st/cfg裸声明时立即失败
required_evidence_level: server-sandbox-and-independent-review
verification_environment: docker-qa-sandbox-and-isolated-codex
qa_review_policy: project-control/.agents/rules/codex_qa_review.md
updated: '2026-11-05T10:31:00+08:00'
---

# TWIN-51 修复test_backoff.cpp在GCC15下的-Werror=maybe-uninitialized编译阻断

## 1. 任务目标与来源
- **关联收件**：[`ISS-20261105-001.yaml`](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/work_intake/issues/ISS-20261105-001.yaml) / `DEM-20261105-001`
- **ARCH 方案依据**：[soc_ap_build_and_startup_issues_arch_breakdown_20261105.md](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/architecture/soc_ap_build_and_startup_issues_arch_breakdown_20261105.md) (`revision: 1`, SHA-256 `04be47f7ca02f7a98e4f249e8313309d32c9642a07574c011cb2161014ac5b36`)

## 2. 验收标准 (`acceptance_criteria`)
1. 在 `soc-ap/runtime/build/tests/test_backoff.cpp` 中对所有局部栈变量 `backoff_state_t st` 与 `backoff_config_t cfg` 进行显式零初始化，消除 GCC 15 下传入 `const` 指针形参触发的 `-Werror=maybe-uninitialized` 阻断。
2. 保留全部空指针防御断言与 `-Werror` 门禁，通过 Release CTest 全套验证。
