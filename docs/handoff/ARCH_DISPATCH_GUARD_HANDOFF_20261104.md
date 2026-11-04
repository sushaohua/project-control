---
title: ARCH 与 COORD 职责纠偏及开发接续
revision: 2
date: 2026-11-04
status: published-documentation-correction
qa_policy: streamlined-v1
---

# ARCH 与 COORD 职责纠偏交接

本轮按用户“仅仅纠偏”的要求，只调整职责规则、已有派单模板和接续提示词，见 [纠偏记录](../planning/arch_dispatch_guard_20261104.md)。Runner 等运行代码的未提交扩展已撤回，不新增合同协议、自动 ARCH 路由、权限/阶段锁改造；未启动业务开发、业务测试、烧录或服务。

**ARCH 实际提供技术方案与任务拆分；COORD 引用并登记、核开工条件、安排执行和收件。** 主会话已指定为 COORD 时，不再借“主对话分阶段讨论”自行代做 ARCH 的技术依赖/路径分析。技术问题交 ARCH 修订，不为通过检查擅改字段；现有准确 ARCH 输入可复用，不要求每卡重复设计。

已有用户批准且范围未变的内容继续引用；实际批准来源的登记由 COORD 按既有规则完成，不改现有概要正文或哈希以伪造批准。简化 QA 沿用 `streamlined-v1`，不加重复 ARCH 审查或报告复核。现有代码的能力和限制保持原样，本次文档修正不冒充程序强制封锁。

## 给 COORD 的接续提示词

```text
你继续担任唯一COORD。先读取：
project-control/docs/handoff/ARCH_DISPATCH_GUARD_HANDOFF_20261104.md
以及其中引用的纠偏记录和更新后的职责/派单规则。

先核实当前实际Agent、在途任务和写入占用，保留已有修改。
实际委派ARCH接管复核Debug/921600概要的技术部分，完成任务拆分、技术依赖、
接口边界、输入版本、路径白名单和验收依据；已有准确ARCH产物直接引用。
记录实际ARCH执行者、方案位置和版本；你根据这些输入登记任务卡、
核查前置接受与授权、安排资源和执行者，不自行翻业务源码补技术结论。
检查发现技术依赖/路径/接口问题就交ARCH修订，不为通过脚本自行增删字段。

沿用我已经给出的准确有效批准；未发生产品或范围实质变化，不重新批准整单。
在现有授权、ARCH输入及开工条件齐全后，派对应ENG/INTEGRATOR启动开发。
工程作者接单时核对ARCH输入与本卡范围，例行技术细节由团队处理。
保持现有streamlined-v1单轮独立QA，不加重复ARCH审查或逐份报告复核。
完整真机QA仍等Debug与921600两项交付后由你发起；授权人员确认并烧录后进入自动测试。
沿用已确认的四项QA选择，Bootloader与硬件操作继续遵守原授权边界。
```

## 发布与独立审阅回执

- `project-control`：`129ee5dce825f7d57d85afa17d19399428da064d`，`main`，已推送；根工作区 `workspace.json` 已 pin 此源码候选。
- 根工作区：`c0c3336d1f5a09c955ceddf1bf6c6b71484ada63`，`main`，已推送。
- 独立文档审阅：会话 `01a1a44c-ca56-7b72-9241-2b2d0dab38e6`（`gpt-6-luna`，只读），`APPROVED`，无 findings。审阅证据见 [run_01 索引](../evidence/arch_dispatch_guard_20261104/reviews/run_01/evidence_index.json)。该结果不代表软件/硬件测试。

发布命令和完整差异清单见 [publication run_01](../evidence/arch_dispatch_guard_20261104/publication/run_01/candidate.json)。这次仍是职责与执行指令纠偏，没有运行代码、改变现有 QA 策略或声称新增运行时拦截。
