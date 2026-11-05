---
submission_id: 20261105_twin55_codex_hil_issues
revision: 1
enabled: true
reported_by:
  actor_type: MODEL
  actor_id: 01a1aa5a-e261-7e93-bda3-157643aeb234
  source_channel: independent_codex_qa
---

# TWIN-55 独立黑盒提单汇总

## 公共约束

只登记本轮实际观察；不修改业务仓、不重编译、不擦写Bootloader、不关闭Issue；根因由Owner调查。BASE-24和物理观察留Stage2。

本单来自用户明确授权的独立Codex QA，不是人工逐项实测签署。现Phase1收件器只接受HUMAN（work_intake.py）；如实保留MODEL，需唯一COORD人工收取/裁决该入口限制，不能伪造身份促通过。尚未扫描、派单或关闭。

正式验收：BLOCKED；已取得的黑盒不符合见各单；Stage1未完整执行，未批准。

## 指令 1

【问题】全量验收总方案缺失，未提供冻结子例及经非作者复核的完整自动化套件

**记录：** `ISS-20261105-005`；用例：HANDOFF, J-01, DELTA-BAUD, DELTA-COMB；建议优先级：P1；建议Owner：QA（待COORD核定）。

**期望：** TWIN-55依赖条款要求消费封存交接单及经非作者独立复核的QA工具；本轮用户指定全量总方案为唯一验收输入。

**观察：** docs/planning/hil_full_acceptance_master_plan_20261105.md不存在。引用的BASE文档revision 4自称草案，T_probe等未绑定；未取得290帧的原始向量/速率/成功准则、五类复合联动的逐例定义和完整套件复核证据。已异步询问正确路径，未收到补充。确认单§3也已披露工具覆盖缺口。

**复现：** 读取用户指定总方案路径，得到ENOENT。 → 核对TWIN-55 dependency_conditions、BASE草案§1/3/4及确认单§3；无法据此枚举冻结全量子例。

**证据：** `project-control/docs/evidence/twin/TWIN-55/runs/codex_qa_01/read_sources.json`

## 指令 2

【问题】运行态含未封板的静态state端点，且当前启动代次未交接

**记录：** `ISS-20261105-006`；用例：HANDOFF, BASE-02, BASE-06；建议优先级：P1；建议Owner：INTEGRATOR（待COORD核定）。

**期望：** 提测交接应覆盖实际部署配置、静态资产及运行身份；实时状态不得由旧缓存冒充。

**观察：** 四进程/三静态资产哈希匹配；但当前PID为1676003/1676008/1676009/1676011，启动13:45:52，晚于交接日志13:38:28。网关实际static-dir=/tmp/aisoc_twin_logs/web_root，其中另有未列入manifest/SHA256SUMS的api/v1/state文件，SHA256=006b793bb8b86e440a4c9a7f3735c06038968ee3ac025dfef74d39fa979c14b3。HTTP /api/v1/state持续返回GEN=1、OFFLINE；真实采样快照已推进并可返回NORMAL。此静态文件返回的Content-Type为application/octet-stream。

**复现：** 核对/proc/<pid>/exe、命令行及进程启动时刻。 → 完成一次新采样后比较GET /api/v1/state与GET /api/v1/temperature/snapshot。 → 核对实际static-dir内api/v1/state的字节及哈希。

**证据：** `project-control/docs/evidence/twin/TWIN-55/runs/codex_qa_01/initial_runtime.log`、`project-control/docs/evidence/twin/TWIN-55/runs/codex_qa_01/runtime_unlisted_static.log`、`project-control/docs/evidence/twin/TWIN-55/runs/codex_qa_01/action_timeline.jsonl`

## 指令 3

【问题】保存料槽配置隐式发起LOAD并附带210°C目标

**记录：** `ISS-20261105-007`；用例：BASE-17, BASE-18；建议优先级：P1；建议Owner：ENG-UI（待COORD核定）。

**期望：** 手册功能5配置保存和BASE-17要求保存配置；进丝是独立物理动作，不能以保存配置替代用户确认的动作。

**观察：** 真实鼠标点击“保存料槽映射配置”后，浏览器发POST /api/v1/filament/slots，body含active_slot=1、action=1、target_temp_deci_c=2100。TH随后出现op=LOAD、step_state=FEEDING；用户没有点击进丝。未测量实际位移，不能声称已经出料。已改为SELECT恢复DONE并将两端温度目标归零；占空比接口报告0。

**复现：** 选择合法single-1预设。 → 在新鲜采样窗口点击“保存料槽映射配置”。 → 检查CDP请求及TH Debug，比较保存前后的动作状态。

