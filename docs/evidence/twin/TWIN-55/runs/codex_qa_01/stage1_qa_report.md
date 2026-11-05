---
task_id: TWIN-55
run_id: codex_qa_01
reviewer_session: 01a1aa5a-e261-7e93-bda3-157643aeb234
decision: BLOCKED
observed_functional_result: FAIL
stage1_complete: false
approved_scope: []
---

# TWIN-55 Stage 1 独立黑盒QA报告

未完成全量Stage1，不签发任何整机/HIL通过。已执行的浏览器/API/真机观察发现13项问题，登记ISS-20261105-005至ISS-20261105-017，根因保持未知。全量总方案不存在；缺冻结子例、完整QA套件及其非作者复核、原始双向业务帧采集交接。当前会话有实际Session UUID及实时codex_session.jsonl，但没有核实运行时模型和新的服务器Docker物证；本轮按用户禁止重编要求消费既有部署，不把manifest中CTest=true当作本轮Docker接受。

准确版本见read_sources.json和build_manifest；四运行进程SHA与三Web资产SHA匹配。只读制品文件哈希匹配；片上MC应用区读回45秒超时、TH/anchor片上读回未执行。未触碰Bootloader扇区；没有编译或修改业务源码。部分操作脚本本轮新写且未获非作者复核，其结果是可重放观察材料，不能作者自证完整正式接受。

实际操作包括干净profile向导、语言/主题/刷新、预设与保存、真实文件控件正负/恢复、M114只读G-code、两端新温度采样和目标归零、TH USART1与MC USART2故障/精确恢复、浏览器断网/恢复。模型载入触发意外start后立即cancel；保存配置触发意外LOAD/2100目标，随后SELECT恢复DONE、两端目标归零。没有把逻辑坐标、进度和ACK提升为物理动作证明。

## 覆盖矩阵

下表是30个Stage1规格组的核对目录，不是完整冻结子例表。FAIL指已有明确不符合；BLOCKED指输入/前提/完整覆盖不足。所有组complete=false，正例、负例、恢复的细节以action_timeline/CDP/故障日志为准，未执行不计通过。

| 组 | 结果 | 实际范围及缺口 |
| --- | --- | --- |
| BASE-01 | FAIL | 干净profile显示向导；通信/传感器健康前提不成立，断料组却显示正常。 |
| BASE-02 | BLOCKED | 两UID匹配，短版本/完整固件及boot epoch映射不足；初始TH无响应，复位后取得真响应。 |
| BASE-03 | BLOCKED | 语言/主题点击和刷新已执行；English切换生效但刷新回中文。未取得该持久化断言的冻结接受条件，记录观察。 |
| BASE-04 | FAIL | 离线时四路传感器全绿；真实四路触发属于Stage2。 |
| BASE-05 | BLOCKED | 实际点击完成、关闭、刷新、重开已采证；前四步健康前提不满足，不算正常完整向导通过。 |
| BASE-06 | FAIL | 取得顶栏/温度面板和浏览器断网；state静态端点与新采样矛盾。 |
| BASE-07 | BLOCKED | 未执行有真实运动及排险条件的急停/解除；不在未经确认场地启动运动。 |
| BASE-08 | FAIL | 一键载入直接start，已cancel；未交付冻结样例文件及哈希，不签模型内容正确。 |
| BASE-09 | FAIL | 合法/非法扩展名、非法内容/空文件/合法恢复均实际选择；后端负例亦接受。上传上限仍未冻结。 |
| BASE-10 | BLOCKED | 仅观察到模型载入隐式启动，不计正常“开始”用例；缺已冻结安全作业及物理执行依据。 |
| BASE-11 | BLOCKED | 未完成安全真实作业暂停/继续；没有通过进度/ACK替代物理依据。 |
| BASE-12 | BLOCKED | 意外启动后cancel确认为IDLE，保存该局部事实；重复/超时/新作业及实际停止证据不全。 |
| BASE-13 | BLOCKED | 没有安全冻结短作业及最终执行/物理完成依据，未执行。 |
| BASE-14 | BLOCKED | 空间/限位及测量前提未交接；不执行100mm或其他未经确认的运动。负向API清单亦未冻结。 |
| BASE-15 | BLOCKED | 回零限位/安全空间未确认，真实过程及效果留人工窗口。 |
| BASE-16 | BLOCKED | 未交付探针/25点实际测量的自动判据和安全前提，未触发调平。 |
| BASE-17 | FAIL | 合法保存已执行，隐式LOAD；合法SELECT恢复完成；配置持久化正常范围未完整接受。 |
| BASE-18 | BLOCKED | single/dual/quad UI预设已观察，实际供料及保存/刷新全链路未完成；保存有副作用。 |
| BASE-19 | FAIL | UI非法总和提示及合法恢复；API非法总和/通道权重被接受，越界slot/action变504。 |
| BASE-20 | FAIL | 新采样、双端目标0及Debug/API/UI已核对；MC300°C有效性和TH ADC映射失败。无独立热测/PWM测量。 |
| BASE-21 | BLOCKED | 未交接四路自动触发夹具；肉眼/人工逐路动作归Stage2，离线假绿另记FAIL。 |
| BASE-22 | BLOCKED | 网络面板已读；独立VM客户端mDNS解析/访问超时，未核实多播/网段前提，环境阻塞。 |
| BASE-23 | BLOCKED | 健康面板和真实UART故障已观察，24类错误码清单/触发/恢复断言缺冻结输入。 |
| BASE-25 | FAIL | 执行TH USART1与MC USART2故障、精确恢复；3秒退化不符合。真实物理断连/全部子例未完成。 |
| BASE-26 | BLOCKED | 首次/完成后刷新/重开已操作；未重启服务（部署会清日志，精确配置和排他迁移未交接）。 |
| BASE-27 | BLOCKED | 真实Chrome网络断开与恢复有截图/事件；未穷举独立SSE/HTTP/网关服务所有故障层及冻结期限。 |
| J-01 | BLOCKED | 依赖的向导、温度、运动、供料与作业正常路径失败/缺前提，未执行完整旅程。 |
| DELTA-DBG | BLOCKED | 已有双路真实日志和MC污染/截断失败；调试开关/慢采集/满缓冲的冻结步骤及工具未交付。 |
| DELTA-BAUD | BLOCKED | VM端921600 8N1已读；双板有seq>255真实往返和UART故障；未执行冻结的290帧突发/速率不匹配/重启全部子例。 |
| DELTA-COMB | BLOCKED | 正常联合通信有观察且日志缺陷已提；五类复合联动定义缺失，未执行完整批次。 |

