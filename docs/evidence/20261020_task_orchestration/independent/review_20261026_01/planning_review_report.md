---
doc_id: REVIEW-MINIMC-V2-PLANNING-20261026-01
title: MiniMCProto v2.0 首个离线协议增量（25 张微步任务卡编排）独立审阅报告
reviewer_session: independent-subagent-session-663fcda3-b02b-4d3a-89f6-ffc1ef283810
reviewer_role: QA / Independent Planning Reviewer (isolated subagent context)
author_under_review: Codex 主对话 /root（2026-10-20 编排批次）及主会话 COORD 修订
receiver_session: parent-coord-session-9e5411f4-acad-421e-b487-9e68b9483320
initial_reviewed_at: '2026-10-26T13:44:30+08:00'
reverified_at: '2026-10-26T13:57:30+08:00'
timezone: 北京时间（UTC+8）
reviewed_control_head: 770bc8433462388132493c3cfca007d5dbf185e0
reviewed_baseline_commit: 517ba18dc9b3ecd9893680b60d7bcaf0ff873e18
reviewed_worktree_tracked_diff_sha256: db0db071ffe29aa4017dc49fe2c7d00e669cc632694b2ef855a1efb4b485511b
reviewed_modified_file_hashes:
  .agents/kanban/microtasks/minimc_v2/V2-P05B.md: d937a740bd1e7a0b1553198fb2a448ccd984e0a0cbfde9252fb0117475cd0f36
  tools/check_task_graph.py: 4d56947e496fea6cd69b4c7b41a8192bf7f7eafbb91f402226e0e597a50bf953
initial_decision: changes_requested
decision: plan_structure_accepted_pending_dispatch
scope: planning-structure-only; not protocol implementation acceptance or MS HIL completion
---

# MiniMCProto v2.0 首个离线协议增量（25 张微步任务卡编排）独立审阅报告

## 1. 审阅身份、时间与独立性声明

| 字段 | 记录值 |
| --- | --- |
| **独立审阅会话标识 (`reviewer_session`)** | `663fcda3-b02b-4d3a-89f6-ffc1ef283810`（独立子 Agent 会话，与规划作者 `/root` 及当前主会话 `9e5411f4-acad-421e-b487-9e68b9483320` 上下文隔离） |
| **审阅角色 (`reviewer_role`)** | 独立 QA / 任务编排审阅者（只读核查权限） |
| **首轮审阅时间（UTC+8）** | `2026-10-26 13:38:08+08:00` ～ `2026-10-26 13:44:30+08:00`（首轮结论：`changes_requested`） |
| **复核完成时间（UTC+8）** | `2026-10-26 13:56:05+08:00` ～ `2026-10-26 13:57:30+08:00`（复核结论：`plan_structure_accepted_pending_dispatch`） |
| **审阅对象** | `marlin-r2-v2-offline-1`（MiniMCProto v2.0 首个本地离线协议增量的 25 张微步任务卡编排、关联工作包/里程碑接入及静态检查工具） |
| **只读与边界声明** | 本次审阅对所有规范任务卡（`project-control/.agents/**`）、规则、协议原稿、业务源码（`soc-ap/**`、`mcu-p3/**`、`test_harness/**`）及管理工具（`project-control/tools/check_task_graph.py`）保持**绝对只读**；未修改任何受审原件，未运行未来协议实现命令，未更改正式任务状态。所有原始日志与本报告仅写入 `project-control/docs/evidence/20261020_task_orchestration/independent/review_20261026_01/`。 |
| **最终审阅结论 (`decision`)** | **`plan_structure_accepted_pending_dispatch`**（首轮发现的 `DEF-01` 与 `DEF-02` 均已由主会话修正并通过独立复核；本批 25 张微步卡编排结构可接受，实际派单字段仍需逐票登记，不代表协议代码已实现或原 MS HIL 已完成）。 |

---

## 2. 所审 Git Commit、工作区差异与文件哈希核对结果

### 2.1 四仓 Git HEAD 与工作区状态（首轮基线与复核状态）

原始核验日志见同目录 [`hash_verify.log`](hash_verify.log)（首轮）与 [`reverify_hashes_and_diff.log`](reverify_hashes_and_diff.log)（第二轮复核）：

