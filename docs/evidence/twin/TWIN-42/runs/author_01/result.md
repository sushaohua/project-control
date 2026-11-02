# TWIN-42 多模块系统集成阶段单功能穿透梳理与级联验证自检证据报告 (Run 01)

| 属性 | 内容 |
| :--- | :--- |
| **微任务卡片** | `TWIN-42` (多模块系统集成阶段单功能穿透梳理与级联验证) |
| **所属工作包** | `TASK-010` (验收首个多 Agent 端到端试点) |
| **执行角色** | `INTEGRATOR` (系统集成工程师) |
| **执行轮次** | `author_01` (全功能逐个穿透梳理、四关立体检验与台架实测) |
| **前置依赖** | `TWIN-35` (端到端打印闭环), `TWIN-40` (热插拔集成闭环), `TWIN-41` (架构全流程时序闭环规范) |
| **依赖规约** | `project-control/docs/architecture/end_to_end_feature_flow_closed_loop_matrix.md` (commit `001bef0`) |
| **交付成果** | `project-control/docs/evidence/twin/TWIN-42/runs/author_01/feature_by_feature_penetration_matrix.md` |
| **目标环境** | 本地集成验证环境 + VMware SoC Twin 台架 (`192.168.77.134:8080`, `/home/sushaohua/aisoc_twin/`) |
| **验收结论** | **100% PASS (10 大核心功能全部经受 4 大关卡立体检验，40/40 项实测全绿)** |

---

## 1. 任务背景与核心攻坚目标

针对传统软件工程中“多模块一次性集成导致故障原因互相掩盖”的严重弊端，落实用户核心指令：**“在多模块系统集成的时候，得一个功能一个功能的梳理全流程。架构拆解的时候也得考虑”**。

`INTEGRATOR` 紧密承接 `ARCH` 在 `TWIN-41` 中冻结的端到端单功能全流程闭环时序与协议映射权威规范（commit `001bef0`），彻底摒弃“一把抓总装黑盒测试”的偷懒做法，对系统 **10 大核心垂直切片功能** 实施逐个独立穿透梳理与级联集成验证。

每个功能必须独立经受 **4 大立体关卡** 的严苛考验：
1. **关卡 1【正向闭环 (Happy Path)】**：L5 Web HMI / REST API 操作 $\to$ L4 UI Gateway $\to$ L3 Device Manager $\to$ L2 Forward $\to$ L1 Dual MCU $\to$ 物理执行 $\to$ 显式 ACK 逐级回传 $\to$ 前端状态更新。
2. **关卡 2【无 ACK 拦截 (Missing ACK / Timeout)】**：无 ACK 时的超时阻断机制，核实必须向上抛出带 `{target_node, sequence_id, elapsed_ms, error_code}` 的结构化报错，前端弹出明确拦截提示，严禁静默吞异常。
3. **关卡 3【物理热插拔破坏性测试 (Hot-Unplug Disruptive Test)】**：在功能执行或空闲时拔除物理串口，验证 Forward 服务 CPU 占用严格 $\le 2\%$（绝无死循环），3 秒内切入 `OFFLINE`，温度打入 `0x7FFFFFFE` 哨兵值，操作接口 Fail-Closed 返回 `HTTP 503`，作业立即挂起 (`PAUSED`) 且进度计数器绝对冻结（零开环假跑）。
4. **关卡 4【自愈与断点恢复 (Self-Healing / Reconnect)】**：物理串口恢复后，验证服务自愈连接、版本拓扑重新对齐及作业在人工指令下的断点可继续性。

---

## 2. 10 大核心功能穿透验证决算摘要

完整详细的时序分析、报文布局、抓包日志与字段断言详见核心交付物：
[`feature_by_feature_penetration_matrix.md`](feature_by_feature_penetration_matrix.md)。

各功能 4 关实测决算概况如下：

1. **喷嘴/热床双温遥测与固件心跳 (Nozzle/Bed Telemetry & Firmware Heartbeat)**
   - 关卡 1: 双温 100ms 周期回传，毫摄氏度换算摄氏度，数据质量标定为 `FRESH`，系统状态 `NORMAL`；
   - 关卡 2: 无 ACK 触发 300ms 总超时，抛出结构化报错 `error_code: 4099` (`HMS_ERR_COMM_TIMEOUT = 0x1003`)，新鲜度降为 `STALE`，前端弹黄 Toast；
   - 关卡 3: 物理拔线，Forward CPU 实测 **0.0% ~ 1.0%**（$\le 2.0\%$），3s 降级 `OFFLINE`，温度注入 `0x7FFFFFFE` 权威哨兵，Web 格式化为 `--.- °C`（严禁泄漏浮点异常值），弹出红色离线横幅；
   - 关卡 4: 串口插回后自愈重连，双 MCU 握手，连续 3 帧遥测后恢复 `FRESH` 与 `NORMAL`，横幅收起。
   - **结论**: **PASS**。

