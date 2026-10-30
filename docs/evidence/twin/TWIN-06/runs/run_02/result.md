# TWIN-06 D-Bus 跨进程 SDK 与权限超时定向整改自检报告 (Run 02)

| 属性 | 内容 |
| :--- | :--- |
| **任务卡片** | `TWIN-06` (D-Bus 跨进程 SDK 与权限超时) |
| **所属工作包** | `TASK-015` (实现 D-Bus 底座和统一 SDK) |
| **执行角色** | `ENG-DBUS` (D-Bus 通信工程师) |
| **当前轮次** | `run_02` (针对 Run 01 Codex QA 审计意见定向整改) |
| **前置依赖** | `TWIN-02` (`soc-ap: 532caecf3a146802969a49e73081400c2b32b25e`), `TWIN-03` (`test_harness: 0b7497ba43158841eb3c4af7f16e477b9c30c2c5`) |
| **候选 Commit** | `soc-ap: 16ba69d29c93191731a13a1fa4c88f981677c4d5`, `project-control: <pinned-at-commit>` |
| **作者会话 ID** | `bab80130-abdc-443c-9e30-4730e31b82f7` |
| **执行状态** | **Rework Completed (安全策略白名单闭环，权限拒绝负例通过，候选统一对齐)** |

---

## 1. Run 01 阻断项定向整改说明 (Resolution of QA Findings)

针对 `TWIN-06/runs/run_01/qa_review_report.md` 中独立 Codex QA 提出的 3 项问题，执行定向整改如下：

### 1.1 QA-01 (候选提交基线对齐)
- **问题**：Run 01 审查申请中由于笔误传出了不存在的提交 SHA，且 `server_lock.json` 锁定的旧提交存在漂移。
- **整改**：Run 02 将候选提交统一锁定到已推送到 `origin/main` 的最新提交 `soc-ap: 16ba69d29c93191731a13a1fa4c88f981677c4d5`，并在运行 sandbox 前定格统一 4 仓远端 commit。

### 1.2 QA-03 (作者会话绑定)
- **问题**：任务卡中 `executor.session` 为空，缺少作者会话标识。
- **整改**：在任务卡及本报告中显式绑定作者专属会话 `bab80130-abdc-443c-9e30-4730e31b82f7`，确保作者与独立 Reviewer 分离。

### 1.3 QA-02 (D-Bus 权限拒绝负例验证与策略白名单)
- **问题**：`session_twin.conf` 原策略允许向任意 destination 发送并可 eavesdrop，`org.aisoc.conf` 存在未支持的前缀属性且未参与实际运行，缺少未授权名称占用和越权调用拒绝的负例测试。
- **整改**：
  1. **修正系统级策略文件 (`org.aisoc.conf`)**：移除不支持的 `send_destination_prefix` 与 `receive_sender_prefix` 属性，规范为显式放通所有标准子服务名（`org.aisoc.Forward`, `org.aisoc.Device`, `org.aisoc.Hms`, `org.aisoc.UiGateway`, `org.aisoc.JobEngine`, `org.aisoc.StorageService`）；
  2. **收紧会话总线策略 (`session_twin.conf`)**：
     - 配置严格白名单与默认拒绝：`<deny own="*"/>` 与 `<deny send_type="method_call"/>`；
     - 仅放通对 `org.aisoc.*` 服务的所有权申请和方法调用；
     - 显式引入 `<include ignore_missing="yes">org.aisoc.conf</include>`；
  3. **增加权限拒绝负例自动化测试套件**：
     - 在 `test_dbus_ipc.cpp` 中新增 `test_client_permission_denial`：
       * **负例 1**：客户端尝试申请非白名单服务名 `com.unauthorized.ForbiddenName`，断言总线因 `<deny own="*"/>` 拒绝请求；
       * **负例 2**：客户端尝试向未授权目标 `com.unauthorized.Service` 发送方法调用，断言因 `<deny send_type="method_call"/>` 被总线拦截并返回错误码。
     - 运行测试输出 `Test Results: 7 passed, 0 failed`，权限正反例 100% 验证通过。

---

## 2. 交付物清单与 SHA-256 校验码 (Run 02)