| 仓库 | `git rev-parse HEAD` | 首轮 `git status --porcelain=v1` | 复核时 `git status --porcelain=v1` | 说明 |
| --- | --- | --- | --- | --- |
| `project-control` | `770bc8433462388132493c3cfca007d5dbf185e0` | 干净（仅新增本独立审阅目录 `?? docs/evidence/20261020_task_orchestration/independent/`） | `M .agents/kanban/microtasks/minimc_v2/V2-P05B.md`<br>`M tools/check_task_graph.py`<br>`?? docs/evidence/20261020_task_orchestration/independent/` | 所审准确组合为：`HEAD 770bc8433462388132493c3cfca007d5dbf185e0` ＋ 已跟踪文件工作区差异 SHA256 `db0db071ffe29aa4017dc49fe2c7d00e669cc632694b2ef855a1efb4b485511b` |
| `soc-ap` | `cf2dff40e8b9d7c94b41d01386f287be45afdb4d` | 干净（无输出） | 干净（无输出） | 与 25 张微步卡 `source_baseline.soc-ap` 完全一致 |
| `mcu-p3` | `14b8057b04030bd659744c874c73ff8f09f29979` | 干净（无输出） | 干净（无输出） | 未在本批离线增量中触发任何写入 |
| `test_harness` | `ad0398e20d3645dbfa37bfd0550ded0828d018b2` | 干净（无输出） | 干净（无输出） | 与 25 张微步卡 `source_baseline.test_harness` 完全一致 |

### 2.2 `517ba18` 基线、`770bc84` 提交与复核修订文件的哈希核对

1. **`517ba18..770bc84` 变更文件核对**：
   `git -C project-control diff 517ba18dc9b3ecd9893680b60d7bcaf0ff873e18..770bc8433462388132493c3cfca007d5dbf185e0 --name-status` 仅包含 3 项交接收尾文件变更：
   - `A docs/evidence/20261020_session_close/record.json`
   - `M docs/handoff/HANDOFF_20261020.md`
   - `M workspace-root/HANDOFF_20261020.md.snapshot`
2. **`card_hash_manifest.json`（80 项文件）核对**：
   - 在 `517ba18dc9b3ecd9893680b60d7bcaf0ff873e18` 基线下：**80/80 项 SHA256 100% 匹配（0 项不匹配）**。
   - 在首轮 `770bc8433462388132493c3cfca007d5dbf185e0` 下：**79/80 项规范任务卡、计划、指南、协议原稿（`9f8d4f9607cb3e76cc30b9ee2f971b23c3e0d936611188466a71f4aa15f3ce54`）与工具（`567d2c51c8b2a4ed8269708584e8788a245cae6289fa5beb523865de9a5fa1c2`）100% 保持原哈希不变**；唯一差异项为 `workspace-root/HANDOFF_20261020.md.snapshot`（由 `517ba18` 时的 `e4028804aab0466972a75fc2bde3de0bc310d7ebe48f3fc18c87c014335040f3` 更新为 `770bc84` 收尾快照 `18934e1d424028fe270be1fe4b87aa233f221b9ddfcd7c588cc982f19f04710e`）。
   - 在第二轮复核（修复 `DEF-01` 与 `DEF-02` 后）工作区下：其余 77 项保持原哈希不变，2 项受修订文件的精确 SHA256 为：
     - `.agents/kanban/microtasks/minimc_v2/V2-P05B.md`（`revision: 2`）：`d937a740bd1e7a0b1553198fb2a448ccd984e0a0cbfde9252fb0117475cd0f36`（原 rev 1 为 `0f7356e27c277a5e0117a98a443024bdf27bbb95fe9089e318ef11f166a76ddd`）
     - `tools/check_task_graph.py`：`4d56947e496fea6cd69b4c7b41a8192bf7f7eafbb91f402226e0e597a50bf953`（原版为 `567d2c51c8b2a4ed8269708584e8788a245cae6289fa5beb523865de9a5fa1c2`）
     - `git -C project-control diff`（已跟踪文件完整 diff）SHA256：`db0db071ffe29aa4017dc49fe2c7d00e669cc632694b2ef855a1efb4b485511b`
