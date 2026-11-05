---
id: CONFIRM-WEB-HMI-FULL-QA-BUILD-DEPLOY-20261105
title: Web HMI 完整 basecase 与增量真实闭环 QA 编译部署执行确认单
revision: 2
date: 2026-11-05
author_role: INTEGRATOR
author_session: 7812a1f6-5006-4971-a954-802f855cf20a
demand_id: DEM-20261105-005
requirement_id: REQ-20261105-001
submission_ref:
  path: project-control/docs/work_intake/submissions/20261105_web_hmi_full_closed_loop_qa.md
  sha256: db143168eb57dfd86f889c0b4987437d2b3e3a41f7bfe8688f721a253b3a98b5
related_inputs:
  basecases_doc:
    path: project-control/docs/planning/qa_web_hmi_basecases_20261103.md
    revision: 4
    sha256: 67a2c1df609ce14773361a83b803ca414f13bf243be87961f97700ef798ff929
    arch_doc_review_session: 01a1a6dc-33a3-7053-875c-a8ef06502d6d
    arch_doc_review_local_record: project-control/docs/evidence/qa_web_hmi_basecases_rev4_20261105/review_receipt.json
  remediation_plan:
    path: project-control/docs/planning/end_to_end_physical_link_remediation_plan_20261104.md
    revision: 3
    sha256: 21dd6cc16b9eb7d643662b6fba681e6360f4dcd98cdece55439c6f759c5b22cc
  vmware_qa_flow:
    path: project-control/docs/planning/independent_qa_vmware_execution_flow_20261103.md
    revision: 2
    sha256: e043a25c169dfdab9de2d241185b9494e186c737cdd424dbf5ff7bf4038f8437
status: Approved
approved_by: sushaohua
approved_at: '2026-11-05T11:55:34+08:00'
approval_session: ff2fb105-fd84-4ecb-b1e6-8f8eb00badc6
---

# Web HMI 完整 basecase 与增量真实闭环 QA 编译部署执行确认单

> [!IMPORTANT]
> **只读核查声明与执行边界**：
> 1. 本确认单严格遵照 `REQ-20261105-001` (`DEM-20261105-005`) 公共约束生成，在编写期间**仅执行了只读状态核查，未启动任何本轮编译、部署、烧录、电机运动或测试动作，未修改任何业务代码仓，未抢占物理台架或串口句柄**。
> 2. 在用户确认本执行流程、并在烧录/物理动作前对具体制品清单（文件路径、字节大小、SHA256、Flash 基地址）给出有效授权前，不得外推执行任何烧录、运动或实加热操作。
> 3. 全程锁死已确认硬约束：**真实 MC (`AT32F435VGT7`) + 真实 TH (`AT32F423CCT7`)、AP↔MC 业务与 MC↔TH 级联波特率 `921600 8N1`、双路 Debug 串口（`[MC-DBG]` / `[TH-DBG]`）`115200 8N1`、加热输出锁死 0%（Option A）、Bootloader 零改动与基地址保护（MC `0x08020000`、TH `0x08004000`）**。

---

## 一、 当前环境、服务器仓库、工具链与历史交付边界只读核查结论

### 1.1 六仓服务器与本地 HEAD 提交只读盘点表

| 仓库名称 | 目标分支 | 当前服务器/本地 `HEAD` 完整 Commit SHA | 最近一次提交摘要 | 本轮角色与保护边界 |
| :--- | :--- | :--- | :--- | :--- |
| **`project-control`** | `main` | `77c679616a09d9c82906ff9bdf27fefc6d6c343f` | `docs(coord): close TWIN-51..53 (ISS-20261105-001..003) with sandbox and Codex QA APPROVED evidence` | 计划、需求、规则、任务卡与证据归档权威仓 |
| **`soc-ap`** | `main` | `79932746d225bb115010c5545ef3f7499482e137` | `chore(soc-ap): fast-forward TWIN-52 and TWIN-53 linear history onto main`（包含 `TWIN-49` `333178c6...`、前端/网关修复 `7c1f3509...`、`TWIN-51` `75f8a1a6...`、`TWIN-52` `ad2538ae...`、`TWIN-53` `87c3bd31...`） | SoC AP 守护进程与 Web HMI 源码仓 |
| **`mcu-p3`** | `feat/soc-debug` | `016e1236af75f6f19282d6b000f4b1b68bd96cc3` | `feat(th): implement TWIN-48 control opcodes, 0x1C G-code bridge and thermistor safety-lock fix`（父提交为 `TWIN-47` `d86041814689b2f353d6fe0b372d31689b826a98`） | MC (`AT32F435`) 与 TH (`AT32F423`) 应用固件仓 |
| **`test_harness`** | `main` | `d14ed04321c6d4f5ddb35a8801604a8af53b5b60` | `fix(hil): preserve pre-jog mc log in inject-mismatch for live reconciliation negative test (TWIN-50)` | 独立 QA 检查器、浏览器 CDP 脚本与 HIL 探针仓 |
| **`boot/bootloadermc`** | `soc_debug` | `4fc171ea61912561949b9a0cfc1da8975e4c39ba` | `docs: version MC Bootloader rules without replacing local links` | **只读封锁**：严禁修改、重编或刷写 MC Bootloader (`0x08000000~0x0801FFFF`) |
| **`boot/bootloaderth`** | `soc_debug` | `769fccbe52464ad7ceb856c5e89cb0d25abbbf87` | `docs: version TH Bootloader rules without replacing local links` | **只读封锁**：严禁修改、重编或刷写 TH Bootloader (`0x08000000~0x08003FFF`) |

---

### 1.2 宿主机、Docker 沙箱、Windows 物理台架与唯一 VMware 虚拟机现状

1. **WSL2 宿主机（`192.168.77.113`，`DESKTOP-0364359`）**：
   - **操作系统**：Linux `6.18.33.2-microsoft-standard-WSL2 x86_64`（Ubuntu 20.04.6 LTS，`glibc 2.31`）。
   - **编译与脚本工具链**：
     - 宿主 C/C++：`gcc / g++ (Ubuntu 9.4.0-1ubuntu1~20.04.2) 9.4.0`
     - MCU 交叉编译器：`arm-none-eabi-gcc (15:9-2019-q4-0ubuntu1) 9.2.1 20191025 (release)`（已安装，支持 `AT32F435` 与 `AT32F423` 真机 `.elf`/`.bin` 确定性构建）
     - CMake：`/home/sushaohua/.local/bin/cmake` (`version 4.4.4`)
     - Python：`Python 3.8.10`
