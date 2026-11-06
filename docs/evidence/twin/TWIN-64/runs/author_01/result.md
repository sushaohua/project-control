# TWIN-64 作者交付与自测报告 (`author_01`)

- **任务 ID**: `TWIN-64`
- **执行角色**: `ENG-MC / ENG-TH` (`07a1f6dc-f47c-45e5-bf00-37ec14e2dfda`)
- **目标仓库与分支**: `mcu-p3` (`feat/soc-debug`)
- **基线 Commit**: `57674d8b07d6c75a4d20b3fcd52c23df964aa7a7`
- **候选 Commit**: `5c8aa04366231cbf8115ecf1c00db1ce43ecd664`

## 1. 规则入口与输入源显式读取登记 (`read_sources`)

- `mcu-p3/.repo-rules/AGENTS.md` + `mcu-p3/.repo-rules/SOURCE.json` (`source_commit: 6dc6d9e9b7ba9a9db4fb9ac7bc8db87fb65bf6de`)
- `project-control/.agents/rules/repository_rule_sources.json`
- `project-control/.agents/rules/repository_rule_boundaries.md`
- `project-control/.agents/rules/bootloader_role_boundaries.md`
- `project-control/.agents/rules/c_cpp_coding_standard.md`
- `project-control/.agents/rules/code_documentation_standard.md`
- `project-control/docs/architecture/minimc_v2_unified_mcu_upgrade_architecture_20261105.md` (`sha256: b2b6d047500180c9f4d67d72c94794cbe5080caa52901ba262aa089bc1543223`)
- `project-control/docs/specs/ap_mc_formal_protocol_v2_0_4_unified_ota_20261106.md` (`sha256: ec874cab3f8f98fec6412b2da2b4f1fa52bfd8a33601da21e908b0ffaeb0522c`)

## 2. 核心修改与交付物清单

1. **MC App 520B 载荷扩容、`0x1D` 受控进 Boot (`0x2005FFF0` `"UPG2"`) 与 `DST=0x03` 维护态 534B 透明代理路由**：
   - `motion-controller-mcu/project/inc/minimc_proto.h` & `src/minimc_proto.c`：`MINIMC_MAX_PAYLOAD_SIZE = 520U`（`534B` 最大帧），`AP_RING_CAPACITY = 1024U`，`drain_ap_rx` 预算 `600U`，`drain_th_rx` 接收缓冲扩容至 `MINIMC_MAX_FRAME_SIZE` (`534B`)；实现 `0x1D CMD_SYSTEM_CONTROL` 安全门禁（忙状态返回 `0x06 CMD_NACK` `0x05 ERR_DEVICE_BUSY`；空闲安全态关加热、急停队列、回 4B `0x00 CMD_ACK`、写 `*(volatile uint32_t *)0x2005FFF0UL = 0x55504732UL` `"UPG2"` 并软复位）；实现 `DST=0x03` `proxy_active` 534B 大帧透明路由、维护期间业务帧 `NACK 0x05` 与 `5000ms` 超时自动恢复。
   - `motion-controller-mcu/project/inc/wk_dma.h` & `src/wk_usart.c`：`FORWARD_UART_TX/RX_BUF_SIZE = 600`，清理 `0x5A 0xA5` 历史残留并在非 `NORMAL` 模式下静默阻断本地 G-code 行下发。
   - `motion-controller-mcu/project/inc/th_upgrade_mgr.h` & `project/marlin/marlin_module/th_upgrade_mgr.c`：`TH_FLASH_MAX_APP_SIZE = 236U * 1024U`，将 U 盘 `0:/fw_th.bin` 升级器 100% 迁移至 MiniMCProto v2.0（`0x1D` ➔ `0x01/0x02` `BOOT_MODE` 确认 ➔ `0x20` `144B` 握手 ➔ `0x21` 分块流 ➔ `0x22` 终验），彻底清除 `M997` 文本与 `0x5A 0xA5` 私有帧。
2. **TH App 520B 载荷扩容、`0x1D` 受控进 Boot (`0x20008000` `"UPGD"`)、动态 `boot_id` 与 `236K` 链接限制**：
   - `color-engine-mcu/io_toggle/inc/minimc_proto.h` & `src/app/minimc_proto.c`：`MINIMC_MAX_PAYLOAD_SIZE = 520U`，轮询预算 `600U`；实现 `0x1D CMD_SYSTEM_CONTROL` 安全门禁（忙状态返回 `NACK 0x05`；空闲安全态关加热/停电机、回 4B `0x00 CMD_ACK`、写 `*(volatile uint32_t *)0x20008000UL = 0x55504744UL` `"UPGD"` 并软复位）、`0x17` 单播/广播急停、`0x19` `action > 2U` `NACK 0x03` 与 `minimc_proto_get_boot_id()`。
   - `color-engine-mcu/io_toggle/src/app/mycontrol.c`：移除 `m997_execute_firmware_upgrade_reset` 中的 `send_quick("ok2\r\nM997 SYSTEM RESET\r\n")`。
   - `color-engine-mcu/io_toggle/libraries/cmsis/cm4/device_support/startup/gcc/linker/AT32F423xC_FLASH.ld`：`FLASH LENGTH = 236K`。
3. **宿主机自包含测试套件**：
   - `motion-controller-mcu/tests/test_mc_ota_and_relay.c` & `run_tests.sh`
   - `color-engine-mcu/tests/test_th_ota_and_bootid.c` & `run_tests.sh`

## 3. 自检命令与客观输出

执行命令：
```bash
rm -rf /tmp/qa_twin64 && cp -r . /tmp/qa_twin64 && cd /tmp/qa_twin64/motion-controller-mcu/tests && sh run_tests.sh && cd /tmp/qa_twin64/color-engine-mcu/tests && sh run_tests.sh && rm -rf /tmp/qa_twin64
```
结果：`Exit Code: 0`，MC 与 TH 回归套件、`TWIN-64` 专项测试套件及 `S04` 函数行数（`<= 50`）、入参（`<= 4`）与中文注释门禁 100% 通过。
