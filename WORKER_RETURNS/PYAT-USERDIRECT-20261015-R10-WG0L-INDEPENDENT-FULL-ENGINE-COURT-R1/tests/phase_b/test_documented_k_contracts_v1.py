"""Reconstructed documented WG0K 15+4 contracts on FULL candidate imports.
Not the unavailable original extracted scripts; expectations come from the
published WG0K 02_ACTUAL_EXECUTION_AND_HOSTILES.json at c506293e.
"""
import copy,json,os,shutil,subprocess,sys,uuid
import pytest
from phase_b_support_v1 import *
from phase_b_adapter_v1 import Adapter
from precommitted_contract import assert_refusal,assert_cold

@pytest.fixture(scope='module')
def a():
 a=Adapter(O);a.out=R/'observations/phase_b/documented_k_v2';a.out.mkdir(exist_ok=True);return a

@pytest.mark.parametrize('case',['held_identity','reason','circular','store_alias','read_alias','snapshot_alias','same_key','restore_alias','rehashed_grant','rehashed_fact'])
def test_documented_ten_negative_method_contracts(a,case):
 mapped={'held_identity':('frontier','equal_count_HELD_identity_swap'),'reason':('frontier','equal_count_reason_forgery'),'circular':('frontier','circular_expected_list'),'store_alias':('custody','store_alias'),'read_alias':('custody','read_alias'),'snapshot_alias':('custody','snapshot_alias'),'same_key':('custody','same_key_collision'),'restore_alias':('custody','restore_alias'),'rehashed_grant':('authority','requester_forged_grant'),'rehashed_fact':('custody','rehashed_changed_fact')}
 if case in ('rehashed_grant','rehashed_fact'):
  p=plan();_,rs=w.run_plan(p,w.make_executor(p),max_units=1);d=json.loads(w.create_checkpoint(p,rs).to_json())
  if case=='rehashed_grant':d['grant_state']='REAL_SOURCE_SIGNED_PERMISSION'
  else:
   key=next(iter(d['fact_custody_snapshot']['facts']));d['fact_custody_snapshot']['facts'][key]['denominator']=999;d['fact_custody_snapshot']['hashes'][key]=w.digest(d['fact_custody_snapshot']['facts'][key])
  d['checkpoint_hash']=w.digest({k:v for k,v in d.items() if k not in ('signature','checkpoint_hash')})
  with pytest.raises(w.ColdRestartError):w.ColdCheckpoint.from_json(json.dumps(d),fixture_owner=p.fixture_owner)
  dump(a.out/(case+'_checkpoint_method.json'),{'case':case,'mutated_checkpoint':d,'refused_at':'actual candidate ColdCheckpoint.from_json with independently provisioned fixture owner'})
  return
 group,name=mapped[case];e=a.execute_case(group,name)
 if 'alias' in case:assert e['original_fact_before']==e['original_fact_after'] and e['read_support_before']==e['read_support_after']
 else:assert_refusal(e)

@pytest.mark.parametrize('case',['exact25','valid_receipts','omission','unmodified_fact','unrehashed_checkpoint'])
def test_documented_five_positive_method_contracts(a,case):
 if case in ('exact25','valid_receipts','omission'):
  ops=builder().enumerate()
  if case=='exact25':assert w.validate_frontier(ops)=={'PRODUCED':3,'HELD':16,'INADMISSIBLE':6} and rows(ops)==O['operations']
  elif case=='valid_receipts':w.validate_frontier_receipts(rows(ops),ops)
  else:
   with pytest.raises(w.FrontierError):w.validate_frontier(ops[1:])
 elif case=='unmodified_fact':
  c=w.FactCustody();value={'denominator':6,'cells':[{'n':2}]};c.store('K',value);assert c.read('K')==value
 else:
  p=plan();_,rs=w.run_plan(p,w.make_executor(p),max_units=1);cp=w.create_checkpoint(p,rs);d=json.loads(cp.to_json());d['source_editions']['REL-A-W1']='FORGED'
  with pytest.raises(w.ColdRestartError,match='CHECKPOINT_PREIMAGE_HASH_MISMATCH'):w.ColdCheckpoint.from_json(json.dumps(d),fixture_owner=p.fixture_owner)
 dump(a.out/('positive_'+case+'.json'),{'case':case,'contract_exercised':True,'scope':'Reconstructed documented contract on full candidate; not original excerpt source replay.'})

def child_attack(a,kind):
 a.ensure_cold();folder=a.out/('cold_'+kind+'_'+uuid.uuid4().hex);folder.mkdir();shutil.copytree(a.cold_folder/'owner',folder/'owner')
 d=json.loads((a.cold_folder/'checkpoint.json').read_text())
 if kind=='nonrehash':d['source_editions']['REL-A-W1']='FORGED'
 elif kind=='grant':d['grant_state']='REAL_SOURCE_SIGNED_PERMISSION'
 elif kind=='fact':
  key=next(iter(d['fact_custody_snapshot']['facts']));d['fact_custody_snapshot']['facts'][key]['denominator']=999;d['fact_custody_snapshot']['hashes'][key]=w.digest(d['fact_custody_snapshot']['facts'][key])
 else:raise AssertionError(kind)
 if kind!='nonrehash':d['checkpoint_hash']=w.digest({k:v for k,v in d.items() if k not in ('signature','checkpoint_hash')})
 dump(folder/'checkpoint.json',d)
 cmd=[sys.executable,str(R/'repro/phase_b_cold_worker_v1.py'),'attack',str(folder)]
 child=subprocess.run(cmd,capture_output=True,text=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'));dump(folder/'command.json',{'command':cmd,'exit':child.returncode,'stdout':child.stdout,'stderr':child.stderr})
 assert child.returncode==0,child.stderr
 return json.loads((folder/'attack.json').read_text())

@pytest.mark.parametrize('case',['real_processes','nonrehash','fact','grant'])
def test_documented_four_real_cold_contracts(a,case):
 if case=='real_processes':assert_cold(a.case_cold('same_original_manifest'))
 else:
  out=child_attack(a,case);assert_refusal(out)
  assert not [c for c in out['calls'] if c['name']=='execute_empirical_query']
