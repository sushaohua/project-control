---
id: MATRIX-VMWARE-SOC-TWIN-20261029
title: VMware至SoC两阶段孪生资产复用与平台适配矩阵
revision: 2
date: 2026-10-29
status: baselined
author_role: ARCH
task_id: TWIN-01
qa_review_policy: project-control/.agents/rules/codex_qa_review.md
references:
  - project-control/docs/interfaces/vmware_soc_twin_architecture_icd_20261029.md
  - project-control/docs/planning/vmware_soc_twin_development_plan_20261029.md
  - project-control/docs/planning/soc_system_architecture_input_register_20261029.md
  - project-control/manifest.yaml
---

# VMware至SoC两阶段孪生资产复用与平台适配矩阵

## 1. 资产复用方针与“有条件设计目标”原则

> [!IMPORTANT]
> **拒绝无依据的绝对保证**：
> 针对从虚拟机（VMware）到目标嵌入式硬件（SoC）的迁移，本项目确立**“有条件的设计目标（Conditional Design Targets）”**。
> 架构设计通过解耦平台差异，致力于最大化复用核心代码与界面资产；但在目标板硬件资料（芯片、ABI、sysroot、GPU/屏幕驱动）到位并经物理实测之前，**严禁将“100% 源码直接搬移”或“生产硬实时性能”作为无条件的既定保证**。

- **设计目标**：
  - 核心通信契约（IDL/XML）、前端交互资产保持 100% 复用；
  - 业务逻辑代码（`forward-service`、`device-manager`、`ui-gateway`）保持 $\ge 90\%$ 源码级复用；
  - 差异集中收敛在编译配置、设备树节点名称、systemd 服务环境参数与显示后端启动脚本中。

---

## 2. 核心组件复用、芯片对账与任务白名单明细

根据 `project-control/manifest.yaml` 的权威硬件登记，MC 与 TH 采用雅特力（Artery Tek）单片机，而非 STM32。下表准确对账硬件芯片、源码路径与后续任务白名单：

| 资产名称 / 模块 | 真实源码路径 (准确核实) | 硬件载体 / 芯片型号 | VMware 阶段角色 | SoC 迁移设计目标 | 平台适配点与待确认项 | 后续开发任务与唯一写白名单 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **通信契约 (ICD/IDL)** | `soc-ap/contracts/twin/` | 跨平台纯文本/代码 | 契约基线 | 100% 原样复用 | 无硬件依赖；全阶段单一事实源 | `TWIN-02`<br/>`soc-ap/contracts/twin/**` |
| **forward-service** | `soc-ap/core/forward/` | AP 主机 / SoC | 独占宿主机串口 `/dev/ttyUSB0` | 源码复用率 $\ge 90\%$ | 需适配 SoC 实际串口设备路径（如 `/dev/ttyS1`）及波特率配置 | `TWIN-07`<br/>`soc-ap/core/forward/**` |
| **device-manager** | `soc-ap/core/state/` | AP 主机 / SoC | 状态机权威聚合与准入控制 | 源码复用率 $\ge 95\%$ | 纯逻辑服务，无硬件直接依赖；注意 CPU 字节序对齐 | `TWIN-08`<br/>`soc-ap/core/state/**` |
| **ui-gateway** | `soc-ap/core/gateway/` | AP 主机 / SoC | 监听 HTTP 8080，转接 D-Bus/DDS | 源码复用率 $\ge 95\%$ | 需评估嵌入式系统静态资源 gzip 压缩与连接数上限 | `TWIN-09`<br/>`soc-ap/core/gateway/**` |
| **Browser HMI (前端)** | `soc-ap/ui/` | 宿主机浏览器 / SoC 本地屏 | 宿主机 Chrome/Firefox 展现真实数据 | 静态资产 100% 复用 | 需适配目标屏分辨率与触摸屏事件（见 U02 待确认项） | `TWIN-10`<br/>`soc-ap/ui/**` |
| **MC 固件** | `mcu-p3/motion-controller-mcu/` | **AT32F435VGT7**<br/>(雅特力，非STM32) | 负责热床温控与透明路由 (原生运行) | 保持同一硬件与固件架构 | 针对 C1~C6 终局决议修订 0.1°C 解码，保持与 TH 协同 | `TWIN-15`<br/>`mcu-p3/motion-controller-mcu/**` |
| **TH 固件** | `mcu-p3/color-engine-mcu/io_toggle/` | **AT32F423CCT7**<br/>(雅特力，非STM32) | 负责喷头温控采样 (原生运行) | 保持同一硬件与固件架构 | 针对 C1~C6 终局决议修订 0.1°C 解码与超时保护 | `TWIN-16`<br/>`mcu-p3/color-engine-mcu/io_toggle/**` |
| **构建系统 (CMake)** | `soc-ap/CMakeLists.txt` | x86_64 GCC / aarch64 交叉工具链 | 主机编译入口 | 构建逻辑复用 $\ge 80\%$ | 需引入 `toolchain-aarch64.cmake` 与 SoC sysroot 链接库 | `TWIN-04`<br/>`soc-ap/CMakeLists.txt` |
| **进程守护 (systemd)** | `soc-ap/deploy/systemd/` | systemd 用户服务 / 系统守护 | VMware 服务单元 | 模板复用 $\ge 90\%$ | 适配 SoC 目标根文件系统用户组、安全策略与 cgroups 限制 | `TWIN-04`<br/>`soc-ap/deploy/**` |

