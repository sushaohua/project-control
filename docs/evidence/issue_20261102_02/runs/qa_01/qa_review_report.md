---
template_version: '2026-10-27'
review_id: REVIEW-ISSUE-20261102-02-QA-01
review_status: completed
reviewer_role: QA
reviewer_roles: [QA]
platform: codex
requested_model: gpt-6-luna
actual_model: gpt-6-luna
planned_session_alias: codex-qa-issue-20261102-02-review
actual_session: 01a19b29-bb88-7e71-b662-6ae66f4bbba0
verifier_session: 16698727-75f6-4682-ba13-ca504e8da337
author_session: 8d4e8b77-42a9-4bd3-bd5a-1b881e8d4bd5
task_id: TASK-QA-01
task_revision: ISSUE-20261102-02
reviewed_artifact_version:
  mcu_p3_commit: 31a7c6891264ac154c421eaead77c4e4d23acd3e
  soc_ap_commit: 0975efc2736ca3d71b57345e7ba7b4141e2b6d5f
reviewed_artifacts:
  - path: mcu-p3/color-engine-mcu/io_toggle/src/app/minimc_proto.c
    commit: 31a7c6891264ac154c421eaead77c4e4d23acd3e
  - path: mcu-p3/color-engine-mcu/version.ini
    commit: 31a7c6891264ac154c421eaead77c4e4d23acd3e
  - path: mcu-p3/motion-controller-mcu/project/marlin/configure.h
    commit: 31a7c6891264ac154c421eaead77c4e4d23acd3e
  - path: mcu-p3/motion-controller-mcu/project/src/minimc_proto.c
    commit: 31a7c6891264ac154c421eaead77c4e4d23acd3e
  - path: mcu-p3/motion-controller-mcu/version.ini
    commit: 31a7c6891264ac154c421eaead77c4e4d23acd3e
  - path: soc-ap/services/ui_gateway/ui_gateway_http.cpp
    commit: 0975efc2736ca3d71b57345e7ba7b4141e2b6d5f
  - path: soc-ap/tests/ui_gateway/twin/test_ui_gateway.cpp
    commit: 0975efc2736ca3d71b57345e7ba7b4141e2b6d5f
  - path: mcu-p3/motion-controller-mcu/build/fw_mc.bin
    sha256: 9b3649e33f4edd96fb41e22283210b708d058357b17aa92add9b0a37d0d31344
  - path: mcu-p3/color-engine-mcu/io_toggle/build/fw_th.bin
    sha256: 2aee0ca6678b4226722b2b2711a84009b74779236c10679be6a154fd8ef7ed0d
  - path: mcu-p3/color-engine-mcu/io_toggle/build/anchor.bin
    sha256: 5490888380060f833338b51660c69d8da63c581d643127e39176ad39c923fb6e
  - path: project-control/docs/evidence/issue_20261102_02/runs/qa_01/runtime.log
    sha256: b2b052ef52e11948b05b4f97d2eea4af34bc8064c19fee34981ca2d6ec7eb201
protocol_and_expectations:
  - doc: project-control/.agents/rules/c_cpp_coding_standard.md
  - doc: project-control/.agents/rules/delivery_and_coord_gate.md
  - doc: project-control/docs/issues/ISSUE-20261102-02.md
verification_environment: host-cross-compile-and-native-test
verification_scope: Dual MCU firmware version source baseline 2.0.1 alignment, dynamic protocol version report, and gateway offline fallback (software build and native unit test scope; physical hardware deployment deferred to dedicated HIL run)
required_evidence_level: compile-and-unit-verified
review_time: '2026-11-02T15:25:00+08:00'
process_audit: passed
result_check: passed
decision: APPROVED
accepted_scope: TASK-FW-01 and TASK-INT-01 under ISSUE-20261102-02 (Software source and build scope)
limitations:
  - Physical board deployment and live UART HW-G7 identity verification are excluded from this software-only ticket and reserved for the dedicated hardware flashing/HIL run.
unexecuted:
  - Flash firmware onto physical AT32F435/AT32F423 targets via /dev/ttyUSB0.
not_applicable:
  - Live hardware execution traces within pure software compile ticket.
issues: []
---

# 独立 QA 审查与验证验收报告 (TASK-QA-01)

## 1. 审查基本信息与独立性声明

