---
schema_version: 1
submission_id: SUB-EXAMPLE-001
revision: 1
example_only: true
enabled: false
reported_by:
  actor_type: HUMAN
  actor_id: example_author
  source_channel: markdown_submission
---

# 三类人工指令混合批次示例（默认禁用，不触发任何执行）

## 公共约束
- 示例文件默认 `enabled: false`，不携带任何业务或代码修改授权
- 一条指令固定映射一条稳定需求，由程序自动生成唯一主分类 YAML

## 指令列表
1. [issue] 队列状态投影在空检查点文件异常时提示信息不够直观，需核查原因（根因待查）
2. [feature] 在 `project-control` 收件报告中补充按需求分组的任务汇总表展示
3. [requirement] 多批次需求合并确认时的展示粒度待澄清，请 PM 与 ARCH 先给出边界建议
