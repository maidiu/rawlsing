"""A41 whole-estate acceptance assessor. Deterministic, fail-closed.

Consumes the frozen independent expected scope and the ingested (preimage
verified) receipt bank. Produces the N11 candidate accounting. It never
constructs its own expected universe and it never promotes a weaker evidence
grade into a stronger occupancy claim.

Acceptance distinctions preserved (never collapsed):
  actual scientific functional completion
  | implemented-but-not-source-populated
  | valid empirical null (with cause)
  | source-intrinsic nonapplicability (only with original proof)
  | missing competent semantic/source permission
  | missing producer or downstream consumer
  | incorrectly claimed coverage
  | accepted source/function/replay evidence
"""
from __future__ import annotations

from collections import defaultdict

from . import receipt_bank

# Ranking: strongest occupancy first. A weaker grade can never overwrite a
# stronger one, and only ORIGINAL_MEASURED_OCCUPANCY fills original occupancy.
GRADE_RANK = {
    "ORIGINAL_MEASURED_OCCUPANCY": 0,
    "HISTORICAL_SCOPE_POSITIVE": 1,
    "EMPIRICAL_NULL_WITH_CAUSE": 2,
    "SOURCEFREE_LOCAL_POSITIVE": 3,
    "DOCUMENTARY_IDENTITY_RECONCILIATION": 4,
    "DEVELOPMENT_BLOCKER_WITH_NARROW_OWNER": 5,
    "SOURCE_INTRINSIC_NONAPPLICABILITY_PROVED": 6,
}

GRADE_TO_CELL_STATUS = {
    "ORIGINAL_MEASURED_OCCUPANCY": "ORIGINAL_MEASURED_OCCUPANCY",
    "HISTORICAL_SCOPE_POSITIVE": "HISTORICAL_SCOPE_POSITIVE__NOT_CURRENT_OCCUPANCY",
    "EMPIRICAL_NULL_WITH_CAUSE": "EMPIRICAL_NULL_WITH_CAUSE",
    "SOURCEFREE_LOCAL_POSITIVE": "SOURCEFREE_LOCAL_POSITIVE__NOT_ORIGINAL_OCCUPANCY",
    "DOCUMENTARY_IDENTITY_RECONCILIATION": "ACCOUNTED_IDENTITY_ONLY__NOT_OCCUPIED",
    "DEVELOPMENT_BLOCKER_WITH_NARROW_OWNER": "DEVELOPMENT_BLOCKER_WITH_NARROW_OWNER",
    "SOURCE_INTRINSIC_NONAPPLICABILITY_PROVED": "SOURCE_INTRINSIC_NONAPPLICABILITY_PROVED",
}

MISSING_STATUS = "MISSING_EXPECTED_ORIGINAL_SCIENCE__NOT_INTRINSICALLY_INAPPLICABLE"


def _strongest(grades):
    return sorted(grades, key=lambda g: GRADE_RANK[g])[0]


