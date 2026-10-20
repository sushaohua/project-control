---
title: MS-01 当前源码、构建配置与现有制品核验
date: 2026-10-20
timezone: 北京时间（UTC+8）
status: source-inventory-prepared
approval_status: Pending independent review
author: AI (Codex)，当前主对话 /root
related_tasks: [MS-01, MS-02, MS-03, MS-12, MS-18]
---

# MS-01 当前工程登记

本次按 2026-10-19 交接继续工程现状核验，读取本地 MC/TH 源码、配置和现有制品；没有修改 MCU 源码、生成 MCU 构建输出、烧录、复位或打开串口。AP 启动候选另作本地主机复现。本文是工程登记交付，尚无独立 ARCH 评审，不能据此把 MS-01 或下游卡标为 Done。

## 1. 准确输入与核查边界

开工时四仓工作区均干净；下列 SHA 来自实际 `git rev-parse HEAD`，不是从交接表照抄。原始元数据、工具版本和 37 个源码/规则/配置文件 SHA256 见 [inventory.json](../evidence/20261020/inventory.json)。证据中的控制仓 status 在开始保存证据后再次采集，包含本次新建证据目录。

| 仓库 | 分支 | 实际 HEAD |
| --- | --- | --- |
| project-control | main | `97b17fb6842d708eccb4a96049c42f415cdbb15a`（本次编辑的基提交） |
| soc-ap | main | `cf2dff40e8b9d7c94b41d01386f287be45afdb4d` |
| mcu-p3 | feat/soc-debug | `14b8057b04030bd659744c874c73ff8f09f29979` |
| test_harness | main | `ad0398e20d3645dbfa37bfd0550ded0828d018b2` |

MC 与 TH 共用 `mcu-p3` 分支和 SHA，上游为 `origin/feat/soc-debug`；本地缓存的 upstream SHA 与 HEAD 相等。远端连接失败，缓存值不能代表服务器现况。

规则原件为 `project-control/.agents/`。另沿 `mcu-p3/AGENTS.md` 和 `.agents/` 已有软链接读取 MCU 约束，只在链接目标范围内读取；未探索其外部兄弟目录。MCU 侧要求 Linux PATH 隔离、实施方案审批后再改代码；本次保持只读。跨仓登记输出在 `project-control/docs/`，未改根目录旧 `.agents/`。

## 2. 工程、配置与依赖

