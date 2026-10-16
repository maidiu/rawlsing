"""Independent row-oracle checks of proposal inputs; no semantic self-adoption."""
from pathlib import Path
import sys,json,hashlib,copy
import pytest
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'repro'))
O=json.loads((R/'frozen_oracle.json').read_text())
def load(p):return json.loads((R/p).read_text())
@pytest.mark.parametrize('profile',['BASELINE','R2_Y1','R1_Y0'])
@pytest.mark.parametrize('namespace',['PV2-ADULT-A','PV2-ADULT-B'])
@pytest.mark.parametrize('slot',['PAIR','B'])
def test_native_fact_counts_and_exact_role_order_match_independent_rows(profile,namespace,slot):
 d=load('evidence/generic/'+profile+'.json');p=next(x for x in d['proposal']['entries'] if x['namespace']==namespace and x['slot']==slot)
 joint=O['joint_XY'][profile if namespace.endswith('-A') else 'BASELINE']
 expected={key if slot=='PAIR' else key[::-1]:value for key,value in joint.items()}
 actual={''.join(x['cell']):x['raw_numerator_support'] for x in p['native_fact_cells']}
 assert actual==expected and p['raw_denominator_support']==2
 assert p['native_role_order']==(['X','Y'] if slot=='PAIR' else ['Y','X'])
 fact=next(x for x in d['trace']['I03'] if x['ref']==p['fact_ref'] and x['query_ref']==p['query_ref'])
 assert p['native_fact_cells']==fact['projection']['semantic_fields']['target_topology']['complete_cell_semantic_projection']
 assert fact['query']['semantic_fields']['target_refs']==p['native_item_refs']
 assert p['proposed_generic_relation']=='GENERIC_NATIVE_SEMANTICS_HOLD' and p['issuer_signature'] is None

@pytest.mark.parametrize('profile',['BASELINE','R2_Y1','R1_Y0'])
def test_full_original_custody_six_current_consumers_and_two_helds(profile):
 d=load('evidence/generic/'+profile+'.json');p=d['proposal'];assert len(p['entries'])==6 and len(p['held'])==2
 expected=json.loads(d['installed']['complete_expected'] if isinstance(d['installed']['complete_expected'],str) else json.dumps(d['installed']['complete_expected']))
 assert {x['expected_work_key'] for x in expected['records']}=={x['expected_work_key'] for x in p['entries']+p['held']}
 assert len({x['expected_work_key'] for x in p['entries']})==6
 assert all(x['hold']=='ORDERED_OWNER_NOT_ISSUED' for x in p['held'])
 assert len(d['current']['links'])==6 and all(x['current_decision']['grant']=='SOURCE_FREE_DEV' or 'SOURCE_FREE_DEV' in str(x['current_decision']) for x in p['entries'])
 assert sum(len(x['records']) for x in d['actual_receipts'])==6
 assert all(x['consumer_material']['roles']['CONDITIONER']['source_native_variable']=='Q86B' and x['consumer_material']['roles']['TARGET']['source_native_variable']=='Q86A' for x in d['report']['links'])
 for k in ['validate_c11_source_release','execute_empirical_query','execute_exact_bounded_discovery','run_integrated','produce_exact_conditional_support_profile']:assert d['trace']['call_counts'][k]>0

@pytest.mark.parametrize('profile',['R2_Y1','R1_Y0'])
def test_A_numerical_effect_changes_original_refs_while_B_is_bit_identical(profile):
 base=load('evidence/generic/BASELINE.json');d=load('evidence/generic/'+profile+'.json')
 for family in ['report','proposal']:
  field='links' if family=='report' else 'entries'
  for x in d[family][field]:
   ns=x['original_identity']['original']['respondent_namespace'] if family=='report' else x['namespace']
   key=x['original_expected_work_key'] if family=='report' else x['expected_work_key']
   if ns=='PV2-ADULT-B':assert x==next(y for y in base[family][field] if (y['original_expected_work_key'] if family=='report' else y['expected_work_key'])==key)
 for link in d['report']['links']:
  if link['original_identity']['original']['respondent_namespace']!='PV2-ADULT-A':continue
  slot=link['original_identity']['operation']['slot'];old=next(x for x in base['report']['links'] if x['original_identity']['original']['respondent_namespace']=='PV2-ADULT-A' and x['original_identity']['operation']['slot']==slot)
  assert link['producer_result_ref']!=old['producer_result_ref'] and link['consumer_ref']!=old['consumer_ref']
  if slot=='DISCOVERY':assert any(link['producer_result_ref'] in r['semantic_fields']['empirical_fact_refs'] and r['semantic_fields']['winning_predicate_ref']==next(f['projection']['semantic_fields']['condition_predicate_ref'] for f in d['trace']['I03'] if f['ref']==link['producer_result_ref'] and f['query_ref']==link['consumer_material']['producer_query_ref']) for v in d['trace']['I05'] for r in v['receipts'])

def test_withdrawal_current_denial_and_historical_proposal_preservation():
 d=load('evidence/generic/current_history.json');assert d['A_after']['entries']==[] and len(d['B_after']['entries'])==3
 assert d['B_before']==d['B_after'] and d['historical_proposal_unchanged'] and d['original_history_verified']
 assert d['generic_current']['claim']=='GENERIC_NATIVE_SEMANTICS_HOLD'

def test_real_native_missing_empty_risk_and_supported_zero_remain_distinct():
 d=load('evidence/generic/edge_cases.json');zero=d['empty_risk'];assert zero['fact']['typed_state']=='ZERO_SUPPORT' and zero['consumer']['typed_state']=='ZERO_SUPPORT'
 assert zero['fact']['semantic_fields']['raw_denominator_support']==0 and zero['consumer']['conditional_count_profile']==[]
 missing=d['missing'];assert missing['typed_state']!='SUPPORTED' or missing['semantic_fields']['raw_resolved_target_support']<missing['semantic_fields']['raw_denominator_support']
 p=next(x for x in load('evidence/generic/BASELINE.json')['proposal']['entries'] if x['slot']=='PAIR')
 assert any(x['raw_numerator_support']==0 and x['cell_state']=='OBSERVED_ZERO_IN_SUPPORTED_RISK_SET' for x in p['native_fact_cells'])

@pytest.mark.parametrize('mutation',['COUNT','ROLE','RISK','NAMESPACE','DOMAIN'])
def test_proposal_reader_refuses_forged_native_input_and_never_issues_generic_semantics(mutation):
 from generic_proposal import derive_entry
 d=load('evidence/generic/BASELINE.json');link=copy.deepcopy(d['report']['links'][0]);facts=copy.deepcopy(d['trace']['I03']);decision=d['current']['current_decisions'][link['original_identity']['original']['respondent_namespace']]
 if mutation=='COUNT':next(x for x in facts if x['ref']==link['producer_result_ref'])['projection']['semantic_fields']['raw_denominator_support']=999
 elif mutation=='ROLE':link['original_identity']['operation']['condition_order'].reverse()
 elif mutation=='RISK':link['consumer_material']['risk_set_ref']['content_hash']='f'*64
 elif mutation=='NAMESPACE':link['original_identity']['original']['respondent_namespace']='FOREIGN_HOUSEHOLD'
 else:next(x for x in facts if x['ref']==link['producer_result_ref'])['query']['semantic_fields']['target_arity_and_topology']['components'][0]['domain']=['0','1','MISSING_AS_ZERO']
 with pytest.raises(ValueError):derive_entry(link,facts,decision)