2. **独立 Docker QA 沙箱（`qa-sandbox:20261029`）**：
   - **镜像摘要**：`sha256:acbab225932c3877fff37f4d9e5a21235e099182c198e4f4034064ea80cf544f`。
   - **能力边界**：内置宿主机同构 `x86_64` GCC 9.4.0、CMake、Python3 及 `/usr/local` 预装 `third_party` 库；**不包含 `arm-none-eabi-gcc` 交叉编译器，且无物理 USB/UART/SWD 设备透传**，仅承担服务器锁定候选的软件构建与软件/PTY 回归验证。
3. **Windows 宿主侧物理调试探针与串口现状（非侵入只读枚举）**：
   - **SWD 烧录工具**：`/mnt/c/Users/EDY/tools/probe-rs/probe-rs.exe`（`34,974,208` 字节，可执行）。
   - **双板 ST-Link V2 在线枚举与唯一芯片身份**：
     - **MC 主控板 (`AT32F435VGT7`)**：`probe_id = 0483:3748:75003800120000334C41534E`，Flash `1024 KB`，MSP `0x20060000`，唯一芯片 UID `053023904C96C0000D819709`。
     - **TH 工具头板 (`AT32F423CCT7`)**：`probe_id = 0483:3748:`（无序列号字符串实例），Flash `256 KB`，MSP `0x2000C000`，唯一芯片 UID `053173C58023C000127C0707`。
   - **Windows 串口列表（`[System.IO.Ports.SerialPort]::GetPortNames()`）**：当前枚举到 `COM1`、`COM12`（对应 MC `USART1` `115200 8N1` `[MC-DBG]`）、`COM13`（对应 TH `USART3` `115200 8N1` `[TH-DBG]`）。
   - **Windows 宿主浏览器**：`/mnt/c/Program Files/Google/Chrome/Application/chrome.exe`（存在）。
4. **唯一 VMware 虚拟机（`sushaohua@192.168.77.134`，`sushaohua-VMware-Virtual-Platform`）现状**：
   - **操作系统与工具链**：Ubuntu Linux `7.0.0-38-generic x86_64`，`g++ (Ubuntu 15.2.0-16ubuntu1) 15.2.0`，`cmake version 4.2.3`，已安装 `/usr/bin/google-chrome` 与 `/usr/bin/firefox`。
   - **当前代码树状态（存在版本漂移与未提交修改，待 Step 1 清理对齐）**：
     - `/home/sushaohua/tmp/ai_soc_project/soc-ap` 的 `git rev-parse HEAD` 为 `333178c66280e785ae1a5c089a6e2a05075cc926`（停留在 `TWIN-49`），且工作区含有手动 `scp` 覆盖产生的 10 个 `M` 修改文件和 3 个 `??` 未跟踪路径，尚未对齐至服务器最新提交 `79932746d225bb115010c5545ef3f7499482e137`。
   - **`third_party/install` 状态**：只读执行 `bash third_party/build.sh --verify` 验证通过（`libdbus-1.so`、`dbus-daemon`、`libfastcdr.so`、`libfastdds.so` 齐全，`install/include/fastcdr/xcdr/optional.hpp` 已含 2 处 `if (val.storage_.engaged_)` 判空守卫）。
   - **物理业务串口映射**：
     - `/dev/ttyUSB0`（`crw-rw---- 1 root dialout 188, 0`）在线；
     - 稳定设备符号链接：`/dev/serial/by-id/usb-1a86_USB_Serial-if00-port0 -> ../../ttyUSB0`。
   - **当前运行进程与干扰源排查**：
     - 4 个核心守护进程在线：`dbus-daemon` (PID `1588460`)、`forward_service_daemon` (PID `1588465`，绑定 `/dev/ttyUSB0 @ 921600`)、`device_manager_daemon` (PID `1588466`)、`ui-gateway` (PID `1588468`，监听 `:8080`)；
     - **发现干扰源**：VMware 后台同时存在 **3 个历史残留的 `python3 /tmp/aisoc_twin_logs/hw_sampler.py` 进程（PID `1556795`、`1561399`、`1588526`）**，它们每 1.5s 周期性调用 `POST /api/v1/temperature/sample`！在正式 QA 采证前（Step 7）必须彻底清理此类非标后台轮询脚本，防止污染请求序列号（`seq`）和业务帧时序。

---

### 1.3 `TWIN-47～50` 与 `TWIN-51～53` 准确交付及实际接受范围核实

| 任务 ID | 仓库与锁定候选 Commit | 独立 Codex QA 会话与结论 | 实际接受范围（`accepted_scope`）与真机 HIL 边界核实 |
| :--- | :--- | :--- | :--- |
| **`TWIN-47`** | `mcu-p3`<br/>`d86041814689b2f353d6fe0b372d31689b826a98` | `01a1a61f-f579-7cd0-a857-cd21096242ac`<br/>`APPROVED` (`qa_03`) | **仅限 Docker 沙箱宿主 GCC 单元测试**：验证 MC `0x10..0x1C` 命令解析、Marlin 队列桥接与 `[MC-DBG]` 日志生成；**不含交叉编译 ELF 上板与物理台架 HIL**。 |
| **`TWIN-48`** | `mcu-p3`<br/>`016e1236af75f6f19282d6b000f4b1b68bd96cc3` | `01a1a639-77f0-7f01-a9ae-b5d814dcfae1`<br/>`APPROVED` (`qa_01`) | **仅限 Docker 沙箱宿主 GCC 单元测试**：验证 TH `0x10`/`0x15`/`0x17`/`0x19`/`0x1C`、`mycontrol.c` 入队、温度防误锁死与 `[TH-DBG]` 日志；**不含物理台架 HIL**。 |
| **`TWIN-49`** | `soc-ap`<br/>`333178c66280e785ae1a5c089a6e2a05075cc926` | `01a1a6c4-7035-7213-8292-e56b4df57c47`<br/>`APPROVED` (`qa_04`) | **仅限 Docker 沙箱软件与 POSIX PTY 测试**：验证 AP `B921600` 修复、双单播全 ACK 闭环与去除 `ui_gateway` 本地 Mock；**不含真机物理串口与机械负载 HIL**。 |
| **`TWIN-50`** | `test_harness`<br/>`d14ed04321c6d4f5ddb35a8801604a8af53b5b60` | `01a1a6f3-2867-7ce0-9e0d-6ddcd2830e13`<br/>`APPROVED` (`qa_03`) | **独立 QA 签署范围仅限 Docker 沙箱静态检查与 921600 PTY 虚拟 MCU 联调**。虽附有 `INTEGRATOR` 工程实测报告 `twin50_real_hil_acceptance_report_20261104.md`（覆盖 `HIL-01~06` 接口级联调），但：(1) 未经独立 QA 完整 `BASE-01～27` + `J-01` + `DELTA-*` 审阅；(2) 当时 `soc-ap` 尚未合入 `7c1f3509` 及 `TWIN-51～53`；(3) `HIL-06` 仅使用了 SWD 关断 `USART2` 寄存器注入，**未执行 `BASE-24` 真实物理拔插 USB 子例**。 |
| **`TWIN-51`** | `soc-ap`<br/>`75f8a1a670edabb21c8d3dfc79243e06f73099af` | `01a1a999-e8d7-7cb3-ad5e-61e0dd08e72c`<br/>`APPROVED` (`qa_02`) | **仅限软件单测**：修复 `test_backoff.cpp` 在 GCC 15 下的 `-Werror=maybe-uninitialized` 编译阻断与 `#undef NDEBUG`。 |
| **`TWIN-52`** | `soc-ap`<br/>`ad2538ae7f4834cac98be97e08b055f80eb81cfc` | `01a1a9ad-5a37-7bb3-9835-4ed9ce0a308b`<br/>`APPROVED` (`qa_03`) | **仅限软件单测**：固化 Fast-CDR 2.2.5 `optional.hpp` 两处 `engaged_` 判空补丁与 `third_party/build.sh` 同秒 `mtime` 强制覆盖安装。 |
| **`TWIN-53`** | `soc-ap`<br/>`87c3bd31b1adc9f17fcc75aa5d7ea26beb44e59a` | `01a1a9ae-e883-7270-8cdd-358b3b47aed9`<br/>`APPROVED` (`qa_02`) | **仅限软件与进程会话沙箱测试**：加固 `deploy_twin.sh` `setsid+nohup+</dev/null+disown` 四进程会话隔离、真实 `SIGHUP` 存活与启动崩溃拦截。 |

