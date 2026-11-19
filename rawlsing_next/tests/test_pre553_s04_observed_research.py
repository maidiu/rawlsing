"""Actual native I03 -> S04 knowledge BEFORE Field Forge. SOURCEFREE ONLY.

Independent expected XOR arithmetic is fixed directly from the input rows,
not from S04's own output. No new physical C11, FF, or source rights.
"""
from dataclasses import replace
from itertools import product

import pytest

from rawlsing_next.pre553_empirical_objects import EmpiricalFact, ExactRef, canonicalize, semantic_hash
from rawlsing_next.pre553_s04_observed_research import (
    S04KnowledgeError, ask_s04_common_risk_predictor_evidence,
    ask_s04_exact_condition, receive_s04_i03_research,
)
from rawlsing_next.tests import test_pre553_empirical_query as native


def _real(parity=0, *, tag="S04-REAL-XOR", targets=("X", "Y", "Z")):
    rows = [
        {"id": f"R{x}{y}", "responses": {"X": x, "Y": y, "Z": x ^ y ^ parity}}
        for x, y in product((0, 1), repeat=2)
    ]
    source = native._build_source(tag, rows, question_namespace="S04-RESEARCH-QUESTIONS")
    qa = native._query_authority(tag)
    pred = native._branch_predicate(source, qa, tag="all")
    query = native._query(source, qa, pred, targets, tag="query")
    actual = native._run(source, qa, pred, query)
    assert actual.facts[0].typed_state == "SUPPORTED"
    return source, qa, pred, query, actual


def _get(data, key):
    return {row["target_state"]: row["raw_count"] for row in data["complete_target_cells"]}[key]


def test_f4_native_true_three_way_kept_pre_field_forge():
    _, _, _, q, native_result = _real()
    s04 = receive_s04_i03_research(query=q, execution=native_result)
    p = s04.material()
    assert p["target_arity"] == 3
    assert len(p["complete_cells"]) == 8
    assert p["raw_eligible_condition_denominator"] == 4
    assert p["raw_fully_resolved_joint_n"] == 4
    assert p["fact_ref"] == native_result.facts[0].ref.as_dict()
    assert p["native_fact_target_domain_identity"] == native_result.facts[0].target_domain_identity
    assert p["full_query_target_topology"] == canonicalize(q.target_arity_and_topology)
    assert p["source_scope_mode"] == "SINGLE_UNIVERSE"
    assert p["measure_kind"] == "RAW"
    assert p["risk_set_type"] == native_result.facts[0].risk_set_type
    assert p["producer_uncertainty_state"] == native_result.facts[0].uncertainty_method_or_typed_state
    assert p["source_authenticity"].endswith("ORIGINAL_SOURCE_RIGHTS_UNVERIFIED")
    assert "COMPARATIVE_DETERMINICITY_METRIC_NOT_ISSUED" in p["not_issued"]


def test_f1_actual_scalar_native_i03_source_cell_is_accepted():
    _, _, _, q, execution = _real(targets=("X",))
    s04 = receive_s04_i03_research(query=q, execution=execution)
    assert s04.material()["target_arity"] == 1
    marginal = ask_s04_exact_condition(
        knowledge=s04, target_index=0, conditions={},
    ).material()
    assert marginal["raw_conditioned_full_case_n"] == 4
    assert _get(marginal, "0") == 2
    assert _get(marginal, "1") == 2
    assert len(s04.material()["complete_cells"]) == 2


def test_f2_forward_reverse_and_double_conditioned_complete_case_support():
    _, _, _, q, actual = _real()
    knowledge = receive_s04_i03_research(query=q, execution=actual)
    lhs = ask_s04_exact_condition(
        knowledge=knowledge, target_index=2, conditions={0: "0", 1: "0"},
    )
    rhs = ask_s04_exact_condition(
        knowledge=knowledge, target_index=0, conditions={2: "0"},
    )
    assert lhs.ref != rhs.ref
    assert lhs.material()["raw_conditioned_full_case_n"] == 1
    assert _get(lhs.material(), "0") == 1
    assert _get(lhs.material(), "1") == 0
    assert rhs.material()["raw_conditioned_full_case_n"] == 2
    assert lhs.material()["complete_target_cells"][0]["raw_fraction_of_selected_full_cases"] == {
        "$exact_fraction": [1, 1]
    }


def test_f4_three_way_parity_different_despite_all_actual_native_pairs_equal():
    src0, qa0, p0, q0, actual0 = _real(0, tag="S04-REAL-PARITY")
    src1, qa1, p1, q1, actual1 = _real(1, tag="S04-REAL-ANTIPARITY")
    a = receive_s04_i03_research(query=q0, execution=actual0)
    b = receive_s04_i03_research(query=q1, execution=actual1)
    assert a.ref != b.ref
    assert a.material()["complete_cells"] != b.material()["complete_cells"]
    for targets in (("X", "Y"), ("Y", "Z"), ("X", "Z")):
        fa = native._run(
            src0, qa0, p0, native._query(src0, qa0, p0, targets, tag="pairs"),
        ).facts[0]
        fb = native._run(
            src1, qa1, p1, native._query(src1, qa1, p1, targets, tag="pairs"),
        ).facts[0]
        def counts(f):
            return {str(row["cell"]): row["raw_numerator_support"]
                    for row in f.target_topology["complete_cell_semantic_projection"]}
        assert counts(fa) == counts(fb)


