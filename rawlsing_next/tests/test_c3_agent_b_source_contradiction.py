"""C-3 Agent B: source-contradiction attack on the actual GT12 C→D ABI.

All claims are SOURCEFREE. Re-signed semantic objects are adversarial inputs,
not original35 evidence, original survey access, or a trusted C11 issuer.
"""
from __future__ import annotations

from dataclasses import replace

import pytest

from rawlsing_next import field_forge_conditional_support as ff
from rawlsing_next import gt12_c_to_d_relation_bridge as bridge
from rawlsing_next import wave1_ff_prev3_relation_admission as adm
from rawlsing_next.pre553_empirical_objects import ExactRef, semantic_hash
from rawlsing_next.tests.test_gt12_closure_b_c_to_d_bridge import _fixture


def _resign_provenance(relation: ff.ExactConditionalSupportProfile, refs):
    """Preserve coherent hash+object identity while altering declared source."""
    refs = tuple(refs)
    projection = relation.semantic_projection()
    projection["producer_provenance_refs"] = [ref.as_dict() for ref in refs]
    digest = semantic_hash(projection)
    return replace(
        relation,
        producer_provenance_refs=refs,
        content_hash=digest,
        object_id=f"urn:rawlsing:field-forge:conditional-support:sha256:{digest}",
    )


def test_c3_t01_original_frozen_sourcefree_case_preserved():
    relation, fact = _fixture()
    assert relation.producer_fact_ref == fact.ref
    assert relation.producer_state_blocking is False
    receipt = bridge.admit_gt12_c_relation(relation)
    assert receipt.admission.decision is adm.AdmissionDecision.ADMITTED
    assert receipt.evidence.source_artifact_ref == ExactRef(
        "SOURCE_ARTIFACT", adm.GT2_SOURCE_PATH, adm.GT2_SOURCE_SHA256
    )


@pytest.mark.parametrize("mode", ["wrong_only", "two_sources"])
def test_c3_t01_self_consistent_wrong_source_ref_cannot_be_stamped(mode):
    relation, _ = _fixture()
    authentic = ExactRef("SOURCE_ARTIFACT", adm.GT2_SOURCE_PATH, adm.GT2_SOURCE_SHA256)
    wrong = ExactRef("SOURCE_ARTIFACT", adm.GT2_SOURCE_PATH, semantic_hash({"wrong_source": mode}))
    preserved = tuple(ref for ref in relation.producer_provenance_refs
                      if ref.kind != "SOURCE_ARTIFACT")
    source_refs = (wrong,) if mode == "wrong_only" else (authentic, wrong)
    attacked = _resign_provenance(relation, (*preserved, *source_refs))
    assert semantic_hash(attacked.semantic_projection()) == attacked.content_hash
    assert attacked.ref != relation.ref
    with pytest.raises(bridge.GT12CToDBridgeError,
                       match="declared producer source contradicts frozen"):
        bridge.admit_gt12_c_relation(attacked)
    # Restoration is an actual D positive, not merely hash recovery.
    assert bridge.admit_gt12_c_relation(relation).admission.decision is adm.AdmissionDecision.ADMITTED


def test_c3_t01_wrong_source_only_is_not_hidden_by_non_source_provenance():
    relation, _ = _fixture()
    wrong = ExactRef("SOURCE_ARTIFACT", "Data/not-the-frozen-survey.sav",
                     semantic_hash({"wrong_origin": "different_path"}))
    attacked = _resign_provenance(
        relation,
        (*tuple(ref for ref in relation.producer_provenance_refs
                if ref.kind != "SOURCE_ARTIFACT"), wrong),
    )
    with pytest.raises(bridge.GT12CToDBridgeError,
                       match="declared producer source contradicts frozen"):
        bridge.bridge_gt12_c_relation_to_d_evidence(attacked)


@pytest.mark.xfail(strict=True, reason=(
    "OPEN: direct GT12 C→D cannot authenticate an absent SOURCE_ARTIFACT ref; "
    "the genuine retained C11 fact has a release/event closure, not a simple source ref"
))
def test_c3_t01_missing_declared_source_requires_trusted_release_origin():
    relation, _ = _fixture()
    absent = _resign_provenance(
        relation,
        tuple(ref for ref in relation.producer_provenance_refs
              if ref.kind != "SOURCE_ARTIFACT"),
    )
    with pytest.raises(bridge.GT12CToDBridgeError):
        bridge.admit_gt12_c_relation(absent)


def test_c3_t01_genuine_retained_current_transport_still_admits_sourcefree():
    # Fixed immutable transport, not external original SAV input.
    from rawlsing_next.pre553_repo_native_current_payload import (
        load_current_gt2_query_fact_from_committed_transport,
    )

    query, fact = load_current_gt2_query_fact_from_committed_transport()
    relation = ff.produce_exact_conditional_support_profile(
        joint_fact=fact, joint_query=query,
        conditioner_ref=query.target_refs[0],
        target_ref=query.target_refs[1],
        producer_permission_ceiling=(adm.GT2_TARGET_USE,),
        relation_permission_ceiling=(adm.GT2_TARGET_USE,),
    )
    receipt = bridge.admit_gt12_c_relation(relation)
    assert receipt.admission.decision is adm.AdmissionDecision.ADMITTED
    assert receipt.evidence.relation_ref == relation.ref
    assert receipt.admission.relation_ref == relation.ref
