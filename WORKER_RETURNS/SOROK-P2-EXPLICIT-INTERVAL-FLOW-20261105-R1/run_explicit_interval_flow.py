#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

RETURN = Path(__file__).resolve().parent
if str(RETURN) not in sys.path:
    sys.path.insert(0, str(RETURN))

from p2_explicit_interval_flow.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
