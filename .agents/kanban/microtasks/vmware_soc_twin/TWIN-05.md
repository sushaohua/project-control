---
id: TWIN-05
title: TWIN-05 DDS跨进程SDK与有界QoS
revision: 2
plan_revision: vmware-soc-twin-20261029
task_kind: implementation
development_stage: vmware-twin
dispatchable: true
status: Done
blocked: false
planning_status: closed
owner: ENG-DDS
proposed_owner: ENG-DDS
executor:
  role: ENG-DDS
  agent_id: 3fbe2d65-b1c3-4c69-8a2d-084bcc76a4c3
  run_id: run_03
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
    planned_session_alias: planned-qa-twin-05
    session: 01a18bab-6746-7fb3-90ba-8d884f417707
    session_evidence:
      path: docs/evidence/twin/TWIN-05/runs/run_03/codex_session.jsonl
      sha256: 0806e3fe2042b3ed9c0f022b3602f327c0098de888c51420e85df2c315578bdc
    decision: APPROVED
    reviewed_task_revision: 2
    artifact_version:
      run: run_03
      requested_candidates:
        soc-ap: ec6081066a4b70e326e99aa124d7bbf356c41b17
        test_harness: 0b7497ba43158841eb3c4af7f16e477b9c30c2c5
        project-control: 81feb7a2d520131205af6cad7d013f87be34127d
        mcu-p3: 1246ea9cb441d074ea444f53320f5632fefcd503
    evidence: docs/evidence/twin/TWIN-05/runs/run_03/qa_review_report.md
    report_sha256: 66a17c0e17917abfc17592472ebb7082096c4a108579927ecc956685a0ab6f8d
    report_review:
      session: 01a18bcb-0ce9-7500-bc2f-22f1a88931d5
      role: ARCH
      decision: APPROVED
      reviewed_task_revision: 2
      artifact_version:
        run: run_03
        requested_candidates:
          soc-ap: ec6081066a4b70e326e99aa124d7bbf356c41b17
          test_harness: 0b7497ba43158841eb3c4af7f16e477b9c30c2c5
          project-control: 58193f4ac35cdf7b894d9b8162842e16b1cab7ba
          mcu-p3: 1246ea9cb441d074ea444f53320f5632fefcd503
        qa_execution_lock_project_control: 81feb7a2d520131205af6cad7d013f87be34127d
      evidence: docs/evidence/twin/TWIN-05/runs/run_03/arch_review_report.md
      report_sha256: f022112db3ba5560b7d207303b676d8c1be9aee0e67f60ba34afb2a83c93e08e
      session_evidence:
        path: docs/evidence/twin/TWIN-05/runs/run_03/arch_codex_session.jsonl
        sha256: 61b7e8211bcb471b8fe7be736b9d59228339629e15a38f4a9fa6526c272bb25f
  - role: ARCH
    platform: codex
    model: gpt-6-luna
    planned_session_alias: planned-arch-twin-05
    session: 01a18bcb-0ce9-7500-bc2f-22f1a88931d5
    session_evidence:
      path: docs/evidence/twin/TWIN-05/runs/run_03/arch_codex_session.jsonl
      sha256: 61b7e8211bcb471b8fe7be736b9d59228339629e15a38f4a9fa6526c272bb25f
    decision: APPROVED
    reviewed_task_revision: 2
    artifact_version:
      run: run_03
      requested_candidates:
        soc-ap: ec6081066a4b70e326e99aa124d7bbf356c41b17
        test_harness: 0b7497ba43158841eb3c4af7f16e477b9c30c2c5
        project-control: 58193f4ac35cdf7b894d9b8162842e16b1cab7ba
        mcu-p3: 1246ea9cb441d074ea444f53320f5632fefcd503
      qa_execution_lock_project_control: 81feb7a2d520131205af6cad7d013f87be34127d
    evidence: docs/evidence/twin/TWIN-05/runs/run_03/arch_review_report.md
    report_sha256: f022112db3ba5560b7d207303b676d8c1be9aee0e67f60ba34afb2a83c93e08e
  verifier_session: null
  integrator_session: null
