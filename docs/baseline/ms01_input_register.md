---
title: MS-01 工程与环境输入登记（本地资料已整理，源核验待进行）
date: 2026-10-13
created: '2026-10-13 13:11:46'
updated: '2026-10-13 13:17:40'
timezone: 北京时间（UTC+8）
status: materials-prepared
approval_status: Draft
related_tasks: [MS-01, MS-02, MS-03, MS-18]
tags: [soc, mc, handoff, input-register]
---

# MS-01 工程与环境输入登记

**MC 工程的位置和历史方法已有文档输入；当前源码、构建结果、固件身份和 Ubuntu/SoC 访问条件仍需核验。**本记录完成当前项目内材料整理，不是 MS-01 验收通过，不把 MS-02/03 标为已执行。

作者：当前主对话助手，整理 INTEGRATOR 交接输入；未登记实际 COORD、独立 Reviewer 或 QA 签署。用户明确选择“本轮仅整理当前文档目录”；本轮不读取项目外工程。资料中的路径和命令只作输入，不构成写入、构建或设备操作授权。

## 1. 本轮步骤与实际执行范围

- [x] INPUT-01：读取 MS-01～03、B0、环境汇总和项目内 MCU 交接资料，提取路径、版本、工具与日志来源。
- [x] INPUT-02：区分报告快照、设计建议、后续设备与待验证事项，整理查询建设前置。
- [ ] SOURCE-01：后续实际执行阶段另落实范围再只读检查 MC 私有工程与适用规则；本轮不执行，核对 Git HEAD/工作区差异、源码/配置和制品身份。
- [ ] BUILD-01：在来源与隔离输出范围具备后，按 MS-02 准备准确构建复现；本轮未构建。
- [ ] CAP-01：按准确源码复核 USART1 RX、版本/M105、回复输出路径；本轮未重新读取 MCU 源码。
- [ ] HOST-01：取得 VMware SSH 入口及 SoC 工程/启动入口，核对设备枚举与资源占用；本轮未联网或开串口。

`rg --files` 检索本项目内 CMakeLists/Makefile、C/H、ELF/BIN/LOG，未返回相关工程输入；这仅是当前检索范围结果，不证明项目外源码或制品不存在。检索没有沿链接访问项目外文件。

## 2. 已取得的交接输入

| 输入 | 文档记载 | 原始来源 | 本次接受状态 |
| --- | --- | --- | --- |
| MC 私有 App | `/home/sushaohua/projects/boot/bootloader435/motion-controller-mcu` | [[mc_th_env_summary_20261012_170811]] §2.1；[[motion_controller_migration_step0_step1_step2_complete_handoff_20261012_163100]] | 路径已提供，实际存在/访问/版本待源核验 `[UNVERIFIED]` |
| MC 远程仓库 | `ssh://git@192.168.77.113:2222/sushaohua/motion-controller-mcu.git`，Project 126 | 同上 | 文档输入；未连接远程，IP 是 GitLab 地址，不能当 VMware 地址 |
| MC Bootloader 父工程 | `/home/sushaohua/projects/boot/bootloader435` | 同上 | 只需适用规则与指定交接日志；不扩大到整个父工程开发 |
| 上游参考仓 | `/home/sushaohua/projects/motion-controller-mcu` | 环境汇总 §2.1 | 保持隔离，不读取或修改以替代私有工程 |
| MC 历史构建基线 | `983b6c5` | 环境汇总 §2.1、Step 0 交接 | 历史报告身份，不作为当前 HEAD |
| MC 能力分析快照 | HEAD `8d1c880d1277c79cd2b9d6c40dc8ed52846f18e1` 加当时工作区 | [[mc_capability_report_baseline]] §1.2、附录 C | 静态报告来源，未独立重读源码；最新状态 `[UNVERIFIED]` |
| MC 历史产物 | `motion-controller-mcu/build/Marlin_AT32.elf`、`Marlin_AT32.bin`、`fw_mc.bin` | 交接与环境汇总 §4 | 实際路径/哈希/对应源码版本待核；既有二进制不代表现行构建通过 |
| TH Bootloader | `/home/sushaohua/projects/boot/bootloader423`，远程 `bootloader423.git` | [[at32a423_project_handoff_20261010_195500]] | 只登记；这不是 TH 混色业务 App，也不在本轮拟请求读取范围 |
| TH 业务 App | 自定义 Marlin / Color Engine | 环境汇总 §2.2、§8 | 仓库 URL、目录、commit 和查询/混色契约待 ENG-TH 提供 |
| SoC 当前环境 | VMware Ubuntu 宿主程序，SSH 访问；CH340 USB 直通 MC | B0 D25；[[开发调试环境搭建（带SoC）.canvas]] | 方向已选；用户明确“还没有配置好。等执行的时候给出。”；访问/工程启动信息在执行时登记，不据此断言虚拟机或源码不存在 |
| Windows/WSL 工具 | probe-rs 0.32.0、Windows Python/pyserial | [[probe_rs_usage_guide_20261010_110700]]；环境汇总 §3 | 历史工具说明，未查实际安装或调用工具 |
| 真实 SoC 板卡 | B0 D25 记录当前无板卡 | [[AI_SoC_协作方案/baseline/B0_方案基线]] | Canvas 实体 C302X/网口是后续环境，宿主 HIL 不代替目标 SoC 运行验收 |

