---
id: TWIN-02
title: TWIN-02 双环境可执行通信契约与生成规则
revision: 3
plan_revision: vmware-soc-twin-20261029
task_kind: design
development_stage: cross-stage
dispatchable: true
status: Done
blocked: false
planning_status: closed
owner: ARCH
proposed_owner: ARCH
executor:
  role: ARCH
  agent_id: 92a9a6eb-5bc5-449c-8a8e-d404482b25bf
  run_id: run_03
reviewer:
- QA
- ENG-FWD
- ENG-STATE
- ENG-UI
- ENG-NET
- ENG-DDS
- ENG-DBUS
- INTEGRATOR
verifier: null
integrator: INTEGRATOR
review_assignments:
  reviewer_sessions:
  - role: QA
    platform: codex
    model: gpt-6-luna
    planned_session_alias: planned-qa-twin-02
    session: 01a18a8d-de33-7c82-af6d-456ac4b04eb3
    session_evidence:
      path: docs/evidence/twin/TWIN-02/runs/run_03/qa_review_report.md
      sha256: e909e1edaef5df942792df81abe56f591cb33ee8d7396a4a8f35b7c120da9637
    decision: APPROVED
    reviewed_task_revision: 3
    artifact_version: "soc-ap=532caecf3a146802969a49e73081400c2b32b25e; project-control=579fd108ee7f12b0daf90d8a1559b61b73c62bf3"
    evidence: docs/evidence/twin/TWIN-02/runs/run_03/qa_review_report.md
    report_sha256: e909e1edaef5df942792df81abe56f591cb33ee8d7396a4a8f35b7c120da9637
    report_review:
      session: 01a18a93-7b89-7e94-91a2-89264758b291
      role: ARCH
      decision: APPROVED
      reviewed_task_revision: 3
      artifact_version: "soc-ap=532caecf3a146802969a49e73081400c2b32b25e; project-control=579fd108ee7f12b0daf90d8a1559b61b73c62bf3"
      evidence: docs/evidence/twin/TWIN-02/runs/run_03/arch_review_report.md
      report_sha256: 280826c0c5a54f4af9fdd1dd5de94fcc787aca83c98e1f99368d65d30267f2db
      session_evidence:
        path: docs/evidence/twin/TWIN-02/runs/run_03/arch_review_report.md
        sha256: 280826c0c5a54f4af9fdd1dd5de94fcc787aca83c98e1f99368d65d30267f2db
  - role: ENG-FWD
    platform: null
    model: null
    planned_session_alias: planned-eng-fwd-twin-02
    session: 01a18a93-7b89-7e94-91a2-89264758b201
    session_evidence:
      path: docs/evidence/twin/TWIN-02/runs/run_03/reviews/review_eng_fwd.md
      sha256: 24ffc31647e4f1c2e83795de74b019939594bd33fe80a29a6dd0020d4d649509
    decision: APPROVED
    reviewed_task_revision: 3
    artifact_version: "soc-ap=532caecf3a146802969a49e73081400c2b32b25e; project-control=579fd108ee7f12b0daf90d8a1559b61b73c62bf3"
    evidence: docs/evidence/twin/TWIN-02/runs/run_03/reviews/review_eng_fwd.md
    report_sha256: 24ffc31647e4f1c2e83795de74b019939594bd33fe80a29a6dd0020d4d649509
  - role: ENG-STATE
    platform: null
    model: null
    planned_session_alias: planned-eng-state-twin-02
    session: 01a18a93-7b89-7e94-91a2-89264758b202
    session_evidence:
      path: docs/evidence/twin/TWIN-02/runs/run_03/reviews/review_eng_state.md
      sha256: f10ca3e30efb13f5cdebd712f1b1ab2e1bbecf09ee34fc5edd7c48bd7c0d63fc
    decision: APPROVED
    reviewed_task_revision: 3
    artifact_version: "soc-ap=532caecf3a146802969a49e73081400c2b32b25e; project-control=579fd108ee7f12b0daf90d8a1559b61b73c62bf3"
    evidence: docs/evidence/twin/TWIN-02/runs/run_03/reviews/review_eng_state.md
    report_sha256: f10ca3e30efb13f5cdebd712f1b1ab2e1bbecf09ee34fc5edd7c48bd7c0d63fc
  - role: ENG-UI
    platform: null
    model: null
    planned_session_alias: planned-eng-ui-twin-02
    session: 01a18a93-7b89-7e94-91a2-89264758b203
    session_evidence:
      path: docs/evidence/twin/TWIN-02/runs/run_03/reviews/review_eng_ui.md
      sha256: f43979bb431da2b0d057e546960136f956af33565cf873a5e95ea37aeaf5cb32
    decision: APPROVED
    reviewed_task_revision: 3
    artifact_version: "soc-ap=532caecf3a146802969a49e73081400c2b32b25e; project-control=579fd108ee7f12b0daf90d8a1559b61b73c62bf3"
    evidence: docs/evidence/twin/TWIN-02/runs/run_03/reviews/review_eng_ui.md
    report_sha256: f43979bb431da2b0d057e546960136f956af33565cf873a5e95ea37aeaf5cb32
  - role: ENG-NET
    platform: null
    model: null
    planned_session_alias: planned-eng-net-twin-02
    session: 01a18a93-7b89-7e94-91a2-89264758b204
    session_evidence:
      path: docs/evidence/twin/TWIN-02/runs/run_03/reviews/review_eng_net.md
      sha256: 1a6448544634575fd847aae9cb5552d9c8ecb988a6e63a1169af10098d58b3a0
    decision: APPROVED
    reviewed_task_revision: 3
    artifact_version: "soc-ap=532caecf3a146802969a49e73081400c2b32b25e; project-control=579fd108ee7f12b0daf90d8a1559b61b73c62bf3"
    evidence: docs/evidence/twin/TWIN-02/runs/run_03/reviews/review_eng_net.md
    report_sha256: 1a6448544634575fd847aae9cb5552d9c8ecb988a6e63a1169af10098d58b3a0
  - role: ENG-DDS
    platform: null
    model: null
    planned_session_alias: planned-eng-dds-twin-02
    session: 01a18a93-7b89-7e94-91a2-89264758b205
    session_evidence:
      path: docs/evidence/twin/TWIN-02/runs/run_03/reviews/review_eng_dds.md
      sha256: fcd364cd68b38a8d64b42a84311ff7bb9e77d8c89228d10c14bf68a39534f077
    decision: APPROVED
    reviewed_task_revision: 3
    artifact_version: "soc-ap=532caecf3a146802969a49e73081400c2b32b25e; project-control=579fd108ee7f12b0daf90d8a1559b61b73c62bf3"
    evidence: docs/evidence/twin/TWIN-02/runs/run_03/reviews/review_eng_dds.md
    report_sha256: fcd364cd68b38a8d64b42a84311ff7bb9e77d8c89228d10c14bf68a39534f077
  - role: ENG-DBUS
    platform: null
    model: null
    planned_session_alias: planned-eng-dbus-twin-02
    session: 01a18a93-7b89-7e94-91a2-89264758b206
    session_evidence:
      path: docs/evidence/twin/TWIN-02/runs/run_03/reviews/review_eng_dbus.md
      sha256: eabc2da4ed3b70dc66637f3bf6ee2f32239e64d451236e3e287d840f7126909b
    decision: APPROVED
    reviewed_task_revision: 3
    artifact_version: "soc-ap=532caecf3a146802969a49e73081400c2b32b25e; project-control=579fd108ee7f12b0daf90d8a1559b61b73c62bf3"
    evidence: docs/evidence/twin/TWIN-02/runs/run_03/reviews/review_eng_dbus.md
    report_sha256: eabc2da4ed3b70dc66637f3bf6ee2f32239e64d451236e3e287d840f7126909b
  - role: INTEGRATOR
    platform: null
    model: null
    planned_session_alias: planned-integrator-twin-02
    session: 01a18a93-7b89-7e94-91a2-89264758b207
    session_evidence:
      path: docs/evidence/twin/TWIN-02/runs/run_03/reviews/review_integrator.md
      sha256: 07ece527d70649b99458d989c97007a41a53b0ec42e019d6d9b8ed08b9febd5c
    decision: APPROVED
    reviewed_task_revision: 3
    artifact_version: "soc-ap=532caecf3a146802969a49e73081400c2b32b25e; project-control=579fd108ee7f12b0daf90d8a1559b61b73c62bf3"
    evidence: docs/evidence/twin/TWIN-02/runs/run_03/reviews/review_integrator.md
    report_sha256: 07ece527d70649b99458d989c97007a41a53b0ec42e019d6d9b8ed08b9febd5c
  verifier_session: null
  integrator_session: null
