from pathlib import Path
import sys,json,hashlib,dataclasses,subprocess,os
from copy import deepcopy
import pytest
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'repro'))
from support import *
from bridge import BridgeDisabled,T
from rawlsing_next.pre553_empirical_objects import ExactRef,semantic_hash
@pytest.fixture(scope='module')
def data():return json.loads((ROOT/'02_ACTUAL_NATIVE_TO_TWO_CONSUMER_PRODUCTS.json').read_text())
@pytest.fixture(scope='module')
def oracle():return json.loads((ROOT/'01_FROZEN_E04T_E05R_BRIDGE_CONTRACT.json').read_text())['expected']
def receipt(d,k):return d['products'][k]['selected_world_receipt']
def test_frozen_contract_precedes_candidate():
 p=ROOT/'01_FROZEN_E04T_E05R_BRIDGE_CONTRACT.json';assert hashlib.sha256(p.read_bytes()).hexdigest()==(ROOT/'01_FREEZE_SHA256.txt').read_text().split()[0]
 content=subprocess.check_output(['git','show','14f247b75:'+str(p.relative_to(ROOT.parents[1]))],cwd=ROOT)
 assert content==p.read_bytes()
def test_off_default():
 with pytest.raises(BridgeDisabled):NativeBridge(None)
 with pytest.raises(BridgeDisabled):NativeBridge(None,enabled=1)
def test_actual_source_current_and_both_clients(data,oracle):
 p=data['products']['CURRENT'];r=p['selected_world_receipt'];assert [list(x) for x in support(r)]==oracle['forward']
 assert len(r['consumers'])==2
 for c in r['consumers']:
  m=c['consumer_material'];assert m['snapshot_ref']==r['snapshot_hash']
  assert m['empirical']['steps']==r['empirical_steps']
  assert all(x['snapshot_ref']==r['snapshot_hash'] for x in m['values_read'])
 assert [next(c['raw_numerator_support'] for c in s['cells'] if c['cell']=='0') for s in r['empirical_steps']]==[14,6,2]
 assert r['request_hash']==p['request']['request_hash'] if 'request_hash' in p['request'] else r['request_hash']==p['acceptance']['request_hash']
 assert data['source_reconstruction']['actual_respondents']==58 and data['source_reconstruction']['actual_C11_events']==232
def test_Y_intervention_actual_producer_products(data,oracle):
 a=receipt(data,'CURRENT');b=receipt(data,'Y_CHANGED');assert [list(x) for x in support(b)]==oracle['Y0to1']
 assert a['structural_values']==b['structural_values'] and a['native_field_readset']==b['native_field_readset']
 for x,y in zip(a['consumers'],b['consumers']):assert x['consumer_material']['empirical']['steps']!=y['consumer_material']['empirical']['steps']
 assert a['empirical_steps'][0]['release_ref']!=b['empirical_steps'][0]['release_ref']
def test_reverse_separate_authorized_role(data):
 a=receipt(data,'REVERSE');assert support(a)==[(18,29)] and a['consumers']==[]
 assert a['empirical_target']=='A' and list(map(list,a['empirical_condition_order']))==[['Y',1]]
def test_current_historical_exact_structural_effect(data):
 a=receipt(data,'CURRENT');b=receipt(data,'HISTORICAL')
 assert [a['structural_values'][k]['value'] for k in ['training_access','exit_cost']]==[False,8]
 assert [b['structural_values'][k]['value'] for k in ['training_access','exit_cost']]==[True,2]
 assert a['empirical_steps']==b['empirical_steps']
 assert a['consumers'][0]['consumer_material']['structural_routes']['training']['state']=='BLOCKED_BY_MODELED_RULE'
 assert b['consumers'][0]['consumer_material']['structural_routes']['training']['state']=='ELIGIBLE'
 assert a['consumers'][1]['consumer_material']['scenarios'][0]['feasibility']=='INFEASIBLE_MODELED_PREMISE'
 assert b['consumers'][1]['consumer_material']['scenarios'][0]['feasibility']=='FEASIBLE_MODELED_PREMISE'
