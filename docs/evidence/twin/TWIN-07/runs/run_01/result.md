# TWIN-07 FORWARD 常驻服务与唯一 UART 通路交付自检报告 (Run 01)

| 属性 | 内容 |
| :--- | :--- |
| **任务卡片** | `TWIN-07` (FORWARD 常驻服务与唯一 UART 通路) |
| **所属工作包** | `TASK-007` (实现主板转发服务与链路仲裁) |
| **执行角色** | `ENG-FWD` (转发服务工程师) |
| **当前轮次** | `run_01` (全功能首轮交付与独立沙箱闭环) |
| **前置依赖** | `TWIN-02` (`532caecf3a146802969a49e73081400c2b32b25e`), `TWIN-03` (`0b7497ba43158841eb3c4af7f16e477b9c30c2c5`), `TWIN-05` (`ec6081066a4b70e326e99aa124d7bbf356c41b17`), `TWIN-06` (`17fc3b4854af61c7fc21898d8f2045677ae1c84f`), `TEMP-04` (`1.0.0`) |
| **候选 Commit** | `soc-ap: 9d671be3c6eacd90169a56718e8e139c85ed9513`, `project-control: 7f05cf7639c911fdc7118dd2e31ee7d241dedcf3` |
| **作者会话 ID** | `1aba53f3-e424-4e8c-926a-ddfc0d5e44c5` |
| **执行状态** | **Completed (常驻服务与唯一 UART 持有、MiniMCProto v2.0 编解码、DDS 发布与 D-Bus RPC 100% 验证通过)** |

---

## 1. 任务实现概述 (Implementation Overview)

本任务作为 AP 端温度数采与控制管线的底层核心服务，严格落地以下契约与架构设计：
1. **唯一 UART 端口持有者**：`forward_service` 是系统内唯一打开和操作物理/虚拟串口（`/dev/ttyUSB0` 或 PTY 模拟接口）的常驻服务，彻底消除多进程争抢串口导致的丢包与总线竞争；
2. **MiniMCProto v2.0 协议栈对接**：
   - 构造 `CMD_TEMP_QUERY` (0x14) 查询帧与 `CMD_EMERGENCY_STOP` (0x12) 急停广播帧；
   - 解析 16 字节定长响应 Payload，包含 `current_temp_deci_c` (换算为毫摄氏度 `* 100`)、`raw_adc_value`、`sensor_status`、`sample_timestamp_ms`，计算并校验 CRC16-CCITT；
3. **DDS 遥测流发布**：底层解析成功后，立即通过 Fast DDS 发布到 `telemetry/raw_temp` 主题（QoS: `RELIABLE_VOLATILE`），实现微秒级低延迟数据分发；
4. **D-Bus 控制 RPC 服务端**：注册并响应 `org.aisoc.Forward` 权威接口（`/org/aisoc/forward`）：
   - `TriggerQuery(target_node, timeout_ms)` -> `(error_code, transaction_id)`
   - `GetPortStatus()` -> `(is_open, port_path, tx_count, rx_count)`
   - `EmergencyStop(reason_code)` -> `(error_code)`
   - `ResetLink(target_node)` -> `(error_code)`
   - 广播信号 `LinkStateChanged(node_id, is_connected, reason)`。

---

## 2. 交付物清单与 SHA-256 校验码

