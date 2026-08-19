#!/usr/bin/env python3
"""D13B explicit synthetic hostile fixtures. No production data or DB access."""
import copy
from itertools import product
BASE_AUTH={"authority_id":"AUTH-EMP-1","authority_version":"1","authority_hash":"sha256:fixture-authority-v1","authority_type":"EMPIRICAL_FIXTURE"}
SCOPE={"source_raw":"Fixture Survey","source_canonical":"fixture_survey","raw_wave":"Wave 1","canonical_wave":"W1","country_code":"ZZ"}

def scoped(d=None, **kwargs):
    x=dict(SCOPE)
    if d: x.update(d)
    x.update(kwargs)
    return x
def resp(rid, positions=None, weight=1, wstatus="VALID", wbasis="W1", scope=None):
    return scoped(scope or {}, respondent_id=str(rid), positions=positions or {}, weight_value=weight, weight_status=wstatus, weight_basis_id=wbasis)
def elig(rid,q,app="APPLICABLE",route="ASKED",scope=None,authority="AUTH-EMP-1"):
    return scoped(scope or {}, respondent_id=str(rid),question_id=q,applicability_state=app,routing_state=route,authority_id=authority)
def ev(rid,q,val=None, topology="SCALAR", state="SUBSTANTIVE", idx=1, rank=0, group="g1", event_id=None, scope=None, authority="AUTH-EMP-1",target_id=""):
    return scoped(scope or {}, respondent_id=str(rid),question_id=q,event_group_id=group,event_id=event_id or f"{q}:{rid}:{idx}",event_index=idx,order_rank=rank,topology=topology,response_state=state,value=val,authority_id=authority,target_id=target_id or q)
def qspec(qid, condition, target_q=None, risk=None, scope=None, target=None, authority="AUTH-EMP-1"):
    return {
        "query_id":qid,"scope":dict(SCOPE if scope is None else scope),
        "condition_ast":condition,"risk_set":risk or {"type":"ALL_SCOPE"},
        "target":target or {"type":"QUESTION","question_id":target_q},
        "measure_basis":"RAW_AND_WEIGHTED","authority_id":authority
    }
def ds(respondents, events=None, eligibility=None, queries=None, branches=None, joints=None, authorities=None):
    return {"authorities":copy.deepcopy(authorities or [BASE_AUTH]),"respondents":respondents,"events":events or [],
            "eligibility":eligibility or [],"queries":queries or [],"branches":branches or [],
            "joint_configurations":joints or []}
TRUE={"op":"TRUE"}
def response_cond(q,val,state="SUBSTANTIVE"):
    return {"op":"RESPONSE","question_id":q,"value":val,"response_state":state}
def pos_cond(c,v):
    return {"op":"POSITION","coordinate":c,"value":v}
def andc(*children):
    return {"op":"AND","children":list(children)}

fixtures=[]

def add(fid,name,required_case,source,hostile,primary,expected_good="PASS",expected_hostile="FAIL",expected_codes=None,trap="",frontier="",notes=""):
    fixtures.append({
        "fixture_id":fid,"fixture_name":name,"required_case":required_case,
        "source":source,"good_replay":copy.deepcopy(source),"hostile_replay":hostile,
        "primary_proof_dimensions":primary,
        "expected_good_state":expected_good,"expected_hostile_state":expected_hostile,
        "expected_failure_or_blocked_states":expected_codes or [],
        "aggregate_equality_trap":trap,"frontier_capability":frontier,"notes":notes
    })

# 1 ordinary scalar
s=ds([resp("r1")],[ev("r1","Q1","YES")],[elig("r1","Q1")],[qspec("Q1_DIST",TRUE,"Q1",{"type":"ELIGIBLE_FOR","questions":["Q1"]})])
h=copy.deepcopy(s); h["events"][0]["value"]="NO"
add("F01","ordinary_scalar_response","ordinary scalar response",s,h,["response_event_multiplicity","response_topology","raw_support"],expected_codes=["D13B_F_RESPONSE_EVENT_MULTIPLICITY_MISMATCH"],frontier="unary response distribution")

