#!/usr/bin/env python3
"""Compile the producer-bound V552J join from verified V551J and V552 manifests."""
from __future__ import annotations
import argparse, hashlib, json, re, shutil, sys, tempfile
from pathlib import Path
from typing import Any, Mapping
import pandas as pd
ROOT=Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
from data.ddm_build_copy.ddm_pipeline_boundary_contract import PIPELINE_BOUNDARY_CONTRACT_VERSION,BoundaryContractError,atomic_write_json,boundary_state_from_payload,inspect_artifact,publish_staged_directory,read_status_document,require_canonical_parquet,sha256_file,validate_machine_output_policy
from data.ddm_build_copy.ddm_v551j_schema import V551J_COMPILER_VERSION,V551J_SCHEMA_VERSION
from data.ddm_build_copy.ddm_v552_structural import V552_COMPILER_VERSION,V552_SCHEMA_VERSION
from data.ddm_build_copy.ddm_v552j_handoff import V552J_JOIN_COMPILER_VERSION,V552J_JOIN_SCHEMA_VERSION,build_v552j_join
DEFAULT_OUTPUT_ROOT=ROOT/"data"/"ddm_repository_copy"/"v552j"/"runs"

def _clean(v:Any)->str:
    if v is None:return ""
    try:
        if pd.isna(v):return ""
    except Exception:pass
    s=str(v).strip();return "" if s.lower() in {"nan","none","null"} else s

def _logical_hash(df:pd.DataFrame)->str:
    if df.empty:return hashlib.sha256(b"").hexdigest()
    w=df.copy()
    for c in w:w[c]=w[c].map(lambda v:"" if v is None else str(v))
    w=w.sort_values(list(w.columns),kind="mergesort").reset_index(drop=True);return hashlib.sha256(w.to_csv(index=False).encode()).hexdigest()

def _read_manifest(path:Path,label:str):
    doc=read_status_document(path)
    if not doc.exists:raise BoundaryContractError(f"{label}_MANIFEST_MISSING:{path}")
    if not doc.readable:raise BoundaryContractError(f"{label}_MANIFEST_UNREADABLE:{path}:{doc.error}")
    p=doc.payload
    if _clean(p.get("contract_version") or p.get("boundary_contract_version"))!=PIPELINE_BOUNDARY_CONTRACT_VERSION:raise BoundaryContractError(f"{label}_BOUNDARY_CONTRACT_VERSION_MISMATCH")
    state=boundary_state_from_payload(p)
    if state.run_integrity_status!="PASS":raise BoundaryContractError(f"{label}_RUN_INTEGRITY_NOT_PASS:{state.run_integrity_status}")
    return p,state

def _scope_from_manifest(p:Mapping[str,Any],label:str)->dict[str,str]:
    raw=p.get("producer_scope_identity"); n=dict(raw) if isinstance(raw,Mapping) else {}
    scope={"run_id":_clean(n.get("run_id") or p.get("producer_run_id") or p.get("run_id")),"source":_clean(n.get("source") or p.get("source")),"wave":_clean(n.get("canonical_wave") or n.get("wave") or p.get("canonical_wave") or p.get("wave")),"country_code":_clean(n.get("country_code") or p.get("country_code")),"shard_id":_clean(n.get("shard_id") or p.get("shard_id"))}
    if not scope["run_id"] or not scope["source"] or not scope["wave"]:raise BoundaryContractError(f"{label}_SCOPE_IDENTITY_INCOMPLETE")
    if not scope["country_code"] and not scope["shard_id"]:raise BoundaryContractError(f"{label}_COUNTRY_OR_SHARD_IDENTITY_REQUIRED")
    return scope

