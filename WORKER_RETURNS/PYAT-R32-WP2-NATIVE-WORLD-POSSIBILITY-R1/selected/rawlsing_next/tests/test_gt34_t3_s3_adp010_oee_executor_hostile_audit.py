"""Independent hostile probes for banked S3 ADP-010 bounded OEE executor.

These tests intentionally demonstrate acceptance/integrity holes in the banked
candidate. A green T3 court means the hostile reproductions are stable, not that
S3 is lawful for adoption.
"""
from dataclasses import replace
from hashlib import sha256

import rawlsing_next.v3_adp010_oee_executor as oee


def h(value: str) -> str:
    return sha256(value.encode("utf-8")).hexdigest()


def ref(kind: str, tag: str) -> oee.ExactRef:
    return oee.ExactRef(kind, f"urn:t3:{tag}", h(tag))


def lawful_shape_subject(
    *,
    subject_ref: str = "urn:rawlsing:v3:subject:sha256:" + "1" * 64,
    owner_id: str = "T3_SYNTHETIC_SUBJECT_OWNER",
    owner_version: str = "1.0.0",
    owner_hash: str | None = None,
    object_hash: str | None = None,
    materialization_kind: str = "SUBJECT_MATERIALIZATION_RECEIPT",
    use_kind: str = "CAUSAL_USE_PERMISSION",
) -> oee.SubjectIngressEvidence:
    return oee.SubjectIngressEvidence(
        subject_ref=subject_ref,
        semantic_owner_authority_id=owner_id,
        semantic_owner_authority_version=owner_version,
        semantic_owner_authority_content_hash=owner_hash or h("subject-owner"),
        semantic_object_hash=object_hash or h("subject-object"),
        materialization_receipt=ref(materialization_kind, "materialization"),
        epistemic_class=oee.EP_GENERATED_RUNTIME_FACT,
        causal_use_permission=ref(use_kind, "causal-use"),
        provenance_refs=(ref("PROVENANCE", "subject-provenance"),),
    )


def active_actor(phase_tag: str = "phase-a") -> oee.ActorPhaseEvidence:
    return oee.ActorPhaseEvidence(
        actor_id="urn:t3:actor:a",
        phase_state_ref=ref("V3DevelopmentalPhaseState", phase_tag),
        provenance_refs=(ref("PROVENANCE", "actor-provenance"),),
    )


def admit_available(
    subject: oee.SubjectIngressEvidence,
    actor: oee.ActorPhaseEvidence,
) -> oee.OEEExecutionResult:
    return oee.admit_available(
        subject=subject,
        actor=actor,
        effective_from="2031-01-01T00:00:00Z",
        effective_until="2031-01-02T00:00:00Z",
        time_granularity="INTERVAL",
        context_or_world_receipt_refs=(ref("CONTEXT_RECEIPT", "context"),),
        prior_ledger_anchor_ref=ref("LEDGER_ANCHOR", "ledger-0"),
        provenance_refs=(ref("PROVENANCE", "available-call"),),
    )


def applicability(
    *,
    authority_id: str = "T3_APPLICABILITY_OWNER_A",
    authority_version: str = "1.0.0",
    authority_hash: str | None = None,
) -> oee.PositiveApplicabilityReceipt:
    return oee.PositiveApplicabilityReceipt(
        receipt=ref("APPLICABILITY_RECEIPT", "shared-applicability-receipt"),
        authority_id=authority_id,
        authority_version=authority_version,
        authority_content_hash=authority_hash or h(authority_id),
        result="POSITIVE",
        provenance_refs=(ref("PROVENANCE", "applicability-provenance"),),
    )


def basis(
    subject: oee.SubjectIngressEvidence,
    actor: oee.ActorPhaseEvidence,
    app: oee.PositiveApplicabilityReceipt,
) -> oee.OpportunityBasisEvidence:
    return oee.OpportunityBasisEvidence(
        basis_ref=ref("ACTOR_SPECIFIC_OPPORTUNITY_BASIS", "basis"),
        actor_id=actor.actor_id,
        subject_ref=subject.subject_ref,
        applicability_receipts=(app,),
        context_or_world_receipt_refs=(ref("CONTEXT_RECEIPT", "context"),),
        position_or_other_constraint_refs=(ref("CONSTRAINT_RECEIPT", "constraint"),),
        provenance_refs=(ref("PROVENANCE", "basis-provenance"),),
    )


