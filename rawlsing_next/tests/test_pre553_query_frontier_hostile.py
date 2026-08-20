"""Wave-03 R12 hostile exact-query frontier oracles against accepted I01-I03."""
from __future__ import annotations

from rawlsing_next.pre553_empirical_objects import canonical_json
from rawlsing_next.tests.pre553_query_frontier_fixtures import (
    FIXTURE_INVENTORY, FIXTURE_ORACLES, _cell_map, _ids_from_fact, _rate,
    k_way_bounded_joint_fixture, multi_universe_noncomparable_fixture,
    observed_zero_zero_support_fixture, raw_weighted_divergence_fixture,
    response_position_fixture, response_response_cotravel_fixture,
    routing_risk_asymmetry_fixture, same_marginals_different_joint_fixture,
    simpson_reversal_fixture, source_indexed_disagreement_fixture,
    special_state_fixture, topology_fixture, xor_zero_unary_fixture,
)


def _row_for_cell(fact, cell):
    key = canonical_json(cell)
    rows = fact.target_topology["complete_cell_semantic_projection"]
    matches = [row for row in rows if canonical_json(row["cell"]) == key]
    assert len(matches) == 1, (cell, rows)
    return matches[0]


def test_fixture_inventory_covers_the_binding_hostile_frontier():
    required = {
        "XOR", "ZERO_UNARY_SIGNAL", "SIMPSON_REVERSAL", "SAME_MARGINALS_DIFFERENT_JOINT",
        "RESPONSE_X_POSITION", "SAME_RESPONDENT_COTRAVEL", "DENOMINATOR_ASYMMETRY",
        "AUTHORIZED_WEIGHTED", "OBSERVED_ZERO", "ZERO_SUPPORT", "MISSING", "DK", "REFUSAL",
        "IAP", "NOT_ASKED", "SOURCE_DISAGREEMENT", "NONCOMPARABLE", "ORDERED_SEQUENCE",
        "RANKED_RESPONSE", "REPEATED_EVENT", "K_WAY",
    }
    covered = {tag for oracle in FIXTURE_ORACLES.values() for tag in oracle.frontier}
    assert required <= covered
    assert len(FIXTURE_INVENTORY) == len(set(FIXTURE_INVENTORY)) == len(FIXTURE_ORACLES)
    for oracle in FIXTURE_ORACLES.values():
        assert oracle.expected
        assert oracle.loss_signature


def test_xor_parity_has_zero_unary_signal_but_exact_same_respondent_joint():
    oracle = FIXTURE_ORACLES["XOR_ZERO_UNARY"].expected
    _, _, facts, xor_fact, joint = xor_zero_unary_fixture()
    assert _rate(facts["X0"]) == oracle["X0_Z1"]
    assert _rate(facts["X1"]) == oracle["X1_Z1"]
    assert _rate(facts["Y0"]) == oracle["Y0_Z1"]
    assert _rate(facts["Y1"]) == oracle["Y1_Z1"]
    assert _rate(xor_fact) == oracle["XOR_Z1"]
    cells = _cell_map(joint)
    assert joint.raw_denominator_support == oracle["JOINT_DENOMINATOR"]
    for cell, count in oracle["JOINT_SUPPORTED"].items():
        assert cells[cell]["raw_numerator_support"] == count
        assert cells[cell]["cell_state"] == "OBSERVED_POSITIVE"
    for cell in oracle["JOINT_ZERO"]:
        assert cells[cell]["raw_numerator_support"] == 0
        assert cells[cell]["cell_state"] == "OBSERVED_ZERO_IN_SUPPORTED_RISK_SET"


def test_simpson_reversal_keeps_pooled_and_stratified_queries_distinct():
    oracle = FIXTURE_ORACLES["SIMPSON_REVERSAL"].expected
    _, facts = simpson_reversal_fixture()
    assert _rate(facts[(1, None)]) == oracle["pooled_X1"]
    assert _rate(facts[(0, None)]) == oracle["pooled_X0"]
    assert _rate(facts[(1, "A")]) == oracle["A_X1"]
    assert _rate(facts[(0, "A")]) == oracle["A_X0"]
    assert _rate(facts[(1, "B")]) == oracle["B_X1"]
    assert _rate(facts[(0, "B")]) == oracle["B_X0"]
    assert facts[(1, None)].ref != facts[(1, "A")].ref != facts[(1, "B")].ref
    assert 5 * 12 < 8 * 13
    assert 3 * 10 > 8 * 3
    assert 2 * 2 > 0 * 10


