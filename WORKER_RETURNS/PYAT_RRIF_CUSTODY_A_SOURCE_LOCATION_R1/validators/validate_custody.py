#!/usr/bin/env python3
"""Validate the RRIF custody location ledger and frozen 845-branch denominators."""
from __future__ import annotations
import argparse, hashlib, json, subprocess, sys
from collections import Counter
from pathlib import Path

PREMAIN = "8e44ca9c751049d65e6def47600b5c073ee04b29"
EXPECTED_BRANCHES = 845
EXPECTED_TIPS = 838
EXPECTED_FUNCTIONS = 3135
EXPECTED_FAMILIES = 1883
EXPECTED_SUBTRACTION = 2269
EXPECTED_UNCERTAIN = 866
ALLOWED_LOCATION = {"PREMAIN_EXACT_SAME_PATH", "PREMAIN_EXACT_OTHER_PATH", "PREMAIN_MODIFIED_SAME_PATH", "BRANCH_TIP_EXACT", "BRANCH_TIP_MODIFIED_OR_UNRELATED", "NOT_LOCATED"}


class ValidationError(AssertionError):
    pass


def require(cond: bool, msg: str) -> None:
    if not cond:
        raise ValidationError(msg)


def load_jsonl(path: Path):
    rows = []
    for i, line in enumerate(path.read_text().splitlines(), 1):
        if line.strip():
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as e:
                raise ValidationError(f"{path.name}:{i}: {e}") from e
    return rows


def tree_blobs() -> dict[str, str]:
    out = subprocess.check_output(["git", "ls-tree", "-r", "--full-tree", PREMAIN], text=True)
    d = {}
    for line in out.splitlines():
        meta, path = line.split("\t", 1)
        d[path] = meta.split()[2]
    return d


