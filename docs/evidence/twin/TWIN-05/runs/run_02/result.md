# TWIN-05 DDS跨进程SDK与有界QoS定向整改自检报告 (Run 02)

| 属性 | 内容 |
| :--- | :--- |
| **任务卡片** | `TWIN-05` (DDS跨进程SDK与有界QoS) |
| **所属工作包** | `TASK-014` (实现 DDS 底座和统一 SDK) |
| **执行角色** | `ENG-DDS` (DDS 通信工程师) |
| **当前轮次** | `run_02` (针对 Run 01 Codex QA 审计意见定向整改) |
| **前置依赖 1** | `TWIN-02` (accepted version: `soc-ap: 532caecf3a146802969a49e73081400c2b32b25e`) |
| **前置依赖 2** | `TWIN-03` (accepted version: `test_harness: 0b7497ba43158841eb3c4af7f16e477b9c30c2c5`) |
| **候选 Commit** | `soc-ap: 16ba69d29c93191731a13a1fa4c88f981677c4d5`, `project-control: <pinned-at-commit>` |
| **作者会话 ID** | `3fbe2d65-b1c3-4c69-8a2d-084bcc76a4c3` |
| **执行状态** | **Rework Completed (实体配额硬上限与负例自测就绪，候选统一对齐)** |

---

## 1. Run 01 阻断项定向整改说明 (Resolution of QA Findings)

针对 `TWIN-05/runs/run_01/qa_review_report.md` 中独立 Codex QA 提出的 3 项问题，执行定向整改如下：

### 1.1 TWIN05-QA-01 (候选提交基线对齐)
- **问题**：Run 01 沙箱中 `server_lock.json` 锁定的旧提交为 `371daa...`，与评审申请候选存在漂移。
- **整改**：Run 02 将候选提交统一锁定到已推送到 `origin/main` 的最新提交 `soc-ap: 16ba69d29c93191731a13a1fa4c88f981677c4d5`，并在运行 sandbox 前定格统一 4 仓远端 commit。

### 1.2 TWIN05-QA-02 (作者会话绑定)
- **问题**：任务卡中 `executor.session` 为空，缺少作者会话标识。
- **整改**：在任务卡及本报告中显式绑定作者专属会话 `3fbe2d65-b1c3-4c69-8a2d-084bcc76a4c3`，明确作者与后续独立 Reviewer 的物理分离。

### 1.3 TWIN05-QA-03 (SDK 实体创建数量硬上限)
- **问题**：Fast DDS QoS 仅约束了 Topic 内部样本队列深度，但 SDK API 未限制调用者可创建的 Participant/Pub/Sub 实体总数，存在无界分配隐患。
- **整改**：
  1. 在 `aisoc_dds.h` 中定义实体硬上限宏：
     - `AISOC_DDS_MAX_PARTICIPANTS` (4U)
     - `AISOC_DDS_MAX_PUBLISHERS` (16U)
     - `AISOC_DDS_MAX_SUBSCRIBERS` (16U)
     - 新增错误码 `AISOC_DDS_ERR_RESOURCE_LIMIT` (-9)
  2. 在 `aisoc_dds_participant.cpp`、`aisoc_dds_pub.cpp`、`aisoc_dds_sub.cpp` 中引入原子计数器 `g_participant_count`, `g_publisher_count`, `g_subscriber_count`，创建时校验若超出上限立即返回 `AISOC_DDS_ERR_RESOURCE_LIMIT`；销毁时严格回退计数器；
  3. 在 `DEFAULT_FASTRTPS_PROFILES.xml` 中配置 `<allocation>` 硬上限；
  4. 在 `test_dds_pubsub.cpp` 中增加专用测试套件 `test_quota_limits`，自动创建至 16 个 Publisher 并断言第 17 个必须返回 `AISOC_DDS_ERR_RESOURCE_LIMIT`，销毁后配额正确恢复，正反例 100% 验证通过。

---

## 2. 交付物清单与 SHA-256 校验码 (Run 02)

