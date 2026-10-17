from dataclasses import replace
import hashlib

import pytest

from rawlsing_next.m6_actor_safe_expression import (
    ActorSafeRef,
    M6ForbiddenBehavioralSource,
    M6SemanticWideningError,
    OpaqueAuditRef,
    ReceiverSnapshot,
    ReceiverState,
    ScopeCeiling,
    evaluate_actor_safe_ingress,
    make_actor_accessible_render_envelope,
    make_actor_safe_claim_entry,
    make_nonrenderable_decision,
    make_replay_closure,
    project_actor_safe_entry,
)
from rawlsing_next.render_bounded_expression import (
    BLOCKED_NAMED_AUTHORITY_REQUIRED,
    BOUND_M6_CONTRACT_ID,
    BOUND_M6_RUNTIME_BLOB,
    BOUND_M6_RUNTIME_FILE,
    BOUND_M6_RUNTIME_HEAD,
    BOUND_M6_SEMANTIC_HEAD,
    BOUND_RENDER_PREFLIGHT_HEAD,
    BOUND_SCRV2APP_HEAD,
    IG_RENDER_CONTRACT_ID,
    AdmittedRenderPlan,
    ExactAuthorityBinding,
    RenderExecutionBinding,
    RenderSemanticConformanceError,
    RenderState,
    RendererCandidate,
    current_positive_plan_authority_status,
    make_admitted_render_plan,
    realize_bounded_expression,
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
):
    return make_actor_safe_claim_entry(
        claim_ref=_ref("CLAIM", tag),
        stance_record_ref=_ref("STANCE", tag),
        accessibility_state=access,
        permitted_component_refs=components,
        first_person_permission=permission,
        memory_refs=(_ref("MEMORY", tag),),
        actor_perceived_view_refs=views,
        source_transition_refs=(_ref("TRANSITION", tag),),
    )


def _bindings(actor_id: str, entries) -> dict[str, str]:
    result = {}
    for entry in entries:
        for ref in (
            entry.stance_record_ref,
            *entry.memory_refs,
            *entry.actor_perceived_view_refs,
            *entry.source_transition_refs,
        ):
            result[ref.key] = actor_id
    return result


def _bundle(
    tag: str,
    *,
    entries=None,
    decisions=(),
    opaque=(),
    actor_id: str = "ACTOR-RENDER",
    as_of: int = 20,
):
    entries = tuple(entries if entries is not None else (_entry(tag),))
    gp = _h(f"gp:{tag}")
    actor_state = _h(f"actor:{tag}")
    memory = _h(f"memory:{tag}")
    epistemic = _h(f"epistemic:{tag}")
    closure = make_replay_closure(
        actor_id=actor_id,
        as_of_causal_time=as_of,
        source_generated_person_record_hash=gp,
        source_actor_state_hash=actor_state,
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
        source_actor_state_hash=actor_state,
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
        actor_state,
        memory,
        epistemic,
        ref_actor_bindings=_bindings(actor_id, entries),
    )
    return entries, closure, envelope, receiver


def _authority(tag: str) -> ExactAuthorityBinding:
    return ExactAuthorityBinding(f"AUTH-{tag}", "1.0.0", _h(f"authority:{tag}"))


def _execution(tag: str = "good") -> RenderExecutionBinding:
    return RenderExecutionBinding(
        _authority(f"policy-{tag}"),
        _authority(f"renderer-{tag}"),
        _ref("VARIABILITY_RECEIPT", tag),
    )


def _projection(entry, closure, envelope, receiver, *, ceiling=None, components=(), views=()):
    decision = evaluate_actor_safe_ingress(envelope, closure, receiver, entry.claim_ref)
    return project_actor_safe_entry(
        decision,
        source_scope_ceiling=ceiling or ScopeCeiling(),
        requested_claim_ref=entry.claim_ref,
        requested_first_person_permission=entry.first_person_permission,
        requested_component_refs=components,
        requested_actor_perceived_view_refs=views,
    )


