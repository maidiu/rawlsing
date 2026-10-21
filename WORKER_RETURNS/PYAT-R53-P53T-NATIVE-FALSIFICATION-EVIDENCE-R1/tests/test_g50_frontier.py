from __future__ import annotations

from dataclasses import replace

import pytest

from g50.enumerate import enumerate_frontier, role_disposition
from g50.fixture import bundle as stock_bundle, policy as stock_policy
from g50.types import ItemOccurrence, ScientificGrammarPolicy


def occurrence(item_id: str, **overrides):
    values = dict(
        item_id=item_id, label=item_id, unit="adult",
        topology="SCALAR_SINGULAR", forms=("F",), domain=(0, 1),
        target_role=True, conditioner_role=True, route_state="KNOWN",
        semantic_state="UNRESOLVED", scope="SYNTH-W1", administered=True,
    )
    values.update(overrides)
    return ItemOccurrence(**values)


def sample_op(frontier, target, claim_class="DIST"):
    return tuple(
        op for op in frontier.operations
        if op.claim_class == claim_class and op.targets == (target,)
        and op.conditions == () and op.measure == "SAMPLE"
    )


def test_g50_arbitrary_non_reserved_item_ids_raise_keyerror_id():
    base = stock_bundle()
    policy = replace(
        stock_policy(),
        target_roles=("Qa", "Qb", "Qy", "Qm"),
        conditioner_roles=("Qa", "Qb", "Qy", "Qm"),
        denied_roles=(),
    )
    frozen = replace(base, items=tuple(
        occurrence(name) for name in ("Qa", "Qb", "Qy", "Qm")))
    with pytest.raises(KeyError) as caught:
        enumerate_frontier(frozen, policy)
    assert caught.value.args == ("ID",)
    frames = []
    entry = caught.value.__traceback__
    while entry is not None:
        if entry.tb_frame.f_code.co_filename.endswith("enumerate.py"):
            frames.append(entry.tb_lineno)
        entry = entry.tb_next
    assert frames[-2:] == [193, 151]


def test_g50_missing_y_with_id_present_raises_at_second_literal():
    base = stock_bundle()
    items = tuple(item for item in base.items if item.item_id != "Y")
    policy = replace(
        stock_policy(),
        target_roles=("A", "B", "M"),
        conditioner_roles=("A", "B", "M"),
    )
    with pytest.raises(KeyError) as caught:
        enumerate_frontier(replace(base, items=items), policy)
    assert caught.value.args == ("Y",)
    frames = []
    entry = caught.value.__traceback__
    while entry is not None:
        if entry.tb_frame.f_code.co_filename.endswith("enumerate.py"):
            frames.append(entry.tb_lineno)
        entry = entry.tb_next
    assert frames[-2:] == [194, 151]


def test_g50_reserved_padding_masks_but_does_not_repair_arbitrary_names():
    base = stock_bundle()
    filler = tuple(item for item in base.items if item.item_id in {
        "ID", "H", "RT", "X1", "X2", "SET", "RANK", "REP"})
    padding = tuple(
        item for item in base.items if item.item_id in {"A", "B", "Y"}
    )
    padding = tuple(replace(item, target_role=False, conditioner_role=False) for item in padding)
    additions = tuple(occurrence(name) for name in ("Qa", "Qb", "Qy"))
    policy = replace(
        stock_policy(),
        target_roles=("Qa", "Qb", "Qy", "M"),
        conditioner_roles=("Qa", "Qb", "Qy", "M"),
    )
    frontier = enumerate_frontier(
        replace(base, items=filler + padding + additions), policy)
    assert frontier.e_pre_count and frontier.e_pre_count > 0
    assert sample_op(frontier, "Qy")
    assert not sample_op(frontier, "Y")


