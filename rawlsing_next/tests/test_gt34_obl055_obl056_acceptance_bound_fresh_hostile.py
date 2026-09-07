from __future__ import annotations

from dataclasses import asdict, replace
from hashlib import sha256

import pytest

import rawlsing_next.gt34_adp010_input_authority_acceptance as acceptance
import rawlsing_next.v3_adp010_oee_executor_authenticated as w2
import rawlsing_next.v3_adp010_oee_executor_obl055_acceptance_bound as oee
from rawlsing_next.tests.test_gt34_obl055_obl056_acceptance_bound_repair import (
    available,
    chain,
    fixtures,
    opportunity,
    r,
    readdress_receipt,
    readdress_record,
)


def exact_auth_ref(kind: str, prefix: str, tag: str) -> oee.ExactRef:
    h = sha256(tag.encode("utf-8")).hexdigest()
    return oee.ExactRef(kind, prefix + h, h)


def replace_one_manifest(record, kind, mutate, *extra_refs):
    old = next(x for x in record.provenance_refs if x.kind == kind)
    body = oee._decode_manifest(old, kind)
    mutate(body)
    new = oee._manifest(kind, body)
    provenance = [new if x == old else x for x in record.provenance_refs]
    provenance.extend(extra_refs)
    return readdress_record(record, provenance_refs=tuple(sorted(set(provenance))))


def replace_causal_manifest(record, mutate, *extra_refs):
    kind = "OBL056_ACCEPTANCE_BINDING_" + acceptance.CAUSAL_USE_PERMISSION
    old = next(x for x in record.provenance_refs if x.kind == kind)
    body = oee._decode_manifest(old, kind)
    mutate(body)
    new = oee._manifest(kind, body)

    subject_kind = "OBL055_SUBJECT_INGRESS_REPLAY_BINDING"
    old_subject = next(x for x in record.provenance_refs if x.kind == subject_kind)
    subject_body = oee._decode_manifest(old_subject, subject_kind)
    subject_body["causal_acceptance_binding_ref"] = oee._ref_dict(new)
    new_subject = oee._manifest(subject_kind, subject_body)

    provenance = [new if x == old else new_subject if x == old_subject else x for x in record.provenance_refs]
    provenance.extend(extra_refs)
    return readdress_record(record, provenance_refs=tuple(sorted(set(provenance))))


def mutate_embedded_receipt(record, role, change):
    kind = "OBL056_ACCEPTANCE_BINDING_" + role
    old = next(x for x in record.provenance_refs if x.kind == kind)
    body = oee._decode_manifest(old, kind)
    receipt = oee._receipt_from_dict(body["receipt"])
    receipt = change(receipt)
    receipt = readdress_receipt(receipt)
    body["receipt"] = asdict(receipt)
    new = oee._manifest(kind, body)
    provenance = [new if x == old else x for x in record.provenance_refs]
    if role == acceptance.CAUSAL_USE_PERMISSION:
        subject_kind = "OBL055_SUBJECT_INGRESS_REPLAY_BINDING"
        old_subject = next(x for x in record.provenance_refs if x.kind == subject_kind)
        subject_body = oee._decode_manifest(old_subject, subject_kind)
        subject_body["causal_acceptance_binding_ref"] = oee._ref_dict(new)
        new_subject = oee._manifest(subject_kind, subject_body)
        provenance = [new_subject if x == old_subject else x for x in provenance]
    return readdress_record(record, provenance_refs=tuple(sorted(set(provenance))))


def test_h1_01_exact_frozen_target_and_authorities():
    assert oee.FROZEN_W2_EXECUTOR_BLOB == "54d9acba40f0eb1db8bb03aec3c1bb900f849588"
    assert oee.HQ_OBL056_AUTHORITY_HASH == "6c9ab99a7d89835e7fdf405511abd7d6d66ced54b6e2fd8ef1863be842f39123"
    assert oee.HQ_OBL056_IMPLEMENTATION_BLOB == "49538b9c36e58e19a6dc293ecac5bc2dff58eebe"
    assert acceptance.REGISTRY_CONTENT_HASH == oee.HQ_OBL056_EMPTY_REGISTRY_HASH


