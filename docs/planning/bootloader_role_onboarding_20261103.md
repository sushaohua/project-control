---
title: ENG_BOOT_MC / ENG_BOOT_TH 角色及仓库接入记录
date: 2026-11-03
revision: 1
status: roles-and-branches-registered-no-development-dispatched
source: 用户指定角色、工作区、远端和 soc_debug 分支；确认本轮只建立边界，规则文档暂仅本机使用
---

# Bootloader 角色与仓库接入记录

## 1. 本轮完成范围

登记 `ENG_BOOT_MC`、`ENG_BOOT_TH` 的独立代码所有权和本仓规则入口；分离 ENG-MC/TH 的 App 与 Bootloader 职责。两个指定仓库本已存在，本轮未重新 clone 或迁移源码。

| 项目 | MC | TH |
| --- | --- | --- |
| 角色 | `ENG_BOOT_MC` | `ENG_BOOT_TH` |
| 本地工作区 | `boot/bootloadermc` | `boot/bootloaderth` |
| origin | `ssh://git@192.168.77.113:2222/sushaohua/bootloadermc.git` | `ssh://git@192.168.77.113:2222/sushaohua/bootloaderth.git` |
| 本地开发分支 | `soc_debug` | `soc_debug` |
| upstream | `origin/soc_debug` | `origin/soc_debug` |
| 创建时已核验 main commit | `01bfda29b82f0576cb255d0b4196aeda1edb8d2e` | `1e4f592feaf400e5d4a1932db5aa86e75e60832b` |
| 创建后远端 soc_debug | `01bfda29b82f0576cb255d0b4196aeda1edb8d2e` | `1e4f592feaf400e5d4a1932db5aa86e75e60832b` |
| 创建后远端 main | 与创建前相同 | 与创建前相同 |
| 本次业务代码、构建、测试、烧录 | 未执行 | 未执行 |

两个远端初查均无 soc_debug，按用户授权从与远端 main 对齐的本地提交创建，普通推送新增分支并设置 upstream；之后实际 `git ls-remote --heads origin refs/heads/main refs/heads/soc_debug` 核对上述结果。没有向 main 推送、修改 main 历史或生成新代码提交。

MC 首次推送出现 `ssh: connect to host 192.168.77.113 port 2222: Connection timed out`，没有将该次失败计为完成；随后只读查询恢复可达，重试原已授权推送成功，并以最终远端查询确认。未绕过认证或更换用户指定远端。

## 2. 本地规则入口及用户补充决定

两仓的 `AGENTS.md`、`.agents`、`docs` 均已存在并为本机软链接，在各自工作区可读取；Git 未跟踪这三个入口。按用户确认，本轮暂仅本机使用，保留原链接及全部历史内容，不实体化、不迁移、不上传它们。

已读取两仓 AGENTS.md、可见规则索引及相关 README/提测材料约束。后续任务仍需按具体范围读取本仓实际原件，不能仅依赖本接入摘要。

- MC 文档描述 AT32F435；TH 文档描述 AT32A423CCT7，硬件指引要求 probe-rs 使用 AT32F423CCT7 参数。此为文档事实，不是本轮芯片或硬件工具实测，不擅自统一名称。
- 本仓历史 README 的旧项目名/下载地址不能替代用户本轮指定 URL；当前角色按表中 origin 定位，不改写历史文档。
- 本仓实施方案/审批、编码、probe-rs、端口/探针归属和提测要求保留；具体操作用当前授权和实测输入，不套用历史工位默认值。
- 用户明确“首个开发目标稍后由 ARCH 分配，当前只建立角色和仓库边界”。因此未创建实现任务、未启动实际 Agent、未分配硬件租约或推断要修改 Bootloader 的新功能。

## 3. 项目级登记位置

- [角色矩阵](../../.agents/rules/02_模块与Agent职责.md)：分离 App 与 Boot 的 Owner，新增两个完整角色 ID。
- [Bootloader 边界规则](../../.agents/rules/bootloader_role_boundaries.md)：路径、URL、分支、本仓输入、跨模块协作及本机使用限制。
- [派单模板](../../.agents/rules/templates/角色任务提示词.md)、[任务模板](../../.agents/rules/templates/任务卡模板.md)和[交付门禁](../../.agents/rules/delivery_and_coord_gate.md)：工程委派、分支核对及不可跨写范围。
- [manifest](../../manifest.yaml)：登记实际嵌套仓路径、角色、开发分支和观察提交；保留 mcu-p3 中历史 Boot 路径为 legacy 引用。
- [根 AGENTS.md](../../../AGENTS.md)、[WORKSPACE.md](../../../WORKSPACE.md)及[恢复说明](../guides/workspace_restore.md)：更新仓库数量和使用边界；总仓忽略 boot/，不把独立仓嵌入总仓历史。

## 4. 明确未做及后续条件

现有 workspace.json 和恢复脚本仍保持原四仓格式，任务检查器/QA Runner 的新仓路径映射尚未适配。本轮仅将缺口记入规则和 manifest，不修改脚本，不声称自动派单或服务器 QA 已支持两个 Boot 仓。

当前建立角色与仓库边界的信息已经足够，无需用户再补充首个实现需求。ARCH 后续明确实际目标后，再由 COORD 核对任务范围、本仓方案及有效批准、准确候选、角色/检查者、工具支持和必要工位信息。只有实际需要跨机器或硬件操作时，才补充相应输入。

本记录为助手的接入事实与文档自检材料，不是独立 QA 签署或 Bootloader 功能验收报告。
