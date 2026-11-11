from __future__ import annotations

from hashlib import sha256

import pytest

import rawlsing_next.gt34_adp010_input_authority_acceptance as acceptance
import rawlsing_next.v3_adp010_oee_executor_obl055_acceptance_bound as r1
import rawlsing_next.v3_adp010_oee_executor_obl055_replay_reconstructed as oee


def r(kind: str, tag: str) -> oee.ExactRef:
    h = sha256(tag.encode()).hexdigest()
    return oee.ExactRef(kind, f"urn:obl055:r2:{tag}", h)


def exact_auth(kind: str, prefix: str, tag: str) -> oee.ExactRef:
    h = sha256(tag.encode()).hexdigest()
    return oee.ExactRef(kind, prefix + h, h)


def fixtures():
    receipts = oee.synthetic_acceptance_receipts()
    subject = oee._synthetic_subject(receipts[acceptance.CAUSAL_USE_PERMISSION])
    actor = oee._synthetic_actor()
    app = oee._synthetic_app(receipts[acceptance.POSITIVE_APPLICABILITY])
    basis = oee._synthetic_basis(subject, actor, app)
    return receipts, subject, actor, app, basis


def available():
    receipts, subject, actor, app, basis = fixtures()
    av = oee._admit_available_noncurrent_for_test(
        causal_use_acceptance_receipt=receipts[acceptance.CAUSAL_USE_PERMISSION],
        subject=subject,
        actor=actor,
        effective_from="2031-01-01T00:00:00Z",
        effective_until="2031-01-02T00:00:00Z",
        time_granularity="INTERVAL",
        context_or_world_receipt_refs=(r("WORLD_RECEIPT", "world"), r("CONTEXT_RECEIPT", "context")),
        prior_ledger_anchor_ref=r("LEDGER_ANCHOR", "l0"),
        provenance_refs=(r("PROVENANCE", "available"),),
    )
    return receipts, subject, actor, app, basis, av


def opportunity():
    receipts, subject, actor, app, basis, av = available()
    op = oee._admit_opportunity_noncurrent_for_test(
        causal_use_acceptance_receipt=receipts[acceptance.CAUSAL_USE_PERMISSION],
        applicability_acceptance_receipts=(receipts[acceptance.POSITIVE_APPLICABILITY],),
        parent_available=av.record,
        subject=subject,
        actor=actor,
        opportunity_basis=basis,
        effective_from="2031-01-01T08:00:00Z",
        effective_until="2031-01-01T18:00:00Z",
        time_granularity="INTERVAL",
        prior_ledger_anchor_ref=r("LEDGER_ANCHOR", "l1"),
        provenance_refs=(r("PROVENANCE", "opportunity"),),
    )
    return receipts, subject, actor, app, basis, av, op


def chain():
    receipts, subject, actor, app, basis, av, op = opportunity()
    witness = oee._synthetic_contact(
        subject,
        actor,
        receipts[acceptance.CONTACT_OCCURRENCE_WITNESS],
        receipts[acceptance.CONTACT_WITNESS_INDEPENDENCE],
    )
    en = oee._admit_encounter_noncurrent_for_test(
        causal_use_acceptance_receipt=receipts[acceptance.CAUSAL_USE_PERMISSION],
        applicability_acceptance_receipts=(receipts[acceptance.POSITIVE_APPLICABILITY],),
        contact_occurrence_acceptance_receipt=receipts[acceptance.CONTACT_OCCURRENCE_WITNESS],
        contact_independence_acceptance_receipt=receipts[acceptance.CONTACT_WITNESS_INDEPENDENCE],
        parent_opportunity=op.record,
        subject=subject,
        actor=actor,
        contact_witness=witness,
        effective_time="2031-01-01T12:00:00Z",
        time_granularity="INSTANT",
        prior_ledger_anchor_ref=r("LEDGER_ANCHOR", "l2"),
        declared_precondition_refs=(r("DECLARED_PRECONDITION", "pre"),),
        provenance_refs=(r("PROVENANCE", "encounter"),),
    )
    return receipts, subject, actor, app, basis, witness, av, op, en


