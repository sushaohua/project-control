# 两阶段孪生能力任务

16张TWIN卡均为Backlog规划，第一张为[TWIN-01](TWIN-01.md)，不是已派单/实现。完整依赖、负责人、验收和历史复用见[执行总表](../../../../docs/planning/vmware_soc_twin_task_execution_20261029.md)。

| [TWIN-01](TWIN-01.md) | 整体服务架构与温度冲突逐项对账 | ARCH | TASK-005 | CR-11 | cross-stage |
| [TWIN-02](TWIN-02.md) | 双环境可执行通信契约与生成规则 | ARCH | TASK-013 | TWIN-01 | cross-stage |
| [TWIN-03](TWIN-03.md) | 独立黄金预期与两阶段故障验收用例 | QA | TASK-010 | TWIN-02 | cross-stage |
| [TWIN-04](TWIN-04.md) | VMware构建配置与同构服务生命周期 | INTEGRATOR | TASK-004 | TWIN-02 | vmware-twin |
| [TWIN-05](TWIN-05.md) | DDS跨进程SDK与有界QoS | ENG-DDS | TASK-014 | TWIN-02, TWIN-03 | vmware-twin |
| [TWIN-06](TWIN-06.md) | D-Bus跨进程SDK与权限超时 | ENG-DBUS | TASK-015 | TWIN-02, TWIN-03 | vmware-twin |
| [TWIN-07](TWIN-07.md) | FORWARD常驻服务与唯一UART通路 | ENG-FWD | TASK-007 | TWIN-02, TWIN-03, TWIN-05, TWIN-06, TEMP-04 | vmware-twin |
| [TWIN-08](TWIN-08.md) | STATE权威快照与统一请求准入 | ENG-STATE | TASK-008 | TWIN-02, TWIN-03, TWIN-05, TWIN-06 | vmware-twin |
| [TWIN-09](TWIN-09.md) | UI网关真实HTTP与SSE通信 | ENG-NET | TASK-009 | TWIN-02, TWIN-03, TWIN-05, TWIN-06 | vmware-twin |
| [TWIN-10](TWIN-10.md) | 浏览器交互屏幕接入真实业务接口 | ENG-UI | TASK-009 | TWIN-02, TWIN-03, TWIN-09 | vmware-twin |
| [TWIN-11](TWIN-11.md) | VMware整链联调与候选交接 | INTEGRATOR | TASK-012 | TWIN-04, TWIN-07, TWIN-08, TWIN-09, TWIN-10, TWIN-15, TWIN-16 | vmware-twin |
| [TWIN-12](TWIN-12.md) | VMware应用孪生与真实MCU独立验收 | QA | TASK-010 | TWIN-03, TWIN-11 | vmware-twin |
| [TWIN-13](TWIN-13.md) | SoC平台迁移与实板候选交接 | BSP | TASK-003 | TWIN-04, TWIN-12 | soc-migration |
| [TWIN-14](TWIN-14.md) | SoC实屏实板独立验收与阶段二收件 | QA | TASK-010 | TWIN-03, TWIN-12, TWIN-13 | soc-migration |
| [TWIN-15](TWIN-15.md) | MC温度契约复核与必要修订 | ENG-MC | TASK-002 | TWIN-02, TWIN-03, TEMP-03 | vmware-twin |
| [TWIN-16](TWIN-16.md) | TH温度契约复核与必要修订 | ENG-TH | TASK-002 | TWIN-02, TWIN-03, TEMP-02 | vmware-twin |
