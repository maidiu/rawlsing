"""P41 structural-versus-empirical separation: rule revision changes routes
with fixed computed empirical evidence; learned-update changes empirical
evidence with fixed world rules."""
from __future__ import annotations

from fixture import prepare
from p41_service import P41Service


def cell_map(step):
    return {cell["cell"]: cell["raw_numerator_support"] for cell in step["cells"]}


def test_rule_revision_changes_routes_not_empirical():
    service = P41Service()
    base = service.progressive()
    assert base["structural"]["routes"]["training"] == "ELIGIBLE"
    assert base["structural"]["routes"]["exit_constraint"] == "WITHIN_MODELED_BUDGET"
    service.publish_rule_revision(
        "training_fee", 6, effective_from="2027-01-01",
        effective_to="2028-01-01", publication="2027-06-01", revision=2)
    service.publish_rule_revision(
        "exit_cost", 8, effective_from="2027-01-01",
        effective_to="2028-01-01", publication="2027-06-01", revision=2)
    late_snapshot = service.current_clock_snapshot("2027-09-01", "2027-09-01")
    revised = service.progressive(snapshot=late_snapshot)
    assert revised["structural"]["routes"]["training"] == "BLOCKED_BY_MODELED_RULE"
    assert revised["structural"]["routes"]["exit_constraint"] == "RESOURCE_CONSTRAINED"
    assert revised["structural"]["routes"]["civil"] == "ELIGIBLE"
    assert revised["n9_world"]["rules"]["training_fee"]["value"] == 6
    assert revised["n9_world"]["rules"]["training_fee"]["publication"] == "2027-06-01"
    assert revised["n9_world"]["rules"]["training_fee"]["revision"] == 2
    assert [step["denominator"] for step in revised["n10e_steps"]] == [32, 16, 8]
    assert [cell_map(step) for step in revised["n10e_steps"]] == \
        [cell_map(step) for step in base["n10e_steps"]]


def test_learned_empirical_update_with_fixed_world_rules():
    base = P41Service()
    changed = P41Service(prepare(same_marginals=True))
    base_receipt = base.progressive()
    changed_receipt = changed.progressive()
    assert [cell_map(step) for step in changed_receipt["n10e_steps"]] == \
        [{"0": 13, "1": 19}, {"0": 5, "1": 11}, {"0": 1, "1": 7}]
    assert [cell_map(step) for step in changed_receipt["n10e_steps"]] != \
        [cell_map(step) for step in base_receipt["n10e_steps"]]
    assert changed_receipt["structural"]["routes"] == \
        base_receipt["structural"]["routes"]
    assert changed_receipt["query"]["query_identity_hash"] == \
        base_receipt["query"]["query_identity_hash"]


def test_empty_world_part_is_explicit_not_substituted():
    receipt = P41Service().progressive(world_part=False)
    assert receipt["structural"] is None
    assert [step["denominator"] for step in receipt["n10e_steps"]] == [32, 16, 8]
