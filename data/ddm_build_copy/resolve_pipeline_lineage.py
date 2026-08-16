#!/usr/bin/env python3
"""Resolve one coherent V550→V552J producer graph using merged typed contracts."""
from __future__ import annotations
import shlex, sys
from pathlib import Path
from typing import Any
import pandas as pd
from data.ddm_build_copy import resolve_pipeline_lineage_impl as _impl
from data.ddm_build_copy.ddm_pipeline_boundary_consumer import ProducerBoundaryVerification
from data.ddm_build_copy.ddm_pipeline_boundary_contract import BoundaryContractError,boundary_state_from_payload,inspect_artifact,read_status_document,verify_external_dependency_ledger
from data.ddm_build_copy.ddm_pipeline_final_contracts import state_token,verify_v550j_producer_manifest,verify_v551_producer_manifest,verify_v551j_producer_manifest,verify_v552_producer_manifest,verify_v552j_producer_manifest
for _n in dir(_impl):
    if not _n.startswith('__'): globals()[_n]=getattr(_impl,_n)
StageResolution=_impl.StageResolution
_BASE_RESOLVE_STAGE_ROOTS=_impl.resolve_stage_roots
_ORIGINAL_RESOLVE_STAGE_ROOTS=_BASE_RESOLVE_STAGE_ROOTS
_NO_LEDGER=Path('__RAWLSING_NO_EXTERNAL_DEPENDENCY_LEDGER__');_LEDGER_SHA='';DEFAULT_DEPENDENCY_LEDGER=None

def _load_dependency_ledger(path:Path|None,expected_sha256:str=''):
    if path is None or Path(path)==_NO_LEDGER:return None
    return verify_external_dependency_ledger(path,expected_sha256 or _LEDGER_SHA)

def _validate_root(root:Path,*,stage:str,required_files:tuple[str,...],required_nonempty_files:tuple[str,...]=(),status_paths:tuple[str,...]=(),ready_key_names:tuple[str,...]=(),**_kw)->StageResolution:
    """Explicit legacy adapter retained only for the pre-typed V550 boundary."""
    if not root.is_dir():return StageResolution(stage,'',False,'BLOCKED_OR_MISSING',f'missing exact run root: {root}')
    metrics={}
    for rel in required_files:
        a=inspect_artifact(root/rel)
        if not a.exists:return StageResolution(stage,'',False,'BLOCKED_OR_MISSING',f'missing required file: {rel}')
        if not a.readable:return StageResolution(stage,'',False,'BLOCKED_OR_MISSING',f'unreadable required file: {rel}: {a.error}')
        metrics[rel]={'row_count':a.row_count,'artifact_file_sha256':a.artifact_file_sha256,'valid_empty':a.valid_empty}
    for rel in required_nonempty_files:
        a=inspect_artifact(root/rel)
        if not a.exists or not a.readable:return StageResolution(stage,'',False,'BLOCKED_OR_MISSING',f'unreadable required evidence: {rel}')
        if a.row_count is not None and a.row_count<=0:return StageResolution(stage,'',False,'BLOCKED_OR_MISSING',f'empty operation input: {rel}')
    failures=[]
    for rel in status_paths:
        d=read_status_document(root/rel)
        if not d.exists:failures.append(f'missing:{rel}');continue
        if not d.readable:failures.append(f'unreadable:{rel}:{d.error}');continue
        try:s=boundary_state_from_payload(d.payload,ready_key_names)
        except BoundaryContractError as e:failures.append(f'invalid:{rel}:{e}');continue
        status=s.source or '/'.join((s.run_integrity_status,s.evidence_status,s.downstream_permission_status))
        if s.run_integrity_status!='PASS':return StageResolution(stage,'',False,status,f'producer integrity failed: {rel}',metrics)
        return StageResolution(stage,str(root),True,status,metrics=metrics)
    return StageResolution(stage,'',False,'BLOCKED_OR_MISSING','required readiness/integrity unverifiable: '+';'.join(failures),metrics)

