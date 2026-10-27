# CR-04 交付与验收记录：AP宿主健壮查询与负例防御改造

| 字段 | 属性 / 内容 |
| :--- | :--- |
| **任务卡片** | `CR-04` |
| **所属计划** | `PLAN-CASCADE-RECOVERY-20261027 v1.1` |
| **执行者 / 角色** | `9e5411f4-acad-421e-b487-9e68b9483320` (COORD) |
| **对应底层规范** | [`CONTRACT-CASCADE-QUERY-20261027`](file:///home/sushaohua/workspace/ai_soc_project/soc-ap/contracts/minimcproto/cascade-query.md) |
| **治理漏洞** | F01（命令冲突）、F02（负例误报 SUCCESS）、F03（持续 EAGAIN 死循环）、F04（波特率静默退化与参数解析）、F05（日志时戳与原始帧截断） |
| **涉及仓库** | `soc-ap`（提交 `4445c8fedc21bafef5e6c971fcb54cec703f0e71`）、`test_harness`（提交 `6c61ce6e51cf83d7fb58d319c23cb91bf95786cb`） |
| **验收状态** | **PASS (100% 14/14 黄金用例及 CTest 通过)** |

---

## 1. 改造内容与漏洞闭环

### 1.1 `serial_posix` 传输层硬化 (F03, F04)
- **严格波特率校验与无静默回退**：重构 `baud_to_speed`，显式校验仅支持的标准波特率，遇到未受支持的波特率直接返回 `false`，由 `serial_open` 拦截并返回失败，彻底杜绝历史静默降级为 115200 的缺陷。
- **有界写阻塞与超时保护**：重构 `serial_write`，在遇到 `EAGAIN` / `EWOULDBLOCK` 时，通过 `poll(POLLOUT)` 进行单调有界等待（最大 1000ms），严禁 CPU 无界空转；写入超时或物理断开立即返回失败并传出已写字节数。

### 1.2 模块化命令构建与严格四层响应判定 (F01, F02, F05)
- 新增 `soc-ap/core/host/query.h` 与 `soc-ap/core/host/query.cpp`，拆解 `main.cpp` 职责：
  - **第 1 层：物理帧完整性与 CRC**：由 `StreamParser` 保证，噪声字节静默过滤，损坏 CRC 丢弃；
  - **第 2 层：响应属性防回环**：严格检验 `flags & 0x02 != 0`（`IS_RESPONSE`），拦截并忽略物理回显帧，等待至超时；
  - **第 3 层：上下文事务关联**：严格匹配 `src_id == target_node`、`dst_id == 0x01` 以及 `seq == req_seq`，拦截节点错位与旧帧；
  - **第 4 层：业务命令与载荷结构**：严格检验操作码（`CMD_VERSION_REPORT` / `CMD_PONG`）与固定载荷长度（16B / 12B），识别并解析 `CMD_NACK` 报错退出。
- **标准退出码与纯净 JSON 格式**：
  - `0`: `EXIT_SUCCESS`
  - `1`: `EXIT_TIMEOUT`
  - `2`: `EXIT_CORRELATION_ERR`
  - `3`: `EXIT_IO_ERROR`
  - `4`: `EXIT_USAGE_ERROR`
  - 成功与失败均按契约输出单行标准 JSON。

---

## 2. 验收证据与测试结果

### 2.1 独立 14 项黄金用例回归 (`run_query_cases.py`)
```text
[OK] 黄金用例集静态校验通过: test_harness/test_cases/cascade/query_cases.json (含 4 正例, 10 负例)
===========================================================================
       执行 AP 宿主程序黑盒 PTY 级联查询测试: soc-ap/build/host/bin/soc-ap
===========================================================================
[PASS] CAS-POS-001  | 退出码: 0 (期望 0) | 耗时: 0.061s | AP 直接查询 MC 固件版本 (单跳 GET_VERSION)
[PASS] CAS-POS-002  | 退出码: 0 (期望 0) | 耗时: 0.062s | AP 经 MC 级联查询 TH 固件版本 (双跳 GET_VERSION 原生透明路由)
[PASS] CAS-POS-003  | 退出码: 0 (期望 0) | 耗时: 0.062s | AP 向 MC 发送心跳探活与时延测量 (单跳 PING/PONG)
[PASS] CAS-POS-004  | 退出码: 0 (期望 0) | 耗时: 0.062s | AP 经 MC 级联向 TH 发送心跳探活 (双跳 PING/PONG 原生透明路由)
[PASS] CAS-NEG-001  | 退出码: 1 (期望 1) | 耗时: 0.352s | 信道持续静默无响应 (Silence / Timeout)
[PASS] CAS-NEG-002  | 退出码: 1 (期望 1) | 耗时: 0.362s | 信道回显原请求报文 (Echo / Reflection Loop)
[PASS] CAS-NEG-003  | 退出码: 1 (期望 1) | 耗时: 0.362s | 响应源节点错位 (Target Mismatch: 查 TH 却收到 MC 回包)
[PASS] CAS-NEG-004  | 退出码: 1 (期望 1) | 耗时: 0.362s | 流水号错位 (Stale / Corrupted Sequence Number)
[PASS] CAS-NEG-005  | 退出码: 2 (期望 2) | 耗时: 0.062s | 操作码定义冲突 (Command Opcode Conflict: 收到 0x03 魔数或非法应答)
[PASS] CAS-NEG-006  | 退出码: 2 (期望 2) | 耗时: 0.062s | 载荷长度截断不匹配 (Truncated / Malformed Payload Length)
[PASS] CAS-NEG-007  | 退出码: 1 (期望 1) | 耗时: 0.362s | 帧尾 CRC-16 损坏 (Corrupted CRC-16)
[PASS] CAS-NEG-008  | 退出码: 2 (期望 2) | 耗时: 0.062s | 终端从机回发标准拒绝报文 (CMD_NACK with Error Code)
[PASS] CAS-NEG-009  | 退出码: 0 (期望 0) | 耗时: 0.062s | 信道夹杂 DWIN 屏幕噪声抗扰 (Inter-packet Noise Resilience)
[PASS] CAS-NEG-010  | 退出码: 4 (期望 4) | 耗时: --s    | 命令行非法参数拒绝 (CLI Argument Defense)
---------------------------------------------------------------------------
测试汇总: 总用例 14, 通过 14, 失败 0
===========================================================================
```

### 2.2 CTest 全量套件执行
```text
Test project /home/sushaohua/workspace/ai_soc_project/soc-ap/build/host
    Start 1: host_runtime_smoke
1/2 Test #1: host_runtime_smoke ...............   Passed    0.11 sec
    Start 2: cascade_query_cases
2/2 Test #2: cascade_query_cases ..............   Passed    2.32 sec

100% tests passed, 0 tests failed out of 2

Total Test time (real) =   2.43 sec
```

### 2.3 代码规范与硬性门禁核验
- **函数行数门禁**：所有自研非结构体函数均严格控制在 50 行以内（最大函数为 45 行）。
- **入参个数门禁**：所有自研函数参数均严格 $\le 4$ 个。
- **内存与指针安全**：零动态堆内存分配（无 new/delete/malloc/free），显式指针边界与空指针 Guard Clause，无二级以上多重指针，完全符合嵌入式及 host 驱动开发规范。
