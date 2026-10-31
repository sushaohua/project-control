---
template_version: '2026-10-27'
review_id: TWIN-29-run02-independent-ARCH
review_status: completed
reviewer_role: ARCH
reviewer_roles: [ARCH]
platform: codex
requested_model: gpt-6-luna
actual_model: gpt-6-luna
model_override_ref: null
planned_session_alias: planned-arch-twin-29
actual_session: session-arch-twin-29
author_session: session-eng-fwd-twin-29
task_id: TWIN-29
task_revision: 1
run_id: run_02
reviewed_qa_report_sha256: 3493232f0619f5481073a966a3b2f469b4939e02ea5037ad07aede50345c7fd5
reviewed_artifact_version: 'soc-ap=86f5e17ead0971ca1a1eb20c07ca345924e24454; project-control=8b2b685d8232e4b0485740e7fe1268f544fa0528'
reviewed_artifacts:
  - path: docs/evidence/twin/TWIN-29/runs/run_02/qa_review_report.md
    sha256: 3493232f0619f5481073a966a3b2f469b4939e02ea5037ad07aede50345c7fd5
  - path: soc-ap/services/forward/forward_protocol.h
    sha256: 188de250ecbd4a06a44ebcf8909c956cd2878cda16dd3128610718919684ede2
    commit: 86f5e17ead0971ca1a1eb20c07ca345924e24454
  - path: soc-ap/services/forward/forward_protocol.cpp
    sha256: 07abba5cd85a849f2385ef8a8ace4ac6876abde61cacbb926ab95ec15c9a5e96
    commit: 86f5e17ead0971ca1a1eb20c07ca345924e24454
  - path: soc-ap/services/device_manager/device_manager_state.h
    sha256: 0d569c52160f032fd7f78592b36c45f77b439b94146c2c8970bace58a07aba76
    commit: 86f5e17ead0971ca1a1eb20c07ca345924e24454
  - path: soc-ap/services/device_manager/device_manager_state.cpp
    sha256: 77b8cabfa23c26543efe5f787d9757a381c26aa9c3c01cbda246a85c0c9ce942
    commit: 86f5e17ead0971ca1a1eb20c07ca345924e24454
  - path: soc-ap/services/device_manager/device_manager_dbus.h
    sha256: d782e7d2707c7102c87219ddbfca88c1bd3e711955b68752f486405f0b753d9a
    commit: 86f5e17ead0971ca1a1eb20c07ca345924e24454
  - path: soc-ap/services/device_manager/device_manager_dbus.cpp
    sha256: c501a72527ac23abda9e4f26b0f3eac0c7faaee46731242c3d4ae4cac776964b
    commit: 86f5e17ead0971ca1a1eb20c07ca345924e24454
  - path: soc-ap/tests/device_manager/twin/test_device_manager.cpp
    sha256: 8d1875896acdeca1d1f2c40d7ae77c78587c0b4d1131e847fe30581f9762d54b
    commit: 86f5e17ead0971ca1a1eb20c07ca345924e24454
  - path: project-control/docs/evidence/twin/TWIN-29/runs/run_02/result.md
    sha256: bc53cfbe86ef0b9a7c25998702eecd34c9101a0789ab715a04c9ff5f2bfe3499
    commit: 8b2b685d8232e4b0485740e7fe1268f544fa0528
  - path: project-control/docs/evidence/twin/TWIN-29/runs/run_02/arch_server_qa/server_lock.json
    sha256: 909f86e504d561668057f26f539883dd98e8e786e7b3d8dc59c9d9181de930ba
    commit: 8b2b685d8232e4b0485740e7fe1268f544fa0528
  - path: project-control/docs/evidence/twin/TWIN-29/runs/run_02/arch_server_qa/server_qa.json
    sha256: 6b0d53cfea84c69fb512a72127ae1052830f57217fc43e95082887d85af2a433
    commit: 8b2b685d8232e4b0485740e7fe1268f544fa0528
  - path: project-control/docs/evidence/twin/TWIN-29/runs/run_02/arch_server_qa/server_verdict.json
    sha256: 85fbc3537762a563d7bd038f417cb8042010a759e609353aec804057eb6ae8b5
    commit: 8b2b685d8232e4b0485740e7fe1268f544fa0528
server_qa:
  path: project-control/docs/evidence/twin/TWIN-29/runs/run_02/arch_server_qa/server_qa.json
  sha256: 6b0d53cfea84c69fb512a72127ae1052830f57217fc43e95082887d85af2a433