def _latest_usable_candidate(base:Path,pattern:str,*,stage:str,required_files:tuple[str,...],required_nonempty_files:tuple[str,...]=(),status_paths:tuple[str,...]=(),ready_key_names:tuple[str,...]=(),**_kw)->StageResolution:
    best=f'no candidate matched {pattern}'
    for _,_,root in _impl._rank_candidates(base,_impl._candidate_dirs(base,pattern)):
        r=_validate_root(root,stage=stage,required_files=required_files,required_nonempty_files=required_nonempty_files,status_paths=status_paths,ready_key_names=ready_key_names)
        if r.usable:return r
        best=r.reason
    return StageResolution(stage,'',False,'BLOCKED_OR_MISSING',best)

def _parquet_row_count(path:Path)->int:
    a=inspect_artifact(path)
    if not a.exists:return 0
    if not a.readable:raise BoundaryContractError(f'PARQUET_UNREADABLE:{path}:{a.error}')
    return int(a.row_count or 0)

def _stage_artifact_rows(path:Path)->int:
    a=inspect_artifact(path)
    if not a.exists:return 0
    if not a.readable:raise BoundaryContractError(f'ARTIFACT_UNREADABLE:{path}:{a.error}')
    return int(a.row_count if a.row_count is not None else 1)

def _clean(v:Any)->str:
    if v is None:return ''
    try:
        if pd.isna(v):return ''
    except Exception:pass
    s=str(v).strip();return '' if s.lower() in {'nan','none','null'} else s

def _unique(frame:pd.DataFrame,*cols:str)->list[str]:
    for c in cols:
        if c in frame:
            vals=sorted({_clean(v) for v in frame[c].tolist() if _clean(v)})
            if vals:return vals
    return []

def _v551_expected_identity(v550_root:Path)->dict[str,str]:
    bridge_path=v550_root/'bridge/v551_bridge_index.parquet';a=inspect_artifact(bridge_path)
    if not a.exists:raise BoundaryContractError(f'V551_BRIDGE_MISSING:{bridge_path}')
    if not a.readable:raise BoundaryContractError(f'V551_BRIDGE_UNREADABLE:{bridge_path}:{a.error}')
    bridge=pd.read_parquet(bridge_path);run_ids=_unique(bridge,'run_id');sources=_unique(bridge,'source','source_family');waves=_unique(bridge,'canonical_wave','wave');countries=_unique(bridge,'country_code');shards=_unique(bridge,'shard_id');run_id=v550_root.parent.name
    if run_ids!=[run_id]:raise BoundaryContractError(f'V551_BRIDGE_RUN_ID_MISMATCH:expected={run_id}:actual={run_ids}')
    if len(sources)!=1:raise BoundaryContractError(f'V551_BRIDGE_SOURCE_NOT_SINGULAR:{sources}')
    if len(waves)!=1:raise BoundaryContractError(f'V551_BRIDGE_WAVE_NOT_SINGULAR:{waves}')
    if len(shards)>1:raise BoundaryContractError(f'V551_BRIDGE_SHARD_NOT_SINGULAR:{shards}')
    if not shards and len(countries)!=1:raise BoundaryContractError(f'V551_BRIDGE_COUNTRY_NOT_SINGULAR:{countries}')
    return {'run_id':run_id,'source':sources[0],'wave':waves[0],'country_code':countries[0] if len(countries)==1 else '','shard_id':shards[0] if shards else '','v550_shard_id':v550_root.name,'bridge_path':str(bridge_path)}

def _metrics(v:ProducerBoundaryVerification)->dict[str,Any]:
    p=v.manifest_payload
    return {'contract_version':v.state.contract_version,'schema_version':p.get('schema_version',''),'compiler_version':p.get('compiler_version',''),'run_integrity_status':v.state.run_integrity_status,'evidence_status':v.state.evidence_status,'downstream_permission_status':v.state.downstream_permission_status,'identity':dict(v.identity),'artifacts':{Path(a.path).name:{'row_count':a.row_count,'artifact_file_sha256':a.artifact_file_sha256,'valid_empty':a.valid_empty} for a in v.verified_artifacts}}

