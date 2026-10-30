"""PYAT HQ281 E03 - source-free N9 to N10W two-step progressive owner run tests.

Development-only, source-free.  These tests execute the REAL accepted owners
(N10E provider, C1 analytical composition, plain F8 evaluator) over an
explicitly synthetic 58-respondent world that is NEVER called real CURRENT.

No N9/N10W owner is claimed implemented; no G0b/model-use/B5-CURRENT/Field
Forge/temporal/actor grant is claimed; no raw SAV/DTA is read.
"""

from __future__ import annotations

import pytest

import rawlsing_next.pre553_n9_n10w_progressive_candidate as pc
from rawlsing_next.pre553_analytical_composition import (
    AnalyticalCompositionError,
    compose_positioned_subject_possibility,
)
from rawlsing_next.source_backed_positioned_subject_possibility import (
    PositionedSubjectPossibilityError,
    evaluate_positioned_subject_possibility,
)
from rawlsing_next.tests.c1_at08_at13_fixture import (
    readdress_witness_with_false_pairing,
)
import rawlsing_next.tests.test_pre553_empirical_query as i03


# ==========================================================================
# FIXTURE / WORLD
# ==========================================================================
def test_synthetic_world_is_58_rows_and_never_real_current():
    rows = pc.synthetic_world_rows()
    assert len(rows) == 58
    assert all(set(r["responses"]) == {"A", "B", "C", "Y"} for r in rows)
    assert len({r["id"] for r in rows}) == 58
    # every positioned subject the chain builds carries real_subject False
    world = pc.build_synthetic_world()
    _, material = pc._subject_ref("step1", "CONDITIONED_SUBJECT")
    assert material["real_subject"] is False
    _, material2 = pc._subject_ref("step3", "CONDITIONED_SUBJECT")
    assert material2["real_subject"] is False


# ==========================================================================
# POSITIVE: the full progressive chain against the hand-derived oracle
# ==========================================================================
def test_full_progressive_chain_matches_hand_derived_oracle():
    world = pc.build_synthetic_world()
    chain = pc.run_progressive_chain(world)
    assert len(chain.steps) == 3
    for step, oracle_key in zip(chain.steps, ("step1", "step2", "step3")):
        oracle = pc.E03_ORACLE[oracle_key]
        assert step.raw_denominator_support == oracle["denominator"], step.step_id
        cells = {k: v["raw_numerator_support"] for k, v in step.cells.items()}
        assert cells == oracle["cells"], step.step_id
        fractions = {
            k: v["raw_probability_exact_fraction"] for k, v in step.cells.items()
        }
        assert fractions["1"] == oracle["fraction"], step.step_id
        assert step.consumer_state == "EXACT_SUPPORTED"
        assert step.uncertainty_state == "UNCERTAINTY_UNQUANTIFIED"
    # exact fractions 9/16, 5/8, 3/4
    assert pc.E03_ORACLE["step1"]["fraction"] == {"$exact_fraction": [9, 16]}
    assert pc.E03_ORACLE["step2"]["fraction"] == {"$exact_fraction": [5, 8]}
    assert pc.E03_ORACLE["step3"]["fraction"] == {"$exact_fraction": [3, 4]}


def test_progressive_steps_preserve_release_risk_and_minority():
    world = pc.build_synthetic_world()
    chain = pc.run_progressive_chain(world)
    first = chain.steps[0]
    for step in chain.steps[1:]:
        assert step.release_ref == first.release_ref
        assert step.risk_set_ref == first.risk_set_ref
        # minority alternatives survive at every depth
        assert set(step.cells) == {"0", "1"}
        assert min(c["raw_numerator_support"] for c in step.cells.values()) >= 1
        assert step.uncertainty_state == first.uncertainty_state


def test_denominator_is_the_conditioned_cohort_not_the_marginal():
    """q(C|A) and q(C|A,B) must measure DIFFERENT denominators by identity."""
    world = pc.build_synthetic_world()
    chain = pc.run_progressive_chain(world)
    d1, d2, d3 = (s.raw_denominator_support for s in chain.steps)
    assert (d1, d2, d3) == (32, 16, 8)
    assert d1 > d2 > d3  # conditioning narrows the cohort exactly