def test_same_marginals_different_joint_remain_distinct_exact_source_facts():
    oracle = FIXTURE_ORACLES["SAME_MARGINALS_DIFFERENT_JOINT"].expected
    _, _, left, right = same_marginals_different_joint_fixture()
    lc, rc = _cell_map(left), _cell_map(right)
    assert left.raw_denominator_support == right.raw_denominator_support == oracle["denominator"]
    for cell, count in oracle["left"].items(): assert lc[cell]["raw_numerator_support"] == count
    for cell, count in oracle["right"].items(): assert rc[cell]["raw_numerator_support"] == count
    assert sum(lc[cell]["raw_numerator_support"] for cell in (("0", "0"), ("0", "1"))) == oracle["marginal_X0"]
    assert sum(rc[cell]["raw_numerator_support"] for cell in (("0", "0"), ("0", "1"))) == oracle["marginal_X0"]
    assert sum(lc[cell]["raw_numerator_support"] for cell in (("0", "0"), ("1", "0"))) == oracle["marginal_Y0"]
    assert sum(rc[cell]["raw_numerator_support"] for cell in (("0", "0"), ("1", "0"))) == oracle["marginal_Y0"]
    assert left.ref != right.ref


def test_response_x_empirical_position_conjunction_uses_one_scoped_respondent():
    oracle = FIXTURE_ORACLES["RESPONSE_POSITION_CONJUNCTION"].expected
    source, fact = response_position_fixture()
    assert fact.raw_denominator_support == oracle["denominator"]
    assert _cell_map(fact)["1"]["raw_numerator_support"] == oracle["Y1"]
    assert _ids_from_fact(fact, source) == oracle["member_ids"]


def test_response_response_cotravel_is_exact_same_respondent_incidence():
    oracle = FIXTURE_ORACLES["RESPONSE_RESPONSE_COTRAVEL"].expected
    source, fact = response_response_cotravel_fixture()
    cells = _cell_map(fact)
    assert fact.raw_denominator_support == oracle["denominator"]
    assert cells["1"]["raw_numerator_support"] == oracle["Y1"]
    assert cells["0"]["raw_numerator_support"] == oracle["Y0"]
    assert _ids_from_fact(fact, source) == oracle["member_ids"]


def test_routing_risk_set_asymmetry_uses_exact_common_member_identity():
    oracle = FIXTURE_ORACLES["ROUTING_RISK_ASYMMETRY"].expected
    source, xfact, yfact, joint = routing_risk_asymmetry_fixture()
    assert xfact.raw_denominator_support == oracle["X_denominator"]
    assert yfact.raw_denominator_support == oracle["Y_denominator"]
    assert joint.raw_denominator_support == oracle["joint_denominator"]
    assert _ids_from_fact(joint, source) == oracle["joint_member_ids"]
    assert xfact.denominator_member_refs != yfact.denominator_member_refs
    assert xfact.ref != yfact.ref != joint.ref


def test_raw_and_authorized_weighted_measure_diverge_without_identity_collapse():
    oracle = FIXTURE_ORACLES["RAW_WEIGHTED_DIVERGENCE"].expected
    _, raw, weighted = raw_weighted_divergence_fixture()
    assert raw.raw_denominator_support == oracle["raw_denominator"]
    assert _cell_map(raw)["1"]["raw_numerator_support"] == oracle["raw_Y1"]
    assert weighted.weighted_denominator_support_if_authorized == oracle["weighted_denominator"]
    assert _cell_map(weighted)["1"]["weighted_numerator_support_if_authorized"] == oracle["weighted_Y1"]
    assert raw.measure_kind == "RAW" and weighted.measure_kind == "GOVERNED_WEIGHTED"
    assert raw.ref != weighted.ref


def test_observed_zero_is_not_zero_support():
    oracle = FIXTURE_ORACLES["OBSERVED_ZERO_VS_ZERO_SUPPORT"].expected
    observed, zero_support = observed_zero_zero_support_fixture()
    assert observed.typed_state == oracle["observed_state"]
    assert observed.raw_denominator_support == oracle["observed_denominator"]
    assert _cell_map(observed)["1"]["cell_state"] == oracle["Y1_cell_state"]
    assert zero_support.typed_state == oracle["zero_support_state"]
    assert zero_support.raw_denominator_support == oracle["zero_support_denominator"]
    assert observed.ref != zero_support.ref


