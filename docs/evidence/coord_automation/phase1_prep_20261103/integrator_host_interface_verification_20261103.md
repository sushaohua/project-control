---
id: PREP-INTAKE-P1-INT-VERIFY-20261103
task_id: PREP-INTAKE-P1-INT
revision: 2
previous_revision: 1
previous_sha256: 83ec1682d9ec4286992c7fd167f52be04aa5958542e58b029159678d902f221e
date: '2026-11-03T13:10:00+08:00'
role: INTEGRATOR
run_id: run_02
actual_session: 25b63893-2611-41ff-87d7-0b9f82cf0375
coord_session: 8d4e8b77-42a9-4bd3-bd5a-1b881e8d4bd5
host_cli_primary_executor: /home/sushaohua/.local/bin/codex (codex-cli 0.166.0)
host_default_model: gpt-6-luna
model_overrides_required: false
agy_cli_observed: /home/sushaohua/.local/bin/agy (1.4.12, interactive TUI host only)
status: completed-verification-evidence
authorization_ref:
  submission_id: SUB-20261103-001
  path: project-control/docs/evidence/coord_automation/phase1_prep_20261103/raw_submission_20261103_01.md
  sha256: f740af045cd3f6dc7d91bc05603849c8c12924e67c9e8e4e0eb4d7e585e944ac
consumed_inputs:
  handoff_rev2:
    path: project-control/docs/planning/coord_intake_dispatch_phase1_handoff_20261103.md
    revision: 2
    sha256: 400e61311c726663c8645a6237ad1084b19fb7b2d3c8b1850b4e20e59a91ab06
  design_rev2:
    path: project-control/docs/architecture/coord_intake_dispatch_phase1_design_20261103.md
    revision: 2
    sha256: 8a2984c6bb4b868cc8e2d6742873527f448f27c7006d99c5ce322207b2941350
  delivery_gate_rev5:
    path: project-control/.agents/rules/delivery_and_coord_gate.md
    revision: 5
    sha256: c48f91e65766da74813cb85bb6e90b286ce27f0ac297c7e95a48e95af17590a6
  codex_qa_rule:
    path: project-control/.agents/rules/codex_qa_review.md
    sha256: b7dfa803382ca6b5d21a6bdb13d345bb0e149226fd0b4c15494be318dd4624f2
  autorun_tasklist:
    path: project-control/docs/planning/coord_autorun_tasklist_20261029.md
    revision: 1
    sha256: f42dec024d6aae9f0e5e63cc6f6b09f46bd82f045134078c960e30a3369706cd
  autorun_queue:
    path: project-control/docs/planning/coord_autorun_queue_20261029.yaml
    sha256: 819fed4f9ca02149f2eafbc29bd27e76960d0075a25b3406ff76cb60be6d0ec1
smoke_test_threads:
  codex_readonly_and_resume_thread: 01a19fcc-2797-7742-8403-3fc4aa2de8b7
  codex_workspace_write_thread: 01a19fcd-0922-75d2-86c8-db2c1f497192
observed_repo_heads:
  workspace: 1e88c17a62bdcb63b4c0b78321eba3c44c3edc11
  project-control: b4af2d32601a07d448ac8d67a07c57f5b9ab36ac
  soc-ap: 427dd6d82caceebb7b4642e78f1dbfa96ff5fc84
  mcu-p3: e051111e68dd61896ed42c0961153b167b8bca41
  test_harness: ccf1476a0b98cb55ca9ee7bd49d73ca5d4704414
  boot/bootloadermc: 01bfda29b82f0576cb255d0b4196aeda1edb8d2e
  boot/bootloaderth: 1e4f592feaf400e5d4a1932db5aa86e75e60832b
verification_level: host-read-only-empirical-probe-and-cli-smoke-verified
---

# 三类人工入口自动调度第一阶段——宿主执行器、会话通道与运行接口核实报告（Revision 2）

