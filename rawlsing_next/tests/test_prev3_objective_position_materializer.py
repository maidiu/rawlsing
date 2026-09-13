import hashlib

import pytest

from rawlsing_next.pre553_empirical_objects import AuthorityRef, ExactRef
from rawlsing_next.prev3_objective_position_materializer import (
    FACT_REF_KIND,
    M2_SOURCE_SLOT,
    ObjectivePositionFact,
    ObjectivePositionInput,
    PositionMaterializerError,
    PositionResultState,
    m2_position_ref_handoff,
    materialize_objective_position,
    replay_objective_position,
    typed_nonpositive_result,
)


def _h(label: str) -> str:
    return hashlib.sha256(label.encode("utf-8")).hexdigest()


def _ref(kind: str, tag: str) -> ExactRef:
    return ExactRef(kind, f"urn:test:{kind.lower()}:{tag}", _h(f"{kind}:{tag}"))


def _aref(tag: str, version: str = "1.0.0") -> AuthorityRef:
    return AuthorityRef(f"AUTH-{tag}", version, _h(f"AUTH:{tag}:{version}"))


def _input(
    *,
    tag: str = "base",
    entity_ref: ExactRef | None = None,
    role_ref: ExactRef | None = None,
    role_receipt: ExactRef | None = None,
    role_na_authority: AuthorityRef | None = None,
    firewall: ExactRef | None = None,
    allowed_uses=("M2_SOURCE_STRUCTURAL_POSITION", "OBJECTIVE_CONTEXT"),
    evidence=None,
    provenance=None,
    dependencies=None,
    predecessor=None,
) -> ObjectivePositionInput:
    if role_receipt is None and role_na_authority is None:
        role_receipt = _ref("POSITION_ROLE_RECEIPT", f"{tag}-pra")
    return ObjectivePositionInput(
        materializer_implementation_ref=_ref("IMPLEMENTATION", tag),
        position_producer_authority_ref=_aref(f"{tag}-producer"),
        position_semantic_authority_ref=_aref(f"{tag}-semantic"),
        entity_or_actor_ref=entity_ref or _ref("OBJECTIVE_ACTOR", f"{tag}-actor"),
        objective_position_role_identity_ref=role_ref
        or _ref("OBJECTIVE_POSITION_ROLE", f"{tag}-role"),
        source_universe_ref=_ref("SOURCE_UNIVERSE", tag),
        source_release_ref=_ref("SOURCE_RELEASE", tag),
        source_claim_ref=_ref("SOURCE_CLAIM", tag),
        source_claim_authority_ref=_aref(f"{tag}-claim"),
        supporting_evidence_refs=tuple(
            evidence
            or (
                _ref("EVIDENCE", f"{tag}-e2"),
                _ref("EVIDENCE", f"{tag}-e1"),
            )
        ),
        position_role_receipt_ref=role_receipt,
        position_role_not_applicable_authority_ref=role_na_authority,
        target_outcome_firewall_ref=firewall,
        applicability_authority_ref=_aref(f"{tag}-applicability"),
        applicability_receipt_ref=_ref("APPLICABILITY_RECEIPT", tag),
        permission_authority_ref=_aref(f"{tag}-permission"),
        allowed_uses=tuple(allowed_uses),
        negative_ceiling_ref=_ref("NEGATIVE_CEILING", tag),
        valid_time_authority_ref=_aref(f"{tag}-valid-time"),
        valid_time_basis_ref=_ref("VALID_TIME_BASIS", tag),
        currentness_authority_ref=_aref(f"{tag}-currentness"),
        currentness_receipt_ref=_ref("CURRENTNESS_RECEIPT", tag),
        provenance_refs=tuple(
            provenance
            or (
                _ref("PROVENANCE", f"{tag}-p2"),
                _ref("PROVENANCE", f"{tag}-p1"),
            )
        ),
        dependency_refs=tuple(
            dependencies
            or (
                _ref("DEPENDENCY", f"{tag}-d2"),
                _ref("DEPENDENCY", f"{tag}-d1"),
            )
        ),
        replay_authority_ref=_aref(f"{tag}-replay"),
        predecessor_position_fact_ref=predecessor,
    )


