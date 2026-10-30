# TWIN-06 D-Bus 跨进程 SDK 与权限超时定向整改自检报告 (Run 03)

| 属性 | 内容 |
| :--- | :--- |
| **任务卡片** | `TWIN-06` (D-Bus 跨进程 SDK 与权限超时) |
| **所属工作包** | `TASK-015` (实现 D-Bus 底座和统一 SDK) |
| **执行角色** | `ENG-DBUS` (D-Bus 通信工程师) |
| **当前轮次** | `run_03` (针对 Run 02 Codex QA 审计意见全面闭环) |
| **前置依赖** | `TWIN-02` (`soc-ap: 532caecf3a146802969a49e73081400c2b32b25e`), `TWIN-03` (`test_harness: 0b7497ba43158841eb3c4af7f16e477b9c30c2c5`) |
| **候选 Commit** | `soc-ap: 17fc3b4e723528b1e4c760416b252069fa4d1b82`, `project-control: <pinned-at-commit>` |
| **作者会话 ID** | `bab80130-abdc-443c-9e30-4730e31b82f7` |
| **执行状态** | **Rework Completed (7套独立测试集命名打标、并发与吞吐基准覆盖、分支规则与远端锁对齐)** |

---

## 1. Run 02 阻断项定向整改说明 (Resolution of QA Findings)

针对 Run 02 Codex QA 审查报告（`TWIN-06/runs/run_02/qa_review_report.md`）及交付门禁演进，执行闭环整改如下：

### 1.1 TWIN06-QA-01 (候选锁定基线与分支核验对齐)
- **分支规则明确**：交付门禁（`delivery_and_coord_gate.md`）明确：各仓按各自登记的分支核验，MCU 仓库依据 `workspace.json` 合法使用 `origin/feat/soc-debug` 分支，分支不同于 `main` 本身不再作为拒绝理由；
- **QA 运行器支持**：QA 运行器（`qa_runner.py`）已更新，缺省使用各仓配置的默认分支，保留 `feat/soc-debug` 完整分支名称；
- **候选前置对齐**：Run 03 在启动沙箱前先定格统一四仓远端提交，确保 `server_lock.json` 与受审候选提交完全一致无漂移。

### 1.2 测试套件结构强化与自研函数规模门禁
- **显式测试集打标**：重构 `soc-ap/tests/dbus/twin/test_dbus_ipc.cpp`，在 stdout 显式输出 7 套独立测试集的执行结果：
  1. `[TEST SUITE: GuardClause] PASS`
  2. `[TEST SUITE: TimeoutHandling] PASS`
  3. `[TEST SUITE: CrossProcessMethodCall] PASS`
  4. `[TEST SUITE: Concurrency] PASS`
  5. `[TEST SUITE: PerformanceThroughput] PASS` (度量 100 次 RPC 调用吞吐耗时)
  6. `[TEST SUITE: PermissionDenial] PASS` (未授权服务名申请与越权方法调用拦截)
  7. `[TEST SUITE: BroadcastSignal] PASS`
- **执行时序与生命周期安全**：将广播信号测试调整到所有 RPC、并发与权限测试完成后执行，避免服务端因收到退出信号提前终止事件循环；
- **函数行数门禁达标**：将测试套件调用逻辑拆解为 `run_connected_client_suites` 辅助函数，`main` 函数控制在 35 行以内，全模块所有自研函数严格遵守 $\le 50$ 行、$\le 4$ 参数硬门禁。

### 1.3 TWIN06-ARCH-01 (移除 own_prefix 通配并增加未授权名称负例)
- **策略文件收敛**：从 `session_twin.conf` 和 `org.aisoc.conf` 中彻底移除 `<allow own_prefix="org.aisoc"/>` 通配指令，仅保留 6 个明确获批的服务名（Forward, Device, Hms, UiGateway, JobEngine, StorageService）白名单；
- **负例用例补齐**：在 `test_client_permission_denial` 中增加对命名空间内未授权服务名 `org.aisoc.UnapprovedService` 的申请拒绝断言，100% 验证精确白名单生效。

---

## 2. 交付物清单与 SHA-256 校验码 (Run 03)

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
| `soc-ap/config/dbus/twin/session_twin.conf` | 严格白名单会话总线配置文件 (默认拒绝所有名称及调用，仅放通获批 6 服务) | `95bf44ab20b8feb90c767dceb68bcc8fcee13c20e7380a2590f4a475ac67524a` |
| `soc-ap/config/dbus/twin/org.aisoc.conf` | 系统总线级策略配置文件 (声明授权通信白名单，无 own_prefix) | `f1359ae1a3af1e171295ea60a27bd1c11893b9861bad76354c3d9ea2bbc74d7d` |
| `soc-ap/tests/dbus/twin/CMakeLists.txt` | 测试目录独立构建配置 | `06ad077ec9e34dac1a496e96aa7e2c39cd68ee4e45c69547e19ab9b1cd61d88c` |
| `soc-ap/tests/dbus/twin/test_dbus_ipc.cpp` | 真实三进程 D-Bus IPC 正反例（含 7 套独立测试集、未授权前缀拒绝、并发吞吐与信号）综合自动化测试套件 | `3bab792f9487d2f396598efcde25181d306a5272e9c156b965648ec87012442d` |
| `soc-ap/third_party/dbus/README.md` | D-Bus 1.16.2 来源、SHA256、许可证及构建说明 | `2898d82324e54110e6c3a95972ee26af794512a03bbf689043e7f961758315f3` |

---

## 3. 编码硬门禁符合性

全模块自研函数行数严格控制在 $\le 50$ 行，入参个数 $\le 4$ 个，每个公开函数入口均有严格的空指针防御，总线权限策略已实现白名单默认拒绝与负例验证覆盖，测试套件按 7 个独立测试集清晰组织并输出。
