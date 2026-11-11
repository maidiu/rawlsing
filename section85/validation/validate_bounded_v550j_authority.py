#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


def hash_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def hash_tree(root: Path) -> dict[str, str]:
    return {str(path.relative_to(root)): hash_file(path) for path in sorted(root.rglob("*")) if path.is_file()}


def run_generator(script: Path, repo: Path, canary: Path, decisions: Path, output: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run([
        sys.executable, str(script),
        "--repo-root", str(repo),
        "--canary-root", str(canary),
        "--output-dir", str(output),
        "--adjudications-path", str(decisions),
    ], text=True, capture_output=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument("--section", type=Path, required=True)
    parser.add_argument("--canary-root", type=Path, required=True)
    args = parser.parse_args()

    repo = args.repo_root.resolve()
    section = args.section.resolve()
    canary = args.canary_root.resolve()
    script = section / "code" / "build_bounded_v550j_authority.py"
    decisions = section / "inputs" / "BOUNDED_JOINT_CONFIGURATION_ADJUDICATIONS.json"
    validation = section / "validation"
    validation.mkdir(parents=True, exist_ok=True)

    checks: list[dict[str, Any]] = []
    with tempfile.TemporaryDirectory(prefix="v550j_bounded_validation_") as temp:
        temp_root = Path(temp)
        run_a = temp_root / "run_a"
        run_b = temp_root / "run_b"
        a = run_generator(script, repo, canary, decisions, run_a)
        b = run_generator(script, repo, canary, decisions, run_b)
        deterministic = a.returncode == 0 and b.returncode == 0 and hash_tree(run_a) == hash_tree(run_b)
        checks.append({"check_id": "deterministic_double_generation", "expected": "PASS", "observed": "PASS" if deterministic else "FAIL", "detail": f"files_a={len(hash_tree(run_a)) if run_a.exists() else 0};files_b={len(hash_tree(run_b)) if run_b.exists() else 0}"})

        payload = json.loads(decisions.read_text(encoding="utf-8"))
        mutations = [
            ("missing_decision", lambda x: x["decisions"].pop(), "missing bounded joint-configuration adjudication"),
            ("stale_p3_parent", lambda x: x.update(p3_parent_authority_release_id="STALE"), "stale P3 parent release"),
            ("unaccepted_decision", lambda x: x["decisions"][0].update(decision_status="PENDING"), "adjudication is not accepted"),
            ("member_order_changed", lambda x: x["decisions"][0]["member_var_codes"].reverse(), "member order mismatch"),
            ("source_structure_changed", lambda x: x["decisions"][0].update(source_structure_id="WRONG"), "source_structure_id mismatch"),
        ]
        for index, (name, mutate, expected_text) in enumerate(mutations, start=1):
            mutated = json.loads(json.dumps(payload))
            mutate(mutated)
            mutation_path = temp_root / f"mutation_{index}.json"
            mutation_path.write_text(json.dumps(mutated, indent=2) + "\n", encoding="utf-8")
            result = run_generator(script, repo, canary, mutation_path, temp_root / f"mutation_{index}_out")
            combined = result.stdout + result.stderr
            passed = result.returncode != 0 and expected_text in combined
            checks.append({"check_id": name, "expected": "REJECT", "observed": "REJECT" if passed else "FAIL", "detail": combined[-800:].replace("\n", " ")})

    failed = [row for row in checks if row["observed"] == "FAIL"]
    result = {
        "status": "PASS_BOUNDED_V550J_AUTHORITY_VALIDATION" if not failed else "FAIL_BOUNDED_V550J_AUTHORITY_VALIDATION",
        "check_count": len(checks),
        "passed_check_count": len(checks) - len(failed),
        "failed_check_count": len(failed),
        "checks": checks,
    }
    (validation / "BOUNDED_V550J_AUTHORITY_VALIDATION_RETURN.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    with (validation / "BOUNDED_V550J_AUTHORITY_VALIDATION_MATRIX.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["check_id", "expected", "observed", "detail"], lineterminator="\n")
        writer.writeheader()
        writer.writerows(checks)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
