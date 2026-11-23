#!/usr/bin/env python3
"""UX-01 实板触控事件注入与帧缓冲正向截图采集辅助工具。

通过 SSH 连接目标板 root@192.168.1.101：
1. 将正向横屏 (1280x720) 坐标按板端 270 度旋转逆变换为 /dev/input/event0 原始坐标并注入；
2. 流式读取 /dev/fb0 (720x1280 BGRA8888) 并逆时针旋转 90 度还原为正向可读 PNG。
"""

from __future__ import annotations

import subprocess
import sys
import zlib
from pathlib import Path
from PIL import Image

BOARD_HOST = "root@192.168.1.101"
EVIDENCE_DIR = Path(__file__).resolve().parent


def run_board_py(code: str) -> bytes:
    """在目标板上执行单段 Python 脚本并返回标准输出原始字节。"""
    cmd = ["ssh", "-o", "ConnectTimeout=5", BOARD_HOST, f"python3 -B -c { subprocess.list2cmdline([code]) }"]
    return subprocess.check_output(cmd, timeout=15)


def capture_fb0_png(filename: str) -> Path:
    """抓取板端 /dev/fb0 帧缓冲并按 270 度旋转配置还原为 1280x720 正向 PNG。"""
    remote_code = (
        "import sys, zlib; "
        "f = open('/dev/fb0', 'rb'); "
        "sys.stdout.buffer.write(zlib.compress(f.read(3686400), 1))"
    )
    comp = run_board_py(remote_code)
    raw = zlib.decompress(comp)
    if len(raw) != 3686400:
        raise RuntimeError(f"帧缓冲长度异常: {len(raw)}")
    out_path = EVIDENCE_DIR / filename
    img = Image.frombytes("RGBA", (720, 1280), raw, "raw", "BGRA").convert("RGB")
    upright = img.transpose(Image.Transpose.ROTATE_90)
    upright.save(out_path)
    print(f"[CAPTURE] {out_path.name} ({upright.size[0]}x{upright.size[1]})")
    return out_path


def tap_ui(ui_x: int, ui_y: int, settle_ms: int = 800) -> None:
    """在正向 1280x720 坐标 (ui_x, ui_y) 注入真实单点触摸点击事件。"""
    raw_x = max(0, min(719, 719 - ui_y))
    raw_y = max(0, min(1279, ui_x))
    remote_code = f"""
import struct, time
EV_SYN, EV_KEY, EV_ABS = 0x00, 0x01, 0x03
SYN_REPORT, BTN_TOUCH = 0x00, 0x14a
ABS_X, ABS_Y = 0x00, 0x01
ABS_MT_SLOT, ABS_MT_POS_X, ABS_MT_POS_Y, ABS_MT_TID = 0x2f, 0x35, 0x36, 0x39
def pkt(t, c, v):
    now = time.time()
    sec = int(now)
    usec = int((now - sec) * 1000000)
    return struct.pack('llHHi', sec, usec, t, c, v)
rx, ry = {raw_x}, {raw_y}
jx = rx - 1 if rx > 0 else rx + 1
jy = ry - 1 if ry > 0 else ry + 1
tid = int(time.time() * 1000) % 30000 + 1
with open('/dev/input/event0', 'wb', buffering=0) as fd:
    fd.write(b''.join([
        pkt(EV_ABS, ABS_MT_SLOT, 0),
        pkt(EV_ABS, ABS_MT_TID, tid),
        pkt(EV_ABS, ABS_MT_POS_X, jx), pkt(EV_ABS, ABS_MT_POS_Y, jy),
        pkt(EV_ABS, ABS_X, jx), pkt(EV_ABS, ABS_Y, jy),
        pkt(EV_KEY, BTN_TOUCH, 1),
        pkt(EV_SYN, SYN_REPORT, 0),
    ]))
    time.sleep(0.025)
    fd.write(b''.join([
        pkt(EV_ABS, ABS_MT_POS_X, rx), pkt(EV_ABS, ABS_MT_POS_Y, ry),
        pkt(EV_ABS, ABS_X, rx), pkt(EV_ABS, ABS_Y, ry),
        pkt(EV_SYN, SYN_REPORT, 0),
    ]))
    time.sleep(0.06)
    fd.write(b''.join([
        pkt(EV_ABS, ABS_MT_TID, -1),
        pkt(EV_KEY, BTN_TOUCH, 0),
        pkt(EV_SYN, SYN_REPORT, 0),
    ]))
time.sleep({settle_ms / 1000.0:.3f})
"""
    run_board_py(remote_code)
    print(f"[TAP] ui=({ui_x},{ui_y}) -> raw=({raw_x},{raw_y})")


