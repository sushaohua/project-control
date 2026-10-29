---
id: PLAN-COMM-MODULE-OWNERSHIP-20261029
revision: 1
date: 2026-10-29
status: user-requirement-recorded-implementation-pending
owner: ARCH
authorization: 用户明确要求D-Bus和Fast DDS作为独立模块，包括代码，维护在当前项目并由通信工程师负责
---

# D-Bus与Fast DDS项目内模块和代码维护

用户要求已确认：D-Bus和Fast DDS分别是项目内独立维护、可构建、可验证的通信模块，不能仅在开发机安装库、写一份选型建议或散落在业务服务内。沿用当前`soc-ap` Git仓，不新增未约定的项目仓，也不复制已有第三方源码形成第二套。

## 1. 岗位、模块与任务

| 模块 | 长期代码Owner | 实现卡 / 主工作包 | 对业务模块的交付 |
| --- | --- | --- | --- |
| Fast DDS通信模块 | ENG-DDS（DDS通信工程师） | TWIN-05 / TASK-014 | 统一发布订阅SDK、发现/QoS/资源与生命周期封装、IDL生成接入、配置、构建入口和跨进程测试 |
| D-Bus通信模块 | ENG-DBUS（D-Bus通信工程师） | TWIN-06 / TASK-015 | 客户端/服务端SDK、名称/方法/属性/信号、错误/期限/重连/权限封装、XML生成接入、配置、构建入口和跨进程测试 |
| 公共通信语义与schema | ARCH，通信与业务Owner共同接受 | TWIN-02 / TASK-013 | 唯一权威IDL/XML/API及错误、单位、时间、版本兼容契约 |
| 共享构建、依赖总索引和部署 | INTEGRATOR | TWIN-04，组合时由TWIN-11组织 | 共用构建入口、双profile、统一打包与版本组合 |

工程师岗位是所有权，不代表已启动Agent。现有COORD按依赖和[总控清单](coord_autorun_tasklist_20261029.md)实际拉起ENG-DDS、ENG-DBUS，保留一张卡内的源码/构建/测试自闭环；不按函数拆卡。业务Owner调用通信SDK并实现业务handler，不各自维护一套DDS/D-Bus连接、队列或重连机制。

## 2. 项目内源码布局与当前事实

```text
soc-ap/
  middleware/
    dds/                 ENG-DDS：公共头、实现、模块CMake、示例、生成接入说明
    dbus/                ENG-DBUS：公共头、实现、模块CMake、示例、生成接入说明
  contracts/twin/        ARCH：权威IDL/XML/schema；不是通信工程师的私有副本
  config/dds/twin/       ENG-DDS：VMware/SoC配置及QoS
  config/dbus/twin/      ENG-DBUS：VMware/SoC总线与权限配置源
  tests/dds/twin/        ENG-DDS：模块正反例与真实跨进程自检
  tests/dbus/twin/       ENG-DBUS：模块正反例与真实跨进程自检
  third_party/
    archives/            Git已管理的上游源码压缩包及既有总校验索引
    dds/                 ENG-DDS：来源/准确版本/校验/许可证/补丁/模块构建配方
    dbus/                ENG-DBUS：来源/准确版本/校验/许可证/补丁/模块构建配方
    src/                 解压工作树，已有忽略规则；不作为唯一源码存档
    build/, install/     可重建输出，已有忽略规则；不能作为QA源码基线
    build.sh, README.md  共享入口与总说明，由INTEGRATOR串行修改
```

本轮盘点：Git已经管理`third_party/archives/`中的D-Bus、Fast DDS、Fast CDR及若干依赖压缩包，并有共用`build.sh`；`middleware/dds/`、`middleware/dbus/`此前不存在。本次只建立模块维护入口和任务契约，不声称SDK源码、真实总线互操作或交叉编译已经完成。已有包/本机库存在不是模块验收。

第三方原始代码继续以受版本控制的准确源码包维护；不要求把整个解压树重复提交。修改不能只留在被忽略的`src/`，须由对应Owner保存可重放补丁、顺序和输入/输出校验。若未来改为维护完整源码树，由ARCH/Owner/INTEGRATOR明确迁移关系，避免源码包与源码树同时成为不一致原件。

## 3. 代码与依赖维护规则

