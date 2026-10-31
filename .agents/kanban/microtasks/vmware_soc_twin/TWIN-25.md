---
id: TWIN-25
title: TWIN-25 AP端0x18调平网格解析与设备状态拓扑呈现
revision: 1
plan_revision: vmware-soc-twin-20261029
task_kind: implementation
development_stage: vmware-twin
dispatchable: true
status: Backlog
blocked: false
planning_status: planned
owner: null
proposed_owner: ENG-FWD
executor:
  role: ENG-FWD
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
    planned_session_alias: planned-qa-twin-25
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
    planned_session_alias: planned-arch-twin-25
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
- TWIN-24
dependency_conditions:
- task: TWIN-24
  accepted_version: mcu-p3=9b017f186665c2c9226146cc0fdc34af3ad5242b
  acceptance_evidence: docs/evidence/twin/TWIN-24/runs/run_01/qa_review_report.md
  required: 开工前继承TWIN-24 MC 5×5调平网格0x18导出协议与固件候选
scope_status: mapped
allowed_repositories:
- soc-ap
- project-control
write_scope:
  soc-ap:
  - services/forward/forward_protocol.cpp
  - services/forward/forward_protocol.h
  - services/device_manager/device_manager_state.cpp
  - services/device_manager/device_manager_state.h
  - tests/device_manager/twin/test_device_manager.cpp
  project-control:
  - docs/evidence/twin/TWIN-25/**
allowed_paths:
- soc-ap/services/forward/forward_protocol.cpp
- soc-ap/services/forward/forward_protocol.h
- soc-ap/services/device_manager/device_manager_state.cpp
- soc-ap/services/device_manager/device_manager_state.h
- soc-ap/tests/device_manager/twin/test_device_manager.cpp
- project-control/docs/evidence/twin/TWIN-25/**
source_baseline:
  project-control: 8ea89b9d1e442894be6bc1f92e4aa1a4c954f9a0
  soc-ap: 6850cc553d405b5e7e511ff181d985fdee8e221f
  mcu-p3: 9b017f186665c2c9226146cc0fdc34af3ad5242b
  test_harness: 0b7497ba43158841eb3c4af7f16e477b9c30c2c5
base_commit: 6850cc553d405b5e7e511ff181d985fdee8e221f
candidate_commit: null
dispatch_binding:
  source_commit: 6850cc553d405b5e7e511ff181d985fdee8e221f
  workspace_diff_sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
  consumed_artifact_versions: {}
protocol_input:
  path: project-control/docs/specs/mcu_motion_leveling_filament_interface_survey_20261029.md
  sha256: 596b4e84252fd71332865663a31187d40e5826ab345712bec34d40eca1f2f4ea
  revision: 1
read_sources:
- project-control/docs/planning/product/first_release_scope_decision_20261029.md
- project-control/docs/planning/product/first_release_requirements_and_task_decomposition_20261029.md
- project-control/docs/specs/mcu_motion_leveling_filament_interface_survey_20261029.md
- project-control/.agents/rules/c_cpp_coding_standard.md
worktree: soc-ap
lease: null
resources:
- resource: isolated-worktree-and-build-output
  location: null
  exclusive: true
  pending: Ready前按实际会话登记；最多两张实现票并行
budget:
  planned_checkpoint_minutes: 30
  max_evidence_based_corrections: 2
  on_limit: 保存证据交COORD
checkpoint: 开工前绑定；0x18网格解析与D-Bus/JSON拓扑呈现自检；准确候选独立检查；收件
execution_contract: project-control/docs/planning/vmware_soc_twin_task_execution_20261029.md
readiness_pending:
- 真实作者、全部必需检查会话、有效租约和隔离worktree/输出待登记
- 开工时重取实际commit/dirty diff及SHA256；前置准确接受版本/证据待绑定
- 验证命令须在已实现入口上具体化并核资源/权限，不运行占位命令
deliverables:
  artifacts:
  - soc-ap/services/forward/forward_protocol.cpp
  - soc-ap/services/device_manager/device_manager_state.cpp
  - soc-ap/tests/device_manager/twin/test_device_manager.cpp
  record: docs/evidence/twin/TWIN-25/runs/<actual-run>/result.md
rollback:
  steps:
  - 仅回退本票候选；保存失败证据和原状态；硬件恢复须按实际SOP及授权执行
handoff:
  receiver_role: COORD
  receiver_session: session-coord-main
  transport: docs
  evidence_location: docs/evidence/twin/TWIN-25
  acknowledgement: null
verification:
  commands:
  - id: check_graph
    cwd: .
    command: PYTHONDONTWRITEBYTECODE=1 python3 project-control/tools/check_task_graph.py
      --workspace .
    expected: 结构无错误；不等于任务/运行/硬件接受
    availability: local
  - id: compile_device_manager_tests
    cwd: soc-ap/tests/device_manager/twin
    command: cmake -B build -S . && cmake --build build
    expected: exit 0, 生成 test_device_manager 可执行文件
    availability: host-toolchain
  - id: run_device_manager_tests
    cwd: soc-ap/tests/device_manager/twin
    command: ./build/test_device_manager
    expected: exit 0, 单元与集成测试全集通过
    availability: host-toolchain
  positive_cases:
  - AP端正确接收并解析0x18 52B 5×5双线性网格报文，转换为微米整型高程拓扑并序列化为GET /api/v1/calibration/mesh与D-Bus GetLevelingGrid数据
  negative_cases:
  - 报文长度不符（非52B载荷）或校验错误时安全丢弃并记录协议异常；空指针防御生效
required_evidence_level: software-verified
verification_environment: isolated-host-or-document
qa_review_policy: project-control/.agents/rules/codex_qa_review.md
updated: '2026-10-31T11:00:00+08:00'
---

# TWIN-25 AP端0x18调平网格解析与设备状态拓扑呈现

## 1. 目标与依据

依据首版调平特性（`MOT-002`）与用户指令 **U-D04**，打通上位机对下位机 5×5 双线性调平网格的消费与呈现闭环：
1. 在 `forward_protocol.cpp` 中增加对 0x18 报文的解析与校验能力；
2. 在 `device_manager_state.cpp` 中维护 5×5 调平高程网格数据模型；
3. 输出合规的网格 JSON 拓扑（供 Web HMI 绘制调平热力图与向导）；
4. 扩充 `test_device_manager.cpp` 正反例单测。
