---
id: TWIN-04
title: TWIN-04 VMware构建配置与同构服务生命周期
revision: 2
plan_revision: vmware-soc-twin-20261029
task_kind: implementation
development_stage: vmware-twin
dispatchable: true
status: InProgress
blocked: false
planning_status: dispatched
owner: INTEGRATOR
proposed_owner: INTEGRATOR
executor:
  role: INTEGRATOR
  agent_id: INTEGRATOR
  run_id: run_02
candidate_commit: soc-ap=688e4d4cd27a1e76d9cd3d9377659a178926d1e1; test_harness=0b7497ba43158841eb3c4af7f16e477b9c30c2c5; project-control=430d30bb2d99211a65dbdc4aa840baef15b2cec7; mcu-p3=1246ea9cb441d074ea444f53320f5632fefcd503
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
    planned_session_alias: planned-qa-twin-04
    session: 01a18ab5-b1e8-7751-8ad8-b7ce15218e37
    decision: REJECTED
    reviewed_task_revision: 2
    artifact_version: soc-ap=89ac9d54c2994f635be49faa1b88ea2440b083ff; project-control=80ffa386f3ff682b0913763109d63c865b0d9808
    evidence: docs/evidence/twin/TWIN-04/runs/run_01/qa_review_report.md
    report_sha256: 3e2796b24bc6eb5ff891cbbc9a5276a0afac718f27c0c66c890357fbc91bbf76
  - role: ARCH
    platform: codex
    model: gpt-6-luna
    planned_session_alias: planned-arch-twin-04
    session: null
    decision: null
    reviewed_task_revision: null
    artifact_version: null
    evidence: null
    report_sha256: null
  verifier_session: null
  integrator_session: null
primary_work_package: TASK-004
related_work_packages: []
depends_on:
- TWIN-02
dependency_conditions:
- task: TWIN-02
  accepted_version: 532caecf3a146802969a49e73081400c2b32b25e
  acceptance_evidence: docs/evidence/twin/TWIN-02/runs/run_03/result.md
  required: 开工前绑定准确产物、必需接受及适用限制；历史Done不批准新契约
