---
id: QA-SIMPLIFY-20261103
revision: 2
status: coord-received-effective
date: 2026-11-03
received_at: 2026-11-04T09:05:00+08:00
coord_receiver_session: ff2fb105-fd84-4ecb-b1e6-8f8eb00badc6
effective_policy: streamlined-v1
effective_source_candidate: cec9b34f8284f7b2580a7d219536d32b7b1ee849
effective_root_candidate: e5b7ec6d80259976b8a38e4164b5596311fed15f
qa_policy: legacy
---

# QA 流程简化与停机切换记录

## 来源与范围

本轮承接 [助理交接](../handoff/CODEX_ASSISTANT_HANDOFF_20261103.md) §5、§8 的简化范围。用户在确认下一步为流程简化后回复“已经停机了。确认。”，作为本轮切换窗口确认；不再启动原 COORD 或后台服务。

本轮只处理 `project-control` 中的 QA 策略、Runner、收件检查器、模板与当前流程文档，并同步根入口规则。业务仓、Bootloader、固件部署和物理台架均不在范围内。用户随后明确“授权提交推送根仓以及本次补丁”，并要求直接使用根仓；本轮沿用根仓与管理仓各自当前 `main`，分别提交推送，不新建专项分支。

开工时 `project-control` 为 `main`，HEAD `9f1ad485751118112fa077743fcc6acfb5857bc1`，工作树干净；根仓和三个业务仓工作树干净。Boot 两仓的未跟踪本机规则链接保留。实际本轮作者代理为 `/root/qa_policy_code`（INTEGRATOR）及 `/root/qa_policy_docs`（流程文档），交付入口为本助理会话。这些是实际工具返回的任务路径，不冒充独立 Codex QA 会话 UUID。

## 预期行为

- 新任务模板和角色派单提示词要求新卡写入 `qa_policy: streamlined-v1`；普通任务默认一个独立 QA，检查代码和功能/必要回归。现有 intake 只生成需求分类记录与任务关联，不是自动任务卡生成器，本次不新增该能力。
- QA 作者交付的测试工具、夹具与独立预期由非作者独立检查，默认 ARCH；不因此递归审阅每份结果报告。
- 特殊协议、跨模块契约、升级/硬件安全变更在开工时明确追加岗位；明确列出的必需岗位不能因简化自动删除。
- 同一准确候选的有效沙箱事实供审阅复用，不为重复岗位重跑相同 Docker 测试；来源、命令、配置、预期或候选变化必须重新验证影响范围。
- 不带标记的旧任务保持 legacy；未知策略必须拒绝。作者分离、候选/报告哈希、正常/异常/恢复、真实 HIL 和必要 Owner 接受继续有效。

## 验证与本次变更的接受

作者对共享策略、Runner、state machine、delivery checker、task graph 执行相关正反例自检。必需覆盖：标准单轮通过；显式额外岗位缺失拒绝；QA 作者自批拒绝；未知策略拒绝；错误候选/篡改报告拒绝；legacy 仍要求旧报告复核；带新标记的任务实际进入新策略。

本次流程变更自身使用 legacy，不能用刚修改的规则自批。正式接受仍须先锁定并发布准确候选，再由旧版受控 Python Runner 从服务器获取候选执行独立 Docker 测试，之后启动独立 Codex 只读审阅同一候选与证据，并取得非作者报告复核。未完成这条链时，本记录不表示正式 QA 通过或允许恢复调度。

## 未完成任务迁移

| 对象 | 本轮处理 | 恢复时条件 |
| --- | --- | --- |
| AUTO-03～06 Done 及历史报告 | 原样保留 | 不追溯改签署或重开已接受任务 |
| TWIN-36～40 Review | 保留 legacy、原 revision、候选和必需 QA/ARCH | 先收件原候选；需要切换时逐卡修订策略、复用证据适用范围及接受岗位，不能直接删 Reviewer |
| 其他未完成任务、superseded 历史票 | 无标记仍 legacy，本轮不批改 | 重新派单时先核实实际输入、Owner 和是否迁移 |
| Debug、VMware/AP↔MC 921600 新需求 | 本轮不实施业务 | 收件查重、概要接受后按新模板拆票 |

