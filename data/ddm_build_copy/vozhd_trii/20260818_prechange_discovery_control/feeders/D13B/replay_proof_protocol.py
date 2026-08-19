#!/usr/bin/env python3
"""D13B feeder-local replay verifier. Standard library only; no DB access."""
import copy,hashlib,json,random
from collections import Counter,defaultdict
from decimal import Decimal

PASS,FAIL,BLOCKED="PASS","FAIL","BLOCKED"
FAILC={
"respondent_incidence":"D13B_F_RESPONDENT_INCIDENCE_MISMATCH","response_event_multiplicity":"D13B_F_RESPONSE_EVENT_MULTIPLICITY_MISMATCH",
"response_topology":"D13B_F_RESPONSE_TOPOLOGY_MISMATCH","risk_set_identity":"D13B_F_RISK_SET_MISMATCH",
"routing_applicability":"D13B_F_ROUTING_APPLICABILITY_MISMATCH","typed_missingness":"D13B_F_TYPED_MISSINGNESS_MISMATCH",
"raw_support":"D13B_F_RAW_SUPPORT_MISMATCH","weighted_support":"D13B_F_WEIGHTED_SUPPORT_MISMATCH","weight_basis":"D13B_F_WEIGHT_BASIS_MISMATCH",
"scope":"D13B_F_SCOPE_MISMATCH","predicate_identity":"D13B_F_PREDICATE_IDENTITY_MISMATCH","condition_ast_hash":"D13B_F_CONDITION_AST_MISMATCH",
"target_identity":"D13B_F_TARGET_IDENTITY_MISMATCH","branch_membership_provenance":"D13B_F_BRANCH_MEMBERSHIP_MISMATCH",
"k_way_joint_topology":"D13B_F_KWAY_JOINT_MISMATCH","authority_identity":"D13B_F_AUTHORITY_IDENTITY_MISMATCH",
"logical_content_hash":"D13B_F_LOGICAL_CONTENT_HASH_MISMATCH","deterministic_replay":"D13B_F_NONDETERMINISTIC_REPLAY",
"duplicate_semantics":"D13B_F_DUPLICATE_SEMANTICS_MISMATCH","order_independence":"D13B_F_ORDER_DEPENDENCE"}
BLOCKC={k:"D13B_B_"+{
"respondent_incidence":"RESPONDENT_IDENTITY_UNRESOLVED","response_event_multiplicity":"RESPONSE_EVENT_IDENTITY_UNRESOLVED",
"response_topology":"RESPONSE_TOPOLOGY_UNRESOLVED","risk_set_identity":"RISK_SET_UNRESOLVED","routing_applicability":"ROUTING_AUTHORITY_UNAVAILABLE",
"typed_missingness":"TYPED_MISSINGNESS_UNRESOLVED","raw_support":"QUERY_NOT_REPLAYABLE","weighted_support":"WEIGHT_BASIS_UNAVAILABLE",
"weight_basis":"WEIGHT_BASIS_UNAVAILABLE","scope":"SCOPE_IDENTITY_UNRESOLVED","predicate_identity":"PREDICATE_AUTHORITY_UNAVAILABLE",
"condition_ast_hash":"CONDITION_AST_UNRESOLVED","target_identity":"TARGET_AUTHORITY_UNAVAILABLE","branch_membership_provenance":"BRANCH_PROVENANCE_UNAVAILABLE",
"k_way_joint_topology":"JOINT_CONFIGURATION_UNRESOLVED","authority_identity":"AUTHORITY_SNAPSHOT_UNAVAILABLE",
"logical_content_hash":"LOGICAL_PROJECTION_UNDEFINED","deterministic_replay":"DETERMINISM_NOT_TESTABLE",
"duplicate_semantics":"SOURCE_DUPLICATE_SEMANTICS_UNRESOLVED","order_independence":"ORDER_SEMANTICS_UNRESOLVED"}[k] for k in FAILC}

def c(v): return "" if v is None else str(v).strip()
def cj(x): return json.dumps(x,sort_keys=True,separators=(",",":"),ensure_ascii=False,default=str)
def sha(x): return hashlib.sha256(cj(x).encode()).hexdigest()
def scope(x): return (c(x.get("source_raw")),c(x.get("source_canonical")),c(x.get("raw_wave")),c(x.get("canonical_wave")),c(x.get("country_code")).upper())
def rk(x): return (*scope(x),c(x.get("respondent_id")))
def st(v): return c(v).upper()