@pytest.mark.parametrize(
    "role,record_index",
    [
        (acceptance.CAUSAL_USE_PERMISSION, 3),
        (acceptance.POSITIVE_APPLICABILITY, 4),
        (acceptance.CONTACT_OCCURRENCE_WITNESS, 5),
        (acceptance.CONTACT_WITNESS_INDEPENDENCE, 5),
    ],
)
def test_h1_02_arbitrary_accepted_authority_readdress_cannot_self_issue(role, record_index):
    items = chain()
    record = items[record_index].record
    forged = mutate_embedded_receipt(
        record,
        role,
        lambda receipt: replace(
            receipt,
            accepted_authority_ref=acceptance.ContentAddressedRef(
                "CALLER_SELECTED_" + role,
                "999.0.0",
                sha256(("caller-" + role).encode()).hexdigest(),
            ),
        ),
    )
    with pytest.raises(oee.OEEIntegrityError, match="stored OBL056 acceptance receipt no longer validates"):
        oee.validate_record(forged)


@pytest.mark.parametrize(
    "change",
    [
        lambda receipt: replace(receipt, accepted_authority_owner_jurisdiction_ref=acceptance.EvidenceRef("urn:caller:owner", "1" * 64)),
        lambda receipt: replace(receipt, source_acceptance_evidence_ref=acceptance.EvidenceRef("urn:caller:source", "2" * 64)),
        lambda receipt: replace(receipt, scope=replace(receipt.scope, transition_use_scope="CALLER_RELABELLED_TRANSITION")),
        lambda receipt: replace(receipt, registry_entry_ref=acceptance.EvidenceRef("urn:caller:entry", "3" * 64)),
        lambda receipt: replace(receipt, registry_ref=acceptance.ContentAddressedRef("CALLER_REGISTRY", "1.0.0", "4" * 64)),
        lambda receipt: replace(receipt, acceptance_authority_ref=acceptance.ContentAddressedRef("CALLER_ACCEPTANCE", "1.0.0", "5" * 64)),
    ],
)
def test_h1_03_embedded_receipt_readdress_mutations_fail_exact_registry_membership(change):
    _, _, _, av = available()
    forged = mutate_embedded_receipt(av.record, acceptance.CAUSAL_USE_PERMISSION, change)
    with pytest.raises(oee.OEEIntegrityError):
        oee.validate_record(forged)


def test_h1_04_synthetic_currentness_relabel_does_not_create_current_competence():
    _, _, _, av = available()
    forged = mutate_embedded_receipt(
        av.record,
        acceptance.CAUSAL_USE_PERMISSION,
        lambda receipt: replace(receipt, currentness_state=acceptance.CURRENT_ACCEPTED),
    )
    with pytest.raises(oee.OEEIntegrityError):
        oee.validate_record(forged)
    assert acceptance.candidate_registry_artifact()["current_positive_entries"] == []


def test_h1_05_contact_receipt_role_reuse_fails():
    receipts, subject, actor, av, op = opportunity()
    witness = oee._synthetic_contact(
        subject,
        actor,
        receipts[acceptance.CONTACT_OCCURRENCE_WITNESS],
        receipts[acceptance.CONTACT_WITNESS_INDEPENDENCE],
    )
    with pytest.raises(oee.OBL055AcceptanceError):
        oee._admit_encounter_noncurrent_for_test(
            causal_use_acceptance_receipt=receipts[acceptance.CAUSAL_USE_PERMISSION],
            applicability_acceptance_receipts=(receipts[acceptance.POSITIVE_APPLICABILITY],),
            contact_occurrence_acceptance_receipt=receipts[acceptance.CONTACT_OCCURRENCE_WITNESS],
            contact_independence_acceptance_receipt=receipts[acceptance.CONTACT_OCCURRENCE_WITNESS],
            parent_opportunity=op.record,
            subject=subject,
            actor=actor,
            contact_witness=witness,
            effective_time="2031-01-01T12:00:00Z",
            time_granularity="INSTANT",
            prior_ledger_anchor_ref=r("LEDGER_ANCHOR", "h1-pair-l2"),
            declared_precondition_refs=(r("DECLARED_PRECONDITION", "h1-pair-pre"),),
            provenance_refs=(r("PROVENANCE", "h1-pair"),),
        )


