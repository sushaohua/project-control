# QA 独立审查与验收报告 (TWIN-12 Run 01)

| 审核属性 | 内容 |
| :--- | :--- |
| **任务卡片** | `TWIN-12` (VMware 应用孪生与真实 MCU 独立验收) |
| **所属计划** | `vmware-soc-twin-20261029` |
| **任务轮次** | `run_01` (物理硬件在环真实台架联调与微服务集群部署) |
| **审查角色** | `QA` (独立质量审查员, 会话: `d9426f0b-71a2-4c28-98e3-057bfd19ea12`) |
| **作者角色** | `QA` (系统测试工程师, 会话: `1aba53f3-e424-4e8c-926a-ddfc0d5e44c5`) |
| **沙箱验证** | 容器 ID: `9d001998ad2d` (镜像 Digest: `sha256:acbab225932c...`) |
| **沙箱证据** | `server_qa.json` (SHA-256: `ba18f970fb2e108706aa68656931206f880792582b9d87d3c58901da6f3d2b7a`) |
| **审查结论** | **APPROVED (台架双端物理穿透 100% 成功，时延严格达标，强电恒为 0%，三总线与网关端到端正常)** |

---

## 1. 独立沙箱与远端候选审计 (Sandbox & Server Baseline)

1. **远端发布基线确认**：
   - `soc-ap`: `4c388a439f6df7f76896a062732d51bd0ef27188` (`main`)
   - `mcu-p3`: `d756a13b3c2a1c47186a07311b2c24fa43431465` (`feat/soc-debug`)
   - `test_harness`: `0b7497ba43158841eb3c4af7f16e477b9c30c2c5` (`main`)
   - `project-control`: `9a36f056a1d7cea83d40220fdb9c38d55960b1e7` (`main`)
   全部 Candidate Commits 均严格拉取自远端服务器，未挂载任何开发者本地工作区。
2. **沙箱命令验证结果**：
   - 命令 1 (`verify_hil`): 真实台架 HIL 捕获数据模式核验通过，状态为 `PASS`，HTTP 状态码 200，系统评估为 `NORMAL`；
   - 命令 2 (`check_graph`): 全局任务图拓扑校验通过，0 错误，0 循环依赖；
   - 退出码均严格为 `0`。

---

## 2. 物理台架硬件在环指标独立复核 (HIL Performance Verification)

审查员对 `twin12_acceptance_summary.json`（SHA-256: `90c69857...`）中记录的真实台架测量数据进行了逐项复核：

1. **单跳与双跳通信时延**：
   - **MC 单跳时延**：实测 Monotonic RTT 为 **`7,509 us`** (`7.51 ms`)，处于预期正常范围；
   - **TH 双跳穿透时延**：经 MC 转发实测 Monotonic RTT 为 **`8,490 us`** (`8.49 ms`)，**100% 满足 $\le 10\text{ ms}$ 的硬性设计指标**。
2. **强电安全红线 (Hardware Safety Invariant)**：
   - MC 热床加热占空比: `heater_duty_percent = 0%`；
   - TH 喷头加热占空比: `heater_duty_percent = 0%`；
   - 无任何越权加热指令下发，强电安全约束执行率 100%。
3. **微服务集群管理与 RPC / SSE 验证**：
   - `aisoc_forward_service` 独占物理串口，D-Bus 方法调用回读确认 `tx=2, rx=2` 零丢包；
   - `aisoc_device_manager` 通过 Fast DDS 订阅 `telemetry/raw_temp` 并同步状态，`GetDeviceState` 返回 `IDLE`；
   - 即时采样接口 `POST /api/v1/temperature/sample` 准入仲裁成功，快照世代号由 3 单调递增至 5；
   - 全部服务优雅退出码均为 0。

---

## 3. 审查裁决

审查员确认 `TWIN-12` 满足全部正面验收条件，负面指标（离线、Mock 替代、无响应）全部排除。本票予以 **APPROVED**，同意向 ARCH 及 COORD 移交收件。
