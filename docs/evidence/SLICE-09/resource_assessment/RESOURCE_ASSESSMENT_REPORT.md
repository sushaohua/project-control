# SLICE-09 (`S09-RES`) 跨端资源评估报告（阶段一：`r18b` 实板基线采样 + 四端 MCU/Bootloader 静态容量完整核算）

- **切片与任务标识**：`SLICE-09` / `S09-RES`（第 5 项交付：资源评估）
- **评估角色与写边界**：`INTEGRATOR`（全业务仓只读 `max_files = 0`、`max_protected_lines = 0`；唯一归档目录 `project-control/docs/evidence/SLICE-09/resource_assessment/`）
- **方案依据**：[helix_p0_experience_implementationplan_20261121_190357.md](../../planning/helix_p0_experience_implementationplan_20261121_190357.md)（`v1.5` 已批准版 `§1.8`、`§2.6`）
- **当前报告阶段**：**阶段一（刷入新候选前的 `SLICE-08 r18b` 实板空闲基线与存储核算 + 四端 MCU/Bootloader 基线对比候选静态容量全量核算）**；需在 `r06` 容器构建及 `Human Gate #2A`（阶段 H1/H2）实板部署后补齐的候选 AP 空闲、双板 OTA 动态采样与新 rootfs 包体积均已在对应列明确标注 `待验证`，绝不伪造待测项。

---

## 1. 评估对象版本身份、工具链与制品锚点总表

| 端点 / 仓库 | `SLICE-08 r18b` 基线锁定 Commit (40-SHA) | `SLICE-09` 候选锁定 Commit (40-SHA) | 构建配置 / 编译选项 | 正式归档制品路径与 SHA-256（前 16 位，全长见 JSON） |
| --- | --- | --- | --- | --- |
| **AP (`printer-soc`)** | `6f28023f7f1b774d181fc4ba59d3c378f260bfc1` | `547162dc1525c7476c7713245feb03aca0a8f150` | `c308l-production`, `armv7l-hf-glibc2.33`, `--hil-ota-integrity-only` | 基线 `SLICE-08/run_20261121_155747_r18b/docker_qa/artifacts/printer-soc-rootfs.tar.gz` (`18,788,600 B`, `76e9348b88fea16a...`)；候选待 `r06` Docker QA 产出 |
| **MC App (`mcu-p3`)** | `a64bffbf1a0c5cbc2fe96b51632098042697878b` | `112842cb42146e466f7001ede30096bd0125c385` | `arm-none-eabi-gcc 9.2.1`, `CMake Debug`, `AT32F435xG_FLASH.ld` | 基线 `SLICE-08/fw_mc_r18.bin` (`384,668 B`, `1a259d259d478ef6...`)；候选 `SLICE-09/candidate_mcu_artifacts/fw_mc.bin` (`384,668 B`, `320966b15cf2fb41...`) |
| **TH App (`mcu-p3`)** | `a64bffbf1a0c5cbc2fe96b51632098042697878b` | `112842cb42146e466f7001ede30096bd0125c385` | `arm-none-eabi-gcc 9.2.1`, `-O2 -fdata-sections -ffunction-sections --gc-sections`, `AT32F423xC_FLASH.ld` | 基线 `SLICE-08/fw_th_r18.bin` (`76,992 B`, `f839e1d56f26ed47...`)；候选 `SLICE-09/candidate_mcu_artifacts/fw_th.bin` (`76,968 B`, `904ceee06e31729b...`) |
| **MC Boot (`boot/bootloadermc`)** | `3e01c00ce4dfb5e9e749e79c3cfbc076e3680bf4` | `157b5317bc8fd90e93f684f949d37e98428ea193` | `arm-none-eabi-gcc 9.2.1`, `-Os -g3 -fdata-sections -ffunction-sections --gc-sections`, `at32f435_bootloader.ld` | 基线 `SLICE-09/candidate_mcu_artifacts/bootloader_3e01c00_rollback.bin` (`37,600 B`, `1082c318fee4aecb...`)；候选 `bootloader.bin` (`37,628 B`, `0e9ace3fc6dc8ffc...`) |
| **TH Boot (`boot/bootloaderth`)** | `1a0351363cf7b9cbc0aa6919b4afc6be61561152` | `1a0351363cf7b9cbc0aa6919b4afc6be61561152`（同源零改动共用） | `arm-none-eabi-gcc 9.2.1`, `-Os -DDEBUG_LOG_ENABLE=1 --gc-sections`, `AT32A423xC_FLASH.ld` | 锁定源码隔离构建 `bootloaderth.bin` (`9,360 B`, `2d28f40544f8e38a...`)，基线与候选同源共用一份静态证据 |

