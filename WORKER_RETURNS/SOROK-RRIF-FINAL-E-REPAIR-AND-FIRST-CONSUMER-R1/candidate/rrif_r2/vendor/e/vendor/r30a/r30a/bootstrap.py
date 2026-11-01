"""Import closure for the R30A product over the immutable R29P code."""
from __future__ import annotations

import sys
from pathlib import Path

RETURN = Path(__file__).resolve().parents[1]
REPO = next(p for p in RETURN.parents if (p / ".git").exists())
VENDOR = RETURN / "vendor" / "r29p"

PATHS = [
    REPO,
    VENDOR,
    VENDOR / "candidate",
    VENDOR / "candidate" / "vendor" / "bp2",
    VENDOR / "candidate" / "vendor" / "bp4",
    VENDOR / "r26e",
]


def install() -> None:
    for path in reversed([str(p) for p in PATHS]):
        if path in sys.path:
            sys.path.remove(path)
        sys.path.insert(0, path)
    import bp2p4.bootstrap as joined_bootstrap

    joined_bootstrap.install()


def origins() -> dict:
    rows = {}
    for name in ("r29p.product", "r29p.runner", "bp2p4.product", "bp4.product",
                 "bp4.perception", "r26e.c12_integrity",
                 "rawlsing_next.m6_actor_safe_expression"):
        module = sys.modules.get(name)
        path = getattr(module, "__file__", "")
        rows[name] = str(Path(path).resolve()) if path else ""
    return rows
