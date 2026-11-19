# SLICE-08 ENG-AP 自检

- 工程基线为 printer-soc@cc7bd31d7fc0d5e23c4e9c5fb0deedcfb326646b。首个本地候选为 printer-soc@d71eb501ef553037ee1431f2e842e96924e607ab；补充修正后的最新本地候选为 printer-soc@dc52a4193ef6110500ab6981f4f7b6d6767bdded，工作树干净。
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
