"""WG0I Phase A — build the independent original35 expected-set oracle.

Derived only from accepted authority at the sealed base and the pinned O35E
35-wave eligible item/operation matrix.  It does not read WG0R output and does
not issue original U/E_pre, source execution or operation permission.
"""
from __future__ import annotations

import collections
import hashlib
import json
import subprocess
from pathlib import Path

R = Path(__file__).resolve().parents[1]
REPO = Path(subprocess.check_output(
    ["git", "rev-parse", "--show-toplevel"], cwd=R, text=True).strip())
BASE = "68873526efe5a39a0849aa401666ac997870f156"
O35E_COMMIT = "30a2ef61230cea4583945493a1ad489f5ab213c5"
O35E_PATH = ("WORKER_RETURNS/PYAT-R28-O35E-ORIGINAL-35-ELIGIBILITY-NATIVE-R1/"
             "01_35_WAVE_ELIGIBLE_ITEM_OPERATION_MATRIX.json")
CRITICAL_GATE = "PYAT_CONTROL_ROOM/WHOLE_MACHINE_COMPLETION_R1/AUTOMATED_WORKLOAD_CONSTRUCTION_CRITICAL_GATE.md"
ESTATE = "PYAT_CONTROL_ROOM/WHOLE_MACHINE_COMPLETION_R1/ESTATE_35X_REQUIREMENTS_MATRIX.json"
TASKS = "PYAT_CONTROL_ROOM/WHOLE_MACHINE_COMPLETION_R1/TASK_LEDGER_101_MACHINE.json"
QUEUE = "PYAT_CONTROL_ROOM/WHOLE_MACHINE_COMPLETION_R1/WAVE35_COMMON_EDGE_ACTION_QUEUE.json"
OUT = R / "phase_a"
STAGE = R / "stage"
STAGE.mkdir(exist_ok=True)


def git_show(ref: str, path: str) -> bytes:
    return subprocess.check_output(["git", "show", ref + ":" + path], cwd=REPO)


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def ids(raw: bytes) -> dict:
    return {"sha256": sha256(raw), "git_blob_sha1":
            hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest(),
            "bytes": len(raw)}