def cast(a):
    if not isinstance(a,dict): return a
    o={"op":st(a.get("op"))}
    for k,v in a.items():
        if k=="op": continue
        if k=="children":
            z=[cast(x) for x in (v or [])]; o[k]=sorted(z,key=cj) if o["op"] in {"AND","OR"} else z
        elif k=="child": o[k]=cast(v)
        elif k=="values": o[k]=sorted(v,key=str) if a.get("set_semantics") else v
        else:o[k]=v
    return o
def ah(a): return sha(cast(a))
def crisk(r):
    r=copy.deepcopy(r or {"type":"ALL_SCOPE"})
    if isinstance(r.get("questions"),list): r["questions"]=sorted(map(str,r["questions"]))
    return r

def maps(d):
    ev=defaultdict(list); el={}; rs={}
    for r in d.get("respondents",[]): rs[rk(r)]=r
    for e in d.get("events",[]): ev[(rk(e),c(e.get("question_id")))].append(e)
    for x in d.get("eligibility",[]): el[(rk(x),c(x.get("question_id")))]=x
    return rs,ev,el

def outcome(es):
    if not es:return {"kind":"NO_OBSERVED_EVENT"}
    tops={st(e.get("topology")) for e in es}
    if len(tops)!=1:return {"kind":"INVALID_MIXED_TOPOLOGY","topologies":sorted(tops)}
    t=next(iter(tops))
    def a(e):
        s=st(e.get("response_state") or "SUBSTANTIVE")
        return {"state":s} if s!="SUBSTANTIVE" else {"state":"SUBSTANTIVE","value":e.get("value")}
    if t=="SCALAR": return {"kind":"SCALAR","value":a(es[0])} if len(es)==1 else {"kind":"INVALID_SCALAR_MULTIPLICITY"}
    if t=="MULTISELECT_SET": return {"kind":t,"values":sorted([a(e) for e in es],key=cj)}
    if t=="ORDERED_RANKED":
        z=sorted(es,key=lambda e:(int(e.get("order_rank") or 0),int(e.get("event_index") or 0),c(e.get("event_id"))))
        return {"kind":t,"values":[{"rank":int(e.get("order_rank") or 0),"value":a(e)} for e in z]}
    z=sorted(es,key=lambda e:(int(e.get("event_index") or 0),c(e.get("event_id"))))
    return {"kind":t,"values":[{"index":int(e.get("event_index") or 0),"value":a(e)} for e in z]}

def validate(d):
    b=[]; seen=set(); rs,ev,_=maps(d)
    for k in rs:
        if any(not x for x in k):b.append("D13B_B_RESPONDENT_IDENTITY_UNRESOLVED")
        if k in seen:b.append("D13B_B_RESPONDENT_IDENTITY_UNRESOLVED")
        seen.add(k)
    for _,es in ev.items():
        tops={st(e.get("topology")) for e in es}
        if not tops or "" in tops or len(tops)>1:b.append("D13B_B_RESPONSE_TOPOLOGY_UNRESOLVED")
        if tops=={"SCALAR"} and len(es)>1:b.append("D13B_B_SOURCE_DUPLICATE_SEMANTICS_UNRESOLVED")
    aids={c(a.get("authority_id")) for a in d.get("authorities",[])}
    for k in ("events","eligibility","branches","joint_configurations","queries"):
        for x in d.get(k,[]):
            if c(x.get("authority_id")) and c(x.get("authority_id")) not in aids:b.append("D13B_B_AUTHORITY_SNAPSHOT_UNAVAILABLE")
    return sorted(set(b))

def eligible(el,k,q):
    x=el.get((k,q))
    return bool(x) and st(x.get("applicability_state")) in {"APPLICABLE","ASKED"} and st(x.get("routing_state")) in {"ASKED","ROUTED_IN","IN_SCOPE",""}
