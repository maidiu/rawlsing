"""PYAT WG0 -- Tests for source-free generic workload builder.

Tests two heterogeneous native item kinds, no-drop oracle, deterministic
sharding, resume, frontier freeze, and hostile cases.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from wg0_workload_builder import (
    WorkloadBuilder, NativeItem, OperationCandidate, Disposition,
    ResponseKind, make_invented_items,
)


def test_two_heterogeneous_items():
    builder = WorkloadBuilder()
    for item in make_invented_items():
        assert builder.add_item(item) == "OK"
    assert len(builder.manifest.items) == 2
    kinds = {i.response_kind for i in builder.manifest.items}
    assert ResponseKind.ORDINAL in kinds
    assert ResponseKind.HOUSEHOLD in kinds


def test_original_response_options_preserved():
    builder = WorkloadBuilder()
    for item in make_invented_items():
        builder.add_item(item)
    ordinal = builder.manifest.items[0]
    assert ordinal.options == ("0", "1", "2", "3", "9")
    assert ordinal.missing_codes == ("9", "997", "998")
    household = builder.manifest.items[1]
    assert household.unit == "household"


def test_operation_enumeration():
    builder = WorkloadBuilder()
    for item in make_invented_items():
        builder.add_item(item)
    ops = builder.enumerate_operations(["MARGINAL_DISTRIBUTION", "CONDITIONAL_DISTRIBUTION"])
    assert len(ops) > 0
    marginal_ops = [o for o in ops if o.op_class == "MARGINAL_DISTRIBUTION"]
    assert len(marginal_ops) == 2
    conditional_ops = [o for o in ops if o.op_class == "CONDITIONAL_DISTRIBUTION"]
    assert len(conditional_ops) == 0
    assert all(set(o.item_ids) and all(
        builder.manifest.items[[i.item_id for i in builder.manifest.items].index(x)].unit ==
        builder.manifest.items[[i.item_id for i in builder.manifest.items].index(o.item_ids[0])].unit
        for x in o.item_ids
    ) for o in conditional_ops)


def test_no_drop_oracle():
    builder = WorkloadBuilder()
    for item in make_invented_items():
        builder.add_item(item)
    for op in builder.enumerate_operations(["MARGINAL_DISTRIBUTION", "CONDITIONAL_DISTRIBUTION"]):
        builder.add_operation(op)
    builder.disposition_all()
    oracle = builder.no_drop_oracle()
    assert oracle["no_drop"] is True
    assert oracle["missing_items"] == []
    assert oracle["missing_operations"] == []


def test_frontier_freeze():
    builder = WorkloadBuilder()
    for item in make_invented_items():
        builder.add_item(item)
    h = builder.manifest.freeze()
    assert builder.manifest.frontier_frozen is True
    assert h != ""
    assert builder.add_item(NativeItem(
        item_id="ITEM-X", source_id="S", wave="W", response_kind=ResponseKind.ORDINAL,
        options=("0",), missing_codes=(), route_condition=None, unit="respondent",
        version="v1", population="p"
    )) == "FRONTIER_FROZEN"


def test_deterministic_sharding():
    builder = WorkloadBuilder()
    for item in make_invented_items():
        builder.add_item(item)
    for op in builder.enumerate_operations(["MARGINAL_DISTRIBUTION"]):
        builder.add_operation(op)
    s1 = builder.shard(2)
    s2 = builder.shard(2)
    assert s1 == s2
    all_ids = [x for shard in s1 for x in shard]
    assert len(all_ids) == len(set(all_ids))


def test_resume():
    builder = WorkloadBuilder()
    for item in make_invented_items():
        builder.add_item(item)
    for op in builder.enumerate_operations(["MARGINAL_DISTRIBUTION"]):
        builder.add_operation(op)
    completed = {"OP-ITEM-ORDINAL-001-MARGINAL"}
    remaining = builder.resume(completed)
    assert "OP-ITEM-ORDINAL-001-MARGINAL" not in remaining
    assert "OP-ITEM-HOUSEHOLD-MR-002-MARGINAL" in remaining


def test_duplicate_item_rejected():
    builder = WorkloadBuilder()
    item = make_invented_items()[0]
    assert builder.add_item(item) == "OK"
    assert builder.add_item(item) == "DUPLICATE_ITEM_ID"


def test_missing_route_distinction():
    builder = WorkloadBuilder()
    item_routed = NativeItem(
        item_id="ITEM-ROUTED", source_id="S", wave="W",
        response_kind=ResponseKind.ROUTED,
        options=("yes", "no"), missing_codes=("9",),
        route_condition="if_q1 == 1", unit="respondent",
        version="v1", population="p",
    )
    item_skipped = NativeItem(
        item_id="ITEM-SKIPPED", source_id="S", wave="W",
        response_kind=ResponseKind.ROUTED,
        options=("yes", "no"), missing_codes=("9",),
        route_condition="  ", unit="respondent",
        version="v1", population="p",
    )
    builder.add_item(item_routed)
    builder.add_item(item_skipped)
    builder.disposition_all()
    assert builder.manifest.dispositions["ITEM-ROUTED"] == Disposition.PRODUCED
    assert builder.manifest.dispositions["ITEM-SKIPPED"] == Disposition.NOT_APPLICABLE


def test_zero_null_minority_preserved():
    builder = WorkloadBuilder()
    item = NativeItem(
        item_id="ITEM-ZERO", source_id="S", wave="W",
        response_kind=ResponseKind.ORDINAL,
        options=("0", "1"), missing_codes=("9",),
        route_condition=None, unit="respondent",
        version="v1", population="p",
    )
    builder.add_item(item)
    ops = builder.enumerate_operations(["MARGINAL_DISTRIBUTION"])
    for op in ops:
        builder.add_operation(op)
    builder.disposition_all()
    assert builder.manifest.dispositions["ITEM-ZERO"] == Disposition.PRODUCED


def test_source_custody_hold_declared():
    items = make_invented_items()
    assert all(i.source_id.startswith("FIXTURE-SRC") for i in items)
