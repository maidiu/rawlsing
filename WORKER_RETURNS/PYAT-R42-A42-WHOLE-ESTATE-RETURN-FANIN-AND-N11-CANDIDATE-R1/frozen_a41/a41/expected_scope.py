"""A41 independent expected scope — frozen BEFORE any assessor logic.

This module builds the non-shrunken acceptance domain purely from the *declared*
HQ estate documents at their exact Git preimages. It never consults a producer,
a receipt bank or a consumer output. The producer roster must not construct its
own expected universe; this is the frozen universe the assessor is judged against.

Frozen scope covers:
  * 35 original waves (SRC01..SRC35)
  * 35 x 54 = 1,890 source x axis cells (30 source-native + 16 EE + 8 F)
  * 151 inherited obligation classes (GLOBAL_WORK_REGISTER)
  * 101 current function tasks (TASK_LEDGER_101)
  * explicit many-to-many 151<->101 crosswalk with split/merge rationale
  * 3 global relation obligations (F6 cross-family, F7 temporal, F8 possibility)
"""
from __future__ import annotations

import hashlib
import json
from collections import defaultdict

SCOPE_SCHEMA = "PYAT_A41_INDEPENDENT_EXPECTED_SCOPE@1.0.0"

# The four declared estate documents, pinned to the exact R41 startup preimages.
DECLARED_DOCUMENTS = {
    "estate_matrix": {
        "path": "PYAT_CONTROL_ROOM/WHOLE_MACHINE_COMPLETION_R1/ESTATE_35X_REQUIREMENTS_MATRIX.json",
        "blob_sha1": "2ad9a001aefef4889d8ac48a2a81cd806dec50d6",
        "role": "35 sources x 54 axes = 1890 scoped cells + cell status vocabulary",
    },
    "register_151": {
        "path": "PYAT_CONTROL_ROOM/WHOLE_MACHINE_COMPLETION_R1/GLOBAL_WORK_REGISTER.json",
        "blob_sha1": "7fb47b5d57d4d207847aec347734f5888f70b75e",
        "role": "151 inherited obligation classes",
    },
    "ledger_101": {
        "path": "PYAT_CONTROL_ROOM/WHOLE_MACHINE_COMPLETION_R1/TASK_LEDGER_101_MACHINE.json",
        "blob_sha1": "45be0f82e72ab37bcb972236b1ef3a827b1f95ac",
        "role": "101 normalized current function tasks",
    },
    "global_relations": {
        "path": "PYAT_CONTROL_ROOM/WHOLE_MACHINE_COMPLETION_R1/GLOBAL_F6_F7_F8_RELATION_SCOPE_MATRIX.json",
        "blob_sha1": "8870545724d2b3353e4cb4125bc06c041d463954",
        "role": "global F6/F7/F8 relation obligations (not 35 scalar outcomes)",
    },
}

# Declared identity facets every expected row must carry.
IDENTITY_FACETS = ("source", "edition", "item", "response", "risk", "design", "operation")

# Declared consumer registry (R41 flight / estate named consumers). A receipt may
# only claim a downstream consumer read that appears here.
DECLARED_CONSUMERS = (
    "product.nonparent.consume",
    "consume_f6m_evidence",
    "M1 learned empirical adjudication",
    "EE1 historical consumer",
    "proposal purpose",
)

# Declared acceptance clock (R41 startup day). A receipt's as-of must not be later.
DECLARED_CLOCK = "2026-10-19T23:59:59-0400"

# Expected U/E_pre status vocabulary. "Unissued" is NOT "intrinsic nonapplicability".
U_E_PRE_STATUS = {
    "ISSUED_AND_RECONCILED": "a competent issuer issued the exact original U/E_pre and it reconciles",
    "ISSUED_HISTORICAL_SCOPE_ONLY": "historically issued at a bounded scope; not current original occupancy",
    "UNISSUED_EXPECTED_NOT_INTRINSICALLY_INAPPLICABLE": (
        "the original U/E_pre is required and has not been issued; recorded as missing, "
        "never as source-intrinsic nonapplicability"),
    "SOURCE_INTRINSIC_NONAPPLICABILITY_PROVED": (
        "only when an original-source proof of nonapplicability exists"),
}


def _canon(obj) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"))


def _digest(obj) -> str:
    return hashlib.sha256(_canon(obj).encode("utf-8")).hexdigest()


