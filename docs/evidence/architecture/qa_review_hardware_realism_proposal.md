---
template_version: '2026-10-27'
review_id: QA-ARCH-HARDWARE-REALISM-20261031-01
review_status: completed
reviewer_role: QA
platform: codex
model: gpt-6.1-sol
actual_model: gpt-6.1-sol
requested_model: gpt-6-luna
model_override_ref: null
actual_session: 01a19173-e092-7781-ae54-54efdb0cce87
author_session: null
task_id: null
task_revision: null
review_time: "2026-10-31T18:23:39+08:00"
decision: REJECTED
decision_scope: proposal-as-written; not an implementation acceptance or task-state change
formal_acceptance_status: BLOCKED_INCONCLUSIVE
process_audit: blocked-candidate-and-provenance
result_check: static-document-and-source-inspection-only
verification_scope: 11 findings, 5 principles, 3 phases, 3 decisions, concurrency and flow control
required_evidence_level: architectural-source-review
verification_environment: host Codex session; independent server fetch; no container build or HIL
local_source_commit: 409846a5ce6c1b1d6115736e7129a71d85ebe875
observed_server_commit: ca6c40b2fdfc421ef628100f8b2d40fe64869d85
project_control_local_commit: afd525946602c973d52feedcf7364f77ab2d221c
server_qa: null
container_id: null
image_digest: null
report_review: null
session_evidence: runs/hardware_realism_20261031_01/session_metadata.json
reviewed_artifacts:
  - path: /home/sushaohua/.gemini/antigravity-cli/brain/8d4e8b77-42a9-4bd3-bd5a-1b881e8d4bd5/system_architectural_review_hardware_realism_and_closed_loop.md
    sha256: f9476502c65653b4052cfac4b06ca65eb07d9b3a967799729a1c926d7c1daff6
    preserved_copy: runs/hardware_realism_20261031_01/proposal_input.md
  - path: soc-ap
    commit: 409846a5ce6c1b1d6115736e7129a71d85ebe875
    source: local-committed-investigation-only; server-fetch-rejected
    file_hashes: runs/hardware_realism_20261031_01/source_manifest.json
  - path: soc-ap
    commit: ca6c40b2fdfc421ef628100f8b2d40fe64869d85
    source: independently-fetched-server-main
    file_hashes: runs/hardware_realism_20261031_01/source_manifest.json
protocol_and_expectations:
  - path: project-control/docs/specs/ap_mc_formal_protocol_v2_0_multidevice_routing_draft_20261015.md
    revision: MiniMCProto v2.0 Rev 2.0.3
    hash_manifest: runs/hardware_realism_20261031_01/input_manifest.json
verified_findings:
  confirmed_core: [D01, D02, D03, D04, D05, D06, D08]
  partially_accurate: [D07, D09, D10, D11]
  runtime_or_hardware_verified: []
blocking_issues:
  proposal: [B01, B02, B03, B04, B05, B06, B07, B08]
  formal_evidence: [E01, E02, E03]
recommendations:
  - Correct factual statements and freeze readiness, freshness and protocol semantics before dispatch.
  - Execute Phase 1 first with all unfinished physical controls disabled or explicitly simulated.
  - Require authenticated device identity, session epochs and explicit recovery approval.
  - Separate accepted data from executed motion and bound queues, retries and control latency.
unexecuted: [build, automated-product-tests, CPU-measurement, real-UART-hotplug, physical-stop, firmware-validation]
accepted_scope: null
---

# 硬件真实性与闭环整改提案独立审查

**结论：REJECTED，提案须修订后再评。** 11 项中的核心缺陷多数存在，但并非全部陈述准确；尤其版本新鲜度为 **5 秒 / 15 秒**，不是 3 秒 / 15 秒，串口忙循环受单次事务超时约束。方案把入队 ACK 当作物理执行完成，并把 AP 本地暂停称为安全暂停，当前不足以成为实施和验收契约。

**正式收件状态另记为 BLOCKED / INCONCLUSIVE。** 本地受审提交未能从服务器取得，缺少任务绑定、同候选沙箱证据及报告非作者复核。下面的源码结果是有版本和文件摘要的静态调查，不能提升为正式服务器候选验收。本文不改变任务状态，不撤销任何历史签署，也不把环境缺证计为代码整改轮次。

## 1. 身份、版本和证据边界

