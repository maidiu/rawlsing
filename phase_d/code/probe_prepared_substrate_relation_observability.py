#!/usr/bin/env python3
"""Bounded, aggregate-only M6-R3.1 probe over existing V550 substrates."""
from __future__ import annotations

import argparse, hashlib, json, math
from pathlib import Path
import pandas as pd

THRESHOLD_RATE = 0.005
SELECTION = [
    ("Arab Barometer", "I", "YE", "J3R3-T01-079198130abd9217351d", "S14-T01", ["question_impl.phase0.881d5d09bf76e891f696", "question_impl.phase0.e8d34b3919db95a4ad22"]),
    ("Arab Barometer", "I", "YE", "J3R3-T01-e0ec29f978eaae529ee9", "S14-T01", ["question_impl.phase0.17219d06fad537def5a1", "question_impl.phase0.330b4a6a537bf8d5a25a", "question_impl.phase0.7f7a79907d693d750021"]),
    ("Latinobarómetro", "1995", "BR", "IQRA-R2-e160d5b43e1e81087bb2", "S14-T01", ["question_impl.phase0.0b8455f5bebf105fbfd3", "question_impl.phase0.617913ae647c4a4d14d1", "question_impl.phase0.645be92203aa2c5da96b", "question_impl.phase0.2593fdb3cad3c14e0d18", "question_impl.phase0.fc75feb0e293ff94608b"]),
]

def sha(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for b in iter(lambda:f.read(1<<20),b""): h.update(b)
    return h.hexdigest()

def threshold(n): return max(2, min(30, math.ceil(n * THRESHOLD_RATE)))

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--crosswalk", required=True); ap.add_argument("--arab-substrate", required=True); ap.add_argument("--latin-substrate", required=True); ap.add_argument("--selection-out", required=True); ap.add_argument("--evidence-out", required=True); args=ap.parse_args()
    cw=pd.read_csv(args.crosswalk, dtype=str).fillna("")
    byid=cw.set_index("question_implementation_id")
    substrate={"Arab Barometer":Path(args.arab_substrate), "Latinobarómetro":Path(args.latin_substrate)}
    selections=[]; rows=[]
    for source,wave,country,aid,rule,members in SELECTION:
        vars_=[]; missing=[]
        for mid in members:
            if mid not in byid.index: missing.append(mid); continue
            vars_.append(str(byid.loc[mid,"source_variable_code"]).strip().upper())
        p=substrate[source]; d=pd.read_parquet(p)
        available=set(d["var_code_norm"].dropna().astype(str).str.upper())
        missing_vars=sorted(set(vars_)-available)
        if missing or missing_vars: raise SystemExit(f"fail closed: {aid} missing members={missing} vars={missing_vars}")
        manifest=p.with_name("v550_shared_respondent_substrate_manifest.json")
        if not manifest.exists(): raise SystemExit(f"missing substrate manifest: {manifest}")
        selections.append({"source_family":source,"wave":wave,"country_code":country,"relation_authority_id":aid,"rule_id":rule,"member_implementation_ids":members,"member_var_codes":vars_,"prepared_substrate_manifest_path":str(manifest),"prepared_substrate_manifest_sha256":sha(manifest),"selection_rationale":"STATICALLY_COVERED_BY_EXISTING_UNION"})
        valid=d[d["var_code_norm"].astype(str).str.upper().isin(vars_)].copy()
        valid["_ok"]=valid["is_valid_substantive_response"].astype(str).str.lower().isin(["true","1","yes"])
        grouped=valid[valid._ok].groupby("respondent_id_norm")["var_code_norm"].apply(lambda s: len(set(s.astype(str).str.upper())))
        n=int((grouped==len(set(vars_))).sum()); total=int(d["respondent_id_norm"].nunique()); th=threshold(total)
        posture="OBSERVED" if n>=th else ("UNDERPOWERED" if n>0 else "NOT_OBSERVED")
        rows.append({"source_family":source,"wave":wave,"country_code":country,"relation_authority_id":aid,"rule_id":rule,"member_implementation_ids_json":json.dumps(members,separators=(",",":")),"member_var_codes_json":json.dumps(vars_,separators=(",",":")),"empirical_evidence_id":f"M6R3.1-{aid}","prepared_substrate_manifest_path":str(manifest),"prepared_substrate_manifest_sha256":sha(manifest),"joint_answered_n":n,"weighted_n":"","kish_ess":"","governed_support_threshold":th,"support_status":"sufficient_support" if n>=th else ("underpowered" if n else "zero_support"),"empirical_posture":posture,"respondent_universe_status":"EXACT_SAME_RESPONDENT_SUBSTRATE","routing_applicability_status":"NO_NEW_ROUTING_INFERENCE","inference_ceiling":"DIAGNOSTIC_COTRAVEL_ONLY","association_mode":"DIAGNOSTIC","provenance_lane":"PREPARED_SUBSTRATE_BOUNDED_COTRAVEL_PROBE","semantic_authority_source":"JOB3_R3_FROZEN_AUTHORITY","semantic_relation_generated_from_responses":False,"no_association_causality_or_personality_inference":True})
    pd.DataFrame(selections).to_csv(args.selection_out,index=False)
    pd.DataFrame(rows).to_csv(args.evidence_out,index=False)

if __name__=="__main__": main()