MC 的两个 commit 属不同历史阶段，不视为矛盾；最终应以实际仓 HEAD、工作区差异、构建配置和制品哈希共同定义本轮身份。

## 3. 构建和原始日志输入（未执行）

较新 Step 3 交接提供在 MC 私有工程运行的历史构建形式：

```bash
# 历史方法记录，未在本轮执行；独立输出参数须先从现行 CMake 配置核对。
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin \
  ninja -C /home/sushaohua/projects/boot/bootloader435/motion-controller-mcu/build
```

该命令写已有 build 目录，不能直接作为 MS-02 的隔离构建命令。只读阶段先取得 CMake 生成器、toolchain、目标与选项，保留原产物；配置新的输出目录后才开展经授权构建。

父工程交接资料引用以下原始日志，当前只确认本项目内文档有这些引用，未读取外部日志：

| 日志（均位于父工程 `docs/`） | 文档声称覆盖 | 本轮状态 |
| --- | --- | --- |
| `step0_private_repo_init_and_sync_verification.log` | 私有建仓和历史基线构建 | 待读取/核对准确制品与完整退出结果 |
| `step1_mc_vtor_and_app_boot_verification.log` | App 偏移和台架启动 | 待读取；不替代 AP 版本查询 |
| `step2_mc_udisk_upgrade_and_rename_verification.log` | MC 自升级与更名 | 待读取；不替代运行期查询或 TH 业务代理 |

## 4. MS-03 需要按源代码复核的入口

下表来自能力报告定位，不是本轮新源码证据。读取范围获准后核对文件、行号、宏条件和调用者，避免仅查到函数名称就认为 AP 能使用。

| 核查项 | MC 工程相对路径 | 应形成的证据 |
| --- | --- | --- |
| 当前版本、构建源清单和制品 | `CMakeLists.txt`、`cmake/at32_workbench/CMakeLists.txt`、toolchain、配置与现有缓存 | 源/配置/工具/制品身份，已加入构建的实际文件 |
| USART1 RX、USART6 接收与文本输出 | `project/src/wk_usart.c`、`project/inc/wk_usart.h`、中断文件、`syscalls.c` | 初始化、中断/调度、RX 入队、输出重定向和缓冲所有权 |
| 版本/M105 命令与 ACK | `project/marlin/marlin_core/Marlin_main.c`、版本/配置头 | M115 是否仍禁用、M105 可请求路径、fromsd 来源/应答语义、显式不支持 |
| 主循环和板级处理 | `project/src/main.c`、`project/marlin/marlin_core/motherboard.c` | 业务处理调用链、心跳时机、TH 回传当前消费规则 |
| 升级与运行独占 | TH 升级状态机、USB 回调、串口模式相关声明/实现 | 声明/实现/构建/主循环接入分别确认，不以头文件声明当功能完成 |

已有 M105 数据可以作为接口建设输入；版本查询或 TH 查询不存在时保留缺口，按 MCQ 微步建设。未经源码确认不发送 M115，不用任意 ok、Banner、心跳或 COM6 旁路作为成功。

## 5. 冲突与证据限制

| 来源差异 | 判断与影响 |
| --- | --- |
| 较早交接写移植独立 `bsp_usart6`；较新 Step 3 指定复用 `wk_usart` 独占 | 以较新明确的设计约束作为参考；当前代码是否实现仍需核对，不能把方案写成已执行 |
| Step 3 设计要求 printf 走 USART1；能力快照指出输出链存在分歧 | 设计与快照实现分开，归档 `wk_usart.h` 并发变化可能改变最新状态，须核对声明/实现/链接 |
| 2026-10-12 交接正文使用 AT32A423，但某条命令仍写 AT32F423 | 不复制旧烧录参数执行；真实芯片、探针与当前工具支持须维护者核对。本轮不调用 probe-rs |
| 环境汇总称宿主代码与目标 SoC 100% 一致；B0 已要求独立验证目标端 | 以当前 B0 为工作依据，设备名/驱动/ABI/性能到板后复验；登记材料不把旧表述变成兼容性承诺 |

