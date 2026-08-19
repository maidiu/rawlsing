#!/usr/bin/env python3
"""D13B hostile fixtures F14-F26, extending part 1."""
from hostile_fixtures_part1 import *
#14 conflicting scalar duplicate
s=ds([resp("r1")],[ev("r1","Q","A",event_id="dup1"),ev("r1","Q","B",event_id="dup2",idx=2)],[elig("r1","Q")],[qspec("DUP",TRUE,"Q",{"type":"ELIGIBLE_FOR","questions":["Q"]})])
h=copy.deepcopy(s); h["events"]=h["events"][:1]
add("F14","conflicting_scalar_duplicate","conflicting duplicate respondent×question",s,h,["duplicate_semantics"],expected_good="BLOCKED",expected_hostile="BLOCKED",expected_codes=["D13B_B_SOURCE_DUPLICATE_SEMANTICS_UNRESOLVED"],trap="Choosing first/last would manufacture a scalar answer.",frontier="source validation")

#15 legitimate repeated
s=ds([resp("r1")],[ev("r1","Q","A","REPEATED",idx=1,event_id="r1a",group="rep"),ev("r1","Q","B","REPEATED",idx=2,event_id="r1b",group="rep")],[elig("r1","Q")],[qspec("REPEAT",TRUE,"Q",{"type":"ELIGIBLE_FOR","questions":["Q"]})])
h=copy.deepcopy(s); h["events"]=h["events"][:1]
add("F15","legitimate_repeated_same_question","legitimate repeated respondent×question",s,h,["duplicate_semantics","response_event_multiplicity"],expected_codes=["D13B_F_RESPONSE_EVENT_MULTIPLICITY_MISMATCH"],trap="Same respondent×question multiplicity is not automatically an error.",frontier="repeated topology")

#16 differing weights
s=ds([resp("r1",weight=1),resp("r2",weight=3)],[ev("r1","Q","A"),ev("r2","Q","B")],[elig("r1","Q"),elig("r2","Q")],[qspec("WGT",TRUE,"Q",{"type":"ELIGIBLE_FOR","questions":["Q"]})])
h=copy.deepcopy(s)
for r in h["respondents"]: r["weight_value"]=1
add("F16","differing_respondent_weights","differing respondent weights",s,h,["weight_basis","weighted_support"],expected_codes=["D13B_F_WEIGHT_BASIS_MISMATCH"],trap="Raw support is identical while weighted mass changes.",frontier="weighted conditional replay")

#17 missing invalid weight
s=ds([resp("r1",weight=None,wstatus="MISSING",wbasis="W1")],[ev("r1","Q","A")],[elig("r1","Q")],[qspec("WMISS",TRUE,"Q",{"type":"ELIGIBLE_FOR","questions":["Q"]})])
h=copy.deepcopy(s); h["respondents"][0]["weight_value"]=1; h["respondents"][0]["weight_status"]="VALID"
add("F17","missing_invalid_weight","missing/invalid weight",s,h,["weighted_support","weight_basis"],expected_good="BLOCKED",expected_hostile="FAIL",expected_codes=["D13B_F_WEIGHT_BASIS_MISMATCH"],trap="Defaulting to 1.0 converts unavailable weighted evidence into fabricated evidence.",frontier="typed weight availability")

#18 source identity alias collision
scopeA={"source_raw":"Survey Alias A","source_canonical":"survey_family","raw_wave":"Wave 1","canonical_wave":"W1","country_code":"ZZ"}
scopeB={"source_raw":"Survey Alias B","source_canonical":"survey_family","raw_wave":"Wave 1","canonical_wave":"W1","country_code":"ZZ"}
s=ds([resp("1",scope=scopeA),resp("1",scope=scopeB)],[ev("1","Q","A",scope=scopeA),ev("1","Q","B",scope=scopeB)],[elig("1","Q",scope=scopeA),elig("1","Q",scope=scopeB)],[
 qspec("SA",TRUE,"Q",{"type":"ALL_SCOPE"},scope=scopeA),qspec("SB",TRUE,"Q",{"type":"ALL_SCOPE"},scope=scopeB)])
h=copy.deepcopy(s)
for coll in ("respondents","events","eligibility"):
    for row in h[coll]:
        if row["source_raw"]=="Survey Alias B": row["source_raw"]="Survey Alias A"
for q in h["queries"]:
    if q["scope"]["source_raw"]=="Survey Alias B": q["scope"]["source_raw"]="Survey Alias A"
add("F18","source_identity_collision","source identity collision",s,h,["scope","respondent_incidence"],expected_codes=["D13B_F_RESPONDENT_INCIDENCE_MISMATCH"],trap="Canonical family identity alone can hide distinct source-native identities.",frontier="source-native replay provenance")