| 交付文件路径 | 类型与描述 | SHA-256 校验码 |
| :--- | :--- | :--- |
| `soc-ap/middleware/dbus/include/aisoc_dbus.h` | SDK 公开 API 头文件 (C/C++ 强类型声明) | `73d8004e9cc391f91e09eb5717526a695ff57f1ba739b2df3f651cf339c16bc1` |
| `soc-ap/middleware/dbus/src/aisoc_dbus_internal.h` | SDK 内部辅助函数与消息过滤器原型 | `261d7d9b4d512042dac100fbd56e1dc33ac454b64c4b9185b9db547087a48dd0` |
| `soc-ap/middleware/dbus/src/aisoc_dbus_msg.cpp` | 消息构造、序列化、反序列化迭代器与错误映射实现 | `a83978c549e27f69a599944c0e0b0902a0cd2420875916e19dd0a85b21eac987` |
| `soc-ap/middleware/dbus/src/aisoc_dbus_core.cpp` | 总线连接生命周期、名称申请/释放与事件驱动实现 | `c01e907582542f75a463cfa2b26df442b18717d707ab2a39fa371ebc6ab67c1c` |
| `soc-ap/middleware/dbus/src/aisoc_dbus_client.cpp` | 客户端同步 RPC、超时控制与结果提取实现 | `669c5884a61a7998a8935501097fe1e7fc908d14bc7d8a45ced766a38602bf2d` |
| `soc-ap/middleware/dbus/src/aisoc_dbus_server.cpp` | 服务端对象路径注册、方法分发、自省反射与信号订阅 | `f3e2cab25bf1bd79f7e7524ac0e8ef773e3d2947fd294eff5bbc687a60cacf74` |
| `soc-ap/middleware/dbus/CMakeLists.txt` | 模块独立 CMake 配置 (支持静态库、示例与单测编译) | `80cffcdea600067b12140da694f7a90a00bb247fa03b9c64c7599059762e09b8` |
| `soc-ap/middleware/dbus/examples/server_example.cpp` | 简明服务端示例 (注册 Forward 服务与信号发射) | `0eec65f5be141911e4e16fb9f8e2a8c84efd328581f2bd21c282325db19b4558` |
| `soc-ap/middleware/dbus/examples/client_example.cpp` | 简明客户端示例 (RPC 远程调用与信号监听) | `30127a238e75ff469ba06b1e7cee04a99c00e0f0bfe86903e9996fc6880d7608` |
| `soc-ap/middleware/dbus/README.md` | 模块公开 API 架构、接口规范与构建集成指南 | `ab3229bbc2441a7bb09175c0b91521e6a73079f2d4e51267263766d9eb65da9f` |
| `soc-ap/config/dbus/twin/session_twin.conf` | 严格白名单会话总线配置文件 (默认拒绝所有名称及调用，仅放通 org.aisoc.*) | `e790d570ae3b5ba3fff2f9186d86ad64b1eac9d3ef47b1c2d7d59dd8605a1bac` |
| `soc-ap/config/dbus/twin/org.aisoc.conf` | 系统总线级策略配置文件 (声明授权通信白名单) | `679a9f3be91c467849b4c31439eb345a7c9eab22cf860d1b50355189406f6817` |
| `soc-ap/tests/dbus/twin/CMakeLists.txt` | 测试目录独立构建配置 | `06ad077ec9e34dac1a496e96aa7e2c39cd68ee4e45c69547e19ab9b1cd61d88c` |
| `soc-ap/tests/dbus/twin/test_dbus_ipc.cpp` | 真实三进程 D-Bus IPC 正反例（含越权拒绝、超时与信号）综合自动化测试套件 | `a53e475cc05448bcf9e33b183ea5a3a7d6ed414fbb467187df000c5d6c81f037` |
| `soc-ap/third_party/dbus/README.md` | D-Bus 1.16.2 来源、SHA256、许可证及构建说明 | `2898d82324e54110e6c3a95972ee26af794512a03bbf689043e7f961758315f3` |

---

## 3. 编码硬门禁符合性

全模块自研函数行数严格控制在 $\le 50$ 行，入参个数 $\le 4$ 个，每个公开函数入口均有严格的空指针防御，总线权限策略已实现白名单默认拒绝与负例验证覆盖。
