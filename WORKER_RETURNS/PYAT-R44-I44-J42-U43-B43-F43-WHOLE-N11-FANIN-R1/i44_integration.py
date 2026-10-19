"""R44 I44 — actual four-return fan-in into the unchanged A42 N11 assessor.

The integration law:

* the five pinned returns are verified at their exact Git preimages;
* the four R43 returns are executed/bound at their real grades;
* the merged receipt bank is fed into A42's own ``ingest_r41_bank`` and the
  whole estate is re-assessed by A42's own ``assess_v2``/``artifacts``;
* the I44 overlay only corrects labels A42 could not know (J42 returned after
  A42 was authored) and appends integration provenance. It never changes a
  cell, grade, tally, verdict or the measured occupancy;
* the S44 socket is exercised separately and never contributes to the real
  artifacts;
* original measured occupancy must remain 0.

No source, model, actor, N11 or N12 authority is created here.
"""
from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from pathlib import Path
from typing import Any, Mapping, Sequence

import bootstrap

PIN_PATHS = bootstrap.ensure_inputs()
bootstrap.ensure_sys_path()

from a42 import core as a42core  # noqa: E402  (unchanged A42 assessor)
from frozen_a41.a41.gitpreimage import GitPreimage, PreimageError  # noqa: E402

RETURN_DIR = bootstrap.RETURN_DIR
ROOT = bootstrap.ROOT
ARTIFACTS = RETURN_DIR / "artifacts"
EVIDENCE = RETURN_DIR / "evidence"

I44_STARTUP = "2e5a8693b2b48df5b2e1281e1d33ff2d5d5d2d2c"
A42_COMMIT = bootstrap.PINS["A42"]["commit"]

F43_IMPL_COMMIT = "4fb2058e57291610e23eca1af7f0b27c6730eba8"

