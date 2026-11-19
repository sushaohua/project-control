# SLICE-08 ENG-AP 自检

- 工程基线为 printer-soc@cc7bd31d7fc0d5e23c4e9c5fb0deedcfb326646b。首个本地候选为 printer-soc@d71eb501ef553037ee1431f2e842e96924e607ab；前序补充修正候选为 printer-soc@dc52a4193ef6110500ab6981f4f7b6d6767bdded；`r08` 第 1 轮定向返修后的最新本地候选为 printer-soc@20528ed21a7838e955e4ddf786d6fdac756ba89c，工作树干净。
- 责任范围为切片卡中的 5 个应用仓文件。公共规则来自 project-control@f131e892afbbf3e9077e20a13b6054bc566daaaf，应用仓规则来自 agents@30ecc6586a861c1543a97804cfe0600bb4778efb。
- 已读方案 v1.7、SLICE-08 r1、c308l_platform_contract.yaml、printer-soc/AGENTS.md、代码文档规范及 printer-soc-build 技能。

## 已验证

- 发布工具 6 项单测、现有打包 9 项回归及改动路径 Fast Gate 全部通过。原始记录位于 artifacts/slice-08-app-check.OWcMsK/。
- 对当前锁定的 SDK release-tool 执行 patch --dry-run --batch --forward --fuzz=0 -p1 通过。补丁与自己的 SHA-256 清单一起提交。
- 真正运行 SDK 的 AML 打包器确认完整解包能读回 system.PARTITION，并核对其与原包字节一致。-u fileType=system 分支在工具最小样本中退出 139，本候选使用通过的 -d 完整解包路径。
- 本地发布链使用独立输出目录 artifacts/slice-08-release.g9zrBD/。已通过 plan，锁定 SDK 的 56 个项目；当前正在执行真实 build。尚无制镜准出结论。

## 待处理

