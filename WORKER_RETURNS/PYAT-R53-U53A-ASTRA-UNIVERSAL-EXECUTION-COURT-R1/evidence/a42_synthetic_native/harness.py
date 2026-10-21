"""Six direct native A42 characterization cases; synthetic Git artifact only."""
from pathlib import Path
import sys,os,subprocess,json,copy,hashlib
T=Path(__file__).resolve().parent
sys.path.insert(0,str(T))
os.environ['GIT_CONFIG_NOSYSTEM']='1';os.environ['GIT_CONFIG_GLOBAL']=os.devnull
for key in ['GIT_DIR','GIT_WORK_TREE','GIT_INDEX_FILE','GIT_OBJECT_DIRECTORY','GIT_ALTERNATE_OBJECT_DIRECTORIES']:
 os.environ.pop(key,None)
from a42 import core
from frozen_a41.a41.gitpreimage import GitPreimage,PreimageError
assert Path(core.__file__).resolve()==T/'a42/core.py'
assert 'site-packages' not in '\n'.join(sys.path)
repo=T/'synthetic_repo';repo.mkdir()
def git(*a):return subprocess.check_output(['git','-c','core.hooksPath='+os.devnull,*a],cwd=repo,stderr=subprocess.PIPE).decode().strip()
git('init','-q');(repo/'fixture.json').write_text('{"synthetic":true,"real_authority":false}\n');git('add','fixture.json');git('-c','user.name=Synthetic Fixture','-c','user.email=synthetic@example.invalid','commit','-qm','synthetic A42 fixture')
commit=git('rev-parse','HEAD');gp=GitPreimage(repo);art=gp.verify(commit,'fixture.json')
globals={k:{'grain':'GLOBAL','expected_status':'OPEN','obligation':'SYNTHETIC_ONLY'} for k in ['cross_family_F6','temporal_F7','possibility_F8']}
scope={'wave_expected_u_e_pre':{'SYN01':'UNISSUED'},'declared_consumers':['synthetic.consumer'],'declared_clock':'2026-01-01','cells':[{'cell_id':'SYN01.S01','source_id':'SYN01','axis_id':'S01','axis_family':'SOURCE','identity':'SYNTHETIC','expected_u_e_pre':'UNISSUED','required_proof':'SYNTHETIC_ONLY'}],'waves':[{'source_id':'SYN01','source_name':'Synthetic only','identity':'SYNTHETIC','expected_u_e_pre':'UNISSUED'}],'f1_f8_gate_grain':{},'global_relations':globals,'crosswalk_151_101':{'unmatched_register_rows':[]},'register_151_rows':[],'ledger_101_rows':[]}
receipt={'receipt_id':'SYNTHETIC_RECEIPT','origin_commit':commit,'claim_id':'SYNTHETIC_ONLY','grade':'SOURCEFREE_INTEGRATED_POSITIVE','coverage':{'wave_ids':[],'axis_ids':[],'f_gate_ids':[],'functional_gates':['F6'],'register_151_ids':[],'ledger_101_ids':[],'global_relations':[],'global_contributions':['cross_family_F6'],'occupancy_grain_note':'SYNTHETIC_ONLY'},'currentness':{'archive_or_current':'CURRENT','as_of':'2025-01-01'},'artifacts':[art],'unknown_bounds':{'real_authority':False},'downstream_consumer_read_refs':['synthetic.consumer']}
old={'verdict':{'original_measured_occupied_cells':0,'missing_expected_cells':1,'sourcefree_covered_cells':0}}
def assess(r):return core.assess_v2(scope,core.ingest_r41_bank({'receipts':[r]},gp,scope),{},old)
def globalrow(a):return next(r for r in a['f1_f8_rows'] if r.get('global_relation_name')=='cross_family_F6')
results=[]
a=assess(receipt);assert globalrow(a)['cell_status']=='OPEN_GLOBAL_OBLIGATION__SOURCEFREE_CONTRIBUTION_ONLY';assert a['verdict']['n11_state']=='N11_NOT_READY';results.append({'case':'baseline_sourcefree_contribution','pass':True,'row':globalrow(a)['cell_status']})
r=copy.deepcopy(receipt);r['coverage']['global_relations']=['cross_family_F6'];a=assess(r);assert globalrow(a)['cell_status']=='ACCEPTED';assert a['verdict']['n11_state']=='N11_NOT_READY' and a['verdict']['global_relations_closed']==0 and a['verdict']['global_relations_open']==3
results.append({'case':'global_label_mutation','pass':True,'engineering_result':'ROW_ACCEPTANCE_LABEL_INCONSISTENT_WITH_TERMINAL_HOLD','row':globalrow(a),'n11_state':a['verdict']['n11_state'],'global_closed':a['verdict']['global_relations_closed'],'global_open':a['verdict']['global_relations_open'],'artifact_preimage_unchanged':r['artifacts']==receipt['artifacts']})
def refuse(name,mutate,expected):
 r=copy.deepcopy(receipt);mutate(r)
 try:assess(r)
 except PreimageError as e:
  assert expected in str(e);results.append({'case':name,'pass':True,'refusal':str(e)})
 else:raise AssertionError(name+' unexpectedly accepted')
def original(r):r['grade']='ORIGINAL_MEASURED_OCCUPANCY';r['coverage']['wave_ids']=['SYN01']
refuse('unissued_original_grade',original,'FALSE_PROMOTION')
refuse('bad_artifact_hash',lambda r:r['artifacts'][0].update(blob_sha1='0'*40),'BLOB_PREIMAGE_MISMATCH')
refuse('unknown_consumer',lambda r:r.update(downstream_consumer_read_refs=['forged.consumer']),'CONSUMER_REF')
refuse('future_clock',lambda r:r['currentness'].update(as_of='2099-01-01'),'CLOCK_VIOLATION')
assert len(results)==6
out={'schema':'U53A_A42_SYNTHETIC_NATIVE_RECEIPT@1','cases':results,'passed':6,'failed':0,'native_scope':'Exact A42 core+GitPreimage; real synthetic Git artifact; no mocks; one synthetic cell, not original35 or full frozen bank','authority_issued':False,'original_data_read':False,'synthetic_commit':commit,'module_sha256':{rel:hashlib.sha256((T/rel).read_bytes()).hexdigest() for rel in ['a42/core.py','frozen_a41/a41/gitpreimage.py']}}
(T/'receipt.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'passed':6,'failed':0,'global_label':globalrow(a)['cell_status'],'n11':a['verdict']['n11_state'],'receipt':str(T/'receipt.json')}))
