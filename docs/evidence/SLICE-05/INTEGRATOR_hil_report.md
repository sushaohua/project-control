# SLICE-05 纯串口真机 HIL 穿刺验收报告 (`C308L /dev/ttyS1 @ 921600`)

- **执行角色**：`INTEGRATOR`（严格零业务仓改动 `diff_budget: max_files=0`）
- **物理台架**：`root@192.168.1.101`（`Linux (none) 5.15.137-g083fce9cdb51 #4 SMP PREEMPT armv7l`），直连真实 UART `/dev/ttyS1 @ 921600 8N1 raw termios` ➔ 真实 MC (`0x02`) ➔ 级联真实 TH (`0x03`)
- **安全与防伪门禁**：
  - 全程禁用探针（`probe-rs` / OpenOCD / SWD / JTAG）：`probe_rs_used: false`
  - Option A 加热安全锁死 `0%`：`heating_pwm_pct: 0`（全程所有 `0x10`/`0x15` 目标温度与占空比均为 `0`）
  - 物理串口硬件绑定：`/sys/class/tty/ttyS1/device` ➔ `/sys/devices/platform/soc/fe000000.apb4/fe080000.serial` (`amlogic,meson-uart`)，无任何 PTY 虚拟设备或后台守护进程占用
- **条件准出裁决与技术债范围**：
  - **总体结论**：**PASS（`passed: true`，按已批准 `DEC-REM-1=A` 条件准出）**
  - **`HIL-FINDING-01`（`B4_TH` L3 透明路由与正交双平面）**：**真机闭环消缺通过**。在 MC 升级至 `mcu-p3@7b623d9a` (`0x7B623D9A`) 后，于 L3 `5000ms` 活跃租约期内下发 `DST=0x03 CMD=0x24`，在 `2.34ms` 内实测收到 `SRC=0x03 CMD=0x06 NACK err=0x04`（零 `SRC=0x02 NACK 0x05` 拦截）；`0x23(4B)`、`0x01/0x03/0x14` 双向无阻塞透传、`DST=0x02 0x01/0x03/0x14` 本地查询零阻塞、`DST=0x02 0x10(0,0)` 平面 B 本地级联让路回 `NACK 0x05` 全部实测通过；`B2_TH` 结束 `0.0001s`（`<1.0s`）内无等待直切 `DST=0x02 0x1D(2)` 立即获 `SRC=0x02 CMD_ACK` 并于 `0.6984s`（`<2.0s`）进入 MC Bootloader；静默 `5.5064s`（`>=5.2s`）后 `0x10(0,0)` 恢复 `SRC=0x02 CMD=0x15`（`duty=0%`）且 `361.02ms` 被动监听零幽灵 `NACK 0x03`。
  - **`HIL-FINDING-02`（`B4_MC` MC Bootloader `boot_id` 跨软复位未刷新）**：**已批准豁免入账（`waived: true`）**。按实施方案 `v1.5` 及 `project-control/slices/ledger.md` 登记的非阻断已接受技术债，如实记录 MC Bootloader (`commit=0x4FC171EA`) 在 `B4_MC` 软复位前后维持 `boot_id=0xC1E6CD05`，随后 `B2_MC` 全量重刷恢复 `0x7B623D9A` App（`boot_id=0x8F1F2C60`）。
  - **`DEC-REM-1=A` 条件准出声明**：按用户已批准的 `DEC-REM-1=A` 范围，C308L 纯串口全链路 `B0_MC_ROLLOUT`、`B1`、`B2_TH`、`IMMEDIATE_TH_TO_MC`、`B3_TH/MC`、`B4_TH/MC`、`B2_MC`、`POST_RECOVERY` 全绿准出；未连接物理硬件的 `B5` 物理 U 盘插拔、独立 Debug UART 与 C308L `printer-soc` REST 守护进程在本报告第 6 节诚实标为 **`[UNVERIFIED / PENDING]`** 且非阻断。

---

## 1. 固件制品与物理硬件溯源物证

### 1.1 固件包校验基准
| 目标节点 | 升级包路径 | 总字节 / 净荷 / 分块 | `fw_version` | 净荷 `CRC32` | 净荷 `SHA256` |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **MC (`0x02`)** | `/tmp/slice04_pkg/fw_mc_v2_0_l3.bin` | `384,240 B` / `384,112 B` / `751` 块 (`512B`) | `0x02000100` | `0x8DC0DC33` | `4ec90793f6feb49c171668203da60dc0f6548d7bf5e3c328f866b84eed0b8ad8` |
| **TH (`0x03`)** | `/tmp/slice04_pkg/fw_th_v2_0.bin` | `76,992 B` / `76,864 B` / `151` 块 (`512B`) | `0x02000100` | `0x6E82DD49` | `ac48de349be04c2a2a1f8de15cc965b8eca04517f66de625cedb8216ed52aeb7` |