- ~~前轮产品包有带空格的图片。厂商文件过滤脚本已证实可用 /usr/share/printer-soc/* 原样复制，候选仍需应用并复验该修正。~~ 已在 `printer-soc@dc52a4193ef6110500ab6981f4f7b6d6767bdded` 应用并复验通过：
  - 改动文件：`printer-soc/tools/release_product.py`（`add_filelist` 将 `usr/share/printer-soc` 下的文件与子目录折叠为 `/usr/share/printer-soc/*`，并校验一级条目名称合法性）、`printer-soc/tests/integration/test_release_product.py`（新增 `test_filtered_filelist_folds_share_with_spaces`）。
  - 实测命令与输出：
    - `python3 -B -m unittest discover -s printer-soc/tests/integration -p test_release_product.py -v` -> `Ran 7 tests in 0.017s`, `OK`
    - `python3 -B -m unittest discover -s printer-soc/tests/packaging -p test_product_package.py -v` -> `Ran 6 tests in 0.411s`, `OK`
    - `python3 -B project-control/tools/gates/fast_gate.py --workspace . --files printer-soc/tools/release_product.py printer-soc/tests/integration/test_release_product.py` -> exit code `0`
    - 真实 `sdk/c308l/release-tool/aml-tools/pc/scripts/files_copy.sh` 临时目录复验 -> `FILES_COPY_OK usr/share/printer-soc/helixscreen/assets/images/orcaslicer test cube.PNG`（exit code `0`）
- 软件候选允许记录缺少两板固件及可信发布方公钥。SLICE-07 使用测试信任锚；晋级仍需相符的实际签名包、同候选 HIL 收据与独立裁决。当前未执行远端推送、设备操作或晋级。

## `r08` 第 1 轮定向返修（`printer-soc@20528ed21a7838e955e4ddf786d6fdac756ba89c`）

- 根因与修复要点（未放宽任何 `0o444` 校验）：
  - `printer-soc/tools/release_product.py`：
    - `vendor_build` 当 `os.geteuid() == 0`（如正式容器内真实 root）时直接执行 `["make", f"-j{args.jobs}", *options, "global"]` 不再套一层 `fakeroot`，确保 `cp -a` 与 `mkfs.ubifs` 保留真实磁盘 `0o444`；当 `os.geteuid() != 0` 时改用 `["fakeroot", "-s", str(args.work / "sdk-fakeroot.state"), "--", "make", f"-j{args.jobs}", *options, "global"]` 持久化虚拟权限表。
    - `post_strip_map`（被 `build_image` 与 `verify_candidate` 共用）通过新增的 `rootfs_virtual_modes` 与 `image_tree_file`，在 `args.work / "sdk-fakeroot.state"` 存在时经 `fakeroot -i <state>` 一次性读取 `rootfs` 下各常规文件的虚拟权限位并严格校验 `actual == expected` 与 `PUBLIC_KEY` `0o444`；否则直接读取磁盘 `stat()`。
  - `printer-soc/tests/integration/test_release_product.py`：
    - 新增 `build_post_strip_fixture`、`test_vendor_build_uses_fakeroot_only_for_non_root`、`test_post_strip_map_with_fakeroot_state` 与 `test_post_strip_map_without_fakeroot_state`，覆盖真实 `fakeroot -s` + `cp -a` 后 `0o444`（`version.json` / `fw_signing_pub.pem`）核验通过、篡改为 `0o644` 拒绝及无状态文件时的磁盘 `0o444` 严格校验。
- 改动文件（位于 `printer-soc` `main` 分支，提交 `20528ed21a7838e955e4ddf786d6fdac756ba89c`）：
  - `printer-soc/tools/release_product.py`
  - `printer-soc/tests/integration/test_release_product.py`
- 实测命令与原始输出（均在提交 `20528ed21a7838e955e4ddf786d6fdac756ba89c` 后执行）：
  1. `python3 -B -m unittest discover -s printer-soc/tests/integration -p test_release_product.py -v`（exit code `0`）：
     ```text
     test_escaping_manifest_path (test_release_product.ReleaseProductTest)
     拒绝安装树索引通过父路径或已存在目录链接逃逸。 ... ok
     test_filtered_filelist_folds_share_with_spaces (test_release_product.ReleaseProductTest)
     产品共享目录折叠为通配符条目，允许内部包含带空格的图片资源。 ... ok
     test_filtered_runtime_filelist (test_release_product.ReleaseProductTest)
     过滤清单保存空目录、符号链接和目标 SDK 的 Python 依赖。 ... ok
     test_immutable_document (test_release_product.ReleaseProductTest)
     同一候选重复读取成功，任何改变均保留原件并被拒绝。 ... ok
     test_post_strip_map_with_fakeroot_state (test_release_product.ReleaseProductTest)
     fakeroot -s 复制 0444 文件后可凭状态文件验过；权限篡改为 0644 必须拒绝。 ... ok
     test_post_strip_map_without_fakeroot_state (test_release_product.ReleaseProductTest)
     无 fakeroot 状态文件时直接读取磁盘权限，0644 拒绝而真实 0444 通过。 ... ok
     test_product_archive_checked (test_release_product.ReleaseProductTest)
     真正归档文件与链接均参与校验，外置树被更改后摘要核对失败。 ... ok
     test_refuses_incomplete_promotion (test_release_product.ReleaseProductTest)
     缺少固件或根仓来源时晋级直接拒绝，并保留候选及工作区状态。 ... ok
     test_vendor_build_uses_fakeroot_only_for_non_root (test_release_product.ReleaseProductTest)
     uid=0 直接执行 make global；非 root 宿主机通过 fakeroot -s 持久化状态。 ... ok
     test_verified_patch_inputs (test_release_product.ReleaseProductTest)
     补丁内容与 SHA-256 锁相符，修改补丁内容后同一检查拒绝。 ... ok

     ----------------------------------------------------------------------
     Ran 10 tests in 0.630s

     OK
     ```
  2. `python3 -B -m unittest discover -s printer-soc/tests/packaging -p test_product_package.py -v`（exit code `0`）：
     ```text
     test_c308l_services_dev_mode_inhibit_and_status (test_product_package.ProductPackageTest)
     验证 c308l_services dev-mode 写入维护抑制并阻止 respect-inhibit 启动。 ... ok
     test_dec_screen_05_three_way_pruning_consistency (test_product_package.ProductPackageTest)
     校验 DEC-SCREEN-05 编译配置、页面与 XML 注册、C308L 打包清单三方一致性。 ... ok
     test_optional_panel_has_separate_writable_runtime (test_product_package.ProductPackageTest)
     验证合入 HelixScreen 后运行时链接指向 /data/printer-soc/helix 且清单为生产模式。 ... ok
     test_package_relocates_and_rejects_overwrite (test_product_package.ProductPackageTest)
     验证目录重定位、生产配置默认值、version.json 生成及防覆盖校验。 ... ok
     test_tampered_runtime_is_rejected_before_output (test_product_package.ProductPackageTest)
     验证运行包文件篡改时拒绝输出。 ... ok
     test_unlisted_file_is_rejected (test_product_package.ProductPackageTest)
     验证出现未登记文件时拒绝打包。 ... ok

     ----------------------------------------------------------------------
     Ran 6 tests in 0.508s

     OK
     ```
  3. `python3 -B project-control/tools/gates/fast_gate.py --workspace . --files printer-soc/tools/release_product.py printer-soc/tests/integration/test_release_product.py` -> exit code `0`（无报错输出）。
  4. `python3 -B project-control/tools/gates/fast_gate.py --workspace . --slice project-control/slices/SLICE-08.yaml` -> exit code `0`（无报错输出）。
- 未执行 `git push` 或任何实板/远端操作。
