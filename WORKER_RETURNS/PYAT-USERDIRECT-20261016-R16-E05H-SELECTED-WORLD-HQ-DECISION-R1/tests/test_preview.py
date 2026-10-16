from pathlib import Path
import json,hashlib,sys
import pytest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'repro'))
import bootstrap
from preview import read_preview,PreviewDisabled
from handoff import fixture_handoff
import e05_n9_selected_world_adapter as E
@pytest.fixture(scope='module')
def result():return json.loads((ROOT/'02_ACTUAL_OPT_IN_SOURCEFREE_CONSUMER_PREVIEW.json').read_text())
def r(d,label):return d['packets'][label]['packet']['selected_world_receipt']
def counts(x):return [(next(c['raw_numerator_support'] for c in s['cells'] if c['cell']=='1'),s['denominator']) for s in x['empirical_steps']]
def test_default_off_before_owner_access():
 with pytest.raises(PreviewDisabled):read_preview(None,{})
 with pytest.raises(PreviewDisabled):read_preview(None,{},enabled=1)
def test_actual_consumers_current_historical(result):
 a=r(result,'CURRENT_TEST_CLOCK');b=r(result,'HISTORICAL_AS_OF')
 assert [a['structural_values'][k]['value'] for k in ['training_access','exit_cost']]==[False,8]
 assert [b['structural_values'][k]['value'] for k in ['training_access','exit_cost']]==[True,2]
 assert a['consumers'][0]['consumer_material']['structural_routes']['training']['state']=='BLOCKED_BY_MODELED_RULE'
 assert b['consumers'][0]['consumer_material']['structural_routes']['training']['state']=='ELIGIBLE'
 assert a['consumers'][1]['consumer_material']['scenarios'][0]['feasibility']=='INFEASIBLE_MODELED_PREMISE'
 assert b['consumers'][1]['consumer_material']['scenarios'][0]['feasibility']=='FEASIBLE_MODELED_PREMISE'
def test_incremental_values_and_minority(result):
 a=r(result,'CURRENT_TEST_CLOCK');b=r(result,'EMPIRICAL_Y_CHANGED')
 assert counts(a)==[(18,32),(10,16),(6,8)] and counts(b)==[(19,32),(11,16),(7,8)]
 assert [next(c['raw_numerator_support'] for c in s['cells'] if c['cell']=='0') for s in a['empirical_steps']]==[14,6,2]
 for x,y in zip(a['consumers'],b['consumers']):
  assert x['consumer_material']['empirical']['steps']!=y['consumer_material']['empirical']['steps']
  assert x['consumer_material']['snapshot_ref']==a['snapshot_hash']
 assert a['structural_values']==b['structural_values'] and a['native_field_readset']==b['native_field_readset']
def test_separate_reverse_request(result):
 p=result['reverse_separate_grant'];assert p['request']['empirical_target']=='A'
 assert counts(p['selected_world_receipt'])==[(18,29)] and p['consumer_values']==[]
 assert p['acceptance']['request_hash']==p['selected_world_receipt']['request_hash']
def test_native_units_custody_and_no_invented_persons(result):
 p=result['packets']['CURRENT_TEST_CLOCK']['packet'];a=p['selected_world_receipt'];v={x['role']:x for x in a['native_field_readset']['values_read']};g=v['GSS_RURAL_LIGHTING'];n=v['NCA_NATIONAL_MOBILE_DATA']
 assert (g['values']['numerator'],g['values']['denominator'])==(2388192,3288063)
 assert sum(g['values']['electricity_subtypes'].values())==2388192
 assert n['values']['active_subscriptions']==23414527
 assert g['native_unit']!=n['native_unit'] and g['native_geography']!=n['native_geography']
 assert not a['pooling'] and not a['person_exposure'] and not a['issued_EE13']
 assert all(c['fixture_only'] and c['source_pdf_sha256'] is None and c['issuer_ref'] is None and c['uncertainty'] for c in p['native_accepted_custody'].values())
 for x in a['consumers']:
  m=x['consumer_material']
  if m['consumer']=='NONPARENT_OPTIONS':assert m['route_probability'] is None
  else:assert not m['person_generation'] and all(s['selection_weight'] is None for s in m['scenarios'])
@pytest.mark.parametrize('role',['GSS_RURAL_LIGHTING','NCA_NATIONAL_MOBILE_DATA'])
@pytest.mark.parametrize('change',['revoke','rekey'])
def test_selective_current_grant_and_archive(result,role,change):
 x=result['selective_current_grant_changes'][role+'_'+change];a=x['before']['packet']['selected_world_receipt'];b=x['after']['packet']['selected_world_receipt']
 assert b['state']=='TYPED_PARTIAL_SELECTED_WORLD'
 assert [v for v in a['native_field_readset']['values_read'] if v['role']!=role]==b['native_field_readset']['values_read']
 for key in ['structural_values','empirical_steps','consumers','acceptance_hash']:assert a[key]==b[key]
 assert len(b['native_field_readset']['dependency_readset'])==2
 assert x['archival']['archival_only'] and not x['archival']['fresh_use_authorized']
 assert not x['archival']['retained']['fresh_use_authorized']