def test_production_and_consumption_are_distinct_invocations():
    world = pc.build_synthetic_world()
    chain = pc.run_progressive_chain(world)
    calls = [e["call"] for e in chain.invocation_log]
    # three production calls, three consumption calls, distinct identities
    assert calls.count("provide_empirical_possibility_slice") == 1
    assert calls.count("compose_positioned_subject_possibility") == 2
    assert calls.count("evaluate_positioned_subject_possibility") == 3
    # F8 consumed the exact evidence object each step produced
    for step, consumption in zip(chain.steps, chain.f8_consumptions):
        produced = step.produced_evidence.evidence_ref.content_hash
        consumed = (consumption["exact_evidence_ref"] or {}).get("content_hash")
        assert consumed == produced, step.step_id
        assert consumption["result_state"] == "EXACT_SUPPORTED"


def test_progressive_declares_no_rights_and_no_real_current():
    world = pc.build_synthetic_world()
    chain = pc.run_progressive_chain(world)
    assert dict(chain.effects) == {
        "source_meaning_inference": False,
        "model_use_grant": False,
        "g0b_issuance": False,
        "b5_current_selection": False,
        "field_forge_effect": False,
        "temporal_current_effect": False,
        "actor_v3_effect": False,
        "real_current_claim": False,
    }


# ==========================================================================
# HOSTILES (all empirically observed refusals)
# ==========================================================================
def test_unordered_conditioner_list_is_refused():
    """Consumer [B,A] with a witness built for [A,B] must refuse."""
    world = pc.build_synthetic_world()
    source = world["source"]
    conds = (("A", 1), ("B", 1))
    predicate = pc._joint_predicate(world, conds)
    producer_query = pc._producer_query(world, predicate)
    forward_query = pc._consumer_query(world, "fwd", conds)
    forward_witness = pc._witness(world, "fwd", forward_query,
                                  producer_query, predicate, conds)
    reversed_query = pc._consumer_query(world, "rev", tuple(reversed(conds)))
    with pytest.raises(Exception) as excinfo:
        compose_positioned_subject_possibility(
            repository=source["repo"], empirical_query=producer_query,
            predicate=predicate, authority_registry=world["registry"],
            release_refs=(source["release_ref"],),
            consumer_query=reversed_query, model_rule=world["model_rule"],
            condition_binding_witness=forward_witness)
    assert "ConditionValueRelationMismatch" in type(excinfo.value).__name__


def test_empty_predicate_cannot_fabricate_a_null_geometry():
    """A zero-support predicate must refuse, never produce invented cells."""
    world = pc.build_synthetic_world()
    source = world["source"]
    empty = i03._branch_predicate(source, world["qauth"], members=(),
                                  tag="e03-empty")
    query = i03._query(source, world["qauth"], empty, ("Y",), risk="R",
                       tag="e03-empty-q")
    consumer_query = pc._consumer_query(world, "empty", (("A", 1),))
    witness = pc._witness(world, "empty", consumer_query, query, empty,
                          (("A", 1),))
    with pytest.raises(Exception) as excinfo:
        compose_positioned_subject_possibility(
            repository=source["repo"], empirical_query=query, predicate=empty,
            authority_registry=world["registry"],
            release_refs=(source["release_ref"],),
            consumer_query=consumer_query, model_rule=world["model_rule"],
            condition_binding_witness=witness)
    assert "no matching producer leaf" in str(excinfo.value)