def _plan(entry, closure, envelope, receiver, *, tag="plan", components=(), views=(), ceiling=None):
    projection = _projection(
        entry,
        closure,
        envelope,
        receiver,
        ceiling=ceiling,
        components=components,
        views=views,
    )
    authority = _authority(tag)
    plan = make_admitted_render_plan(
        projection,
        plan_authority=authority,
        admission_receipt_ref=_ref("SEMANTIC_PLAN_ADMISSION", tag),
        wording_variants={
            "plain": "I can say this bounded claim.",
            "alternate": "This bounded claim is available to me.",
        },
    )
    return projection, authority, plan


def _kwargs(entry, closure, envelope, receiver):
    return {
        "envelope": envelope,
        "replay_closure": closure,
        "receiver": receiver,
        "requested_claim_ref": entry.claim_ref,
        "source_scope_ceiling": ScopeCeiling(),
        "requested_first_person_permission": entry.first_person_permission,
    }


def test_runtime_is_bound_to_exact_accepted_m6_and_current_plan_authority_remains_blocked():
    assert IG_RENDER_CONTRACT_ID == "IG_RENDER_BOUNDED_REALIZATION@1.0.0"
    assert BOUND_M6_RUNTIME_HEAD == "c7dfd69131d0909cd0e4a7bec223ba64ec5d6167"
    assert BOUND_M6_RUNTIME_FILE == "rawlsing_next/m6_actor_safe_expression.py"
    assert BOUND_M6_RUNTIME_BLOB == "74d9701cdc7dabccf61eb5089498db290c1efd9c"
    assert BOUND_M6_SEMANTIC_HEAD == "a93335e577f018241d3d027bb8827a79907b9f28"
    assert BOUND_SCRV2APP_HEAD == "24f8811bb7d2eaa18cfac1cb907c48bba8d08f23"
    assert BOUND_RENDER_PREFLIGHT_HEAD == "385651927ff74c0edf3bce55a5174dfc8e59951e"
    assert BOUND_M6_CONTRACT_ID == "M6_V3_TO_V2_ACTOR_SAFE_EXPRESSION_SEAM@1.0.0"
    assert current_positive_plan_authority_status() == BLOCKED_NAMED_AUTHORITY_REQUIRED


def test_missing_admitted_semantic_plan_blocks_without_model_call():
    entries, closure, envelope, receiver = _bundle("missing-plan")
    called = []

    outcome = realize_bounded_expression(
        **_kwargs(entries[0], closure, envelope, receiver),
        renderer=lambda _: called.append(True),
    )

    assert outcome.state is RenderState.BLOCKED_NAMED_AUTHORITY_REQUIRED
    assert outcome.model_called is False
    assert outcome.semantic_output is False
    assert outcome.artifact is None
    assert not called
    assert "FINAL_ADMITTED_V2_SEMANTIC_PLAN" in outcome.block_reason


def test_exact_bound_plan_direct_variant_replays_deterministically():
    entries, closure, envelope, receiver = _bundle("replay")
    entry = entries[0]
    _, authority, plan = _plan(entry, closure, envelope, receiver, tag="replay")
    execution = _execution("replay")

    first = realize_bounded_expression(
        **_kwargs(entry, closure, envelope, receiver),
        admitted_plan=plan,
        accepted_plan_authority=authority,
        execution=execution,
        selected_variant_id="plain",
    )
    second = realize_bounded_expression(
        **_kwargs(entry, closure, envelope, receiver),
        admitted_plan=plan,
        accepted_plan_authority=authority,
        execution=execution,
        selected_variant_id="plain",
    )

    assert first.state is RenderState.ACCEPTED_BOUNDED_RENDER
    assert first.model_called is False
    assert first.semantic_output is True
    assert first.artifact == second.artifact
    assert first.artifact.semantic_authority is False
    assert first.artifact.causal_occurrence is False


def test_stale_m6_envelope_session_transcript_cannot_restore_renderability_or_call_model():
    entries, closure, envelope, receiver = _bundle("stale")
    entry = entries[0]
    stale = replace(
        receiver,
        causal_time=receiver.causal_time + 1,
        source_actor_state_hash=_h("changed-actor-state"),
    )
    called = []

    outcome = realize_bounded_expression(
        **_kwargs(entry, closure, envelope, stale),
        session_or_transcript_claim_refs=(entry.claim_ref,),
        renderer=lambda _: called.append(True),
    )

    assert outcome.state is RenderState.BLOCKED_M6_STALE
    assert outcome.receiver_state is ReceiverState.BLOCKED_STALE_ACTOR_SAFE_HANDOFF
    assert outcome.semantic_output is False
    assert outcome.model_called is False
    assert not called


