---
id: ARCH-GUARD-20261104
revision: 2
date: 2026-11-04
status: documentation-correction-in-progress
qa_policy: streamlined-v1
scope: role-and-dispatch-instruction-correction-only
---

# ARCH 与 COORD 职责纠偏

## 用户要求与范围收敛

用户要求补齐 COORD 代做 ARCH 技术依赖/路径分析的职责缺口、沿用简化 QA 并推送远端，随后明确：“不要过度修复。仅仅纠偏即可。”本轮据此收敛为职责规则、现有派单模板注释和接续提示词的修正。

不新增合同协议、来源包、自动规划路由、权限系统、阶段锁例外或审批环节；Runner、Ready 检查器和角色适配器的本轮未提交代码扩展已撤回。收敛后只做文档检查，不继续构建或代码测试；未启动业务开发、接管现有 COORD、部署服务、修改现有概要/批准或正式旧任务状态。

## 纠偏后的分工

- ARCH 实际负责技术任务拆分、技术 `depends_on`、接口边界、源码/文档输入、`write_scope`、`allowed_paths` 及技术验收依据；可复用已有准确、已接受的 ARCH 产物，无须每卡重做设计。
- COORD 引用实际 ARCH 方案/任务拆分登记任务卡，核查前置交付和授权、安排人员/租约/资源先后；不在主会话自行翻业务源码补技术结论，也不通过换角色名称代做正式 ARCH 工作。
- 依赖不明、路径/接口冲突、技术条件缺失时交 ARCH；COORD 不为了让脚本通过自行增删技术依赖或改变路径白名单。资源忙只影响排程，不擅自编码成技术依赖。
- 沿用已有 `read_sources`、`protocol_input`、`dispatch_binding` 等输入引用；登记真实 ARCH Agent/会话、方案版本和位置，不引入新 schema。工程作者接单时核对 ARCH 输入与本卡范围，不以 COORD 口头“已检查”替代。
- 已接受且无实质变化的需求/范围不重复向用户批准；实质变化只提交变化部分。`streamlined-v1` 的单轮独立 QA 不变，不增加每卡重复 ARCH 审查或报告二次复核。

这是职责与执行指令纠偏，不宣称新增了运行时代码拦截、权限隔离或常驻自动规划能力。

## 基线与在途改动

管理仓开工基线为 `5964606826b604da81593ab13d0adecdb7728dc3`，根仓为 `e5b7ec6d80259976b8a38e4164b5596311fed15f`，均使用既定 `main`。本轮实际文档作者为 `/root/arch_boundary_docs`，主助理整理范围和交接；未提交的复杂设计与代码草稿已留存 `/tmp/arch_guard_wip_hold_20261104/`，不作为后续待实施要求。

开工前已有的收件、Debug/921600 概要、确认/intake 文件和前轮 handoff 修改按 [原有文件清单](../evidence/arch_dispatch_guard_20261104/preexisting_files.json) 保留，不顺带提交。本轮发布仅包括明确列出的纠偏文档及其检查记录；根入口与对应规则镜像保持一致。

## 验证与交接

按文档范围检查职责表述、模板和提示词是否一致，确认没有新增合同字段/接口指令或 QA 轮次；检查链接、差异空白、源码未变及既有文件保留情况，并安排一次独立文档审阅。不为纯职责文字修改重跑业务构建、硬件测试或调度器整套回归。交接见 [COORD 接续提示词](../handoff/ARCH_DISPATCH_GUARD_HANDOFF_20261104.md)。实际提交和发布结果待完成后登记。
