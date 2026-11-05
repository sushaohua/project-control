"""将本轮实际观察写成逐例矩阵、人工收件单和独立报告；不审批、派单或修改任务卡。"""
import collections
import hashlib
import json
import os
import pathlib
import yaml
from audit_driver import ROOT

PC = ROOT.parents[5]
SESSION = os.environ.get('CODEX_THREAD_ID')
PREFIX = 'project-control/docs/evidence/twin/TWIN-55/runs/codex_qa_01/'
SUBMISSION = PC / 'docs/work_intake/submissions/20261105_twin55_codex_hil_issues.md'
VERSIONS = {'buildno': 'build-20261105-002', 'soc-ap': '79932746d225bb115010c5545ef3f7499482e137', 'mcu-p3': '891a8bb252814c83992a49b01fbe11ba83b92a1f', 'test_harness': 'd14ed04321c6d4f5ddb35a8801604a8af53b5b60', 'project-control_manifest': 'f4e45fb5cdd1d7c1fee405d9a720f19e200b126f', 'project-control_observed': '960f079647a00864fe7913836336b2a2ee3d729a'}

# 各项只描述已经取得的观察；不同现象分别登记，根因交技术角色调查。
FINDINGS = [
    ('全量验收总方案缺失，未提供冻结子例及经非作者复核的完整自动化套件', ['HANDOFF', 'J-01', 'DELTA-BAUD', 'DELTA-COMB'],
     'TWIN-55依赖条款要求消费封存交接单及经非作者独立复核的QA工具；本轮用户指定全量总方案为唯一验收输入。',
     'docs/planning/hil_full_acceptance_master_plan_20261105.md不存在。引用的BASE文档revision 4自称草案，T_probe等未绑定；未取得290帧的原始向量/速率/成功准则、五类复合联动的逐例定义和完整套件复核证据。已异步询问正确路径，未收到补充。确认单§3也已披露工具覆盖缺口。',
     ['读取用户指定总方案路径，得到ENOENT。', '核对TWIN-55 dependency_conditions、BASE草案§1/3/4及确认单§3；无法据此枚举冻结全量子例。'],
     ['read_sources.json'], 'P1', 'QA'),
    ('运行态含未封板的静态state端点，且当前启动代次未交接', ['HANDOFF', 'BASE-02', 'BASE-06'],
     '提测交接应覆盖实际部署配置、静态资产及运行身份；实时状态不得由旧缓存冒充。',
     '四进程/三静态资产哈希匹配；但当前PID为1676003/1676008/1676009/1676011，启动13:45:52，晚于交接日志13:38:28。网关实际static-dir=/tmp/aisoc_twin_logs/web_root，其中另有未列入manifest/SHA256SUMS的api/v1/state文件，SHA256=006b793bb8b86e440a4c9a7f3735c06038968ee3ac025dfef74d39fa979c14b3。HTTP /api/v1/state持续返回GEN=1、OFFLINE；真实采样快照已推进并可返回NORMAL。此静态文件返回的Content-Type为application/octet-stream。',
     ['核对/proc/<pid>/exe、命令行及进程启动时刻。', '完成一次新采样后比较GET /api/v1/state与GET /api/v1/temperature/snapshot。', '核对实际static-dir内api/v1/state的字节及哈希。'],
     ['initial_runtime.log', 'runtime_unlisted_static.log', 'action_timeline.jsonl'], 'P1', 'INTEGRATOR'),
    ('保存料槽配置隐式发起LOAD并附带210°C目标', ['BASE-17', 'BASE-18'],
     '手册功能5配置保存和BASE-17要求保存配置；进丝是独立物理动作，不能以保存配置替代用户确认的动作。',
     '真实鼠标点击“保存料槽映射配置”后，浏览器发POST /api/v1/filament/slots，body含active_slot=1、action=1、target_temp_deci_c=2100。TH随后出现op=LOAD、step_state=FEEDING；用户没有点击进丝。未测量实际位移，不能声称已经出料。已改为SELECT恢复DONE并将两端温度目标归零；占空比接口报告0。',
     ['选择合法single-1预设。', '在新鲜采样窗口点击“保存料槽映射配置”。', '检查CDP请求及TH Debug，比较保存前后的动作状态。'],
     ['BASE-17-fresh-save.txt', 'browser_cdp_raw.jsonl', 'th_debug_qa_window.log', 'SAFETY-target-zero.txt'], 'P1', 'ENG-UI'),
    ('模型一键载入直接启动作业', ['BASE-08', 'BASE-10'],
     '手册功能3区分模型载入与点击“开始打印”；BASE-08只加载，BASE-10独立开始。',
     '仅点击CalibrationCube.gcode“一键载入”，CDP即记录POST /api/v1/jobs/start {"model":"CalibrationCube.gcode"}，界面进入PRINTING、Layer 1/100、1.0%。没有点击开始打印。发现后立即调用cancel，回到IDLE。未把进度或逻辑坐标认定为物理动作。',
     ['取得新鲜采样并进入打印工作台。', '只点击CalibrationCube的一键载入。', '检查网络请求和作业状态，随后取消。'],
     ['BASE-08-fresh-cube.txt', 'BASE-08-fresh-cube.png', 'browser_cdp_raw.jsonl', 'action_timeline.jsonl'], 'P1', 'ENG-UI'),
    ('上传入口接受非法扩展名、非G-code内容和空文件', ['BASE-09'],
     'BASE-09要求非法格式/空文件拒绝，合法文件可恢复。',
     '真实Chrome文件控件先后选择valid.gcode(M114换行)、invalid.txt(非G-code文本)、invalid.gcode(同一非G-code文本)、empty.gcode(0字节)、valid.gcode。CDP原生alert均宣称“上传装载成功”；HTTP只提交name/size。补充公开API负例invalid.txt size=19与empty.gcode size=0均200 Upload staged。未启动这些上传文件。',
     ['使用本run存档的四个fixture，通过文件输入选择，保留真实文件SHA256。', '检查CDP请求、原生alert和HTTP返回。', '以合法valid.gcode重试作为恢复。'],
     ['browser_cdp_raw.jsonl', 'action_timeline.jsonl', 'invalid.txt', 'invalid.gcode', 'empty.gcode', 'valid.gcode'], 'P1', 'ENG-UI'),
    ('料槽API未拒绝非法权重，越界动作进入硬件NACK路径', ['BASE-19'],
     'BASE-19要求非10000、负数、非数及越界按契约拒绝；纯UI校验不覆盖后端准入。',
     '有NORMAL新快照前提时，total_mixing_weight=9999返回200；两个通道权重为-1/10001、总和仍10000时也200 Filament slots updated。slot_id/active_slot=5及action=-1得到504 RPC timeout or NACK，未在API入口报告参数非法。早期503结果保留，不计为参数负例通过。合法SELECT/action=0/目标0恢复得到200。',
     ['以本轮浏览器实际POST配置为基准，固定action=0、target_temp_deci_c=0。', '取得新鲜NORMAL快照后分别修改总和、通道权重、slot_id、action。', '检查HTTP与双路Debug；以合法SELECT恢复。'],
     ['action_timeline.jsonl', 'mc_debug_qa_window.log', 'th_debug_qa_window.log'], 'P1', 'ENG-UI'),
    ('MC热床300.0°C被当作正常新鲜温度', ['BASE-04', 'BASE-20'],
     'BASE-20要求温度有效性真实；OOBE明确标注热床有效范围5~130°C，工程门禁要求无效温度降级。',
     'MC Debug持续bed_ddC=3000；转发日志temp_millic=300000；快照bed.temperature_c=300.0、sensor_status=OK、quality=FRESH，组合system_status可为NORMAL，HMI显示300.0°C。仅凭这些证据不能判断真实热敏电阻、接线或算法根因，也不称其已经证实是伪造物理温度。',
     ['只做POST /api/v1/temperature/sample，不施加任何非零加热目标。', '关联MC Debug、转发日志、快照与HMI热床显示。'],
     ['action_timeline.jsonl', 'final_forward_service.log', 'mc_debug_qa_window.log', 'BASE-08-fresh-cube.txt', 'BASE-04-sensors.txt'], 'P1', 'ENG-MC'),
    ('TH真实ADC未映射到公开快照及HMI', ['BASE-20'],
     '引用整改方案HIL-01和BASE-20要求同采样ADC原始值、温度及有效性对账。',
     'TH本轮Debug有adc_raw约1900~2100且fault=0、真实采样TX；公开temperature/snapshot只有temperature/sensor_status/quality等字段，没有raw_adc映射，温度面板ADC读数显示0。截图保存了新采样后界面及目标0恢复。这里报告映射缺失，不断言真实ADC为0。',
     ['进入温度面板，执行本次新采样。', '将TH RX/STATE/TX采样与HTTP快照及面板ADC对应比较。'],
     ['SAFETY-target-zero.txt', 'SAFETY-target-zero.png', 'th_debug_qa_window.log', 'action_timeline.jsonl'], 'P2', 'ENG-UI'),
    ('设备离线时OOBE仍将四路断料传感器标为正常', ['BASE-01', 'BASE-04', 'BASE-21'],
     'BASE-04要求无效/过期/缺传感器如实降级；不能把离线设备显示成传感器检查正常。',
     '本轮首次进入向导传感器页，MC/TH温度显示未检查/离线且顶栏硬件离线，但4通道断料组显示“正常(料丝在位)”绿色；温度面板四槽均“就绪(正常)”。没有本次四路传感器实际操作或有效新采样支撑。未推断filament_present_mask=0的物理语义。',
     ['在本轮已记录OFFLINE状态下，打开干净profile的向导。', '下一步至传感器检测页，检查四路断料组与离线状态。'],
     ['BASE-04-sensors.txt', 'BASE-04-sensors.png', 'BASE-20-panel.txt', 'BASE-01-initial.html'], 'P1', 'ENG-UI'),
    ('UART断链超过3秒仍保留ONLINE及旧温度，未按引用方案哨兵降级', ['BASE-25', 'DELTA-BAUD'],
     '引用整改方案HIL-06要求断链3秒内OFFLINE/哨兵、控制503；SWD外设故障独立于BASE-24物理拔USB。',
     'TH USART1置0并读回后约3.65秒，快照两节点仍ONLINE、旧温度仍数值、质量STALE、system_status=DEGRADED。MC USART2置0并读回后约3.66秒同样未打哨兵。两次控制负例均503，恢复CTRL1逐字匹配。MC故障CPU2秒窗口0.0%，只说明这个窗口；不外推物理拔线。',
     ['按uart_fault_windows.py，在NORMAL新采样基线保存CTRL1。', '仅将指定CTRL1置0并读回，执行一次真实采样请求。', '3秒等待后取快照与控制负例；finally精确恢复原寄存器并重新采样。'],
     ['fault_TH_02.log', 'fault_MC.log', 'fault_MC_cpu.log', 'uart_fault_windows.py'], 'P1', 'ENG-DM'),
    ('正常观测窗口MC Debug出现裸adc日志交织并增加trunc计数', ['DELTA-DBG', 'DELTA-COMB'],
     'BASE§2.1要求正常窗口日志可关联、无未说明丢失/截断；业务故障上下文需结构化。',
     '本轮MC增量日志存在裸“adc SS_ADC_BUSY”及插入结构化行中间的情况；trunc从23增至37。drop=75在接管时已存在，本轮未增加，不能归因为本轮突发。未执行290帧压力，不声称这是该负载的复现结果。TH复位后的本轮增量drop/trunc均0。具体计数和字节边界见debug_capture_provenance.json。',
     ['从保存的初始前缀字节数截取本轮MC增量，检查原始字节，不补行或清洗。', '检索SS_ADC_BUSY及前后结构化行，核对trunc的实际变化。'],
     ['debug_capture_provenance.json', 'mc_debug_qa_window.log', 'initial_mc_debug_raw.log'], 'P1', 'ENG-MC'),
    ('TH实际复位前后boot_id不变，交接缺完整固件标识映射', ['HANDOFF', 'BASE-02', 'BASE-26'],
     '交付门禁§4.4/HW-G7要求准确固件映射，固定boot_id不能单独证明动态重启代次。',
     '本轮执行probe-rs TH reset并捕获新的TH启动日志后，协议快照boot_id仍为2289543765，与复位前一致；MC显示16909060。协议firmware_version为2.0，manifest MC version_tag为V2.0.1-229D 1105；wire短标识0xA6791332/0x6356C05A与完整891a8bb...的接受映射未在交接包提供。固件暂存制品哈希匹配，片上MC应用区读回超时，不能补称已核实片上字节一致。',
     ['比较TH reset前后两份本轮快照和原始TH启动证据。', '核对manifest及交接清单的短标识/完整commit/制品映射。'],
     ['TH_recovery_reset.log', 'post_th_reset_th_debug_raw.log', 'action_timeline.jsonl', 'sealed_firmware_files.log', 'read_sources.json'], 'P2', 'ENG-TH'),
    ('未知API的404响应Content-Length与实际正文不一致', ['API-NEG-UNKNOWN'],
     '错误接口也应返回完整HTTP响应，Content-Length应与实际正文字节数一致。',
     '对POST /api/v1/temperature/target，服务返回404、Content-Length:35，但只输出4字节{"er后关闭连接；curl退出18，明确报告还缺31字节。该路径来自引用整改方案，真实UI用的是temperature/set；本单针对HTTP响应截断，不把404本身当作实现缺陷。',
     ['按unknown_api_http_framing.log保存的curl参数请求该未知路径。', '对照声明长度与实际接收字节和curl退出码。'],
     ['unknown_api_http_framing.log'], 'P2', 'ENG-UI'),
]