@pytest.mark.parametrize("kind", ["deny", "defer", "empty"])
def test_deny_defer_and_valid_empty_produce_no_model_call_and_no_semantic_output(kind):
    claim = _ref("CLAIM", kind)
    decisions = ()
    if kind == "deny":
        decisions = (
            make_nonrenderable_decision(
                claim_ref=claim,
                permission_record_ref=_ref("PERMISSION", kind),
                accessibility_state="CLAIM_INACCESSIBLE",
                first_person_permission="DENY_FIRST_PERSON_CLAIM",
            ),
        )
    elif kind == "defer":
        decisions = (
            make_nonrenderable_decision(
                claim_ref=claim,
                permission_record_ref=_ref("PERMISSION", kind),
                accessibility_state="CLAIM_ACCESS_UNKNOWN",
                first_person_permission="DEFER_MISSING_AUTHORITY",
            ),
        )
    _, closure, envelope, receiver = _bundle(kind, entries=(), decisions=decisions)
    called = []
    permission = "PERMIT_FIRST_PERSON_BELIEF"

    outcome = realize_bounded_expression(
        envelope=envelope,
        replay_closure=closure,
        receiver=receiver,
        requested_claim_ref=claim,
        source_scope_ceiling=ScopeCeiling(),
        requested_first_person_permission=permission,
        renderer=lambda _: called.append(True),
    )

    expected = {
        "deny": RenderState.BLOCKED_M6_DENY,
        "defer": RenderState.BLOCKED_M6_DEFER,
        "empty": RenderState.VALID_EMPTY_NO_MODEL_CALL,
    }[kind]
    assert outcome.state is expected
    assert outcome.semantic_output is False
    assert outcome.model_called is False
    assert not called


def test_partial_entry_cannot_widen_to_whole_claim():
    component = _ref("COMPONENT", "allowed")
    entry = _entry(
        "partial",
        access="CLAIM_PARTIALLY_ACCESSIBLE",
        components=(component,),
    )
    _, closure, envelope, receiver = _bundle("partial", entries=(entry,))

    with pytest.raises(M6SemanticWideningError):
        realize_bounded_expression(
            **_kwargs(entry, closure, envelope, receiver),
            requested_component_refs=(),
        )


def test_actor_perceived_relationship_scope_cannot_widen():
    allowed_view = _ref("ACTOR_PERCEIVED_RELATIONSHIP_VIEW", "allowed")
    hidden_view = _ref("OBJECTIVE_RELATIONSHIP", "hidden")
    entry = _entry("relationship", views=(allowed_view,))
    _, closure, envelope, receiver = _bundle("relationship", entries=(entry,))

    with pytest.raises(M6SemanticWideningError):
        realize_bounded_expression(
            **_kwargs(entry, closure, envelope, receiver),
            requested_actor_perceived_view_refs=(hidden_view,),
        )


def test_permission_class_cannot_change():
    entry = _entry("permission", permission="PERMIT_FIRST_PERSON_BELIEF")
    _, closure, envelope, receiver = _bundle("permission", entries=(entry,))
    kwargs = _kwargs(entry, closure, envelope, receiver)
    kwargs["requested_first_person_permission"] = "PERMIT_FIRST_PERSON_KNOWLEDGE"

    with pytest.raises(M6SemanticWideningError):
        realize_bounded_expression(**kwargs)


def test_two_allowed_claims_have_no_join_surface_and_third_claim_candidate_is_rejected():
    first_entry = _entry("claim-a")
    second_entry = _entry("claim-b")
    entries, closure, envelope, receiver = _bundle(
        "two-claims", entries=(first_entry, second_entry)
    )
    projection, authority, plan = _plan(
        first_entry, closure, envelope, receiver, tag="two-claims"
    )
    execution = _execution("two-claims")
    third_claim = _ref("CLAIM", "joined-a-plus-b")

    def renderer(model_input):
        variant = model_input.allowed_variants[0]
        return RendererCandidate(
            variant.variant_id,
            variant.text,
            projection.semantic_fingerprint,
            third_claim,
            projection.component_refs,
            projection.actor_perceived_view_refs,
            projection.temporal_scope_refs,
            projection.subject_scope_refs,
            projection.referent_scope_refs,
            projection.first_person_permission,
        )

    with pytest.raises(RenderSemanticConformanceError):
        realize_bounded_expression(
            **_kwargs(first_entry, closure, envelope, receiver),
            admitted_plan=plan,
            accepted_plan_authority=authority,
            execution=execution,
            renderer=renderer,
        )