---

### 1.4 `soc-ap/tools/deploy_twin.sh` 与 `soc-ap/third_party/build.sh` 行为核实

经逐行只读审计 `soc-ap/tools/deploy_twin.sh`（当前 `HEAD` `79932746...`）与 `soc-ap/third_party/build.sh`，其关键行为特性如下：
1. **是否隐式重编译**：
   - `deploy_twin.sh` 默认设置 `AISOC_AUTO_BUILD="1"`（第 22 行），在未传入 `--no-build` 且配置文件未显式设置 `AISOC_AUTO_BUILD="0"` 时，**每次启动都会隐式执行 `build_fullstack()` 触发 5 个模块的 CMake 编译**。
   - **防止部署阶段篡改已封存制品哈希的控制手段**：在部署已封存的 `build-<buildno>` 制品或锁定编译结果后，启动服务时**必须传入 `--no-build`（或在受控配置文件中固定 `AISOC_AUTO_BUILD="0"`）**，严禁启动脚本在部署或重启服务时隐式重新编译覆盖二进制文件。
2. **是否复用旧二进制**：
   - 当 `DO_BUILD_ONLY=0` 且 `build/runtime/CMakeCache.txt` 中的源目录路径与当前 `SOC_AP_DIR` 一致时，`build_fullstack()` 不删除 `build/` 目录，直接执行增量编译并复用未重编的旧目标文件。
   - **保证干净确定性构建的控制手段**：在 Step 3 构建阶段，必须显式先执行 `rm -rf "${SOC_AP_DIR}/build" "${SOC_AP_DIR}/dist/vmware_twin"`（或运行 `deploy_twin.sh --build-only`），确保 100% 从干净状态生成二进制产物。
3. **是否清理旧日志与旧 PID**：
   - `deploy_twin.sh` 在启动新服务前会调用 `purge_previous_deployment()`（第 289～316 行），自动终止记录在 `/tmp/aisoc_twin_logs/*.pid` 的 4 个守护进程、`pkill -f` 匹配的守护进程、占用 `AISOC_HTTP_PORT` 与 `AISOC_UART_DEVICE` 的进程，并**无条件删除 `/tmp/aisoc_twin_logs/*.log`、`*.pid`、`dbus.addr`、`runtime.env` 及 `dist/vmware_twin/logs/*.log`**。
   - **关键约束**：
     - (a) 凡需保留上一轮运行日志（例如验证 `BASE-26` 服务重启前后状态或故障复盘），**必须在调用 `deploy_twin.sh` 前先将 `/tmp/aisoc_twin_logs/` 完整归档拷贝到本轮 `run_id` 证据目录（Step 6）**；
     - (b) `purge_previous_deployment()` 不会匹配外部自编脚本名（如 `hw_sampler.py`），因此在 Step 7 停旧时必须显式查杀 `hw_sampler.py`。

---

## 二、 推荐的 9 步编译部署与采证准备标准执行顺序

以下 9 步流程在用户确认本单并授予排他台架窗口后严格按序执行：

### Step 1：服务器取件与源码锁定（Server Checkout & Candidate Lock）
- **实际执行位置**：
  1. 宿主机（`192.168.77.113`）独立构建工作区 `/tmp/aisoc_release_builds/build-<buildno>/src/`；
  2. 唯一 VMware 虚拟机（`sushaohua@192.168.77.134`）受控目录 `/home/sushaohua/tmp/ai_soc_project/soc-ap`。
- **执行者角色**：`INTEGRATOR` / 受控 QA Runner。
- **命令及工作目录**：
  ```bash
  # 1. 在宿主机独立干净目录从 Git 服务器 (192.168.77.113:2222) 拉取并锁定准确 Commit
  BUILDNO="20261105-001"
  RELEASE_ROOT="/tmp/aisoc_release_builds/build-${BUILDNO}"
  mkdir -p "${RELEASE_ROOT}/src" "${RELEASE_ROOT}/artifacts"
  git clone --no-checkout ssh://git@192.168.77.113:2222/sushaohua/soc-ap.git "${RELEASE_ROOT}/src/soc-ap"
  git -C "${RELEASE_ROOT}/src/soc-ap" checkout --detach 79932746d225bb115010c5545ef3f7499482e137
  git clone --no-checkout ssh://git@192.168.77.113:2222/sushaohua/mcu-p3.git "${RELEASE_ROOT}/src/mcu-p3"
  git -C "${RELEASE_ROOT}/src/mcu-p3" checkout --detach 016e1236af75f6f19282d6b000f4b1b68bd96cc3
  git clone --no-checkout ssh://git@192.168.77.113:2222/sushaohua/test_harness.git "${RELEASE_ROOT}/src/test_harness"
  git -C "${RELEASE_ROOT}/src/test_harness" checkout --detach d14ed04321c6d4f5ddb35a8801604a8af53b5b60

  # 2. 在 VMware 虚拟机清理未提交脏改动并严格对齐到同一 soc-ap Commit
  ssh sushaohua@192.168.77.134 "cd /home/sushaohua/tmp/ai_soc_project/soc-ap && \
    git fetch origin && git reset --hard 79932746d225bb115010c5545ef3f7499482e137 && git clean -fd"
  ```
