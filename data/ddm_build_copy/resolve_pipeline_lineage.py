#!/usr/bin/env python3
"""W05 lineage-integrity shim over the preserved integration resolver."""
from __future__ import annotations
import sys
from pathlib import Path
from typing import Any, Iterable
from data.ddm_build_copy import resolve_pipeline_lineage_impl as _impl
from data.ddm_build_copy.ddm_pipeline_boundary_contract import (
    BoundaryContractError, boundary_state_from_payload, inspect_artifact,
    read_status_document, verify_external_dependency_ledger,
)
for _n in dir(_impl):
    if not _n.startswith('__'): globals()[_n]=getattr(_impl,_n)
_ORIG_RESOLVE=_impl.resolve_stage_roots
StageResolution=_impl.StageResolution
_NO_LEDGER=Path('__RAWLSING_NO_EXTERNAL_DEPENDENCY_LEDGER__')
_LEDGER_SHA=''
DEFAULT_DEPENDENCY_LEDGER=None

def _load_dependency_ledger(path: Path|None, expected_sha256: str=''):
    if path is None or Path(path)==_NO_LEDGER: return None
    return verify_external_dependency_ledger(path, expected_sha256 or _LEDGER_SHA)

def _validate_root(root: Path, *, stage: str, required_files: tuple[str,...], required_nonempty_files: tuple[str,...]=(), status_paths: tuple[str,...]=(), ready_key_names: tuple[str,...]=(), **_kw):
    if not root.is_dir(): return StageResolution(stage,'',False,'BLOCKED_OR_MISSING',f'missing exact run root: {root}')
    metrics={}
    for rel in required_files:
        a=inspect_artifact(root/rel)
        if not a.exists: return StageResolution(stage,'',False,'BLOCKED_OR_MISSING',f'missing required file: {rel}')
        if not a.readable: return StageResolution(stage,'',False,'BLOCKED_OR_MISSING',f'unreadable required file: {rel}: {a.error}')
        metrics[rel]={'row_count':a.row_count,'artifact_file_sha256':a.artifact_file_sha256,'valid_empty':a.valid_empty}
    for rel in required_nonempty_files:
        a=inspect_artifact(root/rel)
        if not a.exists or not a.readable: return StageResolution(stage,'',False,'BLOCKED_OR_MISSING',f'unreadable required evidence: {rel}: {a.error}')
        if a.row_count is not None and a.row_count<=0: return StageResolution(stage,'',False,'BLOCKED_OR_MISSING',f'empty required evidence: {rel}')
    failures=[]
    for rel in status_paths:
        d=read_status_document(root/rel)
        if not d.exists: failures.append(f'missing:{rel}'); continue
        if not d.readable: failures.append(f'unreadable:{rel}:{d.error}'); continue
        try: state=boundary_state_from_payload(d.payload, ready_key_names)
        except BoundaryContractError as e: failures.append(f'invalid:{rel}:{e}'); continue
        status=state.source or '/'.join((state.run_integrity_status,state.evidence_status,state.downstream_permission_status))
        if not state.permits_downstream: return StageResolution(stage,'',False,status,f'producer boundary does not permit downstream: {rel}',metrics)
        return StageResolution(stage,str(root),True,status,metrics=metrics)
    return StageResolution(stage,'',False,'BLOCKED_OR_MISSING','required readiness/integrity unverifiable: '+';'.join(failures),metrics)

def _latest_usable_candidate(base: Path, pattern: str, *, stage: str, required_files: tuple[str,...], required_nonempty_files: tuple[str,...]=(), status_paths: tuple[str,...]=(), ready_key_names: tuple[str,...]=(), **kw):
    best=f'no candidate matched {pattern}'
    for _,_,root in _impl._rank_candidates(base,_impl._candidate_dirs(base,pattern)):
        r=_validate_root(root,stage=stage,required_files=required_files,required_nonempty_files=required_nonempty_files,status_paths=status_paths,ready_key_names=ready_key_names)
        if r.usable: return r
        best=r.reason
    return StageResolution(stage,'',False,'BLOCKED_OR_MISSING',best)

