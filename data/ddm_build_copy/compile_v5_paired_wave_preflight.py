#!/usr/bin/env python3
"""Producer-bound paired-wave preflight for the merged V552→V557 path."""
from __future__ import annotations
import argparse,json,re,sys
from pathlib import Path
from typing import Any,Mapping
ROOT=Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
from data.ddm_build_copy.ddm_pipeline_boundary_contract import BoundaryContractError,inspect_artifact,read_status_document
from data.ddm_build_copy.ddm_pipeline_final_contracts import state_token,verify_v551j_producer_manifest,verify_v552_producer_manifest,verify_v552j_producer_manifest
from data.ddm_build_copy.ddm_v550_manifest import utc_now
from data.ddm_build_copy.ddm_survey_identity import require_survey_identity
from data.ddm_build_copy.ddm_v553_repo_discovery import latest_run_root_for_wave

def _text(v:Any)->str:return '' if v is None else str(v).strip()
def _manifest_scope_hint(path:Path,*,source:str,wave:str,country_code:str)->dict[str,str]:
    d=read_status_document(path)
    if not d.exists or not d.readable:raise BoundaryContractError(f'PREFLIGHT_MANIFEST_UNREADABLE:{path}:{d.error}')
    p=d.payload;raw=p.get('producer_scope_identity');s=dict(raw) if isinstance(raw,Mapping) else {};src=_text(s.get('source') or p.get('source'));wv=_text(s.get('canonical_wave') or s.get('wave') or p.get('canonical_wave') or p.get('wave'));country=_text(s.get('country_code') or p.get('country_code'));shard=_text(s.get('shard_id') or p.get('shard_id'))
    if src!=source or wv!=wave:raise BoundaryContractError(f'PREFLIGHT_SCOPE_MISMATCH:expected={source}/{wave}:actual={src}/{wv}')
    if country and country!=country_code:raise BoundaryContractError(f'PREFLIGHT_COUNTRY_MISMATCH:expected={country_code}:actual={country}')
    if not country and not shard:raise BoundaryContractError('PREFLIGHT_COUNTRY_OR_SHARD_IDENTITY_MISSING')
    return {'country_code':country,'shard_id':shard}
def _declared_artifact(manifest:Path,payload:Mapping[str,Any],name:str)->dict[str,Any]:
    matches=[]
    for row in payload.get('artifacts') or []:
        if isinstance(row,Mapping) and _text(row.get('artifact') or row.get('name'))==name:
            rel=_text(row.get('path') or row.get('relative_path'))
            if rel.endswith('.parquet') and _text(row.get('artifact_kind'))=='canonical':matches.append((dict(row),rel))
    if len(matches)!=1:raise BoundaryContractError(f'V552_PREFLIGHT_CANONICAL_DECLARATION_COUNT:{name}:{len(matches)}')
    row,rel=matches[0];path=(manifest.parent/rel).resolve();a=inspect_artifact(path)
    if not a.exists or not a.readable:raise BoundaryContractError(f'V552_PREFLIGHT_ARTIFACT_UNREADABLE:{name}:{a.error}')
    h=_text(row.get('artifact_file_sha256')).lower()
    if not re.fullmatch(r'[0-9a-f]{64}',h):raise BoundaryContractError(f'V552_PREFLIGHT_ARTIFACT_HASH_INVALID:{name}')
    if a.artifact_file_sha256.lower()!=h:raise BoundaryContractError(f'V552_PREFLIGHT_ARTIFACT_HASH_MISMATCH:{name}')
    if row.get('row_count') is not None and int(row['row_count'])!=int(a.row_count or 0):raise BoundaryContractError(f'V552_PREFLIGHT_ARTIFACT_ROW_COUNT_MISMATCH:{name}')
    return {'artifact':name,'path':str(path),'row_count':a.row_count,'artifact_file_sha256':a.artifact_file_sha256,'valid_empty':a.valid_empty}