def admit_opportunity(
    *,
    available: oee.OEEExecutionResult,
    subject: oee.SubjectIngressEvidence,
    actor: oee.ActorPhaseEvidence,
    app: oee.PositiveApplicabilityReceipt,
) -> oee.OEEExecutionResult:
    return oee.admit_opportunity(
        parent_available=available.record,
        subject=subject,
        actor=actor,
        opportunity_basis=basis(subject, actor, app),
        effective_from="2031-01-01T08:00:00Z",
        effective_until="2031-01-01T18:00:00Z",
        time_granularity="INTERVAL",
        prior_ledger_anchor_ref=ref("LEDGER_ANCHOR", "ledger-1"),
        provenance_refs=(ref("PROVENANCE", "opportunity-call"),),
    )


def contact(
    subject: oee.SubjectIngressEvidence,
    actor: oee.ActorPhaseEvidence,
    *,
    authority_id: str = "T3_CONTACT_OWNER_A",
    authority_version: str = "1.0.0",
    authority_hash: str | None = None,
    provenance_refs: tuple[oee.ExactRef, ...] | None = None,
) -> oee.ContactOccurrenceWitness:
    return oee.ContactOccurrenceWitness(
        witness_ref=ref(oee.CONTACT_WITNESS_KIND, "shared-contact-witness"),
        witness_authority_id=authority_id,
        witness_authority_version=authority_version,
        witness_authority_content_hash=authority_hash or h(authority_id),
        actor_id=actor.actor_id,
        subject_ref=subject.subject_ref,
        occurrence_time="2031-01-01T12:00:00Z",
        semantic=oee.CONTACT_OCCURRENCE_SEMANTIC,
        independence_ref=ref(oee.CONTACT_INDEPENDENCE_KIND, "shared-independence"),
        provenance_refs=provenance_refs
        or (ref("PROVENANCE", "contact-provenance"),),
    )


def admit_encounter(
    *,
    opportunity: oee.OEEExecutionResult,
    subject: oee.SubjectIngressEvidence,
    actor: oee.ActorPhaseEvidence,
    witness: oee.ContactOccurrenceWitness,
) -> oee.OEEExecutionResult:
    return oee.admit_encounter(
        parent_opportunity=opportunity.record,
        subject=subject,
        actor=actor,
        contact_witness=witness,
        effective_time="2031-01-01T12:00:00Z",
        time_granularity="INSTANT",
        prior_ledger_anchor_ref=ref("LEDGER_ANCHOR", "ledger-2"),
        declared_precondition_refs=(ref("DECLARED_PRECONDITION", "precondition"),),
        provenance_refs=(ref("PROVENANCE", "encounter-call"),),
    )


def base_chain():
    subject = lawful_shape_subject()
    actor = active_actor()
    available = admit_available(subject, actor)
    opportunity = admit_opportunity(
        available=available,
        subject=subject,
        actor=actor,
        app=applicability(),
    )
    return subject, actor, available, opportunity


def test_s3_accepts_non_content_addressed_subject_and_wrong_evidence_kinds():
    subject = lawful_shape_subject(
        subject_ref="caller-supplied-free-form-subject",
        owner_id="UNACCEPTED_CALLER_OWNER",
        owner_version="999.999",
        materialization_kind="COLOCATION",
        use_kind="SAME_GEOGRAPHY_TIME",
    )
    result = admit_available(subject, active_actor())
    assert result.record.subject_ref == "caller-supplied-free-form-subject"
    assert any(r.kind == "COLOCATION" for r in result.record.causal_witness_refs)
    assert any(r.kind == "SAME_GEOGRAPHY_TIME" for r in result.record.causal_witness_refs)


def test_exact_phase_state_is_not_bound_into_candidate_or_record_identity():
    subject = lawful_shape_subject()
    left = admit_available(subject, active_actor("phase-state-left"))
    right = admit_available(subject, active_actor("phase-state-right"))

    assert left.record.phase_state_ref != right.record.phase_state_ref
    assert (
        left.record.source_candidate_replay_hash
        == right.record.source_candidate_replay_hash
    )
    assert left.record.record_id == right.record.record_id
    assert left.record.record_hash == right.record.record_hash