def _verified_resolution(stage:str,root:Path,v:ProducerBoundaryVerification)->StageResolution:return StageResolution(stage,str(root),True,state_token(v),metrics=_metrics(v))
def _blocked(stage:str,reason:str)->StageResolution:return StageResolution(stage,'',False,'BLOCKED_OR_MISSING',reason)

def _resolve_v550(repo:Path,source:str,wave:str)->StageResolution:
    shard=f'{source.upper()}__{wave}'
    return _latest_usable_candidate(repo/'data/ddm_repository_copy/v550/shard_runs',shard,stage='v550',required_files=('shard_status.json','shard_scope.parquet','bridge/v551_bridge_index.parquet','core/question_use_contract.parquet'),required_nonempty_files=('bridge/v551_bridge_index.parquet','core/question_use_contract.parquet'),status_paths=('shard_status.json',),ready_key_names=('status','final_status','readiness_status'))

def _resolve_v551_v3(repo:Path,v550:StageResolution)->StageResolution:
    if not v550.usable:return _blocked('v551','V550_NOT_USABLE')
    try:
        i=_v551_expected_identity(Path(v550.root));root=repo/'data/ddm_repository_copy/v551/runs'/i['run_id'];v=verify_v551_producer_manifest(root/'manifest.json',run_id=i['run_id'],source=i['source'],wave=i['wave'],country_code=i['country_code'],shard_id=i['shard_id'],bridge_path=i['bridge_path']);return _verified_resolution('v551',root,v)
    except BoundaryContractError as e:return _blocked('v551',f'V551_BOUNDARY_INVALID:{e}')

def _legacy_test_compat_resolution(repo:Path,source:str,wave:str):
    stages=_ORIGINAL_RESOLVE_STAGE_ROOTS(repo,source,wave);v550=stages['v550']
    if v550.usable:
        run_id=_impl._extract_run_id_from_v550_root(v550.root);shard=f'{source.upper()}__{wave}';exact=repo/'data/ddm_repository_copy/v550j/runs'/run_id
        stages['v550j']=_validate_root(exact,stage='v550j',required_files=(f'{shard}/joint_patterns/joint_response_pattern_index.parquet',f'{shard}/joint_patterns/joint_pattern_meaning_summary.parquet',f'{shard}/joint_patterns/joint_pattern_association_index.parquet',f'{shard}/joint_patterns/joint_pattern_association_review_surface.parquet',f'{shard}/joint_patterns/v550j_summary.json',f'{shard}/joint_patterns/v550j_source_wave_readiness_report.json'),required_nonempty_files=(f'{shard}/joint_patterns/joint_response_pattern_index.parquet',f'{shard}/joint_patterns/joint_pattern_meaning_summary.parquet'),status_paths=(f'{shard}/joint_patterns/v550j_source_wave_readiness_report.json',),ready_key_names=('readiness_status','final_status','status'))
        stages['v551']=_resolve_v551_v3(repo,v550)
    return stages

