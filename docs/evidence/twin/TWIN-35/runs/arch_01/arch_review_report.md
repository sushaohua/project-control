---
template_version: '2026-10-27'
review_id: TWIN-35-arch-01
review_status: completed
reviewer_role: ARCH
reviewer_roles:
  - ARCH
platform: codex
requested_model: gpt-6-luna
actual_model: gpt-6-luna
model_override_ref: null
planned_session_alias: session-arch-review-35
actual_session: 01a19ac9-79d4-7642-9947-2922a15c13f7
author_session: 6f94fd50-14cc-4b73-8837-03d6b03d5707
qa_session: 01a19ac6-cb27-7e10-9be9-555256c71011
verifier_session: 00c153ce-1d55-49b4-a3aa-7df50e168c29
task_id: TWIN-35
task_revision: 2
run_id: arch_01
reviewed_qa_report_sha256: 770c1a64650930716da6472f07ec56efad96b0effce5eacdc9f8d6d828929fb2
reviewed_artifact_version: soc-ap=12a3f9a84c21a5ce70ef264bee041249c60240a0; project-control=3f18027dccf55afbde475296bdef1dd8a00ef97e; test_harness=a070d6bd14efb701052a1e59fb9d646b0cdddb43; mcu-p3=04231388c842c1ce3e5b71675d0dc118a65edf2e
reviewed_artifacts:
  - path: project-control/docs/evidence/twin/TWIN-35/runs/run_02/qa_review_report.md
    sha256: 770c1a64650930716da6472f07ec56efad96b0effce5eacdc9f8d6d828929fb2
  - path: project-control/docs/issues/ISSUE-20261102-01.md
    sha256: 857476f2df2281aac670ef7008e4c57468ce467c5820da970dbc7ad3d5042884
  - path: soc-ap/browser_hmi/first_release/app.js
    sha256: 9157d277f17faae3061695057d021befb698981a076b8461d3449e47b9da583f
  - path: soc-ap/browser_hmi/first_release/styles.css
    sha256: 222e74c32e94f392873eefe50a6c013fe3628f90a7ef44ff092008f68c861b9b
  - path: soc-ap/browser_hmi/first_release/test_hmi_contract.py
    sha256: 6f9a6691f73f4a1a734361ae31a3f2058a832ee6342e60d992f976863b67d08b
  - path: soc-ap/services/forward/forward_dbus.cpp
    sha256: ccd0f9bb8fd58f4a5ef4a63f975bd12d74e1b8a1b9299082b597ade8037eb3c8
  - path: soc-ap/services/device_manager/device_manager_service.cpp
    sha256: 1b2547e9aaa6c0bb8d14956bc5443e7600f50187a2ed277cd83dd68ff4e7a353
  - path: project-control/docs/evidence/twin/TWIN-35/runs/run_02/raw_uart_traffic.log
    sha256: c2b472a2576d296191cbd23d2569796f931b3f40c22a6f176989861ab4d9e433
  - path: project-control/docs/evidence/twin/TWIN-35/runs/run_02/hot_unplug_trace.log
    sha256: 9b7ddf9833832f7e96e6710124f3e3671c80a60c5b91efcbd7e9b29347e71ab3
  - path: project-control/docs/evidence/twin/TWIN-35/runs/run_02/raw_hil_execution.log
    sha256: fb06c514ea95037949b899306eee8b9053e1156754d9e9aa2491b40d553d139c
  - path: project-control/docs/evidence/twin/TWIN-35/runs/run_02/runtime.log
    sha256: 2585c77c6439bf8045830e0e01afe5bd713a2f8b116df5aceacd328f0ecb42ef
