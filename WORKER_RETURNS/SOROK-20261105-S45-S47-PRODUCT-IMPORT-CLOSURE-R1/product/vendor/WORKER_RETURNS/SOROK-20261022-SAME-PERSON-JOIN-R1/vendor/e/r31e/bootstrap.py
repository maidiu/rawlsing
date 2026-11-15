"""Import closure for R31E over the immutable R30A/R29P code."""
from __future__ import annotations

import sys
from pathlib import Path

RETURN = Path(__file__).resolve().parents[1]
REPO = next(p for p in RETURN.parents if (p / ".git").exists())
R30A_ROOT = RETURN / "vendor" / "r30a"


def install() -> None:
    path = str(R30A_ROOT)
    if path in sys.path:
        sys.path.remove(path)
    sys.path.insert(0, path)
    import r30a.bootstrap as r30a_bootstrap

    r30a_bootstrap.install()