1. 两模块都须交付真实SDK源码、公开接口、独立模块构建入口、版本/ABI说明、最小使用示例、配置和测试；目标包名由TWIN-02/04接受。业务只依赖项目公开SDK，第三方类型/实现细节的暴露边界由ARCH明确，不能随意把上游API散布到每个业务服务。
2. 每个依赖记录来源URL、完整commit或准确发行版、实际源码SHA256、许可证/NOTICE、工具链/平台限制、必需传递依赖、构建选项、补丁及升级回退影响。现有归档版本属于观察输入，兼容性和目标支持须复核，不因README写了版本就自动冻结。
3. 第三方源码包、补丁、配方和校验索引必须在服务器候选中可恢复；只写下载URL或依赖作者本机安装不满足交付。生成器及其构建依赖同样锁定；生成绑定由接受的schema生成，不能手改生成文件或另抄一份权威IDL/XML。
4. DDS相关上游文件由ENG-DDS维护，D-Bus相关上游文件由ENG-DBUS维护。`third_party/build.sh`、既有全局`archives/checksums.sha256`、总README与公共构建源只有INTEGRATOR写；工程师先交各自`third_party/dds/`或`dbus/`中的模块来源/校验/构建修改请求。共享文件变更单点串行落地并按新候选复验，不能两卡并发抢写。
5. VMware和SoC复用同一SDK源、接口和schema；工具链/sysroot、传输发现/网卡、设备/权限与部署差异集中在profile。不同任务/架构使用隔离的解压、build和install目录，不共用可写安装前缀。构建不静默下载未锁定新代码，也不以本机残留`src/`代替校验后重建。
6. 原有第三方代码保留上游许可证和最小修改；自研SDK遵守函数≤50行、参数≤4个及项目内存/指针规范。上游库存在动态内存行为不能被宣传成全系统零堆；实际资源上限须按目标组合测量。

## 4. 独立模块与运行进程分别设计

“独立模块”首先落实代码目录、维护Owner、公开API、构建目标、配置和测试。是否额外增加守护进程由ARCH在服务拓扑中明确；不因一个SDK目录就擅加`dds-agent`或`dbus-agent`中转层。D-Bus总线服务与项目SDK分别登记，Fast DDS参与者归属按业务进程图落实；平台总线的安装/启动变更由INTEGRATOR按接受的配置处理。

这不放松阶段一真实跨进程验收：FWD、STATE、网关必须经实际D-Bus/DDS通信，进程内回调和空壳SDK不能代替。UI、NET、STATE/JOB的业务准入及UART独占职责保持原归属。

## 5. 每个模块的完成条件

| 检查项 | 必交证据 |
| --- | --- |
| 项目内代码 | SDK头/实现、模块构建、真实示例及测试；上游源码包、许可证、版本校验与补丁均可从服务器候选恢复 |
| 独立构建 | 从锁定服务器提交和源码包，在独立沙箱重建SDK/依赖；记录完整命令、工具、配置和实际产物哈希，不复制作者install缓存 |
| 生成与兼容 | IDL/XML/生成器/绑定一一对应；业务头依赖、错误映射、ABI和升级/回退策略可检查 |
| DDS实际通信 | 真实跨进程发布订阅、晚加入、服务重启、QoS不匹配、慢消费者、有界队列/内存与错误可观察 |
| D-Bus实际通信 | 真实方法/错误/属性/信号、名称丢失、权限拒绝、总线/对端重启、超时和重复调用；非幂等请求不自动重放 |
| 构建失败防御 | 校验不符、缺源码/依赖、ABI错、缺制品/库或运行失败必须非零；不能仅最后一条命令成功或文件存在就签整组通过 |
| 独立收件 | 独立Codex实际运行在独立沙箱，以服务器固定提交为准；QA报告经另一非作者复核，COORD按同一准确候选收件后再释放业务接入 |

详细调度和证据按[服务器沙箱QA门禁](../../.agents/rules/delivery_and_coord_gate.md)。宿主模块通过不能外推SoC性能，也不能代替真实MC/TH HIL。

## 6. 本次落实与接续

本要求已落入TWIN-02/04/05/06、TASK-014/015、岗位规则和COORD清单。状态保持原值；不冒充已经实现或启动通信Agent。本助手未下载/替换新版本、运行第三方构建脚本、改系统总线或打断其他会话，实际实现由现有COORD按卡安排对应通信工程师。