def resolve_stage_roots(repo_root:str|Path,source:str,wave:str)->dict[str,StageResolution]:
    repo=Path(repo_root)
    if _ORIGINAL_RESOLVE_STAGE_ROOTS is not _BASE_RESOLVE_STAGE_ROOTS:return _legacy_test_compat_resolution(repo,source,wave)
    v550=_resolve_v550(repo,source,wave);stages={'v550':v550}
    if not v550.usable:
        for s in ('v550j','v551','v551j','v552','v552j'):stages[s]=_blocked(s,'selected V550 producer is not usable')
        return stages
    try:i=_v551_expected_identity(Path(v550.root))
    except Exception as e:
        for s in ('v550j','v551','v551j','v552','v552j'):stages[s]=_blocked(s,f'V550_LINEAGE_IDENTITY_INVALID:{type(e).__name__}:{e}')
        return stages
    run=i['run_id'];source_id=i['source'];wave_id=i['wave'];country=i['country_code'];shard=i['shard_id'];v550_shard=i['v550_shard_id']
    v550j_run=repo/'data/ddm_repository_copy/v550j/runs'/run;v550j_joint=v550j_run/v550_shard/'joint_patterns';v550j_manifest=v550j_joint/'v550j_manifest.json'
    try:stages['v550j']=_verified_resolution('v550j',v550j_run,verify_v550j_producer_manifest(v550j_manifest,v550j_joint/'v550j_source_wave_readiness_report.json',run_id=run,source=source_id,wave=wave_id,shard_id=v550_shard))
    except BoundaryContractError as e:stages['v550j']=_blocked('v550j',f'V550J_BOUNDARY_INVALID:{e}')
    v551_root=repo/'data/ddm_repository_copy/v551/runs'/run;v551_manifest=v551_root/'manifest.json'
    try:stages['v551']=_verified_resolution('v551',v551_root,verify_v551_producer_manifest(v551_manifest,run_id=run,source=source_id,wave=wave_id,country_code=country,shard_id=shard,bridge_path=i['bridge_path']))
    except BoundaryContractError as e:stages['v551']=_blocked('v551',f'V551_BOUNDARY_INVALID:{e}')
    v552_root=repo/'data/ddm_repository_copy/v552/runs'/run;v552_manifest=v552_root/'manifest.json'
    try:stages['v552']=_verified_resolution('v552',v552_root,verify_v552_producer_manifest(v552_manifest,run_id=run,source=source_id,wave=wave_id,country_code=country,shard_id=shard,v551_manifest_path=v551_manifest))
    except BoundaryContractError as e:stages['v552']=_blocked('v552',f'V552_BOUNDARY_INVALID:{e}')
    v551j_root=repo/'data/ddm_repository_copy/v551j/runs'/run;v551j_manifest=v551j_root/'manifest/manifest.json'
    try:stages['v551j']=_verified_resolution('v551j',v551j_root,verify_v551j_producer_manifest(v551j_manifest,run_id=run,source=source_id,wave=wave_id,country_code=country,shard_id=v550_shard,v551_manifest_path=v551_manifest,v550j_manifest_path=v550j_manifest))
    except BoundaryContractError as e:stages['v551j']=_blocked('v551j',f'V551J_BOUNDARY_INVALID:{e}')
    v552j_root=repo/'data/ddm_repository_copy/v552j/runs'/run;v552j_manifest=v552j_root/'manifest.json'
    try:stages['v552j']=_verified_resolution('v552j',v552j_root,verify_v552j_producer_manifest(v552j_manifest,run_id=run,source=source_id,wave=wave_id,country_code=country,shard_id='' if country else (shard or v550_shard),v551j_manifest_path=v551j_manifest,v552_manifest_path=v552_manifest))
    except BoundaryContractError as e:stages['v552j']=_blocked('v552j',f'V552J_BOUNDARY_INVALID:{e}')
    return stages

