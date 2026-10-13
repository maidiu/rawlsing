"""PYAT HQ282 P04 — source-free selected-world → progressive-consumer contract tests.

Development-only, source-free.  These tests execute the REAL accepted owners
(N10E provider, C1 analytical composition, plain F8 evaluator) over an
explicitly synthetic 58-respondent world bound to a SelectedWorldContract
that is NEVER called real CURRENT.

No N9/N10W owner is claimed implemented; no G0b/model-use/B5-CURRENT/Field
Forge/temporal/actor grant is claimed; no raw SAV/DTA is read.
"""

from __future__ import annotations

import pytest

import rawlsing_next.pre553_selected_world_progressive_contract as p04
import rawlsing_next.pre553_n9_n10w_progressive_candidate as pc
from rawlsing_next.pre553_analytical_composition import (
    compose_positioned_subject_possibility,
)
from rawlsing_next.source_backed_positioned_subject_possibility import (
    evaluate_positioned_subject_possibility,
)
import rawlsing_next.tests.test_pre553_empirical_query as i03


# ==========================================================================
# FIXTURE / CONTRACT
# ==========================================================================
def test_select_world_emits_frozen_contract_with_synthetic_metadata():
    contract, world = p04.select_world()
    assert contract.contract_id == p04.P04_CONTRACT_ID
    assert contract.world_tag == p04.P04_TAG
    assert contract.real_current is False
    meta = contract.selection_metadata
    assert meta["selection_kind"] == "SOURCE_FREE_SYNTHETIC"
    assert meta["real_current"] is False
    assert meta["n9_owner_status"] == "ABSENT__E01_IMPLEMENTED_FALSE"
    assert meta["n10w_owner_status"] == "ABSENT__E01_IMPLEMENTED_FALSE"
    assert meta["g0b_status"] == "ABSENT__NOT_FABRICATED"
    assert meta["b5_current_status"] == "ABSENT__NOT_SELECTED"
    assert meta["row_count"] == 58
    assert world is not None


def test_contract_is_immutable():
    contract, _ = p04.select_world()
    with pytest.raises(Exception):
        contract.real_current = True
    with pytest.raises(Exception):
        contract.world_tag = "hijacked"


def test_contract_content_hash_is_deterministic():
    c1, _ = p04.select_world()
    c2, _ = p04.select_world()
    assert p04.contract_content_hash(c1) == p04.contract_content_hash(c2)


def test_effects_declare_no_rights():
    eff = p04.effects()
    assert all(v is False for v in eff.values())
    assert eff["n9_owner_implemented"] is False
    assert eff["n10w_owner_implemented"] is False


# ==========================================================================
# POSITIVE: full progressive chain under the selected-world contract
# ==========================================================================
def test_full_chain_matches_hand_derived_oracle_under_contract():
    contract, world = p04.select_world()
    chain = p04.run_selected_world_progressive_chain(contract, world=world)
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


def test_chain_preserves_contract_bindings():
    contract, world = p04.select_world()
    chain = p04.run_selected_world_progressive_chain(contract, world=world)
    checks = p04.verify_chain_preserves_contract(contract, chain)
    assert checks["release_ref_preserved"] is True
    assert checks["risk_set_ref_preserved"] is True
    assert checks["minority_cells_present"] is True
    assert checks["uncertainty_conserved"] is True
    assert checks["real_current_false"] is True
    assert checks["oracle_match"] is True


def test_exact_fractions_9_16_5_8_3_4():
    contract, world = p04.select_world()
    chain = p04.run_selected_world_progressive_chain(contract, world=world)
    fracs = []
    for step in chain.steps:
        f = step.cells["1"]["raw_probability_exact_fraction"]
        fracs.append(f["$exact_fraction"])
    assert fracs == [[9, 16], [5, 8], [3, 4]]


def test_denominator_is_conditioned_cohort():
    contract, world = p04.select_world()
    chain = p04.run_selected_world_progressive_chain(contract, world=world)
    d1, d2, d3 = (s.raw_denominator_support for s in chain.steps)
    assert (d1, d2, d3) == (32, 16, 8)
    assert d1 > d2 > d3


def test_production_and_consumption_are_distinct_invocations():
    contract, world = p04.select_world()
    chain = p04.run_selected_world_progressive_chain(contract, world=world)
    calls = [e["call"] for e in chain.invocation_log]
    assert calls.count("provide_empirical_possibility_slice") == 1
    assert calls.count("compose_positioned_subject_possibility") == 2
    assert calls.count("evaluate_positioned_subject_possibility") == 3
    for step, consumption in zip(chain.steps, chain.f8_consumptions):
        produced = step.produced_evidence.evidence_ref.content_hash
        consumed = (consumption["exact_evidence_ref"] or {}).get("content_hash")
        assert consumed == produced, step.step_id
        assert consumption["result_state"] == "EXACT_SUPPORTED"


