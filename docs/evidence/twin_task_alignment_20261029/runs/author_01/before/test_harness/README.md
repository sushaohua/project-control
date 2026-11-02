# QA Independent Test Harness (test_harness)

本仓库维护独立的 QA 自动化验证资产、协议静态检查基准与硬件在环（HIL）物理夹具工具。

## 目录结构

* [`static_checks/`](file:///home/sushaohua/workspace/ai_soc_project/test_harness/static_checks/)：协议编解码测试套件与参考向量校验工具：
  * [`minimcproto/`](file:///home/sushaohua/workspace/ai_soc_project/test_harness/static_checks/minimcproto/)：MiniMCProto v2.0 基础帧编解码参考实现与测试运行器。
  * [`cascade/run_query_cases.py`](file:///home/sushaohua/workspace/ai_soc_project/test_harness/static_checks/cascade/run_query_cases.py)：**AP-MC-TH 级联查询独立黄金用例运行与校验器 (CR-02Q)**，支持向量自校验与宿主黑盒 PTY 回归。
* [`test_cases/`](file:///home/sushaohua/workspace/ai_soc_project/test_harness/test_cases/)：跨节点协议黄金测试用例集（JSON 契约向量）：
  * [`minimcproto/vectors.json`](file:///home/sushaohua/workspace/ai_soc_project/test_harness/test_cases/minimcproto/vectors.json)：离线帧层编解码测试向量。
  * [`cascade/query_cases.json`](file:///home/sushaohua/workspace/ai_soc_project/test_harness/test_cases/cascade/query_cases.json)：**AP-MC-TH 级联只读查询独立黄金用例集 (CR-02Q)**（含 4 组正向单/双跳黄金帧与 10 组负向防御测试场景）。
* [`hil/`](file:///home/sushaohua/workspace/ai_soc_project/test_harness/hil/)：硬件在环（Hardware-in-the-Loop）物理测试台架与工装资产：
  * [`guides/probe_rs_hardware_fault_injection.md`](file:///home/sushaohua/workspace/ai_soc_project/test_harness/hil/guides/probe_rs_hardware_fault_injection.md)：基于 probe-rs 的非侵入式外设寄存器操控与故障注入指南（承接 `TASK-006` / `MS-16`）。
  * [`tools/device_discovery.py`](file:///home/sushaohua/workspace/ai_soc_project/test_harness/hil/tools/device_discovery.py)：基于硅片硬件指纹（Flash 大小、MSP 栈顶、UID）的探针自动对账与寻址工具，解决探针与 COM 口插乱问题。
  * [`tools/probe_fault_injector.py`](file:///home/sushaohua/workspace/ai_soc_project/test_harness/hil/tools/probe_fault_injector.py)：物理串口在线使能/去使能（UEN/TEN/REN）与瞬态抖动故障注入 CLI 工具。
  * [`tests/test_probe_tools.py`](file:///home/sushaohua/workspace/ai_soc_project/test_harness/hil/tests/test_probe_tools.py)：**HIL 探针工具单元与隔离防御测试套件 (CR-02T)**，基于 AST 与 Mock 离线核验 F23～F26 防御逻辑及函数/参数规模硬性门禁。

## 核心测试能力与执行命令

### 1. 级联查询独立黄金向量自校验 (CR-02Q)
在任何实现代码修改前，验证黄金向量本身的 CRC-16 与物理帧结构绝对准确：
```bash
python3 test_harness/static_checks/cascade/run_query_cases.py --check-vectors
```

### 2. AP 宿主程序黑盒 PTY 回归测试 (CR-02Q / CR-04)
通过虚拟终端（PTY）注入黄金帧与 10 组异常/噪声流量，严格断言退出码、单调时钟有界超时与事务匹配：
```bash
python3 test_harness/static_checks/cascade/run_query_cases.py --test-host <path_to_minimc_host>
```

### 3. 设备与探针自发现 (Auto-Discovery)
避免在测试脚本中硬编码 `--probe` 序号或串口号：
```bash
python3 test_harness/hil/tools/device_discovery.py
```

### 4. 硬件非侵入式故障注入 (Fault Injection)
支持零固件侵入、秒级开合 MC 与 TH 物理通信总线：
```bash
# 查看所有串口状态
python3 test_harness/hil/tools/probe_fault_injector.py list

# 切断 TH 串口
python3 test_harness/hil/tools/probe_fault_injector.py disable --target TH --uart USART1

# 恢复 TH 串口
python3 test_harness/hil/tools/probe_fault_injector.py enable --target TH --uart USART1

# 一键复位所有板卡外设
python3 test_harness/hil/tools/probe_fault_injector.py reset-all
```

### 5. HIL 探针工具单元与隔离防御测试 (CR-02T)
完全隔离硬件 I/O，使用 Mock 与 AST 验证工具在冲突指纹、重复探针、错误地址、快照失败、异常清理等负例下的安全行为：
```bash
python3 -m unittest test_harness/hil/tests/test_probe_tools.py
```
