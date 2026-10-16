from dataclasses import replace
import hashlib

import pytest

from rawlsing_next.m5_runtime_rsc_peer_prior import (
    RSCValidationReceipt,
    ResolvedStructuralContext,
    StructuralCurrentnessReceipt,
    StructuralPeerUseReceipt,
)
from rawlsing_next.m6_actor_safe_expression import (
    ADP017_HASH,
    BLOCKED_NAMED_AUTHORITY_REQUIRED,
    FORBIDDEN_BEHAVIORAL_SOURCE_CLASSES,
    ActorAccessibleRenderEnvelope,
    ActorSafeRef,
    CurrentnessState,
    ExternalEventDecision,
    M6ForbiddenBehavioralSource,
    M6IntegrityError,
    M6NamedAuthorityRequired,
    M6SemanticWideningError,
    OpaqueAuditRef,
    ReceiverSnapshot,
    ReceiverState,
    ScopeCeiling,
    assert_behavioral_source_rejected,
    evaluate_actor_safe_ingress,
    evaluate_currentness,
    external_event_feedback,
    make_actor_accessible_render_envelope,
    make_actor_safe_claim_entry,
    make_nonrenderable_decision,
    make_replay_closure,
    project_actor_safe_entry,
    require_situated_expression_owner,
    situated_expression_behavior_status,
)


def _h(label: str) -> str:
    return hashlib.sha256(label.encode("utf-8")).hexdigest()


def _ref(kind: str, tag: str) -> ActorSafeRef:
    return ActorSafeRef(kind, f"urn:test:{kind.lower()}:{tag}", _h(f"{kind}:{tag}"))


def _entry(
    tag: str,
    *,
    access: str = "CLAIM_ACCESSIBLE",
    permission: str = "PERMIT_FIRST_PERSON_BELIEF",
    components=(),
    views=(),
    memory_count: int = 1,
):
    claim = _ref("CLAIM", tag)
    stance = _ref("STANCE", tag)
    memories = tuple(_ref("MEMORY", f"{tag}-{index}") for index in range(memory_count))
    transitions = (_ref("TRANSITION", tag),)
    entry = make_actor_safe_claim_entry(
        claim_ref=claim,
        stance_record_ref=stance,
        accessibility_state=access,
        permitted_component_refs=components,
        first_person_permission=permission,
        memory_refs=memories,
        actor_perceived_view_refs=views,
        source_transition_refs=transitions,
    )
    return entry


def _actor_bindings(actor_id: str, entries) -> dict[str, str]:
    result = {}
    for entry in entries:
        refs = (
            entry.stance_record_ref,
            *entry.memory_refs,
            *entry.actor_perceived_view_refs,
            *entry.source_transition_refs,
        )
        for ref in refs:
            result[ref.key] = actor_id
    return result


def _bundle(
    tag: str = "good",
    *,
    entries=None,
    decisions=(),
    opaque=(),
    actor_id: str = "ACTOR-1",
    as_of: int = 10,
):
    entries = tuple(entries if entries is not None else (_entry(tag),))
    gp = _h(f"generated-person:{tag}")
    actor = _h(f"actor-state:{tag}")
    memory = _h(f"memory-state:{tag}")
    epistemic = _h(f"epistemic-state:{tag}")
    closure = make_replay_closure(
        actor_id=actor_id,
        as_of_causal_time=as_of,
        source_generated_person_record_hash=gp,
        source_actor_state_hash=actor,
        source_memory_state_hash=memory,
        source_epistemic_state_hash=epistemic,
        exact_causal_parent_sequence_ref_hash=_h(f"parents:{tag}"),
        canonical_claim_refs=tuple(entry.claim_ref for entry in entries),
        adp016_memory_object_and_transition_refs=tuple(
            ref for entry in entries for ref in entry.memory_refs
        ),
        epistemic_effect_and_transition_refs=tuple(
            ref for entry in entries for ref in entry.source_transition_refs
        ),
        permission_record_refs=tuple(item.permission_record_ref for item in decisions),
        actor_perceived_view_refs=tuple(
            ref for entry in entries for ref in entry.actor_perceived_view_refs
        ),
        entry_hashes=tuple(entry.entry_hash for entry in entries),
        decision_ref_hashes=tuple(item.decision_ref_hash for item in decisions),
    )
    envelope = make_actor_accessible_render_envelope(
        actor_id=actor_id,
        as_of_causal_time=as_of,
        source_generated_person_record_hash=gp,
        source_actor_state_hash=actor,
        source_memory_state_hash=memory,
        source_epistemic_state_hash=epistemic,
        replay_closure=closure,
        allowed_claim_entries=entries,
        explicit_denial_refs=decisions,
        other_opaque_provenance_refs=opaque,
    )
    receiver = ReceiverSnapshot(
        actor_id,
        as_of,
        gp,
        actor,
        memory,
        epistemic,
        ref_actor_bindings=_actor_bindings(actor_id, entries),
    )
    return entries, closure, envelope, receiver


