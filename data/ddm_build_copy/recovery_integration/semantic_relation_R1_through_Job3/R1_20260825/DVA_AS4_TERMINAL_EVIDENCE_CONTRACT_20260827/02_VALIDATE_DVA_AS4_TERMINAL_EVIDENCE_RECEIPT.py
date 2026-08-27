#!/usr/bin/env python3
"""Fail-closed validator for rawlsing.dva.as4.terminal-evidence-receipt/1.0.0."""
from __future__ import annotations
import argparse, copy, hashlib, json, sys
from pathlib import Path
from typing import Any
from jsonschema import Draft202012Validator

SCHEMA_ID="rawlsing.dva.as4.terminal-evidence-receipt/1.0.0"
VALIDATOR_ID="rawlsing.dva.as4.terminal-evidence-receipt-validator/1.0.0"
B07={"B07_JOINT_CONFIGURATION_SEMANTIC_IDENTITY","B07_SAME_RESPONDENT_JOINT_MEASUREMENT_IDENTITY","B07_COMPONENT_IDENTITY_ORDER_CONTRACT","B07_COMPONENT_MULTIAXIS_AUTHORITY_VECTOR","B07_COMPONENT_ROLES_CERTIFICATION_CONTRIBUTION","B07_NONSCALAR_VECTORS_LAWFUL_SCALARIZATION","B07_DENOMINATOR_CONTEXT_CERTIFICATION_CONTRACT"}
B08={"C5-F01","C5-F02","C5-F04","C5-F05","C5-F06","C5-F09","C5-F10","C5-F13"}
CAPS={"NINE_STRATA_FIELD","INTER_STRATA_PRESSURE_COUNTERPRESSURE","RELATIONAL_SOURCE_TARGET_DIRECTION","TEMPORAL_HISTORY_PERSISTENCE_DRIFT_RUPTURE_LIMITS","CONTRADICTION_COEXISTING_PRESSURE","MEDIATION","BUFFERING_AMPLIFICATION_DEFLECTION_BLOCKAGE_REROUTING","ORIENTATION_TO_STRATA","ABSOLUTE_HORIZON","STRUCTURAL_PRESSURE_FLOW_TOPOLOGY","ATTRACTOR_PREREQUISITES_FORMATION","ACTOR_DEVELOPMENTAL_CAUSALITY","GENEALOGY_PARENT_PARTNER_CHILD_RECURSION","V2_PHENOMENOLOGY_EXPRESSION","EPISTEMIC_CLASS_PROVENANCE","UNCERTAINTY_ABSENCE_NONCOMPARABILITY_FORBIDDEN_INFERENCE"}
ROLES={"SOURCE_SEMANTIC","RAWLSING_SEMANTIC","P10_PRESERVATION","C11","I03","I05","I04","MEASUREMENT","TERMINAL"}
REF_KEYS={"candidate_definition_ref","host_identity_ref","environment_ref","measurement_mechanism_ref","source_locator_ref","decoder_config_ref","common_manifest_ref","completion_law_ref","measurement_manifest_ref","candidate_order_law_ref","typed_nonpositive_law_ref","logical_release_ref","equivalence_oracle_ref","manifest_ref","result_ref","typed_states_ref","discovery_authority_ref","frontier_ref","candidate_results_ref","terminal_state_ref","fixture_or_scope_ref","admission_receipt_ref","replay_manifest_ref","demand_ref","authorized_universe_ref","row_receipt_ref","retention_boundary_ref","persistent_inventory_ref","failure_receipt_ref","ingress_contract_ref","evidence_bundle_ref","current_stage_ref","downstream_owner_ref"}
REF_LIST_KEYS={"evidence_refs","determinant_refs","product_service_refs","artifact_refs","upstream_authority_refs"}

def pth(parts): return "$"+"".join(f"[{x}]" if isinstance(x,int) else f".{x}" for x in parts)
def refs(o,parts=()):
    out=[]
    if isinstance(o,dict):
        for k,v in o.items():
            q=parts+(k,)
            if k in REF_KEYS and v is not None: out.append((pth(q),str(v)))
            elif k in REF_LIST_KEYS and isinstance(v,list): out += [(pth(q+(i,)),str(x)) for i,x in enumerate(v)]
            out += refs(v,q)
    elif isinstance(o,list):
        for i,v in enumerate(o): out += refs(v,parts+(i,))
    return out

