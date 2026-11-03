---
template_version: '2026-10-27'
review_id: AUTO-03-run_01-QA
review_status: completed
reviewer_role: QA
reviewer_roles: [QA]
platform: codex
requested_model: gpt-6-luna
actual_model: gpt-6-luna
model_override_ref: null
reviewer_session: 01a1a004-0d6b-7701-b89c-bd6da9593112
actual_session: 01a1a004-0d6b-7701-b89c-bd6da9593112
author_session: 25b63893-2611-41ff-87d7-0b9f82cf0375
task_id: AUTO-03
task_revision: 1
run_id: run_01
decision: BLOCKED
reviewed_artifact_version: "project-control=abc0b497d1d56c8e9fbbf65df5ae6abde2ee87c6; soc-ap=427dd6d82caceebb7b4642e78f1dbfa96ff5fc84; mcu-p3=e051111e68dd61896ed42c0961153b167b8bca41; test_harness=ccf1476a0b98cb55ca9ee7bd49d73ca5d4704414"
candidate:
  path: project-control/docs/evidence/coord_automation/AUTO-03/runs/run_01/result.md
  sha256: 006fdc88f648cf67cb1391d2a1634699f18e6dde627105d6a34382e9df1ac436
reviewed_artifacts:
  - path: project-control/docs/evidence/coord_automation/AUTO-03/runs/run_01/result.md
    sha256: 006fdc88f648cf67cb1391d2a1634699f18e6dde627105d6a34382e9df1ac436
  - path: project-control/docs/evidence/coord_automation/AUTO-03/runs/run_01/server_qa.json
    sha256: 0aef8affeeeb660ceb416c79ba702500f89ebca48206159784d2aa695583924e
  - path: project-control/docs/evidence/coord_automation/AUTO-03/runs/run_01/live_drill/drill_summary.json
    sha256: cab642ada34ff4cd5484924059ccad011d2578dac8ebb6404f1b9c70f6376e97
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
server_qa:
  path: project-control/docs/evidence/coord_automation/AUTO-03/runs/run_01/server_qa.json
  sha256: 0aef8affeeeb660ceb416c79ba702500f89ebca48206159784d2aa695583924e
  container_id: 1e87e41bfe1475a69dc30f2d8edbfe83982acc240f4b5a636716c3a45972d3c2
  image_digest: sha256:acbab225932c3877fff37f4d9e5a21235e099182c198e4f4034064ea80cf544f
reviewer_session_evidence:
  path: project-control/docs/evidence/coord_automation/AUTO-03/runs/run_01/codex_session.jsonl
  session_id: 01a1a004-0d6b-7701-b89c-bd6da9593112
content_audit:
  fact_sources:
    result: passed
    basis: "快照中的任务卡、确认单 rev 2、批准记录、result.md、演练摘要和列明源码均已读取；可复算交付物哈希与 result.md 清单一致。"
  protocol_compatibility:
    result: passed
    basis: "本任务为 M1 收件和调度工具，未涉及设备协议或 HIL；按任务范围不适用。"
  claim_scope:
    result: passed
    basis: "审查结论限定于 M1 候选与现有归档记录；未将静态检查或候选自述视为本次独立运行证据。"
  architecture_completeness:
    result: passed
    basis: "检查了收件、批准校验、角色适配、CAS 写入、运行器、调度器、状态机与 M1 演练入口；任务卡映射的十二场景均有实现/测试入口。"

# QA 审查报告

## 决定

**BLOCKED（证据核验受阻，暂不能批准或拒绝功能实现）**。

当前会话为 `01a1a004-0d6b-7701-b89c-bd6da9593112`，与作者会话 `25b63893-2611-41ff-87d7-0b9f82cf0375` 和 COORD 会话 `8d4e8b77-42a9-4bd3-bd5a-1b881e8d4bd5` 不同。候选哈希与交付清单吻合；但远端提交核验和 Docker 容器独立 inspect 均因权限/网络不可用而未完成，且审查会话运行记录未在快照中找到。按 QA 规则，来源与会话物证不足时不能签发 `APPROVED`。

## 候选、会话、容器与证据核验

