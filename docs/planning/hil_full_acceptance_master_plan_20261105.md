---
id: PLAN-HIL-FULL-ACCEPTANCE-MASTER-20261105
title: AI SoC 首版 Web HMI 与双 MCU 端到端全量 HIL 主测试计划（冻结版）
revision: 1
date: 2026-11-05
author_role: QA
task_id: TWIN-61
covers_issues:
  - ISS-20261105-005
  - ISS-20261105-006
  - ISS-20261105-007
  - ISS-20261105-008
  - ISS-20261105-009
  - ISS-20261105-010
  - ISS-20261105-011
  - ISS-20261105-012
  - ISS-20261105-013
  - ISS-20261105-014
  - ISS-20261105-015
  - ISS-20261105-016
  - ISS-20261105-017
related_inputs:
  remediation_arch_plan: project-control/docs/architecture/twin55_issues_005_017_consolidated_remediation_plan_20261105.md
  basecases_spec: project-control/docs/planning/qa_web_hmi_basecases_20261103.md
  build_deploy_confirmation: project-control/docs/planning/web_hmi_full_qa_build_deploy_confirmation_20261105.md
status: Frozen-For-QA-Execution
---

# AI SoC 首版 Web HMI 与双 MCU 端到端全量 HIL 主测试计划（`2026-11-05` 冻结版）

## 1. 目的、适用范围与契约参数冻结

本主测试计划针对 `ISS-20261105-005` 提单要求，将 `qa_web_hmi_basecases_20261103.md`（Revision 4）、`end_to_end_physical_link_remediation_plan_20261104.md`（Revision 3）及 `twin55_issues_005_017_consolidated_remediation_plan_20261105.md`（Revision 1）中的全部待绑定阈值、47 项全量测试子例、290 帧高频突发压测规格、5 类复合业务序列及提测前环境清零 SOP 予以正式冻结，作为独立 Codex QA 执行 Stage 1（全自动 HIL 与软件/契约回归）与 Stage 2（人工物理配合窗口）的唯一权威输入。

### 1.1 全局时限、量程与哨兵参数冻结表

| 参数键名 | 冻结数值 | 契约依据与物理语义 |
| :--- | :--- | :--- |
| **`T_probe`** | **`3000 ms`** | 新机引导（OOBE）或冷启动向双 MCU 发起首次版本与在线探测的最大允许收敛时限 |
| **`T_sample`** | **`1500 ms`** | 单次温度采样请求（`POST /api/v1/temperature/sample`）从发起至快照与 UI 同步的时限 |
| **`T_save`** | **`2000 ms`** | 料槽配置保存（`action=0`）、向导完成状态保存从点击至 HTTP 200 返回的时限 |
| **`T_nav`** | **`1500 ms`** | 向导步骤切换、完成向导进入工作台及温度胶囊打开详情面板的 DOM 切换时限 |
| **`T_stale`** | **`1500 ms`** | `AISOC_FRESHNESS_STALE_MS = 1500U`、`AISOC_DEV_VER_ONLINE_TIMEOUT_NS = 1.5s`（老化预警阈值） |
| **`T_fault`** | **`3000 ms`** | `AISOC_FRESHNESS_FAULT_MS = 3000U`、`AISOC_DEV_VER_STALE_TIMEOUT_NS = 3.0s`（3s 断线离线退化硬红线） |
| **`T_recover`** | **`3000 ms`** | 物理重连或外设恢复后，重新完成探测握手并恢复 `ONLINE` / `FRESH` 的最大收敛时限 |
| **`T_relay_timeout`** | **`200 ms`** | MC 转发至 TH（`USART6 921600 8N1`）单跳级联超时窗口（超时记录 `RELAY_RX status=TIMEOUT err_code=0x03`） |
| **热床有效温度范围** | **`5.0°C ~ 130.0°C`** | `AISOC_BED_VALID_MIN_MILLIC = 5000`、`AISOC_BED_VALID_MAX_MILLIC = 130000`；MC 侧 `ADC` 有效窗 `[70, 4081]` |
| **喷头有效温度范围** | **`5.0°C ~ 300.0°C`** | `AISOC_NOZZLE_VALID_MIN_MILLIC = 5000`、`AISOC_NOZZLE_VALID_MAX_MILLIC = 300000`；TH 侧 `ADC` 有效窗 `[16, 4085]` |
| **MCU 故障温度哨兵** | **`32767` (`0x7FFF`)** | `MINIMC_TEMP_SENTINEL_FAULT`，当热敏电阻开路/短路或超物理量程时由 MCU 填入 `current_temp_deci_c` |
| **AP 传感器故障哨兵** | **`2147483647`** | `AISOC_TEMP_MILLIC_FAULT`，当 MCU 上报故障或超物理量程时由 AP 填入 `temperature_millic` |
| **AP 离线超时哨兵** | **`2147483646`** | `AISOC_TEMP_MILLIC_OFFLINE`，当节点离线或采样间隔 $\ge 3000\text{ ms}$ 时填入，且顶层 `system_status`/`device_state` 置为 `"OFFLINE"` |
| **G-code 上传准入边界** | **扩展名 `.gcode`/`.gco`/`.nc`，`0 < size <= 10 MB`** | 必须包含至少一条合法 `G0/G1/G28/G29/G90/G91/G92/M82/M83/M104/M106/M107/M109/M114/M140/M190/T0..T3` 指令（或预置白名单模型） |
| **料槽与混色准入边界** | **`slot_id/active_slot` $\in [1, 4]$，`action` $\in [0, 2]$** | 单槽 `mixing_weight` $\in [0, 10000]$，且总权重必须严格等于 `10000`；保存配置固定 `action=0, target_temp_deci_c=0` |
| **加热安全锁（Option A）** | **`heater_duty_percent == 0`** | 全程锁死物理加热占空比 0%，验证协议/控制链路而不触发真实发热风险 |

