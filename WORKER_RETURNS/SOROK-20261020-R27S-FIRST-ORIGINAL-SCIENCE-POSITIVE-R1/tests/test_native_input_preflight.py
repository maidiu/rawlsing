from __future__ import annotations

import copy

from bundle_fixture import A, B, build_bundle, native_grade_fixture
from native_input_preflight import (
    STATUS_REFUSED,
    STATUS_TECHNICAL_PASS,
    digest,
    evaluate,
)


def test_positive_technical_fixture_is_green_but_native_false():
    receipt = evaluate(build_bundle())
    assert receipt["status"] == STATUS_TECHNICAL_PASS
    assert receipt["native"] is False
    assert receipt["native_eligible"] is False
    assert receipt["native_issued"] is False
    assert receipt["production_registries"] == "EMPTY"
    assert receipt["grant_written"] is False
    assert receipt["reasons"] == []
    assert all(receipt["checks"].values())


def test_forged_source_hash_refused():
    bundle = build_bundle()
    bundle["source_artifacts"]["TEST_ONLY_A_EP1"]["content_hash"] = "0" * 64
    receipt = evaluate(bundle)
    assert receipt["status"] == STATUS_REFUSED
    assert "SOURCE_CONTENT_HASH_INVALID:TEST_ONLY_A_EP1" in receipt["reasons"]


def test_self_signed_rule_a_refused():
    bundle = build_bundle()
    _set(bundle, "TEST_ONLY_CAN008_RULE_A", "issuer_ref", A)
    receipt = evaluate(bundle)
    assert "CAN008_RULE_A_SELF_ISSUED" in receipt["reasons"]


def test_unissued_rule_refused():
    bundle = build_bundle()
    bundle["rule_a_ref"] = "TEST_ONLY_MISSING_RULE_A"
    receipt = evaluate(bundle)
    assert "SOURCE_ARTIFACT_ABSENT:TEST_ONLY_MISSING_RULE_A" in receipt["reasons"]


def test_absent_adp019_e1_refused():
    bundle = build_bundle()
    _set(bundle, "TEST_ONLY_ADP019_E1", "admission_status", "DEFER")
    receipt = evaluate(bundle)
    assert "ADP019_E1_NOT_ADMITTED" in receipt["reasons"]


def test_stale_source_permission_refused():
    bundle = build_bundle()
    _set(bundle, "TEST_ONLY_SOURCE_GRANT", "expires_at", 900)
    receipt = evaluate(bundle)
    assert "SOURCE_GRANT_STALE" in receipt["reasons"]


def test_malicious_readset_refused():
    bundle = build_bundle()
    bundle["readset"]["declared_refs"].append("TEST_ONLY_UNDECLARED")
    bundle["readset"]["content_hashes"]["TEST_ONLY_UNDECLARED"] = "0" * 64
    receipt = evaluate(bundle)
    assert "READSET_DECLARED_REFS_MISMATCH" in receipt["reasons"]


def test_malicious_readset_content_hash_refused():
    bundle = build_bundle()
    bundle["readset"]["content_hashes"]["TEST_ONLY_A_EP1"] = "1" * 64
    receipt = evaluate(bundle)
    assert "READSET_CONTENT_HASH_MISMATCH:TEST_ONLY_A_EP1" in receipt["reasons"]


def test_backwards_clock_refused():
    bundle = build_bundle()
    _set(bundle, "TEST_ONLY_E2", "action_time", 650)
    receipt = evaluate(bundle)
    assert "E2_ACTION_BEFORE_TARGET_COMMIT" in receipt["reasons"]


def test_same_actor_as_other_refused():
    bundle = build_bundle()
    bundle["actor_b"]["actor_id"] = A
    receipt = evaluate(bundle)
    assert "ACTOR_OTHER_NOT_DISTINCT" in receipt["reasons"]


def test_single_source_owner_for_enactments_refused():
    bundle = build_bundle()
    _set(bundle, "TEST_ONLY_A_EP2", "owner_ref", "TEST_ONLY_OBSERVER_1")
    receipt = evaluate(bundle)
    assert "ACTOR_HISTORY_SINGLE_SOURCE_OWNER" in receipt["reasons"]