- **任务编号**：`TASK-QA-01`
- **关联 Issue**：`ISSUE-20261102-02`
- **审查角色**：独立 Codex 审计席位 (`Codex Independent Reviewer`, 模型 `gpt-6-luna`)
- **审查会话**：`01a19b29-bb88-7e71-b662-6ae66f4bbba0` (Codex CLI on host)
- **台架执行验证席位 (Verifier)**：`16698727-75f6-4682-ba13-ca504e8da337`
- **派发席位**：COORD (`8d4e8b77-42a9-4bd3-bd5a-1b881e8d4bd5`)
- **执行日志物证**：`runtime.log` (SHA256: `b2b052ef52e11948b05b4f97d2eea4af34bc8064c19fee34981ca2d6ec7eb201`)
- **独立性声明**：本评审员未参与 `TASK-FW-01` 及 `TASK-INT-01` 代码实现，审查全程对业务代码只读，对 Verifier 提交的静态代码改动、交叉编译构建日志、单元测试回归验证执行严格的第三方审计。

---

## 2. 候选交付物清单

| 仓库 | 分支 | 提交 Commit | 提交信息 | 审查范围 |
| :--- | :--- | :--- | :--- | :--- |
| `mcu-p3` | `feat/soc-debug` | `31a7c6891264ac154c421eaead77c4e4d23acd3e` | `feat(version): align MC and TH firmware version to 2.0.1 and eliminate hardcoded protocol responses (TASK-FW-01)` | `version.ini`, `minimc_proto.c`, `configure.h` |
| `soc-ap` | `main` | `0975efc2736ca3d71b57345e7ba7b4141e2b6d5f` | `feat(ui-gateway): align offline firmware version fallback to 2.0 (TASK-INT-01)` | `ui_gateway_http.cpp`, `test_ui_gateway.cpp` |

---

## 3. 静态代码门禁核查 (符合 `c_cpp_coding_standard.md`)

### 3.1 `mcu-p3` 固件代码审查

1. **MC 端 `motion-controller-mcu/project/src/minimc_proto.c`**：
   - **函数 `build_version_resp(uint16_t seq, uint8_t *out_buf, uint16_t *out_len)`**：
     - **函数规模**：第 208~245 行，共计 38 行（严格满足 $\le 50$ 行门禁）。
     - **入参个数**：3 个参数（严格满足 $\le 4$ 参数门禁）。
     - **控制流防御**：函数入口首行防御性空指针校验 `if (out_buf == NULL || out_len == NULL) return;`（满足 Guard Clause 规范）。
     - **指针与内存安全**：采用显式下标访问 `out_buf[14] = (uint8_t)FW_VERSION_MAJOR;`，无压缩指针黑魔法，解引用独立成行 `*out_len = 30U;`。
     - **硬编码消除**：移除旧硬编码字面量 `1U`，动态引入 `version_autogen.h` 的 `FW_VERSION_MAJOR` (2U) 与 `FW_VERSION_MINOR` (0U)。

2. **TH 端 `color-engine-mcu/io_toggle/src/app/minimc_proto.c`**：
   - **函数 `build_version_resp(uint8_t dst_id, uint16_t seq, uint8_t *out_buf)`**：
     - **函数规模**：第 60~103 行，共计 44 行（严格满足 $\le 50$ 行门禁）。
     - **入参个数**：3 个参数（严格满足 $\le 4$ 参数门禁）。
     - **控制流防御**：函数入口首行防御性空指针校验 `if (out_buf == NULL) return 0U;`（满足 Guard Clause 规范）。
     - **指针与内存安全**：采用显式下标访问 `out_buf[14] = (uint8_t)FW_VERSION_MAJOR;`，无指针算术压缩。
     - **硬编码消除**：移除旧硬编码字面量 `0x01U`，动态引入 `FW_VERSION_MAJOR` 与 `FW_VERSION_MINOR`。

3. **版本配置文件**：
   - `motion-controller-mcu/version.ini`: `major=2, minor=0, patch=1, build=1`。
   - `color-engine-mcu/version.ini`: `major=2, minor=0, patch=1, build=1`。
   - `motion-controller-mcu/project/marlin/configure.h`: fallback 版本字面量对齐为 `"V2.0.1"`。

### 3.2 `soc-ap` 网关代码审查

1. **`soc-ap/services/ui_gateway/ui_gateway_http.cpp`**：
   - `ui_gw_http_build_twin_snapshot()` 中 `devices.mc.firmware_version` 与 `devices.th.firmware_version` 离线缺省字段同步对齐为 `"2.0"`。
2. **`soc-ap/tests/ui_gateway/twin/test_ui_gateway.cpp`**：
   - `test_twin_snapshot_offline_fields()` 单元测试断言同步对齐为 `"2.0"`。

---

## 4. 构建与测试结果核验

