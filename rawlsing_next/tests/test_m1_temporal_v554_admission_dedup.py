from __future__ import annotations

import copy
import hashlib
import random

import pytest

from rawlsing_next.m1_temporal_v554_admission_dedup import (
    BasisKind,
    M1DecisionState,
    SIG_001,
    SIG_002,
    SIG_003,
    TemporalCompleteness,
    evaluate_m1_temporal_v554_admission_dedup,
    semantic_hash,
)


def _h(label: str) -> str:
    return hashlib.sha256(label.encode()).hexdigest()


def _rule() -> dict[str, str]:
    return {"id": "V554-RULE-17", "version": "1.0.0", "hash": _h("rule")}


def _eq(*, temporal: str = "t:none", source: str = "u:1") -> dict[str, str]:
    return {
        "focal_structural_proposition_ref": "prop:1",
        "target_use": "STRUCTURAL_MEDIATION_INPUT",
        "v554_rule_id": "V554-RULE-17",
        "v554_rule_version": "1.0.0",
        "v554_rule_hash": _h("rule"),
        "rule_relevant_structural_semantic_identity_fingerprint": "struct:1",
        "native_scope_identity_fingerprint": "scope:1",
        "rule_relevant_effective_time_semantics_fingerprint": temporal,
        "originating_structural_empirical_admission_lineage_fingerprint": "adm-lineage:1",
        "source_universe_fingerprint": source,
        "estimand_fingerprint": "estimand:1",
        "measure_and_weight_authority_fingerprint": "measure:1",
        "rule_relevant_source_relation_comparability_authority_fingerprint": "comparability:1",
        "interpretation_critical_semantic_authority_fingerprint": "authority:1",
    }


def _candidate(
    kind: str,
    *,
    object_id: str,
    eq: dict[str, str] | None = None,
    semantics: object = "semantic-support-1",
    families: tuple[str, ...] = (),
    relation_refs: bool = False,
) -> dict[str, object]:
    eq = eq or _eq()
    if kind == BasisKind.DIRECT.value:
        projection = {
            "structural_empirical_admission_id": "admission:1",
            "structural_empirical_admission_content_hash": _h("admission:1"),
            "admission_authority_id": "STRUCTURAL_ADMISSION_AUTH",
            "admission_authority_version": "1.0.0",
            "admission_authority_hash": _h("admission-authority"),
            "admission_decision_state": "ADMITTED",
            "focal_structural_proposition_ref": "prop:1",
            "structural_semantic_identity_refs": ["struct:1"],
            "native_scope_identity_refs": ["scope:1"],
            "target_use_permission_refs": ["permission:1"],
            "effective_time_or_interval_refs_required_by_target_use": [],
            "source_universe_refs": [eq["source_universe_fingerprint"]],
            "estimand_refs": ["estimand:1"],
            "measure_and_weight_authority_refs": ["measure:1"],
            "applicable_negative_denial_noncomparability_refs": [],
            "interpretation_critical_authority_refs": ["authority:1"],
            "producer_replay_locator_or_reference_root": "replay:admission:1",
        }
    else:
        primary_family = families[-1] if families else "TEMPORAL_KEY"
        projection = {
            "v553_object_id": object_id,
            "v553_object_content_hash": _h(object_id),
            "v553_object_family": primary_family,
            "originating_structural_empirical_admission_refs": ["admission:1"],
            "focal_structural_proposition_ref": "prop:1",
            "rule_relevant_temporal_semantic_refs": list(families),
            "native_scope_identity_refs": ["scope:1"],
            "source_universe_refs": [eq["source_universe_fingerprint"]],
            "estimand_refs": ["estimand:1"],
            "measure_and_weight_authority_refs": ["measure:1"],
            "source_relation_comparability_authority_refs_where_required": ["comparability:1"],
            "applicable_temporal_limit_negative_refs": [],
            "interpretation_critical_authority_refs": ["authority:1"],
            "producer_replay_locator_or_reference_root": "replay:v553:1",
        }
    return {
        "basis_kind": kind,
        "basis_ref": {"kind": kind, "object_id": object_id, "content_hash": _h(object_id)},
        "projection": projection,
        "projection_hash": semantic_hash(projection),
        "equivalence_key": eq,
        "selected_rule_relevant_basis_semantics": semantics,
        "v553_families": list(families),
        "all_relation_required_support_limit_refs": relation_refs,
    }


