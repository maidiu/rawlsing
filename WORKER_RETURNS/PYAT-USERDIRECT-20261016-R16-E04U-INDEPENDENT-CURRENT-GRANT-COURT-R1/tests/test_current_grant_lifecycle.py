"""E04T current-use hostiles; no producer, native callable or oracle replacement."""
from common import *
import os,sys,subprocess,pytest
from rawlsing_next.pre553_empirical_authority import AuthorityRegistry
from rawlsing_next.pre553_empirical_objects import AuthoritySnapshot,canonicalize,ExactRef
KEY=('Y',(('A',1),))
def client(s,ss,name):return consume(s,ss) if name=='nonparent' else evaluate(s,ss,PROPOSALS)
def grants(w):return (*w['source']['authorities'],w['qauth'])
def clone(a,**changes):
 fields=canonicalize(a.semantic_fields);fields.update(changes);state=fields['decision_state']
 return AuthoritySnapshot(typed_state=state,authority_snapshot_refs=a.authority_snapshot_refs,dependency_refs=a.dependency_refs,producer_replay_locator_or_reference_root=a.producer_replay_locator_or_reference_root,**fields)
def refusal(s,ss,name):
 start=len(s.value_reads);prior=set(s.receipts)
 with pytest.raises(ValueError) as error:client(s,ss,name)
 assert not any(r['channel']=='empirical' for r in s.value_reads[start:])
 assert set(s.receipts)==prior
 return str(error.value)

@pytest.mark.parametrize('name',['nonparent','scenario'])
@pytest.mark.parametrize('kind',['query','source','coordinate','routing','replay'])
def test_each_exact_native_grant_withdrawal_and_restoration(name,kind):
 s,ss,a,b=full();w=s.provider.world;original=grants(w);index={'query':4,'source':0,'coordinate':1,'routing':2,'replay':3}[kind]
 archive=s.historical_receipt(a['receipt_hash']);cache=deepcopy(s.provider.cache);anchors=dict(s.provider._accepted);structural=s.structural_product(ss)
 for iteration in range(2):
  w['registry']=AuthorityRegistry(x for n,x in enumerate(original) if n!=index)
  error=refusal(s,ss,name)
  assert s.provider.cache==cache and all(s.provider._accepted[k] is v for k,v in anchors.items())
  assert s.historical_receipt(a['receipt_hash'])==archive and s.structural_product(ss)==structural
  w['registry']=AuthorityRegistry(clone(x) for x in reversed(original))
  assert client(s,ss,name)==(a if name=='nonparent' else b)
 dump('e04t_withdraw_restore_'+name+'_'+kind+'.json',dict(error=error,cycles=2,archive_unchanged=True,cache_unchanged=True,structural_unchanged=True,restored_exact_product=True))

@pytest.mark.parametrize('name',['nonparent','scenario'])
@pytest.mark.parametrize('extra',[False,True])
def test_replacement_registry_with_exact_grants_remains_productive(name,extra):
 s,ss,a,b=full();w=s.provider.world;old=w['registry'];items=[clone(x) for x in grants(w)]
 if extra:items.append(clone(w['qauth'],authority_id='UNRELATED-GRANT',authority_content_hash='e'*64))
 w['registry']=AuthorityRegistry(items)
 assert old is not w['registry'] and client(s,ss,name)==(a if name=='nonparent' else b)
 assert any(x['call']=='CURRENT_NATIVE_QUERY_GRANT_VALIDATED' and len(x['source_authority_refs'])==4 for x in s.provider.trace)

@pytest.mark.parametrize('name',['nonparent','scenario'])
@pytest.mark.parametrize('change',['operation','family','source_scope','DENY','DEFER','successor','foreign'])
def test_current_query_permission_cannot_be_replaced_by_nearby_grant(name,change):
 s,ss,a,b=full();w=s.provider.world;q=w['qauth']
 changes={'operation':dict(governed_operations=['FOREIGN-OPERATION']), 'family':dict(governed_object_families=['EmpiricalPredicate@1.0.0']), 'source_scope':dict(scope_envelope={'source_universe_refs':[ExactRef('EmpiricalUniverse','urn:e04t:foreign','a'*64).as_dict()]}),'DENY':dict(decision_state='DENY'),'DEFER':dict(decision_state='DEFER'),'successor':dict(authority_version='2.0.0',authority_content_hash='b'*64),'foreign':dict(authority_id='FOREIGN-QUERY',authority_content_hash='c'*64)}
 replacement=clone(q,**changes[change]);w['registry']=AuthorityRegistry((*w['source']['authorities'],replacement))
 error=refusal(s,ss,name)
 dump('e04t_query_'+name+'_'+change+'.json',dict(error=error,original=q.as_dict(),replacement=replacement.as_dict(),same_exact_key=q.authority_ref==replacement.authority_ref))
 w['registry']=AuthorityRegistry(grants(w));assert client(s,ss,name)==(a if name=='nonparent' else b)