---

## 3. 目标 SoC 参数待确认项 (P01/P02/U02) 与验证方法

当前开发阶段严格隔离目标硬件未决风险，避免因硬件参数未定阻碍 VMware 阶段的真实软件与通信开发：

```mermaid
flowchart TD
    subgraph Phase1 [第一阶段：VMware 孪生验证 (已隔离未决项)]
        DEV["标准 POSIX / C++17 研发"]
        IPC["真实 Fast DDS / D-Bus / HTTP 跨进程通信"]
        HIL["直连真实 AT32F435 / AT32F423 硬件在环"]
    end

    subgraph Inputs [待硬件/BSP团队补充的输入项]
        P01["P01: 目标 SoC 型号、ABI、RAM 容量"]
        P02["P02: 目标 Linux 内核、sysroot、libc"]
        U02["U02: 目标屏幕分辨率、GPU 驱动、Weston"]
    end

    subgraph Phase2 [第二阶段：SoC 迁移与物理验证 (TWIN-13/14)]
        CROSS["基于准确 sysroot 交叉编译"]
        BOOT["冷启动与内存 RSS 实测"]
        PHYS_TEST["实屏触摸、GPU 渲染与示波器物理测时"]
    end

    Phase1 --> CROSS
    Inputs -.->|"TWIN-13 开工前前置注入"| CROSS
    CROSS --> BOOT --> PHYS_TEST
```

### 待确认项与验证方法明细表

| 编号 | 待确认参数 | 现状与风险点 | 设计假设 (当前依据) | 第二阶段验证方法 (TWIN-13/14) |
| :--- | :--- | :--- | :--- | :--- |
| **P01** | 目标 SoC 芯片、CPU 架构/ABI、RAM 容量 | 芯片型号待定；ABI 存在 64位 aarch64 或 32位 armhf 差异；内存余量未知 | 假设为标准 64位 ARM (aarch64)；通信报文均采用明确的显式宽度（如 `int32_t`）与端序转换宏 | 在真实 SoC 上读取 `/proc/cpuinfo`，使用 `valgrind` / `free -m` 测量实际运行 RSS 内存 |
| **P02** | 目标 Linux 发行版、libc 版本、编译器与 sysroot | 尚未提供 SoC 交叉编译工具链与 sysroot；libc 若为 musl 则需注意头文件差异 | 假设支持 glibc 2.31+ 与 GCC 9+，仅依赖标准 POSIX 与开源中间件 | 建立 Docker 交叉编译环境，执行全量 target 编译并在目标板上挂载运行 smoke 测试 |
| **P03** | 系统启动管理与守护权限 | 根文件系统是否为只读分区；守护进程是否具备 `/dev/tty` 读写权限 | 假设具备标准 systemd 守护环境，服务运行于 `aisoc` 专有账户并属于 `dialout` 组 | 部署 systemd 单元，断电拔插测试自启动与权限拦截，检查 systemd 日志 (`journalctl`) |
| **U01/U02**| 目标屏幕物理尺寸、分辨率、触控与 GPU 驱动 | 屏幕是否支持硬件 GPU 加速；Weston/Wayland 环境下运行 Kiosk 浏览器的内存压力 | 假设分辨率为 $800\times 480$ 或 $1024\times 600$；Web 界面采用流式自适应排版 | 真实屏幕接驳，测试触摸点击延迟、CSS 动画帧率 (目标 30~60 FPS) 及长时间运行内存泄露 |
| **T01** | 生产物理延迟与通信 RTT 指标 | 物理板载 UART 布线抗干扰能力；MCU 任务负载下对 AP 轮询的响应延迟 | 目标设定为单向链路 $\le 3\text{ ms}$，整机 RTT 典型值 $\le 8\text{ ms}$ | 逻辑分析仪/示波器挂接 AP-MC USART2 物理引脚，连续采集 1000 次查询测量高分位 RTT |

---

## 4. 两阶段验收与收件边界

| 验收维度 | 第一阶段：VMware 应用孪生验收 (TWIN-12) | 第二阶段：SoC 真机实板验收 (TWIN-14) |
| :--- | :--- | :--- |
| **执行环境** | VMware Ubuntu 22.04 虚拟机 + 真实 AT32F435/AT32F423 硬件链路 | 真实 SoC 开发板 + 真实目标屏幕 + 真实 AT32F435/AT32F423 硬件链路 |
| **验证对象** | 跨进程 IPC、状态聚合算法、Web 前端可见交互、异常断线自愈 | 交叉编译二进制产物、板级驱动加载、GPU/触控响应、系统冷启动时间 |
| **性能基准** | 验证功能语义正确性（Soft Real-time 容许 200ms 抖动） | 严格验证生产资源约束（结合 P01/P02 确定准确门限，通过实测收件） |
| **交付凭证** | 真实浏览器交互录屏/截图、双向 Raw Hex 通信报文、D-Bus/DDS 调用日志 | 板载实拍交互照片/视频、硬件示波器/串口测时数据、资源监测 dump 记录 |

---
*本资产复用矩阵确立了两阶段同构实施路径与硬件芯片基准，已提交 COORD 与相关工程师作为后续开工基准。*
