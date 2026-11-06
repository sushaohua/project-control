# 人工收件单：MC 级联中继超时时间戳无符号下溢与测试分块 512B 优化

## 公共约束

- 提交人及日期：sushaohua，2026-11-06；COORD 在 TWIN-67 物理 HIL 实测与串口日志对账过程中捕获整理。
- 涉及仓库：`mcu-p3`（固件实现）、`test_harness`（测试套件与部署工具）、`project-control`（部署说明书）。
- 约束要求：遵循 COORD 代码只读硬铁律，COORD 主会话不直接修改业务源码。本收件单待排程派单给 `ENG-MC` 与 `INTEGRATOR` 处理。

## 指令 1：mcu-p3 级联中继超时时间戳无符号下溢导致正常 ACK 被丢弃

【问题描述】
在 `mcu-p3/motion-controller-mcu/project/src/minimc_proto.c` 的 `check_th_relay_timeout(uint32_t now_ms)` 函数中：
```c
const uint32_t elapsed = (uint32_t)(now_ms - s_relay_start_ms);
if (elapsed < s_relay_timeout_ms) { return; }
s_relay_pending = false;
```
由于 `now_ms` 是在 `minimc_proto_poll()` 主循环入口统一采样，而中继发包时 `s_relay_start_ms = wk_timebase_get()` 在随后的 `drain_ap_rx()` 中更新。若主循环处理期间系统毫秒计数刚好增加 1ms，导致 `now_ms < s_relay_start_ms`，32 位无符号减法发生下溢变成 `4,294,967,295`。
这导致 MC 在发包后的同一个主循环内瞬间误判超时，将 `s_relay_pending` 置为 `false`。当 TH 在数十毫秒内正常返回 ACK 时，MC 因 `!s_relay_pending` 判定其为非法帧（`BAD_FRAME 0x07`）并丢弃，迫使 AP 等待 1.2s 超时重传。

【处置要求】
1. 派单给 `ENG-MC`，对 `check_th_relay_timeout` 的时钟差计算加入防下溢保护（例如在调用或函数内直接采样最新 `wk_timebase_get()`，或增加正向时间卫语句）。
2. 在 `mcu-p3` 中补充相关时间戳翻转与采样倒流的单测/模拟测试。
3. 经独立 Docker 构建与独立 Codex QA 审阅通过后合入。

## 指令 2：test_harness 自动化部署工具分块恢复 512B 默认值与说明书勘误

【问题描述】
TH Bootloader 原型能力集 `capability_flags = 0xE0080423`（`Bits 16..23 = 0x08` 代表 512B 最大分块，宏定义 `CHUNK_MAX_SIZE = 512U`）。但在实测部署脚本中被写死为 `blk_size = 64`，造成 76,896 字节固件被切分为 1,202 包，交互频繁。

【处置要求】
1. 派单给 `INTEGRATOR`，更新 `test_harness/hil/tools/hil_deploy_via_minimc_ota.py`，将分块大小默认值调整为契约标准的 512 字节（约 150 包）。
2. 在 `project-control/docs/guides/minimc_v2_mcu_upgrade_and_hil_deployment_manual_20261105.md` 中勘误相关位图注释描述。