def validate(schema:dict[str,Any],r:dict[str,Any])->list[str]:
    e=[f"SCHEMA {pth(x.absolute_path)}: {x.message}" for x in sorted(Draft202012Validator(schema).iter_errors(r),key=lambda x:list(x.absolute_path))]
    objs=r.get("evidence_objects",[]); ids=[x.get("evidence_id") for x in objs if isinstance(x,dict)]; known=set(ids)
    if len(ids)!=len(known): e.append("SEMANTIC $.evidence_objects: duplicate evidence_id")
    for where,ref in refs(r):
        if ref not in known: e.append(f"SEMANTIC {where}: dangling evidence reference {ref!r}")
    bindings=r.get("authority_bindings",[]); roles=set()
    for i,x in enumerate(bindings):
        if isinstance(x,dict):
            roles.add(x.get("role")); ref=x.get("evidence_ref")
            if ref not in known: e.append(f"SEMANTIC $.authority_bindings[{i}].evidence_ref: dangling evidence reference {ref!r}")
    if ROLES-roles: e.append("SEMANTIC $.authority_bindings: missing roles "+",".join(sorted(ROLES-roles)))
    c=r.get("common_workload",{}); i5=r.get("i05",{})
    if c.get("candidate_frontier_count")!=c.get("covered_candidate_count"): e.append("SEMANTIC $.common_workload: frontier not fully covered")
    if i5.get("candidate_frontier_count")!=i5.get("covered_candidate_count"): e.append("SEMANTIC $.i05: frontier not fully covered")
    if c.get("candidate_frontier_count")!=i5.get("candidate_frontier_count"): e.append("SEMANTIC $.i05: frontier differs from common workload")
    k=[x.get("function_key") for x in r.get("b07",{}).get("functions",[]) if isinstance(x,dict)]
    if set(k)!=B07 or len(k)!=7: e.append("SEMANTIC $.b07.functions: exact B07 seven-function set required")
    k=[x.get("function_key") for x in r.get("b08",{}).get("functions",[]) if isinstance(x,dict)]
    if set(k)!=B08 or len(k)!=8: e.append("SEMANTIC $.b08.functions: exact B08 eight-function set required")
    rows=r.get("direct_upstream_reuse",[]); k=[x.get("terminal_capability") for x in rows if isinstance(x,dict)]
    if set(k)!=CAPS or len(k)!=16: e.append("SEMANTIC $.direct_upstream_reuse: exact terminal-capability set required")
    for n,x in enumerate(rows):
        if isinstance(x,dict) and x.get("disposition")=="DIRECT_UPSTREAM_REUSE_SUFFICIENT" and not x.get("upstream_authority_refs"): e.append(f"SEMANTIC $.direct_upstream_reuse[{n}]: direct reuse lacks authority refs")
        if isinstance(x,dict) and x.get("disposition")=="MISSING_AUTHORITY" and x.get("current_stage_ref"): e.append(f"SEMANTIC $.direct_upstream_reuse[{n}]: missing authority cannot claim current-stage meaning")
    for n,x in enumerate(r.get("nonpositive_records",[])):
        if not isinstance(x,dict): continue
        kind=x.get("state_kind")
        if kind in {"PROVEN_NEGATIVE","COMPLETE_AUTHORIZED_SEARCH__NO_RELATION_FOUND"} and x.get("search_complete") is not True: e.append(f"SEMANTIC $.nonpositive_records[{n}]: complete negative requires complete search")
        if kind in {"PARTIAL_FRONTIER","BUDGET_EXHAUSTED","BLOCKED_MISSING_AUTHORITY","UNKNOWN"} and x.get("search_complete") is True: e.append(f"SEMANTIC $.nonpositive_records[{n}]: incomplete state cannot claim complete search")
    t=r.get("terminal_vision",{})
    if t.get("state",{}).get("status")=="PASS" and t.get("covered_row_count")!=t.get("required_row_count"): e.append("SEMANTIC $.terminal_vision: PASS requires 34/34")
    v=r.get("handoff",{}).get("v553_plus",{})
    if v.get("state",{}).get("status")=="PASS" and v.get("unchanged") is not True: e.append("SEMANTIC $.handoff.v553_plus: PASS requires unchanged=true")
    f=r.get("final_integrity",{})
    if f.get("receipt_validation_state",{}).get("status")!="PASS": e.append("SEMANTIC $.final_integrity: receipt validation must PASS")
    if f.get("validator_id")!=VALIDATOR_ID: e.append("SEMANTIC $.final_integrity.validator_id: wrong validator")
    return e

