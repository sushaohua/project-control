#!/usr/bin/env python3
"""COORD 运行器命令行模块入口（支持 `python3 -m tools.coord_runner --once` 调用）。"""

import sys

from .runner import main

if __name__ == "__main__":
    sys.exit(main())