@pytest.mark.parametrize('name',['nonparent','scenario'])
@pytest.mark.parametrize('change',['DENY','scope','operation'])
def test_changed_source_permission_under_same_declared_ref_cannot_authorize_cache(name,change):
 s,ss,a,b=full();w=s.provider.world;items=list(grants(w));original=items[2]
 changes={'DENY':dict(decision_state='DENY'),'scope':dict(scope_envelope={'source_universe_refs':[],'predicate_or_risk_set_refs':[]}),'operation':dict(governed_operations=['UNRELATED-RISK-OP'])}
 items[2]=clone(original,**changes[change]);assert items[2].authority_ref==original.authority_ref
 w['registry']=AuthorityRegistry(items);refusal(s,ss,name)
 w['registry']=AuthorityRegistry(grants(w));assert client(s,ss,name)==(a if name=='nonparent' else b)

@pytest.mark.parametrize('name',['nonparent','scenario'])
def test_risk_rekey_is_atomic_even_with_all_original_grants(name):
 s,ss,a,b=full();w=s.provider.world;old=w['source']['risk_refs']['R'];w['source']['risk_refs']['R']=ExactRef('RISK_SET','urn:e04t:foreign-risk','b'*64)
 assert refusal(s,ss,name)=='CATALOG_CONTENT_CHANGED'
 with pytest.raises(ValueError,match='^SOURCE_QUERY_PERMISSION_BINDING_CHANGED$'):s.provider.step('Y',(('A',1),))
 w['source']['risk_refs']['R']=old;assert client(s,ss,name)==(a if name=='nonparent' else b)

@pytest.mark.parametrize('first',['nonparent','scenario'])
def test_grant_loss_between_actual_clients_never_borrows_first_client_permission(first):
 s=GenericSelectedWorldService();ss=s.select();before=client(s,ss,first);w=s.provider.world;w['registry']=AuthorityRegistry(w['source']['authorities'])
 refusal(s,ss,'scenario' if first=='nonparent' else 'nonparent')
 assert s.historical_receipt(before['receipt_hash'])['material']==before['material']
 w['registry']=AuthorityRegistry(grants(w));client(s,ss,'scenario' if first=='nonparent' else 'nonparent')

@pytest.mark.parametrize('state',['withdrawn','restored'])
def test_cold_process_replay_uses_persisted_current_grants_not_fixture_defaults(state,tmp_path):
 s,ss,a,b=full();w=s.provider.world;items=grants(w) if state=='restored' else w['source']['authorities']
 material=dict(state=state,grants=[x.as_dict() for x in items],projection=s.provider.cache[KEY],nonparent=a,scenario=b)
 fixture=tmp_path/'current_grants.json';fixture.write_text(json.dumps(material));preimage=hashlib.sha256(fixture.read_bytes()).hexdigest();outputs=[]
 for attempt in range(2):
  label='cold_'+state+'_'+str(attempt);out=R/'observations'/(label+'.json');audit=R/'observations'/(label+'_process.json')
  env=dict(os.environ,E04S_PROCESS_AUDIT=str(audit),PYTHONDONTWRITEBYTECODE='1',PYTEST_DISABLE_PLUGIN_AUTOLOAD='1')
  command=[sys.executable,str(R/'repro/pytest_entry.py'),'--script',str(R/'repro/cold_worker.py'),str(fixture),str(out)]
  proc=subprocess.run(command,cwd=R,env=env,capture_output=True,text=True)
  dump(label+'_terminal.json',dict(argv=command,exit=proc.returncode,stdout=proc.stdout,stderr=proc.stderr))
  assert proc.returncode==0,proc.stderr
  result=json.loads(out.read_text());outputs.append(result)
  observed=json.loads(audit.read_text());functions={x['function']:x['count'] for x in observed['counts']}
  assert all(functions.get(n,0)>0 for n in ['ingest_c11_source_release','execute_empirical_query','compose_positioned_subject_possibility','provide_empirical_possibility_slice'])
  if state=='restored':assert functions['evaluate_positioned_subject_possibility']>0
 assert len({os.getpid(),outputs[0]['pid'],outputs[1]['pid']})==3
 assert outputs[0]['results']==outputs[1]['results'] and hashlib.sha256(fixture.read_bytes()).hexdigest()==preimage
 dump('e04t_cold_'+state+'.json',dict(parent_pid=os.getpid(),child_pids=[o['pid'] for o in outputs],bit_identical_results=True,persisted_current_grants_sha256=preimage,fixture_unchanged=True,results=outputs[0]['results']))
