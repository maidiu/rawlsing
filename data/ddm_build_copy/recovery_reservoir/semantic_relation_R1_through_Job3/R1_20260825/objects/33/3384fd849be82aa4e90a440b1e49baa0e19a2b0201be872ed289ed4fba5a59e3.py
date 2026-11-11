#!/usr/bin/env python3
import argparse, pandas as pd, json, sys
from pathlib import Path

PROHIB="NO_LEXICAL_TOPIC_DRIVER_FACET_OR_COPRESENCE_AUTHORITY"
POS_CEIL="WORKER_RECOMMENDATION__POSITIVE_T06_RELATION__VOZHD_RECONCILIATION_REQUIRED"
NEG_CEIL="WORKER_RECOMMENDATION__EXACT_OPPORTUNITY_NEGATIVE_T06_RELATION_ONLY__NO_BROADER_RELATION_ABSENCE"
BLK_CEIL="WORKER_BLOCKED__NO_T06_RELATION_AUTHORITY__VOZHD_REQUIRED"
MATCH={"MATCH","MISMATCH","UNKNOWN"}
REL={"POSITIVE_T06_RELATION","NEGATIVE_T06_RELATION","BLOCKED_NEEDS_VOZHD"}
NCD={"EXPLICIT_ACTOR_TARGET_ACTION","NO_EXPECTED_CONDUCT_CONTRACT","AMBIGUOUS_NEEDS_VOZHD"}
CONF={"HIGH","MEDIUM","LOW"}