def _coherent_roots(repo:Path,source:str,wave:str,country:str)->dict[str,Path|None]:
    i=require_survey_identity(source,wave,country,require_country=True);latest=latest_run_root_for_wave(repo/'data/ddm_repository_copy/v552j/runs',i.source,i.canonical_wave,i.country_code)
    if not latest:return {x:None for x in ('v550j','v551','v551j','v552','v552j','v553')}
    j=Path(latest);run=j.name;roots={'v551':repo/'data/ddm_repository_copy/v551/runs'/run,'v551j':repo/'data/ddm_repository_copy/v551j/runs'/run,'v552':repo/'data/ddm_repository_copy/v552/runs'/run,'v552j':j};v553=latest_run_root_for_wave(repo/'data/ddm_repository_copy/v553/runs',i.source,i.canonical_wave,i.country_code);roots['v553']=Path(v553) if v553 else None;roots['v550j']=repo/'data/ddm_repository_copy/v550j/runs'/run;return roots
def _wave_report(repo:Path,source:str,wave:str,country:str)->dict[str,Any]:
    i=require_survey_identity(source,wave,country,require_country=True);roots=_coherent_roots(repo,i.source,i.canonical_wave,i.country_code);missing=[];fail=[];present=[];contracts={};jroot=roots.get('v552j')
    if jroot is None:return {'source':i.source,'country_code':i.country_code,'wave':i.canonical_wave,'run_id':'','status':'blocked','latest_roots':{x:'' for x in roots},'producer_contracts':{},'present_artifacts':[],'missing_artifacts':['v552j:coherent_run_root'],'contract_failures':[],'comparison_ready':False}
    run=jroot.name;v551root=roots['v551'];v551jroot=roots['v551j'];v552root=roots['v552'];assert v551root and v551jroot and v552root
    v551m=v551root/'manifest.json';v551jm=v551jroot/'manifest/manifest.json';v552m=v552root/'manifest.json';v552jm=jroot/'manifest.json'
    try:
        s=_manifest_scope_hint(v551jm,source=i.source,wave=i.canonical_wave,country_code=i.country_code);v550jm=roots['v550j']/s['shard_id']/'joint_patterns/v550j_manifest.json' if s['shard_id'] else None
        v=verify_v551j_producer_manifest(v551jm,run_id=run,source=i.source,wave=i.canonical_wave,country_code=i.country_code,shard_id=s['shard_id'],v551_manifest_path=v551m,v550j_manifest_path=v550jm);contracts['v551j']=state_token(v);present.append('v551j:manifest/manifest.json')
    except BoundaryContractError as e:fail.append(f'v551j:{e}')
    try:
        s2=_manifest_scope_hint(v552m,source=i.source,wave=i.canonical_wave,country_code=i.country_code);v=verify_v552_producer_manifest(v552m,run_id=run,source=i.source,wave=i.canonical_wave,country_code=i.country_code,shard_id=s2['shard_id'],v551_manifest_path=v551m);contracts['v552']=state_token(v);present.append('v552:manifest.json');
        for name in ('v552_artifact_authority_index','v552_known_absence_register'):present.append('v552:'+_declared_artifact(v552m,v.manifest_payload,name)['path'])
    except BoundaryContractError as e:fail.append(f'v552:{e}')
    try:
        s3=_manifest_scope_hint(v552jm,source=i.source,wave=i.canonical_wave,country_code=i.country_code);v=verify_v552j_producer_manifest(v552jm,run_id=run,source=i.source,wave=i.canonical_wave,country_code=i.country_code,shard_id=s3['shard_id'],v551j_manifest_path=v551jm,v552_manifest_path=v552m);contracts['v552j']=state_token(v);present.append('v552j:manifest.json')
    except BoundaryContractError as e:fail.append(f'v552j:{e}')
    for rel in ('manifest/v553_temporal_readiness_report.json','manifest/v553_wave_harmonization_report.json'):
        token='v553:'+rel
        if roots.get('v553') and (roots['v553']/rel).exists():present.append(token)
        else:missing.append(token)
    ready=not fail and not missing;return {'source':i.source,'country_code':i.country_code,'wave':i.canonical_wave,'run_id':run,'status':'ready' if ready else 'blocked','latest_roots':{k:str(v) if v else '' for k,v in roots.items()},'producer_contracts':contracts,'present_artifacts':present,'missing_artifacts':missing,'contract_failures':fail,'comparison_ready':ready}