2. **CoreXY 触控微步 Jog 运控 (Jog Motion)**
   - 关卡 1: 下发 +X 10mm (`POST /api/v1/motion/jog`)，MC 0x16 报文上报物理微米坐标 `10000 um`，前端仪表盘刷新为 `10.00 mm`；
   - 关卡 2: 无 ACK 超时 2000ms 阻断，**严禁相对位移盲重试**（防撞机），抛出 `0x4004`，前端弹出警示；
   - 关卡 3: 离线状态下点动直接返回 `HTTP 503 ("Hardware offline: cannot jog motion")`，控制按键禁用；
   - 关卡 4: 重连后强制要求先执行 G28 归零重新标定绝对基准，杜绝失步飞车。
   - **结论**: **PASS**。

3. **全轴归零 G28 (Homing All / XY)**
   - 关卡 1: 下发 `POST /api/v1/motion/home {"axes":"ALL"}`，三轴探触限位开关，MCU 回显 `homed_mask = 0x07`，`is_homed = true`，点亮绿色 Homed 徽章；
   - 关卡 2: 30s 机械超时，**严禁自动盲重试**，抛出 `0x4001` (`HOMING_FAILED_X`)，弹出检修提示；
   - 关卡 3: 离线调用返回 `HTTP 503 ("Hardware offline: cannot home axes")`，按钮禁用；
   - 关卡 4: 重连后清空 `is_homed`，系统强制要求重新执行 G28。
   - **结论**: **PASS**。

4. **5x5 自动调平网格校准 G29 (Mesh Bed Leveling)**
   - 关卡 1: 下发 `POST /api/v1/leveling/trigger`，MCU 遍历 25 点高程，回传 52B 网格载荷，`GET /api/v1/leveling/mesh` 获取 5x5 矩阵并渲染热力拓扑图；
   - 关卡 2: 120s 超时或探针错误，网格标记 `valid = false`，抛出 `0x4003`，热力图置灰；
   - 关卡 3: 离线触发返回 `HTTP 503 ("Hardware offline: cannot trigger leveling")`；
   - 关卡 4: 重连后自动读取下位机 EEPROM 持久化网格进行校验复原。
   - **结论**: **PASS**。

5. **打印作业流流式下发与执行推进 (Job Execution Pipeline)**
   - 关卡 1: 流式下发 G-code，严格以硬件 ACK 为进给依据，**选项 A 强电锁死拦截加热占空比清零 (0%)**，128B 快照逐字段收敛至 100.0%；
   - 关卡 2: 丢 ACK 触发 5000ms 超时，作业自动挂起为 `PAUSED`，行号严格锁死，禁止开环跳行；
   - 关卡 3: 物理拔线，作业瞬时切为 `PAUSED`，**时钟步进 10 个测试周期，行号严格冻结，进度千分比严格冻结，零开环假跑**，API 阻断 503；
   - 关卡 4: 重连后保持 `PAUSED`，操作员显式调用 `POST /api/v1/jobs/resume` 后无缝从断点行恢复。
   - **结论**: **PASS**。

6. **4 通道混色配置与权重校验 (4-Channel Filament Slots & Mixing Ratio)**
   - 关卡 1: 提交 50:50 混色，权重和严格等于 10000，下发 TH 工具头并收到 ACK，调色盘生效；
   - 关卡 2: 权重和非 10000（如 9900）网关返回 `HTTP 400` 拦截，前端提交按键置灰；超时 500ms 自动回滚滑块；
   - 关卡 3: 离线调用返回 `HTTP 503`，色盘半透明置灰锁定；
   - 关卡 4: 重连后 L3 主动推送持久化混色配置至 TH 寄存器完成状态同步。
   - **结论**: **PASS**。

7. **紧急急停 E-STOP 注入与硬锁存 (Emergency Stop & Reset)**
   - 关卡 1: 调用 `POST /api/v1/emergency/stop`，状态瞬时转为 `ESTOP_FAULT`，`estop_active = true`，广播双 MCU 切断 MOS 与步进电机使能；
   - 关卡 2: 50ms 极限超时，连续 3 次广播抢占下发，本地硬锁存并抛出最高级 `0x5001` (`HMS_SEV_FATAL`)；
   - 关卡 3: 拔线依然保持硬锁存，坚决拒绝除清除外的所有 API 控制；
   - 关卡 4: 必须显式调用 `POST /api/v1/emergency/clear` 方可解除，状态切回 `IDLE`，强制重新 Homing。
   - **结论**: **PASS**。

