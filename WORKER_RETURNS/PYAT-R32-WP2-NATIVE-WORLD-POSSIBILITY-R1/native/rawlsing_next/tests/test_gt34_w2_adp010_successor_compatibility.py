from dataclasses import fields, replace
from hashlib import sha1, sha256

import pytest

import rawlsing_next.v3_adp010_oee_executor_authenticated as oee


def r(kind, tag):
    h = sha256(tag.encode()).hexdigest()
    return oee.ExactRef(kind, f"urn:w2:test:{tag}", h)


def available(subject=None, actor=None, ctx=None):
    subject = subject or oee._synthetic_subject()
    actor = actor or oee._synthetic_actor()
    result = oee._admit_available_noncurrent_for_test(
        subject=subject,
        actor=actor,
        effective_from="2031-01-01T00:00:00Z",
        effective_until="2031-01-02T00:00:00Z",
        time_granularity="INTERVAL",
        context_or_world_receipt_refs=ctx or (r("WORLD_RECEIPT", "world"), r("CONTEXT_RECEIPT", "ctx")),
        prior_ledger_anchor_ref=r("LEDGER_ANCHOR", "l0"),
        provenance_refs=(r("PROVENANCE", "av"),),
    )
    return subject, actor, result


def opportunity(subject=None, actor=None, av=None, basis=None):
    if subject is None or actor is None or av is None:
        subject, actor, av = available(subject, actor)
    result = oee._admit_opportunity_noncurrent_for_test(
        parent_available=av.record,
        subject=subject,
        actor=actor,
        opportunity_basis=basis or oee._synthetic_basis(subject, actor),
        effective_from="2031-01-01T08:00:00Z",
        effective_until="2031-01-01T18:00:00Z",
        time_granularity="INTERVAL",
        prior_ledger_anchor_ref=r("LEDGER_ANCHOR", "l1"),
        provenance_refs=(r("PROVENANCE", "op"),),
    )
    return subject, actor, av, result


def chain():
    subject, actor, av, op = opportunity()
    en = oee._admit_encounter_noncurrent_for_test(
        parent_opportunity=op.record,
        subject=subject,
        actor=actor,
        contact_witness=oee._synthetic_contact(subject, actor),
        effective_time="2031-01-01T12:00:00Z",
        time_granularity="INSTANT",
        prior_ledger_anchor_ref=r("LEDGER_ANCHOR", "l2"),
        declared_precondition_refs=(r("DECLARED_PRECONDITION", "pre"),),
        provenance_refs=(r("PROVENANCE", "en"),),
    )
    return subject, actor, av, op, en


def test_exact_authority_identities_and_obl054_binding():
    m = oee.authority_identity_manifest()
    assert m["ADP-010"]["authority_id"] == "V3_OPPORTUNITY_ENCOUNTER_EXPOSURE_REALIZATION_RULE"
    assert m["ADP-010"]["authority_version"] == "1.0.0"
    assert m["ADP-010"]["artifact_blob_sha"] == "0eac41d081b112255dcfc6dd42a6afab15a2928b"
    assert m["ADP-008"]["authority_id"] == "V3_DEVELOPMENTAL_PHASE_RULE"
    assert m["ADP-008"]["authority_version"] == "1.1.0"
    assert m["ADP-008"]["artifact_blob_sha"] == "c6564c5c2793e9ed86ec0c5cecbcf84ff6f427d6"
    assert m["ADP-020"]["authority_id"] == "ADP-020"
    assert m["ADP-020"]["core_rule_rng"] == "ZERO_DRAW"
    assert m["OBL054"] == {
        "adoption_artifact_blob": "fc46d377dafa5b2c4e274d702e7f26268aa429cb",
        "materializer_id": "GT34_V3P1_CORRECTED_OWNER_AUTHENTICATED_ONE_OBJECT_SUBJECT_MATERIALIZER",
        "materializer_version": "2.0.0",
        "accepted_root_hash": "1563a1661d3e0a76e6781633f1b590147e26ab21014674bbe732f68cef6acfa8",
        "permit_id": "urn:rawlsing:gt34:obl054:one-object-materialization-permit:sha256:3eeea2dcfa0a70f1a5b6ce15d41d9f83d84e39ecde816896150fff21e77573dc",
        "permit_hash": "3eeea2dcfa0a70f1a5b6ce15d41d9f83d84e39ecde816896150fff21e77573dc",
        "historical_invalid_obl053_adoption_blob": "286ff7b851e920ff2760082d8b2fb194560ab127",
    }


def test_successor_has_distinct_identity_and_preserves_historical_ids():
    m = oee.authority_identity_manifest()
    assert m["successor"] == {
        "executor_id": "GT34_V3P5_ADP010_AUTHENTICATED_REPLAY_EXECUTOR",
        "executor_version": "2.0.0",
    }
    assert m["historical_S3"]["semantic_candidate_sha"] == "5bed04b83f0dc61e500da26130892e46ce9c86ff"
    assert m["historical_S3"]["module_blob_sha"] == "cd6e978eea25384482ef2ab75547b8d33bcc4fb7"