---

## 2. AP 运行态 CPU 与内存评估（`root@192.168.1.101`）

### 2.1 采样口径、窗口对齐与现场实况记录
1. **硬件与内核基准**：`C308L-AW419`（`Linux 5.15.137 armv7l`），`CPU_COUNT = 2`，`SC_CLK_TCK = 100`，物理总内存 `MemTotal = 1,784,292 KiB`。
2. **CPU 与内存计算口径（严格执行 `§2.6`）**：
   - 取 `/proc/stat` 首行前 8 列 `total = user + nice + system + idle + iowait + irq + softirq + steal`（**不重复累加第 9/10 列 `guest`/`guest_nice`**）；
   - **整机 CPU%** = `(Δtotal - Δidle - Δiowait) / Δtotal × 100%`（占双核总 tick 容量的 `0%~100%` 归一化占比）；
   - **单服务 CPU%** = `Δ(utime + stime) / Δtotal × 100%`（同时列出 60s 全窗口均值与 60 个 `1s` 区间单秒峰值）；
   - **内存**：各服务报采样窗口内 `/proc/<pid>/status` 的 `VmRSS` 观测峰值（`KiB`），整机报 `/proc/meminfo` 的 `MemAvailable` 观测最低值（`KiB`）。
3. **`r18b` 空闲基线采样窗口与进程零换代核验**（原始证据：[ap_r18b_idle_60s_raw.json](ap_r18b_idle_60s_raw.json)、[ap_r18b_idle_60s_summary.json](ap_r18b_idle_60s_summary.json)）：
   - **宿主机墙钟时段**：`2026-11-23T13:09:09.122+08:00` ➔ `2026-11-23T13:10:10.257+08:00`；
   - **板端 `/proc/uptime` 窗口**：`6485.03 s` ➔ `6545.03 s`（跨度 **`60.0 s`**，共 **`61`** 个样本点、**`60`** 个 `1s` 差分窗口）；
   - **板上版本与开关配置**：`/etc/printer-soc/version.json` `git_sha = "6f28023f"`，`mode = "production"`，`enable_panel = true`，`enable_gateway = false`，`dds_domain = 198`（`SHM`），`uart = "/dev/ttyS1" @ 921600`，`helix-screen` `log_level = "info"`，`rotate = 270`；
   - **采样前后 `printer-soc status` 进程代次核验（100% 零换代）**：
     - `controller` (`/usr/bin/python3.9` `services.py`): `PID=841`, `start_ticks=433`, `alive: true -> true`, `no_pid_churn=true`
     - `dbus` (`/usr/bin/dbus-daemon`): `PID=842`, `start_ticks=455`, `alive: true -> true`, `no_pid_churn=true`
     - `forward` (`/usr/bin/forward_service_daemon`): `PID=843`, `start_ticks=462`, `alive: true -> true`, `no_pid_churn=true`
     - `device_manager` (`/usr/bin/device_manager_daemon`): `PID=858`, `start_ticks=543`, `alive: true -> true`, `no_pid_churn=true`
     - `panel` (`/usr/share/printer-soc/helixscreen/bin/helix-screen`): `PID=868`, `start_ticks=557`, `alive: true -> true`, `no_pid_churn=true`
   - **断电重启后板端现场工况说明（影响可比性备注）**：台架在本次采样前约 `1.8h` 经历过整机断电上电（`uptime=6485s`）：① 持久化 `settings.json` 因掉电前未 `fsync` 处于 `"language": "zh"`（`panel` 当前已加载 29 个 CJK 字体，故 `panel` `VmRSS=30,264 KiB` 已包含 CJK 字库驻留开销）；② 因 `r18b` 存量缺陷 `BOOT-MC-STAY-01`，上电轮询使 `MC` 驻留于 Bootloader（`boot_id=3521563910`, `0x4FC171EA`, `cap=0xC0080435` `[Boot]`），`TH` 显示 `OFFLINE`（`/dev/ttyS1` `tx=11785, rx=5821`，`Forward` 对 `MC` 正常收发、对 `TH` 等待 `200ms` 超时）。阶段 H1 采集候选空闲窗口时须同步记录 `MC/TH` 处于 `App ONLINE` 态的工况差异。