def _coherent_scope(run_id:str,a:Mapping[str,str],b:Mapping[str,str])->dict[str,str]:
    if a["run_id"]!=run_id or b["run_id"]!=run_id:raise BoundaryContractError(f"V552J_CROSS_RUN_MISMATCH:cli={run_id}:v551j={a['run_id']}:v552={b['run_id']}")
    for k in ("source","wave"):
        if a[k]!=b[k]:raise BoundaryContractError(f"V552J_CROSS_SCOPE_MISMATCH:{k}:v551j={a[k]}:v552={b[k]}")
    if a["country_code"] or b["country_code"]:
        if not a["country_code"] or not b["country_code"] or a["country_code"]!=b["country_code"]:raise BoundaryContractError("V552J_CROSS_SCOPE_MISMATCH:country")
        if a["shard_id"] and b["shard_id"] and a["shard_id"]!=b["shard_id"]:raise BoundaryContractError("V552J_CROSS_SCOPE_MISMATCH:shard")
    elif not (a["shard_id"] and b["shard_id"] and a["shard_id"]==b["shard_id"]):raise BoundaryContractError("V552J_CROSS_SCOPE_MISMATCH:shard")
    shard_id=b["shard_id"] if b["shard_id"] and b["shard_id"]==a["shard_id"] else ""
    return {"run_id":run_id,"source":b["source"],"wave":b["wave"],"canonical_wave":b["wave"],"country_code":b["country_code"] or a["country_code"],"shard_id":shard_id,"scope_kind":"shard" if shard_id else "country"}

def _artifact_declarations(p:Mapping[str,Any])->list[dict[str,Any]]:
    raw=p.get("artifacts") or []
    if not isinstance(raw,list):raise BoundaryContractError("V552J_PRODUCER_ARTIFACT_DECLARATIONS_MALFORMED")
    return [dict(x) for x in raw if isinstance(x,Mapping)]

def _find_declaration(p:Mapping[str,Any],*,label:str,artifact_names:tuple[str,...],basenames:tuple[str,...],required:bool):
    matches=[]
    for row in _artifact_declarations(p):
        name=_clean(row.get("artifact") or row.get("name")); rel=_clean(row.get("path") or row.get("relative_path"))
        if name in artifact_names or Path(rel).name in basenames:matches.append(row)
    if not matches:
        if required:raise BoundaryContractError(f"{label}_ARTIFACT_DECLARATION_MISSING:{artifact_names[0]}")
        return None
    canonical=[r for r in matches if _clean(r.get("path") or r.get("relative_path")).endswith(".parquet") and _clean(r.get("artifact_kind"))=="canonical"]
    if len(canonical)!=1:raise BoundaryContractError(f"{label}_CANONICAL_PARQUET_DECLARATION_COUNT:{artifact_names[0]}:{len(canonical)}")
    return canonical[0]

def _resolve_declared_path(manifest:Path,d:Mapping[str,Any],label:str)->Path:
    rel=_clean(d.get("path") or d.get("relative_path"))
    if not rel:raise BoundaryContractError(f"{label}_ARTIFACT_PATH_MISSING")
    path=require_canonical_parquet((manifest.parent/rel).resolve()); root=manifest.parent.parent if manifest.parent.name=="manifest" else manifest.parent
    try:path.relative_to(root.resolve())
    except ValueError as e:raise BoundaryContractError(f"{label}_ARTIFACT_ESCAPES_RUN_ROOT:{rel}") from e
    return path

def _verify_and_read_declared(manifest:Path,d:Mapping[str,Any],*,label:str,expected_schema:str)->pd.DataFrame:
    if _clean(d.get("schema_version"))!=expected_schema:raise BoundaryContractError(f"{label}_ARTIFACT_SCHEMA_VERSION_MISMATCH")
    path=_resolve_declared_path(manifest,d,label); i=inspect_artifact(path)
    if not i.exists or not i.readable:raise BoundaryContractError(f"{label}_ARTIFACT_UNREADABLE:{path}:{i.error}")
    declared=_clean(d.get("artifact_file_sha256")).lower()
    if not re.fullmatch(r"[0-9a-f]{64}",declared):raise BoundaryContractError(f"{label}_ARTIFACT_FILE_SHA256_MISSING_OR_INVALID")
    if i.artifact_file_sha256.lower()!=declared:raise BoundaryContractError(f"{label}_ARTIFACT_FILE_SHA256_MISMATCH:expected={declared}:actual={i.artifact_file_sha256.lower()}")
    if d.get("row_count") is not None and int(d["row_count"])!=int(i.row_count or 0):raise BoundaryContractError(f"{label}_ARTIFACT_ROW_COUNT_MISMATCH")
    return pd.read_parquet(path)

