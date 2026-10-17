"""Precommitted before WG0P4 source. No skip/xfail or automatic pass.
The separate versioned adapter must call the pinned candidate/owner; a missing
adapter is an explicit collection/runtime error, never method acceptance.
Transport evidence contracts are in precommitted_contract.py. Additional Phase B
checks may strengthen this frozen battery; they may not edit it retrospectively.
"""
import importlib,os,pytest
from precommitted_contract import *
@pytest.fixture(scope='module')
def adapter():
 name=os.environ.get('WG0L_PHASE_B_ADAPTER')
 if not name:raise RuntimeError('PHASE_B_NOT_AUTHORIZED_WITHOUT_PUBLISHED_CANDIDATE_READ_CUT_AND_VERSIONED_ADAPTER')
 a=importlib.import_module(name).Adapter(ORACLE)
 assert a.candidate_sha and len(a.candidate_sha)==40
 assert a.owner_source_hashes_verified and a.actual_imports_verified
 return a
@pytest.mark.parametrize('group,case',CASES,ids=[g+'/'+c for g,c in CASES])
def test_precommitted_hostile(adapter,group,case):
 e=adapter.execute_case(group,case)
 assert e['case']==case and e['group']==group and e['candidate_sha']==adapter.candidate_sha
 assert e['actual_command'] and e['physical_module_files'] and e['execution_evidence_path']
 # Acceptance is computed here from raw actual outcomes, never adapter's boolean verdict.
 if group=='custody':
  if case in ('same_key_collision','fact_projection_ref_hash','rehashed_changed_fact','immediate_restore_validation'):assert_refusal(e)
  else:assert e['original_fact_after']==e['original_fact_before'] and e['read_support_after']==e['read_support_before']
 elif group=='frontier':assert_refusal(e)
 elif group=='authority':assert_refusal(e)
 elif group=='native':
  if case=='missing9_not_substantive':
   assert e['missing9_substantive_events']==0 and e['cell9_numerator']==0
  elif case=='missing_observation':
   assert e['invented_observation_count']==0 and (e['typed_state'] in ('UNAVAILABLE','HELD','NONCOMPARABLE','ZERO_SUPPORT') or e['denominator']==e['independently_reconstructed_risk_denominator'])
  elif case=='zero_risk_vs_observed_zero':
   assert e['empty_state']=='ZERO_SUPPORT' and e['empty_denominator']==0
   assert e['observed_zero_state']=='OBSERVED_ZERO_IN_SUPPORTED_RISK_SET' and e['supported_denominator']==6
  else:assert_refusal(e)
 elif group=='binding':
  if case=='source_leaf_mutation':
   assert e['affected_counts_before']!=e['affected_counts_after'] and e['source_bytes_hash_before']!=e['source_bytes_hash_after']
   assert e['actual_fact_ref_before']!=e['actual_fact_ref_after']
  elif case=='W2_wave_identity':assert e['raw_waves']=={'REL-A-W2':'W2','REL-B-W2':'W2'}
  elif case=='unrelated_W2_exact_stability':assert e['W2_release_before']==e['W2_release_after'] and e['W2_values_before']==e['W2_values_after']
  else:assert_refusal(e)
 elif group=='conditional':
  if case=='ordinary_full_chain_yes1_no1_over2':assert_ordinary_conditional(e)
  elif case=='original25_unchanged':assert sorted(e['frontier'],key=lambda x:x['op_id'])==ORACLE['operations']
  elif case=='second_frontier_exact_no_drop':
   assert e['submitted_second_frontier']==e['independently_frozen_second_frontier'] and e['register_frozen_before_execution']
   assert e['equal_count_forgery_rejected'] and e['omission_rejected']
  else:assert_refusal(e)
 elif group=='cold':
  if case.endswith('_refuse'):assert_refusal(e)
  else:assert_cold(e)
