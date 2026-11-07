---
id: TWIN-68-AUTHOR-01-RESULT
task_id: TWIN-68
task_revision: 1
run_id: author_01
role: ENG-MC
session_id: "1e94997f-e120-4f43-b840-bceec750dc20"
status: Completed
date: "2026-11-07T09:29:00+08:00"
target_repository: mcu-p3
branch: feat/soc-debug
base_commit: 3f1cfa66c6d27422cf038936b29aca7e45edb511
candidate_commit: 97c1c2422e98357e72cc822d2b5293b9e0c2abc6
read_sources:
  - path: project-control/.agents/rules/repository_rule_sources.json
    commit: 33de1d299452a09d90f7e1f568d740903429cb83
    sha256: cb56bda30747360eb6057758f181bc9b031662178d1d9fe9eac6d462c89c9e74
    environment: Linux host / Docker QA sandbox
    missing_items: none
  - path: project-control/.agents/rules/repository_rule_boundaries.md
    commit: 33de1d299452a09d90f7e1f568d740903429cb83
    sha256: 023c5e092e1e056e049406cb089d17eee7efc3f069feee649ec6fb8f9b8fcdca
    environment: Linux host / Docker QA sandbox
    missing_items: none
  - path: mcu-p3/.repo-rules/AGENTS.md
    commit: 3f1cfa66c6d27422cf038936b29aca7e45edb511
    sha256: 69b1ca579d6c6cfec2e26d5ffe53097c25c0e2c695dc5c614d781dd66c3a8375
    environment: mcu-p3 bundle rules
    missing_items: none
  - path: mcu-p3/.repo-rules/SOURCE.json
    commit: 3f1cfa66c6d27422cf038936b29aca7e45edb511
    sha256: f1da6b012135a34a6b24283c029b231edcb5982a36678c714c133c6b1a3cee0d
    environment: mcu-p3 bundle rules (PC snapshot 17e0887da07ceb3b017623b791b6a6999e837c79)
    missing_items: none
  - path: project-control/.agents/rules/c_cpp_coding_standard.md
    commit: 33de1d299452a09d90f7e1f568d740903429cb83
    sha256: 08243cd415c99efc8be5a51117b60980b7f99c778d8496ff11a861d23999db6a
    environment: C/C++ firmware & host unit tests
    missing_items: none
  - path: project-control/.agents/rules/code_documentation_standard.md
    commit: 33de1d299452a09d90f7e1f568d740903429cb83
    sha256: 975a181cf7a3af82a47b030698a886af0bb420ea380d059f5b9eeaedc35193b9
    environment: All self-developed code & tests
    missing_items: none
  - path: project-control/docs/architecture/minimc_v2_relay_underflow_and_512b_chunk_arch_breakdown_20261107.md
    commit: 33de1d299452a09d90f7e1f568d740903429cb83
    sha256: b3c295be841195e34598f7f1eec91e6f02457ca9df0374e0147fe60be5344a76
    environment: Architecture Breakdown Rev 1 (§2 TWIN-68)
    missing_items: none
  - path: project-control/docs/specs/ap_mc_formal_protocol_v2_0_4_unified_ota_20261106.md
    commit: 33de1d299452a09d90f7e1f568d740903429cb83
    sha256: ec874cab3f8f98fec6412b2da2b4f1fa52bfd8a33601da21e908b0ffaeb0522c
    environment: MiniMCProto Rev 2.0.4 active baseline
    missing_items: none
  - path: project-control/.agents/kanban/microtasks/vmware_soc_twin/TWIN-68.md
    commit: 33de1d299452a09d90f7e1f568d740903429cb83
    sha256: 2a79b4bdb751027123b39fe790c9fa4a0ed27fbae333d7e2b256d9082afa3a55
    environment: TWIN-68 task contract (revision 1)
    missing_items: none
artifacts:
  - path: mcu-p3/motion-controller-mcu/project/src/minimc_proto.c
    sha256: eb6692767d19054480ca5c97afe1938cb7d807db88717154c8c0a29b8e24afbd
  - path: mcu-p3/motion-controller-mcu/tests/test_mc_ota_and_relay.c
    sha256: c662acb7594bfdd69da4134ef993f66cbb97a943aa43dd2cd939e7b3f2a8d0e6
---

# `TWIN-68` (`author_01`) `ENG-MC` 执行与自检回执

## 1. 规则与输入对账回执 (`read_sources`)

已显式读取并核对全部 9 项必读规则、架构方案、协议规范与任务卡契约（详见 YAML 头部 `read_sources` SHA-256 列表），适用环境为 `mcu-p3` (`feat/soc-debug`) 固件源码与宿主机/Docker 单元测试，无缺失必读项。

## 2. 变更摘要（严格限定于 `allowed_paths`）

