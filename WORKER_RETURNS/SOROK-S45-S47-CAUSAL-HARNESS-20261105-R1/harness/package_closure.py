"""Install and audit the shipped S45-S47 product import closure."""
from __future__ import annotations

import sys
from pathlib import Path

from . import pins


def resolve_product(value: Path) -> Path:
    candidate = value.expanduser().resolve()
    if (candidate / "sorok_s45_s47").is_dir():
        return candidate
    if (candidate / "product" / "sorok_s45_s47").is_dir():
        return (candidate / "product").resolve()
    raise pins.HarnessError("PACKAGE_CLOSURE_NOT_FOUND:" + str(candidate))


def configure(value: Path, module_names: tuple[str, ...]) -> dict:
    product = resolve_product(value)
    text = str(product)
    if text in sys.path:
        sys.path.remove(text)
    sys.path.insert(0, text)
    from sorok_s45_s47.audit import verify_sources
    from sorok_s45_s47.bootstrap import install

    runtime_roots = install()
    source_audit = verify_sources()
    vendor = Path(runtime_roots["vendor"]).resolve()
    origins = pins.module_origins(vendor, module_names)
    modules_under_package = all(
        row["status"] == "IMPORTED" and row["under_stage"]
        for row in origins.values()
    )
    return {
        "schema": "SOROK_S45_S47_HARNESS_PACKAGE_CLOSURE@1",
        "product": str(product),
        "return_root": str(product.parent),
        "vendor": str(vendor),
        "source_manifest": str(product.parent / "SOURCE_MANIFEST.json"),
        "source_audit": source_audit,
        "runtime_roots": runtime_roots,
        "imports": origins,
        "modules_under_package": modules_under_package,
        "all_exact": bool(source_audit["ok"] and modules_under_package),
    }


__all__ = ["configure", "resolve_product"]