### 2.2 工况 A：AP 生产空闲窗口（`60s @ 1Hz`）对比表

| 观测对象 | 指标项 | 单位 | `SLICE-08 r18b` 基线实测值 (`6f28023f`) | `SLICE-09` 候选实测值 (`547162dc`) | 可比差值 (`候选 - 基线`) | 物理总量 / 容量余量 | 取数来源与状态 |
| --- | --- | :---: | :---: | :---: | :---: | --- | --- |
| **AP 整机 (`2 Cores`)** | 系统 CPU 均值 / 1s 峰值 | `%` | **`24.572%` / `30.964%`**（最低 `17.436%`） | `待验证 (Pending Human Gate #2A H1)` | `待验证` | 整机上限 `100%`（`r18b` 均值余量 `75.428%`，峰值余量 `69.036%`） | `/proc/stat` (`ap_r18b_idle_60s_raw.json`) |
| **AP 整机内存** | `MemAvailable` 观测最低值 | `KiB` | **`1,653,820`**（最高 `1,654,072`） | `待验证 (Pending Human Gate #2A H1)` | `待验证` | `MemTotal = 1,784,292 KiB`（可用占比 **`92.69%`**，无固定硬阈值） | `/proc/meminfo` (`ap_r18b_idle_60s_raw.json`) |
| **`panel` (`helix-screen`)** | 服务 CPU 均值 / 1s 峰值 | `%` | **`4.469%` / `10.938%`** | `待验证 (Pending Human Gate #2A H1)` | `待验证` | 无独立 cgroup 配额（受整机 `100%` 约束） | `/proc/868/stat` |
| **`panel` (`helix-screen`)** | `VmRSS` 观测峰值（附 `VmHWM`） | `KiB` | **`30,264`**（`VmHWM = 30,284`） | `待验证 (Pending Human Gate #2A H1)` | `待验证` | 占 `MemTotal` `1.70%` | `/proc/868/status` |
| **`forward` (`forward_service_daemon`)** | 服务 CPU 均值 / 1s 峰值 | `%` | **`5.002%` / `6.186%`** | `待验证 (Pending Human Gate #2A H1)` | `待验证` | 无独立 cgroup 配额 | `/proc/843/stat` |
| **`forward` (`forward_service_daemon`)** | `VmRSS` 观测峰值 | `KiB` | **`8,580`** | `待验证 (Pending Human Gate #2A H1)` | `待验证` | 占 `MemTotal` `0.48%` | `/proc/843/status` |
| **`device_manager` (`device_manager_daemon`)** | 服务 CPU 均值 / 1s 峰值 | `%` | **`2.535%` / `3.158%`** | `待验证 (Pending Human Gate #2A H1)` | `待验证` | 无独立 cgroup 配额 | `/proc/858/stat` |
| **`device_manager` (`device_manager_daemon`)** | `VmRSS` 观测峰值 | `KiB` | **`8,700`** | `待验证 (Pending Human Gate #2A H1)` | `待验证` | 占 `MemTotal` `0.49%` | `/proc/858/status` |
| **`dbus` (`dbus-daemon`)** | 服务 CPU 均值 / 1s 峰值 | `%` | **`3.154%` / `4.188%`** | `待验证 (Pending Human Gate #2A H1)` | `待验证` | 无独立 cgroup 配额 | `/proc/842/stat` |
| **`dbus` (`dbus-daemon`)** | `VmRSS` 观测峰值 | `KiB` | **`1,480`** | `待验证 (Pending Human Gate #2A H1)` | `待验证` | 占 `MemTotal` `0.08%` | `/proc/842/status` |
| **`controller` (`services.py`)** | 服务 CPU 均值 / 1s 峰值 | `%` | **`0.739%` / `1.562%`** | `待验证 (Pending Human Gate #2A H1)` | `待验证` | 无独立 cgroup 配额 | `/proc/841/stat` |
| **`controller` (`services.py`)** | `VmRSS` 观测峰值 | `KiB` | **`7,100`** | `待验证 (Pending Human Gate #2A H1)` | `待验证` | 占 `MemTotal` `0.40%` | `/proc/841/status` |
| **5 个生产进程合计** | 服务 CPU 均值合计 / `VmRSS` 峰值合计 | `%` / `KiB` | **`15.899%` / `56,124 KiB`** | `待验证 (Pending Human Gate #2A H1)` | `待验证` | 5 进程 RSS 合计仅占整机 `MemTotal` 的 **`3.15%`** | 独立进程汇总（零换代） |

