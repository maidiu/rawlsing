"""Build G50 artifacts: frontier, oracle root, native receipts, canaries, census."""
from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
import subprocess
import sys

RETURN_DIR = Path(__file__).resolve().parents[1]
if str(RETURN_DIR) not in sys.path:
    sys.path.insert(0, str(RETURN_DIR))
import bootstrap  # noqa: F401

from g50.canaries import canary_matrix, decision_demands, original35_census
from g50.enumerate import enumerate_frontier
from g50.fixture import bundle, policy
from g50.native_i05 import native_no_drop, run_empty_probe, run_native
from g50.oracle import expected_eligible_ids, expected_epre_root
from g50.plan import native_construction_plan

ART = RETURN_DIR / "artifacts"
ART.mkdir(exist_ok=True)


def dump(name, payload):
    path = ART / name
    text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    path.write_text(text, encoding="utf-8")
    return hashlib.sha256(text.encode()).hexdigest()


def main():
    b, p = bundle(), policy()
    frontier = enumerate_frontier(b, p)
    budget_frontier = enumerate_frontier(b, p, budget=10)
    oracle_ids = expected_eligible_ids(b, p)
    oracle_root = expected_epre_root(b, p)
    native_a = run_native()
    native_b = run_native()
    empty = run_empty_probe()
    no_drop = native_no_drop(frontier, native_a)
    plan = native_construction_plan(frontier, native_a)
    canaries = canary_matrix(frontier, native_a, budget_frontier=budget_frontier,
                             empty_probe=empty)
    census = original35_census()
    demands = decision_demands()

    env = dict(__import__("os").environ)
    env["PYTHONPATH"] = str(RETURN_DIR) + __import__("os").pathsep + env.get("PYTHONPATH", "")
    proc = subprocess.run(
        [sys.executable, "-c",
         "import bootstrap; from g50.native_i05 import run_native; "
         "print(run_native().content_hash)"],
        cwd=str(RETURN_DIR), env=env, capture_output=True, text=True, timeout=900,
    )
    detached_hash = proc.stdout.strip()

    hashes = {}
    hashes["expected_frontier_root.json"] = dump("expected_frontier_root.json", {
        "schema": "G50_EXPECTED_FRONTIER_ROOT@1",
        "bundle_hash": b.content_hash, "policy_hash": p.content_hash,
        "oracle_eligible_count": len(oracle_ids),
        "oracle_e_pre_root": oracle_root,
        "composer_e_pre_root": frontier.e_pre_root,
        "roots_equal": oracle_root == frontier.e_pre_root,
    })
    hashes["frontier_summary.json"] = dump("frontier_summary.json", {
        "schema": "G50_FRONTIER_SUMMARY@1",
        "bundle_id": b.bundle_id, "policy_id": p.policy_id, "policy_grade": p.grade,
        "source_identity": frontier.source_identity,
        "u_item_root": frontier.u_item_root, "u_unit_root": frontier.u_unit_root,
        "u_app_root": frontier.u_app_root,
        "e_pre_count": frontier.e_pre_count, "e_pre_root": frontier.e_pre_root,
        "e_pre_cause": frontier.e_pre_cause,
        "class_counts": frontier.class_counts,
        "disposition_counts": frontier.disposition_counts,
        "native_supported_count": sum(1 for op in frontier.eligible()
                                      if op.native_support.startswith("I05_EXACT:")),
        "budget_state": frontier.budget_state,
        "budget_partial": {"state": budget_frontier.budget_state,
                           "pending": len(budget_frontier.pending_operation_ids),
                           "e_pre_root_unchanged":
                               budget_frontier.e_pre_root == frontier.e_pre_root},
        "maximum_bounds": frontier.maximum_bounds,
        "original_science_grade": frontier.original_science_grade,
        "native_expected_rule_counts": no_drop["expected_rule_coverage"],
        "original_measured_occupancy": 0,
        "accounting_cells_unchanged": 1890,
    })
    hashes["frontier_operations.json"] = dump("frontier_operations.json", {
        "schema": "G50_FRONTIER_OPERATIONS@1",
        "count": len(frontier.operations),
        "operations": [op.material() for op in frontier.operations],
    })
    hashes["native_i05_receipts.json"] = dump("native_i05_receipts.json", {
        "schema": "G50_NATIVE_I05_RECEIPTS@1",
        "run": native_a.material(),
        "no_drop": no_drop,
        "empty_probe": empty,
        "cold_second_identical": native_a.content_hash == native_b.content_hash,
        "detached_process_hash": detached_hash,
        "detached_identical": detached_hash == native_a.content_hash,
    })
    hashes["native_construction_plan.json"] = dump("native_construction_plan.json", plan)
    hashes["original35_census.json"] = dump("original35_census.json", {
        "schema": "G50_ORIGINAL35_CENSUS@1", "source_count": len(census),
        "original_u_e_pre_state": "NULL_WITH_CAUSE",
        "rows": census,
    })
    hashes["DECISION_DEMANDS.json"] = dump("DECISION_DEMANDS.json", {
        "schema": "G50_DECISION_DEMANDS@1", "decisions": demands,
    })
    hashes["mutation_receipt.json"] = dump("mutation_receipt.json", {
        "schema": "G50_MUTATION_RECEIPT@1",
        "baseline": no_drop["no_drop_ok"],
        "dropped_rule": "COND-M1",
        "mutated_no_drop": native_no_drop(frontier, run_native(drop_rule="COND-M1")),
        "restored": native_no_drop(frontier, run_native())["no_drop_ok"],
    })
    path = ART / "28_CANARY_DISPOSITION.csv"
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=("id", "class", "disposition", "evidence", "detail"))
        writer.writeheader()
        writer.writerows(canaries)
    hashes["28_CANARY_DISPOSITION.csv"] = hashlib.sha256(path.read_bytes()).hexdigest()
    hashes["canary_matrix.json"] = dump("canary_matrix.json", {
        "schema": "G50_CANARY_MATRIX@1", "count": len(canaries),
        "dispositions": {r["disposition"]: sum(1 for x in canaries if x["disposition"] == r["disposition"])
                         for r in canaries},
        "rows": canaries,
    })
    (RETURN_DIR / "evidence" / "artifact_hashes.json").write_text(
        json.dumps(hashes, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"e_pre_count": frontier.e_pre_count,
                      "e_pre_root": frontier.e_pre_root,
                      "eligible": len(frontier.eligible()),
                      "native_candidates": native_a.candidate_count,
                      "no_drop": no_drop["no_drop_ok"],
                      "cold_identical": native_a.content_hash == native_b.content_hash,
                      "detached_identical": detached_hash == native_a.content_hash,
                      "canaries": len(canaries),
                      "artifacts": len(hashes)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
