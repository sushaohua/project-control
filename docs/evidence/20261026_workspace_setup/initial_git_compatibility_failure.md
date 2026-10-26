# 首次验证失败与修正

本会话首次初始化/测试实际返回：`error: unknown switch b`（Git 2.25.1 不支持 `git init -b`）。
测试进程退出 1，8 项均在初始化 fixture 时失败；工作区 init 同样在参数检查处停止。
修正为 `git init` 后用 `git symbolic-ref HEAD refs/heads/main` 设置初始分支。

再次测试中 7 项通过，bundle 恢复项失败，原因是 bundle 只列出 main 分支，
克隆时未指定分支，未检出 workspace.json。实际错误与日志见 initial_bundle_test_failure.log。
修正为克隆时显式指定 `--branch main`，同步更新说明。后续 8 项全部通过，退出 0。
没有放宽测试、覆盖用户改动或执行硬件操作。
