"""Independent same-lineage review of PDEV01 N10W subject 883da8fff2."""
from __future__ import annotations
import copy, json, sys, hashlib, subprocess, platform
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
CANDIDATE = Path('/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-pdev01-n10w-join')
REPAIR = CANDIDATE / 'WORKER_RETURNS/PDEV01-N10W-JOIN/repair'
OLD = HERE.parents[0] / 'PDEV01-N10W-INDEPENDENT-REVIEW/evidence'
KEY = 'base/TEST_CURRENT/budget5'
J42_ROWS = '4320b3a505478c274fc756ce0e025e36685e0742e940072aae80ce11286e4c02'
D2P3 = 'cfe7dc6111afcb8eda26eb9a54f6cad43b6d1584'
D2P3_TRACE = ('WORKER_RETURNS/PYAT-USERDIRECT-20261014-R6-D2P3-PRODUCER-READER-'
              'LINEAGE-R1/new/producer_reader_trace.json')
sys.dont_write_bytecode = True
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPAIR))
from rawlsing_next.pre553_empirical_objects import semantic_hash
from rawlsing_next.pre553_universal_world_binding import JoinedWorldField, select_joined_world_view
from rawlsing_next.tests.test_universal_world_binding import _joined_request
from guarded_receiver import guarded_select_joined_world_view, W41_ARTIFACT_SHA256


def sha(b): return hashlib.sha256(b).hexdigest()
def load(p): return json.loads(Path(p).read_text())
def fields(rec,key):
    r=rec['p41_joined_receipts'][key]['n9_world']['rules']
    return (JoinedWorldField('training_access',r['training_access']['value']),
            JoinedWorldField('civil_sanction',r['civil_sanction']['value']))
def run(rec,key=KEY,fields_=None,**chg):
    v=guarded_select_joined_world_view(_joined_request(rec,key,fields=fields(rec,key) if fields_ is None else fields_,**chg))
    return {'state':v.state,'reason_code':v.reason_code,'view_key':v.view_key,'view_hash':v.view_hash,
            'families':None if v.consumer_values_read is None else v.consumer_values_read.get('families'),
            'n9_clock':None if v.consumer_values_read is None else v.consumer_values_read.get('n9_clock'),
            'n9_currentness':None if v.consumer_values_read is None else v.consumer_values_read.get('n9_currentness')}
def p41(rec): return rec['p41_joined_receipts'][KEY]
def rehash(p): p.pop('content_hash',None); p['content_hash']=semantic_hash(p)

