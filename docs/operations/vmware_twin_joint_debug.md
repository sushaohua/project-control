# VMware 数字孪生微服务集群联调与操作手册 (TWIN-11)

| 文档版本 | 发布状态 | 对应发布包 | 适用阶段 |
| :--- | :--- | :--- | :--- |
| **v2.1.0-RC1** | **Approved** | `vmware-soc-twin-candidate-20261030-01` | VMware 孪生联调 & HIL 台架终验 |

---

## 1. 系统架构与服务拓扑

本系统为解决传统单体 CLI 独占串口、阻塞多模块访问及越权操作强电的痛点，采用分权解耦的微服务集群架构：

```
+-------------------------------------------------------------------+
|                        Web HMI 浏览器前端                         |
|                    (soc-ap/ui/twin/index.html)                    |
+---------------------------------+---------------------------------+
                                  | HTTP REST / SSE (Port 8080)
+---------------------------------v---------------------------------+
|                       UI Gateway 边缘网关                         |
|                 (services/ui_gateway: aisoc_ui_gateway)           |
+---------------------------------+---------------------------------+
                                  | D-Bus RPC (org.aisoc.Device)
+---------------------------------v---------------------------------+
|                   STATE 状态机权威服务                            |
|             (services/device_manager: aisoc_device_manager)       |
+---------------------------------+---------------------------------+
                                  ^ Fast DDS (Topic: telemetry/raw_temp)
                                  |
+---------------------------------+---------------------------------+
|                    FORWARD 串口常驻服务                           |
|                 (services/forward: aisoc_forward_service)         |
+---------------------------------+---------------------------------+
                                  | 唯一 UART 通路 (/dev/ttyUSB0 @ 115200)
+---------------------------------v---------------------------------+
|                        双 MCU 硬件集群                            |
|     MC (AT32F435, dst=0x02) <=== USART6 ===> TH (AT32F423, dst=0x03)  |
+-------------------------------------------------------------------+
```

---

## 2. 启动与编排操作步骤 (Startup Orchestration)

### 步骤 1：系统总线与运行环境就绪
确保 Linux 用户态 D-Bus 服务正在运行：
```bash
# 检查 dbus-daemon 状态
ps aux | grep dbus-daemon
# 若处于容器或最小化环境，可启动会话 D-Bus：
export $(dbus-launch)
```

### 步骤 2：启动 FORWARD 串口服务 (唯一独占串口)
```bash
# 物理硬件接入模式 (默认 /dev/ttyUSB0)
./soc-ap/build/bin/aisoc_forward_service --device /dev/ttyUSB0 --baud 115200 --dds-domain 0 &

# 或本地纯软件 PTY 仿真模式 (用于无物理板卡时的联调)
./soc-ap/build/bin/aisoc_forward_service --pty --dds-domain 0 &
```

### 步骤 3：启动 STATE 权威状态机服务
```bash
./soc-ap/build/bin/aisoc_device_manager --dds-domain 0 --dbus-name org.aisoc.Device &
```

### 步骤 4：启动 UI Gateway 边缘网关
```bash
./soc-ap/build/bin/aisoc_ui_gateway --port 8080 --dbus-name org.aisoc.Device &
```

### 步骤 5：打开 Web HMI 界面
在任意现代浏览器（Chrome / Firefox / Edge / 嵌入式 WebKit）中直接打开：
```bash
# 浏览器直接打开前端静态资源
google-chrome soc-ap/ui/twin/index.html &
# 或通过本地静态 Web 服务挂载：
python3 -m http.server 8000 --directory soc-ap/ui/twin &
# 访问 http://localhost:8000
```

---

## 3. 功能验证检查清单 (Verification Checklist)

### 3.1 进程树与服务存活检查
```bash
$ ps aux | grep aisoc
sushaohua  1001  aisoc_forward_service --device /dev/ttyUSB0 ...
sushaohua  1002  aisoc_device_manager --dds-domain 0 ...
sushaohua  1003  aisoc_ui_gateway --port 8080 ...
```

### 3.2 D-Bus 点对点 RPC 联调
直接通过 `dbus-send` 验证状态机接口：
```bash
# 获取权威全量温度快照 JSON
dbus-send --print-reply --dest=org.aisoc.Device /org/aisoc/Device org.aisoc.Device.GetSnapshot

# 预期输出格式：
# string "{"state_generation":12,"nodes":{"toolhead":{"current_temp_deci_c":2100,...}}}"
```

### 3.3 HTTP REST 快照与准入采样验证
```bash
# 1. 测试 REST 获取快照
curl -s http://127.0.0.1:8080/api/v1/temperature/snapshot | jq .

# 2. 测试 POST 触发准入采样
curl -s -X POST http://127.0.0.1:8080/api/v1/temperature/sample \
  -H "Content-Type: application/json" \
  -d '{"client":"OPERATOR_SHELL","reason":"manual_check"}' | jq .
# 预期返回: {"accepted": true, "reason": "Sample accepted and dispatched"}
```

### 3.4 SSE 实时长连接流式推送验证
```bash
curl -N http://127.0.0.1:8080/api/v1/temperature/stream
# 预期持续输出:
# event: temp_update
# data: {"state_generation":13,...}
```

---

## 4. 异常注入与自愈恢复 SOP (Failure Recovery SOP)

| 异常场景 | 表现与现象 | 恢复机制与判定准则 |
| :--- | :--- | :--- |
| **UI 网关进程崩溃** | 浏览器顶部弹出红色警报条，显示重连中 | 前端自动触发指数退避重连；重启 `aisoc_ui_gateway` 后 1 秒内自动无缝恢复 |
| **串口线意外断开** | 数据超过 3 秒未更新，品质降级为 `STALE`，超 10 秒变为 `FAULT` | 遥测数据显示黄色/红色告警，禁止执行加热操作；重新插上串口后系统世代自增并自动恢复 `FRESH` |
| **传感器断路 (开路)** | ADC 读数跃升至 4095，状态码返回 `0x01` | 前端温度值显式渲染为红色 **`FAULT`**，强电安全锁持续生效，杜绝干烧 |
| **高频连续请求采样** | 操作员在 HMI 狂击或外部脚本刷接口 | 状态机 50ms 防抖自动生效，返回 `accepted: false, reason: "Debounced"`，保护 UART 总线不拥塞 |