本会话由用户指定承担独立 QA，未参与被审提案或业务源码的编写，未修业务代码。实际会话 UUID 与实际模型来自当前 Codex rollout 的 `session_meta` / `turn_context`，已选择性导出到 [session_metadata.json](runs/hardware_realism_20261031_01/session_metadata.json)。未取得作者实际会话来源及 COORD 任务卡，故不能宣称已完成制度要求的身份交叉核验。

权威规则以 `project-control/manifest.yaml` 标记的 canonical `project-control` 为准，已阅读 QA 规则、交付门禁、总控清单与 QA 报告模板。[input_manifest.json](runs/hardware_realism_20261031_01/input_manifest.json) 锁定实际读取字节；这些控制输入是本地文档，未冒充服务器锁定版本。

| 核查 | 结果与影响 |
| --- | --- |
| 原始提案 | SHA256 为 frontmatter 所列值；原文副本归档，未修改原文。 |
| 本地源码 | `soc-ap` HEAD 为 `409846a5…`，读取时工作树干净。26 个审阅文件均与该提交相同；生成了本地提交的只读文件快照供静态调查。它不是正式 QA 基线。 |
| 服务器核查 | 实际 `ls-remote` 与独立对象库 fetch 得到 `main=ca6c40b2…`。该提交是本地提交的直接父提交；差异共 11 文件、1384 插入 / 4 删除。 |
| 准确候选获取 | 两次独立 fetch 本地完整 SHA 都返回 `not our ref`，归档命令 exit 128。只能断言本次无法从该服务器获取，不能推断所有服务器/ref 均不存在该对象。 |
| 版本差异 | 服务器提交没有 `ui_gateway_job_ctrl.cpp/.h`，也没有对应新增 REST 作业/轴控端点。D03～D06 的本地新功能不得冒充服务器已部署功能。FWD、STATE、fallback 与 executor 等相同字节可由 manifest 对账。 |
| 沙箱 | Docker server 26.1.3 可用；未创建受测容器，也没有 Container ID / digest / `server_qa.json`。原因是准确受审候选无法获取；没有以本地源码注入容器来冒充服务器 QA。独立 `/tmp` 仓库本身也不算沙箱。 |
| 验证层级 | 只读文档、代码与协议审查；未构建、未跑产品自动化测试、未测 CPU、未操作物理设备。本次文档审查不机械要求固件构建/HIL，但不得据此签发运行或硬件通过。 |
| 模型 / 收件 | 实际 `gpt-6.1-sol` 与项目默认 `gpt-6-luna` 不同，未取得 `model_policy.approved_overrides`。报告非作者复核尚未执行；没有伪造签名或计划会话。 |

可复查的命令、cwd、时刻、退出码、原始 stdout/stderr 与日志 SHA 见 [commands.json](runs/hardware_realism_20261031_01/commands.json)。26 文件的本地/服务器摘要及一致性见 [source_manifest.json](runs/hardware_realism_20261031_01/source_manifest.json)。以下代码行号均针对 `409846a5…`；相同字节文件也适用于所取服务器父提交。

## 2. 11 项发现逐项核实

“成立”指核心源码现象成立，不表示确认了原文所有因果、措辞或硬件影响。