def digest(path):
    """计算path文件真实SHA256；返回十六进制串，不存在时抛异常。"""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def evidence(names):
    """将相对证据names绑定到本run字节哈希；返回引用列表，不补造缺失文件。"""
    return [{'path': PREFIX + name, 'sha256': digest(ROOT / name)} for name in names]


def write_submission():
    """保存真实QA来源的收件单；无参数，返回公共约束文本，不伪造HUMAN报告者。"""
    common = '只登记本轮实际观察；不修改业务仓、不重编译、不擦写Bootloader、不关闭Issue；根因由Owner调查。BASE-24和物理观察留Stage2。'
    lines = ['---', 'submission_id: 20261105_twin55_codex_hil_issues', 'revision: 1', 'enabled: true', 'reported_by:', '  actor_type: MODEL', '  actor_id: ' + SESSION, '  source_channel: independent_codex_qa', '---', '', '# TWIN-55 独立黑盒提单汇总', '', '## 公共约束', '', common, '', '本单来自用户明确授权的独立Codex QA，不是人工逐项实测签署。现Phase1收件器只接受HUMAN（work_intake.py）；如实保留MODEL，需唯一COORD人工收取/裁决该入口限制，不能伪造身份促通过。尚未扫描、派单或关闭。', '', '正式验收：BLOCKED；已取得的黑盒不符合见各单；Stage1未完整执行，未批准。', '']
    for number, finding in enumerate(FINDINGS, 1):
        title, cases, expected, observed, steps, refs, priority, owner = finding
        issue = 'ISS-20261105-' + str(number + 4).zfill(3)
        lines += ['## 指令 ' + str(number), '', '【问题】' + title, '', '**记录：** `' + issue + '`；用例：' + ', '.join(cases) + '；建议优先级：' + priority + '；建议Owner：' + owner + '（待COORD核定）。', '', '**期望：** ' + expected, '', '**观察：** ' + observed, '', '**复现：** ' + ' → '.join(steps), '', '**证据：** ' + '、'.join('`' + PREFIX + ref + '`' for ref in refs), '']
    SUBMISSION.parent.mkdir(parents=True, exist_ok=True)
    with SUBMISSION.open('x') as stream:
        stream.write('\n'.join(lines))
    return common


