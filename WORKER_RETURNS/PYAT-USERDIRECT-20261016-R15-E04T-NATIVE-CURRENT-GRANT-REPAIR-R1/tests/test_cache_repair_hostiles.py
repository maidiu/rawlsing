"""E04R implementer tests; complements, does not replace, frozen E04N51."""
from common import *
import pytest
from dataclasses import FrozenInstanceError
KEY=('Y',(('A',1),))

def rehash(value):value['content_hash']=semantic_hash({k:v for k,v in value.items() if k!='content_hash'})
def client(s,ss,name):return consume(s,ss) if name=='nonparent' else evaluate(s,ss,PROPOSALS)
def assert_no_empirical_read(s,start):assert not any(r['channel']=='empirical' for r in s.value_reads[start:])

@pytest.mark.parametrize('name',['nonparent','scenario'])
@pytest.mark.parametrize('rehash_local',[False,True])
def test_999_with_stale_or_coherent_digest_refused_before_client_read(name,rehash_local):
 s,ss,a,b=full();s.provider.cache[KEY]['cells'][1]['raw_numerator_support']=999
 if rehash_local:rehash(s.provider.cache[KEY])
 start=len(s.value_reads)
 with pytest.raises(ValueError,match='NATIVE_OWNER_CACHE_PROJECTION_MISMATCH'):client(s,ss,name)
 assert_no_empirical_read(s,start)
 assert s.historical_receipt(a['receipt_hash'])['material']==a['material']

@pytest.mark.parametrize('field',['source_universe_ref','release_ref','risk_set_ref','target_ref','evidence_ref','condition_witness_ref','producer_query_ref','producer_fact_ref'])
def test_same_counts_foreign_native_identity_with_recomputed_digest_refuses(field):
 s,ss,a,b=full();entry=s.provider.cache[KEY];foreign=deepcopy(entry[field]);foreign['object_id']='urn:e04r:foreign:'+field;foreign['content_hash']='a'*64;entry[field]=foreign;rehash(entry)
 start=len(s.value_reads)
 with pytest.raises(ValueError,match='NATIVE_OWNER_CACHE_PROJECTION_MISMATCH'):s.possibilities(ss)
 assert_no_empirical_read(s,start)

@pytest.mark.parametrize('mutation',['minority','denominator','fraction','partial_geometry','zero','order','F8_state','permission','authority','provenance'])
def test_partial_or_whole_projection_substitution_refuses(mutation):
 s,ss,a,b=full();e=s.provider.cache[KEY]
 if mutation=='minority':e['cells'][0]['raw_numerator_support']=0
 elif mutation=='denominator':e['denominator']=999
 elif mutation=='fraction':e['cells'][1]['raw_probability_exact_fraction']['$exact_fraction']=[1,1]
 elif mutation=='partial_geometry':e['geometry']={}
 elif mutation=='zero':e.update(state='ZERO_SUPPORT',cells=[],geometry=None,denominator=0)
 elif mutation=='order':e['conditioners']=[['B',1]]
 elif mutation=='F8_state':e['state']='PROXY_SUPPORTED'
 elif mutation=='permission':e['permission_root']='SELF_ISSUED_SAME_VALUES'
 elif mutation=='authority':e['authority_refs']=[]
 else:e['provenance_refs']=[]
 rehash(e);start=len(s.value_reads)
 with pytest.raises(ValueError,match='NATIVE_OWNER_CACHE_PROJECTION_MISMATCH'):s.possibilities(ss)
 assert_no_empirical_read(s,start)

def test_same_key_conflicting_valid_other_query_is_refused():
 s,ss,a,b=full();s.provider.cache[KEY]=deepcopy(s.provider.cache[('Y',(('A',1),('B',1)))])
 with pytest.raises(ValueError,match='NATIVE_OWNER_CACHE_PROJECTION_MISMATCH'):s.possibilities(ss)

def test_cold_service_does_not_accept_even_valid_foreign_process_cache():
 s,ss,a,b=full();t=GenericSelectedWorldService();ts=t.select();t.provider.cache=deepcopy(s.provider.cache)
 with pytest.raises(ValueError,match='UNATTESTED_NATIVE_CACHE_ENTRY'):t.possibilities(ts)
 t.provider.cache.clear();fresh=consume(t,ts);assert fresh==a
 assert any(x['call']=='provide_empirical_possibility_slice' for x in t.provider.trace)

def test_stale_native_owner_repository_cannot_authorize_old_cache():
 s,ss,a,b=full();other=build_source(changed=True);s.provider.world['source']['repo']=other['source']['repo']
 with pytest.raises(ValueError,match='ACCEPTED_NATIVE_SOURCE_UNAVAILABLE'):s.possibilities(ss)

def test_same_value_new_release_instance_requires_fresh_native_production():
 s,ss,a,b=full();other=build_source();s.provider.world['source']['repo']=other['source']['repo']
 with pytest.raises(ValueError,match='ACCEPTED_NATIVE_SOURCE_REPLACED'):s.possibilities(ss)

def test_reissued_query_issuer_and_permits_do_not_certify_cached_values():
 from rawlsing_next.pre553_empirical_objects import AuthoritySnapshot
 s,ss,a,b=full();w=s.provider.world;old=w['qauth'];fields=dict(old.semantic_fields)
 fields.update(authority_id='E04R_SELF_REISSUED_QUERY_ISSUER',authority_content_hash=semantic_hash('E04R_FAKE_ISSUER'))
 w['qauth']=AuthoritySnapshot(typed_state=old.typed_state,authority_snapshot_refs=old.authority_snapshot_refs,dependency_refs=old.dependency_refs,producer_replay_locator_or_reference_root=old.producer_replay_locator_or_reference_root,**fields)
 w['query_permits']['Y']['scope']='REISSUED_SAME_VALUE_PERMISSION'
 with pytest.raises(ValueError,match='SOURCE_QUERY_PERMISSION_BINDING_CHANGED'):s.possibilities(ss)