| ID / 原项 | 裁定 | 独立源码证据与必要修正 |
| --- | --- | --- |
| D01 / 1 默认在线 | **核心成立** | `services/device_manager/device_manager_service.cpp:105–137,157` 无硬件版本应答就构造 MC/TH `is_valid=true`、ONLINE、固定 boot_id/版本/commit。实际字段为 `is_valid`。但整机快照初始化是 `BOOT_INITIALIZING`，温度为 OFFLINE 哨兵（`device_manager_state.cpp:137–150`）；不能说开机所有状态都 ONLINE。 |
| D02 / 2 假降级快照 | **成立** | `ui_gateway_http.cpp:182–205` 固定 ONLINE、245/1177 deci°C、FRESH、固定版本。调用发生于 `ui_gateway_service.cpp:61–68` 的周期 SSE，以及 `ui_gateway_server.cpp:91–104,134–149` 的 REST/初始 SSE。调用失败或空快照也可进入 fallback，不限于总线物理断连。源码不能证明“恶意”，应删除动机断言。 |
| D03 / 3 静态调平网格 | **成立（本地新增候选）** | `ui_gateway_job_ctrl.cpp:17–23,34–40,139–164` 初始化并重新复制 DEFAULT_MESH，无探针调用。网格和 min/max 等统计均固定。STATE 另有含 `valid/updated_ns` 的网格模型，不能由此认为网关已接通它。 |
| D04 / 4 开环作业 | **成立（本地新增候选）** | `ui_gateway_job_ctrl.cpp:193–218` 累加行号、三角函数生成坐标，无发送/ACK/准入；`ui_gateway_service.cpp:83–88` 传入的是 poll 配置超时，不是实际 elapsed，所以“一秒一行”也不是可靠墙钟速率。`PRINTING/COMPLETED` 只证明本地状态机推进。 |
| D05 / 5 Jog/Home | **成立（本地新增候选）** | `ui_gateway_job_ctrl.cpp:108–136` 仅改内存、格式化 G-code；Home 不等待回包就设置 homed，还不区分所请求轴地清零 XYZ。没有真实发送调用。原文关于堵转/脱调不能被发现是能力缺口推论，本次未做物理测试。 |
| D06 / 6 软件急停 | **成立，但实际比文案更直接** | `ui_gateway_job_ctrl.cpp:179–190` 只设状态与保存 `M112/M999` 文本，UI 路由 `ui_gateway_server.cpp:324–333` 没有接入 DEVICE/FWD 的急停链。这里不是“发送可能失败”，而是根本未尝试发送。DEVICE/FWD 另有二进制急停路径，故不能泛化为全工程无急停实现；该路径也未证明物理断电。当前 UI heater duty 被设为 0，不能从这些代码证明实际加热失控。 |
| D07 / 7 新鲜度死代码 | **部分准确** | 生产服务未调用 `dev_state_eval_version_freshness`，但它确实调用内部 `eval_single_mcu_freshness`，且 `tests/device_manager/twin/test_device_manager.cpp:584,590,596` 有直接调用，不能说全工程无人调用。`device_manager_state.h:90–91` 的版本阈值是 **5s / 15s**。3s 是温度 STALE 阈值，后者由 `device_manager_dispatch` 实际调度；没有证据支持“一切超时检测瘫痪”。 |
| D08 / 8 温度冻结 | **核心成立** | `device_manager_state.cpp:258–294` 只更新 quality / system_status，不清空最后数值；JSON `:365–388` 继续导出旧温度。温度 freshness 确实运行，3s STALE、10s FAULT（`telemetry_types.h:102–104,319–339`），并非一直 FRESH。前端优先渲染数字且未依据 quality 屏蔽，见 `app.js:817–830,846–879`。保留历史值本身可以合法，问题是缺少明确 last-known/年龄与当前无效语义；必须覆盖哨兵并非唯一正确方案。 |
| D09 / 9 POLLHUP 自旋 | **部分准确** | `core/forward/transport/serial_posix.cpp:171–214` 对 HUP/ERR/NVAL 返回 false；`forward_uart.cpp:108–121` 丢弃 bool，坏 fd 可立即重复 poll，忙循环路径成立。但 `:104,108,122` 有单次事务 deadline，当前 DEVICE 请求传 800ms（`device_manager_dbus.cpp:21`）。不是无限循环，单核 85%～100%、调度雪崩均未测量。FWD 主循环本身是 D-Bus dispatch，不是无条件永远执行此读循环。 |
| D10 / 10 无重连自愈 | **部分准确** | `forward_service.cpp:100–107` 在 `is_open=false` 时会按原路径重新 open，所以“从不重开”不准确；HUP 路径未 close/清标志，导致该分支通常无法恢复已挂起 fd。没有后台枚举/身份匹配重连。`ResetLink` 只 reset parser，不重开（`forward_dbus.cpp:101–123`）。`ttyUSB1` 并非每次必然分配；“必须重启所有进程”也无依据。 |
| D11 / 11 连接状态混淆 | **部分准确** | `app.js:835–839` 每次接受快照就把顶栏置绿，未依据 `system_status`。它由 SSE **数据事件和初始 REST 快照**两条路径调用（`:953–958,977–985`），并不是 SSE onopen 直接置绿；URL 也优先当前页面 origin（`:15`），不限 127.0.0.1。同时 `updateDeviceVersion(:900–935)` 已区分节点 ONLINE/STALE/OFFLINE，quality 徽标也存在。准确问题是顶栏语义和控制准入不反映硬件就绪，而非整个 UI 完全没有离线表达。 |