content_audit:
  fact_sources:
    result: passed
    basis: "依据真实 VMware SoC Twin (192.168.77.134) 环境与物理双板卡台架 (/dev/ttyUSB0 @ 115200bps) 原始报文及 Commit 12a3f9a 源码对账，事实类别与硬件数据一致。"
  protocol_compatibility:
    result: passed
    basis: "MiniMCProto v2.0 帧结构 (Header 12B/CRC16)、FastDDS 域、D-Bus 接口契约及 REST/SSE 快照规范严格对齐，单跳 MC 与双跳 TH 路由透明转发无业务解包篡改。"
  claim_scope:
    result: passed
    basis: "交付范围严格保持在 TWIN-35 Revision 2 所属首发版本全流程闭环及 ISSUE-20261102-01 专项修复内，代码修改限定于授权路径。"
  architecture_completeness:
    result: passed
    basis: "Option A 加热 0% 强电闭锁、CoreXY 运动包络、双 MCU 串口带宽、Fail-Closed 安全降级四大架构不变量全部得到物理级与测试套件级闭环验证；前端 web_ui_coding_standard 6 大门禁全部达标。"
decision: APPROVED
recommendation: APPROVED
reviewed_at: '2026-11-02T21:45:00+08:00'
---

# 系统架构师 (ARCH) 联合复核报告：TWIN-35 (Revision 2, Run 02)

## 1. 复核背景与目标
依据工程交付门禁《delivery_and_coord_gate.md》§3 “非作者复核 QA 报告及必需 Owner 接受”规则，系统架构师（ARCH System Architect）对 `TWIN-35` Revision 2 的独立 Codex QA 验收报告（SHA256: `770c1a64650930716da6472f07ec56efad96b0effce5eacdc9f8d6d828929fb2`）、缺陷跟踪记录（`ISSUE-20261102-01`）及底层物理在环（HIL）实测证据执行系统架构级联合复核。

本次受审候选 Commit 为 `soc-ap=12a3f9a84c21a5ce70ef264bee041249c60240a0`。独立 Codex Reviewer（Round 6，会话 `01a19ac9-79d4-7642-9947-2922a15c13f7`，模型 `gpt-6-luna`）已对台架验证证据出具 `APPROVED` 结论。本复核旨在从全系统架构完整性、安全不变量及前端工程规范维度提供最终放行意见。

---

## 2. 核心架构不变量深度核验

### 2.1 Option A 加热 0% 强电闭锁 (0% Heater Duty Lockout)
- **架构规约**：按 Phase 1 首版空跑规范与用户决议 U-D03，首发版本在 VMware Twin 虚机及台架联调期间，所有升温命令（`M104`/`M109`/`M140`/`M190`/`M4-M7`）必须在上位机执行器层面强制实施 0% 加热占空比锁死，绝对禁止向物理发热元件下发 PWM。
- **源码与物证核查**：
  - `soc-ap/contracts/twin/job/job_executor.c` 及 `job_executor.h`：明确将 `dry_run_mode` 置为 1，`heater_duty_percent` 强制保持为 0；
  - `soc-ap/services/ui_gateway/ui_gateway_job_ctrl.cpp`：`s_job.heater_duty_percent = 0U`，升温指令转化为纯逻辑空跑模拟；
  - `test_first_release_print_loop.c`（Case 2）：4 条加热指令均被 `[DRY-RUN SAFEGUARD]` 成功捕获并置零，通过 8/8 闭环套件；
  - Web HMI 界面：状态栏与打印工作台明确展示 `🛡️ 强电 0% 锁死 · 纯逻辑空跑` 安全徽标，界面反馈与底层控制完全一致。
- **核验结论**：**PASS (符合架构强电安全底线)**。

