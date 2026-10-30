---
template_version: '2026-10-27'
review_id: TWIN-04-ARCH-run_02-audit
review_status: completed
reviewer_role: ARCH
reviewer_roles: [ARCH]
platform: codex
requested_model: gpt-6-luna
actual_model: gpt-6-luna
model_override_ref: null
planned_session_alias: planned-arch-twin-04-r2
actual_session: 01a18b07-680e-7890-8301-ee5590d73c62
author_session: 1aba53f3-e424-4e8c-926a-ddfc0d5e44c5
task_id: TWIN-04
task_revision: 2
reviewed_artifact_version: "soc-ap=6a7864293f95fd44e5d3cc631289bb71489705b7; test_harness=0b7497ba43158841eb3c4af7f16e477b9c30c2c5; project-control=96db58ee9fb4d7f6ae2e607f4b457b971c4de0db; mcu-p3=1246ea9cb441d074ea444f53320f5632fefcd503"
reviewed_qa_report_sha256: ce0cba99c239cc5372e6aed89b4886003ebe4a5406d0ca983e5df61036385ad6
reviewed_artifacts:
  - {path: soc-ap/cmake/toolchains/vmware.cmake, sha256: fba14e74e65cf40761d2d638149c51840da2d9546067e78667cdc8f3d93f4a98}
  - {path: soc-ap/runtime/common/service_lifecycle.h, sha256: 0c11fe8cae24c5a276c5f499ac269f0509226c53979df7b17fe44a9b243e2977}
  - {path: soc-ap/runtime/common/service_lifecycle.cpp, sha256: a37604e611e94a5328d3e8cfd80a2d96f4a149ab6086232c5902e66db3c6d635}
  - {path: soc-ap/runtime/vmware/supervisor.h, sha256: 779267b37460f3f4d2193b587209c0cc677cf4565219f058ab4b238f05caad30}
  - {path: soc-ap/runtime/vmware/supervisor.cpp, sha256: df2900ee8120534e798f3eb023c519b81af48b45a6b445eb2143b0e6212ec26e}
  - {path: soc-ap/runtime/vmware/main.cpp, sha256: 2c32bd3636f7bd938e1ed4247029562d4ee8da10876ed1a59846c059b2334759}
  - {path: soc-ap/runtime/build/CMakeLists.txt, sha256: adfe12ea3e89c50034f3da1f9b19804c262d87062308b5634e834baf8fcae345}
  - {path: soc-ap/runtime/build/tests/test_service_lifecycle.cpp, sha256: ddc94c4c42208cb51668aa9889a87a5ca36fcca830c1bd46c2b4974fd597a00e}
  - {path: soc-ap/runtime/build/tests/test_backoff.cpp, sha256: e70bde70ea001809a428fda7e846f021fe38f38162d0bf066615c1e7d6cdf3dc}
  - {path: soc-ap/runtime/build/tests/test_supervisor_topology.cpp, sha256: f912a3614947e4db7c41c4b7c00c092f40982853bc5a5374951e5252bd7c7a56}
  - {path: soc-ap/config/runtime/common/services_manifest.json, sha256: 79c529657d3550c59305b039ed2a0e70ab013e7676e4d944c513fc925a840204}
  - {path: soc-ap/config/runtime/vmware/services_manifest.json, sha256: aface080d154ea97017c207e08ff41f810a4b3115933f6c2ec9e91e35c950af1}
  - {path: soc-ap/tools/twin_build/build_vmware.sh, sha256: a911e8b7c60533fcd7adb0111a336aac7f6c24384fcd75e3fedf11ad34ce374f}
  - {path: project-control/docs/evidence/twin/TWIN-04/runs/run_02/result.md, sha256: c23e717791b1808a22d2235dabdb9377766b92dfd1c2db2e508932182fd677c3}
  - {path: project-control/docs/evidence/twin/TWIN-04/runs/run_02/arch_server_qa/server_qa.json, sha256: 6aea8e01261e92414cd3f90c036940c485ac0e3e098ee591df5b8f6eb23bc8e8}
  - {path: project-control/docs/evidence/twin/TWIN-04/runs/run_02/qa_review_report.md, sha256: ce0cba99c239cc5372e6aed89b4886003ebe4a5406d0ca983e5df61036385ad6}
