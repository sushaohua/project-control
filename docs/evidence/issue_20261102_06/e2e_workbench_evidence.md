# ISSUE-20261102-06 Web HMI 打印工作台、5×5 调平与急停熔断端到端自动化测试验收证据

## 1. 验证目标与交付基线
- **关联 Issue**: [ISSUE-20261102-06](../../issues/ISSUE-20261102-06.md)
- **关联任务**: `TASK-QA-E2E-03` (QA 自动化套件编写) & `TASK-INT-E2E-03` (Twin 部署回归与物证归档)
- **代码提交**: `test_harness@ccf1476a0b98cb55ca9ee7bd49d73ca5d4704414`
- **新增用例套件**: `test_harness/hil/tests/test_qa_e2e_workbench_browser.py`
- **执行环境**: VMware Twin (`192.168.77.134:8080`)，挂载真实 AT32F435 MC + AT32F423 TH 硬件台架，Chrome CDP 协议无头会话驱动

---

## 2. 测试用例执行结果清单

```text
==================================================================
=== QA BROWSER E2E WORKBENCH TEST RESULTS SUMMARY             ===
==================================================================
  TC-E2E-JOB-01-POS        : PASS
  TC-E2E-JOB-02-POS        : PASS
  TC-E2E-JOB-03-POS        : PASS
  TC-E2E-MOT-03-POS        : PASS
  TC-E2E-HMS-01-POS        : PASS
  TC-E2E-HMS-02-POS        : PASS

[SUCCESS] All 6 browser E2E workbench test cases passed with 100% compliance!
```

---

## 3. 详细测试物证与 SHA256 校验

### 3.1 TC-E2E-JOB-01-POS: 打印作业启动闭环与流式进度
- **操作动作**: 切换进入“打印工作台”标签页，点击 `#btn-job-start` 开始打印。
- **验证断言**: 状态平滑切为 `PRINTING`（样式 `badge-success`），观测 2.5s 进度百分比/层数递增，拒绝静态假进度。
- **截图物证**: `screenshots/TC-E2E-JOB-01-POS_printing.png`
- **SHA256**: `426ee7d9234611a071ff0d901deb9a1dad773e22b2947c5eb4c4f74462685f1a`

### 3.2 TC-E2E-JOB-02-POS: 作业暂停与继续打流
- **操作动作**: 在 `PRINTING` 态下点击 `#btn-job-pause`，停留 1.5s 后点击 `#btn-job-resume`。
- **验证断言**: 状态转入 `PAUSED` 停滞进给，恢复后切回 `PRINTING` 续打。
- **截图物证**: `screenshots/TC-E2E-JOB-02-POS_paused_resume.png`
- **SHA256**: `70eaa92bf8ea88163683c6ccc0b39a7ad2f94f15fb860e8b095cc54ad8081306`

### 3.3 TC-E2E-JOB-03-POS: 取消打印作业与按钮就绪态
- **操作动作**: 点击 `#btn-job-cancel` 取消打印（通过 CDP 自动接管 window.confirm）。
- **验证断言**: 作业状态转换为 `IDLE` / `CANCELLED`，操作按钮恢复开始就绪态。
- **截图物证**: `screenshots/TC-E2E-JOB-03-POS_cancelled.png`
- **SHA256**: `fd8b5a0a015f6a652b04c43307db266ab3d2de8b23c237569061d11ab53d5fc4`

### 3.4 TC-E2E-MOT-03-POS: 5×5 自动调平网格与热力图
- **操作动作**: 切换至“轴控与调平”标签页，点击 `#btn-trigger-leveling` 重新测量。
- **验证断言**: 触发 `/api/v1/leveling/trigger`，获取 `/api/v1/leveling/mesh`，断言 `#leveling-mesh-grid` 容器完整渲染 25 个 `.mesh-cell` 单元格及离散度极值。
- **截图物证**: `screenshots/TC-E2E-MOT-03-POS_mesh_heatmap.png`
- **SHA256**: `b7acd81e0d0c7a9da80fa2ba75ed1ba0d99c1bb5651d25d0c97ee4c366e51bdd`

### 3.5 TC-E2E-HMS-01-POS: E-STOP 紧急急停熔断
- **操作动作**: 点击顶栏全局急停按钮 `#btn-header-estop`。
- **验证断言**: 即刻下发 M112 急停，作业状态徽章转入 `ESTOP_FAULT`（样式 `badge-danger` 红框高亮锁定），禁止继续下发运动。
- **截图物证**: `screenshots/TC-E2E-HMS-01-POS_estop_active.png`
- **SHA256**: `20c5e2c155fe4e0266115ceb0cbf428398761a1869b4c4198bf7b751a449518d`

### 3.6 TC-E2E-HMS-02-POS: 急停清除恢复
- **操作动作**: 触发清除急停并刷新状态。
- **验证断言**: 状态机平滑恢复 `IDLE` 就绪态，解除危险告警样式，控制恢复可交互。

---

## 4. 结论与闭环判定
首发版本中打印工作台、自动调平与急停熔断的所有核心交互与业务链路全部通过自动化测试验证，物证完整，满足交付门禁。