**证据：** `project-control/docs/evidence/twin/TWIN-55/runs/codex_qa_01/BASE-17-fresh-save.txt`、`project-control/docs/evidence/twin/TWIN-55/runs/codex_qa_01/browser_cdp_raw.jsonl`、`project-control/docs/evidence/twin/TWIN-55/runs/codex_qa_01/th_debug_qa_window.log`、`project-control/docs/evidence/twin/TWIN-55/runs/codex_qa_01/SAFETY-target-zero.txt`

## 指令 4

【问题】模型一键载入直接启动作业

**记录：** `ISS-20261105-008`；用例：BASE-08, BASE-10；建议优先级：P1；建议Owner：ENG-UI（待COORD核定）。

**期望：** 手册功能3区分模型载入与点击“开始打印”；BASE-08只加载，BASE-10独立开始。

**观察：** 仅点击CalibrationCube.gcode“一键载入”，CDP即记录POST /api/v1/jobs/start {"model":"CalibrationCube.gcode"}，界面进入PRINTING、Layer 1/100、1.0%。没有点击开始打印。发现后立即调用cancel，回到IDLE。未把进度或逻辑坐标认定为物理动作。

**复现：** 取得新鲜采样并进入打印工作台。 → 只点击CalibrationCube的一键载入。 → 检查网络请求和作业状态，随后取消。

**证据：** `project-control/docs/evidence/twin/TWIN-55/runs/codex_qa_01/BASE-08-fresh-cube.txt`、`project-control/docs/evidence/twin/TWIN-55/runs/codex_qa_01/BASE-08-fresh-cube.png`、`project-control/docs/evidence/twin/TWIN-55/runs/codex_qa_01/browser_cdp_raw.jsonl`、`project-control/docs/evidence/twin/TWIN-55/runs/codex_qa_01/action_timeline.jsonl`

## 指令 5

【问题】上传入口接受非法扩展名、非G-code内容和空文件

**记录：** `ISS-20261105-009`；用例：BASE-09；建议优先级：P1；建议Owner：ENG-UI（待COORD核定）。

**期望：** BASE-09要求非法格式/空文件拒绝，合法文件可恢复。

**观察：** 真实Chrome文件控件先后选择valid.gcode(M114换行)、invalid.txt(非G-code文本)、invalid.gcode(同一非G-code文本)、empty.gcode(0字节)、valid.gcode。CDP原生alert均宣称“上传装载成功”；HTTP只提交name/size。补充公开API负例invalid.txt size=19与empty.gcode size=0均200 Upload staged。未启动这些上传文件。

**复现：** 使用本run存档的四个fixture，通过文件输入选择，保留真实文件SHA256。 → 检查CDP请求、原生alert和HTTP返回。 → 以合法valid.gcode重试作为恢复。

**证据：** `project-control/docs/evidence/twin/TWIN-55/runs/codex_qa_01/browser_cdp_raw.jsonl`、`project-control/docs/evidence/twin/TWIN-55/runs/codex_qa_01/action_timeline.jsonl`、`project-control/docs/evidence/twin/TWIN-55/runs/codex_qa_01/invalid.txt`、`project-control/docs/evidence/twin/TWIN-55/runs/codex_qa_01/invalid.gcode`、`project-control/docs/evidence/twin/TWIN-55/runs/codex_qa_01/empty.gcode`、`project-control/docs/evidence/twin/TWIN-55/runs/codex_qa_01/valid.gcode`

## 指令 6

【问题】料槽API未拒绝非法权重，越界动作进入硬件NACK路径

**记录：** `ISS-20261105-010`；用例：BASE-19；建议优先级：P1；建议Owner：ENG-UI（待COORD核定）。

**期望：** BASE-19要求非10000、负数、非数及越界按契约拒绝；纯UI校验不覆盖后端准入。

**观察：** 有NORMAL新快照前提时，total_mixing_weight=9999返回200；两个通道权重为-1/10001、总和仍10000时也200 Filament slots updated。slot_id/active_slot=5及action=-1得到504 RPC timeout or NACK，未在API入口报告参数非法。早期503结果保留，不计为参数负例通过。合法SELECT/action=0/目标0恢复得到200。

**复现：** 以本轮浏览器实际POST配置为基准，固定action=0、target_temp_deci_c=0。 → 取得新鲜NORMAL快照后分别修改总和、通道权重、slot_id、action。 → 检查HTTP与双路Debug；以合法SELECT恢复。

**证据：** `project-control/docs/evidence/twin/TWIN-55/runs/codex_qa_01/action_timeline.jsonl`、`project-control/docs/evidence/twin/TWIN-55/runs/codex_qa_01/mc_debug_qa_window.log`、`project-control/docs/evidence/twin/TWIN-55/runs/codex_qa_01/th_debug_qa_window.log`

## 指令 7

【问题】MC热床300.0°C被当作正常新鲜温度

