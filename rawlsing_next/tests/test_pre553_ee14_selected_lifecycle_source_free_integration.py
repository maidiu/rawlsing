"""HQ280 B2: source-free test-local C1 -> M2/B5 -> G1/SA/G2/F8 join.

UNEXECUTED CANDIDATE until a separate pinned-runner court reports results.
No real source, EE14 G0b, model-use authority, N9/N10W, actor or V3.
The M2 C1 producer-contract registration below is deliberately TEST-CREATED:
it proves that a generic M2/B5 view can represent the exact produced C1
preimage; it does NOT prove an owner-issued C1 release contract or operative use.
I4 remains M1-only and is separately expected to refuse the C1 route.

Import the EXISTING accepted XOR and B5 fixtures. No replacement engines.
"""
from __future__ import annotations

from dataclasses import replace
import pytest

from rawlsing_next import pre553_learned_product_release as M2
from rawlsing_next import pre553_learned_product_lifecycle as B5
from rawlsing_next import pre553_learned_world_composition as I4
from rawlsing_next.pre553_empirical_objects import ExactRef, semantic_hash
from rawlsing_next.tests import (
    test_pre553_ee14_c1_owner_authenticated_ingress_hq262 as G1,
    test_pre553_ee14_selected_current_asof_hq260 as G3,
)

DEVELOPMENT = "SOURCE_FREE_DEVELOPMENT_ONLY__NONAUTHORIZING__G0B_NOT_ISSUED"
FAMILY = G3.RELEASE_A.product_family_ref
SCOPE = G3.SCOPE
PURPOSE = G3.PURPOSE
PRODUCER_CONTRACT = G1.ref("ProducerContract", "hq280-b2-fixture-c1-view")
OWNER = G1.ref("ProducerOwner", "hq280-b2-fixture-c1-owner")
PERMISSION_CEILING = G1.ref("PermissionCeiling", "hq280-b2-not-a-grant")
SNAPSHOT = G1.auth("hq280-b2-test-only-nonissuer")
AUTH_TRANSPORT = I4.authority_transport_ref(SNAPSHOT)


