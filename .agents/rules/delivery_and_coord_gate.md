---
id: RULE-COORD-DELIVERY-GATE-V2
revision: 9
status: current-rule
owner: COORD
updated: '2026-11-21'
plan_revision: v2-slice-funnel
---

# COORD V2 垂直切片编排、四阶漏斗门禁与双态准出规程

## C308L 当前入口

AP 使用 `printer-soc`，SDK 使用 `sdk/c308l` 独立 Repo 客户端，角色采用十席。COORD 对业务和平台源码只读；根工作区治理维护仅能写获批方案逐项列出的根路径，不因此取得应用或 SDK 写权。平台 project 的实现委派 `ENG-PLATFORM`，Helix 与打印业务委派 `ENG-AP`。

切片声明 `revision`、`profile`（`host-software` / `c308l-app` / `c308l-system`）、`delivery_kind`（`checkpoint | deliverable`，旧切片缺省按 `deliverable`）及完整候选；交付点须用 `covered_checkpoints` 声明覆盖的检查点，漏项或输入不符立即阻塞。SDK 锁引用来自准确 printer-soc 提交。SDK 输入变化必须重验，账本同一 slice_id 的历史绿行不能跳过新输入。每次门禁明确检查子进程退出状态与真实 verdict，禁止根据“调用返回了字符串”准出。

跨阶段交接与断点续跑须遵循 `project-control/contracts/git_handoff.schema.json` 与 `tools/workflow/git_handoff.py`：
- 内部检查点（`checkpoint`）执行本地快检与合龙并生成 `checkpoint_receipt.json`，不触发独立 Codex 冷审且不写 `SW-Verified` / `HIL-Verified`；
- 同候选、同测试命令、同容器镜像且通过 `server_qa` 校验的 Docker QA 证据支持阶段续跑复用，任一输入变更即拒绝复用；
- 正式交付点准出与账本写入须可从 Git 服务端读回定位符验证，禁止仅凭本地 `verdict.json` 或私有路径放行。

`run_workflow` 仅在运行时实际提供所需原语时启动。环境缺少运行时则报告该部分未演练，可继续由当前客户端按相同写边界委派相互独立的已授权任务；不得伪称自动巡航已运行。软件及应用交叉构建不触碰硬件；发布和物理操作仍按 Human Gate #2。

本规则取代旧版 `coord_runner` 状态机与微票门禁（旧归档件封存于 `project-control/tools/legacy/` 与 `.agents/kanban/archive_v1/`，历史 `Done` 卡片与证据保持原样不改写）。新建与在途研发统一执行 **“两阶段 SSoT 协议 + 垂直切片连坐闭环 + 四阶无状态门禁漏斗”**。

## 1. 两阶段协议与单一真相源（SSoT）入口

1. **Phase 1（实施方案先行，Human Gate #1）**：
   - 流程为：用户表达想法 → `PM` 整理需求 ↔ `ARCH` 核对可行性 → 合成一份方案 → 用户批准 → `COORD` 组织实施。
   - `PM` 使用 `product-requirements` 在本任务方案中明确目标、场景、优先级草案、范围、异常和可观察的完成条件；只问影响产品结果的关键问题，技术事实交 ARCH 核实。
   - `ARCH` 提前反馈现有能力、缺口、依赖、风险及可选阶段范围，不静默更改产品目标；PM 统一与用户收敛产品取舍，双方按章节合成同一方案，不另建目标真源。
   - `ARCH` 基于本地 `graphify` AST 图谱取证与 `project-control/contracts/minimc_v2_contract.yaml` 契约真源，产出时间戳方案 `{summary}_implementationplan_{YYYYMMDD_HHMMSS}.md`。
   - 方案必须**原地迭代更新（In-place Update）**，头部维护实名修订履历（显式标注具体 AI 客户端/引擎实体，如 `AI (Antigravity-CLI)`、`AI (Codex)`），列明 AST 调用链核实表、软硬件契约推演、各子仓 **最小修改预算（Diff Budget）**、拓扑有序切片 `SLICE-XX` 及回滚预案。
   - 产品定义、技术设计和目标/切片/验收映射复用一次实施方案审批；明确目标的小修沿既有授权处理，不增加固定 PM 签字环节。COORD 按获批方案接单，不把 PM/ARCH 放入工程 subtasks。
   - **未获人类明确批准（`Approved` / `批准执行`）前，严禁修改任何工程代码**；一经批准，即授予当前批次（2～3 个垂直切片）连续自动巡航授权。
   - **PM/ARCH 自动拉起与模型选择**（[实施方案](../../docs/planning/pm_arch_model_dispatch_implementationplan_20261121_121337.md)）：COORD 即用户启动的主会话，不派发自身。进入 Phase 1 时先读 `project-control/config/role_models.yaml`（只允许 `PM`、`ARCH` 两键，出现其他键即停止自动拉起并报告）；需产品澄清先拉起 PM，PM 交出产品定义后再拉起 ARCH，目标明确的小修只拉起 ARCH，双方往返由 COORD 中转。
     - agy 主会话：首次拉起前加载 `swarm_pane` 技能；用 `swarm models` 依次检查 `model`、`fallback_model`，取第一个在清单内且额度大于 0% 的执行 `swarm add(name="pm"|"arch", model=<ID>, workspace="inherit", brief=<指针>)`；两者都不可用才省略 `model` 继承主会话并记录；拉起后用 `swarm status` 记录实际型号。
     - Codex 主会话：用原生方式拉起子会话；配置中的 `codex` 项未核实前继承主会话模型并记录。
     - brief 只写指针，不复制历史对话：角色、技能（`product-requirements` / `arch-deep-spec`）、写入边界（仅本任务方案的产品或技术章节）、方案路径、用户原话摘要；交回 COORD 的格式为 `{plan_path, plan_revision, changed_sections, open_items}`，交回消息须以 `@coordinator` 开头（否则唤醒不了主会话）。
     - 复用已在线的 PM/ARCH 前，先用 `swarm status` 核对实际型号，并按上述顺序重新确定目标型号；不一致时，成员处于 `waiting` 就用 `swarm model` 切换（保留对话），处于 `working` 就等本轮结束再切换。
     - 每次拉起、复用或切换都写运行记录 `project-control/docs/evidence/planning/<方案文件名>/dispatch_<role>_<YYYYMMDD_HHMMSS>.json`，字段 `role, action, main_session, requested_model, effective_model, fallback_reason, member_name, ts`，其中 `action` 取 `spawn | reuse | switch`；`effective_model` 取 `swarm status`，查不到记 `unverified`。
     - PM/ARCH 修订方案时，修订人写 `AI (<实际客户端实体，如 Antigravity-CLI / Antigravity-IDE / Codex> / <角色> / <型号 ID>)`；方案获批前保持在线，不执行 `swarm kill`。