### 2.3 工况 B：双板串口 OTA 活跃事务窗口（`@ 1Hz`）对比表

| 观测对象 | 指标项 | 单位 | `SLICE-08 r18b` 基线值 | `SLICE-09` 候选实测值（复用 H2 触屏双板 OTA 同一 `task_id`） | 可比差值 | 说明与对结论的影响 |
| --- | --- | :---: | :---: | :---: | :---: | --- |
| **AP 整机及 5 个生产服务** | 双板（先 TH 后 MC）串口 OTA 全窗口系统 CPU%、各服务 CPU%（均值/1s 峰值）、各服务 `VmRSS` 峰值、整机 `MemAvailable` 最低值 | `%` / `KiB` | **`未测（无同工况历史基线采样）`** | `待验证 (Pending Human Gate #2A H2)` | `不可比（无历史基线）` | 核查 `SLICE-08/hil_r18b/04b_ac03_ota_th_mc_full.log` 确认历史验收未采集 `1Hz` `/proc` CPU/RAM 序列；按 `§1.8`/`§2.6` 禁止补刷或伪造基线，将在阶段 H2 实测候选升级绝对占用与 `MemAvailable` 安全余量，不输出跨版本差值。 |

---

## 3. AP 存储分区与发布制品体积评估

### 3.1 实板挂载分区容量与共用关系核算（`df -k` + `/proc/self/mountinfo`）

| 查询路径 | 实际挂载点与底层设备 (`mountinfo`) | 分区总容量 (`KiB`) | `SLICE-08 r18b` 已用 (`KiB`) | `SLICE-08 r18b` 可用余量 (`KiB` / 占比) | `SLICE-09` 候选部署后已用 / 可用 (`KiB`) | 挂载共用关系与容量说明 |
| --- | --- | :---: | :---: | :---: | :---: | --- |
| **`/`** | `/` ➔ `ubi0_0` (`ubifs`, `ubi=0,vol=0`) | `110,440` | **`75,508`** (`68%`) | **`34,932`** (`31.63%`) | `待验证 (Pending Human Gate #2A H1)` | 存放只读系统文件、`/usr/lib/printer-soc` 与 `/usr/share/printer-soc/helixscreen`（含 29 个 CJK `.bin` 字库与 `zh.xml`）。 |
| **`/data`** | `/data` ➔ `/dev/ubi1_0` (`ubifs`, `ubi=1,vol=0`) | `61,928` | **`7,588`** (`13%`) | **`51,144`** (`82.59%`) | `待验证 (Pending Human Gate #2A H1)` | 存放 `/data/boot_backup.img` 及 `/data/printer-soc/helix/config/settings.json` 等持久化数据。 |
| **`/run/printer-soc/firmware`** | `/run` ➔ `tmpfs` (`mount_id=21`, 内存文件系统) | `892,144` | **`1,528`** (`0%`，固件目录为空) | **`890,616`** (`99.83%`) | `待验证 (Pending Human Gate #2A H1/H2)` | **挂载共用**：与 `/run/printer-soc/` 下的 `state.json`、`*.log` 共用同一 `/run` `tmpfs` 挂载（消耗 RAM `Shmem`，不占闪存）。即便同时置入候选 `fw_mc.bin + fw_th.bin` 共 `461,636 B` (`450.82 KiB`)，仅占 `/run` 余量的 `0.05%`。 |

