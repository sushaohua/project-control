---
task_id: AUTO-03
task_revision: 1
reviewer_role: QA
actual_session: "01a1a048-0ecd-7660-9ecc-93d1432c3b16"
reviewed_artifact_version: abc0b497d1d56c8e9fbbf65df5ae6abde2ee87c6
decision: REJECTED
server_qa:
  path: project-control/docs/evidence/coord_automation/AUTO-03/runs/run_03/server_qa.json
  sha256: 64276b5aab500f34975422d590bde65eb0f839bc476273b70b1019e92ee6957f
reviewed_artifacts:
  - path: project-control/tools/coord_runner/work_intake.py
    sha256: 531c71020a3c7a4437820396c3693b319de0bf235db18d6ce9700fe5e1352549
  - path: project-control/tools/coord_runner/approval_guard.py
    sha256: 6e709eab82285df50c133e1c7df6610ea5bf4e135a186a542fbcbfe406af4d61
  - path: project-control/tools/coord_runner/role_adapter.py
    sha256: a6c051bdc1916e68b351d87eae30f96a77881f553e8b1d43f33bdac70fe98e1e
  - path: project-control/tools/coord_runner/cas_writer.py
    sha256: 438a9aa3668491aaa5b01c0121c51647b7ef9f602710dad48501f22a4f5dff66
  - path: project-control/tools/coord_runner/runner.py
    sha256: 6aa94148750d1a79003f2d9fe4de73c077e54720a5ca0582a2a99767038cd06c
  - path: project-control/tools/coord_runner/scheduler.py
    sha256: d8a58bb957110d84fb47c5ceb50dbcfc11985d63efb3336ff09dfa715c6a36a4
  - path: project-control/config/coord_runner/coord_config.yaml
    sha256: 59a51cd659b1ec64f6dc175b9555e571e7116fea973394cd936fdba8137d62ad
  - path: project-control/tools/test_work_intake.py
    sha256: 52123dee64114e533a86b571e27d912f8b601bec33a77e85ac72e5fcf76dc28b
  - path: project-control/tools/test_coord_runner.py
    sha256: 2cbe58169913e1efc6dd77b35e80f5dfb03c47ca3c884be49d6d2130fe3a8e19
  - path: project-control/docs/evidence/coord_automation/AUTO-03/runs/run_01/result.md
    sha256: 006fdc88f648cf67cb1391d2a1634699f18e6dde627105d6a34382e9df1ac436
content_audit:
  fact_sources:
    result: passed
    basis: 已核对 rev 2 确认单、APPR-20261103-001、rev 2 设计与交接单；确认单 SHA256 为 63c1225d60c377a662bebaa0328f9bc95c19daccaa61d9f2766bc989f06f3f98，批准记录绑定准确确认单版本。
  protocol_compatibility:
    result: not-applicable
    basis: AUTO-03 M1 是 project-control 收件和调度软件范围，不改变外部设备协议或固件字段。
  claim_scope:
    result: failed
    basis: 候选相对基线的 64 项差异中有 12 项不在 AUTO-03 卡片 allowed_paths/write_scope 白名单内，违反任务范围门禁。
  architecture_completeness:
    result: passed
    basis: 已核对 M1 所要求的收件、审批、角色适配、CAS、调度及配置模块；live drill 展示 feature 派发、requirement 澄清及实际角色作业闭环。

# AUTO-03 run_03 独立 QA 审查报告

## 结论

**REJECTED。** 候选版本 `abc0b497d1d56c8e9fbbf65df5ae6abde2ee87c6` 的服务器沙箱检查通过，所审 M1 代码和测试提供了多项符合要求的证据；但差异包含 12 个不在 AUTO-03 精确白名单内的路径，构成授权范围缺陷，不能接受该候选。

## 候选与证据绑定

- 服务器锁定记录将 `project-control` 绑定到完整提交 `abc0b497d1d56c8e9fbbf65df5ae6abde2ee87c6`；checkout 日志记录从服务器 fetch 并检出该提交。
- `server_qa.json` SHA256 与指定值一致。其容器 ID 为 `0cd68c3b582c17e3609bd3012b9a3b927b124ca8efbbc1c13a3f407c0938e046`，镜像 digest 为 `sha256:acbab225932c3877fff37f4d9e5a21235e099182c198e4f4034064ea80cf544f`；源码挂载为只读且无 developer mounts。
- 五项服务器检查均记录 exit code `0`：任务图检查、`test_work_intake.py`、`test_coord_runner.py`、QA runner 与 delivery checks 回归、AST 规范检查。runtime log 中测试通过记录与 `server_qa.json` 一致。
- 容器最终状态 `ExitCode 137` 对应 PID 1 `sleep 3600` 被 `docker stop -t 2` 清理；不影响已记录的五项 `docker exec` 检查结果。
- 会话标识为 `01a1a048-0ecd-7660-9ecc-93d1432c3b16`；run_03 会话记录位于 `project-control/docs/evidence/coord_automation/AUTO-03/runs/run_03/codex_session.jsonl`，SHA256 为 `746ff7f005efd3111fbf6e0ea90d9b1324cab5cb49582b9227948bc77c2b0958`。