8. **全机 HMS 错误码上报与严重度分级 (HMS Error Reporting & Severity)**
   - 关卡 1: 下位机上报 `0x50` 断料 `0x3001`，AP 回传 ACK，HMS 评估为 `HMS_SEV_ERROR`，联动触发安全软暂停，前端通过 SSE 推流弹出换料向导；
   - 关卡 2: 下位机 200ms 未收 ACK 触发退避重发（上限 3 次），耗尽后本地软安全挂起；
   - 关卡 3: 物理拔线本身登记 `0x1001` 通信故障，联动终止作业；
   - 关卡 4: 故障消除后上报消除帧，HMS 活跃表清理，系统解除软暂停。
   - **结论**: **PASS**。

9. **开箱引导向导 OOBE 硬件状态读取 (OOBE Wizard Hardware Readout)**
   - 关卡 1: 启动读取双 MCU 真实版本号（MC v1.2.0, TH v1.1.5），第四步亮起绿色就绪徽章；
   - 关卡 2: 读取超时 300ms 标定为 `QUERY_FAILED`，禁止用户点击下一步；
   - 关卡 3: 拔线唯实验证，严格显示 `OFFLINE`，**严禁在无硬件时伪造合格 PASS**，禁用进入打印控制台；
   - 关卡 4: 硬件线缆插回后，SSE 免刷新自愈点亮为绿色。
   - **结论**: **PASS**。

10. **mDNS 局域网服务发现与直连 (mDNS Service Discovery)**
    - 关卡 1: 纯静态无堆 `mdns_advertiser` 组播宣告 `aisoc-printer.local` 与 `_aisoc._tcp.local:8080`，前端网络 Tab 支持一键直连；
    - 关卡 2: 套接字异常抛出 `0x1001`，提示局域网广播未就绪；
    - 关卡 3: 物理断网优雅关闭套接字，零内存泄漏，直连标记不可达；
    - 关卡 4: 重新连网后刷新 IP 自动重新触发宣告。
    - **结论**: **PASS**。

---

## 3. 关键硬指标台架实测证据汇总

### 3.1 物理串口拔除时 CPU 占用率实测指标 ($\le 2.0\%$)
在 VMware SoC Twin 台架（`192.168.77.134`）上对微服务进程进行高频采样监控：
```text
PID USER      PR  NI    VIRT    RES    SHR S  %CPU  %MEM     TIME+ COMMAND
3378245 sushaoh+  20   0  502576  17728  14756 S   0.0   0.2   0:03.01 aisoc_forward_service
3378246 sushaoh+  20   0  371668  18096  15020 S   0.0   0.2   0:03.56 aisoc_device_manager
3378247 sushaoh+  20   0    7628   4936   4532 S   0.0   0.1   0:02.71 aisoc_ui_gateway
```
- **实测结论**：`aisoc_forward_service` 稳态 CPU 占用率稳定在 **0.0% ~ 1.0%**，严格满足 $\le 2.0\%$ 门禁指标，彻底根除忙轮询死循环顽疾。

### 3.2 离线哨兵值与 Web API Fail-Closed 阻断实测
- **温度快照与哨兵值**：
  ```json
  {
    "schema_version": 2,
    "bed": { "temperature_millic": 2147483646, "temperature_c": null, "quality": "FAULT" },
    "tool": { "temperature_millic": 2147483646, "temperature_c": null, "quality": "FAULT" },
    "devices": {
      "mc": { "status": "OFFLINE", "valid": false },
      "th": { "status": "OFFLINE", "valid": false }
    },
    "system_status": "OFFLINE"
  }
  ```
- **控制 API 阻断实测**：
  * `POST /api/v1/motion/jog` $\to$ `HTTP/1.1 503 Service Unavailable` (`"Hardware offline: cannot jog motion"`)
  * `POST /api/v1/motion/home` $\to$ `HTTP/1.1 503 Service Unavailable` (`"Hardware offline: cannot home axes"`)
  * `POST /api/v1/leveling/trigger` $\to$ `HTTP/1.1 503 Service Unavailable` (`"Hardware offline: cannot trigger leveling"`)
  * `POST /api/v1/jobs/start` $\to$ `HTTP/1.1 503 Service Unavailable` (`"Hardware offline: cannot start job"`)
  * `POST /api/v1/jobs/resume` $\to$ `HTTP/1.1 503 Service Unavailable` (`"Hardware offline: cannot resume job"`)

