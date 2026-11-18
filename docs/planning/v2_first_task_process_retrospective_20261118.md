# AI SoC V2 首单实战过程问题总结与治理改进报告

- **关联任务**：验收现有 MC 与 TH 固件升级功能（`BATCH-OTA-ACCEPTANCE-01`，[实施方案](mc_th_upgrade_acceptance_implementationplan_20261117_174500.md)）
- **记录角色**：`COORD`（`AI (Antigravity-CLI)`）
- **日期**：`2026-11-18`
- **当前阶段进度**：`SLICE-01` 已通过四阶漏斗准出 `SW-Verified`（`3116587`）；`SLICE-02` 在独立 Codex 冷审阶段完成证据闭环定位与整改；已探明真机台架已由离线 VMware 切换至 C308L 板端（`192.168.1.101:/dev/ttyS1`）并正在推进 `SLICE-03`。

---

## 一、本轮实战暴露的流程与工具链问题总览

本任务作为 AI SoC V2“两阶段 SSoT 协议 + 10 席深模块角色 + 四阶无状态门禁漏斗”的首次实战检验，成功验证了 `PM ↔ ARCH → Gate #1 → COORD → ENG_BOOT_TH / INTEGRATOR → 独立 Codex QA` 的跨角色协作能力，同时也真实暴露出 **8 类流程规范与工程工具脱节问题**。

| 编号 | 问题名称 | 发生阶段 | 严重度 | 核心根因 |
| :--- | :--- | :--- | :---: | :--- |
| **P-01** | `qa_runner.py` 强制远端检出与规则 `local_pre_publish_gate` 未对齐 | `SLICE-01` 第 3 阶门禁 | 高 | 规则文本允许本地预检，工具代码强制远端 SSH 拉取 |
| **P-02** | 宿主机与 `qa-sandbox:20261029` 工具链双侧割裂 | Phase 1 / `SLICE-01~02` | 高 | 宿主机缺 FastDDS/D-Bus，容器缺 `arm-none-eabi-gcc`/`ninja`/`pytest` |
| **P-03** | `codex_review.py` 硬编码 `180s` 超时导致跨仓冷审中途被杀 | `SLICE-01` 第 4 阶门禁 | 中 | 跨 7 仓只读冷审需 ~30+ 步取证，180s 不足以吐出 `final.json` |
| **P-04** | `slice_gate.py` 失败证据入库污染与提示词缺当次路径锚点 | `SLICE-02` 第 4 阶门禁 | 高 | 提交旧失败 `run_01/` 入库后，Codex 将其与未入库的 `run_02/` 对撞拒单 |
| **P-05** | `input_repositories` 含 `project-control` 引发的“自指 Commit SHA 悖论” | `SLICE-02` 第 4 阶门禁 | 高 | 在 `project-control` 日志内打印自身 `HEAD` 再提交，提交后 SHA 必变 |
| **P-06** | 活动主线迁移（`soc-ap` ➔ `printer-soc`）未联动 `test_harness` 与契约 | Phase 1 / `SLICE-01` | 高 | `sync_contracts.py` 仅查 C 宏，漏检测试脚本硬编码与 `version_code` 位域冲突 |
| **P-07** | 虚拟靶机 M07 虚构 `0x23` 4B 主动取消语义形成假阳性 | Phase 1 / `SLICE-01` | 高 | 仿真靶机未与真实双 Bootloader（仅 7 条指令）同步收敛 |
| **P-08** | 物理 HIL 载体变迁（VMware 离线 ➔ C308L `/dev/ttyS1`）未前置探测 | Phase 1 / `SLICE-03` | 中 | 历史手册绑定 VMware，未在 Phase 1 强制做非侵入物理连线实探 |

---

## 二、逐项根因分析、本轮应对与永久改进建议

### P-01：`qa_runner.py` 强制远端检出 vs `local_pre_publish_gate` 未落地
- **现象与影响**：[delivery_and_coord_gate.md](../.agents/rules/delivery_and_coord_gate.md) 第 2.3 节允许“远端未同步前本地巡航支持显式标记 `local_pre_publish_gate`”，但 [qa_runner.py](../../tools/qa_runner/qa_runner.py) 强制执行 `require_remote_hash_verification: true`，必须从 `ssh://git@192.168.77.79:2222/...` 拉取候选提交。因此若不提前向人工申请远端 `git push` 授权，`run_slice_batch.py` / `slice_gate.py` 无法跑通第 3 阶容器 QA，且会触发无效的 2 轮工程返修循环。
- **本轮应对**：`COORD` 在本地先执行 `slice_gate.py --fast-only` 与容器预检确认无误后，单列“授权 1”显式呈请用户批准推送 3 个候选分支，再运行完整 `slice_gate.py`。
- **永久改进建议**：
  1. 在 `delivery_and_coord_gate.md` 与 `AGENTS.md` 明确区分“**非受保护候选提交推送（供 QA 沙箱拉取）**”与“**正式版本发布**”的授权颗粒度；或
  2. 在 `qa_runner.py` 真正实现受控的 `--local-pre-publish` 只读快照模式（打 `local_pre_publish_gate` 标记，禁止作为最终发布准出，但允许无远端权限时的本地 `SW-Verified` 预演）。

