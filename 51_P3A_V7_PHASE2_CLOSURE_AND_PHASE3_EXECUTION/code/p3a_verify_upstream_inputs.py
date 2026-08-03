from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def csv_row_count(path: Path) -> int:
    with path.open(encoding="utf-8", newline="") as handle:
        return sum(1 for _ in csv.DictReader(handle))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    root = Path(args.root)
    manifest = (
        root
        / "49_P3_PLAN_SIXTH_EXECUTABLE_CLOSURE_AUDIT_AND_LOCK/upstream/P3_UPSTREAM_INPUT_MANIFEST_v7.csv"
    )
    rows = list(csv.DictReader(manifest.open(encoding="utf-8", newline="")))
    results = []
    for row in rows:
        path = root / row["relative_path"]
        exists = path.exists()
        actual_sha = sha256(path) if exists else None
        actual_rows = csv_row_count(path) if exists and path.suffix == ".csv" else None
        results.append(
            {
                "input_code": row["input_code"],
                "relative_path": row["relative_path"],
                "required": row["required"],
                "exists": exists,
                "expected_sha256": row["sha256"],
                "actual_sha256": actual_sha,
                "sha256_match": exists and actual_sha == row["sha256"],
                "expected_rows": int(row["expected_rows"]),
                "actual_rows": actual_rows,
                "row_count_match": actual_rows == int(row["expected_rows"]),
            }
        )
    status = "PASS" if all(r["exists"] and r["sha256_match"] and r["row_count_match"] for r in results) else "FAIL"
    output = {
        "status": status,
        "manifest": "49_P3_PLAN_SIXTH_EXECUTABLE_CLOSURE_AUDIT_AND_LOCK/upstream/P3_UPSTREAM_INPUT_MANIFEST_v7.csv",
        "required_inputs": len(results),
        "results": results,
    }
    Path(args.output).write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(output, indent=2))
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
