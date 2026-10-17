"""GF1J independent Phase A scientific falsifiers, authored and remote-frozen BEFORE
inspection of GF1H repair. Requires existing GF1G frozen fixture builder, not its oracle
as expected results. Operates on the exact staged GF1H consumer when it exists.

GF1G_COURT = historical R17 court root, with repaired module overlaid AFTER this freeze.
GF1G_ORACLE = original GF1G frozen JSON, used to permit imported native fixture builder.
GF1J_GF1G_TEST = exact GF1G original precommitted suite path.
"""
from __future__ import annotations
import importlib.util
import os
from pathlib import Path
import pytest

GF1G = Path(os.environ["GF1J_GF1G_TEST"]).resolve()
spec = importlib.util.spec_from_file_location("_gf1g_fixture_helpers", GF1G)
assert spec and spec.loader
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)

def consumer(rel):
    return helper.CONS(rel)

def relation(counts, *, risk, denoms=None, typed="SUPPORTED", zero_state="ZERO_SUPPORT"):
    return helper._rebuild(counts=counts, eligible=risk, denoms=denoms,
                           typed=typed, zero_state=zero_state)

def must_refuse(rel):
    output = consumer(rel)
    assert output.get("downstream_value_produced") is False, output
    assert output.get("separation_class") is None, output
    assert output.get("decision_state") not in (
        "PAIR_SUPPORT_SIGNATURE_COMPUTED", "RESPONSE_INPUTS_VALID_EMPTY"), output
    return output

def baseline():
    return {"00":2,"01":0,"10":0,"11":2}

def test_a01_nontrivial_exact_positive_and_minority_count_preservation():
    r=relation(baseline(),risk=4)
    s=consumer(r)
    assert s["separation_class"]=="EXACT_PAIR_SEPARATION"
    assert s["joint_support_total"]==4 and s["downstream_value_produced"] is True

def test_a02_asymmetric_both_conditional_directions_independent_arithmetic():
    r=relation({"00":3,"01":1,"10":2,"11":4},risk=10)
    s=consumer(r)
    assert s["separation_class"]=="NO_PAIR_SEPARATION",s
    assert s["joint_support_total"]==10 and s["downstream_value_produced"] is True
    assert (1,4)!=(1,5)  # P(Y=1|X=0) != P(X=0|Y=1); no inverse transport.

def test_a03_unequal_condition_risk_denominators_preserved():
    r=relation({"00":5,"01":1,"10":2,"11":2},risk=10)
    s=consumer(r)
    assert s["separation_class"]=="NO_PAIR_SEPARATION" and s["joint_support_total"]==10
    native=[v["condition_denominator_support"] for v in r.conditional_count_profile]
    assert native==[6,4]

def test_a04_inconsistent_denominator_must_not_produce_exact():
    must_refuse(relation({"00":1,"11":1},risk=2,denoms={"0":2,"1":1}))

def test_a05_support_exceeds_eligible_must_not_produce_exact():
    must_refuse(relation({"00":1,"11":1},risk=1))

def test_a06_negative_counts_not_coerced_to_positive():
    must_refuse(relation({"00":-1,"01":2,"11":1},risk=2))

@pytest.mark.parametrize("bad",[True,1.0,"1"])
def test_a07_a08_noninteger_bool_float_text_counts_refuse(bad):
    # The self-hash may still be computable; that cannot legitimate nonnative support.
    must_refuse(relation({"00":bad,"11":1},risk=2))

@pytest.mark.parametrize("count,claim",[(0,"OBSERVED_POSITIVE"),(1,"ZERO_SUPPORT")])
def test_a09_a10_cell_state_contradiction_refuse(count,claim):
    r=relation({"00":count,"11":1},risk=2)
    f=dict(r.__dict__);f.pop("content_hash");f.pop("object_id")
    rows=[dict(row) for row in f["conditional_count_profile"]]
    cells=[dict(x) for x in rows[0]["target_counts"]]
    cells[0]["joint_cell_state"]=claim
    rows[0]["target_counts"]=tuple(cells)
    f["conditional_count_profile"]=tuple(rows)
    digest=helper.G.semantic_hash(helper.G._projection(f))
    forged=helper.G.GenericNativePairRelation(
        **f,content_hash=digest,
        object_id=f"urn:rawlsing:gf1:generic-pair-relation:sha256:{digest}")
    must_refuse(forged)

@pytest.mark.parametrize("risk,expected",[
    (0,"UNDETERMINED_NO_ELIGIBLE_RISK"),
    (2,"UNDETERMINED_ZERO_SUPPORT_RISK"),
])
def test_a11_a12_zero_eligible_vs_eligible_zero_observed(risk,expected):
    r=relation({},risk=risk,zero_state="OBSERVED_ZERO_IN_SUPPORTED_RISK_SET")
    s=consumer(r)
    assert s["separation_class"]==expected,s
    assert s["joint_support_total"]==0

@pytest.mark.parametrize("typed",["MISSING_TARGET_STATE","UNRESOLVED_TARGET_STATE","NONRESPONSE"])
def test_a13_a15_blocking_never_valid_empty(typed):
    r=relation({},risk=0,typed=typed)
    s=must_refuse(r)
    assert s["decision_state"]=="PRODUCER_TYPED_STATE_BLOCKING",s

def test_a16_typed_zero_support_is_nonpositive_not_valid_empty():
    r=relation({},risk=0,typed="ZERO_SUPPORT")
    s=consumer(r)
    assert s["downstream_value_produced"] is False,s
    assert s["decision_state"]=="PRODUCER_TYPED_STATE_ZERO_SUPPORT",s
    assert s.get("separation_class")=="UNDETERMINED_ZERO_SUPPORT_RISK",s

def test_a17_supported_empty_response_is_distinct_and_nonpositive():
    r=relation({},risk=0)
    f=dict(r.__dict__);f.pop("content_hash");f.pop("object_id")
    f["conditional_count_profile"]=()
    digest=helper.G.semantic_hash(helper.G._projection(f))
    empty=helper.G.GenericNativePairRelation(
        **f,content_hash=digest,
        object_id=f"urn:rawlsing:gf1:generic-pair-relation:sha256:{digest}")
    s=consumer(empty)
    assert s["decision_state"]=="RESPONSE_INPUTS_VALID_EMPTY",s
    assert s["downstream_value_produced"] is False,s

def test_a18_self_hash_not_independent_source_issuer():
    r=relation(baseline(),risk=4)
    s=consumer(r)
    assert s["production_owner_commit"] is False,s
    assert s["generic_native_semantics_hold"]=="RETAINED",s
    assert s["is_population_evidence_not_actor_fact"] is True,s