### 1.2 物理串口溯源与中断增量（采自 `ttyS1_hw_provenance.log`）
| 溯源维度 | 实测物理证据 |
| :--- | :--- |
| **设备节点与权限** | `/dev/ttyS1` (`crw-rw---- 1 root root 240, 1`)，测试前后 `fuser` / `ps` 占用检查为空 |
| **Sysfs 物理绑定** | `/sys/class/tty/ttyS1/device` ➔ `/sys/devices/platform/soc/fe000000.apb4/fe080000.serial` (`compatible: amlogic,meson-uart`)，无 PTY |
| **驱动字节统计 (`/proc/tty/driver/meson_uart`)** | 测试前 `tx:1430442 rx:181831` ➔ 测试后 `tx:2315730 rx:214138`（串口实发 `+885,288 B` / 实收 `+32,307 B`；注：`/proc/tty/driver/serial` 在 Amlogic 内核中不存在，使用 `meson_uart` 替代） |
| **UART IRQ 37 中断计数 (`/proc/interrupts`)** | `irq_before = 199121` ➔ `irq_after = 247219` ➔ **`irq_delta = 48098`**（`>> 100` 门禁） |
| **Raw Hex 日志哈希** | [hil_raw_hex.log](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/evidence/SLICE-05/hil_raw_hex.log)：`3,565` 行，`1,754` TX / `1,754` 有效 RX / `29` 复位轮询超时，`SHA256 = 05d19e3ad42f8c135973f2271253c273ce431aae50cd5d87236edd35b35225bb` |
| **硬件溯源日志 / 部署回执** | [ttyS1_hw_provenance.log](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/evidence/SLICE-05/ttyS1_hw_provenance.log) · [hil_deployment_receipt.json](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/evidence/SLICE-05/hil_deployment_receipt.json) |

---

## 2. 升级演进全历史与连续 10 阶段实测矩阵

### 2.1 演进全历史透明说明（含前序初始灰度升级记录）
- **初始首次灰度轮次（`12:48:12+08:00`）**：在台架初始状态下采得现网双板均为 `mcu-p3@b865222c`（`MC boot_id=0x02789779, commit=0xB865222C, duty=0%`；`TH boot_id=0xC7076DA8, commit=0xB865222C, duty=0%`），随后通过纯串口 OTA `[B0_MC_ROLLOUT]` 成功将 MC 从 `0xB865222C` 升级至 `mcu-p3@7b623d9a`（`0x7B623D9A`, `boot_id=0x05139CA3`）。该轮在 `B3_TH` 停止，实测发现若直接将 `fw_mc_v2_0_l3.bin` 原始尺寸（`384,112 B`）填入 `0x20`，因 `384,112 > 241,664`（`APP_MAX_SIZE`），`boot/bootloaderth/src/iap.c:348` 会先于 `board_id` 检查返回 `NACK 0x14`（而非 `NACK 0x06`），随后采用合法分区尺寸 `76,864 B` + MC `board_id (0x43500001)` 隔离验证错板拒绝 `NACK 0x06`。
- **次轮复测发现的真机 Boot 窗口边界（`12:50:13+08:00`）**：该轮实测通过 `B1` (`MC=0x7B623D9A, TH=0xB865222C`)、`B0_MC_ROLLOUT`、`B3_TH`、`B4_TH`、`B2_TH`（TH 从 `0xB865222C` 升至 `0x7B623D9A`, `boot_id=0x6532C5B6`）与 `IMMEDIATE_TH_TO_MC`（`gap=0.0001s, entry=0.6988s`）；随后在 `B3_MC` 静默等待 `2.50s` 时，实测发现 MC Bootloader 启动先耗费 `~0.64s`（EEPROM 探测 + USB 主机初始化 `delay_ms(200)`）再进入 `2000ms` 探测窗（总计 `~2.64s`），导致 `2.505s` 发送的 `0x01` 恰好落入窗口尾部并触发 `boot_uart_ota.c:327` `s_ota.stay_in_boot = 1U` 而驻留 Boot。随后将 `B3_MC` 静默等待调整为 `3.30s`（对齐 `SLICE-03` 基线），验证 MC App 正常恢复上线。
- **规范全闭环归档轮次（`12:52:17+08:00`, 本文及回执完整绑定此单次无中断会话）**：在双板均运行正式应用态下完整执行 10 阶段闭环，`1,754` TX / `1,754` RX 全数闭合。

