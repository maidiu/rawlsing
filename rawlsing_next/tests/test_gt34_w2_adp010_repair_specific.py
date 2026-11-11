from dataclasses import replace
from hashlib import sha1

import pytest

import rawlsing_next.v3_adp010_oee_executor_authenticated as oee
from rawlsing_next.tests.test_gt34_w2_adp010_successor_compatibility import r, available, opportunity, chain


def git_blob_sha(raw: bytes) -> str:
    return sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()


def test_synthetic_fixture_is_explicitly_noncurrent_and_cannot_use_public_path():
    subject = oee._synthetic_subject()
    actor = oee._synthetic_actor()
    assert subject.currentness_state == oee.NONCURRENT_SYNTHETIC_TEST_ONLY
    assert actor.currentness_state == oee.NONCURRENT_SYNTHETIC_TEST_ONLY
    with pytest.raises(oee.OEEAdmissionError, match="CURRENT_ACCEPTED"):
        oee.admit_available(
            subject=subject,
            actor=actor,
            effective_from="2031-01-01T00:00:00Z",
            effective_until="2031-01-02T00:00:00Z",
            time_granularity="INTERVAL",
            context_or_world_receipt_refs=(r("CONTEXT_RECEIPT", "public-reject"),),
            prior_ledger_anchor_ref=r("LEDGER_ANCHOR", "public-reject"),
            provenance_refs=(r("PROVENANCE", "public-reject"),),
        )


def test_historical_obl053_root_cannot_authenticate_current_subject_ingress():
    subject = oee._synthetic_subject()
    current_shaped = replace(
        subject,
        currentness_state=oee.CURRENT_ACCEPTED,
        obl054_adoption_artifact_blob=oee.OBL054_ADOPTION_ARTIFACT_BLOB,
        materialization_receipt=replace(
            subject.materialization_receipt,
            currentness_state=oee.CURRENT_ACCEPTED,
            materializer_id=oee.OBL054_MATERIALIZER_ID,
            materializer_version=oee.OBL054_MATERIALIZER_VERSION,
            adoption_artifact_blob=oee.HISTORICAL_INVALID_OBL053_ADOPTION_ARTIFACT_BLOB,
            accepted_owner_root_hash=oee.OBL054_ACCEPTED_ROOT_HASH,
            materialization_permit_id=oee.OBL054_PERMIT_ID,
            materialization_permit_hash=oee.OBL054_PERMIT_HASH,
        ),
    )
    with pytest.raises(oee.OEEAdmissionError, match="exact adopted OBL054"):
        oee._validate_subject(current_shaped, oee.CURRENT_ACCEPTED)


def test_wrong_obl054_adoption_blob_cannot_authenticate_current_ingress():
    subject = oee._synthetic_subject()
    current_shaped = replace(subject, currentness_state=oee.CURRENT_ACCEPTED)
    with pytest.raises(oee.OEEAdmissionError, match="OBL054 adoption"):
        oee._validate_subject(current_shaped, oee.CURRENT_ACCEPTED)


def test_materialization_receipt_wire_is_mechanically_recomputed_in_synthetic_court():
    receipt = oee._synthetic_materialization()
    assert oee._validate_materialization_receipt(
        receipt, oee.NONCURRENT_SYNTHETIC_TEST_ONLY
    ) == receipt
    tampered = replace(receipt, replay_input_hash="0" * 64)
    with pytest.raises(oee.OEEIntegrityError, match="replay_input_hash"):
        oee._validate_materialization_receipt(
            tampered, oee.NONCURRENT_SYNTHETIC_TEST_ONLY
        )


def test_causal_use_permission_is_bound_to_exact_materialization_receipt():
    subject = oee._synthetic_subject()
    wrong = replace(
        subject.causal_use_permission,
        materialization_receipt_ref=r("SUBJECT_MATERIALIZATION_RECEIPT", "wrong"),
    )
    tampered = replace(subject, causal_use_permission=wrong)
    with pytest.raises(oee.OEEAdmissionError, match="exact subject/object/materialization"):
        available(tampered, oee._synthetic_actor())


def test_phase_state_receipt_is_bound_into_replay():
    subject = oee._synthetic_subject()
    actor = oee._synthetic_actor()
    _, _, left = available(subject, actor)
    changed = replace(
        actor,
        phase_state_receipt_ref=r("V3DevelopmentalPhaseStateReceipt", "phase-receipt-changed"),
    )
    changed = replace(
        changed,
        authentication_ref=oee._content_ref(
            "ADP008_PHASE_STATE_AUTHENTICATION",
            "urn:rawlsing:adp008-phase-authentication:sha256:",
            oee._phase_material(changed),
        ),
    )
    _, _, right = available(subject, changed)
    assert left.record.source_candidate_replay_hash != right.record.source_candidate_replay_hash