def main() -> None:
    o35e_raw = git_show(O35E_COMMIT, O35E_PATH)
    (STAGE / "o35e_matrix.json").write_bytes(o35e_raw)
    matrix = json.loads(o35e_raw)
    estate_raw = git_show(BASE, ESTATE)
    tasks_raw = git_show(BASE, TASKS)
    queue_raw = git_show(BASE, QUEUE)
    gate_raw = git_show(BASE, CRITICAL_GATE)
    estate = json.loads(estate_raw)
    tasks = json.loads(tasks_raw)
    queue = json.loads(queue_raw)

    waves = matrix["waves"]
    assert len(waves) == 35, len(waves)
    assert [w["atlas_id"] for w in waves] == ["SRC%02d" % i for i in range(1, 36)]
    status_counts = collections.Counter()
    per_wave = []
    ledger = []
    for w in waves:
        items = w.get("items") or []
        assert len(items) == w["qra_row_count"], (w["atlas_id"], len(items), w["qra_row_count"])
        assert sum((w.get("qra_status_counts") or {}).values()) == len(items), w["atlas_id"]
        for it in items:
            st = it["qra_authority_status"]
            status_counts[st] += 1
            ledger.append({
                "wave": w["atlas_id"],
                "question_id": it["question_id"],
                "p2_identity": it["p2_exact_identity_sha256"],
                "governed_hash": it["governed_row_payload_hash"],
                "status": st,
                "topology": (it.get("topology_metadata") or {}).get("p2_response_topology"),
                "operation_eligibility": it["original_item_operation_eligibility"],
            })
        per_wave.append({
            "atlas_id": w["atlas_id"], "label": w["atlas_label"],
            "family": w["canonical_source_family"], "wave": w["canonical_wave"],
            "qra_row_count": w["qra_row_count"], "items": len(items),
            "status_counts": dict(w.get("qra_status_counts") or {}),
            "source_use_status": w["source_use_status"],
            "permission_warrant_ref": w.get("permission_warrant_ref"),
            "competent_original_U_ref": w.get("competent_original_U_ref"),
            "competent_original_E_pre_ref": w.get("competent_original_E_pre_ref"),
            "eligible_original_count": w.get("eligible_original_count"),
            "native_original_runs": w.get("native_original_runs"),
            "sample_risk_design_edition": w.get("sample_risk_design_edition"),
        })
    ledger.sort(key=lambda r: (r["wave"], r["question_id"]))
    ledger_raw = "".join(json.dumps(r, sort_keys=True, separators=(",", ":")) + "\n"
                         for r in ledger).encode()
    ledger_sha = sha256(ledger_raw)
    (OUT / "02_ITEM_IDENTITY_LEDGER.jsonl").write_bytes(ledger_raw)

    assert len(ledger) == 18259, len(ledger)
    assert sum(status_counts.values()) == 18259
    assert status_counts == collections.Counter({
        "GOVERNED_ADMINISTRATIVE_DISPOSITION": 966,
        "GOVERNED_NON_DIRECTIONAL_DISPOSITION": 12611,
        "GOVERNED_QSMV2_RELATION_AUTHORITY": 4397,
        "GOVERNED_MANUAL_RELATION_AUTHORITY": 173,
        "BLOCKED_IDENTITY_OR_AUTHORITY_JOIN": 9,
        "BLOCKED_STRUCTURAL_MAPPING_AUTHORITY": 41,
        "FROZEN_ACCEPTED_GSS": 52,
        "BLOCKED_SOURCE_AUTHORITY": 10,
    }), status_counts

    # Estate axis cells.
    cells = []
    for s in estate["sources"]:
        for key in ("source_native_axes", "empirical_engine_axes", "f1_f8_axes"):
            for a in s.get(key) or []:
                cells.append({"source": s["id"], "axis": a["id"], "status": a["status"]})
    assert len(cells) == 1890, len(cells)
    assert len(estate["sources"]) == 35
    cell_status = collections.Counter(c["status"] for c in cells)

    # 101 tasks and queue.
    task_rows = tasks["task_rows"]
    assert len(task_rows) == 101 and tasks["task_count"] == 101
    task_states = collections.Counter(r["reconciliation_state"] for r in task_rows)
    queue_sources = queue["sources"]
    assert len(queue_sources) == 35
    refs = ["current_complete_qualified_item_inventory_ref",
            "current_auto_authorized_frontier_ref",
            "current_source_backed_all_expected_products_manifest_ref",
            "final_consumer_receipt_ref",
            "source_intrinsic_nonapplicability_receipt_ref"]
    ref_nulls = {r: sum(1 for s in queue_sources if s.get(r) is None) for r in refs}
    assert all(v == 35 for v in ref_nulls.values())

    operation_classes = list(matrix["operation_requirements"].keys())
    operation_defaults = dict(matrix["original_operation_status_default"])
    assert len(operation_classes) == 7
    operation_counts = {op: {"potential": len(ledger), "permitted": 0,
                             "hold": len(ledger), "executed_with_consumer": 0,
                             "default": operation_defaults[op]}
                        for op in operation_classes}

    primary = {
        "SOURCE_INTRINSIC_NONAPPLICABLE": status_counts["GOVERNED_ADMINISTRATIVE_DISPOSITION"]
        + status_counts["GOVERNED_NON_DIRECTIONAL_DISPOSITION"],
        "AUTHORITY_HELD": status_counts["GOVERNED_QSMV2_RELATION_AUTHORITY"]
        + status_counts["GOVERNED_MANUAL_RELATION_AUTHORITY"]
        + status_counts["BLOCKED_IDENTITY_OR_AUTHORITY_JOIN"]
        + status_counts["BLOCKED_STRUCTURAL_MAPPING_AUTHORITY"]
        + status_counts["BLOCKED_SOURCE_AUTHORITY"],
        "EXECUTED_WITH_CONSUMER": status_counts["FROZEN_ACCEPTED_GSS"],
        "PERMITTED": 0,
        "UNDECIDED": 0,
    }
    assert sum(primary.values()) == 18259, primary

    six_labels = {
        "PERMITTED": {"count": 0, "grain": "current original item/operation",
                      "rule": "requires exact competent original U + E_pre + current source-use permission + operation requirement; none observed"},
        "AUTHORITY_HELD": {"count": primary["AUTHORITY_HELD"], "grain": "item primary (blocked/relation authority without current source permission)"},
        "UNDECIDED": {"count": 0, "grain": "item primary status",
                      "note": "all 18,259 items have incomplete option/carrier/route/risk binding, recorded separately as binding incompleteness, not as an undecided authority class"},
        "SOURCE_INTRINSIC_NONAPPLICABLE": {"count": primary["SOURCE_INTRINSIC_NONAPPLICABLE"],
                                            "grain": "item primary at directed measurement-relation grain",
                                            "note": "marginal/structural operations remain HOLD, never auto-permitted"},
        "PRODUCER_PENDING": {"count": 18259, "grain": "current frontier axis (all items)",
                             "rule": "no current complete qualified item inventory / authorized frontier / expected-products manifest / consumer ref for any of 35 sources"},
        "EXECUTED_WITH_CONSUMER": {"count": 52, "grain": "historical frozen GSS accepted relations",
                                   "note": "LiTS-I AS2B adds 8 historical I03 positives outside the O35E matrix; neither is a current all35 prospective proof"},
    }

    oracle = {
        "schema": "PYAT_R37_WG0I_PHASE_A_FROZEN_ORACLE@1",
        "freeze_phase": "BEFORE_WG0R_OUTPUT",
        "sealed_base": BASE,
        "derivation": {
            "o35e_matrix": {"commit": O35E_COMMIT, "path": O35E_PATH, **ids(o35e_raw)},
            "estate_35x": {"path": ESTATE, **ids(estate_raw)},
            "task_ledger_101": {"path": TASKS, **ids(tasks_raw)},
            "wave35_queue": {"path": QUEUE, **ids(queue_raw)},
            "critical_gate": {"path": CRITICAL_GATE, **ids(gate_raw)},
            "r18_correction": "PYAT_CONTROL_ROOM/R18_WG5_WG5I_SCIENTIFIC_SCOPE_CORRECTION_AND_INHERITANCE_RECOGNITION_20261018.md",
            "p10_g1a": "P10_G1A_MANUAL_AUTHORITY_PRESERVATION_RECLOSURE_PASS @ d73907f2a695a10095f9cac08739545aaa844fa7; 65,354 accounting units, 0 unresolved preservation gaps, 76 held states (documentary, not execution-loaded)",
        },
        "source_census": {
            "expected_sources": 35, "observed_sources": len(waves),
            "no_drop_assertion": "atlas_id SRC01..SRC35 exactly once; no source removed for execution convenience",
            "sources": per_wave,
        },
        "item_census": {
            "all_rows": matrix["census"]["all_rows"],
            "active_rows": matrix["census"]["active_rows"],
            "excluded_Asian_W6_rows": matrix["census"]["excluded_Asian_W6_rows"],
            "active_plus_excluded": matrix["census"]["active_rows"] + matrix["census"]["excluded_Asian_W6_rows"],
            "status_counts": dict(status_counts),
            "identity_ledger": {"path": "phase_a/02_ITEM_IDENTITY_LEDGER.jsonl",
                                "rows": len(ledger), "sha256": ledger_sha},
            "claimed_active_18_259_matches_o35e": matrix["census"]["active_rows"] == 18259,
            "claimed_all_18_518_matches": matrix["census"]["all_rows"] == 18518,
            "difference_18_276_spine": {"value": 18276,
                "status": "EXACT_CROSSWALK_REQUIRED__NOT_AN_OMISSION_TO_DELETE",
                "note": "R18: 18,792 structure rows, 18,276 governed implementation spine, 18,259 O35E active rows, 18,413 historical columns are different units; the 17-row O35E-vs-spine delta must be typed, not dropped"},
        },
        "operation_census": {
            "classes": operation_classes, "requirements": matrix["operation_requirements"],
            "defaults": operation_defaults, "counts": operation_counts,
            "potential_rows": len(ledger) * len(operation_classes),
            "permitted": 0, "hold": len(ledger) * len(operation_classes),
            "executed_with_consumer_current": 0,
        },
        "estate_axis_census": {
            "sources": len(estate["sources"]), "cells": len(cells),
            "source_native_expected": 1050, "ee_expected": 560, "f_expected": 280,
            "status_counts": dict(cell_status),
            "cells_per_source": 54,
        },
        "task_census": {"tasks": 101, "state_counts": dict(task_states),
                        "critical_gate_status": tasks["critical_shared_frontier_gate"]["status"],
                        "gate_owner_evidence": tasks["critical_shared_frontier_gate"]["current_owner_evidence"]},
        "queue_census": {"sources": 35, "current_ref_nulls": ref_nulls,
                         "all_current_refs_null": True,
                         "status": queue.get("status")},
        "six_label_census": six_labels,
        "primary_disposition": primary,
        "accepted_positives": {
            "lits_i_as2b": {
                "commit": "923f2c00b6145182a5e2be5038f579845951da19",
                "respondents": 29002, "respondent_events": 58004, "routing_facts": 58004,
                "coordinate_facts": 145010, "weight_facts": 0,
                "i03_executed": 8, "i03_passed": 8, "i03_failed": 0,
                "typed_nonpositive_dispositions": 11, "hostile_pass": 8, "hostile_fail": 0,
                "exact_hashes": {
                    "GovernedC11Projection": "84361298ae702786a3fd1044bf619ffa4fe9ed2877040724386951e9c9d27872",
                    "C11SourceReleaseCandidate": "7f81a222ea2611638d7ce7ac55c695120b57323832e6dc17ff65c1992201659c",
                    "C11LogicalRelease": "e6c954538fa1830820120465a10a6d065b8a18d1e6b7b08d3f863b0917741e26",
                    "C11Repository": "ff8a49d2560fe3cf229f4d5a0f87a14c52d08086a74649968d8c9c9d0225aa77",
                    "ReplayManifest": "6bfe9862abd6f373309ff6f8868f8871948bb9ed397906d880cda6776941a1dd",
                },
                "grain": "HISTORICAL_EXACT_LITS1_I_SOURCE_BACKED_C11_AND_8_I03__NOT_CURRENT_ALL35",
            },
            "gss_frozen_accepted": 52,
            "o35e_test_only_positive": {
                "verdict": "ORIGINAL35_SOURCE_U_E_PRE_HOLD__NATIVE_TESTONLY_POSITIVE",
                "original_source_run": "NOT_EXECUTED__SOURCE_AND_ISSUER_HOLD",
                "new_original_products": 0, "new_U_or_E_pre": False,
                "grain": "TEST_ONLY_NATIVE_POSITIVE__NOT_ORIGINAL_SOURCE_PRODUCT",
            },
            "wvs7": {"status": "ACCEPTED_REAL_SOURCE_ENGINEERING_PRESENT__EXACT_GRAIN_NOT_RECENSUSED_IN_THIS_FREEZE",
                     "pointer": "PRE-MAIN Verkhovod / Trii real-source history"},
        },
        "refusal_cases": [
            {"id": "RF01_missing_eligible_item", "detect": "ledger identity absent", "expected": "RED, no reduction"},
            {"id": "RF02_substituted_same_cardinality", "detect": "identity/p2 hash set mismatch at equal count", "expected": "RED"},
            {"id": "RF03_duplicate_response_options", "detect": "duplicate option/category identity or conflicting topology", "expected": "RED"},
            {"id": "RF04_country_form_split_change", "detect": "country/form/split key mismatch", "expected": "RED"},
            {"id": "RF05_household_person_confusion", "detect": "respondent carrier/role mismatch", "expected": "RED"},
            {"id": "RF06_mr_ranked_repeated_collapse", "detect": "topology/partial-registry conflict or lost multiplicity", "expected": "RED"},
            {"id": "RF07_d62_semantic_shadowing", "detect": "semantic version/qsmv2 hash or source authority mismatch", "expected": "RED"},
            {"id": "RF08_wrong_weight_or_denominator", "detect": "weight/denominator/estimand mismatch; no default weight=1", "expected": "RED"},
            {"id": "RF09_source_version_temporal_change", "detect": "source SHA/edition/version mismatch", "expected": "RED"},
            {"id": "RF10_false_no_change", "detect": "canonical digest/status census differs while claiming no change", "expected": "RED"},
            {"id": "RF11_post_result_frontier_deletion", "detect": "operation/item removed after a positive receipt", "expected": "RED"},
            {"id": "RF12_hidden_unvisited_work", "detect": "active/excluded/35X/queue census mismatch", "expected": "RED"},
        ],
        "counting_logic": {
            "source_formula": "35 atlas sources, exactly once",
            "item_formula": "sum(per-wave items) = 18,259 active; 18,259 + 259 excluded = 18,518 all rows",
            "status_formula": "sum(8 status classes) = 18,259",
            "operation_formula": "18,259 items x 7 operation classes = 127,813 potential rows; PERMITTED=0, HOLD=127,813",
            "estate_formula": "35 sources x 54 axes = 1,890 cells; 1,050 source-native + 560 EE + 280 F",
            "task_formula": "101 task rows; 101 OPEN_EVIDENCE_BINDING",
            "queue_formula": "35 sources x 5 current refs = 175 null refs",
            "primary_formula": "13,577 SOURCE_INTRINSIC_NONAPPLICABLE + 4,630 AUTHORITY_HELD + 52 EXECUTED_WITH_CONSUMER = 18,259",
        },
        "classification_contract": {
            "PERMITTED": "exact competent original U + E_pre + current source-use permission + operation requirement; none in this freeze",
            "AUTHORITY_HELD": "blocked source/identity/structural status or relation authority without current source permission",
            "UNDECIDED": "no item primary status in this matrix; incomplete option/carrier/route/risk binding is recorded separately for all 18,259 items",
            "SOURCE_INTRINSIC_NONAPPLICABLE": "administrative or non-directional source disposition at the directed measurement-relation grain; does not authorize marginal/structural operations",
            "PRODUCER_PENDING": "no current complete qualified item inventory / authorized frontier / expected products manifest / consumer for a source",
            "EXECUTED_WITH_CONSUMER": "exact historical accepted receipt at its own grain; LiTS-I 8 I03 and GSS 52 are not current all35 prospective proof",
        },
        "authority": "SOURCEFREE TEST_ONLY; no original U/E_pre, source execution, model/actor, Field Forge or production right",
    }
    core = json.dumps(oracle, sort_keys=True, separators=(",", ":")).encode()
    oracle["oracle_digest_sha256"] = sha256(core)
    (OUT / "01_PHASE_A_FROZEN_ORACLE.json").write_text(json.dumps(oracle, indent=2) + "\n")
    print(json.dumps({
        "sources": len(waves), "items": len(ledger), "status_counts": dict(status_counts),
        "ledger_sha256": ledger_sha, "oracle_digest": oracle["oracle_digest_sha256"],
        "estate_cells": len(cells), "tasks": len(task_rows),
        "primary": primary, "queue_nulls": ref_nulls,
    }, indent=2))


if __name__ == "__main__":
    main()