## 范围与 M1 条款核对

**范围门禁失败（决定性发现）。** 对比指定基线 `b4af2d32601a07d448ac8d67a07c57f5b9ab36ac` 与候选，64 个变化路径中 12 个不匹配任务卡的 `allowed_paths`：

- `.agents/kanban/microtasks/coord_automation/AUTO-03.md`
- `.agents/kanban/microtasks/coord_automation/AUTO-04.md`
- `.agents/kanban/microtasks/coord_automation/AUTO-05.md`
- `.agents/kanban/microtasks/coord_automation/AUTO-06.md`
- `docs/architecture/coord_intake_dispatch_phase1_design_20261103.md`
- `docs/evidence/coord_automation/phase1_prep_20261103/coord_prep_receipt_20261103.md`
- `docs/evidence/coord_automation/phase1_prep_20261103/integrator_host_interface_verification_20261103.md`
- `docs/evidence/coord_automation/phase1_prep_20261103/pm_demand_understanding_20261103.md`
- `docs/evidence/coord_automation/phase1_prep_20261103/raw_submission_20261103_01.md`
- `docs/planning/coord_intake_dispatch_phase1_confirmation_20261103.md`
- `docs/planning/coord_intake_dispatch_phase1_handoff_20261103.md`
- `docs/planning/work_packages/TASK-010_验收首个多 Agent 端到端试点.md`

这些路径不在 AUTO-03 卡片列出的 `tools/coord_runner/**`、`config/coord_runner/**`、指定工具/测试文件、`docs/work_intake/**` 或本票 evidence 范围内。超范围变化包括其他 AUTO 任务卡和规划/架构材料。即使这些文件属于 `project-control` 仓库，仍违反本票路径白名单。

其余范围检查：差异中未发现 `soc-ap`、`mcu-p3`、`test_harness` 或双 Bootloader 路径；legacy `coord_autorun_queue_20261029.yaml` 在基线与候选的 SHA256 相同（`819fed4f9ca02149f2eafbc29bd27e76960d0075a25b3406ff76cb60be6d0ec1`）；未发现安装 systemd 服务的证据，符合 M1 与 M3 的阶段边界。

具体 M1 条款证据：

- **P1-01、P1-06：**`test_work_intake.py` 包含批量 MD 到唯一三类 YAML/关联的正例，以及同 revision 篡改、损坏输入隔离测试。`work_intake.py` 保留逐条指令原文和公共约束摘要，并将扫描错误隔离。
- **P1-02、P1-04、P1-17：**测试覆盖 requirement 的 PM/ARCH 澄清、issue 未知根因只读调查与已知 Owner 路由，以及单需求多角色拆分。`role_adapter.py` 对应区分 read-only 与 workspace-write 路径。
- **P1-03、P1-18、P1-19：**审批测试覆盖部分批次/仅确认需求的分流，并拒绝伪造操作者、过期 revision、摘要不匹配及自然语言“批准”字样。已核对确认单 rev 2、批准记录及设计/交接版本哈希。
- **P1-16：**测试覆盖禁用或删除入口时保留在途任务，并阻止 shell 文本及越界仓库路径执行。
- **P1-11、P1-12：**runner 测试覆盖无候选/无证据、未推送候选、缺失或不匹配报告/复核及子 Agent 冒充独立 Codex 等拒收情形；这些负例均在服务器日志中通过。
- **P1-15：**run_01 `drill_summary.json` 记录真实 COORD 与 INTEGRATOR Codex 线程、模型、token 数、作业查询完成状态、交付路径和摘要；feature 实际派发、requirement 保持只读澄清，第二次 COORD 调用为无模型调用的 `NOOP`。演练没有自动写 `Done`。
- **真实执行器与 CAS：**`role_adapter.py` 配置真实 Codex CLI 路径及 `gpt-6-luna`，`cas_writer.py` 以磁盘字节 SHA256 做 CAS；对应测试覆盖内容变化冲突和文件保护。

上述代码与 M1 测试证据支持功能条款，但不消除候选差异的白名单问题。

## AST 代码规范

独立解析 `project-control/tools/coord_runner/*.py` 与 `project-control/tools/test_work_intake.py`：共 230 个函数，0 项违反 `≤50` 行、`≤4` 参数；最长函数 46 行，最大参数数为 4。服务器 AST 检查也记录通过。

## 最终判定

**REJECTED：**AUTO-03 run_03 的候选因 12 项超出 `allowed_paths` 的变化未通过范围门禁。服务器沙箱、M1 正负测试、live drill 与 AST 检查均有通过记录，但本报告不将这些通过结果扩展为整张卡的接受结论。