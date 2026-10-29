---
id: TEMP-04
title: TEMP-04 AP 宿主端温度查询与 CLI 呈现
revision: 1
plan_revision: marlin-r2
task_kind: implementation
dispatchable: true
status: Done
blocked: false
planning_status: closed-done
owner: fwd-session-20261028
proposed_owner: ENG-FWD
executor:
  role: ENG-FWD
  agent_id: fwd-session-20261028
  run_id: run_01
reviewer:
- QA
- ARCH
verifier: null
integrator: null
review_assignments:
  reviewer_sessions:
  - role: QA
    platform: codex
    model: gpt-6-luna
    planned_session_alias: codex-qa-temp04-review
    session: 7f1cda3e-d24d-40ed-92d7-c40afe3a440c
    decision: APPROVED
    reviewed_task_revision: 1
    artifact_version: 1.0.0
    evidence: docs/evidence/temperature_increment/TEMP-04/runs/run_01/qa_review_report.md
    report_sha256: 9bd7d56209454ffaf286b9e6b81b6eceb745a65ddeb7382d9502c9ab628e32f5
  - role: ARCH
    session: arch-session-20261028
    decision: APPROVED
    reviewed_task_revision: 1
    artifact_version: 1.0.0
    evidence: docs/evidence/temperature_increment/TEMP-04/runs/run_01/result.md
  verifier_session: null
  integrator_session: null
primary_work_package: TASK-007
requirement:
- PILOT-REQ-01
- PILOT-REQ-04
depends_on:
- TEMP-01
dependency_conditions:
- task: TEMP-01
  accepted_version: 5675a50c07e8c908aa7da8b3ad90252bf53d253aad78fc26f0e246cb26243a4d
  acceptance_evidence: docs/evidence/temperature_increment/TEMP-01/runs/run_01/result.md
  required: 绑定温度遥测ICD与结构体头文件
scope_status: mapped
allowed_repositories:
- soc-ap
- project-control
write_scope:
  soc-ap:
  - CMakeLists.txt
  - core/host/main.cpp
  - core/host/query.cpp
  - core/host/query.h
  - core/forward/minimc/codec.cpp
  - core/forward/minimc/codec.h
  - tests/protocol/test_telemetry.cpp
  project-control:
  - docs/evidence/temperature_increment/TEMP-04/**
allowed_paths:
- soc-ap/CMakeLists.txt
- soc-ap/core/host/main.cpp
- soc-ap/core/host/query.cpp
- soc-ap/core/host/query.h
- soc-ap/core/forward/minimc/codec.cpp
- soc-ap/core/forward/minimc/codec.h
- soc-ap/tests/protocol/test_telemetry.cpp
- project-control/docs/evidence/temperature_increment/TEMP-04/**
source_baseline:
  project-control: a5e4b5e97439cae4a7093d1d0a29c5dc9b3c7819
  soc-ap: 4445c8fedc21bafef5e6c971fcb54cec703f0e71
  mcu-p3: 1246ea9cb441d074ea444f53320f5632fefcd503
  test_harness: 6c61ce6e51cf83d7fb58d319c23cb91bf95786cb
base_commit: a5e4b5e97439cae4a7093d1d0a29c5dc9b3c7819
dispatch_binding:
  source_commit: a5e4b5e97439cae4a7093d1d0a29c5dc9b3c7819
  workspace_diff_sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
  consumed_artifact_versions: {}
protocol_input:
  path: project-control/docs/specs/ap_mc_formal_protocol_v2_0_multidevice_routing_draft_20261015.md
  sha256: 9f8d4f9607cb3e76cc30b9ee2f971b23c3e0d936611188466a71f4aa15f3ce54
  revision: 2.0.3
read_sources:
- project-control/docs/planning/product/next_increment_design_pl02.md
- project-control/.agents/rules/c_cpp_coding_standard.md
worktree: /home/sushaohua/workspace/ai_soc_project
resources:
- resource: ap-workspace
  location: null
  exclusive: false
  pending: AP宿主工作区
lease:
  owner: fwd-session-20261028
  task_revision: 1
  lease_id: lease-temp04-fwd-20261028-01
  expires_at: '2026-10-28T22:30:00+08:00'
budget:
  planned_checkpoint_minutes: 30
  max_evidence_based_corrections: 2
  on_limit: 保存失败交COORD
checkpoint: 开工前；CLI扩展与解析实现；单元测试全部通过
execution_contract: project-control/docs/planning/product/next_increment_design_pl02.md
readiness_pending: []
deliverables:
  artifacts:
  - soc-ap/build/host/bin/soc-ap
  record: docs/evidence/temperature_increment/TEMP-04/runs/run_01/result.md
rollback:
  steps:
  - 回退AP代码修改
handoff:
  receiver_role: COORD
  receiver_session: main
  transport: docs
  evidence_location: docs/evidence/temperature_increment/TEMP-04
  acknowledgement: accepted
verification:
  commands:
  - id: ap_build
    cwd: soc-ap
    command: cmake --build build/host -j4
    expected: 编译成功生成soc-ap宿主程序与测试程序
    availability: local
  - id: ap_test
    cwd: soc-ap
    command: ./build/host/bin/test_telemetry
    expected: 温度载荷解析单元测试100%通过
    availability: local
  positive_cases:
  - 解析16字节温度载荷，正确显示摄氏度浮点数并支持--json
  negative_cases:
  - 遇到开路短路状态码时返回明确错误并设置非零退出码
updated: '2026-10-28'
required_evidence_level: host-verified
verification_environment: host
qa_review_policy: project-control/.agents/rules/codex_qa_review.md
---

# TEMP-04 AP 宿主端温度查询与 CLI 呈现

扩展 soc-ap 支持 --cmd temp 指令与 --target <mc|th|all>，支持 JSON 格式输出，解析 16 字节温度载荷，异常状态码诊断。
