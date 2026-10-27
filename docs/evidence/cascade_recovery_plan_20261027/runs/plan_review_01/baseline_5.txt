# AP–MC–TH 纠偏：工程流程与工具独立只读核查

核查日期：2026-10-27；工作区：`/home/sushaohua/workspace/ai_soc_project`。本记录供方案作者引用，属于只读技术核查，不是正式任务验收或硬件 APPROVED 签署。已读根 `AGENTS.md` 与 canonical `project-control/.agents/rules/codex_qa_review.md`。未修改工程文件、正式状态、源码或硬件；未联网、推送、烧录。隔离改动仅在 `/tmp`。

## 核查结论与可复核证据

当前正式结构检查实际失败。命令：

```bash
python3 project-control/tools/check_task_graph.py --report /tmp/cascade_task_graph_baseline_20261027.json
```

实际 exit_code=1，canonical_task_count=61，v2_microtask_count=20。错误为 MS-07 frontmatter 语法破损及其造成的三项 missing-reference。原始 JSON：`/tmp/cascade_task_graph_baseline_20261027.json`。

隔离反例：`/tmp/cascade_workflow_repro_20261027.py`，输出：`/tmp/cascade_workflow_repro_20261027.out`。它复制控制文档至 `/tmp/cascade_workflow_fixture_20261027`，业务仓只作为只读路径引用；仅修复副本 MS-07 YAML 引号后，结构检查 errors=[]、任务数62，以下其余漏洞均可独立复现。反例可执行：

```bash
PYTHONDONTWRITEBYTECODE=1 python3 /tmp/cascade_workflow_repro_20261027.py
```

## 1. 当前正式 MS-07 卡的 YAML 已破损，结构检查失效（已证实，P1）

- 位置：`project-control/.agents/kanban/milestones/marlin_ms07_20261007_214108.md:69`。未引用标量 `acknowledgement: COORD accepted MS-07: Genuine ...` 含第二个 `: `，PyYAML 拒绝解析。
- 工具行为：`project-control/tools/check_task_graph.py:224–233` 将坏卡排除，继发 `MS-08/MS-15/TASK-007` 找不到 MS-07。正式 run 的错误不能被历史 PASS 替代。
- 最小修正文件与操作：COORD 给该标量加引号；使用解析/序列化工具更新 frontmatter；将“所有当前卡可解析”纳入每次状态写入后的检查，先验新文本再原子替换。须重跑全图并新留 run，保留原错误证据。

## 2. MCQ 固件卡完全漏扫，通用工具仍硬编码离线 V2 范围（已证实，P0）

- 位置：`project-control/tools/check_task_graph.py:30–37` 只枚举 milestones、minimc_v2/V2-*、TASK-*、PL；漏掉真实 `project-control/.agents/kanban/microtasks/mc_firmware/MCQ-0105.md` 和 `MCQ-0106.md`。`check():243` 又只对 `V2-` 调结构和 readiness 规则。
- 实证：正式与隔离 JSON 的 `card_paths` 均没有任何 MCQ。MCQ-0106 当前 `Done`（卡8行），缺少 V2 所要求的多项结构字段也不被发现。不是推测的新目录风险，而是已经运行的任务未纳入图。
- 其他耦合：工具104–105行一律禁止 `mcu-p3` 写入，155–159行强制 `minimc_v2` evidence 根，无法直接把 MCQ 加入 V2 校验。
- 修改文件与操作：`project-control/tools/check_task_graph.py` 改为有注册表/明确 archive 排除规则的全量任务发现；按 task_kind/evidence_level/schema_version 分型，不按 ID 前缀特判；增加 canonical 任务注册表及覆盖差集检查。修订 `project-control/.agents/kanban/microtasks/mc_firmware/MCQ-0105.md`、`MCQ-0106.md` 补任务契约。增独立负例：新目录有效卡必须被计数，未登记卡不得静默忽略，历史 superseded 不重复派单。

## 3. Review/Verify/Done 缺少接受门禁，已发生作者占用独立评审位及前置未完成关闭（已证实，P0）

