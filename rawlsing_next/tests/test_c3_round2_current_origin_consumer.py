"""C-3 round 2: sourcefree exact current-object first-reader evidence.

Never original35 physical-source, science, actor or N9 proof. Direct D remains
a legacy sourcefree path; this tests the selected *current R1C harness*.
"""
from __future__ import annotations

from dataclasses import replace
import pytest

from rawlsing_next import field_forge_conditional_support as ff
from rawlsing_next import gt12_c_to_d_relation_bridge as bridge
from rawlsing_next import wave1_ff_prev3_relation_admission as adm
from rawlsing_next import pre553_repo_native_current_payload as payload
from rawlsing_next.tests import gt12_e2b_actual_object_consumer_harness as harness
from rawlsing_next.tests.test_gt12_e2b_actual_object_consumer_harness import _objects


def _current():
    query, fact = payload.load_current_gt2_query_fact_from_committed_transport()
    relation = ff.produce_exact_conditional_support_profile(
        joint_fact=fact, joint_query=query,
        conditioner_ref=query.target_refs[0], target_ref=query.target_refs[1],
        producer_permission_ceiling=(adm.GT2_TARGET_USE,),
        relation_permission_ceiling=(adm.GT2_TARGET_USE,),
    )
    return query, fact, relation


def test_verified_current_objects_no_duplicate_transport_load(monkeypatch):
    q, f, r = _current()
    def deny_double_load():
        raise AssertionError("unexpected duplicate frozen closure rehydration")
    monkeypatch.setattr(payload, "load_current_gt2_query_fact_from_committed_transport",
                        deny_double_load)
    unverified = bridge.admit_gt12_c_relation(r)
    bound = bridge.admit_gt12_c_relation_from_verified_current_objects(
        r, joint_query=q, joint_fact=f,
    )
    assert unverified.sourcefree_origin_path == "DECLARED_SOURCE_CONTRADICTION_ONLY__ORIGIN_UNVERIFIED"
    assert bound.sourcefree_origin_path == "EXACT_PINNED_R1C_TRANSPORT_CONTENT__SOURCEFREE_ONLY"
    # Source qualification is a diagnostic on this API result, not a new
    # independently competent D rule, and not a physical native source grant.
    assert unverified.admission.ref == bound.admission.ref
    assert bound.admission.decision is adm.AdmissionDecision.ADMITTED


def test_same_permission_synthetic_cannot_be_passed_off_as_current():
    q, f, c, t = _objects()
    r = ff.produce_exact_conditional_support_profile(
        joint_fact=f, joint_query=q, conditioner_ref=c, target_ref=t,
        producer_permission_ceiling=(adm.GT2_TARGET_USE,),
        relation_permission_ceiling=(adm.GT2_TARGET_USE,),
    )
    assert bridge.admit_gt12_c_relation(r).admission.decision is adm.AdmissionDecision.ADMITTED
    with pytest.raises(bridge.GT12CToDBridgeError, match="not the exact fixed current"):
        bridge.admit_gt12_c_relation_from_verified_current_objects(
            r, joint_query=q, joint_fact=f,
        )


def test_selected_current_first_consumer_calls_bound_admission(monkeypatch):
    q, f, _ = _current()
    observed = []
    real = bridge.admit_gt12_c_relation_from_verified_current_objects
    def witness(relation, *, joint_query, joint_fact):
        observed.append((relation.ref, joint_query.ref, joint_fact.ref))
        return real(relation, joint_query=joint_query, joint_fact=joint_fact)
    monkeypatch.setattr(bridge, "admit_gt12_c_relation_from_verified_current_objects", witness)
    out = harness.run_current_r1c_e2b_actual_objects(q, f)
    assert observed == [(out.relation.ref, q.ref, f.ref)]
    assert out.admission.decision is adm.AdmissionDecision.ADMITTED


def test_wrong_query_or_fact_rejected_and_restoration():
    q, f, r = _current()
    other_q, other_f, _, _ = _objects()
    for cq, cf in ((other_q, f), (q, other_f)):
        with pytest.raises(bridge.GT12CToDBridgeError):
            bridge.admit_gt12_c_relation_from_verified_current_objects(
                r, joint_query=cq, joint_fact=cf,
            )
    assert bridge.admit_gt12_c_relation_from_verified_current_objects(
        r, joint_query=q, joint_fact=f,
    ).admission.decision is adm.AdmissionDecision.ADMITTED


def test_re_signed_mismatched_relation_cannot_bypass_exact_current_reconstruction():
    q, f, r = _current()
    projection = r.semantic_projection()
    # A new internally coherent relation with extra declared provenance is
    # *not* an attested product of the pinned fact, despite a valid new hash.
    from rawlsing_next.pre553_empirical_objects import ExactRef, semantic_hash
    injected = ExactRef("SOURCE_ARTIFACT", adm.GT2_SOURCE_PATH, adm.GT2_SOURCE_SHA256)
    if injected in r.producer_provenance_refs:
        pytest.skip("the retained fact unexpectedly carries direct SOURCE_ARTIFACT")
    refs = (*r.producer_provenance_refs, injected)
    projection["producer_provenance_refs"] = [ref.as_dict() for ref in refs]
    digest = semantic_hash(projection)
    forged = replace(
        r,
        producer_provenance_refs=refs,
        content_hash=digest,
        object_id=f"urn:rawlsing:field-forge:conditional-support:sha256:{digest}",
    )
    assert bridge.admit_gt12_c_relation(forged).admission.decision is adm.AdmissionDecision.ADMITTED
    with pytest.raises(bridge.GT12CToDBridgeError, match="relation differs from"):
        bridge.admit_gt12_c_relation_from_verified_current_objects(
            forged, joint_query=q, joint_fact=f,
        )
    assert bridge.admit_gt12_c_relation_from_verified_current_objects(
        r, joint_query=q, joint_fact=f,
    ).admission.decision is adm.AdmissionDecision.ADMITTED
