# 独立 ARCH 复核：REJECTED

- **所复核 QA 报告 SHA256：**`9157a0a8093f977fba1ce3c6126d7a91e153b2ada08bcf80888563e72f30da76`，与指定值一致。
- **候选 commit：**`5b27106a08212b7d1e5d0f3be615a9f600d930e7`，当前 `HEAD` 与指定提交一致。

## 实际核查

只读检查了三份规划文档及其 PM 目录、PL-01、两阶段方案、任务卡等引用材料。报告对 44 项分期计数、七项首版子范围、TASK-011 与 TEMP/TWIN 状态的描述有文档依据；它也正确区分了产品决定、文档审查、代码实现和硬件验收。报告把本地打印目标后续需求拆解列为建议，没有把未实现功能当作文档阻断。

未执行构建或自动化测试，未修改文件。工作区状态干净。

## 问题

报告称三份文档的相对 Markdown 链接“未发现失效链接”。我在本次指定的独立检出中抽查到 **52 个常规相对 Markdown 链接，其中 3 个目标不存在**：

- [产品功能到任务对照表](/tmp/release-scope-qa-iplc2_px/project-control/docs/planning/product/product_feature_task_traceability_20261029.md) 指向的 TEMP-06 实际记录 `docs/evidence/temperature_increment/TEMP-06/runs/run_01/result.md` 不存在。
- [SoC 架构输入登记](/tmp/release-scope-qa-iplc2_px/project-control/docs/planning/soc_system_architecture_input_register_20261029.md) 指向 `soc-ap/core/host/main.cpp` 和 `soc-ap/core/host/query.h`；该候选检出中没有这些文件，也没有相邻的 `soc-ap` 目录。

第一处使 TEMP-06 验收证据入口无法从候选文档复核；后两处也使源码依据无法在本检出中核对。因此，“未发现失效链接”的报告结论与本次检查结果不符，是拒绝该 QA 报告的理由。

## 限制

源码候选仅包含 `project-control` 独立检出；两个 SoC 源码链接是否能在其他工作区布局中解析，无法从本候选确认。以上结论仅针对这份 QA 报告及指定候选；未复核行政回执，也未要求递归复核。