def test_g50_unadministered_y_is_still_eligible_and_counted():
    base = stock_bundle()
    policy = stock_policy()
    control = enumerate_frontier(base, policy)
    items = tuple(
        replace(item, administered=False) if item.item_id == "Y" else item
        for item in base.items)
    observed = enumerate_frontier(replace(base, items=items), policy)
    eligible = sample_op(observed, "Y")
    assert control.e_pre_count == 432
    assert observed.e_pre_count == 432
    assert [(op.disposition, op.measure, op.unit) for op in eligible] == [
        ("ELIGIBLE", "SAMPLE", "adult")]
    assert sample_op(control, "Y")[0].disposition == "ELIGIBLE"


def test_g50_all_missing_administered_is_indistinguishable_from_unadministered():
    base = stock_bundle()
    policy = stock_policy()
    missing = replace(
        base,
        state_map={"Y": "MISSING"},
        held=("Y_ALL_RESPONSES_MISSING",),
    )
    observed_missing = enumerate_frontier(missing, policy)
    items = tuple(
        replace(item, administered=False) if item.item_id == "Y" else item
        for item in base.items)
    observed_unadministered = enumerate_frontier(replace(base, items=items), policy)
    assert observed_missing.e_pre_count == observed_unadministered.e_pre_count == 432
    assert sample_op(observed_missing, "Y")[0].disposition == "ELIGIBLE"
    assert sample_op(observed_unadministered, "Y")[0].disposition == "ELIGIBLE"
    denied = replace(base, items=tuple(
        replace(item, target_role=False) if item.item_id == "Y" else item
        for item in base.items))
    denied_frontier = enumerate_frontier(denied, policy)
    assert not sample_op(denied_frontier, "Y")
    assert all(op.disposition == "PROHIBITED" for op in denied_frontier.operations
               if op.claim_class == "DIST" and op.targets == ("Y",))


def test_g50_duplicate_item_id_silently_last_wins_and_changes_frontier():
    base = stock_bundle()
    policy = stock_policy()
    control = enumerate_frontier(base, policy)
    first_y = next(item for item in base.items if item.item_id == "Y")
    duplicate = replace(first_y, unit="household", forms=("G",), topology="SCALAR_SINGULAR")
    observed = enumerate_frontier(replace(base, items=base.items + (duplicate,)), policy)
    eligible = sample_op(observed, "Y")
    assert len(eligible) == 1
    assert eligible[0].unit == "household"
    assert control.e_pre_count == 432
    assert observed.e_pre_count == 114
    assert observed.u_item_root != control.u_item_root
    assert observed.u_item_root is not None


def test_g50_y_vs_z_conditioner_lexical_asymmetry_and_absent_policy_field():
    base = stock_bundle()
    z = occurrence("Z")
    policy = replace(
        stock_policy(),
        target_roles=stock_policy().target_roles + ("Z",),
        conditioner_roles=stock_policy().conditioner_roles + ("Z",),
    )
    bundle = replace(base, items=base.items + (z,))
    frontier = enumerate_frontier(bundle, policy)
    y_ops = tuple(
        op for op in frontier.operations
        if op.claim_class == "CONDITIONAL" and op.targets == ("A",)
        and op.conditions == (("Y", 1),))
    z_ops = tuple(
        op for op in frontier.operations
        if op.claim_class == "CONDITIONAL" and op.targets == ("A",)
        and op.conditions == (("Z", 1),))
    assert [(op.disposition, op.reasons) for op in y_ops] == [
        ("PROHIBITED", ("REVERSE_ROLE_RISK_NOT_AUTHORIZED",))]
    assert [(op.disposition, op.reasons) for op in z_ops] == [("ELIGIBLE", ())]
    assert role_disposition(bundle, policy, targets=("A",), conditions=(("Y", 1),)) == (
        "PROHIBITED", ["REVERSE_ROLE_RISK_NOT_AUTHORIZED"])
    assert role_disposition(bundle, policy, targets=("A",), conditions=(("Z", 1),)) == (
        "ELIGIBLE", [])
    assert "reverse_authorized" not in ScientificGrammarPolicy.__dataclass_fields__
    assert not hasattr(policy, "reverse_authorized")
