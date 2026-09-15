#!/usr/bin/env python3
"""Aggregate an already-executed nine-family bounded smoke into the M6 return.

This runner does not query the database. Run the existing local bounded smoke first.
It discovers each family scope under --smoke-root, compiles positioned evidence, and
emits only nonrespondent return artifacts.
"""
from __future__ import annotations
import argparse, base64, gzip, io, json, subprocess
from pathlib import Path
import pandas as pd
from compile_positioned_relational_evidence import compile_scope

DIMS=["POSITION_DISTRIBUTION","MINORITY_OUTLIER","RECURSIVE_BRANCH","ATTITUDE_CLOUD_OR_COSIGNATURE","V550J_JOINT","SEMANTIC_EMPIRICAL_INDEPENDENCE","STRATA_HORIZON","UNCERTAINTY_PROVENANCE"]
SLUGS={"Afrobarometer":["afrobarometer","afro"],"Arab Barometer":["arab_barometer","arabbarometer","arab"],"Asian Barometer":["asian_barometer","asianbarometer","asian"],"EVS":["evs"],"GSS":["gss"],"Latinobarómetro":["latinobarometro","latin"],"LiTS":["lits"],"South Asia":["south_asia","southasia"],"WVS":["wvs"]}

def find_scope(root:Path,fam:str,wave:str,country:str)->Path|None:
    cand=[]
    for p in root.rglob("*"):
        if not p.is_dir(): continue
        t=p.as_posix().lower()
        if any(s in t for s in SLUGS[fam]) and (wave.lower() in t or str(wave).lower().replace(" ","") in t) and country.lower() in t:
            cand.append(p)
    if not cand:
        for p in root.rglob("*"):
            if p.is_dir() and any(s in p.as_posix().lower() for s in SLUGS[fam]): cand.append(p)
    return sorted(cand,key=lambda p:(len(p.parts),len(str(p))))[0] if cand else None

def git(cmd:list[str],cwd:Path)->str:
    try:return subprocess.check_output(["git",*cmd],cwd=cwd,text=True,stderr=subprocess.DEVNULL).strip()
    except Exception:return ""

