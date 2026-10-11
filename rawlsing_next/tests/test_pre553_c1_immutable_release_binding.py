"""HQ280 F8D candidate acceptance/hostile court: UNEXECUTED at authoring.

Uses real accepted C1 and G1 source-free XOR fixture producers. The C1/M2/B5
owner binding is NEW, not adopted. No test manufactures operative G0b permission.
Run independently on a repository-capable Python/pytest executor.
"""
from dataclasses import replace

import pytest

from rawlsing_next import pre553_c1_immutable_release_binding as F8D
from rawlsing_next import pre553_learned_product_release as M2
from rawlsing_next import pre553_learned_product_lifecycle as B5
from rawlsing_next.pre553_empirical_objects import ExactRef, semantic_hash
from rawlsing_next.tests import c1_at08_at13_fixture as FX
from rawlsing_next.tests import (
    test_pre553_ee14_c1_owner_authenticated_ingress_hq262 as G1,
)
from rawlsing_next.tests import (
    test_pre553_ee14_selected_current_asof_hq260 as G3,
)
from rawlsing_next.tests.test_pre553_empirical_query import (
    _query_authority, _registry,
)


@pytest.fixture(scope="module")
def actual():
    source = FX.xor_fixture()
    qauth = _query_authority("c1-at09-xor")
    registry = _registry(source, qauth)
    plans = G1._plans(source)
    out = {}
    for cell in ("q1", "q2"):
        plan = plans[cell]
        composition, consumer_query = G1._compose(
            source=source, qauth=qauth, registry=registry,
            conditions=plan.conditions, target_question=plan.target_question,
            tag=plan.tag,
        )
        assert composition.consumer_query_ref == consumer_query.ref
        out[cell] = (composition, plan.model_rule)
    return source, out


def build(actual, cell="q1", **overrides):
    source, products = actual
    composition, model_rule = products[cell]
    args = {
        "cell": cell,
        "composition": composition,
        "model_rule": model_rule,
        "source_release_ref": source["release_ref"],
    }
    args.update(overrides)
    return F8D.build_source_free_c1_release(**args)


def test_p01_two_actual_c1_products_receive_distinct_exact_m2_releases(actual):
    q1, q2 = build(actual, "q1"), build(actual, "q2")
    assert (q1.composition.raw_denominator_support,
            q2.composition.raw_denominator_support) == (2, 1)
    assert sorted(x["raw_numerator_support"] for x in q1.evidence.geometry["cells"]) == [1, 1]
    assert sorted(x["raw_numerator_support"] for x in q2.evidence.geometry["cells"]) == [0, 1]
    assert q1.evidence.release_ref == q2.evidence.release_ref == actual[0]["release_ref"]
    assert q1.composition.producer_query_ref != q2.composition.producer_query_ref
    assert q1.evidence.evidence_ref != q2.evidence.evidence_ref
    assert q1.release.ref != q2.release.ref
    assert q1.subject.ref != q2.subject.ref
    assert q1.lifecycle_subject.selection_scope_ref == q2.lifecycle_subject.selection_scope_ref
    assert q1.lifecycle_subject.product_family_ref == q2.lifecycle_subject.product_family_ref
    assert q1.lifecycle_subject.producer_contract_ref == q2.lifecycle_subject.producer_contract_ref


def test_p02_all_five_required_m2_closures_and_dependency_graph(actual):
    view = build(actual)
    assert set(view.closures) == {
        "AUTHORITY", "DEPENDENCY", "DETERMINANT",
        "REPLAY_RECONSTRUCTION", "EXPLANATION_LINEAGE",
    }
    assert view.release.release_subject_ref == view.subject.ref
    assert view.subject.producer_contract_ref == F8D.CANDIDATE_CONTRACT_REF
    assert F8D.CANDIDATE_CONTRACT_REF in view.closures["AUTHORITY"].member_refs
    assert view.evidence.evidence_ref in view.closures["DEPENDENCY"].member_refs
    assert actual[0]["release_ref"] in view.closures["DEPENDENCY"].member_refs
    assert view.composition.producer_fact_ref in view.closures["DEPENDENCY"].member_refs
    assert view.composition.producer_query_ref in view.closures["DETERMINANT"].member_refs
    assert view.composition.risk_set_ref in view.closures["DETERMINANT"].member_refs
    assert view.composition.denominator_member_refs[0] in view.closures["DETERMINANT"].member_refs
    assert view.evidence.evidence_ref in view.closures["EXPLANATION_LINEAGE"].member_refs
    assert view.analytical_registration.product_ref == view.subject.ref
    assert view.analytical_registry.registrations == (view.analytical_registration,)


