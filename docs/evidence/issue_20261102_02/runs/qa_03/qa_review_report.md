---
template_version: '2026-10-27'
review_id: REVIEW-ISSUE-20261102-02-QA-03
review_status: completed
reviewer_role: QA
reviewer_roles: [QA]
platform: codex
requested_model: gpt-6-luna
actual_model: gpt-6-luna
planned_session_alias: codex-qa-issue-20261102-02-qa03
actual_session: codex-qa-issue-20261102-02-qa03
verifier_session: d6f1585b-01ca-4fc2-b853-135e58f88490
integrator_session: b322c0f5-b370-4ed0-bc7b-0c5fc6343606
author_session: 8d4e8b77-42a9-4bd3-bd5a-1b881e8d4bd5
task_id: TASK-QA-03
task_revision: ISSUE-20261102-02
reviewed_artifact_version:
  project_control_commit: 5f71cbecee7e106328325d3581d2e942a730b9dc
  mcu_p3_commit: 31a7c6891264ac154c421eaead77c4e4d23acd3e
  soc_ap_commit: 92a6d4076f3b18d86c40fef8de59cd564df4eb63
  test_harness_commit: 1bb89a3955f806cd3a55dc89a6f2007a92657615
server_qa:
  path: project-control/docs/evidence/issue_20261102_02/runs/qa_03/server_qa/server_qa.json
  sha256: 06173acba8fb4851f01303e120dbb5553630a8453a9b7ccb642ad44c87c0949e
reviewed_artifacts:
  - path: project-control/docs/evidence/issue_20261102_02/runs/qa_03/server_qa/server_qa.json
    sha256: 06173acba8fb4851f01303e120dbb5553630a8453a9b7ccb642ad44c87c0949e
  - path: project-control/docs/evidence/issue_20261102_02/runs/qa_03/server_qa/server_verdict.json
    sha256: 83a1edf4ecb09a91dfc3239a4d6e25ea4df39576fbd68563dcad94d84f5a1e33
  - path: project-control/docs/evidence/issue_20261102_02/runs/qa_03/server_qa/runtime.log
    sha256: 641123f0be6db4acbcde03cefae85e8f975057c65e20da0dad6a5e51d2bdec9c
  - path: mcu-p3/motion-controller-mcu/build/fw_mc.bin
    sha256: d738bbd82d0f6d42840d0194ae661348faf68328a22a5f203c3b96a11d503d9b
  - path: mcu-p3/color-engine-mcu/io_toggle/build/fw_th.bin
    sha256: deee2c9b5051dc8b42be3721c8ba4196ada9c511a9afc8c4bf5d40810fb93529
  - path: mcu-p3/color-engine-mcu/io_toggle/build/anchor.bin
    sha256: 14a451cf80f0cc4e53af012e1437c9d79f7e801bbbdda696d2203dd732f17a76
  - path: project-control/docs/evidence/issue_20261102_02/runs/qa_03/raw_capture/probe_flash.log
    sha256: 810c8185deb0fe339c40b0cf1e075fd414b1246cc16cdb37b50a5bf623fa9cdd
  - path: project-control/docs/evidence/issue_20261102_02/runs/qa_03/raw_capture/uart_frames.log
    sha256: ab2e0e380b961bf90c15e29a9a06d9d4febd1875c0fe17a8efba0039be8da8c1
  - path: project-control/docs/evidence/issue_20261102_02/runs/qa_03/raw_capture/temperature_snapshot.json
    sha256: d3bb595cfa17df8d2d02bb8150915f30cf11b51af1c23e3d27a4233084094f12
  - path: project-control/docs/evidence/issue_20261102_02/runs/qa_03/raw_capture/TC-E2E-OOBE-01-POS_step3_versions.png
    sha256: e0cd9f615bc43e150d813a54a47cc10888e1e4ab51206165a39339526d7f46d4
protocol_and_expectations:
  - doc: project-control/.agents/rules/c_cpp_coding_standard.md
  - doc: project-control/.agents/rules/delivery_and_coord_gate.md
  - doc: project-control/.agents/rules/codex_qa_review.md
  - doc: project-control/docs/issues/ISSUE-20261102-02.md