# Files actually consumed from each return; every one is preimage-verified.
CONSUMED: dict[str, tuple[str, ...]] = {
    "J42": (
        "00_RETURN.md",
        "01_FROZEN_JOIN_PLAN.json",
        "n11_actual_join_handback.json",
        "n9_n10e_n10w_real_joined_consumer_receipts.json",
        "sourcefree_vs_retained_scientific_grade_matrix.json",
        "actual_e41_w41_p41_joint_dependency_manifest.json",
        "artifact_manifest.json",
        "evidence/j42-suite.xml",
        "evidence/j42_scientific_projection.sha256",
        "evidence/witness-test_j42_join_core.json",
        "evidence/witness-test_j42_breadth_oracle.json",
        "runtime/j42_join.py",
        "runtime/j42_build.py",
        "tests/test_j42_join_core.py",
        "tests/test_j42_join_core.py.proof.json",
        "tests/test_j42_breadth_oracle.py",
        "tests/test_j42_breadth_oracle.py.proof.json",
        "tests/test_j42_cold_replay.py",
    ),
    "U43": (
        "00_RETURN.md",
        "ARTIFACT_MANIFEST.json",
        "A42_151_101_and_81_owner_demands.json",
        "B43_A42_HANDOFF.json",
        "CONSUMER_BACKWARD_NATIVE_GRAPH.json",
        "RUN_ORIGINAL_SOURCE.md",
        "original35_wave_execution_manifest.json",
        "original35_issuer_decision_packets.json",
        "currently_permitted_native_manifests.json",
        "source_wave_item_operation_frontier.jsonl.gz",
        "WG0R_INPUT_FREEZE.json",
        "PREIMPLEMENTATION_FREEZE.json",
        "evidence/VERIFICATION.json",
        "evidence/wg0l_descriptor_repaired.xml",
        "evidence/wg0l_baseline.xml",
        "evidence/current_p10_descriptor_repair.diff",
        "evidence/wg0p4_descriptor_repair.diff",
        "evidence/cold_identity_comparison.json",
        "tests/test_descriptor_refusal.py",
        "tests/test_frontier.py",
        "tests/test_issued_workload.py",
        "tests/test_issued_workload.py.proof.json",
    ),
    "B43": (
        "00_RETURN.md",
        "b43/admission.py",
        "b43/feeder.py",
        "b43/frontier.py",
        "b43/cli.py",
        "b43_source_frontier.json",
        "b43_source_owner_decision_docket.json",
        "b43_wg0l_repair_receipt.json",
        "b43_a42_source_grade_delta.json",
        "b43_a42_v2_estate_acceptance_manifest.json",
        "b43_a42_v2_f1_f8_acceptance_matrix.json",
        "b43_a42_v2_final_maturity_adjudication.md",
        "tests/test_b43_frontier_feeder.py",
        "tests/test_b43_frontier_feeder.py.proof.json",
        "tests/test_b43_a42_delta.py",
        "source_manifest.json",
    ),
    "F43": (
        "00_RETURN.md",
        "A42_HAND_BACK.md",
        "A42_RECEIPT_BANK.json",
        "a42_intake.py",
        "a42_dependency_manifest.json",
        "world_products.json",
        "output_grades.json",
        "bounded_methods.py",
        "f43_product.py",
        "cell_envelope_bounds.py",
        "00_EXPECTED_WORLD_FREEZE.json",
        "01_METHOD_ORACLE.json",
        "original35_f5_f7_acceptance_cells.json",
        "finite_source_and_method_decisions.json",
        "tests/test_bounded_world.py",
        "tests/test_bounded_world.py.proof.json",
        "evidence/a42_native_intake.json",
        "evidence/proof_witness.json",
        "evidence/cold_replay.json",
    ),
    "A42": (
        "00_RETURN.md",
        "a42/__init__.py",
        "a42/core.py",
        "a42/cli.py",
        "frozen_a41/a41/__init__.py",
        "frozen_a41/a41/estate_assessor.py",
        "frozen_a41/a41/expected_scope.py",
        "frozen_a41/a41/gitpreimage.py",
        "frozen_a41/a41/n11_artifacts.py",
        "frozen_a41/a41/receipt_bank.py",
        "frozen_a41/evidence/expected_scope_frozen.json",
        "frozen_a41/evidence/receipt_bank_frozen.json",
        "evidence/r41_receipt_bank_v2.json",
        "f1_f8_acceptance_matrix.json",
        "estate_acceptance_manifest.json",
        "final_maturity_adjudication.md",
        "n11_r41_return_intake_and_delta.json",
        "tests/test_a42_assessor.py",
        "tests/test_a42_falsifiers.py",
        "tests/test_a42_scope_intake.py",
        "evidence/logs/a42_four_edge_witness.json",
    ),
}

EXPECTED_MERGED_RECEIPT_IDS = (
    "E41-SOURCEFREE-INTEGRATED",
    "W41-RETAINED-GT2-J04",
    "W41-SOURCEFREE-INTEGRATED",
    "P41-SOURCEFREE-INTEGRATED",
    "F43-RETAINED-F5-CONTEXT",
    "F43-BOUNDED-F6-CANDIDATE",
    "F43-TEMPORAL-CANDIDATE",
    "F43-ORIGINAL-E04-TEST",
    "J42-JOINED-E41-W41-P41-NATIVE",
    "U43-ORIGINAL35-FRONTIER-AND-DESCRIPTOR-REPAIR",
    "B43-SELECTED-B-SOURCE-FEEDER",
)