def _condition(kind: str) -> dict[str, object]:
    return {
        "candidate_semantic_key": "candidate:1",
        "condition_kind_id": kind,
        "predicate_id": f"P-{kind}",
        "predicate_version": "1.0.0",
        "semantic_owner": "V554",
        "resolution_owner": "V555" if kind in {"K01", "K02", "K03"} else "V554",
        "binding_producer": "V554",
        "evaluator_owner": "V555" if kind in {"K01", "K02", "K03"} else "V554",
        "canonical_argument_envelope_fingerprint": f"args:{kind}",
        "producer_negative_or_requirement_refs": [f"ref:{kind}"],
    }


def _invocation(
    *,
    signature: str = SIG_001,
    completeness: str = TemporalCompleteness.COMPLETE_FOR_DIRECT_V554.value,
    candidates: list[dict[str, object]] | None = None,
    conditions: list[dict[str, object]] | None = None,
    governed_use_id: str = "use:1",
    publication: bool = False,
) -> dict[str, object]:
    if candidates is None:
        candidates = [_candidate(BasisKind.DIRECT.value, object_id="direct:1")]
    payload: dict[str, object] = {
        "governed_use_id": governed_use_id,
        "use_owner": "V554",
        "v554_rule_ref": _rule(),
        "signature_id": signature,
        "target_use": "STRUCTURAL_MEDIATION_INPUT",
        "focal_structural_proposition_ref": "prop:1",
        "originating_admission_refs": ["admission:1"],
        "scr553_decision_state": (
            "V553_NOT_REQUIRED_FOR_THIS_USE" if signature == SIG_001 else "V553_REQUIRED"
        ),
        "scr553_request_ref": {
            "kind": "V553TemporalizationRequest",
            "object_id": f"scr553-request:{governed_use_id}",
            "content_hash": _h(f"scr553-request:{governed_use_id}"),
        },
        "required_temporal_operations": ([] if signature == SIG_001 else ["EXPRESS_TIME_SCOPED_OBSERVATION"]),
        "required_authority_snapshot_refs": ["authority-snapshot:1"],
        "temporal_completeness": completeness,
        "candidates": candidates,
        "conditions": conditions or [],
        "authority_bundle_material": {
            "scr554": "1.0.0",
            "affordance_authority": {"id": "V554_AFFORDANCE_RULE_REGISTRY", "hash": _h("aff")},
            "rule": _rule(),
        },
        "producer_reference_spine_fingerprint": "spine:1",
    }
    if publication:
        payload["publication_authority"] = {
            "authority_id": "V557-PUBLISH-AUTH-1",
            "authority_version": "1.0.0",
            "authority_hash": _h("publish"),
            "producer": "V554",
            "publisher": "V557",
            "governed_use_id": governed_use_id,
            "rule_ref": _rule(),
            "decision": "AUTHORIZED",
            "allowed_object_families": ["F1", "F2", "B1"],
        }
    return payload


def test_sig001_direct_basis_emits_exactly_one_eligible_f1() -> None:
    result = evaluate_m1_temporal_v554_admission_dedup(_invocation())
    assert result.decision_state is M1DecisionState.ELIGIBLE
    assert result.required_basis_kind == BasisKind.DIRECT.value
    assert result.support_count == 1
    assert result.f1 is not None and result.f1["state"] == "ELIGIBLE"
    assert result.b1 is not None and result.b1["allowed_v555_structural_use"] is True


def test_same_admission_can_be_direct_for_u1_and_temporal_for_u2() -> None:
    u1 = evaluate_m1_temporal_v554_admission_dedup(_invocation(governed_use_id="U1"))
    temporal_candidate = _candidate(
        BasisKind.V553.value,
        object_id="v553:obs:1",
        eq=_eq(temporal="point:2026"),
        semantics={"key": "tk:1", "observation": "to:1"},
        families=("TEMPORAL_KEY", "TEMPORAL_OBSERVATION"),
    )
    u2 = evaluate_m1_temporal_v554_admission_dedup(
        _invocation(
            governed_use_id="U2",
            signature=SIG_002,
            completeness=TemporalCompleteness.REQUIRES_V553_OWNED_TEMPORAL_MEANING.value,
            candidates=[temporal_candidate],
        )
    )
    assert u1.decision_state is M1DecisionState.ELIGIBLE
    assert u2.decision_state is M1DecisionState.ELIGIBLE
    assert u1.required_basis_kind != u2.required_basis_kind


