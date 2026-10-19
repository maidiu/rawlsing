"""R44 I44 native integration courts.

Named fault-witness positives for ``test_i44_integration.py.proof.json``:

* ``test_no_drop_removed_j42_receipt_is_detected`` — the independently frozen
  merged receipt set must include and execute J42; dropping it is detected;
* ``test_false_sourcegrade_promotion_is_refused`` — the I44 path must not
  launder A42's exact false-original-promotion refusal;
* ``test_u43_b43_compiled_adapter_refuses_forged_descriptor`` — B43's
  issuer-bound frontend must refuse a forged U43 descriptor with zero native calls.
"""
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import sys

import pytest

RETURN_DIR = Path(__file__).resolve().parent
if str(RETURN_DIR) not in sys.path:
    sys.path.insert(0, str(RETURN_DIR))

import bootstrap  # noqa: E402

bootstrap.ensure_inputs()
bootstrap.ensure_sys_path()

import i44_integration as i44  # noqa: E402
import s44_adoption_socket as s44  # noqa: E402
import u43_b43_adapter as adapter  # noqa: E402
from a42 import core as a42core  # noqa: E402
from b43.admission import B43AdmissionDenied  # noqa: E402
from frozen_a41.a41.gitpreimage import GitPreimage, PreimageError  # noqa: E402
from rawlsing_next import pre553_issued_workload as u43  # noqa: E402

J42_RECEIPT = "J42-JOINED-E41-W41-P41-NATIVE"


@pytest.fixture(scope="module")
def built():
    return i44.build_all()


def _bank_with(built, receipt):
    return {**built["bank"], "receipts": [receipt]}


# ---------------------------------------------------------------------------
# pins, assessor identity, receipt intake
# ---------------------------------------------------------------------------


def test_pins_and_all_twenty_receipts_are_preimage_verified(built):
    pins = built["pins"]
    assert set(pins) == {"A42", "J42", "U43", "B43", "F43", "U43_ISSUED_WORKLOAD_MODULE"}
    for name in ("A42", "J42", "U43", "B43", "F43"):
        assert pins[name]["commit"] == bootstrap.PINS[name]["commit"]
        assert pins[name]["file_count"] >= 16
    assert built["base"]["a41_receipt_count"] + built["base"]["r41_receipt_count"] == 13
    assert built["merged"]["a41_receipt_count"] + built["merged"]["r41_receipt_count"] == 20
    assert [r["receipt_id"] for r in built["bank"]["receipts"]] == list(
        i44.EXPECTED_MERGED_RECEIPT_IDS
    )


def test_unmodified_a42_assessor_owns_the_result(built):
    assert Path(a42core.__file__).resolve() == (
        bootstrap.path_for("A42") / "a42" / "core.py"
    ).resolve()
    integration = built["overlay"]["integration"]
    assert integration["assessor"]["intake_function"] == "a42.core.ingest_r41_bank"
    assert integration["assessor"]["assessment_function"] == "a42.core.assess_v2"
    assert integration["assessor"]["artifacts_function"] == "a42.core.artifacts"
    # The base run reproduces the committed A42 candidate exactly.
    gp = GitPreimage(bootstrap.ROOT)
    committed = json.loads(
        gp.blob_at(
            bootstrap.PINS["A42"]["commit"],
            bootstrap.PINS["A42"]["dir"] + "/estate_acceptance_manifest.json",
        )
    )
    base = built["base"]["acc"]["verdict"]
    for key in (
        "n11_state",
        "original_measured_occupied_cells",
        "missing_expected_cells",
        "historical_or_retained_cells",
        "unmatched_still_unresolved",
        "total_cells",
    ):
        assert base[key] == committed["verdict"][key], key


# ---------------------------------------------------------------------------
# the four returns at their real grades
# ---------------------------------------------------------------------------


def test_j42_joined_receipt_is_integrated_and_not_original(built):
    receipt = built["j42"]
    assert receipt["receipt_id"] == J42_RECEIPT
    assert receipt["origin_commit"] == bootstrap.PINS["J42"]["commit"]
    assert receipt["grade"] == "SOURCEFREE_INTEGRATED_POSITIVE"
    assert receipt["coverage"]["wave_ids"] == []
    assert set(receipt["coverage"]["functional_gates"]) == {"F1", "F2", "F3", "F4", "F8"}
    assert built["merged"]["acc"]["verdict"]["original_measured_occupied_cells"] == 0
    # J42 never appears as original evidence on any cell.
    for cell in built["merged"]["acc"]["cells"]:
        if any(e["receipt_id"] == J42_RECEIPT for e in cell["actual_evidence"]):
            assert cell["consumed_grade"] != "ORIGINAL_MEASURED_OCCUPANCY"


