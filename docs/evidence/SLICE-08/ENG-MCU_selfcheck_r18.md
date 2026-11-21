# SLICE-08 (r18) ENG-MCU 自检报告 (`S08-R18-MCU`)

- **角色 / 仓库 / 分支**: `ENG-MCU` / `mcu-p3` / `feat/soc-debug`
- **基线提交**: `e5e45eea5fcdcd8cb87ba8f5e99a0cf4904390d3`
- **候选提交 (`candidate_commit`)**: `a64bffbf1a0c5cbc2fe96b51632098042697878b`（已完成 `fetch && rebase && push`，线性历史且工作树干净）
- **依据文档**:
  - `project-control/docs/planning/helix_screen_mc_th_integration_implementationplan_20261118_144741.md`（§5 `MCU-UART-01`）
  - `project-control/slices/SLICE-08.yaml`（`revision: 5`）

## 1. 修改文件与 Diff Budget 核对

本轮仅修改 **2 个文件**（切片累计 `<= max_files: 6`，受保护存量路径增删 14 行 `<= 120` 行）：
1. `motion-controller-mcu/project/src/wk_usart.c`（`+10 / -4`）：`wk_usart2_init()` 将 `PA2` (`USART2_TX`) 与 `PA3` (`USART2_RX`) 的 `gpio_drive_strength` 统一设为 `GPIO_DRIVE_STRENGTH_STRONGER`（对齐 `bootloadermc` 硅片实证值），并以 `AP_USART_BAUDRATE` (`921600U`) 直接初始化 `USART2`，保留 `DMA1_CHANNEL2` 发送与 `PA3` `GPIO_PULL_UP`。
2. `motion-controller-mcu/tests/test_mc_ota_and_relay.c`（`+165 / -1`）：直接包含并调用真实 `wk_usart2_init()`，校验 `GPIOA->odrvr`（`0x40020008`）从旧值 `0x55695AA5U` 更新为 `0x55695A55U`（`PA2/PA3` 均为 `GPIO_DRIVE_STRENGTH_STRONGER`）且波特率为 `921600U`。

## 2. 提交后验证与打包产物
- `(cd mcu-p3/motion-controller-mcu/tests && sh run_tests.sh)`：退出码 `0`（TWIN-44/47/60 + TWIN-64/68 + S04 函数长度/参数/中文注释门禁全绿）。
- 干净树 ARM 打包（`host_mc_arm_build_and_pack_r18.log`）：`MCU_P3_COMMIT=a64bffbf1a0c5cbc2fe96b51632098042697878b`、`FW_MC_BYTES=384668`、`FW_MC_SHA256=1a259d259d478ef6f461932ad72c9f3a418f31d79bb224000226d8c2df7339c1`、`TRAILER_CRC32=0xED911CFB`、`[PASS] HOST_MC_ARM_BUILD_AND_PACK`。