def test_current_verified_full_entry_is_sole_positive_semantic_path_and_replays():
    entries, closure, envelope, receiver = _bundle("positive")
    first = evaluate_actor_safe_ingress(envelope, closure, receiver, entries[0].claim_ref)
    second = evaluate_actor_safe_ingress(envelope, closure, receiver, entries[0].claim_ref)

    assert evaluate_currentness(envelope, closure, receiver) is CurrentnessState.CURRENT
    assert first.receiver_state is ReceiverState.READY_FULL_CLAIM_SCOPE
    assert first.positive_semantics is True
    assert first.claim_ref == entries[0].claim_ref
    assert first.first_person_permission == "PERMIT_FIRST_PERSON_BELIEF"
    assert first == second
    assert first.semantic_fingerprint == second.semantic_fingerprint


def test_partial_access_exposes_only_exact_components_and_actor_perceived_views():
    c1, c2, c3 = (_ref("COMPONENT", name) for name in ("c1", "c2", "c3"))
    view1 = _ref("ACTOR_PERCEIVED_RELATIONSHIP_VIEW", "view1")
    view2 = _ref("ACTOR_PERCEIVED_RELATIONSHIP_VIEW", "view2")
    entry = _entry(
        "partial",
        access="CLAIM_PARTIALLY_ACCESSIBLE",
        components=(c3, c1),
        views=(view2, view1),
    )
    entries, closure, envelope, receiver = _bundle("partial", entries=(entry,))
    decision = evaluate_actor_safe_ingress(envelope, closure, receiver, entry.claim_ref)

    assert decision.receiver_state is ReceiverState.READY_PARTIAL_COMPONENT_SCOPE
    assert set(decision.component_refs) == {c1, c3}
    projection = project_actor_safe_entry(
        decision,
        source_scope_ceiling=ScopeCeiling(("T1", "T2"), ("S1",), ("R1", "R2")),
        requested_claim_ref=entry.claim_ref,
        requested_first_person_permission=entry.first_person_permission,
        requested_component_refs=(c1,),
        requested_actor_perceived_view_refs=(view1,),
        requested_temporal_scope_refs=("T1",),
        requested_subject_scope_refs=("S1",),
        requested_referent_scope_refs=("R2",),
    )
    assert projection.component_refs == (c1,)
    assert projection.actor_perceived_view_refs == (view1,)

    with pytest.raises(M6SemanticWideningError):
        project_actor_safe_entry(
            decision,
            source_scope_ceiling=ScopeCeiling(),
            requested_claim_ref=entry.claim_ref,
            requested_first_person_permission=entry.first_person_permission,
            requested_component_refs=(c2,),
        )
    with pytest.raises(M6SemanticWideningError):
        project_actor_safe_entry(
            decision,
            source_scope_ceiling=ScopeCeiling(),
            requested_claim_ref=entry.claim_ref,
            requested_first_person_permission=entry.first_person_permission,
            requested_actor_perceived_view_refs=(_ref("OBJECTIVE_RELATIONSHIP", "hidden"),),
            requested_component_refs=(c1,),
        )


def test_monotone_projection_rejects_claim_permission_and_scope_widening():
    entry = _entry("monotone", permission="PERMIT_FIRST_PERSON_BELIEF")
    entries, closure, envelope, receiver = _bundle("monotone", entries=(entry,))
    decision = evaluate_actor_safe_ingress(envelope, closure, receiver, entry.claim_ref)
    ceiling = ScopeCeiling(("T1",), ("S1",), ("R1",))

    with pytest.raises(M6SemanticWideningError):
        project_actor_safe_entry(
            decision,
            source_scope_ceiling=ceiling,
            requested_claim_ref=_ref("CLAIM", "joined-or-new"),
            requested_first_person_permission=entry.first_person_permission,
        )
    with pytest.raises(M6SemanticWideningError):
        project_actor_safe_entry(
            decision,
            source_scope_ceiling=ceiling,
            requested_claim_ref=entry.claim_ref,
            requested_first_person_permission="PERMIT_FIRST_PERSON_KNOWLEDGE",
        )
    with pytest.raises(M6SemanticWideningError):
        project_actor_safe_entry(
            decision,
            source_scope_ceiling=ceiling,
            requested_claim_ref=entry.claim_ref,
            requested_first_person_permission=entry.first_person_permission,
            requested_temporal_scope_refs=("T2",),
        )
    with pytest.raises(M6SemanticWideningError):
        project_actor_safe_entry(
            decision,
            source_scope_ceiling=ceiling,
            requested_claim_ref=entry.claim_ref,
            requested_first_person_permission=entry.first_person_permission,
            requested_subject_scope_refs=("S2",),
        )
    with pytest.raises(M6SemanticWideningError):
        project_actor_safe_entry(
            decision,
            source_scope_ceiling=ceiling,
            requested_claim_ref=entry.claim_ref,
            requested_first_person_permission=entry.first_person_permission,
            requested_referent_scope_refs=("R2",),
        )