@pytest.mark.parametrize(
    "source_class",
    [
        "ResolvedStructuralContext",
        "PSEPF",
        "ActorComparatorReceipt",
        "OPAQUE_UPSTREAM_AUDIT_OR_PROVENANCE",
        "StructuralPriorRepository",
        "V557_V558_OBJECT_LOCATOR_INDEX_SELECTION_RECORD",
    ],
)
def test_m5_rsc_psepf_comparator_provenance_and_repository_sources_fail_before_model_call(source_class):
    entries, closure, envelope, receiver = _bundle(f"forbidden-{source_class}")
    called = []

    with pytest.raises(M6ForbiddenBehavioralSource):
        realize_bounded_expression(
            **_kwargs(entries[0], closure, envelope, receiver),
            forbidden_behavioral_sources=((object(), source_class, "PROMPT_OR_METADATA_SIDE_CHANNEL"),),
            renderer=lambda _: called.append(True),
        )

    assert not called


def test_opaque_audit_refs_are_behaviorally_invisible_and_not_model_visible():
    entries, closure, envelope, receiver = _bundle("opaque")
    entry = entries[0]
    projection, authority, plan = _plan(entry, closure, envelope, receiver, tag="opaque")
    execution = _execution("opaque")
    observed_inputs = []

    def renderer(model_input):
        observed_inputs.append(model_input)
        variant = model_input.allowed_variants[0]
        return RendererCandidate(
            variant.variant_id,
            variant.text,
            projection.semantic_fingerprint,
            projection.claim_ref,
            projection.component_refs,
            projection.actor_perceived_view_refs,
            projection.temporal_scope_refs,
            projection.subject_scope_refs,
            projection.referent_scope_refs,
            projection.first_person_permission,
        )

    audit_a = OpaqueAuditRef("AUDIT_ONLY_REF", "TEST", "urn:audit:a", _h("audit-a"))
    audit_b = OpaqueAuditRef("AUDIT_ONLY_REF", "TEST", "urn:audit:b", _h("audit-b"))
    first = realize_bounded_expression(
        **_kwargs(entry, closure, envelope, receiver),
        admitted_plan=plan,
        accepted_plan_authority=authority,
        execution=execution,
        renderer=renderer,
        opaque_audit_refs=(audit_a,),
    )
    second = realize_bounded_expression(
        **_kwargs(entry, closure, envelope, receiver),
        admitted_plan=plan,
        accepted_plan_authority=authority,
        execution=execution,
        renderer=renderer,
        opaque_audit_refs=(audit_b,),
    )

    assert observed_inputs[0] == observed_inputs[1]
    assert first.artifact == second.artifact
    assert first.audit_fingerprint != second.audit_fingerprint


def test_model_candidate_cannot_add_text_or_semantics_beyond_authorized_variant():
    entries, closure, envelope, receiver = _bundle("model-add")
    entry = entries[0]
    projection, authority, plan = _plan(entry, closure, envelope, receiver, tag="model-add")

    def renderer(model_input):
        variant = model_input.allowed_variants[0]
        return RendererCandidate(
            variant.variant_id,
            variant.text + " I also know a hidden fact.",
            projection.semantic_fingerprint,
            projection.claim_ref,
            projection.component_refs,
            projection.actor_perceived_view_refs,
            projection.temporal_scope_refs,
            projection.subject_scope_refs,
            projection.referent_scope_refs,
            projection.first_person_permission,
        )

    with pytest.raises(RenderSemanticConformanceError):
        realize_bounded_expression(
            **_kwargs(entry, closure, envelope, receiver),
            admitted_plan=plan,
            accepted_plan_authority=authority,
            execution=_execution("model-add"),
            renderer=renderer,
        )


