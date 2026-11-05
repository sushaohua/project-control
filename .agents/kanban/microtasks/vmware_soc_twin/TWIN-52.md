---
id: TWIN-52
title: TWIN-52 Fast-CDR 2.2.5 optional未初始化拷贝崩溃补丁固化与third_party可重现构建
revision: 1
plan_revision: vmware-soc-twin-20261105
task_kind: implementation
development_stage: vmware-twin
dispatchable: true
status: Done
blocked: false
planning_status: closed
owner: 7812a1f6-5006-4971-a954-802f855cf20a
proposed_owner: ENG-DDS
executor:
  role: ENG-DDS
  agent_id: 7812a1f6-5006-4971-a954-802f855cf20a
  run_id: author_02
qa_policy: streamlined-v1
reviewer:
- QA
verifier: null
integrator: INTEGRATOR
issue_id: ISS-20261105-002
demand_id: DEM-20261105-002
confirmation_id: CONFIRM-SOC-AP-ISSUES-20261105
approval_id: APPR-20261105-001
accepted_scope: "Software and C++17 sandbox verification of soc-ap/third_party/patches/Fast-CDR-2.2.5-optional-engaged-guard.patch, soc-ap/third_party/build.sh idempotent patch application and verify_install() guard check, soc-ap/middleware/dds/tests/test_fastcdr_optional.cpp (dirty-memory unengaged optional<std::string> copy/move, long-string engaged copy/move, and Fast-DDS participant/publisher startup without SIGSEGV), and test_dds_pubsub CTest suite. Cross-compiler ELF build and physical MCU USB/UART HIL are not applicable in qa-sandbox:20261029: qa-sandbox:20261029 provides host GCC/Python only and no physical MCU hardware; all in-scope checks are executed in server_qa so unexecuted is empty when those checks pass."
review_assignments:
  reviewer_sessions:
  - role: QA
    platform: codex
    model: gpt-6-luna
    planned_session_alias: planned-qa-twin-52
    session: 01a1a9ad-5a37-7bb3-9835-4ed9ce0a308b
    reviewer_session: 01a1a9ad-5a37-7bb3-9835-4ed9ce0a308b
    commit_sha: ad2538ae7f4834cac98be97e08b055f80eb81cfc
    session_evidence:
      path: /home/sushaohua/workspace/ai_soc_project/project-control/docs/evidence/twin/TWIN-52/runs/qa_03/codex_events.jsonl
      sha256: 77241ff8bf7e688ed54cfe3055f6fb34a530544b0d16eca6bae7f8b8bc0cbee6
    decision: APPROVED
    reviewed_task_revision: 1
    artifact_version: project-control=491158cd4f183a01517c36fb093821db54a8a6dd; soc-ap=ad2538ae7f4834cac98be97e08b055f80eb81cfc; mcu-p3=016e1236af75f6f19282d6b000f4b1b68bd96cc3; test_harness=d14ed04321c6d4f5ddb35a8801604a8af53b5b60
    report_path: /home/sushaohua/workspace/ai_soc_project/project-control/docs/evidence/twin/TWIN-52/runs/qa_03/qa_review_report.md
    evidence: docs/evidence/twin/TWIN-52/runs/qa_03/qa_review_report.md
    report_sha256: d37fd97e4322609502fc71db19b8847e514d8180b157b8817d820f8798b42fea
  verifier_session: null
  integrator_session: null
primary_work_package: TASK-005
related_work_packages:
- TASK-004
- TASK-007
- TASK-010
depends_on:
- TWIN-05
- TWIN-49
dependency_conditions:
- task: TWIN-05
  accepted_version: soc-ap=81362a6489704926c89d9b4f93e7a480d610474e; project-control=0c49669a2a89668ef2273197f43a5a852d63be91
  acceptance_evidence: docs/evidence/twin/TWIN-05/runs/run_01/qa_review_report.md
  required: 继承TWIN-05 Fast-DDS中间件封装与Fast-CDR归档基线
- task: TWIN-49
  accepted_version: project-control=17e0887da07ceb3b017623b791b6a6999e837c79; soc-ap=333178c66280e785ae1a5c089a6e2a05075cc926; mcu-p3=016e1236af75f6f19282d6b000f4b1b68bd96cc3; test_harness=30c21f74e74179994eb475c38cc4afc2c1427a26
  acceptance_evidence: docs/evidence/twin/TWIN-49/runs/qa_04/qa_review_report.md
  required: 继承TWIN-49 third_party/build.sh构建入口基线
