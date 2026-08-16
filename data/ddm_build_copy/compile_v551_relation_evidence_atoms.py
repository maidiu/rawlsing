#!/usr/bin/env python3
"""Compile V551 v3 canonical directional adjudication, atoms and coverage."""
from __future__ import annotations
import argparse, hashlib, json, sys
from pathlib import Path
from typing import Any
import pandas as pd
ROOT=Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
from data.ddm_build_copy.ddm_v551_atoms import (V551_SCHEMA_VERSION,V551_COMPILER_VERSION,build_v551_directional_candidate_adjudication,build_v551_relation_evidence_atoms,build_v551_directional_distribution_coverage,validate_v551_bridge_input_contract,validate_v551_atom_contract,validate_v551_adjudication_contract,validate_v551_coverage_contract)
from data.ddm_build_copy.ddm_v551_directionality_expectation import build_v551_directionality_stamp_audit,summarize_v551_directionality_stamp_coverage
DEFAULT_OUTPUT_ROOT=ROOT/"data"/"ddm_repository_copy"/"v551"/"runs"
CANONICAL_ARTIFACTS=("directional_candidate_adjudication","relation_evidence_atoms","directional_distribution_coverage")

def _read(path:Path)->pd.DataFrame:
    return pd.read_csv(path,low_memory=False) if path.suffix.lower()==".csv" else pd.read_parquet(path)
def _logical_hash(df:pd.DataFrame)->str:
    if df.empty:return hashlib.sha256(b"").hexdigest()
    x=df.copy()
    for c in x.columns:x[c]=x[c].fillna("").astype(str)
    x=x.sort_values(list(x.columns),kind="mergesort").reset_index(drop=True)
    return hashlib.sha256(x.to_csv(index=False).encode()).hexdigest()
def _file_hash(path:Path)->str:return hashlib.sha256(path.read_bytes()).hexdigest()
def _write(df:pd.DataFrame,path:Path)->dict[str,Any]:
    path.parent.mkdir(parents=True,exist_ok=True);tmp=path.with_suffix(path.suffix+".tmp");df.to_parquet(tmp,index=False);tmp.replace(path)
    return {"artifact":path.stem,"path":str(path),"row_count":len(df),"artifact_file_sha256":_file_hash(path),"logical_content_sha256":_logical_hash(df),"schema_version":V551_SCHEMA_VERSION}
def parse_args():
    p=argparse.ArgumentParser();p.add_argument("--run-id",required=True);p.add_argument("--bridge-path",required=True);p.add_argument("--output-root",default=str(DEFAULT_OUTPUT_ROOT));p.add_argument("--write-csv",action="store_true");p.add_argument("--v551-compile-mode",choices=("canonical",),default="canonical");return p.parse_args()
def main()->int:
    a=parse_args();bridge=_read(Path(a.bridge_path));contract=validate_v551_bridge_input_contract(bridge)
    if contract["status"]!="PASS":raise RuntimeError(contract["status"]+":"+",".join(contract["missing_columns"]))
    run_ids=sorted(set(bridge.run_id.fillna("").astype(str)))
    if len(run_ids)!=1 or run_ids[0]!=a.run_id:raise RuntimeError(f"BLOCKED_V551_RUN_IDENTITY_MISMATCH expected={a.run_id} observed={run_ids}")
    adjud=build_v551_directional_candidate_adjudication(bridge);atoms,nonpromotable=build_v551_relation_evidence_atoms(bridge);coverage=build_v551_directional_distribution_coverage(adjud);stamp=build_v551_directionality_stamp_audit(bridge)
    issues=validate_v551_adjudication_contract(adjud)+validate_v551_atom_contract(atoms)+validate_v551_coverage_contract(coverage)
    if issues:raise RuntimeError("BLOCKED_V551_CONTRACT_INVALID:"+";".join(issues))
    candidate_count=len(adjud);promotable=int(adjud.promotable.map(bool).sum()) if not adjud.empty else 0;nonprom=candidate_count-promotable
    if candidate_count!=promotable+nonprom:raise RuntimeError("BLOCKED_V551_CANDIDATE_CONSERVATION")
    run_dir=Path(a.output_root)/a.run_id;run_dir.mkdir(parents=True,exist_ok=True);artifacts=[]
    for name,frame in [(CANONICAL_ARTIFACTS[0],adjud),(CANONICAL_ARTIFACTS[1],atoms),(CANONICAL_ARTIFACTS[2],coverage)]:
        artifacts.append(_write(frame,run_dir/f"{name}.parquet"))
        if a.write_csv:frame.to_csv(run_dir/f"{name}.csv",index=False)
    evidence_status="PROMOTABLE_EVIDENCE_PRESENT" if promotable else ("APPLICABLE_REPAIR_DEBT_ONLY" if candidate_count else "NO_APPLICABLE_DIRECTIONAL_EVIDENCE")
    downstream="V551_CONTRACT_READY_FOR_CONSUMER_ADAPTATION" if promotable else "NO_PROMOTABLE_EVIDENCE"
    manifest={"run_id":a.run_id,"schema_version":V551_SCHEMA_VERSION,"compiler_version":V551_COMPILER_VERSION,"run_integrity_status":"PASS","evidence_status":evidence_status,"downstream_permission_status":downstream,"candidate_count":candidate_count,"promotable_candidate_count":promotable,"nonpromotable_candidate_count":nonprom,"atom_count":len(atoms),"distribution_coverage_rows":len(coverage),"directionality_stamp_coverage":summarize_v551_directionality_stamp_coverage(stamp),"canonical_artifacts":artifacts,"nonpromotable_directional_candidate_ids":nonpromotable.candidate_id.tolist() if not nonpromotable.empty else [],"contract_boundary":{"canonical_signed_projection_owner":"V551","v552_pressure_decisions_present":False,"auxiliary_semantic_inputs_rehashed_by_v551":False},"producer_bridge_path":a.bridge_path,"producer_bridge_file_sha256":_file_hash(Path(a.bridge_path))}
    tmp=run_dir/"manifest.json.tmp";tmp.write_text(json.dumps(manifest,indent=2,ensure_ascii=False),encoding="utf-8");tmp.replace(run_dir/"manifest.json");print(json.dumps(manifest,indent=2,ensure_ascii=False));return 0
if __name__=="__main__":raise SystemExit(main())
