# Third-Party Dependencies (soc-ap/third_party)

This directory hosts the vendor dependencies required for the SoC Application runtime:
- **D-Bus**: `1.16.2` (Stable Linux standard)
- **Fast DDS**: `3.6.2` (Long Term Support / LTS)
- **Fast CDR**: `2.2.5` (Fast DDS serialization dependency)
- **foonathan_memory**: `0.7-3` (STL-compatible memory allocators for Fast DDS)
- **asio**: `ed6aa8a` (Standalone Asio networking for Fast DDS)
- **tinyxml2**: `8c8293b` (XML profile parsing for Fast DDS)

All source archives are stored locally under `archives/` with explicit SHA256 verification, enabling fully offline, reproducible builds for both VMware (x86_64) and target SoC (aarch64).

---

## Directory Layout

```
soc-ap/third_party/
├── archives/               # Tracked release tarballs & sha256 checksums
│   ├── Fast-CDR-2.2.5.tar.gz
│   ├── Fast-DDS-3.6.2.tar.gz
│   ├── asio-ed6aa8a.tar.gz
│   ├── checksums.sha256
│   ├── dbus-1.16.2.tar.xz
│   ├── foonathan_memory-0.7-3.tar.gz
│   ├── foonathan_memory_vendor-1.3.1.tar.gz
│   └── tinyxml2-8c8293b.tar.gz
├── src/                    # Extracted source trees (local, ignored in git)
│   ├── Fast-CDR-2.2.5/
│   ├── Fast-DDS-3.6.2/
│   ├── dbus-1.16.2/
│   └── foonathan_memory-0.7-3/
├── build/                  # CMake build artifacts (ignored in git)
├── install/                # Staged installation prefix (ignored in git)
│   ├── bin/                # dbus-daemon, fast-discovery-server, etc.
│   ├── include/            # D-Bus and Fast-DDS C/C++ header trees
│   ├── lib/                # libdbus-1.so, libfastdds.so, libfastcdr.so, etc.
│   └── share/              # CMake module configurations and service definitions
├── build.sh                # Automated build & verification script
└── README.md               # This document
```

---

## Checksums (SHA256)

Verified in `archives/checksums.sha256`:
- `Fast-CDR-2.2.5.tar.gz`: `b01fd34135e9be5183bb69f31fa5b74c53ba6eca30a5b21de0120d21ece22a51`
- `Fast-DDS-3.6.2.tar.gz`: `7ae3e55067a5337da98bc7997ec476fe04218c655457c10d4fbf74576d83f221`
- `asio-ed6aa8a.tar.gz`: `9d4619e1ea963d3c72c8dc07d5d8c9c4fab67141990b4f8cb10e5d8ad2c83f42`
- `dbus-1.16.2.tar.xz`: `0ba2a1a4b16afe7bceb2c07e9ce99a8c2c3508e5dec290dbb643384bd6beb7e2`
- `foonathan_memory-0.7-3.tar.gz`: `4203d15db22a94a3978eeb1afb59a37d35c57c0f148733f0f1a53a6281cb74dd`
- `foonathan_memory_vendor-1.3.1.tar.gz`: `982d11615214497bd7c713f3463af27567c76bed06b9b61021bc24694fd11c4a`
- `tinyxml2-8c8293b.tar.gz`: `17995f6508c54c296f07c8fa661cc3f25927a2b0855cf9b0d50b8c6993a63acb`

---

## Build Instructions

### Prerequisites
- CMake >= 3.20 (Fast DDS / Fast CDR requirement)
- GCC / G++ (C++14 capable)
- `libexpat1-dev` (for D-Bus XML configuration parsing)

### Build All Libraries
Run the helper script:
```bash
./soc-ap/third_party/build.sh
```

### Build Individual Libraries
```bash
# Build only D-Bus 1.16.2
./soc-ap/third_party/build.sh dbus

# Build Fast DDS (automatically builds foonathan_memory and Fast CDR)
./soc-ap/third_party/build.sh fastdds
```

### Verify Existing Build
```bash
./soc-ap/third_party/build.sh --verify
```

---

## Integration with Downstream Tasks

Downstream CMake targets (e.g. `TWIN-04` DDS bus foundation, `TWIN-05` D-Bus foundation) can consume these libraries by setting:
```cmake
set(CMAKE_PREFIX_PATH "${CMAKE_CURRENT_SOURCE_DIR}/third_party/install;${CMAKE_PREFIX_PATH}")
find_package(fastdds REQUIRED)
find_package(DBus1 REQUIRED)
```
Or via PKG_CONFIG_PATH:
```bash
export PKG_CONFIG_PATH="$(pwd)/soc-ap/third_party/install/lib/pkgconfig:${PKG_CONFIG_PATH:-}"
```
