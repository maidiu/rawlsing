"""Source and module-path audit for the pinned product closure."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

from .bootstrap import PRODUCT, RETURN_ROOT, VENDOR, install


def manifest_path() -> Path:
    return RETURN_ROOT / "SOURCE_MANIFEST.json"


def verify_sources() -> dict:
    document = json.loads(manifest_path().read_text(encoding="utf8"))
    problems = []
    for row in document["files"]:
        path = RETURN_ROOT / row["installed_path"]
        if not path.is_file():
            problems.append("MISSING:" + row["installed_path"])
            continue
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if digest != row["sha256"]:
            problems.append("SHA256_MISMATCH:" + row["installed_path"])
    return {
        "schema": "SOROK_S45_S47_PRODUCT_SOURCE_AUDIT@1",
        "manifest": str(manifest_path()),
        "files": len(document["files"]),
        "problems": problems,
        "ok": not problems,
    }


def _stdlib(path: Path) -> bool:
    prefixes = {Path(sys.base_prefix).resolve(), Path(sys.prefix).resolve()}
    return any(path.is_relative_to(prefix) for prefix in prefixes)


def loaded_modules() -> dict:
    install()
    local_roots = (PRODUCT.resolve(), PRODUCT.parents[1].resolve())
    rows = []
    external = []
    for name, module in sorted(sys.modules.items()):
        raw = getattr(module, "__file__", None)
        if not raw or not str(raw).endswith(".py"):
            continue
        path = Path(raw).resolve()
        local = any(path.is_relative_to(root) for root in local_roots)
        stdlib = _stdlib(path)
        rows.append({
            "module": name,
            "path": str(path),
            "local": local,
            "stdlib": stdlib,
        })
        if not local and not stdlib:
            external.append({"module": name, "path": str(path)})
    return {
        "schema": "SOROK_S45_S47_PRODUCT_IMPORT_AUDIT@1",
        "local_roots": [str(root) for root in local_roots],
        "modules": len(rows),
        "local_modules": sum(1 for row in rows if row["local"]),
        "stdlib_modules": sum(1 for row in rows if row["stdlib"]),
        "external_modules": external,
        "ok": not external,
        "rows": rows,
    }
