from __future__ import annotations

import csv
import hashlib
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SECTION = ROOT / "53_P3A_V7_CONTRACT_BINDING_REPAIR_AND_PHASE3_RESUME"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    package_rows = list(csv.DictReader((ROOT / "PACKAGE_INDEX.csv").open(encoding="utf-8")))
    missing = []
    mismatches = []
    for row in package_rows:
        path = ROOT / row["relative_path"]
        if not path.exists():
            missing.append(row["relative_path"])
            continue
        size = path.stat().st_size
        digest = sha256(path)
        if size != int(row["bytes"]) or digest != row["sha256"]:
            mismatches.append(row["relative_path"])

    required = [
        SECTION / "TASK_RETURN.md",
        SECTION / "P3A_PHASE3_IMPLEMENTATION_REPORT.md",
        SECTION / "P3A_PHASE3_OBJECT_COUNTS.json",
        SECTION / "P3A_VERTICAL_SLICE_RETURN.json",
        SECTION / "outputs/p3a_contract_load_return_v31_1.json",
        SECTION / "outputs/p3a_contract_load_return_v31_2.json",
        SECTION / "outputs/p3a_vertical_slice_packet_build_stdout_v31.json",
    ]
    absent_required = [str(p.relative_to(ROOT)) for p in required if not p.exists()]

    validation = json.loads((ROOT / "VALIDATION.json").read_text(encoding="utf-8"))
    vertical = json.loads((SECTION / "P3A_VERTICAL_SLICE_RETURN.json").read_text(encoding="utf-8"))
    object_counts = json.loads((SECTION / "P3A_PHASE3_OBJECT_COUNTS.json").read_text(encoding="utf-8"))

    failures = []
    if validation.get("status") != "PASS":
        failures.append("root VALIDATION status is not PASS")
    if vertical.get("status") != "PASS" or vertical.get("packet_count") != 3:
        failures.append("vertical slice return is not three PASS packets")
    if object_counts["counts"].get("categorical_bindings") != 67:
        failures.append("categorical binding count is not 67")
    if object_counts["counts"].get("object_reference_contracts") != 40:
        failures.append("object reference count is not 40")
    if object_counts["counts"].get("lineage_membership_rows") != 18276:
        failures.append("membership row count is not 18276")
    if missing:
        failures.append(f"manifest missing paths: {len(missing)}")
    if mismatches:
        failures.append(f"manifest mismatches: {len(mismatches)}")
    if absent_required:
        failures.append(f"required section files absent: {absent_required}")

    result = {
        "status": "PASS" if not failures else "FAIL",
        "manifest_rows": len(package_rows),
        "missing": missing,
        "mismatches": mismatches,
        "failures": failures,
    }
    print(json.dumps(result, indent=2))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