> **Revision 2 勘误与关键修正声明（针对 `rev 1` SHA256 `83ec1682d9ec4286992c7fd167f52be04aa5958542e58b029159678d902f221e`）**：
> 1. **`rev 1` 误判根因**：`rev 1` 因观察到当前人工交互主会话（`8d4e8b77-42a9-4bd3-bd5a-1b881e8d4bd5`）运行在 `agy`（Antigravity CLI `1.4.12`）终端内，错误地将外部 `coord_runner` 的角色执行通道绑定到了 `agy -p`（`agy` 仅支持 Gemini/Claude/GPT-OSS 模型族，传 `--model gpt-6-luna` 会直接 `exit 1` 报错），进而错误提议申请 `gemini-4-argon-high` 模型覆盖。
> 2. **`rev 2` 历史溯源与实测更正**：经核查历史证据（`AUTO-02/runs/run_13`、`TWIN-01..35`、`issue_20261102_02..05`、`codex_adapter.py` 及宿主机 `~/.codex/state_5.sqlite` 中已有的 **66 次** `source='exec', model='gpt-6-luna'` 真实执行记录）并完成宿主机 CLI 实测冒烟，确认**本机通过命令行调用 `gpt-6-luna` 的标准执行器正是 `/home/sushaohua/.local/bin/codex exec -m gpt-6-luna`**（且 `~/.codex/config.toml` 已全局默认配置 `model = "gpt-6-luna"`）。
> 3. **全角色零覆盖结论**：`codex exec -m gpt-6-luna` 完整支持 `--sandbox read-only`、`--sandbox workspace-write`、`-C <workdir>`、`--add-dir`、`--json`、`--output-schema`、`-o <file>` 及 `codex exec --sandbox read-only resume <thread_id>`。**`COORD`、`PM`、`ARCH`、`ENG-*`、`INTEGRATOR`、`QA` 全角色均可 100% 统一通过 `/home/sushaohua/.local/bin/codex exec -m gpt-6-luna` 执行，完全不需要任何 `model_policy.approved_overrides` 模型覆盖**（工程作者会话与独立 QA / 非作者复核会话严格使用不同新建 `thread_id` 实现物理会话隔离）。

---

## 1. 历史证据溯源与宿主机真实执行器实测

### 1.1 历史命令行调用 `gpt-6-luna` 证据溯源

经只读检索 `project-control/tools/`、`project-control/docs/evidence/` 及宿主机 `~/.codex/` 非敏感元数据（跳过全部认证/密钥字段），核实此前命令行调用 `gpt-6-luna` 的完整链路如下：

1. **既有受控源码调用链（`project-control/tools/coord_runner/codex_adapter.py:14-15,100-106`）**：
   - 二进制路径：`DEFAULT_CODEX_BIN = Path("/home/sushaohua/.local/bin/codex")`（软链接指向 `/home/sushaohua/.codex/packages/standalone/current/bin/codex`，版本 `codex-cli 0.166.0`）。
   - 默认模型常量：`DEFAULT_MODEL = "gpt-6-luna"`。
   - 真实命令行模板：
     ```bash
     /home/sushaohua/.local/bin/codex exec --skip-git-repo-check \
       --sandbox read-only -c 'approval_policy="never"' \
       -m gpt-6-luna -C <workdir> --json \
       --output-schema <schema.json> --output-last-message <final.json> -
     ```
2. **历史工程与审查运行证据**：
   - `project-control/docs/evidence/coord_automation/AUTO-02/runs/run_13/result.md:45-48` 明确记录：“现场验证 `/home/sushaohua/.local/bin/codex` 指定 `-m gpt-6-luna` 真实调用可用。确立保存 `codex_session.jsonl` 真实事件流机制，绑定真实 `thread_id` 和 token 用量。”
   - `twin/TWIN-01/runs/run_02/result.md`、`twin/TWIN-02..35`、`issue_20261102_02..05`（及当前主会话 `transcript.jsonl` step `9519`, `9579`, `9639`）均通过 `codex exec ... --json -o <result_file> - < <prompt.txt> > <codex_session.jsonl>` 执行并归档会话 JSONL 物证。
3. **宿主机 `~/.codex/` 配置与历史会话持久化底座（实测只读查询）**：
   - `~/.codex/config.toml`（非敏感项）：已全局配置 `model = "gpt-6-luna"`、`model_reasoning_effort = "medium"`、`default_permissions = "workspace-custom"`，且对 `/home/sushaohua/workspace/ai_soc_project` 登记 `trust_level = "trusted"`。
   - `~/.codex/models_cache.json`：共缓存 10 个模型，原生包含 `gpt-6-luna`（显示名 `GPT-6-Luna`）。
   - `~/.codex/state_5.sqlite`（表 `threads`）：实测在此前任务中已累计持久化 **66 条** `model='gpt-6-luna' AND source='exec'` 的命令行独立会话记录（总线程数 138 条），表结构原生记录 `id` (`thread_id`)、`model`、`reasoning_effort`、`tokens_used`、`sandbox_policy`、`approval_mode`、`cwd`、`rollout_path`、`first_user_message`、`created_at_ms`、`updated_at_ms`。
   - 会话轨迹文件落盘路径：`/home/sushaohua/.codex/sessions/YYYY/MM/DD/rollout-<YYYY-MM-DDTHH-MM-SS>-<thread_id>.jsonl`（首行 `session_meta` 记录 `id`/`cwd`/`originator="codex_exec"`，每轮 `turn_context` 精确记录 `'model': 'gpt-6-luna'` 与 `sandbox_policy`），辅以 `~/.codex/session_index.jsonl`、`~/.codex/thread_history_1.sqlite` 及单线程写锁 `~/.codex/thread-writer-locks/<thread_id>.lock`。