def replace_one_r1_manifest(record, kind, mutate, *extra_refs):
    old = next(x for x in record.provenance_refs if x.kind == kind)
    body = r1._decode_manifest(old, kind)
    mutate(body)
    new = r1._manifest(kind, body)
    provenance = [new if x == old else x for x in record.provenance_refs]
    provenance.extend(extra_refs)
    return oee._readdress(record, provenance)


def replace_causal_r1_manifest(record, mutate, *extra_refs):
    kind = "OBL056_ACCEPTANCE_BINDING_" + acceptance.CAUSAL_USE_PERMISSION
    old = next(x for x in record.provenance_refs if x.kind == kind)
    body = r1._decode_manifest(old, kind)
    mutate(body)
    new = r1._manifest(kind, body)
    skind = "OBL055_SUBJECT_INGRESS_REPLAY_BINDING"
    sold = next(x for x in record.provenance_refs if x.kind == skind)
    sbody = r1._decode_manifest(sold, skind)
    sbody["causal_acceptance_binding_ref"] = r1._ref_dict(new)
    snew = r1._manifest(skind, sbody)
    provenance = [new if x == old else snew if x == sold else x for x in record.provenance_refs]
    provenance.extend(extra_refs)
    return oee._readdress(record, provenance)


def test_r2_01_mechanical_chain_reconstructs_all_source_objects():
    *_, av, op, en = chain()
    out = oee.validate_basis_available_opportunity_encounter_chain((av.record, op.record, en.record))
    assert out == (av.record, op.record, en.record)
    for record in out:
        assert oee.R2_SUCCESSOR_REF in record.provenance_refs
        body = oee._state_bundle(record)
        assert body["state"] == record.realization_state
        assert body["subject_ingress_evidence"]
        assert body["actor_phase_evidence"]
        assert body["causal_use_acceptance_receipt"]


def test_r2_02_h1_causal_semantic_ref_swap_is_closed():
    *_, av = available()
    fake = r("CAUSAL_USE_PERMISSION", "fake-causal-semantic")
    forged = replace_causal_r1_manifest(av.record, lambda b: b.__setitem__("semantic_evidence_ref", r1._ref_dict(fake)), fake)
    with pytest.raises(oee.OEEIntegrityError):
        oee.validate_record(forged)


def test_r2_03_h1_causal_auth_ref_swap_is_closed():
    *_, av = available()
    fake = exact_auth("CAUSAL_USE_PERMISSION_AUTHENTICATION", "urn:rawlsing:causal-use-authentication:sha256:", "fake-causal-auth")
    forged = replace_causal_r1_manifest(av.record, lambda b: b.__setitem__("evidence_authentication_ref", r1._ref_dict(fake)), fake)
    with pytest.raises(oee.OEEIntegrityError):
        oee.validate_record(forged)


def test_r2_04_h1_subject_auth_ref_swap_is_closed():
    *_, av = available()
    fake = exact_auth("SUBJECT_INGRESS_AUTHENTICATION", "urn:rawlsing:subject-ingress-authentication:sha256:", "fake-subject-auth")
    forged = replace_one_r1_manifest(av.record, "OBL055_SUBJECT_INGRESS_REPLAY_BINDING", lambda b: b.__setitem__("subject_authentication_ref", r1._ref_dict(fake)), fake)
    with pytest.raises(oee.OEEIntegrityError):
        oee.validate_record(forged)


@pytest.mark.parametrize(
    "field,fake",
    [
        ("phase_state_receipt_ref", r("V3DevelopmentalPhaseStateReceipt", "fake-phase-receipt")),
        ("phase_authentication_ref", exact_auth("ADP008_PHASE_STATE_AUTHENTICATION", "urn:rawlsing:adp008-phase-authentication:sha256:", "fake-phase-auth")),
    ],
)
def test_r2_05_h1_phase_pointer_swaps_are_closed(field, fake):
    *_, av = available()
    forged = replace_one_r1_manifest(av.record, "OBL055_ADP008_PHASE_REPLAY_BINDING", lambda b: b.__setitem__(field, r1._ref_dict(fake)), fake)
    with pytest.raises(oee.OEEIntegrityError):
        oee.validate_record(forged)