因此，**7 项核心成立、4 项部分准确，不能确认“11 项全部事实准确”**。其中 D03～D06 只确认本地已提交版本。原文“假模拟”的评价也须注明既有代码明确写有 twin sandbox / dry-run、0% duty，前端文案写有“流式模拟空跑”；允许隔离的显式模拟，不能把模拟状态混入真实硬件状态。

## 3. 五项原则的架构评价

| 原则 | 评价和必须补足的契约 |
| --- | --- |
| P1 单一物理真源 | 方向正确。STATE 汇总权威事实；FWD 提供链路/节点证据，Gateway/UI 不补造成功。须分别记录 transport-open、peer-identified、telemetry-fresh、motion-ready、fault、boot/session epoch；版本号缓存不是心跳。模拟需明确来源、独立运行模式和接口准入，不能静默 fallback。 |
| P2 故障即阻断 | 接受“停止准入和继续发送”；不接受据此承诺机器已停。HUP 应立即使会话失效，不等 3s；静默失联由单调时钟 deadline 兜底，3s 预算须含轮询/IPC/UI延迟。已进 MCU 队列的运动/加热需要本地 watchdog 与明确停机策略。失联时停止结果记 UNKNOWN，不能填 STOPPED/SAFE。 |
| P3 双链路透明 | 接受。还须分别显示 MC/TH、freshness、故障与作业状态，网关活着不代表 STATE/MC/TH 新鲜；浏览器须对“连接未断但不再来数据”设期限。不要用遮罩阻止急停请求、故障详情或诊断。 |
| P4 自动重连 | 有条件接受。打开 fd 不是 ONLINE；候选设备须验证稳定身份、角色、协议/能力与 boot_id。采用稳定设备映射或受控探测，禁止只凭波特率选首个 ttyUSB。重连只恢复探测能力，不能自动恢复作业、清急停或保留未经重核的 homed。 |
| P5 ACK 背压 | 当前表述不接受。正式协议 ACK 是完整块**入队**成功，不是 planner 完成；ACK 信用亦非执行行号。须区分 submitted / accepted / executed，定义执行完成回执/屏障及其版本。0x16 的现有 AP payload 定义可复用为输入模型，但不能当作已证明部署的 MCU 能力，也不能把开环步进计数宣称为编码器实测位置。 |

## 4. 阻断性方案问题与并发分析

### B01（P0）：入队 ACK 被误作运动执行完成

协议 Rev 2.0.3 §5.2 `CMD_STREAM_CHUNK`（第 503–520 行）明确整块提交内部队列后 ACK；一个 chunk 可有多行，不是一 ACK 对应一行完成。§4.1（234–282 行）要求每 peer 单在途、boot_id 隔离、同 seq/cmd 重试去重；§4.2（286–294 行）要求同时遵守 planner 槽位和 RX FIFO 的 64B 信用，零信用时仍可 200ms PING 探活。

原方案只有“ok/水位→current_line++”，会虚报执行进度，也没有定义 ACK 丢失、BUSY、重复/旧包、会话重启后的对账。必须定义有界 chunk 队列、块大小与完整行边界、字节和槽位预算、按契约关联的 ACK/NACK、固定 seq 重试和最大次数、零信用探活与失联期限。完成/恢复必须有 MCU 可验证的执行游标或屏障语义；没有这种能力时只能报告“已接收”，不能报告“已执行”。

### B02（P0）：本地 PAUSED 无法建立物理安全暂停

AP 掉线后不能保证暂停命令送达，更不能假设 MCU 已清掉预取队列。当前 `ui_gw_job_pause` 只是改本地枚举和文本。方案须增加 LINK_LOST / STOP_REQUESTED / STOP_CONFIRMED / STOP_UNKNOWN 的可区分语义，明确 MC/TH 本地通信 watchdog、热失控保护及停止/保持/断能策略、独立急停边界；具体电气能力由 Owner 确认，本文未验证。

保留最后确认执行游标和未知在途集合；严禁按最后已发送行恢复，也不能在 reconnect 后重发不确定执行的相对运动。boot_id 变化、位置或队列无法对账时保持故障并要求重新建立安全状态。物理停机、最大残余运动及温度响应必须通过真实 HIL 才能签署。

### B03（P1）：准入状态和时间契约不相容

