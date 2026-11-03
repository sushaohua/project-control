---
title: 双板 Bootloader 角色、仓库与开发分支边界
revision: 1
date: 2026-11-03
status: current-rule
owner: COORD
authorization: 用户明确新增 ENG_BOOT_MC、ENG_BOOT_TH，指定独立仓库、规则目录及 soc_debug 开发分支，允许缺失时创建分支
---

# 双板 Bootloader 角色与仓库边界

## 1. 角色登记

角色 ID 按用户指定原样使用下划线，不另造 ENG-BOOT-MC/TH 等别名。角色登记不表示已有实际 Agent、任务认领或新的产品功能授权。

| 角色 | 唯一开发仓库/工作区 | 远端 URL | 开发分支 |
| --- | --- | --- | --- |
| `ENG_BOOT_MC` | `boot/bootloadermc/` | `ssh://git@192.168.77.113:2222/sushaohua/bootloadermc.git` | `soc_debug` |
| `ENG_BOOT_TH` | `boot/bootloaderth/` | `ssh://git@192.168.77.113:2222/sushaohua/bootloaderth.git` | `soc_debug` |

ENG_BOOT_MC 负责 MC Bootloader 的本地启动、App 校验/跳转、升级接收与 Flash/恢复逻辑及其构建/制品；ENG_BOOT_TH 负责 TH 对应能力。具体功能仍以已接受任务和本仓代码为准，不能把登记表视为这些能力均已实现。

ENG-MC、ENG-TH 继续分别负责 `mcu-p3` 内的 MC/TH App；SoC 的 ENG-BSP 继续负责其 U-Boot/Kernel 等板级范围。App 和 Bootloader 分属不同 Owner/仓库，不因同在一块板上就跨仓写入。旧 `mcu-p3/bootloader/435`、`mcu-p3/bootloader/423` 记录保留历史引用，不再作为新增 Bootloader 开发的默认目标，不迁移或删除历史代码。

## 2. 本仓规则与任务输入

派单必须先读取对应工作区根的 `AGENTS.md`、`.agents/` 和 `docs/`，通过工作区路径访问合法软链接，不越出链接目标目录。入口为：

- MC：[AGENTS.md](../../../boot/bootloadermc/AGENTS.md)、[规则目录](../../../boot/bootloadermc/.agents/)、[文档目录](../../../boot/bootloadermc/docs/)。
- TH：[AGENTS.md](../../../boot/bootloaderth/AGENTS.md)、[规则目录](../../../boot/bootloaderth/.agents/)、[文档目录](../../../boot/bootloaderth/docs/)。

本地实施方案先行、审批记录、编码、工具链/解释器、probe-rs、串口归属、提测材料和线性提交要求继续适用。任务绑定所读规则/方案版本和哈希；已有明确有效授权可复用，不重复索要。规则或事实冲突先登记并由 ARCH/Owner 对账，不能择易执行或自行改写本仓规则。

项目级 COORD 调度、服务器候选、独立 Codex 审阅、按 qa_policy 适用的报告复核及正式状态仍按权威交付/QA 规则执行（streamlined-v1 待切换补丁按 legacy 接受并发布后启用；未迁移旧卡保留原报告复核）。本仓提测包是输入材料，不能单独替代独立接受。

## 3. 开发分支与交付要求

1. 开工、提交及推送前核对本仓真实顶层目录、URL、当前分支和任务锁定提交；两个仓库均只在 `soc_debug` 开发。
2. 禁止在 `main` 或其他主分支修改、提交或推送开发内容；不得将 App 的 `feat/soc-debug` 与 Bootloader 的 `soc_debug` 混用。
3. 分支缺失时可按本次用户授权创建；从哪个已核验基线建立须记录。切换不得覆盖用户修改，存在冲突停止相关动作并保留现场。
4. 每张实现卡只包含其 Bootloader 仓库及明确路径；App、SoC 或另一块板的改动通过关联任务由各自 Owner 承担。
5. 交付绑定完整 commit、远端 ref、规则/配置及制品哈希。源码、构建、实机和组合证据分别声明；不能凭构建号或进程退出码认定硬件升级成功。
6. 工程实现仍由 COORD 通过现行角色通道委派；两个 `ENG_BOOT_*` 明确属于工程实现岗位。角色名或本文不证明机器已强制分支保护。

## 4. App—Bootloader—AP 协作

ARCH 与相关 Owner 明确实际 Flash 分区、App 起始地址、VTOR、内存/中断/时钟交接、驻留/升级触发、通信格式、制品/Trailer 校验、生效及恢复契约。ENG_BOOT_* 负责 Boot 端；ENG-MC/TH 负责 App 端；ENG-FWD/STATE 等负责 AP 消费；INTEGRATOR 负责锁定组合和升级编排；独立 QA 按准确范围核验。

本次新增角色不改变既有“首版升级优先复用已有流程、避免修改 Bootloader”的产品约束；不自动批准扩大分区、修改启动协议、擦写 Flash、复位或故障注入。确需 Boot 改动由具体任务说明必要性、兼容组合、最小差异及授权。硬件操作沿用本仓及项目现行门禁，不从历史端口、地址或探针记录推定当前可用。

## 5. 本地接入与工具缺口

2026-11-03 初查，两仓代码分别存在，URL 与用户指定一致；当时本地和远端只有 main，允许按已核验 main 基线创建 soc_debug。分支创建/远端核验结果见[接入记录](../../docs/planning/bootloader_role_onboarding_20261103.md)。未修改业务代码、未构建测试或烧录。

当前三个规则/文档入口在两仓均为未入 Git 的本机软链接，不能随代码 clone 自动取得。用户于本轮确认“暂时仅在本机使用”：保留原链接和历史文档，不实体化、不把内容复制或上传到仓库，也不自动创建迁移任务。未来需要跨机器或服务器 QA 时再明确版本化输入方案；不得把缺规则的服务器检出当作完整验收输入。

本次先完成角色和分支边界，不声称自动工具已接通：

- 根 `tools/workspace.py` 当前只接受直接子目录，不能把 `boot/bootloadermc` 或 `boot/bootloaderth` 直接塞入现有 workspace.json；暂按恢复说明手工取得。
- `tools/check_task_graph.py` 的仓库白名单尚不含这两个仓库，不能靠新角色名绕过校验。
- COORD/QA 的候选路径、远端配置和隔离检出需区分仓库 ID 与工作区嵌套路径；规则/文档来源也需版本化。相关工具改动由 INTEGRATOR 按独立有界任务实现并接受，本轮不修改代码或自行扩大 Runner 支持范围。

用户已确认当前仅建立角色和仓库边界，首个开发目标稍后由 ARCH 明确；COORD 再据此登记实际任务及作者/检查者。台架操作授权等到实际硬件任务时核实，当前不因缺少这些信息阻塞角色登记，也不填写为已落实。
