from dataclasses import fields, replace
from hashlib import sha256

import pytest

import rawlsing_next.v3_adp010_oee_executor as oee


def h(x):
    return sha256(x.encode()).hexdigest()


def ref(kind, x):
    return oee.ExactRef(kind, f"urn:test:{x}", h(x))


def subject(x="s"):
    return oee.SubjectIngressEvidence(
        f"urn:test:subject:{x}",
        "SYNTHETIC_EXACT_SUBJECT_OWNER",
        "1.0.0",
        h("owner"),
        h(x),
        ref("SUBJECT_MATERIALIZATION_RECEIPT", "mat-" + x),
        oee.EP_GENERATED_RUNTIME_FACT,
        ref("CAUSAL_USE_PERMISSION", "use-" + x),
        (ref("PROVENANCE", "sp-" + x),),
    )


def actor(
    x="a",
    phase=oee.DEVELOPMENT_ACTIVE_PHASE,
    blob=oee.ADP008_AUTHORITY_ARTIFACT_BLOB_SHA,
):
    return oee.ActorPhaseEvidence(
        f"urn:test:actor:{x}",
        ref("V3DevelopmentalPhaseState", "phase-" + x),
        phase_authority_artifact_blob_sha=blob,
        base_phase_id=phase,
        provenance_refs=(ref("PROVENANCE", "ap-" + x),),
    )


def app(result="POSITIVE"):
    return oee.PositiveApplicabilityReceipt(
        ref("APPLICABILITY_RECEIPT", "app"),
        "SYNTHETIC_APPLICABILITY_OWNER",
        "1.0.0",
        h("app-owner"),
        result,
        (ref("PROVENANCE", "app-p"),),
    )


def basis(s, a, apps=None):
    return oee.OpportunityBasisEvidence(
        ref("ACTOR_SPECIFIC_OPPORTUNITY_BASIS", "basis"),
        a.actor_id,
        s.subject_ref,
        (app(),) if apps is None else apps,
        (ref("WORLD_RECEIPT", "world"), ref("CONTEXT_RECEIPT", "ctx")),
        (ref("CONSTRAINT_RECEIPT", "constraint"),),
        (ref("PROVENANCE", "basis-p"),),
    )


def contact(
    s,
    a,
    kind=oee.CONTACT_WITNESS_KIND,
    time="2030-01-01T12:00:00Z",
    semantic=oee.CONTACT_OCCURRENCE_SEMANTIC,
    ind_kind=oee.CONTACT_INDEPENDENCE_KIND,
):
    return oee.ContactOccurrenceWitness(
        ref(kind, "contact"),
        "SYNTHETIC_CONTACT_OCCURRENCE_OWNER",
        "1.0.0",
        h("contact-owner"),
        a.actor_id,
        s.subject_ref,
        time,
        semantic,
        ref(ind_kind, "ind"),
        (ref("PROVENANCE", "contact-p"),),
    )


def available(s=None, a=None, ctx=None):
    s = s or subject()
    a = a or actor()
    return s, a, oee.admit_available(
        subject=s,
        actor=a,
        effective_from="2030-01-01T00:00:00Z",
        effective_until="2030-01-02T00:00:00Z",
        time_granularity="INTERVAL",
        context_or_world_receipt_refs=ctx
        or (ref("WORLD_RECEIPT", "world"), ref("CONTEXT_RECEIPT", "ctx")),
        prior_ledger_anchor_ref=ref("LEDGER_ANCHOR", "l0"),
        provenance_refs=(ref("PROVENANCE", "av-call"),),
    )


def opportunity(s=None, a=None, av=None, b=None):
    if s is None or a is None or av is None:
        s, a, av = available(s, a)
    return s, a, av, oee.admit_opportunity(
        parent_available=av.record,
        subject=s,
        actor=a,
        opportunity_basis=b or basis(s, a),
        effective_from="2030-01-01T08:00:00Z",
        effective_until="2030-01-01T18:00:00Z",
        time_granularity="INTERVAL",
        prior_ledger_anchor_ref=ref("LEDGER_ANCHOR", "l1"),
        provenance_refs=(ref("PROVENANCE", "op-call"),),
    )