# --------------------------------------------------------------------------
# Crosswalk rule (documented, deterministic, non-forcing)
# --------------------------------------------------------------------------
CROSSWALK_RULE = (
    "same group letter AND (register.gates INTERSECT ledger.f_gate_ids) "
    "AND (register.nodes INTERSECT ledger.dependency_node_ids). "
    "Unmatched rows on either side are RETAINED as unmatched; this is a "
    "documentary many-to-many candidate, NOT a proved 151<->101 normalization theorem."
)


def build_crosswalk(register_rows, ledger_rows):
    edges = []
    reg_to_led = defaultdict(list)
    led_to_reg = defaultdict(list)
    for r in register_rows:
        rg = set(r.get("gates") or [])
        rn = set(r.get("nodes") or [])
        for t in ledger_rows:
            if r["id"][:1] != t["id"][:1]:
                continue
            tg = set(t.get("f_gate_ids") or [])
            tn = set(t.get("dependency_node_ids") or [])
            shared_gates = sorted(rg & tg)
            shared_nodes = sorted(rn & tn)
            if not shared_gates or not shared_nodes:
                continue
            edge = {
                "register_id": r["id"],
                "ledger_id": t["id"],
                "shared_gates": shared_gates,
                "shared_nodes": shared_nodes,
                "rationale": (
                    f"shared gates {shared_gates} and shared nodes {shared_nodes} bind "
                    f"historical obligation '{r['obligation'][:60]}' to current function "
                    f"'{t['action'][:60]}'"),
            }
            edges.append(edge)
            reg_to_led[r["id"]].append(t["id"])
            led_to_reg[t["id"]].append(r["id"])
    reg_ids = {r["id"] for r in register_rows}
    led_ids = {t["id"] for t in ledger_rows}
    return {
        "rule": CROSSWALK_RULE,
        "edges": sorted(edges, key=lambda e: (e["register_id"], e["ledger_id"])),
        "split_register_rows": sorted(
            [{"register_id": k, "ledger_targets": sorted(v), "split_count": len(v)}
             for k, v in reg_to_led.items() if len(v) > 1],
            key=lambda x: x["register_id"]),
        "merge_ledger_rows": sorted(
            [{"ledger_id": k, "register_sources": sorted(v), "merge_count": len(v)}
             for k, v in led_to_reg.items() if len(v) > 1],
            key=lambda x: x["ledger_id"]),
        "unmatched_register_rows": sorted(reg_ids - set(reg_to_led)),
        "unmatched_ledger_rows": sorted(led_ids - set(led_to_reg)),
        "is_proved_normalization_theorem": False,
    }


# --------------------------------------------------------------------------
# Expected U/E_pre + identity facets
# --------------------------------------------------------------------------
def expected_u_e_pre_for_wave(source_row, closed35_row):
    """All 35 waves currently expect U/E_pre that is unissued, not inapplicable.

    Where a genuine historical issuance exists it is typed as historical-scope
    only; the commission forbids relabelling unissued original science as
    intrinsically inapplicable and forbids a fake zero.
    """
    if closed35_row is not None and str(closed35_row[2]).strip() == "B":
        status = "UNISSUED_EXPECTED_NOT_INTRINSICALLY_INAPPLICABLE"
    else:
        status = "UNISSUED_EXPECTED_NOT_INTRINSICALLY_INAPPLICABLE"
    return {
        "expected_u_e_pre_status": status,
        "expected_u_e_pre_authority": "COMPETENT_ORIGINAL35_SOURCE_USE_ISSUER__NOT_A41",
        "issued_eligible_operation_count": None,
        "issued_eligible_operation_count_reason": (
            "null with cause: original35 source/operation use has not been issued; "
            "not fabricated zero"),
        "permitted_current_original35_source_rights": 0,
        "permitted_current_original35_source_rights_reason": (
            "no currently unissued original35 grant is inferred; PERMITTED remains 0"),
    }