- 位置：`project-control/tools/check_task_graph.py:252–256` 只对 V2 的 Ready/InProgress 调用 readiness；Review/Verify/Done 不核对评审、验证、集成、收件或依赖能力。MS/PL 仅检查引用存在、环，根本不走该门禁。
- 正式实证：MS-07 卡13/17/27行作者和 ARCH reviewer_session 同为 `1c634be7-4be2-4743-af02-dc8ada31bad3`；28–30行 decision/artifact_version/evidence 为 null，36行 integrator_session 为 null，但11行 Done。MS-05、MS-06、MS-18 均 Backlog；MS-07 的 V2-P0506 accepted_version/evidence 也为 null（89–91行）。这说明“已填 reviewer ID”尚不能算实际自批通过，但独立位确被作者占用，必需接受结果缺失。
- 隔离实证：只修 MS-07 语法后全图 errors=[]；进一步把副本 V2-P01A 的 reviewer_session 改作者、decision 改 REJECTED、artifact_version 清空、evidence 改不存在路径，Done 仍 errors=[]。
- 修改文件与操作：`project-control/tools/check_task_graph.py` 增按目标状态的验收校验和旧/新状态转换命令，覆盖全部 active 类型；校验 reviewer/verifier/QA 作者复核与 author、session lineage 分离，必需岗位逐项通过，候选及接受报告同版本，收件/集成项符合任务类型；COORD 在 MS-07 原卡追加异常和恢复条件，保留历史 run，安排真正独立 ARCH review 与适用集成接受，不由核查者改状态。涉及 canonical 规则 `04_公共看板与读写协议.md`、`codex_qa_review.md` 和任务模板。

## 4. Ready 只看绑定非空，过期租约、blocked=true、假 commit/hash/接受报告仍可无阻塞（已证实，P1）

- 位置：`project-control/tools/check_task_graph.py:165–195`。179行只判断 base/source/diff 非空，182–185行租约只看字段存在及 owner/revision，相比当前时间不解析 expires_at；不检查 blocked。193行只判断 accepted_version 与 acceptance_evidence 非空，未核对文件、结论、生产者版本、消费映射。
- 隔离实证：V2-P01A 副本使用 `not-a-commit`、`not-a-sha256`、2000年已过期 lease、blocked=true，`readiness_blockers=[]`；V2-P01C 将所有 accepted_version 改 `not-an-accepted-version`、acceptance_evidence 改 `nonexistent-report.md`，亦 `[]`。
- 修改文件与操作：同工具对 revision/ID/哈希格式、git object 存在且类型commit、准确消费清单和接受报告摘要做实际校验；区分历史记录与当前派单，不应因历史Done租约过期否定过去验收，但 Ready/InProgress 必须当前有效；blocked 为硬停止，资源占用冲突需按真实资源键核对。模板和执行指南需定义证据的结构化 schema、哈希域与时区。

## 5. 写范围冲突仅比较字符串，glob 与子路径、禁止项和实际 diff 未校验（已证实，P1）

- 位置：`project-control/tools/check_task_graph.py:100–114` 只规范部分相对路径，`262` 用 set intersection 查重，不解释 `**`；`forbidden_paths`、真实 diff 范围不参与检查。
- 隔离实证：无依赖的 V2-P01A/P01B 分别声明 `project-control/docs/specs/**` 与 `project-control/docs/specs/protocol_selection_20261020.md`，同步保持各自 write_scope/allowed_paths 一致，全图 errors=[]。这两个范围覆盖同一真实文件。
- 修改文件与操作：同工具实现有界白名单和glob包含/交叠判定，解析后留在授权仓根；公开作用域命令在作者交付及COORD收件阶段，将准确base/candidate diff、未跟踪交付与白名单/禁止项核对；资源锁校验不要被“有依赖关系”替代，因为两张关联任务仍可能并发。为目录/文件/符号链接/禁止项交集添加独立负例。

## 6. artifact_check 输出哈希但不对照获批版本，候选缺少完整最终版本绑定（已证实，P1）

- 位置：`project-control/tools/check_task_graph.py:198–218` 只确认交付文件存在/非空并计算当前哈希；候选只检查大字段非空和协议哈希。没有核对 reviewer.artifact_version、报告SHA256、报告结论、repository commit可定位性或产物内容来自该commit。
- 隔离实证：将副本候选 repositories 的三个 commit 改为全0/全1/全2，`artifact_check(V2-P0506)` 的 errors 仍为空。
- 正式现状：`project-control/docs/releases/minimc_v2_offline_candidate.yaml:10–17` 对soc-ap只写 `base_commit:79be851...` 及路径列表，没有最终候选commit或文件哈希，24–25行控制仓commit为当时输入；V2-P0506 卡29行 artifact_version 只绑定候选YAML哈希，无法单凭清单还原最终库源码。历史 QA 报告确实另外记录parser/CMake/YAML哈希（报告97–99行），应保留历史有效范围；当前 CMake 已演进到另一个哈希本身不是缺陷，不能把旧报告借给新组合。
- 修改文件与操作：同工具将presence/hash命令明确与接受命令分离；新候选清单按每仓最终精确commit+每个分发制品SHA256+协议/配置/工具链+测试run/报告SHA256绑定；`project-control/docs/releases/minimc_v2_offline_candidate.yaml` 作为历史候选原件保留，新建纠偏candidate而非覆盖历史；`tools/workspace.py` 的lock/publish继续负责可恢复同步，发布验收候选时额外绑定被接受release descriptor，不能把verify成功当成QA接受。现有workspace.json是最新锁点，不能指称它“过时”。

