---
id: TWIN-42
title: TWIN-42 多模块系统集成阶段单功能穿透梳理与级联验证
revision: 2
plan_revision: vmware-soc-twin-20261029
task_kind: integration
development_stage: vmware-twin
dispatchable: true
status: Review
blocked: false
planning_status: planned
owner: INTEGRATOR
proposed_owner: INTEGRATOR
executor:
  role: INTEGRATOR
  agent_id: session-integrator-twin-42
  run_id: author_01
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
    planned_session_alias: planned-qa-twin-42
    session: session-qa-hil-twin-42
    session_evidence: docs/evidence/twin/TWIN-42/runs/qa_01/qa_review_report.md
    decision: APPROVED
    reviewed_task_revision: 2
    artifact_version: soc-ap=5955fa57c9be6b90ff34156a1a6b183717f9a3a6; project-control=c50f652e0ecb81c3d8c550c81a24a6fe01dd0fb5; test_harness=3a10e16beae43e51fc9673925179471e43f66114; mcu-p3=04231388c842c1ce3e5b71675d0dc118a65edf2e
    evidence: docs/evidence/twin/TWIN-42/runs/qa_01/qa_review_report.md
    report_sha256: 0743983ad3f1c8b30172daee03ea0286bab519ffe7b80717ceaa550ae7ed7c4e
  - role: ARCH
    platform: codex
    model: gpt-6-luna
    planned_session_alias: planned-arch-twin-42
    session: session-arch-review-42
    session_evidence: docs/evidence/twin/TWIN-42/runs/arch_01/arch_review_report.md
    decision: APPROVED
    reviewed_task_revision: 2
    artifact_version: soc-ap=5955fa57c9be6b90ff34156a1a6b183717f9a3a6; project-control=c50f652e0ecb81c3d8c550c81a24a6fe01dd0fb5; test_harness=3a10e16beae43e51fc9673925179471e43f66114; mcu-p3=04231388c842c1ce3e5b71675d0dc118a65edf2e
    evidence: docs/evidence/twin/TWIN-42/runs/arch_01/arch_review_report.md
    report_sha256: 96fd1d75b47e213e5eab4a2a16528b1691bfc130638e1c023623e387921356c4
  verifier_session: null
  integrator_session: null
primary_work_package: TASK-010
related_work_packages:
- TASK-005
- TASK-009
depends_on:
- TWIN-35
- TWIN-40
- TWIN-41
dependency_conditions:
- task: TWIN-35
  accepted_version: soc-ap=2e19a4242699e3a6a9be5c483d72b2260ffc3dd2; project-control=c6eb49339794cb150fbf9e6584be6e63dc366f60
  acceptance_evidence: docs/evidence/twin/TWIN-35/runs/run_01/qa_review_report.md
  required: 继承TWIN-35端到端打印闭环基础
- task: TWIN-40
  accepted_version: soc-ap=3ff4b144ef4d8c695b5f56d0996524adad0e644c; project-control=afd525946602c973d52feedcf7364f77ab2d221c
  acceptance_evidence: docs/evidence/twin/TWIN-40/runs/run_01/qa_review_report.md
  required: 继承TWIN-40热插拔集成闭环基线
- task: TWIN-41
  accepted_version: project-control=afd525946602c973d52feedcf7364f77ab2d221c
  acceptance_evidence: docs/evidence/twin/TWIN-41/runs/run_01/qa_review_report.md
  required: 消费TWIN-41单功能全流程时序闭环与协议映射
