---
id: TWIN-01
title: TWIN-01 整体服务架构与温度冲突逐项对账
revision: 2
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
  agent_id: 01a1809a-7a11-74f0-9112-88ec09142100
  run_id: run_02
reviewer:
- QA
- ENG-FWD
- ENG-STATE
- ENG-UI
- ENG-NET
- ENG-DDS
- ENG-DBUS
- INTEGRATOR
- ENG-MC
- ENG-TH
verifier: null
integrator: INTEGRATOR
review_assignments:
  reviewer_sessions:
  - role: QA
    platform: codex
    model: gpt-6-luna
    planned_session_alias: planned-qa-twin-01
    session: 01a18795-89f2-74d0-8d5e-adec286d8ef0
    session_evidence:
      path: docs/evidence/twin/TWIN-01/runs/run_02/qa_review_report.md
      sha256: 4a7ec321cfd4f643678148fc912670ff339b908d8c040f2a43e2e7f3ebe17f54
    decision: APPROVED
    reviewed_task_revision: 2
    artifact_version: "project-control=e9c687584e3d161d68355a0a0a5237e20856712a; test_harness=210ddd1c3f6f59594836c91b68aae55fb7a35181"
    evidence: docs/evidence/twin/TWIN-01/runs/run_02/qa_review_report.md
    report_sha256: 4a7ec321cfd4f643678148fc912670ff339b908d8c040f2a43e2e7f3ebe17f54
    report_review:
      session: 01a18797-fe88-7a60-91a7-787643594bd2
      role: ARCH
      decision: APPROVED
      reviewed_task_revision: 2
      artifact_version: "project-control=e9c687584e3d161d68355a0a0a5237e20856712a; test_harness=210ddd1c3f6f59594836c91b68aae55fb7a35181"
      evidence: docs/evidence/twin/TWIN-01/runs/run_02/arch_review_report.md
      report_sha256: 9030e0d9e199184afcede068ccadd80a79d9b1d3724797971d546cc23c9704bb
      session_evidence:
        path: docs/evidence/twin/TWIN-01/runs/run_02/arch_review_report.md
        sha256: 9030e0d9e199184afcede068ccadd80a79d9b1d3724797971d546cc23c9704bb
  - role: ENG-FWD
    platform: null
    model: null
    planned_session_alias: planned-eng-fwd-twin-01
    session: 01a18355-12ab-70a1-8901-c8f2b3e41001
    session_evidence:
      path: docs/evidence/twin/TWIN-01/runs/run_02/reviews/review_eng_fwd.md
      sha256: 8093a2bffff40c3529e2178eca837034c21e2b86cef79a3d21ff47327f3154b4
    decision: APPROVED
    reviewed_task_revision: 2
    artifact_version: "project-control=e9c687584e3d161d68355a0a0a5237e20856712a; test_harness=210ddd1c3f6f59594836c91b68aae55fb7a35181"
    evidence: docs/evidence/twin/TWIN-01/runs/run_02/reviews/review_eng_fwd.md
    report_sha256: 8093a2bffff40c3529e2178eca837034c21e2b86cef79a3d21ff47327f3154b4
  - role: ENG-STATE
    platform: null
    model: null
    planned_session_alias: planned-eng-state-twin-01
    session: 01a18355-12ab-70a1-8901-c8f2b3e41002
    session_evidence:
      path: docs/evidence/twin/TWIN-01/runs/run_02/reviews/review_eng_state.md
      sha256: 0cf9f65319c325a1ba47e333cadecebb5d89bd7bf469e9299429e3b128935f3d
    decision: APPROVED
    reviewed_task_revision: 2
    artifact_version: "project-control=e9c687584e3d161d68355a0a0a5237e20856712a; test_harness=210ddd1c3f6f59594836c91b68aae55fb7a35181"
    evidence: docs/evidence/twin/TWIN-01/runs/run_02/reviews/review_eng_state.md
    report_sha256: 0cf9f65319c325a1ba47e333cadecebb5d89bd7bf469e9299429e3b128935f3d
  - role: ENG-UI
    platform: null
    model: null
    planned_session_alias: planned-eng-ui-twin-01
    session: 01a18355-12ab-70a1-8901-c8f2b3e41003
    session_evidence:
      path: docs/evidence/twin/TWIN-01/runs/run_02/reviews/review_eng_ui.md
      sha256: 4ba8fc3dbbd35297c50d5d6315829685a88f7986c7ee6f47a7a4d881cccc5025
    decision: APPROVED
    reviewed_task_revision: 2
    artifact_version: "project-control=e9c687584e3d161d68355a0a0a5237e20856712a; test_harness=210ddd1c3f6f59594836c91b68aae55fb7a35181"
    evidence: docs/evidence/twin/TWIN-01/runs/run_02/reviews/review_eng_ui.md
    report_sha256: 4ba8fc3dbbd35297c50d5d6315829685a88f7986c7ee6f47a7a4d881cccc5025
  - role: ENG-NET
    platform: null
    model: null
    planned_session_alias: planned-eng-net-twin-01
    session: 01a18355-12ab-70a1-8901-c8f2b3e41004
    session_evidence:
      path: docs/evidence/twin/TWIN-01/runs/run_02/reviews/review_eng_net.md
      sha256: 2d5585f180c788e2c3bc9235b37d7d1cce988301a551b0eb0822f168be3088ad
    decision: APPROVED
    reviewed_task_revision: 2
    artifact_version: "project-control=e9c687584e3d161d68355a0a0a5237e20856712a; test_harness=210ddd1c3f6f59594836c91b68aae55fb7a35181"
    evidence: docs/evidence/twin/TWIN-01/runs/run_02/reviews/review_eng_net.md
    report_sha256: 2d5585f180c788e2c3bc9235b37d7d1cce988301a551b0eb0822f168be3088ad
  - role: ENG-DDS
    platform: null
    model: null
    planned_session_alias: planned-eng-dds-twin-01
    session: 01a18355-12ab-70a1-8901-c8f2b3e41005
    session_evidence:
      path: docs/evidence/twin/TWIN-01/runs/run_02/reviews/review_eng_dds.md
      sha256: abb7df2351ef1e76f41ad1011e08f0c99c077756e553bea30bb34342c6bfc002
    decision: APPROVED
    reviewed_task_revision: 2
    artifact_version: "project-control=e9c687584e3d161d68355a0a0a5237e20856712a; test_harness=210ddd1c3f6f59594836c91b68aae55fb7a35181"
    evidence: docs/evidence/twin/TWIN-01/runs/run_02/reviews/review_eng_dds.md
    report_sha256: abb7df2351ef1e76f41ad1011e08f0c99c077756e553bea30bb34342c6bfc002
  - role: ENG-DBUS
    platform: null
    model: null
    planned_session_alias: planned-eng-dbus-twin-01
    session: 01a18355-12ab-70a1-8901-c8f2b3e41006
    session_evidence:
      path: docs/evidence/twin/TWIN-01/runs/run_02/reviews/review_eng_dbus.md
      sha256: bb69b4524e0f8f4640d47d6a262f127137c805dff1a3287a776049683ca08b01
    decision: APPROVED
    reviewed_task_revision: 2
    artifact_version: "project-control=e9c687584e3d161d68355a0a0a5237e20856712a; test_harness=210ddd1c3f6f59594836c91b68aae55fb7a35181"
    evidence: docs/evidence/twin/TWIN-01/runs/run_02/reviews/review_eng_dbus.md
    report_sha256: bb69b4524e0f8f4640d47d6a262f127137c805dff1a3287a776049683ca08b01
  - role: INTEGRATOR
    platform: null
    model: null
    planned_session_alias: planned-integrator-twin-01
    session: 01a18355-12ab-70a1-8901-c8f2b3e41007
    session_evidence:
      path: docs/evidence/twin/TWIN-01/runs/run_02/reviews/review_integrator.md
      sha256: 14befaff40913a02cdb659c233ef4478dc2f8d209ae51707a9290097ffe97d85
    decision: APPROVED
    reviewed_task_revision: 2
    artifact_version: "project-control=e9c687584e3d161d68355a0a0a5237e20856712a; test_harness=210ddd1c3f6f59594836c91b68aae55fb7a35181"
    evidence: docs/evidence/twin/TWIN-01/runs/run_02/reviews/review_integrator.md
    report_sha256: 14befaff40913a02cdb659c233ef4478dc2f8d209ae51707a9290097ffe97d85
  - role: ENG-MC
    platform: null
    model: null
    planned_session_alias: planned-eng-mc-twin-01
    session: 01a18355-12ab-70a1-8901-c8f2b3e41008
    session_evidence:
      path: docs/evidence/twin/TWIN-01/runs/run_02/reviews/review_eng_mc.md
      sha256: 1374fd164b89775ea6bc23c8f938a8c4ba6923fb79eb5c4580013e24549c7ab6
    decision: APPROVED
    reviewed_task_revision: 2
    artifact_version: "project-control=e9c687584e3d161d68355a0a0a5237e20856712a; test_harness=210ddd1c3f6f59594836c91b68aae55fb7a35181"
    evidence: docs/evidence/twin/TWIN-01/runs/run_02/reviews/review_eng_mc.md
    report_sha256: 1374fd164b89775ea6bc23c8f938a8c4ba6923fb79eb5c4580013e24549c7ab6
  - role: ENG-TH
    platform: null
    model: null
    planned_session_alias: planned-eng-th-twin-01
    session: 01a18355-12ab-70a1-8901-c8f2b3e41009
    session_evidence:
      path: docs/evidence/twin/TWIN-01/runs/run_02/reviews/review_eng_th.md
      sha256: 35b140e4e092282c14a17a8afe64b62a9799979bf0563f529726a01b4ebd4d26
    decision: APPROVED
    reviewed_task_revision: 2
    artifact_version: "project-control=e9c687584e3d161d68355a0a0a5237e20856712a; test_harness=210ddd1c3f6f59594836c91b68aae55fb7a35181"
    evidence: docs/evidence/twin/TWIN-01/runs/run_02/reviews/review_eng_th.md
    report_sha256: 35b140e4e092282c14a17a8afe64b62a9799979bf0563f529726a01b4ebd4d26
  verifier_session: null
  integrator_session: null