## 7. 必要 MCU 规则与指南是未版本化外部软链，五仓恢复不能重建同一规则环境（已证实，P1）

- 实体：`mcu-p3/AGENTS.md -> /home/sushaohua/agents/mcu-p3/AGENTS.md`；`mcu-p3/.agents -> /home/sushaohua/agents/mcu-p3/.agents/`；`mcu-p3/docs -> /home/sushaohua/agents/mcu-p3/docs`。
- 位置：`mcu-p3/.gitignore:1–8` 排除这三者；`git -C mcu-p3 ls-files --stage AGENTS.md .agents docs` 无输出，`git check-ignore` 三者均命中。入口 `.gitignore:4` 也排除整个子仓；workspace.json只锁四仓commit，没有这些外部内容的快照/哈希。
- 恢复行为：`tools/workspace.py:269–294` 仅克隆四仓并补根 .agents 链接，没有恢复MCU原有规则/指南；`WORKSPACE.md:89–90` 已说明未跟踪文件不打包，所以不能说当前 bundle 承诺包含这些内容，但“同commit同工程规则”的假设不成立。
- 修改文件与操作：将实际必须规则归入 `project-control/.agents/rules/` / `docs/guides/` 版本化原件，MCU放可追踪的简短本地入口，明确优先级和来源；需要保留外部资料则只引用，不当作运行必需输入。修改 `mcu-p3/.gitignore`、新增受控 `mcu-p3/AGENTS.md`、`tools/workspace.py`（restore/verify检查）、`tools/test_workspace.py`（干净恢复规则一致性）、`WORKSPACE.md` 与workspace清单的规则版本绑定；做隔离恢复演练并由独立会话验收。

## 8. 根规则副本与看板/索引已漂移，恢复仅在不存在时建软链，保留旧目录（已证实，P1）

- 位置：入口 `.gitignore:12` 忽略 `.agents`，当前它是实际目录，非软链。`tools/workspace.py:291–293` 仅在 .agents 不存在时建 canonical链接，旧目录完全保留，也不告警。
- 已有差异：根 `.agents/rules/04_公共看板与读写协议.md:11` 后没有 canonical 同文件13–15行的独立Codex规定，根旧副本还写TH `AT32A423` 而 canonical193行附近已改为 `AT32F423CCT7`。根MS-07范围另含mcu-p3，canonical当前范围没有；不能把两者当同一份任务。
- canonical 内部投影也已漂移：`project-control/.agents/kanban/KANBAN.md:38–49` 仍称25张并将已关闭多数V2显示Backlog，75行MS-14仍引用MCQ-0106进行中而真实卡Done；`microtasks/minimc_v2/README.md:27–36` 链接已移入superseded的V2-P05C～P06C，仍指定V2-P06C为最终候选，而当前是V2-P0506。工具不核对这些投影。`manifest.yaml` 的2026-10-20工程基线不应一概要求追HEAD；问题是当前入口/派单投影没有明确快照语义并指向已失效任务。
- 修改文件与操作：备份旧根目录后由受控入口显式引用canonical，或安全迁移为相对软链，禁止继续双写；`tools/workspace.py` 的verify发现旧根目录有差异即提示修复，restore不得静默掩盖；更新/生成canonical `KANBAN.md`、V2 `README.md`，将计数、有效ID、superseded关系与正式卡注册表核对；根 `HANDOFF_20261027.md` 保留历史时间语义，仅入口指向最新交接索引，不把旧记录覆盖成当前结果。

## 已查但不扩大结论的项目

- `push_to_server.sh`、`project-control/tools/push_to_server.sh` 都设置 `set -euo pipefail`，现代入口用 `exec python3` 返回真实状态；fallback显式累计failed并exit。`tools/workspace.py:26–34,204–218` 对非零命令退出、远端SHA不符均抛错。此次没有找到“这些发布脚本吞错误码”的已证实问题，不应强行列入方案。
- 发布工具和task graph都明确不等同QA接受；问题在当前关键控制仍靠人工且已有遗漏，不应描述为“已部署自动调度”或声称发布工具本来承诺做业务验收。
- 未验证硬件日志真实性、未访问板卡、未判断新的AP/MC/TH运行行为；这些由相应独立源码/硬件核查负责。

## 建议修订顺序（供方案集成）

先修卡可解析性并冻结当前证据 → 补全任务发现与类型schema → 全类型状态/独立性/版本接受门禁 → Ready租约与准确消费校验 → 真实diff/范围/资源检查 → 新候选与报告摘要绑定 → 规则原件版本化和恢复验证 → 从卡生成当前投影。每项实现与工具测试产物也须按canonical规则由未参与作者工作的独立Codex会话复核，不能由本报告作者直接给自己实现签署。