- **准确输入**：Git 服务器锁定提交（`soc-ap=79932746d225bb115010c5545ef3f7499482e137`、`mcu-p3=016e1236af75f6f19282d6b000f4b1b68bd96cc3`、`test_harness=d14ed04321c6d4f5ddb35a8801604a8af53b5b60`、`project-control=77c679616a09d9c82906ff9bdf27fefc6d6c343f`）。
- **输出路径与哈希核验方式**：生成 `${RELEASE_ROOT}/candidate_lock.yaml` 并计算 `sha256sum "${RELEASE_ROOT}/candidate_lock.yaml"`；核对 `git rev-parse HEAD` 与 `git status --porcelain` 输出为空。
- **成功条件**：宿主机独立检出与 VMware 工作树的 `HEAD` SHA 100% 匹配目标锁定 Commit，且 `git status --porcelain` 为空（零脏文件）。
- **失败停止点与恢复办法**：若任一仓库 `fetch/checkout` 失败或 SHA 不匹配，立即停止后续构建；检查 Git 服务器连接与分支引用，禁止使用作者未提交工作树替代。

---

### Step 2：依赖核验与 `third_party` 复用/构建（Dependency Verification & `third_party` Build）
- **实际执行位置**：唯一 VMware 虚拟机（`sushaohua@192.168.77.134`）及 Docker 沙箱（`qa-sandbox:20261029`）。
- **执行者角色**：`INTEGRATOR` / 受控 QA Runner。
- **命令及工作目录**：
  ```bash
  # 在 VMware (/home/sushaohua/tmp/ai_soc_project/soc-ap) 执行校验，若失败则自动从 archives 重编并打补丁
  ssh sushaohua@192.168.77.134 "cd /home/sushaohua/tmp/ai_soc_project/soc-ap && \
    bash third_party/build.sh --verify || bash third_party/build.sh"
  ```
- **准确输入**：`soc-ap/third_party/archives/*.tar.*`、`soc-ap/third_party/patches/Fast-CDR-2.2.5-optional-engaged-guard.patch`、`soc-ap/third_party/build.sh`。
- **输出路径与哈希核验方式**：
  - `third_party/install/lib/{libdbus-1.so,libfastcdr.so,libfastdds.so,libfoonathan_memory-0.7.3.a}`
  - `third_party/install/bin/dbus-daemon`
  - `third_party/install/include/fastcdr/xcdr/optional.hpp`（校验 `grep -c "if (val.storage_.engaged_)"` 等于 `2`）
  - 执行 `sha256sum` 记录上述库与头文件指纹。
- **成功条件**：`bash third_party/build.sh --verify` 退出码为 `0`，且输出 `[OK] Fast CDR optional.hpp engaged guard verified`。
- **失败停止点与恢复办法**：若 `--verify` 返回非 `0`，立即删除 `third_party/src/Fast-CDR-2.2.5` 与 `third_party/build/Fast-CDR` 后重跑 `bash third_party/build.sh fastcdr && bash third_party/build.sh --verify`；仍失败则阻塞构建并上报。

---

### Step 3：AP/UI 与 MC/TH 双固件确定性构建（Deterministic Build of AP/UI & Dual MCU Firmware）
- **实际执行位置**：
  - **MC/TH 真机固件交叉编译**：WSL2 宿主机（`192.168.77.113`，使用 `arm-none-eabi-gcc 9.2.1`）；
  - **AP/UI 软件单测与沙箱构建**：宿主机 `qa-sandbox:20261029` 容器；
  - **VMware 部署二进制构建**：VMware（`sushaohua@192.168.77.134`，详见第四节问题 1 确认项）。
- **执行者角色**：`INTEGRATOR` / 受控 QA Runner。
- **命令及工作目录**：
  ```bash
  # 1. 宿主机干净交叉编译 MC 固件 (AT32F435VGT7) 与 TH 固件 (AT32F423CCT7)
  make -C "${RELEASE_ROOT}/src/mcu-p3/motion-controller-mcu" \
       BUILD_DIR="${RELEASE_ROOT}/artifacts/mc" clean pack
  make -C "${RELEASE_ROOT}/src/mcu-p3/color-engine-mcu/io_toggle" \
       BUILD_DIR="${RELEASE_ROOT}/artifacts/th" clean pack

  # 2. 符号表强制核验 (确认核心协议与控制函数真实编入 .text 段)
  arm-none-eabi-nm -n "${RELEASE_ROOT}/artifacts/mc/Marlin_AT32.elf" | \
    grep -E "minimc_proto_init|minimc_proto_poll|handle_mc_home|handle_mc_move|minimc_proto_send_th_gcode"
  arm-none-eabi-nm -n "${RELEASE_ROOT}/artifacts/th/fw_th.elf" | \
    grep -E "minimc_proto_init|minimc_proto_poll|th_control_enqueue_gcode|thermistor_adc_get_telemetry|th_debug_notify_filament"

  # 3. VMware 干净全量编译 soc-ap 五大组件 (--build-only 会先 rm -rf build)
  ssh sushaohua@192.168.77.134 "cd /home/sushaohua/tmp/ai_soc_project/soc-ap && \
    bash tools/deploy_twin.sh --build-only && ctest --test-dir build/runtime --output-on-failure && \
    ctest --test-dir build/forward --output-on-failure && ctest --test-dir build/device_manager --output-on-failure && \
    ctest --test-dir build/ui_gateway --output-on-failure"
  ```
- **准确输入**：Step 1 锁定的 `mcu-p3` 与 `soc-ap` 干净源码树、Step 2 验证通过的 `third_party/install`。
- **输出路径与哈希核验方式**：
  - MC 固件：`${RELEASE_ROOT}/artifacts/mc/{Marlin_AT32.elf,Marlin_AT32.bin,fw_mc.bin}`
  - TH 固件：`${RELEASE_ROOT}/artifacts/th/{fw_th.elf,fw_th.bin,anchor.bin}`
  - AP 二进制：`build/runtime/aisoc_supervisor`、`build/forward/forward_service_daemon`、`build/device_manager/device_manager_daemon`、`build/ui_gateway/ui-gateway`、`build/host/soc-ap` 及静态前端 `browser_hmi/first_release/{index.html,app.js,styles.css}`。
- **成功条件**：MC/TH 交叉编译退出码 `0` 且关键符号全部存在；`soc-ap` 5 个构建目标与全部 CTest 100% 通过。
- **失败停止点与恢复办法**：任一编译或单测失败立即停止，不得进入打包与部署；检查编译日志并按 `REQ-20261105-001` 关联或提报编译缺陷。

---