@pytest.mark.parametrize("kind", ["COLOCATION", "COPRESENCE", "SAME_GEOGRAPHY_TIME", "SHARED_V555_ENDPOINT"])
def test_h1_06_proximity_cannot_be_laundered_through_valid_acceptance(kind):
    receipts, subject, actor, av, op = opportunity()
    witness = oee._synthetic_contact(
        subject,
        actor,
        receipts[acceptance.CONTACT_OCCURRENCE_WITNESS],
        receipts[acceptance.CONTACT_WITNESS_INDEPENDENCE],
        contact_basis=(r(kind, "h1-proximity-" + kind),),
    )
    with pytest.raises(oee.OEEAdmissionError):
        oee._admit_encounter_noncurrent_for_test(
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
            prior_ledger_anchor_ref=r("LEDGER_ANCHOR", "h1-prox-l2-" + kind),
            declared_precondition_refs=(r("DECLARED_PRECONDITION", "h1-prox-pre-" + kind),),
            provenance_refs=(r("PROVENANCE", "h1-prox-" + kind),),
        )


def test_h1_07_causal_semantic_ref_cannot_be_swapped_after_full_w2_readdress():
    _, _, _, av = available()
    fake = r("CAUSAL_USE_PERMISSION", "h1-fake-causal-semantic")
    forged = replace_causal_manifest(
        av.record,
        lambda body: body.__setitem__("semantic_evidence_ref", oee._ref_dict(fake)),
        fake,
    )
    with pytest.raises(oee.OEEIntegrityError):
        oee.validate_record(forged)


def test_h1_08_causal_authentication_ref_cannot_be_swapped_after_full_w2_readdress():
    _, _, _, av = available()
    fake = exact_auth_ref(
        "CAUSAL_USE_PERMISSION_AUTHENTICATION",
        "urn:rawlsing:causal-use-authentication:sha256:",
        "h1-fake-causal-auth",
    )
    forged = replace_causal_manifest(
        av.record,
        lambda body: body.__setitem__("evidence_authentication_ref", oee._ref_dict(fake)),
        fake,
    )
    with pytest.raises(oee.OEEIntegrityError):
        oee.validate_record(forged)


def test_h1_09_subject_authentication_ref_cannot_be_swapped_after_full_w2_readdress():
    _, _, _, av = available()
    fake = exact_auth_ref(
        "SUBJECT_INGRESS_AUTHENTICATION",
        "urn:rawlsing:subject-ingress-authentication:sha256:",
        "h1-fake-subject-auth",
    )
    forged = replace_one_manifest(
        av.record,
        "OBL055_SUBJECT_INGRESS_REPLAY_BINDING",
        lambda body: body.__setitem__("subject_authentication_ref", oee._ref_dict(fake)),
        fake,
    )
    with pytest.raises(oee.OEEIntegrityError):
        oee.validate_record(forged)


def test_h1_10_phase_receipt_ref_cannot_be_swapped_after_full_w2_readdress():
    _, _, _, av = available()
    fake = r("V3DevelopmentalPhaseStateReceipt", "h1-fake-phase-receipt")
    forged = replace_one_manifest(
        av.record,
        "OBL055_ADP008_PHASE_REPLAY_BINDING",
        lambda body: body.__setitem__("phase_state_receipt_ref", oee._ref_dict(fake)),
        fake,
    )
    with pytest.raises(oee.OEEIntegrityError):
        oee.validate_record(forged)


def test_h1_11_phase_authentication_ref_cannot_be_swapped_after_full_w2_readdress():
    _, _, _, av = available()
    fake = exact_auth_ref(
        "ADP008_PHASE_STATE_AUTHENTICATION",
        "urn:rawlsing:adp008-phase-authentication:sha256:",
        "h1-fake-phase-auth",
    )
    forged = replace_one_manifest(
        av.record,
        "OBL055_ADP008_PHASE_REPLAY_BINDING",
        lambda body: body.__setitem__("phase_authentication_ref", oee._ref_dict(fake)),
        fake,
    )
    with pytest.raises(oee.OEEIntegrityError):
        oee.validate_record(forged)