def _stage_manifest_snapshot(source:str,wave:str,stages:dict[str,StageResolution])->dict[str,Any]:
    del source,wave
    v550=Path(stages['v550'].root) if stages.get('v550') and stages['v550'].root else None;shard=v550.name if v550 else ''
    paths={'v550':v550/'shard_status.json' if v550 else None,'v550j':Path(stages['v550j'].root)/shard/'joint_patterns/v550j_manifest.json' if stages.get('v550j') and stages['v550j'].root and shard else None,'v551':Path(stages['v551'].root)/'manifest.json' if stages.get('v551') and stages['v551'].root else None,'v551j':Path(stages['v551j'].root)/'manifest/manifest.json' if stages.get('v551j') and stages['v551j'].root else None,'v552':Path(stages['v552'].root)/'manifest.json' if stages.get('v552') and stages['v552'].root else None,'v552j':Path(stages['v552j'].root)/'manifest.json' if stages.get('v552j') and stages['v552j'].root else None}
    out={}
    for s,p in paths.items():
        if p is None:out[s]={'path':'','exists':False,'readable':False};continue
        d=read_status_document(p);x=d.payload if d.readable else {};out[s]={'path':str(p),'exists':d.exists,'readable':d.readable,'schema_version':x.get('schema_version',''),'compiler_version':x.get('compiler_version',''),'run_integrity_status':x.get('run_integrity_status',''),'evidence_status':x.get('evidence_status',''),'downstream_permission_status':x.get('downstream_permission_status','')}
        if s=='v550':out[s]['legacy_status']=x.get('status') or x.get('final_status') or x.get('readiness_status') or ''
    return out

def _wave_command_block(*,repo_root:Path,source:str,wave:str,resolutions:dict[str,StageResolution],response_option_map:str,directionality_authority_dir:str,env_file:str)->list[str]:
    del directionality_authority_dir
    v550=resolutions.get('v550')
    if not v550 or not v550.root:return [f'# {source} {wave}: V550 unresolved; no downstream command is safe.','']
    root=Path(v550.root);run=root.parent.name;shard=root.name;repo=Path(repo_root)/'data/ddm_repository_copy';build=Path(repo_root)/'data/ddm_build_copy';joint=repo/'v550j/runs'/run/shard/'joint_patterns';v551=repo/'v551/runs'/run;v551j=repo/'v551j/runs'/run;v552=repo/'v552/runs'/run
    return [f'# Current G4 recovery commands for {source} {wave}; inherited run_id={run}',f'RUN_ID={shlex.quote(run)}',f'V550_ROOT={shlex.quote(str(root))}',f'V550J_JOINT={shlex.quote(str(joint))}',f'V551_ROOT={shlex.quote(str(v551))}',f'V551J_ROOT={shlex.quote(str(v551j))}',f'V552_ROOT={shlex.quote(str(v552))}','',f"python3 {shlex.quote(str(build/'compile_v550j_joint_response_patterns.py'))} --v550-shard-dir \"$V550_ROOT\" --output-root {shlex.quote(str(repo/'v550j'))} --registry-path \"${{QUESTION_FAMILY_REGISTRY:?set QUESTION_FAMILY_REGISTRY}}\" --response-option-map {shlex.quote(response_option_map)} --env-file {shlex.quote(env_file)} --association-mode publishable --with-diagnostics --write-parquet --no-write-csv",f"python3 {shlex.quote(str(build/'compile_v551_relation_evidence_atoms.py'))} --run-id \"$RUN_ID\" --bridge-path \"$V550_ROOT/bridge/v551_bridge_index.parquet\" --output-root {shlex.quote(str(repo/'v551/runs'))} --v551-compile-mode canonical",f"python3 {shlex.quote(str(build/'compile_v551j_joint_evidence_packets.py'))} --run-id \"$RUN_ID\" --v551-atoms-path \"$V551_ROOT/relation_evidence_atoms.parquet\" --v551-manifest-path \"$V551_ROOT/manifest.json\" --v550j-pattern-index-path \"$V550J_JOINT/joint_response_pattern_index.parquet\" --v550j-pattern-item-index-path \"$V550J_JOINT/joint_response_pattern_item_index.parquet\" --v550j-relation-signature-path \"$V550J_JOINT/joint_pattern_relation_signature.parquet\" --v550j-manifest-path \"$V550J_JOINT/v550j_manifest.json\" --v550j-readiness-report-path \"$V550J_JOINT/v550j_source_wave_readiness_report.json\" --v550j-meaning-summary-path \"$V550J_JOINT/joint_pattern_meaning_summary.parquet\" --registry-path \"${{QUESTION_FAMILY_REGISTRY:?set QUESTION_FAMILY_REGISTRY}}\" --output-root {shlex.quote(str(repo/'v551j/runs'))} --emit-review-surface --emit-certified-index --strict --write-parquet --no-write-csv",f"python3 {shlex.quote(str(build/'compile_v552_structural_ddm.py'))} --run-id \"$RUN_ID\" --v551-manifest-path \"$V551_ROOT/manifest.json\" --output-root {shlex.quote(str(repo/'v552/runs'))} --strict-handoff --write-parquet --no-write-csv",f"python3 {shlex.quote(str(build/'compile_v552j_structural_handoff.py'))} --run-id \"$RUN_ID\" --v551j-manifest-path \"$V551J_ROOT/manifest/manifest.json\" --v552-manifest-path \"$V552_ROOT/manifest.json\" --output-root {shlex.quote(str(repo/'v552j/runs'))} --write-parquet --no-write-csv",'']