| 对象 | 实际入口与当前配置 | 核验结果及限制 |
| --- | --- | --- |
| MC App | `mcu-p3/motion-controller-mcu/`；Make 包装 CMake；`cmake/at32_workbench/CMakeLists.txt` 定义 `AT32F435VGT7`、`USE_STDPERIPH_DRIVER` | 源清单含 Marlin、DGUS、USB MSC、TH upgrade manager 及 `syscalls.c`；未构建 |
| MC 工具链 | `cmake/gcc-arm-none-eabi.cmake`；Cortex-M4、FPv4-SP-D16、hard float，Debug `-O0 -g3`；nano/newlib，`-u _printf_float` | 使用 PATH 中的 `arm-none-eabi-*`；工具存在不代表链接成功 |
| MC 内存/启动 | `AT32F435xG_FLASH.ld`：Flash `0x08020000` / 896 KiB，RAM `0x20000000` / 384 KiB；`project/src/main.c:121` 设置 VTOR `0x08020000` | 链接脚本与 main 的 App 偏移相同；不是板上寄存器读回 |
| MC 配置/版本 | `project/marlin/configure.h`：`FORWARD_USART_SEL=6`、`FORWARD_USART_BAUDRATE=921600`、`EXTRUDERS=2`；`version.ini` 为 1.9.1 / build 2 | 配置文件及版本工具已登记哈希；没有本地 MC 生成版本头 |
| TH App | `mcu-p3/color-engine-mcu/io_toggle/Makefile`；47 个 C 源文件，另有 GCC startup ASM；`AT32F423CCT7`、`USE_STDPERIPH_DRIVER`、`AT_START_F423_V1` | 列出的 C 源文件均存在，未发现 C 对象文件同名冲突；未构建 |
| TH 编译/链接 | Cortex-M4、FPv4-SP-D16、hard float，`-O2`、`-fcommon`、`-Werror=implicit-function-declaration`；nano/nosys，`-u _printf_float` | Make 输出目录可用命令行 `BUILD_DIR=绝对路径` 指定；本次未执行 |
| TH 内存/启动 | `libraries/cmsis/cm4/device_support/startup/gcc/linker/AT32F423xC_FLASH.ld`：Flash `0x08004000` / 240 KiB，RAM `0x20000000` / 48 KiB；`system_at32f423.c:39` 的 `VECT_TAB_OFFSET=0x4000` | 两处 App 偏移一致；不是固件启动验证 |
| TH 配置/版本 | `inc/usart.h`：`BAUDRATE1=921600`、`BAUDRATE2=115200`；`inc/Configuration.h`：`EXTRUDERS=1`；`color-engine-mcu/version.ini` 为 1.0.0 / build 2 | 记录实际工程配置，未推断机械通道或实物配置 |
| Bootloader | `bootloader/435/`、`bootloader/423/` | 这两个目录各只有 ELF/BIN/HEX/MAP，没有可复现构建所需的源码、链接脚本及构建入口；App 可盘点，Bootloader 源构建条件尚不齐全 |

MC CMake 中提取的 102 个源/头目录引用仅 `project/marlin/marlin_gcode` 不存在；该引用属于 include 目录，不能仅据此判定构建失败。其余引用存在，仍需 MS-02 实际编译链接。

厂商 CMSIS、标准外设库、Marlin、USB/FatFs 等依赖随当前 Git 源树提供，CMake/Make 中未见本次构建必须在线下载的步骤。开发版本头由仓内 `tools/version_tool.py` 生成，打包由 `tools/pack_firmware.py` 完成；两者使用 Python 标准库。工具链/newlib 属宿主环境依赖，尚未通过 MCU 构建核验完整性。

## 3. 实际宿主工具

当前执行宿主为 WSL2 x86_64，内核 `6.18.33.2-microsoft-standard-WSL2`，不是 VMware AP。以下来自纯 Linux PATH 下的实际 `--version` 输出，完整信息保存在 inventory：

| 工具 | 路径 | 版本 |
| --- | --- | --- |
| CMake | `/usr/bin/cmake` | 3.16.3 |
| Ninja | `/usr/bin/ninja` | 1.10.0 |
| GNU Make | `/usr/bin/make` | 4.2.1 |
| GCC / G++（宿主） | `/usr/bin/gcc`、`/usr/bin/g++` | 9.4.0 |
| Python | `/usr/bin/python3` | 3.8.10；用于本地控制仓登记及 AP 日志收集，未调用串口 |
| ARM GCC / G++ | `/usr/bin/arm-none-eabi-gcc`、`/usr/bin/arm-none-eabi-g++` | 9.2.1，20191025 |
| ARM objcopy / size | `/usr/bin/arm-none-eabi-objcopy`、`/usr/bin/arm-none-eabi-size` | binutils 2.34 |
| Linux probe-rs | 当前纯 Linux PATH | 未找到；未调用仓内 Windows 工具或检测探针 |

不把 PATH 中没有 Linux probe-rs 扩大为“Windows 烧录工具未安装”；Windows venv、COM6/COM8、探针及物理接线本次均未检查。没有安装或调整环境。

## 4. 串口实际调用路径

用户已确认的端口/引脚/格式继续以 [serial_links.md](serial_links.md) 为原件，不重复请求输入。