`update_system_status_desc` 当前健康状态是 `NORMAL`，故 `system_status != "ONLINE"` 会拒绝真实健康快照。`is_fault` 时该函数还直接返回，不得由超时逻辑覆盖更高优先级的锁存故障。版本 5/15 秒、温度 3/10 秒与提案“3 秒 STALE→OFFLINE”相互不一致，须冻结状态表和命名，而非字符串补丁。

删除默认版本后，`dev_state_update_raw_sample:237,247` 只在已有 `is_valid` 时刷新版本槽；生产中 `dev_state_update_mcu_version` 的调用仅见默认初始化。只删默认值并挂接 freshness 会永久缺失真实版本。须增加真实关联 GET_VERSION/能力协商和周期活性来源，分别覆盖 MC 与 TH；不要把不周期发送的版本报告本身当固定周期心跳。

### B04（P1）：只在 tick / Jog / Home 加 guard 有旁路

start、resume、leveling、加热设定、直接 API 和后续 executor 都须经过同一权威准入。路由当前丢弃这些函数的返回值并返回 HTTP 200（`ui_gateway_server.cpp:241–333`），仅新增 `UI_GW_ERR_HARDWARE_OFFLINE` 不会形成端到端拒绝。应把实际失败映射到 HTTP/业务错误，并且不提前修改已确认坐标、homed 或作业结果。

“读旧 ONLINE→HUP→发送”是准入与发送间的竞态。准入应绑定会话代次与命令 ID，在唯一 UART owner 入队/发送时再核验；旧代次队列和延迟回包不得影响新会话。UI 禁用按钮只能辅助，不能承担硬互锁。tick 的暂停动作要幂等，不能把 IDLE、COMPLETED、ESTOP 覆盖成普通 PAUSED。

### B05（P1）：热插拔线程缺少资源所有权和锁协议

当前 `forward_service_execute_query:100–121` 持 `uart_mutex` 覆盖 open、发送和整个等待；`handle_emergency_stop:89–98` 也要同锁，而且 D-Bus handler 同步执行查询。源码能证明控制响应可被查询占用拖延，**本次没有复现或证明一个现存的必然 ABBA 死锁**。新增扫描线程若不受同一所有权约束，则存在以下具体风险：

| 交错 | 风险 | 修订要求 |
| --- | --- | --- |
| 读线程持旧 fd；扫描线程 close/open；fd 数字复用 | 对错误设备读写、parser/seq 被并发重置 | 单一 UART I/O owner 管理 open/close/read/write/parser/epoch。其他线程只提交有界消息，不直接 close。 |
| 已持 uart_mutex 的 wait_response 调用一个再次取同锁的 close/helper | 非递归 mutex 自锁 | 明确 helper 的锁前置条件；避免隐式重复加锁。 |
| uart/state/job 锁内等待同步 IPC；对端回调等待原锁 | 条件性 ABBA / 回调死锁 | 不跨业务锁同步 RPC、发布或 join；优先 owner 消息化，避免多锁嵌套。若确需嵌套，冻结全局顺序并检查全部调用路径。 |
| stop 持锁 join worker；worker 等同锁，或销毁锁前 worker 未退 | 死锁 / use-after-destroy | 先禁止新命令、唤醒并取消在途等待；不持业务锁 join；worker 退出后再关资源、销毁锁。 |
| 新 watcher 与 HTTP/tick 同时写 `s_job` | 无同步全局状态的数据竞争 | 当前网关主要串行执行，没有据此证明现存并发竞争；新增线程应投递事件给原 owner，或使用一致同步的完整快照。 |

DEVICE 现有 DDS 回调持 `state_mutex` 调用 `aisoc_dds_publish_temp_snapshot`（`device_manager_service.cpp:25–33`）；SDK 最终执行 `dds_writer->write`，不能将外部发布延迟当成零。应锁内更新/复制、锁外发布；同理信号不能持锁做同步等待。回调解锁后又读取 `snapshot.system_status_desc` 用于日志（`:35–37`），与 dispatch 的 freshness 更新可并发；默认版本初始化也未与已启动的 DDS 回调统一加锁。需在改动范围内修正这些访问，不能声称已有锁即线程安全。

### B06（P1）：重连只凭端口/波特率，不足以绑定正确机器