def test_v553_temporal_negative_cannot_be_downgraded_to_direct_positive() -> None:
    payload = _invocation(conditions=[_condition("K08")])
    payload["scr553_decision_state"] = "V553_NEGATIVE_LIMIT_ONLY"
    payload["temporal_completeness"] = TemporalCompleteness.BLOCKED_BY_APPLICABLE_TEMPORAL_OR_SOURCE_NEGATIVE.value
    result = evaluate_m1_temporal_v554_admission_dedup(payload)
    assert result.decision_state is M1DecisionState.INELIGIBLE_NEGATIVE_TEMPORAL_AUTHORITY
    assert result.f1 is None
    assert result.support_count == 0
    assert result.b1 is not None and result.b1["allowed_v555_structural_use"] is False


@pytest.mark.parametrize(
    ("kind", "state"),
    [
        ("K05", M1DecisionState.INELIGIBLE_EXPLICIT_DENIAL),
        ("K06", M1DecisionState.INELIGIBLE_MISSING_REQUIRED_AUTHORITY),
        ("K07", M1DecisionState.INELIGIBLE_UNKNOWN_OR_CONFLICTING_REQUIRED_AUTHORITY),
        ("K09", M1DecisionState.INELIGIBLE_NEGATIVE_TEMPORAL_AUTHORITY),
    ],
)
def test_hard_nonpositive_precedence_emits_no_f1(kind: str, state: M1DecisionState) -> None:
    result = evaluate_m1_temporal_v554_admission_dedup(_invocation(conditions=[_condition(kind)]))
    assert result.decision_state is state
    assert result.f1 is None
    assert result.support_count == 0


def test_deferred_k01_to_k03_remain_f2_without_blocking_f1() -> None:
    result = evaluate_m1_temporal_v554_admission_dedup(
        _invocation(conditions=[_condition("K01"), _condition("K02"), _condition("K03")])
    )
    assert result.decision_state is M1DecisionState.ELIGIBLE
    assert result.support_count == 1
    assert [record["disposition"] for record in result.f2] == ["DEFERRED"] * 3
    assert result.b1 is not None and result.b1["allowed_v555_structural_use"] is True


def test_exact_same_kind_duplicates_collapse_to_one_support_and_aliases() -> None:
    first = _candidate(BasisKind.DIRECT.value, object_id="direct:a")
    second = _candidate(BasisKind.DIRECT.value, object_id="direct:b")
    result = evaluate_m1_temporal_v554_admission_dedup(_invocation(candidates=[second, first]))
    assert result.decision_state is M1DecisionState.ELIGIBLE
    assert result.support_count == 1
    assert result.f1 is not None
    assert result.f1["provenance_alias_refs"] == ["direct:a", "direct:b"]


def test_noop_v553_duplicate_does_not_add_sig001_support() -> None:
    eq = _eq()
    direct = _candidate(BasisKind.DIRECT.value, object_id="direct:1", eq=eq)
    noop_v553 = _candidate(
        BasisKind.V553.value,
        object_id="v553:noop",
        eq=eq,
        semantics="semantic-support-1",
        families=("TEMPORAL_KEY", "TEMPORAL_OBSERVATION"),
    )
    result = evaluate_m1_temporal_v554_admission_dedup(_invocation(candidates=[noop_v553, direct]))
    assert result.decision_state is M1DecisionState.ELIGIBLE
    assert result.support_count == 1
    assert result.f1 is not None and result.f1["provenance_alias_refs"] == ["direct:1"]
    assert result.rejected_or_reference_only_basis_refs == ("v553:noop",)


def test_near_duplicate_source_universe_difference_is_not_collapsed_or_winner_selected() -> None:
    a = _candidate(BasisKind.DIRECT.value, object_id="direct:a", eq=_eq(source="u:a"))
    b = _candidate(BasisKind.DIRECT.value, object_id="direct:b", eq=_eq(source="u:b"))
    result = evaluate_m1_temporal_v554_admission_dedup(_invocation(candidates=[a, b]))
    assert result.decision_state is M1DecisionState.INELIGIBLE_UNKNOWN_OR_CONFLICTING_REQUIRED_AUTHORITY
    assert result.f1 is None
    assert result.support_count == 0


def test_equivalence_unknown_fails_closed() -> None:
    bad_eq = _eq()
    del bad_eq["estimand_fingerprint"]
    candidate = _candidate(BasisKind.DIRECT.value, object_id="direct:bad", eq=bad_eq)
    result = evaluate_m1_temporal_v554_admission_dedup(_invocation(candidates=[candidate]))
    assert result.decision_state is M1DecisionState.EQUIVALENCE_UNKNOWN
    assert result.f1 is None