server_qa:
  path: project-control/docs/evidence/twin/TWIN-04/runs/run_02/arch_server_qa/server_qa.json
  sha256: 6aea8e01261e92414cd3f90c036940c485ac0e3e098ee591df5b8f6eb23bc8e8
content_audit:
  fact_sources: {result: passed, basis: "复算交付物与QA报告哈希；检查候选HEAD、源码、两份manifest、作者结果、QA报告及独立arch_server_qa记录。"}
  protocol_compatibility: {result: not-applicable, basis: "VMware服务生命周期与构建变更不涉及MCU协议变更。"}
  claim_scope: {result: passed, basis: "评估范围为VMware软件构建与进程生命周期；将容器软件测试与物理硬件验证区分。"}
  architecture_completeness: {result: passed, basis: "检查拓扑注册与排序、真实进程启动及exec失败检测、waitpid健康巡检、信号驱动事件循环、反向拓扑停止与超时处理。"}
determination: APPROVED
decision: APPROVED
issues: []
signed_off_at: "2026-10-30T12:15:00+08:00"
---

# TWIN-04 Run 02 Final Audit

## Review summary

**Decision: APPROVED**

The reviewed deliverable hashes and QA report hash match the supplied values. The four workspace repository HEADs match the candidate commits. Static review covered the VMware toolchain and build script, lifecycle implementation, supervisor and CLI, manifests, tests, author result, QA report, and independent server QA evidence.

The two server QA records identify distinct sandbox IDs: `TWIN-04_run_121447_20261030_041447` for primary QA and `TWIN-04_run_121527_20261030_041527` for this ARCH review. The secondary sandbox record pins the same candidate commits.

## Architecture and QA report review

The shared lifecycle implementation provides guarded state transitions, health checks, and bounded backoff. The supervisor registers active and deferred services, computes active-service topology, starts real binaries through `fork`/`execv`, detects exec failure through a close-on-exec pipe, checks child status with `waitpid(..., WNOHANG)`, and stops services in reverse topology order. Its stop path sends SIGTERM, waits within `stop_timeout_ms`, and escalates if needed. The daemon loop handles SIGINT/SIGTERM and polls events and health.

The submitted tests include real-mode missing-binary rejection, valid-binary spawn and health checks, graceful stop, and manifest binding. The manifest binding test opens both manifest files, extracts service names and binary paths, and compares them against registered services.

The build script supports CMake and a direct g++ path. The secondary server QA record reports the direct g++ path, successful build, lifecycle/backoff/topology test suites, CLI dry-run and simulation checks, and package generation. These results are software-level evidence; they do not establish physical SoC or MCU validation. The reviewed QA report accurately scopes the direct compilation fallback and host-side CTest compatibility, and records the required real-process and manifest tests.

## Server evidence verification

Recomputed SHA256 values for the secondary `server_qa.json`, `server_lock.json`, `checkout.log`, `runtime.log`, and `server_verdict.json` match the values recorded for those artifacts. The lock pins all four candidate commits, and the checkout log records fetching and checking out those commits. The primary QA report’s hash also matches the reviewed SHA256.

The secondary sandbox ID differs from the primary QA sandbox ID, as required. The evidence records a read-only workspace bind mount and an exited container state.

## Limitations

This read-only review did not access a host Docker daemon or socket. Container identity, image digest, mount details, checkout, build, and test results were assessed from the hash-verified server QA records rather than queried directly from Docker. Physical hardware validation was outside this task’s software-level evidence.

## Final determination

**APPROVED** for TWIN-04 revision 2 at the reviewed candidate commits. No issues were identified.