def main()->int:
    ap=argparse.ArgumentParser(); ap.add_argument("--repo-root",type=Path,required=True); ap.add_argument("--smoke-root",type=Path,required=True); ap.add_argument("--output-dir",type=Path,required=True); ap.add_argument("--authority-dir",type=Path,default=Path(__file__).resolve().parents[1]/"authority")
    a=ap.parse_args(); out=a.output_dir; out.mkdir(parents=True,exist_ok=True)
    scope=pd.read_csv(a.authority_dir/"NINE_FAMILY_CANARY_SCOPE_R1.csv",dtype=str).fillna("")
    def read_b64_gz(name):
        single=a.authority_dir/(name+".gz.b64")
        if single.exists(): encoded=single.read_text().strip()
        else:
            parts=sorted(a.authority_dir.glob(name+".gz.b64.part*"))
            if not parts: raise FileNotFoundError(single)
            encoded="".join(p.read_text().strip() for p in parts)
        raw=base64.b64decode(encoded)
        return pd.read_csv(io.BytesIO(gzip.decompress(raw)),dtype=str).fillna("")
    top=read_b64_gz("JOB3_R3_FINAL_GOVERNED_RELATION_TOPOLOGY_R1.csv")
    blk=read_b64_gz("JOB3_R3_BLOCKED_CANDIDATE_LEDGER_R1.csv")
    all_ev=[]; returns=[]; gate=[]; fused_all=True
    for _,s in scope.iterrows():
        fam,wave,country=s.source_family,s.wave,s.country_code; sr=find_scope(a.smoke_root,fam,wave,country)
        if sr is None:
            returns.append({"source_family":fam,"wave":wave,"country_code":country,"terminal_status":"PASS_BLOCKED_LOCAL","respondent_universe_status":"BLOCKED","v550_base_status":"BLOCKED","position_distribution_status":"BLOCKED","recursive_branch_status":"BLOCKED","attitude_cloud_status":"BLOCKED","v550j_fused_status":"BLOCKED","v551_status":"BLOCKED","v551j_status":"BLOCKED","strata_horizon_status":"BLOCKED","blocked_code":"LOCAL_SCOPE_OUTPUT_NOT_FOUND","blocked_detail":"No bounded smoke output directory could be resolved for this family.","evidence_refs_json":"[]","notes":"Fail-closed; semantic authority is not erased."})
            for d in DIMS: gate.append({"source_family":fam,"wave":wave,"country_code":country,"gate_dimension":d,"status":"BLOCKED","evidence_count":0,"blocker_code":"LOCAL_SCOPE_OUTPUT_NOT_FOUND","evidence_refs_json":"[]","notes":""})
            fused_all=False; continue
        ev,scan=compile_scope(sr,top,blk,fam,wave,country); all_ev.append(ev); fused_all &= bool(scan["fused_manifest_verified"])
        refs=ev.evidence_id.tolist(); observed=int((ev.empirical_cotravel_posture=="OBSERVED").sum()) if len(ev) else 0
        terminal="PASS_POSITIVE" if observed and (ev.semantic_relation_posture.eq("GOVERNED_POSITIVE") & ev.empirical_cotravel_posture.eq("OBSERVED")).any() else "PASS_EMPIRICAL_ONLY" if observed else "PASS_BLOCKED_LOCAL"
        block_code="" if terminal!="PASS_BLOCKED_LOCAL" else "NO_EXACT_EMPIRICAL_SEMANTIC_LINK_IN_BOUNDED_SCOPE"
        returns.append({"source_family":fam,"wave":wave,"country_code":country,"terminal_status":terminal,"respondent_universe_status":"EXACT_SAME_RESPONDENT_UNIVERSE" if scan["fused_manifest_verified"] else "BLOCKED","v550_base_status":"OBSERVED" if sr.exists() else "BLOCKED","position_distribution_status":"OBSERVED" if scan["position_seen"] else "EMPTY_VALID","recursive_branch_status":"OBSERVED" if scan["branch_seen"] else "EMPTY_VALID","attitude_cloud_status":"OBSERVED" if scan["cloud_seen"] else "EMPTY_VALID","v550j_fused_status":"PASS" if scan["fused_manifest_verified"] else "BLOCKED","v551_status":"PRESENT" if any("v551" in p.as_posix().lower() and "v551j" not in p.as_posix().lower() for p in sr.rglob("*")) else "EMPTY_VALID","v551j_status":"PRESENT" if any("v551j" in p.as_posix().lower() for p in sr.rglob("*")) else "EMPTY_VALID","strata_horizon_status":"OBSERVED" if scan["position_seen"] else "UNPLACED_GOVERNED","blocked_code":block_code,"blocked_detail":"No exact same-row implementation-ID bridge was observed; no semantic/empirical substitution permitted." if block_code else "","evidence_refs_json":json.dumps(refs),"notes":f"scope_root={sr}"})
        dim_status={"POSITION_DISTRIBUTION":scan["position_seen"],"MINORITY_OUTLIER":scan["position_seen"],"RECURSIVE_BRANCH":scan["branch_seen"],"ATTITUDE_CLOUD_OR_COSIGNATURE":scan["cloud_seen"],"V550J_JOINT":scan["joint_seen"],"SEMANTIC_EMPIRICAL_INDEPENDENCE":len(ev)>0,"STRATA_HORIZON":scan["position_seen"],"UNCERTAINTY_PROVENANCE":len(ev)>0}
        for d in DIMS: gate.append({"source_family":fam,"wave":wave,"country_code":country,"gate_dimension":d,"status":"OBSERVED" if dim_status[d] else "EMPTY_VALID","evidence_count":observed if dim_status[d] else 0,"blocker_code":"","evidence_refs_json":json.dumps(refs[:50]),"notes":""})
    evidence=pd.concat(all_ev,ignore_index=True) if all_ev else pd.DataFrame()
    evidence.to_csv(out/"POSITIONED_RELATIONAL_EVIDENCE_CANARY.csv",index=False)
    pd.DataFrame(returns).to_csv(out/"PHASE_D_NINE_FAMILY_CANARY_RETURN.csv",index=False)
    pd.DataFrame(gate).to_csv(out/"APP_GATE_A_EVIDENCE.csv",index=False)
    top.to_csv(out/"JOB3_R3_FINAL_GOVERNED_RELATION_TOPOLOGY_R1.csv",index=False)
    head=git(["rev-parse","HEAD"],a.repo_root); ancestor=(subprocess.call(["git","merge-base","--is-ancestor","acbba91de28b9cee20af05e81e4d8bfdaa876298","HEAD"],cwd=a.repo_root,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)==0)
    manifest={"local_head_sha":head,"fused_ancestor_verified":ancestor,"smoke_root":str(a.smoke_root.resolve()),"association_mode":"DIAGNOSTIC","respondent_data_in_return":False,"evidence_rows":int(len(evidence))}
    (out/"PHASE_D_RUN_MANIFEST.json").write_text(json.dumps(manifest,indent=2,sort_keys=True)+"\n")
    print(json.dumps(manifest,indent=2)); return 0
if __name__=="__main__": raise SystemExit(main())