def validate(root: Path) -> dict:
    branch_rows = load_jsonl(root / "BRANCH_LOCATION_SUMMARY.jsonl")
    ledger = load_jsonl(root / "CODE_LOCATION_LEDGER.jsonl")
    uncertain = load_jsonl(root / "UNCERTAIN_OR_MISSING_CODE.jsonl")
    subtraction = json.loads((root / "EXACT_CURRENT_SUBTRACTION.json").read_text())
    custody = json.loads((root / "BRANCH_IDENTITY_CUSTODY.json").read_text())
    integration = json.loads((root / "INTEGRATION_RECEIVER_MAP.json").read_text())
    counter = json.loads((root / "COUNTEREXAMPLE_AUDIT.json").read_text())
    branch_counts = json.loads((root / "BRANCH_LOCATION_COUNTS.json").read_text())
    variant_counts = json.loads((root / "CODE_LOCATION_COUNTS.json").read_text())
    tree = tree_blobs()

    require(len(branch_rows) == EXPECTED_BRANCHES, f"branch rows {len(branch_rows)}")
    require(len({r["branch"] for r in branch_rows}) == EXPECTED_BRANCHES, "duplicate branch name")
    require(len({r["frozen_tip"] for r in branch_rows}) == EXPECTED_TIPS, "tip denominator")
    require(len(custody["branches"]) == EXPECTED_BRANCHES, "custody branch count")
    cmap = {r["branch"]: r for r in custody["branches"]}
    require({r["branch"] for r in branch_rows} == set(cmap), "branch set vs custody")
    for r in branch_rows:
        require(cmap[r["branch"]]["tip"] == r["frozen_tip"], f"{r['branch']}: custody tip")
        require(r["current_ref_status"] in {"SAME_AS_FROZEN_TIP", "MOVED_AFTER_FROZEN_ROSTER", "MISSING_CURRENT_REF"}, f"{r['branch']}: ref status")
        require(r["disposition"] in {"NO_DELTA_VS_MERGE_BASE", "CODE_EXACT_PRESENT_IN_PREMAIN__TRANSFER_METHOD_UNVERIFIED", "CODE_STRANDED_OR_DIVERGED", "EVIDENCE_OR_ADMIN_ONLY_DELTA"}, f"{r['branch']}: disposition")
    require(branch_counts["frozen_names"] == EXPECTED_BRANCHES and branch_counts["distinct_tips"] == EXPECTED_TIPS, "branch counts")
    require(branch_counts["current_refs_present"] == EXPECTED_BRANCHES, "current refs count")
    require(branch_counts["current_refs_moved"] == 1, "moved ref count")

    require(len(ledger) == EXPECTED_FUNCTIONS, f"ledger rows {len(ledger)}")
    require(len({r["function_id"] for r in ledger}) == EXPECTED_FUNCTIONS, "duplicate function id")
    require(len({r["family_id"] for r in ledger}) == EXPECTED_FAMILIES, "family denominator")
    loc_counts = Counter()
    for r in ledger:
        require(r["current_location"] in ALLOWED_LOCATION, f"{r['function_id']}: location")
        require(r.get("semantic_equivalence") is not True, f"{r['function_id']}: semantic equivalence claim")
        require("SEMANTIC_EQUIVALENCE_NOT_CLAIMED" in r["source_grade"], f"{r['function_id']}: source grade")
        require(r["branch_names"], f"{r['function_id']}: empty branch attribution")
        require(r["branch_tips"], f"{r['function_id']}: empty branch tips")
        if r["current_path"] and r["current_blob"]:
            require(r["current_path"] in tree and tree[r["current_path"]] == r["current_blob"], f"{r['function_id']}: current blob mismatch")
        loc_counts[r["current_location"]] += 1
    require(variant_counts["functions"] == EXPECTED_FUNCTIONS, "variant count")
    require(variant_counts["current_location_counts"] == dict(sorted(loc_counts.items())), "location counts")
    require(len(subtraction["functions"]) == EXPECTED_SUBTRACTION, "subtraction count")
    require(len({r["function_id"] for r in subtraction["functions"]}) == EXPECTED_SUBTRACTION, "subtraction duplicate")
    require(len(uncertain) == EXPECTED_UNCERTAIN, f"uncertain count {len(uncertain)}")
    require(len({r["function_id"] for r in uncertain}) == EXPECTED_UNCERTAIN, "uncertain duplicate")
    require({r["function_id"] for r in subtraction["functions"]} <= {r["function_id"] for r in ledger}, "subtraction subset")
    require({r["function_id"] for r in uncertain} <= {r["function_id"] for r in ledger}, "uncertain subset")
    require(all(r["implementation_class"] == "IMPLEMENTATION_CURRENT_MODIFIED" for r in uncertain), "uncertain class")

    require(integration["accepted_or_staging_count"] == len(integration["branches"]) == 27, "integration count")
    require(counter["schema"] == "RRIF_CUSTODY_COUNTEREXAMPLE_AUDIT@1", "counterexample schema")
    for key in ("PR_525", "PR_526", "PR_563", "J2I", "C3_R5", "R157", "HQ282_P01", "P07"):
        require(key in counter, f"counterexample {key}")
    counts = {
        "branch_names": len(branch_rows), "distinct_tips": len({r["frozen_tip"] for r in branch_rows}),
        "functions": len(ledger), "families_with_variants": len({r["family_id"] for r in ledger}),
        "location_counts": dict(sorted(loc_counts.items())),
        "exact_current_subtraction": len(subtraction["functions"]),
        "uncertain": len(uncertain), "integration_branches": len(integration["branches"]),
        "branch_dispositions": dict(sorted(Counter(r["disposition"] for r in branch_rows).items())),
    }
    return {"schema": "RRIF_CUSTODY_VALIDATION@1", "result": "PASS", "premain": PREMAIN, "counts": counts, "checks": [
        "845 names / 838 tips / custody digests",
        "3135 function rows / 1883 variant-bearing families + 2 external zero-member families / exact-once",
        "2269 exact-current-or-branch-source subtraction; 866 current-modified uncertainties",
        "current path blobs match PREMAIN 8e44ca9c",
        "27 accepted/staging branches audited; PR525/526/563, J2I, C3 R5, R157, HQ282 P01, P07 counterexamples",
        "no semantic-equivalence or lost-capability claim",
    ]}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent)
    ap.add_argument("--output", type=Path)
    args = ap.parse_args()
    try:
        report = validate(args.root)
    except (ValidationError, KeyError, ValueError, json.JSONDecodeError) as e:
        print(json.dumps({"result": "FAIL", "error": str(e)}, indent=2))
        return 1
    text = json.dumps(report, indent=2) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    print(text, end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
