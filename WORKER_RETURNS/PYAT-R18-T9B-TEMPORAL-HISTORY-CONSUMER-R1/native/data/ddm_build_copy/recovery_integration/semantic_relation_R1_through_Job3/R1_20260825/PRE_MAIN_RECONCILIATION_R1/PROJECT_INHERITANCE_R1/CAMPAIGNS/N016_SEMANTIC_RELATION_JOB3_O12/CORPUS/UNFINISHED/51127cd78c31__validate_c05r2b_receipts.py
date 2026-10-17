#!/usr/bin/env python3
"""Fail-closed C05R2B receipt validator.

This validator freezes identities and laws only.  Its self-test uses synthetic
non-empirical receipts and MUST NOT be read as a prediction of LiTS-I I05 results.
"""
from __future__ import annotations
import argparse, copy, hashlib, json
from pathlib import Path
from typing import Any

HERE=Path(__file__).resolve().parent
ORACLE=json.loads((HERE/"C05R2B_ACCEPTANCE_ORACLE.json").read_text(encoding="utf-8"))

class ValidationFailure(Exception):
    pass

def _eq(errors, label, got, want):
    if got != want: errors.append(f"{label}: expected {want!r}, got {got!r}")

def _req(errors, obj, fields, label):
    if not isinstance(obj, dict):
        errors.append(f"{label}: expected object")
        return
    for f in fields:
        if f not in obj: errors.append(f"{label}: missing required field {f}")

def _get(obj, path):
    cur=obj
    for p in path.split("."):
        if not isinstance(cur,dict) or p not in cur: return None
        cur=cur[p]
    return cur

def _sha_ref(value):
    return isinstance(value,dict) and isinstance(value.get("content_hash"),str) and len(value["content_hash"])==64

