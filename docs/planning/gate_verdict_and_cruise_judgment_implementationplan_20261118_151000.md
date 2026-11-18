# 四阶门禁三态裁决与批次巡航判定改进实施方案

## 修订历史

| 版本 | 修订时间 | 修订人 | 变更摘要 | 审批状态 |
| :--- | :--- | :--- | :--- | :--- |
| `v1.0` | `2026-11-18` | `AI (Antigravity-CLI) - COORD` | 补齐四阶门禁三态裁决（`PASSED`/`FAILED`/`BLOCKED`）、当次 `file://` 证据链接、巡航防假绿及阻塞零扣返修简版方案 | 已批准执行 (Approved) |
| `v1.1` | `2026-11-18` | `AI (Antigravity-CLI) - COORD` | 完成 4 个工具脚本改造，通过 `test_qa_runner + test_v2_gates` 48 项单测、`fast_gate` 及 CLI 三态 (`0/1/2`) 实跑校验并归档证据至 `docs/evidence/gate_cruise_v2_20261118/` | 已结项 (SW-Verified) |

---

## 1. 目标与非干扰声明

1. **核心目标**：沿用既有 **四阶无状态门禁**（`fast_gate` ➔ `integration` ➔ `docker_qa` ➔ `codex`），实现：
   - 门禁输出明确三态 **`PASSED` / `FAILED` / `BLOCKED`**，汇报聚焦 **结果、原因、下一步**，并附带本次运行的 `file://` 证据链接；
   - 巡航按真实退出码与 `verdict.json` 推进，杜绝非零退出被误判绿灯；权限拒绝或环境/沙箱/工具阻塞严格走 `BLOCKED` 停机，**零消耗工程 `ENG-*` 2 轮返修次数**；
   - 账本断点跳过校验完整输入指纹（对齐 [delivery_and_coord_gate.md](../../.agents/rules/delivery_and_coord_gate.md) 与 [codex_qa_review.md](../../.agents/rules/codex_qa_review.md)）。
2. **现行任务零中断**：本方案仅规划修改 `project-control/tools/` 下 4 个脚本，不触碰 `tools/qa_runner/`、`Dockerfile.toolchain`、运行中进程/容器、`mc_th_upgrade` 历史证据及暂缓的 HelixScreen 方案；审批与实施均无需中断现有任务。

---

## 2. 经代码核实的现状缺陷

| 问题 | 代码位置（已物理核实） | 缺陷根因与危害 |
| :--- | :--- | :--- |
| **巡航失败误报绿与权限误扣次** | `project-control/tools/workflow/run_slice_batch.py:72-83` | `call_tool("run_command", ...)` 子进程失败时返回含 `Command exited with code N.` 的文本而非抛异常，`L73-75` 直接打印 `门禁全绿 SW-Verified` 并推进；权限拒绝（`ToolError.denied`）或环境报错也被 `except Exception` 捕获并消耗 `ENG-*` 返修次数。 |
| **账本跳过忽略输入变化** | `project-control/tools/workflow/run_slice_batch.py:20,91,95` | `parse_verified_slices()` 只匹配 `slice_id`，未核对 `inputs=<input_fingerprint>` 与 `slices/<SLICE>.yaml` 当前输入指纹。 |
| **门禁缺三态区分与全阶段证据归档** | `project-control/tools/gates/slice_gate.py:84-96,131-156` | 第 1/2 阶失败不生成 `verdict.json`；第 3 阶无 `server_qa.json`（如未 push/SSH/Docker 异常）与容器测试 `passed=false` 均裸抛 `RuntimeError`；返回值与终端输出缺 `next_step` 与当次 `file://` 证据索引。 |
| **Codex 环境阻塞未分层** | `project-control/tools/gates/codex_review.py:101-120` | CLI 缺失、超时、`thread.started` 缺失等环境/工具问题均抛通用 `RuntimeError`，无法在 `slice_gate.py` 中与真实 `BLOCKER` 拒单区分。 |
| **既有自检行数预算漂移** | `project-control/tools/test_v2_gates.py:54` | 实测 `wc -l` 既有 7 文件共 `936` 行，导致 `<= 900` 断言当前 `FAILED (failures=1)`；且巡航单测桩以抛异常代替了 `run_command` 真实输出文本。 |

---

## 3. 最小修改方案与 Diff Budget（仅限 4 文件，0 业务仓改动）

