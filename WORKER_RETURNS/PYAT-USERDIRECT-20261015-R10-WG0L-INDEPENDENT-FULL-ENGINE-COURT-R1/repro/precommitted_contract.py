"""Candidate-neutral, frozen expected science. A Phase B adapter only transports
actual calls/payloads; it may not produce its own pass/fail classifications."""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
ORACLE=json.loads((R/'01_FROZEN_EXPECTATIONS_BEFORE_WG0P4.json').read_text())
CASES=[(group,case) for group,cases in ORACLE['hostiles'].items() for case in cases]
OP='OP-WG0P-ORD-01-MARGINAL'
def assert_refusal(result):
 assert result['attempted'] is True
 assert result['exception_type'] is not None or (result['typed_state'] in ('HELD','INADMISSIBLE','UNAVAILABLE','REVOKED','REFUSED','STALE','ZERO_SUPPORT') and not result['served_positive'])
 assert not result['served_positive']
def assert_native_values(e):
 for op,key in [(OP,'ORD01'),('OP-WG0P-ORD-05-MARGINAL','ORD05')]:
  fact=e[op][0];expected=ORACLE['source_native_values'][key]
  assert fact['denominator']==expected['denominator']
  assert {c['cell']:c['n'] for c in fact['cells']}==expected['counts']
 fact=e['OP-WG0P-HH-MR-02-MARGINAL'][0]
 assert fact['denominator']==4
 profiles={tuple(c['cell']):c['n'] for c in fact['cells'] if c['n']}
 assert profiles=={('yes','yes','no','no','no'):1,('no','yes','yes','no','no'):1,('yes','no','yes','yes','no'):1,('no','no','no','no','yes'):1}
def assert_cold(e):
 assert e['checkpoint_exit']==23 and e['first_pid']!=e['second_pid']
 assert e['first_I03_calls']==1 and e['second_I03_calls']==2
 assert e['manifest_before']==e['manifest_after'] and e['manifest_units']==3
 assert e['original_receipt_hash'] in e['final_receipt_hashes'] and len(e['final_receipt_hashes'])==3
 assert e['owner_receipt_class']=='rawlsing_next.pre553_batch_runner.UnitExecutionReceipt'
 assert e['fsync_file'] and e['fsync_directory'] and e['atomic_replace']
 assert e['original_receipt_preimage_verified'] and e['all_original_results_resolved']
 assert len(e['frontier'])==25 and sorted(e['frontier'],key=lambda x:x['op_id'])==ORACLE['operations']
 assert_native_values(e['consumer'])
def assert_ordinary_conditional(e):
 assert e['route']==ORACLE['ordinary_conditional_case']['required_path']
 assert e['separate_demo_function_called'] is False
 assert e['denominator']==2 and e['counts']=={'yes':1,'no':1}
 assert e['same_respondents']==['R2','R3']
 assert e['owner_query_calls']>=1 and e['owner_batch_calls']>=1
 assert e['second_frontier_verified_against_independent_register']
 assert sorted(e['original_frontier'],key=lambda x:x['op_id'])==ORACLE['operations']
