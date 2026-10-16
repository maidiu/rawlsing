"""Bounded new accession/handoff checks, not the completed PV3N court."""
import json,pathlib,sys,copy,hashlib
import pytest
R=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'repro'))
from method_receipt import verify,digest

def load(path):return json.loads((R/path).read_text())
BASE=load('evidence/handoff/first.json');REPLAY=load('evidence/handoff/replay.json');ORACLE=load('handoff_oracle.json')
KEYS=[(ns,slot) for ns in ['PV2-ADULT-A','PV2-ADULT-B'] for slot in ['PAIR','B','DISCOVERY']]

@pytest.mark.parametrize('namespace,slot',KEYS)
def test_exact_original_consumer_reaches_real_fact_query_unit_and_field_forge(namespace,slot):
 link=next(x for x in BASE['report']['links'] if x['original_identity']['original']['respondent_namespace']==namespace and x['original_identity']['operation']['slot']==slot);m=link['consumer_material'];o=link['original_identity']['original']
 assert o['respondent_unit']=='TEST_ONLY_ADULT' and o['language']=='PV2-LANGUAGE' and o['form']=='F1'
 assert m['roles']['CONDITIONER']['ref']==o['native_item_refs'][0] and m['roles']['TARGET']['ref']==o['native_item_refs'][1]
 assert m['producer_fact_ref']==link['producer_result_ref'];assert m['risk_set_ref'] and m['empirical_universe_refs'] and m['producer_provenance_refs']
 assert m['producer_permission_ceiling']==m['relation_permission_ceiling']==['SOURCE_FREE_DEV']
 fact=next(x for x in BASE['trace']['I03'] if x['ref']==link['producer_result_ref'] and x['query_ref']==m['producer_query_ref'])
 assert fact['projection']['semantic_fields']['risk_set_ref']==m['risk_set_ref']
 assert any(x['ref']==link['consumer_ref'] and x['material']==m for x in BASE['trace']['Field_Forge'])
 receipt=next(r for scope in BASE['original_receipts'] for r in scope['records'] if r['unit_key']==link['batch_unit_ref']['kind']+'|'+link['batch_unit_ref']['object_id']+'|'+link['batch_unit_ref']['content_hash'])
 assert receipt['actual_class']=='rawlsing_next.pre553_batch_runner.UnitExecutionReceipt'
 if slot=='DISCOVERY':
  winner=next(r['semantic_fields'] for event in BASE['trace']['I05'] for r in event['receipts'] if link['producer_result_ref'] in r['semantic_fields']['empirical_fact_refs'])
  assert winner['winning_predicate_ref']==fact['projection']['semantic_fields']['condition_predicate_ref']
 else:assert link['producer_result_ref'] in receipt['projection']['result_refs']

def test_complete_independent_expected_set_and_both_helds():
 receipt=BASE['method_receipt'];verify(receipt)
 assert receipt['expected_root']==ORACLE['original_expected_root'];assert receipt['register_root']==ORACLE['register_root']
 assert {x['expected_work_key'] for x in receipt['operations']}=={x['complete_exact_fixture_identity']['expected_work_key'] for x in ORACLE['inventory']}
 held=[x for x in receipt['operations'] if not x['source_free_positive']];assert len(held)==2
 assert all(x['exact_original_operation']['legacy']['slot']=='ORDERED' and x['hold']=='ORDERED_OWNER_NOT_ISSUED' for x in held)
 assert len({x['original_expected_work_key'] for x in BASE['report']['links']})==6
 assert len({x['legacy_expected_work_key'] for x in BASE['report']['links']})==3