def test_positive_fact_is_content_addressed_and_replays_exactly():
    payload = _input()
    fact = materialize_objective_position(payload)
    assert isinstance(fact, ObjectivePositionFact)
    assert fact.state is PositionResultState.POSITION_FACT_AUTHORIZED
    assert fact.fact_ref.kind == FACT_REF_KIND
    assert fact.fact_ref.object_id == f"PREV3POS:{fact.fact_ref.content_hash}"
    replayed = replay_objective_position(payload, fact.fact_ref)
    assert replayed.fact_ref == fact.fact_ref
    assert replayed.canonical_material == fact.canonical_material


def test_set_like_order_does_not_change_identity():
    a = _input(
        tag="order",
        evidence=(
            _ref("EVIDENCE", "order-a"),
            _ref("EVIDENCE", "order-b"),
        ),
        provenance=(
            _ref("PROVENANCE", "order-a"),
            _ref("PROVENANCE", "order-b"),
        ),
        dependencies=(
            _ref("DEPENDENCY", "order-a"),
            _ref("DEPENDENCY", "order-b"),
        ),
        allowed_uses=("OBJECTIVE_CONTEXT", "M2_SOURCE_STRUCTURAL_POSITION"),
    )
    b = ObjectivePositionInput(
        materializer_implementation_ref=a.materializer_implementation_ref,
        position_producer_authority_ref=a.position_producer_authority_ref,
        position_semantic_authority_ref=a.position_semantic_authority_ref,
        entity_or_actor_ref=a.entity_or_actor_ref,
        objective_position_role_identity_ref=a.objective_position_role_identity_ref,
        source_universe_ref=a.source_universe_ref,
        source_release_ref=a.source_release_ref,
        source_claim_ref=a.source_claim_ref,
        source_claim_authority_ref=a.source_claim_authority_ref,
        supporting_evidence_refs=tuple(reversed(a.supporting_evidence_refs)),
        position_role_receipt_ref=a.position_role_receipt_ref,
        position_role_not_applicable_authority_ref=None,
        target_outcome_firewall_ref=None,
        applicability_authority_ref=a.applicability_authority_ref,
        applicability_receipt_ref=a.applicability_receipt_ref,
        permission_authority_ref=a.permission_authority_ref,
        allowed_uses=tuple(reversed(a.allowed_uses)),
        negative_ceiling_ref=a.negative_ceiling_ref,
        valid_time_authority_ref=a.valid_time_authority_ref,
        valid_time_basis_ref=a.valid_time_basis_ref,
        currentness_authority_ref=a.currentness_authority_ref,
        currentness_receipt_ref=a.currentness_receipt_ref,
        provenance_refs=tuple(reversed(a.provenance_refs)),
        dependency_refs=tuple(reversed(a.dependency_refs)),
        replay_authority_ref=a.replay_authority_ref,
    )
    assert materialize_objective_position(a).fact_ref == materialize_objective_position(b).fact_ref


def test_identity_changes_when_a_canonical_determinant_changes():
    base = materialize_objective_position(_input(tag="drift"))
    changed = materialize_objective_position(
        _input(tag="drift", entity_ref=_ref("OBJECTIVE_ACTOR", "different-actor"))
    )
    assert base.fact_ref != changed.fact_ref


def test_role_authority_path_is_exactly_one_of_receipt_or_explicit_na_authority():
    with pytest.raises(PositionMaterializerError, match="exactly one role-authority path"):
        _input(
            tag="both",
            role_receipt=_ref("POSITION_ROLE_RECEIPT", "both"),
            role_na_authority=_aref("role-na"),
        )
    with pytest.raises(PositionMaterializerError, match="exactly one role-authority path"):
        _input(tag="neither", role_receipt=None, role_na_authority=None)


def test_directly_constitutive_position_can_use_explicit_role_na_authority():
    payload = _input(
        tag="na",
        role_receipt=None,
        role_na_authority=_aref("na-role-authority"),
    )
    fact = materialize_objective_position(payload)
    assert fact.fact_ref.kind == FACT_REF_KIND


def test_v3_or_person_state_cannot_bootstrap_objective_position_identity():
    with pytest.raises(PositionMaterializerError, match="V3/person/psychological"):
        _input(entity_ref=_ref("V3_SUBJECT_RECEIPT", "actor"))
    with pytest.raises(PositionMaterializerError, match="V3/person/psychological"):
        _input(role_ref=_ref("PERSON_STATE_TRAIT", "role"))