def canonical(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def verify_pins(gp: GitPreimage | None = None) -> dict[str, Any]:
    gp = gp or GitPreimage(ROOT)
    report = {}
    for name, files in CONSUMED.items():
        commit = bootstrap.PINS[name]["commit"]
        if not gp.commit_exists(commit):
            raise PreimageError(f"PIN_COMMIT_MISSING:{name}:{commit}")
        checked = [gp.verify(commit, bootstrap.PINS[name]["dir"] + "/" + path) for path in files]
        report[name] = {
            "commit": commit,
            "file_count": len(checked),
            "total_bytes": sum(record["bytes"] for record in checked),
        }
    module = bootstrap.U43_ISSUED_WORKLOAD
    gp.verify(module["commit"], module["path"])
    report["U43_ISSUED_WORKLOAD_MODULE"] = {
        "commit": module["commit"],
        "path": module["path"],
        "file_count": 1,
    }
    return report


def _artifacts(gp: GitPreimage, name: str) -> list[dict[str, Any]]:
    commit = bootstrap.PINS[name]["commit"]
    prefix = bootstrap.PINS[name]["dir"] + "/"
    return [gp.verify(commit, prefix + path) for path in CONSUMED[name]]


# ---------------------------------------------------------------------------
# receipt construction for the four R43 returns
# ---------------------------------------------------------------------------


def build_j42_receipt(gp: GitPreimage) -> dict[str, Any]:
    handback = json.loads(
        gp.blob_at(
            bootstrap.PINS["J42"]["commit"],
            bootstrap.PINS["J42"]["dir"] + "/n11_actual_join_handback.json",
        )
    )
    expected = handback["expected_vs_consumed"]
    if not (expected["no_drop"] and expected["consumed_views"] == expected["expected_views"] == 84):
        raise PreimageError("J42_HANDBACK_NO_DROP_NOT_VERIFIED")
    return {
        "receipt_id": "J42-JOINED-E41-W41-P41-NATIVE",
        "origin_commit": bootstrap.PINS["J42"]["commit"],
        "claim_id": handback["claim_id"],
        "grade": "SOURCEFREE_INTEGRATED_POSITIVE",
        "coverage": {
            "wave_ids": [],
            "axis_ids": [],
            "f_gate_ids": [],
            "functional_gates": ["F1", "F2", "F3", "F4", "F8"],
            "register_151_ids": [],
            "ledger_101_ids": [],
            "global_relations": [],
            "global_contributions": ["possibility_F8"],
            "occupancy_grain_note": (
                "Actual same-source E41×W41×P41 joined PRE-V3 consumer; TEST_ONLY, "
                "zero original35 occupancy"
            ),
        },
        "currentness": {
            "archive_or_current": "ARCHIVE",
            "as_of": "2026-10-19",
            "note": "sourcefree TEST_ONLY joined execution; no current source claim",
        },
        "artifacts": _artifacts(gp, "J42"),
        "unknown_bounds": {
            "original_measured_occupancy": 0,
            "cross_source_join": "TYPED_HELD",
            "f6_transport": "HELD",
            "n9_purpose_admission": "HELD",
            "independent_joint_acceptance": "PENDING",
        },
        "downstream_consumer_read_refs": ["product.nonparent.consume"],
    }


def build_u43_receipt(gp: GitPreimage) -> dict[str, Any]:
    handoff = json.loads(
        gp.blob_at(
            bootstrap.PINS["U43"]["commit"],
            bootstrap.PINS["U43"]["dir"] + "/B43_A42_HANDOFF.json",
        )
    )
    frontier = handoff["frontier"]
    if frontier["research_identities"] != 18285 or frontier["waves"] != 35:
        raise PreimageError("U43_FRONTIER_IDENTITY_MISMATCH")
    if frontier["original_U_count"] is not None or frontier["eligible_E_pre_count"] is not None:
        raise PreimageError("U43_NULL_U_EPRE_WAS_FABRICATED")
    return {
        "receipt_id": "U43-ORIGINAL35-FRONTIER-AND-DESCRIPTOR-REPAIR",
        "origin_commit": bootstrap.PINS["U43"]["commit"],
        "claim_id": (
            "U43 18,285 retained research identities + issuer-bound descriptor transport + "
            "WG0L descriptor repair; original U/E_pre and source execution UNISSUED"
        ),
        "grade": "DOCUMENTARY_IDENTITY_RECONCILIATION",
        "coverage": {
            "wave_ids": [],
            "axis_ids": [],
            "f_gate_ids": [],
            "functional_gates": [],
            "register_151_ids": [],
            "ledger_101_ids": [],
            "global_relations": [],
            "global_contributions": [],
            "occupancy_grain_note": (
                "Research identity/documentary frontier only; no acceptance cell occupation"
            ),
        },
        "currentness": {
            "archive_or_current": "ARCHIVE",
            "as_of": "2026-10-19",
            "note": "retained frontier; no current original source execution",
        },
        "artifacts": _artifacts(gp, "U43"),
        "unknown_bounds": {
            "original_u_count": None,
            "eligible_e_pre_count": None,
            "original_measured_occupancy": 0,
            "research_identities": frontier["research_identities"],
            "hard_fail_flags": frontier["WG0R_hard_fail_flags"],
            "routing_required_flags": frontier["WG0R_route_predicate_required_flags"],
            "issuer_decisions": frontier["exact_owner_decisions"],
            "source_specific_packets": frontier["source_specific_issuer_packets"],
        },
    }


def build_b43_receipt(gp: GitPreimage) -> dict[str, Any]:
    import sys

    if str(bootstrap.path_for("B43")) not in sys.path:
        sys.path.insert(0, str(bootstrap.path_for("B43")))
    from b43 import feeder as b43feeder
    from b43 import frontier as b43frontier

    frontier = b43frontier.load_frontier(gp)
    docket = b43frontier.decision_docket(frontier)
    base = b43feeder.b43_a42_receipt(frontier, docket)
    receipt = deepcopy(base)
    receipt["origin_commit"] = bootstrap.PINS["B43"]["commit"]
    receipt["artifacts"] = _artifacts(gp, "B43")
    receipt["unknown_bounds"] = {
        **base["unknown_bounds"],
        "a42_feeder_receipt_augmented_by": "I44_PINNED_ARTIFACT_CUSTODY",
        "source_grant_present": False,
    }
    return receipt


def build_f43_bank(gp: GitPreimage) -> dict[str, Any]:
    import sys

    f43_root = bootstrap.path_for("F43")
    if str(f43_root) not in sys.path:
        sys.path.insert(0, str(f43_root))
    import a42_intake as f43_intake

    rebuilt = f43_intake.make_bank(F43_IMPL_COMMIT)
    committed = json.loads(
        gp.blob_at(
            bootstrap.PINS["F43"]["commit"],
            bootstrap.PINS["F43"]["dir"] + "/A42_RECEIPT_BANK.json",
        )
    )
    if canonical(rebuilt) != canonical(committed):
        raise PreimageError("F43_BANK_REBUILD_DIFFERS_FROM_COMMITTED_PREIMAGE")
    return rebuilt


def assert_receipt_set(receipt_ids: Sequence[str]) -> None:
    """No-drop: the merged workload must equal the independently frozen set."""

    ids = tuple(receipt_ids)
    if ids != EXPECTED_MERGED_RECEIPT_IDS:
        raise PreimageError(
            "MERGED_BANK_RECEIPT_SET_DIFFERS:"
            + ",".join(sorted(set(ids) ^ set(EXPECTED_MERGED_RECEIPT_IDS)))
        )


def merged_bank(
    base_bank: Mapping[str, Any],
    f43_bank: Mapping[str, Any],
    j42: Mapping[str, Any],
    u43: Mapping[str, Any],
    b43: Mapping[str, Any],
) -> dict[str, Any]:
    receipts = list(base_bank["receipts"]) + list(f43_bank["receipts"]) + [j42, u43, b43]
    ids = [r["receipt_id"] for r in receipts]
    if len(ids) != len(set(ids)):
        raise PreimageError("DUPLICATE_RECEIPT_ID_IN_MERGED_BANK")
    assert_receipt_set(ids)
    return {
        "schema": "A42_RECEIPT_BANK@3.0.0_I44_MERGED",
        "base_bank_schema": base_bank.get("schema"),
        "i44_startup": I44_STARTUP,
        "pins": {name: pin["commit"] for name, pin in bootstrap.PINS.items()},
        "receipt_order_law": "base A42 R41 bank + F43 four + J42 + U43 + B43",
        "receipts": receipts,
        "full_original_product_complete": False,
    }


# ---------------------------------------------------------------------------
# A42 assessment + I44 overlay
# ---------------------------------------------------------------------------


def assess(
    bank: Mapping[str, Any],
    *,
    gp: GitPreimage | None = None,
    scope_override: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    gp = gp or GitPreimage(ROOT)
    scope = deepcopy(scope_override) if scope_override is not None else a42core.load_scope(gp)
    a41 = a42core.a41_receipts_v2(gp)
    r41 = a42core.ingest_r41_bank(bank, gp, scope)
    receipts = a41 + r41
    w41reg = a42core.load_w41_register(gp)
    old_manifest = json.loads(
        gp.blob_at(a42core.A41_COMMIT, a42core.A41_DIR + "/estate_acceptance_manifest.json")
    )
    acc = a42core.assess_v2(scope, receipts, w41reg, old_manifest)
    meta = [
        {
            "receipt_id": r["receipt_id"],
            "grade": r["grade"],
            "origin_commit": r["origin_commit"],
            "claim_id": r["claim_id"],
            "source_return": _source_return(r["receipt_id"]),
        }
        for r in r41
    ]
    f1f8, manifest, md, intake, wake, j42endpoint = a42core.artifacts(
        acc, scope, old_manifest, meta
    )
    return {
        "scope": scope,
        "a41_receipt_count": len(a41),
        "r41_receipt_count": len(r41),
        "receipts": receipts,
        "acc": acc,
        "f1_f8": f1f8,
        "manifest": manifest,
        "md": md,
        "intake": intake,
        "wake": wake,
        "j42_endpoint": j42endpoint,
        "old_manifest": old_manifest,
    }


def _source_return(receipt_id: str) -> str:
    if receipt_id.startswith("E41") or receipt_id.startswith("W41") or receipt_id.startswith("P41"):
        return "A42_BASE_R41_BANK"
    if receipt_id.startswith("F43"):
        return "F43_R43"
    if receipt_id.startswith("J42"):
        return "J42_R42"
    if receipt_id.startswith("U43"):
        return "U43_R43"
    if receipt_id.startswith("B43"):
        return "B43_R43"
    return "UNKNOWN"


def apply_i44_overlay(result: Mapping[str, Any], pins_report: Mapping[str, Any]) -> dict[str, Any]:
    """Correct post-A42 labels and add provenance; never touch numbers or grades."""

    f1f8 = deepcopy(result["f1_f8"])
    manifest = deepcopy(result["manifest"])
    intake = deepcopy(result["intake"])
    wake = deepcopy(result["wake"])
    md = result["md"]
    j42endpoint = deepcopy(result["j42_endpoint"])
    acc = result["acc"]

    j42_state = "INTEGRATED_ACTUAL_NATIVE_JOINED_RETURN__SOURCEFREE_TESTONLY"
    integration = {
        "schema": "I44_FOUR_RETURN_NATIVE_FANIN@1",
        "startup": I44_STARTUP,
        "pins": {name: pin["commit"] for name, pin in bootstrap.PINS.items()},
        "pins_verified": pins_report,
        "merged_receipt_ids": list(EXPECTED_MERGED_RECEIPT_IDS),
        "new_receipts": {
            "J42": "J42-JOINED-E41-W41-P41-NATIVE",
            "U43": "U43-ORIGINAL35-FRONTIER-AND-DESCRIPTOR-REPAIR",
            "B43": "B43-SELECTED-B-SOURCE-FEEDER",
            "F43": [
                "F43-RETAINED-F5-CONTEXT",
                "F43-BOUNDED-F6-CANDIDATE",
                "F43-TEMPORAL-CANDIDATE",
                "F43-ORIGINAL-E04-TEST",
            ],
        },
        "assessor": {
            "owner": "A42 unchanged a42.core",
            "commit": A42_COMMIT,
            "module": str(Path(a42core.__file__).relative_to(ROOT)),
            "intake_function": "a42.core.ingest_r41_bank",
            "assessment_function": "a42.core.assess_v2",
            "artifacts_function": "a42.core.artifacts",
        },
        "overlay_law": (
            "I44 corrects only labels A42 could not know (J42 returned after A42 was "
            "authored) and appends provenance; verdict, tallies, cells, grades, global "
            "relations, 151/101/81 and measured occupancy are A42's own values."
        ),
        "original_measured_occupancy": acc["verdict"]["original_measured_occupied_cells"],
        "n11_state": acc["verdict"]["n11_state"],
        "s44_receiving_interface": "s44_adoption_socket.S44_CURRENT_SOURCE_POSITIVE_RECEIPT@1",
        "j42_return_commit": bootstrap.PINS["J42"]["commit"],
    }

    f1f8["j42_state"] = j42_state
    f1f8["i44_integration"] = {
        key: integration[key]
        for key in ("schema", "startup", "assessor", "overlay_law", "original_measured_occupancy")
    }
    manifest["j42_state"] = j42_state
    manifest["i44_integration"] = integration
    intake["j42_state"] = j42_state
    intake["i44_merged_receipts"] = integration["merged_receipt_ids"]
    intake["i44_new_receipts"] = integration["new_receipts"]
    intake["i44_assessor"] = integration["assessor"]
    intake["i44_overlay_law"] = integration["overlay_law"]
    intake["i44_a42_base_receipts"] = result["a41_receipt_count"] + 4
    intake["i44_merged_receipt_count"] = result["a41_receipt_count"] + result["r41_receipt_count"]
    j42endpoint = {
        "schema": "PYAT_A42_J42_ENDPOINT@2",
        "artifact": "j42_addon_endpoint.json",
        "state": "INTEGRATED_ACTUAL_NATIVE_JOINED_RETURN__SOURCEFREE_TESTONLY",
        "return_commit": bootstrap.PINS["J42"]["commit"],
        "receipt_id": "J42-JOINED-E41-W41-P41-NATIVE",
        "contract": "J42_JOINED_E41_W41_P41_PREV3_CONSUMER@1",
        "coverage": {"views": 84, "e04_receipts": 84, "p41_receipts": 84, "progressive_steps": 252},
        "grade": "SOURCEFREE_INTEGRATED_POSITIVE",
        "original35_state": "UNISSUED_HELD",
        "counted_as_original_occupancy": False,
    }
    pending_sentence = "J42 remains a pending physical return."
    if pending_sentence in md:
        md = md.replace(
            pending_sentence,
            "J42 is integrated as a real sourcefree TEST_ONLY joined return "
            f"(`{bootstrap.PINS['J42']['commit']}`); it adds no original occupancy.",
        )
    md += (
        "\n## I44 four-return native fan-in (R44)\n\n"
        f"- I44 startup: `{I44_STARTUP}`\n"
        f"- J42: `{bootstrap.PINS['J42']['commit']}` — integrated joined E41×W41×P41 "
        "sourcefree TEST_ONLY consumer (84 views, 84 E04 + 84 P41 receipts, 252 steps).\n"
        f"- U43: `{bootstrap.PINS['U43']['commit']}` — 18,285 retained research identities, "
        "35 source packets / 175 decisions, descriptor repair; original U/E_pre NULL.\n"
        f"- B43: `{bootstrap.PINS['B43']['commit']}` — executable selected-B feeder, "
        "issuer-bound admission, all35 source-pending; measured output 0.\n"
        f"- F43: `{bootstrap.PINS['F43']['commit']}` — four bounded A42 receipts "
        "(SRC02.F5 retained, F6/F7 candidate methods, original E04 TEST_ONLY).\n"
        "- A42 is the unchanged assessor; the I44 overlay only corrects the stale "
        "J42-pending label and records provenance.\n"
        "- **Original measured occupancy remains 0. Global F6/F7/F8 remain open. "
        "N11 remains NOT_READY. N12 remains HOLD.**\n"
        "- S44 receiving interface is executable; no S44 source-positive receipt exists.\n"
    )
    return {
        "f1_f8": f1f8,
        "manifest": manifest,
        "md": md,
        "intake": intake,
        "wake": wake,
        "j42_endpoint": j42endpoint,
        "integration": integration,
    }


def terminal_delta(base: Mapping[str, Any], merged: Mapping[str, Any]) -> dict[str, Any]:
    b = base["acc"]["verdict"]
    m = merged["acc"]["verdict"]
    return {
        "schema": "I44_TERMINAL_COMPLETION_DELTA@1",
        "base_a42": {
            "receipts": base["a41_receipt_count"] + base["r41_receipt_count"],
            "original_measured": b["original_measured_occupied_cells"],
            "missing_expected": b["missing_expected_cells"],
            "historical_or_retained": b["historical_or_retained_cells"],
            "functional": {g: v["functional_grade"] for g, v in base["acc"]["functional_maturity"].items()},
            "j42_state": "PENDING_PHYSICAL_RETURN",
        },
        "i44_merged": {
            "receipts": merged["a41_receipt_count"] + merged["r41_receipt_count"],
            "original_measured": m["original_measured_occupied_cells"],
            "missing_expected": m["missing_expected_cells"],
            "historical_or_retained": m["historical_or_retained_cells"],
            "functional": {g: v["functional_grade"] for g, v in merged["acc"]["functional_maturity"].items()},
            "j42_state": "INTEGRATED_SOURCEFREE_TESTONLY",
        },
        "delta": {
            "receipts": (merged["a41_receipt_count"] + merged["r41_receipt_count"])
            - (base["a41_receipt_count"] + base["r41_receipt_count"]),
            "original_measured_cells": m["original_measured_occupied_cells"]
            - b["original_measured_occupied_cells"],
            "missing_expected_cells": m["missing_expected_cells"] - b["missing_expected_cells"],
            "historical_or_retained_cells": m["historical_or_retained_cells"]
            - b["historical_or_retained_cells"],
            "functional_grade_changes": {
                g: {"before": base["acc"]["functional_maturity"][g]["functional_grade"],
                    "after": merged["acc"]["functional_maturity"][g]["functional_grade"]}
                for g in ("F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8")
                if base["acc"]["functional_maturity"][g]["functional_grade"]
                != merged["acc"]["functional_maturity"][g]["functional_grade"]
            },
        },
        "classification": "EVIDENCE_BREADTH_AND_INTEGRATION__NO_ESTATE_OCCUPANCY_DELTA",
        "terminal_statement": (
            "The four R43 returns are actually bound into A42 at their real grades. "
            "No original measured cell, global F6/F7/F8 closure, N11 acceptance or "
            "N12 wake is created. Original35 U/E_pre remains unissued."
        ),
    }


# ---------------------------------------------------------------------------
# artifact emission
# ---------------------------------------------------------------------------


def _write_json(path: Path, payload: Any) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    path.write_text(text, encoding="utf-8")
    return sha256_bytes(text.encode("utf-8"))


def emit(
    merged: Mapping[str, Any],
    overlay: Mapping[str, Any],
    delta: Mapping[str, Any],
    bank: Mapping[str, Any],
    s44_report: Mapping[str, Any],
    out_dir: Path = ARTIFACTS,
) -> dict[str, str]:
    out_dir.mkdir(parents=True, exist_ok=True)
    hashes = {}
    hashes["f1_f8_acceptance_matrix.json"] = _write_json(
        out_dir / "f1_f8_acceptance_matrix.json", overlay["f1_f8"]
    )
    hashes["estate_acceptance_manifest.json"] = _write_json(
        out_dir / "estate_acceptance_manifest.json", overlay["manifest"]
    )
    md_text = overlay["md"]
    (out_dir / "final_maturity_adjudication.md").write_text(md_text, encoding="utf-8")
    hashes["final_maturity_adjudication.md"] = sha256_bytes(md_text.encode("utf-8"))
    hashes["n11_r43_fanin_intake_and_delta.json"] = _write_json(
        out_dir / "n11_r43_fanin_intake_and_delta.json", overlay["intake"]
    )
    hashes["i44_terminal_completion_delta.json"] = _write_json(
        out_dir / "i44_terminal_completion_delta.json", delta
    )
    hashes["j42_addon_endpoint.json"] = _write_json(
        out_dir / "j42_addon_endpoint.json", overlay["j42_endpoint"]
    )
    hashes["original35_source_positive_execution_wake_packet.json"] = _write_json(
        out_dir / "original35_source_positive_execution_wake_packet.json", overlay["wake"]
    )
    hashes["merged_receipt_bank_i44.json"] = _write_json(
        out_dir / "merged_receipt_bank_i44.json", bank
    )
    hashes["s44_receiving_interface_report.json"] = _write_json(
        out_dir / "s44_receiving_interface_report.json", s44_report
    )
    return hashes


def build_all() -> dict[str, Any]:
    pins_report = verify_pins()
    gp = GitPreimage(ROOT)
    a42_bank_raw = gp.blob_at(
        A42_COMMIT,
        bootstrap.PINS["A42"]["dir"] + "/evidence/r41_receipt_bank_v2.json",
    )
    base_bank = json.loads(a42_bank_raw)
    base = assess(base_bank, gp=gp)
    f43_bank = build_f43_bank(gp)
    j42 = build_j42_receipt(gp)
    u43 = build_u43_receipt(gp)
    b43 = build_b43_receipt(gp)
    bank = merged_bank(base_bank, f43_bank, j42, u43, b43)
    merged = assess(bank, gp=gp)
    overlay = apply_i44_overlay(merged, pins_report)
    delta = terminal_delta(base, merged)
    from s44_adoption_socket import socket_report

    s44_report = socket_report(merged["scope"])
    return {
        "pins": pins_report,
        "base": base,
        "base_bank": base_bank,
        "f43_bank": f43_bank,
        "j42": j42,
        "u43": u43,
        "b43": b43,
        "bank": bank,
        "merged": merged,
        "overlay": overlay,
        "delta": delta,
        "s44": s44_report,
    }


def run_all() -> dict[str, Any]:
    built = build_all()
    pins_report = built["pins"]
    base = built["base"]
    merged = built["merged"]
    overlay = built["overlay"]
    delta = built["delta"]
    bank = built["bank"]
    s44_report = built["s44"]
    hashes = emit(merged, overlay, delta, bank, s44_report)
    return {
        "schema": "I44_RUN_REPORT@1",
        "pins": pins_report,
        "base_verdict": base["acc"]["verdict"],
        "merged_verdict": merged["acc"]["verdict"],
        "merged_receipt_count": merged["a41_receipt_count"] + merged["r41_receipt_count"],
        "delta": delta,
        "s44": {
            "state": s44_report["state"],
            "refusal_codes": s44_report["refusal_codes"],
            "synthetic_witness_counted_in_real_artifacts": False,
        },
        "artifact_sha256": hashes,
        "blended": sha256_bytes(canonical(hashes).encode("utf-8")),
    }


if __name__ == "__main__":
    print(json.dumps(run_all(), indent=2, sort_keys=True))