primary_work_package: TASK-005
related_work_packages: []
depends_on:
- CR-11
dependency_conditions:
- task: CR-11
  accepted_version: null
  acceptance_evidence: null
  required: 仅绑定既有只读级联收件及复用限制供对账，不把历史Done作为新契约批准
scope_status: mapped
allowed_repositories:
- project-control
write_scope:
  project-control:
  - docs/interfaces/vmware_soc_twin_architecture_icd_20261029.md
  - docs/planning/twin_reuse_matrix_20261029.md
  - docs/evidence/twin/TWIN-01/**
allowed_paths:
- project-control/docs/interfaces/vmware_soc_twin_architecture_icd_20261029.md
- project-control/docs/planning/twin_reuse_matrix_20261029.md
- project-control/docs/evidence/twin/TWIN-01/**
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
  - project-control/docs/interfaces/vmware_soc_twin_architecture_icd_20261029.md
  - project-control/docs/planning/twin_reuse_matrix_20261029.md
  record: docs/evidence/twin/TWIN-01/runs/run_02/result.md
rollback:
  steps:
  - 仅回退本票候选；保存失败证据和原状态；硬件恢复须按实际SOP及授权执行
handoff:
  receiver_role: COORD
  receiver_session: coord-main-session
  transport: docs
  evidence_location: docs/evidence/twin/TWIN-01/runs/run_02
  acknowledgement: APPROVED
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
    expected: 接受服务/部署图、完整模块清单及首切片边界；C1～C6逐项给出依据、影响、修订或无修改理由和消费限制；VM数值预算与目标待测项分列
    availability: planned-not-runnable
  positive_cases:
  - 接受服务/部署图、完整模块清单及首切片边界；C1～C6逐项给出依据、影响、修订或无修改理由和消费限制；VM数值预算与目标待测项分列
  negative_cases:
  - 拒绝同进程替身、循环就绪依赖、过期值作新值、旧Done自动继承与未冻结字段继续消费
required_evidence_level: document
verification_environment: isolated-host-or-document
qa_review_policy: project-control/.agents/rules/codex_qa_review.md
updated: '2026-10-29T14:30:00+08:00'
---

# TWIN-01 整体服务架构与温度冲突逐项对账

## 范围与交付

接受服务/部署图、完整模块清单及首切片边界；C1～C6逐项给出依据、影响、修订或无修改理由和消费限制；VM数值预算与目标待测项分列。

首条业务采用现有温度只读切片；只读刷新表示请求采样，不增加加热、运动、OTA或打印控制。完整模块登记实现/未实现/后续状态，不为未实现模块启动空进程后声称功能完成。

## 正反验收与边界

正例：接受服务/部署图、完整模块清单及首切片边界；C1～C6逐项给出依据、影响、修订或无修改理由和消费限制；VM数值预算与目标待测项分列。

负例：拒绝同进程替身、循环就绪依赖、过期值作新值、旧Done自动继承与未冻结字段继续消费。

所有运行证据须绑定源码commit与dirty diff、构建日志、制品/配置/契约哈希及实际环境。VM真实应用、隔离测试替身、真实MC/TH HIL、SoC实板四类分别登记。

## 开工与闭环

本卡为Backlog计划，未登记真实作者/检查会话、有效租约和候选输入；当前不是开工许可。Ready前按输入版本、写范围、独立检查、工作区/输出目录、资源排他及可执行验证命令逐项落实。

依赖卡Done只表示其原范围，消费时须绑定准确接受版本、证据和限制；不继承被撤回或超范围签署。若无须改旧实现，也须提交准确复用矩阵及适用验证，不以空实现自动关闭。

实现Owner负责本范围及卡内函数拆分；新增函数≤50行、≤4参。共享CMake/配置/生成输出由既定Owner串行改动并登记精确白名单，其他卡提交接口需求，不并发抢写。

作者提交候选 → COORD安排必需独立检查（QA、ENG-FWD、ENG-STATE、ENG-UI、ENG-NET、ENG-DDS、ENG-DBUS、INTEGRATOR、ENG-MC、ENG-TH）→ 必要真实环境验证 → COORD核对报告/制品哈希与收件 → 按实际范围推进状态。QA作者的预期、工具、报告必须由非作者ARCH独立复核；角色和计划别名不是已启动会话。

硬件使用和操作授权沿用现行HW-G及软硬件交接规范；此文档更新不执行串口、探针、烧录或加热操作。连续两次有证据修正仍失败，保存候选/失败日志交COORD重新裁决，不修改判据促通过。

[执行总表](../../../../docs/planning/vmware_soc_twin_task_execution_20261029.md) · [两阶段方案](../../../../docs/planning/vmware_soc_twin_development_plan_20261029.md)