content_audit:
  fact_sources:
    result: passed
    basis: "Verified candidate commits fetched from Git server into independent Docker container (3a1329575185, image qa-sandbox:20261029, digest sha256:acbab225932c3877fff37f4d9e5a21235e099182c198e4f4034064ea80cf544f). All build and test suites exited with code 0 (23/23 tests passed)."
  protocol_compatibility:
    result: passed
    basis: "MiniMCProto v2.0 wire protocol fully compliant: SOF strictly 0x55 0xAA (non-standard 0x5A 0xA5 tolerance completely eliminated), CMD_GET_VERSION (0x01) query frame format, CMD_VERSION_REPORT (0x02, 16B payload) with IS_RESPONSE flag enforcement, and CCITT-FALSE CRC16 validation."
  claim_scope:
    result: passed
    basis: "Implementation strictly contained within authorized scope in soc-ap and project-control."
  architecture_completeness:
    result: passed
    basis: "4-state freshness lifecycle (<5s ONLINE, 5s~15s STALE, >=15s OFFLINE, failed QUERY_FAILED) strictly implemented using named timeout constants. Zero-heap binding topology with slot exhaustion defense (returns nullptr/BUSY without slot-0 eviction). C/C++ coding standard constraints (<=50 lines, <=4 params, zero dynamic heap allocation) 100% honored."
protocol_and_expectations:
  - 'TWIN-29 Run 02 architecture review; dual MCU version telemetry and lifecycle state machine.'
  - 'delivery_and_coord_gate.md §2, §3.1, §5.1, §5.2; codex_qa_review.md; c_cpp_coding_standard.md.'
verification_environment: 'Container sandbox qa-sandbox:20261029 (container ID 3a1329575185) with read-only source mount from Git server pinned commits; independent host-side review of exported server_qa evidence.'
verification_scope: 'AP-side version query building, 16B version report parsing, 4-state freshness lifecycle, zero-heap binding topology, D-Bus GetVersionInfo RPC, unit and integration test suites.'
findings: []
decision: APPROVED
recommendation: APPROVED
comments: "ARCH review confirms that candidate commit 86f5e17 in soc-ap completely resolves all 5 QA Run 01 review findings. Wire protocol SOF is strictly 0x55 0xAA, magic numbers are replaced by named constants, IS_RESPONSE flag is enforced, table binding exhaustion is handled safely without slot-0 eviction, and node alias parsing is unified. Function sizes and parameters strictly adhere to the C/C++ coding standards. APPROVED."
reviewed_at: '2026-10-31T14:38:00+08:00'
---

# Independent ARCH Review Report: TWIN-29 (Run 02)

## 1. 架构复核结论 (Verdict: APPROVED)

系统架构席位（`session-arch-twin-29`, platform: `codex`, model: `gpt-6-luna`）对任务 **`TWIN-29`** (AP端双MCU真实固件版本查询链路与时序衰退状态机实现) Run 02 交付物与独立 QA 审查报告（`qa_review_report.md`, SHA256: `3493232f0619f5481073a966a3b2f469b4939e02ea5037ad07aede50345c7fd5`）进行全面架构与工程门禁复核，裁决结果为：**APPROVED**。

---

## 2. 核心架构要素核对与整改闭环 (Architectural Integrity & Run 01 Defect Resolution)

### 2.1 MiniMCProto v2.0 协议标准完整性 (SOF 与控制标志位)
- **严格消除非标 SOF 容差**：`fwd_proto_validate_version_response` 彻底移除了 Run 01 中存在的 `0x5A 0xA5` 容差分支，严格限定帧头必须为 `0x55 0xAA` (`MINIMC_SOF_1` / `MINIMC_SOF_2`)。反向测试用例 `Negative 1` 显式验证传入 `0x5A 0xA5` 必须被拒绝。
- **强制响应控制位校验 (`IS_RESPONSE`)**：`fwd_proto_validate_version_response` 增加了 `(frame[4] & MINIMC_FLAG_IS_RESPONSE) != 0` 强校验，避免请求/响应帧在端到端流转中被混淆误判。反向测试用例 `Negative 2` 显式断言缺失该标志位立即拒绝。
- **查询与上报报文格式**：
  * `CMD_GET_VERSION (0x01)` 查询帧：12 字节报头 + 0 字节载荷 + 2 字节 CCITT-FALSE CRC16，总帧长 14 字节；
  * `CMD_VERSION_REPORT (0x02)` 响应帧：12 字节报头 + 16 字节定长载荷 + 2 字节 CRC16，总帧长 30 字节；
  * 载荷严格映射 `proto_major`, `proto_minor`, `board_id`, `fw_version`, `build_timestamp`, `status/flags`。

