---
title: 产品功能目录知识库同步登记
date: 2026-10-28
timezone: 北京时间（UTC+8）
status: source-snapshot-imported
---

# 产品功能目录知识库同步登记

2026-10-28 将下列知识库原件复制到项目控制仓。导入时目标 SHA256 与源文件一致；随后根据 SOC 原件开头的“73 项”及映射表、修订说明，把末尾两处滞后的“69 项”改为“73 项”。源文件保持不变，项目工作以本地副本为输入；知识库后续变化不会自动同步。SOC 文件仍是本地候选目录的唯一维护原件，知识库副本仅作为本次导入来源。

| 文档 | 知识库源文件 | 源文档更新时间 | 项目内副本 | SHA256 | 用途/状态 |
| --- | --- | --- | --- | --- | --- |
| PM 全景产品功能目录 | `/mnt/d/AI_RDdocs/full_color_3d_printer_feature_catalog_baseline.md` | 2026-10-27 09:33:00 | `docs/planning/product/full_color_3d_printer_feature_catalog_baseline.md` | `f97580f464eb477d02a2c00ca1ac5c6080066f886ed8be45eee30133e631c435` | 44 项产品目标输入；指标、SKU 与范围逐项接受，不代表已实现。 |
| SOC 全产品候选功能目录 | `/mnt/d/AI_RDdocs/AI_SoC_协作方案/product_feature_catalog_baseline.md` | 2026-10-27 09:34:00 | `docs/planning/product/product_feature_catalog_baseline.md` | 源 `1c678cdca279411cbb233061b89ff5f893c631fc6b8b7ef3fabf83ffdc650909`；本地校正后 `40be1a328f796e357bc6aa26ba3a5ec81b3cfc4eff144d97f416bea84b341107` | 73 项候选（含新增 4 项）及 PM 映射；仍为 Draft/Open，不代表产品批准。 |


B0 的对应入口和数量已同步；PL-01、PL-02、TASK-001 已绑定新输入版本并修正旧数量及知识库回链。原始知识库文件未修改。任务状态、产品批准、实现与验收状态均未改变；新增候选不自动扩大已选范围。