### 1.2 宿主机 CLI 实测冒烟对比（`codex` vs `agy`）

全部冒烟文件仅写入本会话隔离 `scratch/` 目录，未触碰任何仓库业务文件：

| 实测项 | 真实执行命令 | 退出码 | 实测输出、线程 ID 与落盘证据 | 结论 |
| --- | --- | --- | --- | --- |
| **1. `codex exec` 只读结构化新建会话** | `/home/sushaohua/.local/bin/codex exec --skip-git-repo-check --sandbox read-only -c 'approval_policy="never"' -m gpt-6-luna -C /home/sushaohua/workspace/ai_soc_project --json --output-schema <schema.json> -o <final1.json> "Do not run any shell commands. Reply strictly with JSON {\"ok\": true, \"step\": \"init\"}."` | **`0`** | `final1.json`: `{"ok":true,"step":"init"}`；JSONL 返回 `thread_id="01a19fcc-2797-7742-8403-3fc4aa2de8b7"`，`usage={"input_tokens":16271,"output_tokens":19}`；落盘 `rollout-2026-11-03T13-05-19-01a19fcc-2797-7742-8403-3fc4aa2de8b7.jsonl`，其中 `turn_context` 实测 `'model': 'gpt-6-luna', 'sandbox_policy': {'type': 'read-only'}` | **通过**：可直接承载 `COORD` 决策、`PM`/`ARCH` 只读方案与审查、独立 `QA` 审计 |
| **2. `codex exec` 按 ID 只读恢复会话** | `/home/sushaohua/.local/bin/codex exec --sandbox read-only resume 01a19fcc-2797-7742-8403-3fc4aa2de8b7 --skip-git-repo-check -c 'approval_policy="never"' -m gpt-6-luna --json --output-schema <schema.json> -o <final3.json> "Do not run any shell commands. Reply strictly with JSON {\"ok\": true, \"step\": \"readonly_resumed\"}."` | **`0`** | `final3.json`: `{"ok":true,"step":"readonly_resumed"}`（此前第 2 轮已验证跨轮记忆返回 `"resumed_after_init"` 并命中 `cached_input_tokens: 16128`）；`turn_context` 实测保持 `'model': 'gpt-6-luna', 'sandbox_policy': {'type': 'read-only'}` | **通过**：可持久化恢复同一无头唯一 `COORD` 协调线程。<br>**关键语法细节**：`--sandbox read-only` 必须置于子命令 `resume` **之前**；若省略则会继承 `config.toml` 的 `workspace-custom` 可写权限 |
| **3. `codex exec` 受控工作区写入会话** | `/home/sushaohua/.local/bin/codex exec --skip-git-repo-check --sandbox workspace-write -c 'approval_policy="never"' -m gpt-6-luna -C <isolated_scratch_dir> --json --output-schema <schema.json> -o <final.json> "Write the text 'smoke_ok' to ./probe_out.txt ..."` | **`0`** | `final.json`: `{"ok":true,"wrote_file":"probe_out.txt"}`，`probe_out.txt` 实测内容 `smoke_ok`；`thread_id="01a19fcd-0922-75d2-86c8-db2c1f497192"`；`state_5.sqlite` 实测记录 `model='gpt-6-luna'`，且 `workspace-write` 策略自动将工作区内 `.git`、`.agents`、`.codex` 设为只读保护（`access: "read"`） | **通过**：可直接承载获批 `ENG-*` / `INTEGRATOR` 代码实现与本地自检，原生防止子会话私改 `.git` 元数据或 `.agents` 规则/任务卡 |
| **4. `agy` CLI 传入 `gpt-6-luna` 对照测试** | `/home/sushaohua/.local/bin/agy -p "Reply ok and call no tools" --mode plan --model gpt-6-luna --print-timeout 15s`（同时核查 `agy --help`、`agy models --help` 均 exit `0`） | **`1`** | stderr 原文：`error: invalid model selection (--model "gpt-6-luna" --effort ""): model gpt-6-luna is not recognized as a known model or custom model in settings`（`agy` `settings.json` 当前模型为 `"Gemini 4 Argon (High)"`）；另宿主机 Python `3.8.10` 未安装 `google.antigravity` SDK | **确认边界**：`agy` 仅作人工当前打开的交互式前端之一，**不作为 `coord_runner` 后台角色 CLI 执行器**，因此无需任何模型覆盖 |