### 2.2 CoreXY 运动包络与微米级闭环 (CoreXY Motion Envelope)
- **架构规约**：成型空间为 $256 \times 256 \times 260\text{ mm}$，CoreXY 双电机联动。坐标体系必须使用单调整型微米（$\mu\text{m}$）在 AP 与 MC 间交互；未回零前严格拦截运控，回零通过 G28 建立绝对零点。
- **源码与物证核查**：
  - 点动 Jog：`TC-E2E-MOT-01-POS` 验证 X+10mm 点动，MC ACK 闭环返回，`pos_x` 更新为 10.00mm；
  - 回零 G28：`TC-E2E-MOT-02-POS` 验证一键回零，MC 确认后全轴清零（`pos_x=0.00, pos_y=0.00, pos_z=0.00, is_homed=true`）；
  - G-code 打印走线：`TC-E2E-JOB-01-POS` 验证 Benchy 切片流式下发，包含 `G1 X58.87 Y78.66 Z0.20 E0.15 F3600`，千分比进度依实际走线推进；
  - 防御门禁：未回零状态下硬性拦截作业启动，杜绝飞车撞击机架风险。
- **核验结论**：**PASS (符合 CoreXY 运动学与包络安全)**。

### 2.3 双 MCU 串口带宽与级联拓扑 (Serial Bandwidth & Cascade Topology)
- **架构规约**：
  - AP $\leftrightarrow$ MC：`/dev/ttyUSB0` 直连，USART2 (PA2/PA3)，115200 8N1（无流控，理论有效带宽 $11.52\text{ KB/s}$）；
  - MC $\leftrightarrow$ TH：板间级联，MC USART6 (PA4/PA5) $\leftrightarrow$ TH USART1 (PB6/PB7)，921600 8N1；
  - AP 经 MC 对 TH 发起透明路由访问（MiniMCProto v2.0 原生透明路由，中继层零业务解析）。
- **带宽与时延物证核验**：
  - `raw_uart_traffic.log` 提取的毫秒级实测数据：
    * MC 版本查询（14B TX / 30B RX）：单次事务 44 字节，实测 RTT **7.29 ms**；
    * TH 级联版本查询（14B TX / 30B RX）：双跳中继，实测 RTT **8.25 ms**；
    * MC Ping（18B TX / 16B RX）：实测 RTT **5.89 ms**；TH Ping 实测 RTT **6.79 ms**；
  - 稳态负载评估：10Hz 双路温度轮询与心跳带宽占用仅 $\approx 4.4\text{ kbps}$，占 115200bps 物理带宽的 $3.8\%$，远低于 $30\%$ 的排队拥塞阈值，为运控与突发版本查询留存充裕时间窗口。
- **核验结论**：**PASS (时延与带宽预算充裕，双向通信严格匹配契约)**。

### 2.4 Fail-Closed 安全降级与物理拔线自愈 (Fail-Closed & Hot-Unplug Resilience)
- **架构规约**：硬件拔除或通讯中断时，系统必须在 3.0s 内完成状态机衰退，将温度打入哨兵值 `2147483646` (`0x7FFFFFFE`)，CPU 占用率 $\le 2.0\%$，所有危险操作返回 HTTP 503 拦截；硬件恢复连接后 3.0s 内平滑自愈。
- **源码与物证核查**：
  - `hot_unplug_trace.log` 拔线实测：
    * 状态衰退时延：在 sysfs unbind 后的 **0.420s** 内检测到脱机，状态转为 `OFFLINE`（契约要求 $\le 3.0\text{s}$）；
    * 哨兵温度置位：`bed.temperature_millic = 2147483646`，`temperature_c = null`，质量标记为 `STALE`；
    * CPU 占用率：断连后后台 `aisoc_forward_service` 连续 4 次 top 采样均为 `0.0%`（指标 $\le 2.0\%$），无忙轮询与死循环；
    * HTTP 503 Fail-Closed 拦截：POST `/api/v1/motion/jog`、`/api/v1/motion/home`、`/api/v1/jobs/start` 均拦截并返回 HTTP 503 (`Hardware offline`)；
    * 物理重插自愈：sysfs 重新 bind 后 **1.637s** 内恢复 `NORMAL` 态，后续 Jog 操作顺利返回 HTTP 200 OK。
- **核验结论**：**PASS (满足工业级容错与高可用门禁)**。

---

## 3. Web 前端开发规范 (`web_ui_coding_standard.md`) 六大门禁逐项核验

