---
id: TWIN-67
title: TWIN-67 真实物理HIL全链路升级验收、MC U盘完整回归与升级部署说明书非实现者实操验证
revision: 1
plan_revision: vmware-soc-twin-20261106
task_kind: implementation
development_stage: vmware-twin
dispatchable: true
status: InProgress
blocked: false
planning_status: active
owner: 07a1f6dc-f47c-45e5-bf00-37ec14e2dfda
proposed_owner: INTEGRATOR
executor:
  role: INTEGRATOR
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
accepted_scope: Physical HIL full-chain upgrade verification (H01~H06, U01~U08, N05/N07/N08),
  non-implementer execution of minimc_v2_mcu_upgrade_and_hil_deployment_manual_20261105.md
  (revision 2, executable-validated), and 4-way physical evidence audit by independent
  Codex QA.
review_assignments:
  reviewer_sessions:
  - role: QA
    platform: codex
    model: gpt-6-luna
    planned_session_alias: planned-qa-twin-67
    session: null
    decision: PENDING
    evidence: docs/evidence/twin/TWIN-67/runs/qa_01/qa_review_report.md
  verifier_session: null
  integrator_session: null
primary_work_package: TASK-009
related_work_packages:
- TASK-007
- TASK-012
depends_on:
- TWIN-66
dependency_conditions:
- task: TWIN-66
  accepted_version: project-control=ae168003454eb18acbf5d867c15c52042cc87f4c; soc-ap=7184edfc796923e2f2c6e3e57ef3a9f791164b51;
    mcu-p3=3f1cfa66c6d27422cf038936b29aca7e45edb511; test_harness=cf81195eca55bcd772ef2daa2fd4aa41634c1492;
    boot/bootloadermc=faa2ed00dc9b6c8567dd44e875028f65073aab62; boot/bootloaderth=64b7100d3b0260ad1c24b627986475dcd45ad383
  acceptance_evidence: docs/evidence/twin/TWIN-66/runs/qa_05/qa_review_report.md
  required: 5端门禁与软件OTA套件通过QA+ARCH双审
scope_status: mapped
allowed_repositories:
- project-control
write_scope:
  project-control:
  - docs/guides/minimc_v2_mcu_upgrade_and_hil_deployment_manual_20261105.md
  - docs/evidence/twin/TWIN-67/**
allowed_paths:
- project-control/docs/guides/minimc_v2_mcu_upgrade_and_hil_deployment_manual_20261105.md
- project-control/docs/evidence/twin/TWIN-67/**
forbidden_paths:
- soc-ap/**
- mcu-p3/**
- boot/**
- test_harness/**
source_baseline:
  project-control: 5e8def0aed1a66e4583b5d3e5aed89b86f5a13db
  soc-ap: 7184edfc796923e2f2c6e3e57ef3a9f791164b51
  mcu-p3: 3f1cfa66c6d27422cf038936b29aca7e45edb511
  test_harness: cf81195eca55bcd772ef2daa2fd4aa41634c1492
  boot/bootloadermc: faa2ed00dc9b6c8567dd44e875028f65073aab62
  boot/bootloaderth: 64b7100d3b0260ad1c24b627986475dcd45ad383
base_commit: 5e8def0aed1a66e4583b5d3e5aed89b86f5a13db
branch: main
candidate_commit: null
dispatch_binding:
  source_commit: 5e8def0aed1a66e4583b5d3e5aed89b86f5a13db
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
worktree: project-control
lease:
  owner: 07a1f6dc-f47c-45e5-bf00-37ec14e2dfda
  task_revision: 1
  lease_id: lease-twin-67-20261106-01
  expires_at: '2026-11-07T22:00:00+08:00'
resources:
- resource: project-control-worktree
  location: project-control
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
  - project-control/docs/guides/minimc_v2_mcu_upgrade_and_hil_deployment_manual_20261105.md
  - project-control/docs/evidence/twin/TWIN-67/**
  record: docs/evidence/twin/TWIN-67/runs/author_01/result.md
rollback:
  steps:
  - git -C project-control checkout -- .
handoff:
  receiver_role: COORD
  receiver_session: ff2fb105-fd84-4ecb-b1e6-8f8eb00badc6
  transport: docs
  evidence_location: docs/evidence/twin/TWIN-67
  acknowledgement: accepted
verification:
  commands:
  - id: verify_twin-67_hil_bundle
    cwd: project-control
    command: 'test -f docs/guides/minimc_v2_mcu_upgrade_and_hil_deployment_manual_20261105.md
      && grep -q ''status: executable-validated'' docs/guides/minimc_v2_mcu_upgrade_and_hil_deployment_manual_20261105.md'
    expected: 实板四方物证齐全且升级部署说明书经非实现者实操验证切换为executable-validated
    availability: available
  positive_cases:
  - 完成D4-A受控双Boot迁移后，实板执行先TH后MC MiniMCProto v2.0升级(H01~H05)、MC U盘完整物理回归(U01~U08)及非实现者按说明书独立完成受控双板升级部署(H06)
  negative_cases:
  - 真机241665B/错板零擦除拒绝(N05)、断电/中断驻留Boot重传恢复(N08)、拔除/dev/ttyUSB*后CPU<=2%且3s内置哨兵值返回HTTP
    503/504(N07)
required_evidence_level: server-sandbox-and-independent-review
verification_environment: docker-qa-sandbox-and-isolated-codex
qa_review_policy: project-control/.agents/rules/codex_qa_review.md
updated: '2026-11-06T09:55:00+08:00'
---

# TWIN-67 真实物理HIL全链路升级验收、MC U盘完整回归与升级部署说明书非实现者实操验证

## 1. 权威架构与协议契约依据
- **主架构方案（`revision: 2`）**：[project-control/docs/architecture/minimc_v2_unified_mcu_upgrade_architecture_20261105.md](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/architecture/minimc_v2_unified_mcu_upgrade_architecture_20261105.md) (`sha256: b2b6d047500180c9f4d67d72c94794cbe5080caa52901ba262aa089bc1543223`)
- **协议主规范（`Rev 2.0.4`）**：[project-control/docs/specs/ap_mc_formal_protocol_v2_0_4_unified_ota_20261106.md](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/specs/ap_mc_formal_protocol_v2_0_4_unified_ota_20261106.md) (`sha256: ec874cab3f8f98fec6412b2da2b4f1fa52bfd8a33601da21e908b0ffaeb0522c`)

## 2. 验收标准 (`acceptance_criteria`)
1. 完成D4-A受控双Boot迁移后，实板执行先TH后MC MiniMCProto v2.0升级(H01~H05)、MC U盘完整物理回归(U01~U08)及非实现者按说明书独立完成受控双板升级部署(H06)
2. 真机241665B/错板零擦除拒绝(N05)、断电/中断驻留Boot重传恢复(N08)、拔除/dev/ttyUSB*后CPU<=2%且3s内置哨兵值返回HTTP 503/504(N07)
3. 全部新增/修改自研函数 100% 满足单函数 <= 50 行、入参 <= 4 个、零动态堆分配，且具备符合 `code_documentation_standard.md` 的中文说明注释。