### 1.3 交互式主会话（`agy` 或 `codex` TUI）与外部 `coord_runner` 的真实边界与互锁衔接

1. **进程与文件锁实测边界**：
   - 当前人工交互式 COORD 会话 `8d4e8b77-42a9-4bd3-bd5a-1b881e8d4bd5` 运行于 `PID 898692`（`agy --dangerously-skip-permissions`），持有 `/home/sushaohua/.gemini/antigravity-cli/presence/8d4e8b77-42a9-4bd3-bd5a-1b881e8d4bd5.lock`（inode `1562734`）的内核排他写锁（`/proc/locks`: `FLOCK ADVISORY WRITE 898692`），其内建 `invoke_subagent`/`send_message`/`schedule` 仅限该交互进程内部使用（会话轨迹位于 `~/.gemini/antigravity-cli/brain/<id>/.system_generated/logs/transcript.jsonl`）。
   - 外部独立 Python 进程 `coord_runner` 统一调用 `/home/sushaohua/.local/bin/codex exec -m gpt-6-luna`，走 `~/.codex/` 会话体系（`~/.codex/thread-writer-locks/<thread_id>.lock` + `state_5.sqlite`），**与人工 `agy` TUI 进程完全无底层数据库/锁冲突**。
2. **唯一 COORD 协调权互锁与衔接协议（防止双协调者并存）**：
   - **唯一运行锁**：`coord_runner` 启动时先对 `/home/sushaohua/.local/share/ai_soc_coord_runner/coord_runner.lock` 获取内核非阻塞排他锁 `fcntl.flock(LOCK_EX | LOCK_NB)`；第二个调度进程启动时立即退出或仅投递唤醒信号（满足设计 §7.2）。
   - **人工交互会话与自动运行器的分工衔接**：
     - 人工（或交互主会话助手）负责将原始指令归档至 `docs/work_intake/submissions/`、在审查确认单后将人工批准记录写入 `docs/work_intake/approvals/`，并在第 1 步按需触发 `python3 -m coord_runner --once`。
     - 进入第 2/3 步后，`coord_runner` 持有受控 `active_coord_thread_id`（`codex exec -m gpt-6-luna` 只读决策线程，在 SQLite 中关联来源交互会话 `8d4e8b77-42a9-4bd3-bd5a-1b881e8d4bd5` 形成可审计血缘链）；交互会话不再绕过 `coord_runner` 直接手改受管任务状态，且 `coord_runner` 每次写卡/写队列前强制执行磁盘字节 SHA256 乐观锁（Compare-And-Swap）比对，一旦发现人工并发修改立即停止覆盖并转入冲突对账（满足 P1-13）。

---

## 2. 现有 `coord_runner` 缺口与设计 §6 四接口真实落点分析（全量 `codex exec -m gpt-6-luna`）

### 2.1 `coord_runner` 现状源码核对与关键缺口

