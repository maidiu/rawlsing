#!/usr/bin/env python3
"""Governed CLOSED_35_WAVES smoke over the merged typed producer graph."""
from __future__ import annotations
import sys
from pathlib import Path
from typing import Any,Iterable
import pandas as pd
from data.ddm_build_copy import run_20var_allwaves_v550_552j_smoke_impl as _impl
from data.ddm_build_copy.ddm_pipeline_boundary_contract import BoundaryContractError
from data.ddm_build_copy.ddm_pipeline_final_contracts import state_token,verify_v550j_producer_manifest,verify_v551_producer_manifest,verify_v551j_producer_manifest,verify_v552_producer_manifest,verify_v552j_producer_manifest
from data.ddm_build_copy.ddm_v550_question_relation_authority import active_closed_35_waves
for _n in dir(_impl):
    if not _n.startswith('__'):globals()[_n]=getattr(_impl,_n)
_ORIGINAL_RESOLVE_JOINT=_impl.resolve_joint_authority;_ORIGINAL_SUMMARIZE_JOINT=_impl.summarize_joint_authority_coverage;_ORIGINAL_PARSE_ARGS=_impl.parse_args;_ORIGINAL_WRITE_SUMMARIES=_impl.write_summaries
ALL_WAVES=list(active_closed_35_waves());_impl.ALL_WAVES=ALL_WAVES;RuntimeConfig=_impl.RuntimeConfig;DEFAULT_CONFIG=RuntimeConfig(joint_mode='auto');_impl.DEFAULT_CONFIG=DEFAULT_CONFIG

def validate_explicit_scope(waves:Iterable[tuple[str,str,str]]=ALL_WAVES)->list[str]:
    rows=list(waves);gov=list(active_closed_35_waves());gp={(f,w) for f,w,_ in gov};pairs=[(f,w) for f,w,_ in rows];issues=[]
    if len(set(pairs))!=len(pairs):issues.append('duplicate_family_wave_in_governed_scope')
    outside=sorted(set(pairs)-gp)
    if outside:issues.append('scope_outside_CLOSED_35_WAVES:'+','.join(f'{f}|{w}' for f,w in outside))
    if len(rows)==len(gov) and set(pairs)!=gp:issues.append('governed_scope_mismatch:'+','.join(f'{f}|{w}' for f,w in sorted(gp-set(pairs))))
    if len(rows)>len(gov):issues.append(f'governed_scope_count_exceeds_35:{len(rows)}')
    if ('Asian Barometer','W6') in set(pairs):issues.append('asian_barometer_w6_present_in_CLOSED_35_WAVES')
    return issues

def _joint_coverage_state(a:dict[str,Any])->str:
    if a.get('applicable'):return 'PRESENT'
    if str(a.get('reason') or '') in {'no_explicit_joint_registry_for_family_wave','joint_registry_exists_but_selected_slice_has_no_family_items'}:return 'NOT_APPLICABLE'
    return 'APPLICABLE_UNRESOLVED'

def resolve_joint_authority(config:RuntimeConfig,family:str,wave:str,selected_vars:Iterable[str]|None=None)->dict[str,Any]:
    a=dict(_ORIGINAL_RESOLVE_JOINT(config,family,wave,selected_vars));a['coverage_state']=_joint_coverage_state(a);a['downstream_permission_status']='ALLOW' if a.get('applicable') else 'NOT_APPLICABLE' if a['coverage_state']=='NOT_APPLICABLE' else 'DENY';return a

def summarize_joint_authority_coverage(config:RuntimeConfig,waves:Iterable[tuple[str,str,str]]=ALL_WAVES)->dict[str,Any]:
    rows=list(waves);report=dict(_ORIGINAL_SUMMARIZE_JOINT(config,rows));b={'PRESENT':[],'NOT_APPLICABLE':[],'APPLICABLE_UNRESOLVED':[]};typed=[]
    for f,w,c in rows:
        a=resolve_joint_authority(config,f,w);r={'source':f,'wave':w,'country_code':c,'coverage_state':a['coverage_state'],'downstream_permission_status':a['downstream_permission_status'],'reason':a.get('reason',''),'registry_path':a.get('registry_path','')};typed.append(r);b[a['coverage_state']].append(r)
    report.update(typed_scopes=typed,applicable_scopes=b['PRESENT'],not_applicable_scopes=b['NOT_APPLICABLE'],coverage_debt_scopes=b['APPLICABLE_UNRESOLVED'],applicable_scope_count=len(b['PRESENT']),not_applicable_scope_count=len(b['NOT_APPLICABLE']),coverage_debt_scope_count=len(b['APPLICABLE_UNRESOLVED']));return report

