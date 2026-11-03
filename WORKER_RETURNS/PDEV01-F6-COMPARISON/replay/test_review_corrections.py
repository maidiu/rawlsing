"""Exact corrections demanded by independent review 23edffb32."""
from __future__ import annotations
import json
import sys
from pathlib import Path

R = Path(__file__).resolve().parents[1]
F = json.loads((R / "evidence/replay_f6.json").read_text())
C = json.loads((R / "evidence/f6p-receiver-comparison.json").read_text())
F6P = R / "stage/F6P/WORKER_RETURNS/PYAT-R39-F6P-PARTIAL-BOUND-EVIDENCE-CONSUMER-R1"
for path in (F6P, F6P / "native", F6P / "oracle", F6P / "tests"):
    sys.path.insert(0, str(path))
from f6p_fixtures import build, request  # noqa: E402
import f6p_partial_bound_evidence_consumer as C6P  # noqa: E402


def _wp2_sidecar(value):
    return {"bundle_hash": value["native_bundle"]["content_hash"],
            "conditional": value["native_conditional_consumer"]}


def test_01_raw_keyerror_is_the_observed_boundary_and_label_is_authored():
    result = C6P.consume_f6m_evidence(
        build("B", "W2_mixed_eligibility_trap"),
        request("W2_mixed_eligibility_trap"))
    try:
        _wp2_sidecar(result)
    except KeyError as exc:
        assert type(exc) is KeyError
        assert exc.args == ("native_bundle",)
        assert str(exc) == "'native_bundle'"
    else:
        raise AssertionError("expected raw KeyError('native_bundle')")
    boundary = F["current_receiver"]["boundary_check"]
    assert boundary["raw_exception_type"] == "KeyError"
    assert boundary["raw_exception_args"] == ["native_bundle"]
    assert boundary["raw_exception_str"] == "'native_bundle'"
    assert boundary["authored_diagnostic_label"].startswith("COMPARISON_LOCAL_")
    assert boundary["observed_effect"] is None


def test_02_receiver_not_executed_and_no_effect_claim():
    receiver = F["current_receiver"]
    assert receiver["wp2_receiver_executed"] is False
    assert receiver["observed_effect"] is None
    assert receiver["partial_bounds_reach"] is False
    assert receiver["f6m_to_e04_join_claimed"] is False
    assert receiver["n9_first_import"] is False
    text = json.dumps(F, sort_keys=True) + json.dumps(C, sort_keys=True)
    assert C["receiver_shape_check"]["wp2_receiver_executed"] is False


def test_03_f6c_receipts_are_separate_and_outputs_are_embedded():
    manifest_path = R / "evidence/f6c/F6C_OUTPUT_MANIFEST.json"
    manifest = json.loads(manifest_path.read_text())
    assert manifest["receipt_contains_output_bodies"] is False
    assert manifest["outputs_present_here"] is True
    assert set(manifest["outputs"]) == {"A", "A0", "B"}
    for key in ("A", "A0", "B"):
        p = R / manifest["outputs"][key]["path"]
        assert p.is_file()
        import hashlib
        assert hashlib.sha256(p.read_bytes()).hexdigest() == manifest["outputs"][key]["sha256"]
    obs = manifest["observations"]
    assert obs["nonparent_consumer_invariant"] is True
    assert obs["generic_without_f6_sidecars_invariant"] is True
    assert obs["actual_C1_returns_invariant"] is True
    assert obs["cases_invariant"] is True
    assert obs["f6_sidecars_differ"] is True
    assert F["current_receiver"]["f6c_receipt_contains_output_bodies"] is False
    assert F["current_receiver"]["f6c_outputs_present"] is True


def test_04_checkout_root_hash_limit_is_explicit():
    limit = F["checkout_root_hash_limit"]
    assert limit["path_only_difference"] is True
    assert limit["semantic_fields_equal"] is True
    assert limit["candidate_output_hashes"] != limit["review_output_hashes"]
    assert "module_file" in limit["cause"]
    assert "same-checkout" in limit["scope"]