def test_stale_and_integrity_failures_have_zero_semantics_and_no_session_fallback():
    entries, closure, envelope, receiver = _bundle("stale")
    claim = entries[0].claim_ref
    stale = replace(
        receiver,
        causal_time=11,
        source_memory_state_hash=_h("changed-memory"),
    )
    stale_decision = evaluate_actor_safe_ingress(
        envelope,
        closure,
        stale,
        claim,
        session_or_transcript_claim_refs=(claim,),
    )
    assert stale_decision.receiver_state is ReceiverState.BLOCKED_STALE_ACTOR_SAFE_HANDOFF
    assert stale_decision.positive_semantics is False

    wrong_actor = replace(receiver, actor_id="ACTOR-2")
    assert evaluate_actor_safe_ingress(
        envelope, closure, wrong_actor, claim
    ).receiver_state is ReceiverState.BLOCKED_HANDOFF_INTEGRITY_FAILURE

    early = replace(receiver, causal_time=9)
    assert evaluate_actor_safe_ingress(
        envelope, closure, early, claim
    ).receiver_state is ReceiverState.BLOCKED_HANDOFF_INTEGRITY_FAILURE

    bad_authority = replace(receiver, adp017_authority_hash=_h("wrong-adp017"))
    assert evaluate_actor_safe_ingress(
        envelope, closure, bad_authority, claim
    ).receiver_state is ReceiverState.BLOCKED_HANDOFF_INTEGRITY_FAILURE

    bad_envelope = replace(envelope, envelope_hash=_h("tampered-envelope"))
    assert evaluate_actor_safe_ingress(
        bad_envelope, closure, receiver, claim
    ).receiver_state is ReceiverState.BLOCKED_HANDOFF_INTEGRITY_FAILURE

    bad_closure = replace(closure, closure_hash=_h("tampered-closure"))
    assert evaluate_actor_safe_ingress(
        envelope, bad_closure, receiver, claim
    ).receiver_state is ReceiverState.BLOCKED_HANDOFF_INTEGRITY_FAILURE


def test_same_time_source_hash_mismatch_is_integrity_failure_not_stale():
    entries, closure, envelope, receiver = _bundle("same-time")
    mismatch = replace(receiver, source_actor_state_hash=_h("same-time-conflict"))
    assert evaluate_currentness(envelope, closure, mismatch) is CurrentnessState.INTEGRITY_FAILURE
    assert evaluate_actor_safe_ingress(
        envelope, closure, mismatch, entries[0].claim_ref
    ).positive_semantics is False


def test_actor_bound_stance_memory_relationship_and_transition_refs_must_verify():
    entries, closure, envelope, receiver = _bundle("actor-bind")
    bad_bindings = dict(receiver.ref_actor_bindings)
    bad_bindings[entries[0].stance_record_ref.key] = "ACTOR-OTHER"
    bad_receiver = replace(receiver, ref_actor_bindings=bad_bindings)
    assert evaluate_actor_safe_ingress(
        envelope, closure, bad_receiver, entries[0].claim_ref
    ).receiver_state is ReceiverState.BLOCKED_HANDOFF_INTEGRITY_FAILURE


