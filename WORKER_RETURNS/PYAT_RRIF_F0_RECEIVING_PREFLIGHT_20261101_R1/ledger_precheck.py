#!/usr/bin/env python3
"""Documentary precheck of the existing 34-lineage RRIF terminal ledger.

This does NOT perform a new historical census.  It reads the already-existing
RRIF-C validator/accounting/lineage files and the HQ 34/30 ledger files from
exact Git refs, then checks the documentary counts, source pointers, negative
wakes and R157/C5 scope corrections that the ledger already records.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


LEDGER_PATH = "PYAT_CONTROL_ROOM/BRANCH_RECOVERY_R1/HQ_D1_D5_INTAKE_R1/03_THIRTY_FOUR_GROUP_TERMINAL_CANDIDATES.jsonl"
INTAKE_PATH = "PYAT_CONTROL_ROOM/BRANCH_RECOVERY_R1/HQ_D1_D5_INTAKE_R1/01_THIRTY_LINEAGE_HQ_INTAKE.jsonl"
RRIFC_DIR = "WORKER_RETURNS/RRIF-C-POST-GAP-LINEAGE-REDUCTION-20261031-R1"


def git_show(repo: str, ref: str, path: str) -> str:
    completed = subprocess.run(
        ["git", "-C", repo, "show", f"{ref}:{path}"],
        capture_output=True, text=True, check=False,
    )
    if completed.returncode != 0:
        raise SystemExit(f"cannot read {ref}:{path}: {completed.stderr.strip()}")
    return completed.stdout


def jsonl(text: str) -> list[dict[str, Any]]:
    return [json.loads(line) for line in text.splitlines() if line.strip()]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True)
    parser.add_argument("--ledger-ref", default="d80901e9de78803c031fa9d25146f7d8b6aeba2c")
    parser.add_argument("--rrifc-ref", default="b75addf621c3a6c1a3b196bd92a810fad77ae3ae")
    args = parser.parse_args(argv)

    ledger = jsonl(git_show(args.repo, args.ledger_ref, LEDGER_PATH))
    intake = jsonl(git_show(args.repo, args.ledger_ref, INTAKE_PATH))
    validator = json.loads(git_show(args.repo, args.rrifc_ref, f"{RRIFC_DIR}/DENOMINATOR_AND_DEDUP_VALIDATION.json"))
    accounted = jsonl(git_show(args.repo, args.rrifc_ref, f"{RRIFC_DIR}/ACCOUNTED_FOR_CODE_BRANCHES.jsonl"))
    lineages = jsonl(git_show(args.repo, args.rrifc_ref, f"{RRIFC_DIR}/UNIQUE_IMPLEMENTATION_LINEAGES.jsonl"))

    failures: list[str] = []
    warnings: list[str] = []

    def check(condition: bool, message: str) -> None:
        if not condition:
            failures.append(message)

    ledger_ids = [row.get("id") for row in ledger]
    check(len(ledger) == 34, f"ledger rows {len(ledger)} != 34")
    check(len(set(ledger_ids)) == 34, "ledger ids are not 34 unique")
    check(sum(row.get("branch_identity_count", 0) for row in ledger) == 321,
          "ledger branch_identity_count sum is not 321")
    check(sum(row.get("code_introducing_branches", 0) for row in ledger) == 155,
          "ledger code_introducing_branches sum is not 155")

    intake_ids = [row.get("lineage_id") for row in intake]
    check(len(intake) == 30, f"intake rows {len(intake)} != 30")
    check(len(set(intake_ids)) == 30, "intake ids are not 30 unique")
    check(set(intake_ids) <= set(ledger_ids), "intake contains ids absent from the 34 ledger")

    check(len(accounted) == 321, f"RRIF-C accounted rows {len(accounted)} != 321")
    accounted_names = [row.get("branch") for row in accounted]
    check(len(set(accounted_names)) == 321, "RRIF-C accounted branch names not unique")
    check(sum(1 for row in accounted if row.get("accounting_role") == "CODE_INTRODUCING") == 155,
          "RRIF-C CODE_INTRODUCING count is not 155")
    check(len(lineages) == 34, f"RRIF-C lineage rows {len(lineages)} != 34")
    check(len({row.get("lineage_id") for row in lineages}) == 34,
          "RRIF-C lineage ids are not 34 unique")

    required_counts = {
        "frozen_branch_names": 845,
        "distinct_frozen_tips": 838,
        "code_delta_branches": 321,
        "accounted_code_branches": 321,
        "unique_lineage_rows": 34,
        "code_introducing_branches": 155,
        "original_function_ids": 3135,
        "original_families": 1885,
    }
    for key, expected in required_counts.items():
        check(validator.get("counts", {}).get(key) == expected,
              f"original validator count {key} != {expected}")
    check(all(validator.get("checks", {}).values()), "original validator checks are not all true")
    check(len(validator.get("mutation_tests", [])) == 9, "original validator mutation tests != 9")
    check(all(item.get("result") == "PASS_REJECTED" for item in validator.get("mutation_tests", [])),
          "original validator mutation test was not PASS_REJECTED")

    for row in ledger:
        row_id = row.get("id")
        check(row.get("schema") == "PYAT_RRIF_TERMINAL_ACCOUNTING_CANDIDATE@1",
              f"{row_id}: wrong schema")
        check(row.get("original_RRIF_C_source_cut") == args.rrifc_ref,
              f"{row_id}: wrong original RRIF-C source cut")
        check(bool(row.get("negative_owner_wake")), f"{row_id}: missing negative owner wake")
        check(row.get("receiving_cas") == "NOT_ADOPTED", f"{row_id}: receiving_cas not NOT_ADOPTED")
        check(row.get("authority") == "NOT_ISSUED_BY_RRIF", f"{row_id}: authority issued")
        check(row.get("scientific") == "ORIGINAL_NATIVE_OR_QUALIFIED_SCIENCE_NOT_ISSUED_BY_THIS_LEDGER",
              f"{row_id}: scientific scope not held")
        check(row.get("engineering") == "EVIDENCE_ACCOUNTED__ONLY_SPECIFIC_SOURCEFREE_SCOPES_POSSIBLE",
              f"{row_id}: engineering scope changed unexpectedly")

    by_id = {row["id"]: row for row in ledger}

    r157 = by_id.get("LIN-R157_SOURCE_CONFIGURATION", {})
    check(r157.get("terminal_candidate_status") == "HISTORICAL_RECOVERABLE_NOT_CURRENT__NO_AUTO_REIMPORT",
          "R157 terminal status is not historical-recoverable/no-auto-reimport")
    r157_scope = r157.get("scope_correction", "")
    for token in ("119", "19", "34", "32", "zero same-path PREMAIN"):
        check(token in r157_scope, f"R157 scope correction missing token {token!r}")
    check("reopen from d81bc2c67" in r157.get("negative_owner_wake", ""),
          "R157 restart/source pointer missing")
    check(r157.get("first_consumer", {}).get("kind") == "ENTRYPOINT_ONLY",
          "R157 first consumer is not entrypoint-only")
    check(r157.get("first_consumer", {}).get("path") == "rawlsing_next/source_configuration/cli.py",
          "R157 entrypoint path changed")

    c5 = by_id.get("LIN-C5_N5_STRUCTURAL_CONTEXT", {})
    check(c5.get("terminal_candidate_status") == "ONE_GT2_CASE_RECONSTITUTED__WRAPPER_API_NOT_PROVED",
          "C5 terminal status is not single-case/wrapper-unproved")
    c5_scope = c5.get("scope_correction", "")
    for token in ("19,210", "19,211", "not general zero-arg service"):
        check(token in c5_scope, f"C5 scope correction missing token {token!r}")
    check("Do not re-import the wrapper" in c5.get("negative_owner_wake", ""),
          "C5 negative owner wake missing")
    check("named receiver" in c5.get("negative_owner_wake", ""),
          "C5 restart/consumer pointer missing")
    check(c5.get("first_consumer") is None, "C5 first_consumer should be null")

    c3 = by_id.get("LIN-C3_PHYSICAL_DECODER_R5_G01", {})
    if c3.get("terminal_candidate_status") != "E4F_CORRECTED_REVIEW_PENDING":
        warnings.append("C3 ledger row predates E4/E4F; exact review/CAS must update it, not infer acceptance")
    if "G01" in c3.get("scope_correction", "") and "red" in c3.get("scope_correction", ""):
        pass
    else:
        warnings.append("C3 G01 pre-existing RED pointer not explicit in scope_correction")

    learned = by_id.get("LIN-LEARNED_WORLD_PRODUCT", {})
    check(learned.get("terminal_candidate_status") == "E5_PATCH_COMPLETE__E6_DISTINCT_REVIEW_PENDING",
          "E5 ledger row is not E6-review-pending")
    check("179 pass/14 fail" in learned.get("scope_correction", ""),
          "E5 ledger row does not preserve the unfiltered 179/14 result")

    result = {
        "schema": "PYAT_RRIF_F0_LEDGER_PRECHECK@1.0.0",
        "ledger_ref": args.ledger_ref,
        "rrifc_ref": args.rrifc_ref,
        "documentary_checks_pass": not failures,
        "counts": {
            "ledger_rows": len(ledger),
            "ledger_unique_ids": len(set(ledger_ids)),
            "branch_identity_sum": sum(row.get("branch_identity_count", 0) for row in ledger),
            "code_introducing_sum": sum(row.get("code_introducing_branches", 0) for row in ledger),
            "intake_rows": len(intake),
            "rrifc_accounted_rows": len(accounted),
            "rrifc_lineage_rows": len(lineages),
        },
        "original_validator_counts": validator.get("counts"),
        "original_validator_scope": "README_RRIF_C_SOURCE_CUT_ONLY__NO_NEW_CENSUS",
        "terminal_decision": "PENDING_REVIEW_CAS",
        "failures": failures,
        "warnings": warnings,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
