from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EXCLUDE_DIRS = {".venv", ".local-data", "__pycache__"}
files = []
for path in sorted(ROOT.rglob("*")):
    if not path.is_file():
        continue
    relative = path.relative_to(ROOT)
    if any(part in EXCLUDE_DIRS for part in relative.parts):
        continue
    if relative.name == "MANIFEST.json":
        continue
    files.append({
        "path": relative.as_posix(),
        "bytes": path.stat().st_size,
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
    })
representative = [
    row for row in files if row["path"].startswith("evidence/representative-estate/")
]
document = {
    "schema": "PYAT1006_RETURN_MANIFEST@1",
    "base_production_head": "9d96a9cac7d10f59f2c30d8045dd1696fa3ab969",
    "return_dir": "WORKER_RETURNS/PYAT1006_PHYSICAL_ECONOMICS_R1",
    "file_count": len(files),
    "total_bytes": sum(row["bytes"] for row in files),
    "files": files,
    "representative_estate_file_count": len(representative),
    "representative_estate_bytes": sum(row["bytes"] for row in representative),
    "excluded": [".venv (task-local, uncommitted)", ".local-data (large scratch, uncommitted)", "__pycache__"],
}
(ROOT / "MANIFEST.json").write_text(
    json.dumps(document, indent=2, sort_keys=True) + "\n", encoding="utf-8"
)
print(json.dumps({
    "file_count": document["file_count"],
    "total_bytes": document["total_bytes"],
    "representative_file_count": document["representative_estate_file_count"],
    "representative_bytes": document["representative_estate_bytes"],
}, indent=2, sort_keys=True))