def test_p03_stable_content_addressing_no_new_issuer(actual):
    first, second = build(actual), build(actual)
    assert first.subject.ref == second.subject.ref
    assert first.release.ref == second.release.ref
    assert first.closures["AUTHORITY"].ref == second.closures["AUTHORITY"].ref
    assert first.grade == F8D.DEVELOPMENT_GRADE
    assert first.authorizing is second.authorizing is False
    assert "NONAUTHORIZING" in first.grade
    assert "G0B_HELD" in first.grade
    assert first.lifecycle_subject.producer_permission_ceiling_ref == F8D.PERMISSION_CEILING_REF


def test_p04_b5_stage_register_only_no_publication_or_currentness(actual):
    view = build(actual)
    executor = B5.LearnedProductLifecycleExecutor()
    staged = executor.stage_release(view.lifecycle_subject)
    assert staged == view.lifecycle_subject
    with pytest.raises(B5.LearnedProductLifecycleError):
        executor.lifecycle_state(view.release.ref)
    executor.register_product(
        view.release.ref, event_authority_ref=G3.EVENT_AUTHORITY,
        event_rule_ref=G3.EVENT_RULE,
    )
    state = executor.lifecycle_state(view.release.ref)
    assert state.publication == "UNPUBLISHED"
    assert state.replay == F8D.B5_REPLAY_STATE
    with pytest.raises(B5.LearnedProductLifecycleError, match="MISSING_REPLAY_CLOSURE"):
        executor.publish_product(
            view.release.ref, event_authority_ref=G3.EVENT_AUTHORITY,
            event_rule_ref=G3.EVENT_RULE,
        )
    key = executor.selection_key(
        product_family_ref=F8D.CANDIDATE_FAMILY_REF,
        selection_scope_ref=view.lifecycle_subject.selection_scope_ref,
        selection_purpose_ref=G3.PURPOSE,
    )
    with pytest.raises(B5.LearnedProductLifecycleError):
        executor.current_selection_receipt_ref(key.ref)


def test_p05_historical_only_replay_cannot_claim_fresh_process(actual):
    view = build(actual)
    assert view.replay_claim.replay_grade == "HISTORICAL_EXPLANATION_ONLY"
    assert view.replay_claim.actual_replay_mechanism == "HISTORICAL_NARRATION"
    assert view.replay_claim.replay_state == "REPLAY_UNRESOLVED"
    meta = view.closures["REPLAY_RECONSTRUCTION"].metadata
    assert meta["replay_grade"] == F8D.M2_REPLAY_GRADE
    assert meta["fresh_process_proved"] is False
    assert view.lifecycle_subject.rebuild_state == "REBUILD_BLOCKED"


def test_n01_wrong_source_release_is_refused(actual):
    wrong = ExactRef("C11LogicalRelease", "urn:test:f8d:wrong", "f" * 64)
    with pytest.raises(F8D.C1ImmutableReleaseHold, match="SOURCE_RELEASE_MISMATCH"):
        build(actual, source_release_ref=wrong)


def test_n02_wrong_model_rule_is_refused(actual):
    universe = actual[0]["universe"].ref
    foreign = FX.make_model_rule(universe, "hq280-f8d-foreign")
    with pytest.raises(F8D.C1ImmutableReleaseHold, match="MODEL_RULE_MISMATCH"):
        build(actual, model_rule=foreign)


def test_n03_wrong_conditioner_cell_or_risk_ref_is_refused(actual):
    comp, model = actual[1]["q2"]
    with pytest.raises(F8D.C1ImmutableReleaseHold, match="RISK_CONDITION_MISMATCH"):
        build(actual, cell="q1", composition=comp, model_rule=model)
    drift = replace(comp, risk_set_ref=actual[1]["q1"][0].risk_set_ref)
    with pytest.raises(F8D.C1ImmutableReleaseHold, match="C1_IDENTITY_DRIFT"):
        build(actual, cell="q2", composition=drift, model_rule=model)


def test_n04_forged_same_person_denominator_is_refused_even_if_rehashed(actual):
    comp, model = actual[1]["q1"]
    identical = (comp.denominator_member_refs[0],) * 2
    bad = replace(comp, denominator_member_refs=identical)
    bad = replace(bad, composed_result_identity_hash=semantic_hash(bad.identity_material()))
    with pytest.raises(F8D.C1ImmutableReleaseHold, match="SAME_RESPONDENT_RISK_MISMATCH"):
        build(actual, composition=bad, model_rule=model)


def test_n05_native_nonsupported_valid_empty_mints_no_m2(actual, monkeypatch):
    composition, model = actual[1]["q1"]
    invalid = replace(composition, analytical_state="VALID_EMPTY",
                      producer_fact_state="VALID_EMPTY")
    calls = {"m2": 0}
    original = M2.register_producer_subject
    def watch(*a, **kw):
        calls["m2"] += 1
        return original(*a, **kw)
    monkeypatch.setattr(M2, "register_producer_subject", watch)
    with pytest.raises(F8D.C1ImmutableReleaseHold, match="C1_NATIVE_NONPOSITIVE"):
        build(actual, composition=invalid, model_rule=model)
    assert calls["m2"] == 0


