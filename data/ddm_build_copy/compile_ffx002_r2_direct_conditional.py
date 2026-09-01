#!/usr/bin/env python3
"""Executable entrypoint for FFX002-R2 Core-C direct conditional redistribution."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from data.ddm_build_copy.ddm_ffx002_r2_direct_conditional import main

if __name__ == "__main__":
    raise SystemExit(main())