### 3.2 AP 系统发布包与镜像制品字节数对比（单列压缩包/镜像大小）

| 制品名称 | 单位 | `SLICE-08 r18b` 正式归档值 (`6f28023f`) | `SLICE-09` 候选归档值 (`547162dc`) | 可比差值 (`候选 - 基线`) | 上限 / 约束 | 原始证据来源 |
| --- | :---: | :---: | :---: | :---: | --- | --- |
| **`printer-soc-rootfs.tar.gz`**（应用部署压缩包） | `Bytes` (`KiB`) | **`18,788,600`** (`18,348.24 KiB`) | `待验证 (Pending r06 Docker QA)` | `待验证` | 解压目标 `/`（分区总容 `110,440 KiB`） | `static_and_storage_summary.json` (`sha256=76e9348b...`) |
| **`rootfs.ubi`**（UBI 根文件系统镜像） | `Bytes` (`KiB`) | **`68,681,728`** (`67,072.00 KiB`) | `待验证 (Pending r06 Docker QA)` | `待验证` | `ubi0_0` 卷容量上限内 | `static_and_storage_summary.json` (`sha256=61dc843e...`) |
| **`aml_upgrade_package.img`**（整机线刷包） | `Bytes` (`KiB`) | **`89,827,840`** (`87,722.50 KiB`) | `待验证 (Pending r06 Docker QA)` | `待验证` | 产线烧录镜像（非板载常驻） | `static_and_storage_summary.json` (`sha256=936434bc...`) |

---

## 4. 四端 MCU & Bootloader 静态容量完整核算（`r18b` 基线 vs `SLICE-09` 候选）

> 全部原始 `arm-none-eabi-size -A/-B`、`arm-none-eabi-objdump -h`、`arm-none-eabi-readelf -lW` 与 `.map` 摘录见 [mcu_elf_and_map_extracts.log](mcu_elf_and_map_extracts.log)，机器可读结构化核验结果见 [static_and_storage_summary.json](static_and_storage_summary.json)。

### 4.1 Flash 实际占用跨度、ATSG 封装包体积与分区余量总表
- **核算规则（`§2.6`）**：Flash 占用跨度 = `最高有效 Flash LMA 末址 (含 .data 装载映像及段间对齐间隙) - 分区首址`；余量 = `链接脚本 FLASH LENGTH - Flash 占用跨度`。App 额外通过 `sign_mcu_firmware.validate_atsg_base(..., check_crc=True)` 校验 128B ATSG 尾块与净载一致性。

