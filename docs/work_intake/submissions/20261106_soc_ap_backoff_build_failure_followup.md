# 人工收件单：soc-ap backoff 测试编译阻断现场补充

## 公共约束

- 提交人及日期：sushaohua，2026-11-06；项目助理按用户提供的编译日志整理。用户本轮要求加入任务收件箱，助理不修改业务代码、不运行构建或测试、不操作硬件。
- 已有关联：`ISS-20261105-001`（其记录关联 `TWIN-51`），以及 `20261105_soc_ap_build_and_startup_issues.md` 指令 1。由唯一 COORD 先查重，关联原问题补充现场证据；不因新文件重复派单。若原任务已经关闭，按实际版本核查是否漏同步、旧检出或回归，保留历史结论，必要复验另建 run。
- 现场目录是 `/home/sushaohua/testaaa/ai_soc_project/`，与当前助理工作区不同。现场分支、完整提交、未提交改动、编译器版本和完整构建命令尚未提供，不能默认与当前工作区相同，也不能沿用旧单的 GCC 15 判断本次实际版本。
- 后续按现行职责、已有有效授权和简化 QA 安排工程核查及最小修复；COORD 不代改业务源码。本单不授权占用唯一 VMware/台架、部署、烧录或停止现有任务。

## 指令 1

【问题】补充 test_backoff_null_guards 编译失败现场：cfg 可能未初始化，触发 -Werror=maybe-uninitialized 导致构建退出。

用户报告编译在 `runtime/build/tests/test_backoff.cpp` 失败：函数 `test_backoff_null_guards()` 第 14 行声明 `backoff_config_t cfg;`，第 18 行将 `&cfg` 作为参数传给 `backoff_init(NULL, &cfg)`，编译器将可能未初始化诊断作为错误处理，最终 `gmake` 退出码为 2。

用户提供的原始日志：

```text
In file included from /home/sushaohua/testaaa/ai_soc_project/soc-ap/runtime/build/tests/test_backoff.cpp:9:
/home/sushaohua/testaaa/ai_soc_project/soc-ap/runtime/build/tests/test_backoff.cpp: In function ‘void test_backoff_null_guards()’:
/home/sushaohua/testaaa/ai_soc_project/soc-ap/runtime/build/tests/test_backoff.cpp:18:24: error: ‘cfg’ may be used uninitialized [-Werror=maybe-uninitialized]
   18 |     assert(backoff_init(NULL, &cfg) == LIFECYCLE_ERR_INVALID_ARGUMENT);
      |            ~~~~~~~~~~~~^~~~~~~~~~~~
In file included from /home/sushaohua/testaaa/ai_soc_project/soc-ap/runtime/build/tests/test_backoff.cpp:6:
/home/sushaohua/testaaa/ai_soc_project/soc-ap/runtime/build/tests/../../common/service_lifecycle.h:146:20: note: by argument 2 of type ‘const backoff_config_t*’ to ‘lifecycle_status_t backoff_init(backoff_state_t*, const backoff_config_t*)’ declared here
  146 | lifecycle_status_t backoff_init(backoff_state_t* state, const backoff_config_t* config);
      |                    ^~~~~~~~~~~~
/home/sushaohua/testaaa/ai_soc_project/soc-ap/runtime/build/tests/test_backoff.cpp:14:22: note: ‘cfg’ declared here
   14 |     backoff_config_t cfg;
      |                      ^~~
cc1plus: all warnings being treated as errors
gmake[2]: *** [CMakeFiles/test_backoff.dir/build.make:79: CMakeFiles/test_backoff.dir/tests/test_backoff.cpp.o] Error 1
gmake[1]: *** [CMakeFiles/Makefile2:1119: CMakeFiles/test_backoff.dir/all] Error 2
gmake: *** [Makefile:101: all] Error 2
```

处理要求：

1. 核对本次现场源码/构建输入、编译参数及原任务修复提交的实际包含关系，确认是原问题未解决、检出未更新还是后续回归；不能仅凭问题相同就认定现场已修复。
2. 在确认的受版本管理源码中做最小修复；优先核实 `cfg` 及同函数 `st` 是否应显式零初始化。保持空指针防御断言和严格告警策略，不通过关闭 `-Werror`、屏蔽该告警或删除断言绕过。编译诊断不直接等同于已发生运行期非法读取，运行逻辑另行核实。
3. 验收时记录准确候选、实际编译器、命令与结果；在原触发条件下消除阻断，完成相关 backoff 防御、递增、上限及重置行为验证。若仅验证 runtime 或相关目标，不表述为全栈全部通过。

助理本次仅整理收件材料，未读取该外部现场目录、未复现错误、未确认修复完成。保存本单表示进入 COORD 下次收件检查的输入，不代表已经正式收件、派发或关闭。
