from __future__ import annotations

from dataclasses import replace
from hashlib import sha1, sha256
from pathlib import Path

import pytest

import rawlsing_next.gt34_adp010_input_authority_acceptance as acceptance
import rawlsing_next.v3_adp010_oee_executor_authenticated as w2
import rawlsing_next.v3_adp010_oee_executor_obl055_acceptance_bound as oee


ROOT = Path(__file__).resolve().parents[2]
EXPECTED_W2_BLOB = "54d9acba40f0eb1db8bb03aec3c1bb900f849588"


def r(kind: str, tag: str) -> oee.ExactRef:
    h = sha256(tag.encode("utf-8")).hexdigest()
    return oee.ExactRef(kind, f"urn:obl055:test:{tag}", h)


def git_blob(path: str) -> str:
    raw = (ROOT / path).read_bytes()
    return sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()


def fixtures():
    receipts = oee.synthetic_acceptance_receipts()
    subject = oee._synthetic_subject(receipts[acceptance.CAUSAL_USE_PERMISSION])
    actor = oee._synthetic_actor()
    app = oee._synthetic_app(receipts[acceptance.POSITIVE_APPLICABILITY])
    basis = oee._synthetic_basis(subject, actor, app)
    return receipts, subject, actor, app, basis


def available(receipts=None, subject=None, actor=None):
    if receipts is None or subject is None or actor is None:
        receipts, subject, actor, _, _ = fixtures()
    out = oee._admit_available_noncurrent_for_test(
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
    return receipts, subject, actor, out


def opportunity(receipts=None, subject=None, actor=None, av=None, basis=None):
    if receipts is None or subject is None or actor is None or av is None:
        receipts, subject, actor, app, default_basis = fixtures()
        _, _, _, av = available(receipts, subject, actor)
        basis = basis or default_basis
    elif basis is None:
        app = oee._synthetic_app(receipts[acceptance.POSITIVE_APPLICABILITY])
        basis = oee._synthetic_basis(subject, actor, app)
    out = oee._admit_opportunity_noncurrent_for_test(
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
    return receipts, subject, actor, av, out


def chain():
    receipts, subject, actor, av, op = opportunity()
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
    return receipts, subject, actor, av, op, en


def readdress_receipt(receipt: acceptance.AcceptanceReceipt) -> acceptance.AcceptanceReceipt:
    pending = replace(receipt, receipt_id="PENDING", receipt_hash="0" * 64)
    h = acceptance._digest("RECEIPT", acceptance._receipt_body(pending))
    return replace(pending, receipt_id="urn:rawlsing:gt34:obl056:acceptance-receipt:sha256:" + h, receipt_hash=h)


def readdress_record(record: oee.V3OEERealizationRecord, **changes) -> oee.V3OEERealizationRecord:
    x = replace(record, **changes)
    candidate_hash = w2._digest(w2._CANDIDATE_DOMAIN, w2._candidate_material(x))
    x = replace(
        x,
        source_candidate_id="urn:rawlsing:v3:oee:candidate:sha256:" + candidate_hash,
        source_candidate_replay_hash=candidate_hash,
    )
    record_hash = w2._digest(w2._RECORD_DOMAIN, w2._record_identity(x))
    event_id = None
    if x.event_effect_kind is not None:
        event_hash = w2._digest(w2._EVENT_DOMAIN, {"record_hash": record_hash, "effect": x.event_effect_kind})
        event_id = "urn:rawlsing:v3:oee:event:sha256:" + event_hash
    return replace(
        x,
        record_id="urn:rawlsing:v3:oee:record:sha256:" + record_hash,
        record_hash=record_hash,
        event_id=event_id,
    )


def test_01_frozen_w2_and_hq_obl056_exact_inputs_are_preserved():
    assert git_blob("rawlsing_next/v3_adp010_oee_executor_authenticated.py") == EXPECTED_W2_BLOB
    assert oee.FROZEN_W2_EXECUTOR_BLOB == EXPECTED_W2_BLOB
    assert oee.HQ_OBL056_AUTHORITY_HASH == acceptance.ACCEPTANCE_AUTHORITY_CONTENT_HASH
    assert oee.HQ_OBL056_EMPTY_REGISTRY_HASH == acceptance.REGISTRY_CONTENT_HASH
    assert acceptance.candidate_registry_artifact()["current_positive_entries"] == []
    assert acceptance.candidate_registry_artifact()["positive_fallback"] is False


def test_02_noncurrent_mechanical_chain_passes_with_four_separately_issued_role_receipts():
    receipts, subject, actor, av, op, en = chain()
    out = oee.validate_basis_available_opportunity_encounter_chain((av.record, op.record, en.record))
    assert out == (av.record, op.record, en.record)
    assert [x.realization_state for x in out] == [oee.STATE_AVAILABLE, oee.STATE_OPPORTUNITY, oee.STATE_ENCOUNTER]
    assert len({receipts[x].receipt_id for x in acceptance.SUPPORTED_ROLES}) == 4
    assert receipts[acceptance.CONTACT_OCCURRENCE_WITNESS].accepted_authority_ref != receipts[acceptance.CONTACT_WITNESS_INDEPENDENCE].accepted_authority_ref


def test_03_self_issued_w2_authority_acceptance_formula_is_not_sufficient_anymore():
    receipts, subject, actor, _, _ = fixtures()
    original = receipts[acceptance.CAUSAL_USE_PERMISSION]
    p = subject.causal_use_permission
    arbitrary = acceptance.ContentAddressedRef(p.authority_id + "_CALLER", p.authority_version, sha256(b"caller").hexdigest())
    forged = readdress_receipt(replace(original, accepted_authority_ref=arbitrary))
    caller_subject = w2._synthetic_subject("caller-self-issued")
    cp = caller_subject.causal_use_permission
    cp0 = replace(
        cp,
        authority_id=arbitrary.id,
        authority_version=arbitrary.version,
        authority_content_hash=arbitrary.content_hash,
        authority_acceptance_ref=w2._authority_acceptance_ref(
            "ACCEPTED_CAUSAL_USE_AUTHORITY_RECEIPT", arbitrary.id, arbitrary.version, arbitrary.content_hash, w2.NONCURRENT_SYNTHETIC_TEST_ONLY
        ),
        authentication_ref=w2._fixture_ref("PLACEHOLDER", "caller-self-issued-auth"),
    )
    cp1 = replace(cp0, authentication_ref=w2._content_ref(
        "CAUSAL_USE_PERMISSION_AUTHENTICATION",
        "urn:rawlsing:causal-use-authentication:sha256:",
        w2._permission_material(cp0),
    ))
    cs0 = replace(caller_subject, causal_use_permission=cp1, authentication_ref=w2._fixture_ref("PLACEHOLDER", "caller-subject-auth"))
    caller_subject = replace(cs0, authentication_ref=w2._content_ref(
        "SUBJECT_INGRESS_AUTHENTICATION",
        "urn:rawlsing:subject-ingress-authentication:sha256:",
        w2._subject_material(cs0),
    ))
    with pytest.raises(oee.OBL055AcceptanceError, match="no exact positive registry entry"):
        oee._admit_available_noncurrent_for_test(
            causal_use_acceptance_receipt=forged,
            subject=caller_subject,
            actor=actor,
            effective_from="2031-01-01T00:00:00Z",
            effective_until="2031-01-02T00:00:00Z",
            time_granularity="INTERVAL",
            context_or_world_receipt_refs=(r("WORLD_RECEIPT", "caller-world"),),
            prior_ledger_anchor_ref=r("LEDGER_ANCHOR", "caller-l0"),
            provenance_refs=(r("PROVENANCE", "caller"),),
        )


def test_04_synthetic_acceptance_cannot_masquerade_as_current():
    receipt = oee.synthetic_acceptance_receipts()[acceptance.CAUSAL_USE_PERMISSION]
    with pytest.raises(acceptance.AcceptanceAuthorityError):
        acceptance.validate_acceptance_receipt(
            receipt,
            expected_role=acceptance.CAUSAL_USE_PERMISSION,
            expected_accepted_authority_ref=receipt.accepted_authority_ref,
            expected_owner_jurisdiction_ref=receipt.accepted_authority_owner_jurisdiction_ref,
            expected_source_acceptance_evidence_ref=receipt.source_acceptance_evidence_ref,
            expected_scope=receipt.scope,
            required_currentness=acceptance.CURRENT_ACCEPTED,
        )


def test_05_role_reuse_causal_as_applicability_fails_closed():
    receipts, subject, actor, _, basis = fixtures()
    _, _, _, av = available(receipts, subject, actor)
    with pytest.raises(oee.OBL055AcceptanceError):
        oee._admit_opportunity_noncurrent_for_test(
            causal_use_acceptance_receipt=receipts[acceptance.CAUSAL_USE_PERMISSION],
            applicability_acceptance_receipts=(receipts[acceptance.CAUSAL_USE_PERMISSION],),
            parent_available=av.record,
            subject=subject,
            actor=actor,
            opportunity_basis=basis,
            effective_from="2031-01-01T08:00:00Z",
            effective_until="2031-01-01T18:00:00Z",
            time_granularity="INTERVAL",
            prior_ledger_anchor_ref=r("LEDGER_ANCHOR", "role-l1"),
            provenance_refs=(r("PROVENANCE", "role"),),
        )


def test_06_contact_occurrence_and_independence_receipts_and_authorities_are_distinct():
    receipts, subject, actor, av, op = opportunity()
    occurrence = receipts[acceptance.CONTACT_OCCURRENCE_WITNESS]
    independence = receipts[acceptance.CONTACT_WITNESS_INDEPENDENCE]
    assert occurrence.receipt_id != independence.receipt_id
    assert occurrence.accepted_authority_ref != independence.accepted_authority_ref
    acceptance.validate_contact_acceptance_pair(occurrence, independence)
    witness = oee._synthetic_contact(subject, actor, occurrence, independence)
    with pytest.raises(oee.OBL055AcceptanceError):
        oee._admit_encounter_noncurrent_for_test(
            causal_use_acceptance_receipt=receipts[acceptance.CAUSAL_USE_PERMISSION],
            applicability_acceptance_receipts=(receipts[acceptance.POSITIVE_APPLICABILITY],),
            contact_occurrence_acceptance_receipt=occurrence,
            contact_independence_acceptance_receipt=occurrence,
            parent_opportunity=op.record,
            subject=subject,
            actor=actor,
            contact_witness=witness,
            effective_time="2031-01-01T12:00:00Z",
            time_granularity="INSTANT",
            prior_ledger_anchor_ref=r("LEDGER_ANCHOR", "pair-l2"),
            declared_precondition_refs=(r("DECLARED_PRECONDITION", "pair-pre"),),
            provenance_refs=(r("PROVENANCE", "pair"),),
        )


@pytest.mark.parametrize("bad_kind", ["COLOCATION", "COPRESENCE", "SAME_GEOGRAPHY_TIME", "SHARED_V555_ENDPOINT"])
def test_07_caller_relabeling_cannot_launder_proximity_into_contact_authority(bad_kind):
    receipts, subject, actor, av, op = opportunity()
    witness = oee._synthetic_contact(
        subject,
        actor,
        receipts[acceptance.CONTACT_OCCURRENCE_WITNESS],
        receipts[acceptance.CONTACT_WITNESS_INDEPENDENCE],
        contact_basis=(r(bad_kind, "proximity-" + bad_kind),),
    )
    with pytest.raises(oee.OEEAdmissionError, match="laundered"):
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
            prior_ledger_anchor_ref=r("LEDGER_ANCHOR", "launder-l2-" + bad_kind),
            declared_precondition_refs=(r("DECLARED_PRECONDITION", "launder-pre-" + bad_kind),),
            provenance_refs=(r("PROVENANCE", "launder-" + bad_kind),),
        )


def test_08_validate_record_reconstructs_receipts_and_rejects_readdressed_manifest_loss():
    _, _, _, av, op, en = chain()
    keep = tuple(x for x in en.record.provenance_refs if x.kind != "OBL056_ACCEPTANCE_BINDING_CONTACT_WITNESS_INDEPENDENCE")
    forged = readdress_record(en.record, provenance_refs=keep)
    w2.validate_record(forged)  # base W2 hashes alone are internally coherent
    with pytest.raises(oee.OEEIntegrityError, match="occurrence and one independence"):
        oee.validate_record(forged)


def test_09_validate_record_reconstructs_exact_adp008_phase_identity():
    _, _, _, av = available()
    phase_ref = next(x for x in av.record.provenance_refs if x.kind == "OBL055_ADP008_PHASE_REPLAY_BINDING")
    body = oee._decode_manifest(phase_ref, phase_ref.kind)
    body["phase_authority"][0] = "CALLER_RELABELLED_PHASE_AUTHORITY"
    changed = oee._manifest(phase_ref.kind, body)
    provenance = tuple(sorted(changed if x == phase_ref else x for x in av.record.provenance_refs))
    forged = readdress_record(av.record, provenance_refs=provenance)
    w2.validate_record(forged)
    with pytest.raises(oee.OEEIntegrityError, match="phase replay authority"):
        oee.validate_record(forged)


def test_10_source_candidate_id_commits_exact_obl056_receipt_binding_grain():
    receipts, subject, actor, av, op = opportunity()
    assert oee.validate_record(op.record) == op.record
    assert any(x.kind == "OBL056_ACCEPTANCE_RULE_HASH" for x in op.record.provenance_refs)
    assert any(x.kind == "OBL056_ACCEPTANCE_AUTHORITY_HASH" for x in op.record.provenance_refs)
    assert any(x.kind == "OBL056_ACCEPTANCE_REGISTRY_HASH" for x in op.record.provenance_refs)
    assert op.record.source_candidate_id == "urn:rawlsing:v3:oee:candidate:sha256:" + op.record.source_candidate_replay_hash


def test_11_phase_identity_and_receipt_binding_each_change_candidate_identity():
    receipts, subject, actor, _, basis = fixtures()
    _, _, _, left = available(receipts, subject, actor)
    actor2 = oee._synthetic_actor(phase_tag="other-phase")
    actor2 = replace(actor2, actor_id=actor.actor_id)
    actor2 = replace(actor2, authentication_ref=w2._content_ref(
        "ADP008_PHASE_STATE_AUTHENTICATION",
        "urn:rawlsing:adp008-phase-authentication:sha256:",
        w2._phase_material(actor2),
    ))
    _, _, _, right = available(receipts, subject, actor2)
    assert left.record.source_candidate_id != right.record.source_candidate_id


def test_12_historical_w2_t3_surface_remains_separate_and_no_new_positive_v3_authority_exists():
    manifest = oee.authority_identity_manifest()
    assert manifest["OBL056"]["installed_current_positive_entry_count"] == 0
    assert manifest["OBL056"]["positive_fallback"] is False
    assert not hasattr(oee, "admit_exposure")
    assert not hasattr(oee, "mutate_actor")
    assert oee.validate_basis_available_opportunity_encounter_chain(tuple(x.record for x in chain()[3:]))