### 2.2 连续 10 阶段实测结果汇总表
| 阶段标签 | 实测结论 | 关键实测指标与时间数据 | 原始帧佐证摘要（`hil_raw_hex.log`） |
| :--- | :--- | :--- | :--- |
| **`B1`** | **PASS** | MC (`0x7B623D9A`, `boot_id=0x29199E72`, `Bit31=0`, `duty=0%`)；TH (`0x7B623D9A`, `boot_id=0x6532C5B6`, `Bit31=0`, `duty=0%`) | `TX 55aa010205010400010000004d68` ➔ `RX 55aa0201060204000100100002000200729e19299a3d627b0300000095fe` |
| **`B0_MC_ROLLOUT`** | **PASS** | 进 MC Boot (`0x4FC171EA`, `boot_id=0xC1E6CD05`, `Bit31=1`)；`751` 块 (`384,112 B`, `0` 重传)；Chunk0/Finish 前 `0x23` (`512` / `384,112`)；新 MC App 上线 (`0x7B623D9A`, `boot_id=0x11ED5521`, `Bit31=0`) | `0x23` pre-finish: `RX 55aa0201...0300000270dc0500335d`；新 App `0x02`: `boot_id=0x11ED5521` |
| **`B3_TH`** | **PASS** | `0.1649s` 进 TH Boot (`0x769FCCBE`, `0xE0080423`, `boot_id=0x4F0708F0`)；错板 `0x20` (`board_id=0x43500001`) 回 `SRC=0x03 NACK 0x06` (`bytes_written=0`)；超限 `0x20` (`241,665 B`) 回 `SRC=0x03 NACK 0x14` (`bytes_written=0`)；`0x1D(1)` 静默 `1.5024s` 恢复原 App (`boot_id=0x8FAE0198`, `Bit31=0`) | 错板 RX `55aa030106060304050303000605030780`；超限 RX `55aa0301060603040703030014070385ab`；恢复 App RX `...9801ae8f9a3d627b...` |
| **`B4_TH`** | **PASS** | 进 TH Boot (`boot_id_pre_reset=0x8B71FC52`)；合法 `0x20`+Chunk0 后 `0x23` (`ota_state=2, cached_chunk0=512, written=0`)；活跃 L3 租约期内（全部 `<33ms << 5000ms`）：① `0x24` ➔ **`SRC=0x03 NACK 0x04`** (`2.34ms`)；② 4B `0x23` ➔ `SRC=0x03 NACK 0x06` (`4.89ms`)；③ TH `0x01/0x03/0x14` 透明透传回 `SRC=0x03` (`17.28ms`, `0x14` 回 `NACK 0x04`)；④ MC `0x01/0x03/0x14` 本地零阻塞 (`30.09ms`, `duty=0%`)；⑤ MC `0x10(0,0)` 让路回 **`SRC=0x02 NACK 0x05`** (`32.76ms`)；⑥ `0x1D(1)` 后 `0.1580s` 驻留 TH Boot (`boot_id=0x69A97603` 已刷新, `ota_state=0, written=0`) | `0x24` TX `55aa010305240304100300003be1` ➔ RX `55aa030106060304100303000410033d5c`；`0x10` TX `55aa010205100400180304000000000007b4` ➔ RX `55aa02010606040018030300051803ac8a` |
| **`B2_TH`** | **PASS** | 驻留 TH Boot 直接刷写 `151` 块 (`76,864 B`, `0` 重传)；`0x23` (`512` ➔ `76,352`)；`0x22` 后 `0.155s` 新 TH App 上线 (`0x7B623D9A`, `boot_id=0xF70B7161`, `Bit31=0`)；`0x14` 测得 `duty=0%` | 最后 `0x21` RX `55aa030106000304b403040000100000ea89`；新 App `0x02` `55aa030106020304b70310000200020061710bf79a3d627b0700000034a2` |
| **`IMMEDIATE_TH_TO_MC`** | **PASS** | 距 `B2_TH` 最后一帧 `DST=0x03` 仅 **`0.0001s`（`<1.0s`）** 直发 `DST=0x02 0x1D(2)` ➔ 立即收到 **`SRC=0x02 CMD_ACK (0x00)`**（`2.6ms` 往返，零 `NACK 0x05`）；**`0.6984s`（`<2.0s`）** 确认进入 MC Boot (`0x4FC171EA`, `Bit31=1`) | `12:53:07.290` TX `55aa0102151d0400b903040002011400027c` ➔ `07.293` RX `55aa020106000400b9030400101f00006c13` |
| **`B3_MC`** | **PASS** | 错板 `0x20` (`fw_th_v2_0.bin`, `board_id=0x42300001`) 回 `SRC=0x02 NACK 0x06` (`written=0`)；超限 `0x20` (`917,505 B`) 回 `SRC=0x02 NACK 0x14` (`written=0`)；`0x1D(1)` 静默等待 `3.3042s`（跨过 `~0.64s init + 2.0s` 窗）后 `2.1622s` 恢复 `0x7B623D9A` MC App (`boot_id=0x5BFE57B1`, `Bit31=0`) | 错板 RX `55aa020106060400bf03030006bf035e8b`；超限 RX `55aa020106060400c103030014c103e23b`；恢复 App RX `...b157fe5b9a3d627b...` |
| **`B4_MC`** | **PASS (Waived)** | 进 MC Boot (`boot_id_pre_reset=0xC1E6CD05`)；合法 `0x20`+Chunk0 后 `0x23` (`ota_state=2, cached=512, written=512`)；`0x24` 回 `SRC=0x02 NACK 0x04`；4B `0x23` 回 `SRC=0x02 NACK 0x06`；`0x1D(1)` 安全驻留 MC Boot (`Bit31=1, ota_state=0, written=0`)；`boot_id=0xC1E6CD05` 未刷新按 **`HIL-FINDING-02`** 已批准豁免入账（`waived: true`） | `0x24` RX `55aa020106060400d303030004d303084a`；复位驻留 `0x02` `...05cde6c1ea71c14f350408c0...` |
| **`B2_MC`** | **PASS** | 驻留 MC Boot 全量刷写 `751` 块 (`384,112 B`, `0` 重传)；`0x23` (`512` ➔ `384,112`)；`0x22` 后 `2.852s` 新 MC App 上线 (`0x7B623D9A`, `boot_id=0x8F1F2C60`, `Bit31=0`) | `0x23` pre-finish: `written=384112`；新 App `0x02`: `55aa020106020400cf06100002000200602c1f8f9a3d627b030000008d1b` |
| **`POST_RECOVERY`** | **PASS** | 静默等待 **`5.5064s`（`>=5.2s`）** 释放 L3 租约；`DST=0x02 0x10(0,0)` 收到 **`SRC=0x02 CMD=0x15`** (`target=0, duty=0%`)；被动监听 **`361.02ms`** 收到 `0` 帧、`spurious_nack_count=0`；最终双板 `0x01/0x14/0x16` 均正常（MC `0x16` 回位置 IDLE；TH 不支持 `0x16` 透传回 `SRC=0x03 NACK 0x04`） | `0x10` TX `55aa010205100400d40604000000000046d7` ➔ RX `55aa020106150400d4061000ff7f0000fe0f01002320000000000000dc54`；TH `0x16` RX `55aa030106060304da06030004da065d33` |

