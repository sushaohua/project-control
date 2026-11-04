# TWIN-50 (`author_02`) 交付回执：去旁路全栈 PTY 负向注入对账修复与真机双板四路串口 HIL-01~HIL-06 终验

- **任务 ID**：`TWIN-50`
- **执行角色与会话**：`INTEGRATOR` (`7812a1f6-5006-4971-a954-802f855cf20a`)
- **运行轮次 (`run_id`)**：`author_02`
- **候选提交 (`candidate_commit`)**：`test_harness@d14ed04321c6d4f5ddb35a8801604a8af53b5b60`
- **跨仓基线**：
  - `mcu-p3`: `016e1236af75f6f19282d6b000f4b1b68bd96cc3`
  - `soc-ap`: `333178c66280e785ae1a5c089a6e2a05075cc926`
  - `test_harness`: `30c21f74e74179994eb475c38cc4afc2c1427a26` ➔ `d14ed04321c6d4f5ddb35a8801604a8af53b5b60`

---

## 1. 必读规则与输入源登记 (`read_sources`)
- `project-control/.agents/rules/repository_rule_sources.json`
- `project-control/.agents/rules/repository_rule_boundaries.md`
- `test_harness/AGENTS.md` + `test_harness/.agents/rules/shared/SOURCE.json` (`source_commit: 61de4ef9dc9dc0feb0ab114e6c7fb6e588887b4a`)
- `project-control/.agents/rules/c_cpp_coding_standard.md`
- `project-control/.agents/rules/code_documentation_standard.md`
- `project-control/docs/planning/end_to_end_physical_link_remediation_plan_20261104.md` (`revision: 3`, SHA-256 `21dd6cc16b9eb7d643662b6fba681e6360f4dcd98cdece55439c6f759c5b22cc`)

---

## 2. `author_02` 差量修正说明
1. **`test_harness/hil/tools/debug_reconciliation_probe.py` (`live_pty_ctl`)**：
   - 在 `inject-mismatch` 分支中：由于 `POST /api/v1/motion/jog` 已完全打通至真实 C 固件并在 `pty_responder_loop` 中实时排空 `mc_live.log`，先缓存点动前的 `mc_live.log` (`x_mm_x100=1250`)，随后调用 `POST /api/v1/motion/jog {"axis":"X","step_mm":5.0}` 使 `ui-gateway` 变为 `17.5mm` 并调用 `sync_online` 排空环形缓冲后恢复保存的 `mc_live.log`/`mc_debug.log`，使 `ui-gateway` (`17.5mm`) 与 `mc_live.log` (`12.5mm`) 形成真实坐标失配，从而确保 `! debug_reconciliation_probe.py --ap-url ...` 精确拦截并以非 0 退出码返回（输出 `[RECONCILE FAIL] 2. Homing & Motion Control: Motion coordinates or homed_mask mismatch`）。
   - 在 `restore-mismatch` 分支中：调用 `POST /api/v1/motion/jog {"axis":"X","step_mm":-5.0}` 与 `send_pty_ctl_cmd(work_path, "sync_online")`，使 `ui-gateway` 与 `mc_live.log` 同步恢复至 `12.5mm` (`x_mm_x100=1250`)。
2. **代码规范门禁核验**：
   - `live_pty_ctl` 函数仅 28 行（$\le 50$ 行）、3 个参数（$\le 4$ 参）、嵌套深度 $\le 2$ 层，全部中文 docstring 与注释。

---

## 3. 软件验证命令执行结果 (`verification.commands`)
1. `verify_opcode_alignment_and_probe_selftest`：`exit_code: 0`
   - 零旁路残留检查（`normalize_ap_temp_wire_frame` / `mc_bridge_notify_*` / `th_bridge_notify_*`）0 命中；
   - `check_opcode_alignment.py` 全量 17 个 MiniMCProto V2 命令码跨仓 100% 对齐；
   - `debug_reconciliation_probe.py --self-test` 11 个夹具自检通过。
2. `verify_vertical_slice_e2e_pty_no_bypass`：`exit_code: 0`
   - 921600 POSIX PTY 硬件模式下在线五类对账（`online-5-category`）PASS；
   - 运行态负向注入（`inject-mismatch`、`inject-crc-err`、`inject-drop`）均被 `! debug_reconciliation_probe.py` 非 0 退出拦截，`restore-mismatch` 恢复一致；
   - 离线哨兵（`2147483646` m°C / `32767` ddC + HTTP `503` 控制锁定）与重连恢复（`drive-recovery`）全部 PASS。

---

## 4. 真机双板 SWD 烧录与四路物理串口 `HIL-01` ~ `HIL-06` 终验结论
- 完整报告路径：[twin50_real_hil_acceptance_report_20261104.md](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/evidence/hil/twin50_real_hil_acceptance_report_20261104.md)
- **双板 SWD 烧录**：
  - `TH` (`AT32F423CCT7`, probe `0483:3748:`): `fw_th.bin` (`77,244 B`, SHA-256 `4df53b56797f9d6978e4bdaeb950d3f9faaf2c344c28907036cad31be567908e`) @ `0x08004000` + `anchor.bin` (`140 B`) @ `0x0803F800` 烧录并校验通过。
  - `MC` (`AT32F435VGT7`, probe `0483:3748:75003800120000334C41534E`): `fw_mc.bin` (`383,284 B`, SHA-256 `e065a263c7c43e83ccb4e03cbe5816b562e373655260fe3ef8a9ea8266b9c895`) @ `0x08020000` 烧录并校验通过。
- **四路物理串口与 `HIL-01` ~ `HIL-06` 全部 PASS**：
  - VMware SoC Twin (`192.168.77.134:18088`) 自动探测绑定 `/dev/ttyUSB1 @ 921600`，`MC USART6 <-> TH USART1 @ 921600`，`COM12 ([MC-DBG]) @ 115200`，`COM13 ([TH-DBG]) @ 115200`；
  - `HIL-01`（温度设定与双端采样/SSE）、`HIL-02`（归零、点动、急停与解除）、`HIL-03`（5x5 调平触发与二维网格读取）、`HIL-04`（4 槽耗材选槽/退丝/进丝同步）、`HIL-05`（作业生命周期与 `M104 S205` G-Code 级联透传）、`HIL-06`（SWD 切断 `MC USART2` 后 `1.504s` $\le 3\text{s}$ 降级为 `OFFLINE` + `2147483646` 哨兵 + HTTP `503` 控制锁定 + 守护进程 CPU `0.0%~0.1%` $\le 2\%$ + `reset-all` 后自动恢复 `NORMAL`）全部实测通过！