---

## 2. 提测前现场环境清零 SOP（Pre-Test Environment Reset SOP）

在每次正式 HIL 验收（或重跑）开始前，必须严格按以下 6 步执行现场环境清零，杜绝历史残留进程、旧日志或未复位状态污染本轮测试：

1. **查杀残留轮询进程并停止旧守护进程**：
   - 在 VMware（`192.168.77.134`）执行 `pkill -9 -f 'hw_sampler.py' || true`，并执行 `bash tools/deploy_twin.sh --stop --port 8080`；
   - 核验 `ps -ef` 中无 `forward_service_daemon`、`device_manager_daemon`、`ui-gateway`、`hw_sampler.py` 残留，`/dev/ttyUSB0` 无进程占用。
2. **启动双路 Debug 串口（`[MC-DBG]` / `[TH-DBG]` `115200 8N1`）只追加采集**：
   - 在板卡复位与 AP 服务启动前，率先绑定 Windows 物理调试串口（`COM12` `[MC-DBG]`、`COM13` `[TH-DBG]`），以非阻塞方式写入本轮全新 `mc_debug_raw.log` 与 `th_debug_raw.log`。
3. **双 MCU 硬件复位与动态 `boot_id` / `git_commit_short` 对账（验证 `ISS-20261105-016`）**：
   - 通过 `probe-rs.exe reset` 依次复位 MC（`AT32F435VGT7`）与 TH（`AT32F423CCT7`）；
   - 再次复位前后采集两次 `0x01 GET_VERSION -> 0x02 VERSION_REPORT`，确认双板 `boot_id` 均非零且复位前后严格变化（`boot_id_after != boot_id_before`），且上报的 `git_commit_short` 与 `mcu-p3` 当前锁定 `HEAD` 短 SHA 一致。
4. **验证 `[MC-DBG]` 与 `[TH-DBG]` 干净基线（验证 `ISS-20261105-015`）**：
   - 观察复位后 5 秒空闲窗口内的 `[MC-DBG]` 与 `[TH-DBG]` 原始流，确认**零 `adc SS_ADC_BUSY` 裸打印**，且初始 `drop=0, trunc=0`。
5. **以锁定配置启动 AP 四守护进程并核验二进制哈希与动态 `/api/v1/state`（验证 `ISS-20261105-006`）**：
   - 使用 `AISOC_AUTO_BUILD="0"` 启动 `deploy_twin.sh`，核对 4 个运行中进程 `/proc/<pid>/exe` 的 SHA256 与 `build_manifest.yaml` 完全一致；
   - 确认 `${RUNTIME_WEB_ROOT}/api/v1/state` 静态文件不存在，请求 `GET /api/v1/state` 与 `GET /api/v1/temperature/snapshot` 均返回 `Content-Type: application/json` 且 `generation`、温度、节点状态实时同步。
6. **清理残留作业并核查实机传感器初始状态（验证 `ISS-20261105-011/012`）**：
   - 调用 `POST /api/v1/jobs/cancel` 与零目标设温确保处于 `IDLE`、目标温度 `0°C`；
   - 触发一次 `POST /api/v1/temperature/sample`，记录 `bed.raw_adc` 与 `tool.raw_adc` 实测值：若台架 MC 热床热敏电阻未接（`bed.raw_adc > 4081`），确认快照如实报告 `bed.temperature_millic = 2147483647`、`sensor_status = "OPEN"`、`quality = "FAULT"`。

---

## 3. 全量 47 项冻结 HIL 测试子例规格矩阵（`HIL-CASE-01` ～ `HIL-CASE-47`）

以下 47 项测试子例将 `BASE-01～27`、`J-01`、`DELTA-DBG/BAUD/COMB` 及 `ISS-20261105-005～017` 完整拆解为独立可计数的正例（`POS`）、负例（`NEG`）、故障注入（`FAULT`）与恢复（`REC`）子项：