def test_sig002_requires_exact_v553_key_and_observation() -> None:
    candidate = _candidate(
        BasisKind.V553.value,
        object_id="v553:key-only",
        eq=_eq(temporal="point:2026"),
        families=("TEMPORAL_KEY",),
    )
    result = evaluate_m1_temporal_v554_admission_dedup(
        _invocation(
            signature=SIG_002,
            completeness=TemporalCompleteness.REQUIRES_V553_OWNED_TEMPORAL_MEANING.value,
            candidates=[candidate],
        )
    )
    assert result.decision_state is M1DecisionState.INELIGIBLE_TEMPORAL_SIGNATURE
    assert result.f1 is None


def test_sig003_requires_relation_and_all_required_support_limit_refs() -> None:
    candidate = _candidate(
        BasisKind.V553.value,
        object_id="v553:relation",
        eq=_eq(temporal="relation:2025-2026"),
        families=("TEMPORAL_KEY", "TEMPORAL_RELATION"),
        relation_refs=False,
    )
    result = evaluate_m1_temporal_v554_admission_dedup(
        _invocation(
            signature=SIG_003,
            completeness=TemporalCompleteness.REQUIRES_V553_OWNED_TEMPORAL_MEANING.value,
            candidates=[candidate],
        )
    )
    assert result.decision_state is M1DecisionState.INELIGIBLE_TEMPORAL_SIGNATURE
    assert result.f1 is None


def test_direct_basis_cannot_satisfy_temporal_signature() -> None:
    result = evaluate_m1_temporal_v554_admission_dedup(
        _invocation(
            signature=SIG_002,
            completeness=TemporalCompleteness.REQUIRES_V553_OWNED_TEMPORAL_MEANING.value,
            candidates=[_candidate(BasisKind.DIRECT.value, object_id="direct:1")],
        )
    )
    assert result.decision_state is M1DecisionState.VALID_EMPTY
    assert result.f1 is None


def test_bad_projection_hash_is_presemantic_integrity_failure() -> None:
    candidate = _candidate(BasisKind.DIRECT.value, object_id="direct:1")
    candidate["projection_hash"] = _h("wrong")
    result = evaluate_m1_temporal_v554_admission_dedup(_invocation(candidates=[candidate]))
    assert result.decision_state is M1DecisionState.INTEGRITY_FAILURE
    assert result.f1 is None and result.f2 == () and result.b1 is None


def test_input_order_and_alias_enumeration_do_not_change_f1_identity() -> None:
    a = _candidate(BasisKind.DIRECT.value, object_id="direct:a")
    b = _candidate(BasisKind.DIRECT.value, object_id="direct:b")
    p1 = _invocation(candidates=[a, b], conditions=[_condition("K01"), _condition("K04")])
    p2 = _invocation(candidates=[b, a], conditions=[_condition("K04"), _condition("K01")])
    r1 = evaluate_m1_temporal_v554_admission_dedup(p1)
    r2 = evaluate_m1_temporal_v554_admission_dedup(p2)
    assert r1.f1 is not None and r2.f1 is not None
    assert r1.f1["f1_id"] == r2.f1["f1_id"]
    assert {item["f2_id"] for item in r1.f2} == {item["f2_id"] for item in r2.f2}
    assert r1.b1 is not None and r2.b1 is not None
    assert r1.b1["b1_id"] == r2.b1["b1_id"]


def test_runtime_ignores_wall_clock_random_and_filesystem_because_they_are_not_inputs(tmp_path) -> None:
    payload = _invocation()
    before = copy.deepcopy(payload)
    random_before = random.getstate()
    (tmp_path / "latest").write_text("noise")
    r1 = evaluate_m1_temporal_v554_admission_dedup(payload)
    random.random()
    (tmp_path / "latest").write_text("different noise")
    r2 = evaluate_m1_temporal_v554_admission_dedup(payload)
    assert r1.f1 == r2.f1
    assert payload == before
    assert random_before != random.getstate()  # external RNG moved; evaluator did not consume it


def test_direct_v554_v557_handoff_requires_independent_exact_positive_authority() -> None:
    without = evaluate_m1_temporal_v554_admission_dedup(_invocation(publication=False))
    with_auth = evaluate_m1_temporal_v554_admission_dedup(_invocation(publication=True))
    assert without.direct_v557_handoff is None
    assert with_auth.direct_v557_handoff is not None
    assert with_auth.direct_v557_handoff["route"] == "V554_TO_V557_DIRECT"
    families = {ref["family"] for ref in with_auth.direct_v557_handoff["object_refs"]}
    assert {"F1", "B1"}.issubset(families)


