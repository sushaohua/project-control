---
schema_version: 1
confirmation_id: CONFIRM-DEBUG-BAUD-20261104
revision: 2
status: approved-by-human
date: 2026-11-04
approved_at: 2026-11-04T10:01:02+08:00
coord_session: ff2fb105-fd84-4ecb-b1e6-8f8eb00badc6
qa_policy: streamlined-v1
demands:
  - demand_id: DEM-20261104-001
    category_id: FEAT-20261104-001
    title: MC/TH Debug：双路调试串口与用户 UI 的双向链路对账
    source_confirmation: project-control/docs/planning/mc_th_debug_mode_requirement_confirmation_20261103.md
  - demand_id: DEM-20261104-002
    category_id: FEAT-20261104-002
    title: VMware/AP↔MC 业务 UART 统一至 921600（含 AP 一键全栈编译与配置文件启动脚本）
    source_confirmation: project-control/docs/planning/vmware_mc_921600_requirement_confirmation_20261103.md
---

# MC/TH Debug 模式与 VMware/AP↔MC 921600 合并实施概要确认单（rev 2）

## 1. 查重与收件结论

经核对 `project-control/docs/work_intake/`、`project-control/.agents/board/tasks.yaml` 及 `project-control/.agents/kanban/microtasks/` 全量 134 张主任务卡与 92 张微任务卡：
- **无重复在途卡**：现有 `TWIN-07`/`TWIN-29`/`TWIN-36` 覆盖 115200 基准下的 `forward-service` 串口传输与 `POLLHUP` 容错，`TWIN-15`/`TWIN-16`/`TWIN-21`/`TWIN-24` 覆盖 MC/TH 业务协议处理，`TWIN-41`/`TWIN-42`（已 `Done`）覆盖前期单功能闭环梳理与级联验证；尚未建卡覆盖“MC/TH 双路调试串口与 Web UI 双向对账模式”及“AP↔MC 业务串口切换至 921600”。
- **正式收件登记**：已归档至 `SUB-20261104-001`（rev 1），生成唯一主分类记录 `FEAT-20261104-001`（`DEM-20261104-001`，MC/TH Debug）与 `FEAT-20261104-002`（`DEM-20261104-002`，AP↔MC 921600）。
- **QA 策略**：全部新建任务卡显式采用已生效的 `qa_policy: streamlined-v1`（作者实现与自检 → 锁定候选 → 一轮独立 Codex QA［代码审查 + 功能/必要回归测试］→ COORD 收件）；因涉及跨仓串口参数与硬件台架链路，保留 ARCH 契约审查与真实 HIL 合并验收门禁。

---

## 2. 实施范围与技术边界

### 2.1 需求一：VMware/AP↔MC 业务 UART 统一至 921600（`DEM-20261104-002` / `FEAT-20261104-002`）
- **AP 侧（`soc-ap` 仓，`main` 分支）**：
  - `core/forward/transport/serial_posix.cpp`：在 `baud_to_speed()` 中扩展 `460800`（`B460800`）与 `921600`（`B921600`）映射，保持 `8N1`、无流控、原始模式（raw mode）。
  - `services/forward/forward_types.h`、`services/forward/forward_main.cpp`、`core/host/main.cpp`：将业务串口默认波特率常量 `AISOC_FWD_DEFAULT_BAUD` 更新为 `921600`，保留 `--baud` CLI 显式覆盖能力供排障与回退验证。
  - 运行时配置与一键编译启动：同步更新 `config/runtime/vmware/services_manifest.json`、`config/runtime/common/services_manifest.json`、`dist/vmware_twin/config/services_manifest.json` 及联合调试文档中的 `/dev/ttyUSB0` 业务波特率至 `921600`；新增默认配置文件 `soc-ap/config/runtime/vmware/aisoc_twin.conf` 并升级 `soc-ap/tools/deploy_twin.sh`，支持单条命令完成全量模块（`third_party`、`runtime`、`forward`、`device_manager`、`ui_gateway`、`host`）增量编译、按配置文件默认启动全套服务（`D-Bus` + `forward_service_daemon` + `device_manager_daemon` + `ui-gateway`）、状态查询（`--status`）、仅构建（`--build-only`）与一键停止（`--stop`）。
- **MC 侧（`mcu-p3` 仓，`feat/soc-debug` 分支）**：
  - `motion-controller-mcu/project/src/wk_usart.c`：将连接 AP 的业务串口 `USART2`（PA2 TX / PA3 RX，DMA RX/TX + IDLE 中断）初始化波特率由硬编码 `115200` 更新为具名宏 `921600U`（与板间级联 `USART6` 的 `921600` 保持一致）。