def swipe_ui(start_xy: tuple[int, int], end_xy: tuple[int, int], steps: int = 12, settle_ms: int = 800) -> None:
    """在正向 1280x720 坐标系从 start_xy 平滑滑动至 end_xy（用于列表滚动或亮度滑块拖动）。"""
    sx, sy = start_xy
    ex, ey = end_xy
    remote_code = f"""
import struct, time
EV_SYN, EV_KEY, EV_ABS = 0x00, 0x01, 0x03
SYN_REPORT, BTN_TOUCH = 0x00, 0x14a
ABS_X, ABS_Y = 0x00, 0x01
ABS_MT_SLOT, ABS_MT_POS_X, ABS_MT_POS_Y, ABS_MT_TID = 0x2f, 0x35, 0x36, 0x39
def pkt(t, c, v):
    now = time.time()
    sec = int(now)
    usec = int((now - sec) * 1000000)
    return struct.pack('llHHi', sec, usec, t, c, v)
def to_raw(ux, uy):
    return max(0, min(719, 719 - uy)), max(0, min(1279, ux))
tid = int(time.time() * 1000) % 30000 + 1
n = max(2, {steps})
with open('/dev/input/event0', 'wb', buffering=0) as fd:
    rx0, ry0 = to_raw({sx}, {sy})
    fd.write(b''.join([
        pkt(EV_ABS, ABS_MT_SLOT, 0), pkt(EV_ABS, ABS_MT_TID, tid),
        pkt(EV_ABS, ABS_MT_POS_X, rx0), pkt(EV_ABS, ABS_MT_POS_Y, ry0),
        pkt(EV_ABS, ABS_X, rx0), pkt(EV_ABS, ABS_Y, ry0),
        pkt(EV_KEY, BTN_TOUCH, 1), pkt(EV_SYN, SYN_REPORT, 0),
    ]))
    time.sleep(0.03)
    for i in range(1, n + 1):
        ux = int(round({sx} + ({ex} - {sx}) * i / n))
        uy = int(round({sy} + ({ey} - {sy}) * i / n))
        rx, ry = to_raw(ux, uy)
        fd.write(b''.join([
            pkt(EV_ABS, ABS_MT_POS_X, rx), pkt(EV_ABS, ABS_MT_POS_Y, ry),
            pkt(EV_ABS, ABS_X, rx), pkt(EV_ABS, ABS_Y, ry),
            pkt(EV_SYN, SYN_REPORT, 0),
        ]))
        time.sleep(0.025)
    time.sleep(0.06)
    fd.write(b''.join([
        pkt(EV_ABS, ABS_MT_TID, -1), pkt(EV_KEY, BTN_TOUCH, 0),
        pkt(EV_SYN, SYN_REPORT, 0),
    ]))
time.sleep({settle_ms / 1000.0:.3f})
"""
    run_board_py(remote_code)
    print(f"[SWIPE] ui={start_xy} -> {end_xy} (steps={steps})")


def main() -> None:
    """命令行入口：支持 capture / tap / swipe 子命令。"""
    if len(sys.argv) < 2:
        raise SystemExit("用法: ux01_touch_fb_tool.py capture <png> | tap <x> <y> [png] | swipe <x1> <y1> <x2> <y2> [png]")
    act = sys.argv[1]
    if act == "capture":
        capture_fb0_png(sys.argv[2])
    elif act == "tap":
        tap_ui(int(sys.argv[2]), int(sys.argv[3]))
        if len(sys.argv) >= 5:
            capture_fb0_png(sys.argv[4])
    elif act == "swipe":
        swipe_ui((int(sys.argv[2]), int(sys.argv[3])), (int(sys.argv[4]), int(sys.argv[5])))
        if len(sys.argv) >= 7:
            capture_fb0_png(sys.argv[6])
    else:
        raise SystemExit(f"未知命令: {act}")


if __name__ == "__main__":
    main()
