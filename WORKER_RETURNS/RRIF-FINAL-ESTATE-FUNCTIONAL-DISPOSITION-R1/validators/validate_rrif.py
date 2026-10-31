#!/usr/bin/env python3
"""Validate the RRIF estate ledger, negative preservation and fan-in manifest.

Sourcefree: reads JSON/JSONL, checks exact counts and current PRE-MAIN path
blobs. It does not import or execute any historical branch function.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any

FAMILIES = 1885
FUNCTIONS = 3135
NEGATIVES = 2595
BRANCHES = 845
TIPS = 838
PREMAIN = "8e44ca9c751049d65e6def47600b5c073ee04b29"
S7FIX = "80bc5d9bf6624c2ea04027322947a41c347330aa"
S7FIX_I3 = "1b89fd49c330e4a2c976e6af8d6c1a5e6dbfb088"
ALLOWED = {
    "ALREADY_CURRENT",
    "CURRENT_DIFFERENT",
    "CURRENT_TEST_ONLY",
    "HISTORICAL_ONLY",
    "RETIRED_DEFECTIVE",
    "EVIDENCE_ONLY",
    "DUPLICATE_SUPERSEDED",
    "CANDIDATE_ADAPT",
    "NO_REAL_RECEIVER_VERIFIED",
    "AUTHORITY_HELD",
    "NOT_RESOLVED",
}
DECISION = {
    "ALREADY_CURRENT": "PRESERVE_HISTORICAL",
    "CURRENT_DIFFERENT": "HOLD_EXACT_DECISION",
    "CURRENT_TEST_ONLY": "PRESERVE_HISTORICAL",
    "HISTORICAL_ONLY": "PRESERVE_HISTORICAL",
    "RETIRED_DEFECTIVE": "RETIRE",
    "EVIDENCE_ONLY": "PRESERVE_HISTORICAL",
    "DUPLICATE_SUPERSEDED": "RETIRE",
    "CANDIDATE_ADAPT": "HOLD_EXACT_DECISION",
    "NO_REAL_RECEIVER_VERIFIED": "HOLD_EXACT_DECISION",
    "AUTHORITY_HELD": "HOLD_EXACT_DECISION",
    "NOT_RESOLVED": "HOLD_EXACT_DECISION",
}
BOUNDARY = {
    "S7FAM-0869c56ad5e0c899": "OUTER",
    "S7FAM-82686a98a4281425": "OUTER",
    "S7FAM-5823124c837704c1": "OUTER",
    "S7FAM-6054813ba02c8e44": "OUTER",
    "S7FAM-a7fe27d3f45643c3": "OUTER",
    "S7FAM-3ced5b9ab5b98431": "NESTED_ABSENT",
    "S7FAM-0808b82fba697141": "NESTED_ABSENT",
    "S7FAM-739724b429c79765": "NESTED_ABSENT",
    "S7FAM-dabfb5ad4dc9f0a4": "NESTED_ABSENT",
    "S7FAM-c7246db42c0322e0": "NESTED_ABSENT",
    "S7FAM-41da3f505673271b": "JOIN_CURRENT_DIFFERENT",
}


class ValidationError(AssertionError):
    """The return violates an RRIF invariant."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationError(message)


def load_json(path: Path) -> dict[str, Any]:
    require(path.is_file(), f"missing {path.name}")
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    require(path.is_file(), f"missing {path.name}")
    rows = []
    with path.open(encoding="utf-8") as handle:
        for number, line in enumerate(handle, 1):
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as error:
                raise ValidationError(f"{path.name}:{number}: {error}") from error
    return rows


def tree_blobs() -> dict[str, str]:
    output = subprocess.check_output(["git", "ls-tree", "-r", "--full-tree", PREMAIN], text=True)
    result: dict[str, str] = {}
    for line in output.splitlines():
        meta, path = line.split("\t", 1)
        result[path] = meta.split()[2]
    return result


