# SLICE-08 (`r17`) ENG-MCU 自检报告 (`S08-MCU-FIX-01`)

- **角色与范围**: `ENG-MCU`（`mcu-p3@feat/soc-debug`）
- **切片与方案依据**:
  - `project-control/docs/planning/helix_screen_mc_th_integration_implementationplan_20261118_144741.md`（§4.1–§4.4）
  - `project-control/slices/SLICE-08.yaml`（`revision: 4`）
  - `project-control/contracts/c308l_platform_contract.yaml`
- **基线提交**: `7b623d9`（`origin/feat/soc-debug`）
- **候选提交 (`candidate_commit`)**: `e5e45eea5fcdcd8cb87ba8f5e99a0cf4904390d3`（已推送至 `origin/feat/soc-debug`）
- **边界核查**:
  - 仅修改 `SLICE-08.yaml` `allowed_paths` 授权的 6 个文件（`max_files <= 6`）；
  - 未修改 `boot/bootloadermc/`、`boot/bootloaderth/`、`printer-soc/`、`test_harness/`、`sdk/`、`agents/` 及工作区根文件；
  - `protected_globs`（`wk_usart.c`、`memu_gui.c`、`main.c`）增删总计 `57` 行（`3 + 52 + 2 = 57 <= 120`）。

---

## 1. 修改文件清单与实现要点

| 序号 | 文件路径 | Diff (`+` / `-`) | 实现摘要 |
| :---: | :--- | :---: | :--- |
| 1 | `mcu-p3/motion-controller-mcu/project/src/wk_usart.c` | `+2 / -1` | `wk_usart2_init()` 将 `PA3 (GPIO_PINS_3, USART2_RX)` 的 `gpio_pull` 由 `GPIO_PULL_NONE` 改为 `GPIO_PULL_UP`，并补充中文注释说明对齐 `bootloadermc` 防 AP 重启阶段 TX 浮空拉低产生 BREAK/帧错误。 |
| 2 | `mcu-p3/motion-controller-mcu/project/inc/minimc_proto.h` | `+6 / -0` | 核实已包含 `<stdint.h>` 与 `<stdbool.h>`，新增 `minimc_usart2_clear_rx_errors()`、`usart2_rx_dma_reset()`、`minimc_proto_reset_rx_channel()` 声明及中文说明注释。 |
| 3 | `mcu-p3/motion-controller-mcu/project/src/minimc_proto.c` | `+62 / -1` | 1. 在宿主机桩区域新增弱符号桩 `__attribute__((weak)) void usart_flag_clear(...)` 与 `usart2_rx_dma_reset(void)`；<br>2. 实现 `minimc_usart2_clear_rx_errors()`：采用单次 `if`（非 `while` 循环，兼容 `test_twin44_mc_debug.c` 恒 `SET` 桩且逻辑符 `<=2`）检查 `ROERR/FERR/NERR` 并调 `usart_flag_clear(USART2, USART_ROERR_FLAG)`（读 `STS+DT` 清三者），再单独 `if` 检查 `USART_BFF_FLAG` 调 `usart_flag_clear(USART2, USART_BFF_FLAG)`（写 `sts = ~flag`）；<br>3. 实现 `minimc_proto_reset_rx_channel()`：清接收错误与 `IDLEF`，调 `usart2_rx_dma_reset()`，复位 `s_ap_parser` 与 `s_ap_ring`；<br>4. 在 `drain_ap_rx()` 调用 `usart2_rx_dma_drain()` 前先调 `(void)minimc_usart2_clear_rx_errors()`；<br>5. 在 `minimc_proto_init()` 切完 `921600` 并 `usart_enable(USART2, TRUE)` 后立即调 `minimc_proto_reset_rx_channel()`。 |
| 4 | `mcu-p3/motion-controller-mcu/project/marlin/marlin_lcd/memu_gui.c` | `+48 / -4` | 1. 核实文件顶部已 `#include "minimc_proto.h"` 及 `at32f435_437_dma.h` 中 `dma_channel_type.ctrl_bit.chen` 字段名；<br>2. 将 `s_usart2_dma_rd_idx` 提升为文件级 `static volatile uint16_t s_usart2_dma_rd_idx = 0U;`；<br>3. 在 `usart2_rx_dma_drain()` 关中断进入后调用 `(void)minimc_usart2_clear_rx_errors()`，并在 `DMA1_CHANNEL6->ctrl_bit.chen == 0U` 时补使能；<br>4. 新增 `RAMCODE1` 函数 `usart2_rx_dma_reset()`：在 `PRIMASK` 关中断保护下清 `USART2` 全部错误与 `IDLEF`、确保 `DMA1_CHANNEL6` 使能、同步 `s_usart2_dma_rd_idx` 至硬件写索引并清零 `usart2_rx_len` 与 `rxdata_complete`；<br>5. 在 `gui_rx_callback()` 先采样 `IDLEF` 状态，随后无论是否触发 `IDLEF` 均调用 `(void)minimc_usart2_clear_rx_errors()`，避免 `STS+DT` 读清序列误消解 `IDLEF` 同时确保无条件清错。 |
| 5 | `mcu-p3/motion-controller-mcu/project/src/main.c` | `+2 / -0` | 在 `BottomBox_Fans_On();` 之后、进入 `while(1)` 循环之前调用 `minimc_proto_reset_rx_channel();`（附中文注释），丢弃 `eeprom_Init()` / `Board_init()` / `setup()` 长初始化期间在 `USART2` 吃入的杂波字节与错误标志。 |
| 6 | `mcu-p3/motion-controller-mcu/tests/test_mc_ota_and_relay.c` | `+127 / -0` | 1. 新增 `s_mock_usart2_sts`（默认保留 `USART_TDC_FLAG | USART_TDBE_FLAG` 兼容现有测试）及 `usart_flag_get` / `usart_flag_clear` / `usart2_rx_dma_reset` 覆写模拟；<br>2. 新增全中文注释单测 `test_usart2_clear_rx_errors_all_flags()`、`test_boot_dirty_rx_and_reset_recovery()`、`test_poll_self_heals_usart2_errors_and_acks()`（全部函数总行数 `<=50`、入参 `<=4`、`-Werror` 零警告）。 |

