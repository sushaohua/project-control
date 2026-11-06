---
id: TWIN-66
title: TWIN-66 5端契约静态门禁、G01~G25黄金向量、Docker软件OTA集成测试套件与自动化部署工具
revision: 2
plan_revision: vmware-soc-twin-20261106
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
requirement_id: REQ-20261105-003
demand_id: DEM-20261105-006
confirmation_id: CONFIRM-MINIMC-V2-UNIFIED-UPGRADE-20261106
approval_id: APPR-20261106-001
accepted_scope: "Docker QA sandbox (python3) verification and independent non-author review (QA + ARCH) of 5-endpoint check_opcode_alignment.py (with reverse numeric uniqueness check), G01~G25 golden byte vectors, run_ota_software_suite.py (S01~S04, D01~D08, C01~C09, M01~M08, N01~N10), hil_deploy_via_minimc_ota.py, test_mcu_firmware_upgrade.py (--self-test), and Chinese code documentation check. Physical HIL hardware execution (covered by TWIN-67) is out of scope for qa-sandbox:20261029; all in-scope checks are executed in server_qa so unexecuted is empty when those checks pass."
review_assignments:
  reviewer_sessions:
  - role: QA
    platform: codex
    model: gpt-6-luna
    planned_session_alias: planned-qa-twin-66
    session: null
    decision: PENDING
    evidence: docs/evidence/twin/TWIN-66/runs/qa_02/qa_review_report.md
  - role: ARCH
    platform: codex
    model: gpt-6-luna
    planned_session_alias: planned-arch-twin-66
    session: null
    decision: PENDING
    evidence: docs/evidence/twin/TWIN-66/runs/qa_02/arch_review_report.md
  verifier_session: null
  integrator_session: null
primary_work_package: TASK-009
related_work_packages:
- TASK-007
- TASK-012
depends_on:
- TWIN-61
- TWIN-62
- TWIN-63
- TWIN-64
- TWIN-65
dependency_conditions:
- task: TWIN-61
  accepted_version: project-control=c1d2c461aa65e6497c295843a2735d0d02ee2e2d; soc-ap=c6692b244e0aa09d04e7051293f9fef3c67535dd;
    mcu-p3=57674d8b07d6c75a4d20b3fcd52c23df964aa7a7; test_harness=f41d93b753cfd4496f8d5c82fe1c032d1a4d4803
  acceptance_evidence: docs/evidence/twin/TWIN-61/runs/qa_07/qa_review_report.md
  required: 继承TWIN-61 test_harness基线
- task: TWIN-62
  accepted_version: project-control=45c5cdf791ae3d88b76949525ec1b46d25832083; soc-ap=c6692b244e0aa09d04e7051293f9fef3c67535dd;
    mcu-p3=57674d8b07d6c75a4d20b3fcd52c23df964aa7a7; test_harness=19c12bfeeac852670e8bdcb65ce0abcd1de121c1;
    boot/bootloadermc=4fc171ea61912561949b9a0cfc1da8975e4c39ba; boot/bootloaderth=64b7100d3b0260ad1c24b627986475dcd45ad383
  acceptance_evidence: docs/evidence/twin/TWIN-62/runs/qa_04/qa_review_report.md
  required: TH Boot v2.0就绪
- task: TWIN-63
  accepted_version: project-control=2a86f91735f6865626b0794b726d90e1f2247d68; soc-ap=c6692b244e0aa09d04e7051293f9fef3c67535dd;
    mcu-p3=57674d8b07d6c75a4d20b3fcd52c23df964aa7a7; test_harness=19c12bfeeac852670e8bdcb65ce0abcd1de121c1;
    boot/bootloadermc=faa2ed00dc9b6c8567dd44e875028f65073aab62; boot/bootloaderth=769fccbe52464ad7ceb856c5e89cb0d25abbbf87
  acceptance_evidence: docs/evidence/twin/TWIN-63/runs/qa_03/qa_review_report.md
  required: MC Boot v2.0就绪
- task: TWIN-64
  accepted_version: project-control=6d8b9dc8a59366c9e0d0c8126240b1caf69ab321; soc-ap=c6692b244e0aa09d04e7051293f9fef3c67535dd;
    mcu-p3=3f1cfa66c6d27422cf038936b29aca7e45edb511; test_harness=19c12bfeeac852670e8bdcb65ce0abcd1de121c1;
    boot/bootloadermc=4fc171ea61912561949b9a0cfc1da8975e4c39ba; boot/bootloaderth=769fccbe52464ad7ceb856c5e89cb0d25abbbf87
  acceptance_evidence: docs/evidence/twin/TWIN-64/runs/qa_04/qa_review_report.md
  required: MC/TH App v2.0就绪
- task: TWIN-65
  accepted_version: project-control=bc4c58b9b8230feb75ba956953978fcd5786af4d; soc-ap=7184edfc796923e2f2c6e3e57ef3a9f791164b51;
    mcu-p3=57674d8b07d6c75a4d20b3fcd52c23df964aa7a7; test_harness=19c12bfeeac852670e8bdcb65ce0abcd1de121c1;
    boot/bootloadermc=4fc171ea61912561949b9a0cfc1da8975e4c39ba; boot/bootloaderth=769fccbe52464ad7ceb856c5e89cb0d25abbbf87
  acceptance_evidence: docs/evidence/twin/TWIN-65/runs/qa_04/qa_review_report.md
  required: SoC AP OTA服务就绪
