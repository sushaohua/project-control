# project-control 仓库规则入口

本仓维护跨仓需求、规则、契约、任务及调度/验收工具。先核对实际仓库、分支、工作树和本轮授权；只读规划可以并行，工程写入按已批准范围执行，保留其他任务的改动。

开始任务先读取：

- `.agents/rules/repository_rule_boundaries.md`：公共规则、本仓规则、环境与授权的适用边界。
- `.agents/rules/repository_rule_sources.json`：各仓规则入口和分发方式。
- 涉及派单/验收：`.agents/rules/delivery_and_coord_gate.md`、`.agents/rules/codex_qa_review.md`；按任务实际需要读取相关职责、模板及输入。
- 涉及代码：`.agents/rules/code_documentation_standard.md` 及适用语言规范；`tools/` 的 Python Runner、检查器和脚本同样遵守中文注释要求。

本仓 `.agents/rules/` 是项目跨仓公共规则的唯一权威原件，不再向业务代码仓复制 `shared/` 或 `.repo-rules/` 快照。各业务仓专属的 `AGENTS.md`、`.agents/rules/` 与 `.agents/skills/` 统一独立存放在 `agents/` 仓库中。

用户当前明确指令优先；已批准且范围未变的授权可复用。技术冲突交 ARCH/相应 Owner，授权及产品范围冲突交用户，不以晚读到的规则或简单“取最严”代替冲突裁决。

COORD 登记技术输入、前置条件、执行者和资源；ARCH 实际交付技术拆分、接口、依赖和路径范围。COORD 不代做业务实现；工程角色只写获授权仓库和路径。不得借本仓工具取得业务仓、Bootloader 或物理设备的额外权限。

正式 QA 按当前任务的有效 `qa_policy`、独立会话、服务器准确候选和软件/HIL 范围执行；不要把模型/计划别名、文件存在或静态检查通过写成实际接受。未经实际部署不声称 Runner 或 HIL 服务在运行。

每次派单在现有 `read_sources` 和接单回执列明目标仓入口、相关规则、共享快照来源提交及任务输入。独立检出核对这些必需文件确实随候选取得；缺少当前工作必需的规则或材料则阻塞对应部分，不静默省略。

过程文档按任务另行提供；本轮规则分发不打包或迁移 `docs/`，不替换已有 MCU/Bootloader 链接，不改写历史任务与签署。