def write_issues(common):
    """写入ISS-005起的独立发现；common为公共约束；返回编号列表，不修改既有单。"""
    ids = []
    text = SUBMISSION.read_text()
    for index, finding in enumerate(FINDINGS, 1):
        title, cases, expected, observed, steps, refs, priority, owner = finding
        issue_id = 'ISS-20261105-' + str(index + 4).zfill(3)
        section = text.split('## 指令 ' + str(index) + '\n', 1)[1].split('\n## 指令 ', 1)[0].strip()
        item = dict(schema_version=1, id=issue_id, revision=1, kind='issue', enabled=True, title=title, objective=section)
        item['source_refs'] = dict(submission_id='20261105_twin55_codex_hil_issues', submission_revision=1, instruction_anchor='instruction_' + str(index), submission_path='project-control/docs/work_intake/submissions/' + SUBMISSION.name, submission_sha256=digest(SUBMISSION), instruction_sha256=hashlib.sha256(section.encode()).hexdigest(), verbatim_instruction=section, common_constraints=[common], common_constraints_sha256=hashlib.sha256(common.encode()).hexdigest())
        item.update(demand_ref={'demand_id': 'DEM-20261105-005', 'confirmation_id': 'CONFIRM-WEB-HMI-FULL-QA-BUILD-DEPLOY-20261105'}, reported_by={'actor_type': 'MODEL', 'actor_id': SESSION, 'source_channel': 'independent_codex_qa'}, authorization_refs=[{'path': 'project-control/docs/evidence/twin/TWIN-55/runs/codex_qa_01/read_sources.json', 'sha256': digest(ROOT / 'read_sources.json'), 'basis': '用户本轮明确要求独立测试和ISS-005起提单；不是工程修复批准'}], approval_refs=[], requested_action='triage', priority_hint=priority)
        item.update(related_ids={'engineering_tasks': ['TWIN-54', 'TWIN-55']}, triage_metadata={'root_cause_status': 'unknown', 'clarity_status': 'clear', 'proposed_owner_role': owner}, safety_flags={'shell_execution_disabled': True, 'contains_shell_like_text': True})
        item.update(resolution='open', source_task={'task_id': 'TWIN-55', 'revision': 1, 'run_id': 'codex_qa_01'}, feature_and_case_ids=cases, affected_versions=VERSIONS, preconditions=['本轮锁定部署；实际运行身份及限制见read_sources.json、initial_runtime.log', '测试工具未取得非作者独立接受，不声称完整正式HIL批准'], reproduction_steps=steps, expected=expected, observed=observed, evidence=evidence(refs), impact=title, root_cause=None, verification_runs=[], closure=None, duplicate_of_or_disposition=None, blocker_and_recovery='保持open，COORD查重/人工收件后安排Owner；修复须准确新候选独立复验，不以本轮自动关闭。')
        path = PC / 'docs/work_intake/issues' / (issue_id + '.yaml')
        with path.open('x') as stream:
            yaml.safe_dump(item, stream, allow_unicode=True, sort_keys=False, width=110)
        ids.append(issue_id)
    return ids


