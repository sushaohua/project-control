---
id: TWIN-22
title: TWIN-22 AP端温控倍数换算与故障哨兵防御性治理
revision: 1
plan_revision: vmware-soc-twin-20261029
task_kind: implementation
development_stage: vmware-twin
dispatchable: true
status: InProgress
blocked: false
planning_status: planned
owner: session-eng-fwd-twin-22
proposed_owner: ENG-FWD
executor:
  role: ENG-FWD
  agent_id: session-eng-fwd-twin-22
  run_id: run_01
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
    planned_session_alias: planned-qa-twin-22
    session: session-qa-twin-22
    session_evidence: null
    decision: null
    reviewed_task_revision: null
    artifact_version: null
    evidence: null
    report_sha256: null
  - role: ARCH
    platform: codex
    model: gpt-6-luna
    planned_session_alias: planned-arch-twin-22
    session: session-arch-twin-22
    session_evidence: null
    decision: null
    reviewed_task_revision: null
    artifact_version: null
    evidence: null
    report_sha256: null
  verifier_session: null
  integrator_session: null
primary_work_package: TASK-008
related_work_packages:
- TASK-007
depends_on:
- TWIN-18
dependency_conditions:
- task: TWIN-18
  accepted_version: project-control=579fd108ee7f12b0daf90d8a1559b61b73c62bf3; soc-ap=532caecf3a146802969a49e73081400c2b32b25e;
    mcu-p3=1246ea9cb441d074ea444f53320f5632fefcd503; test_harness=210ddd1c3f6f59594836c91b68aae55fb7a35181
  acceptance_evidence: docs/evidence/twin/TWIN-18/runs/run_03/qa_review_report.md
  required: 开工前绑定准确产物与 SPEC-MCU-MOTION-LEVELING-FILAMENT-20261029 规范定义
scope_status: mapped
allowed_repositories:
- soc-ap
- project-control
write_scope:
  soc-ap:
  - services/forward/forward_protocol.cpp
  - services/device_manager/device_manager_state.cpp
  - tests/device_manager/twin/test_device_manager.cpp
  project-control:
  - docs/evidence/twin/TWIN-22/**
allowed_paths:
- soc-ap/services/forward/forward_protocol.cpp
- soc-ap/services/device_manager/device_manager_state.cpp
- soc-ap/tests/device_manager/twin/test_device_manager.cpp
- project-control/docs/evidence/twin/TWIN-22/**
source_baseline:
  project-control: de5b057510185a64de0ea5adcb08ebea10913920
  soc-ap: 19dd461b1959c170963ebd477aa29c36ea841f63
  mcu-p3: d756a13b3c2a1c47186a07311b2c24fa43431465
  test_harness: 0b7497ba43158841eb3c4af7f16e477b9c30c2c5
base_commit: 19dd461b1959c170963ebd477aa29c36ea841f63
candidate_commit: null
dispatch_binding:
  source_commit: 19dd461b1959c170963ebd477aa29c36ea841f63
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
lease:
  owner: session-eng-fwd-twin-22
  task_revision: 1
  lease_id: lease-twin-22-run01
  expires_at: '2026-10-31T18:00:00+08:00'
resources:
- resource: isolated-worktree-and-build-output
  location: null
  exclusive: true
  pending: Ready前按实际会话登记；最多两张实现票并行
budget:
  planned_checkpoint_minutes: 30
  max_evidence_based_corrections: 2
  on_limit: 保存证据交COORD
checkpoint: 开工前绑定；0x14温控换算与哨兵防御性自检；准确候选独立检查；收件
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
  record: docs/evidence/twin/TWIN-22/runs/<actual-run>/result.md
rollback:
  steps:
  - 仅回退本票候选；保存失败证据和原状态；硬件恢复须按实际SOP及授权执行
handoff:
  receiver_role: COORD
  receiver_session: session-coord-main
  transport: docs
  evidence_location: docs/evidence/twin/TWIN-22
  acknowledgement: null
verification:
  commands:
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
  - 0x7FFF / 0x7FFE 故障哨兵在 device_manager_state 中被正确拦截并标记 FAULT/STALE，JSON 不再输出 2147483.6
  - 0.1℃ (deci_c) 报文在 forward_protocol 中换算为 milli_c，245 deci_c 换算为 24500 milli_c (24.5℃)
  negative_cases:
  - 传入非法空指针时返回 AISOC_DEV_ERR_NULL_PTR 或 AISOC_FWD_ERR_NULL_PTR
  - 哨兵状态下禁止将质量错误标记为 FRESH
---

# TWIN-22 AP端温控倍数换算与故障哨兵防御性治理

## 1. 任务背景与目标

针对 TWIN-12 验收中暴露的温控证据冲突及异常高值：
1. **热床温度冲突治理**：下位机 0.1℃ (`deci_c`) 传输与上位机 `forward_protocol.cpp` 历史 `centi_c` 换算逻辑彻底对账，确保 `245` deci_c 严格换算为 `24500` milli_c（对应 `24.5℃`），杜绝 245.0℃ 的 10 倍放大隐患；
2. **哨兵泄露防御治理**：工具头传感器开路/故障哨兵 `AISOC_TEMP_MILLIC_FAULT` (`0x7FFFFFFF`) 及离线哨兵 `AISOC_TEMP_MILLIC_OFFLINE` (`0x7FFFFFFE`) 在 `device_manager_state.cpp` 中强制拦截，不得继续除以 1000.0 输出 `2147483.6℃`；其对应数据质量必须降级为 `FAULT` 或 `STALE`，禁止错误标记为 `FRESH` 与 `NORMAL`；
3. **C/C++硬编码门禁遵守**：所有新增及修改函数严格遵循 $\le 50$ 行、参数 $\le 4$ 个之硬性约束，第一行必须防御性校验空指针。

## 2. 交付范围

- `soc-ap/services/forward/forward_protocol.cpp`
- `soc-ap/services/device_manager/device_manager_state.cpp`
- `soc-ap/tests/device_manager/twin/test_device_manager.cpp`
- `project-control/docs/evidence/twin/TWIN-22/**`
