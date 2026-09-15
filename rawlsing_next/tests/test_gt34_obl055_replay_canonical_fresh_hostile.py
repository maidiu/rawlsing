from __future__ import annotations

from dataclasses import asdict, replace
from hashlib import sha256
import json

import pytest

import rawlsing_next.gt34_adp010_input_authority_acceptance as acceptance
import rawlsing_next.v3_adp010_oee_executor_obl055_acceptance_bound as r1
import rawlsing_next.v3_adp010_oee_executor_obl055_replay_reconstructed as r2
import rawlsing_next.v3_adp010_oee_executor_obl055_replay_canonical as oee


FROZEN_TARGET_SEMANTIC_CANDIDATE = "702eababa4012512743fd2e729fc9bea167089b1"
FROZEN_TARGET_IMPLEMENTATION_BLOB = "e8c6edab3b310b797997a3826b8acb32f7f08ce9"
FROZEN_ATTACK_MATRIX = "6be26a0ad812b03461c515b9da005b0ba7a89010"


def ref(kind: str, tag: str) -> oee.ExactRef:
    h = sha256(tag.encode("utf-8")).hexdigest()
    return oee.ExactRef(kind, f"urn:obl055:h2:{tag}", h)


def fixtures():
    receipts = oee.synthetic_acceptance_receipts()
    subject = oee._synthetic_subject(receipts[acceptance.CAUSAL_USE_PERMISSION])
    actor = oee._synthetic_actor()
    app = oee._synthetic_app(receipts[acceptance.POSITIVE_APPLICABILITY])
    basis = oee._synthetic_basis(subject, actor, app)
    return receipts, subject, actor, app, basis


def available():
    receipts, subject, actor, app, basis = fixtures()
    result = oee._admit_available_noncurrent_for_test(
        causal_use_acceptance_receipt=receipts[acceptance.CAUSAL_USE_PERMISSION],
        subject=subject,
        actor=actor,
        effective_from="2031-01-01T00:00:00Z",
        effective_until="2031-01-02T00:00:00Z",
        time_granularity="INTERVAL",
        context_or_world_receipt_refs=(ref("WORLD_RECEIPT", "world"), ref("CONTEXT_RECEIPT", "context")),
        prior_ledger_anchor_ref=ref("LEDGER_ANCHOR", "l0"),
        provenance_refs=(ref("PROVENANCE", "available"),),
    )
    return receipts, subject, actor, app, basis, result


def opportunity():
    receipts, subject, actor, app, basis, av = available()
    result = oee._admit_opportunity_noncurrent_for_test(
        causal_use_acceptance_receipt=receipts[acceptance.CAUSAL_USE_PERMISSION],
        applicability_acceptance_receipts=(receipts[acceptance.POSITIVE_APPLICABILITY],),
        parent_available=av.record,
        subject=subject,
        actor=actor,
        opportunity_basis=basis,
        effective_from="2031-01-01T08:00:00Z",
        effective_until="2031-01-01T18:00:00Z",
        time_granularity="INTERVAL",
        prior_ledger_anchor_ref=ref("LEDGER_ANCHOR", "l1"),
        provenance_refs=(ref("PROVENANCE", "opportunity"),),
    )
    return receipts, subject, actor, app, basis, av, result


def encounter():
    receipts, subject, actor, app, basis, av, op = opportunity()
    witness = oee._synthetic_contact(
        subject,
        actor,
        receipts[acceptance.CONTACT_OCCURRENCE_WITNESS],
        receipts[acceptance.CONTACT_WITNESS_INDEPENDENCE],
    )
    result = oee._admit_encounter_noncurrent_for_test(
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
        prior_ledger_anchor_ref=ref("LEDGER_ANCHOR", "l2"),
        declared_precondition_refs=(ref("DECLARED_PRECONDITION", "pre"),),
        provenance_refs=(ref("PROVENANCE", "encounter"),),
    )
    return receipts, subject, actor, app, basis, witness, av, op, result


