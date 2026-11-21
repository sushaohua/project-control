# 第一步：COORD 自动拉起 PM/ARCH 并指定高级模型 实施方案

## 修订历史

| 版本 | 修订时间（北京时间） | 修订人 | 变更摘要 | 审批状态 |
| --- | --- | --- | --- | --- |
| `v0.1` | `2026-11-21 12:13:37` | `AI (Antigravity-CLI)` | 按用户 12:13 的决定，从 [角色模型总体方案 v0.4](role_model_routing_implementationplan_20261121_110624.md) 中拆出第一步：沿用现有流程，COORD 在阶段一自动拉起 PM 和 ARCH，并为两者指定高级模型；巡航脚本、INTEGRATOR 及其他角色一律不动 | 由 `v0.2` 接续 |
| `v0.2` | `2026-11-21 12:16:43` | `AI (Antigravity-CLI)` | 用户确认待决项 Q1：PM 用 `gemini-4-neon-high`，ARCH 用 `gemini-4-carbon-high`（暂定值，修改配置即可更换） | 由 `v0.3` 接续 |
| `v0.3` | `2026-11-21 12:18:30` | `AI (Antigravity-CLI)` | 用户确认待决项 Q2：高级型号不可用时，退回主会话模型继续执行；新增 §7，说明对在途 COORD 的影响和实施时机 | **已批准**（用户 2026-11-21 14:20:59“批准执行”）；14:21 核查 HIL 仍在进行（`hil_r17b/` 最新物证 14:13，ledger 无 `HIL-Verified`），按 §7 暂缓实施 |
| `v0.4` | `2026-11-21 15:25:02` | `AI (Antigravity-CLI)` | 核对在途 COORD 的运行日志后，用户决定 Q3/Q4：配置增加备用高级型号（PM 备用 `gemini-4-neon-xhigh`，ARCH 备用 `claude-opus-5-5-high`），主型号和备用型号都不可用时才继承主会话；复用已在线的 PM/ARCH 前先核对型号，不一致时用 `swarm model` 切换。更正：在途 COORD 是 agy（Orchestrator 模式），不是 Codex。改动文件和 Diff Budget 不变 | 沿用 v0.3 的批准（范围和预算未变，新增内容均为用户 15:25 的决定）；仍按 §7 暂缓实施 |
| `v0.5` | `2026-11-21 15:27:26` | `AI (Antigravity-CLI)` | 用户更正 ARCH 的备用型号：由 `claude-opus-5-5-high` 改为 `gemini-4-neon-xhigh`（与 PM 相同） | 沿用 v0.3 的批准（范围和预算未变）；仍按 §7 暂缓实施 |
| `v0.6` | `2026-11-21 18:24:47` | `AI (Antigravity-CLI)` | **PMARCH-01 已实施**：18:23 核查 ledger 第 30 行已有 SLICE-08 `HIL-Verified`（17:26:46，提交 `1f8399f`），无门禁进程，本地与 `origin/main` 一致，无已跟踪的未提交改动。提交 `58ee28d` 新增 `config/role_models.yaml`（+12），`delivery_and_coord_gate.md` 升到 revision 9（+9/-2），合计 23 行，不超过 45；YAML 解析和键校验通过；`test_v2_gates.py` 12 项全部通过；`fast_gate.py --files` 退出码 0。PMARCH-02 实测待在新的 agy 会话中进行 | PMARCH-01 完成；PMARCH-02 待执行 |

## 1. 产品目标与范围

### 1.1 目标

在现有"用户提出想法 → PM 整理需求 ↔ ARCH 核对可行性 → 合成一份方案 → 用户批准 → COORD 组织实施"的流程下，由 COORD 自动拉起 PM 和 ARCH 两个子 agent，并**指定各自对应的高级模型**。角色职责、技能、写入边界、交付物和审批都不变（见 [角色规则](../../.agents/rules/02_模块与Agent职责.md)、[交付与 COORD 门禁](../../.agents/rules/delivery_and_coord_gate.md)）。

### 1.2 用户已确认的决定