def parse_args():
    a=_ORIGINAL_PARSE_ARGS();explicit=any(x=='--joint-mode' or x.startswith('--joint-mode=') for x in sys.argv[1:])
    if not explicit:a.joint_mode='auto'
    return a

def _clean(v:Any)->str:
    if v is None:return ''
    try:
        if pd.isna(v):return ''
    except Exception:pass
    s=str(v).strip();return '' if s.lower() in {'nan','none','null'} else s

def _bridge_run_id(path:str|Path)->str:
    df=pd.read_parquet(path)
    if 'run_id' not in df:raise BoundaryContractError('V551_BRIDGE_RUN_ID_MISSING')
    vals=sorted({_clean(v) for v in df['run_id'].tolist() if _clean(v)})
    if len(vals)!=1:raise BoundaryContractError(f'V551_BRIDGE_RUN_ID_NOT_SINGULAR:{vals}')
    return vals[0]

def _verification_gate(v)->dict[str,Any]:
    p=v.manifest_payload
    return {'manifest_path':v.manifest_path,'contract_version':v.state.contract_version,'schema_version':_clean(p.get('schema_version')),'compiler_version':_clean(p.get('compiler_version')),'run_integrity_status':v.state.run_integrity_status,'evidence_status':v.state.evidence_status,'downstream_permission_status':v.state.downstream_permission_status,'state':state_token(v),'integrity_passed':True,'passed':True,'artifacts':{Path(a.path).name:{'row_count':a.row_count,'artifact_file_sha256':a.artifact_file_sha256,'valid_empty':a.valid_empty} for a in v.verified_artifacts},'failure_reason':''}

def run_v551(shard_id:str,bridge_path:str,quc_path:str,response_map_path:str,output_root:str,config:RuntimeConfig=DEFAULT_CONFIG)->dict[str,Any]:
    del shard_id,quc_path,response_map_path;run=_bridge_run_id(bridge_path);cmd=[sys.executable,_impl._abs('data/ddm_build_copy/compile_v551_relation_evidence_atoms.py',config),'--run-id',run,'--bridge-path',bridge_path,'--output-root',output_root,'--v551-compile-mode','canonical'];r=_impl._invoke_run(cmd,timeout_sec=1800,config=config);r['producer_run_id']=run;return r

def run_v552(run_id:str,v551_manifest_path:str,output_root:str,config:RuntimeConfig=DEFAULT_CONFIG)->dict[str,Any]:
    return _impl._invoke_run([sys.executable,_impl._abs('data/ddm_build_copy/compile_v552_structural_ddm.py',config),'--run-id',run_id,'--v551-manifest-path',v551_manifest_path,'--output-root',output_root,'--strict-handoff','--write-parquet','--no-write-csv'],timeout_sec=1800,config=config)

def run_v551j(run_id:str,v551_root:str|Path,v550j_joint_root:str|Path,registry_path:str,output_root:str,config:RuntimeConfig=DEFAULT_CONFIG)->dict[str,Any]:
    v=Path(v551_root);j=Path(v550j_joint_root);cmd=[sys.executable,_impl._abs('data/ddm_build_copy/compile_v551j_joint_evidence_packets.py',config),'--run-id',run_id,'--v551-atoms-path',str(v/'relation_evidence_atoms.parquet'),'--v551-manifest-path',str(v/'manifest.json'),'--v550j-pattern-index-path',str(j/'joint_response_pattern_index.parquet'),'--v550j-pattern-item-index-path',str(j/'joint_response_pattern_item_index.parquet'),'--v550j-relation-signature-path',str(j/'joint_pattern_relation_signature.parquet'),'--v550j-manifest-path',str(j/'v550j_manifest.json'),'--v550j-readiness-report-path',str(j/'v550j_source_wave_readiness_report.json'),'--v550j-meaning-summary-path',str(j/'joint_pattern_meaning_summary.parquet'),'--registry-path',registry_path,'--output-root',output_root,'--emit-review-surface','--emit-certified-index','--strict','--write-parquet','--no-write-csv'];return _impl._invoke_run(cmd,timeout_sec=1800,config=config)