def write_matrix():
    """写完整Stage1组目录和实际子项；无参数，返回组列表；组未完成不能填通过。"""
    observed = {
        1: ('FAIL', '干净profile显示向导；通信/传感器健康前提不成立，断料组却显示正常。', ['BASE-01-initial.txt', 'BASE-04-sensors.txt']),
        2: ('BLOCKED', '两UID匹配，短版本/完整固件及boot epoch映射不足；初始TH无响应，复位后取得真响应。', ['MC_uid.log', 'TH_uid.log', 'TH_recovery_reset.log']),
        3: ('BLOCKED', '语言/主题点击和刷新已执行；English切换生效但刷新回中文。未取得该持久化断言的冻结接受条件，记录观察。', ['BASE-03-english.txt', 'BASE-03-reload-english.txt']),
        4: ('FAIL', '离线时四路传感器全绿；真实四路触发属于Stage2。', ['BASE-04-sensors.txt']),
        5: ('BLOCKED', '实际点击完成、关闭、刷新、重开已采证；前四步健康前提不满足，不算正常完整向导通过。', ['BASE-05-after-finish.txt', 'BASE-05-after-refresh.html']),
        6: ('FAIL', '取得顶栏/温度面板和浏览器断网；state静态端点与新采样矛盾。', ['runtime_unlisted_static.log', 'BASE-27-browser-offline.txt']),
        7: ('BLOCKED', '未执行有真实运动及排险条件的急停/解除；不在未经确认场地启动运动。', []),
        8: ('FAIL', '一键载入直接start，已cancel；未交付冻结样例文件及哈希，不签模型内容正确。', ['BASE-08-fresh-cube.txt']),
        9: ('FAIL', '合法/非法扩展名、非法内容/空文件/合法恢复均实际选择；后端负例亦接受。上传上限仍未冻结。', ['browser_cdp_raw.jsonl']),
        10: ('BLOCKED', '仅观察到模型载入隐式启动，不计正常“开始”用例；缺已冻结安全作业及物理执行依据。', ['BASE-08-fresh-cube.txt']),
        11: ('BLOCKED', '未完成安全真实作业暂停/继续；没有通过进度/ACK替代物理依据。', []),
        12: ('BLOCKED', '意外启动后cancel确认为IDLE，保存该局部事实；重复/超时/新作业及实际停止证据不全。', ['action_timeline.jsonl']),
        13: ('BLOCKED', '没有安全冻结短作业及最终执行/物理完成依据，未执行。', []),
        14: ('BLOCKED', '空间/限位及测量前提未交接；不执行100mm或其他未经确认的运动。负向API清单亦未冻结。', []),
        15: ('BLOCKED', '回零限位/安全空间未确认，真实过程及效果留人工窗口。', []),
        16: ('BLOCKED', '未交付探针/25点实际测量的自动判据和安全前提，未触发调平。', []),
        17: ('FAIL', '合法保存已执行，隐式LOAD；合法SELECT恢复完成；配置持久化正常范围未完整接受。', ['BASE-17-fresh-save.txt']),
        18: ('BLOCKED', 'single/dual/quad UI预设已观察，实际供料及保存/刷新全链路未完成；保存有副作用。', ['BASE-18-single-1.txt', 'BASE-18-dual-50.txt', 'BASE-18-quad-25.txt']),
        19: ('FAIL', 'UI非法总和提示及合法恢复；API非法总和/通道权重被接受，越界slot/action变504。', ['action_timeline.jsonl']),
        20: ('FAIL', '新采样、双端目标0及Debug/API/UI已核对；MC300°C有效性和TH ADC映射失败。无独立热测/PWM测量。', ['SAFETY-target-zero.txt', 'action_timeline.jsonl']),
        21: ('BLOCKED', '未交接四路自动触发夹具；肉眼/人工逐路动作归Stage2，离线假绿另记FAIL。', ['BASE-04-sensors.txt']),
        22: ('BLOCKED', '网络面板已读；独立VM客户端mDNS解析/访问超时，未核实多播/网段前提，环境阻塞。', ['BASE-22-network.txt', 'mdns_independent_client.log']),
        23: ('BLOCKED', '健康面板和真实UART故障已观察，24类错误码清单/触发/恢复断言缺冻结输入。', ['BASE-23-health.txt', 'fault_TH_02.log', 'fault_MC.log']),
        25: ('FAIL', '执行TH USART1与MC USART2故障、精确恢复；3秒退化不符合。真实物理断连/全部子例未完成。', ['fault_TH_02.log', 'fault_MC.log']),
        26: ('BLOCKED', '首次/完成后刷新/重开已操作；未重启服务（部署会清日志，精确配置和排他迁移未交接）。', ['BASE-26-reopen.txt', 'BASE-26-reopen-after-complete.txt']),
        27: ('BLOCKED', '真实Chrome网络断开与恢复有截图/事件；未穷举独立SSE/HTTP/网关服务所有故障层及冻结期限。', ['BASE-27-browser-offline.txt', 'BASE-27-browser-restored.txt']),
    }
    groups = [{'case_id': 'BASE-' + str(number).zfill(2), 'status': row[0], 'observed': row[1], 'evidence': [PREFIX + x for x in row[2]], 'complete': False, 'formal_acceptance': False} for number, row in observed.items()]
    groups += [{'case_id': name, 'status': 'BLOCKED', 'observed': reason, 'complete': False, 'formal_acceptance': False} for name, reason in [('J-01', '依赖的向导、温度、运动、供料与作业正常路径失败/缺前提，未执行完整旅程。'), ('DELTA-DBG', '已有双路真实日志和MC污染/截断失败；调试开关/慢采集/满缓冲的冻结步骤及工具未交付。'), ('DELTA-BAUD', 'VM端921600 8N1已读；双板有seq>255真实往返和UART故障；未执行冻结的290帧突发/速率不匹配/重启全部子例。'), ('DELTA-COMB', '正常联合通信有观察且日志缺陷已提；五类复合联动定义缺失，未执行完整批次。')]]
    data = dict(schema_version=1, task_id='TWIN-55', task_revision=1, run_id='codex_qa_01', session_id=SESSION, decision='BLOCKED', observed_functional_result='FAIL', stage1_complete=False, formal_approved_scope=[], versions=VERSIONS, qa_policy_requested='streamlined-v1', test_tools_non_author_review=None, group_counts=dict(collections.Counter(item['status'] for item in groups)), groups=groups, deferred=[{'case_id': 'BASE-24', 'status': 'NOT_EXECUTED', 'stage': 2, 'reason': '必须真实物理拔业务USB；SWD不能替代。'}], raw_http_and_action_events=PREFIX + 'action_timeline.jsonl', independent_case_expansion='缺全量总方案，未把草案的组表冒充已冻结的全量子例，也不把30组名称计为30项通过。')
    (ROOT / 'stage1_case_results.json').write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
    return groups