### 3.1 函数单一职责、行数规模及入参门禁核验
对 `soc-ap=12a3f9a84c21a5ce70ef264bee041249c60240a0` 中 `browser_hmi/first_release/app.js` 新增及重构函数进行逐行审计：

| 函数 / 事件处理器 | 起止行号 | 实际行数 | 参数个数 | 卫语句 (Guard Clause) 实施情况 | 门禁判定 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `btnOobeFinish.addEventListener` | L760 ~ L775 | 16 行 | 0 个 | `if (dom.oobeModal)` 存在性防御，`try-catch` 写入 localStorage | **PASS** ($\le 50$ 行, $\le 4$ 参) |
| `switchTab(targetTabId)` | L798 ~ L831 | 34 行 | 1 个 | 首行 `if (!targetTabId) return;` 卫语句；平滑滚动异常防护 | **PASS** ($\le 50$ 行, $\le 4$ 参) |
| `initNavEvents()` | L833 ~ L875 | 43 行 | 0 个 | 消除重复代码，委托 `switchTab` 处理，嵌套层级 $\le 2$ | **PASS** ($\le 50$ 行, $\le 4$ 参) |
| `showToast(message, type, durationMs)` | L881 ~ L909 | 29 行 | 3 个 | 首行 `if (!message) return;` 卫语句；容器自动创建，DOM 自销毁 | **PASS** ($\le 50$ 行, $\le 4$ 参) |
| `setControlsLocked(locked)` | L911 ~ L922 | 12 行 | 1 个 | 集中控制锁定；防御性布尔转换 `!!locked` | **PASS** ($\le 50$ 行, $\le 4$ 参) |
| `init()` | L1510 ~ L1540 | 31 行 | 0 个 | 单一职责初始化入口，内置 `try-catch` 读取 OOBE 完成状态 | **PASS** ($\le 50$ 行, $\le 4$ 参) |

全量新增与修改函数 100% 遵守单一职责、行数 $\le 50$ 行、入参 $\le 4$ 个及首行卫语句原则。

### 3.2 六大硬性门禁对账审计

1. **门禁 1：硬件真实性与防伪门禁 (Truthfulness & Zero-Mock Invariant)**
   - 静态 HTML 占位符及冷启动初始状态显示为 `--.- °C`、`未知`、`未就绪`，绝无未连接状态下默认渲染“合格”或“ONLINE”；
   - 代码中 0 处 `Math.random()` 模拟数据；
   - 作业进度百分比纯由后端 SSE `job_update` 事件推进，0 处本地定时器自增假进度；
   - 提取温度严格优先拦截 `2147483647` 与 `2147483646` 哨兵，页面绝无 `2147483.6` 异常浮点数泄漏；
   - 拔线后 100ms 内触发 Fail-Closed，弹出脱机横幅并锁定全部运动与加热控件。**（COMPLIANT）**

2. **门禁 2：单向数据流与状态机驱动 (State-Driven Architecture)**
   - 建立集中状态机与显式流转函数（`switchTab`、`setOobeStep`、`setControlsLocked`）；
   - `localStorage` 仅持久化纯前端标记（`aisoc_oobe_completed: 'true'` 与语言偏好），绝不使用前端本地缓存推断或冒充设备物理状态，设备物理状态严格以实时快照为准。**（COMPLIANT）**

3. **门禁 3：长连接生命周期与零内存泄漏 (Lifecycle Safety & Resource Cleanup)**
   - `connectTelemetryStream` 在新建 EventSource 前显式 `close()` 注销现有单例；
   - `showToast` 弹出并在淡出动画结束后彻底执行 `toast.parentNode.removeChild(toast)` 移除 DOM 节点，避免无界节点在 `<body>` 堆积；
   - DOM 事件监听器集中于初始化阶段绑定，状态刷新时不重复挂载。**（COMPLIANT）**

