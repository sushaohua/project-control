---
review_id: PLAN-CASCADE-RECOVERY-20261027-review-01
reviewer: AI (Codex)
actual_session: /root/cascade_plan_review
candidate_document: project-control/docs/planning/ap_mc_th_cascade_recovery_implementationplan_20261027_162003.md
candidate_version: '1.0'
candidate_sha256: 154cb4f72b120e3af8c1faff4088585ac2bd5072b002e62102cc76f9a31d74ea
decision: REJECTED
scope: independent-document-review-only
review_time_utc: '2026-10-27T08:31:56.340460+00:00'
---

# 独立方案审查报告（首轮，保留原件）

结论：**REJECTED**。方案的主要纠偏方向、协议约束和分阶段出口有源码/记录依据；下述两项局部问题修正后需要对新候选重新审查。本结论只针对该准确哈希的文档可接受性，不是用户实施批准，不是源码、固件、部署或真实 HIL 通过，不改变任何正式卡片或历史签署。

## 身份与范围

实际审阅会话为 `/root/cascade_plan_review`，未参与方案写作，未委派，未修业务源码、任务状态、方案或既有报告。唯一写入位置为本 run。`reviewed_plan.md` 是本次准确受审文档副本，不是方案新原件。

已读根 `AGENTS.md`、canonical `project-control/.agents/rules/codex_qa_review.md`、`project-control/manifest.yaml`、通过既有软链读取的 `mcu-p3/AGENTS.md`、正式协议及 `soc-ap/contracts/minimcproto/v2-commands.md`。各原件 SHA256 见 `read_baselines.json`。未跳出 MCU 软链目标探查宿主其他目录。证据清单明确给出的 `/tmp` 原件逐项读取校验，未遍历其他临时目录。

受审文档开始快照列 root `9cf4f7c281345941904e042b5ae7494fdccda1a7`、控制仓 `8a042927ea0c3b58ea26d3a7b197f5727a1b42fb`、AP `8d6c446cd3b0bac57054723ba7da9cd797ab4131`、MCU `a679133204ecbb81ad48694f5372c125db2e749f`、测试仓 `5a2ebe49e26ffb76a55ab74de652142ce9961de7`；归档 `repository_snapshot.json` 列测试仓 `1d0861f199b92f9eac7c2103dfe80b207dbe4838`。核查时当前 root 为 `f5c470e689d4a96e5d71750ced77a5879aa00618`，测试仓为 `1d0861f199b92f9eac7c2103dfe80b207dbe4838`。这些差异的判断见 R1。

## 必须修正的问题

### R1：开始快照与归档/当前恢复锁缺少时间及变更影响说明

位置：方案 §1.2、证据 `repository_snapshot.json`，以及 §7.4/9 的本轮范围说明。

§1.2 表明确为“审查开始时”，因此不能仅因之后 HEAD 前进就判前述审查无效。但紧随的“本次 workspace.json 已绑定上述四个子仓提交”没有限定采样时间，读者会将它与归档快照理解为同一状态。当前锁文件已经绑定 `1d0861f...`，缓存状态也由早先有缓存变成当前干净。

`focus_0.txt` 证明测试仓新提交时间为 2026-10-27 16:24:52+08:00，变更 `.gitignore`、README、新 HIL 指南及两个 HIL 工具；`focus_1.txt` 证明旧 `static_checks/` 和 `test_cases/` 未变。`policy_0.txt` 证明 root 在 16:25:23 更新恢复锁。因此这是**并发推进且新 HIL 范围尚需纳入说明**，不能表述为原 host 测试已自动失效，也不能将新工具默认为已经接受。

最小修复：保留开始快照，并另记归档/当前采样时间和 root/test_harness 新 SHA，限定锁文件/缓存陈述属于哪个时间点；说明变更范围及新 HIL 工具当前未执行/待独立检查或其新增审查证据。无需回退或修改他人提交，也无需重跑不受影响的旧 host 负例。

### R2：F22 模式所有权缺少明确验收反例与退出条件

位置：方案 F22、§3.2、§4.3、§6.3；MCU 独立报告 §6。

文件和修复责任已经列出，但 §6.3 的“并发发送”及升级 ACK/文件反例没有明确检查：升级正在占有 USART6 时，AP 查询或调试 T 入口能否清掉升级 RX 标志；已有 TX DMA 时如何切模式；升级超时后是否能释放所有权并恢复运行查询。这些入口恰是本轮发现的风险，不能仅凭正常只读查询和文件预检通过来关闭。

源码对应：`minimc_proto.c` 的 `handle_th_query` 无模式校验即清共享完成标志；`wk_usart.c` 的 mode_set 直接赋值；升级发送与 perf 入口另有模式行为。该事实由 `source_1.txt`、`focus_2.txt`、`focus_4.txt` 和 MCU原报告支持；本轮没有实机重现字节交织。

