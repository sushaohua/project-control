---
id: TWIN-21
title: TWIN-21 MC固件0x16坐标查询与运动指令响应
revision: 1
plan_revision: vmware-soc-twin-20261029
task_kind: implementation
development_stage: vmware-twin
dispatchable: true
status: InProgress
blocked: false
planning_status: planned
owner: session-eng-mc-twin-21
proposed_owner: ENG-MC
executor:
  role: ENG-MC
  agent_id: session-eng-mc-twin-21
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
    planned_session_alias: planned-qa-twin-21
    session: session-qa-twin-21
    session_evidence: null
    decision: null
    reviewed_task_revision: null
    artifact_version: null
    evidence: null
    report_sha256: null
  - role: ARCH
    platform: codex
    model: gpt-6-luna
    planned_session_alias: planned-arch-twin-21
    session: session-arch-twin-21
    session_evidence: null
    decision: null
    reviewed_task_revision: null
    artifact_version: null
    evidence: null
    report_sha256: null
  verifier_session: null
  integrator_session: null
primary_work_package: TASK-002
related_work_packages: []
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
- mcu-p3
- project-control
write_scope:
  mcu-p3:
  - motion-controller-mcu/project/src/minimc_proto.c
  - motion-controller-mcu/project/inc/minimc_proto.h
  project-control:
  - docs/evidence/twin/TWIN-21/**
allowed_paths:
- mcu-p3/motion-controller-mcu/project/src/minimc_proto.c
- mcu-p3/motion-controller-mcu/project/inc/minimc_proto.h
- project-control/docs/evidence/twin/TWIN-21/**
source_baseline:
  project-control: 638d1ca937f5b106dd26fa30766ad3ebdc3b4552
  soc-ap: 19dd461b1959c170963ebd477aa29c36ea841f63
  mcu-p3: d756a13b3c2a1c47186a07311b2c24fa43431465
  test_harness: 0b7497ba43158841eb3c4af7f16e477b9c30c2c5
base_commit: d756a13b3c2a1c47186a07311b2c24fa43431465
candidate_commit: null
dispatch_binding:
  source_commit: d756a13b3c2a1c47186a07311b2c24fa43431465
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
worktree: mcu-p3
lease:
  owner: session-eng-mc-twin-21
  task_revision: 1
  lease_id: lease-twin-21-run01
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
checkpoint: 开工前绑定；0x16与运动接口自检；准确候选独立检查；收件
execution_contract: project-control/docs/planning/vmware_soc_twin_task_execution_20261029.md
readiness_pending:
- 真实作者、全部必需检查会话、有效租约和隔离worktree/输出待登记
- 开工时重取实际commit/dirty diff及SHA256；前置准确接受版本/证据待绑定
- 验证命令须在已实现入口上具体化并核资源/权限，不运行占位命令
deliverables:
  artifacts:
  - mcu-p3/motion-controller-mcu/project/src/minimc_proto.c
  - mcu-p3/motion-controller-mcu/project/inc/minimc_proto.h
  record: docs/evidence/twin/TWIN-21/runs/<actual-run>/result.md
rollback:
  steps:
  - 仅回退本票候选；保存失败证据和原状态；硬件恢复须按实际SOP及授权执行
handoff:
  receiver_role: COORD
  receiver_session: session-coord-main
  transport: docs
  evidence_location: docs/evidence/twin/TWIN-21
  acknowledgement: null
verification:
  commands:
  - id: check_graph
    cwd: .
    command: PYTHONDONTWRITEBYTECODE=1 python3 project-control/tools/check_task_graph.py
      --workspace .
    expected: 结构无错误；不等于任务/运行/硬件接受
    availability: local
  - id: planned_build_and_acceptance
    cwd: .
    command: Ready前由Owner绑定本票实际构建与正反例运行入口
    expected: 按TWIN-18规范核0x16位置查询响应（20字节载荷微米坐标对账）、点动回零指令转发；遵守c_cpp_coding_standard函数<=50行硬门禁
    availability: planned-not-runnable
  positive_cases:
  - 根据SPEC-MCU-MOTION-LEVELING-FILAMENT-20261029第6.1节，0x16查询返回20字节准确微米坐标pos_x_um/pos_y_um/pos_z_um/pos_e_um与mc_state/homed_mask
  negative_cases:
  - 未就绪/越界/非法帧按独立预期返回NACK 0x04或拒绝；强电加热占空比严禁被修改，恒为0%锁死
required_evidence_level: software-verified
verification_environment: isolated-host-or-document
qa_review_policy: project-control/.agents/rules/codex_qa_review.md
updated: '2026-10-31T09:30:00+08:00'
---

# TWIN-21 MC固件0x16坐标查询与运动指令响应

## 1. 目标与依据

根据用户指令 **U-D03**（选项 A：空跑联调、强电加热 0% 锁死）与 **U-D04**（以固件存量为主要参考、采用 5×5 双线性调平存量），本任务由运控固件工程师 `ENG-MC` 承接，负责在 MC 主控固件（AT32F435VGT7）中落实首版运动学坐标读取与点动/回零指令响应。

参考基线规范：
- [SPEC-MCU-MOTION-LEVELING-FILAMENT-20261029.md](../../../../docs/specs/mcu_motion_leveling_filament_interface_survey_20261029.md) 第 6.1 节
- 编码标准硬性门禁：自研新增/重构函数严格 $\le 50$ 行、参数 $\le 4$ 个，零动态堆内存分配，防御性空指针校验

## 2. 交付范围

1. **`0x16` 位置查询报文响应 (`CMD_POS_QUERY`)**：
   - 在 `mcu-p3/motion-controller-mcu/project/src/minimc_proto.c` 中扩展 `handle_mc_query()`；
   - 增加 `build_pos_resp(seq, resp, &resp_len)` 静态辅助函数（$\le 50$ 行）；
   - 从 Marlin 全局变量 `current_position[X_AXIS]`, `current_position[Y_AXIS]`, `current_position[Z_AXIS]`, `current_position[A_AXIS]` 提取毫米坐标，乘以 1000 转换为 32 位整型微米（`um`）；
   - 打包固定 20 字节 `minimc_pos_report_payload_t` 载荷（`pos_x_um`, `pos_y_um`, `pos_z_um`, `pos_e_um`, `mc_state`, `homed_mask`, `reserved`）；
   - 组装 34 字节合法 MiniMCProto v2.0 帧并通过 `minimc_proto_send()` 发送回 AP。
2. **点动/回零指令接入验证**：
   - 针对手动点动（相对移动）与回零（`G28`）请求进行指令接入校验；
   - 确保强电加热硬件锁死恒为 0%（`thermistor_safety_lock`），不得擅自开启发热丝 PWM。

## 3. 验收标准

- **自检通过**：在独立 Docker 容器沙箱内完成固件编译并生成 `Marlin_AT32.bin` / `Marlin_AT32.elf`；
- **独立 QA**：在独立容器沙箱内执行 `0x16` 协议帧编解码测试（正例：验证返回的微米数据与设定浮点坐标误差 $\le 1\text{ um}$；反例：长度不足或非法命令返回 NACK `0x04`），由独立 Codex QA（`platform: codex`, `model: gpt-6-luna`）审签；
- **非作者复核**：由非作者 ARCH 席位出具复核报告并通过。
