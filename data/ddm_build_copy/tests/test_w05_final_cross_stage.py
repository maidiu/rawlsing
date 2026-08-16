from __future__ import annotations
import argparse,hashlib,json,os,sys
from pathlib import Path
from types import SimpleNamespace
import pandas as pd,pytest
from data.ddm_build_copy.ddm_pipeline_boundary_consumer import ProducerBoundaryVerification
from data.ddm_build_copy.ddm_pipeline_boundary_contract import BoundaryContractError,BoundaryState,PIPELINE_BOUNDARY_CONTRACT_VERSION
import data.ddm_build_copy.ddm_pipeline_boundary_contract as bc
from data.ddm_build_copy.ddm_pipeline_final_contracts import V551J_COMPILER_VERSION,V551J_SCHEMA_VERSION,V552_COMPILER_VERSION,V552_SCHEMA_VERSION,V552J_COMPILER_VERSION,V552J_SCHEMA_VERSION,verify_v551j_producer_manifest,verify_v552_producer_manifest,verify_v552j_producer_manifest
import data.ddm_build_copy.resolve_pipeline_lineage as resolver
import data.ddm_build_copy.run_20var_allwaves_v550_552j_smoke as smoke

@pytest.fixture(autouse=True)
def _portable_parquet(monkeypatch):
    monkeypatch.setattr(pd.DataFrame,'to_parquet',lambda self,path,index=False:self.to_pickle(path));monkeypatch.setattr(pd,'read_parquet',lambda path:pd.read_pickle(path));monkeypatch.setattr(bc,'_parquet_row_count',lambda path:int(len(pd.read_pickle(path))))
def _pq(path:Path,rows:list[dict]):path.parent.mkdir(parents=True,exist_ok=True);df=pd.DataFrame(rows) if rows else pd.DataFrame(columns=['run_id']);df.to_parquet(path,index=False);return df
def _sha(path:Path)->str:return hashlib.sha256(path.read_bytes()).hexdigest()
def _art(base:Path,path:Path,name:str,schema:str)->dict:return {'artifact':name,'path':os.path.relpath(path,base),'artifact_kind':'canonical','row_count':len(pd.read_parquet(path)),'artifact_file_sha256':_sha(path),'schema_version':schema}
def _base(run='r',country='US',shard='GSS__2010')->dict:return {'contract_version':PIPELINE_BOUNDARY_CONTRACT_VERSION,'boundary_contract_version':PIPELINE_BOUNDARY_CONTRACT_VERSION,'producer_run_id':run,'run_id':run,'source':'GSS','wave':'2010','canonical_wave':'2010','country_code':country,'shard_id':shard}

def test_v551j_review_only_zero_certified_is_integrity_valid(tmp_path):
    root=tmp_path/'r';m=root/'manifest';p=root/'packets';m.mkdir(parents=True);_pq(p/'v551j_joint_packet_candidate_index.parquet',[{'run_id':'r','source':'GSS','canonical_wave':'2010','country_code':'US','shard_id':'GSS__2010','packet_id':'p1'}]);_pq(p/'v551j_certified_joint_packet_index.parquet',[]);_pq(p/'v551j_review_surface.parquet',[{'run_id':'r','packet_id':'p1'}]);v551=tmp_path/'v551.json';v550j=tmp_path/'v550j.json';v551.write_text('{}');v550j.write_text('{}');payload={**_base(),'schema_version':V551J_SCHEMA_VERSION,'compiler_version':V551J_COMPILER_VERSION,'run_integrity_status':'PASS','evidence_status':'PRESENT','downstream_permission_status':'DENY','v551_upstream_manifest_sha256':_sha(v551),'v550j_upstream_manifest_sha256':_sha(v550j),'artifacts':[_art(m,p/'v551j_joint_packet_candidate_index.parquet','candidate',V551J_SCHEMA_VERSION),_art(m,p/'v551j_certified_joint_packet_index.parquet','certified',V551J_SCHEMA_VERSION),_art(m,p/'v551j_review_surface.parquet','review_surface',V551J_SCHEMA_VERSION)]};mf=m/'manifest.json';mf.write_text(json.dumps(payload));v=verify_v551j_producer_manifest(mf,run_id='r',source='GSS',wave='2010',country_code='US',shard_id='GSS__2010',v551_manifest_path=v551,v550j_manifest_path=v550j);rows={Path(a.path).name:a.row_count for a in v.verified_artifacts};assert v.state.run_integrity_status=='PASS' and v.state.downstream_permission_status=='DENY';assert rows['v551j_certified_joint_packet_index.parquet']==0 and rows['v551j_review_surface.parquet']==1