def test_subject_surface_is_external_and_unclassified():
    names = {f.name for f in fields(oee.SubjectIngressEvidence)}
    assert not {"classification", "entity_type", "facility_type", "clinic", "hospital"} & names
    assert not hasattr(oee, "create_subject")
    assert not hasattr(oee, "classify_subject")


def test_exact_chain_parentage_and_event_law():
    subject, actor, av, op, en = chain()
    out = oee.validate_basis_available_opportunity_encounter_chain((av.record, op.record, en.record))
    assert out == (av.record, op.record, en.record)
    assert {x.subject_ref for x in out} == {subject.subject_ref}
    assert {x.actor_id for x in out} == {actor.actor_id}
    assert av.record.event_id is None and av.record.event_effect_kind is None
    assert op.record.event_effect_kind == oee.EFFECT_OPPORTUNITY
    assert en.record.event_effect_kind == oee.EFFECT_ENCOUNTER


def test_replay_is_deterministic_idempotent_and_ref_order_canonical():
    subject, actor, av, op = opportunity()
    kw = dict(
        parent_opportunity=op.record,
        subject=subject,
        actor=actor,
        contact_witness=oee._synthetic_contact(subject, actor),
        effective_time="2031-01-01T12:00:00+00:00",
        time_granularity="INSTANT",
        prior_ledger_anchor_ref=r("LEDGER_ANCHOR", "l2"),
        declared_precondition_refs=(r("DECLARED_PRECONDITION", "pre"),),
        provenance_refs=(r("PROVENANCE", "en"),),
    )
    x = oee._admit_encounter_noncurrent_for_test(**kw)
    y = oee._admit_encounter_noncurrent_for_test(**kw)
    assert x == y

    refs = (r("WORLD_RECEIPT", "world2"), r("CONTEXT_RECEIPT", "ctx2"))
    _, _, left = available(ctx=refs)
    _, _, right = available(ctx=tuple(reversed(refs)))
    assert left.record.record_id == right.record.record_id
    assert left.record.source_candidate_replay_hash == right.record.source_candidate_replay_hash


def test_timezone_normalization_preserves_identity():
    subject = oee._synthetic_subject()
    actor = oee._synthetic_actor()
    common = dict(
        subject=subject,
        actor=actor,
        effective_until="2031-01-02T00:00:00Z",
        time_granularity="INTERVAL",
        context_or_world_receipt_refs=(r("WORLD_RECEIPT", "world-tz"),),
        prior_ledger_anchor_ref=r("LEDGER_ANCHOR", "tz-l0"),
        provenance_refs=(r("PROVENANCE", "tz-prov"),),
    )
    x = oee._admit_available_noncurrent_for_test(effective_from="2031-01-01T00:00:00Z", **common)
    y = oee._admit_available_noncurrent_for_test(effective_from="2030-12-31T19:00:00-05:00", **common)
    assert x.record.record_id == y.record.record_id


def test_changed_subject_changes_identity():
    _, actor, _ = available()
    _, _, x = available(oee._synthetic_subject("left"), actor)
    _, _, y = available(oee._synthetic_subject("right"), actor)
    assert x.record.record_id != y.record.record_id


def test_exact_adp008_active_phase_required():
    actor = oee._synthetic_actor()
    broken = replace(actor, base_phase_id="V3DP_GENERATION_PENDING")
    with pytest.raises(oee.OEEAdmissionError, match="V3DP_DEVELOPMENT_ACTIVE"):
        available(actor=broken)


def test_exact_adp008_registry_authentication_required():
    actor = oee._synthetic_actor()
    broken = replace(actor, phase_registry_content_hash="0" * 64)
    with pytest.raises(oee.OEEAdmissionError, match="ADP-008"):
        available(actor=broken)


def test_opportunity_requires_positive_applicability():
    subject, actor, av = available()
    app = oee._synthetic_app()
    negative = replace(app, result="NEGATIVE")
    b = replace(oee._synthetic_basis(subject, actor), applicability_receipts=(negative,))
    with pytest.raises(oee.OEEAdmissionError, match="positive applicability"):
        opportunity(subject, actor, av, b)


def test_opportunity_cannot_skip_parent():
    subject, actor, av, op, en = chain()
    with pytest.raises(oee.OEEAdmissionError, match="expected AVAILABLE"):
        oee._admit_opportunity_noncurrent_for_test(
            parent_available=en.record,
            subject=subject,
            actor=actor,
            opportunity_basis=oee._synthetic_basis(subject, actor),
            effective_from="2031-01-01T13:00:00Z",
            effective_until="2031-01-01T14:00:00Z",
            time_granularity="INTERVAL",
            prior_ledger_anchor_ref=r("LEDGER_ANCHOR", "bad"),
            provenance_refs=(r("PROVENANCE", "bad"),),
        )


def test_parent_subject_continuity_fails_closed():
    subject, actor, av = available()
    with pytest.raises(oee.OEEAdmissionError, match="subject continuity"):
        opportunity(oee._synthetic_subject("other"), actor, av)