def _m2_b5_view(repository, source, composition, cell):
    """Real M2 release objects over a test-registered, actual C1 query/preimage."""
    evidence = composition.possibility_slice_evidence_or_null
    assert composition.analytical_state == "SUPPORTED"
    assert composition.producer_fact_state == "SUPPORTED"
    assert evidence is not None and evidence.evidence_state == "SUPPORTED"
    assert evidence.release_ref == source["release_ref"]
    # This ExactRef derives from C1's *actual* computed composition identity.
    anatomy = ExactRef(
        "C1CompositionIdentity",
        f"urn:hq280:b2:fixture:c1:{composition.composed_result_identity_hash}",
        composition.composed_result_identity_hash,
    )
    subject_ref = composition.consumer_query_ref
    dependencies = (
        composition.producer_fact_ref,
        evidence.evidence_ref,
        source["release_ref"],
    )
    determinants = (
        composition.producer_query_ref,
        composition.risk_set_ref,
        evidence.evidence_ref,
        source["release_ref"],
    )
    replay = (composition.consumer_query_ref,)
    explanation = (subject_ref, PRODUCER_CONTRACT, evidence.evidence_ref)

    subject = M2.register_producer_subject(
        repository,
        subject_ref=subject_ref,
        subject_kind="IMMUTABLE_LEARNED_PRODUCT",
        producer_contract_ref=PRODUCER_CONTRACT,
        typed_state=composition.analytical_state,
        semantic_anatomy_ref=anatomy,
        required_authority_refs=(AUTH_TRANSPORT,),
        required_dependency_refs=dependencies,
        required_determinant_refs=determinants,
        required_replay_refs=replay,
        required_explanation_refs=(evidence.evidence_ref,),
    )
    auth = M2.constitute_closure(
        repository, closure_kind="AUTHORITY",
        member_refs=(PRODUCER_CONTRACT, AUTH_TRANSPORT),
        metadata={"authority_ref_preimages": [SNAPSHOT.as_dict()]},
    )
    dep = M2.constitute_closure(
        repository, closure_kind="DEPENDENCY", member_refs=dependencies,
    )
    det = M2.constitute_closure(
        repository, closure_kind="DETERMINANT", member_refs=determinants,
    )
    rep = M2.constitute_closure(
        repository, closure_kind="REPLAY_RECONSTRUCTION", member_refs=replay,
        metadata={"replay_grade": "EXACT_MATERIALIZED_DEREFERENCE"},
    )
    expl = M2.constitute_closure(
        repository, closure_kind="EXPLANATION_LINEAGE", member_refs=explanation,
    )
    release = M2.constitute_release(
        repository,
        release_subject_ref=subject.ref,
        release_subject_kind="IMMUTABLE_LEARNED_PRODUCT",
        semantic_producer_contract_ref=PRODUCER_CONTRACT,
        authority_closure_ref=auth.ref,
        dependency_closure_ref=dep.ref,
        determinant_closure_ref=det.ref,
        replay_reconstruction_ref=rep.ref,
        explanation_lineage_ref=expl.ref,
    )
    lifecycle_subject = B5.LearnedProductLifecycleSubject(
        release_ref=release.ref,
        product_ref=subject.ref,
        product_family_ref=FAMILY,
        producer_owner_ref=OWNER,
        producer_contract_ref=PRODUCER_CONTRACT,
        semantic_projection_hash=anatomy.content_hash,
        authority_snapshot_refs=(SNAPSHOT,),
        direct_dependency_refs=dep.member_refs,
        determinant_refs=det.member_refs,
        determinant_set_hash=semantic_hash([x.as_dict() for x in det.member_refs]),
        replay_root_ref=composition.consumer_query_ref,
        selection_scope_ref=SCOPE,
        build_or_release_receipt_refs=(release.ref,),
        producer_permission_ceiling_ref=PERMISSION_CEILING,
    )
    assert release.release_subject_ref == lifecycle_subject.product_ref
    assert release.ref == lifecycle_subject.release_ref
    assert evidence.evidence_ref in dep.member_refs
    assert source["release_ref"] in dep.member_refs
    assert composition.producer_query_ref in det.member_refs
    return {
        "cell": cell,
        "composition": composition,
        "evidence": evidence,
        "subject": lifecycle_subject,
        "m2_subject": subject,
        "m2_release": release,
        "artifacts": I4.M2ProductArtifacts(subject, auth, dep, det, rep, expl, release),
    }


@pytest.fixture
def case():
    source = G1.fx.xor_fixture()
    qauth = G1._query_authority("c1-at09-xor")
    registry = G1._registry(source, qauth)
    ingress = G1.build_ingress(source, qauth, registry)
    repository = M2.M2Repository()
    cells = {}
    for cell, plan in G1._plans(source).items():
        composition, consumer_query = G1._compose(
            source=source, qauth=qauth, registry=registry,
            conditions=plan.conditions,
            target_question=plan.target_question, tag=plan.tag,
        )
        assert consumer_query.ref == composition.consumer_query_ref
        cells[cell] = _m2_b5_view(repository, source, composition, cell)
    executor = B5.LearnedProductLifecycleExecutor()
    for cell in ("q1", "q2"):
        G3._publish(executor, cells[cell]["subject"])
    key = executor.selection_key(
        product_family_ref=FAMILY,
        selection_scope_ref=SCOPE,
        selection_purpose_ref=PURPOSE,
    )
    first = G3._select(executor, key, cells["q1"]["subject"])
    return {
        "source": source, "qauth": qauth, "registry": registry,
        "ingress": ingress, "m2": repository, "cells": cells,
        "executor": executor, "key": key, "first": first,
    }