def write_stage2():
    """保存集中人工窗口所需动作与安全门槛；无参数，无返回值，不请求立即操作设备。"""
    text = '''# TWIN-55 Stage 2 人工窗口清单（未执行，未通过）

必须先由COORD落实唯一排他窗口、准确新候选、已复核脚本、恢复联系人及当前传感器/限位/空间事实。继续保持TH加热0%硬锁；不得刷写Bootloader。Stage1失败项修复后先完成必要自动回归，不能用人工签名掩盖。

| 项目 | 现场动作/证据 | 完成判据与恢复 |
| --- | --- | --- |
| BASE-24 | 实际拔业务USB、记录操作者/UTC/设备物理变化；同时录屏、业务帧、双Debug、CPU | 3秒降级、失效温度哨兵、控制503/504、CPU≤2%；插回取得新握手/新采样。SWD不算物理拔线 |
| BASE-07 | 安全有界运动中观察急停，排险确认后解除 | 真实停止/可控证据；不能只看UI徽章 |
| BASE-14/15 | 确认机械空间和限位后测量XYZ步进、微调、回零 | 物理位移/限位与请求对应；100mm先确认空间；异常立即停止 |
| BASE-16 | 确认调平探针和25点测量夹具 | 新鲜实际25点数据，探测过程和网格一致，缺探针保持阻塞 |
| BASE-18/21 | 四路断料传感器逐路触发与恢复，实际选槽/供退料观察 | 通道映射、抖动、实际效果与日志对应；不能把配置保存等同进丝 |
| BASE-20 | 外部温度基准和TH PWM/加热输出测量 | 解释MC300°C和TH ADC映射，直接证明0%输出；API字段不能替代电测 |
| BASE-01/02/25/26 | 如需物理单节点断连/接回及冷启动，集中采证 | 双板分别探测、真实版本、动态重启代次；旧缓存不能满足恢复 |
| 台架工具恢复 | MC探针可枚举但末次两次读取报WinUSB reset not supported；未物理拔插探针 | 由现场恢复工具连接后只读核验MC USART2=0x201C；最后成功精确恢复记录见fault_MC.log；TH末次读回0x202C |

本清单中运动/供料等物理断言是从相关BASE分离出的Stage2人工部分；其余自动子例仍属于Stage1，不能因本清单而删减。mDNS网络/多播前提另由网络Owner核实。290帧突发、五类复合联动、冻结期限及非作者工具复核是Stage1输入阻塞，不能简单移交人工就算完成。
'''
    (ROOT / 'stage2_manual_checklist.md').write_text(text)




