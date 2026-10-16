"""E04U reviewer-authored controls. No owner callable or expected helper replaced."""
from common import *
import pytest,subprocess,sys,os
from rawlsing_next.pre553_empirical_authority import AuthorityRegistry
from rawlsing_next.pre553_empirical_objects import AuthoritySnapshot,canonicalize,ExactRef
KEY=('Y',(('A',1),))
NAMES=['nonparent','scenario']
def client(s,ss,name):return consume(s,ss) if name=='nonparent' else evaluate(s,ss,PROPOSALS)
def all_grants(s):return (*s.provider.world['source']['authorities'],s.provider.world['qauth'])
def hydrate(d):
 return AuthoritySnapshot(typed_state=d['typed_state'],authority_snapshot_refs=d['authority_snapshot_refs'],dependency_refs=d['dependency_refs'],producer_replay_locator_or_reference_root=d['producer_replay_locator_or_reference_root'],**d['semantic_fields'])
def deny_fresh(s,ss,name):
 before=len(s.value_reads);receipts=deepcopy(s.receipts)
 with pytest.raises(ValueError) as error:client(s,ss,name)
 assert not any(v['channel']=='empirical' for v in s.value_reads[before:])
 assert s.receipts==receipts
 return str(error.value)

@pytest.mark.parametrize('name',NAMES)
@pytest.mark.parametrize('kind',['empty','source_removed','query_operation_removed','issuer_reissued','edition_reissued','source_DENY'])
def test_live_nested_attachment_cannot_borrow_historical_grants(name,kind):
 s,ss,a,b=full();w=s.provider.world;items=[g.as_dict() for g in all_grants(s)]
 archived=s.historical_receipt(a['receipt_hash']);cache=deepcopy(s.provider.cache);anchors=dict(s.provider._accepted)
 # Two aliases point at the real catalog/provider world, not a mock registry.
 alias=s.catalog.empirical;assert alias is w
 if kind=='empty':items=[]
 elif kind=='source_removed':items.pop(0)
 elif kind=='query_operation_removed':items[-1]['semantic_fields']['governed_operations']=[]
 elif kind=='issuer_reissued':items[-1]['semantic_fields']['authority_id']='E04U_FOREIGN_ISSUER'
 elif kind=='edition_reissued':items[-1]['semantic_fields']['authority_version']='93.0.0'
 else:items[0]['typed_state']=items[0]['semantic_fields']['decision_state']='DENY'
 alias['registry']=AuthorityRegistry(hydrate(d) for d in items)
 error=deny_fresh(s,ss,name)
 assert s.provider.cache==cache and all(s.provider._accepted[k] is v for k,v in anchors.items())
 assert s.historical_receipt(a['receipt_hash'])==archived
 alias['registry']=AuthorityRegistry(hydrate(g.as_dict()) for g in all_grants(s))
 assert client(s,ss,name)==(a if name=='nonparent' else b)
 dump('e04u_nested_'+name+'_'+kind+'.json',dict(error=error,archive_unchanged=True,restored_product=True,attachment_alias_verified=True))

@pytest.mark.parametrize('name',NAMES)
def test_historical_world_clock_never_overrides_current_query_withdrawal(name):
 s=GenericSelectedWorldService(structural_revision=True)
 ss=s.select(mode='AS_OF',valid_at='2026-06-01',published_asof='2026-03-01');a=consume(s,ss);b=evaluate(s,ss,PROPOSALS)
 old=s.historical_receipt(a['receipt_hash']);s.provider.world['registry']=AuthorityRegistry(s.provider.world['source']['authorities'])
 error=deny_fresh(s,ss,name);assert s.historical_receipt(a['receipt_hash'])==old
 s.provider.world['registry']=AuthorityRegistry(all_grants(s));assert client(s,ss,name)==(a if name=='nonparent' else b)
 dump('e04u_historical_current_'+name+'.json',dict(error=error,archival_only=old['archival_only'],historical_snapshot=ss.material))

@pytest.mark.parametrize('name',NAMES)
@pytest.mark.parametrize('depth',[2,3])
@pytest.mark.parametrize('field',['minority','denominator','authority','query_ref'])
def test_independent_deep_coherently_rehashed_cache_corruption(name,depth,field):
 s,ss,a,b=full();key=('Y',tuple((q,1) for q in 'ABC'[:depth]));anchor=s.provider._accepted[key];p=s.provider.cache[key]
 if field=='minority':next(c for c in p['cells'] if c['cell']=='0')['raw_numerator_support']=314
 elif field=='denominator':p['denominator']=314
 elif field=='authority':p['authority_refs']=[]
 else:p['producer_query_ref']['content_hash']='9'*64
 p['content_hash']=semantic_hash({k:v for k,v in p.items() if k!='content_hash'})
 assert deny_fresh(s,ss,name)=='NATIVE_OWNER_CACHE_PROJECTION_MISMATCH'
 assert s.provider._accepted[key] is anchor
 del s.provider.cache[key];before=len(s.provider.trace)
 assert client(s,ss,name)==(a if name=='nonparent' else b)
 assert any(t['call']=='compose_positioned_subject_possibility' for t in s.provider.trace[before:])
 dump('e04u_deep_'+name+'_'+str(depth)+'_'+field+'.json',dict(refusal='NATIVE_OWNER_CACHE_PROJECTION_MISMATCH',native_recompute=True,restored_projection=json.loads(anchor.projection)))