1. **[`mcu-p3/motion-controller-mcu/project/src/minimc_proto.c`](file:///home/sushaohua/workspace/ai_soc_project/mcu-p3/motion-controller-mcu/project/src/minimc_proto.c)** (`sha256: eb6692767d19054480ca5c97afe1938cb7d807db88717154c8c0a29b8e24afbd`)：
   - **防御层一（修正 `minimc_proto_poll` 采样次序）**：在 `minimc_proto_poll(void)` 中，先执行 `drain_ap_rx()` 与 `drain_th_rx()`，再调用 `const uint32_t now_ms = wk_timebase_get();` 传入 `check_th_relay_timeout(now_ms)` 与 `mc_debug_log_periodic_state(now_ms)`；同时在 `handle_th_relay_req()` 发送成功后将 `s_th_proxy_last_ms` 同步对齐至 `s_relay_start_ms`，从源头消除同轮串口发送跨毫秒导致的 `now_ms < s_relay_start_ms` 采样倒置。
   - **防御层二（`check_th_relay_timeout` 32 位模半空间防下溢保护）**：在 `check_th_relay_timeout(uint32_t now_ms)` 中，对 `proxy_elapsed = (uint32_t)(now_ms - s_th_proxy_last_ms)` 与 `elapsed = (uint32_t)(now_ms - s_relay_start_ms)` 均施加 `< 0x80000000UL` 半空间下溢防护，确保当 `now_ms < s_relay_start_ms`（如无符号减法下溢产生 `0xFFFFFFFFU`）时视为未到期直接返回，而跨 `0xFFFFFFFFU -> 0x00000000U` 的正常正向回绕（`elapsed < 0x80000000UL` 且 `elapsed >= s_relay_timeout_ms`）仍准确触发超时。
   - 提供轻量测试辅助查询接口 `minimc_proto_is_th_relay_pending(void)` 与 `minimc_proto_test_check_th_relay_timeout(uint32_t now_ms)`。

2. **[`mcu-p3/motion-controller-mcu/tests/test_mc_ota_and_relay.c`](file:///home/sushaohua/workspace/ai_soc_project/mcu-p3/motion-controller-mcu/tests/test_mc_ota_and_relay.c)** (`sha256: c662acb7594bfdd69da4134ef993f66cbb97a943aa43dd2cd939e7b3f2a8d0e6`)：
   - 在 `forward_uart_send_raw()` 测试桩中增加可配置钩子 `s_tick_advance_on_th_tx`，模拟级联发送期间 SysTick 中断推进 `+1ms`。
   - 新增 `static void test_th_relay_timeout_underflow_and_wraparound(void)`（34 行 `<= 50` 行，0 参数 `<= 4` 参数，含完整中文注释）并在 `main()` 中调用：
     - **场景 A**：设置 `s_mock_tick_ms = 1120280U` 且 `s_tick_advance_on_th_tx = 1U`，发送 `DST=0x03` 的 `0x21 CMD_OTA_DATA` 帧（使 `s_relay_start_ms = 1120281U`），运行 `minimc_proto_poll()` 并显式调用 `check_th_relay_timeout(1120280U)` 模拟 `elapsed = 0xFFFFFFFFU` 下溢；断言 `s_relay_pending == true` 且 `s_th_proxy_active == true`（零伪超时）；随后推进 `s_mock_tick_ms = 1120283U` 并注入 `TH` `0x00 CMD_ACK`，断言 `MC` 完整透传 `18B` `0x00 CMD_ACK` 至 `AP`，无 `BAD_FRAME 0x07`。
     - **场景 B**：设置 `s_mock_tick_ms = 0xFFFFFFF0UL` 发送 `0x21 CMD_OTA_DATA`（超时阈值 `1500ms`），推进至 `0x00000010UL`（流逝 `32ms < 1500ms`）断言 `s_relay_pending == true`；推进至 `0x00000600UL`（流逝 `1552ms >= 1500ms`）断言 `s_relay_pending == false` 准确触发超时释放。

## 3. 自检与门禁验证结果

执行命令：`sh mcu-p3/motion-controller-mcu/tests/run_tests.sh`

```text
=== [1/3] Run TWIN-44/47/60 MC regression suite (test_twin44_mc_debug.c) ===
All 10 TWIN-44/TWIN-47/TWIN-60 test suites PASSED!
=== [2/3] Run TWIN-64 MC OTA, 0x1D magic (0x2005FFF0), 534B proxy & th_upgrade_mgr suite ===
[PASS] test_mc_ota_and_relay: all TWIN-64/TWIN-68 MC App OTA, 534B relay & underflow tests passed!
=== [3/3] Verify MC zero M997/5AA5 residue & S04 function/comment gates ===
[PASS] MC S04 function length (<=50), params (<=4) and Chinese comments verified!
```

## 4. Git 提交与远端推送凭证

- **仓库与分支**：`mcu-p3` @ `feat/soc-debug`
- **`base_commit`**：`3f1cfa66c6d27422cf038936b29aca7e45edb511`
- **`candidate_commit`**：`97c1c2422e98357e72cc822d2b5293b9e0c2abc6`
- **远端推送状态**：已推送至 `origin/feat/soc-debug` (`3f1cfa6..97c1c24`)
