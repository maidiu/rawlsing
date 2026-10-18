"""WG0K direct FULL WG0P3 Python import hostiles, run on a qualified PRE553 host.

This file is a further independently specified reproducible source. It was NOT
executed by WG0K's container because required accepted-owner import closure
was not available. Separate executed EXTRACTED-SEAM court has JUnit/stdout
receipts and is not mislabeled as full-source execution.

Candidate exact blob: e38a392980ef2eda27cb792408aabfca604e9784
"""
import json
import pytest
from dataclasses import replace
from wg0p3_workload import (
    FactCustody, ColdCheckpoint, ColdRestartError, FrontierError, IdentityError,
    validate_frontier, validate_frontier_receipts, WorkloadBuilder,
    independent_oracle_items, build_executable_plan, make_executor, run_plan,
    consumer_effects, execute_positive_conditional, build_positive_conditional_frontier,
)


def original_ops():
    builder = WorkloadBuilder()
    source_items = independent_oracle_items()
    for row in source_items:
        assert builder.add_item(row) == "OK"
    frozen = builder.freeze()
    return builder.enumerate(), frozen, {x.item_id:x for x in source_items}


def receipt(op):
    return {
        "op_id":op.op_id,"op_class":op.op_class,"target":op.target,
        "conditioners":list(op.conditioners),"item_ids":list(op.item_ids),
        "disposition":op.disposition.value,
        "disposition_reason":op.disposition_reason,
    }


def test_positive_25_frozen_count_unchanged():
    ops, _, _ = original_ops()
    assert len(ops)==25
    assert {k:sum(o.disposition.value==k for o in ops) for k in
            ("PRODUCED","HELD","INADMISSIBLE")} == {
            "PRODUCED":3,"HELD":16,"INADMISSIBLE":6}
    validate_frontier(ops)


def test_red_equal_count_held_identity_substitution():
    ops, _, _ = original_ops()
    old=next(x for x in ops if x.disposition.value=="HELD")
    changed=[replace(x,op_id="OP-NOT-IN-FROZEN-ORIGINAL-ITEM-LEDGER")
             if x is old else x for x in ops]
    with pytest.raises(FrontierError):
        validate_frontier(changed)


def test_red_equal_count_changed_reason():
    ops, _, _ = original_ops()
    old=next(x for x in ops if x.disposition.value=="HELD")
    changed=[replace(x,disposition_reason="SIGNED_REAL_ISSUER")
             if x is old else x for x in ops]
    with pytest.raises(FrontierError):
        validate_frontier(changed)


def test_red_circular_expected_ops_cannot_be_source_oracle():
    ops, _, _ = original_ops()
    old=next(x for x in ops if x.disposition.value=="HELD")
    altered=[replace(x,op_id="OP-INVENTED") if x is old else x for x in ops]
    with pytest.raises(FrontierError):
        validate_frontier_receipts(tuple(receipt(x) for x in altered),altered)


def test_red_store_alias_cannot_corrupt_immutable_published_fact():
    custody=FactCustody()
    original={"op_id":"OP-REAL","denominator":6,"cells":[{"n":2}]}
    custody.store("exact-real-fact-ref",original)
    original["cells"][0]["n"]=999
    assert custody.read("exact-real-fact-ref")["cells"][0]["n"]==2


def test_red_read_alias_cannot_corrupt_immutable_published_fact():
    custody=FactCustody()
    custody.store("exact-real-fact-ref",{"denominator":6,"cells":[{"n":2}]})
    read=custody.read("exact-real-fact-ref")
    read["cells"][0]["n"]=999
    assert custody.read("exact-real-fact-ref")["cells"][0]["n"]==2


def test_red_snapshot_alias_cannot_corrupt_immutable_published_fact():
    custody=FactCustody()
    custody.store("exact-real-fact-ref",{"denominator":6,"cells":[{"n":2}]})
    snapshot=custody.snapshot()
    snapshot["facts"]["exact-real-fact-ref"]["cells"][0]["n"]=999
    assert custody.read("exact-real-fact-ref")["cells"][0]["n"]==2


def test_red_key_cannot_be_rebound_to_different_fact():
    custody=FactCustody()
    custody.store("exact-real-fact-ref",{"denominator":6,"cells":[{"n":2}]})
    with pytest.raises(IdentityError):
        custody.store("exact-real-fact-ref",{"denominator":999,"cells":[{"n":2}]})


def test_red_checkpoint_is_not_caller_issued_grant():
    custody=FactCustody()
    custody.store("fact",{"n":2})
    cp=ColdCheckpoint("F",{"U":"COMPLETED"},custody.snapshot(),{"R":"E"},"GRANTED_FIXTURE")
    forged=ColdCheckpoint(cp.plan_freeze_hash,cp.completed_units,cp.fact_custody_snapshot,
                          cp.source_editions,"ISSUED_ORIGINAL_SOURCE_PERMISSION")
    opened=ColdCheckpoint.from_json(forged.to_json())
    assert opened.grant_state=="GRANTED_FIXTURE", "untrusted string was accepted as upgraded permission"


def test_red_cold_checkpoint_contains_full_batch_receipts():
    custody=FactCustody()
    custody.store("fact",{"n":2})
    cp=ColdCheckpoint("F",{"U":"COMPLETED"},custody.snapshot(),{"R":"E"},"GRANTED_FIXTURE")
    assert hasattr(cp,"prior_receipts"), "completed unit name alone cannot replay immutable original UnitExecutionReceipt"


def test_red_positive_conditional_compiles_via_common_builder():
    ops, frozen, items=original_ops()
    assert not any(o.op_class=="CONDITIONAL" and o.disposition.value=="PRODUCED" for o in ops)
    # The author supplied a separate build_positive_conditional_frontier and
    # execute_positive_conditional demonstration. The shared builder has
    # no input for independent qualified joint carrier/risk permission.
    assert hasattr(WorkloadBuilder,"add_joint_risk_authority"), "no ordinary conditional compiler admission API"