def build_paired_wave_preflight(repo_root:str|Path,source:str,country_code:str,wave_a:str,wave_b:str)->dict[str,Any]:
    repo=Path(repo_root);a=_wave_report(repo,source,wave_a,country_code);b=_wave_report(repo,source,wave_b,country_code);missing=sorted(set(a['missing_artifacts'])|set(b['missing_artifacts']));fail=sorted(set(a['contract_failures'])|set(b['contract_failures']));ready=not missing and not fail;return {'repo_root':str(repo),'created_at':utc_now(),'source':a['source'],'country_code':a['country_code'],'wave_a':wave_a,'wave_b':wave_b,'status':'PAIRED_WAVE_READY' if ready else 'PAIRED_WAVE_BLOCKED','comparison_ready':ready,'missing_artifacts':missing,'contract_failures':fail,'legacy_v552_provenance_sidecar_required':False,'wave_reports':[a,b]}
def _write_json(path:Path,payload:dict[str,Any])->None:path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(payload,indent=2,sort_keys=True,ensure_ascii=False)+'\n',encoding='utf-8')
def _write_markdown(path:Path,r:dict[str,Any])->None:
    lines=['# Paired Wave Preflight Report','',f"- Repo root: `{r['repo_root']}`",f"- Created at: `{r['created_at']}`",f"- Wave A: `{r['wave_a']}`",f"- Wave B: `{r['wave_b']}`",f"- Status: `{r['status']}`",f"- Comparison ready: `{r['comparison_ready']}`",'- V552 contract source: root `manifest.json` + producer-declared canonical artifact hashes','- Legacy V552 provenance sidecar: **not required**','','## Wave Summary','','| Wave | Run ID | Status | Producer contracts | Missing | Contract failures |','| --- | --- | --- | --- | --- | --- |']
    for x in r['wave_reports']:lines.append('| {wave} | {run} | {status} | {contracts} | {missing} | {fail} |'.format(wave=x['wave'],run=x['run_id'],status=x['status'],contracts=', '.join(f'{k}={v}' for k,v in sorted(x['producer_contracts'].items())) or 'none',missing=', '.join(x['missing_artifacts']) or 'none',fail=', '.join(x['contract_failures']) or 'none'))
    lines+=['','## Missing Artifacts','',*([f'- {x}' for x in r['missing_artifacts']] or ['- none']),'','## Contract Failures','',*([f'- {x}' for x in r['contract_failures']] or ['- none'])];path.write_text('\n'.join(lines)+'\n',encoding='utf-8')
def main()->int:
    p=argparse.ArgumentParser();p.add_argument('--repo-root',default=str(ROOT));p.add_argument('--source',required=True);p.add_argument('--country-code',required=True);p.add_argument('--wave-a',required=True);p.add_argument('--wave-b',required=True);p.add_argument('--output-dir',default=str(ROOT/'docs/architecture_control/reports'));a=p.parse_args();r=build_paired_wave_preflight(a.repo_root,a.source,a.country_code,a.wave_a,a.wave_b);o=Path(a.output_dir);_write_json(o/'V552_THROUGH_V557_PAIRED_WAVE_PREFLIGHT_REPORT.json',r);_write_markdown(o/'V552_THROUGH_V557_PAIRED_WAVE_PREFLIGHT_REPORT.md',r);print(o/'V552_THROUGH_V557_PAIRED_WAVE_PREFLIGHT_REPORT.md');return 0
if __name__=='__main__':raise SystemExit(main())
