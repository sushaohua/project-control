---
id: TWIN-27
title: TWIN-27 AP端VMware指定目录固件扫描与安全准入服务实现
revision: 1
plan_revision: vmware-soc-twin-20261029
task_kind: implementation
development_stage: vmware-twin
dispatchable: true
status: Backlog
blocked: true
block_reason: "前置任务TWIN-26被人为冻结，暂不推进"
planning_status: planned
owner: null
proposed_owner: ENG-NET
executor:
  role: ENG-NET
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
    planned_session_alias: planned-qa-twin-27
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
    planned_session_alias: planned-arch-twin-27
    session: null
    session_evidence: null
    decision: null
    reviewed_task_revision: null
    artifact_version: null
    evidence: null
    report_sha256: null
  verifier_session: null
  integrator_session: null
primary_work_package: TASK-007
related_work_packages:
- TASK-008
- TASK-002
depends_on:
- TWIN-26
- TWIN-49
dependency_conditions:
- task: TWIN-26
  accepted_version: mcu-p3=04231388c842c1ce3e5b71675d0dc118a65edf2e
  acceptance_evidence: docs/evidence/twin/TWIN-26/runs/run_01/qa_review_report.md
  required: 开工前继承TWIN-26 双MCU升级通道与IAP协议基线
- task: TWIN-49
  accepted_version: pending
  acceptance_evidence: docs/evidence/twin/TWIN-49/runs/qa_01/qa_review_report.md
  required: 开工前继承TWIN-49 forward_service与921600双节点级联协议基线
scope_status: mapped
allowed_repositories:
- soc-ap
- project-control
write_scope:
  soc-ap:
  - services/forward/forward_service.cpp
  - services/forward/forward_service.h
  - services/device_manager/firmware_updater.cpp
  - services/device_manager/firmware_updater.h
  - tests/device_manager/twin/test_firmware_updater.cpp
  project-control:
  - docs/evidence/twin/TWIN-27/**
allowed_paths:
- soc-ap/services/forward/forward_service.cpp
- soc-ap/services/forward/forward_service.h
- soc-ap/services/device_manager/firmware_updater.cpp
- soc-ap/services/device_manager/firmware_updater.h
- soc-ap/tests/device_manager/twin/test_firmware_updater.cpp
- project-control/docs/evidence/twin/TWIN-27/**
source_baseline:
  project-control: 8ada67cc07b4dd958e821217e47a5051952a26ba
  soc-ap: f2596517c8e7a53da6ff9623d948ec5e70bf6770
  mcu-p3: 04231388c842c1ce3e5b71675d0dc118a65edf2e
  test_harness: 0b7497ba43158841eb3c4af7f16e477b9c30c2c5
base_commit: f2596517c8e7a53da6ff9623d948ec5e70bf6770
candidate_commit: null
dispatch_binding:
  source_commit: f2596517c8e7a53da6ff9623d948ec5e70bf6770
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
worktree: soc-ap
lease:
  owner: null
  task_revision: 1
  lease_id: null
  expires_at: null
resources:
- resource: isolated-worktree-and-build-output
  location: null
  exclusive: true
  pending: null
budget:
  planned_checkpoint_minutes: 30
  max_evidence_based_corrections: 2
  on_limit: 保存证据交COORD
checkpoint: 开工前绑定；目录扫描与Trailer验签自检；前置安全联锁测试；收件
execution_contract: project-control/docs/planning/vmware_soc_twin_task_execution_20261029.md
readiness_pending: []
deliverables:
  artifacts:
  - soc-ap/services/device_manager/firmware_updater.cpp
  - soc-ap/services/device_manager/firmware_updater.h
  - soc-ap/tests/device_manager/twin/test_firmware_updater.cpp
  record: docs/evidence/twin/TWIN-27/runs/<actual-run>/result.md
rollback:
  steps:
  - 仅回退本票候选；保存失败证据和原状态；硬件恢复须按实际SOP及授权执行
handoff:
  receiver_role: COORD
  receiver_session: session-coord-main
  transport: docs
  evidence_location: docs/evidence/twin/TWIN-27
  acknowledgement: null
verification:
  commands:
  - id: check_graph
    cwd: .
    command: PYTHONDONTWRITEBYTECODE=1 python3 project-control/tools/check_task_graph.py
      --workspace .
    expected: 结构无错误；不等于任务/运行/硬件接受
    availability: local
  - id: compile_and_run_firmware_updater_tests
    cwd: .
    command: g++ -std=c++17 -Wall -Wextra -Wpedantic -I soc-ap/services/device_manager -I soc-ap/services/forward -I soc-ap/contracts/twin soc-ap/services/device_manager/firmware_updater.cpp soc-ap/tests/device_manager/twin/test_firmware_updater.cpp -o /tmp/test_firmware_updater && /tmp/test_firmware_updater
    expected: exit 0, 固件目录扫描、128B Trailer验签与安全准入全集测试通过
    availability: host-toolchain
  positive_cases:
  - 正确解析/var/update/下fw_mc.bin与fw_th.bin并提取有效Trailer，前置安全检查通过时触发刷写调度
  negative_cases:
  - 损坏Trailer或强电加热温度>=50°C或作业非空闲时严格拦截并拒绝刷写
required_evidence_level: software-verified
verification_environment: isolated-host-or-document
qa_review_policy: project-control/.agents/rules/codex_qa_review.md
updated: '2026-10-31T11:30:00+08:00'
---

# TWIN-27 AP端VMware指定目录固件扫描与安全准入服务实现

## 1. 目标与依据

根据系统决定 **U-D05**（首版纳入 VMware 指定目录真实双 MCU 固件升级），本任务在 AP 上位机端实现固件目录扫描、Trailer 验签与前置安全准入调度：
1. 监控/扫描 VMware 指定目录（默认 `/var/update/` 或工程专有目录），检出 `fw_mc.bin` 与 `fw_th.bin`；
2. 实现 128 字节 `fw_trailer_t` 结构体解析与强校验（ATSG 魔数、硬件 ID、SHA-256、CRC32）；
3. 接入 `device-manager` 审查前置安全联锁：整机必须为 IDLE、电机静止、喷嘴与热床设定为 0°C 且当前温度 $<50.0^\circ\text{C}$；
4. 严格遵守 C/C++ 编码规范（函数 $\le 50$ 行、参数 $\le 4$ 个，零堆分配/智能指针安全管理）。

参考文档：
- [ARCH-MCU-UPGRADE-DESIGN-20261031.md](../../../../docs/analysis/mcu_firmware_upgrade_design_20261031.md)