### Step 4：组合版本（`buildno`）与制品清单封存（`build_manifest.yaml` & `SHA256SUMS`）
- **实际执行位置**：WSL2 宿主机 `${RELEASE_ROOT}`，并同步归档至 `project-control/docs/evidence/hil/builds/build-${BUILDNO}/`。
- **执行者角色**：`INTEGRATOR`。
- **命令及工作目录**：
  ```bash
  # 采集 VMware AP 制品哈希与宿主机 MC/TH 固件哈希，生成不可变 build_manifest.yaml 与 SHA256SUMS
  ssh sushaohua@192.168.77.134 "cd /home/sushaohua/tmp/ai_soc_project/soc-ap && \
    sha256sum build/runtime/aisoc_supervisor build/forward/forward_service_daemon \
              build/device_manager/device_manager_daemon build/ui_gateway/ui-gateway \
              dist/vmware_twin/bin/ui-gateway build/host/soc-ap \
              browser_hmi/first_release/index.html browser_hmi/first_release/app.js \
              browser_hmi/first_release/styles.css" > "${RELEASE_ROOT}/SHA256SUMS.ap"
  sha256sum "${RELEASE_ROOT}/artifacts/mc/"*.{elf,bin} \
            "${RELEASE_ROOT}/artifacts/th/"*.{elf,bin} > "${RELEASE_ROOT}/SHA256SUMS.mcu"
  cat "${RELEASE_ROOT}/SHA256SUMS.ap" "${RELEASE_ROOT}/SHA256SUMS.mcu" > "${RELEASE_ROOT}/SHA256SUMS"
  ```
- **准确输入**：Step 3 产出的全部 AP/UI 与 MC/TH 制品文件。
- **输出路径与哈希核验方式**：
  - `${RELEASE_ROOT}/build_manifest.yaml`（记录 `buildno`、各仓 commit、编译器版本、文件大小、SHA256、Flash 基地址）
  - `${RELEASE_ROOT}/SHA256SUMS`
- **成功条件**：清单内所有制品大小非零、SHA256 完整，且 `build/ui_gateway/ui-gateway` 与 `dist/vmware_twin/bin/ui-gateway` 哈希一致。
- **失败停止点与恢复办法**：若任一文件缺失或哈希不一致，废弃当前 `buildno` 并排查构建脚本，严禁复用已失败的 `buildno`。

---

### Step 5：制品传递与受控部署（含 MCU 烧录计划前置核验、Bootloader 保护与 0% 加热锁死）
- **实际执行位置**：WSL2 宿主机通过 `/mnt/c/Users/EDY/tools/probe-rs/probe-rs.exe`（经人工确认授权后）操作 Windows 宿主连接的双 ST-Link V2。
- **执行者角色**：`INTEGRATOR` 生成烧录计划与哈希清单 ➔ **用户/授权人员确认** ➔ 受控执行器执行。
- **命令及工作目录**：
  ```bash
  # [前置只读核验] 1. 运行设备发现脚本核对双板 Chip UID 与 Probe ID
  python3 /home/sushaohua/workspace/ai_soc_project/test_harness/hil/tools/device_discovery.py < /dev/null

  # [人工授权门禁] 2. 向用户展示 fw_mc.bin 与 fw_th.bin 的路径、字节大小、SHA256 及基地址（严禁覆盖 Bootloader）：
  #   - MC (AT32F435VGT7, Probe 0483:3748:75003800120000334C41534E): base-address 0x08020000 (保护 0x08000000~0x0801FFFF)
  #   - TH (AT32F423CCT7, Probe 0483:3748:): base-address 0x08004000 (保护 0x08000000~0x08003FFF), anchor 0x0803F800
  # 仅在取得用户对当前具体制品的烧录确认（或按问题 2 选定策略校验 Flash 一致）后执行：
  /mnt/c/Users/EDY/tools/probe-rs/probe-rs.exe download \
    --probe "0483:3748:75003800120000334C41534E" --chip AT32F435VGT7 \
    --binary-format bin --base-address 0x08020000 --verify \
    "${WIN_MC_BIN_PATH}" < /dev/null
  /mnt/c/Users/EDY/tools/probe-rs/probe-rs.exe download \
    --probe "0483:3748:" --chip AT32F423CCT7 \
    --binary-format bin --base-address 0x08004000 --verify \
    "${WIN_TH_BIN_PATH}" < /dev/null
  ```
- **准确输入**：Step 4 封存且经用户确认的 `fw_mc.bin`、`fw_th.bin`、`anchor.bin` 及对应 `SHA256SUMS`。
- **输出路径与哈希核验方式**：保存 `probe-rs.exe download --verify` 完整终端日志至 `${EVIDENCE_DIR}/flash_verify.log`，核对 `Erasing ✔ 100%`、`Programming ✔ 100%` 及 verify 成功状态。
- **成功条件**：双板 Chip UID 与清单完全一致，烧录校验 100% 通过，Bootloader 分区零触碰，加热 PWM 输出锁死 0%。
- **失败停止点与恢复办法**：若 `device_discovery.py` 发现探针缺失或 UID 不匹配，或未取得烧录授权，立即中止烧录；严禁执行全片擦除（`erase --all`）或改写 Bootloader 地址段。

---

### Step 6：旧证据与现场状态归档（Pre-Run Legacy Evidence Archival）
- **实际执行位置**：唯一 VMware 虚拟机（`sushaohua@192.168.77.134`）与 WSL2 宿主机。
- **执行者角色**：`INTEGRATOR` / 受控 QA Runner。
- **命令及工作目录**：
  ```bash
  # 1. 将 VMware 当前 /tmp/aisoc_twin_logs 下的旧运行日志、PID 与状态快照打包归档，防止 deploy_twin.sh 清场时丢失历史记录
  ARCHIVE_TS="$(date -u +%Y%m%dT%H%M%SZ)"
  ssh sushaohua@192.168.77.134 "mkdir -p /home/sushaohua/tmp/aisoc_legacy_archives && \
    if [[ -d /tmp/aisoc_twin_logs ]]; then \
      tar -czf /home/sushaohua/tmp/aisoc_legacy_archives/aisoc_twin_logs_pre_${BUILDNO}_${ARCHIVE_TS}.tar.gz -C /tmp aisoc_twin_logs; \
    fi"

  # 2. 将宿主机 /tmp/qa_web_hmi_debug_closure_rev4_3sewzinb 独立 ARCH 文档审阅原始记录归档并校验 SHA256
  mkdir -p "/home/sushaohua/workspace/ai_soc_project/project-control/docs/evidence/doc_reviews/qa_web_hmi_basecases_rev4"
  cp -a /tmp/qa_web_hmi_debug_closure_rev4_3sewzinb/* \
        "/home/sushaohua/workspace/ai_soc_project/project-control/docs/evidence/doc_reviews/qa_web_hmi_basecases_rev4/"
  ```
