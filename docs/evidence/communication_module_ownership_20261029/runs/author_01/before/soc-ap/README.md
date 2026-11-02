# SoC Application Repository (soc-ap)

The current source includes the host runtime and MiniMCProto query paths for `--target mc|th --cmd version|ping|temp` with optional `--json`. Without query arguments, the original runtime only reports configuration and handles shutdown. Query mode accesses the physical serial device; its accepted hardware scope depends on the exact candidate and evidence.

The next increment is the [VMware→SoC twin task chain](../project-control/docs/planning/vmware_soc_twin_task_execution_20261029.md). Phase 1 must run real persistent services, process management, D-Bus/DDS, and an interactive browser UI backed by the actual modules and MC/TH. Phase 2 reuses business source, contracts, and UI assets with target platform/toolchain/deployment adaptation and real-board acceptance. The planned services and complete twin launch command are not implemented by this documentation change.

## Requirements

- CMake 3.16 or newer
- A C++17 compiler (GCC or Clang)
- Ninja is recommended; Make is also supported

No third-party libraries or system packages are installed by the project.

## Build and check

From this repository root:

```sh
cmake -S . -B build/host -G Ninja -DCMAKE_BUILD_TYPE=Release
cmake --build build/host
(cd build/host && ctest --output-on-failure)
```

The executable is `build/host/bin/soc-ap`. To use Make, omit `-G Ninja`.

## Run

```sh
SOC_AP_SERIAL_PORT=/dev/ttyUSB0 ./build/host/bin/soc-ap
```

The endpoint can also be selected with `--serial-port PATH`; the command-line
option takes precedence over `SOC_AP_SERIAL_PORT`. The default is
`/dev/ttyUSB0`. `config/host.env.example` records the VMware setting; export
the variable in the shell before starting the process. `--check-config` prints
the selected endpoint without touching the device. Press Ctrl-C or send
`SIGTERM` for a clean shutdown.

Do not run diagnostic CLI queries while forward-service owns the UART. Use the accepted candidate/SOP and exclusive device window; building or starting a process alone does not prove the physical chain. See the [handover requirements](../project-control/docs/operations/ap_mc_th_software_hardware_handover.md), including the two-phase checklist.