def _verify_frame_scope(df:pd.DataFrame,scope:Mapping[str,str],label:str)->None:
    if df.empty:return
    checks={"run_id":scope["run_id"],"source":scope["source"],"canonical_wave":scope["wave"]}
    checks["country_code" if scope.get("country_code") else "shard_id"]=scope.get("country_code") or scope.get("shard_id")
    for col,want in checks.items():
        use="source_family" if col=="source" and col not in df and "source_family" in df else col
        if use not in df:raise BoundaryContractError(f"{label}_SCOPE_COLUMN_MISSING:{col}")
        got={_clean(v) for v in df[use] if _clean(v)}
        if got!={want}:raise BoundaryContractError(f"{label}_SCOPE_MISMATCH:{col}:expected={want}:observed={sorted(got)}")

def verify_v551j_producer_bundle(manifest_path:str|Path,*,run_id:str)->dict[str,Any]:
    path=Path(manifest_path); p,state=_read_manifest(path,"V551J")
    if _clean(p.get("schema_version"))!=V551J_SCHEMA_VERSION:raise BoundaryContractError("V551J_SCHEMA_VERSION_MISMATCH")
    if _clean(p.get("compiler_version"))!=V551J_COMPILER_VERSION:raise BoundaryContractError("V551J_COMPILER_VERSION_MISMATCH")
    scope=_scope_from_manifest(p,"V551J")
    if scope["run_id"]!=run_id:raise BoundaryContractError(f"V551J_RUN_ID_MISMATCH:expected={run_id}:actual={scope['run_id']}")
    present=state.evidence_status=="PRESENT"; specs=(("candidate","V551J_CANDIDATE",("candidate","v551j_joint_packet_candidate_index"),("v551j_joint_packet_candidate_index.parquet",)),("certified","V551J_CERTIFIED",("certified","v551j_certified_joint_packet_index"),("v551j_certified_joint_packet_index.parquet",)),("review","V551J_REVIEW",("review_surface","v551j_review_surface"),("v551j_review_surface.parquet",)))
    frames={}
    for key,label,names,bases in specs:
        d=_find_declaration(p,label=label,artifact_names=names,basenames=bases,required=present); frames[key]=_verify_and_read_declared(path,d,label=label,expected_schema=V551J_SCHEMA_VERSION) if d else pd.DataFrame()
    _verify_frame_scope(frames["candidate"],scope,"V551J_CANDIDATE");_verify_frame_scope(frames["certified"],scope,"V551J_CERTIFIED")
    review=frames["review"]
    if not review.empty:
        if "run_id" not in review or "packet_id" not in review:raise BoundaryContractError("V551J_REVIEW_IDENTITY_COLUMNS_MISSING")
        if {_clean(v) for v in review["run_id"] if _clean(v)}!={run_id}:raise BoundaryContractError("V551J_REVIEW_RUN_ID_MISMATCH")
        if frames["candidate"].empty or "packet_id" not in frames["candidate"]:raise BoundaryContractError("V551J_REVIEW_CANDIDATE_SURFACE_REQUIRED")
        byid={_clean(r.get("packet_id")):dict(r) for r in frames["candidate"].to_dict("records") if _clean(r.get("packet_id"))}; enriched=[]
        for r in review.to_dict("records"):
            pid=_clean(r.get("packet_id")); base=byid.get(pid)
            if base is None:raise BoundaryContractError(f"V551J_REVIEW_PACKET_NOT_IN_CANDIDATE:{pid or '<missing>'}")
            row=dict(base);row.update(r);enriched.append(row)
        frames["review"]=pd.DataFrame(enriched);_verify_frame_scope(frames["review"],scope,"V551J_REVIEW")
    for label,key in (("V551J_CANDIDATE","candidate"),("V551J_CERTIFIED","certified"),("V551J_REVIEW","review")):
        df=frames[key]
        if not df.empty:
            if "packet_id" not in df or df["packet_id"].map(_clean).eq("").any():raise BoundaryContractError(f"{label}_PACKET_ID_MISSING")
            if df["packet_id"].map(_clean).duplicated().any():raise BoundaryContractError(f"{label}_DUPLICATE_PACKET_ID")
    return {"manifest":p,"manifest_path":str(path),"manifest_sha256":sha256_file(path),"scope":scope,"state":{"run_integrity_status":state.run_integrity_status,"evidence_status":state.evidence_status,"downstream_permission_status":state.downstream_permission_status},**frames}