def assess(scope: dict, ingested_bank: dict) -> dict:
    """Return the full N11 candidate accounting."""
    # Per-cell coverage from explicit receipt declarations.
    cell_receipts = defaultdict(list)
    for rec in ingested_bank["ingested"]:
        cov = rec["coverage"]
        for wid in cov["wave_ids"]:
            for aid in cov["axis_ids"]:
                cell_receipts[f"{wid}.{aid}"].append(rec)

    # --- 1,890 cell accounting ------------------------------------------
    cells_out = []
    grade_tally = defaultdict(int)
    for cell in scope["cells"]:
        covering = cell_receipts.get(cell["cell_id"], [])
        if covering:
            grades = [r["occupancy_kind"] for r in covering]
            primary = _strongest(grades)
            status = GRADE_TO_CELL_STATUS[primary]
            evidence = [{
                "receipt_id": r["receipt_id"], "occupancy_kind": r["occupancy_kind"],
                "origin_commit": r["origin_commit"], "claim_id": r["claim_id"],
                "proof_grade": r["proof_grade"],
                "downstream_consumer_read_refs": r["coverage"].get("occupancy_grain_note"),
            } for r in sorted(covering, key=lambda x: x["receipt_id"])]
            missing = None
        else:
            primary = None
            status = MISSING_STATUS
            evidence = []
            missing = {
                "obligation": cell["required_proof"],
                "expected_u_e_pre_status": cell["expected_u_e_pre"]["expected_u_e_pre_status"],
                "expected_authority": cell["expected_u_e_pre"]["expected_u_e_pre_authority"],
                "owner": "COMPETENT_ORIGINAL35_SOURCE_OPERATION_ISSUER_OR_NAMED_PRODUCER",
            }
        grade_tally[status] += 1
        cells_out.append({
            "cell_id": cell["cell_id"],
            "source_id": cell["source_id"],
            "axis_id": cell["axis_id"],
            "axis_family": cell["axis_family"],
            "identity": cell["identity"],
            "expected_u_e_pre": cell["expected_u_e_pre"],
            "expected_status": cell["expected_status"],
            "consumed_grade": primary,
            "cell_status": status,
            "actual_evidence": evidence,
            "missing_obligation": missing,
        })

    # --- 35 wave accounting ---------------------------------------------
    waves_out = []
    for wave in scope["waves"]:
        wcells = [c for c in cells_out if c["source_id"] == wave["source_id"]]
        if any(c["consumed_grade"] == "ORIGINAL_MEASURED_OCCUPANCY" for c in wcells):
            var = "ORIGINAL_MEASURED_OCCUPIED"
        elif any(c["consumed_grade"] == "HISTORICAL_SCOPE_POSITIVE" for c in wcells):
            var = "HISTORICAL_SCOPE_ONLY"
        elif any(c["consumed_grade"] == "DEVELOPMENT_BLOCKER_WITH_NARROW_OWNER" for c in wcells):
            var = "BLOCKED_NARROW_OWNER"
        elif any(c["consumed_grade"] == "DOCUMENTARY_IDENTITY_RECONCILIATION" for c in wcells):
            var = "IDENTITY_ACCOUNTED_ONLY"
        else:
            var = "EXPECTED_UNISSUED"
        waves_out.append({
            "source_id": wave["source_id"],
            "source_name": wave["source_name"],
            "identity": wave["identity"],
            "expected_u_e_pre": wave["expected_u_e_pre"],
            "wave_occupancy_state": var,
            "occupied_or_accounted_cells": sum(1 for c in wcells if c["consumed_grade"]),
            "missing_cells": sum(1 for c in wcells if c["consumed_grade"] is None),
        })

    # --- 151 / 101 ------------------------------------------------------
    cov_reg = defaultdict(list)
    cov_led = defaultdict(list)
    global_cov = defaultdict(list)
    for rec in ingested_bank["ingested"]:
        for rid in rec["coverage"]["register_151_ids"]:
            cov_reg[rid].append(rec)
        for lid in rec["coverage"]["ledger_101_ids"]:
            cov_led[lid].append(rec)
        for gr in rec["coverage"]["global_relations"]:
            global_cov[gr].append(rec)

    cw = scope["crosswalk_151_101"]
    split_ids = {e["register_id"] for e in cw["split_register_rows"]}
    merge_ids = {e["ledger_id"] for e in cw["merge_ledger_rows"]}
    register_out = [{
        "register_id": r["id"], "group": r["group"], "obligation": r["obligation"],
        "declared_status": r["declared_status"],
        "crosswalk_split": r["id"] in split_ids,
        "evidence_receipts": [x["receipt_id"] for x in cov_reg.get(r["id"], [])],
        "completion_state": ("EVIDENCE_PRESENT" if cov_reg.get(r["id"]) else "MISSING_EXPECTED"),
    } for r in scope["register_151_rows"]]
    ledger_out = [{
        "ledger_id": t["id"], "scope": t["scope"], "action": t["action"],
        "f_gate_ids": t["f_gate_ids"], "crosswalk_merge": t["id"] in merge_ids,
        "evidence_receipts": [x["receipt_id"] for x in cov_led.get(t["id"], [])],
        "completion_state": ("EVIDENCE_PRESENT" if cov_led.get(t["id"]) else "MISSING_EXPECTED"),
    } for t in scope["ledger_101_rows"]]

    # --- F1-F8 gate rows (280 per-wave + 3 global) ----------------------
    f_axes = scope["axis_ids"][scope["axis_counts"]["source_native"]
                               + scope["axis_counts"]["ee_engine"]:]
    f_rows = []
    for cell in cells_out:
        if cell["axis_family"] != "F_GATE":
            continue
        f_rows.append({
            "gate_id": cell["axis_id"],
            "grain": scope["f1_f8_gate_grain"][cell["axis_id"]],
            "source_id": cell["source_id"],
            "identity": cell["identity"],
            "expected_u_e_pre": cell["expected_u_e_pre"],
            "consumed_grade": cell["consumed_grade"],
            "cell_status": cell["cell_status"],
            "actual_evidence": cell["actual_evidence"],
            "missing_obligation": cell["missing_obligation"],
            "local_pass_cannot_close_global": cell["axis_id"] in ("F6", "F7", "F8"),
        })
    for name, rel in scope["global_relations"].items():
        recs = global_cov.get(name, [])
        f_rows.append({
            "gate_id": name.split("_")[-1],
            "grain": rel["grain"],
            "source_id": "GLOBAL",
            "global_relation_name": name,
            "expected_status": rel["expected_status"],
            "consumed_grade": (_strongest([r["occupancy_kind"] for r in recs]) if recs else None),
            "cell_status": ("SOURCEFREE_CONTRIBUTION_ONLY__GLOBAL_UNCLOSED" if recs
                            else "OPEN_GLOBAL_OBLIGATION__UNCLOSED"),
            "actual_evidence": [{"receipt_id": r["receipt_id"],
                                 "occupancy_kind": r["occupancy_kind"]} for r in recs],
            "missing_obligation": rel["obligation"],
            "local_pass_cannot_close_global": True,
        })

    # --- finite blocker ledger ------------------------------------------
    blockers = []
    for cell in cells_out:
        if cell["missing_obligation"] is not None:
            blockers.append({
                "kind": "MISSING_EXPECTED_CELL_EVIDENCE",
                "cell_id": cell["cell_id"],
                "owner": cell["missing_obligation"]["owner"],
                "expected_authority": cell["missing_obligation"]["expected_authority"],
                "reason": cell["missing_obligation"]["obligation"],
            })
    for row in f_rows:
        if row["source_id"] == "GLOBAL":
            blockers.append({
                "kind": "OPEN_GLOBAL_RELATION",
                "cell_id": f"GLOBAL.{row['global_relation_name']}",
                "owner": "COMPETENT_GLOBAL_RELATION_OWNER_EE12_EE13_EE14",
                "reason": row["expected_status"],
            })
    seen = set()
    blocker_ledger = []
    for b in blockers:
        key = (b["kind"], b["cell_id"])
        if key in seen:
            continue
        seen.add(key)
        blocker_ledger.append(b)

    original_occupied = grade_tally.get("ORIGINAL_MEASURED_OCCUPANCY", 0)
    verdict = {
        "n11_state": "N11_NOT_READY",
        "verdict_scope": "whole declared estate: 35 waves / 1,890 cells / 151<->101 / F1-F8 global",
        "original_measured_occupied_cells": original_occupied,
        "historical_scope_cells": grade_tally.get("HISTORICAL_SCOPE_POSITIVE__NOT_CURRENT_OCCUPANCY", 0),
        "empirical_null_cells": grade_tally.get("EMPIRICAL_NULL_WITH_CAUSE", 0),
        "sourcefree_covered_cells": grade_tally.get("SOURCEFREE_LOCAL_POSITIVE__NOT_ORIGINAL_OCCUPANCY", 0),
        "identity_accounted_only_cells": grade_tally.get("ACCOUNTED_IDENTITY_ONLY__NOT_OCCUPIED", 0),
        "blocked_cells": grade_tally.get("DEVELOPMENT_BLOCKER_WITH_NARROW_OWNER", 0),
        "intrinsic_nonapplicability_cells": grade_tally.get("SOURCE_INTRINSIC_NONAPPLICABILITY_PROVED", 0),
        "missing_expected_cells": grade_tally.get(MISSING_STATUS, 0),
        "total_cells": len(cells_out),
        "finite_blocker_count": len(blocker_ledger),
        "global_relations_closed": 0,
        "global_relations_open": 3,
        "can_self_adopt_n11": False,
        "notes": [
            "SOURCEFREE_LOCAL_PASS != ORIGINAL_ESTATE_OCCUPANCY",
            "TYPED_REFUSAL != COMPLETION",
            "AUTHORIZED_SOURCE != ARBITRARY_QUERY",
            "per-wave F6/F7/F8 cells cannot discharge the global F6/F7/F8 capabilities",
        ],
    }

    preserved_unknown_bounds = [{
        "receipt_id": r["receipt_id"],
        "claim_id": r["claim_id"],
        "unknown_bounds": r.get("unknown_bounds") or r["coverage"].get("unknown_bounds") or {},
    } for r in ingested_bank["ingested"]]
    # attach the receipt-level unknown bounds explicitly (carried from the bank).
    for rec_out, rec_in in zip(preserved_unknown_bounds, ingested_bank["ingested"]):
        pass

    return {
        "verdict": verdict,
        "preserved_unknown_bounds": preserved_unknown_bounds,
        "cells": cells_out,
        "waves": waves_out,
        "register_151": register_out,
        "ledger_101": ledger_out,
        "crosswalk_151_101": cw,
        "f1_f8_rows": f_rows,
        "blocker_ledger": blocker_ledger,
        "grade_tally": dict(sorted(grade_tally.items())),
        "receipt_summary": [{
            "receipt_id": r["receipt_id"], "occupancy_kind": r["occupancy_kind"],
            "origin_commit": r["origin_commit"], "claim_id": r["claim_id"],
            "evidence_state": r["evidence_state"], "proof_grade": r["proof_grade"],
            "verified_artifact_count": len(r["verified_artifacts"]),
        } for r in ingested_bank["ingested"]],
        "pending_slots": ingested_bank.get("pending_slots", []),
    }