def test_deny_defer_absence_and_valid_empty_are_control_or_zero_only():
    denied_claim = _ref("CLAIM", "denied")
    denied = make_nonrenderable_decision(
        claim_ref=denied_claim,
        permission_record_ref=_ref("PERMISSION", "denied"),
        accessibility_state="CLAIM_INACCESSIBLE",
        first_person_permission="DENY_FIRST_PERSON_CLAIM",
    )
    _, closure, envelope, receiver = _bundle("denied", entries=(), decisions=(denied,))
    decision = evaluate_actor_safe_ingress(envelope, closure, receiver, denied_claim)
    assert decision.receiver_state is ReceiverState.DENIED_EXPLICIT_FIRST_PERSON_CLAIM
    assert decision.positive_semantics is False

    deferred_claim = _ref("CLAIM", "deferred")
    deferred = make_nonrenderable_decision(
        claim_ref=deferred_claim,
        permission_record_ref=_ref("PERMISSION", "deferred"),
        accessibility_state="CLAIM_ACCESS_UNKNOWN",
        first_person_permission="DEFER_MISSING_AUTHORITY",
    )
    _, closure, envelope, receiver = _bundle("deferred", entries=(), decisions=(deferred,))
    decision = evaluate_actor_safe_ingress(envelope, closure, receiver, deferred_claim)
    assert decision.receiver_state is ReceiverState.DEFERRED_MISSING_AUTHORITY
    assert decision.first_person_permission is None
    assert decision.positive_semantics is False

    entry = _entry("other")
    _, closure, envelope, receiver = _bundle("absent", entries=(entry,))
    missing = _ref("CLAIM", "missing")
    decision = evaluate_actor_safe_ingress(
        envelope, closure, receiver, missing, session_or_transcript_claim_refs=(missing,)
    )
    assert decision.receiver_state is ReceiverState.NO_RENDERABLE_ENTRY_FOR_REQUEST
    assert decision.positive_semantics is False

    _, closure, envelope, receiver = _bundle("empty", entries=())
    decision = evaluate_actor_safe_ingress(envelope, closure, receiver, missing)
    assert decision.receiver_state is ReceiverState.VALID_EMPTY_NO_RENDERABLE_ACTOR_CLAIMS
    assert decision.positive_semantics is False


def test_entry_constructor_rejects_actor_stance_fabrication_from_system_unknown_or_control_state():
    with pytest.raises(M6IntegrityError):
        make_actor_safe_claim_entry(
            claim_ref=_ref("CLAIM", "bad-access"),
            stance_record_ref=_ref("STANCE", "bad-access"),
            accessibility_state="CLAIM_ACCESS_UNKNOWN",
            first_person_permission="PERMIT_FIRST_PERSON_UNCERTAINTY",
        )
    with pytest.raises(M6IntegrityError):
        make_actor_safe_claim_entry(
            claim_ref=_ref("CLAIM", "bad-permission"),
            stance_record_ref=_ref("STANCE", "bad-permission"),
            accessibility_state="CLAIM_ACCESSIBLE",
            first_person_permission="DEFER_MISSING_AUTHORITY",
        )


@pytest.mark.parametrize(
    "source_class",
    sorted(FORBIDDEN_BEHAVIORAL_SOURCE_CLASSES),
)
@pytest.mark.parametrize("representation", ["DIRECT", "SUMMARY", "EMBEDDING", "PROMPT_FRAGMENT", "SESSION_MEMO"])
def test_forbidden_upstream_sources_remain_forbidden_through_representation_changes(source_class, representation):
    with pytest.raises(M6ForbiddenBehavioralSource):
        assert_behavioral_source_rejected(
            object(), declared_source_class=source_class, representation=representation
        )


def test_concrete_accepted_m5_runtime_types_are_bound_and_have_zero_direct_positive_m6_effect():
    concrete_m5_types = (
        ResolvedStructuralContext,
        RSCValidationReceipt,
        StructuralCurrentnessReceipt,
        StructuralPeerUseReceipt,
    )
    assert len(set(concrete_m5_types)) == 4
    assert ActorAccessibleRenderEnvelope not in concrete_m5_types
    for runtime_type in concrete_m5_types:
        source = object.__new__(runtime_type)
        with pytest.raises(M6ForbiddenBehavioralSource):
            assert_behavioral_source_rejected(source)


def test_opaque_provenance_is_behaviorally_inert_and_never_appears_in_ingress_decision():
    entry = _entry("opaque")
    opaque_a = OpaqueAuditRef("AUDIT_ONLY_REF", "OTHER_AUDIT_PROVENANCE", "audit:A", _h("audit-A"))
    opaque_b = OpaqueAuditRef("AUDIT_ONLY_REF", "OTHER_AUDIT_PROVENANCE", "audit:B", _h("audit-B"))
    _, closure_a, envelope_a, receiver_a = _bundle("opaque", entries=(entry,), opaque=(opaque_a,))
    _, closure_b, envelope_b, receiver_b = _bundle("opaque", entries=(entry,), opaque=(opaque_b,))
    decision_a = evaluate_actor_safe_ingress(envelope_a, closure_a, receiver_a, entry.claim_ref)
    decision_b = evaluate_actor_safe_ingress(envelope_b, closure_b, receiver_b, entry.claim_ref)

    assert envelope_a.envelope_hash != envelope_b.envelope_hash
    assert decision_a == decision_b
    assert decision_a.semantic_fingerprint == decision_b.semantic_fingerprint
    assert "opaque" not in "".join(decision_a.__dataclass_fields__).lower()