def cond(d,k,a,rs,ev,el,br):
    op=st(a.get("op"))
    if op in {"","TRUE"}:return True
    if op=="FALSE":return False
    if op=="AND":return all(cond(d,k,x,rs,ev,el,br) for x in a.get("children",[]))
    if op=="OR":return any(cond(d,k,x,rs,ev,el,br) for x in a.get("children",[]))
    if op=="NOT":return not cond(d,k,a.get("child",{"op":"FALSE"}),rs,ev,el,br)
    if op=="POSITION":return rs[k].get("positions",{}).get(a.get("coordinate"))==a.get("value")
    if op=="RESPONSE":
        vals=set(a.get("values") or ([a.get("value")] if "value" in a else [])); state=st(a.get("response_state") or "SUBSTANTIVE")
        return any(st(e.get("response_state") or "SUBSTANTIVE")==state and (not vals or e.get("value") in vals) for e in ev.get((k,c(a.get("question_id"))),[]))
    if op=="BRANCH":return k in br.get(c(a.get("branch_id")),set())
    if op=="ELIGIBILITY":
        x=el.get((k,c(a.get("question_id"))))
        return bool(x) and (not a.get("applicability_state") or st(x.get("applicability_state"))==st(a.get("applicability_state"))) and (not a.get("routing_state") or st(x.get("routing_state"))==st(a.get("routing_state")))
    raise ValueError(op)

def evaluate_query(d,q):
    rs,ev,el=maps(d); sc=scope(q.get("scope",{})); members={k for k in rs if k[:5]==sc}
    r=q.get("risk_set") or {"type":"ALL_SCOPE"}; typ=st(r.get("type"))
    if typ=="ELIGIBLE_FOR": members={k for k in members if all(eligible(el,k,c(x)) for x in r.get("questions",[]))}
    elif typ=="COMPLETE_CASE": members={k for k in members if all(eligible(el,k,c(x)) and bool(ev.get((k,c(x)))) for x in r.get("questions",[]))}
    elif typ=="ROUTED_INTO": members={k for k in members if eligible(el,k,c(r.get("question_id")))}
    elif typ=="EXPLICIT_RESPONDENTS": members={k for k in members if k[-1] in set(map(str,r.get("respondent_ids",[])))}
    elif typ!="ALL_SCOPE": raise ValueError(typ)
    br={c(b.get("branch_id")):{rk(m) if isinstance(m,dict) else tuple(map(str,m)) for m in b.get("members",[])} for b in d.get("branches",[])}
    sel=sorted(k for k in members if cond(d,k,cast(q.get("condition_ast") or {"op":"TRUE"}),rs,ev,el,br))
    joints={c(j.get("joint_configuration_id")):j for j in d.get("joint_configurations",[])}
    def targ(k):
        t=q.get("target",{}); typ=st(t.get("type"))
        if typ=="QUESTION":return outcome(ev.get((k,c(t.get("question_id"))),[]))
        j=joints.get(c(t.get("joint_configuration_id")))
        return {"kind":"JOINT_CONFIG","joint_configuration_id":c(t.get("joint_configuration_id")),"components":[{"question_id":c(x.get("question_id")),"outcome":outcome(ev.get((k,c(x.get("question_id"))),[]))} for x in (j or {}).get("components",[])]}
    raw=Counter(); w=defaultdict(Decimal); wb=None
    for k in sel:
        z=cj(targ(k)); raw[z]+=1; rr=rs[k]
        try:
            if st(rr.get("weight_status")) not in {"VALID","WEIGHTED_AVAILABLE"} or not c(rr.get("weight_basis_id")):raise ValueError
            v=Decimal(str(rr.get("weight_value")))
            if not v.is_finite() or v<0:raise ValueError
            w[z]+=v
        except Exception:wb="D13B_B_WEIGHT_BASIS_UNAVAILABLE"
    return {"query_id":c(q.get("query_id")),"condition_ast":cast(q.get("condition_ast") or {"op":"TRUE"}),"condition_ast_hash":ah(q.get("condition_ast") or {"op":"TRUE"}),
    "risk_set":crisk(r),"risk_member_keys":[list(k) for k in sorted(members)],"selected_member_keys":[list(k) for k in sel],"target":q.get("target",{}),
    "raw_denominator":len(sel),"raw_counts":dict(sorted(raw.items())),"weighted_state":BLOCKED if wb else PASS,"weighted_blocked_state":wb,
    "weighted_denominator":None if wb else str(sum(w.values(),Decimal(0))),"weighted_counts":None if wb else {k:str(v) for k,v in sorted(w.items())}}

