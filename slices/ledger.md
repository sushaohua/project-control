# AI SoC V2 垂直切片执行账本 (`ledger.md`)

本账本由 `project-control/tools/workflow/run_slice_batch.py` 与 `tools/gates/slice_gate.py` 追加维护，作为断点幂等续跑与双态准出（`SW-Verified` / `HIL-Verified`）唯一状态记录。

## 1. 切片准出流水表

| 时间戳 (UTC+8) | 批次 ID | 切片 ID | 准出状态 | 锁定多仓 Commit 摘要 | Docker 容器 ID | Codex 会话 ID | Verdict SHA256 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |

| 2026-11-18 09:40:38 | BATCH-OTA-ACCEPTANCE-01 | SLICE-01 | SW-Verified | `test_harness:371a3a3,boot/bootloaderth:1a03513,project-control:e905220,agents:30ecc65,printer-soc:888d389,mcu-p3:b865222,boot/bootloadermc:3e01c00; inputs=d78eb1084e0a5c5bfe96e77aee1da621b93cfbb535a30ea6f3fe05b55620fbda` | `b10cc87ff2f6` | `01a1ec4e-08c6-74a1-a55d-1bf92676034d` | `77c377c2f09723ac` |

| 2026-11-18 10:01:30 | BATCH-OTA-ACCEPTANCE-01 | SLICE-02 | SW-Verified | `project-control:537ab04,agents:30ecc65,test_harness:371a3a3,printer-soc:888d389,mcu-p3:b865222,boot/bootloadermc:3e01c00,boot/bootloaderth:1a03513; inputs=e8a7d086a38815181b74c695d95ba86dc8a75293724318353444aa45314c5f16` | `4b590b2a03ce` | `01a1ec62-1579-7310-be0e-fa816ff31d6c` | `a6c468bd972c349d` |

| 2026-11-18 12:34:06 | BATCH-OTA-ACCEPTANCE-01 | SLICE-04 | SW-Verified | `mcu-p3:7b623d9,project-control:c2dd08e,agents:30ecc65,test_harness:371a3a3,printer-soc:888d389,boot/bootloadermc:3e01c00,boot/bootloaderth:1a03513; inputs=447bbb6667afd86a4ec7a145008028a9d17858fef6685304f9cef4f90b1d8b0b` | `09f53545ed28` | `01a1eced-e0c0-72f3-a67e-7270f2214a3b` | `1eafe77e4d8cc0a6` |

| 2026-11-18 13:01:24 | BATCH-OTA-ACCEPTANCE-01 | SLICE-05 | HIL-Verified | `project-control:1eeeaa1,agents:30ecc65,test_harness:371a3a3,printer-soc:888d389,mcu-p3:7b623d9,boot/bootloadermc:3e01c00,boot/bootloaderth:1a03513; inputs=d9be5022f99c8609d8d6e4e8876bb8ebae74e00887efdd8fe273a6a9c592e4e9` | `a615c1036923` | `01a1ed06-c06d-7711-8584-5f543ceffdfc` | `35f9f4b3e3ec733a` |

| 2026-11-19 11:11:43 | BATCH-HELIX-P0-01 | SLICE-06 | SW-Verified | `printer-soc:595eeee,project-control:c1221e0,agents:30ecc65,test_harness:371a3a3; inputs=6c71809c88d325523d1bf140cbefe12694a72a421f6da6b46b7a0fd3cfe0b728` | `4a429a9f463b` | `01a1f1c6-d2a0-7510-b515-5ff33b747491` | `2c77f26a2adad8a8` |

| 2026-11-19 14:20:02 | BATCH-HELIX-P0-01 | SLICE-07 | SW-Verified | `printer-soc:cc7bd31,project-control:f131e89,agents:30ecc65,test_harness:371a3a3; inputs=4c491ae44dd440f7ffa7160a063c4bfc320ef4b67f8372436740ce9c2215a488` | `9c85f030abcd` | `01a1f274-e596-7382-9a84-2a3284331b3e` | `79585d2da124db86` |

| 2026-11-20 14:28:35 | BATCH-HELIX-P0-01 | SLICE-08 | SW-Verified | `printer-soc:962ce1a,test_harness:d601cc5,project-control:ab9dc5c,agents:30ecc65,mcu-p3:7b623d9,boot/bootloadermc:3e01c00,boot/bootloaderth:1a03513; inputs=4a41896ea67ec8d4809ea9bc76667e78b6e7632e807f8e201bd50367fa52aeba` | `f593c1989ee1` | `01a1f7a2-5b59-7831-933d-540c52c3fae6` | `b50d42fc19d763c1` |

| 2026-11-20 17:40:09 | BATCH-HELIX-P0-01 | SLICE-08 | SW-Verified | `printer-soc:8f26e97,test_harness:fb1409b,project-control:b957c08,agents:30ecc65,mcu-p3:7b623d9,boot/bootloadermc:3e01c00,boot/bootloaderth:1a03513; inputs=7150145bbe210847fc340c18991f2321c753a6c0102f42cd9dc5cac742ca1637` | `cab377dea9a2` | `01a1f852-5fd5-7b02-ab55-6b4e409f0017` | `f579aacae78788b0` |