def test_publication_asof_denial(result):
 a=r(result,'TYPED_PARTIAL_PRE_NCA_PUBLICATION')
 assert a['native_field_readset']['refusals']
 assert 'NCA_NATIONAL_MOBILE_DATA' not in [v['role'] for v in a['native_field_readset']['values_read']]
 assert result['packets']['CURRENT_TEST_CLOCK']['packet']['acceptance']['request_hash']!=result['packets']['TYPED_PARTIAL_PRE_NCA_PUBLICATION']['packet']['acceptance']['request_hash']
def test_zero_support_downstream_terminal(result):
 a=r(result,'ZERO_SUPPORT');assert [x['denominator'] for x in a['empirical_steps']]==[24,8,0]
 s=a['empirical_steps'][-1];assert s['state']=='ZERO_SUPPORT' and s['cells']==[] and s['geometry'] is None and s.get('evidence_ref') is None
 assert len(a['native_field_readset']['values_read'])==2
 assert all('PARTIAL' in x['state'] for x in a['consumers'])
def test_oc05_no_installation(result):
 assert result['actual_oc05']['direct_refusal']['type']=='NotYetApplicableConsumer'
 for x in result['actual_oc05']['manifest']:
  if 'OC05' in x['policy_id']:assert x['consumer_seam'] is None and x['current_applicability']=='NOT_YET_APPLICABLE'
 assert all(not x['installed'] and not x['default_enabled'] for x in result['packets'].values())
def test_native_execution_and_exact_sources(result):
 t=result['native_trace'];names={x['function'] for x in t['actual_entries'] if x['count']}
 assert {'consume','evaluate','execute_empirical_query','compose_positioned_subject_possibility','evaluate_positioned_subject_possibility','read_historical_test_only'}.issubset(names)
 assert t['same_concrete_C1_evidence_objects_into_F8']>0
 for x in json.loads((ROOT/'native_source_manifest.json').read_text()):
  b=(ROOT/'inherited_e05a/runtime'/x['local']).read_bytes();assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==x['git_blob']
 for x in json.loads((ROOT/'source_manifest.json').read_text()):
  b=(ROOT/x['local']).read_bytes();assert hashlib.sha256(b).hexdigest()==x['sha256']
def test_weak_null_products_match_actual_source(result):
 from rawlsing_next.pre553_n9_n10w_progressive_candidate import synthetic_world_rows
 data=synthetic_world_rows();assert len(data)==58
 for a in result['weak_null_branches'].values():
  for s in a['empirical_steps']:
   selected=[x for x in data if all(x['responses'][k]==v for k,v in s['conditioners'])]
   assert s['denominator']==len(selected)
   assert {c['cell']:c['raw_numerator_support'] for c in s['cells']}=={str(v):sum(x['responses']['Y']==v for x in selected) for v in [0,1]}

def test_fresh_request_substitution_and_revoked_world():
 rows=json.loads((bootstrap.RT/'WORKER_RETURNS/PYAT-R3-HQ297-N9-TWO-FIELD-VALUES-READER-R1/02_TWO_FIELD_TESTONLY_READER_AND_ASOF.json').read_text())['fields']
 h=fixture_handoff(rows);q=E.standard_request(label='CURRENT_TEST_CLOCK').binding();p=h.prepare(q)
 other=E.standard_request(label='HISTORICAL_AS_OF').binding()
 with pytest.raises(ValueError,match='REQUEST_BINDING'):read_preview(h,other,enabled=True,prepared=p)
 h.adapter.invalidate('training_access')
 out=read_preview(h,q,enabled=True,prepared=p)['packet']['selected_world_receipt']
 assert out['state']=='TYPED_PARTIAL_SELECTED_WORLD'
 assert out['structural_values']['training_access']['state']=='REVOKED'
 assert 'value' not in out['structural_values']['training_access']

def test_archive_is_not_fresh_acceptance():
 rows=json.loads((bootstrap.RT/'WORKER_RETURNS/PYAT-R3-HQ297-N9-TWO-FIELD-VALUES-READER-R1/02_TWO_FIELD_TESTONLY_READER_AND_ASOF.json').read_text())['fields']
 h=fixture_handoff(rows);q=E.standard_request(label='CURRENT_TEST_CLOCK').binding();p=h.prepare(q);out=h.serve(p);archive=h.archive(out)
 assert not archive['fresh_use_authorized']
 fresh=fixture_handoff(rows)
 with pytest.raises(E.N9SelectedWorldRefusal,match='ACCEPTANCE_BINDING_MISMATCH'):
  fresh.adapter.serve(p.request,p.acceptance,p.snapshot)
