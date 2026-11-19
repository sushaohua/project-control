# QA Docker 工具链补齐与候选镜像验证方案

## 修订历史

| 版本 | 修订时间 | 修订人 Agent / Author | 变更摘要 | 审批状态 |
| :--- | :--- | :--- | :--- | :--- |
| v0.1 | 2026-11-18 11:59:38 +0800 | AI (Codex) | 提出独立候选镜像、版本锁定与同镜像回归方案 | 待用户批准实施 |
| v1.0 | 2026-11-18 14:03:44 +0800 | AI (Codex) | 记录用户「批准方案」，按既定范围执行候选构建与验证 | 已批准执行 |
| v1.1 | 2026-11-18 14:08:27 +0800 | AI (Codex) | 候选镜像构建及工具检查通过；AP 回归 C08 失败，按规则停机并保留物证 | 候选未通过验收 |

## 目标与范围

解决首单复盘 P-02。让 AP 软件回归与 MC、TH App 和两个 Bootloader 的 ARM 交叉构建，能在同一个确定的 Docker 镜像中重现。现行 OTA 批次继续使用其已批准环境。本方案只准备候选并验证，不改现行门禁配置、切片、账本、业务源码、协议、固件运行逻辑或硬件状态。

用户要求提前告知任何需要中断 COORD 的动作。候选使用独立镜像名、构建目录、检出副本和证据路径。开始重负载构建前核对当前宿主负载及共享环境占用；各组顺序执行，回归容器限制为两个 CPU 配额，因为已有 OTA 套件内部固定使用 `-j4`。如只能通过停用 COORD 的任务、重启 Docker 服务或改用现行镜像标签来推进，先停在该动作之前，说明原因与影响。

## 已核实的入口与技术取舍

| 入口 | 核实结论 |
| :--- | :--- |
| 本机 `qa-sandbox:20261029` 与 SLICE-01/02 Docker 证据 | 本机为 Ubuntu 20.04、`linux/amd64`，镜像 ID `sha256:acbab225932c3877fff37f4d9e5a21235e099182c198e4f4034064ea80cf544f`，与两次归档证据一致。既有镜像具备 AP 软件回归所需库，首单 ARM 构建证据来自宿主机。 |
| `tools/qa_runner/qa_runner.py` 的 `accepted_profile_image(req: QARunRequest, config: dict) -> str` | `host-software` 返回 `sandbox.image`；`image_digest` 用于 C308L 目标 profile。本次候选通过准确镜像 ID 启动并核对 `docker inspect`，正式切换时应针对 `host-software` 明确锁定方式。 |
| `start_docker_sandbox(name: str, image: str, mount_dir: Path, read_only: bool = True) -> str` | 现有约定为 `/workspace` 源码只读、`/output` 制品可写。候选验证沿用这两个路径约定。 |
| `boot/bootloadermc/tests/run_tests.sh`、`boot/bootloaderth/tests/run_tests.sh`、`mcu-p3/color-engine-mcu/io_toggle/Makefile` | 现有流程会在工程目录内产生 `build/`，需要在 `/output` 下使用只供本次运行的源码副本。MC／TH App 的版本生成会读取 Git HEAD，副本须保留且核对 Git 元数据。 |

选择在现有镜像上追加工具，复用已验证的 AP 依赖环境。另一条路线是从 Ubuntu 基础镜像重新构造 AP 库和 ARM 工具链，能消除对现有本地镜像的依赖，但涉及重新确认 Fast DDS、D-Bus 和 AP 回归，本次成本更高。候选交付记录基准镜像、包版本和候选镜像 ID；基准镜像跨机器的可取得性尚待验证 `[UNVERIFIED]`，不得仅凭本机通过签发跨机器可重建的结论。

## 有序子任务、边界与验证