def test_native_fields_remain_distinct_not_persons(data):
 a=receipt(data,'CURRENT');v={x['role']:x for x in a['native_field_readset']['values_read']};g=v[GSS];n=v[NCA]
 assert (g['values']['numerator'],g['values']['denominator'])==(2388192,3288063)
 assert sum(g['values']['electricity_subtypes'].values())==2388192
 assert n['values']['active_subscriptions']==23414527
 assert g['native_unit']!=n['native_unit'] and g['native_geography']!=n['native_geography']
 assert not a['pooling'] and not a['person_exposure'] and not a['issued_EE13'] and not a['model_use']
 for c in a['consumers']:
  m=c['consumer_material']
  if m['consumer']=='NONPARENT_OPTIONS':assert m['route_probability'] is None
  else:assert not m['person_generation'] and not m['actual_conception'] and all(x['selection_weight'] is None for x in m['scenarios'])
def test_warm_query_grant_loss_and_exact_restoration(data):
 x=data['products']['QUERY_GRANT_LIFECYCLE'];a=x['before'];d=x['withdrawn'];z=x['restored']
 assert len(x['warm_cache_keys_before'])==3 and x['accepted_anchors_before']==3
 assert x['warm_query_grant_validations_before']==a['native_query_validation_count'] and x['warm_query_grant_validations_before']>0
 assert d['state']=='DEPENDENT_EMPIRICAL_USE_REFUSED' and not d['fresh_empirical_use_authorized']
 assert len(d['actual_warm_client_denials'])==2 and all(not c['fresh_receipt'] for c in d['actual_warm_client_denials'])
 p=d['selected_world_receipt'];assert p['state']=='TYPED_PARTIAL_SELECTED_WORLD'
 assert all(not s['cells'] and s.get('evidence_ref') is None and s['geometry'] is None for s in p['empirical_steps'])
 assert all('PARTIAL' in c['state'] for c in p['consumers'])
 assert p['structural_values']==a['selected_world_receipt']['structural_values']
 assert p['native_field_readset']==a['selected_world_receipt']['native_field_readset']
 assert x['same_acceptance'] and a['selected_world_receipt']==z['selected_world_receipt']
 assert x['archive']['archival_only'] and not x['archive']['fresh_use_authorized']
 assert x['archive']['receipt']['empirical_steps']==a['selected_world_receipt']['empirical_steps']
@pytest.mark.parametrize('role',[GSS,NCA])
def test_selective_native_revoke(data,role):
 x=data['products']['SELECTIVE_NATIVE_REVOCATION'][role];a=x['before']['selected_world_receipt'];b=x['after']['selected_world_receipt']
 assert b['state']=='TYPED_PARTIAL_SELECTED_WORLD'
 assert b['native_field_readset']['values_read']==[v for v in a['native_field_readset']['values_read'] if v['role']!=role]
 assert any(v['role']==role and v['reason']=='UNKNOWN_EXACT_FIELD_REF' for v in b['native_field_readset']['refusals'])
 assert a['native_field_readset']['dependency_readset']==b['native_field_readset']['dependency_readset']
 for k in ['structural_values','empirical_steps','consumers']:assert a[k]==b[k]
def test_publication_denial_is_distinct(data):
 a=receipt(data,'PRE_NCA_PUBLICATION');assert any(x['reason']=='NOT_PUBLISHED_AT_SELECTED_ASOF' for x in a['native_field_readset']['refusals'])
 assert a['empirical_steps']==[] and a['empirical_state']=='UNAVAILABLE_PUBLICATION_OR_EFFECTIVE_CLOCK'
def test_zero_support_is_actual_terminal(data):
 a=receipt(data,'ZERO_SUPPORT');s=a['empirical_steps'];assert [(next(c['raw_numerator_support'] for c in x['cells'] if c['cell']=='1'),x['denominator']) for x in s[:2]]==[(12,24),(4,8)]
 assert [x['denominator'] for x in s]==[24,8,0]
 assert s[-1]['state']=='ZERO_SUPPORT' and s[-1]['cells']==[] and s[-1]['geometry'] is None and s[-1].get('evidence_ref') is None
 assert all('PARTIAL' in x['state'] for x in a['consumers']) and len(a['native_field_readset']['values_read'])==2
def test_native_observed_zero_is_present_number(data):
 a=receipt(data,'OBSERVED_NATIVE_ZERO');n=next(x for x in a['native_field_readset']['values_read'] if x['role']==NCA)
 assert n['values']['active_subscriptions']==0 and a['state']=='SELECTED_WORLD_VALUES_SERVED'