def validate_run(run:dict[str,Any])->list[str]:
    e=[]
    _req(e,run,ORACLE["receipt_contract"]["top_level_required"],"run")
    _eq(e,"source.sha256",_get(run,"source.sha256"),ORACLE["source"]["sha256"])
    _eq(e,"source.rows",_get(run,"source.rows"),ORACLE["source"]["rows"])
    _eq(e,"source.variables",_get(run,"source.variables"),ORACLE["source"]["variables"])
    _eq(e,"source.physical_cells",_get(run,"source.physical_cells"),ORACLE["source"]["physical_cells"])
    _eq(e,"c11.logical_release_ref",_get(run,"c11.logical_release_ref"),ORACLE["c11"]["logical_release_ref"])
    _eq(e,"c11.replay_manifest_ref",_get(run,"c11.replay_manifest_ref"),ORACLE["c11"]["replay_manifest_ref"])
    _eq(e,"as3r2.discovery_authority_ref",_get(run,"as3r2.discovery_authority_ref"),ORACLE["as3r2"]["discovery_authority_ref"])
    _eq(e,"as3r2.official_frontier_ref",_get(run,"as3r2.official_frontier_ref"),ORACLE["as3r2"]["official_frontier_ref"])

    i03=run.get("i03",{})
    _eq(e,"i03.oracle_ref",i03.get("oracle_ref"),ORACLE["i03_common_oracle"]["ref"])
    _eq(e,"i03.operations",i03.get("operations"),ORACLE["i03_common_oracle"]["operations"])

    i04=run.get("i04",{})
    _eq(e,"i04.oracle_ref",i04.get("oracle_ref"),ORACLE["i04_common_typed_nonpositive_target"]["ref"])
    for k in ("admission_decision_state","public_typed_state","positive_pre_v3_structural_product"):
        _eq(e,f"i04.{k}",i04.get(k),ORACLE["i04_common_typed_nonpositive_target"][k])

    i05=run.get("i05",{})
    _req(e,i05,ORACLE["receipt_contract"]["i05_result_required"],"i05")
    _eq(e,"i05.contract_id",i05.get("contract_id"),ORACLE["production_law"]["i05_contract"])
    _eq(e,"i05.discovery_authority_ref",i05.get("discovery_authority_ref"),ORACLE["as3r2"]["discovery_authority_ref"])
    _eq(e,"i05.candidate_grammar_ref",i05.get("candidate_grammar_ref"),ORACLE["as3r2"]["candidate_grammar_ref"])
    _eq(e,"i05.evaluated_frontier_ref",i05.get("evaluated_frontier_ref"),ORACLE["as3r2"]["official_frontier_ref"])
    _eq(e,"i05.coverage_claim",i05.get("coverage_claim"),ORACLE["production_law"]["coverage_claim"])
    _eq(e,"i05.candidate_count",i05.get("candidate_count"),82)
    _eq(e,"i05.covered_candidate_count",i05.get("covered_candidate_count"),82)
    _eq(e,"i05.no_pruning",i05.get("no_pruning"),True)
    _eq(e,"i05.frontier_frozen_before_empirical_evaluation",i05.get("frontier_frozen_before_empirical_evaluation"),True)
    _eq(e,"i05.candidate_addition_count",i05.get("candidate_addition_count"),0)
    _eq(e,"i05.candidate_deletion_count",i05.get("candidate_deletion_count"),0)

    receipts=i05.get("receipts",[])
    if not isinstance(receipts,list):
        e.append("i05.receipts: expected list"); receipts=[]
    if len(receipts)!=82: e.append(f"i05.receipts: expected 82, got {len(receipts)}")
    expected={(c["candidate_id"],c["candidate_hash"]) for c in ORACLE["as3r2"]["candidates"]}
    seen=[]
    terminal=set(ORACLE["production_law"]["terminal_coverage_states"])
    for n,r in enumerate(receipts):
        _req(e,r,ORACLE["receipt_contract"]["discovery_receipt_required"],f"receipt[{n}]")
        if not isinstance(r,dict): continue
        ci=r.get("candidate_identity",{})
        pair=(ci.get("candidate_id"),ci.get("candidate_hash"))
        seen.append(pair)
        if pair not in expected: e.append(f"receipt[{n}]: candidate identity not in frozen frontier")
        if r.get("coverage_state") not in terminal: e.append(f"receipt[{n}]: nonterminal/unknown coverage_state {r.get('coverage_state')!r}")
        if r.get("typed_state")=="UNEVALUATED": e.append(f"receipt[{n}]: UNEVALUATED forbidden by exact-evaluate-all law")
        expected_pairs={
          "EVALUATED_SUPPORTED":{"DISCOVERED_RESULT_SUPPORTED"},
          "EVALUATED_VALID_EMPTY":{"VALID_EMPTY"},
          "EVALUATED_UNDERPOWERED":{"INSUFFICIENT_SUPPORT"},
          "EVALUATED_NONCOMPARABLE":{"NONCOMPARABLE"},
          "EVALUATED_DENIED_BY_EXACT_AUTHORITY":{"PRUNED_BY_AUTHORITY"},
          "EVALUATED_MISSING_OR_CONFLICTING_AUTHORITY":{"COVERAGE_LIMITED"},
        }
        if r.get("typed_state") not in expected_pairs.get(r.get("coverage_state"),set()):
            e.append(f"receipt[{n}]: typed_state/coverage_state mismatch")
        _eq(e,f"receipt[{n}].discovery_authority_ref",r.get("discovery_authority_ref"),ORACLE["as3r2"]["discovery_authority_ref"])
        _eq(e,f"receipt[{n}].evaluated_frontier_ref",r.get("evaluated_frontier_ref"),ORACLE["as3r2"]["official_frontier_ref"])
        _eq(e,f"receipt[{n}].source_release_refs",r.get("source_release_refs"),[ORACLE["c11"]["logical_release_ref"]])
        _eq(e,f"receipt[{n}].exact_query_contract_id",r.get("exact_query_contract_id"),ORACLE["production_law"]["i03_query_contract"])
        for flag in ("diagnostic_score_is_empirical_fact","structural_truth_effect","actor_v3_effect"):
            _eq(e,f"receipt[{n}].{flag}",r.get(flag),False)
        for refname in ("ref","replay_ref","producer_replay_locator_or_reference_root"):
            if not _sha_ref(r.get(refname)): e.append(f"receipt[{n}].{refname}: exact content-hash ref required")
    if len(set(seen))!=len(seen): e.append("i05.receipts: duplicate candidate identity")
    if set(seen)!=expected: e.append("i05.receipts: exact frozen candidate membership mismatch")

    rb=run.get("route_b",{})
    _req(e,rb,ORACLE["receipt_contract"]["route_b_required"],"route_b")
    _eq(e,"route_b.session_boundary",rb.get("session_boundary"),ORACLE["route_b"]["session_boundary"])
    for k,v in ORACLE["route_b"]["required_after_session"].items(): _eq(e,f"route_b.{k}",rb.get(k),v)
    dr=rb.get("delete_reconstruction",{})
    _req(e,dr,ORACLE["receipt_contract"]["delete_reconstruction_required"],"route_b.delete_reconstruction")
    for k in ORACLE["receipt_contract"]["delete_reconstruction_required"]: _eq(e,f"route_b.delete_reconstruction.{k}",dr.get(k),True)

    proc=run.get("process",{})
    _eq(e,"process.fresh_process",proc.get("fresh_process"),True)
    res=run.get("resources",{})
    _req(e,res,ORACLE["receipt_contract"]["resources_required"],"resources")
    opens=res.get("source_opens_high_level")
    dec=res.get("decoder_passes")
    if not isinstance(opens,int) or isinstance(opens,bool) or opens<1: e.append("resources.source_opens_high_level: exact positive integer required")
    if not isinstance(dec,int) or isinstance(dec,bool) or dec<1: e.append("resources.decoder_passes: exact positive integer accounting required")
    _eq(e,"resources.decoder_call",res.get("decoder_call"),ORACLE["source"]["decoder"])
    _eq(e,"resources.persistent_transformed_empirical_payload_bytes",res.get("persistent_transformed_empirical_payload_bytes"),0)
    return e