def chain():
    s, a, av, op = opportunity()
    en = oee.admit_encounter(
        parent_opportunity=op.record,
        subject=s,
        actor=a,
        contact_witness=contact(s, a),
        effective_time="2030-01-01T12:00:00Z",
        time_granularity="INSTANT",
        prior_ledger_anchor_ref=ref("LEDGER_ANCHOR", "l2"),
        declared_precondition_refs=(ref("DECLARED_PRECONDITION", "pre"),),
        provenance_refs=(ref("PROVENANCE", "en-call"),),
    )
    return s, a, av, op, en


def test_exact_authority_identities_reproduced():
    m = oee.authority_identity_manifest()
    assert m["ADP-010"] == {
        "authority_id": "V3_OPPORTUNITY_ENCOUNTER_EXPOSURE_REALIZATION_RULE",
        "authority_version": "1.0.0",
        "registry_id": "V3_OEE_REALIZATION_RULE_REGISTRY",
        "registry_version": "1.0.0",
        "artifact_path": oee.ADP010_AUTHORITY_ARTIFACT_PATH,
        "artifact_blob_sha": "0eac41d081b112255dcfc6dd42a6afab15a2928b",
    }
    assert m["ADP-008"]["authority_id"] == "V3_DEVELOPMENTAL_PHASE_RULE"
    assert m["ADP-008"]["authority_version"] == "1.1.0"
    assert m["ADP-008"]["artifact_blob_sha"] == "c6564c5c2793e9ed86ec0c5cecbcf84ff6f427d6"
    assert m["ADP-020"]["authority_id"] == "ADP-020"
    assert m["ADP-020"]["authority_version"] == "1.0.0"
    assert m["ADP-020"]["artifact_blob_sha"] == "1f13dc7ccc69bda562613d6215acc996a9c092e4"
    assert m["ADP-020"]["core_rule_rng"] == "ZERO_DRAW"


def test_subject_is_external_and_unclassified():
    names = {x.name for x in fields(oee.SubjectIngressEvidence)}
    assert not {"classification", "entity_type", "facility_type", "clinic", "hospital"} & names
    assert not hasattr(oee, "create_subject")
    assert not hasattr(oee, "classify_subject")


def test_exact_chain_parentage_subject_continuity_and_event_law():
    s, a, av, op, en = chain()
    out = oee.validate_basis_available_opportunity_encounter_chain(
        (av.record, op.record, en.record)
    )
    assert out == (av.record, op.record, en.record)
    assert {r.subject_ref for r in out} == {s.subject_ref}
    assert {r.actor_id for r in out} == {a.actor_id}
    assert av.record.event_id is None and av.record.event_effect_kind is None
    assert op.record.event_effect_kind == oee.EFFECT_OPPORTUNITY
    assert en.record.event_effect_kind == oee.EFFECT_ENCOUNTER
    assert all(r.rng_decision_receipt_ref is None for r in out)


def test_replay_is_deterministic_idempotent_and_order_canonical():
    s, a, av, op = opportunity()
    kw = dict(
        parent_opportunity=op.record,
        subject=s,
        actor=a,
        contact_witness=contact(s, a),
        effective_time="2030-01-01T12:00:00+00:00",
        time_granularity="INSTANT",
        prior_ledger_anchor_ref=ref("LEDGER_ANCHOR", "l2"),
        declared_precondition_refs=(ref("DECLARED_PRECONDITION", "pre"),),
        provenance_refs=(ref("PROVENANCE", "en-call"),),
    )
    assert oee.admit_encounter(**kw) == oee.admit_encounter(**kw)

    refs = (ref("WORLD_RECEIPT", "world"), ref("CONTEXT_RECEIPT", "ctx"))
    _, _, x = available(ctx=refs)
    _, _, y = available(ctx=tuple(reversed(refs)))
    assert x.record.record_id == y.record.record_id
    assert x.record.source_candidate_replay_hash == y.record.source_candidate_replay_hash