决策表 A 比正文 VID:PID 更弱，写成“匹配波特率即绑定”，可能误选另一块同型号设备。VID:PID 只标识设备类型，也不足以识别某台机器。要求绑定稳定 USB/拓扑身份与协议角色/能力，定义多候选歧义拒绝、独占访问、权限和资源释放；发现失败用有上限的退避和日志节流。重连成功后 MC、TH 分别验证，不能用 AP–MC 的 fd-open 一次性宣布两节点 ONLINE。

### B07（P1）：仅接入现有 executor 仍是本地执行模型

`contracts/twin/job/job_executor.c:94–118,121–148` 直接把 home/目标坐标写入内存，再 `aisoc_job_step_progress`；`:177–201` 解析后直接 dispatch，没有串口发送或 ACK 回调。Phase 3 不能靠接线这个组件就宣称物理闭环。须剥离“命令目标”和“硬件确认状态”，把进度推进移到按契约验证的受理/执行事件，保留 dry-run 0% heating 基线，真实热控单独接受。

还须明确 Jog/Home/Leveling 的真实实现或禁用策略；现有三阶段仅具体描述流式打印，未消除这些本地假成功端点。0x16 payload 在 `job_executor.h:31,54–67` 有 AP 定义，但本次未检查/锁定 MCU firmware，不能据此断言硬件已经支持或可直接消费。

### B08（P1）：超时传播、JSON 和慢消费者没有闭环

`dev_state_eval_freshness` 不递增 generation，也不发布 DDS/SnapshotUpdated；仅加入版本 evaluator 仍不会自动通知事件消费者。新鲜度或链接变化应形成一致的一次状态提交：按节点使数据失效、更新 generation/epoch、保留锁存故障，锁外发布；Gateway 同时做自己单调时钟超时兜底，避免丢一个信号就永久在线。当前 SSE 周期拉取能读到变化，不代表所有 DDS/信号消费者都能收到。

JSON 不应把数值字段改成 `"--.-"`；可保持数值哨兵的兼容契约或使用 nullable 数值加 validity/quality/age，由 UI 格式化。尤其 `app.js:823–824` 把所有 `temperature_millic >= 2147483640` 都判 FAULT，包含真正的 `0x7FFFFFFE` OFFLINE；后续 OFFLINE 比较还使用 16-bit sentinel，所以只写后端哨兵并不能得到要求的离线显示。`temperature_c` 有值时还优先忽略 quality。

SSE 客户端为 nonblocking（`ui_gateway_server.cpp:71`），broadcast 单次 send 对正数短写不续传（`:510–513`），可能截断事件；主循环还做 500ms 同步 GetSnapshot。要求有界发送缓冲、短写续传或明确断开重取快照、慢客户端策略，并定义断连/坏 JSON/缺事件时 UI 的数据时效。不得把这些进程级时限等同为物理停止时限。

## 5. 三阶段方案修订与验收

保留“阶段 1 优先”的切分；每阶段是独立候选，不沿用原提案的“改几行就全系统恢复在线”承诺。

| 阶段 | 必须修订的实施边界 | 后续独立验收的关键证据（本次均未运行） |
| --- | --- | --- |
| 1 止血和如实阻断 | 区分 serial timeout/暂时无数据/硬错误；检查 send 与 read 结果、失效 fd、取消在途；删除真实模式伪数据，接通真实身份/活性来源和 authoritative readiness；所有控制入口及 HTTP 返回值闭环。未接真实实现的作业/轴控/调平禁用，或清楚标记为隔离模拟，不能硬件 ONLINE 后继续冒充实机。 | 无设备启动、只断 TH、HUP/ERR/NVAL、静默拔线、FWD/STATE/DBus 重启、旧快照及同代/异代迟到包；验证进度停止且无假成功。记录从故障触发到失效/拒绝/UI 告警的单调时钟时延与 CPU 样本，不预填“3s/100%”。 |
| 2 重连 | 单 owner 串口状态机：DISCONNECTED→DISCOVERING→HANDSHAKING→READY；固定身份、双节点握手、boot_id 与旧队列隔离、可取消退避。自动恢复通信后仍锁住待对账作业。 | 重插同路径、改设备号、两块同 VID:PID、错误角色/协议、USB 抖动、权限失败、重连同时 query/estop/stop；核 fd/线程泄漏、无死锁、旧回包不使新会话就绪、不自动继续。 |
| 3 真实运动与背压 | 先冻结流式与执行回执、暂停/急停/恢复契约及节点能力；再改 executor 与 FWD 收发/分发。保留单在途、双信用和控制优先级；独立实现并接受 Jog/Home/Leveling 或保持禁用。 | 锁定 AP/MC/TH 的准确服务器版本；真实 Raw Hex TX/RX 对账。覆盖信用归零恢复、队列满 BUSY、丢/重/乱 ACK、CRC 错误、超时重试上限、半包/短写、boot_id/seq 回绕、队列有积压时拔线和急停。验证“无重复执行、无假完成”及实际停止预算。 |