def verify_v552_producer_bundle(manifest_path:str|Path,*,run_id:str)->dict[str,Any]:
    path=Path(manifest_path);p,state=_read_manifest(path,"V552")
    if _clean(p.get("schema_version"))!=V552_SCHEMA_VERSION:raise BoundaryContractError("V552_SCHEMA_VERSION_MISMATCH")
    if _clean(p.get("compiler_version"))!=V552_COMPILER_VERSION:raise BoundaryContractError("V552_COMPILER_VERSION_MISMATCH")
    scope=_scope_from_manifest(p,"V552")
    if scope["run_id"]!=run_id:raise BoundaryContractError(f"V552_RUN_ID_MISMATCH:expected={run_id}:actual={scope['run_id']}")
    fd=_find_declaration(p,label="V552_STRUCTURAL_FACT",artifact_names=("v552_structural_fact_index",),basenames=("v552_structural_fact_index.parquet",),required=True);td=_find_declaration(p,label="V552_TEMPORAL_KEY",artifact_names=("v552_temporal_key_source_index",),basenames=("v552_temporal_key_source_index.parquet",),required=True);facts=_verify_and_read_declared(path,fd,label="V552_STRUCTURAL_FACT",expected_schema=V552_SCHEMA_VERSION);temporal=_verify_and_read_declared(path,td,label="V552_TEMPORAL_KEY",expected_schema=V552_SCHEMA_VERSION);_verify_frame_scope(facts,scope,"V552_STRUCTURAL_FACT");_verify_frame_scope(temporal,scope,"V552_TEMPORAL_KEY")
    return {"manifest":p,"manifest_path":str(path),"manifest_sha256":sha256_file(path),"scope":scope,"state":{"run_integrity_status":state.run_integrity_status,"evidence_status":state.evidence_status,"downstream_permission_status":state.downstream_permission_status},"structural_facts":facts,"temporal_keys":temporal,"artifact_paths":{"v552_structural_fact_index":str(_resolve_declared_path(path,fd,"V552_STRUCTURAL_FACT")),"v552_temporal_key_source_index":str(_resolve_declared_path(path,td,"V552_TEMPORAL_KEY"))}}

def _v553_compatibility_frame(join:pd.DataFrame)->pd.DataFrame:
    f=join.copy(); empty=pd.Series(dtype=str); probe=f.get("ready_for_v553_probe",pd.Series(dtype=bool)).map(bool); sid=f.get("source_v552_temporal_key_source_id",empty)
    aliases={"v552j_packet_id":f.get("packet_id",empty),"v553_input_id":f.get("v552j_join_id",empty),"source_family":f.get("source",empty),"country":f.get("country_code",empty),"source_v552_structural_fact_id":f.get("v552_structural_fact_id",empty),"source_v552_structural_fact_ids_diagnostic_json":f.get("source_v552_structural_fact_ids_json",empty),"source_v552_temporal_key_source_ids_json":sid.map(lambda v:json.dumps([_clean(v)] if _clean(v) else [])),"source_v552_temporal_key_source_ids_diagnostic_json":sid.map(lambda v:json.dumps([_clean(v)] if _clean(v) else [])),"structural_fact_lane":f.get("source_v552_structural_fact_lane",empty),"structural_fact_grain":f.get("source_v552_structural_fact_grain",empty),"single_wave_probe_allowed":probe,"ready_for_v553":probe,"packet_ready_for_v553":probe,"temporal_field_allowed":False,"must_temporalize":probe,"temporal_anchor_required":probe,"comparability_required":probe,"ready_for_runtime_consumption":False,"comparability_status":"not_supplied","fallback_permission_profile_key":"","packet_class":f.get("v551j_lane",empty),"read_permission":f.get("join_permission",empty).map(lambda v:"v553_constraint_candidate" if _clean(v)=="ALLOW" else "v553_context_only" if _clean(v)=="REVIEW_ONLY" else "blocked"),"blocking_reason":f.get("v553_handoff_blocked_reason",empty)}
    for k,v in aliases.items():f[k]=v
    return f

