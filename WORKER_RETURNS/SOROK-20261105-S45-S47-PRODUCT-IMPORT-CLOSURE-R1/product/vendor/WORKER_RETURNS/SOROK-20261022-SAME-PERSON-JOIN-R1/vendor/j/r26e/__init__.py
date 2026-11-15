"""R26E owned derivative: qualified C12 custody + N1 method on the live product.

The pinned BP2P4J/BP4/N1 sources are imported from read-only staged copies; no
original file is edited. This package supplies only the corrected C12 verifier,
the TEST_ONLY external witness, the live product adapter and the N1 bridge.
"""
from __future__ import annotations

import sys
from pathlib import Path

RET = Path(__file__).resolve().parents[1]
TARGET = RET / "runtime" / "target"
N1 = RET / "runtime" / "n1" / "source"
for _path in (str(TARGET), str(N1)):
    if _path not in sys.path:
        sys.path.insert(0, _path)

import bp2p4  # noqa: E402

bp2p4.install()

__all__ = ["RET", "TARGET", "N1"]
