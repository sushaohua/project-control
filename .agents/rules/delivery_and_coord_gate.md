---
id: RULE-COORD-DELIVERY-GATE-V2
revision: 7
status: current-rule
owner: COORD
updated: '2026-11-14'
plan_revision: v2-slice-funnel
---

# COORD V2 垂直切片编排、四阶漏斗门禁与双态准出规程

本规则取代旧版 `coord_runner` 状态机与微票门禁（旧归档件封存于 `project-control/tools/legacy/` 与 `.agents/kanban/archive_v1/`，历史 `Done` 卡片与证据保持原样不改写）。新建与在途研发统一执行 **“两阶段 SSoT 协议 + 垂直切片连坐闭环 + 四阶无状态门禁漏斗”**。

## 1. 两阶段协议与单一真相源（SSoT）入口

1. **Phase 1（实施方案先行，Human Gate #1）**：
   - `ARCH` 基于本地 `graphify` AST 图谱取证与 `project-control/contracts/minimc_v2_contract.yaml` 契约真源，产出时间戳方案 `{summary}_implementationplan_{YYYYMMDD_HHMMSS}.md`。
   - 方案必须**原地迭代更新（In-place Update）**，头部维护实名修订履历（显式标注具体 AI 客户端/引擎实体，如 `AI (Antigravity-CLI)`、`AI (Codex)`），列明 AST 调用链核实表、软硬件契约推演、各子仓 **最小修改预算（Diff Budget）**、拓扑有序切片 `SLICE-XX` 及回滚预案。
   - **未获人类明确批准（`Approved` / `批准执行`）前，严禁修改任何工程代码**；一经批准，即授予当前批次（2～3 个垂直切片）连续自动巡航授权。
2. **Phase 2（`run_workflow` 有界自动巡航）**：
   - `COORD` 通过 `project-control/tools/workflow/run_slice_batch.py` 按序推进批次切片，以追加式账本 `project-control/slices/ledger.md` 实现幂等断点续跑，耗时 $>1\text{ min}$ 步骤通过 `phase()`/`log()` 实时输出进度。
   - **`COORD` 业务仓只读硬铁律**：`COORD` 严禁直接修改 `soc-ap/`、`mcu-p3/`、`test_harness/`、`boot/bootloadermc/`、`boot/bootloaderth/`，所有代码变更必须委派对应 `ENG-*` / `ENG_BOOT_*` / `INTEGRATOR` 执行。

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
   - 宿主机启动独立只读会话（`codex exec --sandbox read-only -m gpt-6-luna`），输出 `BLOCKER / MINOR / NIT` 三级结论：
     - **存在 `BLOCKER`**：判定 `REJECTED`，唤醒原 `ENG-*` 保活会话定向修复并重过漏斗（**最多允许 2 轮返修**；第 2 轮仍未闭环或同因复发立即 Fail-Fast 熔断停机升级人类）。
     - **`0 BLOCKER`（含仅有 `MINOR` / `NIT`）**：签发带 `report_sha256` 的 `verdict.json`（`APPROVED`），`MINOR` 记入 `ledger.md` 技术债表，切片标记为 **`SW-Verified`** 自动推进下一切片。

## 3. 双态准出（`SW-Verified` / `HIL-Verified`）与发布红线（Human Gate #2）

1. **业务域真机穿刺**：每跑完 1 个业务域批次（2～3 个 `SW-Verified` 切片），或涉及底层串口驱动/DMA/中断/Bootloader 擦写跳转改动时，工作流自动停机请求 **Human Gate #2**，在排他台架执行正负配对真机 HIL 实测（采集双向 Raw Hex、毫秒时戳、固件 SHA256 与物理状态变化），经独立 Codex 审计通过后升级为 **`HIL-Verified`**。
2. **线性历史与冲突熔断**：推送远端前必须拉取目标分支执行 `git rebase` 保持严格线性历史（禁默认 `git pull` 产生 Merge 节点）；一旦发生变基冲突立即 `git rebase --abort` 或停机保留现场交人工仲裁，严禁强推或静默覆盖。