3. **`docs/evidence/20261020_session_close/record.json` 核对**：
   - `baseline_commit` 记录为 `517ba18dc9b3ecd9893680b60d7bcaf0ff873e18`。
   - 3 项交接文件哈希实测完全匹配：
     - `HANDOFF_20261020.md`: `18934e1d424028fe270be1fe4b87aa233f221b9ddfcd7c588cc982f19f04710e`（匹配）
     - `project-control/docs/handoff/HANDOFF_20261020.md`: `72855bacab46e37a007765d77f18175012b22d5729bec9b3662fb0378f3472f4`（匹配）
     - `project-control/workspace-root/HANDOFF_20261020.md.snapshot`: `18934e1d424028fe270be1fe4b87aa233f221b9ddfcd7c588cc982f19f04710e`（匹配）
4. **历史 42 张旧卡与旧首轮计划快照核对（`docs/evidence/20261020_task_audit/`）**：
   - `docs/evidence/20261020_task_audit/inputs/` 下归档的 **42 张修订前任务卡**与 `task_audit.json` 中 `cards[*].sha256` 逐一比对：**42/42 全部匹配（0 项篡改）**。
   - 归档的旧版计划 `inputs/docs/planning/minimc_v2_first_increment_20261020.md` 实测 SHA256 为 `83575aea05a9ac1524478b9b3ee95c76479e23e541a8eb5b3cd23493e55668ff`，与 `task_audit.json` 中的 `v2_plan_sha256` 完全一致。

---

## 3. 实际执行的只读检查命令与退出码

| 轮次 | 执行命令 | 工作目录 (`cwd`) | 实际退出码 | 原始日志路径 | 结果摘要 |
| --- | --- | --- | --- | --- | --- |
| 首轮 | `python3 project-control/tools/check_task_graph.py --workspace .` | `/home/sushaohua/workspace/ai_soc_project` | `0` | [`structure_check.log`](structure_check.log) | 规范任务卡 67 张、v2 微步卡 25 张；静态结构错误 0、依赖循环 0；28 对共享写路径均有先后依赖顺序 |
| 首轮 | `python3 project-control/tools/check_task_graph.py --workspace . --check-ready V2-P01A` | `/home/sushaohua/workspace/ai_soc_project` | `2` | [`v2_p01a_ready_check.log`](v2_p01a_ready_check.log) | 正确拒绝未就绪派单（退出码 `2`），准确列出 5 项缺失的派单登记字段，未修改任何任务状态 |
| 首轮 | 独立哈希与 Git 状态复核脚本（核对四仓 HEAD/status、`card_hash_manifest.json`、`20261020_session_close/record.json`、`20261020_task_audit/task_audit.json`） | `/home/sushaohua/workspace/ai_soc_project` | `0` | [`hash_verify.log`](hash_verify.log) | `517ba18` 下 80/80 匹配；`770bc84` 下 79/80 不变 + 1 项交接快照按 `record.json` 更新匹配；42 张旧卡与旧计划快照 100% 匹配 |
| **复核** | `python3 project-control/tools/check_task_graph.py --workspace .` | `/home/sushaohua/workspace/ai_soc_project` | `0` | [`structure_recheck.log`](structure_recheck.log) | 在增强 `.cpp` 编译检查与 9 个 `--case-set` 覆盖检查后，67 张规范卡与 25 张微步卡（含 `V2-P05B` rev 2）全部通过（`errors: []`） |
| **复核** | `python3 project-control/tools/check_task_graph.py --workspace . --check-ready V2-P01A` | `/home/sushaohua/workspace/ai_soc_project` | `2` | [`v2_p01a_ready_recheck.log`](v2_p01a_ready_recheck.log) | 仍正确退出 `2` 并报告 5 项待派单阻塞项，未改任务状态 |
| **复核** | 修订哈希、diff 与内存中旧版 `V2-P05B` 反例拦截复核脚本 | `/home/sushaohua/workspace/ai_soc_project` | `0` | [`reverify_hashes_and_diff.log`](reverify_hashes_and_diff.log) | 确认 `V2-P05B.md` rev 2 的 5 步命令完整；确认新版 `check_task_graph.py` 对内存中构造的旧版 `V2-P05B` 准确报出 2 项错误拦截 |

---

## 4. 首轮发现的缺陷、修复情况与复核结果