@pytest.mark.parametrize('name',['R2_Y1','R1_Y0'])
def test_source_specific_joint_intervention_and_native_I05_custody(name):
 x=load('evidence/intervention_'+name+'.json');verify(x['method_receipt']);rows={}
 for c in x['source_cells']:
  data={}
  for cell in c['cells']:data.setdefault(cell['row'],{})[cell['item']]=cell['value']
  rows[c['namespace']]=data
 a=rows['PV2-ADULT-A'];joint={k:0 for k in ['00','01','10','11']}
 for i in [1,2]:joint[a[i]['X']+a[i]['Y']]+=1
 assert joint==ORACLE[name+'_joint'];assert a[3]['Y']=='1'  # original row exists; it is Y-ineligible
 for link in x['report']['links']:
  ns=link['original_identity']['original']['respondent_namespace'];slot=link['original_identity']['operation']['slot'];old=next(l for l in BASE['report']['links'] if l['original_identity']['original']['respondent_namespace']==ns and l['original_identity']['operation']['slot']==slot)
  if ns=='PV2-ADULT-B':assert link==old
  elif slot=='PAIR':
   profile={str(c['condition_state']):{str(t['target_state']):t['joint_support_count'] for t in c['target_counts']} for c in link['consumer_material']['conditional_count_profile']}
   assert profile=={str(v):{str(y):joint[str(v)+str(y)] for y in [0,1]} for v in [0,1]}
  if ns=='PV2-ADULT-A' and name=='R1_Y0' and slot=='DISCOVERY':
   assert link['producer_result_ref']!=old['producer_result_ref'];assert link['consumer_ref']!=old['consumer_ref']
   fact=next(f for f in x['trace']['I03'] if f['ref']==link['producer_result_ref']);assert any(link['producer_result_ref'] in r['semantic_fields']['empirical_fact_refs'] and r['semantic_fields']['winning_predicate_ref']==fact['projection']['semantic_fields']['condition_predicate_ref'] for e in x['trace']['I05'] for r in e['receipts'])
 assert x['method_receipt']['counts']['legacy_keys']==6  # source A has a new edition; no identity collapse

def test_true_cold_restore_has_zero_new_jobs_and_nonzero_original_recomputation():
 summary=load('evidence/handoff/summary.json');assert summary['processes'][0]['exit']==-9;assert summary['first_pid']!=summary['replay_pid']
 assert summary['first_new_durable']==[3,3] and summary['replay_new_durable']==[0,0]
 assert BASE['method_receipt']==REPLAY['method_receipt'];assert BASE['original_receipts']==REPLAY['original_receipts']
 assert all(REPLAY['trace']['call_counts'][k]==v for k,v in ORACLE['cold']['actual_replay_recomputation'].items());assert summary['byte_identical_journals']

def test_current_A_withdrawal_B_invariance_archival_A_and_offline_hold():
 x=load('evidence/handoff/history_and_current.json');assert x['A_current']['servable'] is False and x['A_current']['links']==[]
 assert x['B_before']==x['B_current'];assert len(x['B_current']['links'])==len(x['archival_A'])==3
 assert x['original_history_verified'] and x['history_unchanged'] and x['method_receipt_unchanged']
 assert load('evidence/handoff/offline.json')['claim']=='OFFLINE_FACT_RESTORATION_HOLD'
 assert x['generic_current']['claim']=='GENERIC_NATIVE_SEMANTICS_HOLD'

def test_source_scope_risk_zero_support_and_observed_zero_are_distinct():
 for l in BASE['report']['links']:
  if l['original_identity']['operation']['slot']!='PAIR':continue
  cells=l['consumer_material']['conditional_count_profile'];assert all(x['condition_denominator_support']==1 for x in cells)
  counts=[x['joint_support_count'] for c in cells for x in c['target_counts']];assert sorted(counts)==[0,0,1,1]
 assert {x['public'][0]['semantic_fields']['respondent_namespace'] for x in BASE['trace']['C11']}=={'PV2-ADULT-A','PV2-ADULT-B'}
 # Retained original empty-risk proof is a prior independently accepted owner control.
 assert ORACLE['baseline_joint']=={'00':1,'01':0,'10':0,'11':1}
 empty=load('retained/PV3N_empty_risk_owner_consumer.json');assert empty['fact']['typed_state']=='ZERO_SUPPORT'
 assert empty['consumer']['typed_state']=='ZERO_SUPPORT' and empty['consumer']['conditional_count_profile']==[]

@pytest.mark.parametrize('field',['drop_held','probability','generic_label'])
def test_return_receipt_tampering_cannot_borrow_unchanged_digest(field):
 bad=copy.deepcopy(BASE['method_receipt'])
 if field=='drop_held':bad['operations']=[x for x in bad['operations'] if x['source_free_positive']]
 elif field=='probability':next(x for x in bad['operations'] if x['source_free_positive'])['link']['consumer_material']['person_probability']=1
 else:next(x for x in bad['operations'] if x['source_free_positive'])['link']['consumer_material']['roles']['CONDITIONER']['source_native_variable']='X'
 with pytest.raises(AssertionError):verify(bad)

def test_all_74_owner_blobs_still_exact_and_provenance_preserved():
 import hashlib
 for row in load('native_74_source_manifest.json')['files']:
  b=(R/'runtime/court/runtime_root'/row['staged_path']).read_bytes();assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==row['git_blob_sha1']