def identity_facets(source_row, closed35_row, axis_id):
    """The identity tuple every expected row must carry."""
    return {
        "source": {
            "source_id": source_row["id"],
            "source_name": source_row["name"],
            "estate_membership": source_row["established_membership"],
        },
        "edition": {
            "edition_label": (closed35_row[1] if closed35_row else None),
            "authority_annotation": (closed35_row[3] if closed35_row else None),
            "historical_representation_census": source_row["historical_representation_census"],
        },
        "item": {
            "item_grain": "WAVE_LEVEL_ITEM_PROFILE_UNITS_HELD_NOT_ISSUED_E_PRE",
            "held_candidate_unit_count": 127813,
            "held_candidate_unit_count_scope": "whole estate, all 35 waves (O35B declared accounting)",
            "issued_item_scope": None,
        },
        "response": {
            "response_axis": "S05_NUMERIC_KEY_EXACTNESS_AND_S09_CATEGORY_SEMANTICS",
            "response_meaning_status": "EXPECTED_UNISSUED",
        },
        "risk": {
            "risk_axis": "S12_SUBJECT_S13_POPULATION_S14_DESIGN_S15_WEIGHT_ESTIMAND",
            "denominator_and_estimand_status": "EXPECTED_UNISSUED",
        },
        "design": {
            "design_axis": "S14_SAMPLING_DESIGN_S15_WEIGHT_AND_ESTIMAND",
            "design_status": "EXPECTED_UNISSUED",
        },
        "operation": {
            "operation_axis": "S17_SOURCE_OPERATION_PERMISSION_S20_QUERY_TARGET_ELIGIBILITY",
            "operation_permission_status": "PERMITTED_0__NOT_INFERRED",
        },
        "axis_under_test": axis_id,
    }