| 编号 | 严重性 | 定位（任务 ID / 文件路径） | 首轮问题描述 | 复核验证结果 |
| --- | --- | --- | --- | --- |
| **DEF-01** | **High (P1)** | `V2-P05B`<br>`project-control/.agents/kanban/microtasks/minimc_v2/V2-P05B.md` | 首轮 rev 1 中 `V2-P05B`（修改 `soc-ap/core/forward/minimc/parser.cpp`，对应 `stream_header` 功能组）的 `verification.commands` 仅含 `precheck` 与 `header`（`-fsyntax-only -include parser.h /dev/null`），缺失 `configure`、`build`、`focused_cases (--case-set stream_header)` 与 `host_regression`。 | **已修复并复核通过（Closed）**：<br>`V2-P05B.md` 已升至 `revision: 2`（SHA256 `d937a740bd1e7a0b1553198fb2a448ccd984e0a0cbfde9252fb0117475cd0f36`），`verification.commands` 已补齐 `precheck`、`configure`（`-B /tmp/ai_soc_v2_build/V2-P05B`）、`build`、`focused_cases`（`--probe /tmp/ai_soc_v2_build/V2-P05B/bin/minimc-probe --case-set stream_header`）、`host_regression`（`ctest --output-on-failure -R ^host_runtime_smoke$`）共 5 步，与 `V2-P05A`/`V2-P05C` 完全对齐。 |
| **DEF-02** | **Medium (P2)** | `project-control/tools/check_task_graph.py` | 首轮 `structural_errors()` 未校验 `.cpp` 实现卡必须包含编译/构建命令（禁止仅 `header` 语法检查），也未校验 `V2-P04A`～`V2-P05E` 必须各自包含对应的 9 个 `--case-set` 功能组。 | **已修复并复核通过（Closed）**：<br>`check_task_graph.py`（SHA256 `4d56947e496fea6cd69b4c7b41a8192bf7f7eafbb91f402226e0e597a50bf953`）第 131～150 行已新增上述两项静态检查；经内存中注入旧版 `V2-P05B` 反例验证，工具准确报出 `cpp implementation task must compile/build cpp target, not header-only check` 与 `missing focused_cases command with --case-set stream_header` 两条错误（见 [`reverify_hashes_and_diff.log`](reverify_hashes_and_diff.log)）。 |
| **OBS-01** | **Low (P3 / 非阻塞建议)** | `V2-P04B`～`V2-P04D` (`codec.cpp`), `V2-P05B`～`V2-P05E` (`parser.cpp`) | 同文件串行微步卡的 `focused_cases` 仅运行本票新增的单一 `--case-set`，同文件前序分组在 `V2-P06A` CTest 汇总时统一复验。 | **保留为执行期观察项**：不影响本批编排结构接受；建议在逐票执行与 Review 时核对 diff 仅触及本票函数/状态分支，或顺带回归同文件已完成分组。 |
| **OBS-02** | **Low (P3 / 非阻塞提醒)** | `MS-05`, `MS-06`, `MS-07`<br>`project-control/.agents/kanban/milestones/marlin_ms05_20261007_214108.md` 等 | `MS-05/06/07` 的 YAML `dependency_conditions` 仅列出新增的 `V2-*` 项，原有 `MS-*` 条件保留在正文表格中。 | **保留为远期里程碑派单提醒**：`MS-05/06/07` 当前仍为 `scope_status: unmapped` 且不在本批离线增量派单范围内；未来映射派发 `MS-05/06/07` 前再将正文表格中的 `MS-*` 条件同步至 YAML。 |

---

## 5. 对《审阅说明》六个核心问题的逐项独立回答

