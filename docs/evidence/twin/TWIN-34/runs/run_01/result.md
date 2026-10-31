# TWIN-34 Web HMI手动轴控盘与5×5调平网格热力图组件实现自检报告 (Self-Check Report)

- **执行角色**：ENG-UI (前端与界面工程师)
- **任务编号**：TWIN-34
- **运行轮次**：run_01
- **状态**：COMPLETED (待独立 QA / ARCH 审签)
- **交付制品**：
  1. `soc-ap/browser_hmi/first_release/index.html`
  2. `soc-ap/browser_hmi/first_release/app.js`
  3. `soc-ap/browser_hmi/first_release/styles.css`
  4. `soc-ap/browser_hmi/first_release/test_hmi_contract.py`

## 自检核对结果
1. **[PASS] 手动轴控面板与步长微调组件**：
   - 实现独立【🕹️ 轴控与调平】Tab 标签页（`#tab-motion`）；
   - 提供 0.1mm、1mm、10mm、100mm 步长微调档位切换（`#step-selector`）；
   - 实现 CoreXY 运动方向触控罗盘（▲ +Y, ▼ -Y, ◀ -X, +X ▶）与中心一键 XY 归零按钮（`#btn-home-xy`）；
   - 实现 Z 轴升降抬起/下降大键与 $\pm 0.05\text{mm}$ 婴儿步（Baby-stepping）首层微调按钮；
   - 顶部提供全轴复位归零大按钮（`#btn-home-all`，触发 G28 ALL）。
2. **[PASS] 实时坐标读数板**：
   - 包含 X、Y、Z、E 四轴毫厘级数字读数（`#coord-val-x`, `#coord-val-y`, `#coord-val-z`, `#coord-val-e`），由 SSE 流及每次 Jog 响应双向同步更新。
3. **[PASS] 5×5 自动调平高程热力图渲染**：
   - 实现 25 点高程网格容器（`#leveling-mesh-grid`）；
   - 根据真实网格偏差值（-0.20mm ~ +0.20mm）映射动态色阶（深蓝、浅蓝、翠绿、琥珀黄、警戒红）；
   - 底部同步展示极值跨度（`#mesh-variance-val`）与平面倾斜度特征分析（`#mesh-tilt-val`）；
   - 具备“重新测量”按钮（`#btn-trigger-leveling`）并与后端 `/api/v1/leveling/trigger` 联动。
4. **[PASS] 契约与单元测试全绿**：
   - `soc-ap/browser_hmi/first_release/test_hmi_contract.py` 全部 8 项断言 100% 通过。