### P-02：宿主机与 `qa-sandbox:20261029` 工具链双侧割裂
- **现象与影响**：`qa-sandbox:20261029` 内具备 `/usr/local` FastDDS/D-Bus 与 `gcc`/`cmake`，但缺少 `arm-none-eabi-gcc`、`ninja`、`pytest`；宿主机具备 `arm-none-eabi-gcc`/`ninja`/`pytest`，但缺少 FastDDS/D-Bus。导致 `SLICE-01`（`printer-soc` + `test_harness`）与 `SLICE-02`（ARM 交叉编译）无法在同一个容器镜像内闭环完成。
- **本轮应对**：按用户确认的 `DEC-USER-4=A`，在 `SLICE-01` 中将 `run_ota_software_suite.py` 迁移至容器只读挂载 + `/tmp` 构建；在 `SLICE-02` 中将 ARM 交叉编译放宿主机采集原始日志，容器内执行宿主 C 单测编译运行与边界检查。
- **永久改进建议**：升级构建统一的基础 QA 镜像（如 `qa-sandbox:202611xx`），预装 `gcc-arm-none-eabi`、`ninja-build`、`python3-pytest` 及 FastDDS/D-Bus，并在 `project-control/config/qa_runner/default_config.yaml` 锁定新 `image_digest`，让软件与固件交叉编译均可在单一隔离容器内复现。

### P-03：`codex_review.py` 硬编码 `180s` 超时不足
- **现象与影响**：`SLICE-01` 首轮完整门禁（`run_01`）中，`qa_runner.py` 在隔离容器内全部通过（`server_qa.json` `passed: true`），但随后 `codex_review.py` 在执行第 ~34 步跨 7 仓核查时触及硬编码 `timeout=180` 秒而被强杀，未能生成 `final.json`。
- **本轮应对**：已将 [codex_review.py](../../tools/gates/codex_review.py) 调整为 `int(os.environ.get("CODEX_TIMEOUT_SEC", "420"))`，调整后 `SLICE-01` 顺利完成全量双轴审查并签发 `APPROVED`（会话 `01a1ec4e-08c6-74a1-a55d-1bf92676034d`）。
- **永久改进建议**：保留 `420s` 默认值与 `CODEX_TIMEOUT_SEC` 环境变量配置，同时在 `codex_review.py` 超时异常时保留已输出的 `codex.jsonl` 摘要以便快速诊断。

### P-04：`slice_gate.py` 失败证据入库污染与提示词缺当次路径锚点
- **现象与影响**：`SLICE-02` 首轮 `run_01` 未通过后，若直接把失败的 `docs/evidence/SLICE-02/run_01/` 提交入库再跑 `run_02`，独立 Codex 只读审阅时会从锁定 Commit 中读到已提交的 `run_01/docker_qa/server_verdict.json`（`build_count=0`），并将新生成的未提交 `run_02/docker_qa/` 判定为“未包含在锁定提交内”。
- **本轮应对**：清理失效 `run_*` 目录，并在 [slice_gate.py](../../tools/gates/slice_gate.py) 的 `_build_review_prompt` 中显式注入当前运行的 `server_verdict` 与 `runtime_log` 路径。
- **永久改进建议**：
  1. 明确约定：`FAILED / REJECTED` 的临时 `run_XX/` 审阅目录不应提交到待审计的 `project-control` 提交中（或由 `slice_gate.py` 将第 2 阶 `integration_cmd` 日志一并落盘到 `--out-dir/integration.log` 并写入 `prompt` 供 Codex 审查，仅在 `APPROVED` 准出后再连同 `ledger.md` 归档提交）。
  2. `slice_gate.py` 可直接在 `execute_slice_funnel` 中将 `integration_cmd` 的完整 stdout/stderr 保存为 `out_dir/integration.log` 并传给 Codex。

