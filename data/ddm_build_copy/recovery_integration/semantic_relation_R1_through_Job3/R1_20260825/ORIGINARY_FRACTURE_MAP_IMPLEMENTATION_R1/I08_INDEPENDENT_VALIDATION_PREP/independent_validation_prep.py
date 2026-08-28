#!/usr/bin/env python3
"""I08 merge-independent Authority-37 anti-cheat/replay validator prep.
No rawlsing_next or I01-I07 imports. HQ supplies a normalized post-merge bundle.
"""
import copy, hashlib, json

CONTRACT="I08_INDEPENDENT_VALIDATION_CONTRACT@1.0.0"
NO_PRUNE="NONE_EXACT_EVALUATE_ALL"
HANDOFF="EXACT_HANDOFF_REPLAY"
J3_SOURCE="EXACT_SAME_RESPONDENT_JOINT"
CALLER_FORBIDDEN={"modal_response","modal_pattern","primary_predictor","predictor_winner","branch_members","branch_membership","secondary_splitter","grandchild_path","cotravel_targets","cosignature_targets","target_pair","target_triple"}
ACTOR_FORBIDDEN={"actor_belief","actor_state","personality","personality_label","persona","persona_label","v3_state","v3_person","causal_actor_label"}
P_SPECIAL={"MISSING","NOT_APPLICABLE","INAPPLICABLE","UNKNOWN","NOT_ASKED","UNRESOLVED","UNAVAILABLE"}
R_SPECIAL={"DK","DONT_KNOW","REFUSED","REFUSAL","MISSING","NOT_APPLICABLE","INAPPLICABLE","UNKNOWN","NOT_ASKED","UNAVAILABLE"}

def h(refs):
    b=json.dumps({"candidate_refs":sorted(map(str,refs))},sort_keys=True,separators=(",",":")).encode()
    return hashlib.sha256(b).hexdigest()
def fail(code,path,detail=""): return {"code":code,"path":path,"detail":detail}
def walk(v,path="$"):
    if isinstance(v,dict):
        for k,x in v.items():
            p=f"{path}.{k}"; yield p,k,x; yield from walk(x,p)
    elif isinstance(v,list):
        for i,x in enumerate(v): yield from walk(x,f"{path}[{i}]")

