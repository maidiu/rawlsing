"""Read-only access to the accepted shipped closure and projection adapter."""
from __future__ import annotations

import sys
from pathlib import Path

sys.dont_write_bytecode = True

RETURN = Path(__file__).resolve().parents[1]
WORKER_RETURNS = RETURN.parent
WORKSPACE = WORKER_RETURNS.parent
PACKAGE_RETURN = WORKER_RETURNS / "SOROK-20261105-S45-S47-PRODUCT-IMPORT-CLOSURE-R1"
PACKAGE_PRODUCT = PACKAGE_RETURN / "product"
PROJECTION_RETURN = WORKER_RETURNS / "SOROK-S45-S47-PROJECTION-20261105-R1"

_INSTALLED = False


def install() -> None:
    global _INSTALLED
    if _INSTALLED:
        return
    for path in (PROJECTION_RETURN, PACKAGE_PRODUCT):
        if not path.is_dir():
            raise RuntimeError("SOROK_P2_SHIPPING_UNIT_MISSING:" + str(path))
        text = str(path)
        if text in sys.path:
            sys.path.remove(text)
        sys.path.insert(0, text)
    from sorok_s45_s47.bootstrap import install as install_product

    install_product()
    import s45_projection.adapter  # noqa: F401

    _INSTALLED = True


def projection_class():
    install()
    from s45_projection.adapter import S45Projection

    return S45Projection


__all__ = [
    "PACKAGE_PRODUCT",
    "PACKAGE_RETURN",
    "PROJECTION_RETURN",
    "RETURN",
    "WORKER_RETURNS",
    "WORKSPACE",
    "install",
    "projection_class",
]
