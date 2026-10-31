---
id: TWIN-29
title: TWIN-29 AP端双MCU真实固件版本查询链路与时序衰退状态机实现
revision: 1
plan_revision: vmware-soc-twin-20261029
task_kind: implementation
development_stage: vmware-twin
dispatchable: true
status: Done
blocked: false
planning_status: closed
owner: session-eng-fwd-twin-29
proposed_owner: ENG-FWD
executor:
  role: ENG-FWD
  agent_id: session-eng-fwd-twin-29
  run_id: run_02
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
    planned_session_alias: planned-qa-twin-29
    session: session-qa-twin-29
    session_evidence:
      path: docs/evidence/twin/TWIN-29/runs/run_02/qa_review_report.md
      sha256: 3493232f0619f5481073a966a3b2f469b4939e02ea5037ad07aede50345c7fd5
    decision: APPROVED
    reviewed_task_revision: 1
    artifact_version: soc-ap=86f5e17ead0971ca1a1eb20c07ca345924e24454; project-control=8b2b685d8232e4b0485740e7fe1268f544fa0528
    evidence: docs/evidence/twin/TWIN-29/runs/run_02/qa_review_report.md
    report_sha256: 3493232f0619f5481073a966a3b2f469b4939e02ea5037ad07aede50345c7fd5
    report_review:
      session: session-arch-twin-29
      role: ARCH
      decision: APPROVED
      reviewed_task_revision: 1
      artifact_version: soc-ap=86f5e17ead0971ca1a1eb20c07ca345924e24454; project-control=8b2b685d8232e4b0485740e7fe1268f544fa0528
      evidence: docs/evidence/twin/TWIN-29/runs/run_02/arch_review_report.md
      report_sha256: 475c2bb08e07badeb5fda3e1f8479f1c288db21e7a5e4c8696ac10bc13608b49
      session_evidence:
        path: docs/evidence/twin/TWIN-29/runs/run_02/arch_review_report.md
        sha256: 475c2bb08e07badeb5fda3e1f8479f1c288db21e7a5e4c8696ac10bc13608b49
  - role: ARCH
    platform: codex
    model: gpt-6-luna
    planned_session_alias: planned-arch-twin-29
    session: session-arch-twin-29
    session_evidence:
      path: docs/evidence/twin/TWIN-29/runs/run_02/arch_review_report.md
      sha256: 475c2bb08e07badeb5fda3e1f8479f1c288db21e7a5e4c8696ac10bc13608b49
    decision: APPROVED
    reviewed_task_revision: 1
    artifact_version: soc-ap=86f5e17ead0971ca1a1eb20c07ca345924e24454; project-control=8b2b685d8232e4b0485740e7fe1268f544fa0528
    evidence: docs/evidence/twin/TWIN-29/runs/run_02/arch_review_report.md
    report_sha256: 475c2bb08e07badeb5fda3e1f8479f1c288db21e7a5e4c8696ac10bc13608b49
  verifier_session: null
  integrator_session: null