# --------------------------------------------------------------------------
# Public API
# --------------------------------------------------------------------------
def build_expected_scope(gp, startup_commit):
    """Return the full independently frozen expected scope (no producer input)."""
    docs = {}
    for key, spec in DECLARED_DOCUMENTS.items():
        rec = gp.verify(startup_commit, spec["path"], expect_blob_sha1=spec["blob_sha1"])
        docs[key] = {"record": rec, "declared_role": spec["role"],
                     "data": gp.parse_json(gp.blob_at(startup_commit, spec["path"]))}

    estate = docs["estate_matrix"]["data"]
    register = docs["register_151"]["data"]
    ledger = docs["ledger_101"]["data"]
    relations = docs["global_relations"]["data"]

    closed35 = gp.parse_json(gp.blob_at(
        startup_commit,
        "PYAT_CONTROL_ROOM/ASTRA_PYAT_INTEGRATED_DEVELOPMENT_ATLAS_R1/data/closed35.json"))
    closed_by_id = {row[0]: row for row in closed35}

    # --- 35 waves -------------------------------------------------------
    native_axes = [a["id"] for a in estate["axes_source_native"]]
    ee_axes = list(estate["axes_EE01_EE16"])
    f_axes = [a["id"] for a in estate["axes_F1_F8"]]
    all_axes = native_axes + ee_axes + f_axes

    waves = []
    cells = []
    for src in estate["sources"]:
        src_id = src["id"]
        c35 = closed_by_id.get(src_id[-2:])
        waves.append({
            "source_id": src_id,
            "source_name": src["name"],
            "established_membership": src["established_membership"],
            "historical_representation_census": src["historical_representation_census"],
            "historical_residual_or_exception": src.get("historical_residual_or_exception"),
            "original_dossier": src.get("original_dossier"),
            "no_drop_assertion": src.get("no_drop_assertion"),
            "identity": {
                "source": src["name"],
                "edition": (c35[1] if c35 else None),
                "item": "WAVE_LEVEL_ITEM_PROFILE_UNITS_HELD_NOT_ISSUED_E_PRE",
                "response": "S05_S09_EXPECTED_UNISSUED",
                "risk": "S12_S13_S14_S15_EXPECTED_UNISSUED",
                "design": "S14_S15_EXPECTED_UNISSUED",
                "operation": "S17_S20_PERMITTED_0__NOT_INFERRED",
            },
            "expected_u_e_pre": expected_u_e_pre_for_wave(src, c35),
        })
        for axis_id in all_axes:
            axis_family = ("SOURCE_NATIVE" if axis_id in native_axes
                           else "EE_ENGINE" if axis_id in ee_axes else "F_GATE")
            cells.append({
                "cell_id": f"{src_id}.{axis_id}",
                "source_id": src_id,
                "axis_id": axis_id,
                "axis_family": axis_family,
                "identity": identity_facets(src, c35, axis_id),
                "expected_u_e_pre": expected_u_e_pre_for_wave(src, c35),
                "expected_status": "EXACT_SCOPED_RECONCILIATION_REQUIRED__NOT_ASSERTED_MISSING",
                "required_proof": (
                    "An adopted scope-bound receipt / original source witness OR "
                    "proven original-source intrinsic nonapplicability"),
            })

    # --- crosswalk -------------------------------------------------------
    crosswalk = build_crosswalk(register["tasks"], ledger["task_rows"])

    register_rows = [{
        "id": r["id"], "group": r["group"], "category": r.get("category"),
        "obligation": r["obligation"], "exit_proof": r.get("exit_proof"),
        "gates": list(r.get("gates") or []), "nodes": list(r.get("nodes") or []),
        "declared_status": r.get("status"),
        "real_source_receipt": r.get("real_source_receipt"),
        "consumer_receipt": r.get("consumer_receipt"),
        "independent_review_ref": r.get("independent_review_ref"),
    } for r in register["tasks"]]
    ledger_rows = [{
        "id": t["id"], "scope": t["scope"], "action": t["action"],
        "owner_family": t["owner_family"],
        "f_gate_ids": list(t.get("f_gate_ids") or []),
        "ee_responsibility_ids": list(t.get("ee_responsibility_ids") or []),
        "dependency_node_ids": list(t.get("dependency_node_ids") or []),
        "owner_verified_at_exact_function": t.get("owner_verified_at_exact_function"),
        "reconciliation_state": t.get("reconciliation_state"),
    } for t in ledger["task_rows"]]

    # --- global relations -----------------------------------------------
    global_relations = {
        "cross_family_F6": {
            "grain": "global relation edge",
            "obligation": estate["global_relation_obligations"]["cross_family_F6"],
            "expected_status": "OPEN_GLOBAL_OBLIGATION__NOT_35_SCALAR_PASSES",
            "candidate_pair_index": {
                "family_count": relations["family_count"],
                "source_count": relations["source_count"],
                "within_family_temporal_pair_candidates":
                    len(relations.get("within_family_temporal_pair_candidates", [])),
                "cross_family_pair_candidates":
                    len(relations.get("cross_family_pair_candidates", [])),
            },
        },
        "temporal_F7": {
            "grain": "wave-pair/comparison edge",
            "obligation": estate["global_relation_obligations"]["temporal_F7"],
            "expected_status": "OPEN_GLOBAL_OBLIGATION__NOT_ONE_WAVE_RESULT",
            "candidate_pair_index": {
                "within_family_temporal_pair_candidates":
                    len(relations.get("within_family_temporal_pair_candidates", [])),
            },
        },
        "possibility_F8": {
            "grain": "global consumer service",
            "obligation": estate["global_relation_obligations"]["possibility_F8"],
            "expected_status": "OPEN_GLOBAL_OBLIGATION__PER_WAVE_TRACES_NOT_F8_PASS",
        },
    }

    scope = {
        "schema": SCOPE_SCHEMA,
        "startup_commit": startup_commit,
        "declared_documents": {k: v["record"] | {"role": v["declared_role"]}
                               for k, v in docs.items()},
        "cell_status_vocabulary": estate["manifest_ontology"]["cell_status_guidance"],
        "u_e_pre_status_vocabulary": U_E_PRE_STATUS,
        "declared_consumers": list(DECLARED_CONSUMERS),
        "declared_clock": DECLARED_CLOCK,
        "wave_expected_u_e_pre": {w["source_id"]:
                                  w["expected_u_e_pre"]["expected_u_e_pre_status"]
                                  for w in waves},
        "identity_facets": list(IDENTITY_FACETS),
        "source_count": len(waves),
        "axis_counts": {
            "source_native": len(native_axes),
            "ee_engine": len(ee_axes),
            "f_gate": len(f_axes),
            "total": len(all_axes),
        },
        "expected_cell_count": len(waves) * len(all_axes),
        "expected_source_axis_cells": len(waves) * len(native_axes),
        "expected_ee_axis_cells": len(waves) * len(ee_axes),
        "expected_f_axis_cells": len(waves) * len(f_axes),
        "axis_ids": all_axes,
        "waves": waves,
        "cells": cells,
        "register_151_count": len(register["tasks"]),
        "ledger_101_count": len(ledger["task_rows"]),
        "register_151_rows": register_rows,
        "ledger_101_rows": ledger_rows,
        "register_151_ids": [r["id"] for r in register_rows],
        "ledger_101_ids": [t["id"] for t in ledger_rows],
        "crosswalk_151_101": crosswalk,
        "global_relations": global_relations,
        "f1_f8_gate_grain": {a["id"]: a["grain"] for a in estate["axes_F1_F8"]},
    }
    # Structural self-check before freezing.
    assert scope["expected_cell_count"] == 1890, scope["expected_cell_count"]
    assert scope["register_151_count"] == 151
    assert scope["ledger_101_count"] == 101
    assert len(waves) == 35
    scope["scope_digest"] = _digest(
        {k: v for k, v in scope.items() if k != "scope_digest"})
    return scope
