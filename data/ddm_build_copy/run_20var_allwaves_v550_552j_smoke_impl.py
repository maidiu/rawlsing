#!/usr/bin/env python3
"""Compatibility import for the governed W05-B smoke implementation.

Identity and orchestration authority live only in
``run_20var_allwaves_v550_552j_smoke``.  This module intentionally contains no
source/wave aliases, normalization tables, compiler selection, or independent
``main`` implementation.
"""
from __future__ import annotations

from data.ddm_build_copy.run_20var_allwaves_v550_552j_smoke import *  # noqa: F401,F403
from data.ddm_build_copy.run_20var_allwaves_v550_552j_smoke import main

if __name__ == "__main__":
    raise SystemExit(main())
