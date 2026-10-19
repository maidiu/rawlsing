#!/usr/bin/env python3
import hashlib, json
from pathlib import Path
R = Path(__file__).resolve().parent.parent
files = []
for p in sorted(R.rglob("*")):
    if p.is_file() and "evidence/logs" not in p.as_posix() and p.name != "source_manifest.json":
        b = p.read_bytes()
        files.append({"path": str(p.relative_to(R)), "bytes": len(b),
                      "sha256": hashlib.sha256(b).hexdigest()})
(R / "source_manifest.json").write_text(json.dumps({
    "schema": "A41_RETURN_SOURCE_MANIFEST@1.0.0",
    "startup": "c4934fd71120d37a4d06f7c830891e6e97fe4ecf",
    "files": files}, indent=2) + "\n")
print("source manifest:", len(files), "files")