# 2 repeated
s=ds([resp("r1")],[ev("r1","QR","A","REPEATED",idx=1,group="rep"),ev("r1","QR","B","REPEATED",idx=2,group="rep")],[elig("r1","QR")],[qspec("QR_DIST",TRUE,"QR",{"type":"ELIGIBLE_FOR","questions":["QR"]})])
h=copy.deepcopy(s); h["events"]=h["events"][:1]
add("F02","repeated_response_event","repeated response event",s,h,["response_event_multiplicity","response_topology","duplicate_semantics"],expected_codes=["D13B_F_RESPONSE_EVENT_MULTIPLICITY_MISMATCH"],trap="One respondent/question row count after dedup looks superficially valid.",frontier="repeated response replay")

#3 multiselect
s=ds([resp("r1")],[ev("r1","QM","A","MULTISELECT_SET",idx=1,group="set"),ev("r1","QM","C","MULTISELECT_SET",idx=2,group="set")],[elig("r1","QM")],[qspec("QM_DIST",TRUE,"QM",{"type":"ELIGIBLE_FOR","questions":["QM"]})])
h=copy.deepcopy(s); h["events"]=h["events"][:1]; h["events"][0]["topology"]="SCALAR"
add("F03","multiselect_set_response","multiselect set response",s,h,["response_event_multiplicity","response_topology"],expected_codes=["D13B_F_RESPONSE_EVENT_MULTIPLICITY_MISMATCH"],frontier="set-valued response replay")

#4 ordered ranked
s=ds([resp("r1")],[ev("r1","QO","A","ORDERED_RANKED",idx=1,rank=1,group="rank"),ev("r1","QO","B","ORDERED_RANKED",idx=2,rank=2,group="rank")],[elig("r1","QO")],[qspec("QO_DIST",TRUE,"QO",{"type":"ELIGIBLE_FOR","questions":["QO"]})])
h=copy.deepcopy(s); h["events"][0]["order_rank"]=2; h["events"][1]["order_rank"]=1
add("F04","ordered_ranked_response","ordered/ranked response",s,h,["response_topology","order_independence"],expected_codes=["D13B_F_RESPONSE_EVENT_MULTIPLICITY_MISMATCH","D13B_F_RESPONSE_TOPOLOGY_MISMATCH"],trap="Same chosen options, different ranking.",frontier="ranked response replay")

#5 routed/not asked
rs=[resp("r1"),resp("r2")]
es=[ev("r1","Y","YES")]
els=[elig("r1","Y","APPLICABLE","ASKED"),elig("r2","Y","NOT_APPLICABLE","NOT_ASKED")]
s=ds(rs,es,els,[qspec("Y_ELIG",TRUE,"Y",{"type":"ELIGIBLE_FOR","questions":["Y"]})])
h=copy.deepcopy(s); h["eligibility"][1]["applicability_state"]="APPLICABLE"; h["eligibility"][1]["routing_state"]="ASKED"
add("F05","routed_not_asked_target","routed/not-asked target",s,h,["routing_applicability","risk_set_identity","raw_support"],expected_codes=["D13B_F_ROUTING_APPLICABILITY_MISMATCH"],trap="Observed YES numerator can remain 1 while denominator semantics change.",frontier="routed target risk-set replay")

#6 DK
s=ds([resp("r1")],[ev("r1","Q","",state="DK")],[elig("r1","Q")],[qspec("QDK",TRUE,"Q",{"type":"ELIGIBLE_FOR","questions":["Q"]})])
h=copy.deepcopy(s); h["events"][0]["response_state"]="MISSING"
add("F06","dk_typed_state","DK",s,h,["typed_missingness"],expected_codes=["D13B_F_RESPONSE_EVENT_MULTIPLICITY_MISMATCH","D13B_F_TYPED_MISSINGNESS_MISMATCH"],frontier="typed missingness")

#7 refusal
s=ds([resp("r1")],[ev("r1","Q","",state="REFUSAL")],[elig("r1","Q")],[qspec("QREF",TRUE,"Q",{"type":"ELIGIBLE_FOR","questions":["Q"]})])
h=copy.deepcopy(s); h["events"][0]["response_state"]="MISSING"
add("F07","refusal_typed_state","refusal",s,h,["typed_missingness"],expected_codes=["D13B_F_TYPED_MISSINGNESS_MISMATCH"],frontier="typed missingness")