| 模块与源码行号 | 当前真实行为 | 与第一阶段设计 rev 2 的核心差距 |
| --- | --- | --- |
| `CoordRunner.default_agent_executor`<br>`project-control/tools/coord_runner/runner.py:412-424`（含 `_resolve_task_repo` `L389-396`、`_verify_server_commit` `L398-410`） | 仅按任务 ID 前缀映射到 4 个仓库目录，运行 `git rev-parse HEAD` 并核验远端存在后直接返回当前 `HEAD` | **未启动任何真实角色会话**，无提示词/白名单/异步 job，不支持 `boot/*` 仓或 PM/ARCH 确认单生成；必须替换为真实 `CodexRoleAdapter` |
| `CoordRunner.default_qa_executor`<br>`runner.py:426-443`、`qa_contract.py:63-90`、`codex_qa.py:68-119` | 调用 `qa_runner.py` 在独立 Docker 容器内从服务器拉取锁定 commit 构建测试，校验 `server_qa.json` 与 `container_inspect` | **机制合规且直接复用**；需由同步阻塞 `subprocess.run`（`codex_qa.py:103`）外置为异步受管作业以防阻塞其他就绪任务 |
| `CoordRunner.default_review_executor`<br>`runner.py:445-458`、`review_bundle.py:148-167`、`codex_adapter.py:100-136` | 调用 `/home/sushaohua/.local/bin/codex exec --skip-git-repo-check --sandbox read-only -c approval_policy="never" -m gpt-6-luna --json --output-schema ...` 执行独立 QA 审计与非作者 ARCH 报告复核 | **命令与模型完全正确且直接复用**；同样需把同步 `subprocess.run`（`codex_adapter.py:113`）改为异步可查询作业 |
| 调度循环、检查点与租约<br>`runner.py:306-320,468-522`、`scheduler.py:28-90`、`checkpoint.py:20-51`、`lease_manager.py:41-80` | 只读静态队列 `bootstrap + order`；`scheduler.py:81-83` 遇 `Done` 不验 `done_acceptance_errors`；无 `flock`；`prune_expired_leases` 到期直接释放而不查宿主进程；错误写往 `/tmp` | 需补齐 `docs/work_intake/` 收件与审批绑定、SQLite 运行库 + `flock` 单实例、异步作业轮询、租约过期宿主存活对账及正式任务卡 CAS 回写 |

### 2.2 设计 §6 四接口真实落点（统一使用 `/home/sushaohua/.local/bin/codex` + `-m gpt-6-luna`）

1. **`coordinate(request) -> DecisionResult`**
   - **零变化短路**：先计算 `submissions/`、`approvals/`、在途作业回执及到期定时器的聚合摘要；若与上一轮已处理摘要相同，**直接返回 `NOOP`，零模型调用**（满足 P1-14）。
   - **真实调用命令（100% 物理只读沙箱 + `gpt-6-luna`）**：
     - 首次创建受控无头 COORD 协调线程：
       ```bash
       /home/sushaohua/.local/bin/codex exec --skip-git-repo-check \
         --sandbox read-only -c 'approval_policy="never"' \
         -m gpt-6-luna -C /home/sushaohua/workspace/ai_soc_project --json \
         --output-schema <decision_schema.json> -o <decision_out.json> - < <prompt.txt>
       ```
     - 后续增量唤醒同一唯一 COORD 线程（`--sandbox read-only` 置于 `resume` 前）：
       ```bash
       /home/sushaohua/.local/bin/codex exec --sandbox read-only resume <active_coord_thread_id> \
         --skip-git-repo-check -c 'approval_policy="never"' \
         -m gpt-6-luna --json \
         --output-schema <decision_schema.json> -o <decision_out.json> - < <delta_prompt.txt>
       ```
   - **确定性程序门禁**：校验 `<decision_out.json>` 严格匹配 `decision_schema.json`，核对输入版本哈希、人工 `approval_refs` 精确版本映射与路径白名单；未获批准的实现动作一律拦截。