**记录：** `ISS-20261105-011`；用例：BASE-04, BASE-20；建议优先级：P1；建议Owner：ENG-MC（待COORD核定）。

**期望：** BASE-20要求温度有效性真实；OOBE明确标注热床有效范围5~130°C，工程门禁要求无效温度降级。

**观察：** MC Debug持续bed_ddC=3000；转发日志temp_millic=300000；快照bed.temperature_c=300.0、sensor_status=OK、quality=FRESH，组合system_status可为NORMAL，HMI显示300.0°C。仅凭这些证据不能判断真实热敏电阻、接线或算法根因，也不称其已经证实是伪造物理温度。

**复现：** 只做POST /api/v1/temperature/sample，不施加任何非零加热目标。 → 关联MC Debug、转发日志、快照与HMI热床显示。

**证据：** `project-control/docs/evidence/twin/TWIN-55/runs/codex_qa_01/action_timeline.jsonl`、`project-control/docs/evidence/twin/TWIN-55/runs/codex_qa_01/final_forward_service.log`、`project-control/docs/evidence/twin/TWIN-55/runs/codex_qa_01/mc_debug_qa_window.log`、`project-control/docs/evidence/twin/TWIN-55/runs/codex_qa_01/BASE-08-fresh-cube.txt`、`project-control/docs/evidence/twin/TWIN-55/runs/codex_qa_01/BASE-04-sensors.txt`

## 指令 8

【问题】TH真实ADC未映射到公开快照及HMI

**记录：** `ISS-20261105-012`；用例：BASE-20；建议优先级：P2；建议Owner：ENG-UI（待COORD核定）。

**期望：** 引用整改方案HIL-01和BASE-20要求同采样ADC原始值、温度及有效性对账。

**观察：** TH本轮Debug有adc_raw约1900~2100且fault=0、真实采样TX；公开temperature/snapshot只有temperature/sensor_status/quality等字段，没有raw_adc映射，温度面板ADC读数显示0。截图保存了新采样后界面及目标0恢复。这里报告映射缺失，不断言真实ADC为0。

**复现：** 进入温度面板，执行本次新采样。 → 将TH RX/STATE/TX采样与HTTP快照及面板ADC对应比较。

**证据：** `project-control/docs/evidence/twin/TWIN-55/runs/codex_qa_01/SAFETY-target-zero.txt`、`project-control/docs/evidence/twin/TWIN-55/runs/codex_qa_01/SAFETY-target-zero.png`、`project-control/docs/evidence/twin/TWIN-55/runs/codex_qa_01/th_debug_qa_window.log`、`project-control/docs/evidence/twin/TWIN-55/runs/codex_qa_01/action_timeline.jsonl`

## 指令 9

【问题】设备离线时OOBE仍将四路断料传感器标为正常

**记录：** `ISS-20261105-013`；用例：BASE-01, BASE-04, BASE-21；建议优先级：P1；建议Owner：ENG-UI（待COORD核定）。

**期望：** BASE-04要求无效/过期/缺传感器如实降级；不能把离线设备显示成传感器检查正常。

**观察：** 本轮首次进入向导传感器页，MC/TH温度显示未检查/离线且顶栏硬件离线，但4通道断料组显示“正常(料丝在位)”绿色；温度面板四槽均“就绪(正常)”。没有本次四路传感器实际操作或有效新采样支撑。未推断filament_present_mask=0的物理语义。

**复现：** 在本轮已记录OFFLINE状态下，打开干净profile的向导。 → 下一步至传感器检测页，检查四路断料组与离线状态。

**证据：** `project-control/docs/evidence/twin/TWIN-55/runs/codex_qa_01/BASE-04-sensors.txt`、`project-control/docs/evidence/twin/TWIN-55/runs/codex_qa_01/BASE-04-sensors.png`、`project-control/docs/evidence/twin/TWIN-55/runs/codex_qa_01/BASE-20-panel.txt`、`project-control/docs/evidence/twin/TWIN-55/runs/codex_qa_01/BASE-01-initial.html`

## 指令 10

【问题】UART断链超过3秒仍保留ONLINE及旧温度，未按引用方案哨兵降级

**记录：** `ISS-20261105-014`；用例：BASE-25, DELTA-BAUD；建议优先级：P1；建议Owner：ENG-DM（待COORD核定）。

**期望：** 引用整改方案HIL-06要求断链3秒内OFFLINE/哨兵、控制503；SWD外设故障独立于BASE-24物理拔USB。

**观察：** TH USART1置0并读回后约3.65秒，快照两节点仍ONLINE、旧温度仍数值、质量STALE、system_status=DEGRADED。MC USART2置0并读回后约3.66秒同样未打哨兵。两次控制负例均503，恢复CTRL1逐字匹配。MC故障CPU2秒窗口0.0%，只说明这个窗口；不外推物理拔线。

