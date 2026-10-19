"""Emit the exact N11 named products at CANDIDATE / NOT_READY grade."""
from __future__ import annotations

ARTIFACT_SCHEMA = "PYAT_A41_N11_CANDIDATE@1.0.0"

GATE_AXES = ("historical_function", "current_owner_capacity", "current_carrier",
             "current_algorithm_producer", "current_composed_realization",
             "current_35_wave_authority", "live_occupancy", "downstream_consumer")


def gate_maturity(gp, startup_commit):
    path = ("PYAT_CONTROL_ROOM/ASTRA_PYAT_INTEGRATED_DEVELOPMENT_ATLAS_R1/data/"
            "functional_gate_maturity.json")
    rows = gp.parse_json(gp.blob_at(startup_commit, path))
    out = {}
    for row in rows:
        gate = row[0].split()[0]
        out[gate] = dict(zip(GATE_AXES, row[1:]))
    return out


def f1_f8_matrix(accounting, scope, gm):
    per_gate = {}
    for row in accounting["f1_f8_rows"]:
        per_gate.setdefault(row["gate_id"], []).append(row)
    return {
        "schema": ARTIFACT_SCHEMA,
        "artifact": "f1_f8_acceptance_matrix.json",
        "grade": "CANDIDATE_NOT_READY",
        "scope_digest": scope["scope_digest"],
        "declared_gate_grain": scope["f1_f8_gate_grain"],
        "frozen_eight_axis_maturity": gm,
        "global_relation_rule": ("F6/F7/F8 global capabilities are separate global "
                                 "relation/service obligations and cannot be discharged "
                                 "by filling independent per-wave cells."),
        "row_count": len(accounting["f1_f8_rows"]),
        "per_wave_row_count": sum(1 for r in accounting["f1_f8_rows"] if r["source_id"] != "GLOBAL"),
        "global_row_count": sum(1 for r in accounting["f1_f8_rows"] if r["source_id"] == "GLOBAL"),
        "rows": accounting["f1_f8_rows"],
        "gate_summary": {
            g: {
                "rows": len(rows),
                "original_measured": sum(1 for r in rows if r["consumed_grade"] == "ORIGINAL_MEASURED_OCCUPANCY"),
                "sourcefree_or_history": sum(1 for r in rows if r["consumed_grade"] in (
                    "SOURCEFREE_LOCAL_POSITIVE", "HISTORICAL_SCOPE_POSITIVE", "EMPIRICAL_NULL_WITH_CAUSE")),
                "missing": sum(1 for r in rows if r["consumed_grade"] is None),
                "global_unclosed": g in ("F6", "F7", "F8"),
            } for g, rows in sorted(per_gate.items())
        },
        "n11_state": accounting["verdict"]["n11_state"],
    }


def estate_manifest(accounting, scope):
    return {
        "schema": ARTIFACT_SCHEMA,
        "artifact": "estate_acceptance_manifest.json",
        "grade": "CANDIDATE_NOT_READY",
        "startup_commit": scope["startup_commit"],
        "scope_digest": scope["scope_digest"],
        "declared_documents": scope["declared_documents"],
        "expected_accounting": {
            "source_count": scope["source_count"],
            "axis_counts": scope["axis_counts"],
            "expected_cell_count": scope["expected_cell_count"],
            "register_151_count": scope["register_151_count"],
            "ledger_101_count": scope["ledger_101_count"],
        },
        "verdict": accounting["verdict"],
        "grade_tally": accounting["grade_tally"],
        "receipt_summary": accounting["receipt_summary"],
        "preserved_unknown_bounds": accounting.get("preserved_unknown_bounds", []),
        "pending_return_slots": accounting["pending_slots"],
        "crosswalk_151_101": accounting["crosswalk_151_101"],
        "waves": accounting["waves"],
        "cells": accounting["cells"],
        "register_151": accounting["register_151"],
        "ledger_101": accounting["ledger_101"],
        "blocker_ledger": accounting["blocker_ledger"],
        "global_relations": scope["global_relations"],
    }