| ID | 改动或执行位置 | 依赖与交付 | 通过条件 |
| :--- | :--- | :--- | :--- |
| QA-IMG-01 | 新增 `project-control/tools/qa_runner/Dockerfile.toolchain` | 用户批准后核对现有基准镜像 ID；确认可用且兼容的 `gcc-arm-none-eabi`、`ninja-build`、`python3-pytest` 版本和 ARM 工具依赖，记录具体来源及版本。以 `qa-sandbox:toolchain-20261118-candidate` 构建，构建输入仅包含该配方。 | `docker build --pull=false -f Dockerfile.toolchain -t qa-sandbox:toolchain-20261118-candidate .` 在仅含配方的独立构建目录中成功。候选运行时的 `arm-none-eabi-gcc --version`、`arm-none-eabi-objcopy --version`、`arm-none-eabi-nm --version`、`ninja --version` 和 `python3 -m pytest --version` 均成功。镜像配方与版本清单能够追溯各项新增工具。 |
| QA-IMG-02 | `artifacts/qa-docker-toolchain/` 下新建本次独立检出与证据目录 | QA-IMG-01 通过。按 SLICE-01/02 锁定 `printer-soc@888d389`、`mcu-p3@b865222`、`boot/bootloadermc@3e01c00`、`boot/bootloaderth@1a03513`、`test_harness@371a3a3` 及 `project-control@537ab04`、`agents@30ecc65`。检出前解析并记录完整 SHA，不从 COORD 工作树复制文件。运行挂载的原始检出为只读，构建需要的副本在独立输出区创建并校验 HEAD。 | 下列现有构建和用例按组全部返回 0；产物符合现有容量上限，日志、命令、退出码、检出提交、镜像 ID、产物哈希对应同一轮执行。 |

Diff Budget 为 **1 个实现文件，最多 40 行**，另维护本方案记录。候选验证复用既有脚本，无公开接口签名或跨仓契约变更。启动容器前核对镜像 ID，容器不直连台架，不挂载开发工作树或 Docker socket；验证命令仅用已检出输入，构建测试容器关闭外网。镜像构建阶段仅为取得批准版本的依赖使用网络。测试产物保存在根工作区 Git 忽略的 `artifacts/qa-docker-toolchain/`，不写现行验收归档。

在新容器中按组使用以下入口。每组独立保存原始 stdout、stderr 和退出码。失败时保留该运行目录供复核。

| 组别 | 执行命令与判据 |
| :--- | :--- |
| AP 与协议回归 | 在 `test_harness` 执行 `python3 static_checks/minimcproto/run_ota_software_suite.py`。复用该套件 C05～C08 的 AP 服务构建及五项 CTest（含 Gateway/Forward 的 PTY 回归），核对 39 项全部通过。补跑 `python3 -m unittest discover -s hil/tests -p test_mcu_firmware_upgrade.py`，核对六项软件单测通过。 |
| 两个 Bootloader | 在各自的 `/output` 工作副本执行 `sh tests/run_tests.sh`。MC 二进制不超过 131,072 字节，TH 不超过 16,384 字节；两边脚本已有的单测、编译或打包边界检查全部通过。 |
| 两个 App | 在 MC 工作副本执行 `cmake -S motion-controller-mcu -B /output/build_mc_arm -G Ninja` 与 `cmake --build /output/build_mc_arm -j2`；在 TH 工作副本 `color-engine-mcu/io_toggle` 执行 `make -j2 all`。分别在双板 App 的 `tests/` 目录执行 `sh run_tests.sh`。确认 MC 净荷不超过 917,504 字节，TH 不超过 241,664 字节。 |

这轮结果说明候选镜像的实际覆盖。真机 HIL、C308L 目标应用或制镜 profile 与正式 `SW-Verified` 仍分别按各自流程取证。当前主线仅保留原镜像；候选失败时保留证据和独立运行目录，继续使用现行基线。候选成功后出示镜像和证据，在任何需要切换共享默认配置或影响 COORD 的操作前告知用户。

## 执行记录

- QA-IMG-01 通过。候选镜像 ID 为 `sha256:6a0b568976683a70ff8dd68ea3723217fda94bbf6b2d8ec5cd75feeffefa2dd7`。镜像配方固定 Ubuntu Focal 的 17 个新增软件包版本。ARM GCC 9.2.1、Binutils 2.34、Ninja 1.10.0、pytest 4.6.9 均在候选容器内实际运行检查。旧镜像 ID 与方案记录一致。
- QA-IMG-02 首项失败。七仓检出核对了准确提交，容器以普通用户运行、禁用外网，挂载 `/workspace` 只读和 `/output` 可写。既有 OTA 软件套件报告 38 项通过、1 项失败。C08 中 `test_ui_gateway_routes` 返回 8，现有套件输出记录 `job start via D-Bus ok` 断言失败。套件本身截断了内层 CTest 输出，现有证据不足以定责。已停止回归，双板应用和 Bootloader 交叉编译未执行。
- 原始记录保存在 `artifacts/qa-docker-toolchain/run-20261118-140344/`。`logs/image-build.log`、`logs/tool-versions.log`、`logs/input-commits-final.txt` 和 `logs/container-inspect.json` 分别记录环境与输入，`output/steps/ap-ota-suite.stdout` 和同名 `.stderr`、`.exit` 保存首项原始输出和退出码。首次浅检出失败另保留在 `logs/checkout.stderr`；改用本地分支历史后，七个检出均与原计划提交一致。