def test_exact_same_governed_model_attempt_replays_at_acceptance_layer():
    entries, closure, envelope, receiver = _bundle("model-replay")
    entry = entries[0]
    projection, authority, plan = _plan(entry, closure, envelope, receiver, tag="model-replay")
    execution = _execution("model-replay")

    def renderer(model_input):
        variant = model_input.allowed_variants[1]
        return RendererCandidate(
            variant.variant_id,
            variant.text,
            projection.semantic_fingerprint,
            projection.claim_ref,
            projection.component_refs,
            projection.actor_perceived_view_refs,
            projection.temporal_scope_refs,
            projection.subject_scope_refs,
            projection.referent_scope_refs,
            projection.first_person_permission,
        )

    first = realize_bounded_expression(
        **_kwargs(entry, closure, envelope, receiver),
        admitted_plan=plan,
        accepted_plan_authority=authority,
        execution=execution,
        renderer=renderer,
    )
    second = realize_bounded_expression(
        **_kwargs(entry, closure, envelope, receiver),
        admitted_plan=plan,
        accepted_plan_authority=authority,
        execution=execution,
        renderer=renderer,
    )

    assert first.artifact == second.artifact
    assert first.artifact.artifact_hash == second.artifact.artifact_hash


@pytest.mark.parametrize(
    "spdm_class",
    [
        "SITUATED_PHENOMENOLOGY",
        "DISCLOSURE_WILLINGNESS",
        "DISCLOSURE_PLANNING",
        "SALIENCE_OR_FOREGROUND_SELECTION",
        "INHIBITION_OR_SUPPRESSION_PSYCHOLOGY",
        "AFFECTIVE_FOREGROUNDING",
        "INTERLOCUTOR_SPECIFIC_OPENNESS",
        "PSYCHOLOGICAL_REGISTER_OR_VOICE_SELECTION",
    ],
)
def test_blocked_spdm_classes_remain_named_authority_required_and_are_not_inferred(spdm_class):
    entries, closure, envelope, receiver = _bundle(f"spdm-{spdm_class}")
    called = []

    outcome = realize_bounded_expression(
        **_kwargs(entries[0], closure, envelope, receiver),
        requested_spdm_classes=(spdm_class,),
        renderer=lambda _: called.append(True),
    )

    assert outcome.state is RenderState.BLOCKED_NAMED_AUTHORITY_REQUIRED
    assert BLOCKED_NAMED_AUTHORITY_REQUIRED in outcome.block_reason
    assert outcome.model_called is False
    assert outcome.semantic_output is False
    assert not called


def test_plan_authority_mismatch_fails_closed_before_model_call():
    entries, closure, envelope, receiver = _bundle("authority-mismatch")
    entry = entries[0]
    _, authority, plan = _plan(entry, closure, envelope, receiver, tag="authority-mismatch")
    called = []

    with pytest.raises(Exception) as exc:
        realize_bounded_expression(
            **_kwargs(entry, closure, envelope, receiver),
            admitted_plan=plan,
            accepted_plan_authority=_authority("different"),
            execution=_execution("authority-mismatch"),
            renderer=lambda _: called.append(True),
        )

    assert "plan authority" in str(exc.value)
    assert not called


def test_pre_authorized_variant_is_the_only_text_surface_not_freeform_model_completion():
    entries, closure, envelope, receiver = _bundle("variant")
    entry = entries[0]
    projection, authority, plan = _plan(entry, closure, envelope, receiver, tag="variant")

    def renderer(model_input):
        assert {item.text for item in model_input.allowed_variants} == {
            "I can say this bounded claim.",
            "This bounded claim is available to me.",
        }
        return RendererCandidate(
            "not-listed",
            "An invented sentence.",
            projection.semantic_fingerprint,
            projection.claim_ref,
            projection.component_refs,
            projection.actor_perceived_view_refs,
            projection.temporal_scope_refs,
            projection.subject_scope_refs,
            projection.referent_scope_refs,
            projection.first_person_permission,
        )

    with pytest.raises(RenderSemanticConformanceError):
        realize_bounded_expression(
            **_kwargs(entry, closure, envelope, receiver),
            admitted_plan=plan,
            accepted_plan_authority=authority,
            execution=_execution("variant"),
            renderer=renderer,
        )