| 固件端点 | 分区首址与链接脚本 | 指标项 | 单位 | `SLICE-08 r18b` 基线 | `SLICE-09` 候选 | 可比差值 (`候选 - 基线`) | 分区上限 (`Bytes` / `KiB`) | 候选可用余量 (`Bytes` / 占比) | 超限判定与对账说明 |
| --- | --- | --- | :---: | :---: | :---: | :---: | :---: | :---: | --- |
| **`MC App`** (`AT32F435`) | `0x08020000` (`AT32F435xG_FLASH.ld`) | Flash 占用跨度 (`0x08020000..0x0807de1c`) | `Bytes` | **`384,540`** | **`384,540`** | **`0 B`** | `917,504` (`896 KiB`) | **`532,964 B`** (`58.09%`) | **未超限**；等于 ATSG 净载长度（含 `.isr_vector` `524B` + `52B` 间隙 + `.text` `195,172B` + `4B` 间隙 + `RAMCODE1` `4,068B` + `4B` 间隙 + `.rodata` `183,760B` + `.ARM`/init/fini `16B` + `.data` LMA `940B`）。 |
| **`MC App`** (`AT32F435`) | ATSG 升级包 (`0x43500001`) | `fw_mc.bin` 总字节数（含 `128B` ATSG 尾块） | `Bytes` | **`384,668`** | **`384,668`** | **`0 B`** | 净载上限 `917,504` | — | `validate_atsg_base(check_crc=True)` 通过；本轮 MC App 源码零改动，仅内嵌短提交由 `0xA64BFFBF` 变为 `0x112842CB`。 |
| **`TH App`** (`AT32F423`) | `0x08004000` (`AT32F423xC_FLASH.ld`) | Flash 占用跨度（基线 `..0x08016c40` / 候选 `..0x08016c28`） | `Bytes` | **`76,864`** | **`76,840`** | **`-24 B`** | `241,664` (`236 KiB`) | **`164,824 B`** (`68.20%`) | **未超限**；`TH-ESTOP-01` 修复精简 `handle_th_motion_stop()` 使 `.text` 由 `70,340B` (`0x112c4`) 降至 `70,316B` (`0x112ac`)，净减 `24 B`。 |
| **`TH App`** (`AT32F423`) | ATSG 升级包 (`0x42300001`) | `fw_th.bin` 总字节数（含 `128B` ATSG 尾块） | `Bytes` | **`76,992`** | **`76,968`** | **`-24 B`** | 净载上限 `241,664` | — | `validate_atsg_base(check_crc=True)` 通过；净载严格等于 ELF Flash LMA 跨度（`76,864 B` / `76,840 B`）。 |
| **`MC Bootloader`** (`AT32F435`) | `0x08000000` (`at32f435_bootloader.ld`) | Flash 占用跨度 / `bootloader.bin` 大小（基线 `..0x080092e0` / 候选 `..0x080092fc`） | `Bytes` | **`37,600`** | **`37,628`** | **`+28 B`** | `131,072` (`128 KiB`) | **`93,444 B`** (`71.29%`) | **未超限**；`BOOT-MC-STAY-01` 移除 `handle_cmd_get_version()` 中误置的 `s_ota.stay_in_boot = 1U;` 并提炼 `boot_uart_ota_should_jump_after_window()`（`S09-06`），`.text` 净增 `28 B`（`33,824B` ➔ `33,852B`）。 |
| **`TH Bootloader`** (`AT32A423`) | `0x08000000` (`AT32A423xC_FLASH.ld`) | Flash 占用跨度 / `bootloaderth.bin` 大小 (`0x08000000..0x08002490`) | `Bytes` | **`9,360`** | **`9,360`** | **`0 B`（同源共用）** | `16,384` (`16 KiB`) | **`7,024 B`** (`42.87%`) | **未超限**；基线与候选锁定同一提交 `1a035136`，共用同一静态构建证据。 |

- **隔离重编与正式归档包差异核对记录**：在 `.tmp_baseline_build/`（提取后已彻底删除）基于锁定 40 位 SHA 重编的 6 份基线/候选二进制与已归档正式制品逐字节比对，原始字节差异数分别为 `mc_app_r18b=5B`、`mc_app_s09=4B`、`th_app_r18b=9B`、`th_app_s09=10B`、`mc_boot_r18b=6B`、`mc_boot_s09=0B`（`157b5317` 当轮洁净重编直接归档），经 `normalize_stamps()` 归一化 `version_autogen.h` 开发流水号与 `__DATE__/__TIME__` 构建时间字符串后，**全部 100% 逐字节机器码与常量表完全一致（`normalized_machine_code_identical = true`）**。

### 4.2 各 RAM Bank 静态区、编译期堆栈预留与 `BOOT_IPC` 独立核算表
- **核算规则（`§2.6`）**：按链接脚本定义的独立 `MEMORY` 区域（`RAM`、`BOOT_IPC`、`RAM_STACK`）按 VMA 分别核算；静态全局占用含 `.data`、`.bss`、`.noinit` 及段间对齐间隙；编译期链接预留检查段 `._user_heap_stack`（含 `_Min_Heap_Size`、`_Min_Stack_Size` 及 8B 对齐填充）独立列出，不与静态区重复双扣。