def test_f43_four_receipts_are_ingested(built):
    ids = {r["receipt_id"] for r in built["bank"]["receipts"]}
    assert {
        "F43-RETAINED-F5-CONTEXT",
        "F43-BOUNDED-F6-CANDIDATE",
        "F43-TEMPORAL-CANDIDATE",
        "F43-ORIGINAL-E04-TEST",
    } <= ids
    src02_f5 = next(c for c in built["merged"]["acc"]["cells"] if c["cell_id"] == "SRC02.F5")
    assert src02_f5["consumed_grade"] == "HISTORICAL_RETAINED_EVIDENCE"
    assert "F43-RETAINED-F5-CONTEXT" in {
        e["receipt_id"] for e in src02_f5["actual_evidence"]
    }
    functional = built["merged"]["acc"]["functional_maturity"]
    for gate in ("F6", "F7"):
        assert "F43-" in " ".join(functional[gate]["evidence_receipts"])


def test_u43_frontier_descriptor_and_151_101_81_are_bound(built):
    receipt = built["u43"]
    unknown = receipt["unknown_bounds"]
    assert unknown["research_identities"] == 18285
    assert unknown["original_u_count"] is None
    assert unknown["eligible_e_pre_count"] is None
    assert unknown["hard_fail_flags"] == 10418
    assert unknown["routing_required_flags"] == 4447
    assert unknown["issuer_decisions"] == 175
    assert Path(u43.__file__).resolve() == (
        bootstrap.ROOT / "rawlsing_next" / "pre553_issued_workload.py"
    ).resolve()
    assert u43.DESCRIPTOR_FIELDS == {
        "source_edition", "native_item_ids", "release_tag", "routing_and_risk",
        "carrier", "country_and_population", "weight_design_estimand",
        "missing_and_occurrence_policy", "target_conditioner_roles",
    }
    gp = GitPreimage(bootstrap.ROOT)
    demands = json.loads(
        gp.blob_at(
            bootstrap.PINS["U43"]["commit"],
            bootstrap.PINS["U43"]["dir"] + "/A42_151_101_and_81_owner_demands.json",
        )
    )
    assert demands["AT_obligations"] == [f"AT{i:02d}" for i in range(1, 36)]
    assert len(demands["register_151"]) == 151
    assert len(demands["ledger_101"]) == 101
    assert len(demands["unmatched81"]) == 81
    assert demands["a42_commit"] == bootstrap.PINS["A42"]["commit"]


def test_b43_source_pending_gate_is_preserved(built):
    receipt = built["b43"]
    assert receipt["grade"] == "DEVELOPMENT_BLOCKER_WITH_NARROW_OWNER"
    assert receipt["coverage"]["wave_ids"] == []
    assert receipt["unknown_bounds"]["source_grant_present"] is False
    assert receipt["unknown_bounds"]["expected_original_operations_total"] is None
    assert receipt["unknown_bounds"]["executed_original_operations_total"] == 0
    assert receipt["unknown_bounds"]["wave_count_pending"] == 35


def test_1890_cells_283_rows_151_101_81_preserved(built):
    f1f8 = built["overlay"]["f1_f8"]
    manifest = built["overlay"]["manifest"]
    assert f1f8["row_count"] == 283
    assert f1f8["per_wave_row_count"] == 280
    assert f1f8["global_row_count"] == 3
    assert manifest["expected_accounting"]["expected_cell_count"] == 1890
    assert manifest["expected_accounting"]["register_151_count"] == 151
    assert manifest["expected_accounting"]["ledger_101_count"] == 101
    assert len(manifest["unmatched_register_resolution"]) == 81
    verdict = built["merged"]["acc"]["verdict"]
    assert verdict["total_cells"] == 1890
    assert verdict["global_relations_open"] == 3
    assert verdict["original_measured_occupied_cells"] == 0
    assert verdict["unmatched_still_unresolved"] == 81
    assert verdict["n11_state"] == "N11_NOT_READY"


