#!/usr/bin/env python3
"""CLI module entrypoint supporting `python3 -m tools.coord_runner --once`."""

import sys

from .runner import main

if __name__ == "__main__":
    sys.exit(main())
