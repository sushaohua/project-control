# SoC Application Repository (soc-ap)

This repository starts the Ubuntu host-side SoC/AP runtime. The current MS-18
foundation is deliberately small: it builds, starts, reports its configured
serial endpoint, and exits cleanly on `SIGINT`/`SIGTERM`. It does **not** open
the serial device or implement MC/TH commands; those need accepted interfaces
and follow-on task cards.

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

Until an interface task defines the wire contract, this host runtime does not
open the endpoint, issue queries, or claim a successful MC/TH connection. The
VMware path `ssh vmware` and CH341 device `/dev/ttyUSB0` are environment inputs;
runtime access and the device's current availability still need verification.
