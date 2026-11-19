# COORD 会话交接清单（`SLICE-06 -> SLICE-07`）

- **交接时间**：`2026-11-18T19:22:30+08:00`
- **接手身份**：`COORD`（严守根 `AGENTS.md`：业务仓只读，工程改动委派 `ENG-AP` 并通过 `run_slice_batch.py` + 四阶门禁推进）

## 1. 已锁定规划与仓基线

- **已批准 SSoT 方案（`v1.7`）**：`project-control/docs/planning/helix_screen_mc_th_integration_implementationplan_20261118_144741.md`
  - `DEC-SCREEN-01=A`（本轮只做 P0 + 同源制镜 + 冷启动验收 + 发版骨架；`SLICE-09` P1 挂起后续单排）
  - `DEC-SCREEN-02=B`（固定固件目录读取）
  - `DEC-SCREEN-03=有条件A`（复用 `Forward.OtaCommand` + DDS；真机前补齐并发/维护互斥/急停测试；屏幕区分“后台已锁定(`BUSY`)”与“设备已确认急停”；`AC-09` 半断连与单板 OTA 准入解耦）
  - `DEC-SCREEN-04=留待 P1`（按温区隔离，热敏开路须拦截含通用 G-code 在内的全部加热入口）
  - `DEC-SCREEN-05=已确认`（编译源码、页面注册、打包清单三方验收裁剪）
  - `DEC-SCREEN-06=A`（程序入 `/`，持久数据留 `/data`；清理前复测两处余量并列清单；**保留 `/data/boot_backup.img`**）
  - `DEC-SCREEN-07=A`（同源镜像校验；实板同源包验冷启动/断连/P0；部署、整机刷写、发布分别报批）
  - `DEC-SCREEN-08=B`（`Forward` 写刷前 ECDSA-P256 验签，签发/验签统一 `trailer[0..52]`，覆盖合法/未签名/坏签名/缺失公钥 4 类验收，注明 MC U 盘救援无数字签名边界）
- **`project-control@main`**：`98ef7f97fc18b2af012864667967a8c464ac1301`（已含 `v1.7` 方案及 `SLICE-06.yaml` / `SLICE-07.yaml`；工作区中 `qa_docker_toolchain_implementationplan_20261118_115938.md` 与 `tools/qa_runner/Dockerfile.toolchain` 属并行任务未跟踪文件，**勿动勿提交**）。
- **`mcu-p3` / `boot/*` / `test_harness` / `agents` / `sdk/c308l`**：保持只读干净。

## 2. 当前正在运行的现场状态（交接刻实况）

- **主巡航任务**：对话 `3896821b-3820-46cd-80f7-a2c41178c8e2` 的后台 `run_workflow` `task-1383`（脚本 `project-control/tools/workflow/run_slice_batch.py`，目标 `SLICE-06`）**仍在运行中**。
- **`SLICE-06` 第 1 轮已落盘提交与裁决**：
  - `printer-soc@main` Candidate：`9875c9f655159993d803a6ae4aa96866bdfdea03`（已推送 GitLab）；
  - 第 1 次四阶门禁在 Stage 3 (`docker_qa`) 判 **`FAILED`**（已过 `fast_gate` 与宿主合龙），裁决见 `project-control/docs/evidence/SLICE-06/run_20261118_191806_071219_34fd1a7f_r01/verdict.json`（完整沙箱日志见同目录 `docker_qa/runtime.log`）。
- **第 1 轮自动保活返修正在进行**：
  - `run_slice_batch.py` 已自动唤醒原 `ENG-AP` 会话（`82b4ebc1-2ac3-47ea-95b9-06c746b52bec`）进入第 1 轮返修，当前已本地修改：
    - `printer-soc/services/helixscreen/tests/unit/aisoc/test_aisoc_p0.cpp`
    - `printer-soc/tests/forward/startup/test_startup_fail_fast.py`
  - 完成后将重新提交推送 `printer-soc@main` 并进入第 2 次四阶门禁核验。

## 3. 接续方式（严禁并发冲突写同一 `printer-soc` 工作树）

1. **若旧任务未退出**：先确认旧对话 `3896821b-3820-46cd-80f7-a2c41178c8e2` 的 `task-1383` 与 `82b4ebc1` 已结束或已在 `slices/ledger.md` 写入 `SLICE-06 | SW-Verified`。**切勿在旧 `ENG-AP` 写入 `printer-soc/` 时同时派发新 Agent 改同一目录**。
2. **检查当前状态**：
   - 查 `git -C project-control status --short` 与 `project-control/slices/ledger.md`；
   - 查 `git -C printer-soc status --short` 与 `git -C printer-soc log -n 3 --oneline`；
   - 查 `ls -lt project-control/docs/evidence/SLICE-06/` 最新 `run_*/verdict.json`。
3. **继续推进顺序（严格遵守用户批复边界）**：
   - **若 `SLICE-06` 尚未 `SW-Verified`**：让 `ENG-AP` 基于当前 `printer-soc` 状态修复并跑通 `fast_gate.py --slice project-control/slices/SLICE-06.yaml`、宿主机/C308L 自检、线性 `rebase + push` `printer-soc@main`，再以 `run_workflow(run_slice_batch.py)` 跑过四阶门禁写入 `ledger.md`。
   - **`SLICE-06` 达成 `SW-Verified` 后**：汇报“通过 + 证据路径”，随后用 `run_workflow(run_slice_batch.py)` 启动 `project-control/slices/SLICE-07.yaml`（**仅软件联调与四阶门禁**，不触硬件）。
   - **`SLICE-07` 达成 `SW-Verified` 后**：整理 `SLICE-08` 上板前置清单（含 `DEC-SCREEN-06` 清前 `/` 与 `/data` 容量复测 + 清理清单 + 保留 `boot_backup.img`），停机申请 **`Human Gate #2`**，未获批前严禁触碰 `192.168.1.101` 或烧写/发布。
4. **汇报格式硬约束**（用户明确要求）：进度汇报只写 **通过 / 失败 / 阻塞**，并附当次证据文件路径（`verdict.json` 等），`project-control` 新增成果/证据注意适时线性同步推送 `origin/main`。
