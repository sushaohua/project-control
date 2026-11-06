---
id: TWIN-65
title: TWIN-65 SoC AP协议栈对齐Rev 2.0.4、/var/update原子封存、维护互斥与四阶段升级编排服务
revision: 1
plan_revision: vmware-soc-twin-20261106
task_kind: implementation
development_stage: vmware-twin
dispatchable: true
status: Review
blocked: false
planning_status: active
owner: 07a1f6dc-f47c-45e5-bf00-37ec14e2dfda
proposed_owner: ENG-FWD
executor:
  role: ENG-FWD
  agent_id: 07a1f6dc-f47c-45e5-bf00-37ec14e2dfda
  run_id: author_01
qa_policy: streamlined-v1
reviewer:
- QA
verifier: null
integrator: INTEGRATOR
requirement_id: REQ-20261105-003
demand_id: DEM-20261105-006
confirmation_id: CONFIRM-MINIMC-V2-UNIFIED-UPGRADE-20261106
approval_id: APPR-20261106-001
accepted_scope: "Docker QA sandbox (gcc/g++ + cmake + ctest) verification of SoC AP Rev 2.0.4 protocol alignment (remove 0x05 ESTOP_ACK, move SYSTEM_CONTROL to 0x1D, add 0x20~0x23 structs & 520B payload support), /var/update .part->.bin->sealed read-only staging and offline 128B ATSG Trailer verification, 4-condition safety admission & UPGRADING_MAINTENANCE state interlock, Stage 1~4 stop-and-wait upgrade orchestrator, and S04 function length (<=50), params (<=4) & Chinese comment checks. Physical HIL verification (covered by TWIN-67) is out of scope for qa-sandbox:20261029; all in-scope checks are executed in server_qa so unexecuted is empty when those checks pass."
review_assignments:
  reviewer_sessions:
  - role: QA
    platform: codex
    model: gpt-6-luna
    planned_session_alias: planned-qa-twin-65
    session: null
    decision: PENDING
    evidence: docs/evidence/twin/TWIN-65/runs/qa_01/qa_review_report.md
  verifier_session: null
  integrator_session: null
primary_work_package: TASK-009
related_work_packages:
- TASK-007
- TASK-012
depends_on:
- TWIN-57
- TWIN-58
- TWIN-59
dependency_conditions:
- task: TWIN-57
  accepted_version: project-control=960f079647a00864fe7913836336b2a2ee3d729a; soc-ap=c6692b244e0aa09d04e7051293f9fef3c67535dd;
    mcu-p3=891a8bb252814c83992a49b01fbe11ba83b92a1f; test_harness=d14ed04321c6d4f5ddb35a8801604a8af53b5b60
  acceptance_evidence: docs/evidence/twin/TWIN-57/runs/qa_03/qa_review_report.md
  required: 继承TWIN-57 forward与device_manager状态机基线
- task: TWIN-58
  accepted_version: project-control=c1d2c461aa65e6497c295843a2735d0d02ee2e2d; soc-ap=c6692b244e0aa09d04e7051293f9fef3c67535dd;
    mcu-p3=57674d8b07d6c75a4d20b3fcd52c23df964aa7a7; test_harness=19c12bfeeac852670e8bdcb65ce0abcd1de121c1
  acceptance_evidence: docs/evidence/twin/TWIN-58/runs/qa_06/qa_review_report.md
  required: 继承TWIN-58 ui_gateway与browser_hmi基线
- task: TWIN-59
  accepted_version: project-control=c1d2c461aa65e6497c295843a2735d0d02ee2e2d; soc-ap=c6692b244e0aa09d04e7051293f9fef3c67535dd;
    mcu-p3=57674d8b07d6c75a4d20b3fcd52c23df964aa7a7; test_harness=19c12bfeeac852670e8bdcb65ce0abcd1de121c1
  acceptance_evidence: docs/evidence/twin/TWIN-59/runs/qa_06/qa_review_report.md
  required: 继承TWIN-59 core/middleware/runtime基线
