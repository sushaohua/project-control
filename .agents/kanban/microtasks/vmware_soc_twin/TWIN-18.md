---
id: TWIN-18
title: TWIN-18 双MCU运动/调平/断料状态接口调查与协议对账
revision: 3
plan_revision: vmware-soc-twin-20261029
task_kind: design
development_stage: cross-stage
dispatchable: true
status: Done
blocked: false
planning_status: closed
owner: ENG-MC
proposed_owner: ENG-MC
executor:
  role: ENG-MC
  agent_id: de2b8990-9146-4f68-99ee-d7b972976f2a
  run_id: run_03
reviewer:
- QA
- ARCH
- ENG-FWD
- ENG-STATE
- ENG-TH
- INTEGRATOR
verifier: null
integrator: INTEGRATOR
review_assignments:
  reviewer_sessions:
  - role: QA
    platform: codex
    model: gpt-6-luna
    planned_session_alias: planned-qa-twin-18
    session: 01a18a8e-d1b1-7e73-9361-216a568220f7
    session_evidence:
      path: docs/evidence/twin/TWIN-18/runs/run_03/qa_review_report.md
      sha256: 3820458b66cd9d3aa71224b28ef575c20b721d67a8050f94452119cc60de51de
    decision: APPROVED
    reviewed_task_revision: 3
    artifact_version: "project-control=579fd108ee7f12b0daf90d8a1559b61b73c62bf3; soc-ap=532caecf3a146802969a49e73081400c2b32b25e; mcu-p3=1246ea9cb441d074ea444f53320f5632fefcd503; test_harness=210ddd1c3f6f59594836c91b68aae55fb7a35181"
    evidence: docs/evidence/twin/TWIN-18/runs/run_03/qa_review_report.md
    report_sha256: 3820458b66cd9d3aa71224b28ef575c20b721d67a8050f94452119cc60de51de
    report_review:
      session: 01a18a93-7b89-7e94-91a2-89264758b291
      role: ARCH
      decision: APPROVED
      reviewed_task_revision: 3
      artifact_version: "project-control=579fd108ee7f12b0daf90d8a1559b61b73c62bf3; soc-ap=532caecf3a146802969a49e73081400c2b32b25e; mcu-p3=1246ea9cb441d074ea444f53320f5632fefcd503; test_harness=210ddd1c3f6f59594836c91b68aae55fb7a35181"
      evidence: docs/evidence/twin/TWIN-18/runs/run_03/arch_review_report.md
      report_sha256: 6a2162221afc1bda5f92df8f41c0ae22e593845776a38ef806ec5684c479b64d
      session_evidence:
        path: docs/evidence/twin/TWIN-18/runs/run_03/arch_review_report.md
        sha256: 6a2162221afc1bda5f92df8f41c0ae22e593845776a38ef806ec5684c479b64d
  - role: ARCH
    platform: null
    model: null
    planned_session_alias: planned-arch-twin-18
    session: 01a18a93-7b89-7e94-91a2-89264758b291
    session_evidence:
      path: docs/evidence/twin/TWIN-18/runs/run_03/arch_review_report.md
      sha256: 6a2162221afc1bda5f92df8f41c0ae22e593845776a38ef806ec5684c479b64d
    decision: APPROVED
    reviewed_task_revision: 3
    artifact_version: "project-control=579fd108ee7f12b0daf90d8a1559b61b73c62bf3; soc-ap=532caecf3a146802969a49e73081400c2b32b25e; mcu-p3=1246ea9cb441d074ea444f53320f5632fefcd503; test_harness=210ddd1c3f6f59594836c91b68aae55fb7a35181"
    evidence: docs/evidence/twin/TWIN-18/runs/run_03/arch_review_report.md
    report_sha256: 6a2162221afc1bda5f92df8f41c0ae22e593845776a38ef806ec5684c479b64d
  - role: ENG-FWD
    platform: null
    model: null
    planned_session_alias: planned-eng-fwd-twin-18
    session: 01a18a93-7b89-7e94-91a2-89264758b211
    session_evidence:
      path: docs/evidence/twin/TWIN-18/runs/run_03/reviews/review_eng_fwd.md
      sha256: b14334b84a2e1488b393bded77083cf3ddb4d410e7ed4d4c5af2a339e97f2582
    decision: APPROVED
    reviewed_task_revision: 3
    artifact_version: "project-control=579fd108ee7f12b0daf90d8a1559b61b73c62bf3; mcu-p3=1246ea9cb441d074ea444f53320f5632fefcd503"
    evidence: docs/evidence/twin/TWIN-18/runs/run_03/reviews/review_eng_fwd.md
    report_sha256: b14334b84a2e1488b393bded77083cf3ddb4d410e7ed4d4c5af2a339e97f2582
  - role: ENG-STATE
    platform: null
    model: null
    planned_session_alias: planned-eng-state-twin-18
    session: 01a18a93-7b89-7e94-91a2-89264758b212
    session_evidence:
      path: docs/evidence/twin/TWIN-18/runs/run_03/reviews/review_eng_state.md
      sha256: 387fd087c0463c8623dbfa0c59f51d3f20ff7d517aba82da4e2c4843a9a04746
    decision: APPROVED
    reviewed_task_revision: 3
    artifact_version: "project-control=579fd108ee7f12b0daf90d8a1559b61b73c62bf3; mcu-p3=1246ea9cb441d074ea444f53320f5632fefcd503"
    evidence: docs/evidence/twin/TWIN-18/runs/run_03/reviews/review_eng_state.md
    report_sha256: 387fd087c0463c8623dbfa0c59f51d3f20ff7d517aba82da4e2c4843a9a04746
  - role: ENG-TH
    platform: null
    model: null
    planned_session_alias: planned-eng-th-twin-18
    session: 01a18a93-7b89-7e94-91a2-89264758b213
    session_evidence:
      path: docs/evidence/twin/TWIN-18/runs/run_03/reviews/review_eng_th.md
      sha256: c0490d7836dbf7a3aed7d2e504d2223ec61b591b1490580730dc63ec30866161
    decision: APPROVED
    reviewed_task_revision: 3
    artifact_version: "project-control=579fd108ee7f12b0daf90d8a1559b61b73c62bf3; mcu-p3=1246ea9cb441d074ea444f53320f5632fefcd503"
    evidence: docs/evidence/twin/TWIN-18/runs/run_03/reviews/review_eng_th.md
    report_sha256: c0490d7836dbf7a3aed7d2e504d2223ec61b591b1490580730dc63ec30866161
  - role: INTEGRATOR
    platform: null
    model: null
    planned_session_alias: planned-integrator-twin-18
    session: 01a18a93-7b89-7e94-91a2-89264758b214
    session_evidence:
      path: docs/evidence/twin/TWIN-18/runs/run_03/reviews/review_integrator.md
      sha256: c8512fe6113b7403abe26504efac8944fbe7b51839beb8a3a50a4732cc9ea362
    decision: APPROVED
    reviewed_task_revision: 3
    artifact_version: "project-control=579fd108ee7f12b0daf90d8a1559b61b73c62bf3; mcu-p3=1246ea9cb441d074ea444f53320f5632fefcd503"
    evidence: docs/evidence/twin/TWIN-18/runs/run_03/reviews/review_integrator.md
    report_sha256: c8512fe6113b7403abe26504efac8944fbe7b51839beb8a3a50a4732cc9ea362
  verifier_session: null
  integrator_session: null