def validate_pair(a,b):
    e=[f"run1: {x}" for x in validate_run(a)]+[f"run2: {x}" for x in validate_run(b)]
    for path in ORACLE["replay_and_fresh_process"]["exact_semantic_parity_fields"]:
        if _get(a,path)!=_get(b,path): e.append(f"fresh-process parity mismatch: {path}")
    return e

def _ref(kind,seed):
    h=hashlib.sha256(seed.encode()).hexdigest()
    return {"kind":kind,"object_id":f"urn:synthetic:{kind}:sha256:{h}","content_hash":h}

def synthetic_valid_run():
    # Synthetic validator fixture only: NOT an empirical result prediction.
    rec=[]
    for c in ORACLE["as3r2"]["candidates"]:
        seed=c["candidate_hash"]
        rec.append({
          "ref":_ref("DiscoveryResultReceipt@1.0.0","receipt:"+seed),
          "typed_state":"VALID_EMPTY",
          "authority_snapshot_refs":[ORACLE["as3r2"]["discovery_frontier_authority_snapshot_ref"]],
          "dependency_refs":[],
          "producer_replay_locator_or_reference_root":_ref("PRE553_I05_DISCOVERY_REPLAY","replay:"+seed),
          "discovery_authority_ref":ORACLE["as3r2"]["discovery_authority_ref"],
          "candidate_identity":{"candidate_id":c["candidate_id"],"candidate_hash":c["candidate_hash"]},
          "winning_predicate_ref":_ref("EmpiricalPredicate@1.0.0","pred:"+seed),
          "empirical_fact_refs":[_ref("EmpiricalFact@1.0.0","fact:"+seed)],
          "validation_fact_refs":[_ref("EmpiricalFact@1.0.0","fact:"+seed)],
          "coverage_state":"EVALUATED_VALID_EMPTY",
          "evaluated_frontier_ref":ORACLE["as3r2"]["official_frontier_ref"],
          "branch_or_parent_ancestry_refs":[],
          "support_uncertainty_state":{"synthetic_not_empirical":True},
          "replay_ref":_ref("PRE553_I05_DISCOVERY_REPLAY","replay:"+seed),
          "source_release_refs":[ORACLE["c11"]["logical_release_ref"]],
          "exact_query_contract_id":ORACLE["production_law"]["i03_query_contract"],
          "diagnostic_score_is_empirical_fact":False,"structural_truth_effect":False,"actor_v3_effect":False
        })
    return {
      "schema":"C05R2B_ROUTE_B_PRODUCTION_RECEIPT@1.0.0",
      "source":{"sha256":ORACLE["source"]["sha256"],"rows":29002,"variables":1198,"physical_cells":34744396},
      "c11":{"logical_release_ref":ORACLE["c11"]["logical_release_ref"],"replay_manifest_ref":ORACLE["c11"]["replay_manifest_ref"]},
      "as3r2":{"discovery_authority_ref":ORACLE["as3r2"]["discovery_authority_ref"],"official_frontier_ref":ORACLE["as3r2"]["official_frontier_ref"]},
      "i03":{"oracle_ref":ORACLE["i03_common_oracle"]["ref"],"operations":ORACLE["i03_common_oracle"]["operations"]},
      "i04":{"oracle_ref":ORACLE["i04_common_typed_nonpositive_target"]["ref"],"admission_decision_state":"MISSING_STRUCTURAL_ADMISSION_AUTHORITY","public_typed_state":"MISSING_AUTHORITY","positive_pre_v3_structural_product":"NONE"},
      "i05":{"contract_id":ORACLE["production_law"]["i05_contract"],"discovery_authority_ref":ORACLE["as3r2"]["discovery_authority_ref"],"candidate_grammar_ref":ORACLE["as3r2"]["candidate_grammar_ref"],"evaluated_frontier_ref":ORACLE["as3r2"]["official_frontier_ref"],"coverage_claim":ORACLE["production_law"]["coverage_claim"],"candidate_count":82,"covered_candidate_count":82,"receipts":rec,"empirical_fact_refs":[],"valid_empty":True,"replay_ref":_ref("PRE553_I05_FRONTIER_REPLAY","final"),"no_pruning":True,"frontier_frozen_before_empirical_evaluation":True,"candidate_addition_count":0,"candidate_deletion_count":0},
      "route_b":{"session_boundary":ORACLE["route_b"]["session_boundary"],"session_boundary_closed":True,"retained_transformed_empirical_accelerator_count":0,"persistent_transformed_empirical_payload_bytes":0,"persistent_forbidden_survivors":[],"no_hidden_transformed_persistence":True,"delete_reconstruction":{"source_reopened":True,"authority_reloaded":True,"c11_reconstructed":True,"fresh_process_reconstruction":True}},
      "process":{"fresh_process":True},
      "resources":{"source_opens_high_level":4,"source_opens_method":"synthetic validator fixture","decoder_passes":1,"decoder_call":ORACLE["source"]["decoder"],"persistent_transformed_empirical_payload_bytes":0}
    }