2. **`submit_role_task(request, dispatch_key) -> JobHandle`**
   - **写前意图登记（WAL Intent）**：在 `~/.local/share/ai_soc_coord_runner/state.sqlite3` 的 `role_jobs` 表插入唯一主键 `dispatch_key = sha256(task_id:task_revision:role:phase:input_sha256:attempt)`（初始状态 `SUBMITTING`），创建 `<runtime_dir>/jobs/<job_id>/`，并在 `prompt.txt` 第一行固定写入唯一对账锚点 `[COORD_DISPATCH_KEY:<dispatch_key>]`。
   - **异步后台派生（`job_launcher.py`，`start_new_session=True`，绝不阻塞调度主线程）**：
     - **`PM` / `ARCH` 需求确认单、澄清与实施概要编制**（只读沙箱生成结构化 JSON/Markdown 内容，由控制器校验白名单后原子落盘至 `docs/work_intake/confirmations/`）：
       ```bash
       /home/sushaohua/.local/bin/codex exec --skip-git-repo-check \
         --sandbox read-only -c 'approval_policy="never"' \
         -m gpt-6-luna -C /home/sushaohua/workspace/ai_soc_project --json \
         --output-schema <plan_schema.json> -o <job_dir>/final.json \
         - < <job_dir>/prompt.txt > <job_dir>/codex_events.jsonl 2> <job_dir>/stderr.log
       ```
     - **获批工程角色（`ENG-*` / `INTEGRATOR` 代码实现与作者自检）**（每次独立新建 `codex exec` 会话，不复用 COORD 线程）：
       ```bash
       /home/sushaohua/.local/bin/codex exec --skip-git-repo-check \
         --sandbox workspace-write -c 'approval_policy="never"' \
         -m gpt-6-luna -C <target_repo_dir> [--add-dir <extra_allowed_dir>] --json \
         --output-schema <delivery_schema.json> -o <job_dir>/final.json \
         - < <job_dir>/prompt.txt > <job_dir>/codex_events.jsonl 2> <job_dir>/stderr.log
       ```
       > 实测确认：`--sandbox workspace-write` 原生保护 `<target_repo_dir>/.git` 与 `.agents` 为只读（`access: "read"`），工程作者只能在受控工作区改业务源码并跑本地编译/单测自检；完成后由控制器审计改动文件 100% 落在任务卡 `allowed_paths` 白名单内，再由受控 `INTEGRATOR` 交付包装步骤执行单逻辑 Git commit/push 并向远端 `git ls-remote origin` 对账。
     - **正式独立 QA 与非作者报告复核**：异步调用既有 Docker `qa_runner.py` 产出 `server_qa.json`，再启动**全新独立 `thread_id`** 的宿主机 `codex exec --sandbox read-only -m gpt-6-luna`（严禁 `resume` 作者线程，强制校验 `reviewer_thread_id != author_thread_id` 且 `report_reviewer_thread_id not in {author_thread_id, qa_thread_id}`）。
   - **返回标识**：包装器启动子进程后立即原子写入 `<job_dir>/pid.json`（含 `pid` 与 `/proc/<pid>/stat` 第 22 字段 `pid_starttime`），返回 `JobHandle(job_id, dispatch_key, pid, pid_starttime, job_dir)`，控制器立即返回主循环继续推进其他无资源冲突的就绪任务（满足 P1-08）。

3. **`query_role_job(job_id_or_dispatch_key) -> JobStatus`**
   - **五源确定性交叉对账**：
     1. **控制器运行库**：查询 `state.sqlite3` `role_jobs` 记录。
     2. **OS 进程精确身份**：读取 `/proc/<pid>/stat`，核对 `starttime == recorded_pid_starttime` 且状态非僵尸 `Z`（防 PID 回绕误判）。
     3. **作业事件流日志**：读取 `<job_dir>/codex_events.jsonl` 提取首包 `thread.started.thread_id` 与末包 `turn.completed.usage`。
     4. **Codex 宿主状态库与 Rollout 轨迹只读核验**：通过只读 URI `file:/home/sushaohua/.codex/state_5.sqlite?mode=ro` 查询 `threads` 表中对应 `id = <thread_id>` 的 `model`（核验实为 `'gpt-6-luna'`）、`tokens_used`、`rollout_path`，并核对 `~/.codex/sessions/YYYY/MM/DD/rollout-*-<thread_id>.jsonl` 的 `turn_context.model == 'gpt-6-luna'`。
     5. **原子退出回执**：检查包装器在进程退出时原子落盘的 `<job_dir>/exit_status.json`（含 `exit_code`, `finished_at`, `final_sha256`）。
   - **返回状态**：`RUNNING`、`FINISHED_PENDING_COLLECT`、`FAILED`、`LAUNCH_UNKNOWN`、`NOT_FOUND`。租约过期时必须先调 `query_role_job`：只要旧作业仍为 `RUNNING` 或 `LAUNCH_UNKNOWN`，资源锁保持占用待核实，绝不释放给另一任务（满足设计 §7.2 与 P1-10）。

4. **`collect_role_result(job_id) -> VerifiedRoleDelivery`**
   - 读取并核验 `<job_dir>/exit_status.json`、`final.json`、`codex_events.jsonl` 及宿主 `rollout-*.jsonl` 证据哈希；
   - 强制校验：(a) `actual_model == "gpt-6-luna"` 且 `thread_id` 真实非空；(b) `final.json` 满足输出 schema 且绑定的 `(task_id, task_revision, dispatch_key)` 一致；(c) 进程 `exit 0` 但无有效候选/产物或校验不通过时，一律判阻塞/失败，绝不写 `Done`（满足 P1-11）；(d) 代码任务须通过白名单 diff 校验、远端 `git ls-remote origin` 40 位 SHA 对账及后续独立 Docker + 独立 Codex QA + 非作者报告复核门禁后，才由唯一 COORD 推进任务卡状态。

