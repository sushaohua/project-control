---
id: TWIN-06
title: TWIN-06 D-Bus跨进程SDK与权限超时
revision: 2
plan_revision: vmware-soc-twin-20261029
task_kind: implementation
development_stage: vmware-twin
dispatchable: true
status: Backlog
blocked: false
planning_status: planned-not-dispatched
owner: null
proposed_owner: ENG-DBUS
executor:
  role: ENG-DBUS
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
    planned_session_alias: planned-qa-twin-06
    session: null
    decision: null
    reviewed_task_revision: null
    artifact_version: null
    evidence: null
    report_sha256: null
  - role: ARCH
    platform: codex
    model: gpt-6-luna
    planned_session_alias: planned-arch-twin-06
    session: null
    decision: null
    reviewed_task_revision: null
    artifact_version: null
    evidence: null
    report_sha256: null
  verifier_session: null
  integrator_session: null
primary_work_package: TASK-015
related_work_packages: []
depends_on:
- TWIN-02
- TWIN-03
dependency_conditions:
- task: TWIN-02
  accepted_version: null
  acceptance_evidence: null
  required: 开工前绑定准确产物、必需接受及适用限制；历史Done不批准新契约
- task: TWIN-03
  accepted_version: null
  acceptance_evidence: null
  required: 开工前绑定准确产物、必需接受及适用限制；历史Done不批准新契约
scope_status: mapped
allowed_repositories:
- soc-ap
- project-control
write_scope:
  soc-ap:
  - middleware/dbus/**
  - config/dbus/twin/**
  - tests/dbus/twin/**
  - third_party/dbus/**
  - third_party/archives/dbus-*.tar.*
  project-control:
  - docs/evidence/twin/TWIN-06/**
allowed_paths:
- soc-ap/middleware/dbus/**
- soc-ap/config/dbus/twin/**
- soc-ap/tests/dbus/twin/**
- soc-ap/third_party/dbus/**
- soc-ap/third_party/archives/dbus-*.tar.*
- project-control/docs/evidence/twin/TWIN-06/**
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
  - soc-ap/middleware/dbus/**
  - soc-ap/config/dbus/twin/**
  - soc-ap/tests/dbus/twin/**
  - soc-ap/third_party/dbus/**
  - soc-ap/third_party/archives/dbus-*.tar.*
  record: docs/evidence/twin/TWIN-06/runs/<actual-run>/result.md
rollback:
  steps:
  - 仅回退本票候选；保存失败证据和原状态；硬件恢复须按实际SOP及授权执行
handoff:
  receiver_role: COORD
  receiver_session: null
  transport: docs
  evidence_location: docs/evidence/twin/TWIN-06
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
    expected: 真实总线服务/对象/方法/错误、请求期限、权限及名称所有权按XML互操作；两profile使用同一封装
    availability: planned-not-runnable
  positive_cases:
  - 真实总线服务/对象/方法/错误、请求期限、权限及名称所有权按XML互操作；两profile使用同一封装
  - 项目内SDK头/实现/模块构建/示例/配置/测试与上游源码包、依赖版本、许可证、校验和补丁均可从服务器锁定候选恢复；在新独立沙箱真实跨进程通信
  negative_cases:
  - 名称丢失、对端重启、越权、超时、重复调用与背压按契约处理；调用返回不冒充设备完成
  - 只有README/安装库或作者install缓存、忽略src中的未归档补丁、校验失败/缺依赖却返回成功、共享脚本并行抢写或业务私建连接实现，均不得通过
required_evidence_level: server-sandbox-verified
verification_environment: independent-codex-server-sandbox-with-real-cross-process-ipc
qa_review_policy: project-control/.agents/rules/codex_qa_review.md
updated: '2026-10-29T15:26:38+08:00'
module_maintenance_requirement: project-control/docs/planning/communication_modules_ownership_20261029.md
module_owner: ENG-DBUS
module_code_root: soc-ap/middleware/dbus
---

# TWIN-06 D-Bus跨进程SDK与权限超时

## 范围与交付

真实总线服务/对象/方法/错误、请求期限、权限及名称所有权按XML互操作；两profile使用同一封装。

首条业务采用现有温度只读切片；只读刷新表示请求采样，不增加加热、运动、OTA或打印控制。完整模块登记实现/未实现/后续状态，不为未实现模块启动空进程后声称功能完成。

## 正反验收与边界

正例：真实总线服务/对象/方法/错误、请求期限、权限及名称所有权按XML互操作；两profile使用同一封装。

负例：名称丢失、对端重启、越权、超时、重复调用与背压按契约处理；调用返回不冒充设备完成。

所有运行证据须绑定源码commit与dirty diff、构建日志、制品/配置/契约哈希及实际环境。VM真实应用、隔离测试替身、真实MC/TH HIL、SoC实板四类分别登记。

## 开工与闭环

本卡为Backlog计划，未登记真实作者/检查会话、有效租约和候选输入；当前不是开工许可。Ready前按输入版本、写范围、独立检查、工作区/输出目录、资源排他及可执行验证命令逐项落实。

依赖卡Done只表示其原范围，消费时须绑定准确接受版本、证据和限制；不继承被撤回或超范围签署。若无须改旧实现，也须提交准确复用矩阵及适用验证，不以空实现自动关闭。

实现Owner负责本范围及卡内函数拆分；新增函数≤50行、≤4参。共享CMake/配置/生成输出由既定Owner串行改动并登记精确白名单，其他卡提交接口需求，不并发抢写。

作者提交候选 → COORD安排必需独立检查（QA、ARCH）→ 必要真实环境验证 → COORD核对报告/制品哈希与收件 → 按实际范围推进状态。QA作者的预期、工具、报告必须由非作者ARCH独立复核；角色和计划别名不是已启动会话。

硬件使用和操作授权沿用现行HW-G及软硬件交接规范；此文档更新不执行串口、探针、烧录或加热操作。连续两次有证据修正仍失败，保存候选/失败日志交COORD重新裁决，不修改判据促通过。

[执行总表](../../../../docs/planning/vmware_soc_twin_task_execution_20261029.md) · [两阶段方案](../../../../docs/planning/vmware_soc_twin_development_plan_20261029.md)


## 2026-10-29 独立通信模块与源码维护

ENG-DBUS长期维护`soc-ap/middleware/dbus/`的公开API、真实SDK源码、独立模块CMake、示例及生成接入，并维护`config/dbus/twin/`、`tests/dbus/twin/`和`third_party/dbus/`的来源/准确版本/校验/许可证/补丁/配方。原始上游源码包沿用`third_party/archives/`，不另复制一套。模块代码纳入当前soc-ap仓和服务器候选，不依赖个人安装。

公共`third_party/build.sh`、总校验索引/总README及公共构建由INTEGRATOR按TWIN-04串行修改；本卡只提交自身模块配方/校验与集成请求，不越界修改公共文件。权威IDL/XML由ARCH在TWIN-02维护；业务Owner调用SDK，不私建另一套通信底座。

本次只更新计划/维护入口，尚未实现SDK。验收必须从服务器源码在独立沙箱重建并实际跨进程运行，不能以源码包、库文件或空壳目录存在替代。详见[模块维护规范](../../../../docs/planning/communication_modules_ownership_20261029.md)。