def test_wrong_publication_binding_does_not_publish_or_change_f1() -> None:
    payload = _invocation(publication=True)
    baseline = evaluate_m1_temporal_v554_admission_dedup(payload)
    assert baseline.f1 is not None
    payload["publication_authority"]["governed_use_id"] = "other-use"  # type: ignore[index]
    result = evaluate_m1_temporal_v554_admission_dedup(payload)
    assert result.decision_state is M1DecisionState.ELIGIBLE
    assert result.f1 is not None and result.f1["f1_id"] == baseline.f1["f1_id"]
    assert result.direct_v557_handoff is None


def test_v553_not_required_is_not_enough_without_independent_direct_temporal_completeness() -> None:
    payload = _invocation(
        completeness=TemporalCompleteness.UNKNOWN_FAIL_CLOSED.value
    )
    assert payload["scr553_decision_state"] == "V553_NOT_REQUIRED_FOR_THIS_USE"
    result = evaluate_m1_temporal_v554_admission_dedup(payload)
    assert result.decision_state is M1DecisionState.INELIGIBLE_UNKNOWN_OR_CONFLICTING_REQUIRED_AUTHORITY
    assert result.f1 is None


def test_sig001_cannot_run_when_scr553_says_this_exact_use_requires_temporal_meaning() -> None:
    payload = _invocation()
    payload["scr553_decision_state"] = "V553_REQUIRED"
    payload["required_temporal_operations"] = ["COMPARE_ACROSS_TIME"]
    result = evaluate_m1_temporal_v554_admission_dedup(payload)
    assert result.decision_state is M1DecisionState.INELIGIBLE_TEMPORAL_SIGNATURE
    assert result.f1 is None


def test_valid_empty_does_not_fabricate_b1_or_publication() -> None:
    result = evaluate_m1_temporal_v554_admission_dedup(_invocation(candidates=[], publication=True))
    assert result.decision_state is M1DecisionState.VALID_EMPTY
    assert result.f1 is None and result.f2 == () and result.b1 is None
    assert result.direct_v557_handoff is None


def test_coherent_zero_candidates_is_valid_empty_no_filler() -> None:
    result = evaluate_m1_temporal_v554_admission_dedup(_invocation(candidates=[]))
    assert result.decision_state is M1DecisionState.VALID_EMPTY
    assert result.support_count == 0 and result.f1 is None


def test_noop_v553_route_presence_does_not_change_sig001_f1_identity() -> None:
    eq = _eq()
    direct = _candidate(BasisKind.DIRECT.value, object_id="direct:stable", eq=eq)
    noop_v553 = _candidate(
        BasisKind.V553.value,
        object_id="v553:noop:stable",
        eq=eq,
        semantics="semantic-support-1",
        families=("TEMPORAL_KEY", "TEMPORAL_OBSERVATION"),
    )
    direct_only = evaluate_m1_temporal_v554_admission_dedup(
        _invocation(candidates=[direct])
    )
    with_noop = evaluate_m1_temporal_v554_admission_dedup(
        _invocation(candidates=[noop_v553, direct])
    )
    assert direct_only.f1 is not None and with_noop.f1 is not None
    assert direct_only.f1["f1_id"] == with_noop.f1["f1_id"]
    assert direct_only.canonical_basis_semantic_id == with_noop.canonical_basis_semantic_id


def test_hard_negative_direct_publication_preserves_only_nonpositive_context() -> None:
    payload = _invocation(conditions=[_condition("K08")], publication=True)
    payload["scr553_decision_state"] = "V553_NEGATIVE_LIMIT_ONLY"
    payload["temporal_completeness"] = TemporalCompleteness.BLOCKED_BY_APPLICABLE_TEMPORAL_OR_SOURCE_NEGATIVE.value
    result = evaluate_m1_temporal_v554_admission_dedup(payload)
    assert result.f1 is None and result.support_count == 0
    assert result.b1 is not None and result.b1["allowed_v555_structural_use"] is False
    assert result.direct_v557_handoff is not None
    families = [ref["family"] for ref in result.direct_v557_handoff["object_refs"]]
    assert "F1" not in families
    assert "F2" in families and "B1" in families


def test_material_source_change_changes_canonical_f1_identity() -> None:
    a = evaluate_m1_temporal_v554_admission_dedup(
        _invocation(candidates=[_candidate(BasisKind.DIRECT.value, object_id="direct:a", eq=_eq(source="u:a"))])
    )
    b = evaluate_m1_temporal_v554_admission_dedup(
        _invocation(candidates=[_candidate(BasisKind.DIRECT.value, object_id="direct:b", eq=_eq(source="u:b"))])
    )
    assert a.f1 is not None and b.f1 is not None
    assert a.f1["f1_id"] != b.f1["f1_id"]