| 链路/能力 | 当前源码证据 | 对下一步的影响 |
| --- | --- | --- |
| AP↔MC 目标 | MC `project/src/wk_usart.c:247` 初始化 USART2 PA2/PA3、115200 8N1、无硬件流控 | 初始化与用户接线输入相符 |
| USART2 当前所有者 | `project/src/main.c:183` 初始化旧屏 RX DMA；`wk_dma.c:56` / `:266` 使用 GUI `rx_fifo`；`at32f435_437_int.c:354` 调用 `gui_rx_callback()`；DGUS 文件仍负责 TX | AP 尚无独立请求/响应入口；迁移须同时处理 RX、解析和 TX，不能只改串口初始化 |
| MC↔TH | MC `wk_usart.c:166` 配置 USART6 PA4/PA5；TH `src/bsp/usart.c:172` 起配置 GPIOB PB6/PB7 与 USART1；双方 921600 8N1 | 与已确认输入一致；MCU README §1.2 的 TH PA9/PA10 是旧说明，本次不将其当实物依据 |
| MC 查询 | `Marlin_main.c:3339` 的 M105 调用 `handleQueryTemp()`，`:5487` 生成 `ok T:... /... B:... /...`，经 printf；`syscalls.c:83` 的 `_write()` 发 USART1 | 有温度格式代码不代表能从 AP USART2 请求并收回 |
| MC 版本 | `Marlin_main.c:3542` 的 M115 位于 `:3514` 开始的 `#if 0` 内 | M115 分支仍禁用；不能把 README 查询示例当已可用接口 |
| TH 回传 | MC `motherboard.c:345` 读取 `forward_uart_rx_read()`，交 `FilamentCheckUart()` 检查 `filaout` | 尚无通用 TH 业务回复返回 AP 的路径 |
| 既有测时 | MC `main.c:280` 起从 USART1 读 `T`，调用 `mc_th_usart_perf_test(500U)`；`wk_usart.c` 发送 `G4 P0 ;#...`、检查 `ok2` | 属现有 MC↔TH 调试测时；没有本次运行证据，不代表 AP 全链路 RTT |

TH 的软件流控和 `ok2` 在现有驱动/命令处理中存在，不因“无硬件流控”而消失；是否用于新业务契约须结合待提供协议另核对。本次未发送任何 G-code，也未尝试升级二进制通道。

## 5. 现有制品与身份限制

MC `motion-controller-mcu/build/` 不存在。TH 存在旧 build 目录，未覆盖或清理。Bootloader 两目录有现成制品，完整文件大小与 SHA256 见 inventory。

| 文件（相对 mcu-p3） | 字节数 | SHA256 |
| --- | --- | --- |
| `color-engine-mcu/io_toggle/build/fw_th.bin` | 64068 | `6b5265083e8d9ef093b382f741bae7129eb5a4af45c35a7369a807146efcfecf` |
| `color-engine-mcu/io_toggle/build/fw_th.elf` | 572736 | `dba37c6a2fb510c22ab08b9ade454fb1207719816c9a4f9f37ca7ab68761065e` |
| `color-engine-mcu/io_toggle/build/anchor.bin` | 140 | `4ab5573c383ea1c3e5560080cbcdce63aaca9a1d78a4c19853b8fbf42ad76549` |
| `bootloader/435/bootloader.bin` | 34384 | `c68457f30eb027329132c800499a86f20bef4c27934761c6782930fe630336e0` |
| `bootloader/423/bootloader423.bin` | 15692 | `d85f0ec9c8d91894ec2f1eba8f02fadc2c7168f38d469fc99b335328e534eefc` |

TH 旧版本头为 `V1.0.0-A8FD 1019`，版本值 `0x0100A8FD`，时间戳 `1792407725`；与 BIN Trailer 中的版本和时间相同。按当前打包工具的数据布局直接只读检查，payload 长 63940 字节、board ID `0x42300001`、payload SHA256、Trailer CRC32、Anchor 内容/CRC32 均一致，详见 [th_existing_artifact_check.json](../evidence/20261020/th_existing_artifact_check.json)。这是现有字节的一致性检查，不是签名真实性、源码到二进制复现或板上固件身份核验。