## 关键原始证据与限制

- stage1_case_results.json：机器可读组矩阵；action_timeline.jsonl：带case/action/UTC/单调时钟的实际请求和操作。
- browser_cdp_raw.jsonl：真实Chrome CDP与网络/原生alert记录；同名的早期生成截图曾被后续恢复快照覆盖，原始CDP逐事件追加仍在，不能把单张截图当完整前后序列。脚本失败/重试保留在实时会话日志；原生alert阻塞、Windows代理访问失败、429导致工具KeyError均作为采证工具限制，不伪造业务失败。后续试验按独立可核验事件核对。
- mc_debug_raw.log/th_debug_raw.log为已有受控串口采集器文件的真实字节前缀复制；qa_window文件为按初始字节边界截取的未清洗增量。采集器PID22000负责COM12/13@115200；本会话没有争抢串口。完整来源、前缀不变证明、哈希、计数见debug_capture_provenance.json。未保存新的AP双向全Hex采集，不能声称四方证据完整。
- 本轮实际seq最大值见provenance，两端存在seq=260等>255的真实RX/TX及中继；这只证明已观察事务保留16-bit序号，不等于290帧高频突发通过。MC裸ADC污染与trunc增加有本轮证据；drop=75是初始已有，未归因本轮。TH复位后的窗口drop/trunc=0。
- fault_TH_02.log/fault_MC.log：置0/读回/请求/快照/finally精确恢复；fault_TH.log是Windows访问失败后立即恢复的失败采证，未混成通过。fault_MC_cpu.log的0.0%只代表所记2秒单核窗口，不替代BASE-24。
- 时钟通过clock_binding.log及timeline绑定，各主机单调时钟不可直接比较；板上ts分MC/TH和TH复位epoch，不跨epoch错误配seq。
- 初始TH日志冻结且USART1=0x200C，按引用工具恢复0x202C后仍无新采样，TH reset后恢复。当前进程启动晚于交接记录，旧运行物证不能冒充当前epoch。运行短标识/boot_id不等于完整固件字节证明。

## 恢复与收件

精确寄存器恢复已在两次故障日志读回；TH末次只读仍0x202C。MC末次两次核验遇WinUSB错误，最后成功读回0x201C见fault_MC.log，之后未再写MC寄存器。四进程存活且哈希未变；作业IDLE、接口报告heater_duty_percent=0、两端目标归零均有记录。最终链路采样状态以timeline中EXIT-RECOVERY为准，不隐瞒间歇性超时/DEGRADED，也不把NORMAL字样作为温度健康批准。MC探针工具连接仍需现场恢复。

未重启/重建服务来掩盖现场，未强停作者Debug采集器；仅停止本会话专用Chrome和SSH隧道。BASE-24及物理测量/观察清单见stage2_manual_checklist.md。完整Stage1仍需COORD补齐总方案及独立复核套件、准确输入/资源和原始帧采集，再按失败项和未执行项继续，不修改原历史签署。本轮不启动普通子Agent充当独立QA，不更改任务卡、审批或看板。

Issue来源如实为MODEL；现Phase1校验只接受HUMAN，需COORD人工收件处理，具体校验结果另存intake_validation.json。文件生成不表示已被COORD接收、派单或关闭。

## 文件入口

- [逐例与子项JSON](/home/sushaohua/workspace/ai_soc_project/project-control/docs/evidence/twin/TWIN-55/runs/codex_qa_01/stage1_case_results.json)
- [Stage 2人工清单](/home/sushaohua/workspace/ai_soc_project/project-control/docs/evidence/twin/TWIN-55/runs/codex_qa_01/stage2_manual_checklist.md)
- [13项提单汇总](/home/sushaohua/workspace/ai_soc_project/project-control/docs/work_intake/submissions/20261105_twin55_codex_hil_issues.md)
- [收件格式校验](/home/sushaohua/workspace/ai_soc_project/project-control/docs/evidence/twin/TWIN-55/runs/codex_qa_01/intake_validation.json)