def test_structural_access_fee_sanction_and_M4_denial(data):
 a=receipt(data,'BASE_STRUCTURAL');fee=receipt(data,'FEE_CHANGED');san=receipt(data,'SANCTION_CHANGED')
 assert a['consumers'][0]['consumer_material']['structural_routes']['training']['state']=='ELIGIBLE'
 assert fee['consumers'][0]['consumer_material']['structural_routes']['training']['state']=='BLOCKED_BY_MODELED_RULE'
 assert a['empirical_steps']==fee['empirical_steps']==san['empirical_steps']
 assert fee['native_field_readset']==a['native_field_readset']==san['native_field_readset']
 assert san['consumers'][1]['consumer_material']['scenarios'][1]['feasibility']=='INFEASIBLE_MODELED_PREMISE'
 x=data['products']['STRUCTURAL_DENIED'];assert x['selected_native_state']=='RESOLUTION_DENIED_OR_NOT_APPLICABLE'
 assert x['product']['selected_world_receipt']['structural_values']['training_access']['state']=='REVOKED'
def test_actual_imports_frames_and_original_identity(data):
 t=json.loads((ROOT/data['native_trace']['path']).read_text());assert hashlib.sha256((ROOT/data['native_trace']['path']).read_bytes()).hexdigest()==data['native_trace']['sha256'];names={x['function'] for x in t['actual_frames'] if x['count']}
 assert {'ingest_c11_source_release','execute_empirical_query','provide_empirical_possibility_slice','compose_positioned_subject_possibility','evaluate_positioned_subject_possibility','resolve_v558','materialize_resolved_structural_context','validate_resolved_structural_context','_authorize_cached_use','consume','evaluate','serve','accept'}.issubset(names)
 assert t['same_concrete_C1_evidence_into_F8']>0
 for c in t['compositions']:assert any(c['id'] in x['ids'] and c['evidence_ref'] in x['refs'] for x in t['F8_inputs'])
 assert any(x['module']=='e04t_empirical' and x['commit']=='79cb8244a5291218bde17142b93fc2419eade396' for x in t['imports'])
 assert any(x['module']=='product.empirical' and x['git_blob']=='475feb9f9aea495c11c40a56b083f0b628c34e15' for x in t['imports'])
 import e04t_empirical,product.empirical
 assert e04t_empirical.GenericProgressiveProvider is not product.empirical.GenericProgressiveProvider
 a=receipt(data,'CURRENT');facts={x['ref']['content_hash'] for x in t['I03_facts']}
 for s in a['empirical_steps']:
  assert s['producer_fact_ref']['content_hash'] in facts
  assert any(c['fact_ref']==s['producer_fact_ref'] and c['query_ref']==s['producer_query_ref'] and c['evidence_ref']==s['evidence_ref'] for c in t['compositions'])
 ss=[x for x in t['client_snapshots'] if x['snapshot_hash']==a['snapshot_hash']]
 assert {x['consumer'] for x in ss}=={'consume','evaluate'}
 assert any({x['consumer'] for x in ss if x['snapshot_object_id']==i}=={'consume','evaluate'} for i in {x['snapshot_object_id'] for x in ss})
def test_weak_null_source_support(data):
 strata=json.loads((ROOT/'01_FROZEN_E04T_E05R_BRIDGE_CONTRACT.json').read_text())['source_strata'];source=[dict(zip('ABC',map(int,k)),Y=y) for k,(yes,no) in strata.items() for y,n in [(1,yes),(0,no)] for _ in range(n)]
 for x in data['products']['WEAK_NULL'].values():
  for s in x['selected_world_receipt']['empirical_steps']:
   selected=[r for r in source if all(r[q]==v for q,v in s['conditioners'])]
   assert s['denominator']==len(selected)
   assert {c['cell']:c['raw_numerator_support'] for c in s['cells']}=={str(v):sum(r['Y']==v for r in selected) for v in [0,1]}
@pytest.mark.parametrize('change',['query_missing','source_missing','wrong_operation','DENY','wrong_issuer','successor'])
def test_no_unauthorized_grant_reissue(change):
 b=bridge();p=b.prepare(request());before=b.read(p);w=b.provider.world;original=grants(w)
 if change=='query_missing':items=w['source']['authorities']
 elif change=='source_missing':items=original[1:]
 else:
  delta={'wrong_operation':dict(governed_operations=['FOREIGN']),'DENY':dict(decision_state='DENY'),'wrong_issuer':dict(authority_id='FOREIGN-ISSUER',authority_content_hash='c'*64),'successor':dict(authority_version='2.0.0',authority_content_hash='b'*64)}[change]
  items=(*w['source']['authorities'],clone(w['qauth'],**delta))
 w['registry']=AuthorityRegistry(items)
 try:out=b.read(p)
 except ValueError as exc:assert str(exc)
 else:
  assert out['state']!='SELECTED_WORLD_VALUES_SERVED'
  assert not out['selected_world_receipt']['empirical_steps'][0]['cells']
 # Unrelated channels remain actually readable; restoring only original grants succeeds.
 assert b.service.structural_product(p.snapshot)['material']['state']=='VALUES_READ'
 w['registry']=AuthorityRegistry(original);assert b.read(p)['selected_world_receipt']==before['selected_world_receipt']