def main():
    a=load(OLD/'J42_RECEIPTS_actual_1.json'); b=load(OLD/'J42_RECEIPTS_actual_2.json')
    assert a==b
    assert sha((OLD/'J42_RECEIPTS_actual_1.json').read_bytes()) == 'c54b215bb03bba391571b4c51357831b14f256b7c4c6eec98d85dd9bda30eebf'
    all84={k:run(a,k) for k in sorted(a['p41_joined_receipts'])}
    cold={k:run(b,k) for k in sorted(b['p41_joined_receipts'])}
    positive=sum(v['state']=='SELECTED_VIEW_FROM_ACTUAL_JOINED_CONSUMER' for v in all84.values())
    # R05 mismatch and provider substitution, then restore.
    r05=load(CANDIDATE/'WORKER_RETURNS/PDEV01-N10W-JOIN/R05_P41_TRACE.json')
    r05_rows=r05['r05_source']['source_rows_hash']
    r05_rows_result=run(a,source_rows_hash=r05_rows)
    r05_provider=copy.deepcopy(a); r05_provider['p41_joined_receipts'][KEY]['providers']=dict(r05['p41_providers']); rehash(p41(r05_provider))
    r05_provider_result=run(r05_provider)
    restored=run(a)
    # D2P3 exact trace and mismatch to J42 lineage.
    d2p3=json.loads(subprocess.check_output(['git','-C',str(CANDIDATE),'show',f'{D2P3}:{D2P3_TRACE}'],timeout=180))
    d2p3_text=json.dumps(d2p3,sort_keys=True)
    d2p3_refs=d2p3.get('producer_refs') or {}
    d2p3_families=d2p3.get('reader_source_family') or []
    d2p3_is_n9='W41_READONLY_SOURCE_QUALIFIED_WORLD@1' in d2p3_text
    d2p3_has_rows=J42_ROWS in d2p3_text
    d2p3_has_e41='E41_N10E' in d2p3_text or 'E41_' in d2p3_text
    refs_in_j42=any(ref in json.dumps(a) for ref in d2p3_refs.values())
    # The smallest existing lawful construction path: exact existing W41/E41 binding must already exist.
    existing_path=bool(d2p3_is_n9 and d2p3_has_rows and d2p3_has_e41)
    # Host/runtime/import marker; sanitized.
    passport={'schema':'PDEV01_N10W_SAME_LINEAGE_ENV_PASSPORT@1.0.0','host_marker':'darwin-x86_64-local-s2','hostname_redacted':True,'platform':platform.platform(),'machine':platform.machine(),'python':sys.version.split()[0],'executable':sys.executable,'cwd_scope':'review worktree outside author worktree','candidate':'883da8fff2bb10fe2181d0c0a7ddc84d34bb5a8c','review_base':'02b98ec3dd88e5e742ce459e54d233f547768145','model':'opencode-go/deepseek-v4.1-flash','variant':'max','quota':'UNKNOWN','test_only':True,'source_reads':False,'browser':'NOT_USED_LOCAL_RUNTIME','imports':{'guarded_receiver_sha256':sha((REPAIR/'guarded_receiver.py').read_bytes()),'rawlsing_world_binding_sha256':sha((REPO/'rawlsing_next/pre553_universal_world_binding.py').read_bytes())}}
    doc={
      'schema':'PDEV01_N10W_SAME_LINEAGE_INDEPENDENT_REVIEW@1.0.0',
      'subject':'883da8fff2bb10fe2181d0c0a7ddc84d34bb5a8c',
      'review_base':'02b98ec3dd88e5e742ce459e54d233f547768145',
      'reused_e79':'e79be4a3d8cd2cbe57c4a25361acc5e4dd9a8e1c',
      'actual_j42':{'receipt_sha256':sha((OLD/'J42_RECEIPTS_actual_1.json').read_bytes()),'receipt_2_sha256':sha((OLD/'J42_RECEIPTS_actual_2.json').read_bytes()),'cold_byte_equal':a==b,'views':len(all84),'positive':positive,'first_refusals':{k:v for k,v in all84.items() if v['state']!='SELECTED_VIEW_FROM_ACTUAL_JOINED_CONSUMER'},'cold_all_view_hashes_equal':all84==cold,'base':all84[KEY]},
      'j42_lineage':{'n9':p41(a)['providers']['n9_world'],'n10e':p41(a)['providers']['n10e_empirical'],'n10w':p41(a)['providers']['n10w_progressive'],'source_rows':J42_ROWS,'clock':p41(a)['j42_bindings']['w41_clock'],'currentness':p41(a)['n9_world']['currentness']},
      'mismatch_restore':{'r05_source_rows':r05_rows,'r05_rows_vs_j42':r05_rows==J42_ROWS,'r05_rows_result':r05_rows_result,'r05_provider_result':r05_provider_result,'restored':restored,'restore_matches_positive':restored['view_hash']==all84[KEY]['view_hash']},
      'd2p3_boundary':{'candidate':D2P3,'trace_path':D2P3_TRACE,'trace_sha256':sha(subprocess.check_output(['git','-C',str(CANDIDATE),'show',f'{D2P3}:{D2P3_TRACE}'],timeout=180)),'reader_state':d2p3.get('reader_state'),'producer_refs':d2p3_refs,'source_families':d2p3_families,'is_n9':d2p3_is_n9,'has_j42_rows':d2p3_has_rows,'has_e41':d2p3_has_e41,'refs_in_j42_receipt':refs_in_j42,'existing_lawful_construction_path':existing_path,'first_missing_binding':'W41 version-selected N9 world + E41 N10E receipt + exact J42 source-row/currentness binding for D2P3 GSS/NCA field refs','smallest_path':'NONE_EXISTING; a new W41-style N9 artifact binding would be required and is outside this authority'},
      'environment_passport':passport,
      'limits':['TEST_ONLY sourcefree W41/E41/P41 and synthetic E04 only.','D2P3 is a field reader, not N9; not fed to N10W.','No original data/source read, production edit, merge/CI, adoption or new trust authority.'],
    }
    (HERE/'evidence'/'same_lineage_review.json').write_text(json.dumps(doc,indent=2,sort_keys=True)+'\n')
    (HERE/'evidence'/'ENVIRONMENT_PASSPORT.json').write_text(json.dumps(passport,indent=2,sort_keys=True)+'\n')
    print(json.dumps({k:doc[k] for k in ['actual_j42','mismatch_restore','d2p3_boundary']},indent=2))

if __name__=='__main__': main()