这是逐类衔接记录，不是批量迁移完成证明。恢复前由现有 COORD 按实际待派卡确认策略；不得将静态检查通过当作停机/服务运行/正式 QA 证据。

## 当前检查点

本地候选已实现共享策略、Runner/状态机/收件检查联动，以及真实 runtime 报告的交付物哈希与静态收件兼容；根 AGENTS 和九份对应规则镜像已同步。旧任务卡、Done 与原始报告未改。

作者自检八套合计 196 项全部 exit 0：review policy 7、delivery 25、pipeline 24、runner 74、graph 12、recovery 19、phase1 acceptance 20、systemd 15。这些都是作者检查，不是独立 QA。完整命令、cwd、退出码与原始日志哈希见 [作者自检记录](../evidence/qa_streamline_20261103/author/run_01/self_check_results.json)。最终小修后定向补跑 policy 7 与 pipeline 24 项全部 exit 0，见 [补跑记录](../evidence/qa_streamline_20261103/author/run_01/final_checks.json)，不覆盖八套原记录。作者登记新增/修改函数的规模与参数违规为 0，差异空白检查通过；准确源码哈希及结果引用见 [源码清单](../evidence/qa_streamline_20261103/author/run_01/source_manifest.json)。

根入口完整候选、补丁与规则镜像哈希见 [文档作者快照](../evidence/qa_streamline_20261103/docs/run_01/README.md)。根镜像本机一致不表示已远程发布。

本专项已按授权由 INTEGRATOR 分别在根仓与管理仓 `main` 发布，并完成独立服务器 fetch 核对。下列独立 QA 已批准准确候选；本助理只整理交付资料，正式收件仍待现有 COORD，调度继续保持停机。

## 发布、独立 QA 与待收件入口

- 管理仓源码候选：`cec9b34f8284f7b2580a7d219536d32b7b1ee849`，服务器 `ssh://git@192.168.77.113:2222/sushaohua/project-control.git`，ref `refs/heads/main`。
- 根仓候选：`e5b7ec6d80259976b8a38e4164b5596311fed15f`，服务器 `ssh://git@192.168.77.113:2222/sushaohua/ai-soc-workspace.git`，ref `refs/heads/main`；`workspace.json` 的管理仓恢复锁为上述源码候选，其他仓锁未改。
- 可信执行器来自服务器独立取得的旧基线 `9f1ad485751118112fa077743fcc6acfb5857bc1`，未用新流程自批。`qa_02` 和 `report_review_02` 分别从服务器获取同一组五仓准确提交，使用两个独立 Docker 沙箱，各执行八套 **196 项测试**及根 AGENTS、恢复锁、九份源码 SHA256 核对，九条命令全部 exit 0；这是客观运行结果，独立结论另见下列报告。

| 检查 | 实际独立 Codex 会话 | 结论与证据 |
| --- | --- | --- |
| 主 QA，代码与客观运行证据 | `01a1a1bf-39cd-74a0-a864-16d4f33b6d1c` | APPROVED；[原始报告](../evidence/qa_streamline_20261103/runs/qa_02/reviews/567487c89275475896c1b76474b1aac6/review_report.md)，SHA256 `6b0a1568b8819f60cd99f3a20aa72626a9a39d9517905f29239b2b0edc27a297` |
| ARCH，非作者复核主报告与独立沙箱证据 | `01a1a1c1-8534-7dc1-9a21-612aa61b85d6` | APPROVED；[原始报告](../evidence/qa_streamline_20261103/runs/report_review_02/reviews/495ba427603b44a7be622474f69290f7/review_report.md)，SHA256 `fab8ddea4364814de81dc6f4836423e6abde1e353e804fd09603b1df7cc2f8cc`；独立重算并绑定前述主报告 SHA256 |