### 2.3 三步演进路径与“派单超时 / 崩溃结果未知（`LAUNCH_UNKNOWN`）”宿主机级防重机制

- **分段落地**：
  1. **第 1 步（手动单步 `coord_runner --once`）**：人工提交 MD 指令至 `submissions/` -> `coord_runner --once` 调 `codex exec -m gpt-6-luna` 生成确认单与分类 YAML -> 人工批次批准写入 `approvals/` -> 再次 `--once` 拆卡登记并异步启动获批角色作业/收取已完成结果。
  2. **第 2 步（持续推进与恢复 `coord_runner --daemon --poll-interval 5`）**：异步并行推进无冲突就绪卡（P1-08），演练重复扫描、进程 `SIGKILL` 崩溃恢复、双实例拦截、租约活跃保护与写冲突保护（P1-05～P1-13）。
  3. **第 3 步（定时服务 `systemd --user`）**：由 INTEGRATOR 在第 1、2 步独立验收通过后部署单个用户态 `coord-runner.service` 托管同一 `--daemon` 入口，无变化零模型调用（P1-14）。
- **`LAUNCH_UNKNOWN` 宿主机数据库级防重对账（实测已验证）**：
  - 实测证实 `/home/sushaohua/.codex/state_5.sqlite` 的 `threads` 表在会话启动瞬间即持久化 `first_user_message` 列（本次冒烟实测精确读回 `'Do not run any shell commands. Reply strictly with JSON {"ok": true, "step": "init"}.'`）。
  - 因此，即使控制器在 `SUBMITTING` 阶段尚未写回 `pid.json` 就遭遇超时或 `SIGKILL` 崩溃，恢复对账器只需：
    1. 检查 `<job_dir>/pid.json` / `exit_status.json` 及 `/proc/[0-9]*/cmdline`（匹配 `<job_dir>/final.json`）；
    2. 只读查询 `file:/home/sushaohua/.codex/state_5.sqlite?mode=ro`：`SELECT id, model, rollout_path FROM threads WHERE first_user_message LIKE '[COORD_DISPATCH_KEY:' || ? || ']%'`！
  - 若命中记录，直接绑回真实 `thread_id` 与 `rollout_path` 转入追踪或结果回收；若未命中且 `<job_dir>` 无输出、目标仓库工作树干净，可确证未启动；若工作树存在不明改动无法确认，则标为 `RECONCILE_REQUIRED`（派单待核实）冻结重发并继续其他无关就绪任务（满足设计 §6 与 P1-09）。

---

## 3. 定时运行环境与单实例底座核查

本轮仅执行只读探测，未创建任何服务目录、单元文件或改动系统设置：

| 核查项 | 实测只读命令 | 退出码 | 实测结果与第 3 步部署事实 |
| --- | --- | --- | --- |
| **`systemd --user` 版本与用户总线** | `systemctl --user --version && systemctl --user show-environment >/dev/null && systemctl --user is-system-running` | `0` | `systemd 245 (245.4-4ubuntu3.24)`；用户 D-Bus 可达，`is-system-running` 返回 **`running`**；`/run/user/1000` 正常挂载；`~/.config/systemd/user` 待第 3 步部署时按需创建 |
| **账户 Linger 与 WSL2 宿主边界** | `loginctl show-user "$USER" -p Linger -p State -p Sessions; uname -r; sudo -n true` | `0` | `State=active`、`Sessions=1`、**`Linger=no`**（`/var/lib/systemd/linger` 为空）；内核为 `6.18.33.2-microsoft-standard-WSL2`，当前账户具备免密 sudo（`sudo_nopasswd=yes`）。第 3 步获批部署时可执行 `sudo loginctl enable-linger sushaohua`，并如实记录 WSL2 宿主关闭全部终端且无保活时 VM 休眠的边界 |
| **既有 Crontab 保护** | `crontab -l` | `0` | 存在用户既有任务 `0,30 * * * * /bin/bash /home/sushaohua/scripts/sync_md.sh`。第 3 步采用单个 `systemd --user` service 管理轮询，**严禁修改或覆盖用户既有 crontab** |
| **持久化可写运行目录候选** | `ls -ld "$HOME/.local/share"; df -h "$HOME/.local/share"` | `0` | `/home/sushaohua/.local/share` 归属 `sushaohua:sushaohua`，位于 `/dev/sdd`（总计 `1007G`，可用 **`820G`**，已用 `15%`），持久化且位于所有 Git 仓库之外。选定 **`/home/sushaohua/.local/share/ai_soc_coord_runner/`** 存放 `state.sqlite3`、`coord_runner.lock` 与 `jobs/` |
| **Python `sqlite3` 与 `fcntl.flock`** | `python3 -c "import sqlite3, fcntl; print(sqlite3.sqlite_version, hasattr(fcntl, 'flock'))"` | `0` | Python `3.8.10` 内置 `sqlite3` **`3.31.1`**，`fcntl.flock` 为 **`True`**，完全满足无外部中间件的事务存储与内核级进程排他锁要求 |