def test_timezone_normalization_preserves_identity():
    s, a = subject(), actor()
    kw = dict(
        subject=s,
        actor=a,
        effective_until="2030-01-02T00:00:00Z",
        time_granularity="INTERVAL",
        context_or_world_receipt_refs=(ref("WORLD_RECEIPT", "world"),),
        prior_ledger_anchor_ref=ref("LEDGER_ANCHOR", "l0"),
        provenance_refs=(ref("PROVENANCE", "p"),),
    )
    x = oee.admit_available(effective_from="2030-01-01T00:00:00Z", **kw)
    y = oee.admit_available(effective_from="2029-12-31T19:00:00-05:00", **kw)
    assert x.record.record_id == y.record.record_id


def test_changed_subject_changes_identity():
    _, a, _ = available()
    _, _, x = available(subject("x"), a)
    _, _, y = available(subject("y"), a)
    assert x.record.record_id != y.record.record_id


def test_active_phase_and_exact_adp008_binding_required():
    with pytest.raises(oee.OEEAdmissionError, match="V3DP_DEVELOPMENT_ACTIVE"):
        available(a=actor(phase="V3DP_GENERATION_PENDING"))
    with pytest.raises(oee.OEEAdmissionError, match="ADP-008"):
        available(a=actor(blob="0" * 40))


def test_opportunity_requires_positive_applicability_and_cannot_skip_parent():
    s, a, av = available()
    b = basis(s, a, (app("NEGATIVE"),))
    with pytest.raises(oee.OEEAdmissionError, match="positive applicability"):
        opportunity(s, a, av, b)

    s, a, av, op, en = chain()
    with pytest.raises(oee.OEEAdmissionError, match="expected AVAILABLE"):
        oee.admit_opportunity(
            parent_available=en.record,
            subject=s,
            actor=a,
            opportunity_basis=basis(s, a),
            effective_from="2030-01-01T13:00:00Z",
            effective_until="2030-01-01T14:00:00Z",
            time_granularity="INTERVAL",
            prior_ledger_anchor_ref=ref("LEDGER_ANCHOR", "bad"),
            provenance_refs=(ref("PROVENANCE", "bad"),),
        )


def test_parent_actor_and_subject_continuity_fail_closed():
    s, a, av = available()
    with pytest.raises(oee.OEEAdmissionError, match="subject continuity"):
        opportunity(subject("other"), a, av)
    with pytest.raises(oee.OEEAdmissionError, match="actor continuity"):
        opportunity(s, actor("other"), av)


def test_encounter_requires_independent_exact_contact_witness():
    s, a, av, op = opportunity()
    base = dict(
        parent_opportunity=op.record,
        subject=s,
        actor=a,
        effective_time="2030-01-01T12:00:00Z",
        time_granularity="INSTANT",
        prior_ledger_anchor_ref=ref("LEDGER_ANCHOR", "l2"),
        declared_precondition_refs=(ref("DECLARED_PRECONDITION", "pre"),),
        provenance_refs=(ref("PROVENANCE", "en"),),
    )
    with pytest.raises(oee.OEEAdmissionError, match="ContactOccurrenceWitness"):
        oee.admit_encounter(contact_witness=None, **base)
    with pytest.raises(oee.OEEAdmissionError, match="independence"):
        oee.admit_encounter(
            contact_witness=contact(s, a, ind_kind="COLOCATION"), **base
        )
    with pytest.raises(oee.OEEAdmissionError, match="CONTACT_OCCURRENCE"):
        oee.admit_encounter(
            contact_witness=contact(s, a, semantic="CO_PRESENCE"), **base
        )
    with pytest.raises(oee.OEEAdmissionError, match="time"):
        oee.admit_encounter(
            contact_witness=contact(s, a, time="2030-01-01T13:00:00Z"), **base
        )