def projection(d):
    rs,ev,el=maps(d)
    A=sorted([{"authority_id":c(a.get("authority_id")),"authority_version":c(a.get("authority_version")),"authority_hash":c(a.get("authority_hash")),"authority_type":c(a.get("authority_type"))} for a in d.get("authorities",[])],key=cj)
    R=sorted([{"key":k,"positions":r.get("positions",{}),"weight_value":None if r.get("weight_value") is None else str(r.get("weight_value")),"weight_status":st(r.get("weight_status")),"weight_basis_id":c(r.get("weight_basis_id"))} for k,r in rs.items()],key=cj)
    E=sorted([{"key":k,"q":q,"n":len(es),"outcome":outcome(es),"events":sorted([{"id":c(e.get("event_id")),"group":c(e.get("event_group_id")),"index":int(e.get("event_index") or 0),"rank":int(e.get("order_rank") or 0),"topology":st(e.get("topology")),"state":st(e.get("response_state") or "SUBSTANTIVE"),"value":e.get("value"),"authority_id":c(e.get("authority_id"))} for e in es],key=cj)} for (k,q),es in ev.items()],key=cj)
    L=sorted([{"key":rk(x),"q":c(x.get("question_id")),"app":st(x.get("applicability_state")),"route":st(x.get("routing_state")),"authority_id":c(x.get("authority_id"))} for x in d.get("eligibility",[])],key=cj)
    B=sorted([{"branch_id":c(b.get("branch_id")),"ast":cast(b.get("condition_ast") or {"op":"TRUE"}),"hash":ah(b.get("condition_ast") or {"op":"TRUE"}),"algorithm_id":c(b.get("algorithm_id")),"algorithm_version":c(b.get("algorithm_version")),"parent_chain":b.get("parent_chain",[]),"authority_id":c(b.get("authority_id")),"members":sorted([list(rk(m)) if isinstance(m,dict) else list(m) for m in b.get("members",[])])} for b in d.get("branches",[])],key=cj)
    J=sorted([{"id":c(j.get("joint_configuration_id")),"components":j.get("components",[]),"minimum":j.get("minimum_items_answered"),"completion":j.get("completion_rule"),"order":j.get("component_order_semantics","ORDERED"),"authority_id":c(j.get("authority_id"))} for j in d.get("joint_configurations",[])],key=cj)
    Q=sorted([{"id":c(q.get("query_id")),"scope":scope(q.get("scope",{})),"ast":cast(q.get("condition_ast") or {"op":"TRUE"}),"hash":ah(q.get("condition_ast") or {"op":"TRUE"}),"risk":crisk(q.get("risk_set")),"target":q.get("target",{}),"authority_id":c(q.get("authority_id"))} for q in d.get("queries",[])],key=cj)
    QR={c(q.get("query_id")):evaluate_query(d,q) for q in d.get("queries",[])}
    return {"authorities":A,"respondents":R,"events":E,"eligibility":L,"branches":B,"joint":J,"queries":Q,"query_results":QR}