scope_status: mapped
allowed_repositories:
- test_harness
- project-control
write_scope:
  test_harness:
  - static_checks/minimcproto/**
  - hil/tools/hil_deploy_via_minimc_ota.py
  - hil/twin_capture/twin_capture_analyzer.py
  - hil/tools/debug_reconciliation_probe.py
  - hil/tests/test_mcu_firmware_upgrade.py
  project-control:
  - docs/evidence/twin/TWIN-66/**
allowed_paths:
- test_harness/static_checks/minimcproto/**
- test_harness/hil/tools/hil_deploy_via_minimc_ota.py
- test_harness/hil/twin_capture/twin_capture_analyzer.py
- test_harness/hil/tools/debug_reconciliation_probe.py
- test_harness/hil/tests/test_mcu_firmware_upgrade.py
- project-control/docs/evidence/twin/TWIN-66/**
forbidden_paths:
- soc-ap/**
- mcu-p3/**
- boot/**
- test_harness/.agents/rules/**
source_baseline:
  project-control: d817294ac45357e718acb0b2908088492110b4f1
  soc-ap: 7184edfc796923e2f2c6e3e57ef3a9f791164b51
  mcu-p3: 3f1cfa66c6d27422cf038936b29aca7e45edb511
  test_harness: f41d93b753cfd4496f8d5c82fe1c032d1a4d4803
  boot/bootloadermc: faa2ed00dc9b6c8567dd44e875028f65073aab62
  boot/bootloaderth: 64b7100d3b0260ad1c24b627986475dcd45ad383
base_commit: f41d93b753cfd4496f8d5c82fe1c032d1a4d4803
branch: main
candidate_commit: 3e3fb659e9bb3e54222ded1169a70fc331681c48
dispatch_binding:
  source_commit: f41d93b753cfd4496f8d5c82fe1c032d1a4d4803
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
worktree: test_harness
lease:
  owner: 07a1f6dc-f47c-45e5-bf00-37ec14e2dfda
  task_revision: 2
  lease_id: lease-twin-66-20261106-01
  expires_at: '2026-11-07T22:00:00+08:00'
resources:
- resource: test_harness-worktree
  location: test_harness
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
  - test_harness/static_checks/minimcproto/**
  - test_harness/hil/tools/hil_deploy_via_minimc_ota.py
  - test_harness/hil/tests/test_mcu_firmware_upgrade.py
  record: docs/evidence/twin/TWIN-66/runs/author_01/result.md
rollback:
  steps:
  - git -C test_harness checkout -- .
handoff:
  receiver_role: COORD
  receiver_session: ff2fb105-fd84-4ecb-b1e6-8f8eb00badc6
  transport: docs
  evidence_location: docs/evidence/twin/TWIN-66
  acknowledgement: accepted
verification:
  commands:
  - id: verify_twin-66
    cwd: test_harness
    command: python3 static_checks/minimcproto/check_opcode_alignment.py && python3
      static_checks/minimcproto/run_codec_cases.py && python3 static_checks/minimcproto/run_ota_software_suite.py
      && python3 hil/tests/test_mcu_firmware_upgrade.py --self-test
    expected: 5端命令与520B容量静态门禁、G01~G25黄金向量及Docker软件OTA全链路集成测试100%通过
    availability: available
  positive_cases:
  - 升级5端check_opcode_alignment.py含反向数值唯一性断言，固化G01~G25固定字节黄金向量，通过S01~S04/D01~D08/C01~C09/M01~M08/N01~N10软件集成测试并交付hil_deploy_via_minimc_ota.py
  negative_cases:
  - 注入冲突宏数值、伪0x05 ACK、241665B超限包、错board_id、内块CRC损坏与断电中断场景100%按契约拦截或恢复
required_evidence_level: server-sandbox-and-independent-review
verification_environment: docker-qa-sandbox-and-isolated-codex
qa_review_policy: project-control/.agents/rules/codex_qa_review.md
updated: '2026-11-06T09:55:00+08:00'
---

# TWIN-66 5端契约静态门禁、G01~G25黄金向量、Docker软件OTA集成测试套件与自动化部署工具

## 1. 权威架构与协议契约依据
- **主架构方案（`revision: 2`）**：[project-control/docs/architecture/minimc_v2_unified_mcu_upgrade_architecture_20261105.md](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/architecture/minimc_v2_unified_mcu_upgrade_architecture_20261105.md) (`sha256: b2b6d047500180c9f4d67d72c94794cbe5080caa52901ba262aa089bc1543223`)
- **协议主规范（`Rev 2.0.4`）**：[project-control/docs/specs/ap_mc_formal_protocol_v2_0_4_unified_ota_20261106.md](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/specs/ap_mc_formal_protocol_v2_0_4_unified_ota_20261106.md) (`sha256: ec874cab3f8f98fec6412b2da2b4f1fa52bfd8a33601da21e908b0ffaeb0522c`)

## 2. 验收标准 (`acceptance_criteria`)
1. 升级5端check_opcode_alignment.py含反向数值唯一性断言，固化G01~G25固定字节黄金向量，通过S01~S04/D01~D08/C01~C09/M01~M08/N01~N10软件集成测试并交付hil_deploy_via_minimc_ota.py
2. 注入冲突宏数值、伪0x05 ACK、241665B超限包、错board_id、内块CRC损坏与断电中断场景100%按契约拦截或恢复
3. 全部新增/修改自研函数 100% 满足单函数 <= 50 行、入参 <= 4 个、零动态堆分配，且具备符合 `code_documentation_standard.md` 的中文说明注释。
