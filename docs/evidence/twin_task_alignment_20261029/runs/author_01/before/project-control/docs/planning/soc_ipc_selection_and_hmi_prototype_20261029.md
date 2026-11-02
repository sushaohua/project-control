# SoC D-Bus / DDS 版本选型与模拟屏幕提案

日期：2026-10-29。范围：用户要求的版本推荐与浏览器交互屏幕原型；本文件为选型提案，不修改当前架构、任务状态、系统总线或设备部署。

**后续用户方向更新**：用户进一步明确[VMware→SoC两阶段应用孪生开发](vmware_soc_twin_development_plan_20261029.md)。第一阶段需有对接真实模块、目标进程与IPC的可见显示；本文件第3节离线原型只保留为界面布局参考，不满足该阶段交付。进程管理与真实总线也需第一阶段实现和验证。

## 1. 建议与前置

| 对象 | 建议 | 使用条件 |
| --- | --- | --- |
| 新目标 Linux 根文件系统中的 D-Bus 参考实现 | 以稳定线 **1.16.x** 为候选，当前查到 **1.16.2**；优先使用目标发行版/BSP维护的软件包及安全补丁 | D-Bus 服务实现版本与线缆协议/接口版本是不同对象；没有 target rootfs/sysroot 前不能冻结最终包版本。不要为原型替换开发机系统总线 |
| 当前 VMware Ubuntu 环境 | 先沿用发行版维护的 D-Bus 包 | 旧上游版本号不等于发行版没有安全回补；按该发行版支持情况和包来源核实，不能直接套用上游 EOL 判断系统包 |
| D-Bus API | Linux服务已有systemd时评估 **sd-bus**；若屏幕最终用Qt，UI层评估 **QtDBus**；已有GLib服务可用GDBus | 以sysroot依赖和进程布局决定，绑定库版本跟随相应systemd/Qt/GLib，不能将这些库统称为dbus-1.16.2；避免在业务层直接操作低层libdbus |
| DDS 主选 | **eProsima Fast DDS 3.6.x LTS**，当前查到 **3.6.2** | 延续项目已有Fast DDS规划。锁定准确tag、编译器、依赖、配置和工具；不把LTS或可靠QoS解释成硬实时/零堆/物理动作恰好执行一次 |
| IDL生成器 | 与3.6线配套的 **Fast DDS-Gen 4.3.x**，官方当前列出 **4.3.0** | 在构建主机生成，生成器与IDL、输出、编译库共同锁版本；生成工具不必部署在目标板 |
| DDS兼容性备选 | 仅当目标BSP/现有依赖约束需要时评估 **Fast DDS 2.14.x LTS**，当前查到2.14.7 | 新工程优先评估3.6；2.x与3.x接口迁移和生成器要单独核对，禁止把其生成文件/库混用 |

目标板型、CPU ABI、内存、libc、编译器和sysroot尚未在本提案核实。本次不承诺目标SoC可直接运行所推荐版本。Fast DDS 3.6官方构建依赖表列CMake最低3.28，当前soc-ap README最低3.16，两者要求不同；构建基础设施可单独升级/提供工具链，不能仅改README就宣称兼容。

## 2. 官方来源与核对范围

- [D-Bus官方说明](https://wiki.freedesktop.org/www/Software/dbus/)：1.16.x为稳定线，推荐优先发行版包；1.17.x为开发线。
- [D-Bus官方发行目录](https://dbus.freedesktop.org/releases/dbus/)：本次查到1.16.2稳定发行包。
- [D-Bus绑定选择](https://wiki.freedesktop.org/www/Software/DBusBindings/)和[API设计指南](https://dbus.freedesktop.org/doc/dbus-api-design.html)：建议使用GDBus、sd-bus、QtDBus等，低层libdbus不适合大多数业务直接使用。
- [Fast DDS当前支持周期](https://github.com/eProsima/Fast-DDS/blob/master/RELEASE_SUPPORT.md)：当前3.6.x LTS列3.6.2；标准支持到2028-03，EOL到2031-05；3.4.x已EOL。支持周期可能变化，正式冻结前重新核对。
- [Fast DDS-Gen配套表](https://github.com/eProsima/Fast-DDS-Gen/blob/master/RELEASE_SUPPORT.md)：3.6配套4.3.x，当前列4.3.0。
- [Fast DDS 3.6依赖与平台表](https://fast-dds.docs.eprosima.com/en/stable/notes/versions.html)：构建版本和平台要求。正式使用应锁3.6.2对应文档及源码，不用滚动master替代tag。

本次只做官方资料核查，未安装中间件、未交叉编译、未测RSS/CPU或端到端延迟。历史独立查询CLI可用于诊断；后续两阶段孪生交付应按TASK-013/014/015接受并实际运行所选D-Bus/DDS通道，与显示和业务服务共同验收，不能以同进程回调或临时CLI轮询替代目标服务架构。

## 3. 已交付的浏览器交互原型

[模拟屏幕](../../../artifacts/soc_hmi_simulator_20261029/index.html)及[使用说明](../../../artifacts/soc_hmi_simulator_20261029/README.md)。用户选择“浏览器交互原型”；直接打开index.html，保持style.css和app.js同目录，无依赖安装、服务器或外部网络请求。

界面显示双端温度、数据质量、接收后年龄、连接拓扑、有效样本趋势及模拟事件。五种场景：正常、TH过期、TH传感器故障、链路断开、AP进程重启；也可暂停采样观察数据自然过期。恢复需要新的有效样本；重启清空旧快照，代次增加。

所有数据在浏览器内模拟，明确标注未接AP/MC/TH。无D-Bus、DDS、串口、加热或运动接口。演示的1Hz、3秒陈旧期限、1.5秒重启等待及温度曲线不是生产参数。该原型不满足HIL、不证明真实传感器或物理安全，不能据此关闭已有验收任务。

后续UI/STATE Owner确认信息层级和快照API后再选择Qt/QML或其他实际部署方式。真实屏分辨率、触控、字体、帧率和目标SoC资源预算待硬件/BSP输入；浏览器布局不作为实屏验收。