取消预取和优先处理急停不能随意截断一个已经发出的协议帧；须定义最大帧发送和在途事务时长、控制队列优先级及 MCU 独立安全机制。预算需由实际波特率、最大帧、队列深度和测试负载推导，不能用 AP mutex 的可用性替代。

所有新增代码继续执行 ≤50 行 / ≤4 参、指针防御、≤3 层嵌套和嵌入式零堆等既有门禁；不为本提案引入无关重构。

## 6. 三个决策点

| 决策 | QA 建议 | 接受前提 |
| --- | --- | --- |
| 1 拔线 Safe Pause / Fault Abort | **不原样接受 A，也不接受 B 的“复位到 IDLE”。** 立即停止新准入和发送，进入带不确定执行边界的 LINK_LOST/FAULT，保留诊断与最后确认上下文。 | 只有 MCU 已确认停稳且恢复对账成立，才能命名为 Safe Pause 并允许显式继续；无法对账则终止本作业并保持故障，不能靠 AP 清 IDLE 假装机器已停。两选项都需要相同的底层物理安全保障。 |
| 2 端口漂移自动重连 / 原路径重连 | **接受有身份约束的自动重连；拒绝“仅匹配波特率”。** 固定稳定路径可作为部署策略之一。 | 设备唯一身份、角色/协议/能力、boot_id、多设备歧义拒绝、退避和不自动恢复运动。原路径重连可作为范围受限的首步，必须明确能力边界，不称为完整漂移自愈。 |
| 3 先阶段 1 / 合并 1+2 | **建议先阶段 1。** 但先冻结阶段 2 也要使用的 fd owner、epoch 与 readiness 边界，避免止血方案再引入热插拔竞态。 | 阶段 1 全部异常准入/失效传播验收后再释放阶段 2；阶段 3 的真实运动在其固件/契约前置接受前不得启用。 |

以上是 QA 技术建议，不代替用户产品取向、ARCH 契约接受、MC/TH Owner 或唯一 COORD 的派单权限。

## 7. 正式收件阻塞与后续交接

| ID | 当前缺项 | 解除条件 / 负责边界 |
| --- | --- | --- |
| E01 | 准确候选 `409846a5…` 无法从服务器 fetch；提案原件也未绑定已发布文档候选及任务 revision。 | 由 COORD/作者发布准确候选并冻结任务/文档 SHA；QA 从服务器重新取得并核对。不能由 QA 推送作者本地代码来补成已发布事实。 |
| E02 | 缺少同候选独立 Docker checkout/运行及 inspect / server_qa 绑定。 | COORD 按文档审查适用范围提供准确候选独立环境和真实来源证据；未要求本提案先做全部整改的 HIL，但任何实现/HIL结论另需对应实测。 |
| E03 | 缺作者实际会话来源、任务登记/模型例外，以及本 QA 报告的非作者复核。 | 记录真实会话和批准依据；本报告发布后由另一独立会话按其准确 SHA 复核。保留本报告原始字节，不伪造计划会话为完成签署。 |

本次已交付：指定路径报告、原提案副本、26 文件版本/摘要对账、真实服务器查询/候选获取失败日志、实际会话/模型元数据。实际验证层级仅静态架构与源码调查，**没有运行或硬件通过项**。

未完成项是 E01～E03，对应正式验收仍无法签发。当前仅本 Reviewer 会话执行，无其他实际 QA/ARCH agent 或后台调度由本次启动。下一步由现有 COORD 收件并组织提案作者按 B01～B08 修订，补齐 E01～E03 后再安排准确候选复核；本会话未更改任务/看板状态。确需用户处理事项：无，当前不是要求用户再逐项确认技术实现。

**最终裁决：REJECTED（提案原样不可接受）；正式候选验收 BLOCKED / INCONCLUSIVE。** 主要方向可保留，但事实、入队/执行语义、物理停机与恢复边界、并发所有权以及全面准入必须先修订。此裁决不构成代码、部署、硬件或项目收件批准。