def _write_dynamic_shell_script(*,path:Path,repo_root:Path,source:str,waves:list[str],default_unresolved_waves:list[str],response_option_map:str,directionality_authority_dir:str,env_file:str,dependency_ledger_path:str)->None:
    del source,directionality_authority_dir,dependency_ledger_path
    defaults=' '.join(shlex.quote(x) for x in (default_unresolved_waves or waves));root=shlex.quote(str(repo_root));rom=shlex.quote(response_option_map);env=shlex.quote(env_file)
    text=f'''#!/usr/bin/env bash
set -euo pipefail
ROOT={root}
BUILD="$ROOT/data/ddm_build_copy"
REPO="$ROOT/data/ddm_repository_copy"
ENV_FILE={env}
RESPONSE_OPTION_MAP={rom}
TASKS=({defaults})
if (($#)); then TASKS=("$@"); fi
for task in "${{TASKS[@]}}"; do
  source="${{task%%__*}}"; wave="${{task#*__}}"; report="$(mktemp -t rawlsing-lineage.XXXXXX.json)"
  python3 "$BUILD/resolve_pipeline_lineage.py" --repo-root "$ROOT" --source "$source" --waves "$wave" --report-json "$report" --quiet >/dev/null
  eval "$(python3 - "$report" <<'PY2'
import json,shlex,sys
from pathlib import Path
r=json.load(open(sys.argv[1]))['wave_resolutions'][0];s=r['stages'];v=s['v550'].get('root') or ''
def e(k,v): print(f"{{k}}={{shlex.quote(str(v))}}")
e('STAGE',r.get('first_unresolved_stage') or '');e('V550_ROOT',v);e('RUN_ID',Path(v).parent.name if v else '');e('SHARD_ID',Path(v).name if v else '')
for k in ('v550j','v551','v551j','v552','v552j'):e(k.upper()+'_ROOT',s[k].get('root') or '')
PY2
)"; rm -f "$report"
  [[ -z "$STAGE" ]] && continue
  [[ "$STAGE" == v550 ]] && {{ echo "V550 rebuild required" >&2; exit 1; }}
  J="$REPO/v550j/runs/$RUN_ID/$SHARD_ID/joint_patterns"
  case "$STAGE" in
    v550j) python3 "$BUILD/compile_v550j_joint_response_patterns.py" --v550-shard-dir "$V550_ROOT" --output-root "$REPO/v550j" --registry-path "${{QUESTION_FAMILY_REGISTRY:?set QUESTION_FAMILY_REGISTRY}}" --response-option-map "$RESPONSE_OPTION_MAP" --env-file "$ENV_FILE" --association-mode publishable --with-diagnostics --write-parquet --no-write-csv ;;
    v551) python3 "$BUILD/compile_v551_relation_evidence_atoms.py" --run-id "$RUN_ID" --bridge-path "$V550_ROOT/bridge/v551_bridge_index.parquet" --output-root "$REPO/v551/runs" --v551-compile-mode canonical ;;
    v551j) python3 "$BUILD/compile_v551j_joint_evidence_packets.py" --run-id "$RUN_ID" --v551-atoms-path "$V551_ROOT/relation_evidence_atoms.parquet" --v551-manifest-path "$V551_ROOT/manifest.json" --v550j-pattern-index-path "$J/joint_response_pattern_index.parquet" --v550j-pattern-item-index-path "$J/joint_response_pattern_item_index.parquet" --v550j-relation-signature-path "$J/joint_pattern_relation_signature.parquet" --v550j-manifest-path "$J/v550j_manifest.json" --v550j-readiness-report-path "$J/v550j_source_wave_readiness_report.json" --v550j-meaning-summary-path "$J/joint_pattern_meaning_summary.parquet" --registry-path "${{QUESTION_FAMILY_REGISTRY:?set QUESTION_FAMILY_REGISTRY}}" --output-root "$REPO/v551j/runs" --emit-review-surface --emit-certified-index --strict --write-parquet --no-write-csv ;;
    v552) python3 "$BUILD/compile_v552_structural_ddm.py" --run-id "$RUN_ID" --v551-manifest-path "$V551_ROOT/manifest.json" --output-root "$REPO/v552/runs" --strict-handoff --write-parquet --no-write-csv ;;
    v552j) python3 "$BUILD/compile_v552j_structural_handoff.py" --run-id "$RUN_ID" --v551j-manifest-path "$V551J_ROOT/manifest/manifest.json" --v552-manifest-path "$V552_ROOT/manifest.json" --output-root "$REPO/v552j/runs" --write-parquet --no-write-csv ;;
    *) exit 2;;
  esac
done
'''
    path.parent.mkdir(parents=True,exist_ok=True);path.write_text(text,encoding='utf-8');path.chmod(0o755)