def compare_datasets(s,r):
    sb=validate(s); rb=validate(r); dims=[]
    def add(n,a,b):dims.append({"name":n,"state":PASS if a==b else FAIL,"failure_or_blocked_state":None if a==b else FAILC[n]})
    if sb:
        for n in FAILC:dims.append({"name":n,"state":BLOCKED,"failure_or_blocked_state":"D13B_B_SOURCE_DUPLICATE_SEMANTICS_UNRESOLVED" if n=="duplicate_semantics" and "D13B_B_SOURCE_DUPLICATE_SEMANTICS_UNRESOLVED" in sb else BLOCKC[n]})
        return {"overall_state":BLOCKED,"source_blockers":sb,"replay_blockers":rb,"dimensions":dims,"logical_source_hash":None,"logical_replay_hash":None}
    S,R=projection(s),projection(r)
    add("respondent_incidence",[(x["key"],x["positions"]) for x in S["respondents"]],[(x["key"],x["positions"]) for x in R["respondents"]])
    add("response_event_multiplicity",S["events"],R["events"]); add("response_topology",[(x["key"],x["q"],x["outcome"]) for x in S["events"]],[(x["key"],x["q"],x["outcome"]) for x in R["events"]])
    add("routing_applicability",S["eligibility"],R["eligibility"]); add("typed_missingness",[(x["key"],x["q"],[(e["state"],e["value"]) for e in x["events"]]) for x in S["events"]],[(x["key"],x["q"],[(e["state"],e["value"]) for e in x["events"]]) for x in R["events"]])
    add("weight_basis",[(x["key"],x["weight_value"],x["weight_status"],x["weight_basis_id"]) for x in S["respondents"]],[(x["key"],x["weight_value"],x["weight_status"],x["weight_basis_id"]) for x in R["respondents"]])
    add("scope",sorted({x["key"][:5] for x in S["respondents"]}),sorted({x["key"][:5] for x in R["respondents"]}))
    add("predicate_identity",[(x["id"],x["ast"]) for x in S["queries"]],[(x["id"],x["ast"]) for x in R["queries"]]); add("condition_ast_hash",[(x["id"],x["hash"]) for x in S["queries"]],[(x["id"],x["hash"]) for x in R["queries"]])
    add("target_identity",[(x["id"],x["target"]) for x in S["queries"]],[(x["id"],x["target"]) for x in R["queries"]]); add("branch_membership_provenance",S["branches"],R["branches"]); add("k_way_joint_topology",S["joint"],R["joint"]); add("authority_identity",S["authorities"],R["authorities"])
    ids=sorted(set(S["query_results"])|set(R["query_results"])); sr=[];rr=[];su=[];ru=[];sw=[];rw=[]
    for i in ids:
        a,b=S["query_results"].get(i),R["query_results"].get(i)
        sr.append((i,None if a is None else (a["risk_set"],a["risk_member_keys"],a["selected_member_keys"]))); rr.append((i,None if b is None else (b["risk_set"],b["risk_member_keys"],b["selected_member_keys"])))
        su.append((i,None if a is None else (a["raw_denominator"],a["raw_counts"]))); ru.append((i,None if b is None else (b["raw_denominator"],b["raw_counts"])))
        sw.append((i,None if a is None else (a["weighted_state"],a["weighted_denominator"],a["weighted_counts"],a["weighted_blocked_state"]))); rw.append((i,None if b is None else (b["weighted_state"],b["weighted_denominator"],b["weighted_counts"],b["weighted_blocked_state"])))
    add("risk_set_identity",sr,rr); add("raw_support",su,ru)
    if sw==rw and any(x[1] and x[1][0]==BLOCKED for x in sw):dims.append({"name":"weighted_support","state":BLOCKED,"failure_or_blocked_state":"D13B_B_WEIGHT_BASIS_UNAVAILABLE"})
    else:add("weighted_support",sw,rw)
    add("duplicate_semantics",[(x["key"],x["q"],x["outcome"]) for x in S["events"]],[(x["key"],x["q"],x["outcome"]) for x in R["events"]])
    sh,rh=sha(S),sha(R); add("logical_content_hash",sh,rh)
    dims.append({"name":"deterministic_replay","state":PASS if sha(projection(s))==sh and sha(projection(r))==rh else FAIL,"failure_or_blocked_state":None})
    def rev(d):
        z=copy.deepcopy(d)
        for k in ("authorities","respondents","eligibility","events","branches","joint_configurations","queries"):z[k]=list(reversed(z.get(k,[])))
        return z
    oi=sha(projection(s))==sha(projection(rev(s))) and sha(projection(r))==sha(projection(rev(r)))
    dims.append({"name":"order_independence","state":PASS if oi else FAIL,"failure_or_blocked_state":None if oi else FAILC["order_independence"]})
    states=[x["state"] for x in dims]; overall=FAIL if FAIL in states else BLOCKED if BLOCKED in states else PASS
    return {"overall_state":overall,"source_blockers":sb,"replay_blockers":rb,"dimensions":dims,"logical_source_hash":sh,"logical_replay_hash":rh}

def shuffled_physical_copy(d,seed=13):
    z=copy.deepcopy(d); g=random.Random(seed)
    for k in ("authorities","respondents","eligibility","events","branches","joint_configurations","queries"):g.shuffle(z.get(k,[]))
    return z
def failure_codes(r):return sorted({x.get("failure_or_blocked_state") for x in r.get("dimensions",[]) if x.get("failure_or_blocked_state")})