verification_environment: server-sandbox-and-physical-hil
verification_scope: Dual MCU firmware version 2.0.1 closed-loop verification combining server-locked Docker sandbox build/test (server_qa.json), physical probe-rs SWD flashing (probe_flash.log), reconciled raw UART Hex traffic (uart_frames.log), and browser E2E cold-start tests (unblocking ISSUE-20261102-02)
required_evidence_level: server-sandbox-and-physical-hil-verified
review_time: '2026-11-02T16:55:00+08:00'
process_audit: passed
result_check: passed
decision: APPROVED
accepted_scope: Full server-sandbox and hardware-in-the-loop firmware version 2.0.1 closed loop under ISSUE-20261102-02
limitations:
  - boot_id (MC: 0x01020304, TH: 0x8877AA55) is currently a compile-time static placeholder constant in minimc_proto.c; dynamic generation/session reboot isolation is deferred to a future hardware TRNG milestone.
unexecuted: []
not_applicable: []
issues: []
---

# 独立 QA 物理在环与端到端版本闭环验收报告 (Run QA-03)

## 1. 审查基本信息与独立性声明

- **任务编号**：`TASK-QA-03` (Reconciled Server Sandbox & Physical HIL Verification)
- **关联 Issue**：`ISSUE-20261102-02` (解除历史 `BLOCKED` 状态并达成终审闭环)
- **执行环境**：受控 Docker 独立沙箱 (`qa-sandbox:20261029`) + VMware Twin 虚拟机 (`192.168.77.134:8080`) + 物理双 AT32 MCU 台架 (`/dev/ttyUSB0` 115200 8N1)
- **集成与烧录工程师**：`INTEGRATOR` (`b322c0f5-b370-4ed0-bc7b-0c5fc6343606`)
- **QA 自动化工程师**：`QA` (`d6f1585b-01ca-4fc2-b853-135e58f88490`)
- **派发协调**：COORD (`8d4e8b77-42a9-4bd3-bd5a-1b881e8d4bd5`)
- **独立审查会话**：Codex Reviewer Session (`codex-qa-issue-20261102-02-qa03`)
- **独立性声明**：本评审员未参与代码编写或固件打包，严格基于已推送到 GitLab 服务器的锁定 Commit 检出物证、受控 Docker 沙箱构建物证 (`server_qa.json`)、物理探针烧录物证 (`probe_flash.log`)、硬件串口原始双向 14B/30B Hex 交互报文 (`uart_frames.log`) 与无头 Chrome CDP 自动化端到端测试物证进行第三方独立质量验收。

---

## 2. 服务器锁定候选与受控 Docker 沙箱核验 (`server_qa.json`)

依据 `delivery_and_coord_gate.md` 规范，所有源码候选已确定性推送到 GitLab 远端服务器并通过 `qa_runner.py` 在受控隔离容器中完成全量静态断言与测试构建：

1. **GitLab 远端服务器锁定候选 Commit**：
   - `mcu-p3`: `31a7c6891264ac154c421eaead77c4e4d23acd3e` (`refs/heads/feat/soc-debug`)
   - `soc-ap`: `92a6d4076f3b18d86c40fef8de59cd564df4eb63` (`refs/heads/main`)
   - `test_harness`: `1bb89a3955f806cd3a55dc89a6f2007a92657615` (`refs/heads/main`)
   - `project-control`: `5f71cbecee7e106328325d3581d2e942a730b9dc` (`refs/heads/main`)
2. **Docker 沙箱隔离与运行时 Inspect 物证**：
   - 容器 ID：`b3d64c347ac90c675dc97882f1947f242cfa988c49941467695a9dfa54cfbf78`
   - 镜像 Digest：`sha256:acbab225932c3877fff37f4d9e5a21235e099182c198e4f4034064ea80cf544f`
   - 挂载模式：只读挂载 (`Mode: ro, RW: false`)
   - 判定结果：`server_verdict.json` 返回 `PASSED` (Exit Code 0, 4/4 套件全通)
   - 物证引用：`server_qa/server_qa.json` (SHA256: `06173acba8fb4851f01303e120dbb5553630a8453a9b7ccb642ad44c87c0949e`)

---

## 3. 固件标识与 HIL 闭环对账门禁 (HW-G7 对照表)

依据 `codex_qa_review.md` 第 6 条 HW-G7 门禁规范，对双板源码、制品哈希、期望标识、现场实际回显及代次限制逐项登记对账：

