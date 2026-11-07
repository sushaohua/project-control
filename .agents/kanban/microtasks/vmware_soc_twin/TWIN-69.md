---
id: TWIN-69
title: TWIN-69 MiniMC OTA部署工具默认512B分块对齐与升级部署说明书能力位图勘误
revision: 1
plan_revision: vmware-soc-twin-20261107
task_kind: implementation
development_stage: vmware-twin
dispatchable: true
status: Review
blocked: true
blocker_reason: "前置依赖 TWIN-68 的受控 Docker QA 沙箱因宿主环境变量 GITLAB_TOKEN 过期（GitLab REST API v4 返回 HTTP 401 Token is expired）暂停待审。"
unblock_condition: "待 GITLAB_TOKEN 刷新、TWIN-68 通过受控 Docker 沙箱与独立 Codex 审阅（Done）后，立即执行 TWIN-69 的受控 Docker 沙箱与独立 Codex 只读审阅。"
planning_status: active
owner: cc065151-7c24-4606-b449-e03a5e7c2eba
proposed_owner: INTEGRATOR
executor:
  role: INTEGRATOR
  agent_id: cc065151-7c24-4606-b449-e03a5e7c2eba
  run_id: author_01
qa_policy: streamlined-v1
reviewer:
- QA
verifier: null
integrator: INTEGRATOR
requirement_id: REQ-20261105-003
feature_id: FEAT-20261106-002
demand_id: DEM-20261106-002
confirmation_id: CONFIRM-MINIMC-V2-UNIFIED-UPGRADE-20261106
approval_id: APPR-20261106-001
accepted_scope: "Docker QA sandbox (python3) verification of hil_deploy_via_minimc_ota.py DEFAULT_OTA_CHUNK_SIZE=512 (matching TH_BOOT_CAPABILITY_FLAGS=0xE0080423 Bits 16..23=0x08 -> 512B and CHUNK_MAX_SIZE=512U), chunk_size boundary validation, CLI arguments (--chunk-size 512, --port, --baud, --th-pkg, --mc-pkg, --receipt-out), 76,896B TH image 151-chunk streaming verification in test_mcu_firmware_upgrade.py, capability bitmap typo & 512B default chunk correction in minimc_v2_mcu_upgrade_and_hil_deployment_manual_20261105.md (revision 5), and Chinese code documentation check. Physical HIL hardware execution is out of scope for qa-sandbox:20261029; all in-scope checks are executed in server_qa so unexecuted is empty when those checks pass."
review_assignments:
  reviewer_sessions:
  - role: QA
    platform: codex
    model: gpt-6-luna
    planned_session_alias: planned-qa-twin-69-01
    session: null
    reviewer_session: null
    decision: PENDING
    commit_sha: null
    reviewed_task_revision: null
    artifact_version: null
    report_path: null
    evidence: null
    report_sha256: null
    session_evidence: null
  verifier_session: null
  integrator_session: null
primary_work_package: TASK-009
related_work_packages:
- TASK-007
- TASK-012
depends_on:
- TWIN-66
- TWIN-67
- TWIN-68
dependency_conditions:
- task: TWIN-66
  accepted_version: project-control=ae168003454eb18acbf5d867c15c52042cc87f4c; soc-ap=7184edfc796923e2f2c6e3e57ef3a9f791164b51;
    mcu-p3=3f1cfa66c6d27422cf038936b29aca7e45edb511; test_harness=cf81195eca55bcd772ef2daa2fd4aa41634c1492;
    boot/bootloadermc=faa2ed00dc9b6c8567dd44e875028f65073aab62; boot/bootloaderth=64b7100d3b0260ad1c24b627986475dcd45ad383
  acceptance_evidence: docs/evidence/twin/TWIN-66/runs/qa_05/qa_review_report.md
  required: 继承TWIN-66 test_harness部署工具与升级测试套件基线
- task: TWIN-67
  accepted_version: project-control=d9ed9b699067410f89c8119404f9895ec3fdb6f2; soc-ap=7184edfc796923e2f2c6e3e57ef3a9f791164b51;
    mcu-p3=3f1cfa66c6d27422cf038936b29aca7e45edb511; test_harness=cf81195eca55bcd772ef2daa2fd4aa41634c1492;
    boot/bootloadermc=faa2ed00dc9b6c8567dd44e875028f65073aab62; boot/bootloaderth=64b7100d3b0260ad1c24b627986475dcd45ad383
  acceptance_evidence: docs/evidence/twin/TWIN-67/runs/qa_03/qa_review_report.md
  required: 继承TWIN-67升级操作与HIL部署说明书(revision 4)基线
