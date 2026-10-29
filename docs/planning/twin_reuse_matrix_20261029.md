---
id: MATRIX-VMWARE-SOC-TWIN-20261029
title: VMware至SoC两阶段孪生资产复用与平台适配矩阵
revision: 1
date: 2026-10-29
status: baselined
author_role: ARCH
task_id: TWIN-01
qa_review_policy: project-control/.agents/rules/codex_qa_review.md
references:
  - project-control/docs/interfaces/vmware_soc_twin_architecture_icd_20261029.md
  - project-control/docs/planning/vmware_soc_twin_development_plan_20261029.md
  - project-control/docs/planning/soc_system_architecture_input_register_20261029.md
---

# VMware至SoC两阶段孪生资产复用与平台适配矩阵

## 1. 复用战略与总体方针

为了彻底消除嵌入式软件开发中“仿真环境写一套、真机移植重写一套”的返工损耗，本项目确立了**“1:1 同构软件架构”**方针。

- **原则**：业务逻辑、进程拓扑、IPC 通信协议与人机交互前端在两阶段中**保持 100% 源码级与契约级复用**。
- **差异隔离**：将底层硬件依赖（串口设备名、编译工具链、启动守护进程配置、显示后端）收敛在专用的构建配置层与适配层，严禁在业务逻辑中编写条件宏分歧。

---

## 2. 核心组件复用与适配明细表

| 资产名称 / 模块 | 归属仓 / 路径 | VMware 第一阶段 (数字孪生) | SoC 第二阶段 (真机迁移) | 复用比例与代码改动预算 | 平台适配点与外部依赖 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **通信契约 (ICD/IDL)** | `project-control/docs/interfaces/` | Fast DDS IDL<br/>D-Bus XML<br/>REST/SSE 契约 | **完全一致，原样复用** | **100% 复用** (0 行改动) | 无。契约作为全阶段单一事实源（Single Source of Truth）。 |
| **forward-service** | `soc-ap/core/forward/` | 独占宿主机串口（如 `/dev/ttyUSB0`），处理 MiniMCProto 事务与 DDS/D-Bus 转换 | 独占 SoC 板载 UART（如 `/dev/ttyS1`），处理相同协议 | **$\ge 95\%$ 源码复用** | 仅通过启动配置文件 (`/etc/aisoc/forward.conf`) 修改串口设备路径与波特率，C++ 源码保持不变。 |
| **device-manager** | `soc-ap/core/state/` | 运行状态机聚合、准入控制、DDS 状态广播与 D-Bus 快照 | 运行完全相同的状态机逻辑与准入控制 | **100% 源码复用** | 无硬件直接依赖，纯逻辑服务。 |
| **ui-gateway** | `soc-ap/core/gateway/` | 监听 HTTP 8080，转换 HTTP ↔ D-Bus/DDS，分发 Web 静态资源 | 监听相同端口或 Unix Domain Socket，执行相同网关功能 | **100% 源码复用** | 可选针对嵌入式资源调整静态文件压缩与缓存策略。 |
| **Browser HMI (前端)** | `soc-ap/ui/` | 运行于外部/宿主机桌面浏览器 (Chrome / Firefox)，连接网关实时推流 | 运行于 SoC 本地 Weston/Wayland 桌面内置的轻量 Kiosk 浏览器或远程 Web | **100% 资产复用** | 界面布局自适应屏幕分辨率；业务交互与 API 路径完全一致。 |
| **MC 固件** | `mcu-p3/mc/` | 运行于真实 MC STM32 单片机，负责热床控温与透明路由 | 保持同一硬件，无需额外变更 | **100% 复用** | 仅针对 C1～C6 终局决议微调 flags (`0x05`/`0x06`) 与 0.1°C 解码。 |
| **TH 固件** | `mcu-p3/th/` | 运行于真实 TH STM32 单片机，负责喷头控温 | 保持同一硬件，无需额外变更 | **100% 复用** | 遵循 C1～C6 终局决议保持与 MC 协议一致。 |
| **构建系统 (CMake)** | `soc-ap/CMakeLists.txt` | 使用 x86_64-linux-gnu 原生 GCC 11+ 编译 | 使用 aarch64-linux-gnu 交叉编译工具链与 SoC sysroot | **构建逻辑 90% 复用** | 增加 `toolchain-aarch64.cmake`，业务 target 声明完全一致。 |
| **进程管理 (systemd)** | `soc-ap/deploy/systemd/` | VMware Ubuntu 用户会话服务或系统守护单元 | SoC 根文件系统标准守护服务 | **服务声明 95% 复用** | 适配不同运行账户 (root/aisoc) 与日志持久化路径。 |

---

## 3. 目标 SoC 资料缺口与解耦策略

在架构登记表（`INPUT-SOC-SYSTEM-ARCH-20261029.md`）中，部分目标 SoC 参数（P01 芯片型号/ABI、P02 BSP/sysroot、U02 屏幕分辨率/GPU 驱动）仍待硬件团队补充。

本复用矩阵确立了**严格解耦策略**：
1. **VMware 阶段不等待 SoC 硬件资料**：
   - 业务逻辑以 POSIX 标准接口、标准 Fast DDS 3.6.x LTS、标准 D-Bus 1.16.x 与标准 HTML5/ES6 为开发基线。
   - 所有通信报文使用固定字节宽度与明确端序定义（大端序/网络序在通信层显式转换），消除 x86_64 与 aarch64 的数据布局分歧。
2. **缺口封闭时间节点**：
   - 目标 SoC/BSP 资料仅在进入 **TWIN-13 (SoC 平台迁移)** 前作为前置开工门卡点。
   - 在完成 TWIN-12（VMware 原生系统与真实 MCU 完整在环验收）之前，任何目标板硬件资料缺失均**不得阻塞 VMware 阶段的研发与交付**。

---

## 4. 两阶段验收与收件边界

| 验收维度 | 第一阶段：VMware 应用孪生验收 (TWIN-12) | 第二阶段：SoC 真机实板验收 (TWIN-14) |
| :--- | :--- | :--- |
| **执行环境** | VMware Ubuntu 22.04 虚拟机 + 真实 MC/TH 硬件链路 | 真实 SoC 开发板 + 真实本地屏幕 + 真实 MC/TH 硬件链路 |
| **验证对象** | 跨进程 IPC、状态聚合算法、Web 前端可见交互、异常断线自愈 | 交叉编译二进制产物、板级驱动加载、GPU/触控响应、系统冷启动时间 |
| **性能基准** | 验证功能语义正确性（Soft Real-time 容许 200ms 抖动） | 严格验证生产资源约束（CPU $\le 15\%$, RAM $\le 128\text{MB}$, RTT $\le 8\text{ms}$） |
| **交付凭证** | 真实浏览器交互录屏/截图、双向 Raw Hex 通信报文、D-Bus/DDS 调用日志 | 板载实拍交互照片/视频、硬件示波器/串口测时数据、资源监测 dump 记录 |

---
*本资产复用矩阵确立了两阶段同构实施路径，已提交 COORD 与相关工程师作为后续开工基准。*