def _advance(case):
    """Real B5 owner supersession, never a manually assigned 'current' flag."""
    e, k = case["executor"], case["key"]
    return e.supersede_current(
        k.ref,
        predecessor_release_ref=case["cells"]["q1"]["subject"].release_ref,
        successor_release_ref=case["cells"]["q2"]["subject"].release_ref,
        expected_previous_receipt_ref=case["first"].ref,
        event_authority_ref=G3.EVENT_AUTHORITY,
        event_rule_ref=G3.EVENT_RULE,
        selection_attestation_ref=G3.SELECTION_ATTESTATION,
        supersession_basis_ref=G3.SUPERSESSION_BASIS,
    )


def _join(case, *, as_of_event_ref, mode, claimed_cell=None):
    """Test-local strict join; NONAUTHORIZING; no public service owner is minted."""
    e, k = case["executor"], case["key"]
    at = e.resolve_current_as_of(k.ref, as_of_event_ref=as_of_event_ref)
    if at.state != "CURRENT_SELECTED" or at.selected_release_ref is None:
        raise ValueError("NO_SELECTED_RELEASE_AS_OF")
    current_receipt = e.current_selection_receipt_ref(k.ref)
    live = e.resolve_selection_exact(k.ref, current_receipt)
    if mode == "CURRENT":
        if live.state != "CURRENT_SELECTED" or (
            live.selected_release_ref != at.selected_release_ref
            or live.receipt_ref != at.receipt_ref
        ):
            raise ValueError("HISTORICAL_SELECTION_IS_NOT_CURRENT")
    elif mode != "HISTORICAL":
        raise ValueError("EXPLICIT_MODE_REQUIRED")

    matches = [
        row for row in case["cells"].values()
        if row["m2_release"].ref == at.selected_release_ref
    ]
    if len(matches) != 1:
        raise ValueError("SELECTED_M2_RELEASE_UNBOUND")
    row = matches[0]
    cell = row["cell"]
    if claimed_cell is not None and claimed_cell != cell:
        raise ValueError("C1_CELL_NOT_THE_SELECTED_PRODUCT")
    ids = G1.Q1_STRATUM if cell == "q1" else G1.Q2_STRATUM
    origin = case["ingress"].serve(G1.SelectedRequest(cell=cell, stratum_ids=ids))
    composition, evidence = row["composition"], row["evidence"]
    assert origin.c1_identity_hash == composition.composed_result_identity_hash
    assert origin.c1_evidence_ref_key == G1._key(evidence.evidence_ref)
    assert origin.c1_producer_query_key == G1._key(composition.producer_query_ref)
    assert origin.c1_risk_set_key == G1._key(composition.risk_set_ref)
    assert origin.c1_raw_denominator_support == composition.raw_denominator_support
    assert origin.release_key == case["source"]["release_ref"].object_id
    assert origin.authorizing is False
    material = {
        "grade": DEVELOPMENT, "as_of_mode": mode, "cell": cell,
        "selection_key": k.ref.as_dict(),
        "selection_receipt": at.receipt_ref.as_dict(),
        "selected_m2_release": at.selected_release_ref.as_dict(),
        "c1_subject_ref": row["m2_subject"].ref.as_dict(),
        "c1_composition_hash": composition.composed_result_identity_hash,
        "c1_origin_receipt_hash": origin.origin_receipt_hash,
        "c1_evidence_ref": evidence.evidence_ref.as_dict(),
        "source_c11_release": evidence.release_ref.as_dict(),
        "g2_receipt_hash": origin.g2_receipt_hash,
        "f8_result_hash": origin.f8_result_hash,
        "authorizing": False,
    }
    return material | {"technical_join_hash": semantic_hash(material)}