scope_status: mapped
allowed_repositories:
- soc-ap
- project-control
write_scope:
  soc-ap:
  - contracts/twin/telemetry_types.h
  - services/forward/**
  - services/device_manager/**
  - services/ui_gateway/**
  - tests/forward/**
  - tests/device_manager/**
  - tests/ui_gateway/**
  - CMakeLists.txt
  project-control:
  - docs/evidence/twin/TWIN-65/**
allowed_paths:
- soc-ap/contracts/twin/telemetry_types.h
- soc-ap/services/forward/**
- soc-ap/services/device_manager/**
- soc-ap/services/ui_gateway/**
- soc-ap/tests/forward/**
- soc-ap/tests/device_manager/**
- soc-ap/tests/ui_gateway/**
- soc-ap/CMakeLists.txt
- project-control/docs/evidence/twin/TWIN-65/**
forbidden_paths:
- mcu-p3/**
- boot/**
- test_harness/**
- soc-ap/.agents/rules/**
source_baseline:
  project-control: 9798fdf601d958d2c5064220d9ff0d29a3f5e0ad
  soc-ap: c6692b244e0aa09d04e7051293f9fef3c67535dd
  mcu-p3: 57674d8b07d6c75a4d20b3fcd52c23df964aa7a7
  test_harness: 19c12bfeeac852670e8bdcb65ce0abcd1de121c1
  boot/bootloadermc: 4fc171ea61912561949b9a0cfc1da8975e4c39ba
  boot/bootloaderth: 769fccbe52464ad7ceb856c5e89cb0d25abbbf87
base_commit: c6692b244e0aa09d04e7051293f9fef3c67535dd
branch: main
candidate_commit: 42a1dc4465b4a848c768283c570a48be63ec1e6b
dispatch_binding:
  source_commit: c6692b244e0aa09d04e7051293f9fef3c67535dd
  workspace_diff_sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
  consumed_artifact_versions:
    master_upgrade_architecture: b2b6d047500180c9f4d67d72c94794cbe5080caa52901ba262aa089bc1543223
    protocol_v2_0_4: ec874cab3f8f98fec6412b2da2b4f1fa52bfd8a33601da21e908b0ffaeb0522c
protocol_input:
  path: project-control/docs/specs/ap_mc_formal_protocol_v2_0_4_unified_ota_20261106.md
  sha256: ec874cab3f8f98fec6412b2da2b4f1fa52bfd8a33601da21e908b0ffaeb0522c
  revision: Rev 2.0.4
icd_versions:
- path: project-control/docs/architecture/minimc_v2_unified_mcu_upgrade_architecture_20261105.md
  version: 2
- path: project-control/docs/specs/ap_mc_formal_protocol_v2_0_4_unified_ota_20261106.md
  version: Rev 2.0.4
read_sources:
- project-control/.agents/rules/repository_rule_sources.json
- project-control/.agents/rules/repository_rule_boundaries.md
- project-control/.agents/rules/bootloader_role_boundaries.md
- project-control/.agents/rules/c_cpp_coding_standard.md
- project-control/.agents/rules/code_documentation_standard.md
- project-control/docs/architecture/minimc_v2_unified_mcu_upgrade_architecture_20261105.md
- project-control/docs/specs/ap_mc_formal_protocol_v2_0_4_unified_ota_20261106.md
- project-control/docs/planning/minimc_v2_upgrade_engineering_inputs_20261105.md
- project-control/docs/planning/minimc_v2_upgrade_qa_planning_input_20261105.md
- project-control/docs/guides/minimc_v2_mcu_upgrade_and_hil_deployment_manual_20261105.md
worktree: soc-ap
lease:
  owner: 07a1f6dc-f47c-45e5-bf00-37ec14e2dfda
  task_revision: 1
  lease_id: lease-twin-65-20261106-01
  expires_at: '2026-11-07T22:00:00+08:00'
resources:
- resource: soc-ap-worktree
  location: soc-ap
  exclusive: false
  pending: null
budget:
  planned_checkpoint_minutes: 60
  max_evidence_based_corrections: 2
  on_limit: 保存证据交COORD
checkpoint: 开工前绑定；自检单测与注释规范检查；独立沙箱与QA审查；收件
execution_contract: project-control/docs/planning/vmware_soc_twin_task_execution_20261029.md
readiness_pending: []
deliverables:
  artifacts:
  - soc-ap/contracts/twin/telemetry_types.h
  - soc-ap/services/forward/**
  - soc-ap/services/device_manager/**
  - soc-ap/services/ui_gateway/**
  - soc-ap/tests/forward/**
  - soc-ap/tests/device_manager/**
  - soc-ap/tests/ui_gateway/**
  record: docs/evidence/twin/TWIN-65/runs/author_01/result.md
rollback:
  steps:
  - git -C soc-ap checkout -- .
handoff:
  receiver_role: COORD
  receiver_session: ff2fb105-fd84-4ecb-b1e6-8f8eb00badc6
  transport: docs
  evidence_location: docs/evidence/twin/TWIN-65
  acknowledgement: accepted
verification:
  commands:
  - id: build_and_verify_twin-65
    cwd: soc-ap
    command: rm -rf /tmp/qa_twin65 && mkdir -p /tmp/qa_twin65 && cp -r ../soc-ap /tmp/qa_twin65/soc-ap
      && rm -rf /tmp/qa_twin65/soc-ap/build && ([ -e /tmp/qa_twin65/soc-ap/third_party/install
      ] || (mkdir -p /tmp/qa_twin65/soc-ap/third_party && ln -s /usr/local /tmp/qa_twin65/soc-ap/third_party/install))
      && cd /tmp/qa_twin65/soc-ap && bash tools/deploy_twin.sh --build-only && ctest
      --test-dir build/forward --output-on-failure && ctest --test-dir build/device_manager
      --output-on-failure && ctest --test-dir build/ui_gateway --output-on-failure
      && rm -rf /tmp/qa_twin65
    expected: soc-ap编译及forward/device_manager/ui_gateway全部单测与OTA四阶段状态机测试100%通过
    availability: available
  positive_cases:
  - 对齐Rev 2.0.4头文件与520B帧容量，实现/var/update封存与128B ATSG预检、4项安全准入、UPGRADING_MAINTENANCE维护互斥及Stage
    1~4四阶段升级状态机（先TH后MC）
  negative_cases:
  - .part未完成文件不触发就绪；温度失效或加热非0%拒绝进入升级；维护态拦截普通运动/调温/打印请求回HTTP 409/503；未完成Stage 4新App在线核验严禁宣称100%
    SUCCEEDED
required_evidence_level: server-sandbox-and-independent-review
verification_environment: docker-qa-sandbox-and-isolated-codex
qa_review_policy: project-control/.agents/rules/codex_qa_review.md
updated: '2026-11-06T09:55:00+08:00'
---

# TWIN-65 SoC AP协议栈对齐Rev 2.0.4、/var/update原子封存、维护互斥与四阶段升级编排服务

## 1. 权威架构与协议契约依据
- **主架构方案（`revision: 2`）**：[project-control/docs/architecture/minimc_v2_unified_mcu_upgrade_architecture_20261105.md](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/architecture/minimc_v2_unified_mcu_upgrade_architecture_20261105.md) (`sha256: b2b6d047500180c9f4d67d72c94794cbe5080caa52901ba262aa089bc1543223`)
- **协议主规范（`Rev 2.0.4`）**：[project-control/docs/specs/ap_mc_formal_protocol_v2_0_4_unified_ota_20261106.md](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/specs/ap_mc_formal_protocol_v2_0_4_unified_ota_20261106.md) (`sha256: ec874cab3f8f98fec6412b2da2b4f1fa52bfd8a33601da21e908b0ffaeb0522c`)

## 2. 验收标准 (`acceptance_criteria`)
1. 对齐Rev 2.0.4头文件与520B帧容量，实现/var/update封存与128B ATSG预检、4项安全准入、UPGRADING_MAINTENANCE维护互斥及Stage 1~4四阶段升级状态机（先TH后MC）
2. .part未完成文件不触发就绪；温度失效或加热非0%拒绝进入升级；维护态拦截普通运动/调温/打印请求回HTTP 409/503；未完成Stage 4新App在线核验严禁宣称100% SUCCEEDED
3. 全部新增/修改自研函数 100% 满足单函数 <= 50 行、入参 <= 4 个、零动态堆分配，且具备符合 `code_documentation_standard.md` 的中文说明注释。