def validate(b):
    out=[]
    if b.get("contract_version")!=CONTRACT: out.append(fail("CONTRACT_VERSION_MISMATCH","$.contract_version"))
    for p,k,v in walk(b.get("caller_request",{}),"$.caller_request"):
        if k in CALLER_FORBIDDEN and v not in (None,"",[],{}): out.append(fail("CALLER_ORACLE_LEAKAGE",p,k))
    catalog=b.get("lawful_candidate_catalog",{})
    for i,g in enumerate(b.get("generations",[])):
        p=f"$.generations[{i}]"; fr=g.get("frontier",{}); declared=list(map(str,fr.get("declared_candidate_refs",[]))); ds=set(declared); seal=fr.get("seal_event_index")
        if fr.get("sealed_hash")!=h(declared): out.append(fail("FRONTIER_SEAL_MISMATCH",p+".frontier"))
        if not isinstance(seal,int): out.append(fail("FRONTIER_NOT_PRESEALED",p+".frontier")); seal=-1
        for m in g.get("frontier_mutation_events",[]):
            if isinstance(m.get("event_index"),int) and m["event_index"]>=seal: out.append(fail("OPEN_FRONTIER_MUTATION",p+".frontier_mutation_events"))
        evaluated=[]
        for e in g.get("evaluation_events",[]):
            c=str(e.get("candidate_ref","")); evaluated.append(c)
            if isinstance(e.get("event_index"),int) and e["event_index"]<=seal: out.append(fail("EVALUATION_BEFORE_FRONTIER_SEAL",p+".evaluation_events"))
            if c not in ds: out.append(fail("UNDECLARED_CANDIDATE_EVALUATED",p+".evaluation_events",c))
        pr=g.get("pruning",{})
        if pr.get("mode")!=NO_PRUNE: out.append(fail("FORBIDDEN_PRUNING_MODE",p+".pruning.mode"))
        if pr.get("removed_candidate_refs"): out.append(fail("FORBIDDEN_CANDIDATE_PRUNING",p+".pruning.removed_candidate_refs"))
        lawful=set(map(str,catalog.get(str(g.get("node_ref","")),[])))
        if lawful!=ds: out.append(fail("INCOMPLETE_LAWFUL_FRONTIER",p+".frontier"))
        if sorted(evaluated)!=sorted(declared): out.append(fail("INCOMPLETE_FRONTIER_EVALUATION",p+".evaluation_events"))
    branches=b.get("branches",[])
    for i,br in enumerate(branches):
        p=f"$.branches[{i}]"; pred=br.get("predicate",{})
        if pred.get("not_predictor") is True:
            if not pred.get("resolved_coordinate_guard_ref"): out.append(fail("NOT_P_WITHOUT_RESOLVED_COORDINATE_GUARD",p+".predicate"))
            if {str(x).upper() for x in pred.get("included_predictor_special_states",[])} & P_SPECIAL: out.append(fail("NOT_P_SWALLOWS_PREDICTOR_MISSINGNESS",p+".predicate"))
        if str(pred.get("response_partition","")).upper()=="NM":
            if {str(x).upper() for x in pred.get("included_response_special_states",[])} & R_SPECIAL: out.append(fail("NM_SWALLOWS_TYPED_NONRESPONSE",p+".predicate"))
            if not pred.get("substantive_nonmodal_patterns"): out.append(fail("NM_NOT_EXPLICIT_SUBSTANTIVE_SET",p+".predicate"))
        if br.get("membership_source")!=HANDOFF or not br.get("handoff_ref"): out.append(fail("PRIVATE_BRANCH_MEMBERSHIP_RECONSTRUCTION",p))
        disp=br.get("continuation",{}).get("disposition")
        if disp in {"RETAIN_REPORT_ONLY_STOP","RETAIN_TERMINAL_STOP","RETAIN_TYPED_NONPOSITIVE_STOP"}:
            if not br.get("retained"): out.append(fail("STOPPED_BRANCH_RETENTION_LOSS",p))
            if not br.get("continuation",{}).get("stop_reason"): out.append(fail("STOP_WITHOUT_EXACT_REASON",p))
    retained=set(map(str,b.get("public_map",{}).get("retained_branch_refs",[])))
    for br in branches:
        if br.get("retained") and str(br.get("branch_ref")) not in retained: out.append(fail("PUBLIC_MAP_DROPS_RETAINED_BRANCH","$.public_map"))
    for i,t in enumerate(b.get("topology",[])):
        p=f"$.topology[{i}]"; ar=t.get("arity")
        if ar==3:
            if len(t.get("target_refs",[]))!=3: out.append(fail("J3_TARGET_ARITY_MISMATCH",p))
            if t.get("source_kind")!=J3_SOURCE or t.get("derived_from_pairwise_only") is True: out.append(fail("PAIRWISE_PROJECTION_MISLABELED_J3",p))
            if not t.get("joint_fact_refs"): out.append(fail("J3_WITHOUT_DIRECT_JOINT_FACT",p))
        if isinstance(ar,int) and ar>3: out.append(fail("ARITY_EXCEEDS_AUTHORITY37",p))
    for p,k,v in walk(b):
        if k in ACTOR_FORBIDDEN and v not in (None,"",[],{}): out.append(fail("ACTOR_V3_PERSONALITY_LEAKAGE",p,k))
    if b.get("jurisdiction",{}).get("output_layer") not in (None,"EMPIRICAL"): out.append(fail("ACTOR_V3_PERSONALITY_LEAKAGE","$.jurisdiction"))
    return out

def identity(b): return {"frontier":b.get("identity",{}).get("frontier_identities",{}),"map":b.get("identity",{}).get("map_identity"),"replay":b.get("identity",{}).get("replay_identity"),"artifacts":b.get("artifact_identities",{})}
def replay(a,b):
    if a.get("determinant_values")!=b.get("determinant_values"): return [fail("REPLAY_INPUTS_DIFFER","$.determinant_values")]
    if a.get("authority_identity")!=b.get("authority_identity"): return [fail("REPLAY_AUTHORITY_DIFFERS","$.authority_identity")]
    return [] if identity(a)==identity(b) else [fail("NONDETERMINISTIC_REPLAY_IDENTITY","$.identity")]
def closure(graph,art):
    seen=set(); stack=list(graph.get(art,[]))
    while stack:
        d=str(stack.pop())
        if d in seen: continue
        seen.add(d); stack.extend(map(str,graph.get(d,[])))
    return seen