def test_p01_current_selected_q1_and_progressive_q2_exact_owners(case):
    q1 = _join(
        case, as_of_event_ref=case["first"].current_select_event_ref,
        mode="CURRENT",
    )
    assert q1["cell"] == "q1"
    assert case["cells"]["q1"]["composition"].raw_denominator_support == 2
    selected_q2 = _advance(case)
    q2 = _join(
        case, as_of_event_ref=selected_q2.current_select_event_ref,
        mode="CURRENT",
    )
    assert q2["cell"] == "q2"
    assert case["cells"]["q2"]["composition"].raw_denominator_support == 1
    def counts(cell):
        result = case["cells"][cell]["composition"].consumer_result_or_null
        assert result.result_state == "EXACT_SUPPORTED"
        return {v["cell"]: v["raw_numerator_support"]
                for v in result.material()["exact_lane"]["geometry"]["cells"]}
    assert counts("q1") == {"0": 1, "1": 1}
    assert counts("q2") == {"0": 0, "1": 1}
    assert q1["technical_join_hash"] != q2["technical_join_hash"]
    assert q1["c1_origin_receipt_hash"] != q2["c1_origin_receipt_hash"]
    assert q1["source_c11_release"] == q2["source_c11_release"]
    assert q2["authorizing"] is False


def test_p02_exact_historical_event_and_checkpoint_do_not_relabel_current(case):
    old = case["first"].current_select_event_ref
    prior_checkpoint = case["executor"].export_checkpoint()
    second = _advance(case)
    historical = _join(case, as_of_event_ref=old, mode="HISTORICAL")
    live = _join(
        case, as_of_event_ref=second.current_select_event_ref, mode="CURRENT"
    )
    restored = B5.LearnedProductLifecycleExecutor.from_checkpoint(prior_checkpoint)
    key = case["key"].ref
    earlier = restored.resolve_current_as_of(
        key, as_of_checkpoint=prior_checkpoint
    )
    assert earlier.selected_release_ref == case["cells"]["q1"]["m2_release"].ref
    assert historical["as_of_mode"] == "HISTORICAL"
    assert historical["selected_m2_release"] != live["selected_m2_release"]
    assert historical["selection_receipt"] == case["first"].ref.as_dict()


def test_n01_superseded_or_unselected_product_never_current(case):
    old = case["first"].current_select_event_ref
    _advance(case)
    with pytest.raises(ValueError, match="HISTORICAL_SELECTION_IS_NOT_CURRENT"):
        _join(case, as_of_event_ref=old, mode="CURRENT")
    with pytest.raises(ValueError, match="C1_CELL_NOT_THE_SELECTED_PRODUCT"):
        _join(
            case, as_of_event_ref=case["executor"].events[-1].ref,
            mode="CURRENT", claimed_cell="q1",
        )


def test_n02_owner_invalidation_blocks_stale_and_preserves_sibling(case):
    second = _advance(case)
    q1, q2 = case["cells"]["q1"], case["cells"]["q2"]
    changed = q2["composition"].producer_query_ref
    assert changed not in q1["subject"].determinant_refs
    owner = case["executor"]
    result = owner.declare_invalidation(
        [changed],
        event_authority_ref=G3.EVENT_AUTHORITY,
        event_rule_ref=G3.EVENT_RULE,
        dependency_closure_receipt_ref=G3.DEPENDENCY_CLOSURE,
        selection_attestation_ref=G3.SELECTION_ATTESTATION,
        current_transitions={case["key"].ref.key: None},
    )
    assert q2["m2_release"].ref in (
        result.directly_affected_release_refs
        + result.transitively_affected_release_refs
    )
    assert q1["subject"].product_ref in result.unaffected_product_refs
    resolution = owner.resolve_current_as_of(
        case["key"].ref, as_of_event_ref=owner.events[-1].ref
    )
    assert resolution.state == "NO_CURRENT"
    with pytest.raises(ValueError, match="NO_SELECTED_RELEASE_AS_OF"):
        _join(case, as_of_event_ref=owner.events[-1].ref, mode="CURRENT")
    past = owner.resolve_current_as_of(
        case["key"].ref, as_of_event_ref=second.current_select_event_ref
    )
    assert past.selected_release_ref == q2["m2_release"].ref
    # Historical addressability is not live currentness.


