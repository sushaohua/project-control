# 四阶门禁三态裁决与批次巡航判定改进实施方案

## 修订历史

| 版本 | 修订时间 | 修订人 | 变更摘要 | 审批状态 |
| :--- | :--- | :--- | :--- | :--- |
| `v1.0` | `2026-11-18` | `AI (Antigravity-CLI) - COORD` | 补齐四阶门禁三态裁决（`PASSED`/`FAILED`/`BLOCKED`）、当次 `file://` 证据链接、巡航防假绿及阻塞零扣返修简版方案 | 已批准执行 (Approved) |
| `v1.1` | `2026-11-18` | `AI (Antigravity-CLI) - COORD` | 完成 4 个工具脚本改造，通过 `test_qa_runner + test_v2_gates` 48 项单测、`fast_gate` 及 CLI 三态 (`0/1/2`) 实跑校验并归档证据至 `docs/evidence/gate_cruise_v2_20261118/` | 已结项 (SW-Verified) |
| `v1.2` | `2026-11-18` | `AI (Antigravity-CLI) - COORD` | 针对 `6d52ac8f` 复核执行三项返修：后台门禁等待结束并读真实退出码、缺失 `verdict.json` 统一 `BLOCKED` 零扣次、每次运行独立证据目录与 Docker QA/巡航退出码证据强一致门禁，并完成真实 `agy` 运行时全链路与冲突补测 | 返修执行中 |

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
| **`project-control/tools/gates/slice_gate.py`** | 1. 保持 `fast_gate -> integration -> docker_qa -> codex` 顺序与 `ledger.md`（支持可选 `ledger_ref` 隔离回归）写入规则；<br>2. 拒绝复用已有非空 `--out-dir`（命中直接 `BLOCKED(2)`），杜绝覆写历史证据；<br>3. 第 3 阶 Docker QA 必须同时满足 `proc.returncode == 0` 且当次 `server_qa.json`（`passed=True`、`fresh_checkout=True`、`task_id`）、`server_verdict.json`（`PASSED/0` 及 `SHA256`）与 `server_lock.json`（锁定提交及 `SHA256`）全量一致才准推进，退出码与证据冲突一律 `BLOCKED(2)`；<br>4. 任何阶段结束均写 `out_dir/verdict.json`，仅扫描当次 `--out-dir` 实际产出生成 `file://` 证据链接。 | 单函数 `<= 50` 行、`<= 4` 参数、全中文 docstring |
| **`project-control/tools/workflow/run_slice_batch.py`** | 1. 每次运行通过时间戳 + UUID 分配全局唯一 `out_rel`，重启续跑绝不复用旧目录；<br>2. 命令转入后台后轮询 `manage_task`（支持终态等待与原子 `gate_exit.rc` 落盘核验）直至真实结束再读取实际退出码和 `verdict.json`；<br>3. 缺失 `verdict.json`（不论退出码）及退出码与 `verdict.json` 状态冲突均统一判 **`BLOCKED`**，**绝不派发 `ENG-*` 返修、零扣减次数**；仅合法 `FAILED(1)` 才消耗最多 `2` 轮返修。 | 单函数 `<= 50` 行、`<= 4` 参数、全中文 docstring |
| **`project-control/tools/test_v2_gates.py`** | 1. 保持生产 6 文件 `<= 900` 行、含单测总计 `<= 1150` 行硬约束；<br>2. 修正缺失 `verdict.json` 预期为 `BLOCKED` 且 `remediation_used=0`；补测后台门禁等待结束、`run_slice_batch` 与 `slice_gate` 双层退出码与证据冲突、非空证据目录拒复用及重启独立目录隔离。 | 与上面共享同一组门禁校验 |

> **Diff Budget**：`project-control/tools/` 内精确 **4 个文件**，生产 6 文件总行数控制于 `<= 900` 行；`printer-soc` / `mcu-p3` / `test_harness` / `boot/*` / `agents` / `sdk/c308l` **`0` 改动**。

---

## 4. 验收命令与回滚预案

1. **宿主全量门禁与单测**：
   - `python3 -m unittest discover -s project-control/tools -p "test_*.py"`（全部通过，0 failed / 0 skipped）。
   - `python3 project-control/tools/gates/fast_gate.py --workspace . --files project-control/tools/gates/codex_review.py project-control/tools/gates/slice_gate.py project-control/tools/workflow/run_slice_batch.py project-control/tools/test_v2_gates.py`（退出码 `0`）。
2. **真实 `agy` 运行时与双端负例补测（全新独立证据目录 `docs/evidence/gate_cruise_rework_20261118_*`）**：
   - `run_workflow` 真实触发门禁转后台 ➔ 轮询等待至结束 ➔ 读取实际退出码与当次 `verdict.json` 正常通过；
   - 补测缺 `verdict.json` 判 `BLOCKED`（零返修扣次）、退出码与 `verdict.json` / Docker QA 证据冲突判 `BLOCKED`、以及独立目录隔离与重启不复用。
3. **回滚预案**：若任何门禁兼容性异常，直接执行 `git -C project-control checkout -- tools/gates/codex_review.py tools/gates/slice_gate.py tools/workflow/run_slice_batch.py tools/test_v2_gates.py` 即可单仓零残留恢复。