---

## 3. 节点身份与 `boot_id` 跃迁表

| 节点 | 阶段 | 模式 (`Bit31`) | `fw` | `commit` | `boot_id` | `capability_flags` |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **MC (`0x02`)** | 首轮升级前原始现场 (`Run #1 B1`) | `App (0)` | `2.0` | `0xB865222C` | `0x02789779` | `0x00000003` |
| **MC (`0x02`)** | 首轮 `B0_MC_ROLLOUT` 升级后 (`Run #1`) | `App (0)` | `2.0` | `0x7B623D9A` | `0x05139CA3` | `0x00000003` |
| **MC (`0x02`)** | 归档全闭环 `B1` 基线 | `App (0)` | `2.0` | `0x7B623D9A` | `0x29199E72` | `0x00000003` |
| **MC (`0x02`)** | `B0_MC_ROLLOUT` Boot / 新 App | `Boot (1)` ➔ `App (0)` | `1.0` ➔ `2.0` | `0x4FC171EA` ➔ `0x7B623D9A` | `0xC1E6CD05` ➔ `0x11ED5521` | `0xC0080435` ➔ `0x00000003` |
| **MC (`0x02`)** | `IMMEDIATE_TH_TO_MC` / `B3_MC` App 恢复 | `Boot (1)` ➔ `App (0)` | `1.0` ➔ `2.0` | `0x4FC171EA` ➔ `0x7B623D9A` | `0xC1E6CD05` ➔ `0x5BFE57B1` | `0xC0080435` ➔ `0x00000003` |
| **MC (`0x02`)** | `B4_MC` 进 Boot / 软复位驻留 (`HIL-FINDING-02`) | `Boot (1)` ➔ `Boot (1)` | `1.0` | `0x4FC171EA` | `0xC1E6CD05` ➔ `0xC1E6CD05` *(已豁免)* | `0xC0080435` |
| **MC (`0x02`)** | `B2_MC` 终极重刷及 `POST_RECOVERY` | `App (0)` | `2.0` | `0x7B623D9A` | `0x8F1F2C60` | `0x00000003` |
| **TH (`0x03`)** | 前序升级前现场 (`Run #1 / #2 B1`) | `App (0)` | `2.0` | `0xB865222C` | `0xC7076DA8` / `0x897C97FF` | `0x00000007` |
| **TH (`0x03`)** | 归档全闭环 `B1` 基线 | `App (0)` | `2.0` | `0x7B623D9A` | `0x6532C5B6` | `0x00000007` |
| **TH (`0x03`)** | `B3_TH` Boot / 软复位回 App | `Boot (1)` ➔ `App (0)` | `1.0` ➔ `2.0` | `0x769FCCBE` ➔ `0x7B623D9A` | `0x4F0708F0` ➔ `0x8FAE0198` | `0xE0080423` ➔ `0x00000007` |
| **TH (`0x03`)** | `B4_TH` Boot 进 / 软复位驻留 Boot | `Boot (1)` ➔ `Boot (1)` | `1.0` | `0x769FCCBE` | `0x8B71FC52` ➔ `0x69A97603` *(已刷新)* | `0xE0080423` |
| **TH (`0x03`)** | `B2_TH` 升级及 `POST_RECOVERY` | `App (0)` | `2.0` | `0x7B623D9A` | `0xF70B7161` | `0x00000007` |