- **准确输入**：VMware `/tmp/aisoc_twin_logs/*`、宿主机 `/tmp/qa_web_hmi_debug_closure_rev4_3sewzinb/*`。
- **输出路径与哈希核验方式**：对归档包与 `review_receipt.json` 计算 `sha256sum`，核对 `reviewed_sha256 == 67a2c1df609ce14773361a83b803ca414f13bf243be87961f97700ef798ff929`。
- **成功条件**：旧日志归档包与文档审阅记录完整保存且哈希可追溯。
- **失败停止点与恢复办法**：若归档目录不可写或磁盘空间不足，先清理无关临时文件再继续，禁止未归档直接覆盖旧证据。

---

### Step 7：停旧与排他资源释放（Stop Legacy Services & Exclusive Bench Resource Release）
- **实际执行位置**：唯一 VMware 虚拟机（`sushaohua@192.168.77.134`）与 Windows/WSL2 宿主机。
- **执行者角色**：`INTEGRATOR` / 受控 QA Runner。
- **命令及工作目录**：
  ```bash
  # 1. 在 VMware 显式查杀所有残留的 hw_sampler.py 后台轮询进程，并调用 deploy_twin.sh --stop 停止 4 个守护进程
  ssh sushaohua@192.168.77.134 "pkill -9 -f '/tmp/aisoc_twin_logs/hw_sampler.py' 2>/dev/null || true && \
    rm -f /tmp/aisoc_twin_logs/hw_sampler.py /tmp/aisoc_twin_logs/hw_sampler.log && \
    cd /home/sushaohua/tmp/ai_soc_project/soc-ap && bash tools/deploy_twin.sh --stop --port 8080"

  # 2. 核验 VMware 上 4 个守护进程、hw_sampler.py 及 /dev/ttyUSB* 占用者全部清零
  ssh sushaohua@192.168.77.134 "ps -ef | grep -E 'forward_service_daemon|device_manager_daemon|ui-gateway|hw_sampler' | grep -v grep || true"
  ```
- **准确输入**：VMware 正在运行的旧守护进程及残留 `hw_sampler.py`。
- **输出路径与哈希核验方式**：检查 `/tmp/aisoc_twin_logs/*.pid` 均已删除（`! -e`），`fuser /dev/ttyUSB*` 与 `:8080` 均无占用进程，Windows `COM12`/`COM13` 无残留 PowerShell/Python 采集进程占用。
- **成功条件**：VMware 4 个守护进程与 `hw_sampler.py` 100% 退出，`/dev/ttyUSB*`、`COM12`、`COM13` 全部处于空闲可排他绑定状态。
- **失败停止点与恢复办法**：若发现其他未知任务或外部终端占用 `/dev/ttyUSB*` 或 `COM12/COM13`，立即停止并报告冲突，不强行抢占其他任务的台架。

---

### Step 8：双 Debug（`[MC-DBG]` / `[TH-DBG]` 115200）采集先于本轮启动及动作拉起（Pre-Boot Dual Debug Capture Startup）
- **实际执行位置**：WSL2/Windows 宿主机（读取 Windows 物理 `COM12` 与 `COM13`），**必须在板卡冷启动复位和 VMware 服务启动之前率先拉起**。
- **执行者角色**：受控 QA 执行器。
- **命令及工作目录**：
  ```bash
  # 1. 记录宿主机与 VMware UTC 时钟差 (clock offset) 与本轮 run_id 元数据
  RUN_DIR="/home/sushaohua/workspace/ai_soc_project/project-control/docs/evidence/hil/runs/${RUN_ID}"
  mkdir -p "${RUN_DIR}"

  # 2. 启动受控非阻塞双路 Debug 串口持续采集器（使用 SerialPort.ReadExisting() 轮询，严禁 ReadLine() 阻塞，追加写入只读原始日志）
  #    并在采集器就绪后，通过 probe-rs reset 触发 MC 与 TH 同步冷启动，捕获 boot epoch 起点！
  /mnt/c/Users/EDY/tools/probe-rs/probe-rs.exe reset --probe "0483:3748:75003800120000334C41534E" --chip AT32F435VGT7 < /dev/null
  /mnt/c/Users/EDY/tools/probe-rs/probe-rs.exe reset --probe "0483:3748:" --chip AT32F423CCT7 < /dev/null
  ```
- **准确输入**：动态核实角色的 `[MC-DBG]` 端口（当前 `COM12 @ 115200 8N1`）与 `[TH-DBG]` 端口（当前 `COM13 @ 115200 8N1`）。
- **输出路径与哈希核验方式**：
  - `${RUN_DIR}/mc_debug_raw.log`（只追加原始日志）
  - `${RUN_DIR}/th_debug_raw.log`（只追加原始日志）
  - `${RUN_DIR}/action_timeline.jsonl`（旁路记录每个 `case_id`、`action_id`、UTC/单调时间戳、boot epoch）
  - `${RUN_DIR}/serial_binding.json`（记录端口、Chip UID、固件 SHA256、`drop`/`trunc` 初始值 `0`）
- **成功条件**：两路采集器在服务冷启动前已处于活跃写入状态，成功捕获板卡复位后的首条 `[MC-DBG]` / `[TH-DBG]` 帧（`drop=0, trunc=0`）。
- **失败停止点与恢复办法**：若任一 COM 口打开失败（`Access Denied`）或角色特征（`[MC-DBG]` vs `[TH-DBG]`）不匹配，立即停止测试，禁止在缺失 Debug 采集的情况下执行固件相关用例。

---

### Step 9：VMware 四守护进程受控启动、健康检查与版本/状态对账（Controlled 4-Daemon Startup, Health Check & Reconciliation）
- **实际执行位置**：唯一 VMware 虚拟机（`sushaohua@192.168.77.134`）。
- **执行者角色**：受控 QA 执行器 / `INTEGRATOR`。
- **命令及工作目录**：
  ```bash
  # 1. 生成锁定配置 (强制 AISOC_AUTO_BUILD="0" 防止启动时隐式重编译篡改已封存二进制哈希)
  ssh sushaohua@192.168.77.134 "cat > /tmp/aisoc_qa_locked.conf << 'EOF'
  AISOC_MODE=\"hardware\"
  AISOC_UART_DEVICE=\"/dev/ttyUSB0\"
  AISOC_UART_BAUD=\"921600\"
  AISOC_HTTP_PORT=\"8080\"
  AISOC_AUTO_BUILD=\"0\"
  EOF
  cd /home/sushaohua/tmp/ai_soc_project/soc-ap && \
  bash tools/deploy_twin.sh --config /tmp/aisoc_qa_locked.conf && \
  bash tools/deploy_twin.sh --status"

  # 2. 二次校验运行中 4 个守护进程可执行文件 (/proc/<pid>/exe) 的 SHA256 与 Step 4 SHA256SUMS 完全一致
  ssh sushaohua@192.168.77.134 "for pfile in dbus.pid forward.pid device_manager.pid ui_gateway.pid; do \
    pid=\$(cat /tmp/aisoc_twin_logs/\${pfile}); \
    sha256sum /proc/\${pid}/exe; \
  done"
  ```