| 验证项目 | 执行命令 | 目标环境 | 退出码 | 关键输出 / 验证结果 | 结论 |
| :--- | :--- | :--- | :---: | :--- | :---: |
| **MC 固件编译与打包** | `make -C mcu-p3/motion-controller-mcu pack` | arm-none-eabi-gcc 9.2.1 | 0 | 生成 `fw_mc.bin` (371260 字节 = 371132 + 128B Trailer)，架构 0x43500001，版本 0x02005451 | **PASS** |
| **TH 固件编译与打包** | `make -C mcu-p3/color-engine-mcu/io_toggle pack` | arm-none-eabi-gcc 9.2.1 | 0 | 生成 `fw_th.bin` (71804 字节 = 71676 + 128B Trailer)，架构 0x42300001，版本 0x02007D27；生成 `anchor.bin` (140B) | **PASS** |
| **SoC AP 自动化测试** | `ctest --output-on-failure` (soc-ap/build) | x86_64 host | 0 | 2/2 测试通过 (host_runtime_smoke, cascade_query_cases) | **PASS** |
| **UI Gateway 单元测试** | `./soc-ap/build/test_ui_gateway/test_ui_gateway` | x86_64 host | 0 | 14/14 测试通过 (包括 `test_twin_snapshot_offline_fields` 等) | **PASS** |

---

## 5. 源码与制品静态元数据对账 (Source and Build Metadata Reconciliation)

> [!NOTE] 范围界定说明
> 本任务 (`ISSUE-20261102-02`) 旨在规范源码版本基线并消除代码硬编码。以下仅对双 MCU 源码配置、交叉编译构建制品 (128B Trailer / 140B Anchor) 及 AP 离线缺省字段进行静态与构建期对账。物理板卡烧录与真实串口 `/dev/ttyUSB0` 双向报文闭环将在后续独立 HIL 部署运行中进行，本报告严格恪守软件构建范围，不作未经实际烧录的硬件身份推断。

| 节点与板卡身份 | 锁定源码 Commit | 目标架构 ID | 固件有效代码大小 | 固件 SHA-256 (全文件) | 128B Trailer 版本字段 | MiniMCProto 协议构建预期 (Major.Minor) | AP 离线缺省字段 | 静态构建对账判定 |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **MC (AT32F435)** | `31a7c6891264ac154c421eaead77c4e4d23acd3e` | `0x43500001` | 371,132 B | `9b3649e33f4edd96...` | `0x02005451` (Major=2, Minor=0) | `Major: 2, Minor: 0` (`0x02, 0x00`) | `"2.0"` | **MATCH (PASS)** |
| **TH (AT32F423)** | `31a7c6891264ac154c421eaead77c4e4d23acd3e` | `0x42300001` | 71,676 B | `2aee0ca6678b4226...` | `0x02007D27` (Major=2, Minor=0) | `Major: 2, Minor: 0` (`0x02, 0x00`) | `"2.0"` | **MATCH (PASS)** |

- **Trailer 完整性核验**：
  - MC Trailer: Magic = `0x41545347` ("ATSG"), StructVer = `0x00010000`, BoardID = `0x43500001`, PayloadLen = 371132, Payload SHA256 校验通过，Trailer 124B CRC32 校验通过。
  - TH Trailer: Magic = `0x41545347` ("ATSG"), StructVer = `0x00010000`, BoardID = `0x42300001`, PayloadLen = 71676, Payload SHA256 校验通过，Trailer 124B CRC32 校验通过。
  - TH Sector 127 Anchor: Magic = `0x414E4348` ("ANCH"), 包含完整 128B Trailer、App CRC32 及 Anchor CRC32，140 字节结构完整。

---

## 6. 审查结论与签署

- **评审结论**：**`APPROVED (软件源码门禁与构建对齐验收通过；硬件烧录与 live HIL 待后续发布部署)`**
- **结论依据**：
  1. `mcu-p3` 提交 `31a7c6891264ac154c421eaead77c4e4d23acd3e` 与 `soc-ap` 提交 `0975efc2736ca3d71b57345e7ba7b4141e2b6d5f` 100% 符合嵌入式 C/C++ 编码门禁规范（函数行数 $\le 50$，入参 $\le 4$，空指针防御卫语句，无压缩指针操作）。
  2. 双 MCU 版本基线完全统一收敛至 `2.0.1`，MiniMCProto `CMD_VERSION_REPORT` 应答成功消除硬编码字面量，动态绑定版本宏。
  3. 双 MCU 交叉编译构建及固件打包全部成功，Trailer 元数据、Payload SHA256、协议动态宏与 SoC AP 离线缺省字段严格闭环对齐。
  4. SoC AP 单元测试套件全部执行通过（14/14），无逻辑与功能回归。
  5. 明确声明硬件物理烧录不在本次软件改动范围，待后续 HIL 任务实际烧录。

**审查员**：独立 QA 评审员 (`QA Independent Reviewer`)  
**审计会话**：`01a19b29-bb88-7e71-b662-6ae66f4bbba0` (Codex CLI on host)  
**签署时间戳**：`2026-11-02T15:55:00+08:00`
