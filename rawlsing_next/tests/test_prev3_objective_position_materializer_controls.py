import hashlib

from rawlsing_next.pre553_empirical_objects import AuthorityRef, ExactRef
from rawlsing_next.prev3_objective_position_materializer import (
    FACT_REF_KIND,
    ObjectivePositionInput,
    PositionResultState,
    materialize_objective_position,
    typed_nonpositive_result,
)


def _h(label: str) -> str:
    return hashlib.sha256(label.encode("utf-8")).hexdigest()


def _ref(kind: str, tag: str) -> ExactRef:
    return ExactRef(kind, f"urn:test:{kind.lower()}:{tag}", _h(f"{kind}:{tag}"))


def _aref(tag: str) -> AuthorityRef:
    return AuthorityRef(f"AUTH-{tag}", "1.0.0", _h(f"AUTH:{tag}"))


def _payload(tag: str, *, predecessor=None, currentness_tag=None) -> ObjectivePositionInput:
    currentness_tag = currentness_tag or tag
    return ObjectivePositionInput(
        materializer_implementation_ref=_ref("IMPLEMENTATION", tag),
        position_producer_authority_ref=_aref(f"{tag}-producer"),
        position_semantic_authority_ref=_aref(f"{tag}-semantic"),
        entity_or_actor_ref=_ref("OBJECTIVE_ACTOR", "actor-1"),
        objective_position_role_identity_ref=_ref("OBJECTIVE_POSITION_ROLE", "role-1"),
        source_universe_ref=_ref("SOURCE_UNIVERSE", "u1"),
        source_release_ref=_ref("SOURCE_RELEASE", "r1"),
        source_claim_ref=_ref("SOURCE_CLAIM", "claim-1"),
        source_claim_authority_ref=_aref("claim-owner"),
        supporting_evidence_refs=(_ref("EVIDENCE", "e1"),),
        position_role_receipt_ref=_ref("POSITION_ROLE_RECEIPT", "pra-1"),
        position_role_not_applicable_authority_ref=None,
        target_outcome_firewall_ref=_ref("TARGET_OUTCOME_FIREWALL", "pre-result"),
        applicability_authority_ref=_aref("applicability"),
        applicability_receipt_ref=_ref("APPLICABILITY_RECEIPT", "applies"),
        permission_authority_ref=_aref("permission"),
        allowed_uses=("OBJECTIVE_CONTEXT",),
        negative_ceiling_ref=_ref("NEGATIVE_CEILING", "ceiling"),
        valid_time_authority_ref=_aref("valid-time"),
        valid_time_basis_ref=_ref("VALID_TIME_BASIS", "interval-1"),
        currentness_authority_ref=_aref("currentness"),
        currentness_receipt_ref=_ref("CURRENTNESS_RECEIPT", currentness_tag),
        provenance_refs=(_ref("PROVENANCE", "p1"),),
        dependency_refs=(_ref("DEPENDENCY", "d1"),),
        replay_authority_ref=_aref("replay"),
        predecessor_position_fact_ref=predecessor,
    )


def test_currentness_receipt_changes_content_addressed_identity():
    a = materialize_objective_position(_payload("currentness", currentness_tag="current-a"))
    b = materialize_objective_position(_payload("currentness", currentness_tag="current-b"))
    assert a.fact_ref != b.fact_ref


def test_successor_binds_exact_predecessor_without_mutating_old_fact():
    old = materialize_objective_position(_payload("old"))
    successor = materialize_objective_position(
        _payload("successor", predecessor=old.fact_ref)
    )
    assert old.fact_ref.kind == FACT_REF_KIND
    assert successor.fact_ref.kind == FACT_REF_KIND
    assert successor.fact_ref != old.fact_ref
    assert successor.canonical_material["predecessor_position_fact_ref"] == old.fact_ref.as_dict()


def test_unavailable_noncomparable_and_use_denied_are_distinct_nonpositive_controls():
    states = (
        PositionResultState.UNAVAILABLE,
        PositionResultState.NONCOMPARABLE,
        PositionResultState.USE_DENIED,
    )
    results = [
        typed_nonpositive_result(
            state,
            reason_ref=_ref("MATERIALIZATION_REASON", state.value.lower()),
        )
        for state in states
    ]
    assert [result.state for result in results] == list(states)
    assert all(result.fact_ref is None for result in results)
