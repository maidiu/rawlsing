"""Locate and install the shipped S45-S47 product import closure."""
from __future__ import annotations

import os
import sys
from pathlib import Path

PACKAGE_RETURN = "SOROK-20261105-S45-S47-PRODUCT-IMPORT-CLOSURE-R1"
WORKER_RETURNS = Path(__file__).resolve().parents[2]


def package_product() -> Path | None:
    candidates = []
    override = os.environ.get("SOROK_S45_S47_PACKAGE_ROOT")
    if override:
        candidates.append(Path(override).expanduser())
    candidates.append(WORKER_RETURNS / PACKAGE_RETURN / "product")
    candidates.append(WORKER_RETURNS / PACKAGE_RETURN)
    for candidate in candidates:
        resolved = candidate.resolve()
        if (resolved / "sorok_s45_s47").is_dir():
            return resolved
        if (resolved / "product" / "sorok_s45_s47").is_dir():
            return (resolved / "product").resolve()
    return None


def install_package_closure() -> dict | None:
    product = package_product()
    if product is None:
        return None
    text = str(product)
    if text in sys.path:
        sys.path.remove(text)
    sys.path.insert(0, text)
    from sorok_s45_s47.bootstrap import install, roots

    info = install()
    info["package_product"] = str(product)
    info["package_return"] = str(product.parent)
    info["runtime_roots"] = roots()
    return info


__all__ = [
    "PACKAGE_RETURN",
    "WORKER_RETURNS",
    "install_package_closure",
    "package_product",
]