def validate(root: Path, s7fix_path: Path | None = None) -> dict[str, Any]:
    ledger = load_jsonl(root / "ALL_1885_FAMILY_DISPOSITIONS.jsonl")
    negatives = load_jsonl(root / "HISTORICAL_NEGATIVES_AND_ANTI_REBUILD.jsonl")
    custody = load_jsonl(root / "FUNCTION_ID_CUSTODY.jsonl")
    branches = load_json(root / "BRANCH_ROSTER_845.json")
    manifest = load_json(root / "CONSEQUENTIALLY_JUSTIFIED_FANIN_MANIFEST.json")
    post_negatives = load_jsonl(root / "POST_S7FIX_RETURN_NEGATIVES.jsonl")
    summary = load_json(root / "LEDGER_BUILD_SUMMARY.json")
    sourcefree = None

    require(len(ledger) == FAMILIES, f"expected {FAMILIES} families, got {len(ledger)}")
    ids = [row["family_id"] for row in ledger]
    require(len(ids) == len(set(ids)), "duplicate family id")
    require(len(custody) == FUNCTIONS, f"expected {FUNCTIONS} function IDs, got {len(custody)}")
    functions = [row["function_id"] for row in custody]
    require(len(functions) == len(set(functions)), "duplicate function id")
    require(len(negatives) == NEGATIVES, f"expected {NEGATIVES} negatives, got {len(negatives)}")
    require(len({row['negative_id'] for row in negatives}) == NEGATIVES, "duplicate negative id")
    require(branches.get("total_branches") == BRANCHES, "branch count")
    require(len(branches.get("branches", [])) == BRANCHES, "branch roster length")
    require(len({row.get("roster_tip") for row in branches["branches"]}) == TIPS, "distinct tips")
    require(summary.get("families") == FAMILIES and summary.get("function_ids") == FUNCTIONS, "summary counts")
    require(summary.get("negative_records") == NEGATIVES, "summary negatives")

    status_counts = Counter()
    seen_functions = set()
    variant_count = 0
    current_blobs = tree_blobs()
    current_tree = subprocess.check_output(["git", "rev-parse", f"{PREMAIN}:rawlsing_next"], text=True).strip()
    require(current_tree == "1d88d3fbb1d18dadfda946d9cd7f309d84afa479", "current rawlsing_next tree")
    for row in ledger:
        fid = row["family_id"]
        require(row.get("schema") == "RRIF_FAMILY_DISPOSITION@1", f"{fid}: schema")
        if row.get("external_zero_member"):
            require(row["original"].get("function_ids") == [], f"{fid}: external family has IDs")
        else:
            require(row.get("original", {}).get("function_ids"), f"{fid}: no original IDs")
        require(row["disposition"]["status"] in ALLOWED, f"{fid}: status")
        require(row["disposition"]["decision"] == DECISION[row["disposition"]["status"]], f"{fid}: decision")
        require(row["disposition"]["decision"] != "ADOPT", f"{fid}: worker may not adopt")
        require(row["disposition"].get("fanin_candidate") is False, f"{fid}: fanin candidate without receiver")
        require(row["current"].get("production_receiver_verified") is False, f"{fid}: production receiver claim")
        require(row["grades"].get("native_product_accepted") is False, f"{fid}: native promotion")
        require(row["grades"].get("source_science_issued") is False, f"{fid}: science issuance")
        require(row["tests"].get("rrif_run") == [], f"{fid}: untracked test run")
        for item in row["current"].get("current_path_blobs", []):
            path = item["path"]
            require(path in current_blobs, f"{fid}: current path missing {path}")
            require(current_blobs[path] == item["blob"], f"{fid}: current blob mismatch {path}")
        if row["current"].get("current_implementation_sha") not in (None, "MULTIPLE_PATH_BLOBS"):
            require(any(item["blob"] == row["current"]["current_implementation_sha"] for item in row["current"]["current_path_blobs"]), f"{fid}: implementation sha not in current paths")
        if row["disposition"]["status"] == "ALREADY_CURRENT":
            require(row["current"].get("matched_current_member_ids"), f"{fid}: already-current without exact source match")
        if fid in BOUNDARY:
            role = BOUNDARY[fid]
            require(row["current"].get("current_boundary_role") == role, f"{fid}: boundary role")
            require(row["current"].get("current_owner_mapping_status", "").startswith("RED__"), f"{fid}: boundary owner mapping must be red")
            if role == "NESTED_ABSENT":
                require(row["disposition"]["status"] == "HISTORICAL_ONLY", f"{fid}: nested must be historical")
                require(row["current"].get("current_nested_owner_absent") is True, f"{fid}: nested absence")
            else:
                require(row["disposition"]["status"] == "CURRENT_DIFFERENT", f"{fid}: outer/join must be current different")
                require(bool(row["current"].get("current_ast_sha")), f"{fid}: current AST prefix")
        for mid in row["original"]["function_ids"]:
            require(mid in functions, f"{fid}: missing function custody {mid}")
        variants = row["comparison"].get("variant_comparisons", [])
        require(len(variants) == len(row["original"]["function_ids"]), f"{fid}: variant count")
        for variant in variants:
            require(variant["variant_decision"] in DECISION.values(), f"{fid}: variant decision")
        variant_count += len(variants)
        status_counts[row["disposition"]["status"]] += 1

    require(set(BOUNDARY).issubset(set(ids)), "missing six-boundary families")
    require(sum(status_counts.values()) == FAMILIES, "status denominator")
    require(variant_count == FUNCTIONS, f"expected {FUNCTIONS} variant comparisons, got {variant_count}")
    require(summary.get("status_counts") == dict(sorted(status_counts.items())), "status summary mismatch")

    negative_family_ids = Counter(row["family_id"] for row in negatives)
    require(set(negative_family_ids).issubset(set(ids)), "negative family unknown")
    for row in negatives:
        require(row.get("schema") == "RRIF_HISTORICAL_NEGATIVE_RECORD@1", f"{row['negative_id']}: schema")
        require(row.get("source", {}).get("s7fix") == S7FIX, f"{row['negative_id']}: source")
        require(isinstance(row.get("record"), dict), f"{row['negative_id']}: raw record")
    require(sum(negative_family_ids.values()) == NEGATIVES, "negative denominator")
    require(len(post_negatives) == 8, "post-S7FIX negatives")
    require(all(row.get("schema") == "RRIF_POST_S7FIX_RETURN_NEGATIVE@1" for row in post_negatives), "post-S7FIX schema")
    require({"POST-NEG-PE-OVERLAY","POST-NEG-R9-SIX","POST-NEG-F7-HQ227","POST-NEG-P07-NATIVE","POST-NEG-S7-OWNER-RED","POST-NEG-R9-ISSUER","POST-NEG-V2K-ANTIJOIN","POST-NEG-R157-SCOPE"} == {row["id"] for row in post_negatives}, "post-S7FIX IDs")

    require(manifest.get("premain") == PREMAIN, "manifest premain")
    require(manifest.get("inputs", {}).get("S7FIX") == S7FIX, "manifest S7FIX")
    require(manifest.get("integration_ready") == [], "manifest claims integration ready")
    require(any(item.get("id") == "RRIF-C3-D01-ENCODING" for item in manifest.get("candidates", [])), "D01 missing")
    require(any(item.get("id") == "RRIF-C3-D02-OPAQUE-DATE-TIME" for item in manifest.get("candidates", [])), "D02 missing")
    require(any(item.get("id") == "RRIF-F7-PURE-METHOD" for item in manifest.get("candidates", [])), "F7 missing")
    require(any(item.get("id") == "RRIF-R9-BROKER-SESSION-BINDING" for item in manifest.get("not_fanin_or_retired", [])), "R9 missing")
    require(any(item.get("id") == "RRIF-P07-NATIVE-OWNER" for item in manifest.get("not_fanin_or_retired", [])), "P07 missing")
    for item in manifest.get("candidates", []):
        require(item.get("fanin_ready") is False, f"{item['id']}: fanin ready")
        require(item.get("decision") in {"HOLD_EXACT_DECISION", "PRESERVE_HISTORICAL", "RETIRE"}, f"{item['id']}: decision")

    if s7fix_path is not None:
        source = json.loads(s7fix_path.read_text(encoding="utf-8"))
        source_families = source["corrected_families"]
        require(len(source_families) == FAMILIES, "S7FIX family count")
        require({x["family_id"] for x in source_families} == set(ids), "S7FIX family ids")
        source_functions = {m["function_id"] for x in source_families for m in x["members"]}
        require(source_functions == set(functions), "S7FIX function ids")
        require(sum(len(x.get("review_negative_preservation") or []) for x in source_families) == NEGATIVES, "S7FIX negative count")
        require(sum(1 for x in source_families if x["correction"]["type"] != "NONE") == 11, "S7FIX boundary count")

    counts = {
        "families": len(ledger),
        "function_ids": len(custody),
        "negative_records": len(negatives),
        "branch_names": len(branches["branches"]),
        "distinct_tips": len({row.get("roster_tip") for row in branches["branches"]}),
        "status_counts": dict(sorted(status_counts.items())),
        "six_boundary_families": len(BOUNDARY),
        "variant_comparisons": variant_count,
        "post_s7fix_negatives": len(post_negatives),
        "current_tree": current_tree,
    }
    checks = [
        "1885 families / 3135 exact-once function IDs / 2595 negative records / 845 branches / 838 tips",
        "11 corrected boundary families: 5 outer, 5 nested, 1 joined",
        "no worker adoption, native acceptance or science issuance",
        "current path blobs match PRE-MAIN 8e44ca9c",
        "six boundary current-owner mapping remains RED",
        "manifest has no integration-ready item; D01/D02/F7/R9/P07 decisions retained",
        "all 2,595 S7FIX negative records preserve source and raw cause",
        "8 post-S7FIX PE/R9/F7/P07/S7/V2K/R157 negatives preserved",
    ]
    return {"schema": "RRIF_VALIDATION@1", "result": "PASS", "premain": PREMAIN, "s7fix": S7FIX, "s7fix_i3": S7FIX_I3, "counts": counts, "checks": checks, "sourcefree_results": sourcefree}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent)
    parser.add_argument("--s7fix", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        report = validate(args.root, args.s7fix)
    except (ValidationError, KeyError, ValueError, json.JSONDecodeError) as error:
        print(json.dumps({"result": "FAIL", "error": str(error)}, indent=2))
        return 1
    text = json.dumps(report, indent=2) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    print(text, end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