def die(msg):
    print("FAIL:",msg); sys.exit(2)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--pack-root",required=True)
    ap.add_argument("--return-dir",required=True)
    a=ap.parse_args()
    root=Path(a.pack_root); ret=Path(a.return_dir)
    assign=pd.read_csv(root/"ASSIGNMENT/C4_OPPORTUNITIES.csv.gz",dtype=str).fillna("")
    ct0=pd.read_csv(root/"ASSIGNMENT/NORM_CONTRACT_TEMPLATE.csv",dtype=str).fillna("")
    rr=pd.read_csv(ret/"C4_WORKER_RETURN.csv.gz",dtype=str).fillna("")
    ct=pd.read_csv(ret/"NORM_CONTRACT_RETURN.csv",dtype=str).fillna("")
    pl=pd.read_csv(ret/"PROPAGATION_RULE_LEDGER.csv",dtype=str).fillna("")

    if len(rr)!=len(assign): die(f"return rows {len(rr)} != assigned {len(assign)}")
    if rr.opportunity_id.duplicated().any(): die("duplicate opportunity_id")
    if set(rr.opportunity_id)!=set(assign.opportunity_id): die("opportunity partition mismatch")
    immutable=["opportunity_id","source_family","wave","semantic_unit_id","norm_contract_id",
               "endpoint_implementation_id","endpoint_source_variable_code","endpoint_exact_question_text",
               "endpoint_class","endpoint_actor","endpoint_target","endpoint_action_or_exposure"]
    z=assign[immutable].merge(rr[immutable],on="opportunity_id",suffixes=("_a","_r"))
    for c in immutable[1:]:
        if (z[c+"_a"]!=z[c+"_r"]).any(): die("immutable mutation: "+c)

    if len(ct)!=len(ct0) or ct.norm_contract_id.duplicated().any() or set(ct.norm_contract_id)!=set(ct0.norm_contract_id):
        die("norm contract identity mismatch")
    cimm=["norm_contract_id","source_family","wave","semantic_unit_id","norm_source_variable_code",
          "norm_exact_question_text","norm_semantic_summary","norm_measured_predicate","norm_positive_authority_origin"]
    zc=ct0[cimm].merge(ct[cimm],on="norm_contract_id",suffixes=("_a","_r"))
    for c in cimm[1:]:
        if (zc[c+"_a"]!=zc[c+"_r"]).any(): die("norm immutable mutation: "+c)
    mutable_contract=["norm_contract_disposition","norm_actor","norm_target","norm_action","norm_modality_or_operator","contract_basis","contract_confidence"]
    if (ct[mutable_contract]=="").any().any(): die("blank norm contract mutable field")
    if not set(ct.norm_contract_disposition)<=NCD: die("bad norm_contract_disposition")
    if not set(ct.contract_confidence)<=CONF: die("bad contract_confidence")

    rmut=["relation_disposition","actor_match","target_match","action_domain_match","adjudication_basis",
          "authority_ceiling","prohibited_inference_ack","manual_review_flag","worker_confidence"]
    if (rr[rmut]=="").any().any(): die("blank opportunity mutable field")
    if not set(rr.relation_disposition)<=REL: die("bad relation disposition")
    for c in ["actor_match","target_match","action_domain_match"]:
        if not set(rr[c])<=MATCH: die("bad match value "+c)
    if not set(rr.worker_confidence)<=CONF: die("bad worker_confidence")
    if not set(rr.manual_review_flag.str.lower())<= {"true","false"}: die("bad manual_review_flag")
    if (rr.prohibited_inference_ack!=PROHIB).any(): die("prohibited inference ack mismatch")

    rj=rr.merge(ct[["norm_contract_id","norm_contract_disposition"]],on="norm_contract_id",validate="many_to_one")
    for _,r in rj.iterrows():
        ms=[r.actor_match,r.target_match,r.action_domain_match]
        if r.relation_disposition=="POSITIVE_T06_RELATION":
            if ms!=["MATCH","MATCH","MATCH"]: die("positive without triple MATCH: "+r.opportunity_id)
            if r.authority_ceiling!=POS_CEIL: die("positive ceiling")
            if r.manual_review_flag.lower()!="true": die("positive not manual")
        elif r.relation_disposition=="NEGATIVE_T06_RELATION":
            if "MISMATCH" not in ms: die("negative without mismatch: "+r.opportunity_id)
            if r.authority_ceiling!=NEG_CEIL: die("negative ceiling")
        else:
            if "MISMATCH" in ms or "UNKNOWN" not in ms: die("blocked match pattern: "+r.opportunity_id)
            if r.authority_ceiling!=BLK_CEIL: die("blocked ceiling")
            if r.manual_review_flag.lower()!="true": die("blocked not manual")
        if r.norm_contract_disposition=="AMBIGUOUS_NEEDS_VOZHD" and r.relation_disposition!="BLOCKED_NEEDS_VOZHD":
            die("ambiguous norm not blocked")
        if r.norm_contract_disposition=="NO_EXPECTED_CONDUCT_CONTRACT":
            if r.relation_disposition!="NEGATIVE_T06_RELATION" or r.action_domain_match!="MISMATCH":
                die("no-contract norm not action-mismatch negative")
        if r.manual_review_flag.lower()=="false" and not r.propagation_rule_id:
            die("nonmanual row lacks propagation rule")

    used=set(x for x in rr.propagation_rule_id if x)
    if used:
        if pl.rule_id.duplicated().any(): die("duplicate propagation rule id")
        if not used<=set(pl.rule_id): die("used propagation rule missing ledger")
        for rid in used:
            sub=rr[rr.propagation_rule_id==rid]
            row=pl[pl.rule_id==rid].iloc[0]
            if int(row.affected_opportunity_count)!=len(sub): die("propagation count mismatch "+rid)
            for c in ["source_family","wave","semantic_unit_id"]:
                if sub[c].nunique()!=1 or sub[c].iloc[0]!=row[c]: die("propagation crosses "+c+" "+rid)

    print(json.dumps({"status":"PASS","assigned_rows":len(assign),"norm_contracts":len(ct0),
                      "positive":int((rr.relation_disposition=="POSITIVE_T06_RELATION").sum()),
                      "negative":int((rr.relation_disposition=="NEGATIVE_T06_RELATION").sum()),
                      "blocked":int((rr.relation_disposition=="BLOCKED_NEEDS_VOZHD").sum()),
                      "propagation_rules_used":len(used)},indent=2))

if __name__=="__main__": main()