def test_returned_step_store_read_and_nested_client_readsets_are_isolated():
 s=GenericSelectedWorldService();ss=s.select();first=s.possibilities(ss);original=deepcopy(first)
 first['steps'][0]['cells'][0]['raw_numerator_support']=999
 assert s.possibilities(ss)==original
 a=consume(s,ss);history=s.historical_receipt(a['receipt_hash']);before=deepcopy(a)
 a['material']['values_read'][-1]['value_read'][0]['raw_numerator_support']=777
 a['material']['empirical']['steps'][0]['cells'].clear()
 assert s.historical_receipt(before['receipt_hash'])==history
 assert consume(s,ss)==before
 second=s.possibilities(ss);second['steps'][0]['authority_refs'].clear()
 assert s.possibilities(ss)==original

def test_owner_anchor_has_no_mutable_descendants_and_captures_actual_owners():
 s,ss,a,b=full();entry=s.provider._accepted[KEY]
 assert isinstance(entry.projection,bytes) and isinstance(entry.native_owner_material,bytes)
 with pytest.raises(FrozenInstanceError):entry.projection=b'forged'
 owner=json.loads(entry.native_owner_material);projection=json.loads(entry.projection)
 assert owner['facts'][0]['content_hash']==projection['producer_fact_ref']['content_hash']
 assert owner['evidence']['evidence_ref']==projection['evidence_ref']
 assert owner['composition']['raw_denominator_support']==projection['denominator']==32
 assert owner['F8']['exact_lane']['evidence_ref']==projection['evidence_ref']
 assert owner['F8']['exact_lane']['geometry']==projection['geometry']
 assert owner['query']['content_hash']==projection['producer_query_ref']['content_hash']

@pytest.mark.parametrize('field',['rows_hash','publication'])
def test_source_clock_or_rows_reissue_refuses_cache(field):
 s,ss,a,b=full();s.provider.world[field]='FOREIGN_SOURCE_REISSUE'
 with pytest.raises(ValueError):s.possibilities(ss)

def test_deep_corruption_is_atomic_for_empirical_reads_selective_for_structure():
 s,ss,a,b=full();history=s.historical_receipt(a['receipt_hash']);civil=s.structural_product(ss);key=('Y',(('A',1),('B',1),('C',1)))
 original=deepcopy(s.provider.cache[key]);anchors=dict(s.provider._accepted);s.provider.cache[key]['cells'][0]['raw_numerator_support']=999
 start=len(s.value_reads)
 with pytest.raises(ValueError):s.possibilities(ss)
 assert_no_empirical_read(s,start)
 assert s.structural_product(ss)==civil
 assert all(s.provider._accepted[k] is v for k,v in anchors.items())
 # Discard only the corrupt projection. Actual owner recomputation repairs
 # this descendant; unrelated accepted owner entries and M4/M5 stay intact.
 del s.provider.cache[key];restored=s.possibilities(ss)
 assert restored['steps'][-1]==original
 assert all(s.provider._accepted[k] is v for k,v in anchors.items() if k!=key)
 assert s.structural_product(ss)==civil
 assert s.historical_receipt(a['receipt_hash'])==history


def test_source_release_intervention_changes_only_empirical_descendants():
 s,ss,a,b=full();t,ts,c,d=full(empirical_changed=True)
 assert [geometry(x)['cells']['1'] for x in c['material']['empirical']['steps']]==[19,11,7]
 assert a['material']['structural_routes']==c['material']['structural_routes']
 assert ss.material['fields']==ts.material['fields']
 assert [x['feasibility'] for x in b['material']['scenarios']]==[x['feasibility'] for x in d['material']['scenarios']]
 assert s.historical_receipt(a['receipt_hash'])['material']==a['material']
 # Stale source cache injected into a newly produced source cannot be used.
 t.provider.cache[KEY]=deepcopy(s.provider.cache[KEY])
 with pytest.raises(ValueError):t.possibilities(ts)


def test_uncached_ZERO_SUPPORT_cannot_be_overridden_by_complete_cached_projection():
 s,ss,a,b=full(support_loss=True);key=('Y',(('A',1),('B',1),('C',1)))
 assert key not in s.provider.cache
 s.provider.cache[key]=deepcopy(s.provider.cache[KEY])
 with pytest.raises(ValueError,match='UNATTESTED_NATIVE_CACHE_ENTRY'):s.possibilities(ss)

@pytest.mark.parametrize('surface',['issuer','permit'])
def test_query_issuer_and_role_permit_reissue_each_refuse_independently(surface):
 s,ss,a,b=full();w=s.provider.world
 if surface=='permit':w['query_permits']['Y']['scope']='REISSUED'
 else:w['qauth']=build_source(changed=True)['qauth']
 with pytest.raises(ValueError,match='SOURCE_QUERY_PERMISSION_BINDING_CHANGED'):s.possibilities(ss)

def test_same_values_reordered_native_query_does_not_alias_original_key():
 s,ss,a,b=full();key=('Y',(('A',1),('B',1)))
 other=s.possibilities(ss,conditions=[('B',1),('A',1)])['steps'][-1]
 assert other['cells']==s.provider.cache[key]['cells']
 assert other['condition_witness_ref']!=s.provider.cache[key]['condition_witness_ref']
 s.provider.cache[key]=deepcopy(other)
 with pytest.raises(ValueError,match='NATIVE_OWNER_CACHE_PROJECTION_MISMATCH'):s.possibilities(ss)
