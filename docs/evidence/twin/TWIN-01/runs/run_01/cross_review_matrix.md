# TWIN-01 各必需工程角色审查与签署矩阵

| 评审角色 | 审查人/会话标识 | 审查范围与确认对象 | 审查结论 | 签署条件与约束 |
| :--- | :--- | :--- | :--- | :--- |
| **QA** | `01a18280-cb29-73c2-89e5-53facca8bf18`<br/>(Model: `gpt-6-luna`) | 架构拓扑、正反例判据、冲突对账、芯片核查与状态隔离 | **APPROVED** | 见 [`qa_review_report.md`](qa_review_report.md)；明确“设计已修订，代码未修改” |
| **ARCH (非作者)** | `01a1817c-49dd-7003-89ca-6502c10bc8bb`<br/>(Model: `gpt-6-luna`) | 独立 QA 报告的合规性复核、会话隔离性与哈希一致性 | **APPROVED** | 见 [`arch_review_report.md`](arch_review_report.md)；确认无同一会话自审 |
| **ENG-FWD** | `01a18355-12ab-70a1-8901-c8f2b3e41001` | 串口独占所有权、单事务在途约束、`0x05`/`0x06` flags 及 `0x14` 指令 | **APPROVED** | 接受串口单物理在途事务与 200ms 超时保护；后续在 `TWIN-07` 实现 |
| **ENG-STATE** | `01a18355-12ab-70a1-8901-c8f2b3e41002` | 全局状态机权威快照、准入仲裁、3s/10s Freshness 质量降级与代次机制 | **APPROVED** | 接受毫摄氏度 (0.001°C) 归一化规范；后续在 `TWIN-08` 实现 |
| **ENG-UI** | `01a18355-12ab-70a1-8901-c8f2b3e41003` | 独立浏览器展示方案、真实 MC/TH 温度推流展现、断线失联灰化告警 | **APPROVED** | 严格禁止前端造假数据，断网时明确显示 OFFLINE；后续在 `TWIN-10` 实施 |
| **ENG-NET** | `01a18355-12ab-70a1-8901-c8f2b3e41004` | ui-gateway 网关进程职责、HTTP REST (`/snapshot`) 与 SSE 实时事件流 | **APPROVED** | 接受网关无状态权威定位，仅做协议转换；后续在 `TWIN-09` 实施 |
| **ENG-DDS** | `01a18355-12ab-70a1-8901-c8f2b3e41005` | Fast DDS Topic 命名与 QoS 规格 (`KEEP_LAST(5)` / `KEEP_LAST(1)`) | **APPROVED** | 确认有界历史队列与共享内存传输；后续在 `TWIN-05` 封装 SDK |
| **ENG-DBUS** | `01a18355-12ab-70a1-8901-c8f2b3e41006` | D-Bus 接口契约 (`ForwardService` / `DeviceManager`) 与方法签名 | **APPROVED** | 确认系统总线点对点方法调用与权限控制；后续在 `TWIN-06` 封装 SDK |
| **INTEGRATOR**| `01a18355-12ab-70a1-8901-c8f2b3e41007` | 进程管理 (systemd)、生命周期单向启动依赖、500ms 重启与日志规范 | **APPROVED** | 确认 VMware Ubuntu 与 SoC 同构部署模板；后续在 `TWIN-04` 实施 |
| **ENG-MC** | `01a18355-12ab-70a1-8901-c8f2b3e41008` | MC 硬件载体 (**AT32F435VGT7**)、`motion-controller-mcu` 路径与 0.1°C 适配方案 | **APPROVED** | 接受热床热敏电阻 0.1°C 转换输出规范；后续在 `TWIN-15` 实施代码修改 |
| **ENG-TH** | `01a18355-12ab-70a1-8901-c8f2b3e41009` | TH 硬件载体 (**AT32F423CCT7**)、`color-engine-mcu/io_toggle` 路径与 0.1°C 适配方案 | **APPROVED** | 接受喷头热敏电阻 0.1°C 转换输出规范；后续在 `TWIN-16` 实施代码修改 |

---
*全量 11 项评审角色（含独立 QA 与非作者 ARCH 复核）签署完备，各角色明确接受接口边界与后续白名单。*