| # | 决定 |
| --- | --- |
| S1 | COORD 是用户启动的主会话本身，不是派发出来的 |
| S2 | 第一步只为 **PM 和 ARCH** 指定模型，要求用对应的高级模型 |
| S3 | **触发时机**：用户提出想法、进入阶段一时，COORD 自动拉起 PM；PM 交出产品定义后，COORD 再自动拉起 ARCH；双方往返都由 COORD 中转。目标明确的小修只拉起 ARCH |
| S4 | 巡航脚本 `run_slice_batch.py`、相关测试和 INTEGRATOR 都不动，Diff Budget 为 0；原 ROLE-01 移到后续步骤 |
| S5 | 第一步单独成一份方案（即本文件），后续步骤以后另开新方案 |
| S6 | （由 S8 细化）指定型号不可用时，退回继承主会话模型继续执行，并记录退回原因 |
| S7 | 型号暂定为：PM 用 `gemini-4-neon-high`，ARCH 用 `gemini-4-carbon-high` |
| S8 | **退回顺序**：先用主型号；不可用时用备用高级型号（PM 和 ARCH 都备用 `gemini-4-neon-xhigh`，用户 15:27 确认）；两者都不可用才继承主会话，并记录实际用到的型号。原因：Orchestrator 模式下，`inherit` 往往落到 `gemini-flash-worker-agy` |
| S9 | **复用前核对型号**：复用已在线的 PM/ARCH 之前，先用 `swarm status` 核对实际型号。和配置不一致时：成员空闲（`waiting`）就用 `swarm model` 切换，保留对话；成员正在工作就等它这一轮结束再切换。每次核对和切换都记录 |

### 1.3 包含与排除

- **包含**：PM/ARCH 的模型配置；COORD 在阶段一自动拉起 PM/ARCH 的规则条款；运行记录；实测一次。
- **排除**：跨执行器拉起（`runner: codex`，即总体方案 D9）；INTEGRATOR 及其他角色的模型；巡航脚本；QA；业务仓、SDK、台架和契约。这些都留给后续方案。

### 1.4 完成条件（可观察）

1. 在 agy 主会话里提出一个新想法后，COORD **无需用户再下指令**就拉起 PM；`swarm status` 显示 PM 跑在配置的型号上。
2. PM 交出产品定义后，COORD 自动拉起 ARCH，`swarm status` 显示 ARCH 跑在配置的型号上；两者修改的是**同一份方案**的不同章节。
3. 目标明确的小修只拉起 ARCH，不拉起 PM。
4. 主型号不在可用清单里或额度为 0 时，改用备用高级型号；两者都不可用时继承主会话模型。运行记录写明原因和实际型号。
5. 每次拉起都在 `project-control/docs/evidence/planning/<方案文件名>/` 下留一份运行记录。
6. 修改配置里的型号后再复用已在线的 PM/ARCH 时，`swarm status` 显示它已切换到新型号，而且对话上下文保留。

## 2. 实测事实与现状