#19 raw/canonical wave collision
scopeA={"source_raw":"Fixture Survey","source_canonical":"fixture_survey","raw_wave":"Form A 2000","canonical_wave":"W1","country_code":"ZZ"}
scopeB={"source_raw":"Fixture Survey","source_canonical":"fixture_survey","raw_wave":"Form B 2000","canonical_wave":"W1","country_code":"ZZ"}
s=ds([resp("1",scope=scopeA),resp("1",scope=scopeB)],[ev("1","Q","A",scope=scopeA),ev("1","Q","B",scope=scopeB)],[elig("1","Q",scope=scopeA),elig("1","Q",scope=scopeB)],[
 qspec("WA",TRUE,"Q",{"type":"ALL_SCOPE"},scope=scopeA),qspec("WB",TRUE,"Q",{"type":"ALL_SCOPE"},scope=scopeB)])
h=copy.deepcopy(s)
for coll in ("respondents","events","eligibility"):
    for row in h[coll]:
        if row["raw_wave"]=="Form B 2000": row["raw_wave"]="Form A 2000"
for q in h["queries"]:
    if q["scope"]["raw_wave"]=="Form B 2000": q["scope"]["raw_wave"]="Form A 2000"
add("F19","raw_canonical_wave_collision","raw-wave/canonical-wave collision",s,h,["scope","respondent_incidence"],expected_codes=["D13B_F_RESPONDENT_INCIDENCE_MISMATCH"],trap="Same canonical wave can conceal source-native form/wave distinction.",frontier="source-native temporal replay")

#20 country collision
scopeUS=dict(SCOPE);scopeUS["country_code"]="US"
scopeCA=dict(SCOPE);scopeCA["country_code"]="CA"
s=ds([resp("1",scope=scopeUS),resp("1",scope=scopeCA)],[ev("1","Q","A",scope=scopeUS),ev("1","Q","B",scope=scopeCA)],[elig("1","Q",scope=scopeUS),elig("1","Q",scope=scopeCA)],[
 qspec("US",TRUE,"Q",{"type":"ALL_SCOPE"},scope=scopeUS),qspec("CA",TRUE,"Q",{"type":"ALL_SCOPE"},scope=scopeCA)])
h=copy.deepcopy(s)
for coll in ("respondents","events","eligibility"):
    for row in h[coll]:
        if row["country_code"]=="CA": row["country_code"]="US"
for q in h["queries"]:
    if q["scope"]["country_code"]=="CA": q["scope"]["country_code"]="US"
add("F20","country_collision","country collision",s,h,["scope","respondent_incidence"],expected_codes=["D13B_F_RESPONDENT_INCIDENCE_MISMATCH"],trap="Same respondent/question IDs in two countries must never coalesce.",frontier="country-scoped replay")

#21 same ID diff source canonical scopes
scopeA={"source_raw":"Source A","source_canonical":"source_a","raw_wave":"W1","canonical_wave":"W1","country_code":"ZZ"}
scopeB={"source_raw":"Source B","source_canonical":"source_b","raw_wave":"W1","canonical_wave":"W1","country_code":"ZZ"}
s=ds([resp("42",scope=scopeA),resp("42",scope=scopeB)],[ev("42","Q","A",scope=scopeA),ev("42","Q","B",scope=scopeB)],[elig("42","Q",scope=scopeA),elig("42","Q",scope=scopeB)],[
 qspec("SRC_A",TRUE,"Q",{"type":"ALL_SCOPE"},scope=scopeA),qspec("SRC_B",TRUE,"Q",{"type":"ALL_SCOPE"},scope=scopeB)])
h=copy.deepcopy(s)
for coll in ("respondents","events","eligibility"):
    for row in h[coll]:
        if row["source_canonical"]=="source_b":
            row.update({"source_raw":"Source A","source_canonical":"source_a"})
for q in h["queries"]:
    if q["scope"]["source_canonical"]=="source_b":
        q["scope"].update({"source_raw":"Source A","source_canonical":"source_a"})
add("F21","same_respondent_id_cross_source","same respondent ID across different source scopes",s,h,["respondent_incidence","scope"],expected_codes=["D13B_F_RESPONDENT_INCIDENCE_MISMATCH"],trap="Global respondent-ID uniqueness cannot be assumed across source-native universes.",frontier="scoped respondent binder")

#22 branch reconstruction
rs=[resp("r1",{"group":"A"}),resp("r2",{"group":"A"}),resp("r3",{"group":"B"})]
branch={"branch_id":"B_A","condition_ast":pos_cond("group","A"),"algorithm_id":"fixture_branch","algorithm_version":"1","parent_chain":["ROOT"],"authority_id":"AUTH-EMP-1","members":[scoped(respondent_id="r1"),scoped(respondent_id="r2")]}
s=ds(rs,[],[],[qspec("BRANCH_Q",{"op":"BRANCH","branch_id":"B_A"},target_q="Q",risk={"type":"ALL_SCOPE"})],branches=[branch])
h=copy.deepcopy(s); h["branches"][0]["members"]=[scoped(respondent_id="r1"),scoped(respondent_id="r3")]
add("F22","exact_branch_membership","exact branch membership reconstruction",s,h,["branch_membership_provenance","risk_set_identity"],expected_codes=["D13B_F_BRANCH_MEMBERSHIP_MISMATCH"],trap="Branch support remains two while member identity changes.",frontier="branch/cohort replay")