| 交付文件路径 | 类型与描述 | SHA-256 校验码 |
| :--- | :--- | :--- |
| `soc-ap/config/dds/twin/DEFAULT_FASTRTPS_PROFILES.xml` | Fast DDS 有界 QoS 与 allocation 硬上限 XML 配置文件 | `566a4893171c89fd976ce73dc61895215875d64c8d9d4f5b780caf6d11fe742d` |
| `soc-ap/middleware/dds/include/aisoc_dds.h` | 自研统一发布/订阅 SDK 公开 C/C++ 接口头文件 (含配额限制常量) | `3ca44e38eabb3ac69c2546d5fb517e51f733819405f97509f1b39c0f193c6ce0` |
| `soc-ap/middleware/dds/src/aisoc_dds.cpp` | SDK 顶层入口与语义版本实现 | `cc34be1ee06784ea38d5606dcae27ed38cc63382f5fdbf0be0ff071610ac3011` |
| `soc-ap/middleware/dds/src/aisoc_dds_common.cpp` | 有界 QoS 映射与实体原子计数器定义 | `5c10e45eac063d82c5a1415a7787f83e0468e5f06d9815aa494d8eba282d3030` |
| `soc-ap/middleware/dds/src/aisoc_dds_internal.hpp` | 内部句柄结构体、上下文锁与监听器私有定义 | `029c977887de32e90a1e6c2e15e20aed2df85383af5bd09a18311a8883271233` |
| `soc-ap/middleware/dds/src/aisoc_dds_participant.cpp` | DomainParticipant 生命周期与配额检查 | `01137d727324188d3c4327b82dad51c227a67e5dfaa8e4fc3bd7b8a5c33a6a99` |
| `soc-ap/middleware/dds/src/aisoc_dds_pub.cpp` | DataWriter 创建、销毁、配额保护与遥测发布 | `689a9b62752bccf724ca7508bcffd5607242e736196e02ab62393667f888cefb` |
| `soc-ap/middleware/dds/src/aisoc_dds_sub.cpp` | DataReader 创建、销毁、配额保护与非阻塞 Take | `19e72cdbd121f1ff4f9e5a90c1d9b8c5994a02c5706e55e48e0abbfa63ebd684` |
| `soc-ap/middleware/dds/src/aisoc_dds_types.cpp` | 权威 IDL 消息序列化/反序列化与 TopicDataType | `5d025812b81eb015b00366b69b8485ba9407f402cf393665590a11dbbaa00213` |
| `soc-ap/middleware/dds/src/aisoc_dds_types.hpp` | TopicDataType 子类头文件声明 | `d2d6dd8e7aafd067c0bdabced6101035002509c727b234f21358e357e5725ed3` |
| `soc-ap/middleware/dds/CMakeLists.txt` | 模块独立 CMake 配置 | `a5921ad4024328a1d0f0985670ae9fb979652049f15ac46ad777ea6f85c8cf18` |
| `soc-ap/middleware/dds/README.md` | 模块使用说明与构建接入指南 | `0840c17dcf17c0184898c605d0c5409126cd7bf76fa03c70dc13c5c8c1786e51` |
| `soc-ap/middleware/dds/examples/CMakeLists.txt` | 示例构建脚本 | `c8d70445e4688a238319626f317a9e1fe14b618cd6e8cfa397eb1595e6c18fb8` |
| `soc-ap/middleware/dds/examples/publisher_example.cpp` | 遥测发布端标准示例程序 | `34b035b61ba1de90150ab3c19f382c5c31d62600886e03725e349c7a1dcbf4b6` |
| `soc-ap/middleware/dds/examples/subscriber_example.cpp` | 遥测订阅端标准示例程序 | `47d230b9e7ad967c46c6601cfb2d34006606314b2b275c51e22662e6afd90c80` |
| `soc-ap/tests/dds/twin/CMakeLists.txt` | 测试套件构建脚本 | `1dff2c0658c49f180a2deb0c6ac57271ce92c9e1eae123249bac3e60de54c775` |
| `soc-ap/tests/dds/twin/test_dds_pubsub.cpp` | 综合测试用例 (含配额上限、晚加入、队列深度、IPC) | `86fa9c929e9802e8ec934fc1563a35cacf9829564af20827209b819079b5c7b2` |
| `soc-ap/third_party/dds/README.md` | Fast DDS 第三方归档与依赖说明 | `3f523e14bfd21b00135cbaf0c0d841c87f1e37df0f7ad3e85f1b5acebf4cc525` |

---

## 3. 编码硬门禁符合性

全模块自研函数行数严格控制在 $\le 50$ 行（最大函数 48 行），自研函数入参个数 $\le 4$ 个，每个公开函数入口均有严格的空指针防御，静态无界分配已全部由硬配额截断。