### 问题 1：粒度是否落实到一个结果/接口层，是否仍有应继续分离的函数、构建或测试预期变更？每卡的白名单能否支撑其目标且不越界？
- **回答**：**粒度与白名单边界设计合理，已落实到单一结果与单一接口/函数/状态分支层。**
  1. 原先粗粒度的 `V2-P01`～`V2-P06` 已被拆分为 25 张不可再混派的微步卡：
     - **契约与独立预期分离**：帧格式契约（`V2-P01A`）、版本/心跳命令契约（`V2-P01B`）、固定测试向量 JSON 数据（`V2-P01C`）、纯 Python 标准库参考校验器脚本（`V2-P01D`）各自独立成票。
     - **接口声明与测试探针协议分离**：编解码头文件 `codec.h`（`V2-P02A`）、流式解析器头文件 `parser.h`（`V2-P02B`）、测试探针 CLI/文本输出协议 `test-probe.md`（`V2-P02C`）分别冻结。
     - **符号桩、构建接入、探针实现与运行器分离**：`codec.cpp` 桩（`V2-P03A`）、`parser.cpp` 桩（`V2-P03B`）、`CMakeLists.txt` 协议库构建目标接入（`V2-P03C`）、`probe.cpp` 适配器实现（`V2-P03D`）、`CMakeLists.txt` 探针构建目标接入（`V2-P03E`）、`run_codec_cases.py` 独立比较运行器（`V2-P03F`）完全解耦，不存在同票同时改业务源码与构建脚本或测试运行器的情况。
     - **核心算法与解析器 FSM 分支逐票拆解**：`codec.cpp` 拆为 `crc16`（`V2-P04A`）、`encode_frame`（`V2-P04B`）、解码长度/边界防御（`V2-P04C`）、完整帧校验与字段提取（`V2-P04D`）四票；`parser.cpp` 拆为 `reset` 与 `WAIT_SOF1/SOF2` 同步（`V2-P05A`）、10B 帧头累积与长度门禁（`V2-P05B`）、载荷与 CRC 收尾分发（`V2-P05C`）、50ms 字节超时先检后刷与 `uint32_t` 回绕（`V2-P05D`）、坏帧后同步恢复（`V2-P05E`）五票。
  2. **白名单边界（`write_scope` / `allowed_paths` / `forbidden_paths`）核查**：每张业务/测试卡在 `soc-ap` 或 `test_harness` 中最多只允许写 **1 个具体文件路径**（`V2-P06B` 独立复验卡对业务/测试仓完全只读，仅写 `project-control/docs/evidence/minimc_v2/V2-P06B/**`），且全部明确禁止写 `mcu-p3/**`、外部知识库 `D:/AI_RDdocs/**`、以及 `project-control/.agents/**` 正式状态目录。28 对共享写路径（如 `codec.cpp`、`parser.cpp`、`CMakeLists.txt`）均具备严格的 `depends_on` 偏序关系。

### 问题 2：输入/前置/产物/能力条件是否形成有向、可执行的关系？设计是否错误等待实测，是否有未在字段图体现的循环？
- **回答**：**依赖图有向无环（DAG），且正确区分了“离线协议设计前置”与“真实硬件实测前置”，无隐式循环。**
  1. 静态工具与人工复核均确认 67 张任务卡（含 25 张 `V2-*` 卡）无缺失前置 ID、无显式或隐式依赖循环。
  2. 首票 `V2-P01A` 仅消费项目内已落盘并锁死 SHA256（`9f8d4f9607cb3e76cc30b9ee2f971b23c3e0d936611188466a71f4aa15f3ce54`）的本地协议原稿 `Rev 2.0.3`，不等待任何尚未产生的代码或硬件实测。
  3. 后续微步卡严格按 `契约 → 独立样例/参考校验器 → 头文件接口/探针契约 → 符号桩/构建目标/探针/运行器 → 单函数/单分支实现 → CTest 集成 → 独立复现 → 离线候选归档` 单向推进。
  4. 与主线里程碑及 `TASK-005` 内 `MCQ` 微步的连接方向正确：`TASK-005` 中的 `MCQ-01` 消费 `V2-P01B` 离线命令契约与 `MS-03` 源码核查结论，不反过来等待 `MS-04` 实收样例；`MS-05` 消费 `MS-03`、`MS-04` 与 `V2-P01B`；`MS-06` 消费 `MS-05` 与 `V2-P01D`；`MS-07` 消费 `MS-05`、`MS-06`、`MS-18` 与离线最终候选 `V2-P06C`。既未让离线设计错误等待硬件实测，也未用离线通过替代 `MS-03/04/05/06/07/11/17` 的真实固件/HIL 验收条件。