@pytest.mark.parametrize(
    "kind",
    [
        "COLOCATION",
        "COPRESENCE",
        "SAME_GEOGRAPHY_TIME",
        "SHARED_V555_ENDPOINT",
        "SAME_STRUCTURAL_TARGET",
        "SAME_INSTITUTION_CATEGORY",
        "SIMULTANEOUS_RESOLVER_SELECTION",
        "NARRATIVE_PLAUSIBILITY",
    ],
)
def test_co_location_and_proximity_never_become_encounter(kind):
    s, a, av, op = opportunity()
    with pytest.raises(oee.OEEAdmissionError, match="insufficient for ENCOUNTER"):
        oee.admit_encounter(
            parent_opportunity=op.record,
            subject=s,
            actor=a,
            contact_witness=contact(s, a, kind=kind),
            effective_time="2030-01-01T12:00:00Z",
            time_granularity="INSTANT",
            prior_ledger_anchor_ref=ref("LEDGER_ANCHOR", "l2"),
            declared_precondition_refs=(ref("DECLARED_PRECONDITION", "pre"),),
            provenance_refs=(ref("PROVENANCE", "en"),),
        )


def test_contact_actor_subject_and_parent_time_must_match():
    s, a, av, op = opportunity()
    w = replace(contact(s, a), actor_id="urn:test:actor:wrong")
    with pytest.raises(oee.OEEAdmissionError, match="actor/subject mismatch"):
        oee.admit_encounter(
            parent_opportunity=op.record,
            subject=s,
            actor=a,
            contact_witness=w,
            effective_time="2030-01-01T12:00:00Z",
            time_granularity="INSTANT",
            prior_ledger_anchor_ref=ref("LEDGER_ANCHOR", "l2"),
            declared_precondition_refs=(ref("DECLARED_PRECONDITION", "pre"),),
            provenance_refs=(ref("PROVENANCE", "en"),),
        )
    with pytest.raises(oee.OEEAdmissionError, match="within active parent"):
        oee.admit_encounter(
            parent_opportunity=op.record,
            subject=s,
            actor=a,
            contact_witness=contact(s, a, time="2030-01-01T22:00:00Z"),
            effective_time="2030-01-01T22:00:00Z",
            time_granularity="INSTANT",
            prior_ledger_anchor_ref=ref("LEDGER_ANCHOR", "l2"),
            declared_precondition_refs=(ref("DECLARED_PRECONDITION", "pre"),),
            provenance_refs=(ref("PROVENANCE", "en"),),
        )


def test_malformed_hash_and_tampered_parent_fail_closed():
    s = subject()
    bad = replace(s, semantic_object_hash="bad")
    with pytest.raises(oee.OEEIntegrityError):
        available(bad, actor())

    s, a, av, op = opportunity()
    tampered = replace(op.record, source_candidate_replay_hash="0" * 64)
    with pytest.raises(oee.OEEIntegrityError, match="identity/hash mismatch"):
        oee.validate_record(tampered)


def test_no_exposure_api_no_rng_and_no_actor_or_subject_mutation():
    s, a, av, op, en = chain()
    assert not hasattr(oee, "admit_exposure")
    assert s == subject() and a == actor()
    assert all(x.record.rng_decision_receipt_ref is None for x in (av, op, en))
    with pytest.raises(Exception):
        s.subject_ref = "mutate"
    with pytest.raises(Exception):
        a.actor_id = "mutate"


def test_record_contract_fields_are_exactly_materialized():
    expected = {
        "record_id",
        "actor_id",
        "authority_id",
        "authority_version",
        "registry_id",
        "registry_version",
        "rule_id",
        "rule_version",
        "realization_state",
        "subject_ref",
        "parent_record_id",
        "effective_from",
        "effective_until",
        "time_granularity",
        "source_candidate_id",
        "source_candidate_replay_hash",
        "context_or_world_receipt_refs",
        "applicability_receipt_refs",
        "phase_state_ref",
        "position_or_other_constraint_refs",
        "causal_witness_refs",
        "rng_decision_receipt_ref",
        "event_id",
        "event_effect_kind",
        "prior_ledger_anchor_ref",
        "provenance_refs",
        "record_hash",
    }
    assert {x.name for x in fields(oee.V3OEERealizationRecord)} == expected
