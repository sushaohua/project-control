# 发布命令日志（run_01）

时间：2026-11-04（Asia/Shanghai）  
说明：源码候选为纯文档职责纠偏。以下记录发布命令与结果；`publication/run_01/` 在两个源码候选之后创建，不属于源码候选。

## project-control 候选

工作目录：`/home/sushaohua/workspace/ai_soc_project/project-control`

```text
$ git status --short --branch
## main...origin/main
 M .agents/rules/02_模块与Agent职责.md
 M .agents/rules/04_公共看板与读写协议.md
 M .agents/rules/delivery_and_coord_gate.md
 M .agents/rules/templates/任务卡模板.md
 M .agents/rules/templates/角色任务提示词.md
 M docs/architecture/coord_intake_dispatch_phase1_design_20261103.md
 M docs/evidence/qa_streamline_20261103/handoff_manifest.json
 M docs/handoff/CODEX_ASSISTANT_HANDOFF_20261103.md
 M docs/handoff/HANDOFF_20261104.md
 M docs/planning/qa_streamline_cutover_20261103.md
 ?? docs/evidence/arch_dispatch_guard_20261104/
 ?? docs/evidence/qa_streamline_20261103/coord_receipt_20261104.json
 ?? docs/handoff/ARCH_DISPATCH_GUARD_HANDOFF_20261104.md
 ?? docs/planning/arch_dispatch_guard_20261104.md
 ?? docs/planning/debug_and_921600_merged_implementation_summary_20261104.md
 ?? docs/work_intake/.intake_digests.json
 ?? docs/work_intake/confirmations/CONFIRM-DEBUG-BAUD-20261104.yaml
 ?? docs/work_intake/features/FEAT-20261104-001.yaml
 ?? docs/work_intake/features/FEAT-20261104-002.yaml
 ?? docs/work_intake/submissions/SUB-20261104-001.md
 Exit: 0

$ git diff --quiet -- tools
 Exit: 0
$ git diff --quiet -- README.md tools/coord_runner/README.md
 Exit: 0

$ git add -- <exact nine authorized paths>
 Exit: 0
$ git diff --cached --name-only
 <exact authorized nine paths; scope-set comparison passed>
 Exit: 0
$ git diff --cached --check
 Warning: reports CRLF carriage returns on newly added lines in the two pre-existing CRLF templates; line endings were preserved.
 Exit code was not captured in the command transcript; this warning did not modify content. The staged path-set comparison was separately checked and passed.

$ git commit -m "docs: clarify ARCH and COORD task boundaries"
[main 129ee5dce825f7d57d85afa17d19399428da064d] docs: clarify ARCH and COORD task boundaries
 9 files changed, 141 insertions(+), 12 deletions(-)
 Exit: 0

$ git push origin main
To ssh://192.168.77.113:2222/sushaohua/project-control.git
   5964606..129ee5d  main -> main
 Exit: 0

$ git ls-remote origin refs/heads/main
129ee5dce825f7d57d85afa17d19399428da064d refs/heads/main
 Exit: 0

$ git clone --no-checkout ssh://git@192.168.77.113:2222/sushaohua/project-control.git /tmp/arch_role_correction_pc_fetch_20261104
Cloning into '/tmp/arch_role_correction_pc_fetch_20261104'...
$ git -C /tmp/arch_role_correction_pc_fetch_20261104 rev-parse origin/main
129ee5dce825f7d57d85afa17d19399428da064d
 Exit: 0
```

## 根工作区候选

工作目录：`/home/sushaohua/workspace/ai_soc_project`

```text
$ bash tools/workspace_git.sh status --short --branch
## main...origin/main
 M AGENTS.md
 Exit: 0
$ bash tools/workspace_git.sh diff -- AGENTS.md workspace.json
Diff showed only the ARCH/COORD wording in AGENTS.md and project-control.commit in workspace.json.
 Exit: 0
$ bash tools/workspace_git.sh add -- AGENTS.md workspace.json
 Exit: 0
$ bash tools/workspace_git.sh diff --cached --name-only
AGENTS.md
workspace.json
 Exit: 0
$ bash tools/workspace_git.sh commit -m "docs: sync ARCH task boundary guidance"
[main c0c3336] docs: sync ARCH task boundary guidance
 2 files changed, 6 insertions(+), 5 deletions(-)
 Exit: 0
$ bash tools/workspace_git.sh push origin main
To ssh://192.168.77.113:2222/sushaohua/ai-soc-workspace.git
   e5b7ec6..c0c3336  main -> main
 Exit: 0
```

## 独立审阅快照

```text
$ git clone --branch main --single-branch ssh://git@192.168.77.113:2222/sushaohua/ai-soc-workspace.git /tmp/arch_role_correction_review_20261104/ai-soc-workspace
Exit: 0
$ git clone --branch main --single-branch ssh://git@192.168.77.113:2222/sushaohua/project-control.git /tmp/arch_role_correction_review_20261104/project-control
Exit: 0
```

完整双仓差异、精确 base/current commit、变更文件 SHA-256 和范围说明位于 `/tmp/arch_role_correction_review_20261104/evidence/`。审阅快照两个克隆均已移除写权限。本轮未运行软件构建、业务测试、服务或真实 ARCH 规划作业。