def test_v551j_shard_grain_valid_empty(tmp_path):
    m=tmp_path/'r/manifest';m.mkdir(parents=True);v550j=tmp_path/'v550j.json';v550j.write_text('{}');payload={**_base(country=''),'schema_version':V551J_SCHEMA_VERSION,'compiler_version':V551J_COMPILER_VERSION,'run_integrity_status':'PASS','evidence_status':'VALID_EMPTY','downstream_permission_status':'NOT_APPLICABLE','v550j_upstream_manifest_sha256':_sha(v550j),'artifacts':[]};mf=m/'manifest.json';mf.write_text(json.dumps(payload));v=verify_v551j_producer_manifest(mf,run_id='r',source='GSS',wave='2010',country_code='US',shard_id='GSS__2010',v550j_manifest_path=v550j);assert v.state.evidence_status=='VALID_EMPTY';assert v.identity['shard_id']=='GSS__2010';
    

def test_v552_unresolved_zero_rows_current_manifest(tmp_path):
    root=tmp_path/'r';s=root/'structural';root.mkdir(parents=True);_pq(s/'v552_structural_fact_index.parquet',[]);_pq(s/'v552_temporal_key_source_index.parquet',[]);up=tmp_path/'v551.json';up.write_text('up');payload={**_base(),'schema_version':V552_SCHEMA_VERSION,'compiler_version':V552_COMPILER_VERSION,'run_integrity_status':'PASS','evidence_status':'APPLICABLE_UNRESOLVED','downstream_permission_status':'DENY','upstream_v551':{'manifest_file_sha256':_sha(up),'schema_version':'v3.0','compiler_version':'v3.0'},'artifacts':[_art(root,s/'v552_structural_fact_index.parquet','v552_structural_fact_index',V552_SCHEMA_VERSION),_art(root,s/'v552_temporal_key_source_index.parquet','v552_temporal_key_source_index',V552_SCHEMA_VERSION)]};mf=root/'manifest.json';mf.write_text(json.dumps(payload));v=verify_v552_producer_manifest(mf,run_id='r',source='GSS',wave='2010',country_code='US',shard_id='GSS__2010',v551_manifest_path=up);assert v.state.evidence_status=='APPLICABLE_UNRESOLVED';assert all(a.valid_empty for a in v.verified_artifacts)

def test_v552j_typed_absence_hash_bound(tmp_path):
    root=tmp_path/'r';p=root/'packets';a=root/'audits';root.mkdir(parents=True);_pq(p/'v552j_structural_join_index.parquet',[]);_pq(a/'v552j_join_audit.parquet',[]);u1=tmp_path/'u1';u2=tmp_path/'u2';u1.write_text('a');u2.write_text('b');payload={**_base(),'schema_version':V552J_SCHEMA_VERSION,'compiler_version':V552J_COMPILER_VERSION,'run_integrity_status':'PASS','evidence_status':'NOT_APPLICABLE','downstream_permission_status':'NOT_APPLICABLE','canonical_artifact_names':['v552j_structural_join_index','v552j_join_audit'],'upstream_v551j':{'manifest_file_sha256':_sha(u1),'schema_version':V551J_SCHEMA_VERSION,'compiler_version':V551J_COMPILER_VERSION},'upstream_v552':{'manifest_file_sha256':_sha(u2),'schema_version':V552_SCHEMA_VERSION,'compiler_version':V552_COMPILER_VERSION},'artifacts':[_art(root,p/'v552j_structural_join_index.parquet','v552j_structural_join_index',V552J_SCHEMA_VERSION),_art(root,a/'v552j_join_audit.parquet','v552j_join_audit',V552J_SCHEMA_VERSION)]};mf=root/'manifest.json';mf.write_text(json.dumps(payload));v=verify_v552j_producer_manifest(mf,run_id='r',source='GSS',wave='2010',country_code='US',shard_id='GSS__2010',v551j_manifest_path=u1,v552_manifest_path=u2);assert v.state.evidence_status=='NOT_APPLICABLE';assert all(x.row_count==0 for x in v.verified_artifacts)