def mutation(a,b,changed):
    if a.get("dependency_graph",{})!=b.get("dependency_graph",{}): return [fail("DEPENDENCY_GRAPH_MUTATED_DURING_METAMORPHIC_TEST","$.dependency_graph")]
    graph=a.get("dependency_graph",{}); changed=set(map(str,changed)); ai=a.get("artifact_identities",{}); bi=b.get("artifact_identities",{}); out=[]
    for art in sorted(set(ai)|set(bi)):
        relevant=bool(closure(graph,art)&changed); same=ai.get(art)==bi.get(art)
        if not relevant and not same: out.append(fail("IRRELEVANT_DETERMINANT_INVALIDATED_UNRELATED_TOPOLOGY",f"$.artifact_identities.{art}"))
        if relevant and same: out.append(fail("RELEVANT_DETERMINANT_FAILED_TO_INVALIDATE_DESCENDANT",f"$.artifact_identities.{art}"))
    return out

def good():
    c=["P0","P1","Q0","Q1"]; sh=h(c)
    branches=[
      {"branch_ref":"B:DEV","parent_ref":"ROOT","predicate":{"not_predictor":False,"resolved_coordinate_guard_ref":"CR:P","response_partition":"NM","substantive_nonmodal_patterns":["A_ONLY","B_ONLY","NONE"],"included_response_special_states":[],"included_predictor_special_states":[]},"membership_source":HANDOFF,"handoff_ref":"H:DEV","retained":True,"continuation":{"disposition":"RETAIN_AND_CONTINUE_ELIGIBLE","stop_reason":None}},
      {"branch_ref":"B:ALT","parent_ref":"ROOT","predicate":{"not_predictor":True,"resolved_coordinate_guard_ref":"CR:P","response_partition":"M","included_response_special_states":[],"included_predictor_special_states":[]},"membership_source":HANDOFF,"handoff_ref":"H:ALT","retained":True,"continuation":{"disposition":"RETAIN_TERMINAL_STOP","stop_reason":"MAX_DEPTH"}},
      {"branch_ref":"B:DEV:Q1","parent_ref":"B:DEV","predicate":{"not_predictor":False,"resolved_coordinate_guard_ref":"CR:Q","response_partition":"NM","substantive_nonmodal_patterns":["A_ONLY"],"included_response_special_states":[],"included_predictor_special_states":[]},"membership_source":HANDOFF,"handoff_ref":"H:Q1","retained":True,"continuation":{"disposition":"RETAIN_REPORT_ONLY_STOP","stop_reason":"LOW_N"}}]
    return {"contract_version":CONTRACT,"authority_identity":"AUTH37:V1","caller_request":{"root_query_ref":"TARGET","scope_ref":"HOSTILE","provided_hints":{}},"lawful_candidate_catalog":{"ROOT":c},"generations":[{"node_ref":"ROOT","frontier":{"declared_candidate_refs":c,"sealed_hash":sh,"seal_event_index":10},"frontier_mutation_events":[],"evaluation_events":[{"event_index":11+i,"candidate_ref":x} for i,x in enumerate(c)],"pruning":{"mode":NO_PRUNE,"removed_candidate_refs":[]}}],"branches":branches,"topology":[{"arity":3,"target_refs":["X","Y","Z"],"source_kind":J3_SOURCE,"joint_fact_refs":["J3:X:Y:Z"],"derived_from_pairwise_only":False}],"public_map":{"retained_branch_refs":[x["branch_ref"] for x in branches]},"jurisdiction":{"output_layer":"EMPIRICAL"},"determinant_values":{"TARGET":"v1","P":"v1","Q":"v1","R":"0","S":"v1"},"dependency_graph":{"ROOT":["TARGET"],"P_TOPO":["TARGET","P"],"Q_CHILD":["P_TOPO","Q"],"S_CHILD":["Q_CHILD","S"],"R_TOPO":["TARGET","R"],"COSIG":["Q_CHILD"],"J3":["TARGET"]},"artifact_identities":{"ROOT":"r1","P_TOPO":"p1","Q_CHILD":"q1","S_CHILD":"s1","R_TOPO":"rr1","COSIG":"c1","J3":"j1"},"identity":{"frontier_identities":{"ROOT":sh},"map_identity":"m1","replay_identity":"rp1"}}