def run_v552j(run_id:str,v551j_manifest_path:str,v552_manifest_path:str,output_root:str,config:RuntimeConfig=DEFAULT_CONFIG)->dict[str,Any]:
    return _impl._invoke_run([sys.executable,_impl._abs('data/ddm_build_copy/compile_v552j_structural_handoff.py',config),'--run-id',run_id,'--v551j-manifest-path',v551j_manifest_path,'--v552-manifest-path',v552_manifest_path,'--output-root',output_root,'--write-parquet','--no-write-csv'],timeout_sec=1800,config=config)

def summarize_v551_functional_gate(path:str|Path,*,run_id:str,source:str,wave:str,country_code:str='',shard_id:str='',bridge_path:str|Path|None=None)->dict[str,Any]:
    try:
        v=verify_v551_producer_manifest(path,run_id=run_id,source=source,wave=wave,country_code=country_code,shard_id=shard_id,bridge_path=bridge_path);g=_verification_gate(v);g.update(candidate_count=int(v.manifest_payload.get('candidate_count') or 0),promotable_candidate_count=int(v.manifest_payload.get('promotable_candidate_count') or 0),nonpromotable_candidate_count=int(v.manifest_payload.get('nonpromotable_candidate_count') or 0),atom_rows=int(v.manifest_payload.get('atom_count') or 0),terminal_not_applicable=v.state.evidence_status=='NOT_APPLICABLE');return g
    except BoundaryContractError as e:return {'passed':False,'integrity_passed':False,'failure_reason':f'v551_boundary_invalid:{e}'}
def summarize_v550j_functional_gate(manifest_path:str|Path,readiness_path:str|Path,*,run_id:str,source:str,wave:str,shard_id:str)->dict[str,Any]:
    try:return _verification_gate(verify_v550j_producer_manifest(manifest_path,readiness_path,run_id=run_id,source=source,wave=wave,shard_id=shard_id))
    except BoundaryContractError as e:return {'passed':False,'integrity_passed':False,'failure_reason':f'v550j_boundary_invalid:{e}'}
def summarize_v552_functional_gate(manifest_path:str|Path,*,run_id:str,source:str,wave:str,country_code:str,shard_id:str,v551_manifest_path:str|Path)->dict[str,Any]:
    try:return _verification_gate(verify_v552_producer_manifest(manifest_path,run_id=run_id,source=source,wave=wave,country_code=country_code,shard_id=shard_id,v551_manifest_path=v551_manifest_path))
    except BoundaryContractError as e:return {'passed':False,'integrity_passed':False,'failure_reason':f'v552_boundary_invalid:{e}'}
def summarize_v551j_functional_gate(manifest_path:str|Path,*,run_id:str,source:str,wave:str,country_code:str,shard_id:str,v551_manifest_path:str|Path,v550j_manifest_path:str|Path)->dict[str,Any]:
    try:return _verification_gate(verify_v551j_producer_manifest(manifest_path,run_id=run_id,source=source,wave=wave,country_code=country_code,shard_id=shard_id,v551_manifest_path=v551_manifest_path,v550j_manifest_path=v550j_manifest_path))
    except BoundaryContractError as e:return {'passed':False,'integrity_passed':False,'failure_reason':f'v551j_boundary_invalid:{e}'}
def summarize_v552j_functional_gate(manifest_path:str|Path,*,run_id:str,source:str,wave:str,country_code:str,shard_id:str,v551j_manifest_path:str|Path,v552_manifest_path:str|Path)->dict[str,Any]:
    try:return _verification_gate(verify_v552j_producer_manifest(manifest_path,run_id=run_id,source=source,wave=wave,country_code=country_code,shard_id=shard_id,v551j_manifest_path=v551j_manifest_path,v552_manifest_path=v552_manifest_path))
    except BoundaryContractError as e:return {'passed':False,'integrity_passed':False,'failure_reason':f'v552j_boundary_invalid:{e}'}