def final_maturity_md(accounting, scope):
    v = accounting["verdict"]
    L = []
    A = L.append
    A("# A41 - N11 whole-estate terminal acceptance assembly - CANDIDATE adjudication")
    A("")
    A(f"**State: {v['n11_state']}** at the exact whole declared-estate grain.")
    A("")
    A("Machine-generated candidate adjudication from the frozen independent expected scope")
    A("and the preimage-verified receipt bank. It does NOT self-adopt N11, issue")
    A("source/model/actor permission, or wake N12. Recording remaining obligations is not")
    A("completion.")
    A("")
    A(f"- startup commit: `{scope['startup_commit']}`")
    A(f"- frozen scope digest: `{scope['scope_digest']}`")
    A(f"- expected cells: {scope['expected_cell_count']} (35 x {scope['axis_counts']['total']}: "
      f"{scope['axis_counts']['source_native']} native + {scope['axis_counts']['ee_engine']} EE + "
      f"{scope['axis_counts']['f_gate']} F)")
    A(f"- 151 register obligations, 101 ledger tasks, "
      f"{len(accounting['crosswalk_151_101']['edges'])} crosswalk edges, "
      f"{len(accounting['crosswalk_151_101']['unmatched_register_rows'])} unmatched register rows")
    A("")
    A("## Occupancy by grade (non-substitutable)")
    A("")
    A("| Grade | Cells |")
    A("|---|---|")
    A(f"| original measured occupancy | {v['original_measured_occupied_cells']} |")
    A(f"| historical scope only | {v['historical_scope_cells']} |")
    A(f"| empirical null with cause | {v['empirical_null_cells']} |")
    A(f"| sourcefree local positive (not original occupancy) | {v['sourcefree_covered_cells']} |")
    A(f"| accounted identity only (not occupied) | {v['identity_accounted_only_cells']} |")
    A(f"| development blocker, narrow owner | {v['blocked_cells']} |")
    A(f"| source-intrinsic nonapplicability proved | {v['intrinsic_nonapplicability_cells']} |")
    A(f"| missing expected original science | {v['missing_expected_cells']} |")
    A(f"| **total** | **{v['total_cells']}** |")
    A("")
    A("## Global F1-F8 obligations")
    A("")
    A("The global F6 (cross-family without pooling), F7 (comparable-wave temporal) and F8")
    A("(progressive possibility service) capabilities are separate global relation/service")
    A("obligations. Per-wave F-axis cells are recorded but explicitly cannot close them.")
    A("")
    for row in accounting["f1_f8_rows"]:
        if row.get("source_id") == "GLOBAL":
            A(f"- `{row['global_relation_name']}`: {row['cell_status']} - {row['expected_status']}")
    A("")
    A("## Receipts ingested (preimage verified)")
    A("")
    A("| Receipt | Occupancy kind | Origin commit |")
    A("|---|---|---|")
    for r in accounting["receipt_summary"]:
        A(f"| {r['receipt_id']} | {r['occupancy_kind']} | `{r['origin_commit'][:12]}` |")
    A("")
    A("Pending concurrent return slots (NOT accepted): " +
      ", ".join(s["slot_id"] for s in accounting["pending_slots"]))
    A("")
    A("## Finite blocker ledger (largest remaining owners)")
    A("")
    A(f"Total finite blockers: {len(accounting['blocker_ledger'])}")
    A("")
    kinds = {}
    for b in accounting["blocker_ledger"]:
        kinds.setdefault(b["kind"], []).append(b)
    for kind, rows in sorted(kinds.items()):
        A(f"- `{kind}`: {len(rows)}")
    A("")
    A("## Terminal decision")
    A("")
    A("N11 remains NOT_READY. The next competent decisions are the finite issuer/producer")
    A("obligations in `estate_acceptance_manifest.json` (blocker_ledger) plus the concurrent")
    A("E41/W41/P41 returns. No further reviewer is auto-commissioned.")
    return "\n".join(L) + "\n"
