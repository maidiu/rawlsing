"""Explicit synthetic fixture custody. Never production positive authority.

The fixture issuer allowlist is hand-authored test setup, not authentication of
external people/events. Admission verifies the full sealed synthetic event.
"""
from dataclasses import dataclass, asdict
from copy import deepcopy
from datetime import datetime
import hashlib,json
FIXTURE_ID='WORKER_CANDIDATE_REGISTRY_FIXTURE'
FIXTURE_VERSION='2.0.0'
FIXTURE_GRAIN='SOURCEFREE_CANDIDATE_FIXTURE__NOT_ACCEPTED_AUTHORIZATION'
PRODUCTION_REGISTRY_UNTOUCHED=True

def canon(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False)
def digest(x):return hashlib.sha256(canon(x).encode()).hexdigest()
def event_digest(event):return digest({k:v for k,v in asdict(event).items() if k!='event_hash'})
def parse_time(value):
    t=datetime.fromisoformat(value.replace('Z','+00:00'))
    if t.tzinfo is None:raise ValueError('Timezone required')
    return t

@dataclass(frozen=True)
class CandidateRuleRegistration:
    rule_id:str
    rule_version:str
    rule_content_hash:str
    issuer_authority_id:str
    issuer_authority_version:str
    actor_scope:str
    temporal_scope:str
    effect_kinds:tuple
    target_owner_kind:str
    admission_state:str
    binding_digest:str=''

class CandidateRegistryFixture:
    def __init__(self):
        self._rules={};self._admissions=[];self._events={};self._evaluations={}
        self._integrity=digest(self._state())
    def _state(self):
        return dict(rules={k:asdict(v) for k,v in self._rules.items()},admissions=self._admissions,events=self._events,evaluations=self._evaluations)
    def verify(self):return self._integrity==digest(self._state())
    def _seal(self):self._integrity=digest(self._state())
    def checkpoint(self):
        if not self.verify():raise ValueError('REGISTRY_INTEGRITY_FAILURE')
        return deepcopy((self._rules,self._admissions,self._events,self._evaluations,self._integrity))
    def restore(self,snapshot):self._rules,self._admissions,self._events,self._evaluations,self._integrity=deepcopy(snapshot)
    def register(self,reg):
        from .can008_candidate_rule import build_default_binding,binding_digest
        expected=build_default_binding()
        if not self.verify():return {'status':'REFUSED','code':'REGISTRY_INTEGRITY_FAILURE'}
        if reg.admission_state!='CANDIDATE_ADMITTED_IN_FIXTURE':return {'status':'REFUSED','code':'REGISTRATION_NOT_ADMITTED'}
        # This candidate implements ONE fixed actor/time cell, not a generic issuer.
        if (reg.rule_id,reg.rule_version,reg.rule_content_hash,reg.actor_scope,reg.temporal_scope,tuple(reg.effect_kinds),reg.target_owner_kind,reg.issuer_authority_id,reg.issuer_authority_version,reg.binding_digest)!=(expected.rule_id,expected.rule_version,expected.rule_content_hash,expected.actor_scope,expected.temporal_scope,expected.effect_kinds,'CAN008_CURRENT','ISSUER_AUTH_CANDIDATE_FIXTURE','1',binding_digest(expected)):
            return {'status':'REFUSED','code':'REGISTRATION_BINDING_MISMATCH'}
        key=reg.rule_id+'@'+reg.rule_version
        if key in self._rules:return {'status':'REFUSED','code':'DUPLICATE_RULE_REGISTRATION'}
        self._rules[key]=reg
        receipt=dict(status='CANDIDATE_REGISTERED_IN_FIXTURE',rule_key=key,fixture_id=FIXTURE_ID,fixture_grain=FIXTURE_GRAIN,production_registry_mutated=False)
        self._admissions.append(deepcopy(receipt));self._seal();return receipt
    def lookup(self,rule_id,rule_version):
        return self._rules.get(rule_id+'@'+rule_version) if self.verify() else None
    def admit_event(self,event):
        if not self.verify():return {'status':'REFUSED','code':'REGISTRY_INTEGRITY_FAILURE'}
        code=validate_event(event)
        if code:return {'status':'REFUSED','code':code}
        if event.event_id in self._events:return {'status':'REFUSED','code':'BLOCK_DUPLICATE_EVENT_IDENTITY'}
        for p in event.causal_parent_event_ids:
            parent=self._events.get(p)
            if not parent:return {'status':'REFUSED','code':'MISSING_PARENT_EVENT'}
            if parse_time(parent['effective_causal_time'])>=parse_time(event.effective_causal_time):return {'status':'REFUSED','code':'BLOCK_REVERSE_CHRONOLOGY_CAUSAL_PARENT'}
        self._events[event.event_id]=deepcopy(asdict(event))
        rec=dict(kind='EVENT_IDENTITY',event_id=event.event_id,event_hash=event.event_hash,issuer_authority_id=event.issuer_authority_id,issuer_authority_version=event.issuer_authority_version,status='EVENT_IDENTITY_ADMITTED_IN_FIXTURE')
        self._admissions.append(rec);self._seal();return deepcopy(rec)
    def admit_event_identity(self,*args):return {'status':'REFUSED','code':'FULL_EVENT_REQUIRED'}
    def verify_event(self,event):return self.verify() and self._events.get(event.event_id)==asdict(event)
    def event(self,event_id):return deepcopy(self._events.get(event_id)) if self.verify() else None
    def remember_evaluation(self,content):
        key=digest(content);self._evaluations[key]=deepcopy(content);self._seal();return key
    def verify_evaluation(self,key,content):return self.verify() and self._evaluations.get(key)==content and digest(content)==key
    def ledger(self):return deepcopy(self._admissions)
    def as_dict(self):return dict(fixture_id=FIXTURE_ID,fixture_grain=FIXTURE_GRAIN,production_registry_untouched=True,registered_rules=list(self._rules),ledger=self.ledger())

