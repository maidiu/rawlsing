"""EVIDENCE_MANIFEST — hash the return and pinned external identities."""
import hashlib, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C
root = C.OUT
rows = []
for f in sorted(root.rglob("*")):
    if f.is_file() and f.name != "EVIDENCE_MANIFEST.json":
        data = f.read_bytes()
        rows.append(dict(path=f.relative_to(root).as_posix(), bytes=len(data),
                         sha256=hashlib.sha256(data).hexdigest()))
q = json.loads((root/"QUALITY_CHECKS.json").read_text())
payload = dict(
    schema="R53_U53F_EVIDENCE_MANIFEST@1",
    sealed_startup=C.SEALED,
    sealed_commit_date=C.git("show","-s","--format=%cI",C.SEALED).strip(),
    branch=C.git("rev-parse","--abbrev-ref","HEAD").strip(),
    observed_head=C.git("rev-parse","HEAD").strip(),
    quality_all_pass=q["checks"]["all_pass"],
    upstream_refs=dict(
        B49="b5600da96358f8526471d635a1befa8daa3f098b",
        G50="d379bafe36b8d89da27ea5bf33614d33aca7f2d2",
        I51="9bbf9e0509411beb210331d28160324b005a784e",
        F43="100ae7832ddc2c5edb7abdbd7e2cb94b5f9e8733",
        J42="f53cb0d2bce52640268c844c398bbd8007d28edc",
        W41="b0a68e4ff5d5e2ca62b080376fda6b5f5431a6c2",
        E41="6e123bafe749d6997c764ae117fb5e68e0139ed7",
        P41="f27d1101048638bba395143a48efb7ef00bfcda4",
        STOP_blob="e2a04d6fc82bea95d0f88a14c7ebf38af6dd4f63"),
    files=rows)
(root/"EVIDENCE_MANIFEST.json").write_text(json.dumps(payload, indent=2, sort_keys=True)+"\n")
print("files:", len(rows), "quality:", q["checks"]["all_pass"])
