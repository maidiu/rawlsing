"""Phase A tests were devised and committed before WP1 source/outputs were opened."""
import copy
from fractions import Fraction
import pytest
from wp1i_independent_oracle import *
@pytest.fixture
def o():return load()
def refuse(code,f):
    with pytest.raises(ScienceRefusal) as e:f()
    assert e.value.code==code

@pytest.mark.parametrize("given,target,want",[
 ("X1","Y1","9/20"),("Y1","X1","3/5"),("X0","Y1","1/5"),("Y0","X1","11/35")])
def test_A_conditional_exact(o,given,target,want):
    assert directional(o["sample_A"]["two_by_two"],given,target)==Fraction(want)
def test_A_denominators(o):
    t=o["sample_A"]["two_by_two"]
    assert sum(t.values())==100 and t["X1_Y1"]+t["X1_Y0"]==40 and t["X1_Y1"]+t["X0_Y1"]==30
    assert directional(t,"X1","Y1")!=directional(t,"Y1","X1")
def test_B_independent_universe(o):
    t=o["sample_B"]["two_by_two"]
    assert sum(t.values())==40 and directional(t,"X1","Y1")==Fraction(1,4)
    assert directional(t,"Y1","X1")==Fraction(1,6)
    assert directional(t,"X1","Y1")!=directional(o["sample_A"]["two_by_two"],"X1","Y1")
@pytest.mark.parametrize("i,status,val",[
 (0,"OBSERVED_ZERO",Fraction(0)),(1,"UNSUPPORTED",None),
 (2,"PARTIAL_IDENTIFICATION",(Fraction(9,25),Fraction(14,25))),(3,"SUPPRESSED",None)])
def test_four_evidence_states(o,i,status,val):
    x=o["support_cases"][i]
    assert support(x["positive"],x["negative"],x["missing"],x["suppressed"])==(status,val)
def test_minority_not_overwritten(o):
    x=o["minority_case"];assert Fraction(x["event_within_minority"],x["minority_n"])==Fraction(1,4)
    assert Fraction(x["event_within_minority"],x["eligible_n"])!=Fraction(1,4)
def test_nonpooling(o):
    x=separated_source(o["sample_A"],o["sample_B"],o["cross_source_relation"]["valid_kind"])
    assert x["combined_denominator"] is None and x["joint_distribution"] is None and not x["respondent_matching"]
def test_cross_source_join_refusal(o):
    refuse("CROSS_SURVEY_POOLING",lambda:separated_source(o["sample_A"],o["sample_B"],"JOINED_RESPONDENTS"))
def test_F6_A_complete(o):
    x=o["F6"]["WorldA"];assert support(x["positive"],x["negative"],x["missing"])==("COMPLETE",Fraction(3,10))
def test_F6_B_partial(o):
    x=o["F6"]["WorldB"]
    assert support(x["positive"],x["negative"],x["missing"])==("PARTIAL_IDENTIFICATION",(Fraction(9,50),Fraction(2,5)))
    assert Fraction(x["positive"],x["positive"]+x["negative"])!=Fraction(9,50)
def test_F6_no_renormalizing_missing(o):
    x=o["F6"]["WorldB"];a,b=support(x["positive"],x["negative"],x["missing"])[1]
    assert a<=Fraction(18,78)<=b and (a,b)==(Fraction(18,100),Fraction(40,100))
def test_world_rule_changes_opportunity(o):
    result=compare_worlds(o["worlds"]["A"],o["worlds"]["B"])
    assert result["substantive_effect"] and result["changed_action_set"]==("reach_clinic",)
def test_label_only_not_an_effect(o):
    result=compare_worlds(o["worlds"]["A"],o["worlds"]["A_label_only_changed"])
    assert result["substantive_effect"] is False and not result["changed_action_set"]
def test_unchanged_control(o):
    assert not compare_worlds(o["worlds"]["A"],o["worlds"]["A_unchanged"])["substantive_effect"]
def test_absent_rule_hold(o):
    refuse("NO_QUALIFIED_WORLD_RULE",lambda:actions(o["worlds"]["A"],policy_present=False))
def test_prepublication_refused(o):
    x=o["publication_clock"]
    refuse("SOURCE_NOT_YET_PUBLISHED",lambda:publication_asof(as_of=x["invalid_before_publication"],observed=x["observed_at"],release=x["release_at"],world_time=x["observed_at"],epoch="e1",required_epoch="e1"))
def test_future_world_refused(o):
    x=o["publication_clock"]
    refuse("FUTURE_SELECTED_WORLD",lambda:publication_asof(as_of=x["valid_asof"],observed=x["observed_at"],release=x["release_at"],world_time=x["invalid_future_world_asof"],epoch="e1",required_epoch="e1"))
def test_stale_epoch_refused(o):
    x=o["publication_clock"]
    refuse("STALE_EPOCH",lambda:publication_asof(as_of=x["valid_asof"],observed=x["observed_at"],release=x["release_at"],world_time=x["observed_at"],epoch="stale",required_epoch="e1"))
def test_valid_asof(o):
    x=o["publication_clock"]
    assert publication_asof(as_of=x["valid_asof"],observed=x["observed_at"],release=x["release_at"],world_time=x["observed_at"],epoch="e1",required_epoch="e1")
def test_admit_spoof():
    refuse("CALLER_ADMIT_FORGERY",lambda:authority_gate({"issuer":"SOURCEFREE_UNISSUED","origin":"INDEPENDENT_SYNTHETIC_TEST_ONLY"},caller_admit=True))
def test_issuer_spoof():
    refuse("ISSUER_FORGERY",lambda:authority_gate({"issuer":"ACCEPTED","origin":"INDEPENDENT_SYNTHETIC_TEST_ONLY"}))
def test_source_spoof():
    refuse("SOURCE_IDENTITY_FORGERY",lambda:authority_gate({"issuer":"SOURCEFREE_UNISSUED","origin":"CLAIMED_REAL_SURVEY"}))
@pytest.mark.parametrize("flag",("person_requested","model_requested"))
def test_actor_model_boundary(flag):
    refuse("ACTOR_OR_MODEL_PROMOTION",lambda:authority_gate({"issuer":"SOURCEFREE_UNISSUED","origin":"INDEPENDENT_SYNTHETIC_TEST_ONLY"},**{flag:True}))
def test_other_source_unchanged_by_source_mutation(o):
    a=copy.deepcopy(o["sample_A"]);b=copy.deepcopy(o["sample_B"]);digest=hash_obj(b)
    a["two_by_two"]["X1_Y1"]+=1;a["two_by_two"]["X1_Y0"]-=1
    assert hash_obj(a)!=hash_obj(o["sample_A"]) and hash_obj(b)==digest
def test_cold_deterministic_frozen_content(o):
    assert o==load() and hash_obj(o)==hash_obj(load())