---

## 4. 存量任务与成果保护核查

### 4.1 队列、`AUTO-01/02`、在途任务与未提交工作区现状

1. **任务图与现有队列只读核查**：
   - `PYTHONDONTWRITEBYTECODE=1 python3 project-control/tools/check_task_graph.py --workspace .` -> **退出码 `0`**（130 张规范卡、88 张微任务卡，零结构错误、零循环依赖）。
   - `--check-done AUTO-01`、`--check-done AUTO-02`、`--check-done TWIN-01` -> **退出码均为 `0`**。`AUTO-01`（候选 `38064f1f...`）与 `AUTO-02`（候选 `0a3b1a4c...`，`run_13` QA `01a18780-...` 与 ARCH `01a18782-...` 签署 `APPROVED`）历史证据完整保留，其批准范围限于锁定软件候选测试，不替代本阶段三类人工入口宿主派发与常驻验收。
   - `coord_queue.py --workspace .` -> **退出码 `0`**，`runner_status: "not-deployed"`（`coord_state.json` 不存在），`next` 指向 `TWIN-15`（`reconcile-evidence`：`coord_autorun_queue_20261029.yaml` 22 张卡中 11 张 `Done` 且 `done_errs=0`，`TWIN-15..12` 共 8 张存在历史报告哈希/证据引用待对账项，`TWIN-13/14` 为 `Backlog` 且 `blocked=True`）。全仓另有 `MS-22`（`Verify`）与 `TWIN-36..40`（`Review`）处于非 `Done` 状态。
2. **各仓库未提交工作区差异核查（`git status -sb`）**：
   - **总仓（`workspace`）**：`.gitignore`、`AGENTS.md`、`WORKSPACE.md` 已修改未提交，`.vscode/` 未跟踪。
   - **`project-control`**：7 个规则/模板/指南/清单文件已修改未提交，另有 `bootloader_role_*`、第一阶段设计单/交接单/确认单及 `docs/evidence/coord_automation/phase1_prep_20261103/` 未跟踪。
   - **`boot/bootloadermc`、`boot/bootloaderth`**：各含本机未跟踪 `.agents`、`AGENTS.md`、`docs`。
   - **`soc-ap`、`mcu-p3`、`test_harness`**：工作区完全干净。

### 4.2 零破坏隔离建议

1. **前置基线固化与未提交改动保护**：开工实现前先将 `project-control` 已获确认的规则与设计/交接文档按单逻辑提交推送形成干净服务器基线，或将非本票改动列入写保护黑名单；**严禁执行 `git checkout -- .`、`git reset --hard`、`git clean -fd` 或 `git add -A`**。
2. **保留 `AUTO-01/02` 原件，新建兼容任务编号**：不修改、不重开 `AUTO-01`/`AUTO-02` 及其历史证据；新微任务建议采用 `check_task_graph.py:87` `is_microtask()` 原生支持的 `AUTO-03+` 前缀（或在获批白名单内显式扩展前缀并补单测），通过 `depends_on: [AUTO-02]` 关联可复用运行器底座。
3. **三类新入口与历史 `coord_autorun_queue_20261029.yaml` 隔离**：新运行器默认仅消费经 `work_intake` 审批释放的任务队列，**不自动遍历重跑旧 `coord_autorun_queue_20261029.yaml` 中的历史 TWIN 卡**（同时补齐 `scheduler.py` 对前置 `Done` 卡的 `done_acceptance_errors` 校验）。
4. **写前 SHA256 CAS 乐观锁与运行态外置**：回写任何任务卡或索引文件前强制核验磁盘 SHA256 未变；SQLite、锁文件与作业日志统一外置到 `/home/sushaohua/.local/share/ai_soc_coord_runner/`，保持 Git 工作树纯净。