#8 inapplicable
s=ds([resp("r1")],[ev("r1","Q","",state="IAP")],[elig("r1","Q","INAPPLICABLE","ROUTED_OUT")],[qspec("QIAP",TRUE,"Q",{"type":"ALL_SCOPE"})])
h=copy.deepcopy(s); h["events"][0]["response_state"]="MISSING"; h["eligibility"][0]["applicability_state"]="APPLICABLE"; h["eligibility"][0]["routing_state"]="ASKED"
add("F08","inapplicable_typed_state","inapplicable",s,h,["typed_missingness","routing_applicability"],expected_codes=["D13B_F_ROUTING_APPLICABILITY_MISMATCH"],frontier="typed applicability")

#9 zero overlap
rs=[resp("r1"),resp("r2")]
es=[ev("r1","X","A"),ev("r2","Y","B")]
els=[elig("r1","X"),elig("r1","Y","NOT_APPLICABLE","NOT_ASKED"),elig("r2","X","NOT_APPLICABLE","NOT_ASKED"),elig("r2","Y")]
s=ds(rs,es,els,[qspec("ZERO_PAIR",response_cond("X","A"),"Y",{"type":"COMPLETE_CASE","questions":["X","Y"]})])
h=copy.deepcopy(s); h["events"].append(ev("r1","Y","B")); h["eligibility"][1]["applicability_state"]="APPLICABLE"; h["eligibility"][1]["routing_state"]="ASKED"
add("F09","zero_overlap_pair","zero-overlap question pair",s,h,["risk_set_identity","raw_support","respondent_incidence"],expected_codes=["D13B_F_RISK_SET_MISMATCH"],trap="A system that drops zero-overlap facts can fabricate cotravel.",frontier="pairwise same-respondent replay")

#10 sparse overlap same counts diff member
rs=[resp(f"r{i}") for i in range(1,7)]
es=[]; els=[]
for i in range(1,6):
    es.append(ev(f"r{i}","X","A" if i<4 else "B")); els.append(elig(f"r{i}","X"))
# Y on r5 and r6 only
for i,val in [(5,"Y1"),(6,"Y2")]:
    es.append(ev(f"r{i}","Y",val)); els.append(elig(f"r{i}","Y"))
for i in range(1,5): els.append(elig(f"r{i}","Y","NOT_APPLICABLE","NOT_ASKED"))
els.append(elig("r6","X","NOT_APPLICABLE","NOT_ASKED"))
s=ds(rs,es,els,[qspec("SPARSE",TRUE,"Y",{"type":"COMPLETE_CASE","questions":["X","Y"]})])
h=copy.deepcopy(s)
# move Y from r5 to r4, preserve Y marginal and overlap count=1
for row in h["events"]:
    if row["question_id"]=="Y" and row["respondent_id"]=="r5":
        row["respondent_id"]="r4"; row["event_id"]="Y:r4:1"
for row in h["eligibility"]:
    if row["question_id"]=="Y" and row["respondent_id"]=="r5":
        row["applicability_state"]="NOT_APPLICABLE"; row["routing_state"]="NOT_ASKED"
    if row["question_id"]=="Y" and row["respondent_id"]=="r4":
        row["applicability_state"]="APPLICABLE"; row["routing_state"]="ASKED"
add("F10","sparse_overlap_exact_members","sparse overlap",s,h,["risk_set_identity","response_event_multiplicity"],expected_codes=["D13B_F_RESPONSE_EVENT_MULTIPLICITY_MISMATCH"],trap="Same marginals and same overlap count, different overlapping respondent.",frontier="exact pair overlap membership")

#11 XOR
rs=[resp(f"r{i}") for i in range(4)]
comb=[("0","0","0"),("0","1","1"),("1","0","1"),("1","1","0")]
es=[];els=[]
for i,(a,b,y) in enumerate(comb):
    rid=f"r{i}"
    for q,v in [("A",a),("B",b),("Y",y)]:
        es.append(ev(rid,q,v)); els.append(elig(rid,q))