### 问题 3：每票的正常/异常判据、命令与其可用时点是否相符？桩、空测试、只跑 host smoke 是否可能误报成协议通过？
- **回答**：**在 `V2-P05B` 修订为 rev 2 并补齐 5 步验证命令后，全部 25 张卡的正常/异常判据、命令与可用时点完全相符，且对桩、空测试、仅跑 `host_runtime_smoke` 建立了严密的防误报门禁。**
  1. 所有未执行命令均明确标记 `availability: planned-output`，严禁当作本轮已执行证据。
  2. 符号桩阶段（`V2-P03A`/`P03B`/`P03D`/`P03F`）强制要求桩函数返回显式 `not_implemented` 且输出长度为 0，`--case-set stub` 专门断言 `not_implemented`，并明确规定最终 CTest（`V2-P06A`）只注册 `reference` + 9 个功能组 + `host_runtime_smoke`（共 11 项），不注册 `stub` 或重复的 `all`。
  3. `V2-P04A`～`V2-P05E` 九张核心实现卡现已一对一完整覆盖 `crc`、`encode`、`decode_bounds`、`decode`、`stream_sync`、`stream_header`、`stream_payload`、`timeout`、`recovery` 九个功能组，每票均包含本票独立构建与专项用例执行，不推迟到最终 QA。
  4. `V2-P01D`（`--self-check`）与 `V2-P03F`（`--self-check`）均要求对损坏 CRC、重复 `case_id`、缺失探针、空分组、子进程超时做自身反例拒绝自检；每组测试均强制要求非零用例数（`no_empty_test_pass: true`）。
  5. `V2-P06A`/`V2-P06B` 规定显式传入 `MINIMC_QA_ROOT` 时若缺失 QA 脚本/样例必须配置失败；未传入时必须标明协议测试未启用，禁止用原有的 `host_runtime_smoke`（1/1）冒充协议验收通过。
  6. 原稿 `V04`（急停广播帧 §5.1/§5.2 规定 2B 载荷而 §7 V04 为 `L=0`、14B）在 `V2-P01A`/`P01B`/`P01C`/`P04D`/`P06B` 中均被明确限定为“帧结构层有效、急停业务长度语义冲突未决”，禁止据此宣称急停业务通过。

### 问题 4：独立预期是否在实现前接受，作者/QA/状态写入/收件是否区分，失败重试与回退是否保留用户差异？
- **回答**：**是，职责分离与安全回退规则清晰完整。**
  1. **独立预期先于实现冻结并接受**：QA 负责的独立测试向量（`V2-P01C`）与独立参考校验器（`V2-P01D`）均由 `ARCH` 独立评审接受，并作为 `V2-P02A`（编解码接口）、`V2-P02C`（探针契约）、`V2-P03F`（比较运行器）及后续所有实现票的前置依赖；同时禁止探针（`V2-P03D`）内嵌参考算法自证，也禁止从生产输出倒推或更新测试预期。
  2. **作者 / Reviewer / 状态写入 / 收件严格区分**：
     - 契约/设计/实现/集成票（`ARCH`、`ENG-FWD`、`ENG-SIM`、`INTEGRATOR`）均指定 `QA` 为必需独立 Reviewer；
     - QA 编写的样例、参考校验器、比较运行器与独立复现票（`V2-P01C`、`V2-P01D`、`V2-P03F`、`V2-P06B`）均指定 `ARCH` 为必需独立 Reviewer；
     - `check_task_graph.py` 在 `readiness_blockers()` 中硬性拦截 `author == reviewer_session` 的自审行为；
     - 正式状态（`project-control/.agents/**`）与收件回执（`handoff.acknowledgement`）仅允许唯一 `COORD` 在核对同一候选版本的独立评审结论后写入，执行者只写各自 `docs/evidence/minimc_v2/<task-id>/runs/<actual-run-id>/`。
  3. **失败停止与非破坏性回退**：25 张卡全部配置 `budget.planned_checkpoint_minutes: 30`、`budget.max_evidence_based_corrections: 2`（首次失败立即停步分析，最多两次有依据纠正仍失败则保存检查点交回 COORD），且 `rollback.forbidden` 明确禁止 `git reset --hard`、全仓 `git clean`、对脏文件整文件 `checkout`、以及删减/放宽检查促通过，确保只撤回本票差异并保留用户既有修改。