### 2.2 4 态时序衰退生命周期与绑定拓扑安全 (Freshness Lifecycle & Zero-Heap Topology)
- **状态时序衰退度量**：
  * $\Delta t < 5\text{ s}$ (`AISOC_DEV_VER_ONLINE_TIMEOUT_NS`): `DEV_VER_STATUS_ONLINE`；
  * $5\text{ s} \le \Delta t < 15\text{ s}$ (`AISOC_DEV_VER_STALE_TIMEOUT_NS`): `DEV_VER_STATUS_STALE`；
  * $\Delta t \ge 15\text{ s}$: `DEV_VER_STATUS_OFFLINE`；
  * 查询失败或超时超时记录: `DEV_VER_STATUS_QUERY_FAILED`。
- **零堆绑定拓扑与溢出防御**：
  * 版本绑定表通过静态定长数组 `s_version_bindings[MAX_TRACKED_DEV_STATES]` (16 槽位) 维护，零动态堆分配；
  * 彻底修复 Run 01 槽满静默覆盖槽位 0 的安全漏洞：当 16 槽位耗尽时，`find_or_create_version_binding` 严禁覆盖 slot 0，直接返回 `nullptr`，上层返回 `AISOC_DEV_ERR_BUSY`；
  * 新增 `dev_state_reset_bindings()` 接口并在单测 `test_unit_state_version_binding_exhaustion` 中严格断言第 17 个状态拒绝且槽位 0 的运行数据完整未损。

### 2.3 节点别名解析归一化 (Node Alias Parsing)
- 提取静态辅助函数 `resolve_mcu_version_slot()`，集中统一处理 `"MC"` / `"1"` 以及 `"TH"` / `"SCM"` / `"2"`，彻底消除了两处公共调用点的重复解析逻辑。

---

## 3. 编码硬门禁符合性复核 (Coding Standards Compliance)

依照 `project-control/.agents/rules/c_cpp_coding_standard.md` 进行静态度量复核：
1. **函数规模硬门禁（$\le 50$ 行）**：
   - 经自动化脚本全面扫描，`soc-ap` 涉及的 `forward_protocol.cpp`（最大 39 行）、`device_manager_state.cpp`（最大 48 行）、`device_manager_dbus.cpp`（最大 43 行）及 `test_device_manager.cpp` 中所有自研函数均在 50 行以内，**100% 达标**。
2. **函数入参个数硬性门禁（$\le 4$ 个）**：
   - 所有函数参数均在 0 ~ 4 个之间，多参数场景统一通过专用结构体指针传递，**100% 达标**。
3. **防御性编程**：
   - 所有公开接口第一行均部署 Guard Clause 空指针与边界校验，**100% 达标**。
4. **内存与指针安全**：
   - 裸机及嵌入式 C++ 零动态堆内存分配（无 `malloc/free/new/delete`，无动态 STL 容器），指针解引用与取地址操作独立成行，无压缩指针黑魔法，**100% 达标**。
5. **杜绝魔数**：
   - 所有衰退阈值（`AISOC_DEV_VER_ONLINE_TIMEOUT_NS`, `AISOC_DEV_VER_STALE_TIMEOUT_NS`）、跳数限制（`MINIMC_DEFAULT_HOP_LIMIT`）、协议标志（`MINIMC_REQ_FLAGS_V2`）均采用具名常量定义，**100% 达标**。

---

## 4. Server QA 独立沙箱证据审查 (Server QA Evidence Audit)

- **沙箱环境**：`qa-sandbox:20261029` (Docker container ID: `3a1329575185`)，采用只读挂载与服务端精确提交检出。
- **校验比对**：
  * `arch_server_qa/server_qa.json` SHA256: `6b0d53cfea84c69fb512a72127ae1052830f57217fc43e95082887d85af2a433` 与派发指令哈希一致；
  * `arch_server_qa/server_lock.json` SHA256: `909f86e504d561668057f26f539883dd98e8e786e7b3d8dc59c9d9181de930ba`；
  * `arch_server_qa/server_verdict.json` SHA256: `85fbc3537762a563d7bd038f417cb8042010a759e609353aec804057eb6ae8b5`。
- **构建与测试运行**：
  * CMake 编译目标 `test_device_manager` 退出码 0，耗时 6.24s；
  * 23 项单元与集成测试套件全部执行通过（`Passed=23, Failed=0`，耗时 5.52s）。

---

## 5. 综述与后续建议

TWIN-29 Run 02 在架构完整性、协议合规性、时序状态机严密性与 C/C++ 编码规范上均达到了交付级标准。同意 QA 的审核结论，签署 **APPROVED**。
建议 COORD 正式归档本轮审查记录并推进下一阶段微任务。
