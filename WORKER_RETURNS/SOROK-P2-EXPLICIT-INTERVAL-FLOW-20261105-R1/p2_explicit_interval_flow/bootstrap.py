"""Locate and install the accepted S45-S47 product closure without editing it."""
from __future__ import annotations

import os
import sys
from pathlib import Path

RETURN = Path(__file__).resolve().parents[1]
REPO = RETURN.parents[1]
PRODUCT_RETURN = "SOROK-20261105-S45-S47-PRODUCT-IMPORT-CLOSURE-R1"
PROJECTION_RETURN = "SOROK-S45-S47-PROJECTION-20261105-R1"
PRODUCT_PACKAGE = "product/sorok_s45_s47"


def _valid_root(path: Path) -> bool:
    return (path / "WORKER_RETURNS" / PRODUCT_RETURN / PRODUCT_PACKAGE).is_dir()


def base_root(explicit: str | Path | None = None) -> Path:
    candidates = []
    if explicit:
        candidates.append(Path(explicit))
    if os.environ.get("SOROK_P2_BASE_ROOT"):
        candidates.append(Path(os.environ["SOROK_P2_BASE_ROOT"]))
    candidates.extend((
        REPO,
        REPO / ".local-logs" / "p2-explicit-interval-flow" / "base",
        RETURN.parents[1],
    ))
    for candidate in candidates:
        path = candidate.expanduser().resolve()
        if _valid_root(path):
            return path
        product = path / "WORKER_RETURNS" / PRODUCT_RETURN / "product"
        if (product / "sorok_s45_s47").is_dir():
            return path
    raise RuntimeError("SOROK_P2_BASE_ROOT_NOT_FOUND")


def paths(explicit: str | Path | None = None) -> dict:
    root = base_root(explicit)
    return {
        "base_root": root,
        "product_return": root / "WORKER_RETURNS" / PRODUCT_RETURN,
        "product": root / "WORKER_RETURNS" / PRODUCT_RETURN / "product",
        "projection_return": root / "WORKER_RETURNS" / PROJECTION_RETURN,
        "product_cli": (
            root / "WORKER_RETURNS" / PRODUCT_RETURN / "product" /
            "run_s45_s47.py"
        ),
    }


def install(explicit: str | Path | None = None) -> dict:
    info = paths(explicit)
    product = info["product"].resolve()
    projection = info["projection_return"].resolve()
    os.environ["SOROK_S45_S47_PACKAGE_ROOT"] = str(product)
    os.environ["SOROK_S45_S47_PROJECTION_ROOT"] = str(projection)
    for path in (product, projection):
        text = str(path)
        if text in sys.path:
            sys.path.remove(text)
        sys.path.insert(0, text)
    from sorok_s45_s47.bootstrap import install as product_install

    product_install()
    info["installed"] = True
    return info


__all__ = ["base_root", "install", "paths"]