- **准确输入**：Step 3/4 封存的 VMware `soc-ap` 二进制与 `/tmp/aisoc_qa_locked.conf`（`hardware` 模式、`921600` 波特率、`AISOC_AUTO_BUILD=0`）。
- **输出路径与哈希核验方式**：
  - `/tmp/aisoc_twin_logs/{dbus.pid,forward.pid,device_manager.pid,ui_gateway.pid}`
  - `/tmp/aisoc_twin_logs/{dbus.log,forward_service.log,device_manager.log,ui_gateway.log}`
  - `/proc/<pid>/exe` 的实时 `sha256sum` 与 Step 4 `SHA256SUMS.ap` 100% 匹配。
- **成功条件**：
  1. `deploy_twin.sh --status` 退出码 `0`，4 个进程全部 `[RUNNING]` 且 `State != Z`、`fd/0 -> /dev/null`；
  2. `/proc/<pid>/exe` 哈希与 `build_manifest.yaml` 封存哈希 100% 一致；
  3. 注意：若先测 `BASE-01`（新机引导向导冷启动首次探测），在 `deploy_twin.sh` 启动后**严禁提前运行外部预探测脚本预填缓存**，直接由独立干净 profile 的 Chrome 发起向导触发首次真实探测！
- **失败停止点与恢复办法**：若任一守护进程未存活、`/proc/<pid>/exe` 哈希漂移或业务串口未绑定到真实 MC，立即停止测试并保留 `/tmp/aisoc_twin_logs/` 现场。

---

## 三、 当前材料、工具与物理台架连接缺口盘点表（如实报告，零隐瞒）

| 序号 | 缺口/风险类别 | 当前实测客观现状 | 对 `BASE-01～27` / `J-01` / `DELTA-*` 的影响范围 | 责任角色与解决/处理方式 |
| :--- | :--- | :--- | :--- | :--- |
| **1** | **VMware 工作树落后且含未提交修改与残留 `hw_sampler.py`** | VMware `/home/sushaohua/tmp/ai_soc_project/soc-ap` 当前 `HEAD` 仍为 `333178c6...`，含手动 `scp` 留下的未提交修改，且有 3 个残留 `hw_sampler.py` 进程每 1.5s 发请求。 | 若不清理，会污染本轮版本身份与串口序列号 `seq`。 | **已纳入本确认单 Step 1 & Step 7**：开工时由 `INTEGRATOR` 强制 `git reset --hard 79932746... && git clean -fd` 并杀除 `hw_sampler.py`。 |
| **2** | **宿主机/Docker (`glibc 2.31`, GCC 9.4) 与 VMware (`glibc 2.39+`, GCC 15.2) C++ 运行库版本差异** | 宿主机与 `qa-sandbox:20261029` 为 Ubuntu 20.04，VMware 为新版 Ubuntu（GCC 15.2.0）；且 `qa-sandbox:20261029` 内不含 `arm-none-eabi-gcc`。 | Docker 沙箱用于独立软件门禁验证；真机 MCU 固件需在宿主机用 `arm-none-eabi-gcc` 构建，VMware 运行的 AP 二进制需明确封存基准（见第四节**问题 1**）。 | 由用户在**问题 1** 确认 AP 制品封存方式后，由 `INTEGRATOR` 固定到 Step 3/4。 |
| **3** | **浏览器自动化与全量 `BASE-01～27` + `DELTA-*` 脚本覆盖缺口** | 1. VMware 已安装 `/usr/bin/google-chrome`，但未装 `playwright` Python 包；`test_harness/hil/tests/test_qa_e2e_*.py` 采用原生 WebSocket CDP (`CDPClient`) 驱动真 Chrome。<br/>2. 现有 4 个脚本仅覆盖部分 OOBE、语言/主题、料槽、点动与热拔插，尚未完整覆盖全部 `BASE-01～27`（正/负/恢复拆分子例）、`J-01` 及 `DELTA-DBG/BAUD/COMB` 的逐例四方对账。 | 缺少完整自动化覆盖的用例需由 **QA 用例/工具作者** 扩展 CDP + 双路 Debug 对账脚本（并经非作者独立复核）。 | 登记为 **QA 工具缺口**：由 `COORD` 派发 QA 用例/工具作者补齐并交独立复核，不以现有 `HIL-01~06` 探针冒充完整 basecase。 |
| **4** | **物理台架传感器与外设挂载状态（NTC 热敏电阻、4 路断料传感器、Z 探针、电机限位）** | 根据昨日 `TWIN-50` 实测遥测：MC 热床与喷嘴上报 `3000 ddC` (`300.0°C`，对应裸板 NTC 未接或开路夹持值)，TH 喷嘴上报 `1226 ddC` (`122.6°C`，`adc_raw=2036`)，`filament_present_mask` 在 `0x0F`/`0x00` 间切换。 | 1. `BASE-04`/`BASE-20` 明确规定：“裸板故障哨兵只证明负例，不得作为有效温度正例”；<br/>2. `BASE-14/15/16`（点动/回零/25 点调平）与 `BASE-21`（四路断料逐路触发）要求真实限位、探针、传感器动作或现场物理观察，不能仅凭逻辑坐标或 ACK 判 PASS。 | 凡台架实际未接物理传感器/探针或无物理位移观察条件的子断言，严格按 `qa_web_hmi_basecases_20261103.md` §5 如实记录为 `BLOCKED`（注明物理台架前置条件），**绝不把逻辑坐标或开路哨兵伪报为物理正例 PASS**。 |
| **5** | **`BASE-24` 真实物理拔插业务 USB 子例需人工或受控物理动作配合** | `REQ-20261105-001` 与 `basecases` §2 强制要求：保留 `BASE-24` 实际拔业务 USB 子例，软件 `unbind` 或 SWD 关闭 `USART2` 寄存器不能替代。 | 纯软件/SWD 命令无法完成物理拔除 USB 线缆动作。 | 需在执行 `BASE-24` 时由现场人员配合拔插一端 USB 串口线（见第四节**问题 3**）。 |
| **6** | **本地 `basecases revision 4` 独立 ARCH 复核原始记录尚未归入仓库正式路径** | `/tmp/qa_web_hmi_debug_closure_rev4_3sewzinb/` 下存有会话 `01a1a6dc-33a3-7053-875c-a8ef06502d6d` 的 `manifest.json` 与 `review_receipt.json`，但尚在 `/tmp` 下。 | 若宿主机重启可能丢失 `/tmp` 下的审阅凭据。 | 已纳入 Step 6，在正式执行时归档至 `project-control/docs/evidence/doc_reviews/`。 |