| 子例编号 | 映射组 / 关联 Issue | 类型 / 阶段 | 输入与操作步骤 | 预期 HTTP/API 响应 | 预期串口协议帧 (`AP↔MC↔TH`) | 预期 `[MC-DBG]` / `[TH-DBG]` 日志与 UI/物理判据 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **`HIL-CASE-01`** | `BASE-01` | POS / Stage 1 | 干净浏览器 Profile 打开首页进入 OOBE Step 1，检查初始引导拉起 | `GET /` `200 OK`；`GET /api/v1/state` `200 OK` (`application/json`) | 启动周期 `0x01 GET_VERSION`、`0x14 GET_TEMP` | `[MC-DBG]`/`[TH-DBG]` `dir=RX/TX cmd=0x01/0x02`；UI 弹出新机引导 Step 1 |
| **`HIL-CASE-02`** | `BASE-01` / `ISS-014` | NEG+REC / Stage 1 | 未接/关断串口时打开 OOBE Step 3，观察未就绪态；恢复串口后点击重新检测 | 断链时采样返回 `503` 或快照 `OFFLINE`；恢复后返回 `200` | 恢复后 `0x01->0x02`、`0x14->0x14` | 断链时 UI 显示离线未就绪；恢复后 `T_recover` (3s) 内双板显示 `ONLINE` |
| **`HIL-CASE-03`** | `BASE-02` / `ISS-016` | POS / Stage 1 | OOBE Step 3 触发双 MCU 版本与在线自检，之后复位双板再次查询 | `GET /api/v1/state` 返回 MC/TH `online=true`、非零 `boot_id` 与匹配 `commit` | `AP->MC 0x01` (`dst=2`), `AP->TH 0x01` (`dst=3`) | `[MC-DBG] dir=TX cmd=0x02 fw=2.0 boot_id=0x... commit=0x...`；复位后 `boot_id` 必变 |
| **`HIL-CASE-04`** | `BASE-02` | NEG+REC / Stage 1 | 仅使 TH 失联（SWD 关断 TH `USART1`）触发探测，随后恢复 TH `USART1` | TH 探测超时，快照 `mc=ONLINE, th=OFFLINE, device_state=OFFLINE` | `MC->TH 0x01` 无应答 | `[MC-DBG] dir=RELAY_RX node=TH cmd=0x01 status=TIMEOUT err_code=0x03`；恢复后双板 `ONLINE` |
| **`HIL-CASE-05`** | `BASE-03` | POS+REC / Stage 1 | OOBE Step 2 与顶栏切换中/英文与亮/暗主题，刷新页面验证状态 | 纯前端与本地配置读写无 HTTP 报错 | 不强制额外 MCU 帧 | 文案与主题立即切换，刷新后无白屏或脚本报错，不掩盖硬件真实状态 |
| **`HIL-CASE-06`** | `BASE-04` / `ISS-011/012` | POS / Stage 1 | OOBE Step 4 传感器检查：触发实时采样，核对温度与 `raw_adc` | `POST /api/v1/temperature/sample` `200`；快照含 `bed.raw_adc`、`tool.raw_adc` | `AP->MC 0x14`、`AP->TH 0x14` | `[TH-DBG] dir=TX cmd=0x14 status=ACK nozzle_ddC=... adc_raw=...` 与快照 `tool.raw_adc` 一致 |
| **`HIL-CASE-07`** | `BASE-04` / `ISS-011/013` | NEG+REC / Stage 1 | 设备离线或热床超量程（`>130°C` / 开路 `ADC>4081`）时查看 OOBE Step 4 与断料显示 | 快照 `bed.temperature_millic=2147483647` (`FAULT`) 或离线 `2147483646` (`OFFLINE`) | MC 上报 `0x7FFF` (`sensor_status=3/4`) | 热床显示红色故障态（严禁把 `300°C` 标绿）；离线时 4 路断料显示 `离线 / 未知`（严禁假绿） |
| **`HIL-CASE-08`** | `BASE-05` | POS+REC / Stage 1 | 点击完成向导进入工作台，刷新页面，再点击顶栏“新机引导”重开向导 | 状态保持正常，无异常控制请求 | 不触发隐式运动或加热帧 | 向导正常关闭与重开，`localStorage` 完成标志通过真实点击写入 |
| **`HIL-CASE-09`** | `BASE-06` / `ISS-006` | POS / Stage 1 | 对比 `GET /api/v1/state` 与 `GET /api/v1/temperature/snapshot` 响应头与正文 | 两者均返回 `200 OK`、`Content-Type: application/json`，`generation` 同步递增 | 随 `POST /api/v1/temperature/sample` 更新 | 顶栏网关状态、硬件在线状态及温度胶囊数值与实时快照完全一致 |
| **`HIL-CASE-10`** | `BASE-06` / `BASE-27` | NEG+REC / Stage 1 | 断开浏览器网络（CDP Offline）观察顶栏降级，恢复网络后观察重连 | 断网期间前端捕获 fetch 异常；恢复后 `GET /api/v1/state` `200` | MCU 保持正常运行，无异常复位 | 浏览器断网时顶栏显示网关连接断开且锁定控制；恢复后自动重连同步 |
| **`HIL-CASE-11`** | `BASE-07` | POS+REC / Stage 1 | 发送急停请求 `POST /api/v1/motion/stop`（或点击 E-STOP），确认急停闭环 | `POST /api/v1/motion/stop` 返回 `200 OK` (`{"status":"ok","action":"emergency_stop"}`) | `AP->MC 0x17` + `AP->TH 0x17`，双板返回 `0x05 ACK` | `[MC-DBG] dir=STATE cmd=0x17 op=STOP`、`[TH-DBG] dir=STATE cmd=0x17 target_ddC=0` |
| **`HIL-CASE-12`** | `BASE-08` / `ISS-008` | POS / Stage 1 | 在工作台点击模型卡片 `Calibration_Cube.gcode` 的“一键载入”按钮 | 仅触发 `POST /api/v1/jobs/upload` (`{"name":"Calibration_Cube.gcode","preset":true}`) `200` | **严禁下发 `0x13 JOB_CONTROL` 启动帧** | 模型名称载入 `#job-model-name`，作业状态保持 `IDLE`（不进入 `PRINTING`） |
| **`HIL-CASE-13`** | `BASE-08` / `ISS-009` | NEG+REC / Stage 1 | 调用 `POST /api/v1/jobs/upload` 传入不在白名单的伪造预置模型名 | 返回 HTTP `400 Bad Request` (`Invalid or empty G-code file`) | 无串口帧下发 | 非法预置模型被后端拒绝；随后重新载入合法预置模型成功返回 `200` |
| **`HIL-CASE-14`** | `BASE-09` / `ISS-009` | POS / Stage 1 | 通过文件控件上传合法 `valid.gcode`（含 `G28\nM114\n`） | `POST /api/v1/jobs/upload` 返回 `200 OK` (`{"status":"ok","message":"Upload staged"}`) | 暂存阶段不下发串口帧 | UI 显示上传成功并更新当前待打印模型名称为 `valid.gcode` |
| **`HIL-CASE-15`** | `BASE-09` / `ISS-009` | NEG+REC / Stage 1 | 依次上传 `invalid.txt`（非 G-code 扩展名）、`invalid.gcode`（无 G/M/T 指令）、`empty.gcode`（0B），再上传 `valid.gcode` | 三个非法文件前端拦截且后端 `POST /api/v1/jobs/upload` 均返回 HTTP `400 Bad Request` | 无串口帧下发 | 非法文件显示红色错误提示且不弹成功 alert；最后上传 `valid.gcode` 恢复成功 |
| **`HIL-CASE-16`** | `BASE-10` / `ISS-008` | POS / Stage 1 | 载入模型后显式点击 `#btn-job-start`（“开始打印”），观察作业启动闭环 | `POST /api/v1/jobs/start` 返回 `200 OK` | `AP->MC 0x13` (`op=1 START`), MC 返回 `0x13` | `[MC-DBG] dir=STATE node=MC cmd=0x13 status=OK job_state=PRINTING` |
| **`HIL-CASE-17`** | `BASE-10` | NEG / Stage 1 | 在硬件离线（503）状态下尝试调用 `POST /api/v1/jobs/start` | 返回 HTTP `503 Service Unavailable` 或 `504` | 超时无 ACK | 拒绝启动作业，严禁在无硬件 ACK 时进入本地假 `PRINTING` 状态 |
| **`HIL-CASE-18`** | `BASE-11` | POS / Stage 1 | 在 `PRINTING` 状态下依次点击“暂停”（`pause`）与“继续”（`resume`） | `POST /api/v1/jobs/pause` `200`；`POST /api/v1/jobs/resume` `200` | `AP->MC 0x13` (`op=2 PAUSE`, `op=3 RESUME`) | `[MC-DBG]` 依次输出 `job_state=PAUSED` 与 `job_state=PRINTING`，暂停期间进度不自增 |
| **`HIL-CASE-19`** | `BASE-12` | POS+REC / Stage 1 | 在途作业点击“取消”（`cancel`），确认回到 `IDLE` 并可重新启动新作业 | `POST /api/v1/jobs/cancel` 返回 `200 OK` | `AP->MC 0x13` (`op=4 CANCEL` / `op=0`) | `[MC-DBG] dir=STATE node=MC cmd=0x13 job_state=IDLE progress_permille=0` |
| **`HIL-CASE-20`** | `BASE-13` | POS / Stage 1 | 执行短作业步进（`op=4` step advance + `0x1C GCODE_EXEC`）直至完成 | 全部步进返回 `200 OK` | `AP->MC 0x13` + `MC->TH 0x1C` 级联帧 | `[MC-DBG]` 与 `[TH-DBG]` 完整记录 `0x1C` 级联闭环，进度随真实硬件 ACK 推进 |
| **`HIL-CASE-21`** | `BASE-14` / `HIL-02` | POS / Stage 1 & 2 | 发送受控小步幅点动请求 `POST /api/v1/motion/jog`（如 X/Y/Z `0.1mm`/`1mm`）并查询坐标 | `POST /api/v1/motion/jog` `200 OK` | `AP->MC 0x12 MOTION_MOVE` -> `0x16 POS_QUERY` | `[MC-DBG] dir=STATE cmd=0x12 op=MOVE` 且 `MC_DBG_LINE_MAX_LEN=256` 下 204B 行 `trunc=0`（Stage 2 人工核验物理位移） |
| **`HIL-CASE-22`** | `BASE-14` | NEG / Stage 1 | 发送缺参数或空轴掩码的非法点动请求 | 返回 HTTP `400` 或按契约拦截 | 不产生非法越界步进 | 系统保持稳定，后续合法点动正常响应 |
| **`HIL-CASE-23`** | `BASE-15` / `HIL-02` | POS / Stage 1 & 2 | 发送归零请求 `POST /api/v1/motion/home`（`axes_mask=0x07`） | `POST /api/v1/motion/home` 返回 `200 OK` | `AP->MC 0x11 MOTION_HOME` -> `0x16 POS_QUERY` | `[MC-DBG] dir=STATE cmd=0x11 status=OK op=HOME axes_mask=0x07 x_mm_x100=0 y_mm_x100=0 z_mm_x100=0 homed_mask=0x07` |
| **`HIL-CASE-24`** | `BASE-16` / `HIL-03` | POS / Stage 1 & 2 | 发送调平触发与 5×5 网格读取 `POST /api/v1/motion/level` | `POST /api/v1/motion/level` 返回 `200 OK` | `AP->MC 0x1A LEVEL_TRIGGER` + `0x18 LEVEL_GRID_QUERY` | `[MC-DBG] dir=STATE cmd=0x18 status=OK op=GRID_READ probe_idx=7 z_offset_um=... grid_valid=1 status=DONE` |
| **`HIL-CASE-25`** | `BASE-17` / `ISS-007` | POS / Stage 1 | 在工作台点击 `#btn-save-slots`（“保存料槽映射配置”） | `POST /api/v1/filament/slots` 请求体为 `action:0, target_temp_deci_c:0`，返回 `200 OK` | `AP->MC 0x19` (`slot_id=0..3, action=0`) -> `MC->TH 0x19` | **严禁触发 `action=1 (LOAD)` 或 `210°C` 设温**；`[TH-DBG]` 显示 `op=SELECT`、`step_state=DONE` |
| **`HIL-CASE-26`** | `BASE-18` / `HIL-04` | POS / Stage 1 & 2 | 切换单色/双色/四色混色预设（权重和 `10000`），分别测试显式选槽（`action=0`）、进丝（`action=1`）、退丝（`action=2`） | `POST /api/v1/filament/slots` 返回 `200 OK` | `AP->MC 0x19` -> `MC->TH 0x19` 级联往返 | `[MC-DBG] RELAY_TX/RELAY_RX cmd=0x19`、`[TH-DBG] op=SELECT/LOAD/UNLOAD` 一致 |
| **`HIL-CASE-27`** | `BASE-19` / `ISS-010` | NEG+REC / Stage 1 | 向 `POST /api/v1/filament/slots` 依次发送：`total_mixing_weight=9999`、通道权重 `[-1, 10001]`、`slot_id=5`、`action=-1`，最后发送合法配置恢复 | 四组非法输入均在网关入口立即返回 **HTTP `400 Bad Request`**（严禁返回 `200` 或 `504`） | 非法请求在 AP 网关拦截，不下发至串口 | 恢复请求（`slot_id=1, action=0, total_mixing_weight=10000`）返回 `200 OK` |
| **`HIL-CASE-28`** | `BASE-19` / `ISS-010(MC)` | NEG+REC / Stage 1 | 直接向 MC 协议层注入越界 `0x19` 帧（`slot_id=4` 或 `action=4`） | 协议层返回 `0x06 NACK` (`err_code=0x03`) | `MC->AP 0x06 NACK` (`err_code=0x03`) | `[MC-DBG] dir=ERR node=MC cmd=0x19 status=BAD_PAYLOAD err_code=0x03`，严禁 `& 0x03U` 掩盖 |
| **`HIL-CASE-29`** | `BASE-20` / `ISS-011/012` | POS / Stage 1 | 打开温度监控面板，触发新采样并发送受控目标设温 `POST /api/v1/temperature/set`（Option A 0% PWM）后归零 | `POST /api/v1/temperature/set` `200 OK`；快照包含真实 `raw_adc` | `AP->MC 0x10` -> `MC->TH 0x10` 级联设温；`0x14` 温度采样 | `[MC-DBG]`/`[TH-DBG]`、`GET /api/v1/state` 与温度面板 ADC 数值三方一致；`heater_duty_percent=0` |
| **`HIL-CASE-30`** | `BASE-20` / `ISS-011` | NEG+REC / Stage 1 | 热床超量程（如 MC `raw_bed=300°C` 或 `ADC>4081`/`<70`）时检查 MC、AP 与 Web HMI 降级表现 | 快照 `bed.temperature_millic=2147483647`、`sensor_status="OPEN"/"SHORT"`、`quality="FAULT"` | `MC->AP 0x14` 携带 `current_temp_deci_c=0x7FFF` 与真实 `raw_adc` | Web HMI 热床卡片与 OOBE 徽章显示红色 `异常/故障`，严禁将 `300.0°C` 显示为绿色正常 |
| **`HIL-CASE-31`** | `BASE-21` / `ISS-013` | NEG / Stage 1 | 在硬件离线（`hwOnline=false`）时检查 OOBE Step 4 与工作台 4 路断料传感器状态 | 快照 `device_state="OFFLINE"` | 无在线采样帧 | OOBE 与工作台 4 路断料传感器均显示 `离线 / 未知`（非绿色） |
| **`HIL-CASE-32`** | `BASE-21` | POS+REC / Stage 2 | 在线状态下在物理台架逐路触发 4 路断料光电传感器并恢复（人工物理窗口） | 快照与遥测同步更新 `filament_present_mask` | `0x14`/`0x19` 报告实时 `present_mask` | `[TH-DBG] filament_present_mask` 随物理抽插丝变化（若台架无四路物理夹具则按规则记 Stage 2 阻塞） |
| **`HIL-CASE-33`** | `BASE-22` | POS / Stage 1 | 打开网络发现面板，验证主机地址展示与链接复制交互 | `GET /` 与静态资源 `200 OK` | 不要求 MCU 帧 | 网络面板正确展示当前可访问地址；跨网段 mDNS 按实际网络多播能力如实记录 |
| **`HIL-CASE-34`** | `BASE-23` | POS+NEG+REC / Stage 1 | 健康态检查无虚假 HMS 告警；注入通信超时故障触发 HMS 告警，恢复链路后验证告警消退 | 故障时 `device_state="OFFLINE"` / `is_fault=true`；恢复后归零 | 故障时超时，恢复后 `0x14->0x14` 成功 | 告警面板在故障时显示结构化告警，恢复新鲜采样后恢复正常态 |
| **`HIL-CASE-35`** | `BASE-24` / `HIL-06` | FAULT+REC / Stage 2 | **物理拔除业务 USB 串口线（`/dev/ttyUSB0`）** 保持 > 3.0s，测量 CPU 占用与状态降级，再插回恢复（Stage 2 人工物理窗口） | 拔线 $\ge 3.0\text{s}$ 内 `device_state="OFFLINE"`、温度=`2147483646`、控制请求返回 `503`；插回后恢复 `200` | 拔线期间无业务帧，插回后重握手成功 | 拔线期间 AP 守护进程 CPU 占用 $\le 2\%$；Web 界面锁定控制；插回后 `T_recover` (3s) 内恢复 |
| **`HIL-CASE-36`** | `BASE-25` / `ISS-014` | FAULT+REC / Stage 1 | **TH `USART1` 外设断链 > 3.0s 故障注入与恢复**：SWD 备份并置零 TH `USART1->CTRL1`，触发采样并等待 `3.2s`，验证退化后精确恢复 `CTRL1` | 断链 `3.2s` 后 `GET /api/v1/state` 返回 `th.state="OFFLINE"`、`tool.temperature_millic=2147483646`、`device_state="OFFLINE"`；控制返回 `503` | `MC->TH` 级联超时 | `[MC-DBG] RELAY_RX node=TH status=TIMEOUT`；恢复 `CTRL1` 并重采样后恢复 `ONLINE` 与真实温度 |
| **`HIL-CASE-37`** | `BASE-25` / `ISS-014` | FAULT+REC / Stage 1 | **MC `USART2` 外设断链 > 3.0s 故障注入与恢复**：SWD 备份并置零 MC `USART2->CTRL1`，触发采样并等待 `3.2s`，验证退化后精确恢复 `CTRL1` | 断链 `3.2s` 后 `GET /api/v1/state` 返回 `mc.state="OFFLINE"`、`bed.temperature_millic=2147483646`、`device_state="OFFLINE"`；控制返回 `503` | `AP->MC` 串口超时，发射 `LinkStateChanged(false)` | AP 进程 CPU 占用 $\le 2\%$；恢复 `CTRL1` 并重采样后双节点恢复 `ONLINE` |
| **`HIL-CASE-38`** | `BASE-26` | POS+REC / Stage 1 | 验证首次打开向导、完成向导后刷新保持、手动重呼向导及服务受控重启后恢复四个生命周期场景 | 重启后 `GET /api/v1/state` 与 `GET /api/v1/temperature/snapshot` 正常恢复 | 服务重启后自动完成首轮版本与温度探测 | 重启前后已归档日志，新进程 `/proc/<pid>/exe` 哈希一致 |
| **`HIL-CASE-39`** | `API-NEG-UNKNOWN` / `ISS-017` | NEG / Stage 1 | 请求未知 API 路由 `POST /api/v1/temperature/target`（及 `GET /api/v1/unknown`） | 返回 HTTP `404 Not Found`，`Content-Length: 35`，完整返回 35B `{"error":404,"message":"Not Found"}` | 无串口帧 | `curl` 退出码 `0`（零字节截断，彻底消除 `curl: (18) transfer closed with 31 bytes remaining`） |
| **`HIL-CASE-40`** | `DELTA-DBG` / `ISS-015` | POS+NEG / Stage 1 | 检查正常观测窗口与高频查询下的 `[MC-DBG]` / `[TH-DBG]` 连续性、无裸 `adc SS_ADC_BUSY`、204B `POS_QUERY` 零截断 | 查询接口全部 `200 OK` | `0x14`、`0x16`、`0x18` 正常收发 | `[MC-DBG]` 无 `adc SS_ADC_BUSY` 混入；`MC_DBG_LINE_MAX_LEN=256` 下 `trunc=0, drop=0` |
| **`HIL-CASE-41`** | `DELTA-BAUD` | POS / Stage 1 | 核验 AP（`/dev/ttyUSB0`）、MC（`USART2` & `USART6`）、TH（`USART1`）全部工作在 `921600 8N1`，执行 **290 帧高频突发压测** | 压测期间全部 RPC/API 正常响应 | 连续 290 帧（`seq=1..290`）双向收发无丢包 | `seq` 跨越 `255 -> 256..290` 无 8-bit 截断；`CRC_ERR=0, BAD_FRAME=0, drop=0, trunc=0` |
| **`HIL-CASE-42`** | `DELTA-COMB-SEQ-01` | POS / Stage 1 | **复合序列 1**：OOBE 探测 -> 双板版本/动态 `boot_id` 校验 -> 双端温度与真实 `raw_adc` 采样对账 | 全链路 `200 OK` | `0x01->0x02` (MC/TH) + `0x14->0x14` (MC/TH) | 四方对账（HTTP <-> AP <-> `[MC-DBG]` <-> `[TH-DBG]`）100% 匹配 |
| **`HIL-CASE-43`** | `DELTA-COMB-SEQ-02` | POS / Stage 1 | **复合序列 2**：三轴归零（`0x11`）-> 调平触发与网格读取（`0x1A`+`0x18`）-> XYZ 点动（`0x12`）-> 位置查询（`0x16`） | 全链路 `200 OK` | `0x11 -> 0x1A -> 0x18 -> 0x12 -> 0x16` | `[MC-DBG]` 完整记录 `HOME -> LEVEL_TRIGGER -> GRID_READ -> MOVE -> POS_QUERY` 且 `trunc=0` |
| **`HIL-CASE-44`** | `DELTA-COMB-SEQ-03` | POS+NEG / Stage 1 | **复合序列 3**：设温（`0x10` 0% PWM）-> 料槽配置保存（`action=0` 不触发进丝）-> 显式进退丝（`action=1/2`）-> 非法权重/槽位 `400` 拦截与恢复 | 正例 `200 OK`，负例 `400 Bad Request` | `0x10` + `0x19` (MC->TH 级联) | 完整验证 `ISS-007` 与 `ISS-010` 修复闭环 |
| **`HIL-CASE-45`** | `DELTA-COMB-SEQ-04` | POS+NEG / Stage 1 | **复合序列 4**：非法 G-code 上传 `400` 拒绝 -> 合法模型载入（`upload` 不自动启动）-> 显式启动（`0x13`）-> `0x1C` 级联步进（`seq>255`）-> 暂停 -> 继续 -> 取消 | 负例 `400`，正例全流程 `200 OK` | `0x13` (`op=1,4,2,3,4`) + `0x1C` (`MC->TH`) | 完整验证 `ISS-008`、`ISS-009` 及 16-bit `seq` G-code 级联闭环 |
| **`HIL-CASE-46`** | `DELTA-COMB-SEQ-05` | FAULT+REC / Stage 1 | **复合序列 5**：急停（`0x17`）-> 外设断链 > 3.0s 触发 `OFFLINE` 与 `2147483646` 哨兵及 `503` 锁定 -> 恢复重连重采样 -> 未知路由 `404` 完整帧验证 | 断链 `503`、未知路由 `404` (35B 完整)、恢复 `200` | `0x17` -> 断链超时 -> 恢复后 `0x01`/`0x14` | 完整验证 `ISS-013`、`ISS-014`、`ISS-017` 修复闭环 |
| **`HIL-CASE-47`** | `J-01` | POS / Stage 1 & 2 | **跨功能端到端主旅程（`J-01`）**：串联 `SEQ-01` ➔ `SEQ-02` ➔ `SEQ-03` ➔ `SEQ-04` ➔ `SEQ-05` 全旅程连续执行无人工篡改状态 | 全旅程正负例响应 100% 符合契约 | 全旅程序列号连续、CRC 100% 合法 | 全程 `[MC-DBG]` / `[TH-DBG]` `CRC_ERR=0, BAD_FRAME=0, drop=0, trunc=0` |

