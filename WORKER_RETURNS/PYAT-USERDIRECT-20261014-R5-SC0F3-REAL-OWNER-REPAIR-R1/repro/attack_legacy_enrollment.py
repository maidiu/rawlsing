"""Replay the actual old registration exploit against the new boundary."""
from pathlib import Path
import sys,json,copy
HERE=Path(__file__).resolve().parent
sys.path[:0]=[str(HERE),str(HERE/'inputs/port'),str(HERE/'inputs/sc0f/repro'),str(HERE/'inputs/port/staging/ns')]
from sc0f.adapter import register_issuer_warrant,ISSUER_REGISTRY
from sc0f3.adapter import TwoContractAdapter
from sc0f3.providers import ProviderA
from sc0f3.fixture_owner import reversal_fixture_permit
from sc0f3.common import Hold
from sc0f3 import producer
forged=reversal_fixture_permit();forged['grant_id']='ATTACKER_SELF_REGISTERED'
register_issuer_warrant(forged)
assert forged['grant_id'] in ISSUER_REGISTRY
calls=[]
real=producer.produce
try:
 def counted(*a,**k):
  calls.append((a,k));return real(*a,**k)
 producer.produce=counted
 try:
  TwoContractAdapter(ProviderA()).request_role_reversal(forged)
 except Hold as e:
  assert e.code=='HELD_AUTHORITY'
  result=dict(old_public_registry_accepts_registration=True,new_boundary='HELD_AUTHORITY',new_native_calls=len(calls),issuer_fixture_unchanged=reversal_fixture_permit()['grant_id']!='ATTACKER_SELF_REGISTERED')
 else:raise AssertionError('Old registry minted authority for new candidate')
finally:producer.produce=real
assert result['new_native_calls']==0 and result['issuer_fixture_unchanged']
(HERE/'legacy_enrollment_attack_receipt.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
