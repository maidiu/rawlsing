#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import subprocess
import sys
import tempfile
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--handoff-zip", required=True)
    parser.add_argument("--section-root", default=str(Path(__file__).resolve().parents[1]))
    args = parser.parse_args()
    root = Path(args.section_root).resolve()
    script = root / "code/run_layer1_35wave_contract_audit.py"

    checks = []
    compile_proc = subprocess.run([sys.executable, "-m", "py_compile", str(script)], capture_output=True, text=True)
    checks.append({"check": "py_compile", "passed": compile_proc.returncode == 0, "detail": compile_proc.stderr[-2000:]})

    test_proc = subprocess.run([sys.executable, "-m", "pytest", "-q", str(root / "tests/test_layer1_35wave_contract_audit.py")], capture_output=True, text=True)
    checks.append({"check": "pytest", "passed": test_proc.returncode == 0, "detail": (test_proc.stdout + test_proc.stderr)[-2000:]})

    with tempfile.TemporaryDirectory(prefix="rawlsing_layer1_validate_") as td:
        out = Path(td) / "out"
        plan_proc = subprocess.run([
            sys.executable, str(script),
            "--handoff-zip", str(Path(args.handoff_zip).resolve()),
            "--output-root", str(out),
        ], capture_output=True, text=True)
        status_path = out / "reports/LAYER1_STATUS.json"
        scope_path = out / "reports/AUDIT_SCOPE_MATRIX.csv"
        selection_path = out / "reports/AUDIT_VARIABLE_SELECTION.csv"
        plan_path = out / "reports/LAYER1_RUN_PLAN.json"
        status = json.loads(status_path.read_text()) if status_path.exists() else {}
        scopes = list(csv.DictReader(scope_path.open(encoding="utf-8"))) if scope_path.exists() else []
        selections = list(csv.DictReader(selection_path.open(encoding="utf-8"))) if selection_path.exists() else []
        plan = json.loads(plan_path.read_text()) if plan_path.exists() else {}
        scope_keys = [(r.get("source_family"), r.get("wave")) for r in scopes]
        expected_unique = len(scope_keys) == len(set(scope_keys)) == 35
        counts_valid = all(20 <= int(r.get("selected_variable_count", 0)) <= 50 for r in scopes)
        selected_keys = [(r.get("source_family"), r.get("wave"), r.get("source_variable_code")) for r in selections]
        selection_unique = len(selected_keys) == len(set(selected_keys))
        plan_passed = (
            plan_proc.returncode == 0
            and status.get("status") == "PLAN_COMPLETE_NOT_EXECUTED"
            and status.get("scope_count") == 35
            and plan.get("scope_count") == 35
            and expected_unique
            and counts_valid
            and selection_unique
        )
        checks.append({
            "check": "real_35wave_plan",
            "passed": plan_passed,
            "detail": {
                "returncode": plan_proc.returncode,
                "scope_count": len(scopes),
                "selection_rows": len(selections),
                "unique_scopes": expected_unique,
                "counts_valid": counts_valid,
                "selection_unique": selection_unique,
                "stderr_tail": plan_proc.stderr[-1000:],
            },
        })

    result = {
        "status": "PASS" if all(c["passed"] for c in checks) else "FAIL",
        "checks": checks,
    }
    output = root / "validation/LAYER1_PROGRAM_VALIDATION_RETURN.json"
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