---

## 4. 线缆字节重组校验（对齐 `SLICE-05.yaml`）

对 `hil_raw_hex.log` 中 `[B2_TH]` 与 `[B2_MC]` 的 `0x21` 发送帧按小端 `offset` 字节拼接重组核验结果：
- **`[B2_TH]` 重组**：`151` 个唯一分片 ➔ `76,864 B`、`CRC32 = 0x6E82DD49`、`SHA256 = ac48de349be04c2a2a1f8de15cc965b8eca04517f66de625cedb8216ed52aeb7`，包含 `0x7B623D9A` 小端字节序 `9a3d627b`（`>= 1` 次）。
- **`[B2_MC]` 重组**：`751` 个唯一分片 ➔ `384,112 B`、`CRC32 = 0x8DC0DC33`、`SHA256 = 4ec90793f6feb49c171668203da60dc0f6548d7bf5e3c328f866b84eed0b8ad8`，包含 `0x7B623D9A` 小端字节序 `9a3d627b`（`>= 1` 次）。

---

## 5. 已批准豁免与未实测硬件边界声明

1. **`HIL-FINDING-02` 已批准豁免入账**：`B4_MC` 实测复现 MC Bootloader (`0x4FC171EA`) 跨软复位返回相同 `boot_id=0xC1E6CD05`，按实施方案 `v1.5` 及 `project-control/slices/ledger.md` 已批准非阻断技术债处理（全程未动用 SWD 探针，未修改 `boot/bootloadermc`）。芯片内部 `CRM->ctrlsts` 寄存器位状态与中断发生时的 MCU 内部堆栈寄存器未通过硬件探针直接读取，诚实标为 **`[UNVERIFIED]`**。
2. **未接物理外设诚实边界（`DEC-REM-1=A` 条件准出范围）**：
   - **`[UNVERIFIED / PENDING]` `B5_UDISK_MANUAL_PLUG_HW_G1`**：当前 C308L `/dev/ttyS1` 台架无物理 FAT32 U 盘插拔与人工供电开关条件，MC U 盘升级（`0:/fw_mc.bin -> FW_MC.CUR / .err`）、防重刷及 U 盘/串口物理并发互斥未在本轮真机实测。
   - **`[UNVERIFIED / PENDING]` `EXTERNAL_DEBUG_UART_USART1_USART3`**：未授权访问且未连接独立 MC USART1 (`[MC-DBG]`) 与 TH USART3 (`[TH-DBG]`) 调试串口，芯片串口文本日志未采集。
   - **`[UNVERIFIED / PENDING]` `PRINTER_SOC_REST_ON_C308L`**：C308L 上未运行 `printer-soc` 守护进程集群（REST / D-Bus / `forward_ota` / DDS），C308L 板端 REST 业务入口未实测。
