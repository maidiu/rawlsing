from __future__ import annotations

import csv, hashlib, json, sys
from pathlib import Path

CONTROL = {"PACKAGE_INDEX.csv", "SHA256SUMS.csv", "VALIDATION.json"}

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def main() -> int:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[2]
    manifest = root / "PACKAGE_INDEX.csv"
    rows = list(csv.DictReader(manifest.open(newline="", encoding="utf-8")))
    expected = {r["relative_path"]: r for r in rows}
    actual = {}
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        rel = p.relative_to(root).as_posix()
        if rel in CONTROL or p.name == ".DS_Store" or "/.DS_Store" in rel:
            continue
        actual[rel] = p
    missing = sorted(set(expected) - set(actual))
    unexpected = sorted(set(actual) - set(expected))
    mismatches = []
    for rel, row in expected.items():
        p = actual.get(rel)
        if not p:
            continue
        if str(p.stat().st_size) != row["bytes"] or sha256(p) != row["sha256"]:
            mismatches.append(rel)
    validation = json.loads((root / "VALIDATION.json").read_text())
    sec = root / "54_P3A_V7_POPULATED_OBJECT_CLOSURE_REPAIR_AND_PILOT"
    closure = json.loads((sec / "P3A_V32_CLOSURE_RECONCILIATION.json").read_text())
    query = json.loads((sec / "outputs/v32_populated_validation_matrix_summary.json").read_text())
    ok = not missing and not unexpected and not mismatches and validation["handoff_version"] == "v32" and closure["status"] == "PASS" and query["failures"] == ["q01b_postpromotion_pointer", "q15b_no_unadjudicated_at_p3_close"]
    result = {"status": "PASS" if ok else "FAIL", "manifested_payload_files": len(expected), "actual_payload_files": len(actual), "missing": missing, "unexpected": unexpected, "mismatches": mismatches, "validation_status": validation.get("status"), "query_failures": query.get("failures")}
    print(json.dumps(result, indent=2))
    return 0 if ok else 1

if __name__ == "__main__":
    raise SystemExit(main())