scope_status: mapped
allowed_repositories:
- soc-ap
- project-control
write_scope:
  soc-ap:
  - third_party/patches/Fast-CDR-2.2.5-optional-engaged-guard.patch
  - third_party/build.sh
  - middleware/dds/tests/CMakeLists.txt
  - middleware/dds/tests/test_fastcdr_optional.cpp
  project-control:
  - docs/evidence/twin/TWIN-52/**
allowed_paths:
- soc-ap/third_party/patches/Fast-CDR-2.2.5-optional-engaged-guard.patch
- soc-ap/third_party/build.sh
- soc-ap/middleware/dds/tests/CMakeLists.txt
- soc-ap/middleware/dds/tests/test_fastcdr_optional.cpp
- project-control/docs/evidence/twin/TWIN-52/**
forbidden_paths:
- mcu-p3/**
- test_harness/**
- boot/**
- soc-ap/tests/**
- soc-ap/services/**
- soc-ap/tools/**
source_baseline:
  project-control: 491158cd4f183a01517c36fb093821db54a8a6dd
  soc-ap: 75f8a1a670edabb21c8d3dfc79243e06f73099af
  mcu-p3: 016e1236af75f6f19282d6b000f4b1b68bd96cc3
  test_harness: d14ed04321c6d4f5ddb35a8801604a8af53b5b60
base_commit: 75f8a1a670edabb21c8d3dfc79243e06f73099af
branch: main
candidate_commit: ad2538ae7f4834cac98be97e08b055f80eb81cfc
dispatch_binding:
  source_commit: 75f8a1a670edabb21c8d3dfc79243e06f73099af
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
  lease_id: lease-twin-52-20261105-01
  expires_at: '2026-11-05T16:00:00+08:00'
resources:
- resource: dds-build-env
  location: soc-ap
  exclusive: true
  pending: null
budget:
  planned_checkpoint_minutes: 60
  max_evidence_based_corrections: 2
  on_limit: 保存证据交COORD
checkpoint: 开工前绑定；Fast-CDR补丁校验与DDS单测自检；独立沙箱与QA审查；收件
execution_contract: project-control/docs/planning/vmware_soc_twin_task_execution_20261029.md
readiness_pending: []
deliverables:
  artifacts:
  - soc-ap/third_party/patches/Fast-CDR-2.2.5-optional-engaged-guard.patch
  - soc-ap/third_party/build.sh
  - soc-ap/middleware/dds/tests/CMakeLists.txt
  - soc-ap/middleware/dds/tests/test_fastcdr_optional.cpp
  record: docs/evidence/twin/TWIN-52/runs/author_02/result.md
rollback:
  steps:
  - git -C soc-ap checkout -- third_party/ middleware/dds/
handoff:
  receiver_role: COORD
  receiver_session: ff2fb105-fd84-4ecb-b1e6-8f8eb00badc6
  transport: docs
  evidence_location: docs/evidence/twin/TWIN-52
  acknowledgement: received-author_02-ad2538ae7f4834cac98be97e08b055f80eb81cfc
verification:
  commands:
  - id: build_and_test_fastcdr_optional_patch_and_dds_startup
    cwd: soc-ap
    command: 'rm -rf /tmp/qa_twin52 && mkdir -p /tmp/qa_twin52/raw && tar -xzf third_party/archives/Fast-CDR-2.2.5.tar.gz -C /tmp/qa_twin52/raw && test "$(grep -c "if (val.storage_.engaged_)" /tmp/qa_twin52/raw/Fast-CDR-2.2.5/include/fastcdr/xcdr/optional.hpp || true)" -eq 0 && cp -r ../soc-ap /tmp/qa_twin52/soc-ap && ([ -e /tmp/qa_twin52/soc-ap/third_party/install ] || (mkdir -p /tmp/qa_twin52/soc-ap/third_party && cp -a /usr/local /tmp/qa_twin52/soc-ap/third_party/install)) && cp /tmp/qa_twin52/raw/Fast-CDR-2.2.5/include/fastcdr/xcdr/optional.hpp /tmp/qa_twin52/soc-ap/third_party/install/include/fastcdr/xcdr/optional.hpp && rm -rf /tmp/qa_twin52/soc-ap/third_party/src/Fast-CDR-2.2.5 && (! bash /tmp/qa_twin52/soc-ap/third_party/build.sh --verify) && mkdir -p /tmp/qa_twin52/soc-ap/third_party/src/foonathan_memory-0.7-3 /tmp/qa_twin52/soc-ap/third_party/src/Fast-DDS-3.6.2/thirdparty/asio/asio/include /tmp/qa_twin52/soc-ap/third_party/src/Fast-DDS-3.6.2/thirdparty/tinyxml2 /tmp/qa_twin52/soc-ap/third_party/src/dbus-1.16.2 && touch /tmp/qa_twin52/soc-ap/third_party/src/Fast-DDS-3.6.2/thirdparty/asio/asio/include/asio.hpp /tmp/qa_twin52/soc-ap/third_party/src/Fast-DDS-3.6.2/thirdparty/tinyxml2/tinyxml2.cpp && bash /tmp/qa_twin52/soc-ap/third_party/build.sh fastcdr && bash /tmp/qa_twin52/soc-ap/third_party/build.sh --verify && bash /tmp/qa_twin52/soc-ap/third_party/build.sh && test "$(grep -c "if (val.storage_.engaged_)" /tmp/qa_twin52/soc-ap/third_party/install/include/fastcdr/xcdr/optional.hpp)" -eq 2 && cmake -S /tmp/qa_twin52/soc-ap/middleware/dds/tests -B /tmp/qa_twin52/build_opt_test && cmake --build /tmp/qa_twin52/build_opt_test --parallel && LD_LIBRARY_PATH="/tmp/qa_twin52/soc-ap/third_party/install/lib:${LD_LIBRARY_PATH:-}" ctest --test-dir /tmp/qa_twin52/build_opt_test --output-on-failure && cmake -S /tmp/qa_twin52/soc-ap/tests/dds/twin -B /tmp/qa_twin52/build_dds_twin && cmake --build /tmp/qa_twin52/build_dds_twin --parallel && LD_LIBRARY_PATH="/tmp/qa_twin52/soc-ap/third_party/install/lib:${LD_LIBRARY_PATH:-}" ctest --test-dir /tmp/qa_twin52/build_dds_twin --output-on-failure && rm -rf /tmp/qa_twin52'
    expected: 先注入未打补丁的原始optional.hpp触发third_party/build.sh --verify负向拒绝放行（[FAIL] missing engaged guard并返回非0），随后执行build.sh fastcdr自动从Fast-CDR-2.2.5.tar.gz干净解压、应用Fast-CDR-2.2.5-optional-engaged-guard.patch、重编并安装两处engaged守卫，再次执行build.sh --verify与build.sh校验100%通过；test_fastcdr_optional与test_dds_pubsub全套CTest 100% PASS且零SIGSEGV
    availability: available
  positive_cases:
  - Fast-CDR-2.2.5.tar.gz干净解压后通过third_party/patches/Fast-CDR-2.2.5-optional-engaged-guard.patch幂等打上两处if (val.storage_.engaged_)守卫
  - 脏内存上未激活的eprosima::fastcdr::optional<std::string>拷贝/移动构造与Fast-DDS participant/publisher创建100%通过且无SIGSEGV
  negative_cases:
  - 当install/include/fastcdr/xcdr/optional.hpp缺失if (val.storage_.engaged_)守卫时，verify_install拒绝放行并触发重新打补丁构建
required_evidence_level: server-sandbox-and-independent-review
verification_environment: docker-qa-sandbox-and-isolated-codex
qa_review_policy: project-control/.agents/rules/codex_qa_review.md
updated: '2026-11-05T10:31:00+08:00'
---

# TWIN-52 Fast-CDR 2.2.5 optional未初始化拷贝崩溃补丁固化与third_party可重现构建

## 1. 任务目标与来源
- **关联收件**：[`ISS-20261105-002.yaml`](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/work_intake/issues/ISS-20261105-002.yaml) / `DEM-20261105-002`
- **ARCH 方案依据**：[soc_ap_build_and_startup_issues_arch_breakdown_20261105.md](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/architecture/soc_ap_build_and_startup_issues_arch_breakdown_20261105.md) (`revision: 1`, SHA-256 `04be47f7ca02f7a98e4f249e8313309d32c9642a07574c011cb2161014ac5b36`)

## 2. 验收标准 (`acceptance_criteria`)
1. 新增受版本控制的补丁 `soc-ap/third_party/patches/Fast-CDR-2.2.5-optional-engaged-guard.patch`，在 `soc-ap/third_party/build.sh` 中固化幂等补丁应用与 `verify_install()` 守卫检查。
2. 新增 `soc-ap/middleware/dds/tests/test_fastcdr_optional.cpp` 覆盖脏内存未激活 `optional<std::string>` 拷贝/移动、已激活长字符串拷贝/移动与 Fast-DDS participant/publisher 启动，零 `SIGSEGV`。