queries=[qspec("XOR11",andc(response_cond("A","1"),response_cond("B","1")),"Y",{"type":"COMPLETE_CASE","questions":["A","B","Y"]}),
         qspec("XOR10",andc(response_cond("A","1"),response_cond("B","0")),"Y",{"type":"COMPLETE_CASE","questions":["A","B","Y"]})]
s=ds(rs,es,els,queries)
h=copy.deepcopy(s)
# preserve every unary marginal while altering respondent-bound XOR incidence
yrows=[r for r in h["events"] if r["question_id"]=="Y"]
v0=yrows[2]["value"]; yrows[2]["value"]=yrows[3]["value"]; yrows[3]["value"]=v0
add("F11","xor_interaction","XOR",s,h,["raw_support","respondent_incidence"],expected_codes=["D13B_F_RESPONSE_EVENT_MULTIPLICITY_MISMATCH"],trap="All unary marginals remain 50/50 while conditional structure changes.",frontier="arbitrary conjunction replay")

#12 Simpson
rs=[];es=[];els=[]
ridnum=0
def add_sim(group,x_values):
    global ridnum
# Group A: X1 9, Y success 8; X0 1, success1
for group, rows in [
    ("A",[("1","1")]*8+[("1","0")]+[("0","1")]),
    ("B",[("1","0")]+[("0","1")]+[("0","0")]*8)
]:
    for x,y in rows:
        rid=f"r{len(rs)+1}"
        rs.append(resp(rid,{"group":group}))
        for q,v in [("X",x),("Y",y)]:
            es.append(ev(rid,q,v));els.append(elig(rid,q))
queries=[
 qspec("SIM_AGG_X1",response_cond("X","1"),"Y",{"type":"COMPLETE_CASE","questions":["X","Y"]}),
 qspec("SIM_A_X1",andc(pos_cond("group","A"),response_cond("X","1")),"Y",{"type":"COMPLETE_CASE","questions":["X","Y"]}),
 qspec("SIM_A_X0",andc(pos_cond("group","A"),response_cond("X","0")),"Y",{"type":"COMPLETE_CASE","questions":["X","Y"]}),
 qspec("SIM_B_X1",andc(pos_cond("group","B"),response_cond("X","1")),"Y",{"type":"COMPLETE_CASE","questions":["X","Y"]}),
 qspec("SIM_B_X0",andc(pos_cond("group","B"),response_cond("X","0")),"Y",{"type":"COMPLETE_CASE","questions":["X","Y"]})
]
s=ds(rs,es,els,queries)
h=copy.deepcopy(s)
for r in h["respondents"]: r["positions"].pop("group",None)
add("F12","simpson_reversal","Simpson reversal",s,h,["respondent_incidence","raw_support","predicate_identity"],expected_codes=["D13B_F_RESPONDENT_INCIDENCE_MISMATCH"],trap="Aggregate association can reverse every within-group association.",frontier="conditioned empirical replay")

#13 rare three-way conjunction
rs=[];es=[];els=[]
for i,(a,b,c) in enumerate(product(["0","1"], repeat=3)):
    rid=f"r{i}"
    rs.append(resp(rid))
    y="RARE" if (a,b,c)==("1","1","1") else "COMMON"
    for q,v in [("A",a),("B",b),("C",c),("Y",y)]:
        es.append(ev(rid,q,v));els.append(elig(rid,q))
s=ds(rs,es,els,[qspec("RARE3",andc(response_cond("A","1"),response_cond("B","1"),response_cond("C","1")),"Y",{"type":"COMPLETE_CASE","questions":["A","B","C","Y"]})])
h=copy.deepcopy(s)
# swap C between 110 and 111: C marginal preserved, rare three-way membership changes
crows={r["respondent_id"]:r for r in h["events"] if r["question_id"]=="C"}
crows["r6"]["value"],crows["r7"]["value"]=crows["r7"]["value"],crows["r6"]["value"]
add("F13","rare_three_way_conjunction","rare three-way conjunction",s,h,["raw_support","response_event_multiplicity"],expected_codes=["D13B_F_RESPONSE_EVENT_MULTIPLICITY_MISMATCH"],trap="Unary and much pairwise information can survive while rare 3-way cell moves.",frontier="k-predicate conjunction replay")