TH `pack` 的输入输出都是 `build/fw_th.bin`。工具先完整读取输入，并用 `strip_existing_trailer()` 剥离已存在且 CRC 合法的 Trailer，再输出 payload＋128 字节 Trailer；静态代码不支持“每打包一次就必然重复追加”的判断。但原始 BIN 与发布 BIN 名称相同，后续构建/验收应明确生成时点及文件身份。生成版本头包含时间/PID 派生 build ID，不能要求不同时间构建的整个 BIN 哈希天然一致。

## 6. 后续构建入口（本次未执行 MCU 命令）

以下是从当前脚本核对的开发模式候选命令，供 MS-02 落实独立执行者和隔离输出后使用。不能复制为“已通过”的日志；不执行 `release`，它会改写受版本管理的 `version.ini`。

```bash
# 从工作区根目录执行；先确认输出目录未被占用。
export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

# MC：使用现有 Make 包装，显式指定隔离输出。
make -C mcu-p3/motion-controller-mcu \
  BUILD_DIR=/tmp/ai_soc_ms02_20261020/mc pack

# TH：必须显式选择 all/pack，不能假定无目标的 make 完成构建。
# 当前 Makefile 第一条普通目标是版本头生成目标。
make -C mcu-p3/color-engine-mcu/io_toggle \
  BUILD_DIR=/tmp/ai_soc_ms02_20261020/th pack
```

预期 MC 输出 `Marlin_AT32.elf/.bin/.hex`、`fw_mc.bin`、版本头；TH 输出 `fw_th.elf/.hex/.bin`、`anchor.bin`、map 和版本头。准入仍需 MS-01 独立评审、MS-02 路径/证据/执行者登记；运行记录应包含完整 stdout/stderr、退出码、编译器版本、源/配置/版本头哈希、size 与制品哈希，并核对源码树未被更改。硬件启动/烧录另按实际授权与资源条件进行。

## 7. 实际运行结果及缺项

AP 在 `/tmp/soc_ap_work_20261020` 重新配置和构建，命令退出码均 0，CTest `host_runtime_smoke` 1/1 通过；`--check-config` 为 `/dev/ttyUSB0`、`serial_opened=false`。[完整日志](../evidence/20261020/ap_host_build.log)。可执行文件 SHA256 为 `1cf1708ac16a8dfdc2df234c89a5991cbe9d4d5502820c49453a9e7ed21f95f3`，与上轮相同。这是作者本地主机复现，未作为独立 QA 或 VMware 验收。

服务器普通 push 脚本退出 1，四仓均因 `socket: Operation not permitted` 失败；[本次原始推送日志](../evidence/20261020/push_attempt.log)。只读 `ssh -o BatchMode=yes -o ConnectTimeout=10 vmware true` 退出 255，同样在 socket 阶段失败；[VMware 日志](../evidence/20261020/vmware_ssh.log)。未进入认证，未验证 VMware 系统、设备存在性、串口权限/占用或板上固件。

用户先回复新协议“等我确认后再提供”，随后已明确采用 MiniMCProto v2.0 / Rev 2.0.3 并要求项目内保存。当前协议身份、文件哈希和工程适用说明见[本地采用记录](../specs/protocol_selection_20261020.md)，不再保持“协议待提供”状态；时延验收门槛仍需在具体任务中登记。

后续需要：独立 ARCH 读取本文与准确源码版；MS-02 登记后独立复现 App 构建；在可联网环境核对推送及 VMware；基于已选本地 v2.0 协议细化首个最小事务。MS-01 正式状态保持 Backlog，仅更新实际输入版本和证据入口，不虚构实际 COORD 指派、独立签署或硬件通过。
