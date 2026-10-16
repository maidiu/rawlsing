"""Fresh E05A product/transport checks; do not rerun the completed E05S court."""
from pathlib import Path
import json,hashlib,subprocess,sys
import pytest
R=Path(__file__).resolve().parents[1]
@pytest.fixture(scope='module')
def execution():return json.loads((R/'02_EXECUTED_TWO_CONSUMER_SERVICE_HANDOFF.json').read_text())
def receipt(execution,label):return execution['packets'][label]['selected_world_receipt']
def support(r):return [(next(c['raw_numerator_support'] for c in s['cells'] if c['cell']=='1'),s['denominator']) for s in r['empirical_steps']]

def test_versioned_real_request_acceptance_receipt_transport(execution):
 p=execution['packets']['CURRENT_TEST_CLOCK'];r=p['selected_world_receipt']
 assert p['schema']=='E05A_SOURCEFREE_METHOD_HANDOFF@1'
 assert p['request']['schema']=='N9_SELECTED_WORLD_REQUEST@2'
 assert p['acceptance']['request_hash']==r['request_hash']
 assert p['acceptance']['snapshot_hash']==r['snapshot_hash']
 assert p['consumer_values']==r['consumers']
 assert len(r['consumers'])==2

def test_current_historical_worlds_change_actual_options(execution):
 current=receipt(execution,'CURRENT_TEST_CLOCK');history=receipt(execution,'HISTORICAL_AS_OF')
 assert current['structural_values']['training_access']['value'] is False
 assert current['structural_values']['exit_cost']['value']==8
 assert history['structural_values']['training_access']['value'] is True
 assert history['structural_values']['exit_cost']['value']==2
 assert current['structural_values']['training_access']['field_ref']!=history['structural_values']['training_access']['field_ref']
 a=current['consumers'][0]['consumer_material'];b=history['consumers'][0]['consumer_material']
 assert a['structural_routes']['training']['state']=='BLOCKED_BY_MODELED_RULE'
 assert b['structural_routes']['training']['state']=='ELIGIBLE'
 assert current['consumers'][1]['consumer_material']['scenarios'][0]['feasibility']=='INFEASIBLE_MODELED_PREMISE'
 assert history['consumers'][1]['consumer_material']['scenarios'][0]['feasibility']=='FEASIBLE_MODELED_PREMISE'

def test_exact_progression_and_minorities_reach_consumers(execution):
 r=receipt(execution,'CURRENT_TEST_CLOCK');assert support(r)==[(18,32),(10,16),(6,8)]
 assert [next(c['raw_numerator_support'] for c in s['cells'] if c['cell']=='0') for s in r['empirical_steps']]==[14,6,2]
 for c in r['consumers']:
  m=c['consumer_material'];assert m['snapshot_ref']==r['snapshot_hash']
  assert [s['denominator'] for s in m['empirical']['steps']]==[32,16,8]
  assert all(x['snapshot_ref']==r['snapshot_hash'] for x in m['values_read'])

def test_source_empirical_change_propagates_both_clients_only(execution):
 a=receipt(execution,'CURRENT_TEST_CLOCK');b=receipt(execution,'EMPIRICAL_Y_CHANGED')
 assert support(b)==[(19,32),(11,16),(7,8)]
 assert a['structural_values']==b['structural_values'];assert a['native_field_readset']==b['native_field_readset']
 for x,y in zip(a['consumers'],b['consumers']):assert x['consumer_material']['empirical']['steps']!=y['consumer_material']['empirical']['steps']
 assert [x['source_balance_count'] for x in b['consumers'][0]['consumer_material']['source_balance_reads']]==[6,6,6]

def test_native_facts_remain_distinct_unpooled(execution):
 r=receipt(execution,'CURRENT_TEST_CLOCK');native={x['role']:x for x in r['native_field_readset']['values_read']}
 g=native['GSS_RURAL_LIGHTING'];n=native['NCA_NATIONAL_MOBILE_DATA']
 assert g['values']['numerator']==2388192 and g['values']['denominator']==3288063
 assert g['values']['published_percent']==72.6 and len(g['values']['electricity_subtypes'])==5
 assert sum(g['values']['electricity_subtypes'].values())==2388192
 assert n['values']['active_subscriptions']==23414527
 assert g['native_unit']!=n['native_unit'] and g['native_geography']!=n['native_geography']
 assert g['publication_date']=='2022-02-24' and n['publication_date']=='2022-07-08'
 assert not r['pooling'] and not r['person_exposure'] and not r['issued_EE13']

def test_native_accepted_custody_does_not_issue_rights(execution):
 p=execution['packets']['CURRENT_TEST_CLOCK']
 for role,c in p['native_accepted_custody'].items():
  assert c['fixture_only'] and not c['issued']
  assert c['permission']=='TEST_ONLY_NO_EXTERNAL_USE_GRANT'
  assert c['issuer_ref'] is None and c['source_pdf_sha256'] is None
  assert c['uncertainty']