| 固件端点 | RAM Bank 名称与地址范围 | Bank 总容量 (`Bytes`) | 静态全局区占用 (`.data+.bss+.noinit` 含对齐，`r18b` ➔ `SLICE-09`) | 可比差值 | 编译期预留检查段 `._user_heap_stack` 明细（不重复双扣） | 扣除静态区与最小预留后链接余量 (`Bytes` / 占比) | 物理总可用堆栈池 (`_estack - 静态区末址`) |
| --- | --- | :---: | :---: | :---: | --- | :---: | :---: |
| **`MC App`** | `RAM` (`0x20000000..0x2005FFF0`) | `393,200` | **`43,036 B` ➔ `43,036 B`**（`.data=940B` + `4B` 对齐 + `.bss=42,084B` + `.noinit=8B`） | **`0 B`** | **`1,540 B`**（`4B` 对齐 + `_Min_Heap_Size=512B` + `_Min_Stack_Size=1,024B`） | **`348,624 B`** (`88.66%`) | **`350,164 B`**（`0x2000a81c..0x2005fff0`） |
| **`MC App`** | `BOOT_IPC` (`0x2005FFF0..0x20060000`) | `16` | **`.boot_ipc`: `4 B` ➔ `4 B`** | **`0 B`** | 无（专用于跨复位 `UPG2` 魔数保留） | **`12 B`** (`75.00%`) | N/A |
| **`TH App`** | `RAM` (`0x20000000..0x20008000`) | `32,768` | **`16,668 B` ➔ `16,668 B`**（`.data=844B` + `.bss=15,816B` + `.noinit=8B`） | **`0 B`** | 无（堆栈独立置于 `RAM_STACK`） | **`16,100 B`** (`49.13%`) | 见下方 `RAM_STACK` |
| **`TH App`** | `BOOT_IPC` (`0x20008000..0x20008010`) | `16` | **`.boot_ipc`: `4 B` ➔ `4 B`** | **`0 B`** | 无（专用于跨复位 Boot IPC 保留） | **`12 B`** (`75.00%`) | N/A |
| **`TH App`** | `RAM_STACK` (`0x20008010..0x2000C000`) | `16,368` | **`0 B` ➔ `0 B`** | **`0 B`** | **`1,536 B`**（`_Min_Heap_Size=512B` + `_Min_Stack_Size=1,024B`） | **`14,832 B`** (`90.62%`) | **`16,368 B`**（`0x20008010..0x2000c000` 全区专供堆栈） |
| **`MC Bootloader`** | `RAM` (`0x20000000..0x20060000`) | `393,216` | **`7,160 B` ➔ `7,160 B`**（`.data=176B` + `.bss=6,984B`） | **`0 B`** | **`12,288 B`**（`_Min_Heap_Size=4,096B` + `_Min_Stack_Size=8,192B`） | **`373,768 B`** (`95.05%`) | **`386,056 B`**（`0x20001bf8..0x20060000`） |
| **`TH Bootloader`** | `RAM` (`0x20000000..0x2000C000`) | `49,152` | **`2,300 B` ➔ `2,300 B`**（`.data=4B` + `.bss=2,296B`） | **`0 B`（共用）** | **`1,540 B`**（`4B` 对齐 + `_Min_Heap_Size=512B` + `_Min_Stack_Size=1,024B`） | **`45,312 B`** (`92.19%`) | **`46,852 B`**（`0x200008fc..0x2000c000`） |

### 4.3 MCU 运行时缺测项声明与影响边界（`§1.8` / `§2.6`）

| 评估维度 | 基线状态 | 候选状态 | 缺测原因与对交付结论的影响说明 |
| --- | :---: | :---: | --- |
| **MC / TH 运行时 CPU 利用率** | `未测（无固件埋点）` | `未测（无固件埋点）` | 遵循 `§2.6` 零业务代码篡改约束（`max_files=0`），不向候选固件插入 DWT/SysTick 性能打点以避免改变待测二进制及引入串口/中断观测开销；通信吞吐与延迟留由独立通信性能测试方案专项评估。 |
| **MC / TH 运行时实际栈峰值水位** | `未测（无固件埋点）` | `未测（无固件埋点）` | 固件未启用启动期栈涂色（Stack Painting）与水位读回命令，故无法实测动态最大栈深；但静态核算证实本轮 `TH-ESTOP-01`（`-24B` Flash、`0B` RAM）与 `BOOT-MC-STAY-01` + `S09-06`（`+28B` Flash、`0B` RAM）零新增递归或大局部数组，且四端物理堆栈池（`350.2 KiB` / `16.0 KiB` 独立区 / `377.0 KiB` / `45.8 KiB`）相对各自 `_Min_Stack_Size` 均具备充裕静态安全边界。 |