scope_status: mapped
allowed_repositories:
- project-control
- soc-ap
write_scope:
  project-control:
  - docs/evidence/twin/TWIN-42/**
allowed_paths:
- project-control/docs/evidence/twin/TWIN-42/**
source_baseline:
  project-control: afd525946602c973d52feedcf7364f77ab2d221c
  soc-ap: 3ff4b144ef4d8c695b5f56d0996524adad0e644c
  mcu-p3: 04231388c842c1ce3e5b71675d0dc118a65edf2e
  test_harness: 0b7497ba43158841eb3c4af7f16e477b9c30c2c5
base_commit: afd525946602c973d52feedcf7364f77ab2d221c
candidate_commit: cb59514a74ccbde68832b12f4340114bc6645b55
dispatch_binding:
  source_commit: afd525946602c973d52feedcf7364f77ab2d221c
  workspace_diff_sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
  consumed_artifact_versions: {}
protocol_input:
  path: project-control/docs/evidence/architecture/qa_review_hardware_realism_proposal.md
  sha256: df3db0adf20bb9cc240b1bf144ce050d3a77a5c0fb6e104b2578a5b936a91ae5
  revision: 1
read_sources:
- soc-ap/tests/integration/test_first_release_print_loop.c
worktree: project-control
lease: null
resources:
- resource: integrator-twin-env
  location: null
  exclusive: true
  pending: Ready前落实
- resource: qa-independent-vmware-hil-env
  location: null
  exclusive: true
  pending: COORD在Ready前落实独立QA VMware实例、锁定候选部署环境及真实MC/TH HIL独占时段；QA不得复用INTEGRATOR运行实例或证据作为自己的验证结果
budget:
  planned_checkpoint_minutes: 60
  max_evidence_based_corrections: 2
  on_limit: 保存证据交COORD
checkpoint: 开工前绑定；组件自检；双独立沙箱检查；收件
execution_contract: project-control/docs/planning/vmware_soc_twin_task_execution_20261029.md
readiness_pending: []
deliverables:
  artifacts:
  - project-control/docs/evidence/twin/TWIN-42/runs/author_01/feature_by_feature_penetration_matrix.md
  - project-control/docs/evidence/twin/TWIN-42/runs/<qa-run>/qa_review_report.md（独立QA从服务器候选重新构建、部署并执行真实MC/TH HIL后的报告与环境证据）
  record: docs/evidence/twin/TWIN-42/runs/author_01/result.md
rollback:
  steps:
  - 仅回退本票候选；保存失败证据和原状态
handoff:
  receiver_role: COORD
  receiver_session: session-coord-autorun
  transport: docs
  evidence_location: docs/evidence/twin/TWIN-42
  acknowledgement: null
verification:
  commands:
  - id: check_graph
    cwd: .
    command: PYTHONDONTWRITEBYTECODE=1 python3 project-control/tools/check_task_graph.py --workspace .
    expected: 结构无错误
    availability: local
  positive_cases:
  - 按单功能维度逐个执行端到端穿透验证，产出 10 大功能的穿透验证闭环矩阵
  - 每个功能均通过正向闭环、无 ACK 超时阻断、带 Sequence 报错核实
  - 关键运控功能在执行中经受物理拔线测试，CPU 保持正常（<= 2%），UI 准确阻断
  - 热插拔恢复后具备自愈重连验证记录
  - 独立QA使用独立Codex会话和新建隔离环境，从服务器获取本卡锁定的准确候选，自行构建并部署SoC服务；不得复用INTEGRATOR的工作区、构建产物、运行会话或原始验证结果
  - 独立QA在COORD分配的排他HIL时段接入真实MC/TH，按10个功能的适用用例独立复验；记录VM/沙箱身份、源码/配置/制品哈希、串口与设备身份、MC/TH固件版本、原始双向通信轨迹、逐例结果及未执行项
  - QA报告与INTEGRATOR的集成矩阵及原始证据分别保存，并明确两次运行绑定的候选一致；任一环境或候选不一致时标记BLOCKED/INCONCLUSIVE并交COORD处理
  negative_cases:
  - 严禁采用全系统一次性总装黑盒测试替代单功能垂直穿透
  - 严禁忽略任何功能的无 ACK 超时与断线测试
  - 严禁以INTEGRATOR的HIL运行结果、日志或签署替代独立QA在其隔离环境中的重新构建、部署和真实硬件复验
required_evidence_level: hardware-verified
verification_environment: independent-vmware-and-server-sandbox-with-real-mc-th-hil
qa_review_policy: project-control/.agents/rules/codex_qa_review.md
updated: '2026-11-02T09:12:00+08:00'
---

# TWIN-42 多模块系统集成阶段单功能穿透梳理与级联验证

## 1. 任务背景与目标
针对传统“多模块一次性集成导致故障原因互相掩盖”的弊端，由 INTEGRATOR 依据 `TWIN-41` 架构时序规范，在真实环境（VMware Twin / SoC 台架）实施**按“单功能”逐个穿透梳理与级联集成验证**：
1. **一个功能一个功能地梳理验证**：
   - 不再将所有子服务混在一起一把抓，而是按 Feature 切片依次验证；
   - 依次穿透：遥测心跳 -> Jog轴动 -> 归零 -> 调平 -> 打印流控 -> 混色 -> E-STOP -> HMS告警 -> OOBE -> mDNS。
2. **四维立体测试判据（每个功能必须经历 4 关）**：
   - 关卡 1【正向闭环】：Web 操作 -> 下行到 MCU -> 真实执行 -> ACK 逐级回传 -> 前端状态更新；
   - 关卡 2【无 ACK 拦截】：模拟 MCU 丢 ACK，验证系统是否准确在超时窗口内阻断，并向前端抛出带 `Sequence ID` 的错误弹窗；
   - 关卡 3【物理热插拔破坏性测试】：在该功能执行期间拔除物理串口，验证 CPU 保持平稳（$\le 2\%$），系统在 3s 内衰退至 `OFFLINE`，前端锁定按钮；
   - 关卡 4【自愈与断点恢复】：插回串口后，系统能否正确重新握手，作业是否保持 `PAUSED` 可继续状态。

## 2. 交付成果
- 交付文档：[`project-control/docs/evidence/twin/TWIN-42/runs/author_01/feature_by_feature_penetration_matrix.md`](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/evidence/twin/TWIN-42/runs/author_01/feature_by_feature_penetration_matrix.md)
- INTEGRATOR 交付每个功能的集成穿透记录、原始通信/日志物证与复现步骤；QA 在独立 run 中交付自己的复验报告和环境证据。两类记录分别绑定准确候选，不把作者证据写成 QA 结果。

## 3. 独立 QA 环境准备与真实 HIL 复验

1. **INTEGRATOR 提供可复现输入**：交付服务器候选及各仓完整 commit、构建/部署步骤、配置与制品哈希、MC/TH 固件身份、串口映射、逐功能操作步骤和预期结果，并保留自身集成运行证据。INTEGRATOR 不代替 QA 创建或签署 QA 结果。
2. **QA 独立搭建软件验证环境**：由未参与本卡实现的独立 Codex 会话，从服务器重新获取同一锁定候选，在独立隔离环境中重新构建和部署 SoC 服务。记录实际 VM/容器身份、镜像或快照、挂载与权限、构建依赖和命令、配置及制品哈希。不得挂载作者可写工作区或拷贝作者构建产物充当独立构建。
3. **QA 独立执行真实 MC/TH HIL**：COORD 预先安排 QA 可独占的真实台架/串口时段，记录设备身份、MC/TH 固件版本和 USB 串口路径。QA 从自己的部署发起测试，独立采集双向原始帧、时间戳、CPU/状态/UI 响应及逐例结果；PTY/Mock 只可用于对应软件用例，不能替代真实 MC/TH 正向闭环和物理拔线/恢复用例。
4. **物理资源排他与安全边界**：同一台架、UART、探针同一时刻只由一名操作者占用；INTEGRATOR 与 QA 分时运行，不共享活动中的串口会话。拔线、复位及其他物理测试须符合已批准的硬件操作窗口和安全规则；本卡不授权烧录固件或启用加热输出。
5. **独立判定与阻塞处理**：QA 报告逐项区分通过、失败、未覆盖、未执行，并将独立运行的候选与 INTEGRATOR 候选对账。缺服务器候选、隔离证据、硬件时段或真实设备时，记录 BLOCKED/INCONCLUSIVE 及解除条件，不以作者的 HIL 证据代签独立通过。