def test_present_time_withdrawal_keeps_gss_and_other_channels(execution):
 before=execution['native_withdrawal_before']['selected_world_receipt'];after=receipt(execution,'LATE_NCA_WITHDRAWAL')
 assert after['state']=='TYPED_PARTIAL_SELECTED_WORLD'
 assert [x['role'] for x in after['native_field_readset']['values_read']]==['GSS_RURAL_LIGHTING']
 assert len(after['native_field_readset']['dependency_readset'])==2
 for k in ['structural_values','empirical_steps','consumers']:assert after[k]==before[k]
 assert after['acceptance_hash']==before['acceptance_hash']

def test_archival_receipt_preserves_old_material_without_fresh_permission(execution):
 a=execution['archival_receipt'];before=execution['native_withdrawal_before']['selected_world_receipt']
 assert a['archival_only'] and not a['fresh_use_authorized']
 old=a['retained']['receipt'];assert len(old['native_field_readset']['values_read'])==2
 assert old['snapshot_hash']==before['snapshot_hash']
 assert not a['retained']['fresh_use_authorized']

def test_late_publication_requires_separate_acceptance(execution):
 p=execution['late_publication_and_separate_acceptance']
 assert p['new_acceptance']
 assert p['before']['selected_world_receipt']['native_field_readset']['state']!='TWO_VALUES_READ_TEST_ONLY'
 assert p['after']['selected_world_receipt']['native_field_readset']['state']=='TWO_VALUES_READ_TEST_ONLY'
 assert p['before']['acceptance']['request_hash']!=p['after']['acceptance']['request_hash']

def test_zero_support_remains_typed_with_lawful_native_arms(execution):
 r=receipt(execution,'ZERO_SUPPORT');s=r['empirical_steps']
 assert [x['denominator'] for x in s]==[24,8,0]
 assert s[-1]['state']=='ZERO_SUPPORT' and s[-1]['cells']==[]
 assert s[-1]['geometry'] is None and s[-1].get('evidence_ref') is None
 assert r['state']=='TYPED_PARTIAL_SELECTED_WORLD' and len(r['native_field_readset']['values_read'])==2
 assert all('PARTIAL' in x['state'] for x in r['consumers'])

def test_authorized_reverse_is_own_request_and_scalar_only(execution):
 p=execution['packets']['AUTHORIZED_REVERSE'];r=p['selected_world_receipt']
 assert p['request']['empirical_target']=='A' and support(r)==[(18,29)]
 assert r['request_hash']==p['acceptance']['request_hash']
 assert p['consumer_values']==[]

def test_no_person_or_selection_probability_is_invented(execution):
 for p in execution['packets'].values():
  for c in p['consumer_values']:
   m=c['consumer_material']
   if m['consumer']=='NONPARENT_OPTIONS':assert m['route_probability'] is None
   else:
    assert not m['person_generation'] and not m['actual_conception']
    assert all(x['selection_weight'] is None for x in m['scenarios'])

def test_actual_native_trace_and_git_preimages(execution):
 trace=execution['native_trace'];functions={x['function'] for x in trace['actual_entries'] if x['count']>0}
 assert {'ingest_c11_source_release','execute_empirical_query','provide_empirical_possibility_slice','compose_positioned_subject_possibility','evaluate_positioned_subject_possibility','resolve_v558','materialize_resolved_structural_context','validate_resolved_structural_context','read_historical_test_only','consume','evaluate'}.issubset(functions)
 assert trace['same_concrete_C1_evidence_objects_into_F8']>0
 assert all(x['actual_physical_path_verified'] for x in trace['imports'])
 m=json.loads((R/'source_manifest.json').read_text())
 for x in m:
  b=(R/'runtime'/x['local']).read_bytes();assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==x['git_blob']

def test_off_not_installed_labels_and_actual_oc05_refusal(execution):
 for p in execution['packets'].values():
  assert p['status']=='SOURCEFREE_OFF_NOT_INSTALLED'
  assert not any(p['boundary'].values())
 assert execution['actual_OC05']['direct_refusal']['type']=='NotYetApplicableConsumer'
 for m in execution['actual_OC05']['manifest'].values():
  if 'OC05' in m['policy_id']:assert m['consumer_seam'] is None and m['current_applicability']=='NOT_YET_APPLICABLE'

def test_fresh_json_cli_uses_real_pipeline(execution):
 dest=R/'observations/cli_current.json'
 p=subprocess.run([sys.executable,str(R/'repro/demo.py'),'--request',str(R/'examples/request_current_test_clock.json'),'--output',str(dest)],cwd=R,capture_output=True,text=True)
 assert p.returncode==0,p.stderr
 packet=json.loads(dest.read_text());assert support(packet['selected_world_receipt'])==[(18,32),(10,16),(6,8)]
 assert len(packet['consumer_values'])==2
 assert dest.with_suffix('.md').read_text().find('18/32')>=0
 assert dest.with_suffix('.md').read_text().find('SOURCEFREE_OFF_NOT_INSTALLED')>=0