def test_weighted_measure_is_typed_unavailable_never_collapsed():
    """A GOVERNED_WEIGHTED producer over an unweighted fixture is UNAVAILABLE."""
    world = pc.build_synthetic_world()
    source = world["source"]
    conds = (("A", 1),)
    predicate = pc._joint_predicate(world, conds)
    weighted_query = pc._producer_query(world, predicate)
    grain = dict(weighted_query.requested_output_grain)
    grain["measure_kind"] = "GOVERNED_WEIGHTED"
    grain["weight_basis_id"] = "W"
    weighted_query = pc.EmpiricalQuerySpec(
        typed_state=weighted_query.typed_state,
        authority_snapshot_refs=weighted_query.authority_snapshot_refs,
        dependency_refs=weighted_query.dependency_refs,
        producer_replay_locator_or_reference_root=(
            weighted_query.producer_replay_locator_or_reference_root),
        target_refs=weighted_query.target_refs,
        target_arity_and_topology=weighted_query.target_arity_and_topology,
        condition_predicate_ref=weighted_query.condition_predicate_ref,
        risk_set_ref=weighted_query.risk_set_ref,
        empirical_universe_refs=weighted_query.empirical_universe_refs,
        scope_refs=weighted_query.scope_refs,
        measure_basis_ref=i03._ref("MEASURE_BASIS", "GOVERNED_WEIGHTED"),
        requested_output_grain=grain,
        query_authority_refs=weighted_query.query_authority_refs,
    )
    consumer_query = pc._consumer_query(world, "weighted", conds)
    witness = pc._witness(world, "weighted", consumer_query, weighted_query,
                          predicate, conds)
    result = compose_positioned_subject_possibility(
        repository=source["repo"], empirical_query=weighted_query,
        predicate=predicate, authority_registry=world["registry"],
        release_refs=(source["release_ref"],),
        consumer_query=consumer_query, model_rule=world["model_rule"],
        condition_binding_witness=witness)
    assert result.analytical_state == "UNAVAILABLE"
    assert result.possibility_slice_evidence_or_null is None
    # and the raw measure stays distinct and supported
    raw_step = pc.run_single_conditioner_step(world)
    assert raw_step.raw_denominator_support == 32