---

## 四、 需用户确认的决策事项（共 3 道选择题）

请确认以下 3 项存在可行替代方案的执行决策（确认后即固定为本轮标准执行规程）：

### 问题 1：AP/UI 部署制品的构建位置与 `build-<buildno>` 哈希封存方式
- **背景**：独立 Docker 沙箱（`qa-sandbox:20261029`，Ubuntu 20.04 `GCC 9.4.0`）负责软件门禁验证，而唯一运行环境 VMware（`192.168.77.134`）为 Ubuntu `GCC 15.2.0` 且已安装验证通过的 `third_party/install`。
- **选项 A（推荐）**：**Docker 沙箱执行独立软件门禁构建与测试 + VMware 从服务器干净检出同一锁定 Commit 独立执行 `--build-only` 构建，并将两端产物哈希同时封存入同一 `build_manifest.yaml`，随后以 `AISOC_AUTO_BUILD=0` 启动并核验 `/proc/<pid>/exe` SHA256**。
  - **时间/台架占用影响**：最快（VMware 干净编译约 25 秒），100% 匹配 VMware 本地 `GCC 15.2.0` / `glibc` 与 `third_party/install` ABI，无跨系统动态库符号兼容风险。
- **选项 B**：在宿主机/Docker 中构建 AP 二进制与 `third_party/install` 并打包传输到 VMware 覆盖运行。
  - **时间/台架占用影响**：每次传输约需额外打包同步 `third_party/install` 动态库（约 80MB），且跨 Ubuntu 20.04 与 Ubuntu 24+/26 系统系统库可能引入 `GLIBC` / `libstdc++` 兼容风险。

### 问题 2：本轮开工时 MC (`AT32F435`) 与 TH (`AT32F423`) 真机固件的烧录核验策略
- **背景**：当前服务器 `mcu-p3` 锁定提交仍为 `016e1236af75f6f19282d6b000f4b1b68bd96cc3`（`TWIN-47` + `TWIN-48`），双板已在昨日烧录过同源固件，但本轮将分配正式 `build-<buildno>` 并要求完整可追溯的制品身份与启动前 Debug 采集。
- **选项 A（推荐）**：**在 Step 3 从服务器干净检出 `mcu-p3@016e1236...` 重新生成 `fw_mc.bin` 与 `fw_th.bin` 并登记到 `build_manifest.yaml`；在 Step 5 向您呈报准确文件大小、SHA256 与基地址（MC `0x08020000`、TH `0x08004000`），获批后通过 `probe-rs.exe download --verify` 重新烧录并校验，确保片上 Flash 与本轮 `build-<buildno>` 100% 绑定**。
  - **时间/台架占用影响**：烧录加校验耗时约 **38 秒**（MC 约 31s + TH 约 7s），可 100% 保证片上固件身份与本轮封存制品字节级一致。
- **选项 B**：在 Step 3 干净编译后，先通过 `probe-rs.exe read` 读回双板 Flash 应用区字节并与新编译的 `.bin` 比对 SHA256；若字节完全一致则免去擦写重刷，仅在 Step 8 执行 `probe-rs.exe reset` 冷复位启动。
  - **时间/台架占用影响**：节省约 30 秒 Flash 擦写时间，但需额外编写 Flash 读回截取比对脚本。

### 问题 3：含人工物理动作/现场观察用例（`BASE-24` 物理拔 USB、`BASE-21` 断料触发、`BASE-14/15/16` 机械动作观察）的执行窗口编排
- **背景**：`BASE-01～27` 与 `DELTA-*` 中，绝大部分软件/协议/级联/SWD 故障注入用例可全自动连续执行，但 `BASE-24`（真实物理拔插业务 USB）、`BASE-21`（四路断料传感器物理触发）及机械位移/限位观察需要现场物理配合或确认台架物理条件。
- **选项 A（推荐）**：**分两阶段执行——第一阶段（无人值守全自动批次）先连续跑完所有无需人工搬动硬件的 `BASE`、`J-01` 及 `DELTA-DBG/BAUD/COMB` 用例并产出阶段结果；第二阶段（集中人工物理配合窗口）一次性集中提示您配合完成 `BASE-24` 物理拔插 USB 与具备条件的传感器/机械观察用例**。
  - **时间/台架占用影响**：最大化节省您的等待时间（无需在电脑前盯守数十分钟自动化执行），且第一阶段发现的任何软件/协议缺陷可立即并行交开发修复。
- **选项 B**：严格按 `BASE-01` ➔ `BASE-27` 编号顺序单趟串行执行，遇到需物理动作的用例时实时暂停并等待您操作后再继续下一编号。
  - **时间/台架占用影响**：顺序直观，但需要您在测试全程保持在线响应，台架占用窗口较长。

---

## 五、 用户确认与裁决记录（`2026-11-05T11:55:34+08:00`）

- **确认人**：`sushaohua`（通过 COORD 交互式会话 `ff2fb105-fd84-4ecb-b1e6-8f8eb00badc6` `ask_question` 逐项确认）
- **问题 1 裁决**：**选项 A**（Docker 沙箱独立完成软件门禁构建测试 + VMware 从服务器干净检出同一锁定 Commit 独立执行 `--build-only`，两端产物 SHA256 同时封存入 `build_manifest.yaml`，并以 `AISOC_AUTO_BUILD=0` 启动且核验 `/proc/<pid>/exe` 哈希）。
- **问题 2 裁决**：**选项 A**（从服务器干净检出 `mcu-p3@016e1236` 重新生成 `fw_mc.bin` 与 `fw_th.bin` 并封存 SHA256；在 Step 5 呈报准确文件大小、哈希与基地址 `MC 0x08020000`、`TH 0x08004000` 获批后，通过 `probe-rs download --verify` 重新烧录校验）。
- **问题 3 裁决**：**选项 A**（分两阶段执行——第一阶段无人值守全自动批次先连续跑完所有无需人工搬动硬件的 `BASE`、`J-01` 及 `DELTA-DBG/BAUD/COMB` 用例；第二阶段集中人工物理配合窗口一次性提示配合完成 `BASE-24` 物理拔插业务 USB 及具备条件的传感器/机械观察用例）。
- **流程放行裁决**：**批准**（按上述 9 步编译部署执行确认单推进 `REQ-20261105-001`，并同步放行 `AUTO-07` 实现）。
