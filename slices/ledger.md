# AI SoC V2 垂直切片执行账本 (`ledger.md`)

本账本由 `project-control/tools/workflow/run_slice_batch.py` 与 `tools/gates/slice_gate.py` 追加维护，作为断点幂等续跑与双态准出（`SW-Verified` / `HIL-Verified`）唯一状态记录。

## 1. 切片准出流水表

| 时间戳 (UTC+8) | 批次 ID | 切片 ID | 准出状态 | 锁定多仓 Commit 摘要 | Docker 容器 ID | Codex 会话 ID | Verdict SHA256 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |

| 2026-11-18 09:40:38 | BATCH-OTA-ACCEPTANCE-01 | SLICE-01 | SW-Verified | `test_harness:371a3a3,boot/bootloaderth:1a03513,project-control:e905220,agents:30ecc65,printer-soc:888d389,mcu-p3:b865222,boot/bootloadermc:3e01c00; inputs=d78eb1084e0a5c5bfe96e77aee1da621b93cfbb535a30ea6f3fe05b55620fbda` | `b10cc87ff2f6` | `01a1ec4e-08c6-74a1-a55d-1bf92676034d` | `77c377c2f09723ac` |

| 2026-11-18 10:01:30 | BATCH-OTA-ACCEPTANCE-01 | SLICE-02 | SW-Verified | `project-control:537ab04,agents:30ecc65,test_harness:371a3a3,printer-soc:888d389,mcu-p3:b865222,boot/bootloadermc:3e01c00,boot/bootloaderth:1a03513; inputs=e8a7d086a38815181b74c695d95ba86dc8a75293724318353444aa45314c5f16` | `4b590b2a03ce` | `01a1ec62-1579-7310-be0e-fa816ff31d6c` | `a6c468bd972c349d` |

## 2. 非阻断技术债登记表 (`MINOR` Findings)

| 时间戳 (UTC+8) | 切片 ID | 审计轴 | 代码位置 | 问题描述与后续收敛建议 |
| :--- | :--- | :--- | :--- | :--- |
| 2026-11-18 09:40:38 | SLICE-01 | `spec_realism` | `printer-soc/contracts/twin/telemetry_types.h:410` | ATSG trailer 的 version_code 注释仍称编码为 (major << 8) | minor，与契约及实际解析使用的高位 major/minor 布局不一致。当前传递和 Stage 4 解析按新布局工作，属于文档残留；建议更正以免后续维护误用。 |
| 2026-11-18 11:49:29 | SLICE-03 (`HIL-FINDING-02`) | `embedded_safety` | `boot/bootloadermc/bootloader/src/boot_uart_ota.c:52,206-223; cmake/linker/at32f435_bootloader.ld:14` | MC Bootloader `.bss` 变量 `s_boot_salt` 软复位清零致 `Boot->Boot` 连续软复位 `boot_id` 恒为 `0xC1E6CD05`，且 `-Os` 下 `main()` 栈帧压入 `0x2005FFF0` 覆盖 `UPG2`、当前依赖 `2000ms` 探测窗进入 Boot（正常 `App->Boot->新App` 三态跃迁不受影响）。经用户 2026-11-18 评估确认风险可承受、首版豁免不修以规避 `0x08000000` SWD 单点擦写风险。 |
