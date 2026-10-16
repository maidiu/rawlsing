"""Fresh E04S scientific and cache-trust invariants, no author expected helper."""
from common import *
import dataclasses,pytest
from rawlsing_next.pre553_empirical_authority import AuthorityRegistry
KEY=('Y',(('A',1),))
def client(s,ss,name):return consume(s,ss) if name=='nonparent' else evaluate(s,ss,PROPOSALS)
def rehash(d):d['content_hash']=semantic_hash({k:v for k,v in d.items() if k!='content_hash'})
def record(name,data):dump('e04s_'+name+'.json',data)

@pytest.mark.parametrize('name',['nonparent','scenario'])
@pytest.mark.parametrize('mutation',['numerator','minority','denominator','fraction','source','release','risk','evidence','fact','query','witness','permission','authority','policy','order','state'])
def test_changed_projection_never_reaches_either_client(name,mutation):
 s,ss,a,b=full();anchors=dict(s.provider._accepted);original=deepcopy(s.provider.cache[KEY]);entry=s.provider.cache[KEY]
 if mutation=='numerator':next(c for c in entry['cells'] if c['cell']=='1')['raw_numerator_support']=999
 elif mutation=='minority':next(c for c in entry['cells'] if c['cell']=='0')['raw_numerator_support']=999
 elif mutation=='denominator':entry['denominator']=1
 elif mutation=='fraction':entry['cells'][1]['raw_probability_exact_fraction']['$exact_fraction']=[1,1]
 elif mutation in ['source','release','risk','evidence','fact','query','witness']:
  key={'source':'source_universe_ref','release':'release_ref','risk':'risk_set_ref','evidence':'evidence_ref','fact':'producer_fact_ref','query':'producer_query_ref','witness':'condition_witness_ref'}[mutation]
  entry[key]=dict(entry[key],object_id='urn:e04s:foreign:'+mutation,content_hash='b'*64)
 elif mutation=='permission':entry['permission_root']='WITHDRAWN_OR_FOREIGN_PERMISSION'
 elif mutation=='authority':entry['authority_refs']=[]
 elif mutation=='policy':entry['measure']='POLICY_PROMOTED_PERSON_SELECTION'
 elif mutation=='order':entry['conditioners']=[['Y',1]]
 else:entry.update(state='ZERO_SUPPORT',cells=[],denominator=0,geometry=None)
 rehash(entry);start=len(s.value_reads);prior=set(s.receipts)
 with pytest.raises(ValueError,match='NATIVE_OWNER_CACHE_PROJECTION_MISMATCH') as caught:client(s,ss,name)
 assert not any(x['channel']=='empirical' for x in s.value_reads[start:])
 assert set(s.receipts)==prior
 assert all(s.provider._accepted[k] is v for k,v in anchors.items())
 assert json.loads(anchors[KEY].projection)==original
 record(name+'_'+mutation,dict(error=str(caught.value),accepted_projection=original,hostile_projection=entry,reads_before_refusal=s.value_reads[start:],new_product_receipts=sorted(set(s.receipts)-prior)))

@pytest.mark.parametrize('depth',[2,3])
@pytest.mark.parametrize('name',['nonparent','scenario'])
def test_later_step_corruption_is_atomic_and_recompute_is_selective(depth,name):
 s,ss,a,b=full();key=('Y',tuple((q,1) for q in 'ABC'[:depth]));old=deepcopy(s.provider.cache[key]);anchors=dict(s.provider._accepted);structural=s.structural_product(ss);history=s.historical_receipt(a['receipt_hash'])
 s.provider.cache[key]['content_hash']='0'*64;start=len(s.value_reads)
 with pytest.raises(ValueError):client(s,ss,name)
 assert not any(x['channel']=='empirical' for x in s.value_reads[start:])
 assert s.structural_product(ss)==structural
 del s.provider.cache[key];before=len(s.provider.trace);actual=s.possibilities(ss)
 assert actual['steps'][depth-1]==old
 assert any(x['call']=='compose_positioned_subject_possibility' for x in s.provider.trace[before:])
 assert all(s.provider._accepted[k] is v for k,v in anchors.items() if k!=key)
 assert s.historical_receipt(a['receipt_hash'])==history
 record('recompute_'+name+'_'+str(depth),dict(before=old,after=actual['steps'][depth-1],new_trace=s.provider.trace[before:],structural_unchanged=True,historical_unchanged=True))

