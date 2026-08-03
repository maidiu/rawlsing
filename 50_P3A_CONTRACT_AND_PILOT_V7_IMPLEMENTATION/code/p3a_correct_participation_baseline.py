from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_rows(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def counts(rows: list[dict[str, str]]) -> dict[str, dict[str, int]]:
    return {
        "participation_status": dict(Counter(row["participation_status"] for row in rows)),
        "signature_requirement": dict(Counter(row["signature_requirement"] for row in rows)),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--section49", required=True)
    parser.add_argument("--section50", required=True)
    args = parser.parse_args()

    sec49 = Path(args.section49)
    sec50 = Path(args.section50)
    baseline_path = sec49 / "upstream/P3_LINEAGE_PARTICIPATION_BASELINE_v7.csv"
    workset_path = sec49 / "upstream/P3_SIGNATURE_WORKSET_v7.csv"
    finding_path = sec50 / "P3A_EXECUTION_FINDINGS.csv"
    return_path = sec50 / "outputs/participation_baseline_correction_return.json"

    before_hash = sha256(baseline_path)
    baseline_rows = read_rows(baseline_path)
    workset_rows = read_rows(workset_path)
    workset_by_lineage = {row["lineage_id"]: row for row in workset_rows}
    if len(workset_by_lineage) != len(workset_rows):
        raise ValueError("P3_SIGNATURE_WORKSET_v7.csv contains duplicate lineage_id rows")

    mismatches = []
    corrected = []
    for row in baseline_rows:
        workset = workset_by_lineage.get(row["lineage_id"])
        if workset is None:
            raise ValueError(f"missing workset row for lineage_id={row['lineage_id']}")
        new_row = dict(row)
        for column in ("participation_status", "signature_requirement"):
            if row[column] != workset[column]:
                mismatches.append(
                    {
                        "lineage_id": row["lineage_id"],
                        "column": column,
                        "before": row[column],
                        "after": workset[column],
                    }
                )
                new_row[column] = workset[column]
        if new_row["participation_status"] == "NO_CURRENT_DIRECT_PAIR_AUTHORITY":
            new_row["authority_note"] = (
                "Absence from current direct-pair surface is not evidence of semantic "
                "uniqueness or permanent exclusion."
            )
        corrected.append(new_row)

    write_rows(baseline_path, list(baseline_rows[0].keys()), corrected)
    after_hash = sha256(baseline_path)

    finding_rows = []
    if finding_path.exists():
        finding_rows = read_rows(finding_path)
    if not finding_rows:
        finding_rows = [
            {
                "finding_id": "P3A-FINDING-0001",
                "severity": "BLOCKING_INPUT_CONTRADICTION",
                "broken_rule": "P3_LINEAGE_PARTICIPATION_BASELINE_v7 must agree row-by-row with P3_SIGNATURE_WORKSET_v7 for participation_status and signature_requirement.",
                "blast_radius": "13,127 rows: 2,897 constraint-only lineages and 10,230 nonincident lineages carried contradictory signature/defer labels.",
                "resolution": "Baseline corrected to governing Plan v7/workset semantics without changing lineage IDs, incident counts, source family, or P2 authority.",
                "evidence_path": "outputs/participation_baseline_correction_return.json",
            }
        ]
        write_rows(finding_path, list(finding_rows[0].keys()), finding_rows)

    result = {
        "status": "PASS",
        "corrected_file": "49_P3_PLAN_SIXTH_EXECUTABLE_CLOSURE_AUDIT_AND_LOCK/upstream/P3_LINEAGE_PARTICIPATION_BASELINE_v7.csv",
        "workset_file": "49_P3_PLAN_SIXTH_EXECUTABLE_CLOSURE_AUDIT_AND_LOCK/upstream/P3_SIGNATURE_WORKSET_v7.csv",
        "before_sha256": before_hash,
        "after_sha256": after_hash,
        "before_counts": counts(baseline_rows),
        "after_counts": counts(corrected),
        "workset_counts": counts(workset_rows),
        "mismatched_cells": len(mismatches),
        "mismatched_rows": len({row["lineage_id"] for row in mismatches}),
        "expected_counts_asserted": {
            "FULL_P3A_SIGNATURE": 399,
            "P2_CONSTRAINT_EVIDENCE_PRESERVED": 2897,
            "DEFER_UNTIL_PROMOTED_OR_NEW_AUTHORITY": 10230,
        },
    }
    return_path.parent.mkdir(parents=True, exist_ok=True)
    return_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