- task: TWIN-68
  accepted_version: mcu-p3=97c1c2422e98357e72cc822d2b5293b9e0c2abc6
  acceptance_evidence: docs/evidence/twin/TWIN-68/runs/qa_01/qa_review_report.md
  required: 串行继承TWIN-68 MC防下溢修复候选并执行跨仓整体联调
scope_status: mapped
allowed_repositories:
- test_harness
- project-control
write_scope:
  test_harness:
  - hil/tools/hil_deploy_via_minimc_ota.py
  - hil/tests/test_mcu_firmware_upgrade.py
  project-control:
  - docs/guides/minimc_v2_mcu_upgrade_and_hil_deployment_manual_20261105.md
  - docs/evidence/twin/TWIN-69/**
allowed_paths:
- test_harness/hil/tools/hil_deploy_via_minimc_ota.py
- test_harness/hil/tests/test_mcu_firmware_upgrade.py
- project-control/docs/guides/minimc_v2_mcu_upgrade_and_hil_deployment_manual_20261105.md
- project-control/docs/evidence/twin/TWIN-69/**
forbidden_paths:
- soc-ap/**
- mcu-p3/**
- boot/**
- test_harness/.agents/rules/**
source_baseline:
  project-control: b764378b4d3232d1c7ce77fd4922f520dd31ef51
  soc-ap: 7184edfc796923e2f2c6e3e57ef3a9f791164b51
  mcu-p3: 97c1c2422e98357e72cc822d2b5293b9e0c2abc6
  test_harness: cf81195eca55bcd772ef2daa2fd4aa41634c1492
  boot/bootloadermc: faa2ed00dc9b6c8567dd44e875028f65073aab62
  boot/bootloaderth: 64b7100d3b0260ad1c24b627986475dcd45ad383
base_commit: cf81195eca55bcd772ef2daa2fd4aa41634c1492
branch: main
candidate_commit: 54231c8d4372998bb91aefc3ec2df5c99169b274
dispatch_binding:
  source_commit: cf81195eca55bcd772ef2daa2fd4aa41634c1492
  workspace_diff_sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
  consumed_artifact_versions:
    arch_breakdown: b3c295be841195e34598f7f1eec91e6f02457ca9df0374e0147fe60be5344a76
    protocol_v2_0_4: ec874cab3f8f98fec6412b2da2b4f1fa52bfd8a33601da21e908b0ffaeb0522c
protocol_input:
  path: project-control/docs/specs/ap_mc_formal_protocol_v2_0_4_unified_ota_20261106.md
  sha256: ec874cab3f8f98fec6412b2da2b4f1fa52bfd8a33601da21e908b0ffaeb0522c
  revision: Rev 2.0.4
icd_versions:
- path: project-control/docs/architecture/minimc_v2_relay_underflow_and_512b_chunk_arch_breakdown_20261107.md
  version: 1
- path: project-control/docs/specs/ap_mc_formal_protocol_v2_0_4_unified_ota_20261106.md
  version: Rev 2.0.4
read_sources:
- project-control/.agents/rules/repository_rule_sources.json
- project-control/.agents/rules/repository_rule_boundaries.md
- test_harness/AGENTS.md
- test_harness/.agents/rules/shared/SOURCE.json
- project-control/.agents/rules/code_documentation_standard.md
- project-control/docs/architecture/minimc_v2_relay_underflow_and_512b_chunk_arch_breakdown_20261107.md
- project-control/docs/specs/ap_mc_formal_protocol_v2_0_4_unified_ota_20261106.md
- project-control/docs/guides/minimc_v2_mcu_upgrade_and_hil_deployment_manual_20261105.md
worktree: test_harness
lease:
  owner: cc065151-7c24-4606-b449-e03a5e7c2eba
  task_revision: 1
  lease_id: lease-twin-69-20261107-01
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
  - test_harness/hil/tools/hil_deploy_via_minimc_ota.py
  - test_harness/hil/tests/test_mcu_firmware_upgrade.py
  - project-control/docs/guides/minimc_v2_mcu_upgrade_and_hil_deployment_manual_20261105.md
  record: docs/evidence/twin/TWIN-69/runs/author_01/result.md
rollback:
  steps:
  - git -C test_harness checkout -- hil/tools/hil_deploy_via_minimc_ota.py hil/tests/test_mcu_firmware_upgrade.py
handoff:
  receiver_role: COORD
  receiver_session: ff2fb105-fd84-4ecb-b1e6-8f8eb00badc6
  transport: docs
  evidence_location: docs/evidence/twin/TWIN-69
  acknowledgement: received-author_01-54231c8d4372998bb91aefc3ec2df5c99169b274
verification:
  commands:
  - id: verify_ota_deploy_tool_512b_and_manual
    cwd: test_harness
    command: 'sh ../mcu-p3/motion-controller-mcu/tests/run_tests.sh && python3 hil/tools/hil_deploy_via_minimc_ota.py --self-test && python3 hil/tests/test_mcu_firmware_upgrade.py --self-test && python3 -m unittest discover -s hil/tests -p "test_mcu_firmware_upgrade.py" -v && python3 static_checks/minimcproto/run_ota_software_suite.py && grep -q "revision: 5" ../project-control/docs/guides/minimc_v2_mcu_upgrade_and_hil_deployment_manual_20261105.md && grep -q "Bits 16..23=0x08 (Bit19=1)" ../project-control/docs/guides/minimc_v2_mcu_upgrade_and_hil_deployment_manual_20261105.md'
    expected: hil_deploy_via_minimc_ota.py默认DEFAULT_OTA_CHUNK_SIZE=512（76,896B镜像精确切分151块）、能力位0xE0080423/0xC0080435解码512B校验、非法chunk_size拦截、test_mcu_firmware_upgrade.py与run_ota_software_suite.py全量PASS
    availability: available
  positive_cases:
  - hil_deploy_via_minimc_ota.py固化DEFAULT_OTA_CHUNK_SIZE=512，支持CLI参数--chunk-size 512/--port/--baud/--th-pkg/--mc-pkg/--receipt-out，76896B TH固件切分为151块完成Stage 1~4验证
  - 升级操作与HIL部署说明书(revision 5)修正0xE0080423能力位注释为Bits 16..23=0x08 (Bit19=1) 512B最大分块，并对齐默认512B(151块)部署参数说明
  negative_cases:
  - 传入非法chunk_size（<=0或>512）时确定性拦截并记录错误；严禁回退默认64B分块
required_evidence_level: server-sandbox-and-independent-review
verification_environment: docker-qa-sandbox-and-isolated-codex
qa_review_policy: project-control/.agents/rules/codex_qa_review.md
updated: '2026-11-07T09:18:00+08:00'
---

# TWIN-69 MiniMC OTA部署工具默认512B分块对齐与升级部署说明书能力位图勘误

## 1. 权威架构与协议契约依据
- **关联收件**：[`FEAT-20261106-002.yaml`](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/work_intake/features/FEAT-20261106-002.yaml) / `DEM-20261106-002`
- **专项架构拆解方案（`revision: 1`）**：[project-control/docs/architecture/minimc_v2_relay_underflow_and_512b_chunk_arch_breakdown_20261107.md](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/architecture/minimc_v2_relay_underflow_and_512b_chunk_arch_breakdown_20261107.md) (`sha256: b3c295be841195e34598f7f1eec91e6f02457ca9df0374e0147fe60be5344a76`)
- **协议主规范（`Rev 2.0.4`）**：[project-control/docs/specs/ap_mc_formal_protocol_v2_0_4_unified_ota_20261106.md](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/specs/ap_mc_formal_protocol_v2_0_4_unified_ota_20261106.md) (`sha256: ec874cab3f8f98fec6412b2da2b4f1fa52bfd8a33601da21e908b0ffaeb0522c`)

## 2. 验收标准 (`acceptance_criteria`)
1. 在 `test_harness/hil/tools/hil_deploy_via_minimc_ota.py` 中固化 `DEFAULT_OTA_CHUNK_SIZE = 512` / `MAX_OTA_CHUNK_SIZE = 512`、能力位最大分块（`0xE0080423` / `0xC0080435` `Bits 16..23 = 0x08` -> `512B`）校验、非法 `chunk_size` 边界拦截及完整 CLI 参数入口（`--chunk-size 512`），并在 `test_harness/hil/tests/test_mcu_firmware_upgrade.py` 中补充 `76,896 B` 固件 `151` 块流式发送与非法分块拦截单测。
2. 在 `project-control/docs/guides/minimc_v2_mcu_upgrade_and_hil_deployment_manual_20261105.md`（升级至 `revision: 5`）中勘误第 37 行 `TH Bootloader` `0xE0080423` 位图说明为 `Bits 16..23=0x08 (Bit19=1)` 512B 最大分块，并更新默认 `512B`（`151` 块）部署说明。
3. 全部新增/修改代码具备符合 `code_documentation_standard.md` 的中文说明注释与 docstring。