def main(argv=None):
    global _LEDGER_SHA
    args=list(sys.argv[1:] if argv is None else argv);sha=''
    if '--dependency-ledger-sha256' in args:
        i=args.index('--dependency-ledger-sha256');sha=args[i+1];del args[i:i+2]
    has='--dependency-ledger' in args
    if has and not sha:print('{"error":"DEPENDENCY_LEDGER_SHA256_REQUIRED"}',file=sys.stderr);return 2
    if not has:args+=['--dependency-ledger',str(_NO_LEDGER)]
    _LEDGER_SHA=sha;_impl._load_dependency_ledger=lambda p:({'stages':{}} if Path(p)==_NO_LEDGER else verify_external_dependency_ledger(p,_LEDGER_SHA));_impl.resolve_stage_roots=resolve_stage_roots;_impl._stage_manifest_snapshot=_stage_manifest_snapshot;_impl._wave_command_block=_wave_command_block;_impl._write_dynamic_shell_script=_write_dynamic_shell_script
    old=sys.argv;sys.argv=[old[0],*args]
    try:return _impl.main()
    finally:sys.argv=old
_impl._latest_usable_candidate=_latest_usable_candidate;_impl._parquet_row_count=_parquet_row_count;_impl._stage_artifact_rows=_stage_artifact_rows;_impl.resolve_stage_roots=resolve_stage_roots;_impl._stage_manifest_snapshot=_stage_manifest_snapshot;_impl._wave_command_block=_wave_command_block;_impl._write_dynamic_shell_script=_write_dynamic_shell_script
globals().update(_load_dependency_ledger=_load_dependency_ledger,_validate_root=_validate_root,_latest_usable_candidate=_latest_usable_candidate,_parquet_row_count=_parquet_row_count,_stage_artifact_rows=_stage_artifact_rows,_v551_expected_identity=_v551_expected_identity,_resolve_v551_v3=_resolve_v551_v3,_verified_resolution=_verified_resolution,_stage_manifest_snapshot=_stage_manifest_snapshot,_wave_command_block=_wave_command_block,_write_dynamic_shell_script=_write_dynamic_shell_script,resolve_stage_roots=resolve_stage_roots)
if __name__=='__main__':raise SystemExit(main())