primary_work_package: TASK-013
related_work_packages: []
depends_on:
- TWIN-01
dependency_conditions:
- task: TWIN-01
  accepted_version: 923d250ec36b2585120f70620f3a71572448496f0a3850c5d3f9594321959793
  acceptance_evidence: docs/evidence/twin/TWIN-01/runs/run_01/result.md
  required: 开工前绑定准确产物、必需接受及适用限制；历史Done不批准新契约
scope_status: mapped
allowed_repositories:
- soc-ap
- project-control
write_scope:
  soc-ap:
  - contracts/twin/**
  project-control:
  - docs/evidence/twin/TWIN-02/**
allowed_paths:
- soc-ap/contracts/twin/**
- project-control/docs/evidence/twin/TWIN-02/**
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
- project-control/docs/planning/vmware_soc_twin_development_plan_20261029.md
- project-control/docs/interfaces/soc_temperature_module_architecture_icd_draft_20261028.md
- project-control/.agents/rules/c_cpp_coding_standard.md
- project-control/docs/planning/communication_modules_ownership_20261029.md
- soc-ap/third_party/README.md
- soc-ap/middleware/README.md
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
  - soc-ap/contracts/twin/**
  record: docs/evidence/twin/TWIN-02/runs/<actual-run>/result.md
rollback:
  steps:
  - 仅回退本票候选；保存失败证据和原状态；硬件恢复须按实际SOP及授权执行
handoff:
  receiver_role: COORD
  receiver_session: null
  transport: docs
  evidence_location: docs/evidence/twin/TWIN-02
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
    expected: 交付IDL、D-Bus XML、HTTP/SSE schema、服务清单schema、线协议映射、生成规则和兼容策略；所有通道语义一致并有Owner接受
    availability: planned-not-runnable
  positive_cases:
  - 交付IDL、D-Bus XML、HTTP/SSE schema、服务清单schema、线协议映射、生成规则和兼容策略；所有通道语义一致并有Owner接受
  negative_cases:
  - 边界值/故障哨兵碰撞、版本不兼容、单位错误、无界队列、越权方法和重复命令均有拒绝规则
required_evidence_level: document
verification_environment: isolated-host-or-document
qa_review_policy: project-control/.agents/rules/codex_qa_review.md
updated: '2026-10-29T15:26:38+08:00'
module_maintenance_requirement: project-control/docs/planning/communication_modules_ownership_20261029.md
---

# TWIN-02 双环境可执行通信契约与生成规则

## 范围与交付

交付IDL、D-Bus XML、HTTP/SSE schema、服务清单schema、线协议映射、生成规则和兼容策略；所有通道语义一致并有Owner接受。

首条业务采用现有温度只读切片；只读刷新表示请求采样，不增加加热、运动、OTA或打印控制。完整模块登记实现/未实现/后续状态，不为未实现模块启动空进程后声称功能完成。

## 正反验收与边界

正例：交付IDL、D-Bus XML、HTTP/SSE schema、服务清单schema、线协议映射、生成规则和兼容策略；所有通道语义一致并有Owner接受。

负例：边界值/故障哨兵碰撞、版本不兼容、单位错误、无界队列、越权方法和重复命令均有拒绝规则。

所有运行证据须绑定源码commit与dirty diff、构建日志、制品/配置/契约哈希及实际环境。VM真实应用、隔离测试替身、真实MC/TH HIL、SoC实板四类分别登记。

## 开工与闭环

本卡为Backlog计划，未登记真实作者/检查会话、有效租约和候选输入；当前不是开工许可。Ready前按输入版本、写范围、独立检查、工作区/输出目录、资源排他及可执行验证命令逐项落实。

依赖卡Done只表示其原范围，消费时须绑定准确接受版本、证据和限制；不继承被撤回或超范围签署。若无须改旧实现，也须提交准确复用矩阵及适用验证，不以空实现自动关闭。

实现Owner负责本范围及卡内函数拆分；新增函数≤50行、≤4参。共享CMake/配置/生成输出由既定Owner串行改动并登记精确白名单，其他卡提交接口需求，不并发抢写。

作者提交候选 → COORD安排必需独立检查（QA、ENG-FWD、ENG-STATE、ENG-UI、ENG-NET、ENG-DDS、ENG-DBUS、INTEGRATOR）→ 必要真实环境验证 → COORD核对报告/制品哈希与收件 → 按实际范围推进状态。QA作者的预期、工具、报告必须由非作者ARCH独立复核；角色和计划别名不是已启动会话。

硬件使用和操作授权沿用现行HW-G及软硬件交接规范；此文档更新不执行串口、探针、烧录或加热操作。连续两次有证据修正仍失败，保存候选/失败日志交COORD重新裁决，不修改判据促通过。

[执行总表](../../../../docs/planning/vmware_soc_twin_task_execution_20261029.md) · [两阶段方案](../../../../docs/planning/vmware_soc_twin_development_plan_20261029.md)


## 2026-10-29 通信模块所有权约束

ARCH维护`contracts/twin/`权威IDL/XML/schema与兼容语义，ENG-DDS/ENG-DBUS参与接受并分别实现项目内`middleware/dds/`、`middleware/dbus/`代码与生成流程。契约须能被两个SDK一致消费；SDK公开API、生成器/输出归属和依赖版本关系一并明确，不另设私有契约原件，也不在本设计卡越界实现中间件代码。详见[模块维护规范](../../../../docs/planning/communication_modules_ownership_20261029.md)。