@pytest.mark.parametrize('name',NAMES)
def test_projection_miss_with_withdrawn_native_grant_returns_typed_absence(name):
 s,ss,a,b=full();archive=s.historical_receipt(a['receipt_hash']);s.provider.cache.clear()
 s.provider.world['registry']=AuthorityRegistry(s.provider.world['source']['authorities'])
 out=client(s,ss,name);emp=out['material']['empirical']
 assert emp['state']=='PARTIAL_TYPED_EMPIRICAL_SUPPORT'
 assert all(t['state']=='UNAVAILABLE' and t['denominator']==0 and not t['cells'] and t['geometry'] is None for t in emp['steps'])
 assert s.historical_receipt(a['receipt_hash'])==archive
 s.provider.world['registry']=AuthorityRegistry(all_grants(s));assert client(s,ss,name)==(a if name=='nonparent' else b)
 dump('e04u_uncached_withdrawn_'+name+'.json',dict(absence=out,archive_unchanged=True,restored=True))

@pytest.mark.parametrize('conditions',[(('C',1),('A',1),('B',1)),(('B',0),('C',1)),(('A',0),('C',0))])
def test_native_order_and_minority_follow_independently_counted_rows(conditions):
 s=GenericSelectedWorldService();ss=s.select();out=s.possibilities(ss,conditions=conditions)
 for depth,step in enumerate(out['steps'],1):
  assert step['conditioners']==[list(c) for c in conditions[:depth]]
  assert geometry(step)==direct(independent_rows(),'Y',conditions[:depth])
 assert all(c['raw_numerator_support']>0 for c in out['steps'][-1]['cells'])

@pytest.mark.parametrize('name',NAMES)
def test_detached_nested_grant_alias_cannot_mutate_attached_native_registry(name):
 s,ss,a,b=full();d=s.provider.world['qauth'].as_dict();d['semantic_fields']['governed_operations'].clear()
 assert client(s,ss,name)==(a if name=='nonparent' else b)
 s.provider.world['registry']=AuthorityRegistry((*s.provider.world['source']['authorities'],hydrate(d)))
 deny_fresh(s,ss,name)

@pytest.mark.parametrize('name',NAMES)
def test_structural_revision_is_not_empirical_revocation(name):
 s,ss,a,b=full(structural_revision=True)
 assert [geometry(t) for t in a['material']['empirical']['steps']]==[dict(denominator=d,cells={'1':n,'0':d-n}) for n,d in [(18,32),(10,16),(6,8)]]
 before=deepcopy(s.provider.cache);s.invalidate('training_access')
 new=s.select();client(s,new,name);assert s.provider.cache==before

@pytest.mark.parametrize('state',['withdrawn','restored'])
def test_independent_cold_permission_hydration_before_any_native_query(state,tmp_path):
 s,ss,a,b=full();items=all_grants(s) if state=='restored' else s.provider.world['source']['authorities']
 payload=dict(state=state,grants=[g.as_dict() for g in items],projection=s.provider.cache[KEY],nonparent=a,scenario=b)
 fixture=tmp_path/'independent_current_grants.json';fixture.write_text(json.dumps(payload));digest=hashlib.sha256(fixture.read_bytes()).hexdigest();results=[]
 for k in range(2):
  out=R/'observations'/('e04u_cold_'+state+'_'+str(k)+'.json');audit=out.with_name(out.stem+'_process.json')
  p=subprocess.run([sys.executable,str(R/'repro/pytest_entry.py'),'--script',str(R/'repro/cold_worker.py'),str(fixture),str(out)],cwd=R,env=dict(os.environ,E04S_PROCESS_AUDIT=str(audit),PYTHONDONTWRITEBYTECODE='1'),capture_output=True,text=True)
  assert p.returncode==0,p.stderr
  results.append(json.loads(out.read_text()))
 assert len({os.getpid(),*[x['pid'] for x in results]})==3
 assert results[0]['results']==results[1]['results'];assert hashlib.sha256(fixture.read_bytes()).hexdigest()==digest
 dump('e04u_cold_'+state+'_proof.json',dict(parent_pid=os.getpid(),children=[x['pid'] for x in results],fixture_sha256=digest,bit_identical=True,hydration_before_first_query=True,results=results[0]['results']))
