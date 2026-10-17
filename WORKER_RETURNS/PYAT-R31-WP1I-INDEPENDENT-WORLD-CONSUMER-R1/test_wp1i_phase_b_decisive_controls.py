"""Executed independent WP1I decisive Phase-B controls (not WP1 author code).

RED tests capture erroneous *successful* comparator calls; pytest PASS there
means the scientific counterexample was reproduced, NOT that WP1 is accepted.
"""
import copy
from fractions import Fraction as F
import pytest
import wp1_world_consumer as w

def test_observed_numbers_and_nonpooling():
    p=w.build_products()
    a=p["world_A"]["value_bearing_sources"]
    b=p["world_B"]["value_bearing_sources"]
    assert [w.fraction_pair(x["world_conditioned_observed"]) for x in a]==[F(4,5),F(2,3)]
    assert [w.fraction_pair(x["world_conditioned_observed"]) for x in b]==[F(2,5),F(1,2)]
    assert p["world_A"]["dependency_readset"]==p["world_B"]["dependency_readset"]
    assert p["comparison"]["joint_delta"] is None

def test_label_only_control_zero(monkeypatch):
    rules=copy.deepcopy(w.RULES)
    rules["WORLD_B"]["multipliers"]=copy.deepcopy(rules["WORLD_A"]["multipliers"])
    monkeypatch.setattr(w,"RULES",rules)
    p=w.build_products()
    assert all(w.fraction_pair(d["world_A_minus_B_observed"])==0 for d in p["comparison"]["deltas"])

def test_red_comparator_accepts_tampered_values_under_original_ref():
    p=w.build_products()
    corrupt=copy.deepcopy(p["world_B"])
    corrupt["value_bearing_sources"][0]["world_conditioned_observed"]=[0,1]
    forged=w.compare(p["world_A"],corrupt)
    assert forged["deltas"][0]["world_A_minus_B_observed"]==[4,5]
    assert forged["world_B_ref"]==p["world_B"]["product_ref"]
    assert p["comparison"]["deltas"][0]["world_A_minus_B_observed"]==[2,5]

def test_red_comparator_accepts_forged_early_clock():
    p=w.build_products()
    corrupt=copy.deepcopy(p["world_B"])
    corrupt["asof"]="2023-01-01"
    assert w.compare(p["world_A"],corrupt)["deltas"][0]["world_A_minus_B_observed"]==[2,5]

def test_red_cached_comparator_accepts_revoke_without_epoch():
    r=w.TestOnlyRegistry(w.sourcefree_inputs())
    ids=r.refs();consumer=w.HistoricalWorldPossibilityConsumer(r)
    a=consumer.consume(ids,"WORLD_A")
    b=consumer.consume(ids,"WORLD_B")
    r.revoke(ids["LAB_SOURCE_BETA"])
    with pytest.raises(w.Refusal,match="SOURCE_REVOKED"):
        consumer.consume(ids,"WORLD_A")
    assert w.compare(a,b)["deltas"][1]["world_A_minus_B_observed"]==[1,6]