def test_cross_sample_join_is_refused():
    """A consumer query from a different universe/release cannot join."""
    world = pc.build_synthetic_world()
    source = world["source"]
    other = i03._build_source(
        "e03-other-sample",
        [{"id": f"X{n:03d}",
          "responses": {"A": n % 2, "B": (n // 2) % 2, "C": 1, "Y": n % 2}}
         for n in range(1, 21)],
        question_namespace="e03-other-sample",
        risk_sets={"R_ALL": {q: {r["id"] for r in
                                  [{"id": f"X{n:03d}",
                                    "responses": {"A": n % 2, "B": (n // 2) % 2,
                                                  "C": 1, "Y": n % 2}}
                                   for n in range(1, 21)]}
                            for q in ("A", "B", "C", "Y")}},
        risk_namespace="e03-other-sample",
    )
    other["risk_refs"]["R"] = other["risk_refs"]["R_ALL"]
    conds = (("A", 1),)
    predicate = pc._joint_predicate(world, conds)
    producer_query = pc._producer_query(world, predicate)
    foreign_pairing = pc.fx.make_pairing_authority("e03-other-sample")
    foreign_bindings = tuple(
        pc.fx.make_conditioner_binding(
            binding_id=q.lower(),
            subject_fact_ref=pc.ExactRef(**pc.fx.subject_fact_ref(
                other, q, value)),
            empirical_coordinate_ref=other["qrefs"][q],
            comparability_authority_ref=foreign_pairing,
            source_universe_ref=other["universe"].ref,
            release_ref=other["release_ref"])
        for q, value in conds)
    foreign_query = pc.fx.make_multi_conditioner_consumer_query(
        query_id="e03-cross-sample",
        subject_ref=pc._subject_ref("x", "FOREIGN_SUBJECT")[0],
        target_ref=other["qrefs"]["Y"],
        source_universe_ref=other["universe"].ref,
        release_ref=other["release_ref"],
        bindings=list(foreign_bindings),
        projection_kind="E03_PROGRESSIVE_CONDITIONAL_DISTRIBUTION")
    witness = pc._witness(world, "x", foreign_query, producer_query,
                          predicate, conds)
    with pytest.raises(Exception) as excinfo:
        compose_positioned_subject_possibility(
            repository=source["repo"], empirical_query=producer_query,
            predicate=predicate, authority_registry=world["registry"],
            release_refs=(source["release_ref"],),
            consumer_query=foreign_query, model_rule=world["model_rule"],
            condition_binding_witness=witness)
    assert "SOURCE_UNIVERSE_MISMATCH" in str(excinfo.value)


def test_false_pairing_value_is_refused():
    world = pc.build_synthetic_world()
    source = world["source"]
    conds = (("A", 1), ("B", 1))
    predicate = pc._joint_predicate(world, conds)
    producer_query = pc._producer_query(world, predicate)
    consumer_query = pc._consumer_query(world, "step2", conds)
    witness = pc._witness(world, "step2", consumer_query, producer_query,
                          predicate, conds)
    forged = readdress_witness_with_false_pairing(
        witness, conditioner_index=1, false_exact_value=0)
    with pytest.raises(Exception) as excinfo:
        compose_positioned_subject_possibility(
            repository=source["repo"], empirical_query=producer_query,
            predicate=predicate, authority_registry=world["registry"],
            release_refs=(source["release_ref"],),
            consumer_query=consumer_query, model_rule=world["model_rule"],
            condition_binding_witness=forged)
    assert "pairing exact value mismatch" in str(excinfo.value)


def test_own_topic_joint_conditioners_are_refused():
    """A and A=1 twice is a co-topic fake joint, not a coparent inference."""
    world = pc.build_synthetic_world()
    with pytest.raises(Exception) as excinfo:
        pc.run_joint_conditioner_step(world, "P_Y_given_A_A",
                                      (("A", 1), ("A", 1)))
    assert "duplicate conditioner binding" in str(excinfo.value)


def test_exact_absence_is_unresolved_not_proxied_or_exact():
    """Absent exact stratum: UNRESOLVED, never EXACT_SUPPORTED."""
    world = pc.build_synthetic_world()
    source = world["source"]
    step3_conds = (("A", 1), ("B", 1), ("C", 1))
    predicate = pc._joint_predicate(world, step3_conds)
    producer_query = pc._producer_query(world, predicate)
    consumer_query = pc._consumer_query(world, "step3", step3_conds)
    witness = pc._witness(world, "step3", consumer_query, producer_query,
                          predicate, step3_conds)
    composition = compose_positioned_subject_possibility(
        repository=source["repo"], empirical_query=producer_query,
        predicate=predicate, authority_registry=world["registry"],
        release_refs=(source["release_ref"],),
        consumer_query=consumer_query, model_rule=world["model_rule"],
        condition_binding_witness=witness)
    evidence = composition.possibility_slice_evidence_or_null
    # ask F8 for a stratum the supplied evidence does not cover
    result = evaluate_positioned_subject_possibility(
        query=pc._consumer_query(world, "P_Y_given_A_B", (("A", 1), ("B", 1))),
        rule=world["model_rule"], evidence=(evidence,))
    assert result.result_state == "UNRESOLVED"
    assert result.exact_reason == "EXACT_POSITIONED_STRATUM_ABSENT"
    assert result.exact_evidence_ref is None
    # and an entirely disjoint stratum is likewise UNRESOLVED
    disjoint = evaluate_positioned_subject_possibility(
        query=pc._consumer_query(world, "P_Y_given_A_B", (("A", 0), ("B", 1))),
        rule=world["model_rule"], evidence=(evidence,))
    assert disjoint.result_state == "UNRESOLVED"


def test_walkback_proxy_is_labelled_never_presented_as_exact():
    """An authorized walkback yields a proxy-labelled state, not EXACT."""
    world = pc.build_synthetic_world()
    source = world["source"]
    from rawlsing_next.pre553_empirical_objects import AuthorityRef
    from rawlsing_next.source_backed_positioned_subject_possibility import (
        PositionedSubjectPossibilityModelRule,
        SpecificityWalkbackStep,
    )
    proxy_material = {"role": "E03_FIXTURE_ONLY_WALKBACK_PROXY",
                      "real_proxy": False}
    proxy_auth = AuthorityRef(
        authority_id="urn:test:e03:fixture-proxy",
        authority_version="1.0.0",
        authority_content_hash=pc.semantic_hash(proxy_material))
    rule = PositionedSubjectPossibilityModelRule(
        model_authority_ref=world["model_rule"].model_authority_ref,
        walkback_authority_ref=world["model_rule"].walkback_authority_ref,
        source_universe_refs=(source["universe"].ref,),
        walkback_steps=(SpecificityWalkbackStep(
            step_id="w1",
            retained_conditioner_ids=("a",),
            proxy_authority_ref=proxy_auth,
            source_universe_ref=source["universe"].ref,
            release_ref=source["release_ref"],
            rationale="E03 fixture-only walkback probe"),),
        positive_proxy_authority_refs=(proxy_auth,))
    # produce ONLY the single-conditioner (A=1) evidence
    step1 = pc.run_single_conditioner_step(world)
    # ask F8 for the TWO-conditioner stratum with only that evidence present
    result = evaluate_positioned_subject_possibility(
        query=pc._consumer_query(world, "P_Y_given_A_B", (("A", 1), ("B", 1))),
        rule=rule, evidence=(step1.produced_evidence,))
    # the proxy is available and labelled; it is NOT EXACT_SUPPORTED
    assert result.result_state == "EXACT_UNRESOLVED_PROXY_AVAILABLE"
    assert result.exact_reason == "EXACT_POSITIONED_STRATUM_ABSENT"
    assert result.exact_evidence_ref is None
    assert result.proxy is not None


def test_single_conditioner_provider_rejects_multi_conditioner_query():
    """The exact missing edge: N10E supports ONLY one conditioner."""
    from rawlsing_next.pre553_empirical_possibility_provider import (
        _single_binding,
    )
    from rawlsing_next.source_backed_positioned_subject_possibility import (
        PositionedSubjectPossibilityQuery,
    )
    world = pc.build_synthetic_world()
    conds = (("A", 1), ("B", 1))
    query = pc._consumer_query(world, "step2", conds)
    assert len(query.conditioner_bindings) == 2
    with pytest.raises(Exception) as excinfo:
        _single_binding(query)
    assert "exactly one conditioner" in str(excinfo.value)


# ==========================================================================
# GOVERNANCE: import surface, fixture posture
# ==========================================================================
def test_module_import_surface_contains_no_forbidden_owner():
    import inspect
    source = inspect.getsource(pc)
    imports = "\n".join(
        line for line in source.splitlines()
        if line.startswith("from ") or line.startswith("import ")
    )
    for token in ("learned_product_lifecycle", "field_forge",
                  "v3_adp", "structural_admission", "m5_runtime", "m6_actor"):
        assert token not in imports


def test_no_raw_sav_dta_and_no_respondent_row_leakage():
    source = (pc.E03_TAG and __import__("pathlib").Path(
        __import__("rawlsing_next.pre553_n9_n10w_progressive_candidate",
                   fromlist=["__file__"]).__file__).read_text())
    for forbidden in (".sav", ".dta", "pyreadstat"):
        assert forbidden not in source
    rows = pc.synthetic_world_rows()
    # the fixture is synthetic E03 ids, never real respondent identities
    assert all(r["id"].startswith("E03-") for r in rows)


def test_single_conditioner_step_uses_real_provider_state_vocabulary():
    world = pc.build_synthetic_world()
    step = pc.run_single_conditioner_step(world)
    assert step.producer_route == "N10E_SINGLE_CONDITIONER"
    log = step.invocation_log[0]
    assert log["call"] == "provide_empirical_possibility_slice"
    assert log["outputs"]["provider_state"] == "EXACT_SUPPORTED_SLICE_PRODUCED"