@pytest.mark.parametrize('kind',['missing_query','empty'])
@pytest.mark.parametrize('name',['nonparent','scenario'])
def test_current_native_authority_withdrawal_blocks_cached_fresh_use(kind,name):
 s,ss,a,b=full();w=s.provider.world
 w['registry']=AuthorityRegistry(w['source']['authorities'] if kind=='missing_query' else ())
 # Current attached native registry no longer resolves the required authority.
 with pytest.raises(ValueError):w['registry'].resolve_exact(w['qauth'].authority_ref)
 before=len(s.value_reads);prior=set(s.receipts)
 try:out=client(s,ss,name)
 except ValueError as exc:
  record('authority_'+kind+'_'+name,dict(refused=True,error=str(exc)));return
 record('authority_'+kind+'_'+name,dict(refused=False,returned=out,new_reads=s.value_reads[before:],new_receipts=sorted(set(s.receipts)-prior)))
 pytest.fail('WITHDRAWN_NATIVE_QUERY_AUTHORITY_STILL_SERVES_CACHED_PRODUCT:'+out['material']['state'])

@pytest.mark.parametrize('name',['nonparent','scenario'])
def test_cold_injection_has_no_native_attestation(name):
 s,ss,a,b=full();t=GenericSelectedWorldService();ts=t.select();t.provider.cache=deepcopy(s.provider.cache)
 with pytest.raises(ValueError,match='UNATTESTED_NATIVE_CACHE_ENTRY'):client(t,ts,name)
 t.provider.cache.clear();assert client(t,ts,name)==(a if name=='nonparent' else b)

@pytest.mark.parametrize('surface',['rows','publication','query_grant','query_issuer','same_value_repository','different_repository'])
def test_source_clock_edition_or_grant_reissue_cannot_renew_old_cache(surface):
 s,ss,a,b=full();w=s.provider.world
 if surface=='rows':w['rows_hash']='a'*64
 elif surface=='publication':w['publication']='2028-12-31'
 elif surface=='query_grant':w['query_permits']['Y']['scope']='NEW_REQUESTER_GRANT'
 elif surface=='query_issuer':w['qauth']=build_source(changed=True)['qauth']
 else:w['source']['repo']=build_source(changed=surface=='different_repository')['source']['repo']
 with pytest.raises(ValueError):s.possibilities(ss)

@pytest.mark.parametrize('name',['nonparent','scenario'])
def test_returned_client_descendants_are_not_private_anchors(name):
 s,ss,a,b=full();result=client(s,ss,name);unchanged=deepcopy(result);anchors={k:v.projection for k,v in s.provider._accepted.items()}
 result['material']['empirical']['steps'][0]['cells'][0]['raw_numerator_support']=999
 result['material']['values_read'].clear()
 if name=='scenario':result['material']['scenarios'][0]['empirical_profiles'][0]['complete_native_cells'].clear()
 else:result['material']['source_balance_reads'][0]['all_alternatives'].clear()
 assert client(s,ss,name)==unchanged
 assert {k:v.projection for k,v in s.provider._accepted.items()}==anchors
 assert s.historical_receipt(unchanged['receipt_hash'])['material']==unchanged['material']