2. **Phase 2（`run_workflow` 有界自动巡航）**：
   - `COORD` 通过 `project-control/tools/workflow/run_slice_batch.py` 按序推进批次切片，以追加式账本 `project-control/slices/ledger.md` 实现幂等断点续跑，耗时 $>1\text{ min}$ 步骤通过 `phase()`/`log()` 实时输出进度。
   - **`COORD` 业务仓只读硬铁律**：`COORD` 严禁直接修改 `printer-soc/`、`mcu-p3/`、`test_harness/`、`boot/bootloadermc/`、`boot/bootloaderth/`，所有代码变更必须委派对应 `ENG-*` / `ENG_BOOT_*` / `INTEGRATOR` 执行。

## 2. 垂直切片连坐与四阶无状态漏斗门禁

每个 `project-control/slices/SLICE-XX.yaml` 是最小结单单元。**单仓子任务绝不单独跑 Codex QA 或单独结单**，必须依次通过以下四阶机械漏斗：

1. **第 1 阶：秒级机械快检（`tools/gates/fast_gate.py`，`<3s`）**
   - 校验五端协议契约一致性（`tools/sync_contracts.py --check`）；
   - 校验仓库开发分支红线（`mcu-p3` 锁定 `feat/soc-debug`，双 Bootloader 锁定 `soc_debug` 且禁写 `main`）、`allowed_paths` 白名单与 `diff_budget`；
   - 校验自研代码单函数 `≤50 行`、入参 `≤4 个`、全中文文档字符串与逻辑块注释、零未消解 `[UNVERIFIED]`、零改字节测试桥垫片（Shim）与零后门伪日志注入。
2. **第 2 阶：跨仓全进程零篡改合龙门禁**
   - 由 `INTEGRATOR` / 合龙命令在真实守护进程群与真实固件协议/业务核之间完成端到端正负黄金字节向量闭环；失败按黄金帧偏差直接退回违约端修复。
3. **第 3 阶：隔离 Docker 干净沙箱构建与回归（`tools/qa_runner/qa_runner.py`）**
   - 对锁定的多仓 40 位 Commit SHA 在隔离只读容器内全新检出、干净构建并运行回归测试，产出带 `container_inspect` 与 SHA256 绑定的 `server_qa.json`（远端未同步前本地巡航支持显式标记 `local_pre_publish_gate`，正式发布前须锁定远端 Commit 复核）。
4. **第 4 阶：独立异构 Codex 双轴分级冷审（`tools/gates/codex_review.py`）**
   - 宿主机按[独立 QA 规则](codex_qa_review.md#1-独立会话与物理隔离红线)启动独立只读会话，输出 `BLOCKER / MINOR / NIT` 三级结论：
     - **存在 `BLOCKER`**：判定 `REJECTED`，唤醒原 `ENG-*` 保活会话定向修复并重过漏斗（**最多允许 2 轮返修**；第 2 轮仍未闭环或同因复发立即 Fail-Fast 熔断停机升级人类）。
     - **`0 BLOCKER`（含仅有 `MINOR` / `NIT`）**：签发带 `report_sha256` 的 `verdict.json`（`APPROVED`），`MINOR` 记入 `ledger.md` 技术债表，切片标记为 **`SW-Verified`** 自动推进下一切片。

## 3. 双态准出（`SW-Verified` / `HIL-Verified`）与发布红线（Human Gate #2）

1. **业务域真机穿刺**：每跑完 1 个业务域批次（2～3 个 `SW-Verified` 切片），或涉及底层串口驱动/DMA/中断/Bootloader 擦写跳转改动时，工作流自动停机请求 **Human Gate #2**，在排他台架执行正负配对真机 HIL 实测（采集双向 Raw Hex、毫秒时戳、固件 SHA256 与物理状态变化），经独立 Codex 审计通过后升级为 **`HIL-Verified`**。
2. **线性历史与冲突熔断**：推送远端前必须拉取目标分支执行 `git rebase` 保持严格线性历史（禁默认 `git pull` 产生 Merge 节点）；一旦发生变基冲突立即 `git rebase --abort` 或停机保留现场交人工仲裁，严禁强推或静默覆盖。