| 节点/芯片及板卡身份 | 锁定完整源码commit | 固件SHA256 | 期望构建标识及映射依据 | 现场返回标识 | boot_id及能力/限制 | 实际RTT与样本引用 | 部署/收发证据引用 | 判定 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **MC 运动控制**<br>(AT32F435VGT7, Node 2) | `31a7c6891264ac154c421eaead77c4e4d23acd3e` | `d738bbd82d0f6d42840d0194ae661348faf68328a22a5f203c3b96a11d503d9b` | 期望: `0xA6791332`；依据: `mcu-p3/motion-controller-mcu/project/src/minimc_proto.c` L233 映射 | `proto: 2.0`<br>`fw: 2.0`<br>`commit: 0xA6791332` | `boot_id`: `0x01020304` (16909060)。**限制项**：固件当前为静态占位常量，未实现硬件真随机动态代次生成，已登记限制项。 | `7.42 ms`<br>(样本引用: `raw_capture/uart_frames.log` Seq 1) | 烧录: `raw_capture/probe_flash.log`<br>协议: `raw_capture/uart_frames.log` | **MATCH**<br>(限制项已确认) |
| **TH 工具头**<br>(AT32F423CCT7, Node 3) | `31a7c6891264ac154c421eaead77c4e4d23acd3e` | `deee2c9b5051dc8b42be3721c8ba4196ada9c511a9afc8c4bf5d40810fb93529` | 期望: `0x6356C05A`；依据: `mcu-p3/color-engine-mcu/io_toggle/src/app/minimc_proto.c` L24 宏定义映射 | `proto: 2.0`<br>`fw: 2.0`<br>`commit: 0x6356C05A` | `boot_id`: `0x8877AA55` (2289543765)。**限制项**：固件当前为静态占位常量，未实现硬件真随机动态代次生成，已登记限制项。 | `8.62 ms`<br>(样本引用: `raw_capture/uart_frames.log` Seq 2) | 烧录: `raw_capture/probe_flash.log`<br>协议: `raw_capture/uart_frames.log` | **MATCH**<br>(限制项已确认) |

---

## 4. 物理固件 SWD 烧录与芯片复位物证 (probe-rs)

依据 `DOC-HIL-FAULT-INJECTION-20261027` 规范，通过宿主机 `probe-rs.exe` SWD 探针对双板执行物理直刷（完整控制台记录见 `raw_capture/probe_flash.log`）：

1. **从控 TH 工具头 (`AT32F423CCT7`, 探针 `0483:3748:`)**：
   - 固件：`fw_th.bin` (71,804 字节, SHA256: `deee2c9b5051dc8b42be3721c8ba4196ada9c511a9afc8c4bf5d40810fb93529`) 刷入 `0x08004000` (`--verify`)，耗时 5.23s，逐字节物理回读一致。
   - 锚点：`anchor.bin` (140 字节, SHA256: `14a451cf80f0cc4e53af012e1437c9d79f7e801bbbdda696d2203dd732f17a76`) 刷入 `0x0803F800` (`--verify --reset`)，耗时 0.32s，硬件复位释放 CPU。
2. **主控 MC 运动控制 (`AT32F435VGT7`, 探针 `0483:3748:75003800120000334C41534E`)**：
   - 固件：`fw_mc.bin` (371,260 字节, SHA256: `d738bbd82d0f6d42840d0194ae661348faf68328a22a5f203c3b96a11d503d9b`) 刷入 `0x08020000` (`--verify --reset`)，耗时 29.60s，逐字节物理回读一致，拉低 nRESET 成功复位。

---

## 5. 物理串口真实双向 Hex 报文与对账核验 (/dev/ttyUSB0)

在 VMware Twin 环境下独占抓取物理串口交互报文（完整报文记录见 `raw_capture/uart_frames.log`）：

### 5.1 节点编号与帧结构规范对账说明
1. **节点编号对账**：
   - **D-Bus 逻辑节点索引**：`1 = MC, 2 = TH`（由 `aisoc_forward_service` 暴露给 `device_manager` 的 D-Bus `QueryVersion` 接口定义）。
   - **物理总线地址**：`0x01 = AP, 0x02 = MC, 0x03 = TH`（由底层 MiniMCProto v2.0 物理链路规范定义）。
   - **映射逻辑**：D-Bus 查询 `target=MC(1)` 会下发物理线网目的地址 `DST=0x02`；D-Bus 查询 `target=TH(2)` 会下发物理线网目的地址 `DST=0x03`。两者为分层映射关系，完全一致。