def test_person_side_allowed_use_is_rejected():
    with pytest.raises(PositionMaterializerError, match="objective PRE-V3 uses only"):
        _input(allowed_uses=("M2_SOURCE_STRUCTURAL_POSITION", "V3_PERSON_STATE_UPDATE"))


def test_constitutive_role_path_can_require_outcome_firewall():
    payload = _input(tag="firewall")
    with pytest.raises(PositionMaterializerError, match="target_outcome_firewall_ref"):
        materialize_objective_position(payload, require_target_outcome_firewall=True)
    guarded = _input(
        tag="firewall-positive",
        firewall=_ref("TARGET_OUTCOME_FIREWALL", "frozen-before-result"),
    )
    assert materialize_objective_position(
        guarded, require_target_outcome_firewall=True
    ).fact_ref.kind == FACT_REF_KIND


def test_missing_evidence_provenance_or_dependencies_fails_closed():
    for kwargs in (
        {"evidence": ()},
        {"provenance": ()},
        {"dependencies": ()},
    ):
        with pytest.raises(PositionMaterializerError, match="must not be empty"):
            _input(tag=f"missing-{next(iter(kwargs))}", **kwargs)


def test_mutable_authority_selector_is_rejected():
    bad = AuthorityRef("LATEST", "1.0.0", _h("latest"))
    with pytest.raises(PositionMaterializerError, match="latest/default/fuzzy/nearest"):
        ObjectivePositionInput(
            **{
                **_input(tag="authority").__dict__,
                "position_producer_authority_ref": bad,
            }
        )


def test_nonpositive_states_never_mint_positive_fact_ref():
    result = typed_nonpositive_result(
        PositionResultState.UNAVAILABLE,
        reason_ref=_ref("MATERIALIZATION_REASON", "source-not-present"),
    )
    assert result.fact_ref is None
    assert result.state is PositionResultState.UNAVAILABLE


def test_explicit_negative_requires_its_own_authority_and_evidence():
    with pytest.raises(PositionMaterializerError, match="exact negative authority and evidence"):
        typed_nonpositive_result(
            PositionResultState.EXPLICIT_NEGATIVE_OBJECTIVE_POSITION,
            reason_ref=_ref("NEGATIVE_REASON", "failed-positive-is-not-negative"),
        )
    negative = typed_nonpositive_result(
        PositionResultState.EXPLICIT_NEGATIVE_OBJECTIVE_POSITION,
        reason_ref=_ref("NEGATIVE_REASON", "exact-negative"),
        evidence_refs=(_ref("NEGATIVE_EVIDENCE", "e1"),),
        explicit_negative_authority_ref=_aref("negative-authority"),
    )
    assert negative.fact_ref is None


def test_m2_handoff_preserves_exact_ref_and_does_not_claim_route_authority():
    payload = _input(tag="m2")
    fact = materialize_objective_position(payload)
    handoff = m2_position_ref_handoff(
        fact,
        slot=M2_SOURCE_SLOT,
        requested_use="M2_SOURCE_STRUCTURAL_POSITION",
        allowed_uses=payload.allowed_uses,
    )
    assert handoff[M2_SOURCE_SLOT] == fact.fact_ref.as_dict()
    assert handoff["d03_handoff_only"] is True
    assert handoff["m2_route_authority_still_required"] is True
    assert handoff["m2_f1_closure_still_required"] is True


def test_m2_handoff_fails_if_use_not_permitted_or_slot_is_wrong():
    payload = _input(tag="m2-denied", allowed_uses=("OBJECTIVE_CONTEXT",))
    fact = materialize_objective_position(payload)
    with pytest.raises(PositionMaterializerError, match="not in the fact permission ceiling"):
        m2_position_ref_handoff(
            fact,
            slot=M2_SOURCE_SLOT,
            requested_use="M2_SOURCE_STRUCTURAL_POSITION",
            allowed_uses=payload.allowed_uses,
        )
    with pytest.raises(PositionMaterializerError, match="exact M2 structural-position slot"):
        m2_position_ref_handoff(
            fact,
            slot="latest_position_ref",
            requested_use="OBJECTIVE_CONTEXT",
            allowed_uses=payload.allowed_uses,
        )


def test_predecessor_must_be_exact_position_fact_ref():
    with pytest.raises(PositionMaterializerError, match="predecessor_position_fact_ref"):
        _input(predecessor=_ref("OTHER_FACT", "old"))