@pytest.mark.parametrize('conditions',[(('A',0),),(('A',1),('B',0)),(('A',0),('B',1),('C',1))])
def test_independent_minority_weak_null_native_strata(conditions):
 s=GenericSelectedWorldService();ss=s.select();actual=s.possibilities(ss,conditions=conditions)
 for depth,step in enumerate(actual['steps'],1):assert geometry(step)==direct(independent_rows(),'Y',conditions[:depth])
 assert all(c['raw_numerator_support']>0 for c in actual['steps'][-1]['cells'])
 assert all(x['uncertainty']=='UNCERTAINTY_UNQUANTIFIED' for x in actual['steps'])
 record('stratum_'+''.join(k+str(v) for k,v in conditions),actual)

def test_source_mutation_propagates_to_both_profiles_keeps_native_structural_bytes():
 s,ss,a,b=full();t,ts,c,d=full(empirical_changed=True)
 assert ss.material['fields']==ts.material['fields']
 assert [geometry(x) for x in c['material']['empirical']['steps']]==[{'denominator':32,'cells':{'0':13,'1':19}},{'denominator':16,'cells':{'0':5,'1':11}},{'denominator':8,'cells':{'0':1,'1':7}}]
 assert c['material']['structural_routes']==a['material']['structural_routes']
 assert d['material']['scenarios'][0]['empirical_profiles']!=b['material']['scenarios'][0]['empirical_profiles']
 t.provider.cache[KEY]=deepcopy(s.provider.cache[KEY])
 with pytest.raises(ValueError):t.possibilities(ts)

def test_actual_zero_support_remains_uncached_and_cannot_be_laundered():
 s,ss,a,b=full(support_loss=True);steps=a['material']['empirical']['steps']
 assert [x['denominator'] for x in steps]==[24,8,0];assert steps[-1]['state']=='ZERO_SUPPORT' and steps[-1]['geometry'] is None and steps[-1]['cells']==[]
 assert a['material']['state']=='PARTIAL_OPTIONS_OR_EMPIRICAL_SUPPORT';assert b['material']['state']=='PARTIAL_PROPOSALS_EVALUATED'
 assert ('Y',(('A',1),('B',1),('C',1))) not in s.provider._accepted
 record('zero_support',dict(nonparent=a,scenario=b))

def test_original_private_entry_is_deeply_immutable_and_owner_bound():
 s,ss,a,b=full();entry=s.provider._accepted[KEY]
 with pytest.raises(dataclasses.FrozenInstanceError):entry.projection=b'forged'
 with pytest.raises(TypeError):entry.projection[0]=0
 material=json.loads(entry.native_owner_material);projection=json.loads(entry.projection)
 assert material['facts'][0]['content_hash']==projection['producer_fact_ref']['content_hash']
 assert material['evidence']['evidence_ref']==projection['evidence_ref']
 assert material['F8']['exact_lane']['evidence_ref']==projection['evidence_ref']
 assert material['query']['content_hash']==projection['producer_query_ref']['content_hash']
 material['facts'][0]['content_hash']='FOREIGN'
 assert json.loads(entry.native_owner_material)['facts'][0]['content_hash']==projection['producer_fact_ref']['content_hash']
 record('immutable_private_entry',dict(owner_material=json.loads(entry.native_owner_material),projection=projection))

def test_native_release_and_fact_carriers_reject_normal_mutation():
 s,ss,a,b=full();release=s.provider._source_release;event=next(x for x in release.public_objects if x.schema_id=='EmpiricalCoordinateFact')
 before=event.semantic_projection()
 with pytest.raises(dataclasses.FrozenInstanceError):release.semantic_release_hash='0'*64
 with pytest.raises(AttributeError):event.raw_response_value=999
 with pytest.raises(TypeError):event.semantic_fields['raw_response_value']=999
 detached=event.semantic_projection();detached['semantic_fields']['raw_response_value']=999
 assert event.semantic_projection()==before
 assert consume(s,ss)==a
 record('native_carrier_mutation',dict(native_fact_ref=event.ref.as_dict(),before=before,after=event.semantic_projection(),normal_assignment_refused=True,detached_projection_isolated=True))