def replace_bundle(record, mutate):
    kind = oee._BUNDLE_KIND[record.realization_state]
    old = next(x for x in record.provenance_refs if x.kind == kind)
    body = r2._decode_bundle(old, record.realization_state)
    mutate(body)
    new = r2._bundle_ref(record.realization_state, body)
    return r2._readdress(record, (new if x == old else x for x in record.provenance_refs))


def replace_causal_binding(record, mutate):
    kind = "OBL056_ACCEPTANCE_BINDING_" + acceptance.CAUSAL_USE_PERMISSION
    old = next(x for x in record.provenance_refs if x.kind == kind)
    body = r1._decode_manifest(old, kind)
    mutate(body)
    new = r1._manifest(kind, body)

    subject_kind = "OBL055_SUBJECT_INGRESS_REPLAY_BINDING"
    subject_old = next(x for x in record.provenance_refs if x.kind == subject_kind)
    subject_body = r1._decode_manifest(subject_old, subject_kind)
    subject_body["causal_acceptance_binding_ref"] = r1._ref_dict(new)
    subject_new = r1._manifest(subject_kind, subject_body)

    provenance = tuple(
        new if x == old else subject_new if x == subject_old else x
        for x in record.provenance_refs
    )
    return r2._readdress(record, provenance)


def test_h2_01_frozen_target_and_freshness_pins():
    assert FROZEN_TARGET_SEMANTIC_CANDIDATE == "702eababa4012512743fd2e729fc9bea167089b1"
    assert FROZEN_TARGET_IMPLEMENTATION_BLOB == oee.FROZEN_R2_REPAIR_BLOB.replace(
        oee.FROZEN_R2_REPAIR_BLOB, FROZEN_TARGET_IMPLEMENTATION_BLOB
    )
    assert FROZEN_ATTACK_MATRIX == "6be26a0ad812b03461c515b9da005b0ba7a89010"


def test_h2_02_lawful_chain_survives_json_tuple_array_roundtrip():
    *_, av, op, en = encounter()
    assert oee.validate_basis_available_opportunity_encounter_chain((av.record, op.record, en.record)) == (
        av.record,
        op.record,
        en.record,
    )


def test_h2_03_canonical_wire_equality_is_exact_not_permissive():
    receipt = oee.synthetic_acceptance_receipts()[acceptance.CAUSAL_USE_PERMISSION]
    wire = json.loads(r2._canonical(asdict(receipt)))
    assert oee._receipt_wire_equal(wire, receipt)

    attacks = []
    extra = dict(wire)
    extra["caller_added_semantics"] = True
    attacks.append(extra)
    missing = dict(wire)
    missing.pop("receipt_hash")
    attacks.append(missing)
    role = dict(wire)
    role["role"] = acceptance.POSITIVE_APPLICABILITY
    attacks.append(role)
    scope = json.loads(json.dumps(wire))
    scope["scope"]["transition_use_scope"] = "CALLER_RELABELED_TRANSITION"
    attacks.append(scope)
    subject_scope = json.loads(json.dumps(wire))
    subject_scope["scope"]["subject_scope"] = ["caller-subject"]
    attacks.append(subject_scope)

    for attacked in attacks:
        assert not oee._receipt_wire_equal(attacked, receipt)


def test_h2_04_source_bundle_only_receipt_mutation_fails_after_full_readdress():
    *_, av = available()
    forged = replace_bundle(
        av.record,
        lambda body: body["causal_use_acceptance_receipt"].__setitem__(
            "role", acceptance.POSITIVE_APPLICABILITY
        ),
    )
    with pytest.raises((oee.OBL055AcceptanceError, oee.OEEIntegrityError)):
        oee.validate_record(forged)


def test_h2_05_base_binding_only_extra_semantic_key_fails_after_full_readdress():
    *_, av = available()
    forged = replace_causal_binding(
        av.record,
        lambda body: body["receipt"].__setitem__("caller_added_semantics", True),
    )
    with pytest.raises(oee.OEEIntegrityError):
        oee.validate_record(forged)