2. **14 字节请求帧结构逐字节解析**（针对 `check_layout.c` 与 `telemetry_types.h`）：
   - `Offset 0..1`: `0x55 0xAA` (SOF 帧头)
   - `Offset 2`: `0x01` (SRC=AP)
   - `Offset 3`: `0x02` (DST=MC) 或 `0x03` (DST=TH)
   - `Offset 4`: `0x05` (FLAGS, 请求帧)
   - `Offset 5`: `0x01` (CMD_GET_VERSION)
   - `Offset 6`: `0x04` (**HOP_LIMIT = 4**，非载荷长度)
   - `Offset 7`: `0x00` (**ROUTE_CTRL = 0**，非载荷长度)
   - `Offset 8..9`: `0x0001` (SEQ = 1，小端 `01 00`)
   - `Offset 10..11`: `0x0000` (**PAYLOAD_LEN = 0**，小端 `00 00`，**PLEN 确定性为 0**)
   - `Offset 12..13`: CRC-16/CCITT-FALSE 校验和
   - 证明：请求帧总长恰为 $12\text{B(Header)} + 0\text{B(Payload)} + 2\text{B(CRC)} = 14\text{ 字节}$。

### 5.2 MC 主控 (Physical Wire Node 2) Get Version 物理交互
- **时间戳**：`2026-11-02 16:54:43.175726+0800`（物理烧录后采集）
- **TX Frame (14B)**: `55 AA 01 02 05 01 04 00 01 00 00 00 4D 68`
  - SOF=`0x55AA`, SRC=`0x01`, DST=`0x02`, CMD=`0x01`, HOP=`0x04`, RCTRL=`0x00`, SEQ=1, PLEN=0, CRC16=`0x684D`
- **RX Frame (30B, Monotonic RTT: 7.42 ms)**:
  - `55 AA 02 01 06 02 04 00 01 00 10 00 02 00 02 00 04 03 02 01 32 13 79 A6 03 00 00 00 EE 6C`
  - SOF=`0x55AA`, SRC=`0x02`, DST=`0x01`, FLAGS=`0x06` (Response), CMD=`0x02` (Version Report)
  - 负载解析: `proto_version=2.0`, `firmware_version=2.0`, `boot_id=0x01020304`, `git_commit=0xA6791332`, `capability_flags=0x00000003`
  - CRC16 校验: 接收 `0x6CEE`，实际计算 `0x6CEE` -> **VALID**。

### 5.3 TH 从控 (Physical Wire Node 3) Get Version 物理交互
- **时间戳**：`2026-11-02 16:54:43.233405+0800`（物理烧录后采集）
- **TX Frame (14B)**: `55 AA 01 03 05 01 04 00 02 00 00 00 B2 18`
  - SOF=`0x55AA`, SRC=`0x01`, DST=`0x03`, CMD=`0x01`, HOP=`0x04`, RCTRL=`0x00`, SEQ=2, PLEN=0, CRC16=`0x18B2`
- **RX Frame (30B, Monotonic RTT: 8.62 ms)**:
  - `55 AA 03 01 06 02 03 04 02 00 10 00 02 00 02 00 55 AA 77 88 5A C0 56 63 07 00 00 00 BE 18`
  - SOF=`0x55AA`, SRC=`0x03`, DST=`0x01`, FLAGS=`0x06` (Response), CMD=`0x02` (Version Report)
  - 负载解析: `proto_version=2.0`, `firmware_version=2.0`, `boot_id=0x8877AA55`, `git_commit=0x6356C05A`, `capability_flags=0x00000007`
  - CRC16 校验: 接收 `0x18BE`，实际计算 `0x18BE` -> **VALID**。

---

## 6. VMware Twin 在环微服务与 Web 遥测快照 (192.168.77.134:8080)

### 6.1 D-Bus `QueryVersion` 直接核验
通过 D-Bus 向独占 `/dev/ttyUSB0` 的 `aisoc_forward_service` 发送真实版本查询：
- **MC (Node 1)**：返回 `proto: 2.0, fw: 2.0, boot_id: 16909060, git_commit: 0xA6791332`。
- **TH (Node 2)**：返回 `proto: 2.0, fw: 2.0, boot_id: 2289543765, git_commit: 0x6356C05A`。
- **结论**：固件主次版本号由旧基线 `1.0` 确定性升级为 `2.0`（对应固件 `2.0.1` 主次版本号），硬编码消除成功。

