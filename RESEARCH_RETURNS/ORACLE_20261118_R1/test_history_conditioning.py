from fractions import Fraction as F
from graphlib import CycleError
import pytest
from history_conditioning import Alternative, ConditionedHistories, PopulationConstraint, constrained_world_range


def test_household_risk_is_a_ratio_of_totals_and_witness_is_whole():
    # One eligible resident in A and three in B. Equal household weights
    # would give only one in four eligible residents with the target response.
    source = PopulationConstraint("synthetic-risk", F(1, 2), ((1, 1), (0, 3)))
    lo, hi = constrained_world_range([source], (1, 0), basis_budget=3)
    assert lo == hi == (F(3, 4), (F(3, 4), F(1, 4)))


def test_missing_risk_and_limited_compute_are_not_evidence_of_infeasibility():
    source = PopulationConstraint("synthetic-risk", F(1), ((0, 0), (1, 1)))
    with pytest.raises(ValueError, match="risk can vanish"):
        constrained_world_range([source], (0, 1), basis_budget=2)
    with pytest.raises(ValueError, match="budget"):
        constrained_world_range([source], (0, 1), basis_budget=1)


def test_shared_suffix_accumulates_every_prefix_and_cannot_fabricate_a_cell():
    a = Alternative
    graph = {"s": (a("x", F(1, 2)), a("y", F(1, 2))),
             "x": (a("z", F(1)),), "y": (a("z", F(1, 2)), a("w", F(1, 2)))}
    observed = {"z": ("a",), "w": ("b",)}
    law = ConditionedHistories("s", graph, observed, {("a",): F(1, 2), ("b",): F(1, 2)})
    assert law.routes["s"] == (a("x", F(1, 3)), a("y", F(2, 3)))
    with pytest.raises(ValueError, match="unreachable"):
        ConditionedHistories("s", graph, observed, {("c",): F(1), ("a",): F(0), ("b",): F(0)})
    with pytest.raises(CycleError):
        ConditionedHistories("s", {"s": (a("s", F(1)),)}, {}, {("a",): F(1)})


def test_fitting_source_may_change_initial_worlds_but_cannot_rig_a_later_actor():
    from history_conditioning import free_action_range
    # Distinct exact rates under the same free-running forward measurement.
    kernel = {"a": {"yes": F(1, 2), "no": F(1, 2)}, "b": {"yes": F(0), "no": F(1)}}
    outcome = {"a": 1, "b": 0}
    lo, hi = free_action_range(kernel, {"yes": F(1, 4), "no": F(3, 4)}, outcome, basis_budget=4)
    assert lo == hi == (F(1, 2), (F(1, 2), F(1, 2)))
    with pytest.raises(ValueError, match="incompatible"):
        free_action_range(kernel, {"yes": F(3, 4), "no": F(1, 4)}, outcome, basis_budget=4)