def test_common_complete_case_risk_candidate_tables_do_not_rank():
    _, _, _, q, actual = _real()
    knowledge = receive_s04_i03_research(query=q, execution=actual)
    data = ask_s04_common_risk_predictor_evidence(
        knowledge=knowledge, target_index=2, candidate_indices=(1, 0), context={},
    )
    p = data.material()
    assert p["state"] == "COUNTS_AVAILABLE__SCIENTIFIC_METHOD_HELD"
    assert p["common_full_case_n"] == 4
    assert p["ranking"] is None
    assert p["variance_or_population_estimate"] is None
    assert [row["candidate_index"] for row in p["tables"]] == [0, 1]
    assert all(sum(s["raw_conditioned_full_case_n"] for s in t["states"]) == 4
               for t in p["tables"])
    assert data.ref == ask_s04_common_risk_predictor_evidence(
        knowledge=knowledge, target_index=2, candidate_indices=(0, 1), context={},
    ).ref


def test_context_changes_candidate_knowledge_without_faking_importance():
    _, _, _, q, actual = _real()
    knowledge = receive_s04_i03_research(query=q, execution=actual)
    zero = ask_s04_common_risk_predictor_evidence(
        knowledge=knowledge, target_index=2, candidate_indices=(1,), context={0: "0"},
    )
    one = ask_s04_common_risk_predictor_evidence(
        knowledge=knowledge, target_index=2, candidate_indices=(1,), context={0: "1"},
    )
    assert zero.ref != one.ref
    assert zero.material()["common_full_case_n"] == one.material()["common_full_case_n"] == 2
    assert zero.material()["tables"][0]["states"] != one.material()["tables"][0]["states"]
    assert zero.material()["ranking"] is one.material()["ranking"] is None


def test_query_source_risk_current_substitution_refuses():
    _, _, _, q, execution = _real()
    wrong = ExactRef("C11_RELEASE", "urn:test:foreign", semantic_hash("foreign"))
    with pytest.raises(S04KnowledgeError, match="closure"):
        receive_s04_i03_research(
            query=q, execution=replace(execution, release_refs=(wrong,)),
        )
    original = execution.facts[0]
    bad = EmpiricalFact(
        typed_state=original.typed_state,
        authority_snapshot_refs=original.authority_snapshot_refs,
        dependency_refs=original.dependency_refs,
        producer_replay_locator_or_reference_root=original.producer_replay_locator_or_reference_root,
        **{**dict(original.semantic_fields), "risk_set_ref": wrong},
    )
    with pytest.raises(S04KnowledgeError, match="risk"):
        receive_s04_i03_research(
            query=q, execution=replace(execution, facts=(bad,)),
        )


def test_condition_outside_native_domain_is_refused_not_zero():
    _, _, _, q, actual = _real()
    knowledge = receive_s04_i03_research(query=q, execution=actual)
    with pytest.raises(S04KnowledgeError, match="domain"):
        ask_s04_exact_condition(
            knowledge=knowledge, target_index=2, conditions={0: "NONE"},
        )
    with pytest.raises(S04KnowledgeError, match="target leakage"):
        ask_s04_exact_condition(
            knowledge=knowledge, target_index=2, conditions={2: "0"},
        )


def test_low_support_real_counts_cannot_become_valid_scientific_distribution():
    _, _, _, q, actual = _real()
    fact = actual.facts[0]
    low = EmpiricalFact(
        typed_state="LOW_SUPPORT",
        authority_snapshot_refs=fact.authority_snapshot_refs,
        dependency_refs=fact.dependency_refs,
        producer_replay_locator_or_reference_root=fact.producer_replay_locator_or_reference_root,
        **dict(fact.semantic_fields),
    )
    knowledge = receive_s04_i03_research(
        query=q, execution=replace(actual, facts=(low,)),
    )
    m = knowledge.material()
    assert m["state"] == "PRODUCER_TYPED_HELD"
    assert m["raw_fully_resolved_joint_n"] == 4
    assert m["complete_cells"] == []
    assert m["nonpositive_positive_count_retained_not_served"] == 4
    assert ask_s04_exact_condition(
        knowledge=knowledge, target_index=2, conditions={0: "0"},
    ).material()["state"] == "UPSTREAM_SCIENCE_OR_SOURCE_HELD"


def test_native_positive_source_full_cells_cannot_be_truncated():
    _, _, _, q, actual = _real()
    fact = actual.facts[0]
    topo = dict(fact.target_topology)
    topo["complete_cell_semantic_projection"] = list(topo["complete_cell_semantic_projection"])[:-1]
    changed = EmpiricalFact(
        typed_state=fact.typed_state,
        authority_snapshot_refs=fact.authority_snapshot_refs,
        dependency_refs=fact.dependency_refs,
        producer_replay_locator_or_reference_root=fact.producer_replay_locator_or_reference_root,
        **{**dict(fact.semantic_fields), "target_topology": topo},
    )
    with pytest.raises(S04KnowledgeError, match="incomplete"):
        receive_s04_i03_research(
            query=q, execution=replace(actual, facts=(changed,)),
        )