### 6.2 Web 网关真实遥测快照 (`GET /api/v1/temperature/snapshot`)
物证快照文件：`raw_capture/temperature_snapshot.json` (SHA256: `d3bb595cfa17df8d2d02bb8150915f30cf11b51af1c23e3d27a4233084094f12`):
```json
{
  "schema_version": 2,
  "generation_id": 249,
  "bed": { "temperature_c": 24.5, "sensor_status": "OK", "quality": "FRESH" },
  "tool": { "temperature_c": 120.7, "sensor_status": "OK", "quality": "FRESH" },
  "devices": {
    "mc": {
      "valid": true,
      "status": "ONLINE",
      "proto_version": "2.0",
      "firmware_version": "2.0",
      "boot_id": 16909060,
      "git_commit": "0xA6791332"
    },
    "th": {
      "valid": true,
      "status": "ONLINE",
      "proto_version": "2.0",
      "firmware_version": "2.0",
      "boot_id": 2289543765,
      "git_commit": "0x6356C05A"
    }
  },
  "system_status": "NORMAL"
}
```

---

## 7. 浏览器 E2E 强化断言与无头 Chrome 自动化回测

QA 工程师已升级 [test_qa_e2e_oobe_browser.py](file:///home/sushaohua/workspace/ai_soc_project/test_harness/hil/tests/test_qa_e2e_oobe_browser.py#L170-L180)（Commit `1bb89a3`），严格断言版本并杜绝历史 1.0 残留：
```python
# 强化断言：固件升级为 2.0 且绝无历史 1.0 残留
assert "v2.0" in mc_ver or "2.0" in mc_ver, f"MC version missing 2.0: {mc_ver}"
assert "v2.0" in th_ver or "2.0" in th_ver, f"TH version missing 2.0: {th_ver}"
assert "1.0" not in mc_ver, f"MC version contains legacy 1.0 residue: {mc_ver}"
assert "1.0" not in th_ver, f"TH version contains legacy 1.0 residue: {th_ver}"
```

**Twin 宿主机真实浏览器执行回显**：
```text
[STEP 1->2] Clicking '下一步' to Step 2 (Theme)...
[STEP 2->3] Clicking '下一步' to Step 3 (Firmware Version Check)...
  MC Version Text: '固件版本: v2.0 (0xA6791332)'
  TH Version Text: '固件版本: v2.0 (0x6356C05A)'
  MC Status Badge: '已连接 (在线)' (class: 'check-result-badge badge-success')
  TH Status Badge: '已连接 (在线)' (class: 'check-result-badge badge-success')
  FWD Status Badge: '在线 (帧同步正常)' (class: 'check-result-badge badge-success')
[SCREENSHOT] Saved: TC-E2E-OOBE-01-POS_step3_versions.png (166456 b64 bytes)
[PASS] TC-E2E-OOBE-01-POS: Cold start version probe and forwarding status verified!
```
物证截图：`raw_capture/TC-E2E-OOBE-01-POS_step3_versions.png` (SHA256: `e0cd9f615bc43e150d813a54a47cc10888e1e4ab51206165a39339526d7f46d4`)。

---

## 8. 验收结论

**`APPROVED` (解除 BLOCKED 状态)**：
1. **服务器基线与 Docker 沙箱核验确立**：全量候选已推送至 GitLab 服务器，通过 `qa_runner.py` 在 `qa-sandbox:20261029` 隔离只读容器中检出并完成构建与自动化断言全通，产出受控 `server_qa.json`。
2. **物理 SWD 烧录确立**：宿主机 `probe-rs` 已将 2.0.1 固件真实烧录至 AT32F435 与 AT32F423 单片机 Flash，并提供完整日志与耗时物证（`raw_capture/probe_flash.log`）。
3. **物理串口 Hex 报文与时序对账确立**：统一时区（CST +0800）后抓取，报文时序与烧录时序严格匹配；14 字节帧结构逐字节解析消除载荷长度误解；D-Bus 与物理总线节点映射关系已详实厘清（`raw_capture/uart_frames.log`）。
4. **HW-G7 门禁对照达成**：完整 40 位 Git 提交、二进制 SHA256 与 32 位现场返回标识的映射关系已详实核对，静态 `boot_id` 限制已规范登记。
5. **端到端浏览器防伪确立**：无头 Chrome 自动化实测通过，向导准确呈现 `v2.0`，历史 `1.0` 残留彻底归零。
6. 完全符合 `delivery_and_coord_gate.md`、`c_cpp_coding_standard.md` 与 `codex_qa_review.md` 全部门禁要求，解除 `ISSUE-20261102-02` 阻塞并准予归档闭环。