**复现：** 按uart_fault_windows.py，在NORMAL新采样基线保存CTRL1。 → 仅将指定CTRL1置0并读回，执行一次真实采样请求。 → 3秒等待后取快照与控制负例；finally精确恢复原寄存器并重新采样。

**证据：** `project-control/docs/evidence/twin/TWIN-55/runs/codex_qa_01/fault_TH_02.log`、`project-control/docs/evidence/twin/TWIN-55/runs/codex_qa_01/fault_MC.log`、`project-control/docs/evidence/twin/TWIN-55/runs/codex_qa_01/fault_MC_cpu.log`、`project-control/docs/evidence/twin/TWIN-55/runs/codex_qa_01/uart_fault_windows.py`

## 指令 11

【问题】正常观测窗口MC Debug出现裸adc日志交织并增加trunc计数

**记录：** `ISS-20261105-015`；用例：DELTA-DBG, DELTA-COMB；建议优先级：P1；建议Owner：ENG-MC（待COORD核定）。

**期望：** BASE§2.1要求正常窗口日志可关联、无未说明丢失/截断；业务故障上下文需结构化。

**观察：** 本轮MC增量日志存在裸“adc SS_ADC_BUSY”及插入结构化行中间的情况；trunc从23增至37。drop=75在接管时已存在，本轮未增加，不能归因为本轮突发。未执行290帧压力，不声称这是该负载的复现结果。TH复位后的本轮增量drop/trunc均0。具体计数和字节边界见debug_capture_provenance.json。

**复现：** 从保存的初始前缀字节数截取本轮MC增量，检查原始字节，不补行或清洗。 → 检索SS_ADC_BUSY及前后结构化行，核对trunc的实际变化。

**证据：** `project-control/docs/evidence/twin/TWIN-55/runs/codex_qa_01/debug_capture_provenance.json`、`project-control/docs/evidence/twin/TWIN-55/runs/codex_qa_01/mc_debug_qa_window.log`、`project-control/docs/evidence/twin/TWIN-55/runs/codex_qa_01/initial_mc_debug_raw.log`

## 指令 12

【问题】TH实际复位前后boot_id不变，交接缺完整固件标识映射

**记录：** `ISS-20261105-016`；用例：HANDOFF, BASE-02, BASE-26；建议优先级：P2；建议Owner：ENG-TH（待COORD核定）。

**期望：** 交付门禁§4.4/HW-G7要求准确固件映射，固定boot_id不能单独证明动态重启代次。

**观察：** 本轮执行probe-rs TH reset并捕获新的TH启动日志后，协议快照boot_id仍为2289543765，与复位前一致；MC显示16909060。协议firmware_version为2.0，manifest MC version_tag为V2.0.1-229D 1105；wire短标识0xA6791332/0x6356C05A与完整891a8bb...的接受映射未在交接包提供。固件暂存制品哈希匹配，片上MC应用区读回超时，不能补称已核实片上字节一致。

**复现：** 比较TH reset前后两份本轮快照和原始TH启动证据。 → 核对manifest及交接清单的短标识/完整commit/制品映射。

**证据：** `project-control/docs/evidence/twin/TWIN-55/runs/codex_qa_01/TH_recovery_reset.log`、`project-control/docs/evidence/twin/TWIN-55/runs/codex_qa_01/post_th_reset_th_debug_raw.log`、`project-control/docs/evidence/twin/TWIN-55/runs/codex_qa_01/action_timeline.jsonl`、`project-control/docs/evidence/twin/TWIN-55/runs/codex_qa_01/sealed_firmware_files.log`、`project-control/docs/evidence/twin/TWIN-55/runs/codex_qa_01/read_sources.json`

## 指令 13

【问题】未知API的404响应Content-Length与实际正文不一致

**记录：** `ISS-20261105-017`；用例：API-NEG-UNKNOWN；建议优先级：P2；建议Owner：ENG-UI（待COORD核定）。

**期望：** 错误接口也应返回完整HTTP响应，Content-Length应与实际正文字节数一致。

**观察：** 对POST /api/v1/temperature/target，服务返回404、Content-Length:35，但只输出4字节{"er后关闭连接；curl退出18，明确报告还缺31字节。该路径来自引用整改方案，真实UI用的是temperature/set；本单针对HTTP响应截断，不把404本身当作实现缺陷。

**复现：** 按unknown_api_http_framing.log保存的curl参数请求该未知路径。 → 对照声明长度与实际接收字节和curl退出码。

**证据：** `project-control/docs/evidence/twin/TWIN-55/runs/codex_qa_01/unknown_api_http_framing.log`
