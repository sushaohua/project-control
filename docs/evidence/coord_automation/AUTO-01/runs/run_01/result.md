# AUTO-01 单票实际执行记录 (run_01)

```yaml
template_version: '2026-10-27'
task_id: AUTO-01
task_revision: 1
actual_run_id: run_01
actor_role: INTEGRATOR
actor_model: inherit
model_override_ref: null
actor_session: fad98376-ae68-4254-a199-e4d2983d21c5
lease_id: lease_auto-01_20261029_01
start_time: '2026-10-29T15:20:50+08:00'
end_time: '2026-10-29T15:30:00+08:00'
workspace: /home/sushaohua/workspace/ai_soc_project
branch: main
source_head: a5e4b5e97439cae4a7093d1d0a29c5dc9b3c7819
verification_environment: independent-codex-in-server-based-sandbox
verification_scope: server-verification-and-sandbox-runner
required_evidence_level: server-sandbox-verified
commands:
  - command: python3 project-control/tools/test_qa_runner.py
    cwd: .
    exit_code: 0
    passed: true
  - command: ./test_harness/runner/qa_entrypoint.sh
    cwd: .
    exit_code: 0
    passed: true
  - command: python3 project-control/tools/qa_runner/qa_runner.py --check-only
    cwd: .
    exit_code: 0
    passed: true
  - command: python3 project-control/tools/qa_runner/qa_runner.py --task AUTO-01 --revision 1 --repo-commit test_harness=6c61ce6e51cf83d7fb58d319c23cb91bf95786cb:refs/heads/main --cmd "test:test_harness:python3 static_checks/cascade/run_query_cases.py --check-vectors --cases test_cases/cascade/query_cases.json" --output-dir /tmp/qa_sandboxes/test_evidence_auto01
    cwd: .
    exit_code: 0
    passed: true
actual_result: passed
```

## 执行说明与验证总结

1. **已交付组件**：
   - `project-control/tools/qa_runner/qa_runner.py`: 核心 QA 运行器，支持 GitLab API 校验、SSH 远端鉴权、commit 服务端真实存在性核验、物理隔离沙箱创建、从服务器拉取源码、沙箱构建/测试执行、结构化证据报告生成。
   - `project-control/tools/qa_runner/__init__.py`: 包初始化文件。
   - `project-control/config/qa_runner/default_config.yaml`: 默认服务器（192.168.77.113:2222）、沙箱目录、超时与安全策略配置。
   - `test_harness/runner/harness_runner.py`: 夹具测试套件执行器，支持离线向量及 HIL 单元测试执行。
   - `test_harness/runner/qa_entrypoint.sh`: 夹具运行入口脚本，支持沙箱环境独立调用。
   - `project-control/tools/test_qa_runner.py`: 全量单元测试（20 项测试全部通过），严格验证代码规模硬性门禁（自研函数 $\le 50$ 行、$\le 4$ 参数）。

2. **服务端与沙箱隔离核实**：
   - 验证 GitLab REST API 连接与凭据鉴权成功（用户 `sushaohua`）。
   - 验证 SSH (192.168.77.113:2222) 远端连接成功。
   - 正例核验：从服务器检出 `test_harness` 指定 commit `6c61ce6e51cf83d7fb58d319c23cb91bf95786cb` 至沙箱 `/tmp/qa_sandboxes/AUTO-01_run_...` 并运行测试，生成完全兼容 `delivery_checks.py:check_server_qa` 的标准结构化 JSON 证据报告。
   - 负例拦截：未推送 commit 拒绝、占位 hash 拒绝、本地文件路径挂载拒绝、沙箱越权逃逸拦截全部生效。
