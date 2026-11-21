# 固定角色流程与可替换模型实施方案

## 修订历史

| 版本 | 修订时间（北京时间） | 修订人 | 变更摘要 | 审批状态 |
| --- | --- | --- | --- | --- |
| `v0.1` | `2026-11-21 11:06:24` | `AI (Codex)` | 汇总角色模型、自动派单和 Git 交接，定义替换执行器的边界及验收 | 由 `v0.2` 接续评审 |
| `v0.2` | `2026-11-21 11:08:44` | `AI (Codex)` | 按用户确认固定角色矩阵、职责、交付和流程，把替换模型明确为启动时的配置能力 | 由 `v0.3` 接续评审 |
| `v0.3` | `2026-11-21 11:19:02` | `AI (Codex)` | 主会话担任 COORD，使用用户启动时选择的客户端和模型；模型表只配置子角色 | 由 `v0.4` 接续评审 |
| `v0.4` | `2026-11-21 11:55:05` | `AI (Antigravity-CLI)` | 依据评审与用户决定 D1–D9 重写：实测运行时只接受档位（`agent()` 不接受型号 ID，且型号写错会中止整个工作流）；PM/ARCH 在 agy 下改用 swarm 指定精确型号；INTEGRATOR 本期先白名单校验，不通过就退回 inherit；写代码的角色不得与 QA 同属一家；补充接口签名、运行记录、Diff Budget 和三个检查点 | 由 `v0.5` 接续 |
| `v0.5` | `2026-11-21 12:13:37` | `AI (Antigravity-CLI)` | 用户决定分步实施：第一步（COORD 自动拉起 PM/ARCH 并指定高级模型，巡航脚本和 INTEGRATOR 不动）拆到 [pm_arch_model_dispatch_implementationplan_20261121_121337.md](pm_arch_model_dispatch_implementationplan_20261121_121337.md)。本方案其余内容（ROLE-01、`runner: codex`、ROLE-03）保留为后续步骤的设计参考，后续另开新方案时再审批 | 暂不审批（参考设计） |

> [!NOTE]
> 第一步请审阅上面链接的新方案。本文件 §2–§6 只作后续步骤的设计参考，不在本轮实施范围内。

## 1. 产品目标与范围

### 1.1 背景与目标

现在的角色矩阵、职责、交付物和流程都不改（见 [角色规则](../../.agents/rules/02_模块与Agent职责.md)、[交付与 COORD 门禁](../../.agents/rules/delivery_and_coord_gate.md)）。目标是**按角色挑选能力合适的模型**，比如 ARCH 用长上下文、推理强的型号，PM 用更擅长对话的型号。为此需要精确到模型系列和推理强度，并且事后能查到当次用的是哪个型号。

### 1.2 用户已确认的决定

| # | 决定 |
| --- | --- |
| D1 | **COORD 就是用户启动的主会话**，不是派发出来的。用 Codex 启动，COORD 就是这个 Codex 会话；用 `agy` 启动，就是这个 Antigravity 会话。COORD 不进配置表 |
| D2 | 只有 `PM`、`ARCH`、`INTEGRATOR` 三个角色可以配置模型。其余角色（ENG-\*、ENG_BOOT_\*）照旧继承主会话模型；QA 照旧只由 `codex_review.py` 决定 |
| D3 | 配置填精确型号 ID，推理强度也算在内 |
| D4 | 写代码的角色和正式 QA（Codex，OpenAI）属于同一家时，判 `BLOCKED`。PM/ARCH 不写业务代码，不受这条限制 |
| D5 | Codex 当主会话时，只做规划（派发 PM/ARCH）和调用门禁；工程批次巡航仍用 `agy` 启动 |
| D6 | PM/ARCH 由 COORD 按技能派发，派发前读配置决定模型。agy 主会话用 `swarm add(model=<ID>)`，Codex 主会话用 `codex -m <型号>` 加推理强度 |
| D7 | 本期 INTEGRATOR 先用档位或 inherit。配置里可以写精确 ID，派发前做白名单校验，不通过就退回 `inherit` 并记录；等运行时支持后再升级 |
| D8 | 建议型号不可用（不在清单里、额度为 0、账号无权限）时，退回 `inherit` 继续执行，并在运行记录里写明 |
| D9 | agy 当主会话时，ARCH（以及 PM）也可以配 `runner: codex`，由 COORD 用 `codex exec` 拉起 |