def sh(s): return hashlib.sha256(s.encode()).hexdigest()
def ev(i,kind="RECEIPT"): return {"evidence_id":i,"kind":kind,"locator":"fixture://"+i,"content_sha256":sh(i)}
def cl(ref="E.G"): return {"status":"PASS","evidence_refs":[ref]}
def ex(status="PASS",ref="E.G"): return {"status":status,"exercised":status in {"PASS","FAIL","EXECUTION_FAILED"},"evidence_refs":[ref]}
def pr(ref,reopen): return {"status":"PRESERVED_AS_EXACT_UNRESOLVED/BLOCKED_AUTHORITY","evidence_refs":[ref],"reopen_condition":reopen}

def fixture(schema):
    names={"CAND.DEF","HOST","ENV","MEASURE","SOURCE.LOC","DECODER.CFG","MANIFEST","COMPLETE","MMAN","ORDER","NPLAW","C11.REL","C11.ORACLE","I03.MAN","I03.RES","I03.TYPED","DISC.AUTH","FRONTIER","I05.RES","I05.TERM","I04.FIX","I04.ADM","REPLAY","PREV3","V553","TROWS","RETENTION","PINV","FAILREC","BUNDLE","E.G","AUTH.SOURCE","AUTH.RAWLSING","AUTH.P10","AUTH.C11","AUTH.I03","AUTH.I05","AUTH.I04","AUTH.MEASURE","AUTH.TERMINAL"}
    auth=[("SOURCE_SEMANTIC","AUTH.SOURCE"),("RAWLSING_SEMANTIC","AUTH.RAWLSING"),("P10_PRESERVATION","AUTH.P10"),("C11","AUTH.C11"),("I03","AUTH.I03"),("I05","AUTH.I05"),("I04","AUTH.I04"),("MEASUREMENT","AUTH.MEASURE"),("TERMINAL","AUTH.TERMINAL")]
    b07=[{"function_key":k,"governed_function":k,"preservation":pr("AUTH.P10","prove DIRECT_REUSE, PERSIST, or EXACT_DERIVATION"),"exercise":ex("NOT_EXERCISED_BY_THIS_BENCHMARK","AUTH.P10"),"consumer_disposition":"UNRESOLVED_GOVERNED_OBLIGATION"} for k in sorted(B07)]
    b08=[{"function_key":k,"governed_function":k,"preservation":pr("AUTH.P10","later selected architecture proves owner/executor witness"),"exercise":ex("NOT_EXERCISED_BY_THIS_BENCHMARK","AUTH.P10"),"consumer_disposition":"UNRESOLVED_GOVERNED_OBLIGATION"} for k in sorted(B08)]
    rr=[{"terminal_capability":k,"disposition":"PRESERVE_BY_REFERENCE","upstream_authority_refs":["AUTH.TERMINAL"],"evidence_refs":["AUTH.TERMINAL"]} for k in sorted(CAPS)]
    ms={}
    for k in schema["properties"]["resource_lifecycle"]["required"]: ms[k]={"status":"MEASURED","value":1,"unit":"count","evidence_refs":["MEASURE"]}
    lw={k:ex("NOT_EXERCISED_BY_THIS_BENCHMARK","MANIFEST") for k in ["candidate_discovery_validation_transition","accepted_empirical_relation_release_provenance","higher_order_joint_multimodal_capability","source_universe_time_indexed_selection","positioned_subject_empirical_inference","explanation_lineage_reconstruction","adaptive_discovery_replay"]}; lw["product_service_refs"]=[]
    return {"schema_id":SCHEMA_ID,"schema_version":"1.0.0","receipt_id":"SELFTEST","candidate":{"candidate_id":"FIX","candidate_definition_ref":"CAND.DEF","implementation_commit_sha":"1"*40},"execution":{"run_id":"R","host_identity_ref":"HOST","environment_ref":"ENV","measurement_mechanism_ref":"MEASURE","fresh_process":True,"concurrent_candidate_execution":False},"source":{"source_id":"S","source_sha256":"2"*64,"exact_bytes_verified":True,"source_locator_ref":"SOURCE.LOC","decoder_identity":"fixture","decoder_config_ref":"DECODER.CFG"},"evidence_objects":[ev(x,"AUTHORITY" if x.startswith("AUTH.") else "RECEIPT") for x in sorted(names)],"authority_bindings":[{"authority_id":"A_"+role,"role":role,"evidence_ref":ref,"authority_ceiling":"fixture"} for role,ref in auth],"common_workload":{"common_manifest_ref":"MANIFEST","discovery_authority_sha256":"3"*64,"official_frontier_sha256":"4"*64,"candidate_frontier_count":82,"covered_candidate_count":82,"no_pruning":True,"completion_law_ref":"COMPLETE","measurement_manifest_ref":"MMAN","candidate_order_law_ref":"ORDER","typed_nonpositive_law_ref":"NPLAW"},"c11":{"state":cl("C11.REL"),"logical_release_ref":"C11.REL","equivalence_oracle_ref":"C11.ORACLE","observable_parity_sha256":"5"*64,"fresh_process_parity":ex("PASS","C11.ORACLE")},"i03":{"state":cl("I03.RES"),"manifest_ref":"I03.MAN","result_ref":"I03.RES","typed_states_ref":"I03.TYPED","fresh_process_parity":ex("PASS","I03.RES")},"i05":{"primitive":ex("PASS","I05.RES"),"discovery_program":ex("PASS","I05.RES"),"semantic_identity_parity":cl("I05.RES"),"discovery_authority_ref":"DISC.AUTH","frontier_ref":"FRONTIER","candidate_results_ref":"I05.RES","terminal_state_ref":"I05.TERM","candidate_frontier_count":82,"covered_candidate_count":82,"no_pruning":True},"i04":{"state":ex("PASS","I04.ADM"),"fixture_or_scope_ref":"I04.FIX","admission_receipt_ref":"I04.ADM"},"nonpositive_records":[{"record_id":"NP","subject_ref":"X","state_kind":"COMPLETE_AUTHORIZED_SEARCH__NO_RELATION_FOUND","search_complete":True,"authorized_universe_ref":"FRONTIER","completion_law_ref":"COMPLETE","evidence_refs":["I05.TERM"]}],"provenance_replay":{"replay_manifest_ref":"REPLAY","replay_closure_sha256":"6"*64,"determinant_refs":["SOURCE.LOC","DECODER.CFG","DISC.AUTH","FRONTIER"],"deterministic_replay":ex("PASS","REPLAY"),"fresh_process_parity":ex("PASS","REPLAY"),"audit_replay":ex("PASS","REPLAY"),"delete_reconstruct_replay":ex("PASS","REPLAY")},"b07":{"functions":b07},"b08":{"functions":b08},"learned_world":lw,"handoff":{"pre_v3":{"state":cl("PREV3"),"artifact_refs":["PREV3"]},"v553_plus":{"state":cl("V553"),"ingress_contract_ref":"V553","unchanged":True}},"terminal_vision":{"checksum_id":"VC4_TERMINAL_VISION_CHECKSUM","required_row_count":34,"covered_row_count":34,"state":ex("PASS","TROWS"),"checksum_sha256":"7"*64,"row_receipt_ref":"TROWS"},"persistence_regeneration":{"retention_boundary_ref":"RETENTION","persistent_inventory_ref":"PINV","regeneration":ex("PASS","PINV"),"stale_corrupt_fail_closed":ex("PASS","PINV"),"delete_all_regenerable_state":ex("PASS","PINV"),"no_hidden_persistence":ex("PASS","PINV"),"authority_reachability_after_deletion":ex("PASS","PINV"),"cache_schema_blind_api":ex("PASS","PINV")},"failure_recovery":{"interrupted_build":ex("PASS","FAILREC"),"cleanup_after_success":ex("PASS","FAILREC"),"cleanup_after_failure":ex("PASS","FAILREC"),"reopen_after_failure":ex("PASS","FAILREC"),"failure_receipt_ref":"FAILREC"},"direct_upstream_reuse":rr,"transformed_persistence_authority":{"PERSISTENT_EMPIRICAL_LEARNED_PRODUCT":{"authority_class":"GOVERNED_DERIVED_LEARNED_PRODUCT","evidence_refs":["AUTH.RAWLSING"]},"PERSISTENT_STRUCTURAL_LEARNED_PRODUCT":{"authority_class":"GOVERNED_DERIVED_LEARNED_PRODUCT","evidence_refs":["AUTH.RAWLSING"]},"PERSISTENT_CANONICAL_EMPIRICAL_CARRIER":{"authority_class":"OPERATIONALLY_RETAINED_REGENERABLE_REPRESENTATION","evidence_refs":["PINV"]},"PERSISTENT_REGENERABLE_CACHE":{"authority_class":"OPTIONAL_CACHE","evidence_refs":["PINV"]}},"resource_lifecycle":ms,"final_integrity":{"receipt_validation_state":cl("BUNDLE"),"validator_id":VALIDATOR_ID,"evidence_bundle_ref":"BUNDLE"}}