---

## 4. 290 帧高频突发压测精确规格（`DELTA-BAUD-BURST-290`）

为严格验证 `921600 8N1` 波特率、16-bit 序列号跨越 `255 -> 256+` 不回绕、以及 `[MC-DBG]`（`MC_DBG_LINE_MAX_LEN=256U`、`MC_DBG_RING_CAPACITY=4096U`）与 `[TH-DBG]`（`2048U` DMA 环形缓冲）在高负载下的非阻塞排空能力，冻结 290 帧突发压测规格如下：

### 4.1 290 帧构成与序列号编排
- **总帧数**：**`290` 帧**（连续递增 16-bit `seq` 从 `1` 至 `290`，显式覆盖 `seq = 1..255` 与 `seq = 256..290` 跨 8-bit 边界区间）。
- **帧类型周期混合分布（每 10 帧为一个均衡业务周期，共 29 个周期 = 290 帧）**：
  1. `offset 0`: `AP -> MC` (`dst=0x02`) `0x01 GET_VERSION`（无载荷，14B）
  2. `offset 1`: `AP -> TH` (`dst=0x03`, 经 MC 级联) `0x01 GET_VERSION`（无载荷，14B）
  3. `offset 2`: `AP -> MC` (`dst=0x02`) `0x03 PING`（4B 时间戳载荷，18B）
  4. `offset 3`: `AP -> TH` (`dst=0x03`, 经 MC 级联) `0x03 PING`（4B 时间戳载荷，18B）
  5. `offset 4`: `AP -> MC` (`dst=0x02`) `0x14 GET_TEMP`（无载荷，14B，触发 `200B+` 状态与温度报告）
  6. `offset 5`: `AP -> TH` (`dst=0x03`, 经 MC 级联) `0x14 GET_TEMP`（无载荷，14B）
  7. `offset 6`: `AP -> MC` (`dst=0x02`) `0x16 POS_QUERY`（无载荷，14B，触发 ~204B 长行 `[MC-DBG]` 日志以检验 `MC_DBG_LINE_MAX_LEN=256U` 零截断）
  8. `offset 7`: `AP -> MC` (`dst=0x02`) `0x18 LEVEL_GRID_QUERY`（1B `probe_idx = seq % 25`，15B）
  9. `offset 8`: `AP -> MC` (`dst=0x02`) `0x19 SLOT_SELECT`（3B `{slot_id = seq % 4, action = 0, param = 0}`，17B，触发 MC->TH 自动级联）
  10. `offset 9`: `AP -> MC` (`dst=0x02`) `0x1C GCODE_EXEC`（`M114` 只读 G-code，触发 MC->TH `0x1C` 级联）