def test_missing_contrary_and_nonperformance_refused():
    bundle = build_bundle()
    bundle["actor_a"]["contrary_refs"] = []
    bundle["actor_a"]["nonperformance_refs"] = []
    receipt = evaluate(bundle)
    assert "CONTRARY_COMMITMENT_EVIDENCE_MISSING" in receipt["reasons"]
    assert "MATCHED_NONPERFORMANCE_EVIDENCE_MISSING" in receipt["reasons"]


def test_self_actuator_e2_refused():
    bundle = build_bundle()
    _set(bundle, "TEST_ONLY_E2", "actuator_ref", A)
    receipt = evaluate(bundle)
    assert "E2_SELF_ACTUATOR" in receipt["reasons"]


def test_untrusted_c8_refused():
    bundle = build_bundle()
    _set(bundle, "TEST_ONLY_C8_PROTECTED", "proof_verified", False)
    receipt = evaluate(bundle)
    assert "C8_PROOF_UNVERIFIED" in receipt["reasons"]


def test_can011_owner_not_separate_refused():
    bundle = build_bundle()
    rule_a_owner = bundle["source_artifacts"]["TEST_ONLY_CAN008_RULE_A"]["content"][
        "source_owner_ref"
    ]
    _set(bundle, "TEST_ONLY_CAN011_RULE_T", "source_owner_ref", rule_a_owner)
    receipt = evaluate(bundle)
    assert "CAN011_TARGET_OWNER_NOT_SEPARATE" in receipt["reasons"]


def test_grant_wrong_response_refused():
    bundle = build_bundle()
    _set(bundle, "TEST_ONLY_CAN011_GRANT", "response_ref", "TEST_ONLY_OTHER_RESPONSE")
    receipt = evaluate(bundle)
    assert "CAN011_GRANT_RESPONSE_MISMATCH" in receipt["reasons"]


def test_native_candidate_without_verifier_refused():
    receipt = evaluate(native_grade_fixture())
    assert receipt["status"] == STATUS_REFUSED
    assert "NATIVE_SIGNATURE_VERIFIER_UNAVAILABLE" in receipt["reasons"]
    assert receipt["native"] is False
    assert receipt["native_eligible"] is False


def test_native_candidate_with_denying_verifier_refused():
    class Deny:
        def verify(self, signature):
            return False

    receipt = evaluate(native_grade_fixture(), signature_verifier=Deny())
    assert receipt["status"] == STATUS_REFUSED
    assert any(code.startswith("NATIVE_SIGNATURE_") for code in receipt["reasons"])


def test_demographic_or_role_psychogenesis_forbidden():
    bundle = build_bundle()
    bundle["actor_a"]["occupation_psyche"] = "worker"
    receipt = evaluate(bundle)
    assert (
        "DEMOGRAPHIC_OR_ROLE_PSYCHOGENESIS_FORBIDDEN:actor_a:occupation_psyche"
        in receipt["reasons"]
    )


def test_nonempty_production_registry_refused():
    bundle = build_bundle()
    bundle["production"]["production_registry_entries"] = 1
    receipt = evaluate(bundle)
    assert "PRODUCTION_REGISTRY_NOT_EMPTY" in receipt["reasons"]


def test_receipt_and_input_digest_are_stable():
    bundle = build_bundle()
    first = evaluate(bundle)
    second = evaluate(copy.deepcopy(bundle))
    assert first == second
    assert first["input_digest"] == digest(bundle)
    body = {key: value for key, value in first.items() if key != "receipt_hash"}
    assert first["receipt_hash"] == digest(body)


def _set(bundle, ref, key, value):
    wrapper = bundle["source_artifacts"][ref]
    wrapper["content"][key] = value
    wrapper["content_hash"] = digest(wrapper["content"])
    bundle["readset"]["content_hashes"][ref] = wrapper["content_hash"]


def test_committed_technical_fixture_is_valid():
    import json
    from pathlib import Path

    root = Path(__file__).resolve().parents[1]
    bundle = json.loads(
        (root / "fixtures" / "positive_technical_bundle.json").read_text(encoding="utf-8")
    )
    receipt = evaluate(bundle)
    assert receipt["status"] == STATUS_TECHNICAL_PASS
    assert receipt["native"] is False
    assert receipt["production_registries"] == "EMPTY"