- **不变边界**：
  - MC↔TH 板间级联串口（MC `USART6` PA4/PA5 ↔ TH `USART1` PB6/PB7）已为 `921600`，无需改动。
  - MC 调试串口（`USART1` PA9/PA10，COM8）与 TH 调试串口（`USART3` PC4/PC5，COM6）维持 `115200 8N1` 不变。
  - **严禁触碰 Bootloader**：`boot/bootloadermc` 与 `boot/bootloaderth` 不作任何修改；MCU OTA 升级（`TWIN-26`～`TWIN-28`）继续保持人工冻结。

### 2.2 需求二：MC/TH Debug 双路调试串口与用户 UI 双向链路对账（`DEM-20261104-001` / `FEAT-20261104-001`）
- **MC 侧（`mcu-p3/motion-controller-mcu`，`feat/soc-debug` 分支）**：
  - **非阻塞环形缓冲**：在 `wk_usart.c` 将 `USART1`（PA9/PA10，115200）调试输出改造为静态环形缓冲区（零动态堆分配），主循环非阻塞排空；缓冲区满时严格丢弃或截断并递增 `drop_count` / `trunc_count`，严禁在中断或运动控制路径阻塞等待。
  - **结构化观测点（`minimc_proto.c` / `wk_usart.c`）**：在 Debug 开启时输出单行结构化日志（含 `boot_id`、`tick_ms`、`dir=RX|TX|RELAY`、`evt=RECV_RAW|CRC_OK|CRC_ERR|CMD_EXEC|ACK_ENQ|TX_DONE|DROP`、`src/dst/cmd/seq/len`、摘要 `hex`、`status`、`drop_count`），完整覆盖：
    1. AP→MC 业务帧接收、CRC/帧格式校验、指令执行与 ACK 发送；
    2. MC 状态/温度生成与上报；
    3. MC↔TH（`USART6`）双向透传转发与丢包/超时计数。
- **TH 侧（`mcu-p3/color-engine-mcu/io_toggle`，`feat/soc-debug` 分支）**：
  - **复用既有 DMA 环形缓冲**：复用 `src/bsp/usart.c` 已有的 `USART3`（PC4/PC5，115200）DMA 非阻塞环形缓冲 `USART3_write()` 与 `usart3_tx_drop_count`。
  - **结构化观测点（`src/app/minimc_proto.c` 及采样上报路径）**：输出与 MC 格式对齐的结构化调试行，明确区分：收到 MC 转发帧、CRC/解析结果、指令执行、温度/状态原始值与有效值生成（`raw_adc`/`deci_c`/`valid`）、写入发送缓冲、DMA 发送完成及 `drop_count`。
- **开关控制与 UI 边界**：
  - 支持编译期默认配置与运行期轻量级开关（默认关闭高频 HEX 转储，开启后输出全链路对账日志），不改变现有业务串口协议帧结构。
  - **不新增独立 Debug UI 页面**：直接使用现有用户 Web UI（`soc-ap/ui/twin/index.html`）开展“UI 操作 → AP → MC → TH”与“TH/MC 上报 → AP → UI 显示”双向闭环核对。

---

## 3. 角色分工与依赖顺序

| 阶段 | 任务代号（拟建） | 负责角色 | 所属仓库与分支 | 核心交付物与职责 | 依赖关系 |
| --- | --- | --- | --- | --- | --- |
| Phase 0 | 架构定界与拆卡 | `ARCH` | `project-control` (`main`) | 梳理三端代码依赖与前置任务链（`depends_on`），冻结跨端 Debug 日志字段契约与 921600 接口边界，生成 `TWIN-43`～`TWIN-46` 精确文件白名单并通过 `check_task_graph.py` 静态校验 | 人工批准后首先执行 |
| Phase 1 | `TWIN-43` | `ENG-FWD` | `soc-ap` (`main`) | `serial_posix` 921600 支持、业务串口默认波特率与 VMware/通用运行时配置切换至 921600、单元与回退自检 | `ARCH` 定界后即刻派发 |
| Phase 1 | `TWIN-44` | `ENG-MC` | `mcu-p3` (`feat/soc-debug`) | MC `USART2` 切换至 921600；`USART1` 非阻塞静态环形缓冲与 `drop_count`；MC 业务收发与 `USART6` 转发 Debug 观测日志 | `ARCH` 定界后与 `TWIN-43`、`TWIN-45` 并行 |
| Phase 1 | `TWIN-45` | `ENG-TH` | `mcu-p3` (`feat/soc-debug`) | TH `USART3` 结构化 Debug 观测日志（接收、校验、执行、温度/状态生成、DMA 入队与发送完成、`drop_count`） | `ARCH` 定界后与 `TWIN-43`、`TWIN-44` 并行 |
| Phase 2 | `TWIN-46` | `INTEGRATOR` | `soc-ap` (`main`) / `test_harness` (`main`) | 升级 `soc-ap/tools/deploy_twin.sh` 与 `soc-ap/config/runtime/vmware/aisoc_twin.conf` 实现单脚本全量编译与按配置默认启动；自动构建打包 AP + MC/TH 固件制品、生成 SHA256 清单与烧录执行计划；配合人工确认与烧录后执行双路串口 + Web UI 对账采集与稳定性回归 | 依赖 `TWIN-43`、`TWIN-44`、`TWIN-45` |
| Phase 3 | 独立 QA 审阅 | 独立 Codex `QA` (+ `ARCH`) | 只读快照 + 独立 Docker 沙箱 | 按 `qa_policy: streamlined-v1` 在两项功能均交付并完成台架烧录后，执行首次完整独立验收 | 依赖 `TWIN-46` |