def selftest(schema):
    base=fixture(schema); cases=[("valid_base",base,True)]
    x=copy.deepcopy(base); del x["source"]["source_sha256"]; cases.append(("missing_source_sha",x,False))
    x=copy.deepcopy(base); x["c11"]["state"]["evidence_refs"]=[]; cases.append(("fake_pass_without_evidence",x,False))
    x=copy.deepcopy(base); x["b07"]["functions"][0]["exercise"]={"status":"PASS","exercised":False,"evidence_refs":["AUTH.P10"]}; cases.append(("nonexercise_conflated_as_pass",x,False))
    x=copy.deepcopy(base); x["i04"]["state"]={"status":"BLOCKED_MISSING_AUTHORITY","exercised":False,"evidence_refs":["I04.ADM"],"authority_gap":{"required_authority_id":"X","demand_ref":"AUTH.I04","reopen_condition":"recover"},"execution_failure":{"failure_class":"runtime","phase":"i04","evidence_refs":["I04.ADM"]}}; cases.append(("missing_authority_conflated_with_execution_failure",x,False))
    x=copy.deepcopy(base); x["nonpositive_records"][0]["search_complete"]=False; cases.append(("fake_negative_without_complete_search",x,False))
    x=copy.deepcopy(base); x["provenance_replay"]["determinant_refs"].append("DOES.NOT.EXIST"); cases.append(("dangling_exact_ref",x,False))
    x=copy.deepcopy(base); x["i05"]["covered_candidate_count"]=81; cases.append(("frontier_coverage_mismatch",x,False))
    x=copy.deepcopy(base); x["direct_upstream_reuse"]=x["direct_upstream_reuse"][:-1]; cases.append(("missing_terminal_capability_disposition",x,False))
    bad=0
    for name,r,want in cases:
        ok=not validate(schema,r); expected=ok==want; print(f"{name}: {'PASS' if ok else 'FAIL_CLOSED'} ({'EXPECTED' if expected else 'UNEXPECTED'})"); bad += 0 if expected else 1
    print(f"SELF_TEST_RESULT: {len(cases)-bad}/{len(cases)} expected outcomes"); return 1 if bad else 0

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("receipt",nargs="?"); ap.add_argument("--schema",default=str(Path(__file__).with_name("01_DVA_AS4_TERMINAL_EVIDENCE_RECEIPT.schema.json"))); ap.add_argument("--self-test",action="store_true"); a=ap.parse_args()
    s=json.loads(Path(a.schema).read_text()); Draft202012Validator.check_schema(s)
    if s.get("$id")!="urn:rawlsing:dva:as4:terminal-evidence-receipt:1.0.0": return 2
    if a.self_test: return selftest(s)
    if not a.receipt: ap.error("receipt required unless --self-test")
    e=validate(s,json.loads(Path(a.receipt).read_text()))
    if e: print("INVALID"); print("\n".join(e)); return 1
    print("VALID"); return 0
if __name__=="__main__": raise SystemExit(main())