### 4.2 发送速率与窗口时长
- **帧间发送间隔（Pacing）**：默认 **`20 ms` / 帧**（50 fps 突发速率，总压测窗口约 **`5.8 s`**），且每条级联帧严格等待前一条在途级联完成后发出。
- **客观通过判据（Pass Criteria）**：
  1. **100% 响应完成率**：290 帧全部收到匹配的 `ACK` / 业务响应帧，零超时（`TIMEOUT = 0`）；
  2. **16-bit 序列号完整性**：`seq = 256..290` 在业务响应帧、`[MC-DBG]`（`seq=` 与 `ack_seq=`）及 `[TH-DBG]`（`seq=`）中 100% 原样输出十进制 `256..290`，严禁回绕为 `0..34`；
  3. **零协议错误**：`[MC-DBG]` 与 `[TH-DBG]` 中 `status=CRC_ERR` 计数为 `0`，`status=BAD_FRAME` 计数为 `0`；
  4. **零日志截断与零丢弃**：压测窗口内 `[MC-DBG]` 与 `[TH-DBG]` 的 `drop_delta == 0`、`trunc_delta == 0`，且无任何 `adc SS_ADC_BUSY` 裸文本。

### 4.3 固化自动化脚本入口
- 脚本路径：[`test_harness/hil/tests/test_290_frame_burst_stress.py`](file:///home/sushaohua/workspace/ai_soc_project/test_harness/hil/tests/test_290_frame_burst_stress.py)
- 支持模式：
  - `--self-test`（或 `unittest` 发现执行）：运行宿主机真实 C 固件协议栈桥接 / 确定性帧生成与四方对账自检，验证 290 帧编排、`seq > 255` 校验器及 `CRC_ERR/BAD_FRAME/drop/trunc` 门禁逻辑；
  - `--live --http-base http://192.168.77.134:8080 --mc-log <path> --th-log <path>`：在实机 HIL 环境驱动真实业务突发并产出 JSON 对账证据报告。

---

## 5. 5 类复合业务序列自动化脚本规格（`DELTA-COMB-SEQ-01..05`）

- 脚本路径：[`test_harness/hil/tests/test_composite_lifecycle_sequences.py`](file:///home/sushaohua/workspace/ai_soc_project/test_harness/hil/tests/test_composite_lifecycle_sequences.py)
- 覆盖 5 类端到端复合序列：
  1. **`SEQ-01`（OOBE 探测 + 双板动态 `boot_id` + 温度与 `raw_adc` 映射对账）**：覆盖 `ISS-006`、`ISS-011`、`ISS-012`、`ISS-016`；
  2. **`SEQ-02`（归零 -> 25 点网格调平 -> XYZ 点动 -> 坐标查询无截断闭环）**：覆盖 `HIL-02`、`HIL-03`、`ISS-015`；
  3. **`SEQ-03`（0% 安全设温 -> 料槽保存不触发 LOAD -> 显式进退丝 -> 混色/槽位 400 负例与 MC 0x19 NACK 0x03）**：覆盖 `ISS-007`、`ISS-010`；
  4. **`SEQ-04`（G-code 上传 400 双重校验 -> 模型一键载入不自动启动 -> 显式启动 -> 0x1C 级联步进 -> 暂停 -> 继续 -> 取消）**：覆盖 `ISS-008`、`ISS-009`、`HIL-05`；
  5. **`SEQ-05`（急停 -> 3.0s 断链离线哨兵 `2147483646` 与 OOBE 断料去假绿 -> 链路恢复 -> 未知路由 404 完整正文校验）**：覆盖 `ISS-013`、`ISS-014`、`ISS-017`、`HIL-06`。