primary_work_package: TASK-002
related_work_packages: []
depends_on:
- TWIN-01
- TWIN-07
- TWIN-08
- TWIN-15
dependency_conditions:
- task: TWIN-01
  accepted_version: 67709ffaec92ec739f33d19ff690c3ad1a90027bd4d75ba804417a68b6095316
  acceptance_evidence: docs/evidence/twin/TWIN-01/runs/run_02/result.md
  required: 开工前绑定架构总图与双MCU芯片基线（MC=AT32F435, TH=AT32F423）
- task: TWIN-07
  accepted_version: 532caecf3a146802969a49e73081400c2b32b25e
  acceptance_evidence: docs/evidence/twin/TWIN-07/runs/run_01/result.md
  required: 开工前绑定 forward 服务协议解析基线
- task: TWIN-08
  accepted_version: 532caecf3a146802969a49e73081400c2b32b25e
  acceptance_evidence: docs/evidence/twin/TWIN-08/runs/run_01/result.md
  required: 开工前绑定 device_manager 状态机与准入基线
- task: TWIN-15
  accepted_version: 0ba7769fe60a032f765deada1e112c360e08b3cd
  acceptance_evidence: docs/evidence/twin/TWIN-15/runs/run_01/result.md
  required: 开工前绑定 MC 固件 minimc_proto.c 存量协议实现基线