def validate_event(event):
    if event is None:return 'MISSING_PARENT_EVENT'
    if event.admission_state!='ADMITTED':return 'BLOCK_UNADMITTED_EVENT'
    if event.event_kind!='EXTERNAL_RUNTIME_EVENT':return 'BLOCK_NON_OCCURRENCE_KIND'
    if event.derived_from_future_partition:return 'BLOCK_HIDDEN_FUTURE_LEAK'
    if event.reverse_chronology_flag:return 'BLOCK_REVERSE_CHRONOLOGY_CAUSAL_PARENT'
    if event.issuer_authority_id not in ('ISSUER_AUTH_WORLD_SCHED','ISSUER_AUTH_INSTITUTION') or event.issuer_authority_version!='1':return 'BLOCK_FORGED_OR_MISMATCHED_ISSUER'
    if not event.event_id or not event.event_hash:return 'MISSING_PARENT_EVENT'
    if event.actor_scope!='ACTOR_SYNTH_1':return 'BLOCK_WRONG_ACTOR_SCOPE'
    if event.world_ref!='W_SYNTH_1998' or event.world_as_of!='1998-10-03T16:00:00Z':return 'BLOCK_STALE_OR_MISMATCHED_WORLD_ASOF'
    try:
        t=parse_time(event.effective_causal_time)
        if not parse_time('1998-01-01T00:00:00Z')<=t<parse_time('2001-01-01T00:00:00Z'):return 'BLOCK_TIME_OUTSIDE_RULE_SCOPE'
    except (ValueError,TypeError,AttributeError):return 'BLOCK_TIME_OUTSIDE_RULE_SCOPE'
    if event.event_hash!=event_digest(event):return 'PARENT_EVENT_HASH_MISMATCH'
    if not isinstance(event.public_features,tuple) or any(not isinstance(x,str) or not x.strip() for x in event.public_features):return 'RESPONSE_EVENT_RECEIVABILITY_UNRESOLVED'
    return None
CANDIDATE_REGISTRY=CandidateRegistryFixture()
