---
review_id: PLAN-CASCADE-RECOVERY-20261027-review-02
reviewer: AI (Codex)
actual_session: /root/cascade_plan_review
candidate_document: project-control/docs/planning/ap_mc_th_cascade_recovery_implementationplan_20261027_162003.md
candidate_version: '1.1'
candidate_sha256: aca5b186e073d9117cbba265be8231c0bb11223e293cfdafbccc096352eb6a5d
decision: APPROVED
scope: independent-document-review-only
review_time_utc: '2026-10-27T08:36:02.854556+00:00'
---

# 独立方案内容复审报告（第二轮）

结论：**APPROVED**，仅接受上述准确 SHA256 的实施方案文档。首轮 R1/R2 已修正；新增 F23～F26 有源码/隔离软件反例依据，并已落实到文件、拟建票、前置接受和验收要求。本结论不表示用户或 MCU Owner 已批准实施，不表示代码/固件被接受、实际部署或真实 HIL 通过；不推进任何正式任务状态。

## 身份、基线与差量范围

实际会话 `/root/cascade_plan_review`，沿用首轮未参与写作的独立审阅者，未委派。首次所读规则、协议及代码基线见 `../plan_review_01/qa_review_report.md` 与 `read_baselines.json`；本轮未重复运行不受并发新提交影响的旧 host 负例或构建。首轮 REJECTED 报告 SHA256 仍为 `a7be7a8be8f447d98fc1e66ace83402c07f9c18e3edf2115ff126264dc185da3`，原件未改。

对比首轮 `reviewed_plan.md` 与 v1.1，差异原件为本 run 的 `candidate_diff.patch`；当前准确文档副本为本 run `reviewed_plan.md`。本轮核对 R1/R2 修正、新 HIL 工具和其独立补审原件、15份归档证据哈希及文档链接。

基线：AP `8d6c446cd3b0bac57054723ba7da9cd797ab4131`、MCU `a679133204ecbb81ad48694f5372c125db2e749f`、控制仓 `8a042927ea0c3b58ea26d3a7b197f5727a1b42fb`。增量为测试仓 `1d0861f199b92f9eac7c2103dfe80b207dbe4838` 与入口 `f5c470e689d4a96e5d71750ced77a5879aa00618`；当前锁文件绑定这组子仓版本。新增工具仅只读源审与 AST 隔离反例，未执行工具本体入口。

## R1/R2 复核

| 首轮问题 | 实际复核与结果 |
| --- | --- |
| R1 双快照/并发增量 | §1.2保留初始A并另列B，解释16:24:52测试仓提交和16:25:23入口提交，以及锁文件/缓存观察所属阶段。Git元数据、差异文件列表、当前锁文件与归档快照吻合。归档文件 st_mtime_ns=`1793089645157975892`，对应16:27:25.157975892+08:00；文档准确称文件落盘时间而非声称全部仓库同时采样。旧static_checks/test_cases未改，新增HIL工具有独立补审和未接受限制。R1关闭。 |
| R2 模式验收缺口 | §6.3新增F22专项，明确UPGRADE中插AP查询/T/迟到文本、不得清/消费升级RX或抢TX/切PERF_TEST、在途DMA交接、超时/拔盘/发送失败后的归还与运行查询恢复，映射CR-05B/D与CR-07；不选升级部署仍须验证查询不越权。R2关闭。 |

## 新增 F23～F26 事实与可执行性

逐读新增独立报告、AST提取反例脚本及输出，并与两个生产工具和指南对应。事先检查反例脚本：它只以AST选取函数、以假依赖替代硬件I/O和sleep，不导入原工具模块或执行CLI，不创建缓存。随后本轮实际运行该隔离脚本；exit0，stdout与归档输出逐字节一致。该退出码表示反例程序执行完成，证明的是**当前工具存在缺陷**，不是修复通过。