def test_missing_dk_refusal_iap_not_asked_remain_typed_and_noncollapsed():
    oracle = FIXTURE_ORACLES["SPECIAL_STATE_NONCOLLAPSE"].expected
    _, fact, event_states, routing_states = special_state_fixture()
    assert fact.typed_state == "SUPPORTED"
    assert fact.raw_denominator_support == oracle["eligible_denominator"]
    assert event_states == oracle["carrier_states"]
    assert routing_states == oracle["routing_states"]
    assert _row_for_cell(fact, "1")["raw_numerator_support"] == oracle["eligible_cells"]["1"]
    for state in ("MISSING", "DK", "REFUSAL", "IAP", "NOT_ASKED"):
        row = _row_for_cell(fact, {"typed_response_state": state})
        assert row["raw_numerator_support"] == oracle["eligible_cells"][state]
    assert _row_for_cell(fact, {"typed_response_state": "IAP"})["cell_state"] == "OBSERVED_ZERO_IN_SUPPORTED_RISK_SET"
    assert _row_for_cell(fact, {"typed_response_state": "NOT_ASKED"})["cell_state"] == "OBSERVED_ZERO_IN_SUPPORTED_RISK_SET"


def test_source_indexed_disagreement_stays_two_exact_facts():
    oracle = FIXTURE_ORACLES["SOURCE_INDEXED_DISAGREEMENT"].expected
    _, _, left, right = source_indexed_disagreement_fixture()
    lc, rc = _cell_map(left), _cell_map(right)
    assert left.raw_denominator_support == oracle["left"]["denominator"]
    assert lc["1"]["raw_numerator_support"] == oracle["left"]["Y1"]
    assert lc["0"]["raw_numerator_support"] == oracle["left"]["Y0"]
    assert right.raw_denominator_support == oracle["right"]["denominator"]
    assert rc["1"]["raw_numerator_support"] == oracle["right"]["Y1"]
    assert rc["0"]["raw_numerator_support"] == oracle["right"]["Y0"]
    assert left.ref != right.ref


def test_multi_universe_composite_without_authority_is_typed_noncomparable():
    oracle = FIXTURE_ORACLES["MULTI_UNIVERSE_NONCOMPARABLE"].expected
    fact = multi_universe_noncomparable_fixture()
    assert fact.typed_state == oracle["typed_state"]
    assert fact.p02_failure_state == oracle["p02_failure_state"]
    assert fact.raw_denominator_support == oracle["raw_denominator"]


def test_ordered_ranked_and_repeated_topologies_preserve_exact_information():
    oracle = FIXTURE_ORACLES["ORDERED_RANKED_MULTIPLICITY"].expected
    _, facts = topology_fixture()
    assert facts["ordered"].raw_denominator_support == 1
    assert _row_for_cell(facts["ordered"], oracle["ordered"])["raw_numerator_support"] == 1
    assert _row_for_cell(facts["ranked"], oracle["ranked"])["raw_numerator_support"] == 1
    assert _row_for_cell(facts["repeated"], oracle["repeated"])["raw_numerator_support"] == 1
    assert facts["ordered"].ref != facts["ranked"].ref != facts["repeated"].ref


def test_four_way_bounded_joint_retains_higher_order_parity_frontier():
    oracle = FIXTURE_ORACLES["K_WAY_BOUNDED_JOINT"].expected
    _, fact = k_way_bounded_joint_fixture()
    cells = fact.target_topology["complete_cell_semantic_projection"]
    assert fact.target_topology["arity"] == oracle["arity"]
    assert fact.raw_denominator_support == oracle["denominator"]
    assert len(cells) == oracle["domain_cells"]
    supported = [row for row in cells if row["raw_numerator_support"] > 0]
    zero = [row for row in cells if row["raw_numerator_support"] == 0]
    assert len(supported) == oracle["supported_cells"]
    assert len(zero) == oracle["zero_cells"]
    for row in cells:
        a, b, c, y = map(int, row["cell"])
        expected = a ^ b ^ c
        assert row["raw_numerator_support"] == (1 if y == expected else 0)
        assert row["cell_state"] == ("OBSERVED_POSITIVE" if y == expected else "OBSERVED_ZERO_IN_SUPPORTED_RISK_SET")