def test_n06_tampered_c1_provenance_and_evidence_are_refused(actual):
    comp, model = actual[1]["q1"]
    ev = comp.possibility_slice_evidence_or_null
    substituted = replace(ev, provenance_refs=())
    altered = replace(comp, possibility_slice_evidence_or_null=substituted)
    with pytest.raises(F8D.C1ImmutableReleaseHold):
        build(actual, composition=altered, model_rule=model)
    bad_evidence = replace(ev, raw_support=99)
    mismatch = replace(comp, possibility_slice_evidence_or_null=bad_evidence)
    with pytest.raises(F8D.C1ImmutableReleaseHold):
        build(actual, composition=mismatch, model_rule=model)


def test_n07_replay_overclaim_is_refused(actual):
    with pytest.raises(F8D.C1ImmutableReleaseHold, match="REPLAY_GRADE_OVERCLAIM"):
        build(actual, requested_replay_grade="EXACT_DETERMINISTIC_REBUILD")
    with pytest.raises(F8D.C1ImmutableReleaseHold, match="REPLAY_GRADE_OVERCLAIM"):
        build(actual, requested_replay_grade="EXACT_SERVICE_REEXECUTION")


def test_n08_missing_dependency_or_determinant_closure_refused_by_real_m2(actual):
    view = build(actual)
    for kind, code in [
        ("DEPENDENCY", "DEPENDENCY_CLOSURE_INCOMPLETE"),
        ("DETERMINANT", "DETERMINANT_CLOSURE_INCOMPLETE"),
        ("AUTHORITY", "AUTHORITY_CLOSURE_INCOMPLETE"),
    ]:
        empty = M2.constitute_closure(
            view.repository, closure_kind=kind, member_refs=(),
        )
        ref = {
            "authority_closure_ref": view.closures["AUTHORITY"].ref,
            "dependency_closure_ref": view.closures["DEPENDENCY"].ref,
            "determinant_closure_ref": view.closures["DETERMINANT"].ref,
            "replay_reconstruction_ref": view.closures["REPLAY_RECONSTRUCTION"].ref,
            "explanation_lineage_ref": view.closures["EXPLANATION_LINEAGE"].ref,
        }
        field = {"DEPENDENCY": "dependency_closure_ref",
                 "DETERMINANT": "determinant_closure_ref",
                 "AUTHORITY": "authority_closure_ref"}[kind]
        ref[field] = empty.ref
        with pytest.raises(M2.M2ReleaseError) as err:
            M2.constitute_release(
                view.repository, release_subject_ref=view.subject.ref,
                release_subject_kind=view.subject.subject_kind,
                semantic_producer_contract_ref=F8D.CANDIDATE_CONTRACT_REF,
                **ref,
            )
        assert err.value.code == code


def test_n09_substituted_contract_refuses_and_is_not_g0b(actual):
    view = build(actual)
    fake = ExactRef("C1DevelopmentContractCandidate", "urn:test:f8d:forged", "f" * 64)
    with pytest.raises(M2.M2ReleaseError, match="PRODUCER_CONTRACT_MISMATCH"):
        M2.constitute_release(
            view.repository,
            release_subject_ref=view.subject.ref,
            release_subject_kind=view.subject.subject_kind,
            semantic_producer_contract_ref=fake,
            authority_closure_ref=view.closures["AUTHORITY"].ref,
            dependency_closure_ref=view.closures["DEPENDENCY"].ref,
            determinant_closure_ref=view.closures["DETERMINANT"].ref,
            replay_reconstruction_ref=view.closures["REPLAY_RECONSTRUCTION"].ref,
            explanation_lineage_ref=view.closures["EXPLANATION_LINEAGE"].ref,
        )
    with pytest.raises(TypeError):
        build(actual, operative_g0b_permission=fake)
    with pytest.raises(TypeError):
        build(actual, producer_issuer_root=fake)


def test_n10_i4_m1_only_and_no_selected_service_path(actual):
    from rawlsing_next import pre553_learned_world_composition as I4
    view = build(actual)
    assert view.subject.subject_kind == "IMMUTABLE_LEARNED_PRODUCT"
    assert view.subject.producer_contract_ref != I4.M1_DISPOSITION_PRODUCER_CONTRACT_REF
    assert not hasattr(F8D, "serve_selected_release")
    assert not hasattr(F8D, "issue_model_use_permission")
    assert not hasattr(F8D, "select_current")
