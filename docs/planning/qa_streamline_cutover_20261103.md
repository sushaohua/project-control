---
id: QA-SIMPLIFY-20261103
revision: 1
status: publication-authorized-awaiting-legacy-qa
date: 2026-11-03
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

本专项提交/推送已获授权，交付操作继续由 INTEGRATOR 执行。分别在根仓与管理仓 `main` 形成有界候选；服务器核对准确提交，按本次 legacy 门禁接受，再登记生效版本与恢复条件。正式服务器沙箱 QA、独立 Codex 与报告非作者复核尚未完成；保持停机，不得将本记录的作者检查当作 Done 或恢复许可。
