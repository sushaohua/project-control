---
task_id: TWIN-54
run_id: codex_qa_01
reviewer_session: 01a1aa5a-e261-7e93-bda3-157643aeb234
decision: REJECTED
scope: handoff-completeness-only
full_hil_approval: false
---

# TWIN-54 独立交接完整性审计

交接完整性不通过。此结论只针对交接包及当前运行态的一致性，不是源码审查或整机HIL验收。仅从用户指定材料和其权威引用取得预期；没有借用开发/集成会话记忆。实际会话与author 7812a1f6-5006-4971-a954-802f855cf20a不同；可核验来源见TWIN-55同run的codex_session.jsonl和read_sources.json。

## 独立核验结果

| 项目 | 结果与物证 |
| --- | --- |
| 四进程/proc/exe SHA256 | 4/4匹配manifest：dbus 73d24dd0…、forward c13a44dc…、device_manager 2a0313ef…、gateway 41824294…；完整64位值见initial_runtime.log及exit_runtime_status.log |
| Web index/app/styles | 源目录及实际static-dir内三资产3/3匹配manifest/SHA256SUMS；额外state文件未封板，不能宣布整个部署100%一致 |
| 串口 | VMware /dev/ttyUSB0由forward独占、921600 8N1；Windows实际COM12/13，PNP映射及采集进程见windows_binding.log；两板UID与manifest精确匹配 |
| 探针 | 双STLink ID匹配；初次MC USART2=0x201C、TH USART1=0x200C；末次MC探针访问有WinUSB阻塞，不能写成始终健康 |
| 固件制品 | 三个本机封存.bin哈希匹配。片上字节一致性未独立证实，读回超时有记录；没有刷写或触碰Bootloader |
| 运行代次 | 当前四PID及启动13:45:52不同于step9日志13:38:28，无对应交接epoch/启动记录；不以哈希相同冒充同一次启动 |

以上实测原件均位于：project-control/docs/evidence/twin/TWIN-55/runs/codex_qa_01/。审计命令、完整哈希和UTC见initial_runtime.log、runtime_unlisted_static.log、action_timeline.jsonl，输入原件逐项SHA见read_sources.json。

## 交接缺陷及缺项

1. ISS-20261105-005：指定总方案不存在，完整冻结全量用例/工具和非作者接受证据缺失。现有确认单已披露覆盖缺口，轻量清单的HANDOFF_READY不能补齐它。290帧/五类复合场景无法在零上下文下准确执行，影响Stage1全量验收。
2. ISS-20261105-006：实际部署多出api/v1/state静态文件（SHA 006b793bb8b86e440a4c9a7f3735c06038968ee3ac025dfef74d39fa979c14b3），持续回GEN=1/OFFLINE；未列配置、文件和新启动代次，实际端点与新采样矛盾。
3. 串口采集接管信息不足：轻量清单只给dual_dbg_logger.ps1名字，没有可直接复用的精确位置/哈希、只追加日志位置/切片与时钟/epoch接口、原始业务帧采集器。审阅者必须从进程枚举和步骤日志反查作者Windows临时目录并读取脚本才完成接管；这些是后续调查所得，不能倒填为交接已提供。
4. 芯片/探针可匹配，但片上固件完整哈希和wire短标识到891a8bb…的接受映射不足；ISS-20261105-016登记TH真实复位后boot_id不变。step5日志只有Finished和标题，未保留完整download --verify实际命令/输出，不能仅凭标题自证Flash字节。TWIN-55任务卡仍引用旧MCU基线016e1236…、candidate/lease/实际QA会话未落地，未由本会话改卡促通过。
5. 初始TH Debug于14:08:02停止更新，MC drop=75/trunc=23；这些现场事实不等于已具备“新鲜健康、零截断”的提测起点。未交代残留作业状态、异常温度、UART恢复及mDNS依赖的接管SOP。

## 接受边界

认可的只是4个运行exe和3个主Web资产哈希匹配、端口与两芯片UID核对事实。不认可完整交接、实际片上固件一致、动态身份、Docker QA或全量HIL通过。TWIN-55另交阶段报告，未以该阶段的局部软件/API现象补签TWIN-54。全部问题保持open，COORD收件后按准确输入/差异补齐再独立复核，保留本报告和历史物证。

[机器可读哈希核验与实际HTTP资产](./handoff_audit_results.json) · [TWIN-55阶段报告](/home/sushaohua/workspace/ai_soc_project/project-control/docs/evidence/twin/TWIN-55/runs/codex_qa_01/stage1_qa_report.md)
