# ISSUE-20261102-04 Web HMI 核心交互特性端到端自动化测试验收证据

## 1. 验证目标与交付基线
- **关联 Issue**: [ISSUE-20261102-04](../../issues/ISSUE-20261102-04.md)
- **关联任务**: `TASK-QA-E2E-02` (QA 自动化套件编写) & `TASK-INT-E2E-02` (Twin 部署回归与物证归档)
- **代码提交**: `test_harness@c574fb22f99221283fc3737c536402cdbf78107f`
- **新增用例套件**: `test_harness/hil/tests/test_qa_e2e_features_browser.py`
- **执行环境**: VMware Twin (`192.168.77.134:8080`)，挂载真实 AT32F435 MC + AT32F423 TH 硬件台架，Chrome CDP 协议无头会话驱动

---

## 2. 测试用例执行结果清单

```text
==================================================================
=== QA BROWSER E2E CORE FEATURES TEST RESULTS SUMMARY         ===
==================================================================
  TC-E2E-LANG-01           : PASS
  TC-E2E-THEME-01          : PASS
  TC-E2E-FILAMENT-01       : PASS
  TC-E2E-JOG-01            : PASS

[SUCCESS] All 4 browser E2E core features passed with 100% compliance!
```

---

## 3. 详细测试物证与 SHA256 校验

### 3.1 TC-E2E-LANG-01: 动态多语言即时切换
- **操作动作**: 触发顶栏 `#btn-lang-toggle` 及 OOBE 单选按钮，校验中英文 (zh-CN <-> en-US) 免刷新即时动态翻译。
- **验证断言**: DOM 文本由“新机检查引导向导 (OOBE)”即时切换为“Out of Box Setup Wizard (OOBE)”，工具头变更为“Toolhead Nozzle (TH)”，按钮状态同步更新。
- **截图物证**: `screenshots/TC-E2E-LANG-01_en_switch.png`
- **SHA256**: `3108c7176c366096443ae5f1136e0e76266f4ddb9e9e80fab21951acba1c0f44`

### 3.2 TC-E2E-THEME-01: 亮暗主题即时切换
- **操作动作**: 点击 `#btn-theme-toggle` 按钮切换主题。
- **验证断言**: `data-theme` 属性由 `dark` 动态切换为 `light`，图标变更为 `🌙`，计算样式背景色即时转为高对比度浅色（`rgb(248, 250, 252)`），再次点击平滑切回。
- **截图物证**: `screenshots/TC-E2E-THEME-01_light_theme.png`
- **SHA256**: `8618801c219098adba7d91743cd7afaa3c51cbc1e9a0dd12b6cc86fbc057f711`

### 3.3 TC-E2E-FILAMENT-01: 4 通道供料与混色管理
- **操作动作**: 切换 4 色耗材槽（Slot 0~3），选取材质（PLA/PETG/ABS/TPU），调节混色权重至 10000 守恒并触发保存。
- **验证断言**: 槽位激活态互斥切换，材质选择框响应即时，下发进退料指令弹出合法 Toast，权重守恒逻辑满足 `Sum=10000` 约束。
- **截图物证**: `screenshots/TC-E2E-FILAMENT-01_slot_active.png`
- **SHA256**: `ff7499ea098cd0cd3628850d18b7de23d399fa4837864c07ff4550ea2e27f077`

### 3.4 TC-E2E-JOG-01: 手动运控点动与三轴读数
- **操作动作**: 切换步长档位（0.1mm / 1mm / 10mm），点击 `+X/-X/+Y/-Y/+Z/-Z` 及 `+0.05mm` 婴儿步微调，点击 `#btn-home-xy` 与 `#btn-home-all` 归零动作。
- **验证断言**: 触发真实 `/api/v1/motion/jog` 与 `/api/v1/motion/home` REST 下发，三轴实时坐标仪表 (`#coord-val-x`, `#coord-val-y`, `#coord-val-z`) 稳定回显。
- **截图物证**: `screenshots/TC-E2E-JOG-01_motion_active.png`
- **SHA256**: `f1dd7664c9911cd2b3b8aa83f15ea6715d123fba389a126917ca1ee412c954f9`

---

## 4. 结论与闭环判定
Web HMI 前端已支持的 4 大核心交互特性（多语言、主题、供料、运控）已全部由独立的 Chrome CDP 自动化测试套件完整覆盖，实机回归全部通过，物证齐全，满足交付门禁要求。