def test_r2_06_h1_app_auth_ref_swap_is_closed():
    *_, op = opportunity()
    fake = exact_auth("POSITIVE_APPLICABILITY_AUTHENTICATION", "urn:rawlsing:positive-applicability-authentication:sha256:", "fake-app-auth")
    forged = replace_one_r1_manifest(op.record, "OBL056_ACCEPTANCE_BINDING_" + acceptance.POSITIVE_APPLICABILITY, lambda b: b.__setitem__("evidence_authentication_ref", r1._ref_dict(fake)), fake)
    with pytest.raises(oee.OEEIntegrityError):
        oee.validate_record(forged)


@pytest.mark.parametrize(
    "role,field,fake",
    [
        (acceptance.CONTACT_OCCURRENCE_WITNESS, "semantic_evidence_ref", r("CONTACT_OCCURRENCE_WITNESS", "fake-contact-semantic")),
        (acceptance.CONTACT_OCCURRENCE_WITNESS, "evidence_authentication_ref", exact_auth("CONTACT_OCCURRENCE_AUTHENTICATION", "urn:rawlsing:contact-occurrence-authentication:sha256:", "fake-contact-auth")),
        (acceptance.CONTACT_WITNESS_INDEPENDENCE, "semantic_evidence_ref", r("CONTACT_WITNESS_INDEPENDENCE_RECEIPT", "fake-independence-receipt")),
        (acceptance.CONTACT_WITNESS_INDEPENDENCE, "evidence_authentication_ref", exact_auth("CONTACT_INDEPENDENCE_AUTHENTICATION", "urn:rawlsing:contact-independence-authentication:sha256:", "fake-independence-auth")),
    ],
)
def test_r2_07_h1_contact_pointer_swaps_are_closed(role, field, fake):
    *_, en = chain()
    forged = replace_one_r1_manifest(en.record, "OBL056_ACCEPTANCE_BINDING_" + role, lambda b: b.__setitem__(field, r1._ref_dict(fake)), fake)
    with pytest.raises(oee.OEEIntegrityError):
        oee.validate_record(forged)


def test_r2_08_source_bundle_itself_cannot_be_relabelled_and_readdressed():
    *_, av = available()
    old = next(x for x in av.record.provenance_refs if x.kind == oee._BUNDLE_KIND[oee.STATE_AVAILABLE])
    body = oee._decode_bundle(old, oee.STATE_AVAILABLE)
    fake = exact_auth("SUBJECT_INGRESS_AUTHENTICATION", "urn:rawlsing:subject-ingress-authentication:sha256:", "bundle-fake-subject-auth")
    body["subject_ingress_evidence"]["authentication_ref"] = r1._ref_dict(fake)
    new = oee._bundle_ref(oee.STATE_AVAILABLE, body)
    provenance = [new if x == old else x for x in av.record.provenance_refs]
    provenance.append(fake)
    forged = oee._readdress(av.record, provenance)
    with pytest.raises(oee.OEEIntegrityError, match="subject ingress authentication mismatch"):
        oee.validate_record(forged)


def test_r2_09_zero_positive_and_no_semantic_authority_widening():
    assert acceptance.candidate_registry_artifact()["current_positive_entries"] == []
    assert acceptance.candidate_registry_artifact()["positive_fallback"] is False
    for name in ("admit_exposure", "create_comparator", "create_psepf", "mutate_actor", "issue_current_acceptance"):
        assert not hasattr(oee, name)
    manifest = oee.authority_identity_manifest()
    assert manifest["successor"]["frozen_w2_executor_blob"] == oee.FROZEN_W2_EXECUTOR_BLOB
    assert manifest["successor"]["frozen_r1_repair_blob"] == oee.FROZEN_R1_REPAIR_BLOB