def test_lineage_integrity_not_permission():
    v=ProducerBoundaryVerification('m',BoundaryState(PIPELINE_BOUNDARY_CONTRACT_VERSION,'PASS','PRESENT','DENY'),(),{'run_id':'r'},{'schema_version':'x','compiler_version':'y'});x=resolver._verified_resolution('v551j',Path('/tmp/r'),v);assert x.usable and x.status=='PASS/PRESENT/DENY' and x.metrics['downstream_permission_status']=='DENY'
def test_joint_mode_equals_not_overwritten(monkeypatch):
    monkeypatch.setattr(smoke,'_ORIGINAL_PARSE_ARGS',lambda:argparse.Namespace(joint_mode='required'));monkeypatch.setattr(sys,'argv',['prog','--joint-mode=required']);assert smoke.parse_args().joint_mode=='required'
def test_no_active_w05_ghost_or_partial_tokens():
    root=Path(__file__).resolve().parents[1]
    for f in ('resolve_pipeline_lineage.py','compile_v5_paired_wave_preflight.py','run_20var_allwaves_v550_552j_smoke.py'):
        t=(root/f).read_text();assert 'v552_input_provenance_manifest.json' not in t;assert 'PARTIAL_AWAITING_CROSS_HOOK' not in t
def test_merged_stage_hooks_reject_no_parquet(monkeypatch):
    import data.ddm_build_copy.compile_v550j_joint_response_patterns as a
    import data.ddm_build_copy.compile_v551j_joint_evidence_packets as b
    import data.ddm_build_copy.compile_v552_structural_ddm as c
    import data.ddm_build_copy.compile_v552j_structural_handoff as d
    monkeypatch.setattr(a,'parse_args',lambda:SimpleNamespace(write_parquet=False));
    with pytest.raises(RuntimeError,match='CANONICAL_PARQUET_REQUIRED'):a.main()
    monkeypatch.setattr(b,'parse_args',lambda:SimpleNamespace(write_parquet=False));
    with pytest.raises(BoundaryContractError,match='PARQUET_CANONICAL_OUTPUT_REQUIRED'):b.main()
    monkeypatch.setattr(c,'parse_args',lambda:SimpleNamespace(run_id='r',v551_manifest_path='x',atoms_path=None,coverage_path=None,adjudication_path=None,conditional_determinicity_path=None,output_root='o',strict_handoff=True,diagnostic_only=False,write_parquet=False,write_csv=True));
    with pytest.raises(BoundaryContractError,match='PARQUET_CANONICAL_OUTPUT_REQUIRED'):c.main()
    monkeypatch.setattr(d,'parse_args',lambda:SimpleNamespace(run_id='r',v551j_manifest_path='x',v552_manifest_path='y',output_root='o',write_parquet=False,write_csv=True));
    with pytest.raises(BoundaryContractError,match='PARQUET_CANONICAL_OUTPUT_REQUIRED'):d.main()
def test_v552j_rejects_country_shard_coercion():
    import data.ddm_build_copy.compile_v552j_structural_handoff as v
    shard={'run_id':'r','source':'GSS','wave':'2010','country_code':'','shard_id':'GSS__2010'};country={'run_id':'r','source':'GSS','wave':'2010','country_code':'US','shard_id':'GSS__2010'}
    with pytest.raises(BoundaryContractError,match='CROSS_SCOPE_MISMATCH:country'):v._coherent_scope('r',shard,country)