def test_applicability_auth_ref_is_persisted_in_provenance():
    _, _, _, op = opportunity()
    kinds = {x.kind for x in op.record.provenance_refs}
    assert "POSITIVE_APPLICABILITY_AUTHENTICATION" in kinds


def test_contact_and_independence_auth_refs_are_persisted_in_provenance():
    _, _, _, _, en = chain()
    kinds = {x.kind for x in en.record.provenance_refs}
    assert "CONTACT_OCCURRENCE_AUTHENTICATION" in kinds
    assert "CONTACT_INDEPENDENCE_AUTHENTICATION" in kinds


def test_all_record_mutable_refs_are_committed_by_recomputed_candidate_hash():
    _, _, _, op = opportunity()
    original = op.record
    mutations = [
        replace(original, context_or_world_receipt_refs=(r("CONTEXT_RECEIPT", "mut1"),)),
        replace(original, applicability_receipt_refs=(r("POSITIVE_APPLICABILITY_RECEIPT", "mut2"),)),
        replace(original, phase_state_ref=r("V3DevelopmentalPhaseState", "mut3")),
        replace(original, position_or_other_constraint_refs=(r("CONSTRAINT_RECEIPT", "mut4"),)),
        replace(original, causal_witness_refs=(r("ACTOR_SPECIFIC_OPPORTUNITY_BASIS", "mut5"),)),
        replace(original, prior_ledger_anchor_ref=r("LEDGER_ANCHOR", "mut6")),
        replace(original, provenance_refs=tuple(sorted(original.provenance_refs + (r("PROVENANCE", "mut7"),)))),
    ]
    for tampered in mutations:
        with pytest.raises(oee.OEEIntegrityError):
            oee.validate_record(tampered)


def test_zero_draw_and_no_hidden_rng_surface():
    _, _, av, op, en = chain()
    assert all(x.record.rng_decision_receipt_ref is None for x in (av, op, en))
    assert not hasattr(oee, "random")
    assert not hasattr(oee, "rng")


def test_no_exposure_or_out_of_scope_authority_surfaces():
    forbidden = {
        "admit_exposure",
        "classify_subject",
        "create_subject",
        "run_comparator",
        "psepf",
        "metabolize",
        "can008",
        "render_v2",
    }
    assert forbidden.isdisjoint(set(dir(oee)))


def test_candidate_material_commits_event_effect_and_ledger_anchor():
    _, _, _, op = opportunity()
    base = op.record
    with pytest.raises(oee.OEEIntegrityError):
        oee.validate_record(replace(base, event_effect_kind="FORGED_EFFECT"))
    with pytest.raises(oee.OEEIntegrityError):
        oee.validate_record(replace(base, prior_ledger_anchor_ref=r("LEDGER_ANCHOR", "forged-anchor")))


def test_exact_fixed_provenance_contains_adp010_adp008_adp020():
    _, _, av = available()
    kinds = {x.kind for x in av.record.provenance_refs}
    assert {
        "ADP010_AUTHORITY_HASH",
        "ADP010_REGISTRY_HASH",
        "ADP010_RULE_HASH",
        "ADP008_AUTHORITY_HASH",
        "ADP008_REGISTRY_HASH",
        "ADP020_AUTHORITY_HASH",
    }.issubset(kinds)


def test_synthetic_contact_independence_proximity_laundering_rejected():
    subject, actor, av, op = opportunity()
    witness = oee._synthetic_contact(
        subject,
        actor,
        independence_basis=(r("SAME_GEOGRAPHY_TIME", "ind-launder"),),
    )
    with pytest.raises(oee.OEEAdmissionError, match="proximity"):
        oee._admit_encounter_noncurrent_for_test(
            parent_opportunity=op.record,
            subject=subject,
            actor=actor,
            contact_witness=witness,
            effective_time="2031-01-01T12:00:00Z",
            time_granularity="INSTANT",
            prior_ledger_anchor_ref=r("LEDGER_ANCHOR", "ind-launder"),
            declared_precondition_refs=(r("DECLARED_PRECONDITION", "ind-launder"),),
            provenance_refs=(r("PROVENANCE", "ind-launder"),),
        )


def test_historical_s3_module_and_test_blobs_remain_exact():
    from pathlib import Path
    module_raw = Path("rawlsing_next/v3_adp010_oee_executor.py").read_bytes()
    test_raw = Path("rawlsing_next/tests/test_v3_adp010_oee_executor.py").read_bytes()
    assert git_blob_sha(module_raw) == oee.HISTORICAL_S3_MODULE_BLOB_SHA
    assert git_blob_sha(test_raw) == oee.HISTORICAL_S3_TEST_BLOB_SHA