def self_test():
    base=synthetic_valid_run()
    cases=[]
    def hostile(name,mut):
        a=copy.deepcopy(base); b=copy.deepcopy(base); mut(a,b)
        errs=validate_pair(a,b)
        if not errs: raise ValidationFailure(name+" unexpectedly passed")
        cases.append({"id":name,"status":"PASS","observed_failures":len(errs)})
    if validate_pair(base,copy.deepcopy(base)): raise ValidationFailure("synthetic valid control failed")
    hostile("H01_WRONG_SOURCE",lambda a,b:a["source"].__setitem__("sha256","0"*64))
    hostile("H02_WRONG_DISCOVERY_AUTHORITY",lambda a,b:a["as3r2"].__setitem__("discovery_authority_ref",_ref("DiscoveryAuthority@1.0.0","wrong")))
    hostile("H03_WRONG_OFFICIAL_FRONTIER",lambda a,b:a["i05"].__setitem__("evaluated_frontier_ref",_ref("PRE553_I05_EVALUATED_FRONTIER","wrong")))
    hostile("H04_MISSING_OR_SUBSTITUTED_CANDIDATE",lambda a,b:a["i05"]["receipts"].pop())
    hostile("H05_CORRUPT_OR_INCOMPLETE_DISCOVERY_RECEIPT",lambda a,b:a["i05"]["receipts"][0].pop("replay_ref"))
    hostile("H06_FRESH_PROCESS_SEMANTIC_MISMATCH",lambda a,b:b["i05"]["receipts"][0].__setitem__("typed_state","NONCOMPARABLE"))
    hostile("H07_WRONG_AS2B_REPLAY_MANIFEST",lambda a,b:a["c11"].__setitem__("replay_manifest_ref",_ref("ReplayManifest","wrong")))
    hostile("H08_HIDDEN_TRANSFORMED_PERSISTENCE",lambda a,b:a["route_b"].__setitem__("persistent_transformed_empirical_payload_bytes",1))
    hostile("H09_I04_POSITIVE_AUTHORITY_MANUFACTURE",lambda a,b:a["i04"].__setitem__("positive_pre_v3_structural_product","SYNTHETIC_FORBIDDEN_POSITIVE"))
    hostile("H10_UNEVALUATED_OR_NONTERMINAL_CANDIDATE",lambda a,b:a["i05"]["receipts"][0].__setitem__("coverage_state","UNEVALUATED"))
    return {"schema":"C05R2B_HOSTILE_VALIDATOR_SELF_TEST@1.0.0","status":"PASS","synthetic_only":True,"cases":cases}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--run1",type=Path); p.add_argument("--run2",type=Path); p.add_argument("--self-test",action="store_true")
    a=p.parse_args()
    if a.self_test:
        print(json.dumps(self_test(),indent=2,sort_keys=True)); return 0
    if not a.run1 or not a.run2: p.error("--run1 and --run2 required unless --self-test")
    r1=json.loads(a.run1.read_text()); r2=json.loads(a.run2.read_text())
    errs=validate_pair(r1,r2)
    print(json.dumps({"status":"PASS" if not errs else "FAIL","errors":errs},indent=2,sort_keys=True))
    return 0 if not errs else 2
if __name__=="__main__": raise SystemExit(main())