def test_h2_06_synchronized_extra_key_across_bundle_and_binding_still_fails():
    *_, av = available()
    first = replace_bundle(
        av.record,
        lambda body: body["causal_use_acceptance_receipt"].__setitem__("caller_added_semantics", True),
    )
    forged = replace_causal_binding(
        first,
        lambda body: body["receipt"].__setitem__("caller_added_semantics", True),
    )
    with pytest.raises(oee.OEEIntegrityError):
        oee.validate_record(forged)


@pytest.mark.parametrize("successor_ref", [oee.R3_SUCCESSOR_REF, oee.R2_SUCCESSOR_REF])
def test_h2_07_successor_provenance_removal_fails_even_after_readdress(successor_ref):
    *_, av = available()
    forged = r2._readdress(av.record, (x for x in av.record.provenance_refs if x != successor_ref))
    with pytest.raises(oee.OEEIntegrityError, match="successor provenance"):
        oee.validate_record(forged)


@pytest.mark.parametrize(
    "fixed_ref",
    [
        r1.OBL056_ACCEPTANCE_AUTHORITY_HASH_REF,
        r1.OBL056_ACCEPTANCE_REGISTRY_HASH_REF,
        r1.OBL056_ACCEPTANCE_RULE_HASH_REF,
        r1.OBL056_HQ_ADOPTION_PROVENANCE_REF,
    ],
)
def test_h2_08_hq_obl056_fixed_provenance_removal_fails(fixed_ref):
    *_, av = available()
    forged = r2._readdress(av.record, (x for x in av.record.provenance_refs if x != fixed_ref))
    with pytest.raises(oee.OEEIntegrityError):
        oee.validate_record(forged)


def test_h2_09_source_candidate_id_mismatch_fails_without_mutating_semantics():
    *_, av = available()
    forged = replace(av.record, source_candidate_id="urn:rawlsing:v3:oee:candidate:sha256:" + "0" * 64)
    with pytest.raises(oee.OEEIntegrityError):
        oee.validate_record(forged)


def test_h2_10_zero_positive_registry_blocks_current_path():
    receipts, subject, actor, *_ = fixtures()
    assert acceptance.candidate_registry_artifact()["current_positive_entries"] == []
    assert acceptance.candidate_registry_artifact()["positive_fallback"] is False
    with pytest.raises((oee.OBL055AcceptanceError, oee.OEEIntegrityError, oee.OEEAdmissionError)):
        oee.admit_available(
            causal_use_acceptance_receipt=receipts[acceptance.CAUSAL_USE_PERMISSION],
            subject=subject,
            actor=actor,
            effective_from="2031-01-01T00:00:00Z",
            effective_until="2031-01-02T00:00:00Z",
            time_granularity="INTERVAL",
            context_or_world_receipt_refs=(ref("WORLD_RECEIPT", "world-current"),),
            prior_ledger_anchor_ref=ref("LEDGER_ANCHOR", "l0-current"),
            provenance_refs=(ref("PROVENANCE", "current-attempt"),),
        )


def test_h2_11_contact_roles_remain_distinct_and_no_capability_widening():
    receipts = oee.synthetic_acceptance_receipts()
    occurrence = receipts[acceptance.CONTACT_OCCURRENCE_WITNESS]
    independence = receipts[acceptance.CONTACT_WITNESS_INDEPENDENCE]
    assert occurrence.receipt_id != independence.receipt_id
    assert occurrence.accepted_authority_ref != independence.accepted_authority_ref
    acceptance.validate_contact_acceptance_pair(occurrence, independence)

    for name in (
        "issue_current_acceptance",
        "admit_exposure",
        "create_comparator",
        "create_psepf",
        "mutate_actor",
        "metabolize",
        "can_008",
    ):
        assert not hasattr(oee, name)


def test_h2_12_readdressed_contact_chain_keeps_exact_w2_transition_ceiling():
    *_, av, op, en = encounter()
    assert [x.record.realization_state for x in (av, op, en)] == [
        oee.STATE_AVAILABLE,
        oee.STATE_OPPORTUNITY,
        oee.STATE_ENCOUNTER,
    ]
    assert all(oee.R3_SUCCESSOR_REF in x.record.provenance_refs for x in (av, op, en))