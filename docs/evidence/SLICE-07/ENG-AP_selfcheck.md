# SLICE-07 ENG-AP 自检记录

- **角色**：`ENG-AP`
- **目标仓库与分支**：`printer-soc` (`main`)
- **Candidate Commit**：`cc7bd31d7fc0d5e23c4e9c5fb0deedcfb326646b`
- **遵循方案与切片**：
  - `project-control/docs/planning/helix_screen_mc_th_integration_implementationplan_20261118_144741.md`
  - `project-control/slices/SLICE-07.yaml`
  - `project-control/contracts/minimc_v2_contract.yaml`

---

## 一、改动清单与预算核验

- **改动文件总数**：`20 / 20`（全部落在 `SLICE-07.yaml` `allowed_paths` 内；未触碰 `application.cpp`、`aisoc_json.cpp`、`mk/tests.mk`、`bootloadermc`、`mcu-p3`）
- **受保护存量变更行数**：`332 / 400`（`ui_settings_ota.h` 71 行 + `ui_settings_ota.cpp` 247 行 + `ui_settings_about.cpp` 11 行 + `xml_registration.cpp` 3 行）

### 改动文件列表
1. `tools/sign_mcu_firmware.py`（新建）：纯标准库 + `/usr/bin/openssl` CLI 实现 `--generate-key`、`--key --input --output`、`--verify --pubkey --input`，签名覆盖 `trailer[0:52]` 并重算 CRC32；注明 `boot/bootloadermc` 冻结 0 改动、MC FAT32 U 盘直接救援通道无 ECDSA 校验边界。
2. `boards/c308l-aw419/rootfs-overlay/etc/printer-soc/fw_signing_pub.pem`（新建）：合法 NIST P-256 测试信任锚公钥 PEM。
3. `tools/package_c308l_product.py`：`populate_base_tree()` 合入 `etc/printer-soc/fw_signing_pub.pem` 并设权限 `0o444`。
4. `core/firmware/CMakeLists.txt`：三模式 OpenSSL 适配（C308L SDK 静态 `libcrypto.a` / 宿主 `OpenSSL::Crypto` / 无头文件容器 `dlopen("libcrypto.so.1.1")`），保持 `-Wall -Wextra -Wpedantic -Werror -fno-exceptions -fno-rtti`。
5. `core/firmware/firmware_hash.h` / `core/firmware/firmware_hash.cpp`：导出纯 C 接口 `fw_image_resolve_pubkey_path`（默认 `/etc/printer-soc/fw_signing_pub.pem`，拒绝 `/data/`、`/media/` 测试覆盖）与 `fw_image_verify_ecdsa_p256`（校验 P-256 `NID=415`、拒绝全零签名与缺失/非法公钥、`memcpy` 规避 `-Wpedantic`）。
6. `services/forward/modules/ota/ota_image.cpp`、`services/forward/forward_ota.cpp`、`services/device_manager/firmware_updater.cpp`：三端统一调用 `fw_image_verify_ecdsa_p256`；验签失败时 `Forward` 原子返回 `PACKAGE_SIGNATURE_INVALID` 且中止于 `prepare_images()`，串口 **0 帧** `0x1D`/`0x20`；`fw_updater_verify_buffer()` 返回 `AISOC_DEV_ERR_INVALID_ARG`。
7. `services/helixscreen/include/aisoc/aisoc_connection.h` / `src/aisoc/aisoc_connection.cpp`：新增 `dds_domain_id`（支持 `AISOC_DDS_DOMAIN` 覆盖）、`AisocOtaRequest`/`AisocOtaNodeInfo`/`AisocOtaStatus`、`request_ota()`、`set_ota_callback()`、`ota_status()` 及 `AisocSnapshot::last_estop_outcome/detail`；后台线程真实调用 `ForwardInterface.OtaCommand` 并订阅 DDS `state/ota_status`（单调 `event_id` 过滤）；收到 `SUCCEEDED` 后经 DM `GetVersionInfo` 复核目标节点 `Bit31==0` App 在线且 `boot_id != pre_boot_id` 才置 `reboot_verified=true`。
8. `services/helixscreen/include/ui_settings_ota.h`、`src/ui/ui_settings_ota.cpp`、`ui_xml/ota_local_overlay.xml`（新建）及 `src/ui/ui_settings_about.cpp`、`ui_xml/about_settings_overlay.xml`、`src/xml_registration.cpp`：固定目录扫描、目标勾选（先 TH 后 MC）、安全确认、`allow_reflash`、真进度订阅与重启核验提示、明确区分 `"后台已锁定 (BUSY)"` 与 `"设备已确认急停"`，并挂载至关于页与 `#ifdef HELIX_ENABLE_AISOC` XML 注册。
9. `tests/ota/test_ota_e2e.py`、`tests/device_manager/twin/test_firmware_updater.cpp`、`services/helixscreen/tests/unit/aisoc/test_aisoc_p0.cpp`：覆盖全部 12 既有场景 + 4 类 ECDSA-P256 签发/拒签场景 + `DEC-SCREEN-03` 并发/维护锁/急停后端联调 + 真实 DDS `state/ota_status` 订阅与重启 `Bit31=0`/`boot_id` 正负例核验。