primary_work_package: TASK-014
related_work_packages: []
depends_on:
- TWIN-02
- TWIN-03
dependency_conditions:
- task: TWIN-02
  accepted_version: 532caecf3a146802969a49e73081400c2b32b25e
  acceptance_evidence: docs/evidence/twin/TWIN-02/runs/run_03/result.md
  required: 开工前绑定准确产物、必需接受及适用限制；历史Done不批准新契约
- task: TWIN-03
  accepted_version: 0b7497ba43158841eb3c4af7f16e477b9c30c2c5
  acceptance_evidence: docs/evidence/twin/TWIN-03/runs/run_02/result.md
  required: 开工前绑定准确产物、必需接受及适用限制；历史Done不批准新契约
scope_status: mapped
allowed_repositories:
- soc-ap
- project-control
write_scope:
  soc-ap:
  - middleware/dds/**
  - config/dds/twin/**
  - tests/dds/twin/**
  - third_party/dds/**
  - third_party/archives/Fast-DDS-*.tar.*
  - third_party/archives/Fast-CDR-*.tar.*
  - third_party/archives/foonathan_memory*.tar.*
  - third_party/archives/asio-*.tar.*
  - third_party/archives/tinyxml2-*.tar.*
  project-control:
  - docs/evidence/twin/TWIN-05/**
allowed_paths:
- soc-ap/middleware/dds/**
- soc-ap/config/dds/twin/**
- soc-ap/tests/dds/twin/**
- soc-ap/third_party/dds/**
- soc-ap/third_party/archives/Fast-DDS-*.tar.*
- soc-ap/third_party/archives/Fast-CDR-*.tar.*
- soc-ap/third_party/archives/foonathan_memory*.tar.*
- soc-ap/third_party/archives/asio-*.tar.*
- soc-ap/third_party/archives/tinyxml2-*.tar.*
- project-control/docs/evidence/twin/TWIN-05/**
source_baseline:
  project-control: a5e4b5e97439cae4a7093d1d0a29c5dc9b3c7819
  soc-ap: 4445c8fedc21bafef5e6c971fcb54cec703f0e71
  mcu-p3: 1246ea9cb441d074ea444f53320f5632fefcd503
  test_harness: 6c61ce6e51cf83d7fb58d319c23cb91bf95786cb
base_commit: 6a7864293f95fd44e5d3cc631289bb71489705b7
candidate_commit: soc-ap=ec6081066a4b70e326e99aa124d7bbf356c41b17
dispatch_binding:
  source_commit: 6a7864293f95fd44e5d3cc631289bb71489705b7
  workspace_diff_sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
  consumed_artifact_versions:
    TWIN-02: 532caecf3a146802969a49e73081400c2b32b25e
    TWIN-03: 0b7497ba43158841eb3c4af7f16e477b9c30c2c5
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
worktree: soc-ap
lease:
  owner: ENG-DDS
  task_revision: 2
  lease_id: lease-twin-05-run01
  expires_at: '2026-10-30T18:00:00+08:00'
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
  - soc-ap/middleware/dds/**
  - soc-ap/config/dds/twin/**
  - soc-ap/tests/dds/twin/**
  - soc-ap/third_party/dds/**
  record: docs/evidence/twin/TWIN-05/runs/run_03/result.md
rollback:
  steps:
  - 仅回退本票候选；保存失败证据和原状态；硬件恢复须按实际SOP及授权执行
handoff:
  receiver_role: COORD
  receiver_session: coord-main-session
  transport: docs
  evidence_location: docs/evidence/twin/TWIN-05
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
    expected: 真实跨进程发布订阅、晚加入、重启与生成绑定可复现；版本/生成器/QoS/CPU内存实际值锁定
    availability: planned-not-runnable
  positive_cases:
  - 真实跨进程发布订阅、晚加入、重启与生成绑定可复现；版本/生成器/QoS/CPU内存实际值锁定
  - 项目内SDK头/实现/模块构建/示例/配置/测试与上游源码包、依赖版本、许可证、校验和补丁均可从服务器锁定候选恢复；在新独立沙箱真实跨进程通信
  negative_cases:
  - 慢消费者、无订阅者、乱序/旧代次、资源上限和中间件错误保持有界；不推导业务已完成
  - 只有README/安装库或作者install缓存、忽略src中的未归档补丁、校验失败/缺依赖却返回成功、共享脚本并行抢写或业务私建连接实现，均不得通过
required_evidence_level: server-sandbox-verified
verification_environment: independent-codex-server-sandbox-with-real-cross-process-ipc
qa_review_policy: project-control/.agents/rules/codex_qa_review.md
updated: '2026-10-29T15:26:38+08:00'
module_maintenance_requirement: project-control/docs/planning/communication_modules_ownership_20261029.md
module_owner: ENG-DDS
module_code_root: soc-ap/middleware/dds
---

# TWIN-05 DDS跨进程SDK与有界QoS

## 范围与交付

真实跨进程发布订阅、晚加入、重启与生成绑定可复现；版本/生成器/QoS/CPU内存实际值锁定。

首条业务采用现有温度只读切片；只读刷新表示请求采样，不增加加热、运动、OTA或打印控制。完整模块登记实现/未实现/后续状态，不为未实现模块启动空进程后声称功能完成。

## 正反验收与边界

正例：真实跨进程发布订阅、晚加入、重启与生成绑定可复现；版本/生成器/QoS/CPU内存实际值锁定。

负例：慢消费者、无订阅者、乱序/旧代次、资源上限和中间件错误保持有界；不推导业务已完成。

所有运行证据须绑定源码commit与dirty diff、构建日志、制品/配置/契约哈希及实际环境。VM真实应用、隔离测试替身、真实MC/TH HIL、SoC实板四类分别登记。

## 开工与闭环

本卡为Backlog计划，未登记真实作者/检查会话、有效租约和候选输入；当前不是开工许可。Ready前按输入版本、写范围、独立检查、工作区/输出目录、资源排他及可执行验证命令逐项落实。

依赖卡Done只表示其原范围，消费时须绑定准确接受版本、证据和限制；不继承被撤回或超范围签署。若无须改旧实现，也须提交准确复用矩阵及适用验证，不以空实现自动关闭。

实现Owner负责本范围及卡内函数拆分；新增函数≤50行、≤4参。共享CMake/配置/生成输出由既定Owner串行改动并登记精确白名单，其他卡提交接口需求，不并发抢写。

作者提交候选 → COORD安排必需独立检查（QA、ARCH）→ 必要真实环境验证 → COORD核对报告/制品哈希与收件 → 按实际范围推进状态。QA作者的预期、工具、报告必须由非作者ARCH独立复核；角色和计划别名不是已启动会话。

硬件使用和操作授权沿用现行HW-G及软硬件交接规范；此文档更新不执行串口、探针、烧录或加热操作。连续两次有证据修正仍失败，保存候选/失败日志交COORD重新裁决，不修改判据促通过。

[执行总表](../../../../docs/planning/vmware_soc_twin_task_execution_20261029.md) · [两阶段方案](../../../../docs/planning/vmware_soc_twin_development_plan_20261029.md)


## 2026-10-29 独立通信模块与源码维护

ENG-DDS长期维护`soc-ap/middleware/dds/`的公开API、真实SDK源码、独立模块CMake、示例及生成接入，并维护`config/dds/twin/`、`tests/dds/twin/`和`third_party/dds/`的来源/准确版本/校验/许可证/补丁/配方。原始上游源码包沿用`third_party/archives/`，不另复制一套。模块代码纳入当前soc-ap仓和服务器候选，不依赖个人安装。

公共`third_party/build.sh`、总校验索引/总README及公共构建由INTEGRATOR按TWIN-04串行修改；本卡只提交自身模块配方/校验与集成请求，不越界修改公共文件。权威IDL/XML由ARCH在TWIN-02维护；业务Owner调用SDK，不私建另一套通信底座。

本次只更新计划/维护入口，尚未实现SDK。验收必须从服务器源码在独立沙箱重建并实际跨进程运行，不能以源码包、库文件或空壳目录存在替代。详见[模块维护规范](../../../../docs/planning/communication_modules_ownership_20261029.md)。