---

## 4. 兼容性、故障诊断与回退方案

1. **波特率失配显式可观测**：若 AP 与 MC 波特率不一致（如一方 921600、一方 115200），AP `forward-service` 在探针握手中连续超时/帧同步失败，结构化日志显式输出 `target_node`、`sequence_id`、`elapsed_ms`、`error_code`，并在 3s 内将状态机推进至断连衰退，温度打入哨兵值，Web UI 锁定控制并返回 HTTP 503/504，绝不静默伪造正常状态。
2. **Debug 负载安全隔离**：MC `USART1` 与 TH `USART3` 均通过固定上限静态环形缓冲异步输出，与 921600 业务串口 DMA/中断通道物理隔离；当 115200 调试口带宽饱和时直接丢弃新增调试行并累加 `drop_count`，确保主业务帧 0 阻塞、运动控制 0 抖动。
3. **一键回退机制**：
   - AP 侧支持通过 `services_manifest.json` 的 `baud_rate` 或 `--baud 115200` 参数瞬时切回 `115200` 排障。
   - MC/TH 侧保留上一版已验证固件制品及 `USART2` 波特率宏定义；Debug 模式可随时关闭以恢复纯静默生产态。

---

## 5. 验收方法（沿用已确认的四项 QA 决策）

严格沿用已确认的四项 QA 决策（**Q1=C 现有 VMware 独占窗口/冻结快照；Q2=B 两项功能均交付后执行首次完整验收；Q3=A 已有 MC/TH 及完整台架；Q4=A 自动生成制品和烧录计划 → 授权人员确认并烧录 → 自动测试**）：

1. **阶段一（单仓 Docker 确定性构建与单测）**：
   - 受控 Runner 在独立 Docker 沙箱中拉取服务器锁定候选，验证 `soc-ap` 921600 串口配置/单测、`mcu-p3` MC/TH 固件编译零警告、函数规模（$\le 50$ 行）与入参个数（$\le 4$ 个）100% 合规。
2. **阶段二（制品与烧录计划生成 → 人工确认烧录）**：
   - `INTEGRATOR` 自动生成 MC/TH 固件制品、SHA256 校验值、目标串口映射及回退镜像说明，交由授权人员确认并烧录至真实 MC/TH 台架（不动 Bootloader）。
3. **阶段三（VMware 独占窗口 + 真实台架 HIL + 独立 Codex QA 合并完整验收）**：
   - **链路一（UI → AP → MC）**：在现有用户 Web UI 触发控制指令，核对 AP 发送日志、MC `USART1` Debug 接收/校验/执行/ACK 日志及 UI 状态更新一致。
   - **链路二（UI → AP → MC → TH）**：在 Web UI 触发目标为 TH 的指令，核对 AP 发送、MC `USART6` 转发、TH `USART3` 接收/执行/响应、MC 回传及 UI 结果一致。
   - **链路三（TH/MC → AP → UI）**：核对 TH `USART3` 温度/状态生成与发送完成日志、MC 转发与自身状态上报日志、AP 接收快照及 Web UI 展示数值一致。
   - **921600 稳定性与异常恢复**：持续业务交互与调温/运动并发下无新增 `crc_error`/`frame_error`、无乱序卡死；拔除 `/dev/ttyUSB0` 后 CPU $\le 2\%$、3s 内 UI 锁定并置哨兵值，重插后自动重连恢复；失配场景显式报错。
   - **独立 Codex 终审**：由真实独立 Codex 会话审阅锁定候选代码与上述客观测试/HIL 证据并出具结论，COORD 核验后收件关闭。