| 事实 | 证据 |
| --- | --- |
| agy 的 `invoke_subagent` 和工作流 `agent()` 只接受档位，不能指定具体型号 | 2026-11-21 11:47 实测：`agent(model="gemini-4-neon-high")` 报 `invalid model`，并中止整个工作流 |
| agy 的 `swarm add(model=<ID>)` 可以指定具体型号，`swarm status` 能查到实际型号 | 2026-11-21 11:44 `swarm models` 返回 27 个 ID，包括 `gemini-4-neon-high`、`gemini-4-carbon-high`、`gemini-4-hydrogen-xhigh`、`gemini-4-neon-xhigh`、`claude-opus-5-5-high`，并附带额度 |
| 现在 PM/ARCH 没有自动拉起的入口 | `project-control/tools/` 中检索不到规划派发代码；[delivery_and_coord_gate.md §1](../../.agents/rules/delivery_and_coord_gate.md#L29-L36) 只规定了流程，没有规定由谁、怎样拉起 |
| 第一次 `swarm add` 之前，COORD 须先加载 `swarm_pane` 技能 | 该内置技能的说明为 "Load it before you brief and add the first workers to a swarm" |
| **`inherit` 在创建时就固定，复用时不会跟着变** | 2026-11-21 15:22 核对在途 COORD 的日志：主会话第 111 步（10:48:34）在 worker 层调用 `invoke_subagent(Model="inherit")`，拉起的 eng-ap、eng-mcu 每一步都是 `gemini-flash-worker-agy`；主会话第 756 步（14:24:05）切到 `gemini-4-carbon-high` 后，15:09 复用这两个会话时仍是 Flash |
| **Orchestrator 模式下，`inherit` 往往落到 Flash Worker** | 同一份日志中，`gemini-pro-orchestrator-neon` 和 `gemini-flash-worker-agy` 交替出现，派单动作落在 worker 层 |
| 空闲的 swarm 成员可以换模型并保留对话 | swarm 工具说明：`model` 会把处于 `waiting` 的成员切换到其他模型，保留对话 |
| 子会话日志记录了每一步的实际模型 | `transcript.jsonl` 每一步都有 `"model"` 字段。但日志在 `~/.gemini/...` 下，超出工作区边界，第一步不读取，仍以 `swarm status` 为准 |
| `[UNVERIFIED]` | ① Codex 主会话原生拉起子会话的方式，以及指定型号和推理强度的参数；② Codex 型号 ID；③ `swarm kill` 对 `workspace="inherit"` 成员会不会删除共享的工作区。第一步不依赖 ①②（Codex 主会话下按 S6 退回继承并记录）；③ 通过"阶段一结束前不 kill"规避 |

协议、帧布局、超时、中断、内存、VTOR 推演：**N/A**，本方案不涉及业务仓和协议。

## 3. 设计

### 3.1 新增 `project-control/config/role_models.yaml`

```yaml
# PM/ARCH 子角色模型配置（第一步）。COORD 是主会话，不在此表中；其他角色暂不配置。
schema_version: 1
roles:
  PM:
    antigravity: {model: gemini-4-neon-high, fallback_model: gemini-4-neon-xhigh}      # 用户 12:16 / 15:25 确认
    codex: {model: "[UNVERIFIED]"}
  ARCH:
    antigravity: {model: gemini-4-carbon-high, fallback_model: gemini-4-neon-xhigh}    # 用户 12:16 / 15:27 确认
    codex: {model: "[UNVERIFIED]"}
```

这份配置**没有脚本读取**，由 COORD 按 §3.2 的规则条款读取后执行。这是有意设计的接入点，不算悬空配置。只允许出现 `PM` 和 `ARCH` 两个键，出现其他键时 COORD 停止自动拉起并报告。

### 3.2 拟写入 `delivery_and_coord_gate.md` §1 的条款（约 15 行）

1. **触发**：进入阶段一时，COORD 先读 `config/role_models.yaml`。任务需要产品澄清就先拉起 PM，PM 交出产品定义后再拉起 ARCH；目标明确的小修只拉起 ARCH。双方往返都由 COORD 中转。
2. **agy 主会话**：
   - 第一次拉起前加载 `swarm_pane` 技能；
   - 用 `swarm models` 依次检查 `model`、`fallback_model`，取第一个在清单里且额度大于 0% 的，执行 `swarm add(name="pm" | "arch", model=<ID>, workspace="inherit", brief=<拉起说明>)`；两者都不可用时省略 `model`（继承主会话）并记录；
   - 拉起后用 `swarm status` 记下实际型号。
3. **Codex 主会话**：用 Codex 原生方式拉起子会话，配置里的 `codex` 项还没核实时继承主会话模型并记录。
4. **拉起说明（brief）只写指针**，不复制历史对话：角色、对应技能（`product-requirements` 或 `arch-deep-spec`）、写入边界（只改本任务方案的产品章节或技术章节）、方案路径、用户原话摘要，以及交回格式 `{plan_path, plan_revision, changed_sections, open_items}`，交回对象为 COORD。
5. **运行记录**：写到 `docs/evidence/planning/<方案文件名>/dispatch_<role>_<YYYYMMDD_HHMMSS>.json`，字段为 `role, main_session, requested_model, effective_model, fallback_reason, member_name, ts`。`effective_model` 取 `swarm status` 的结果，查不到时为 `unverified`。
6. **修订人**：PM/ARCH 修改方案时，修订人写成 `AI (Antigravity-CLI / PM / <型号 ID>)` 这种格式。
7. **生命周期**：方案获批之前，PM/ARCH 一直保持在线（空闲时处于 `waiting`，不消耗额度），以便返工；第一步不执行 `swarm kill`。
8. **复用前核对**：每次给已在线的 PM/ARCH 派活之前，先用 `swarm status` 核对实际型号，再按 S8 的顺序重新确定应该用的型号。两者不一致时：成员空闲就用 `swarm model` 切换（保留对话）；成员正在工作就等这一轮结束再切换。写入运行记录（`action: reuse | switch`）。

## 4. 实施切片与 Diff Budget

只改 `project-control`：2 个文件，增删合计不超过 45 行。业务仓、SDK、台架、契约、`run_slice_batch.py`、`test_v2_gates.py` 的 Diff Budget 都为 **0**。

| ID | 目标文件 | 内容 | 验收 |
| --- | --- | --- | --- |
| `PMARCH-01` | 新增 `config/role_models.yaml`；修改 `.agents/rules/delivery_and_coord_gate.md`（§1 增加 §3.2 的条款，frontmatter 的 `revision` 由 8 升到 9） | 配置与规则条款 | `git -C project-control diff --numstat` 两个文件增删合计不超过 45 行；`python3 -c "import yaml; yaml.safe_load(open('project-control/config/role_models.yaml'))"` 解析通过，键只有 `PM` 和 `ARCH`；`python3 -B project-control/tools/test_v2_gates.py` 仍然全部通过（证明巡航没受影响） |
| `PMARCH-02` | 不改代码，只做实测 | 在 agy 主会话里用一个只写方案、不改代码的示例想法跑一遍阶段一，按 §1.4 的 1–6 条逐项取证；另把配置临时改成不存在的型号（不提交），分别验证"主型号不可用改用备用型号"和"两者都不可用才继承"；再把配置改成另一个型号后复用 PM，验证 `swarm model` 切换后对话保留 | 运行记录和 `swarm status` 输出归档到 `docs/evidence/planning/pm_arch_model_dispatch/`；Codex 主会话没有实测的部分标为"未验证" |

依赖关系：`PMARCH-02` 依赖 `PMARCH-01`。

## 5. 回滚

- 删除 `config/role_models.yaml`，并 `git revert` 规则条款的那次提交，COORD 就恢复为现在的手动方式。
- 巡航脚本和业务仓没有改动，不需要回滚。

## 6. 待决项

| # | 问题 | 当前建议 |
| --- | --- | --- |
| Q1 | PM 和 ARCH 各自用哪个"高级模型"？ | **已决定（12:16）**：PM 用 `gemini-4-neon-high`，ARCH 用 `gemini-4-carbon-high`，均为暂定值，日后修改配置即可更换 |
| Q2 | 高级模型不可用时，是退回继承主会话模型（S6），还是暂停并请用户换型号？ | **已决定（12:18）**：退回主会话模型继续执行，并记录原因 |
| Q3 | Orchestrator 模式下，`inherit` 往往落到 Flash Worker，退回时怎么办？ | **已决定（15:25）**：见 S8，先用备用高级型号（均已在 11:44 的 `swarm models` 清单中核实存在），两者都不可用才继承 |
| Q4 | 复用已在线的 PM/ARCH 时，型号和配置不一致怎么办？ | **已决定（15:25）**：见 S9 和 §3.2 第 8 条 |

## 7. 对在途 COORD 的影响与实施时机

2026-11-21 12:18 核查现场：
- `project-control` 最新提交为 `cb25ab0`（12:09:56，记录 SLICE-08 r17b 的 SW-Verified 结论）；
- 当前没有 `slice_gate`、`qa_runner`、`codex exec` 门禁进程在运行；
- 工作区内有在途 COORD 留下的未跟踪 SLICE-08 证据文件。

| 影响面 | 结论 | 依据或措施 |
| --- | --- | --- |
| 巡航和门禁脚本 | **无影响** | `run_slice_batch.py`、`slice_gate.py`、`codex_review.py`、`qa_runner` 都不读取 `role_models.yaml`，`delivery_and_coord_gate.md` §1 的新条款也不读 |
| 在途 COORD 的当前会话 | **无影响** | 新条款只在进入阶段一时生效；已加载的规则不会自动刷新。COORD 下次重新读规则并开始新的阶段一时才会按新条款拉起 PM/ARCH |
| 切片输入指纹 | **只有提交时才会改变** | SLICE-08 的 `input_repositories` 包含 `project-control`，`input_fingerprint()` 会读取它的 HEAD。只改工作区文件不会改变 HEAD；一旦提交，就会像 COORD 自己的证据提交一样改变指纹。门禁运行期间提交，可能导致当次裁决判为指纹不一致的 `BLOCKED`（不扣返修次数，但会浪费一次 Docker QA） |
| Git 共用工作区 | **有并发风险，需规避** | COORD 和本任务共用同一个 `project-control` 工作区和 `main` 分支。只用精确路径 `git add`，绝不使用 `-A`；不碰任何 SLICE-08 证据文件和他人未跟踪的方案；推送前先 fetch，再 rebase 到 `origin/main`；遇到冲突立即停止 |

**实施时机**：`PMARCH-01` 只在没有门禁进程运行时执行。编辑和提交连续完成，中间不留未提交改动，避免被 COORD 的提交一并带走。动手前重新核查进程和最新提交；发现门禁正在运行就暂停，等结束后再做。`PMARCH-02` 的实测在新的 agy 会话里进行，不干扰在途 COORD。

**HIL 上板验收期间（12:21 用户告知在途 COORD 正在做 SLICE-08 的 HIL 验收）**：
- 本改动不涉及固件、板卡、串口和台架，不改变 HIL 节点（AP/MC/TH/Bootloader）的固件身份链。
- 但 HIL 期间 COORD 会持续向 `project-control` 提交 HIL 物证。ledger 中 SLICE-08 的 SW-Verified 记录绑定的是 `project-control:dc9a027`。HIL 的 Codex 审计会不会比对 `project-control` 在 SW-Verified 到 HIL 之间的差异，目前是 `[UNVERIFIED]`。如果会，夹在中间的本改动可能被误判为切片范围外的改动。
- 因此 **HIL 期间不编辑、不提交、不推送**。可以先审批，实施等到以下任一条件满足、且用户确认后再开始：ledger 出现 SLICE-08 的 `HIL-Verified` 记录；或者用户明确告知 HIL 已结束或暂停。

请审阅本方案。批准（`批准执行` / `Approved`）前不改任何配置或规则。
