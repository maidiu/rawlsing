from __future__ import annotations

import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
PRE = HERE / "_pinned/b53h/09_trusted_oracle_prefilter.py"
PUBLISHED = HERE / "_pinned/b53h/10_test_trusted_oracle_prefilter.py"


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def published():
    return load(PUBLISHED, "p53t_b53h_published")


def prefilter():
    return load(PRE, "p53t_b53h_prefilter")


def test_published_b53h_r2_sourcefree_controls_all_pass():
    module = published()
    names = sorted(
        name for name, value in vars(module).items()
        if name.startswith("test_") and callable(value))
    assert len(names) == 8
    for name in names:
        getattr(module, name)()


def test_self_attested_native_claims_pass_structural_prefilter():
    module = published()
    policy, pin, result = module.case()
    result["fixture_runs"][0]["public_call_trace_id"] = "claimed-without-replay"
    for row in result["fixture_runs"]:
        row["actual_native_c11"] = True
        row["actual_native_i03"] = True
        row["actual_native_i05"] = True
    outcome = module.g.analyze(policy, pin, result)
    assert outcome["failures"] == []
    assert outcome["status"] == \
        "STRUCTURAL_CROSSWALK_READY_FOR_INDEPENDENT_NATIVE_VALIDATION"
    assert outcome["limit"] == "NO_NATIVE_EXECUTION_OR_ATTESTATION_VALIDATED_HERE"
    assert set(outcome["cannot_issue"]) == {
        "SOURCE_RIGHT", "SCIENTIFIC_MEANING", "UNIVERSAL_ACCEPT", "N11", "N12"}


def test_caller_can_self_pin_a_forged_policy():
    module = published()
    policy, _, result = module.case()
    policy["fixtures"][0]["expected_operation_states"] = {"forged": "NATIVE_PRODUCED"}
    result["fixture_runs"][0]["operation_states"] = {"forged": "NATIVE_PRODUCED"}
    pin = module.g.digest(policy)
    outcome = module.g.analyze(policy, pin, result)
    assert outcome["failures"] == []
    assert outcome["status"] == \
        "STRUCTURAL_CROSSWALK_READY_FOR_INDEPENDENT_NATIVE_VALIDATION"


def test_independently_pinned_expected_set_rejects_operation_swap():
    module = published()
    policy, pin, result = module.case()
    result["fixture_runs"][0]["operation_states"] = {"fake_op": "NATIVE_PRODUCED"}
    outcome = module.g.analyze(policy, pin, result)
    assert "OPERATION_STATE_ANTI_JOIN:fx0" in outcome["failures"]
    assert outcome["status"] == "REVISE"


def test_prefilter_does_not_check_replay_or_runtime_provenance():
    module = published()
    policy, pin, result = module.case()
    result.pop("metamorphic_events")
    outcome = module.g.analyze(policy, pin, result)
    assert "RENAMING_WITNESS_MISSING" in outcome["failures"]
    assert "CONSUMER_RED_RESTORE_MISSING" in outcome["failures"]
    result["metamorphic_events"] = [
        {"kind": "RENAMING", "source_fixture": "fx0",
         "same_normalized_op_root": True, "same_consumer_value_root": True,
         "no_reserved_fixture_ids": True},
        {"kind": "MUTATION", "baseline": "PASS", "mutant": "ASSERTION_FAILED",
         "cold_restore": "PASS", "real_consumer_id": "E04"},
    ]
    outcome = module.g.analyze(policy, pin, result)
    assert outcome["failures"] == []
    assert outcome["limit"] == "NO_NATIVE_EXECUTION_OR_ATTESTATION_VALIDATED_HERE"


def test_mutated_candidate_commit_is_rejected():
    module = published()
    policy, pin, result = module.case()
    result["candidate_commit"] = "0" * 39
    outcome = module.g.analyze(policy, pin, result)
    assert "CANDIDATE_COMMIT_MISSING" in outcome["failures"]
    assert outcome["status"] == "REVISE"


def test_mutated_source_roster_is_rejected():
    module = published()
    policy, pin, result = module.case()
    result["original35"][0]["id"] = "not-an-issued-source"
    outcome = module.g.analyze(policy, pin, result)
    assert "SOURCE_ROSTER_ANTI_JOIN" in outcome["failures"]
    assert outcome["status"] == "REVISE"