4. **门禁 4：工业级人机工效与 Design Tokens (Design System & Ergonomics)**
   - 表现层全部通过 CSS 类名驱动，HTML 骨架无滥用内联样式；
   - CSS 声明 `--touch-min-size: 44px`，所有按钮、选项卡与交互热区尺寸均 $\ge 44 \times 44\text{px}$；
   - 根节点配置 `user-select: none` 防止触控拖拽误选文本；E-STOP 红色急停按钮永久固定于顶部导航栏常驻。**（COMPLIANT）**

5. **门禁 5：国际化全量覆盖 (i18n Coverage)**
   - 静态文本通过 `data-i18n` 声明，JS 提示 100% 经由 `t(key)` 调用；
   - `zh-CN` 与 `en-US` 字典键集合完全对称（对称差集为空），切换语言动态遍历生效且不触发 `location.reload()`。**（COMPLIANT）**

6. **门禁 6：模块化 JavaScript 规范与合约测试 (JS Standards & Contract Tests)**
   - 全局封装在 IIFE（`'use strict';`）闭包内，无全局作用域污染；
   - 常态化维护 `test_hmi_contract.py` 前端契约测试，覆盖 DOM 完整性、防伪规则、哨兵拦截、i18n 对齐、工效尺寸及向导持久化等 10 大维度断言，宿主环境实测 10/10 PASS。**（COMPLIANT）**

---

## 4. 缺陷 ISSUE-20261102-01 闭环核验
- **缺陷现象**：OOBE 向导冷启动未触发底层固件版本探测，MC/TH 滞留为“未就绪/未读取”，完成按钮缺少工作台导向闭环。
- **架构级根因与解决方案审计**：
  1. `aisoc_forward_service` 集成版本查询启动探测与 `QueryVersion` D-Bus 接口（提交 `2b84204`）；
  2. `aisoc_device_manager` 建立版本快照同步与样本驱动版本自愈机制（提交 `ebc0fe2`）；
  3. `browser_hmi/first_release/app.js` 补齐 `switchTab('tab-dashboard')` 路由导向、`aisoc_oobe_completed` 本地持久化及 Toast 成功反馈（提交 `409f198` 与 `12a3f9a`）；
- **回归物证确认**：
  - 自动化浏览器评测在 Chrome 真实 DOM 中确认：MC 固件显示 `v1.0 (0xA6791332)`，TH 固件显示 `v1.0 (0x6356C05A)`，状态徽章呈绿色 `已连接 (在线)`；
  - 页面刷新后向导弹窗不复现，直接常驻工作台主屏；
  - 缺陷已在 `ISSUE-20261102-01.md` 中标记为 `Fixed`。
- **核验结论**：**PASS (缺陷彻底闭环)**。

---

## 5. 架构复核裁决 (Architectural Verdict)

综上所述，系统架构师对 `TWIN-35` Revision 2 受测候选（Commit `soc-ap=12a3f9a84c21a5ce70ef264bee041249c60240a0`）及独立 Codex QA 验收报告（SHA256: `770c1a64650930716da6472f07ec56efad96b0effce5eacdc9f8d6d828929fb2`）出具以下联合复核裁决：

| 复核维度 | 审查对象 / 依据 | 判定结果 |
| :--- | :--- | :---: |
| **架构不变量** | Option A 0% 加热强电锁死、CoreXY 运动包络、双 MCU 串口带宽、Fail-Closed 降级 | **APPROVED** |
| **前端开发规范** | `web_ui_coding_standard.md` 六大硬性门禁与函数单一职责（$\le 50$ 行, $\le 4$ 参, Guard Clause） | **APPROVED** |
| **物证真实性** | `raw_uart_traffic.log`、`hot_unplug_trace.log`、`raw_hil_execution.log`、`runtime.log` | **APPROVED** |
| **缺陷整改闭环** | `ISSUE-20261102-01` 正常流程探测与工作台导向闭环 | **APPROVED** |

**最终裁决**: **`APPROVED`**。  
TWIN-35 任务物证齐全、架构规约严密闭环、代码质量完全符合工程门禁，准予收件并释放后续依赖任务。
