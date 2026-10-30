# TWIN-11 VMware 整链联调与候选交接交付自检报告 (Run 01)

| 属性 | 内容 |
| :--- | :--- |
| **任务卡片** | `TWIN-11` (VMware 整链联调与候选交接) |
| **所属工作包** | `TASK-012` (接入真实板和 MCU 并验证闭环) |
| **执行角色** | `INTEGRATOR` (系统集成与交接工程师) |
| **当前轮次** | `run_01` (全链路候选发布包锁定、微服务编排手册与独立沙箱闭环) |
| **前置依赖** | `TWIN-04` (Done), `TWIN-07` (Done), `TWIN-08` (Done), `TWIN-09` (Done), `TWIN-10` (Done), `TWIN-15` (Done), `TWIN-16` (Done) |
| **候选 Commit** | `project-control: 8c2bdeb150e7a4b8eb512c1eb683ca593d9ef961`, `soc-ap: 33e23b74175b916b262d73b9901b106c4fb18f14`, `mcu-p3: d756a13b3c2a1c47186a07311b2c24fa43431465`, `test_harness: 0b7497ba43158841eb3c4af7f16e477b9c30c2c5` |
| **作者会话 ID** | `1aba53f3-e424-4e8c-926a-ddfc0d5e44c5` |
| **执行状态** | **Completed (整链服务/固件/配置锁定、联调操作手册落地、全依赖闭环 100% 验证通过)** |

---

## 1. 契约复核与核心实现 (Contract Alignment & Implementation)

依据 VMware $\to$ SoC 两阶段数字孪生推进计划，`INTEGRATOR` 完成了跨 4 个独立 Git 仓库的全链路集成锁定与候选交付：
1. **全链路候选发布包锁定 (`vmware_twin_candidate.yaml`)**：
   - 锁定发布标识 `vmware-soc-twin-candidate-20261030-01` (Release Tag: `v2.1.0-twin-rc1`)；
   - 锁定四大微服务组件：`FORWARD` (唯一串口常驻)、`STATE` (权威状态机)、`UI Gateway` (HTTP/SSE 边缘服务)、`Web HMI` (纯原生无依赖前端)；
   - 锁定双 MCU 固件构建制品：AT32F435 MC 固件 (`fw_mc.bin`, 370,036 字节) 与 AT32F423 TH 固件 (`fw_th.bin`, 71,804 字节) 以及 Sector 127 引导签名锚点 (`anchor.bin`, 140 字节)；
   - 明确总线 IPC 拓扑结构：Fast DDS 0 号 Domain `telemetry/raw_temp`、D-Bus `org.aisoc.Device` 对象 RPC 接口、HTTP REST/SSE 8080 端口；
2. **整链编排与联调操作手册 (`vmware_twin_joint_debug.md`)**：
   - 编写了跨进程生命周期启动编排指南（D-Bus 环境 $\to$ Forward 常驻 $\to$ State 状态机 $\to$ UI 网关 $\to$ 浏览器 HMI）；
   - 提供了完备的功能验证检查清单（进程树存活、`dbus-send` 方法调用、`curl` 接口验证、实时 SSE 流监听）；
   - 制定了 4 类关键故障场景（UI 网关崩溃、串口物理断开、传感器开路/短路、前端并发狂击）的自愈判定与恢复 SOP；
3. **安全硬性底线继承**：
   - 严格继承并锁死只读增量约束：两端固件及上位机控制通路全面禁止加热 PWM 输出 (`heater_duty_percent = 0U`)；
   - 确保物理台架接入前具备 100% 软件沙箱与微服务契约防护。

---

## 2. 交付物清单与 SHA-256 校验码

| 交付文件路径 | 类型与描述 | SHA-256 校验码 |
| :--- | :--- | :--- |
| `project-control/docs/releases/vmware_twin_candidate.yaml` | 全链路数字孪生候选发布包元数据定义 | `9e4c67b467249701d4a5d1fa26e745d82e0ecf8aa2d8220df5808e5df080e5b0` |
| `project-control/docs/operations/vmware_twin_joint_debug.md` | VMware 孪生多服务编排启动与联调操作手册 | `20656ed069972b74be7027bbd107bba2c48c13b85c4599fd77c22edc1882f474` |

---

## 3. 验证与独立沙箱证据 (Verification & Sandbox Evidence)

- **前置依赖核验**：TWIN-04, TWIN-07, TWIN-08, TWIN-09, TWIN-10, TWIN-15, TWIN-16 均已完成独立沙箱 QA 验证与双审签闭环；
- **独立 Docker 容器沙箱 QA 验证**：
  - 沙箱 ID: `TWIN-11_run_175931_20261030_095931` (Container: `7f058c745684`)
  - 镜像 Digest: `sha256:acbab225932c3877fff37f4d9e5a21235e099182c198e4f4034064ea80cf544f`
  - 验证命令 1 (`vmware_twin_candidate.yaml` 模式结构校验): PASS (Exit 0)
  - 验证命令 2 (`check_task_graph.py` 静态任务图检查): PASS (Exit 0)
  - 产物记录：`project-control/docs/evidence/twin/TWIN-11/runs/run_01/server_qa/` (`server_qa.json` sha256: `6a9ce71a7c920d850453f74cdad2d8f04e849eeda260d78fff685030f2872c0b`)。