def test_h1_12_applicability_authentication_ref_cannot_be_swapped_after_full_w2_readdress():
    _, _, _, _, op = opportunity()
    fake = exact_auth_ref(
        "POSITIVE_APPLICABILITY_AUTHENTICATION",
        "urn:rawlsing:positive-applicability-authentication:sha256:",
        "h1-fake-app-auth",
    )
    forged = replace_one_manifest(
        op.record,
        "OBL056_ACCEPTANCE_BINDING_" + acceptance.POSITIVE_APPLICABILITY,
        lambda body: body.__setitem__("evidence_authentication_ref", oee._ref_dict(fake)),
        fake,
    )
    with pytest.raises(oee.OEEIntegrityError):
        oee.validate_record(forged)


@pytest.mark.parametrize(
    "role,field,fake",
    [
        (
            acceptance.CONTACT_OCCURRENCE_WITNESS,
            "semantic_evidence_ref",
            r("CONTACT_OCCURRENCE_WITNESS", "h1-fake-contact-semantic"),
        ),
        (
            acceptance.CONTACT_OCCURRENCE_WITNESS,
            "evidence_authentication_ref",
            exact_auth_ref(
                "CONTACT_OCCURRENCE_AUTHENTICATION",
                "urn:rawlsing:contact-occurrence-authentication:sha256:",
                "h1-fake-contact-auth",
            ),
        ),
        (
            acceptance.CONTACT_WITNESS_INDEPENDENCE,
            "semantic_evidence_ref",
            r("CONTACT_WITNESS_INDEPENDENCE_RECEIPT", "h1-fake-independence-receipt"),
        ),
        (
            acceptance.CONTACT_WITNESS_INDEPENDENCE,
            "evidence_authentication_ref",
            exact_auth_ref(
                "CONTACT_INDEPENDENCE_AUTHENTICATION",
                "urn:rawlsing:contact-independence-authentication:sha256:",
                "h1-fake-independence-auth",
            ),
        ),
    ],
)
def test_h1_13_contact_replay_constituents_cannot_be_swapped_after_full_w2_readdress(role, field, fake):
    _, _, _, _, _, en = chain()
    forged = replace_one_manifest(
        en.record,
        "OBL056_ACCEPTANCE_BINDING_" + role,
        lambda body: body.__setitem__(field, oee._ref_dict(fake)),
        fake,
    )
    with pytest.raises(oee.OEEIntegrityError):
        oee.validate_record(forged)


@pytest.mark.parametrize(
    "kind",
    ["OBL056_ACCEPTANCE_AUTHORITY_HASH", "OBL056_ACCEPTANCE_REGISTRY_HASH", "OBL056_ACCEPTANCE_RULE_HASH"],
)
def test_h1_14_obl056_fixed_provenance_removal_rejected_even_after_full_w2_readdress(kind):
    _, _, _, _, op = opportunity()
    provenance = tuple(x for x in op.record.provenance_refs if x.kind != kind)
    forged = readdress_record(op.record, provenance_refs=provenance)
    with pytest.raises(oee.OEEIntegrityError, match="missing exact HQ-current OBL056"):
        oee.validate_record(forged)


def test_h1_15_deterministic_replay_is_stable():
    receipts, subject, actor, _, _ = fixtures()
    _, _, _, left = available(receipts, subject, actor)
    _, _, _, right = available(receipts, subject, actor)
    assert left.record == right.record
    assert left.record.source_candidate_id == right.record.source_candidate_id


def test_h1_16_zero_positive_current_registry_and_no_downstream_authority_surface():
    artifact = acceptance.candidate_registry_artifact()
    assert artifact["current_positive_entries"] == []
    assert artifact["positive_fallback"] is False
    for name in ("admit_exposure", "create_comparator", "create_psepf", "mutate_actor", "issue_current_acceptance"):
        assert not hasattr(oee, name)
