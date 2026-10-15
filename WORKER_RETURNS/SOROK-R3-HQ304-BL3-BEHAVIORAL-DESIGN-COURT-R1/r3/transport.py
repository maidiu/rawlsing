"""Closed local synthetic transport; no provider adapter or operative grant path."""
import hashlib,hmac,json,secrets
from .policies import POLICIES,respond
class Denied(ValueError):pass
def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':')).encode()
class MockIssuer:
 def __init__(self):self._key=secrets.token_bytes(32)
 def issue(self,freeze,policy,n):
  body=dict(mode='MOCK_ONLY',freeze=freeze,policy=policy,max_dispatches=n,named_provider_exact_endpoint='local://BL3-SYNTHETIC',exact_model_and_version_pin='SCRIPTED_POLICY_R3@1.0.0',privacy_permission_for_synthetic_lab_packets='TEST_ONLY_LOCAL',experiment_use_grant_behavioral_actor_trials='NO_REAL_TRIALS',explicit_monetary_cap=0,price_class_and_quota_observed='NO_EXTERNAL_CALL',raw_request_response_retention_permission='LOCAL_SYNTHETIC_ONLY',per_trial_call_budget=1)
  return dict(body=body,signature=hmac.new(self._key,canonical(body),hashlib.sha256).hexdigest())
class MockTransport:
 def __init__(self,grant,issuer,freeze,policy,planned,*,mode='MOCK_ONLY',provider_adapter=None):
  self.dispatches=0;self.external_dispatches=0;self.seen=set();self.policy=policy
  if mode!='MOCK_ONLY' or provider_adapter is not None:raise Denied('LIVE_PROVIDER_ADAPTER_UNCONDITIONALLY_DENIED')
  if type(issuer) is not MockIssuer or type(grant) is not dict or type(policy) is not str or policy not in POLICIES:raise Denied('UNISSUED_OR_UNREGISTERED')
  from .data import verify_freeze,load_schedule,load_cases,DerivedCache
  if freeze!=verify_freeze():raise Denied('FREEZE_BINDING')
  actual={r['id']:r for r in load_schedule()}
  if any(actual.get(r['id'])!=r for r in planned):raise Denied('UNPLANNED_ROW')
  b=grant.get('body',{});expected=issuer.issue(freeze,policy,len(planned))
  if b!=expected['body'] or not hmac.compare_digest(str(grant.get('signature','')),expected['signature']):raise Denied('MOCK_SCOPE_OR_SIGNATURE')
  if type(b['max_dispatches']) is not int or b['max_dispatches']<1:raise Denied('MOCK_BUDGET')
  self.planned={r['id']:r for r in planned};self.limit=b['max_dispatches'];self.cases={c['id']:c for c in load_cases()};self.cache=DerivedCache()
  if len(self.planned)!=len(planned):raise Denied('DUPLICATE_PLANNED_ROW')
 def call(self,row,payload):
  from .data import packet
  if row['id'] not in self.planned or self.planned[row['id']]!=row:raise Denied('FROZEN_REQUEST_MISMATCH')
  expected_payload=packet(self.cases[row['case']],row,self.cache)[0]
  if payload!=expected_payload:raise Denied('FROZEN_REQUEST_MISMATCH')
  if row['id'] in self.seen or self.dispatches>=self.limit:raise Denied('REPLAY_OR_BUDGET')
  self.seen.add(row['id']);position=self.dispatches;self.dispatches+=1
  return respond(payload,self.policy,dispatch_position=position)