def test_chain_without_explicit_world_rebuilds_from_contract():
    contract, _ = p04.select_world()
    chain = p04.run_selected_world_progressive_chain(contract)
    assert len(chain.steps) == 3
    checks = p04.verify_chain_preserves_contract(contract, chain)
    assert checks["oracle_match"] is True


# ==========================================================================
# HOSTILE: unauthorized world substitution
# ==========================================================================
def test_unauthorized_world_substitution_is_refused():
    """A consumer query from a different universe cannot join this contract."""
    contract, world = p04.select_world()
    source = world["source"]
    other = i03._build_source(
        "p04-foreign-world",
        [{"id": f"F{n:03d}",
          "responses": {"A": n % 2, "B": (n // 2) % 2, "C": 1, "Y": n % 2}}
         for n in range(1, 21)],
        question_namespace="p04-foreign-world",
        risk_sets={"R_ALL": {q: {r["id"] for r in
                                  [{"id": f"F{n:03d}",
                                    "responses": {"A": n % 2, "B": (n // 2) % 2,
                                                  "C": 1, "Y": n % 2}}
                                   for n in range(1, 21)]}
                            for q in ("A", "B", "C", "Y")}},
        risk_namespace="p04-foreign-world",
    )
    other["risk_refs"]["R"] = other["risk_refs"]["R_ALL"]
    conds = (("A", 1),)
    predicate = pc._joint_predicate(world, conds)
    producer_query = pc._producer_query(world, predicate)
    foreign_pairing = pc.fx.make_pairing_authority("p04-foreign-world")
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
        query_id="p04-cross-world",
        subject_ref=pc._subject_ref("x", "FOREIGN_SUBJECT")[0],
        target_ref=other["qrefs"]["Y"],
        source_universe_ref=other["universe"].ref,
        release_ref=other["release_ref"],
        bindings=list(foreign_bindings),
        projection_kind="P04_PROGRESSIVE_CONDITIONAL_DISTRIBUTION")
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


def test_contract_verify_bindings_rejects_wrong_universe():
    contract, world = p04.select_world()
    source = world["source"]
    other = i03._build_source(
        "p04-wrong-universe",
        [{"id": f"W{n:03d}",
          "responses": {"A": n % 2, "B": (n // 2) % 2, "C": 1, "Y": n % 2}}
         for n in range(1, 11)],
        question_namespace="p04-wrong-universe",
        risk_sets={"R_ALL": {q: {r["id"] for r in
                                  [{"id": f"W{n:03d}",
                                    "responses": {"A": n % 2, "B": (n // 2) % 2,
                                                  "C": 1, "Y": n % 2}}
                                   for n in range(1, 11)]}
                            for q in ("A", "B", "C", "Y")}},
        risk_namespace="p04-wrong-universe",
    )
    with pytest.raises(p04.P04WorldSubstitutionError):
        contract.verify_bindings(
            source_universe_ref=other["universe"].ref,
            release_ref=source["release_ref"],
            risk_set_ref=source["risk_refs"]["R"],
        )


def test_contract_verify_bindings_rejects_wrong_release():
    contract, world = p04.select_world()
    source = world["source"]
    wrong_release = pc.ExactRef(
        "RELEASE", "urn:test:p04:wrong-release",
        "a" * 64,
    )
    with pytest.raises(p04.P04WorldSubstitutionError):
        contract.verify_bindings(
            source_universe_ref=source["universe"].ref,
            release_ref=wrong_release,
            risk_set_ref=source["risk_refs"]["R"],
        )


def test_contract_verify_bindings_rejects_wrong_risk_set():
    contract, world = p04.select_world()
    source = world["source"]
    wrong_risk = pc.ExactRef(
        "RISK_SET", "urn:test:p04:wrong-risk",
        "b" * 64,
    )
    with pytest.raises(p04.P04WorldSubstitutionError):
        contract.verify_bindings(
            source_universe_ref=source["universe"].ref,
            release_ref=source["release_ref"],
            risk_set_ref=wrong_risk,
        )


# ==========================================================================
# HOSTILE: replay / invalidation
# ==========================================================================
def test_replayed_chain_matches_original():
    """A replayed run produces identical results — deterministic owners."""
    contract, world = p04.select_world()
    chain1 = p04.run_selected_world_progressive_chain(contract, world=world)
    chain2 = p04.run_selected_world_progressive_chain(contract, world=world)
    for s1, s2 in zip(chain1.steps, chain2.steps):
        assert s1.raw_denominator_support == s2.raw_denominator_support
        assert {k: v["raw_numerator_support"] for k, v in s1.cells.items()} == \
               {k: v["raw_numerator_support"] for k, v in s2.cells.items()}
        assert s1.produced_evidence.evidence_ref.content_hash == \
               s2.produced_evidence.evidence_ref.content_hash


def test_changed_selected_context_is_refused():
    """A contract built for one tag cannot run a world built for another."""
    contract, _ = p04.select_world()
    other_world = pc.build_synthetic_world(tag="p04-different-tag")
    with pytest.raises(p04.P04WorldSubstitutionError):
        p04.run_selected_world_progressive_chain(contract, world=other_world)


# ==========================================================================
# HOSTILE: invalid joins (inherited from E03, re-verified under contract)
# ==========================================================================
def test_unordered_conditioner_list_is_refused_under_contract():
    contract, world = p04.select_world()
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


def test_empty_predicate_cannot_fabricate_null_geometry_under_contract():
    contract, world = p04.select_world()
    source = world["source"]
    empty = i03._branch_predicate(source, world["qauth"], members=(),
                                  tag="p04-empty")
    query = i03._query(source, world["qauth"], empty, ("Y",), risk="R",
                       tag="p04-empty-q")
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


def test_own_topic_joint_conditioners_are_refused_under_contract():
    contract, world = p04.select_world()
    with pytest.raises(Exception) as excinfo:
        pc.run_joint_conditioner_step(world, "P_Y_given_A_A",
                                      (("A", 1), ("A", 1)))
    assert "duplicate conditioner binding" in str(excinfo.value)


def test_exact_absence_is_unresolved_not_proxied_under_contract():
    contract, world = p04.select_world()
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
    result = evaluate_positioned_subject_possibility(
        query=pc._consumer_query(world, "P_Y_given_A_B", (("A", 1), ("B", 1))),
        rule=world["model_rule"], evidence=(evidence,))
    assert result.result_state == "UNRESOLVED"
    assert result.exact_reason == "EXACT_POSITIONED_STRATUM_ABSENT"
    assert result.exact_evidence_ref is None


def test_walkback_proxy_is_labelled_never_exact_under_contract():
    contract, world = p04.select_world()
    source = world["source"]
    from rawlsing_next.pre553_empirical_objects import AuthorityRef
    from rawlsing_next.source_backed_positioned_subject_possibility import (
        PositionedSubjectPossibilityModelRule,
        SpecificityWalkbackStep,
    )
    proxy_material = {"role": "P04_FIXTURE_ONLY_WALKBACK_PROXY",
                      "real_proxy": False}
    proxy_auth = AuthorityRef(
        authority_id="urn:test:p04:fixture-proxy",
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
            rationale="P04 fixture-only walkback probe"),),
        positive_proxy_authority_refs=(proxy_auth,))
    step1 = pc.run_single_conditioner_step(world)
    result = evaluate_positioned_subject_possibility(
        query=pc._consumer_query(world, "P_Y_given_A_B", (("A", 1), ("B", 1))),
        rule=rule, evidence=(step1.produced_evidence,))
    assert result.result_state == "EXACT_UNRESOLVED_PROXY_AVAILABLE"
    assert result.exact_reason == "EXACT_POSITIONED_STRATUM_ABSENT"
    assert result.exact_evidence_ref is None
    assert result.proxy is not None


# ==========================================================================
# GOVERNANCE: import surface, fixture posture
# ==========================================================================
def test_module_import_surface_contains_no_forbidden_owner():
    import inspect
    source = inspect.getsource(p04)
    imports = "\n".join(
        line for line in source.splitlines()
        if line.startswith("from ") or line.startswith("import ")
    )
    for token in ("learned_product_lifecycle", "field_forge",
                  "v3_adp", "structural_admission", "m5_runtime", "m6_actor",
                  "learned_world_composition"):
        assert token not in imports


def test_no_raw_sav_dta_and_no_respondent_row_leakage():
    import pathlib
    source = pathlib.Path(p04.__file__).read_text()
    for forbidden in (".sav", ".dta", "pyreadstat"):
        assert forbidden not in source
    rows = pc.synthetic_world_rows()
    assert all(r["id"].startswith("E03-") for r in rows)


def test_synthetic_world_is_58_rows_and_never_real_current():
    rows = pc.synthetic_world_rows()
    assert len(rows) == 58
    contract, _ = p04.select_world()
    assert contract.real_current is False
    assert contract.selection_metadata["real_current"] is False
