"""Install the shipped S45-S47 closure and expose the P2 later-event callables."""
from __future__ import annotations

import os
import sys
from pathlib import Path

RETURN = Path(__file__).resolve().parents[1]
REPO = RETURN.parents[1]
BASE_ROOT = Path(os.environ.get("SOROK_P2_BASE_ROOT", str(REPO))).expanduser().resolve()
PRODUCT = BASE_ROOT / "WORKER_RETURNS/SOROK-20261105-S45-S47-PRODUCT-IMPORT-CLOSURE-R1/product"
PROJECTION = BASE_ROOT / "WORKER_RETURNS/SOROK-S45-S47-PROJECTION-20261105-R1"

_LOADED = False
_DEPS: dict | None = None


def load() -> dict:
    global _LOADED, _DEPS
    if _LOADED and _DEPS is not None:
        return _DEPS
    for path in (str(PROJECTION), str(PRODUCT)):
        if path in sys.path:
            sys.path.remove(path)
        sys.path.insert(0, path)

    from sorok_s45_s47.bootstrap import install as product_install

    product_install()

    from s37.harness import case_for, source_for
    from s45.fixtures import root_bundle
    from s45_projection.adapter import S45Projection
    from s46.errors import S46Refusal
    from s46.model import make_domain
    from s47.session import S47Session

    _LOADED = True
    _DEPS = {
        "return": RETURN,
        "repo": REPO,
        "base_root": BASE_ROOT,
        "product": PRODUCT,
        "projection": PROJECTION,
        "S47Session": S47Session,
        "S45Projection": S45Projection,
        "S46Refusal": S46Refusal,
        "make_domain": make_domain,
        "case_for": case_for,
        "source_for": source_for,
        "root_bundle": root_bundle,
    }
    return _DEPS


def roots() -> dict:
    return {
        "return": RETURN,
        "repo": REPO,
        "base_root": BASE_ROOT,
        "product": PRODUCT,
        "projection": PROJECTION,
        "product_source_manifest": PRODUCT.parent / "SOURCE_MANIFEST.json",
    }


__all__ = ["BASE_ROOT", "PRODUCT", "PROJECTION", "REPO", "RETURN", "load", "roots"]