scope_status: mapped
allowed_repositories:
- soc-ap
- project-control
write_scope:
  soc-ap:
  - runtime/build/**
  - runtime/common/**
  - runtime/vmware/**
  - config/runtime/common/**
  - config/runtime/vmware/**
  - cmake/toolchains/vmware.cmake
  - tools/twin_build/**
  - third_party/build.sh
  - third_party/README.md
  - third_party/archives/checksums.sha256
  project-control:
  - docs/evidence/twin/TWIN-04/**
allowed_paths:
- soc-ap/runtime/build/**
- soc-ap/runtime/common/**
- soc-ap/runtime/vmware/**
- soc-ap/config/runtime/common/**
- soc-ap/config/runtime/vmware/**
- soc-ap/cmake/toolchains/vmware.cmake
- soc-ap/tools/twin_build/**
- soc-ap/third_party/build.sh
- soc-ap/third_party/README.md
- soc-ap/third_party/archives/checksums.sha256
- project-control/docs/evidence/twin/TWIN-04/**
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
  - soc-ap/runtime/build/**
  - soc-ap/runtime/common/**
  - soc-ap/runtime/vmware/**
  - soc-ap/config/runtime/common/**
  - soc-ap/config/runtime/vmware/**
  - soc-ap/cmake/toolchains/vmware.cmake
  - soc-ap/tools/twin_build/**
  record: docs/evidence/twin/TWIN-04/runs/<actual-run>/result.md
rollback:
  steps:
  - 仅回退本票候选；保存失败证据和原状态；硬件恢复须按实际SOP及授权执行
handoff:
  receiver_role: COORD
  receiver_session: null
  transport: docs
  evidence_location: docs/evidence/twin/TWIN-04
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
    expected: 真实VM启动/停止/就绪/健康/退避/账户权限/日志限制可复现；同一业务构建入口与profile机制可供SoC复用；最终共享构建文件由本Owner集中改动
    availability: planned-not-runnable
  positive_cases:
  - 真实VM启动/停止/就绪/健康/退避/账户权限/日志限制可复现；同一业务构建入口与profile机制可供SoC复用；最终共享构建文件由本Owner集中改动
  negative_cases:
  - 基础IPC未就绪、设备缺失、服务崩溃、重启风暴、日志满与异常退出可观察；ready与设备健康分离且无循环依赖
required_evidence_level: software-verified
verification_environment: isolated-host-or-document
qa_review_policy: project-control/.agents/rules/codex_qa_review.md
updated: '2026-10-29T15:26:38+08:00'
module_maintenance_requirement: project-control/docs/planning/communication_modules_ownership_20261029.md
---

# TWIN-04 VMware构建配置与同构服务生命周期

## 范围与交付

真实VM启动/停止/就绪/健康/退避/账户权限/日志限制可复现；同一业务构建入口与profile机制可供SoC复用；最终共享构建文件由本Owner集中改动。

首条业务采用现有温度只读切片；只读刷新表示请求采样，不增加加热、运动、OTA或打印控制。完整模块登记实现/未实现/后续状态，不为未实现模块启动空进程后声称功能完成。

## 正反验收与边界

正例：真实VM启动/停止/就绪/健康/退避/账户权限/日志限制可复现；同一业务构建入口与profile机制可供SoC复用；最终共享构建文件由本Owner集中改动。

负例：基础IPC未就绪、设备缺失、服务崩溃、重启风暴、日志满与异常退出可观察；ready与设备健康分离且无循环依赖。

所有运行证据须绑定源码commit与dirty diff、构建日志、制品/配置/契约哈希及实际环境。VM真实应用、隔离测试替身、真实MC/TH HIL、SoC实板四类分别登记。

## 开工与闭环

本卡为Backlog计划，未登记真实作者/检查会话、有效租约和候选输入；当前不是开工许可。Ready前按输入版本、写范围、独立检查、工作区/输出目录、资源排他及可执行验证命令逐项落实。

依赖卡Done只表示其原范围，消费时须绑定准确接受版本、证据和限制；不继承被撤回或超范围签署。若无须改旧实现，也须提交准确复用矩阵及适用验证，不以空实现自动关闭。

实现Owner负责本范围及卡内函数拆分；新增函数≤50行、≤4参。共享CMake/配置/生成输出由既定Owner串行改动并登记精确白名单，其他卡提交接口需求，不并发抢写。

作者提交候选 → COORD安排必需独立检查（QA、ARCH）→ 必要真实环境验证 → COORD核对报告/制品哈希与收件 → 按实际范围推进状态。QA作者的预期、工具、报告必须由非作者ARCH独立复核；角色和计划别名不是已启动会话。

硬件使用和操作授权沿用现行HW-G及软硬件交接规范；此文档更新不执行串口、探针、烧录或加热操作。连续两次有证据修正仍失败，保存候选/失败日志交COORD重新裁决，不修改判据促通过。

[执行总表](../../../../docs/planning/vmware_soc_twin_task_execution_20261029.md) · [两阶段方案](../../../../docs/planning/vmware_soc_twin_development_plan_20261029.md)


## 2026-10-29 通信依赖公共集成

INTEGRATOR是`third_party/build.sh`、总README及`archives/checksums.sha256`的唯一公共文件写入者。ENG-DDS/ENG-DBUS分别维护自己的SDK源码、模块CMake、配方和校验，INTEGRATOR接收其已接受的集成请求后单点串行更新公共入口，绑定新候选并复验。先提供模块注册/构建约定，后续实现就绪再集成，不制造TWIN-04与05/06的循环依赖；共享构建若需再改，按本卡原Owner修订受影响候选，不允许其他卡越界抢写。

两平台用隔离build/install/profile；第三方版本/依赖/许可证与源码归档需可从服务器恢复。当前共用脚本和本机install存在不代表可复现构建或运行已验收。详见[模块维护规范](../../../../docs/planning/communication_modules_ownership_20261029.md)。