### P-05：`input_repositories` 含 `project-control` 引发的“自指 Commit SHA 悖论”
- **现象与影响**：`SLICE-02` 的 `input_repositories` 包含 `project-control`。当把宿主机编译原始日志 `host_arm_build_and_tests.log` 写入 `project-control` 并在日志头部打印了当时的 `project-control HEAD` (`3116587`) 后再执行 `git commit && push`（生成新 SHA `a0a56b4`），独立 Codex 核对锁定提交 `a0a56b4` 时必然发现日志里记录的 `project-control HEAD` (`3116587`) 与本次锁定提交 (`a0a56b4`) 不一致（**`SLICE-02-B1`**）。只要日志内容写入了当前正在生成提交的同一个仓库自身 SHA，就永远无法自洽。
- **本轮应对**：日志内只锁定记录被测业务/工具/契约目标仓的 HEAD Commit（`mcu-p3`、`boot/bootloadermc`、`boot/bootloaderth`、`test_harness`）以及契约文件 SHA256，不把自指的 `project-control HEAD` 写入待提交文本；并由 `slice_gate.py` 现场再跑 `integration_cmd` 产生当次日志。
- **永久改进建议**：在证据模板中明确禁止“自指 Commit SHA”（证据文件内只记录上游代码仓与契约文件哈希，当前证据提交自身的哈希由 Git 与 `ledger.md` 在准出后登记）。

### P-06 & P-07：主线切仓未联动测试套件、契约缺 `version_code` 位域及 M07 假阳性
- **现象与影响**：AP 主线已从 `soc-ap` 切至 `printer-soc`，但 `test_harness` 中 `check_opcode_alignment.py` 与 `run_ota_software_suite.py` 仍指向 `soc-ap`；`printer-soc` 与 `boot/bootloadermc` 使用 `(major<<24)|(minor<<16)`，而 `hil_deploy_via_minimc_ota.py` 使用 `(major<<8)|minor`、`boot/bootloaderth/tools/pack_firmware.py` 默认 `0x00010000`；且虚拟靶机 M07 测试了真实 Bootloader 并不支持的 `0x23` 4B 主动取消指令。
- **本轮应对**：在 [minimc_v2_contract.yaml](../../contracts/minimc_v2_contract.yaml) 新增 `version_code_layout` 契约锁；通过 `SLICE-01` 统一 5 端与工具脚本，清理 M07 假取消断言并补充真实 `0x24 -> NACK 0x04`、`4B 0x23 -> NACK 0x06` 与断连驻留 Bootloader 恢复测试。
- **永久改进建议**：
  1. 后续任何仓库迁移/封存任务，必须将 `test_harness/static_checks/` 与 `project-control/tools/sync_contracts.py` 纳入强制联动检查范围；
  2. 将 `version_code` 位域一致性测试直接纳入 `sync_contracts.py` 或 `check_opcode_alignment.py` 的常规门禁。

### P-08：HIL 物理台架载体切换未在 Phase 1 前置实探
- **现象与影响**：历史部署手册与早期假设绑定 VMware（`192.168.77.134` + `/dev/ttyUSB0`），直到进入执行探测才发现 VMware 离线，而真实 MC/TH 板卡当前接在 C308L 开发板（`192.168.1.101:/dev/ttyS1`），且开发板 SSH 主机公钥已更新、宿主机未连接物理 U 盘与独立 Windows `COM12/COM13` Debug 串口。
- **本轮应对**：经用户确认更新公钥后，已在 C308L `/dev/ttyS1` 实测收到真实 MC (`0x02`) 与 TH (`0x03`) 的 `0x01/0x02` 响应（均运行 `mcu-p3@97c1c242`），并据实规划在 C308L `/dev/ttyS1` 完成可执行的真机串口升降级穿刺验收、如实标记未连接硬件（物理 U 盘 / `COM12/13`）的未测边界。
- **永久改进建议**：在 `ARCH` 的 `arch-deep-spec` 与 `COORD` 的 Phase 1 收口清单中新增“**非侵入物理台架连通性预探项**”（只读检查目标 IP/串口/外设存在性），避免规划阶段沿用过时台架假设。

---

## 三、待后续批次收敛的治理任务清单（建议）

1. **[TECH-DEBT-01]** 修正 `printer-soc/contracts/twin/telemetry_types.h:410` 中过时的 `version_code` `(major<<8)|minor` 注释（来自 `SLICE-01` Codex `MINOR` 发现）。
2. **[TECH-DEBT-02]** 清理 `test_harness/static_checks/minimcproto/golden_vectors.json:G16h` 与 `run_codec_cases.py:86-88` 的中性命名（来自 `SLICE-01` Codex `NIT` 发现）。
3. **[GOVERNANCE-01]** 构建含 `arm-none-eabi-gcc` + `ninja` + `pytest` + FastDDS/D-Bus 的统一 `qa-sandbox` 镜像，并在 `slice_gate.py` 中自动保存 `integration.log` 供 Codex 审阅。
4. **[GOVERNANCE-02]** 在 `qa_runner.py` 落地受控的 `local_pre_publish_gate` 本地只读快照预检模式。