def test_n03_substituted_c1_provenance_cannot_reach_authenticated_f8(case, monkeypatch):
    calls = {"n": 0}
    from rawlsing_next import pre553_service_f8_source_scope_binding as F8
    real = F8.evaluate_bound_positioned_subject_possibility

    def counted(*args, **kwargs):
        calls["n"] += 1
        return real(*args, **kwargs)

    monkeypatch.setattr(F8, "evaluate_bound_positioned_subject_possibility", counted)
    def mutated(evidence):
        return replace(
            evidence,
            provenance_refs=(G1.ref("UNRELATED_PROVENANCE", "hq280-b2-forgery"),),
        )
    hostile = G1.build_ingress(
        case["source"], case["qauth"], case["registry"],
        c1_compose=G1._hostile_compose(G1._compose, mutate=mutated),
    )
    with pytest.raises(G1.SelectedIngressAuthenticationError):
        hostile.serve(G1.SelectedRequest(cell="q2", stratum_ids=G1.Q2_STRATUM))
    assert calls["n"] == 0
    with pytest.raises(ValueError, match="C1_CELL_NOT_THE_SELECTED_PRODUCT"):
        _join(
            case,
            as_of_event_ref=case["first"].current_select_event_ref,
            mode="CURRENT", claimed_cell="q2",
        )


def test_n04_no_operative_g0b_even_after_successful_source_free_join(case):
    joined = _join(
        case, as_of_event_ref=case["first"].current_select_event_ref,
        mode="CURRENT",
    )
    assert joined["grade"] == DEVELOPMENT
    assert joined["authorizing"] is False
    assert joined["technical_join_hash"] not in (
        joined["c1_origin_receipt_hash"], joined["f8_result_hash"]
    )
    assert "G0B_NOT_ISSUED" in joined["grade"]
    assert not hasattr(case["ingress"], "issue_model_use")


def test_i4_m1_only_adapter_refuses_test_registered_c1_product(case):
    """Exact first I4 public-contract ceiling; never rewrite it for C1."""
    row = case["cells"]["q1"]
    contract = I4.LearnedWorldProductContractBinding(
        route="M1_M2_B5",
        product_family_ref=FAMILY,
        producer_owner_ref=OWNER,
        producer_contract_ref=PRODUCER_CONTRACT,
        release_subject_kind="IMMUTABLE_LEARNED_PRODUCT",
        selection_scope_ref=SCOPE,
        producer_permission_ceiling_ref=PERMISSION_CEILING,
        consumer_product_purpose_ref=PURPOSE,
    )
    with pytest.raises(
        I4.LearnedWorldCompositionBlocked,
        match="TYPED_DISPOSITION",
    ):
        I4.adapt_m2_release_to_b5(row["artifacts"], contract=contract)


def test_m2_missing_exact_c1_dependency_refuses_instead_of_release(case):
    """Adopted M2 enforces declared producer closure, even for a test C1 subject."""
    row = case["cells"]["q1"]
    a = row["artifacts"]
    inadequate = M2.constitute_closure(
        case["m2"], closure_kind="DEPENDENCY",
        member_refs=(case["source"]["release_ref"],),
    )
    with pytest.raises(M2.M2ReleaseError, match="DEPENDENCY_CLOSURE_INCOMPLETE"):
        M2.constitute_release(
            case["m2"],
            release_subject_ref=a.subject.ref,
            release_subject_kind="IMMUTABLE_LEARNED_PRODUCT",
            semantic_producer_contract_ref=PRODUCER_CONTRACT,
            authority_closure_ref=a.authority_closure.ref,
            dependency_closure_ref=inadequate.ref,
            determinant_closure_ref=a.determinant_closure.ref,
            replay_reconstruction_ref=a.replay_closure.ref,
            explanation_lineage_ref=a.explanation_closure.ref,
        )