---

## 2. 实测验证命令与输出摘要（均在最终提交 `e5e45eea5fcdcd8cb87ba8f5e99a0cf4904390d3` 后复核）

### 2.1 宿主机单测与静态编码门禁 (`run_tests.sh`)
- 命令：`(cd mcu-p3/motion-controller-mcu/tests && sh run_tests.sh)`
- 结果：退出码 `0`（3/3 全过）：
  - `[1/3] test_twin44_mc_debug.c`：`All 10 TWIN-44/TWIN-47/TWIN-60 test suites PASSED!`
  - `[2/3] test_mc_ota_and_relay.c`（`-Werror` 编译）：`[PASS] test_mc_ota_and_relay: all TWIN-64/TWIN-68 MC App OTA, 534B relay & underflow tests passed!`
  - `[3/3] S04/文档/分支逻辑门禁`：`[PASS] MC S04 function length (<=50), params (<=4), flat if/ternary and Chinese comments verified!`

### 2.2 V2 Fast-Gate 机械门禁
- 命令 1：`python3 project-control/tools/gates/fast_gate.py --workspace . --files mcu-p3/motion-controller-mcu/project/inc/minimc_proto.h mcu-p3/motion-controller-mcu/project/src/minimc_proto.c mcu-p3/motion-controller-mcu/tests/test_mc_ota_and_relay.c` -> 退出码 `0`（零报错）
- 命令 2：`python3 project-control/tools/gates/fast_gate.py --workspace . --slice project-control/slices/SLICE-08.yaml` -> 退出码 `0`（零报错，含 `max_files <= 6` 与 `max_protected_lines <= 120` 核验）

### 2.3 已提交干净树 ARM 交叉编译与 `fw_mc.bin` 打包验证
- 在干净树 `mcu-p3@e5e45eea5fcdcd8cb87ba8f5e99a0cf4904390d3` 执行 `make -C mcu-p3/motion-controller-mcu pack`（编译期注入 `FW_GIT_COMMIT_SHORT=0xe5e45eeaU`）：
  - `MARLIN_BIN_BYTES=384540`（`<= 917504 B`，FLASH `41.91%`，RAM `11.34%`，BOOT_IPC `25.00%`）
  - `FW_MC_BYTES=384668`
  - `FW_MC_SHA256=d94b42b47e0b7ff74e474c0710e2303c99d36ee032d5b581e258ffcd33896e87`
  - ATSG 128B 尾块校验：`TRAILER_MAGIC=0x41545347`, `TRAILER_STRUCT_VER=0x00010000`, `TRAILER_BOARD_ID=0x43500001`, `TRAILER_FW_VERSION=0x0200BA79`, `TRAILER_PAYLOAD_LEN=384540`, `TRAILER_CRC32=0x3EA0E6FB`（CRC32 与 Payload SHA-256 校验通过）
  - 归档证据文件：
    - `project-control/docs/evidence/SLICE-08/fw_mc_r17.bin`
    - `project-control/docs/evidence/SLICE-08/host_mc_arm_build_and_pack_r17.log`（含 `MCU_P3_COMMIT=e5e45eea5fcdcd8cb87ba8f5e99a0cf4904390d3` 与 `[PASS] HOST_MC_ARM_BUILD_AND_PACK`）

### 2.4 工作树清理与远端线性推送
- `make -C mcu-p3/motion-controller-mcu clean` -> 退出码 `0`
- `git -C mcu-p3 status --porcelain` -> 空（100% 干净）
- `git -C mcu-p3 fetch origin feat/soc-debug && git -C mcu-p3 rebase origin/feat/soc-debug` -> 线性无冲突
- `git -C mcu-p3 push origin feat/soc-debug` -> `7b623d9..e5e45ee feat/soc-debug -> feat/soc-debug`（`git rev-parse HEAD` 与 `origin/feat/soc-debug` 均为 `e5e45eea5fcdcd8cb87ba8f5e99a0cf4904390d3`）