---

## 5. 阶段一结论摘要与阶段二（`r06` QA & `Human Gate #2A`）待补齐清单

1. **已闭环结论（零超限）**：
   - **四端 MCU / Bootloader 静态评估 100% 完成**：相对 `SLICE-08 r18b`，`SLICE-09` 候选的 `MC App` Flash/RAM 增量为 `0 B` / `0 B`（Flash 余量 `532,964 B` / `58.09%`），`TH App` Flash 减少 `24 B`、RAM 增量 `0 B`（Flash 余量 `164,824 B` / `68.20%`），`MC Bootloader` Flash 增加 `28 B`、RAM 增量 `0 B`（Flash 余量 `93,444 B` / `71.29%`），`TH Bootloader` 同源零变化（Flash 余量 `7,024 B` / `42.87%`），全部 Flash 分区与独立 RAM Bank 均远低于硬上限。
   - **实板 `r18b` 空闲 60s @ 1Hz 与存储基线采集完成**：采样期间 5 个生产守护进程零换代（`no_pid_churn=true`），整机系统 CPU 均值 `24.572%`（1s 峰值 `30.964%`），5 进程 `VmRSS` 峰值合计 `56,124 KiB`（其中 `panel` `30,264 KiB`），整机 `MemAvailable` 最低 `1,653,820 KiB`（占总内存 `92.69%`）；`/` 可用 `34,932 KiB`，`/data` 可用 `51,144 KiB`，`/run/printer-soc/firmware` 共用 `/run` `tmpfs` 可用 `890,616 KiB`。
2. **阶段二待补齐项（严禁提前虚标通过）**：
   - 待 `r06` Docker QA 产出新候选 `printer-soc-rootfs.tar.gz`、`rootfs.ubi`、`aml_upgrade_package.img` 后，补齐 §3.2 候选制品字节数、SHA-256 与差值；
   - 待用户批准 `Human Gate #2A` 部署候选上板后，在阶段 H1 采集候选稳定空闲 `60s @ 1Hz` 样本及 `df -k` 存储余量，在阶段 H2 同一次真实触屏双板 OTA 事务窗口采集 `@ 1Hz` 动态 CPU/RAM 样本并按 `task_id` 与 `forward.log` 对齐更新本报告 §2.2、§2.3 与 §3.1。

---

## 6. 本目录归档证据文件清单

- `RESOURCE_ASSESSMENT_REPORT.md`：本跨端资源评估主报告
- `ap_r18b_idle_60s_raw.json`：实板 `r18b` 空闲 `60s @ 1Hz` 完整 61 个原始样本点、`mountinfo`、`df -k` 与前后 `printer-soc status` 记录
- `ap_r18b_idle_60s_summary.json`：实板 `r18b` 空闲窗口聚合指标与进程零换代核验摘要
- `mcu_elf_and_map_extracts.log`：四端 7 份固件 ELF 的 `arm-none-eabi-size -A/-B`、`objdump -h`、`readelf -lW` 与 `.map` 关键段表原始摘录
- `static_and_storage_summary.json`：四端 Flash LMA 跨度、ATSG 净载核验与 `SLICE-08`/`SLICE-09` 归档制品 SHA-256 对账数据
- `collect_ap_r18b_baseline.py`：实板 AP `1Hz` 资源采样与汇总脚本（已通过 `fast_gate.py`）
- `extract_static_and_storage.py`：MCU/Bootloader 静态 ELF/map 提取与 ATSG 归档对账脚本（已通过 `fast_gate.py`）