def _parquet_row_count(path: Path)->int:
    a=inspect_artifact(path)
    if not a.exists: return 0
    if not a.readable: raise BoundaryContractError(f'PARQUET_UNREADABLE:{path}:{a.error}')
    return int(a.row_count or 0)

def _stage_artifact_rows(path: Path)->int:
    a=inspect_artifact(path)
    if not a.exists: return 0
    if not a.readable: raise BoundaryContractError(f'ARTIFACT_UNREADABLE:{path}:{a.error}')
    return int(a.row_count if a.row_count is not None else 1)

def resolve_stage_roots(repo_root: str|Path, source: str, wave: str):
    _impl._latest_usable_candidate=globals()['_latest_usable_candidate']
    _impl._parquet_row_count=globals()['_parquet_row_count']
    _impl._stage_artifact_rows=globals()['_stage_artifact_rows']
    stages=_ORIG_RESOLVE(repo_root,source,wave)
    v550=stages['v550']
    if v550.usable:
        run_id=_impl._extract_run_id_from_v550_root(v550.root)
        shard=f'{source.upper()}__{wave}'
        exact=Path(repo_root)/'data/ddm_repository_copy/v550j/runs'/run_id
        stages['v550j']=globals()['_validate_root'](exact,stage='v550j',required_files=(f'{shard}/joint_patterns/joint_response_pattern_index.parquet',f'{shard}/joint_patterns/joint_pattern_meaning_summary.parquet',f'{shard}/joint_patterns/joint_pattern_association_index.parquet',f'{shard}/joint_patterns/joint_pattern_association_review_surface.parquet',f'{shard}/joint_patterns/v550j_summary.json',f'{shard}/joint_patterns/v550j_source_wave_readiness_report.json'),required_nonempty_files=(f'{shard}/joint_patterns/joint_response_pattern_index.parquet',f'{shard}/joint_patterns/joint_pattern_meaning_summary.parquet',f'{shard}/joint_patterns/joint_pattern_association_index.parquet'),status_paths=(f'{shard}/joint_patterns/v550j_source_wave_readiness_report.json',f'{shard}/joint_patterns/v550j_summary.json'),ready_key_names=('readiness_status','final_status','status'))
    return stages

def main(argv=None):
    global _LEDGER_SHA
    args=list(sys.argv[1:] if argv is None else argv)
    sha=''
    if '--dependency-ledger-sha256' in args:
        i=args.index('--dependency-ledger-sha256'); sha=args[i+1]; del args[i:i+2]
    has_ledger='--dependency-ledger' in args
    if has_ledger and not sha:
        print('{"error":"DEPENDENCY_LEDGER_SHA256_REQUIRED"}',file=sys.stderr); return 2
    if not has_ledger: args += ['--dependency-ledger',str(_NO_LEDGER)]
    _LEDGER_SHA=sha
    _impl._load_dependency_ledger=lambda p: ({'stages':{}} if Path(p)==_NO_LEDGER else verify_external_dependency_ledger(p,_LEDGER_SHA))
    _impl.resolve_stage_roots=resolve_stage_roots
    old=sys.argv; sys.argv=[old[0],*args]
    try: return _impl.main()
    finally: sys.argv=old

_impl._latest_usable_candidate=_latest_usable_candidate
_impl._parquet_row_count=_parquet_row_count
_impl._stage_artifact_rows=_stage_artifact_rows
_impl.resolve_stage_roots=resolve_stage_roots
globals().update(_load_dependency_ledger=_load_dependency_ledger,_validate_root=_validate_root,_latest_usable_candidate=_latest_usable_candidate,_parquet_row_count=_parquet_row_count,_stage_artifact_rows=_stage_artifact_rows,resolve_stage_roots=resolve_stage_roots)
if __name__=='__main__': raise SystemExit(main())