- `CODEX_THREAD_ID`：`01a1a004-0d6b-7701-b89c-bd6da9593112`，与作者、COORD 会话不同。
- 本地快照提交核验通过：`project-control=abc0b497d1d56c8e9fbbf65df5ae6abde2ee87c6`、`soc-ap=427dd6d82caceebb7b4642e78f1dbfa96ff5fc84`、`mcu-p3=e051111e68dd61896ed42c0961153b167b8bca41`、`test_harness=ccf1476a0b98cb55ca9ee7bd49d73ca5d4704414`。
- `git ls-remote origin refs/heads/main` 未能连接到远端 SSH 服务（`192.168.77.113:2222`），所以远端 main 与锁定提交的相等关系未能独立确认。
- `server_qa.json` 记录了完整容器 ID `1e87e41bfe1475a69dc30f2d8edbfe83982acc240f4b5a636716c3a45972d3c2`、镜像摘要 `sha256:acbab225932c3877fff37f4d9e5a21235e099182c198e4f4034064ea80cf544f`、退出状态、`/workspace` 只读挂载及空 `developer_mounts`。但当前 Docker daemon 拒绝 inspect 请求，以上容器属性只能与归档记录核对，不能由本次 inspect 独立复验。
- 归档 `server_lock.json`、`checkout.log`、`runtime.log`、`server_verdict.json` 的 SHA256 分别为 `98ad35b38088630fa8870168342908a5492946f790f9695677430702480d1006`、`de0b1cbab9d49ea78a8b9a8b2d8f6edc735667cf43e1a827d670f1efcdfb72a2`、`05a537513abccc04f85df2ed752963a177f3cf8af45e61509844d1be0df7ec53`、`5b6aca8fd21b5b67f7614618c53799697374956a3a2a8d427c99b0bc2252e6d3`；`server_qa.json` SHA256 为 `0aef8affeeeb660ceb416c79ba702500f89ebca48206159784d2aa695583924e`。
- 快照中未发现要求绑定的 `codex_session.jsonl`。因此本报告可记录实际 session ID，但缺少可核验的会话运行事件证据。
- 已重新计算 `result.md`、演练摘要和 9 项 `deliverables.artifacts` 的 SHA256；全部与候选清单一致。具体值见 frontmatter。

## M1 十二项正反例与代码审计结论

审阅了任务卡要求的实现/测试文件及 M1 演练入口。代码结构提供以下场景对应实现和测试入口；容器归档结果声称测试通过，但本次没有在宿主机重跑候选测试。

| 场景 | 审计观察 |
|---|---|
| P1-01 | `work_intake.py` 提供批量解析、稳定 demand 映射和分类记录生成；任务卡列出对应测试及演练。 |
| P1-02 | `role_adapter.py` 路由到 PM/ARCH 只读澄清；任务卡列出路由测试和演练证据。 |
| P1-03 | `approval_guard.py` 绑定批准与确认单版本/哈希；任务卡列出批准校验正反用例。 |
| P1-04 | 角色适配器区分 issue 只读调查与已知根因的 Owner 派发；任务卡列出路由测试。 |
| P1-06 | 收件模块校验同版本摘要、schema、分类及损坏记录；任务卡列出隔离测试。 |
| P1-11 | 回收结果时校验候选提交及交付物；任务卡列出缺项拒收用例。 |
| P1-12 | 校验远端提交、独立 Codex 审核和会话证据；任务卡列出伪造/缺失审核证据拒收用例。远端条件本次无法实测。 |
| P1-15 | 演练摘要记录 `codex exec -m gpt-6-luna` 的真实会话与收件闭环；摘要及事件文件存在于快照。独立复验演练未执行。 |
| P1-16 | 收件生命周期保护与越界写入审计/回滚具有实现和测试入口。 |
| P1-17 | 角色拆分保留 demand 关联；任务卡列出多角色拆分测试。 |
| P1-18 | 批次部分批准及仅确认需求的分流有批准逻辑及正反测试入口。 |
| P1-19 | 批准来源、过期版本、篡改哈希及自然语言触发等拒绝逻辑有测试入口。 |

归档 `server_qa.json` 的 verdict 为 `PASSED`，记录 5 组检查命令退出码为 0；其中候选测试日志报告 `test_work_intake.py` 15 项、`test_coord_runner.py` 74 项通过。该记录支持“容器归档报告测试通过”，但受容器 inspect 与远端核验受阻的限制，本报告不将其表述为已由 QA 独立复跑验证。

## AST 与禁区核查

- 归档 AST 检查输出 `AST violations: []`，覆盖 `tools/coord_runner/*.py` 与 `tools/test_work_intake.py`，符合函数不超过 50 行、参数不超过 4 个的门槛；本次未重跑候选测试/检查命令。
- 快照所审范围限定在 `project-control` 工具、配置、计划和证据文件；锁定提交记录亦列出其他仓库提交。`result.md` 声明未改 `soc-ap`、`mcu-p3`、`test_harness`、`boot/*`，未装 systemd/cron，未生成 QA issue。
- 旧队列隔离由 `scheduler.py` 对 `coord_autorun_queue_20261029.yaml`、`TWIN-*`/`MS-*` 的隔离逻辑及对应测试覆盖。单凭当前只读快照无法验证历史旧队列文件在实施前后是否完全未变；此项按归档记录审阅，不作为独立运行事实确认。

## 未执行项与适用范围限制

- 未能运行 `docker inspect 1e87e41bfe14`：Docker daemon socket 权限拒绝。
- 未能运行远端 `git ls-remote`：远端 SSH 连接失败。
- 未执行候选单元测试、现场演练、构建或额外代码修改；未读取作者可写工作树。
- 未找到 `codex_session.jsonl`，无法独立验证本审查会话的 rollout/事件记录及实际模型物证。
- 本结论只针对 AUTO-03 revision 1 的 M1 软件范围；不是 HIL、物理硬件或 M2/M3 验收。需补齐可访问的远端/容器核验证据和 reviewer session 记录后，针对准确候选另行复审。