### 问题 5：单票记录能否绑定输入、diff/候选、命令、原始日志、失败/修正、独立结论及收件？历史旧卡/旧计划是否确实保留原哈希？
- **回答**：**是，单票追溯链字段完备，且历史 42 张旧卡与旧计划的原字节快照经独立哈希复核 100% 保留。**
  1. 每张微步卡的 `deliverables` 与 `docs/guides/templates/task_run_record.md` 均强制要求绑定：`task_id`、`task_revision`、`actual_run_id`、`actor_session`、`lease_id`、`start_time/end_time`、`workspace`、`input_versions`、`source_head`、`workspace_diff_sha256`、逐条命令的 `cwd/actual_exit_code/stdout_stderr_path/actual_case_count/warning_count`、`candidate_commit/candidate_diff_sha256`、`artifact_hashes`、`failures_and_corrections`、`independent_review`（`reviewer_session/reviewed_artifact_version/report_path/report_sha256/decision`）及 `handoff`（`receiver_session/acknowledgement_path/decision`）。
  2. 最终候选归档卡 `V2-P06C`（产出 `docs/releases/minimc_v2_offline_candidate.yaml`）要求锁定 `candidate_id`、`scope`、`repositories`、`protocol`（核对 SHA256）、`verification`、`limitations`、`handoff`。
  3. 经本会话实测 SHA256 核对（见 [`hash_verify.log`](hash_verify.log)），`docs/evidence/20261020_task_audit/inputs/` 中保存的 42 张旧卡与 1 份旧版首轮计划与 `task_audit.json` 记录的原始 SHA256 **100% 逐字节一致（0 误差）**，历史审计证据链完整无覆盖。

### 问题 6：正式状态是否如实保持 Backlog，哪些真实派单条件仍待补？不要把计划结构接受变成“25 张开发任务已经验收”。
- **回答**：**全部 67 张规范任务卡（含 25 张 `V2-*` 微步卡与 42 张原有卡）当前正式状态均如实保持 `Backlog`，没有任何卡片被虚假标为 `Ready` 或 `Done`。**
  1. 本次审阅结论 `plan_structure_accepted_pending_dispatch` **仅代表 25 张微步任务卡的编排结构可接受，绝不代表 25 张开发任务已实现、已通过协议测试或已完成原 MS 硬件验收**。
  2. 首票 `V2-P01A` 要从 `Backlog` 进入 `Ready`，仍须由实际 COORD 在有效授权下逐项补齐以下 5 项真实派单条件（当前 `check_task_graph.py --workspace . --check-ready V2-P01A` 实测退出码 `2` 并准确报告这 5 项缺口）：
     - `actual owner/executor is not assigned consistently`：登记实际作者会话标识（`owner` 与 `executor.agent_id` 一致且非空）；
     - `required independent reviewer session is not assigned`：登记与作者不同的实际独立审阅会话标识（`review_assignments.reviewer_sessions[*].session`）；
     - `actual worktree/working directory is not bound`：绑定实际工作区路径（`worktree`）；
     - `dispatch input commit/diff is not bound`：绑定派单时的准确源码提交与工作区差异摘要（`base_commit`、`dispatch_binding.source_commit`、`dispatch_binding.workspace_diff_sha256`）；
     - `actual lease and checkpoint deadline are not registered`：登记有效人工租约（`lease.owner`、`lease.task_revision`、`lease.lease_id`、`lease.expires_at`）。
  3. 其余 24 张后续微步卡（`V2-P01B`～`V2-P06C`）除上述 5 项外，还必须等待其直接前置卡真实执行完毕、通过独立评审与验证、由 COORD 确认收件更新为 `Done`，并在本卡 `dependency_conditions[*].accepted_version` 与 `acceptance_evidence` 中绑定已接受的上游准确交付版本后，方可逐票进入 `Ready`。

---

## 6. 最终审阅结论

- **首轮结论（`2026-10-26T13:44:30+08:00`）**：`changes_requested`（定位 `DEF-01` 与 `DEF-02`）
- **复核后最终结论（`2026-10-26T13:57:30+08:00`）**：**`plan_structure_accepted_pending_dispatch`**
- **收件入库提醒**：主会话 COORD 在收件并归档本次修订时，请同步刷新 `docs/evidence/20261020_task_orchestration/card_hash_manifest.json`（及对应检查证据 JSON/SHA256SUMS）中 `V2-P05B.md`（rev 2: `d937a740bd1e7a0b1553198fb2a448ccd984e0a0cbfde9252fb0117475cd0f36`）与 `tools/check_task_graph.py`（`4d56947e496fea6cd69b4c7b41a8192bf7f7eafbb91f402226e0e597a50bf953`）的哈希记录并提交控制仓 Git 检查点。