最小修复：在 §6.3 补一组模式反例，并映射 CR-05B/D 与部署相关 CR-07：UPGRADE 中注入 AP 查询/调试入口须明确拒绝或延后，不能清升级事件/插入运行字节；有在途 DMA 时切换按冻结契约排空/拒绝；超时/失败退出后允许正常查询恢复。若不选中继升级部署，说明应隔离/禁用不受支持入口并验证它不会破坏当前运行。这里只要求补明验收要求，不要求本轮执行硬件或扩成全 OTA。

## 已核对且未发现阻断的部分

- 正式协议 SHA256 与方案元数据一致；GET_VERSION/REPORT 的 0x01→0x02、L0→L16，PING/PONG 的 0x03→0x04、L4→L12 与正式契约一致。Hop>1、递减、routed、重算 CRC 未私自改变既有协议。
- AP 默认错误命令/载荷、任意完整帧即成功、无条件成功退出、发送无 deadline、baud 回退等描述可由所读源码和归档 host 原件支持。未将帧层 parser 的无业务分发本身判缺陷。
- USART2 IRQ→gui_rx_callback→解析→TH 忙等，及 USART2/6 同抢占级2、DMA先重启后消费同槽，均可由源码对应；方案明确这是源码推导而非实机复现。
- 升级调用者 ACK[8] 与下层容量32的静态容量错配确实存在；方案未声称实际已触发板上溢出。
- 当前 task graph 实跑 exit 1，61卡/20个V2，MS-07 YAML 冒号错误和附带缺引用与方案一致。卡片自审、空签署、旧代理转译等问题有原件支持。
- 12 项归档副本均同时匹配清单 SHA256 和对应 `/tmp` 原件；结果见 `hash_check.json`。方案6个 Markdown 链接全部有目标，见 `links_check.json`。
- 现有命令契约、独立预期→三端实现→准确组合→工程联调→独立HIL→COORD接受的主顺序未发现必须靠最终HIL先通过才能准备候选的循环。CR-03用于前置门禁的解释为其A～D工具阶段；实例化时仍应填精确票ID。
- F01～F21 均已有相应文件/票及验证或明确的契约冻结步骤。保留历史原件、另建撤回记录，独立Codex及QA作者复核要求，软链迁移前不覆盖外部目标，最小差异/回退等边界符合本次任务。

## 实际命令、退出码与原始记录

全部命令 cwd 为 `/home/sushaohua/workspace/ai_soc_project`。多命令均由 Python subprocess 分别捕获实际 stdout/stderr 与退出码，没有用外层 Python exit0 替代子命令结果。命令清单及完整输出在本 run：

| 清单/原件 | 实际操作 | 实际退出结果 |
| --- | --- | --- |
| `initial_0.txt`～`initial_4.txt` | cat证据README/清单/快照/manifest，sed方案文件清单 | 每条0；首次打印的准确参数保留在实际工具事件 |
| `baseline_commands.json` | git测试仓log/status、cat锁文件/MCU规则/三份独立报告、sed方案 | 每条0；原始输出 `baseline_*.txt` |
| `source_commands.json` | sed命令契约/AP主程序/transport/MC原生协议/方案 | 每条0；原始输出 `source_*.txt` |
| `focus_commands.json` | git show/diff新测试仓提交；sed升级/串口/配置源码 | 每条0；原始输出 `focus_*.txt` |
| `workflow_commands.json` | task graph实际检查；git入口读取；cat MS-07/MS-14/MCQ-0106 | task graph=1；直接root git两条=128；其他=0 |
| `policy_commands.json` | 按仓库要求用workspace_git.sh读取入口历史；重读AGENTS和QA规则 | 每条0；原始输出 `policy_*.txt` |
| `hash_check.json` | Python hashlib核对12项证据副本与原件 | 12/12 copy_match/source_match为true，脚本0 |
| `links_check.json`、`protocol_extract.txt`、`irq_extract.txt` | Python只读链接存在性、协议哈希/路由、IRQ调用链摘录 | 脚本0；所有Markdown链接存在 |

直接root git的128原始错误为无法使用受保护.git gitdir；已改用仓库规定wrapper成功，未申请扩大权限。初始读取与后续捕获重复发生，首次读取只存在工具原始事件；本run另存了完整受审方案和规则便于复核。没有把未保存的初次8例stdout再造为“本次运行日志”。

## 未执行与限制

未运行AP/MC/TH构建、CTest、PTY负例、系统调用注入或隔离task graph反例；本次仅核对前述独立会话原件及只读源码/结构检查。未执行新HIL工具、设备发现、探针操作、串口打开、刷写/复位、网络、push及实机性能采集。未重新签署历史任务或证明现有Bootloader行为。文档接受后仍需用户实施批准和所有适用工程/硬件门禁。

作者修复后必须新候选哈希、新审查run；本REJECTED报告不覆盖或改成APPROVED。