def selftest():
    checks=[]; g=good(); checks.append(("good",not validate(g)))
    for k,v in [("modal_pattern","A+B"),("primary_predictor","P"),("branch_members",["R1"]),("secondary_splitter","Q"),("grandchild_path",["P","Q","S"]),("cotravel_targets",["C1","C2"])]:
        x=copy.deepcopy(g); x["caller_request"]["provided_hints"][k]=v; checks.append(("leak_"+k,"CALLER_ORACLE_LEAKAGE" in {z["code"] for z in validate(x)}))
    x=copy.deepcopy(g); x["generations"][0]["frontier_mutation_events"]=[{"event_index":12}]; checks.append(("frontier_mutation","OPEN_FRONTIER_MUTATION" in {z["code"] for z in validate(x)}))
    x=copy.deepcopy(g); x["generations"][0]["frontier"]["declared_candidate_refs"]=["P0","P1"]; x["generations"][0]["frontier"]["sealed_hash"]=h(["P0","P1"]); x["generations"][0]["evaluation_events"]=[{"event_index":11,"candidate_ref":"P0"},{"event_index":12,"candidate_ref":"P1"}]; x["generations"][0]["pruning"]={"mode":"TOP_K","removed_candidate_refs":["Q0","Q1"]}; codes={z["code"] for z in validate(x)}; checks.append(("pruning",{"FORBIDDEN_PRUNING_MODE","FORBIDDEN_CANDIDATE_PRUNING","INCOMPLETE_LAWFUL_FRONTIER"}<=codes))
    x=copy.deepcopy(g); x["branches"][1]["predicate"].update(resolved_coordinate_guard_ref=None,included_predictor_special_states=["MISSING"]); codes={z["code"] for z in validate(x)}; checks.append(("not_p_missing",{"NOT_P_WITHOUT_RESOLVED_COORDINATE_GUARD","NOT_P_SWALLOWS_PREDICTOR_MISSINGNESS"}<=codes))
    x=copy.deepcopy(g); x["branches"][0]["predicate"]["included_response_special_states"]=["DK","REFUSED"]; checks.append(("nm_special","NM_SWALLOWS_TYPED_NONRESPONSE" in {z["code"] for z in validate(x)}))
    x=copy.deepcopy(g); x["topology"][0].update(source_kind="PAIRWISE_PROJECTION",joint_fact_refs=[],derived_from_pairwise_only=True); codes={z["code"] for z in validate(x)}; checks.append(("fake_j3",{"PAIRWISE_PROJECTION_MISLABELED_J3","J3_WITHOUT_DIRECT_JOINT_FACT"}<=codes))
    x=copy.deepcopy(g); x["branches"][2].update(membership_source="PRIVATE",handoff_ref=None); checks.append(("private_membership","PRIVATE_BRANCH_MEMBERSHIP_RECONSTRUCTION" in {z["code"] for z in validate(x)}))
    x=copy.deepcopy(g); x["branches"][1]["retained"]=False; checks.append(("retention_loss","STOPPED_BRANCH_RETENTION_LOSS" in {z["code"] for z in validate(x)}))
    x=copy.deepcopy(g); x["identity"]["map_identity"]="m2"; checks.append(("nondeterminism","NONDETERMINISTIC_REPLAY_IDENTITY" in {z["code"] for z in replay(g,x)}))
    x=copy.deepcopy(g); x["actor_belief"]="invented"; checks.append(("actor_v3","ACTOR_V3_PERSONALITY_LEAKAGE" in {z["code"] for z in validate(x)}))
    x=copy.deepcopy(g); x["determinant_values"]["R"]="1"; x["artifact_identities"]["R_TOPO"]="rr2"; checks.append(("r_only_noninterference",not mutation(g,x,["R"])))
    y=copy.deepcopy(x); y["artifact_identities"]["Q_CHILD"]="q2"; checks.append(("irrelevant_invalidation","IRRELEVANT_DETERMINANT_INVALIDATED_UNRELATED_TOPOLOGY" in {z["code"] for z in mutation(g,y,["R"])}))
    x=copy.deepcopy(g); x["determinant_values"]["R"]="1"; checks.append(("relevant_not_invalidated","RELEVANT_DETERMINANT_FAILED_TO_INVALIDATE_DESCENDANT" in {z["code"] for z in mutation(g,x,["R"])}))
    failed=[n for n,ok in checks if not ok]; return {"contract_version":CONTRACT,"checks_total":len(checks),"checks_passed":len(checks)-len(failed),"failed_checks":failed,"checks":[{"name":n,"passed":ok} for n,ok in checks]}
if __name__=="__main__":
    r=selftest(); print(json.dumps(r,indent=2,sort_keys=True)); raise SystemExit(bool(r["failed_checks"]))
