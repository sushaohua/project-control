# COORD 接管交接备忘录 (Account Switch Handoff)

- **交接时间**：2026-11-06 17:18 (UTC+8)
- **交接原因**：用户切换 Antigravity 客户端登录账号，在完成当前阶段物证准备后安全平稳交接。
- **交接前角色**：`COORD`（会话 ID：`ff2fb105-fd84-4ecb-b1e6-8f8eb00badc6`）
- **接收角色**：新会话 `COORD`

---

## 1. 仓库与代码基线（全部已同步至服务器）

| 仓库名称 | 分支 | 锁定 Commit | 状态 |
| :--- | :--- | :--- | :--- |
| `project-control` | `main` | `5cbe3ef` (本交接文档提交将更新至最新 HEAD) | 工作区干净，包含 `qa_01` 完整物证 |
| `soc-ap` | `main` | `7184edfc796923e2f2c6e3e57ef3a9f791164b51` | 工作区干净，零未提交修改 |
| `mcu-p3` | `feat/soc-debug` | `3f1cfa66c6d27422cf038936b29aca7e45edb511` | 工作区干净，零未提交修改 |
| `test_harness` | `main` | `cf81195eca55bcd772ef2daa2fd4aa41634c1492` | 工作区干净，零未提交修改 |
| `boot/bootloadermc` | `soc_debug` | `faa2ed00dc9b6c8567dd44e875028f65073aab62` | 工作区干净，零未提交修改 |
| `boot/bootloaderth` | `soc_debug` | `64b7100d3b0260ad1c24b627986475dcd45ad383` | 工作区干净，零未提交修改 |

---

## 2. 核心任务卡状态：`TWIN-67` (Revision 2)

- **任务卡位置**：`project-control/.agents/kanban/microtasks/vmware_soc_twin/TWIN-67.md`
- **任务目标**：`REQ-20261105-003` 真实物理 HIL 全链路升级验收、MC U 盘完整回归与升级部署说明书非实现者实操验证
- **当前状态**：`status: InProgress`, `revision: 2`, `owner: INTEGRATOR`, `run_id: author_02`
- **首轮 QA 审阅结果**：
  - 独立 Codex QA 会话：`01a1b00f-f9ab-7f62-82fb-bc5c1712626b`
  - 审阅报告：`project-control/docs/evidence/twin/TWIN-67/runs/qa_01/qa_review_report.md`
  - 审阅结论：`REJECTED`
  - 阻断项及整改进展：
    1. **Finding-1（写入范围）**：`author_02` 必须保持纯净提交，仅允许修改 `docs/guides/minimc_v2_mcu_upgrade_and_hil_deployment_manual_20261105.md` 和 `docs/evidence/twin/TWIN-67/**`。
    2. **Finding-2（U 盘真实烧录回归）**：用户已确认将包含 `fw_mc.bin`（383,272 字节）的 FAT32 U 盘重新插入了 MC 主板（AT32F435）的 USB-A 接口。只需复位 MC 进入 Bootloader 即可完成烧录，捕获 Bootloader 升级日志及重命名为 `FW_MC.CUR` 的记录。
    3. **Finding-3（TH 错板零擦除）**：测试脚本已在 `/tmp/twin67_rev2/run_stepB2_n05_n08.py` 准备就绪，在发送错板与超限 NACK 后立即发送 `0x23 CMD_OTA_STATUS` 查询 `bytes_written=0`。
    4. **Finding-4（H06 非实现者实操）**：在说明书中补充非实现者独立核验记录。
    5. **Suggestion-1（遥测一致性）**：台架无热敏传感器时的哨兵值说明已就绪。

---

## 3. 本地已就绪的执行资产与环境

1. **固件文件**：
   - MC 打包固件：`/tmp/twin67_rev2/out/fw_mc.bin`（以及 Windows 桌面 `C:\Users\EDY\Desktop\fw_mc.bin`）
2. **测试脚本**：
   - `/tmp/twin67_rev2/run_stepB2_n05_n08.py`（自动化执行 TH N05 零擦除与 OTA）
3. **物理日志记录器**：
   - 正在 Windows 后台监听：`C:\Users\EDY\AppData\Local\Temp\twin67_rev2_dbg\capture_dbg.ps1`
   - 日志文件：`C:\Users\EDY\AppData\Local\Temp\twin67_rev2_dbg\mc_com12.log` 与 `th_com13.log`
4. **硬件台架通信**：
   - VMware 地址：`192.168.77.134`（`ssh vmware`）
   - 业务串口：`ssh vmware` 上的 `/dev/ttyUSB0`（波特率 `921600`）
   - 物理串口：Windows 上的 `COM12` (MC Debug) 和 `COM13` (TH Debug)

---

## 4. 接管 COORD 的下一步操作指南

新会话拉起后，新 COORD 角色仅需执行以下操作即可迅速闭环 `TWIN-67`：

1. **拉起 `INTEGRATOR` 或执行实测采集**：
   - 运行 `/tmp/twin67_rev2/run_stepB2_n05_n08.py` 捕获 TH 包含 `0x23` 状态查询的 N05 零擦除证据；
   - 通过 VMware `/dev/ttyUSB0` 向 MC 下发进入 Bootloader 指令（或重启 MC），MC Bootloader 会自动扫描 U 盘中的 `fw_mc.bin` 并烧录，记录 `COM12` 日志为 `stepB5_mc_udisk_regression.log`；
2. **整理物证并提交候选**：
   - 将采集到的日志放入 `project-control/docs/evidence/twin/TWIN-67/runs/author_02/`；
   - 更新说明书 `minimc_v2_mcu_upgrade_and_hil_deployment_manual_20261105.md`；
   - 仅对上述允许路径提交 Git，生成纯净的 `candidate_commit`，并更新 `TWIN-67.md` 状态为 `Review`；
3. **启动第 2 轮独立 QA**：
   - 运行 `python3 /home/sushaohua/.gemini/antigravity-cli/brain/ff2fb105-fd84-4ecb-b1e6-8f8eb00badc6/scratch/run_twin57_61_qa.py TWIN-67`（或将其复制到新会话 scratch 运行）；
   - 获得 `APPROVED` 结论后，关闭 `TWIN-67` 并完成 `REQ-20261105-003` 总体验收。