| 2026-11-21 12:08:57 | BATCH-HELIX-P0-01 | SLICE-08 | SW-Verified | `printer-soc:c9a1541,mcu-p3:e5e45ee,project-control:dc9a027,agents:30ecc65,test_harness:fb1409b,boot/bootloadermc:3e01c00,boot/bootloaderth:1a03513; inputs=2d78eecbda2581f0fe9091c72843f4d5cf99bce0844158b5227ff5c5d1d9c018` | `080ae3a07474` | `01a1fc48-463a-7d10-a07d-14fd1b64b53c` | `85b9fef0c903d68d` |

| 2026-11-21 16:30:58 | BATCH-HELIX-P0-01 | SLICE-08 | SW-Verified | `printer-soc:6f28023,mcu-p3:a64bffb,project-control:d528cd5,agents:30ecc65,test_harness:fb1409b,boot/bootloadermc:3e01c00,boot/bootloaderth:1a03513; inputs=ceea6db89736859451720586a4239dc1f8a6dc064c976e6422912431dc613363` | `5fc544710549` | `01a1fd38-682b-7dc1-853a-45cf18e9640f` | `8dfca02c9e446448` |

| 2026-11-21 17:26:46 | BATCH-HELIX-P0-01 | SLICE-08 | HIL-Verified | `printer-soc:6f28023,mcu-p3:a64bffb,project-control:3c24d42,agents:30ecc65,test_harness:fb1409b,boot/bootloadermc:3e01c00,boot/bootloaderth:1a03513; inputs=68ac2cfd3724021eb157338dc8c85385faab9ca112b36d81356ac9641a8b719c` | `5fc544710549` | `01a1fd6b-eccd-7ea3-90b7-c93c478fe86b` | `b418e4ba5fb032a2` |

## 2. 非阻断技术债登记表 (`MINOR` Findings)

| 时间戳 (UTC+8) | 切片 ID | 审计轴 | 代码位置 | 问题描述与后续收敛建议 |
| :--- | :--- | :--- | :--- | :--- |
| 2026-11-18 09:40:38 | SLICE-01 | `spec_realism` | `printer-soc/contracts/twin/telemetry_types.h:410` | ATSG trailer 的 version_code 注释仍称编码为 (major << 8) | minor，与契约及实际解析使用的高位 major/minor 布局不一致。当前传递和 Stage 4 解析按新布局工作，属于文档残留；建议更正以免后续维护误用。 |
| 2026-11-18 11:49:29 | SLICE-03 (`HIL-FINDING-02`) | `embedded_safety` | `boot/bootloadermc/bootloader/src/boot_uart_ota.c:52,206-223; cmake/linker/at32f435_bootloader.ld:14` | MC Bootloader `.bss` 变量 `s_boot_salt` 软复位清零致 `Boot->Boot` 连续软复位 `boot_id` 恒为 `0xC1E6CD05`，且 `-Os` 下 `main()` 栈帧压入 `0x2005FFF0` 覆盖 `UPG2`、当前依赖 `2000ms` 探测窗进入 Boot（正常 `App->Boot->新App` 三态跃迁不受影响）。经用户 2026-11-18 评估确认风险可承受、首版豁免不修以规避 `0x08000000` SWD 单点擦写风险。 |
| 2026-11-19 11:11:43 | SLICE-06 | `spec_realism` | `printer-soc/tests/packaging/test_product_package.py:245-268` | 监管器测试只在没有活动子进程、UART/fb0 节点不存在的夹具中验证 dev-mode/status/inhibit；未直接启动并停止监管器及真实子进程来验证退出后 UART 与 fb0 无残留。实现中有停止等待和资源占用检查，但该生命周期闭环缺少运行时回归覆盖。 |
| 2026-11-19 14:20:02 | SLICE-07 | `spec_realism` | `project-control/docs/planning/helix_screen_mc_th_integration_implementationplan_20261118_144741.md:474,575` | 方案将签名范围写作 trailer[0..52]，按闭区间理解为 53B；验收要求 52B trailer[0..51]，且签发脚本使用前 52B、验证实现传入长度 52U，实际代码符合验收。建议将方案中的边界统一改为 trailer[0..51] 或明确写“前 52 字节”。 |
| 2026-11-21 16:30:58 | SLICE-08 | `spec_realism` | `printer-soc/services/forward/modules/ota/ota_transfer.cpp:16` | Stage-4 重试次数注释称“首轮 + 最多8次重询”，但常量控制的总探测次数为8轮（首轮加7次重询）。实现符合“最多8轮”判据，建议修正注释以免误读。 |
| 2026-11-21 17:26:46 | SLICE-08 (`BOOT-MC-STAY-01`) | `spec_realism` | `boot/bootloadermc/bootloader/src/boot_uart_ota.c:323-337` | 只读 `0x01` 查询置位 `stay_in_boot` 致 MC 复位撞上 2s 探测窗时驻留 Bootloader（不影响 `0x22` 直接 `jump_to_app()`）。按用户批准选项 B 延后至下一轮 `soc_debug` 修复，交接单：`project-control/docs/planning/bootloadermc_0x01_stay_in_boot_handoff_20261121_145800.md`。 |
| 2026-11-21 17:26:46 | SLICE-08 (`TH-ESTOP-01`) | `embedded_safety` | `mcu-p3/color-engine-mcu/io_toggle/src/app/minimc_proto.c:661-670` | TH App 对 `0x17` (`plen=1`) 返回 `0B ACK`（Forward 要求 `4B ACK` 致 `AC-05` 返 `-8`）且未区分 `stop_mode=0` 解除语义。按用户批准选项 B 延后至下一轮控制面任务修复，交接单：`project-control/docs/planning/th_app_0x17_estop_ack_handoff_20261121_171500.md`。 |