# ---------------------------------------------------------------------------
# discriminator (a): no-drop merged receipt set
# ---------------------------------------------------------------------------


def test_no_drop_removed_j42_receipt_is_detected(built):
    assert J42_RECEIPT in i44.EXPECTED_MERGED_RECEIPT_IDS
    dropped = [r for r in i44.EXPECTED_MERGED_RECEIPT_IDS if r != J42_RECEIPT]
    with pytest.raises(PreimageError) as excinfo:
        i44.assert_receipt_set(dropped)
    assert "MERGED_BANK_RECEIPT_SET_DIFFERS" in str(excinfo.value)
    assert J42_RECEIPT in str(excinfo.value)


# ---------------------------------------------------------------------------
# discriminator (b): false sourcegrade promotion and forged/missing inputs
# ---------------------------------------------------------------------------


def test_false_sourcegrade_promotion_is_refused(built):
    bad_receipt = deepcopy(built["f43_bank"]["receipts"][0])
    bad_receipt["grade"] = "ORIGINAL_MEASURED_OCCUPANCY"
    bad_bank = {
        "schema": built["bank"]["schema"],
        "receipts": [bad_receipt] + [r for r in built["bank"]["receipts"] if r["receipt_id"] != bad_receipt["receipt_id"]],
    }
    with pytest.raises(PreimageError) as excinfo:
        i44.assess(bad_bank)
    assert "FALSE_PROMOTION_SOURCEFREE_TO_ORIGINAL_OCCUPANCY" in str(excinfo.value)


def test_forged_artifact_preimage_is_refused(built):
    bad_receipt = deepcopy(built["j42"])
    bad_receipt["artifacts"][0]["sha256"] = "0" * 64
    with pytest.raises(PreimageError) as excinfo:
        i44.assess(_bank_with(built, bad_receipt))
    assert "CONTENT_PREIMAGE_MISMATCH" in str(excinfo.value)


def test_clock_violation_is_refused(built):
    bad_receipt = deepcopy(built["j42"])
    bad_receipt["currentness"]["as_of"] = "2027-01-01"
    with pytest.raises(PreimageError) as excinfo:
        i44.assess(_bank_with(built, bad_receipt))
    assert "CURRENTNESS_CLOCK_VIOLATION" in str(excinfo.value)


def test_forged_consumer_ref_is_refused(built):
    bad_receipt = deepcopy(built["j42"])
    bad_receipt["downstream_consumer_read_refs"] = ["FORGED_ACTOR_CONSUMER"]
    with pytest.raises(PreimageError) as excinfo:
        i44.assess(_bank_with(built, bad_receipt))
    assert "R41_UNKNOWN_OR_FORGED_CONSUMER_REF" in str(excinfo.value)


def test_missing_origin_commit_artifact_refuses(built):
    bad_receipt = deepcopy(built["u43"])
    bad_receipt["origin_commit"] = "f" * 40
    with pytest.raises(PreimageError) as excinfo:
        i44.assess(_bank_with(built, bad_receipt))
    assert "COMMIT_UNAVAILABLE" in str(excinfo.value)


# ---------------------------------------------------------------------------
# discriminator (c): U43 descriptor -> B43 issuer-bound frontend
# ---------------------------------------------------------------------------


def _descriptor(**overrides):
    material = {
        "source_edition": "ED1",
        "native_item_ids": ["I1", "I2"],
        "release_tag": "R1",
        "routing_and_risk": {
            "risk_name": "R_ALL",
            "member_ids": ["R1", "R2"],
            "grant": "GRANTED_FIXTURE",
            "targets": [["Y", ["0", "1"]]],
        },
        "carrier": "SAV",
        "country_and_population": {"country": "US", "population": "ADULTS"},
        "weight_design_estimand": {"weight": "W1", "design": "D1", "estimand": "E1"},
        "missing_and_occurrence_policy": {"missing": "M1", "occurrence": "O1"},
        "target_conditioner_roles": {"targets": [["Y", ["0", "1"]]]},
    }
    material.update(overrides)
    return material


def _expect_no_native_calls(fn):
    calls = []

    def profiler(frame, event, arg):
        if event == "call" and frame.f_code.co_name in {
            "execute_empirical_query",
            "execute_route_b_production",
            "execute_issued_workload",
        }:
            calls.append(frame.f_code.co_filename)

    sys.setprofile(profiler)
    try:
        result = fn()
    finally:
        sys.setprofile(None)
    return result, calls