---

## 二、真实构建、测试与门禁实证

| 验证项 | 命令 | 结果 |
| :--- | :--- | :--- |
| 秒级机械门禁（提交后） | `python3 project-control/tools/gates/fast_gate.py --workspace . --slice project-control/slices/SLICE-07.yaml` | **PASS**（exit 0，20/20 文件，332/400 受保护行，0 规范/契约报错） |
| 协议契约同步校验 | `python3 project-control/tools/sync_contracts.py --workspace .` | **PASS**（exit 0） |
| 常规模式全量 CMake + CTest | `cmake -S printer-soc -B /tmp/s7_std -DSOC_AP_BUILD_SERVICES=ON -DTHIRDPARTY_INSTALL_DIR=$(pwd)/printer-soc/third_party/install && cmake --build /tmp/s7_std -j4 && ctest --test-dir /tmp/s7_std --output-on-failure` | **PASS**（24/24 全部通过，0 编译告警） |
| 常规模式 OTA + 验签 + 并发/急停 E2E | `python3 printer-soc/tests/ota/test_ota_e2e.py printer-soc /tmp/s7_std/bin printer-soc/third_party/install` | **PASS**（12 既有 + 4 签名 + `dec_screen_03_concurrency_estop`: `estop_idle=0, estop_clear=0, dup_ota=-5, gcode=-5, home=-5, estop_busy=-5`；拒签 3 负例均 `PACKAGE_SIGNATURE_INVALID` 且 0 帧 `0x1D`/`0x20`） |
| 无头文件容器模拟 `dlopen` 路径 | `cmake -S printer-soc -B /tmp/s7_dl -DSOC_AP_BUILD_SERVICES=ON -DAISOC_FORCE_DLOPEN_LIBCRYPTO=ON ... && cmake --build /tmp/s7_dl -j4 && /tmp/s7_dl/bin/test_firmware_updater && python3 printer-soc/tests/ota/test_ota_e2e.py printer-soc /tmp/s7_dl/bin printer-soc/third_party/install` | **PASS**（`-Wpedantic -Werror` 0 告警，`test_firmware_updater` 与 `test_ota_e2e` 17 场景全过） |
| HelixScreen 原生 AISoC + DDS 单测 | `g++ ... src/aisoc/*.cpp tests/unit/aisoc/test_aisoc_p0.cpp ... && /tmp/s7_final/test_aisoc_p0 ...` | **PASS**（`[PASS] test_aisoc_p0`，覆盖真实 DDS 订阅、单调 `event_id`、`BUSY` vs `CONFIRMED` 及 `Bit31=0`+`boot_id` 重启核验正负例） |
| 打包与 DEC-SCREEN-05 回归 | `python3 -m unittest discover -s printer-soc/tests/packaging -p "test_*.py" -v` | **PASS**（9/9 OK） |
| 签发工具 CLI 正负例 | `tools/sign_mcu_firmware.py --generate-key / --key / --verify` | **PASS**（未签名拒签、签名后验签通过） |
| 临时目录清理与线性推送 | 清理 `/tmp/s7_*`；`git -C printer-soc fetch origin main && rebase origin/main && push origin main` | **PASS**（线性推送至 `origin/main`，`cc7bd31d7fc0d5e23c4e9c5fb0deedcfb326646b`） |