- F23：冲突Flash/MSP仍识别MC、重复角色被最后probe覆盖、手工probe不核身份、错误地址/数量返回仍被解析，与源码及反例一致。文件为两个HIL工具，CR-02T要求唯一授权目标和完整读取校验。
- F24：初读失败仍写零、缓存只按role/uart、glitch异常无finally及重复发现目标，与源码及反例一致。CR-02T已要求原状态快照、固定目标/run、恢复事务、finally和无可信快照时拒绝。
- F25：reset-all吞写失败仍报告全恢复、一般写后仅读取未比对目标值，与源码及反例一致。CR-02T已要求返回码、读回核对和部分失败明细。
- F26：指南宣称纳秒/毫秒精确性，控制流含多次发现/CLI/读回；方案将请求等待与实际观测窗口分开，并明确寄存器禁用不等于掉电/物理断线。没有推断未经核查的硅片寄存器、probe实际暂停CPU行为或真实时序。

§4.4列两个工具、HIL指南、README及新增隔离测试路径；§5给CR-02T的拆票阶段、前置、独立Codex复核，并阻止未接受工具进入CR-09/10；§6.3覆盖身份冲突、读取失败、写失败、读回不符、中断/负时长、跨设备/run缓存与枚举变化。CR-02T未要求最终HIL先通过，未新增循环依赖。生产协议、历史签署和双固件最终出口未改变。

## 哈希、链接与实际命令

15份副本逐项校验清单 SHA256，并读取清单指定原始 `/tmp` 文件作一致性对照；**15/15副本和原件均匹配**。原始结果为 `hash_check.json`。6个方案 Markdown 链接均有目标，结果为 `links_check.json`。首轮报告哈希复核一致。

所有命令 cwd 为 `/home/sushaohua/workspace/ai_soc_project`，每条子命令独立捕获stdout/stderr和退出码；没有用外层脚本退出0替代子命令结果。

| 命令/检查 | 退出码/记录 |
| --- | --- |
| `cat`新HIL补审报告、AST反例脚本、归档输出、两个工具及指南 | 6条均0；准确参数在 `read_commands.json`，全文为 `new_scope_0.txt`～`new_scope_5.txt` |
| `python3 -B project-control/docs/evidence/cascade_recovery_plan_20261027/hil_tools/cascade_new_hil_tools_repro_20261027.py` | 0；输出 `verify_0.txt`，字节匹配归档反例输出 |
| `git -C test_harness log -2 --format=%H %cI %s` | 0；`verify_1.txt` |
| `git -C test_harness diff --name-only 5a2ebe49e26ffb76a55ab74de652142ce9961de7 1d0861f199b92f9eac7c2103dfe80b207dbe4838` | 0；`verify_2.txt` |
| `git -C test_harness status --short --branch` | 0；`verify_3.txt` |
| `bash tools/workspace_git.sh log -2 --format=%H %cI %s` | 0；`verify_4.txt` |
| `cat workspace.json` | 0；`verify_5.txt` |
| Python标准库difflib/hashlib/stat/路径检查 | 0；`candidate_diff.patch`、`candidate.sha256`、`hash_check.json`、`links_check.json`、`verification_summary.json` |

完整子命令/cwd/退出码索引为 `verify_commands.json`。读取/校验脚本只写本run目录；没有改方案、业务源码、正式任务状态、历史报告或软链目标，没有遍历工作区外目录。对清单明确指定的临时证据原件仅作逐项读取。

## 未执行项与接受限制

未执行真实硬件工具入口、probe-rs、设备发现、串口、刷写/复位、网络或push；未构建AP/MC/TH，未重跑旧CTest/PTY负例。没有验证真实寄存器地址、UID来源、SWD对CPU影响、物理恢复及时序，后续必须按准确任务和HW-G门禁独立核查。新HIL工具当前仍不可作为已接受夹具使用，本次通过的是指出这些缺陷并约束修复/验证的方案文档。

后续若方案内容改变，本报告不自动接受新哈希；QA报告的后续独立复核和唯一COORD收件/正式状态更新仍按canonical政策执行。