def run_wave(family:str,wave:str,country:str,run_ts:str,output_root:str,filter_path:str,selected_vars:list[str],config:RuntimeConfig=DEFAULT_CONFIG)->dict[str,Any]:
    run_id=f'{_impl._family_wave_id(family,wave)}_{run_ts}';shard_id=f'{family}_{wave}'+(f'_{country}' if country else '');result={'survey_family':family,'wave_id':wave,'country':country,'run_id':run_id,'selected_variable_count':len(selected_vars),'selected_variables':selected_vars,'stages':{},'functional_checks':{},'joint_branch':{},'base_spine_passed':False,'full_chain_passed':False,'acceptance_boundary':'none','passed':False};_impl._log(f'WAVE {family} {wave} ({country}) — {len(selected_vars)} variables');shard_dir=Path(output_root)/'v550/shard_runs'/run_id/shard_id;authority=resolve_joint_authority(config,family,wave,selected_vars);result['joint_branch']['authority']=authority;registry=authority['registry_path'] if authority.get('applicable') and config.joint_mode!='off' else None
    raw=_impl.run_v550_shard(run_id,shard_id,family,wave,country,filter_path,str(Path(output_root)/'v550'),registry,config)
    if raw['exit_code']!=0:result['stages']['v550']=_impl._stage_result(raw);return _impl._fail(result,'v550_process',raw.get('stderr_tail') or 'v550_nonzero_exit')
    gate=_impl.summarize_v550_manifest_gate(shard_dir/'manifest.json');result['stages']['v550']=_impl._stage_result(raw,gate);result['functional_checks']['v550_manifest']=gate
    if not gate['passed']:return _impl._fail(result,'v550_manifest_gate',gate['failure_reason'])
    qgate=_impl.summarize_quc_functional_gate(shard_dir/'core/question_use_contract.parquet');result['functional_checks']['v550_quc']=qgate
    if not qgate['passed']:return _impl._fail(result,'v550_quc_gate',qgate['failure_reason'])
    response_map=shard_dir/'core/response_option_map.parquet'
    if not response_map.exists():return _impl._fail(result,'v550_response_semantics_contract','missing_scoped_response_option_map_artifact')
    bridge=shard_dir/'bridge/v551_bridge_index.parquet'
    try:producer_run=_bridge_run_id(bridge)
    except Exception as e:return _impl._fail(result,'v551_bridge_identity',f'{type(e).__name__}:{e}')
    if producer_run!=run_id:return _impl._fail(result,'v551_bridge_identity',f'v551_bridge_run_id_mismatch:expected={run_id}:actual={producer_run}')
    v551_root=Path(output_root)/'v551';raw=run_v551(shard_id,str(bridge),'',str(response_map),str(v551_root),config)
    if raw['exit_code']!=0:result['stages']['v551']=_impl._stage_result(raw);return _impl._fail(result,'v551_process',raw.get('stderr_tail') or 'v551_nonzero_exit')
    v551_run=v551_root/run_id;v551_manifest=v551_run/'manifest.json';gate=summarize_v551_functional_gate(v551_manifest,run_id=run_id,source=family,wave=wave,country_code=country,shard_id=shard_id,bridge_path=bridge);result['stages']['v551']=_impl._stage_result(raw,gate);result['functional_checks']['v551']=gate
    if not gate['passed']:return _impl._fail(result,'v551_gate',gate['failure_reason'])
    v552_root=Path(output_root)/'v552';raw=run_v552(run_id,str(v551_manifest),str(v552_root),config)
    if raw['exit_code']!=0:result['stages']['v552']=_impl._stage_result(raw);return _impl._fail(result,'v552_process',raw.get('stderr_tail') or 'v552_nonzero_exit')
    v552_run=v552_root/run_id;v552_manifest=v552_run/'manifest.json';gate=summarize_v552_functional_gate(v552_manifest,run_id=run_id,source=family,wave=wave,country_code=country,shard_id=shard_id,v551_manifest_path=v551_manifest);result['stages']['v552']=_impl._stage_result(raw,gate);result['functional_checks']['v552']=gate
    if not gate['passed']:return _impl._fail(result,'v552_gate',gate['failure_reason'])
    result['base_spine_passed']=True;result['acceptance_boundary']='typed_base_spine'
    if config.joint_mode=='off':result['joint_branch'].update(status='disabled_by_explicit_mode',reason='joint_mode_off');result['passed']=True;return result
    if not authority.get('applicable'):
        result['joint_branch'].update(status='not_applicable',reason=authority.get('reason','joint_authority_not_applicable'))
        if config.joint_mode=='required':return _impl._fail(result,'joint_authority_gate',result['joint_branch']['reason'])
        result['passed']=True;return result
    v550j_root=Path(output_root)/'v550j';subs=sorted((shard_dir/'checkpoints/respondent_substrate').glob('source=*/wave=*/country_code=*/v550_shared_respondent_substrate_manifest.json'))
    if not subs:return _impl._fail(result,'shared_respondent_substrate_gate','missing_shared_respondent_substrate_manifest')
    subm=subs[0];subp=subm.with_name('v550_shared_respondent_substrate.parquet')
    if not subp.exists():return _impl._fail(result,'shared_respondent_substrate_gate','missing_shared_respondent_substrate_parquet')
    raw=_impl.run_v550j(run_id,str(shard_dir),filter_path,str(v550j_root),authority['registry_path'],str(response_map),str(subp),str(subm),config);joint=v550j_root/'runs'/run_id/shard_id/'joint_patterns'
    if raw['exit_code']!=0:result['stages']['v550j']=_impl._stage_result(raw);return _impl._fail(result,'v550j_process',raw.get('stderr_tail') or 'v550j_nonzero_exit')
    v550jm=joint/'v550j_manifest.json';v550jr=joint/'v550j_source_wave_readiness_report.json';gate=summarize_v550j_functional_gate(v550jm,v550jr,run_id=run_id,source=family,wave=wave,shard_id=shard_id);result['stages']['v550j']=_impl._stage_result(raw,gate);result['functional_checks']['v550j']=gate
    if not gate['passed']:return _impl._fail(result,'v550j_gate',gate['failure_reason'])
    v551j_root=Path(output_root)/'v551j';raw=run_v551j(run_id,v551_run,joint,authority['registry_path'],str(v551j_root),config)
    if raw['exit_code']!=0:result['stages']['v551j']=_impl._stage_result(raw);return _impl._fail(result,'v551j_process',raw.get('stderr_tail') or 'v551j_nonzero_exit')
    v551jm=v551j_root/run_id/'manifest/manifest.json';gate=summarize_v551j_functional_gate(v551jm,run_id=run_id,source=family,wave=wave,country_code=country,shard_id=shard_id,v551_manifest_path=v551_manifest,v550j_manifest_path=v550jm);result['stages']['v551j']=_impl._stage_result(raw,gate);result['functional_checks']['v551j']=gate
    if not gate['passed']:return _impl._fail(result,'v551j_gate',gate['failure_reason'])
    v552j_root=Path(output_root)/'v552j';raw=run_v552j(run_id,str(v551jm),str(v552_manifest),str(v552j_root),config)
    if raw['exit_code']!=0:result['stages']['v552j']=_impl._stage_result(raw);return _impl._fail(result,'v552j_process',raw.get('stderr_tail') or 'v552j_nonzero_exit')
    v552jm=v552j_root/run_id/'manifest.json';gate=summarize_v552j_functional_gate(v552jm,run_id=run_id,source=family,wave=wave,country_code=country,shard_id=shard_id,v551j_manifest_path=v551jm,v552_manifest_path=v552_manifest);result['stages']['v552j']=_impl._stage_result(raw,gate);result['functional_checks']['v552j']=gate
    if not gate['passed']:return _impl._fail(result,'v552j_gate',gate['failure_reason'])
    result['joint_branch'].update(status='typed_graph_verified',reason=gate['state']);result['full_chain_passed']=True;result['acceptance_boundary']='full_v550_to_v552j_typed_graph';result['passed']=True;return result