@pytest.mark.parametrize('change',['release','risk','permission','provider'])
def test_exact_binding_substitution_refuses(change):
 b=bridge();p=b.prepare(request());b.read(p);w=b.provider.world
 if change=='release':w['source']['release_ref']=ExactRef('C11_RELEASE','urn:foreign','f'*64)
 elif change=='risk':w['source']['risk_refs']['R']=ExactRef('RISK_SET','urn:foreign','b'*64)
 elif change=='permission':w['permission_root']='FOREIGN'
 else:
  import product.empirical
  b.service.provider=product.empirical.GenericProgressiveProvider(w)
 with pytest.raises(ValueError):b.read(p)
@pytest.mark.parametrize('attack',['clock','client_native_contamination','foreign_partial_snapshot'])
def test_clock_and_partial_readset_contamination_refuse(attack):
 b=bridge();p=b.prepare(request());a=b.read(p)
 if attack=='clock':
  q=E.N9SelectedWorldRequest.from_binding(request('HISTORICAL_AS_OF'))
  with pytest.raises(E.N9SelectedWorldRefusal):b.adapter.serve(q,p.acceptance,p.snapshot)
 elif attack=='client_native_contamination':
  c=[x['consumer_material'] for x in a['selected_world_receipt']['consumers']];c[0]['native_field_readset']={'state':'TWO_VALUES_READ_TEST_ONLY','values_read':[{'role':NCA,'values':{'active_subscriptions':999}}]}
  with pytest.raises(E.N9SelectedWorldRefusal,match='NOT_EXACT'):b.read(p,supplied_consumers=c)
 else:
  rr=rows();next(x for x in rr if x['role']==NCA)['status']='REVOKED_TEST_ONLY';b.adapter.registry=TestOnlyRegistry(rr);partial=b.read(p)
  other=bridge().prepare(request())
  with pytest.raises(ValueError,match='FOREIGN_PREPARED'):b.read(other)
  c=[x['consumer_material'] for x in partial['selected_world_receipt']['consumers']];c[0]['values_read'][0]['snapshot_ref']='FOREIGN_PARTIAL'
  with pytest.raises(E.N9SelectedWorldRefusal):b.read(p,supplied_consumers=c)
def test_archival_not_new_process_acceptance(data):
 x=data['products']['QUERY_GRANT_LIFECYCLE'];b=bridge();p=b.prepare(request());a=b.read(p);arch=b.archive(a);fresh=bridge()
 assert arch['archival_only'] and not arch['fresh_use_authorized']
 with pytest.raises(ValueError,match='FOREIGN_PREPARED'):fresh.read(p)
 assert x['withdrawn']['selected_world_receipt']['empirical_steps']!=x['archive']['receipt']['empirical_steps']