#23 k-way V550J
rs=[resp(f"r{i}") for i in range(1,5)]
vals=[("A","A","A"),("A","B","B"),("B","A","B"),("B","B","A")]
es=[];els=[]
for rid,trip in zip([f"r{i}" for i in range(1,5)],vals):
    for q,v in zip(["Q1","Q2","Q3"],trip):
        es.append(ev(rid,q,v));els.append(elig(rid,q))
joint={"joint_configuration_id":"J3","components":[{"question_id":"Q1","role":"a"},{"question_id":"Q2","role":"b"},{"question_id":"Q3","role":"c"}],"minimum_items_answered":3,"completion_rule":"ALL_COMPONENTS","component_order_semantics":"ORDERED","authority_id":"AUTH-EMP-1"}
s=ds(rs,es,els,[qspec("J3Q",TRUE,target={"type":"JOINT_CONFIG","joint_configuration_id":"J3"},risk={"type":"COMPLETE_CASE","questions":["Q1","Q2","Q3"]})],joints=[joint])
h=copy.deepcopy(s); h["joint_configurations"][0]["components"]=h["joint_configurations"][0]["components"][:2]; h["joint_configurations"][0]["minimum_items_answered"]=2
add("F23","k_way_v550j_configuration","k-way V550J configuration",s,h,["k_way_joint_topology","target_identity","raw_support"],expected_codes=["D13B_F_KWAY_JOINT_MISMATCH"],trap="Pairwise/component marginals cannot certify a 3-way configured pattern.",frontier="bounded k-way joint replay")

#24 same marginals diff joint
rs=[resp("r1"),resp("r2")]
es=[ev("r1","X","A"),ev("r1","Y","A"),ev("r2","X","B"),ev("r2","Y","B")]
els=[elig("r1","X"),elig("r1","Y"),elig("r2","X"),elig("r2","Y")]
s=ds(rs,es,els,[qspec("PAIR",response_cond("X","A"),"Y",{"type":"COMPLETE_CASE","questions":["X","Y"]})])
h=copy.deepcopy(s)
yrows=[r for r in h["events"] if r["question_id"]=="Y"]; yrows[0]["value"],yrows[1]["value"]=yrows[1]["value"],yrows[0]["value"]
add("F24","same_unary_marginals_different_joint","same unary marginals/different joint incidence",s,h,["response_event_multiplicity","raw_support"],expected_codes=["D13B_F_RESPONSE_EVENT_MULTIPLICITY_MISMATCH"],trap="X and Y marginals are identical in source/replay; P(Y|X) is not.",frontier="same-respondent pair incidence")

#25 future coordinate
rs=[resp("r1",{"housing_tenure":"RENTER"}),resp("r2",{"housing_tenure":"OWNER"})]
es=[ev("r1","Y","YES"),ev("r2","Y","NO")];els=[elig("r1","Y"),elig("r2","Y")]
s=ds(rs,es,els,[qspec("FUTURE_COORD",pos_cond("housing_tenure","RENTER"),"Y",{"type":"ELIGIBLE_FOR","questions":["Y"]})])
h=copy.deepcopy(s)
for r in h["respondents"]: r["positions"].pop("housing_tenure",None)
add("F25","future_coordinate_not_in_fixed_indicators","future empirical coordinate absent from today's fixed INDICATOR_FIELDS",s,h,["respondent_incidence","raw_support","predicate_identity"],expected_codes=["D13B_F_RESPONDENT_INCIDENCE_MISMATCH"],trap="Today's implementation inventory is not the future query frontier.",frontier="future-authorized empirical coordinate")

#26 same displayed answer diff predicates/risk sets
rs=[resp("r1",{"group":"A"}),resp("r2",{"group":"B"})]
es=[ev("r1","Y","YES"),ev("r2","Y","YES"),ev("r1","X","K"),ev("r2","X","K")]
els=[elig("r1","Y"),elig("r2","Y"),elig("r1","X"),elig("r2","X")]
qA=qspec("FACT_A",pos_cond("group","A"),"Y",{"type":"ELIGIBLE_FOR","questions":["Y"]})
qB=qspec("FACT_B",response_cond("X","K"),"Y",{"type":"EXPLICIT_RESPONDENTS","respondent_ids":["r2"]})
s=ds(rs,es,els,[qA,qB])
h=copy.deepcopy(s)
h["queries"][1]["condition_ast"]=copy.deepcopy(h["queries"][0]["condition_ast"])
h["queries"][1]["risk_set"]=copy.deepcopy(h["queries"][0]["risk_set"])
add("F26","same_displayed_answer_different_predicate_risk","same displayed answer under different predicates/risk sets",s,h,["predicate_identity","condition_ast_hash","risk_set_identity"],expected_codes=["D13B_F_PREDICATE_IDENTITY_MISMATCH"],trap="Both source facts can display 100% YES while remaining different empirical facts.",frontier="fact identity under predicate/risk-set semantics")


def load_fixtures():
    return copy.deepcopy(fixtures)

if __name__ == '__main__':
    import json
    print(json.dumps({'fixture_count': len(fixtures), 'fixture_ids': [f['fixture_id'] for f in fixtures]}, indent=2))