两会话均为实际新启动、只读、`gpt-6-luna` 审阅，未 fork/resume 作者会话。两轮客观证据、容器身份、原始审阅 JSONL/final/schema/prompt、报告及条目已原文归档。首次执行的路径门禁拦截和首次主审输出协议拒收均保留，后者记录为 INCONCLUSIVE，不作为源码返修或有效接受。

批准范围为本次 QA 策略、Runner/收件检查器、模板及当前流程文档。业务构建、真实 HIL、固件部署和常驻服务恢复不适用，不能据本次批准宣称已执行。

**现有 COORD 的收件入口：**[机器核对交付清单](../evidence/qa_streamline_20261103/handoff_manifest.json)。该清单只核对准确候选、旧执行器、两轮证据、会话差异与报告字节，不新增自签 QA。本助理不代替原 COORD 签署收件、不改任何旧任务 Done、不启动服务。现有 COORD 须按上述确切版本收件并登记采用范围后，才可对新任务使用 `streamlined-v1`；未完成旧票仍按本文迁移表处理。

后续证据/本记录作为独立元数据提交发布；受审源码候选始终为 `cec9b34f8284f7b2580a7d219536d32b7b1ee849`，根仓仍为 `e5b7ec6d80259976b8a38e4164b5596311fed15f`，不因证据归档递归换版或再次修改恢复锁。

## COORD 正式收件与生效版本登记（2026-11-04）

- **接管与收件会话**：`ff2fb105-fd84-4ecb-b1e6-8f8eb00badc6`（原 COORD 会话 `8d4e8b77-42a9-4bd3-bd5a-1b881e8d4bd5` 经人工确认停机；核查后台任务、Docker 容器、`coord_runner.lock` 及 SQLite `in_flight_tasks`/`leases`/`role_jobs` 均为 0 活跃占用）。
- **准确候选与归档证据核验**：
  - 管理仓源码候选：`cec9b34f8284f7b2580a7d219536d32b7b1ee849`（9 份受审源码 SHA256 与当前工作树 100% 一致）
  - 根仓候选：`e5b7ec6d80259976b8a38e4164b5596311fed15f`（根 `AGENTS.md` 与 9 份规则镜像 SHA256 100% 一致，`workspace.json` 恢复锁匹配）
  - 独立 QA 与交接证据归档提交：`613f3cbc9a58283ff085cee241de9810895cfdb4`（`handoff_manifest.json` 所列 114 份归档文件 SHA256 逐一校验 0 偏差；当前管理仓 HEAD `5964606826b604da81593ab13d0adecdb7728dc3` 完好保留，不回退）
  - 独立 Codex 主审（`qa_02`，会话 `01a1a1bf-39cd-74a0-a864-16d4f33b6d1c`，容器 `58144a07c319`，196 项测试通过，结论 `APPROVED`）与非作者 ARCH 报告复核（`report_review_02`，会话 `01a1a1c1-8534-7dc1-9a21-612aa61b85d6`，容器 `d5e9523472d7`，196 项测试通过，结论 `APPROVED`）均已核实并直接复用有效证据，不重复执行整轮 Docker 验收。
- **新流程正式生效版本与适用边界**：
  - 生效策略标识：`qa_policy: streamlined-v1`
  - 生效基准版本：`project-control@cec9b34f8284f7b2580a7d219536d32b7b1ee849` + `ai-soc-workspace@e5b7ec6d80259976b8a38e4164b5596311fed15f`
  - 标准主链：`作者实现与自检 → 锁定候选 → 一轮独立 QA（代码审查 + 功能/必要回归测试） → COORD 收件`
  - 存量与特殊门禁：新任务显式写入 `qa_policy: streamlined-v1`；未迁移旧任务维持 `legacy`（含报告复核要求），按上文迁移表逐卡处理；QA 自产测试资产非作者独立审查、跨模块/协议/安全特殊变更追加审查、Owner 接受及真实 HIL 要求全部保留。
  - 收件回执归档：[coord_receipt_20261104.json](../evidence/qa_streamline_20261103/coord_receipt_20261104.json) 与 [handoff_manifest.json](../evidence/qa_streamline_20261103/handoff_manifest.json)。
