# 2026-10-20 工程核验原始证据

作者：AI (Codex)，当前主对话 `/root`。这些是作者实际采集/复现的结果，没有独立 Reviewer 或 QA 签署。

| 文件 | 来源与适用范围 |
| --- | --- |
| [inventory.json](inventory.json) | 本地 Git 元数据、纯 Linux PATH 下工具 `--version`、37 个实际文件的 SHA256、既有制品大小/哈希。Git upstream 是本地缓存；控制仓 status 在证据开始写入后采集。CMake 路径按 `${CMAKE_SOURCE_DIR}/...` 引用提取；TH 按 `C_SOURCES` 检查文件存在性与 C 对象同名。这不是编译检查。 |
| [th_existing_artifact_check.json](th_existing_artifact_check.json) | 只读解析既有 TH BIN 尾部 128 字节 Trailer 和 140 字节 Anchor；布局及 CRC/SHA 算法来自当前 `mcu-p3/tools/pack_firmware.py`。未调用打包工具写文件；未核验二进制对应当前源码或板上固件。 |
| [ap_host_build.log](ap_host_build.log) | 本地主机在 `/tmp/soc_ap_work_20261020` 新建输出，依次实际配置、构建、CTest、配置输出；含命令与退出码。CTest 以 build 为 cwd 运行，兼容本机 CMake 3.16.3。 |
| [push_attempt.log](push_attempt.log) | 根目录 `bash push_to_server.sh` 的完整 stdout/stderr，退出 1，四仓均失败；根目录原始副本在 `artifacts/server_sync_20261020/push_attempt.log`。执行时四仓干净，未强推、未改分支。 |
| [vmware_ssh.log](vmware_ssh.log) | 实际 `ssh -o BatchMode=yes -o ConnectTimeout=10 vmware true` 的完整 stdout/stderr，退出 255；未进入认证或运行远端命令。 |
| [SHA256SUMS](SHA256SUMS) | 本目录其他文件的摘要，可在此目录用 `sha256sum -c SHA256SUMS` 复核。 |

本批没有 MCU 构建日志或硬件 TX/RX。Linux Python 3.8 用于控制仓本地登记/哈希收集，没有调用 Windows 程序、串口或 probe-rs，也没有安装依赖。只读探索期间遇到旧路径不存在、PATH 净化后 `rg` 不在 PATH、Python 3.8 不支持 `Path.readlink()` 等工具差异；后续用实际路径、`os.readlink()` 和现有 Linux 工具采集，不把这些探索错误当作 MCU 构建失败。

工程结论和未确认项见 [MS-01 当前工程登记](../../baseline/ms01_source_inventory_20261020.md)。