primary_work_package: TASK-007
related_work_packages:
- TASK-008
- TASK-009
- TASK-002
depends_on:
- TWIN-25
dependency_conditions:
- task: TWIN-25
  accepted_version: soc-ap=f2596517c8e7a53da6ff9623d948ec5e70bf6770
  acceptance_evidence: docs/evidence/twin/TWIN-25/runs/run_01/qa_review_report.md
  required: 开工前继承TWIN-25 0x18网格解析与device_manager状态基线
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
  - services/device_manager/device_manager_dbus.cpp
  - services/device_manager/device_manager_dbus.h
  - tests/device_manager/twin/CMakeLists.txt
  - tests/device_manager/twin/test_device_manager.cpp
  project-control:
  - docs/evidence/twin/TWIN-29/**
allowed_paths:
- soc-ap/services/forward/forward_protocol.cpp
- soc-ap/services/forward/forward_protocol.h
- soc-ap/services/device_manager/device_manager_state.cpp
- soc-ap/services/device_manager/device_manager_state.h
- soc-ap/services/device_manager/device_manager_dbus.cpp
- soc-ap/services/device_manager/device_manager_dbus.h
- soc-ap/tests/device_manager/twin/CMakeLists.txt
- soc-ap/tests/device_manager/twin/test_device_manager.cpp
- project-control/docs/evidence/twin/TWIN-29/**
source_baseline:
  project-control: c652045e170e1305601d5fa2824e8b2c9a3d54b7
  soc-ap: f2596517c8e7a53da6ff9623d948ec5e70bf6770
  mcu-p3: 04231388c842c1ce3e5b71675d0dc118a65edf2e
  test_harness: 0b7497ba43158841eb3c4af7f16e477b9c30c2c5
base_commit: f2596517c8e7a53da6ff9623d948ec5e70bf6770
candidate_commit: 86f5e17ead0971ca1a1eb20c07ca345924e24454
dispatch_binding:
  source_commit: f2596517c8e7a53da6ff9623d948ec5e70bf6770
  workspace_diff_sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
  consumed_artifact_versions: {}
protocol_input:
  path: project-control/docs/specs/ap_mc_formal_protocol_v2_0_multidevice_routing_draft_20261015.md
  sha256: 9f8d4f9607cb3e76cc30b9ee2f971b23c3e0d936611188466a71f4aa15f3ce54
  revision: 1
read_sources:
- project-control/docs/planning/product/first_release_scope_decision_20261029.md
- project-control/docs/planning/product/first_release_requirements_and_task_decomposition_20261029.md
- project-control/docs/specs/ap_mc_formal_protocol_v2_0_multidevice_routing_draft_20261015.md
- project-control/.agents/rules/c_cpp_coding_standard.md
worktree: soc-ap
lease:
  owner: session-eng-fwd-twin-29
  task_revision: 1
  lease_id: lease-twin-29-run01
  expires_at: '2026-10-31T18:00:00+08:00'
resources:
- resource: isolated-worktree-and-build-output
  location: null
  exclusive: true
  pending: null
budget:
  planned_checkpoint_minutes: 30
  max_evidence_based_corrections: 2
  on_limit: 保存证据交COORD
checkpoint: 开工前绑定；0x01/0x02版本报文与衰退状态机自检；准确候选独立检查；收件
execution_contract: project-control/docs/planning/vmware_soc_twin_task_execution_20261029.md
readiness_pending: []
deliverables:
  artifacts:
  - soc-ap/services/forward/forward_protocol.cpp
  - soc-ap/services/forward/forward_protocol.h
  - soc-ap/services/device_manager/device_manager_state.cpp
  - soc-ap/services/device_manager/device_manager_state.h
  - soc-ap/services/device_manager/device_manager_dbus.cpp
  - soc-ap/services/device_manager/device_manager_dbus.h
  - soc-ap/tests/device_manager/twin/CMakeLists.txt
  - soc-ap/tests/device_manager/twin/test_device_manager.cpp
  - soc-ap/tests/device_manager/twin/CMakeLists.txt
  - soc-ap/tests/device_manager/twin/test_device_manager.cpp
  record: docs/evidence/twin/TWIN-29/runs/run_02/result.md
rollback:
  steps:
  - 仅回退本票候选；保存失败证据和原状态；硬件恢复须按实际SOP及授权执行
handoff:
  receiver_role: COORD
  receiver_session: session-coord-main
  transport: docs
  evidence_location: docs/evidence/twin/TWIN-29
  acknowledgement: docs/evidence/twin/TWIN-29/runs/run_02/result.md
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
  - AP端下发0x01查询并准确解析MC(0x02)与TH(0x03)返回的0x02 16B版本报文，提取proto_ver, fw_major, fw_minor, git_commit, boot_id，状态标记为ONLINE/FRESH并提供D-Bus与REST /api/v1/system/version接口
  negative_cases:
  - 校验失败、超时未响应或断开时进入QUERY_FAILED/OFFLINE状态；采样时延>5s标记为STALE；严禁硬编码或伪造版本数据
required_evidence_level: software-verified
verification_environment: isolated-host-or-document
qa_review_policy: project-control/.agents/rules/codex_qa_review.md
updated: '2026-10-31T14:32:00+08:00'
---

# TWIN-29 AP端双MCU真实固件版本查询链路与时序衰退状态机实现

## 1. 目标与依据

根据用户高优先级指令（显示 MC 和 TH 当前真实固件版本），落实 AP 上位机端真实双 MCU 固件版本查询、校验、时序衰退状态机及网关接口：
1. 恪守绝对真实性原则：严禁硬编码、构建版本或模拟响应代替真实设备版本；
2. 依据 MiniMCProto v2.0 规约实现 `CMD_GET_VERSION` (0x01) 组帧与 `CMD_VERSION_REPORT` (0x02, 16B payload) 解析；
3. 在 `device_manager` 维护 MC 与 TH 独立版本拓扑，落实 4 态衰退状态机：ONLINE/FRESH (<5s)、STALE (5s~15s)、OFFLINE (>15s/断开)、QUERY_FAILED (校验/CRC错误)；
4. 导出 D-Bus `GetVersionInfo` 与 UI Gateway HTTP REST `GET /api/v1/system/version` 接口，为 HMI 提供权威数据源；
5. 严格遵守 C/C++ 编码规范（函数 $\le 50$ 行、参数 $\le 4$ 个，零堆内存泄漏）。

参考文档：
- [ap_mc_formal_protocol_v2_0_multidevice_routing_draft_20261015.md](../../../../docs/specs/ap_mc_formal_protocol_v2_0_multidevice_routing_draft_20261015.md)
