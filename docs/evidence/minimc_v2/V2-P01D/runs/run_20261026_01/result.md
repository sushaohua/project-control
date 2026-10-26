# V2-P01D Execution Record (`run_20261026_01`)

- `task_id`: `V2-P01D`
- `revision`: `1`
- `run_id`: `run_20261026_01`
- `executor_role`: `QA`
- `executor_session`: `663fcda3-b02b-4d3a-89f6-ffc1ef283810`
- `lease_id`: `lease_v2_p01d_20261026_01`
- `started_at`: `2026-10-26T15:56:00+08:00`
- `finished_at`: `2026-10-26T16:10:02+08:00`
- `base_commit`:
  - `test_harness`: `a3cccf17ac0e740352413daeebe20ef89d82f594`
  - `soc-ap` (read-only contract source): `849135ee69500e7e96ee75eed73c245e1ac94851`
- `head_commit`:
  - `test_harness`: `a3cccf17ac0e740352413daeebe20ef89d82f594` (uncommitted working tree deliverable `test_harness/static_checks/minimcproto/reference_vectors.py` ready for independent `ARCH` review)
- `consumed_artifacts`:
  - `soc-ap/contracts/minimcproto/v2-minimal.md` (`sha256:5fc11e865fde44d780db94487855a7d762092a38362e9be66491b66626ad5ade`, accepted in `docs/evidence/minimc_v2/V2-P01A/runs/run_20261026_01/qa_review_report.md`)
  - `soc-ap/contracts/minimcproto/v2-commands.md` (`sha256:25345c74b20051266626a1684be7f68f49bb570382969364b39301b7496a05e4`, accepted in `docs/evidence/minimc_v2/V2-P01B/runs/run_20261026_01/qa_review_report.md`)
  - `test_harness/test_cases/minimcproto/vectors.json` (`sha256:6d46bd05a4133e678611abe2ab1cb88db190c394f23151900009c0c077c8d995`, accepted in `docs/evidence/minimc_v2/V2-P01C/runs/run_20261026_01/arch_review_report.md`)
  - `project-control/docs/minimc/MiniMC_Protocol_Spec_v2.0_r3_fixed.md` (`sha256:9f8d4f9607cb3e76cc30b9ee2f971b23c3e0d936611188466a71f4aa15f3ce54`)
- `produced_artifacts`:
  - `test_harness/static_checks/minimcproto/reference_vectors.py` (`sha256:a8664e5d461a960feaf4d28fc1e73e2fac5ebf568da202df552b849e2382d67a`, `28503` bytes)
  - `project-control/docs/evidence/minimc_v2/V2-P01D/runs/run_20261026_01/01_precheck.log`
  - `project-control/docs/evidence/minimc_v2/V2-P01D/runs/run_20261026_01/02_reference_check.log`
  - `project-control/docs/evidence/minimc_v2/V2-P01D/runs/run_20261026_01/03_reference_self_check.log`
  - `project-control/docs/evidence/minimc_v2/V2-P01D/runs/run_20261026_01/result.md`
- `commands_executed`:
  1. `git -C soc-ap rev-parse HEAD && git -C soc-ap status --porcelain=v1 && git -C test_harness rev-parse HEAD && git -C test_harness status --porcelain=v1` -> `exit_code: 0` (logged in `01_precheck.log`)
  2. `python3 test_harness/static_checks/minimcproto/reference_vectors.py --vectors test_harness/test_cases/minimcproto/vectors.json --check` -> `exit_code: 0` (logged in `02_reference_check.log`)
  3. `python3 test_harness/static_checks/minimcproto/reference_vectors.py --vectors test_harness/test_cases/minimcproto/vectors.json --self-check` -> `exit_code: 0` (logged in `03_reference_self_check.log`)
  4. `sha256sum test_harness/static_checks/minimcproto/reference_vectors.py test_harness/test_cases/minimcproto/vectors.json && wc -c test_harness/static_checks/minimcproto/reference_vectors.py` -> `exit_code: 0`
- `verification_summary`:
  - **Pure Python 3 Standard Library**: Uses only `argparse`, `copy`, `hashlib`, `json`, `pathlib`, `struct`, `sys`, and `typing`. Zero third-party packages; zero imports or subprocess invocations of production C/C++ libraries or test probes.
  - **Independent Reference Engine**: Implements bit-by-bit `CRC-16/CCITT-FALSE` (`poly=0x1021`, `init=0xFFFF`, `refin=False`, `refout=False`, `xorout=0x0000`), little-endian 12-byte header pack/unpack, whole-frame encode/decode with `OQ-01` broadcast (`dst_id == 0xFF`) vs command-profile validation (`V04` `frame_valid=True, command_valid=False`), and the 4-state `ReferenceStreamParser` (`WAIT_SOF1`, `WAIT_SOF2`, `READ_HEADER`, `READ_PAYLOAD`, `READ_CRC`) with `0x55 0x55 0xAA` resynchronization, `payload_len > 1024` immediate header-stage rejection, 50ms inter-byte timeout with `uint32_t` wraparound (`(uint32_t)(now_ms - last_byte_rx_ms) > 50`), and CRC-error recovery.
  - **`--check` Verification**: Validated `schema_version`, `protocol_sha256`, `consumed_contracts` (`V2-P01A`, `V2-P01B`), all 5 golden frames (`V01`, `V02_INBOUND`, `V02_OUTBOUND`, `V03`, `V04`), and all 64 cases across `stub` (4) and all 9 required functional groups (`crc`: 9, `encode`: 8, `decode_bounds`: 6, `decode`: 12, `stream_sync`: 5, `stream_header`: 5, `stream_payload`: 5, `timeout`: 6, `recovery`: 4) with `errors: []` and `exit_code: 0`.
  - **`--self-check` Verification**: Executed 8 in-memory negative mutations (corrupt golden `V01` CRC, corrupt `CRC-001` expected CRC, duplicate `case_id`, empty functional group `timeout`, tampered `protocol_sha256`, violated `V04` `OQ-01` `command_valid`, corrupted `DEC-002` `header.seq`, corrupted `REC-004` `dispatched_frames`) without modifying `vectors.json` on disk; all 8 mutations were caught with `simulated_exit_code == 1`, returning overall `exit_code: 0`.
- `residual_risks`:
  - `reference_vectors.py` validates the offline specification and vector contract (`vectors.json`). Actual C/C++ production library and probe conformance against these vectors will be verified in `V2-P02B` (`--group stub`) and `V2-P04`～`V2-P06` (`run_minimcproto_vectors.py`).
