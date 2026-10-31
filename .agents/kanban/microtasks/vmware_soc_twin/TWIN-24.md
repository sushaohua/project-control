---
id: TWIN-24
title: TWIN-24 MC固件5×5调平网格导出(0x18)响应实现
revision: 1
plan_revision: vmware-soc-twin-20261029
task_kind: implementation
development_stage: vmware-twin
dispatchable: true
status: Backlog
blocked: false
planning_status: planned
owner: null
proposed_owner: ENG-MC
executor:
  role: ENG-MC
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
    planned_session_alias: planned-qa-twin-24
    session: null
    session_evidence: null
    decision: null
    reviewed_task_revision: null
    artifact_version: null
    evidence: null
    report_sha256: null
  - role: ARCH
    platform: codex
    model: gpt-6-luna
    planned_session_alias: planned-arch-twin-24
    session: null
    session_evidence: null
    decision: null
    reviewed_task_revision: null
    artifact_version: null
    evidence: null
    report_sha256: null
  verifier_session: null
  integrator_session: null
primary_work_package: TASK-002
related_work_packages:
- TASK-007
- TASK-008
depends_on:
- TWIN-21
- TWIN-22
dependency_conditions:
- task: TWIN-21
  accepted_version: mcu-p3=abbc3ae240972f5a60d751c6204c8b73f1f464bf
  acceptance_evidence: docs/evidence/twin/TWIN-21/runs/run_01/qa_review_report.md
  required: 开工前继承TWIN-21坐标查询与微米整型对账及强电锁死基线
- task: TWIN-22
  accepted_version: soc-ap=6850cc553d405b5e7e511ff181d985fdee8e221f
  acceptance_evidence: docs/evidence/twin/TWIN-22/runs/run_01/qa_review_report.md
  required: 开工前继承TWIN-22温控换算与哨兵防御治理基线
scope_status: mapped
allowed_repositories:
- mcu-p3
- project-control
write_scope:
  mcu-p3:
  - motion-controller-mcu/project/src/minimc_proto.c
  - motion-controller-mcu/project/inc/minimc_proto.h
  project-control:
  - docs/evidence/twin/TWIN-24/**
allowed_paths:
- mcu-p3/motion-controller-mcu/project/src/minimc_proto.c
- mcu-p3/motion-controller-mcu/project/inc/minimc_proto.h
- project-control/docs/evidence/twin/TWIN-24/**
source_baseline:
  project-control: 2377278cee99fea116f121b2f6add293e7b50121
  soc-ap: 6850cc553d405b5e7e511ff181d985fdee8e221f
  mcu-p3: abbc3ae240972f5a60d751c6204c8b73f1f464bf
  test_harness: 0b7497ba43158841eb3c4af7f16e477b9c30c2c5
base_commit: abbc3ae240972f5a60d751c6204c8b73f1f464bf
candidate_commit: null
dispatch_binding:
  source_commit: abbc3ae240972f5a60d751c6204c8b73f1f464bf
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
checkpoint: 开工前绑定；0x18网格导出与微米整型精度自检；准确候选独立检查；收件
execution_contract: project-control/docs/planning/vmware_soc_twin_task_execution_20261029.md
readiness_pending:
- 真实作者、全部必需检查会话、有效租约和隔离worktree/输出待登记
- 开工时重取实际commit/dirty diff及SHA256；前置准确接受版本/证据待绑定
- 验证命令须在已实现入口上具体化并核资源/权限，不运行占位命令
deliverables:
  artifacts:
  - mcu-p3/motion-controller-mcu/project/src/minimc_proto.c
  - mcu-p3/motion-controller-mcu/project/inc/minimc_proto.h
  record: docs/evidence/twin/TWIN-24/runs/<actual-run>/result.md
rollback:
  steps:
  - 仅回退本票候选；保存失败证据和原状态；硬件恢复须按实际SOP及授权执行
handoff:
  receiver_role: COORD
  receiver_session: session-coord-main
  transport: docs
  evidence_location: docs/evidence/twin/TWIN-24
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
    expected: 按TWIN-18规范核0x18网格查询响应（52字节载荷5×5微米网格对账）；遵守c_cpp_coding_standard函数<=50行硬门禁
    availability: planned-not-runnable
  positive_cases:
  - 依据SPEC-MCU-MOTION-LEVELING-FILAMENT-20261029第6.2节及U-D04裁决，0x18查询返回52字节5×5双线性网格数据，z_offset_um高程整型误差<=1um
  negative_cases:
  - 非法查询长度或异常参数返回NACK 0x04，强电加热占空比恒为0%锁死
required_evidence_level: software-verified
verification_environment: isolated-host-or-document
qa_review_policy: project-control/.agents/rules/codex_qa_review.md
updated: '2026-10-31T10:50:00+08:00'
---

# TWIN-24 MC固件5×5调平网格导出(0x18)响应实现

## 1. 目标与依据

根据系统指令 **U-D04**（“固件存量为 5×5 双线性网格，PM 目标要求 7×7 网格，未达成技术裁决，采用固件存量；当前开发功能以固件存量为主要参考”），本任务落实首版调平特性（`MOT-002`）在 MC 下位机的协议导出闭环：
1. 在 MC 固件中打通 `MINIMC_CMD_LEVEL_GRID_QUERY = 0x18`；
2. 导出存量 `bed_level[5][5]` 高程整型微米数组（52 字节载荷，25 点相对偏差）；
3. 扩展局部响应缓冲区至 128 字节，杜绝 66 字节报文栈溢出隐患；
4. 严格保持强电加热占空比 0% 锁死。

参考基线规范：
- [SPEC-MCU-MOTION-LEVELING-FILAMENT-20261029.md](../../../../docs/specs/mcu_motion_leveling_filament_interface_survey_20261029.md) 第 3.4/6.2 节
- 编码标准硬性门禁：自研新增/重构函数严格 $\le 50$ 行、参数 $\le 4$ 个，零动态堆内存分配，防御性空指针校验