def test_applicability_authority_signature_changes_do_not_change_identity():
    subject = lawful_shape_subject()
    actor = active_actor()
    available = admit_available(subject, actor)

    left = admit_opportunity(
        available=available,
        subject=subject,
        actor=actor,
        app=applicability(
            authority_id="UNRELATED_APPLICABILITY_OWNER_A",
            authority_version="1",
            authority_hash=h("app-owner-a"),
        ),
    )
    right = admit_opportunity(
        available=available,
        subject=subject,
        actor=actor,
        app=applicability(
            authority_id="UNRELATED_APPLICABILITY_OWNER_B",
            authority_version="77",
            authority_hash=h("app-owner-b"),
        ),
    )

    assert left.record.applicability_receipt_refs == right.record.applicability_receipt_refs
    assert (
        left.record.source_candidate_replay_hash
        == right.record.source_candidate_replay_hash
    )
    assert left.record.record_id == right.record.record_id


def test_contact_witness_authority_signature_changes_do_not_change_identity():
    subject, actor, _available, opportunity = base_chain()

    left = admit_encounter(
        opportunity=opportunity,
        subject=subject,
        actor=actor,
        witness=contact(
            subject,
            actor,
            authority_id="UNACCEPTED_CONTACT_OWNER_A",
            authority_version="1",
            authority_hash=h("contact-owner-a"),
        ),
    )
    right = admit_encounter(
        opportunity=opportunity,
        subject=subject,
        actor=actor,
        witness=contact(
            subject,
            actor,
            authority_id="UNACCEPTED_CONTACT_OWNER_B",
            authority_version="999",
            authority_hash=h("contact-owner-b"),
        ),
    )

    assert left.record.causal_witness_refs == right.record.causal_witness_refs
    assert (
        left.record.source_candidate_replay_hash
        == right.record.source_candidate_replay_hash
    )
    assert left.record.record_id == right.record.record_id


def test_validate_record_accepts_semantically_tampered_uncommitted_fields():
    _subject, _actor, _available, opportunity = base_chain()
    original = opportunity.record
    tampered = replace(
        original,
        source_candidate_id="urn:t3:forged-source-candidate",
        context_or_world_receipt_refs=(ref("COLOCATION", "forged-context"),),
        applicability_receipt_refs=(ref("NEGATIVE_APPLICABILITY", "forged-negative"),),
        phase_state_ref=ref("COLOCATION", "forged-phase-state"),
        position_or_other_constraint_refs=(ref("NARRATIVE_PLAUSIBILITY", "forged-constraint"),),
        prior_ledger_anchor_ref=ref("UNRELATED_REF", "forged-ledger"),
        provenance_refs=(ref("PROVENANCE", "forged-provenance"),),
    )

    assert tampered.record_id == original.record_id
    assert tampered.record_hash == original.record_hash
    assert tampered.source_candidate_replay_hash == original.source_candidate_replay_hash
    assert oee.validate_record(tampered) == tampered


def test_colocation_can_be_laundered_by_relabeling_caller_supplied_witness():
    subject, actor, _available, opportunity = base_chain()
    witness = contact(
        subject,
        actor,
        authority_id="UNACCEPTED_CALLER_ASSERTION_OWNER",
        authority_version="not-an-accepted-authority",
        authority_hash=h("caller-assertion-owner"),
        provenance_refs=(
            ref("COLOCATION", "only-positive-evidence"),
            ref("SAME_GEOGRAPHY_TIME", "only-positive-time-evidence"),
        ),
    )
    result = admit_encounter(
        opportunity=opportunity,
        subject=subject,
        actor=actor,
        witness=witness,
    )

    assert result.record.realization_state == oee.STATE_ENCOUNTER
    assert result.record.event_effect_kind == oee.EFFECT_ENCOUNTER
    assert result.record.event_id is not None


def test_rule_and_authority_hash_provenance_is_not_mechanically_required():
    subject = lawful_shape_subject()
    result = admit_available(subject, active_actor())
    kinds = {r.kind for r in result.record.provenance_refs}
    assert not any("RULE_HASH" in kind for kind in kinds)
    assert not any("ADP010_AUTHORITY" in kind for kind in kinds)
    assert result.record.record_id.startswith("urn:rawlsing:v3:oee:record:sha256:")


def test_record_candidate_id_is_not_derived_or_validated():
    _subject, _actor, _available, opportunity = base_chain()
    forged = replace(
        opportunity.record,
        source_candidate_id="this-is-not-the-content-addressed-candidate-id",
    )
    assert forged.record_id == opportunity.record.record_id
    assert oee.validate_record(forged) == forged