def _write_frame(df:pd.DataFrame,path:Path,*,artifact:str,kind:str="canonical")->dict[str,Any]:
    path.parent.mkdir(parents=True,exist_ok=True);df.to_parquet(path,index=False);return {"artifact":artifact,"path":str(path.relative_to(path.parents[1])),"artifact_kind":kind,"row_count":len(df),"artifact_file_sha256":sha256_file(path),"logical_content_sha256":_logical_hash(df),"schema_version":V552J_JOIN_SCHEMA_VERSION,"compiler_version":V552J_JOIN_COMPILER_VERSION}
def _write_csv(df:pd.DataFrame,path:Path,*,artifact:str)->dict[str,Any]:
    path.parent.mkdir(parents=True,exist_ok=True);df.to_csv(path,index=False);return {"artifact":artifact,"path":str(path.relative_to(path.parents[1])),"artifact_kind":"diagnostic_csv","row_count":len(df),"artifact_file_sha256":sha256_file(path),"logical_content_sha256":_logical_hash(df),"schema_version":V552J_JOIN_SCHEMA_VERSION,"compiler_version":V552J_JOIN_COMPILER_VERSION}

def compile_v552j_run(*,run_id:str,v551j_manifest_path:str|Path,v552_manifest_path:str|Path,output_root:str|Path=DEFAULT_OUTPUT_ROOT,write_parquet:bool=True,write_csv:bool=False)->dict[str,Any]:
    validate_machine_output_policy(write_parquet=write_parquet,write_csv=write_csv);a=verify_v551j_producer_bundle(v551j_manifest_path,run_id=run_id);b=verify_v552_producer_bundle(v552_manifest_path,run_id=run_id);scope=_coherent_scope(run_id,a["scope"],b["scope"]);result=build_v552j_join(run_id=run_id,v551j_certified=a["certified"],v551j_review=a["review"],v552_structural_facts=b["structural_facts"],v552_temporal_keys=b["temporal_keys"],v551j_state=a["state"],v552_state=b["state"],v551j_manifest_sha256=a["manifest_sha256"],v552_manifest_sha256=b["manifest_sha256"]);join=result["join_index"];audit=result["join_audit"];compat=_v553_compatibility_frame(join);state=result["state"];metrics=result["metrics"];root=Path(output_root);root.mkdir(parents=True,exist_ok=True);final=root/run_id;staging=Path(tempfile.mkdtemp(prefix=f".{run_id}.v552j-stage-",dir=str(root)))
    try:
        artifacts=[_write_frame(join,staging/"packets"/"v552j_structural_join_index.parquet",artifact="v552j_structural_join_index"),_write_frame(audit,staging/"audits"/"v552j_join_audit.parquet",artifact="v552j_join_audit"),_write_frame(compat,staging/"packets"/"v552j_v553_input_index.parquet",artifact="v552j_v553_input_index",kind="compatibility"),_write_frame(compat,staging/"packets"/"v552j_to_v553_handoff_index.parquet",artifact="v552j_to_v553_handoff_index",kind="compatibility")]
        if write_csv:artifacts += [_write_csv(join,staging/"packets"/"v552j_structural_join_index.csv",artifact="v552j_structural_join_index"),_write_csv(audit,staging/"audits"/"v552j_join_audit.csv",artifact="v552j_join_audit")]
        readiness={"contract_version":PIPELINE_BOUNDARY_CONTRACT_VERSION,"boundary_contract_version":PIPELINE_BOUNDARY_CONTRACT_VERSION,"producer_run_id":run_id,"run_id":run_id,"source":scope["source"],"wave":scope["wave"],"canonical_wave":scope["canonical_wave"],"country_code":scope["country_code"],"shard_id":scope["shard_id"],"producer_scope_identity":scope,"schema_version":V552J_JOIN_SCHEMA_VERSION,"compiler_version":V552J_JOIN_COMPILER_VERSION,**state,**metrics,"primary_row_count":len(join),"v552_structural_fact_index_path":b["artifact_paths"]["v552_structural_fact_index"],"v552_temporal_key_source_index_path":b["artifact_paths"]["v552_temporal_key_source_index"],"constraint_evidence_status":"PRESENT" if metrics["constraint_count"] else "VALID_EMPTY","observed_zero_is_measurement_not_absence":True,"created_from_verified_producers":True}
        manifest={**readiness,"artifacts":artifacts,"canonical_artifact_names":["v552j_structural_join_index","v552j_join_audit"],"upstream_v551j":{"manifest_path":a["manifest_path"],"manifest_file_sha256":a["manifest_sha256"],"schema_version":V551J_SCHEMA_VERSION,"compiler_version":V551J_COMPILER_VERSION,**a["state"]},"upstream_v552":{"manifest_path":b["manifest_path"],"manifest_file_sha256":b["manifest_sha256"],"schema_version":V552_SCHEMA_VERSION,"compiler_version":V552_COMPILER_VERSION,**b["state"]},"contract_boundary":{"synthetic_unknown_primary_rows_allowed":False,"missing_constraint_metrics_are_zero":False,"structural_matching_requires_exact_scope_before_semantic_score":True,"observed_zero_distinct_from_absence_or_unresolved":True,"canonical_machine_format":"parquet"}}
        atomic_write_json(staging/"manifest.json",manifest);atomic_write_json(staging/"manifest"/"v552j_readiness_report.json",readiness);atomic_write_json(staging/"manifest"/"v552j_runtime_handoff_manifest.json",manifest);atomic_write_json(staging/"manifest"/"v552j_v553_handoff_manifest.json",{**readiness,"v553_input_index_path":"packets/v552j_v553_input_index.parquet","v553_probe_row_count":int(join["ready_for_v553_probe"].map(bool).sum()) if not join.empty else 0,"v553_temporal_field_row_count":0});publish_staged_directory(staging,final);return manifest
    except Exception:
        if staging.exists():shutil.rmtree(staging,ignore_errors=True)
        raise

def parse_args()->argparse.Namespace:
    p=argparse.ArgumentParser(description="Compile producer-bound V552J structural join.");p.add_argument("--run-id",required=True);p.add_argument("--v551j-manifest-path",required=True);p.add_argument("--v552-manifest-path",required=True);p.add_argument("--output-root",default=str(DEFAULT_OUTPUT_ROOT));p.add_argument("--write-parquet",dest="write_parquet",action="store_true",default=True);p.add_argument("--no-write-parquet",dest="write_parquet",action="store_false");p.add_argument("--write-csv",dest="write_csv",action="store_true",default=False);p.add_argument("--no-write-csv",dest="write_csv",action="store_false");return p.parse_args()
def main()->int:
    a=parse_args();m=compile_v552j_run(run_id=a.run_id,v551j_manifest_path=a.v551j_manifest_path,v552_manifest_path=a.v552_manifest_path,output_root=a.output_root,write_parquet=a.write_parquet,write_csv=a.write_csv);print(json.dumps(m,indent=2,ensure_ascii=False));return 0
if __name__=="__main__":raise SystemExit(main())