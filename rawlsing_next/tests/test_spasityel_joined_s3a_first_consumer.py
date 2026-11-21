"""PYAT-SPASITYEL R27: one selected S3-A → GT12-D first consumer, sourcefree only.

Do not interpret a self-re-signed fixture as source/authentic respondent evidence.
Exercises the combined current-owner 067 + 086 + 081 safeguards as one path.
No standalone subsystem, original survey grant, or population inference.
"""
from __future__ import annotations

from dataclasses import replace

import pytest

from rawlsing_next import field_forge_conditional_support as ff
from rawlsing_next import gt12_c_to_d_relation_bridge as d
from rawlsing_next import wave1_ff_prev3_relation_admission as adm
from rawlsing_next.pre553_empirical_objects import ExactRef, semantic_hash
from rawlsing_next.tests.test_gt12_e2b_actual_object_consumer_harness import _objects
from rawlsing_next.tests.test_s3a_r5_denominator_membership_closure import (
    _compact_supported, _respondent,
)
from rawlsing_next.tests.test_field_forge_conditional_support import _fixture
from rawlsing_next.wave1_r5_q86_c11_projection import question_ref


def _rel(query, fact, c, t):
    return ff.produce_exact_conditional_support_profile(
        joint_fact=fact,
        joint_query=query,
        conditioner_ref=c,
        target_ref=t,
        producer_permission_ceiling=(adm.GT2_TARGET_USE,),
        relation_permission_ceiling=(adm.GT2_TARGET_USE,),
    )


def test_067_conditional_membership_and_086_question_identity_reach_same_081_d():
    q, fact, c, t = _objects()
    r1, r2, r3, r4, outsider = (_respondent(n) for n in range(5))
    genuine = _compact_supported(
        fact, risk_members=(r1, r2, r3, r4),
        denominator_members=(r1, r2, r3),
    )
    positive = _rel(q, genuine, c, t)
    outcome = d.admit_gt12_c_relation(positive)
    assert outcome.admission.decision is adm.AdmissionDecision.ADMITTED
    assert outcome.evidence.relation_ref == positive.ref
    assert outcome.evidence.relation_owner == ff.SEMANTIC_OWNER
    assert outcome.sourcefree_origin_path.endswith("ORIGIN_UNVERIFIED")
    assert set(outcome.admission.target_use_permissions) <= set(
        positive.relation_permission_ceiling
    )

    # An internally re-signed but false member cannot be accepted by FF01
    # and therefore cannot reach D as a positive.
    wrong_population = _compact_supported(
        fact, risk_members=(r1, r2, r3, r4),
        denominator_members=(r1, r2, outsider),
    )
    assert wrong_population.ref != fact.ref
    with pytest.raises(
        ff.FieldForgeConditionalSupportError,
        match="denominator member outside risk set",
    ):
        _rel(q, wrong_population, c, t)

    # The same combined FF01 must not accept a lookalike Q86B implementation.
    spoof_q86b = ExactRef(
        "QUESTION_IMPLEMENTATION",
        question_ref("Q86B").object_id,
        semantic_hash({"forged": "q86b-implementation"}),
    )
    wrong_q, wrong_f, wrong_c, wrong_t = _fixture(
        conditioner_ref=spoof_q86b, target_ref=question_ref("Q86A")
    )
    with pytest.raises(
        ff.FieldForgeConditionalSupportError,
        match="exact Q86B/Q86A QUESTION_IMPLEMENTATION",
    ):
        _rel(wrong_q, wrong_f, wrong_c, wrong_t)

    # These disqualifying cases did not poison the original admissible path.
    restored = d.admit_gt12_c_relation(_rel(q, genuine, c, t))
    assert restored.admission.ref == outcome.admission.ref


def test_081_d_rejects_self_signed_alien_source_after_valid_067_086_profile():
    q, fact, c, t = _objects()
    valid = _rel(q, fact, c, t)
    accepted = d.admit_gt12_c_relation(valid)
    assert accepted.admission.decision is adm.AdmissionDecision.ADMITTED

    # Forge a distinct SOURCE_ARTIFACT that is self-consistently hashed.
    # This is a hostile SOURCEFREE profile, not the actual original source.
    altered = replace(valid)
    old_sources = tuple(
        ref for ref in altered.producer_provenance_refs if ref.kind == "SOURCE_ARTIFACT"
    )
    assert len(old_sources) == 1
    foreign = ExactRef(
        "SOURCE_ARTIFACT",
        "urn:spasityel:foreign-source",
        semantic_hash({"spasityel": "independent-foreign-source"}),
    )
    new_refs = tuple(
        foreign if ref == old_sources[0] else ref
        for ref in altered.producer_provenance_refs
    )
    object.__setattr__(altered, "producer_provenance_refs", new_refs)
    new_hash = semantic_hash(altered.semantic_projection())
    object.__setattr__(altered, "content_hash", new_hash)
    object.__setattr__(
        altered, "object_id",
        "urn:rawlsing:field-forge:conditional-support:sha256:" + new_hash,
    )
    assert altered.content_hash == semantic_hash(altered.semantic_projection())
    assert altered.ref != valid.ref

    with pytest.raises(
        d.GT12CToDBridgeError,
        match="declared producer source contradicts frozen GT12 physical source",
    ):
        d.admit_gt12_c_relation(altered)

    # The actual same-authority first consumer stays admissible and replayable.
    restored = d.admit_gt12_c_relation(valid)
    assert restored.admission.ref == accepted.admission.ref
    assert d.replay_gt12_c_to_d_admission(
        valid, accepted.admission
    ).ref == accepted.admission.ref