def test_parent_actor_continuity_fails_closed():
    subject, actor, av = available()
    with pytest.raises(oee.OEEAdmissionError, match="actor continuity"):
        opportunity(subject, oee._synthetic_actor("other"), av)


def test_encounter_requires_contact_witness_object():
    subject, actor, av, op = opportunity()
    with pytest.raises(oee.OEEAdmissionError, match="ContactOccurrenceWitness"):
        oee._admit_encounter_noncurrent_for_test(
            parent_opportunity=op.record,
            subject=subject,
            actor=actor,
            contact_witness=None,
            effective_time="2031-01-01T12:00:00Z",
            time_granularity="INSTANT",
            prior_ledger_anchor_ref=r("LEDGER_ANCHOR", "l2-null"),
            declared_precondition_refs=(r("DECLARED_PRECONDITION", "pre-null"),),
            provenance_refs=(r("PROVENANCE", "null"),),
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
def test_direct_insufficient_contact_kinds_never_become_encounter(kind):
    subject, actor, av, op = opportunity()
    witness = oee._synthetic_contact(subject, actor, witness_kind=kind)
    with pytest.raises(oee.OEEAdmissionError, match="insufficient for ENCOUNTER"):
        oee._admit_encounter_noncurrent_for_test(
            parent_opportunity=op.record,
            subject=subject,
            actor=actor,
            contact_witness=witness,
            effective_time="2031-01-01T12:00:00Z",
            time_granularity="INSTANT",
            prior_ledger_anchor_ref=r("LEDGER_ANCHOR", "l2-" + kind),
            declared_precondition_refs=(r("DECLARED_PRECONDITION", "pre-" + kind),),
            provenance_refs=(r("PROVENANCE", "p-" + kind),),
        )


def test_contact_actor_subject_must_match():
    subject, actor, av, op = opportunity()
    witness = replace(oee._synthetic_contact(subject, actor), actor_id="urn:w2:wrong")
    with pytest.raises(oee.OEEAdmissionError, match="actor/subject mismatch"):
        oee._admit_encounter_noncurrent_for_test(
            parent_opportunity=op.record,
            subject=subject,
            actor=actor,
            contact_witness=witness,
            effective_time="2031-01-01T12:00:00Z",
            time_granularity="INSTANT",
            prior_ledger_anchor_ref=r("LEDGER_ANCHOR", "l2-actor"),
            declared_precondition_refs=(r("DECLARED_PRECONDITION", "pre-actor"),),
            provenance_refs=(r("PROVENANCE", "p-actor"),),
        )


def test_contact_time_must_match_and_remain_in_parent():
    subject, actor, av, op = opportunity()
    witness = oee._synthetic_contact(subject, actor, occurrence_time="2031-01-01T22:00:00Z")
    with pytest.raises(oee.OEEAdmissionError, match="within active parent"):
        oee._admit_encounter_noncurrent_for_test(
            parent_opportunity=op.record,
            subject=subject,
            actor=actor,
            contact_witness=witness,
            effective_time="2031-01-01T22:00:00Z",
            time_granularity="INSTANT",
            prior_ledger_anchor_ref=r("LEDGER_ANCHOR", "l2-time"),
            declared_precondition_refs=(r("DECLARED_PRECONDITION", "pre-time"),),
            provenance_refs=(r("PROVENANCE", "p-time"),),
        )


def test_malformed_hash_fails_closed():
    subject = oee._synthetic_subject()
    broken = replace(subject, semantic_owner_authority_content_hash="bad")
    with pytest.raises(oee.OEEIntegrityError):
        available(broken, oee._synthetic_actor())


def test_tampered_parent_fails_closed():
    subject, actor, av, op = opportunity()
    tampered = replace(op.record, source_candidate_replay_hash="0" * 64)
    with pytest.raises(oee.OEEIntegrityError, match="source candidate replay hash mismatch"):
        oee.validate_record(tampered)


def test_no_exposure_no_rng_no_mutation():
    subject, actor, av, op, en = chain()
    assert not hasattr(oee, "admit_exposure")
    assert all(x.record.rng_decision_receipt_ref is None for x in (av, op, en))
    with pytest.raises(Exception):
        subject.subject_ref = "mutate"
    with pytest.raises(Exception):
        actor.actor_id = "mutate"


def test_record_contract_fields_exactly_preserved():
    expected = {
        "record_id", "actor_id", "authority_id", "authority_version",
        "registry_id", "registry_version", "rule_id", "rule_version",
        "realization_state", "subject_ref", "parent_record_id",
        "effective_from", "effective_until", "time_granularity",
        "source_candidate_id", "source_candidate_replay_hash",
        "context_or_world_receipt_refs", "applicability_receipt_refs",
        "phase_state_ref", "position_or_other_constraint_refs",
        "causal_witness_refs", "rng_decision_receipt_ref",
        "event_id", "event_effect_kind", "prior_ledger_anchor_ref",
        "provenance_refs", "record_hash",
    }
    assert {f.name for f in fields(oee.V3OEERealizationRecord)} == expected