### 1.3 包含与排除

- **包含**：配置文件；INTEGRATOR 在巡航里的派发、校验、退回和运行记录；COORD 派发 PM/ARCH 的技能说明；三种拉起方式各实测一次。
- **排除**：业务仓、SDK、台架和契约；QA 的模型；把巡航改成 swarm 派发；修复 `_wait_bg_gate()` 依赖 `call_tool` 的既有问题（见 §6 风险 R3，另立任务）。

### 1.4 完成条件（可观察）

1. 没有配置文件时，巡航的派单参数、提示词和门禁命令与现在**完全一致**。
2. 同一个 PM/ARCH 任务只改配置里的型号，重新派发后，`swarm status` 或 Codex 运行记录显示用的是新型号，任务指针、权限和交回格式都不变。
3. 配置违反 D2 或 D4 时，在派单**之前**就判 `BLOCKED`，不扣返修次数。
4. 每次派发都留下运行记录，区分**请求的型号**和**能核实的实际型号**；核实不了的记为 `unverified`。

## 2. 实测事实与调用链核实

| 事实 | 证据（2026-11-21 实测或源码） |
| --- | --- |
| 工作流的 `agent(model=)` 只接受 `inherit / flash_lite / flash / pro` | `agent(model="gemini-4-neon-high")` 返回 `invalid model ... (valid choices: inherit, flash_lite, flash, pro)`，**整个工作流立即中止**，`try` 捕获不到 |
| 工作流脚本里调用不到 swarm | `call_tool("swarm", ...)` 报 `NameError: name 'call_tool' is not defined` |
| agy 可以通过 swarm 指定精确型号 | `swarm models` 返回 27 个 ID，包括 `gemini-4-neon-medium`、`gemini-4-carbon-high`、`gemini-4-neon-high`、`claude-opus-5-5-high`、`gpt-oss-120b-medium`，并附带剩余额度；`swarm status` 显示每个成员实际跑在哪个模型上 |
| 巡航派单接缝 | [run_slice_batch.py:139](../../tools/workflow/run_slice_batch.py#L139) `run_single_slice()` 内 `agent(role=..., workspace="inherit", schema=subtask_schema())`；第 142、153 行用 `parallel()` 派发和返修时**丢弃了返回值**，候选提交由门禁从 Git 读取 |
| 模型选择不影响账本复用 | [slice_gate.py:60-65](../../tools/gates/slice_gate.py#L60-L65) `input_fingerprint()` 只哈希 `spec`、根提交、子任务仓提交和 `workspace.json`，不含 `project-control/config` |
| Codex 原生参数 | [codex_review.py:98-100](../../tools/gates/codex_review.py#L98-L100) 已在用 `codex exec --sandbox ... -m <model> --json --output-schema` |
| 测试桩 | [test_v2_gates.py:27](../../tools/test_v2_gates.py#L27) `"agent": lambda **_: FakeWorker()` 会吞掉所有参数，需要改成能记录参数 |
| `[UNVERIFIED]` | Codex 型号 ID `gpt-6.2-sol` 是否可用、推理强度的参数名（暂写 `-c model_reasoning_effort=<e>`）、`codex exec --json` 事件流里有没有实际型号。这三项在 ROLE-03 实测后消除 |

协议、帧布局、超时、中断、内存、VTOR 推演：**N/A**，本方案不涉及业务仓和协议。

## 3. 配置设计

### 3.1 `project-control/config/role_models.yaml`（初始值）

```yaml
schema_version: 1
roles:
  PM:
    runner: native            # native = 按主会话原生方式拉起；codex = 强制用 Codex 拉起
    antigravity: {model: gemini-4-neon-medium}
    codex: {model: gpt-6.2-sol, reasoning_effort: medium}   # [UNVERIFIED] 待 ROLE-03 实测
  ARCH:
    runner: native
    antigravity: {model: gemini-4-carbon-high}
    codex: {model: gpt-6.2-sol, reasoning_effort: high}     # [UNVERIFIED] 待 ROLE-03 实测
  INTEGRATOR:
    antigravity: {model: gemini-4-neon-high}   # 本期巡航只接受档位，此值会退回 inherit 并记录
```

### 3.2 解析规则（先校验，再派发）

| 主会话 | 角色与 runner | 派发方式 | 校验与退回 |
| --- | --- | --- | --- |
| agy | PM/ARCH，`native` | `swarm add(name=<pm/arch>, model=<antigravity.model>)` | 型号必须在 `swarm models` 列表里，且额度大于 0%；否则不传 `model`（继承 COORD 模型）并记录 |
| agy | PM/ARCH，`codex` | `codex exec -m <codex.model> -c model_reasoning_effort=<e> --json --output-schema <规划返回 schema>` | 启动失败就退回 agy 原生 swarm 并记录 |
| Codex | PM/ARCH，`native` 或 `codex` | Codex 原生子会话，用 `codex` 块里的配置 | 不可用就继承主会话模型并记录 |
| agy（巡航） | INTEGRATOR | `agent(..., model=<档位>)` | 值属于四个档位就直接传；否则传 `inherit` 并记录 `fallback_reason=runtime_tier_only` |
| 任意 | INTEGRATOR 配 `runner: codex`，或 `antigravity.model` 以 `gpt-` 开头 | 不派发 | **判 `BLOCKED`**（D4），零扣次 |
| 任意 | 配置里出现 `COORD`、`QA`、`ENG-*`、`ENG_BOOT_*` 或未知键 | 不派发 | **判 `BLOCKED`**（D1/D2），零扣次 |

- **单次任务覆盖**：只能通过 `run_workflow` 的 `Args.role_model_overrides` 传入，或由用户当次在会话里明确指定；**不允许写进切片 YAML**，因为切片内容参与输入指纹，写进去会让已通过的账本记录失效。
- **运行记录**：
  - 巡航：写到 `docs/evidence/<SLICE>/dispatch_<YYYYMMDD_HHMMSS>_<rand>.json`，同时合并进 `run_single_slice()` 返回结果的 `dispatch` 字段；
  - PM/ARCH：由 COORD 写到 `docs/evidence/planning/<方案文件名>/dispatch_<role>_<ts>.json`；
  - 字段：`role, runner, main_session, requested_model, effective_model, fallback_reason, session_ref, ts`。`effective_model` 的取值：swarm 取 `swarm status` 的结果；巡航取 `inherit`；查不到时为 `unverified`。

## 4. 实施切片与 Diff Budget

只改 `project-control`，业务仓、SDK、台架和契约的 Diff Budget 为 **0**。

### `ROLE-01` INTEGRATOR 在巡航中的派发与校验

- **文件**（3 个，合计增删不超过 120 行）：
  - 新增 `config/role_models.yaml`
  - 修改 `tools/workflow/run_slice_batch.py`
  - 修改 `tools/test_v2_gates.py`
- **接口签名**（每个函数不超过 50 行、不超过 4 个参数、中文文档字符串）：
  - `load_role_models(ws: Path, overrides: Optional[dict]) -> dict`：读配置并合并 Args 覆盖；文件不存在时返回 `{}`。
  - `validate_role_models(table: dict) -> str`：违反 D1/D2/D4 时返回原因，合法返回 `""`。
  - `resolve_workflow_model(role: str, table: dict) -> Tuple[Optional[str], dict]`：返回 `(档位或 None, 派发记录)`。`None` 表示该角色不传 `model`，保持现有行为。
  - `run_single_slice(workspace_str, plan_path, slice_yaml, role_models: Optional[dict] = None)`：只有拿到档位时才给 `agent(...)` 传 `model=`。
  - `run_batch_cruise(cfg)`：开头调用一次 `load_role_models` 和 `validate_role_models`，校验失败就返回 `_blk(sid, "role_models", reason)`。
- **验收**：在工作区根目录执行 `python3 -B project-control/tools/test_v2_gates.py`，全部通过，并新增以下用例：
  1. 没有配置文件：所有 `agent` 调用都不带 `model`，现有用例全部通过。
  2. INTEGRATOR 分别配 `flash` 和 `pro`：两次派单只有 `model` 不同，提示词和门禁命令逐字相同。
  3. INTEGRATOR 配 `gemini-4-neon-high`：传 `inherit`，记录里写明 `fallback_reason=runtime_tier_only`。
  4. INTEGRATOR 配 `runner: codex` 或 `gpt-oss-120b-medium`：判 `BLOCKED`，派单 0 次，`remediation_used=0`。
  5. 配置里出现 `COORD`、`QA` 或 `ENG-AP`：判 `BLOCKED`。
  6. `Args.role_model_overrides` 优先于配置文件，输入指纹不变。

### `ROLE-02` COORD 派发 PM/ARCH 的技能说明

- **文件**：修改 `.agents/skills/slice-batch-orchestrator/SKILL.md`，增加"子角色模型选择"一节。1 个文件，增删不超过 20 行。
- **内容**：
  - 按 §3.2 的表格派发 PM/ARCH：agy 用 `swarm models` 校验后 `swarm add(model=)`，派发完用 `swarm status` 核对实际型号；`runner: codex` 用 `codex exec`；Codex 主会话用原生子会话。
  - 规划返回统一为 `{plan_path, plan_revision, changed_sections, open_items}`。
  - 写运行记录。
  - 用 `gpt-*` 主会话启动巡航前给出警告（见 R2）。
- **验收**：`git -C project-control diff --numstat -- .agents/skills/slice-batch-orchestrator/SKILL.md` 显示增删合计不超过 20 行；人工核对新增内容与 §3.2 逐项一致。`fast_gate.py --files` 是否检查 Markdown 尚未核实，不作为本项的通过依据。

### `ROLE-03` 三种拉起方式实测（只读，不改代码）

- 基于同一个冻结的 `project-control` 提交，让 ARCH 做同一项只读评审，不写文件，只交回规划返回结构。依次实测：
  - (a) agy 主会话，用 swarm 指定 `gemini-4-carbon-high`；
  - (b) agy 主会话，`runner: codex`；
  - (c) Codex 主会话，原生子会话。
- **通过标准**：三次交回的结构相同，角色、权限和输入指针一致；(a) 的 `effective_model` 能通过 `swarm status` 核实；(b)(c) 消除 §2 中三项 `[UNVERIFIED]`，消除不了的照实标注。实测结果和运行记录归档到 `docs/evidence/planning/role_model_routing/`。没有实际跑过的项标为"未验证"。

依赖关系：`ROLE-01` 和 `ROLE-02` 互相独立，可以并行；`ROLE-03` 依赖 `ROLE-02`。

## 5. 回滚

- 删除 `config/role_models.yaml`，行为就与现在逐字节一致（ROLE-01 验收用例 1 已覆盖）。
- 需要彻底回滚时，按提交逐个 `git revert` ROLE-01 和 ROLE-02，保留已生成的运行记录和 Git 收据。
- 切片续跑按切片、候选提交和输入指纹进行，不受模型配置影响。

## 6. 风险与待办

| # | 风险 | 处理 |
| --- | --- | --- |
| R1 | 运行时开放 `agent()` 精确型号之前，INTEGRATOR 只能跟主会话同一型号 | 已按 D7 接受；运行记录写明退回原因，运行时开放后只需放宽白名单 |
| R2 | agy 主会话本身是 `gpt-oss-*` 时，INTEGRATOR 继承后会和 QA 同属一家，而脚本检测不到主会话型号 | ROLE-02 在技能里要求 COORD 启动巡航前自查，主会话是 `gpt-*` 时不启动巡航 |
| R3 | `_wait_bg_gate()` 依赖 `call_tool`，当前运行时没有这个函数 | 不在本方案范围内，另立任务核查 |
| R4 | swarm 派发的 PM/ARCH 交回内容没有固定格式校验 | 要求按规划返回结构交回，并以方案文件里实际的修订记录为准 |

请审阅本方案。批准（`批准执行` / `Approved`）前不改任何代码或配置。
