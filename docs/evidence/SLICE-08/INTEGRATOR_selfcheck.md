# SLICE-08 INTEGRATOR 软件自检回执

- 本地候选 `test_harness@d601cc5a63bbe453b4d4c253fc5e62a2d0a5a19b`，基线 `371a3a3de7e878d4035388ccab70ef4bc84f9046`。
- 规则来源 `project-control@f131e892afbbf3e9077e20a13b6054bc566daaaf`、`agents@30ecc6586a861c1543a97804cfe0600bb4778efb` 和任务切片 r1。
- 变更范围为 `test_harness/hil/tests/test_helix_screen_integration.py`，1 个文件。软件自测完成。当前无本轮现场收据、正式 HIL 审签或远端候选。

## 本地验证

`python3 -B test_harness/hil/tests/test_helix_screen_integration.py --self-test` 退出码 0。

```text
test_disallow_path_escape_before_read (__main__.OfflineChecks)
物证相对路径不得读取收据目录之外的数据。 ... ok
test_latency_and_promotion_changes_rejected (__main__.OfflineChecks)
超时和晋级时更换产物摘要均须失败。 ... ok
test_rejected_package_trace_with_write_command_fails (__main__.OfflineChecks)
离线重放旧日志中的合法启动写刷帧，确认拒签窗口判据会拒绝它。 ... ok
test_reordered_reply_is_not_evidence (__main__.OfflineChecks)
同一对历史帧若回包早于请求，即使 CRC 合法也不能作为本次关联。 ... ok
test_short_or_damaged_tx_cannot_prove_zero_erase (__main__.OfflineChecks)
归档缺失整帧时，不能将一次截断采集解释为零写刷。 ... ok
test_valid_promotion_can_append_evidence (__main__.OfflineChecks)
晋级附加审签证据时复用候选构建身份和制品信息。 ... ok
test_version_exchange_uses_raw_frame_identity (__main__.OfflineChecks)
复用 SLICE-05 的 B1 两行采集向量，核对配对、短版本和 App 模式。 ... ok
test_wrong_artifact_hash_rejected (__main__.OfflineChecks)
同目录真实文件的错误摘要必须拒绝。 ... ok

----------------------------------------------------------------------
Ran 8 tests in 0.001s

OK
```

`python3 -B project-control/tools/gates/fast_gate.py --workspace . --files test_harness/hil/tests/test_helix_screen_integration.py` 退出码 0，无标准输出。提交前 `git -C test_harness diff --cached --check` 退出码 0。

使用既有 `SLICE-05/hil_raw_hex.log` 对照锁定 Bootloader 源码的固件版本宏。此处为解析回归，现场窗口归属 SLICE-05。

```text
mc_boot 3e01c00ce4dfb5e9e749e79c3cfbc076e3680bf4 0x4FC171EA archived-frame match
th_boot 1a0351363cf7b9cbc0aa6919b4afc6be61561152 0x769FCCBE archived-frame match
```

## 实板取证与离线复核

1. Human Gate #2 后确认台架独占、UART 硬件来源、零加热和恢复条件。安装前保存 `/`、`/data` 的空间记录与清理清单，记录 `/data/boot_backup.img` 的清理前后摘要。部署只使用已验候选中绑定的 `printer-soc-rootfs.tar.gz`。归档现场 `/etc/printer-soc/version.json`、双板 App 候选摘要、两个 Bootloader 制品及对应的历史安装物证。
2. 先采正常无 SSH 干预冷启动、生产入口触控和 About 版本，再采双板 OTA 和急停正例。保存真实 UI/D-Bus 入口记录、UART 原文和板端观察，保留升级完结 ACK 后新 App 的版本回包。接着执行方案中全断连、半断连、各 OTA 负例、急停 BUSY、调试资源释放和默认启动退出码的对应测试。
3. 收据 JSON 以 `slice_id`、`candidate_sha256`（候选原始 JSON 字节摘要）、`target`、`uart`、`preflight`、`nodes` 和 `cases` 为顶层键。文件引用使用 `{path, sha256}`，路径相对收据目录。UART 配置 `{transport, port, baud, provenance}` 取实板；`preflight` 保存 `physical`、`probe_rs_used`、`heating_pwm_pct`、`gateway_running`、根与数据分区各自的 `*_free_before_bytes` 和 `*_free_after_bytes`、`boot_backup_sha256_before`、`boot_backup_sha256_after`、`cleanup_paths`、`install_prefix` 与 `installed_rootfs_sha256`。
4. `nodes.ap/mc/th` 记录 `commit`、`artifact_sha256`，AP 另有 `readback` 文件引用。两个 Bootloader 对应 `nodes.mc_boot/th_boot`，各自记录 `commit`、`artifact` 和 `install_record`。按脚本 `CASE_EXPECTATIONS` 逐一记录用例的 `entry`、`physical` 和 `observed`。有串口断言的用例还需 `uart` 文件引用及 `phase`。沿用原始日志行格式 `[阶段] ISO8601时间(+相对毫秒ms) TX|RX 十六进制帧`。全断连和半断连在同一采集窗口拉通前后，在 `observed.reconnect_at_ms` 中记录与串口相同时间原点下的实际复接时标，并记录 `recovery_ms`。有关时限的其余键见脚本 `check_cases`。
5. 按下方命令核对文件及帧对账。退出 0 表示 `EVIDENCE-CHECKED`，独立审阅仍需确认物理记录来源及真实同源候选。冷启目标单列为 `cold_boot_target_met`，原始用时保留。Human Gate #3 后如生成晋级清单，可用 `--promoted` 核对封套与实测候选原件和制品是否相同。

```bash
python3 -B test_harness/hil/tests/test_helix_screen_integration.py \
  --candidate "$release_dir/release-manifest.json" \
  --evidence "$hil_dir/hil-receipt.json" \
  --board printer-soc/boards/c308l-aw419/board.yaml
```