if __name__ == '__main__':
    assert PC.name == 'project-control', PC
    common = write_submission()
    ids = write_issues(common)
    groups = write_matrix()
    write_stage2()
    print(json.dumps({'issues': ids, 'group_counts': dict(collections.Counter(x['status'] for x in groups))}))


table = '\n'.join('| ' + row['case_id'] + ' | ' + row['status'] + ' | ' + row['observed'] + ' |' for row in groups)
stage1 = f'''---
task_id: TWIN-55
run_id: codex_qa_01
reviewer_session: {SESSION}
decision: BLOCKED
observed_functional_result: FAIL
stage1_complete: false
approved_scope: []
---

# TWIN-55 Stage 1 独立黑盒QA报告

未完成全量Stage1，不签发任何整机/HIL通过。已执行的浏览器/API/真机观察发现13项问题，登记{ids[0]}至{ids[-1]}，根因保持未知。全量总方案不存在；缺冻结子例、完整QA套件及其非作者复核、原始双向业务帧采集交接。当前会话有实际Session UUID及实时codex_session.jsonl，但没有核实运行时模型和新的服务器Docker物证；本轮按用户禁止重编要求消费既有部署，不把manifest中CTest=true当作本轮Docker接受。

准确版本见read_sources.json和build_manifest；四运行进程SHA与三Web资产SHA匹配。只读制品文件哈希匹配；片上MC应用区读回45秒超时、TH/anchor片上读回未执行。未触碰Bootloader扇区；没有编译或修改业务源码。部分操作脚本本轮新写且未获非作者复核，其结果是可重放观察材料，不能作者自证完整正式接受。

实际操作包括干净profile向导、语言/主题/刷新、预设与保存、真实文件控件正负/恢复、M114只读G-code、两端新温度采样和目标归零、TH USART1与MC USART2故障/精确恢复、浏览器断网/恢复。模型载入触发意外start后立即cancel；保存配置触发意外LOAD/2100目标，随后SELECT恢复DONE、两端目标归零。没有把逻辑坐标、进度和ACK提升为物理动作证明。

## 覆盖矩阵

下表是30个Stage1规格组的核对目录，不是完整冻结子例表。FAIL指已有明确不符合；BLOCKED指输入/前提/完整覆盖不足。所有组complete=false，正例、负例、恢复的细节以action_timeline/CDP/故障日志为准，未执行不计通过。

| 组 | 结果 | 实际范围及缺口 |
| --- | --- | --- |
{table}

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
'''
(ROOT / 'stage1_qa_report.md').write_text(stage1)
handoff = ROOT.parents[2] / 'TWIN-54/runs/codex_qa_01'
handoff.mkdir(parents=True, exist_ok=True)
report = f'''---
task_id: TWIN-54
run_id: codex_qa_01
reviewer_session: {SESSION}
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

以上实测原件均位于../TWIN-55/runs/codex_qa_01（从本文件请按workspace路径索引）：project-control/docs/evidence/twin/TWIN-55/runs/codex_qa_01/。审计命令、完整哈希和UTC见initial_runtime.log、runtime_unlisted_static.log、action_timeline.jsonl，输入原件逐项SHA见read_sources.json。

## 交接缺陷及缺项

1. {ids[0]}：指定总方案不存在，完整冻结全量用例/工具和非作者接受证据缺失。现有确认单已披露覆盖缺口，轻量清单的HANDOFF_READY不能补齐它。290帧/五类复合场景无法在零上下文下准确执行，影响Stage1全量验收。
2. {ids[1]}：实际部署多出api/v1/state静态文件（SHA 006b793bb8b86e440a4c9a7f3735c06038968ee3ac025dfef74d39fa979c14b3），持续回GEN=1/OFFLINE；未列配置、文件和新启动代次，实际端点与新采样矛盾。
3. 串口采集接管信息不足：轻量清单只给dual_dbg_logger.ps1名字，没有可直接复用的精确位置/哈希、只追加日志位置/切片与时钟/epoch接口、原始业务帧采集器。审阅者必须从进程枚举和步骤日志反查作者Windows临时目录并读取脚本才完成接管；这些是后续调查所得，不能倒填为交接已提供。
4. 芯片/探针可匹配，但片上固件完整哈希和wire短标识到891a8bb…的接受映射不足；{ids[11]}登记TH真实复位后boot_id不变。step5日志只有Finished和标题，未保留完整download --verify实际命令/输出，不能仅凭标题自证Flash字节。TWIN-55任务卡仍引用旧MCU基线016e1236…、candidate/lease/实际QA会话未落地，未由本会话改卡促通过。
5. 初始TH Debug于14:08:02停止更新，MC drop=75/trunc=23；这些现场事实不等于已具备“新鲜健康、零截断”的提测起点。未交代残留作业状态、异常温度、UART恢复及mDNS依赖的接管SOP。

## 接受边界

认可的只是4个运行exe和3个主Web资产哈希匹配、端口与两芯片UID核对事实。不认可完整交接、实际片上固件一致、动态身份、Docker QA或全量HIL通过。TWIN-55另交阶段报告，未以该阶段的局部软件/API现象补签TWIN-54。全部问题保持open，COORD收件后按准确输入/差异补齐再独立复核，保留本报告和历史物证。
'''
(handoff / 'qa_review_report.md').write_text(report)