def test_u43_b43_compiled_adapter_refuses_forged_descriptor():
    issued = u43.canonical(_descriptor())
    # BEFORE: a raw U43 descriptor object is not a B43 plan.
    before = adapter.raw_descriptor_frontend_probe(issued)
    assert before == {"state": "B43_TYPED_REFUSAL", "code": "B43_PLAN_HAS_NO_OP_SPECS"}

    # AFTER: the qualified adapter maps the issued descriptor and admits.
    result, calls = _expect_no_native_calls(
        lambda: adapter.admit_via_b43(issued, op_ids=("OP1",))
    )
    assert result["state"] == "B43_ISSUER_BOUND_ADMITTED"
    assert result["checked_count"] == 1
    assert calls == []

    for field, forged, code in (
        ("source_edition", "FORGED_EDITION", "B43_ADMISSION_BOUND_SOURCE_EDITION_MISMATCH"),
        ("native_item_ids", ["I1", "FOREIGN"], "B43_ADMISSION_BOUND_NATIVE_ITEM_IDS_MISMATCH"),
        ("release_tag", "FORGED_TAG", "B43_ADMISSION_BOUND_RELEASE_TAG_MISMATCH"),
    ):
        candidate = u43.canonical(_descriptor(**{field: forged}))
        with pytest.raises(B43AdmissionDenied) as excinfo:
            adapter.admit_via_b43(
                issued, op_ids=("OP1",), candidate_descriptor=candidate
            )
        assert excinfo.value.code == code
    assert calls == []


def test_u43_descriptor_shape_is_fail_closed():
    with pytest.raises(adapter.AdapterShapeError):
        adapter.parse_descriptor(b"{}")
    with pytest.raises(adapter.AdapterShapeError):
        adapter.parse_descriptor(u43.canonical(_descriptor(carrier="UNBOUND")))
    with pytest.raises(adapter.AdapterShapeError):
        adapter.issuer_contract_for_descriptor(
            u43.canonical(_descriptor()), op_ids=("OP1",), issuer_ref="REAL_ISSUER_NOT_ALLOWED"
        )


# ---------------------------------------------------------------------------
# S44 receiving interface
# ---------------------------------------------------------------------------


def test_s44_socket_mechanics_and_typed_refusals(built):
    report = built["s44"]
    assert report["state"] == "EXECUTABLE_SOCKET_READY__NO_REAL_S44_RECEIPT_PRESENT"
    assert report["validation"]["synthetic_witness"] is True
    assert report["synthetic_witness_counted_in_real_artifacts"] is False
    assert report["synthetic_witness_original_cells_in_witness_assessment"] == 1
    assert report["synthetic_witness_cell_ids"] == ["SRC01.S01"]
    assert report["real_artifacts_original_measured"] == 0
    refusals = report["refusal_codes"]
    expected = {
        "missing_grant", "revoked_grant", "missing_host", "missing_purpose",
        "operation_not_granted", "u_e_pre_not_issued", "issuance_missing",
        "synthetic_issuance_without_witness_mode", "clock_not_current",
        "clock_after_estate", "forged_consumer", "wave_out_of_scope",
        "no_measured_product", "artifact_preimage_changed",
    }
    assert expected <= set(refusals)
    for key, value in refusals.items():
        assert value != "ACCEPTED_UNEXPECTEDLY", key
        assert value, key


def test_s44_socket_never_changes_real_artifacts(built):
    assert built["merged"]["acc"]["verdict"]["original_measured_occupied_cells"] == 0
    assert built["overlay"]["manifest"]["verdict"]["original_measured_occupied_cells"] == 0
    assert built["delta"]["delta"]["original_measured_cells"] == 0


# ---------------------------------------------------------------------------
# deterministic replay
# ---------------------------------------------------------------------------


def test_cold_replay_is_byte_identical(built):
    first = i44.run_all()
    second = i44.run_all()
    assert first["artifact_sha256"] == second["artifact_sha256"]
    assert first["blended"] == second["blended"]
    assert first["merged_verdict"]["original_measured_occupied_cells"] == 0
    assert first["merged_receipt_count"] == 20