def test_deterministic_identity_is_invariant_to_set_like_input_order():
    m1 = _ref("MEMORY", "1")
    m2 = _ref("MEMORY", "2")
    v1 = _ref("ACTOR_PERCEIVED_RELATIONSHIP_VIEW", "1")
    v2 = _ref("ACTOR_PERCEIVED_RELATIONSHIP_VIEW", "2")
    t1 = _ref("TRANSITION", "1")
    t2 = _ref("TRANSITION", "2")
    claim = _ref("CLAIM", "order")
    stance = _ref("STANCE", "order")
    first = make_actor_safe_claim_entry(
        claim_ref=claim,
        stance_record_ref=stance,
        accessibility_state="CLAIM_ACCESSIBLE",
        first_person_permission="PERMIT_FIRST_PERSON_KNOWLEDGE",
        memory_refs=(m2, m1),
        actor_perceived_view_refs=(v2, v1),
        source_transition_refs=(t2, t1),
    )
    second = make_actor_safe_claim_entry(
        claim_ref=claim,
        stance_record_ref=stance,
        accessibility_state="CLAIM_ACCESSIBLE",
        first_person_permission="PERMIT_FIRST_PERSON_KNOWLEDGE",
        memory_refs=(m1, m2),
        actor_perceived_view_refs=(v1, v2),
        source_transition_refs=(t1, t2),
    )
    assert first == second
    assert first.entry_hash == second.entry_hash


def test_session_transcript_and_prior_render_never_restore_withdrawn_or_missing_access():
    entry = _entry("withdrawn")
    _, closure, envelope, receiver = _bundle("withdrawn", entries=(entry,))
    stale = replace(receiver, causal_time=20, source_epistemic_state_hash=_h("withdrawn-state"))
    decision = evaluate_actor_safe_ingress(
        envelope,
        closure,
        stale,
        entry.claim_ref,
        session_or_transcript_claim_refs=(entry.claim_ref,),
    )
    assert decision.receiver_state is ReceiverState.BLOCKED_STALE_ACTOR_SAFE_HANDOFF
    assert decision.positive_semantics is False


def test_external_event_truth_table_preserves_zero_mutation_and_admit_only_occurrence():
    for state in (ExternalEventDecision.REJECT, ExternalEventDecision.DEFER, ExternalEventDecision.INVALID):
        result = external_event_feedback(state)
        assert result.admitted_occurrence_count == 0
        assert result.v3_causal_mutation_count == 0
        assert result.event_cursor_advance == 0
        assert result.causal_session_cursor_advance == 0
        assert result.automatic_actor_effect is False

    admitted = external_event_feedback(ExternalEventDecision.ADMIT)
    assert admitted.admitted_occurrence_count == 1
    assert admitted.v3_causal_mutation_count == 1
    assert admitted.event_cursor_advance == 1
    assert admitted.causal_session_cursor_advance == 1
    assert admitted.automatic_actor_effect is False


def test_m6_does_not_implement_situated_phenomenology_disclosure_salience_or_register():
    assert situated_expression_behavior_status() == BLOCKED_NAMED_AUTHORITY_REQUIRED
    with pytest.raises(M6NamedAuthorityRequired):
        require_situated_expression_owner()
    forbidden_fields = {
        "persona",
        "situated_phenomenology",
        "disclosure_willingness",
        "salience",
        "inhibition",
        "affective_foregrounding",
        "interlocutor_openness",
        "interaction_mode",
        "register",
        "utterance_plan",
        "rendered_expression",
    }
    assert forbidden_fields.isdisjoint(ActorAccessibleRenderEnvelope.__dataclass_fields__)


def test_actor_safe_envelope_is_not_generated_person_or_rendered_expression_object():
    fields = set(ActorAccessibleRenderEnvelope.__dataclass_fields__)
    assert "source_generated_person_record_hash" in fields
    assert "generated_person_record" not in fields
    assert "rendered_expression" not in fields
    assert "persona" not in fields
    assert ADP017_HASH.startswith("git-blob-sha1:")
