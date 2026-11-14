---
id: TWIN-28
title: TWIN-28 端到端真实双MCU固件升级在环联调与验收
revision: 1
plan_revision: vmware-soc-twin-20261029
task_kind: test
development_stage: vmware-twin
dispatchable: true
status: Backlog
blocked: true
block_reason: "前置任务TWIN-26被人为冻结，暂不推进"
planning_status: planned
owner: null
proposed_owner: INTEGRATOR
executor:
  role: INTEGRATOR
  agent_id: null
  run_id: null
reviewer:
- QA
- ARCH
verifier: null
integrator: INTEGRATOR
review_assignments:
  reviewer_sessions:
  - role: QA
    platform: codex
    model: gpt-6-luna
    planned_session_alias: planned-qa-twin-28
    session: null
    session_evidence: null
    decision: null
    reviewed_task_revision: null
    artifact_version: null
    evidence: null
    report_sha256: null
  - role: ARCH
    platform: codex
    model: gpt-6-luna
    planned_session_alias: planned-arch-twin-28
    session: null
    session_evidence: null
    decision: null
    reviewed_task_revision: null
    artifact_version: null
    evidence: null
    report_sha256: null
  verifier_session: null
  integrator_session: null
primary_work_package: TASK-012
related_work_packages:
- TASK-002
- TASK-007
depends_on:
- TWIN-27
dependency_conditions:
- task: TWIN-27
  accepted_version: null
  acceptance_evidence: null
  required: 开工前继承TWIN-27 固件扫描与安全准入服务实现基线
scope_status: mapped
allowed_repositories:
- test_harness
- project-control
write_scope:
  test_harness:
  - hil/tests/test_mcu_firmware_upgrade.py
  project-control:
  - docs/evidence/twin/TWIN-28/**
allowed_paths:
- test_harness/hil/tests/test_mcu_firmware_upgrade.py
- project-control/docs/evidence/twin/TWIN-28/**
source_baseline:
  project-control: 8ea89b9d1e442894be6bc1f92e4aa1a4c954f9a0
  soc-ap: 6850cc553d405b5e7e511ff181d985fdee8e221f
  mcu-p3: 9b017f186665c2c9226146cc0fdc34af3ad5242b
  test_harness: 0b7497ba43158841eb3c4af7f16e477b9c30c2c5
base_commit: 0b7497ba43158841eb3c4af7f16e477b9c30c2c5
candidate_commit: null
dispatch_binding:
  source_commit: 0b7497ba43158841eb3c4af7f16e477b9c30c2c5
  workspace_diff_sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
  consumed_artifact_versions: {}
protocol_input:
  path: project-control/docs/analysis/mcu_firmware_upgrade_design_20261031.md
  sha256: c5a79270ec6017a071944bbf314ebb11e345ec61d62fee6f5563336110c7505c
  revision: 1
read_sources:
- project-control/docs/planning/product/first_release_scope_decision_20261029.md
- project-control/docs/planning/product/first_release_requirements_and_task_decomposition_20261029.md
- project-control/docs/analysis/mcu_firmware_upgrade_design_20261031.md
- project-control/.agents/rules/c_cpp_coding_standard.md
worktree: test_harness
lease:
  owner: null
  task_revision: 1
  lease_id: null
  expires_at: null
resources:
- resource: physical-hardware-mcu-bench
  location: VMware /dev/ttyUSB0 and ST-Link probes
  exclusive: true
  pending: null
budget:
  planned_checkpoint_minutes: 40
  max_evidence_based_corrections: 2
  on_limit: 保存证据交COORD
checkpoint: 开工前绑定；真实物理刷写与0x01/0x02版本对账；准确候选独立检查；收件
execution_contract: project-control/docs/planning/vmware_soc_twin_task_execution_20261029.md
readiness_pending: []
deliverables:
  artifacts:
  - test_harness/hil/tests/test_mcu_firmware_upgrade.py
  record: docs/evidence/twin/TWIN-28/runs/<actual-run>/result.md
rollback:
  steps:
  - 仅回退本票候选；保存失败证据和原状态；硬件恢复须按实际SOP及授权执行
handoff:
  receiver_role: COORD
  receiver_session: session-coord-main
  transport: docs
  evidence_location: docs/evidence/twin/TWIN-28
  acknowledgement: null
verification:
  commands:
  - id: check_graph
    cwd: .
    command: PYTHONDONTWRITEBYTECODE=1 python3 project-control/tools/check_task_graph.py
      --workspace .
    expected: 结构无错误；不等于任务/运行/硬件接受
    availability: local
  - id: planned_build_and_acceptance
    cwd: .
    command: Ready前由Owner绑定本票实际构建与正反例运行入口
    expected: 在真实物理MC/TH台架上实测刷写；版本回读对账与开机Banner验证；零Mock
    availability: planned-not-runnable
  positive_cases:
  - 在VMware指定目录放入fw_mc.bin与fw_th.bin，真实物理刷新MC与TH，0x01与0x02回读新版本匹配
  negative_cases:
  - 严禁以虚拟PTY或本地文件复制冒充真实升级；未完成真实物理刷写直接一票否决
required_evidence_level: hardware-verified
verification_environment: hardware-bench
qa_review_policy: project-control/.agents/rules/codex_qa_review.md
updated: '2026-10-31T11:30:00+08:00'
---

# TWIN-28 端到端真实双MCU固件升级在环联调与验收

## 1. 目标与依据

根据系统决定 **U-D05**（首版纳入 VMware 指定目录真实双 MCU 固件升级），本任务在物理台架上执行端到端真实双 MCU 固件刷写与在环联调验收：
1. 真实物理环境刷写：严禁将文件复制或模拟升级当作真实升级成功（零 Mock、零 PTY）；
2. 完整记录升级前版本查询（`0x01` / `0x02`）、升级分块进度、Flash 写入回读校验与升级后开机 Banner 及版本核验；
3. 执行独立 Codex QA 审查与非作者 ARCH 架构复核，完成硬件验证级别验收。

参考文档：
- [ARCH-MCU-UPGRADE-DESIGN-20261031.md](../../../../docs/analysis/mcu_firmware_upgrade_design_20261031.md)
