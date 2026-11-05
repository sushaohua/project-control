# TWIN-46 Full-Stack Live Gateway (http://127.0.0.1:18085) & Bidirectional Reconciliation Matrix

| Suite / Scenario | Category | `[MC-DBG]` Evidence | `[TH-DBG]` Evidence | AP HTTP/SSE Snapshot | Verdict | Detail |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Live HTTP Snapshot Offline Sentinel & 503 | OFFLINE Sentinel & HTTP 503 Control Lock | `records=15, drop=0` | `records=4, drop=0` | `system_status=OFFLINE, bed=2147483646, tool=2147483646, lock=HTTP 503` | **PASS** | PASS |
| Live SSE Stream Offline Sentinel & 503 | OFFLINE Sentinel & HTTP 503 Control Lock | `records=15, drop=0` | `records=4, drop=0` | `system_status=OFFLINE, bed=2147483646, tool=2147483646, lock=HTTP 503` | **PASS** | PASS |
| Live /api/v1/jobs/status & /api/v1/leveling/mesh | 1. Temperature Reporting & Setpoint | `bed=600/600 ddC, nozzle=2100/2100 ddC` | `nozzle=2100 ddC, adc=820, pullup=1` | `bed=600/600 ddC, nozzle=2100/2100 ddC, adc=820` | **PASS** | PASS |
| Live /api/v1/jobs/status & /api/v1/leveling/mesh | 2. Homing & Motion Control | `x=0, y=0, z=0, homed=0x07, state=IDLE` | `N/A (MC local axis planner)` | `x=0, y=0, z=0, homed=0x07, state=IDLE` | **PASS** | PASS |
| Live /api/v1/jobs/status & /api/v1/leveling/mesh | 3. 5x5 Bed Leveling Grid | `op=GRID_READ, idx=7, z_um=0, valid=1, status=DONE` | `N/A (MC Z-probe matrix)` | `points=25, idx=7, z_um=0, status=OK` | **PASS** | PASS |
| Live /api/v1/jobs/status & /api/v1/leveling/mesh | 4. Filament Feed/Retract & Slot Select | `op=LOAD, slot=1, mask=0x0F, step=DONE` | `op=LOAD, slot=1, mask=0x0F, step=DONE` | `op=LOAD, slot=1, mask=0x0F, step=DONE` | **PASS** | PASS |
| Live /api/v1/jobs/status & /api/v1/leveling/mesh | 5. Print Job State Machine | `state=IDLE, progress=0‰, ack_seq=6` | `Cascade thermal ready` | `state=IDLE, progress=0‰, ack_seq=6` | **PASS** | PASS |
| 5-Category Active Printing Reconciliation | 1. Temperature Reporting & Setpoint | `bed=600/600 ddC, nozzle=2100/2100 ddC` | `nozzle=2100 ddC, adc=820, pullup=1` | `bed=600/600 ddC, nozzle=2100/2100 ddC, adc=820` | **PASS** | PASS |
| 5-Category Active Printing Reconciliation | 2. Homing & Motion Control | `x=1250, y=2500, z=40, homed=0x07, state=IDLE` | `N/A (MC local axis planner)` | `x=1250, y=2500, z=40, homed=0x07, state=IDLE` | **PASS** | PASS |
| 5-Category Active Printing Reconciliation | 3. 5x5 Bed Leveling Grid | `op=GRID_READ, idx=7, z_um=0, valid=1, status=DONE` | `N/A (MC Z-probe matrix)` | `points=25, idx=7, z_um=0, status=OK` | **PASS** | PASS |
| 5-Category Active Printing Reconciliation | 4. Filament Feed/Retract & Slot Select | `op=LOAD, slot=1, mask=0x0F, step=DONE` | `op=LOAD, slot=1, mask=0x0F, step=DONE` | `op=LOAD, slot=1, mask=0x0F, step=DONE` | **PASS** | PASS |
| 5-Category Active Printing Reconciliation | 5. Print Job State Machine | `state=PRINTING, progress=250‰, ack_seq=6` | `Cascade thermal ready` | `state=PRINTING, progress=250‰, ack_seq=6` | **PASS** | PASS |
| Post-Fault Recovery | 1. Temperature Reporting & Setpoint | `bed=600/600 ddC, nozzle=2100/2100 ddC` | `nozzle=2100 ddC, adc=820, pullup=1` | `bed=600/600 ddC, nozzle=2100/2100 ddC, adc=820` | **PASS** | PASS |
| Post-Fault Recovery | 2. Homing & Motion Control | `x=1250, y=2500, z=40, homed=0x07, state=IDLE` | `N/A (MC local axis planner)` | `x=1250, y=2500, z=40, homed=0x07, state=IDLE` | **PASS** | PASS |
| Post-Fault Recovery | 3. 5x5 Bed Leveling Grid | `op=GRID_READ, idx=7, z_um=0, valid=1, status=DONE` | `N/A (MC Z-probe matrix)` | `points=25, idx=7, z_um=0, status=OK` | **PASS** | PASS |
| Post-Fault Recovery | 4. Filament Feed/Retract & Slot Select | `op=LOAD, slot=1, mask=0x0F, step=DONE` | `op=LOAD, slot=1, mask=0x0F, step=DONE` | `op=LOAD, slot=1, mask=0x0F, step=DONE` | **PASS** | PASS |
| Post-Fault Recovery | 5. Print Job State Machine | `state=PRINTING, progress=250‰, ack_seq=6` | `Cascade thermal ready` | `state=PRINTING, progress=250‰, ack_seq=6` | **PASS** | PASS |

## Additional Verification Evidence

- `GET /api/v1/temperature/snapshot` -> HTTP 200 (`system_status=OFFLINE`)
- `GET /api/v1/temperature/stream` -> HTTP 200 (`event=temp_update`, `system_status=OFFLINE`)
- `GET /api/v1/jobs/status` -> HTTP 200 (`job_state=IDLE`, `is_homed=True`)
- `GET /api/v1/leveling/mesh` -> HTTP 200 (`status=OK`, 5x5 grid verified)
- `POST /api/v1/jobs/start` (offline lock check) -> HTTP 503
- `POST /api/v1/motion/home` (offline lock check) -> HTTP 503
- Negative mismatch, CRC_ERR, TIMEOUT, BAD_FRAME, TX_ERR, and drop>0/trunc>0 fault injections intercepted and recovered.