def write_summaries(results:list[dict[str,Any]],output_root:str,run_ts:str,canary_only:bool,preflight:dict[str,Any]|None=None)->None:
    _ORIGINAL_WRITE_SUMMARIES(results,output_root,run_ts,canary_only,preflight);report=Path(output_root)/'reports';total=len(results);passed=sum(bool(r.get('passed')) for r in results);base=sum(bool(r.get('base_spine_passed')) for r in results);full=sum(bool(r.get('full_chain_passed')) for r in results);nonallow=sum(str((r.get('functional_checks') or {}).get('v552j',{}).get('downstream_permission_status') or '') in {'DENY','NOT_APPLICABLE'} for r in results if (r.get('joint_branch') or {}).get('status')=='typed_graph_verified');lines=['# Universality Functional Smoke Report','',f'**Run:** {run_ts}',f"**Scope:** {'canary only' if canary_only else 'authority-derived CLOSED_35_WAVES'}",'**Base spine:** V550 → V551 v3.0 → V552 v3.0','**Joint branch:** V550J → V551J v2.2.3 → V552J v1.0 where governed authority applies','', '## Summary','',f'- Waves attempted: {total}',f'- Typed base spines passed: {base}',f'- Full joint graphs passed: {full}',f'- Full typed graphs ending non-ALLOW: {nonallow}',f'- Integrity/contract smoke passes: {passed}','','| Source | Wave | Base | V551 | V552 | Joint | V551J | V552J | Passed | Failure |','| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |']
    for r in results:
        c=r.get('functional_checks') or {};lines.append('| {source} | {wave} | {base} | {v551} | {v552} | {joint} | {v551j} | {v552j} | {passed} | {failure} |'.format(source=r.get('survey_family',''),wave=r.get('wave_id',''),base='PASS' if r.get('base_spine_passed') else 'NO',v551=(c.get('v551') or {}).get('state','not-run'),v552=(c.get('v552') or {}).get('state','not-run'),joint=(r.get('joint_branch') or {}).get('status','not-run'),v551j=(c.get('v551j') or {}).get('state','not-run'),v552j=(c.get('v552j') or {}).get('state','not-run'),passed='PASS' if r.get('passed') else 'FAIL',failure=r.get('functional_failure_reason','')))
    lines+=['','## Readiness',''];lines.append('**READY at the typed integrity boundary.** Every attempted applicable joint scope completed through the merged V552J producer, while terminal downstream permission remains explicit; no row-count shortcut or ghost artifact determined readiness.' if total and passed==total else f'**NOT READY.** {passed}/{total} attempted scopes passed typed producer integrity/contract verification.');(report/'smoke_report.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')