@pytest.mark.parametrize('state',['restored','withdrawn'])
def test_cold_persisted_current_grants(state,data):
 source=ROOT/'observations'/('current_grants_'+state+'.json');preimage=hashlib.sha256(source.read_bytes()).hexdigest();results=[]
 for i in range(2):
  dest=ROOT/'observations'/('cold_'+state+'_'+str(i)+'.json')
  args=[sys.executable,str(ROOT/'repro/cold_worker.py'),str(source.relative_to(ROOT)),str(dest.relative_to(ROOT))]
  p=subprocess.run(args,cwd=ROOT,capture_output=True,text=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
  (ROOT/'observations'/('cold_'+state+'_'+str(i)+'.terminal.json')).write_text(json.dumps(dict(argv=['python3','repro/cold_worker.py',str(source.relative_to(ROOT)),str(dest.relative_to(ROOT))],exit=p.returncode,stdout=p.stdout,stderr=p.stderr.replace(str(ROOT),'<RETURN>')),indent=2)+'\n')
  assert p.returncode==0,p.stderr
  x=json.loads(dest.read_text());results.append(x)
  assert x['grant_ledger_attached_before_first_query'] and x['ledger_sha256']==preimage
  assert x['foreign_projection']['reason']=='UNATTESTED_NATIVE_CACHE_ENTRY'
  assert any(f['function']=='ingest_c11_source_release' and f['count'] for f in x['trace']['actual_frames'])
 assert len({os.getpid(),*(x['pid'] for x in results)})==3
 assert json.dumps(results[0]['result'],sort_keys=True)==json.dumps(results[1]['result'],sort_keys=True)
 r=results[0]['result']['selected_world_receipt']
 if state=='restored':assert r==receipt(data,'CURRENT')
 else:assert all(not s['cells'] and s.get('evidence_ref') is None for s in r['empirical_steps']) and all('PARTIAL' in c['state'] for c in r['consumers'])
 assert hashlib.sha256(source.read_bytes()).hexdigest()==preimage
 (ROOT/'observations'/('cold_'+state+'_comparison.json')).write_text(json.dumps(dict(parent_pid=os.getpid(),child_pids=[x['pid'] for x in results],bit_identical_serialized_result=True,persisted_ledger_sha256=preimage,original_fixture_grants_not_renewed=True),indent=2)+'\n')
def test_every_imported_git_preimage_and_no_installation(data):
 m=json.loads((ROOT/'source_manifest.json').read_text());assert len(m)==402
 for x in m:
  b=(ROOT/x['local']).read_bytes();assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==x['git_blob'] and hashlib.sha256(b).hexdigest()==x['sha256']
 assert all(x['same'] for x in json.loads((ROOT/'native_closure_compatibility.json').read_text()))
 for x in receipt(data,'CURRENT')['installed_OC05'].values():
  if 'OC05' in x['policy_id']:assert x['consumer_seam'] is None and x['current_applicability']=='NOT_YET_APPLICABLE'

@pytest.mark.parametrize('role',[GSS,NCA])
def test_explicit_native_source_revoked_differs_from_rekey_and_publication(data,role):
 x=data['products']['SELECTIVE_NATIVE_EXPLICIT_WITHDRAWAL'][role];a=x['before']['selected_world_receipt'];b=x['after']['selected_world_receipt']
 assert any(v['role']==role and v['reason']=='SOURCE_REVOKED' for v in b['native_field_readset']['refusals'])
 assert a['empirical_steps']==b['empirical_steps'] and a['structural_values']==b['structural_values']
 assert a['consumers']==b['consumers']
 assert b['native_field_readset']['values_read']==[v for v in a['native_field_readset']['values_read'] if v['role']!=role]
 assert a['receipt_hash'] in x['invalidation']['invalidated_for_fresh_use']

def test_same_ref_foreign_native_release_object_refuses():
 b=bridge();p=b.prepare(request());b.read(p);w=b.provider.world
 w['source']['repo']=T.build_source()['source']['repo']
 with pytest.raises(ValueError,match='ACCEPTED_NATIVE_SOURCE_REPLACED'):b.read(p)

@pytest.mark.parametrize('kind',['numeric','foreign_release'])
def test_e04t_owner_cache_guard_precedes_e05r_clear(kind):
 b=bridge();p=b.prepare(request());b.read(p);key=('Y',(('A',1),));cached=b.provider.cache[key]
 if kind=='numeric':cached['cells'][1]['raw_numerator_support']=999
 else:cached['release_ref']=dict(kind='C11_RELEASE',object_id='FOREIGN',content_hash='f'*64)
 content=deepcopy(cached);content.pop('content_hash');cached['content_hash']=semantic_hash(content)
 with pytest.raises(ValueError,match='NATIVE_OWNER_CACHE_PROJECTION_MISMATCH'):b.read(p)

def test_e05r_service_factory_cannot_swap_back_to_original():
 b=bridge();p=b.prepare(request());b.read(p)
 from product.service import GenericSelectedWorldService
 b.adapter.service=GenericSelectedWorldService(structural_revision=True)
 with pytest.raises(ValueError,match='PINNED_E04T_PROVIDER_SUBSTITUTED'):b.read(p)


def test_clock_denied_world_does_not_prewarm_future_empirical_evidence():
 b=bridge();p=b.prepare(request('TYPED_PARTIAL_PRE_NCA_PUBLICATION'));out=b.read(p)
 assert b.provider.cache=={} and b.provider._accepted=={}
 assert b.provider.trace==[]
 assert out['selected_world_receipt']['empirical_steps']==[]
 assert out['selected_world_receipt']['empirical_state']=='UNAVAILABLE_PUBLICATION_OR_EFFECTIVE_CLOCK'