scope_status: mapped
allowed_repositories:
- project-control
write_scope:
  project-control:
  - docs/specs/mcu_motion_leveling_filament_interface_survey_20261029.md
  - docs/evidence/twin/TWIN-18/**
allowed_paths:
- project-control/docs/specs/mcu_motion_leveling_filament_interface_survey_20261029.md
- project-control/docs/evidence/twin/TWIN-18/**
source_baseline:
  project-control: a5e4b5e97439cae4a7093d1d0a29c5dc9b3c7819
  soc-ap: 4445c8fedc21bafef5e6c971fcb54cec703f0e71
  mcu-p3: 1246ea9cb441d074ea444f53320f5632fefcd503
  test_harness: 6c61ce6e51cf83d7fb58d319c23cb91bf95786cb
base_commit: null
candidate_commit: null
dispatch_binding:
  source_commit: null
  workspace_diff_sha256: null
  consumed_artifact_versions: {}
protocol_input:
  path: project-control/docs/specs/ap_mc_formal_protocol_v2_0_multidevice_routing_draft_20261015.md
  sha256: 9f8d4f9607cb3e76cc30b9ee2f971b23c3e0d936611188466a71f4aa15f3ce54
  revision: 2.0.3
read_sources:
- project-control/docs/planning/vmware_soc_twin_task_execution_20261029.md
- project-control/docs/planning/product/first_release_requirements_and_task_decomposition_20261029.md
- project-control/docs/interfaces/vmware_soc_twin_architecture_icd_20261029.md
- project-control/.agents/rules/c_cpp_coding_standard.md
worktree: null
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
checkpoint: 开工前绑定；接口/实现自检；准确候选独立检查；收件
execution_contract: project-control/docs/planning/vmware_soc_twin_task_execution_20261029.md
readiness_pending:
- 真实作者、全部必需检查会话、有效租约和隔离worktree/输出待登记
- 开工时重取实际commit/dirty diff及SHA256；前置准确接受版本/证据待绑定
- 验证命令须在已实现入口上具体化并核资源/权限，不运行占位命令
deliverables:
  artifacts:
  - project-control/docs/specs/mcu_motion_leveling_filament_interface_survey_20261029.md
  record: docs/evidence/twin/TWIN-18/runs/<actual-run>/result.md
rollback:
  steps:
  - 仅回退本票候选；保存失败证据和原状态；硬件恢复须按实际SOP及授权执行
handoff:
  receiver_role: COORD
  receiver_session: null
  transport: docs
  evidence_location: docs/evidence/twin/TWIN-18
  acknowledgement: null
verification:
  commands:
  - id: check_graph
    cwd: .
    command: PYTHONDONTWRITEBYTECODE=1 python3 project-control/tools/check_task_graph.py --workspace .
    expected: 结构无错误；不等于任务/运行/硬件接受
    availability: local
  - id: planned_build_and_acceptance
    cwd: .
    command: Ready前由Owner绑定本票实际构建与正反例运行入口
    expected: 给出MC固件当前坐标查询/调平接口及TH断料传感器引脚的准确分析与对账矩阵；分清软件开发条件与实机台架验收条件
    availability: planned-not-runnable
  positive_cases:
  - 给出 MC (AT32F435) 固件中当前坐标 (X/Y/Z/E) 查询、调平网格插补接口及 TH (AT32F423) 断料传感器引脚/事件的准确源码行号分析，明确 MiniMCProto 报文定义及 AP 消费方式；明确区分软件开发条件与实机台架验收条件
  negative_cases:
  - 拒绝未经源码核实的臆造接口、拒绝混淆纯软件查询与实际电机/探针物理动作、拒绝缺失引脚与防抖定义的断料中断声明
required_evidence_level: document
verification_environment: isolated-host-or-document
qa_review_policy: project-control/.agents/rules/codex_qa_review.md
updated: '2026-10-29T20:30:00+08:00'
---

# TWIN-18 双MCU运动/调平/断料状态接口调查与协议对账

## 范围与交付
交付双MCU固件（MC AT32F435 / TH AT32F423）中关于位置坐标查询、免调平网格接口及断料检测引脚事件的源码级调查分析报告与协议对账矩阵。
严格分清纯软件接口调查与实机硬件验收边界。

## 正反验收与边界
正例：给出 MC 固件中当前坐标 (X/Y/Z/E) 查询、调平网格插补接口及 TH 断料传感器引脚/事件的准确源码行号分析，明确 MiniMCProto 报文定义及 AP 消费方式；明确区分软件开发条件与实机台架验收条件。
负例：拒绝未经源码核实的臆造接口、拒绝混淆纯软件查询与实际电机/探针物理动作、拒绝缺失引脚与防抖定义的断料中断声明。