## 6. 需要补齐的最小信息

1. **MC 只读源核验范围**：私有 App 工程，以及父目录适用 AGENTS.md、指定 `docs/` 交接日志。用户选择本轮仅整理当前目录，源读取留到后续实际执行阶段。当前项目 [[AGENTS]] 的访问范围要求项目外资料先征得同意。
2. **VMware/SoC 入口**：用户说明尚未配置好，实际执行时提供 SSH 地址/用户名或别名、SoC 工程目录和构建/启动入口，本轮不继续索取。
3. **正式交接与独立检查**：唯一 COORD 的实际入口、ARCH Reviewer、后续 MS-02 QA 及资料收件回执。当前未登记，不虚构签署。

TH 业务 App 资料主要影响出口 B，可以并行准备，不应把其缺失扩大为 MC 只读材料整理的阻塞。SoC 访问缺失主要影响 MS-18/07，不妨碍获准后的 MC 源核验。

## 7. 下一步准入与交付

当前项目内材料整理完成。后续进入实际工程执行并落实源读取范围后，先读取适用规则，捕获 HEAD/status/构建配置及关键源码身份，形成与能力报告的差异核查；不修改源工程，不联网拉取，不构建或操作设备。MS-01 需独立评审与实际收件后才能按本轮范围接受；MS-02 的隔离构建、硬件启动和 MS-03 正式交付分别留下实际结果。

本记录不调整 MS 卡状态、owner、executor、evidence 或看板投影，不把未经独立检查的材料记为 Done。

## 本地输入文件身份

以下 SHA256 由本轮读取的项目内文件计算，标识的是文档，不是 MCU 源码或固件身份。

| 输入文件 | SHA256 |
| --- | --- |
| [[mc_th_env_summary_20261012_170811]] | `91dee89be8614aff9aea882c900b8e6fc9d19d53d6d42d7f08ee8a499609f8e4` |
| [[mc_capability_report_baseline]] | `596ffa8da76b142a65fc6bbbafc06b3793c66ec4e18cd9a99ecb5c377f0ff06a` |
| [[motion_controller_migration_step0_step1_step2_complete_handoff_20261012_163100]] | `345f91858d09f0fbb2a32255f8e3966ea2c38660a85bdfb93e907af997dc124c` |
| [[motion_controller_step3_usart6_unified_and_relay_upgrade_handoff_20261012_182700]] | `0ae11221a19d66a37a4834f5bb4de15ca99634fdb1c48668837f8a5e4017c53f` |
| [[at32a423_project_handoff_20261010_195500]] | `37b5e1663a283d026ff0fd07046d1f57f52dbca0807162d25bd13349d9b179cc` |
| [[probe_rs_usage_guide_20261010_110700]] | `e7cd60f315cdb14bada632e197bc6a9f475c67e23a052bd407be0be718376b0f` |

已修正既有 next_step_engineering_handoff 操作提示的模拟器主线，与 B0 D24/D25、当前 MS 卡一致；来源资料、MS-01～03 和看板原字节保留。本轮只整理当前项目内输入，未读取项目外工程、未连接 SSH/GitLab、未构建或操作设备。

## 本轮文档验收

2026-10-13 13:15:20（北京时间（UTC+8））：本地输入登记与操作提示的 YAML、Wiki 链接、代码围栏和元数据已检查；11 项原输入/任务/看板/Canvas 的 SHA256 与整理前一致。MS-01～03 仍保留原状态、执行者与证据字段。仅完成项目内材料核对和入口同步，不代表源核验、构建或硬件通过。

## 用户本轮范围与环境答复

2026-10-13 13:17:40（北京时间（UTC+8））：用户选择“本轮仅整理当前文档目录”，并说明“还没有配置好。等执行的时候给出。”。本轮只整理 /mnt/d/AI_RDdocs 的交接材料；环境/源码/制品核验留到实际执行时落实，不访问项目外源码、不连接远程、不构建或操作设备。环境未配置不阻塞本轮文档整理，也不证明虚拟机或源码不存在。MS-01～03 状态、执行者、证据与看板保持原值。