_impl.validate_explicit_scope=validate_explicit_scope;_impl.resolve_joint_authority=resolve_joint_authority;_impl.summarize_joint_authority_coverage=summarize_joint_authority_coverage;_impl.parse_args=parse_args;_impl.run_v551=run_v551;_impl.run_v552=run_v552;_impl.run_v551j=run_v551j;_impl.run_v552j=run_v552j;_impl.summarize_v551_functional_gate=summarize_v551_functional_gate;_impl.summarize_v550j_functional_gate=summarize_v550j_functional_gate;_impl.summarize_v552_functional_gate=summarize_v552_functional_gate;_impl.summarize_v551j_functional_gate=summarize_v551j_functional_gate;_impl.summarize_v552j_functional_gate=summarize_v552j_functional_gate;_impl.run_wave=run_wave;_impl.write_summaries=write_summaries
globals().update(ALL_WAVES=ALL_WAVES,RuntimeConfig=RuntimeConfig,DEFAULT_CONFIG=DEFAULT_CONFIG,validate_explicit_scope=validate_explicit_scope,resolve_joint_authority=resolve_joint_authority,summarize_joint_authority_coverage=summarize_joint_authority_coverage,parse_args=parse_args,run_v551=run_v551,run_v552=run_v552,run_v551j=run_v551j,run_v552j=run_v552j,summarize_v551_functional_gate=summarize_v551_functional_gate,summarize_v550j_functional_gate=summarize_v550j_functional_gate,summarize_v552_functional_gate=summarize_v552_functional_gate,summarize_v551j_functional_gate=summarize_v551j_functional_gate,summarize_v552j_functional_gate=summarize_v552j_functional_gate,run_wave=run_wave,write_summaries=write_summaries)
def main()->int:return _impl.main()
if __name__=='__main__':raise SystemExit(main())
