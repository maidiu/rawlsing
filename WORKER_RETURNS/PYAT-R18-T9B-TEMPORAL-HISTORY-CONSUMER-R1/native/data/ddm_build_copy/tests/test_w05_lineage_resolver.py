from __future__ import annotations
import hashlib,json
from pathlib import Path
import pandas as pd,pytest
import data.ddm_build_copy.resolve_pipeline_lineage as r
from data.ddm_build_copy.ddm_pipeline_boundary_contract import BoundaryContractError,DependencyLedgerError

def _ready(path:Path,status:str='READY_V550')->None:path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps({'status':status}),encoding='utf-8')
def test_missing_default_dependency_ledger_is_not_opened(tmp_path:Path)->None:assert r._load_dependency_ledger(None) is None
def test_external_ledger_requires_verified_hash(tmp_path:Path)->None:
    p=tmp_path/'ledger.json';p.write_text(json.dumps({'stages':{}}),encoding='utf-8')
    with pytest.raises(DependencyLedgerError):r._load_dependency_ledger(p,'0'*64)
    assert r._load_dependency_ledger(p,hashlib.sha256(p.read_bytes()).hexdigest())=={'stages':{}}
def test_malformed_required_readiness_fails_closed(tmp_path:Path)->None:
    root=tmp_path/'run';root.mkdir();(root/'manifest.json').write_text('{bad',encoding='utf-8');x=r._validate_root(root,stage='x',required_files=('manifest.json',),status_paths=('manifest.json',),ready_key_names=('status',));assert not x.usable;assert 'unreadable required file' in x.reason or 'unverifiable' in x.reason
def test_unknown_status_fails_closed(tmp_path:Path)->None:
    root=tmp_path/'run';root.mkdir();_ready(root/'manifest.json','MAYBE_READY_LATER');x=r._validate_root(root,stage='x',required_files=('manifest.json',),status_paths=('manifest.json',),ready_key_names=('status',));assert not x.usable;assert 'unverifiable' in x.reason
def test_corrupt_parquet_is_not_valid_empty(monkeypatch:pytest.MonkeyPatch,tmp_path:Path)->None:
    root=tmp_path/'run';root.mkdir();p=root/'a.parquet';p.write_bytes(b'bad');_ready(root/'manifest.json');monkeypatch.setattr(pd,'read_parquet',lambda _p:(_ for _ in ()).throw(ValueError('corrupt')));x=r._validate_root(root,stage='x',required_files=('a.parquet','manifest.json'),status_paths=('manifest.json',),ready_key_names=('status',));assert not x.usable;assert 'unreadable required file' in x.reason
def test_v550j_resolution_is_exactly_bound_to_selected_v550_run(monkeypatch:pytest.MonkeyPatch,tmp_path:Path)->None:
    repo=tmp_path;v550=repo/'data/ddm_repository_copy/v550/shard_runs/run_old/GSS__2010';v550.mkdir(parents=True);(repo/'data/ddm_repository_copy/v550j/runs/run_new/GSS__2010/joint_patterns').mkdir(parents=True)
    monkeypatch.setattr(r,'_resolve_v550',lambda *_a,**_k:r.StageResolution('v550',str(v550),True,'READY_V550'));monkeypatch.setattr(r,'_v551_expected_identity',lambda _root:{'run_id':'run_old','source':'GSS','wave':'2010','country_code':'US','shard_id':'GSS__2010','v550_shard_id':'GSS__2010','bridge_path':str(v550/'bridge/v551_bridge_index.parquet')});observed={}
    def fake_v550j(manifest_path,readiness_path,**_kwargs):observed['manifest']=Path(manifest_path);observed['readiness']=Path(readiness_path);raise BoundaryContractError('fixture')
    monkeypatch.setattr(r,'verify_v550j_producer_manifest',fake_v550j)
    for name in ('verify_v551_producer_manifest','verify_v551j_producer_manifest','verify_v552_producer_manifest','verify_v552j_producer_manifest'):monkeypatch.setattr(r,name,lambda *_a,**_k:(_ for _ in ()).throw(BoundaryContractError('fixture')))
    r.resolve_stage_roots(repo,'GSS','2010');assert observed['manifest']==repo/'data/ddm_repository_copy/v550j/runs/run_old/GSS__2010/joint_patterns/v550j_manifest.json';assert 'run_new' not in str(observed['manifest'])