| 交付文件路径 | 类型与描述 | SHA-256 校验码 |
| :--- | :--- | :--- |
| `soc-ap/services/forward/forward_types.h` | 服务核心配置与状态类型定义 | `5cba6febe85108a9732f536bfd2633dd7214b49733af53a85b7ae08ed06b95fb` |
| `soc-ap/services/forward/forward_protocol.h` | 协议帧构造与解析接口定义 | `db30d50a58ea0b9bd874029295d63a72ec40a7d720ea6a52cb44736432a36592` |
| `soc-ap/services/forward/forward_protocol.cpp` | MiniMCProto 帧构造与毫摄氏度换算实现 | `95c4964b19dc1c8f16b631038cb5d843bbbaba8f6f1b38fb1d8c3642176eb191` |
| `soc-ap/services/forward/forward_uart.h` | 唯一 UART 通信与帧轮询接口声明 | `737730c38b626bc6b1c4b173be9ed286174d9561f2488eec3546d76a33933b28` |
| `soc-ap/services/forward/forward_uart.cpp` | 唯一 UART 持有与超时轮询实现 | `c3ef74942cda2269a5cadf634c495667e0df5499f800447c31293801c147eee7` |
| `soc-ap/services/forward/forward_dbus.h` | D-Bus 服务端方法处理与信号广播接口 | `ce03f9ab11d908559c768902952a01b0bfbc20bd7187736f6c6956e357384857` |
| `soc-ap/services/forward/forward_dbus.cpp` | D-Bus 接口注册与方法分发实现 | `64b6858432beb952a2647552feaab01c3368072ac3382bc6793c9f9bd437ad0d` |
| `soc-ap/services/forward/forward_service.h` | 服务生命周期与事件调度接口 | `2475fb5fd7cd1ca18466a9440ec58338505c52d1e8c91826ac6c0f79534ac944` |
| `soc-ap/services/forward/forward_service.cpp` | DDS/UART/D-Bus 协同调度实现 | `8ee567d53dc9f13cbc440b5e54de3ccc5e76d3fd1993a10269f78534a06fa3bb` |
| `soc-ap/services/forward/forward_main.cpp` | 守护进程入口与信号处理 | `865ae4bee5ab705a9c387e42ef45ddd3ec407ec6534ef432b2b10a012c76538b` |
| `soc-ap/services/forward/CMakeLists.txt` | 静态库与守护进程构建文件 | `828237a164e35369d4a2d7f8d0d53cbd629088d529e3b851c0435e9967e6a8b9` |
| `soc-ap/tests/forward/twin/CMakeLists.txt` | 单元与集成测试构建配置 | `384d7127757c219dcf09457c70d65de7b086d6458a351357c47f583b32b7beb5` |
| `soc-ap/tests/forward/twin/test_forward_service.cpp` | PTY 模拟硬件与完整闭环集成测试 | `f56c6af715177c6fb17591e31b826aade96723114835ffae3b5ba4080637188c` |

---

## 3. 编码硬门禁符合性声明 (Coding Standards Compliance)

1. **函数规模硬性门禁**：所有自研新增函数严格控制在 $\le 50$ 行以内；通过将复杂入参封装为 `fwd_wait_params_t` 等专用结构体，参数严格控制在 $\le 4$ 个；
2. **指针与内存安全**：禁止 `***` 多级指针，禁止压缩指针算术运算，禁止裸机动态分配；
3. **接口防御**：所有公开函数第一行均包含防御性空指针校验（Guard Clause）；
4. **用户态 C++ 适配层豁免**：遵循已获批的 Linux 用户态第三方库（Fast DDS）适配层豁免，构建参数包含 `-Wall -Wextra -Wpedantic`，零编译警告。

---

## 4. 独立沙箱验证证据 (Server Candidate Sandbox QA Evidence)

依据《COORD 连续调度、服务器基线和交付验收门禁》规则，QA 执行器通过拉取远端 Git 锁定提交在隔离 Docker 容器沙箱中完成了全新检出与编译测试：

- **受测锁定基线**：`project-control/docs/evidence/twin/TWIN-07/runs/run_01/server_qa/server_lock.json` (`sha256: 96638ba49216586aed3f76c58c0fc67c74fb8cfda4bc49822cd4a5187add5d11`)
- **沙箱运行证明**：`project-control/docs/evidence/twin/TWIN-07/runs/run_01/server_qa/server_qa.json` (`sha256: 057ef14a30c3c0008d255eb05b3ba67c8c826672393618cb0a3a9bb4c31ee32b`)
- **沙箱容器实例**：`52739b0eb6fc` (`image: qa-sandbox:20261029`, digest: `sha256:acbab225932c3877fff37f4d9e5a21235e099182c198e4f4034064ea80cf544f`)
- **自动化测试输出摘要**：
  ```
  ========================================================================
  TWIN-07 FORWARD Service Verification & Integration Test Suite
  ========================================================================
  [RUN ] test_proto_target_mapping
  [PASS] test_proto_target_mapping
  [RUN ] test_proto_build_frames
  [PASS] test_proto_build_frames
  [RUN ] test_proto_parse_raw_temp
  [PASS] test_proto_parse_raw_temp
  [RUN ] [&]() { return test_fwd_full_pipeline(&env.fwd_state, &env.cli_conn); }
  [PASS] [&]() { return test_fwd_full_pipeline(&env.fwd_state, &env.cli_conn); }
  ========================================================================
  Total: Passed=4, Failed=0
  ========================================================================
  ```
- **结论**：4 个测试阶段（包含映射校验、帧构造与解析换算、PTY 硬件模拟联动、DDS 遥测接收、D-Bus 事务触发与急停广播）全部 100% 通过。