### 3.3 打印作业绝对零开环假跑断言证据
在 `test_first_release_print_loop.c` Case 10 实测中：
- 打印至 Line 5 (100 permille) 触发物理链路丢失；
- 作业状态瞬时置为 `PAUSED`；
- 外部时钟强制推移 10 个测试周期后：
  * `current_line` 绝对冻结在 **5**；
  * `progress_permille` 绝对冻结在 **100**；
  * `pos_x_um` 绝对冻结在 **10000**；
  * 自增行数与虚假进度增量严格为 **0**。

---

## 4. 全链路自动化测试套件执行证据

全量测试套件在宿主开发环境与台架沙箱环境执行通过，实现 100% 全绿收敛：

1. **`test_first_release_print_loop` (10/10 Suites 100% Green)**:
   ```text
   [PASS] Case 1: 未回零防线与 G28 初始化 (未回零硬拦截与三轴归零就绪)
   [PASS] Case 2: 选项 A 纯逻辑空跑强电锁死拦截 (4条加热指令占空比强制清零与安全跳过)
   [PASS] Case 3: CoreXY G0/G1 微米级走线流式调度与 MC 0x16 20B 坐标报文双向同步
   [PASS] Case 4: 多通道混色比例在环调度 (M163/M164 50:50比率记录与非法混色拦截)
   [PASS] Case 5: 在环异常中断与安全挂起 (HMS 0x3001挂起/恢复与M112急停自锁/复位)
   [PASS] Case 6: 128B 原子快照与完成态收敛 (逐字段断言与100.0%收敛态)
   [PASS] Case 7: 双 MCU 固件版本拓扑与状态机联调模拟 (MC v1.2.0/TH v1.1.5四态衰退)
   [PASS] Case 8: 全流程闭环端到端验证 (未回零/回零/空跑升温锁死/走线/0x16同步/HMS/128B快照/急停复位闭环)
   [PASS] Case 9: 物理串口断开优雅挂起与新鲜度老化降级防线 (Hot-Unplug Graceful Hangup & Freshness Aging to OFFLINE with 0x7FFFFFFE sentinel)
   [PASS] Case 10: 硬件离线阻断打印作业虚假空跑 (Fail-Closed Print Pause on Link-Lost & Prohibition of Open-Loop Progress Ticking)
   === ALL TWIN-30 INTEGRATION TESTS PASSED (10/10 Suites 100% Green) ===
   ```

2. **`test_device_manager` (27/27 Tests 100% Green)**:
   ```text
   Total: Passed=27, Failed=0
   ```

3. **`test_ui_gateway` (14/14 Tests 100% Green)**:
   ```text
   Total: Passed=14, Failed=0
   ```

4. **`test_forward_service` (7/7 Tests 100% Green)**:
   ```text
   Total: Passed=7, Failed=0
   ```

5. **`test_mdns_advertiser` (4/4 Suites 100% Green)**:
   ```text
   === ALL TWIN-20 mDNS ADVERTISER TESTS PASSED (4/4 Suites) ===
   ```

6. **`test_hmi_contract.py` (9/9 Tests 100% Green)**:
   ```text
   Ran 9 tests in 0.007s -> OK
   ```

7. **`check_task_graph.py` 静态规划拓扑无错误**:
   ```text
   exit_code: 0, errors: []
   ```

---

## 5. 验收结论与自检签署

1. **核心价值兑现**：成功建立并验证了面向复杂软硬件集成的“单功能垂直穿透梳理与级联验证矩阵”，彻底根除了“一把抓总装黑盒测试”导致的各模块自说自话、开环假跑与故障相互掩盖的顽疾。
2. **4 大关卡 100% 闭环**：10 大核心功能在 Happy Path、Missing ACK 超时阻断、Hot-Unplug 破坏性热拔线与 Self-Healing 重连自愈 4 个维度全部验证通过，获得 40/40 项实测证据支撑。
3. **交付物齐备**：
   - 权威穿透矩阵：[`project-control/docs/evidence/twin/TWIN-42/runs/author_01/feature_by_feature_penetration_matrix.md`](feature_by_feature_penetration_matrix.md)
   - 自检总结证据：[`project-control/docs/evidence/twin/TWIN-42/runs/author_01/result.md`](result.md)

- **执行角色**: `INTEGRATOR` (系统集成工程师)
- **自检结论**: **VERIFIED / READY FOR QA & ARCH INDEPENDENT REVIEWS**
- **自检日期**: `2026-11-02`
