from dataclasses import replace
from hashlib import sha256

import pytest

import rawlsing_next.v3_adp010_oee_executor_authenticated as oee
from rawlsing_next.tests.test_gt34_w2_adp010_successor_compatibility import (
    r, available, opportunity, chain
)


def test_t3_01_caller_shaped_subject_and_wrong_evidence_kinds_fail():
    subject = oee._synthetic_subject()
    free = replace(
        subject,
        subject_ref="caller-supplied-free-form-subject",
        obl054_adoption_artifact_blob=oee.OBL054_ADOPTION_ARTIFACT_BLOB,
    )
    with pytest.raises(oee.OEEAdmissionError):
        available(free, oee._synthetic_actor())


def test_t3_02_phase_state_changes_replay_and_record_identity():
    subject = oee._synthetic_subject()
    left_actor = oee._synthetic_actor(phase_tag="left")
    right_actor = oee._synthetic_actor(phase_tag="right")
    right_actor = replace(right_actor, actor_id=left_actor.actor_id)
    right_actor = replace(
        right_actor,
        authentication_ref=oee._content_ref(
            "ADP008_PHASE_STATE_AUTHENTICATION",
            "urn:rawlsing:adp008-phase-authentication:sha256:",
            oee._phase_material(right_actor),
        ),
    )
    _, _, left = available(subject, left_actor)
    _, _, right = available(subject, right_actor)
    assert left.record.phase_state_ref != right.record.phase_state_ref
    assert left.record.source_candidate_replay_hash != right.record.source_candidate_replay_hash
    assert left.record.record_id != right.record.record_id


def test_t3_03_applicability_authority_signature_changes_identity():
    subject, actor, av = available()
    left = oee._synthetic_app(authority_tag="A")
    right = oee._synthetic_app(authority_tag="B")
    b_left = oee._synthetic_basis(subject, actor, left)
    b_right = oee._synthetic_basis(subject, actor, right)
    _, _, _, op_left = opportunity(subject, actor, av, b_left)
    _, _, _, op_right = opportunity(subject, actor, av, b_right)
    assert op_left.record.applicability_receipt_refs == op_right.record.applicability_receipt_refs
    assert op_left.record.source_candidate_replay_hash != op_right.record.source_candidate_replay_hash
    assert op_left.record.record_id != op_right.record.record_id


def test_t3_04_contact_authority_signature_changes_identity():
    subject, actor, av, op = opportunity()
    left = oee._synthetic_contact(subject, actor, authority_tag="A")
    right = oee._synthetic_contact(subject, actor, authority_tag="B")
    common = dict(
        parent_opportunity=op.record,
        subject=subject,
        actor=actor,
        effective_time="2031-01-01T12:00:00Z",
        time_granularity="INSTANT",
        prior_ledger_anchor_ref=r("LEDGER_ANCHOR", "contact-id"),
        declared_precondition_refs=(r("DECLARED_PRECONDITION", "contact-pre"),),
        provenance_refs=(r("PROVENANCE", "contact-prov"),),
    )
    en_left = oee._admit_encounter_noncurrent_for_test(contact_witness=left, **common)
    en_right = oee._admit_encounter_noncurrent_for_test(contact_witness=right, **common)
    assert en_left.record.causal_witness_refs == en_right.record.causal_witness_refs
    assert en_left.record.source_candidate_replay_hash != en_right.record.source_candidate_replay_hash
    assert en_left.record.record_id != en_right.record.record_id


@pytest.mark.parametrize(
    "field,value",
    [
        ("source_candidate_id", "urn:w2:forged-candidate"),
        ("context_or_world_receipt_refs", (r("COLOCATION", "forged-context"),)),
        ("applicability_receipt_refs", (r("NEGATIVE_APPLICABILITY", "forged-app"),)),
        ("phase_state_ref", r("V3DevelopmentalPhaseState", "forged-phase")),
        ("position_or_other_constraint_refs", (r("NARRATIVE_PLAUSIBILITY", "forged-constraint"),)),
        ("prior_ledger_anchor_ref", r("UNRELATED_REF", "forged-ledger")),
        ("provenance_refs", (r("PROVENANCE", "forged-prov"),)),
    ],
)
def test_t3_05_validate_record_rejects_all_previously_uncommitted_tampering(field, value):
    _, _, _, op = opportunity()
    tampered = replace(op.record, **{field: value})
    with pytest.raises(oee.OEEIntegrityError):
        oee.validate_record(tampered)


@pytest.mark.parametrize(
    "bad_kind",
    [
        "COLOCATION",
        "COPRESENCE",
        "SAME_GEOGRAPHY_TIME",
        "SHARED_V555_ENDPOINT",
        "SAME_STRUCTURAL_TARGET",
        "SAME_INSTITUTION_CATEGORY",
        "NARRATIVE_PLAUSIBILITY",
    ],
)
def test_t3_06_colocation_cannot_be_laundered_inside_authenticated_contact_wrapper(bad_kind):
    subject, actor, av, op = opportunity()
    witness = oee._synthetic_contact(
        subject,
        actor,
        contact_basis=(r(bad_kind, "only-positive-evidence-" + bad_kind),),
    )
    with pytest.raises(oee.OEEAdmissionError, match="laundered"):
        oee._admit_encounter_noncurrent_for_test(
            parent_opportunity=op.record,
            subject=subject,
            actor=actor,
            contact_witness=witness,
            effective_time="2031-01-01T12:00:00Z",
            time_granularity="INSTANT",
            prior_ledger_anchor_ref=r("LEDGER_ANCHOR", "launder-" + bad_kind),
            declared_precondition_refs=(r("DECLARED_PRECONDITION", "pre-" + bad_kind),),
            provenance_refs=(r("PROVENANCE", "p-" + bad_kind),),
        )


def test_t3_07_exact_rule_and_authority_hash_provenance_is_required():
    _, _, _, op = opportunity()
    stripped = tuple(
        x for x in op.record.provenance_refs
        if x.kind not in {"ADP010_AUTHORITY_HASH", "ADP010_REGISTRY_HASH", "ADP010_RULE_HASH"}
    )
    tampered = replace(op.record, provenance_refs=stripped)
    with pytest.raises(oee.OEEIntegrityError, match="missing exact accepted"):
        oee.validate_record(tampered)


def test_t3_08_source_candidate_id_is_derived_and_validated():
    _, _, _, op = opportunity()
    forged = replace(op.record, source_candidate_id="this-is-not-content-addressed")
    with pytest.raises(oee.OEEIntegrityError, match="source_candidate_id"):
        oee.validate_record(forged)