| 目标文件 | 精确修改内容 | 函数/规模约束 |
| :--- | :--- | :--- |
| **`project-control/tools/gates/codex_review.py`** | 1. 新增 `CodexGateBlockedError`（附带 `reason` 与 `out_dir` 日志路径）；<br>2. Codex CLI 不可用、进程超时（`subprocess.TimeoutExpired`）、无 `thread.started`/非正常退出或无效输出时抛出 `CodexGateBlockedError`，保留 `decision == "BLOCKED"` 正常返回供上层统一裁决。 | 单函数 `<= 50` 行、`<= 4` 参数、全中文 docstring |
| **`project-control/tools/gates/slice_gate.py`** | 1. 保持 `fast_gate -> integration -> docker_qa -> codex` 顺序与 `ledger.md` 写入规则（仅完整四阶 `PASSED` 且 `decision == "APPROVED"` 时写入 `SW-Verified`）；<br>2. 任何阶段结束（含第 1~3 阶失败/阻塞及 `--fast-only`）均写 `out_dir/verdict.json`（含 `status`: `PASSED`/`FAILED`/`BLOCKED`/`FAST-PASSED`、`stage`、`reason`、`next_step`、`input_fingerprint`、`evidence` 当次 `file://` 路径映射、`verdict_sha256`）；<br>3. 第 3 阶无有效 `server_qa.json` 或捕获 Docker/SSH/Git 远端错误，以及第 4 阶 `CodexGateBlockedError` / `decision == "BLOCKED"` 均归类为 **`BLOCKED`（退出码 `2`）**；真实校验/测试/`BLOCKER` 拒单归类为 **`FAILED`（退出码 `1`）**；全绿归类为 **`PASSED`（退出码 `0`）**；<br>4. 仅扫描本次 `--out-dir` 实际生成的文件生成 `file://` 证据链接，严禁引用未入列或旧次目录；精简输出为 `{status, stage, reason, next_step, evidence, verdict_sha256}`。 | 单函数 `<= 50` 行、`<= 4` 参数、全中文 docstring |
| **`project-control/tools/workflow/run_slice_batch.py`** | 1. 新增退出码与真实 `out_dir/verdict.json` 双重解析校验（严格核对 `slice_id`、`input_fingerprint` 与 `status`），杜绝非零输出字符串误报通过；<br>2. 仅 `status == "FAILED"` 时按 `remediation_used` 上限 `2` 轮唤醒原 `ENG-*` 修复并只递交 `{reason, next_step, evidence}` 摘要指针；若 `status == "FAILED"` 但无 `subtasks` 或超 `2` 轮，立即 `RuntimeError` 停机；<br>3. 遇 `status == "BLOCKED"`、`verdict.json` 缺失/指纹不一致或 `ToolError.denied == True`，立即停机返回 `BLOCKED` 摘要，**绝不递增返修次数、不唤醒 `ENG-*`**；<br>4. 续跑前比对 `ledger.md` 对应 `slice_id` 行 `inputs=<fingerprint>` 与当次 `slice_gate.input_fingerprint()`，一致才跳过；汇报输出固定三段：**结果 / 原因 / 下一步 + 当次证据 `file://` 链接**。 | 单函数 `<= 50` 行、`<= 4` 参数、全中文 docstring |
| **`project-control/tools/test_v2_gates.py`** | 1. 将总行数自检调整为**生产 6 文件 `<= 900` 行、含单测总计 `<= 1150` 行**（单函数 `<= 50` 行、入参 `<= 4`、中文注释约束保持不变）；<br>2. 新增测试：① `run_command` 返回 `"Command exited with code 1."` 时绝不判通过；② `BLOCKED` 与 `ToolError(denied=True)` 均直接停机且 **`ENG` 返修次数 = 0**；③ 第 1/2/3/4 阶 `FAILED`/`BLOCKED`/`PASSED` 均写 `verdict.json` 并附带当次真实存在的 `file://` 链接与退出码 `0/1/2`；④ `inputs=` 指纹变更时不误跳过 `ledger.md`。 | 与上面共享同一组门禁校验 |

> **Diff Budget**：`project-control/tools/` 内精确 **4 个文件**，生产 6 文件总行数控制于 `<= 900` 行；`printer-soc` / `mcu-p3` / `test_harness` / `boot/*` / `agents` / `sdk/c308l` **`0` 改动**。

---

## 4. 验收命令与回滚预案

1. **宿主全量门禁与单测**：
   - `python3 -m unittest discover -s project-control/tools -p "test_*.py"`（全部通过，0 failed / 0 skipped）。
   - `python3 project-control/tools/gates/fast_gate.py --workspace . --files project-control/tools/gates/codex_review.py project-control/tools/gates/slice_gate.py project-control/tools/workflow/run_slice_batch.py project-control/tools/test_v2_gates.py`（退出码 `0`）。
2. **三态实跑验证（临时只读/隔离切片目录 `/tmp/`，不污染 `slices/` 与 `ledger.md`）**：
   - 使用隔离 `--out-dir` 实跑并核验：`fast_gate` 失败（`exit 1`, `status="FAILED"`）；`docker_qa` 未推送/环境阻断（`exit 2`, `status="BLOCKED"`）；`--fast-only`（`exit 0`, `status="FAST-PASSED"`, `ledger.md` 无新增）；`verdict.json` 均含当次有效 `file://` 链接。
3. **回滚预案**：若任何门禁兼容性异常，直接执行 `git -C project-control checkout -- tools/gates/codex_review.py tools/gates/slice_gate.py tools/workflow/run_slice_batch.py tools/test_v2_gates.py` 即可单仓零残留恢复。
