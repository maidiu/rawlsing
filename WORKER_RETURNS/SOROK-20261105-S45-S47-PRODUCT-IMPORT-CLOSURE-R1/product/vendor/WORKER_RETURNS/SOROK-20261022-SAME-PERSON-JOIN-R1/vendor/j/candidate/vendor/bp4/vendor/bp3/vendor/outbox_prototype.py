"""Candidate source-free occurrence/outbox repair. NOT an ADP019 implementation.

A missing optional field in a legacy S01-S28 fixture receives only a *marked*
source-free compatibility grant. Explicit None/empty authority is refused.
A strict envelope requires an externally supplied capability decision; token-shaped
strings and narrative content never grant world/actor/renderer authority.
"""
from __future__ import annotations
import copy, hashlib, json, os, tempfile, re
from datetime import datetime
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Optional

class OccurrenceState(str, Enum):
    CANDIDATE="CANDIDATE"; ADMITTED="ADMITTED"; EMITTED="EMITTED"; DELIVERED="DELIVERED"; PERCEIVED="PERCEIVED"
class DeliveryState(str, Enum):
    NOT_SENT="NOT_SENT"; ADMITTED_UNDELIVERED="ADMITTED_UNDELIVERED"; DELIVERED_UNACKED="DELIVERED_UNACKED"; ACKNOWLEDGED="ACKNOWLEDGED"; FAILED="FAILED"

_MISSING=object()
# The keys below are issuer/owner results, not candidate proposals.  Neither
# an injected boolean decider nor a payload-supplied field can issue them.
_FORBIDDEN_PROPOSAL_KEYS=frozenset({
    'admit','admitted','admitted_event_id','occurrence_id','event_id',
    'event_cursor','cursor_after','cursor_before','admitted_cursor',
    'state_delta','final_state','effect_result','effect_state','effect_delta',
    'memory_delta','memory_update','actor_memory_update','world_owner',
    'material_effect','physical_transition','objective_employment_transition',
    'client_perceived','human_perceived','perception_receipt',
})

_FORBIDDEN_COLLAPSED=frozenset(re.sub(r'[^a-z0-9]','',k.lower()) for k in _FORBIDDEN_PROPOSAL_KEYS)

def _normalized_directive(k):
    if not isinstance(k,str):return False
    compact=re.sub(r'[^a-z0-9]','',k.lower())
    # Lowercase, uppercase, PascalCase and separator variants must not turn
    # executable owner-output directives into accepted proposal input.
    return compact in _FORBIDDEN_COLLAPSED or compact.startswith('objective')

def _unlicensed_fields(mapping):
    # Only *keys*, not narrative word values, can pose as executable directives.
    if isinstance(mapping,list):return any(_unlicensed_fields(v) for v in mapping)
    if not isinstance(mapping,dict):return False
    return any(_normalized_directive(k)
               or _unlicensed_fields(v) for k,v in mapping.items())

def _canonical(data):
    return json.dumps(data,sort_keys=True,separators=(',', ':'),ensure_ascii=False,allow_nan=False)
def _hash(data):
    return hashlib.sha256(_canonical(data).encode('utf8')).hexdigest()
def _safe_copy(value):
    try: return json.loads(_canonical(value))
    except (ValueError,TypeError,OverflowError): return None

@dataclass
class OccurrenceLedger:
    _events: list[dict]=field(default_factory=list)
    _by_id: dict[str,dict]=field(default_factory=dict)
    admission_decider: Optional[Callable[[dict],bool]]=None
    last_refusal: Optional[str]=None
    @property
    def events(self): return copy.deepcopy(self._events)
    def count(self): return len(self._events)
    def get(self,occurrence_id):
        return next((copy.deepcopy(e) for e in self._events if e['occurrence_id']==occurrence_id),None)
    def admit(self,candidate):
        self.last_refusal=None
        if not isinstance(candidate,dict) or not isinstance(candidate.get('candidate_id'),str) or not candidate['candidate_id']:
            self.last_refusal='MISSING_CANDIDATE_ID';return None
        if not isinstance(candidate.get('payload',{}),dict):
            self.last_refusal='INVALID_PAYLOAD';return None
        try: immutable=_safe_copy(candidate)
        except Exception: immutable=None
        if immutable is None:
            self.last_refusal='INVALID_CANONICAL_BYTES';return None
        p=immutable.get('payload',{})
        if _unlicensed_fields(p) or _unlicensed_fields(immutable):
            self.last_refusal='UNLICENSED_AUTHORITY_DIRECTIVE';return None
        if 'envelope_mode' in immutable and immutable['envelope_mode']!='STRICT':
            self.last_refusal='UNKNOWN_ENVELOPE_MODE';return None
        # The minimal S01-S28 fixture is preserved; an owner-shaped envelope
        # cannot obtain legacy privilege merely by dropping its mode marker.
        _authority_shape={'issuer_ref','authority_ref','release_ref','artifact_id',
                          'artifact_digest','participant_refs','parent_refs'}
        if 'envelope_mode' not in immutable and _authority_shape.intersection(immutable):
            self.last_refusal='MISSING_STRICT_ENVELOPE_MODE';return None
        explicit_source='source_refs' in immutable
        source_refs=immutable.get('source_refs',['SOURCEFREE_FIXTURE_ONLY'])
        if not isinstance(source_refs,list) or not source_refs or not all(isinstance(x,str) and bool(x.strip()) for x in source_refs):
            self.last_refusal='MISSING_SOURCE_AUTHORITY';return None
        explicit_time='causal_time' in immutable
        causal_time=immutable.get('causal_time','SOURCEFREE_FIXTURE_UNDATED')
        if causal_time is None or causal_time=='' or isinstance(causal_time,(list,dict)):
            self.last_refusal='DEFER_MISSING_CAUSAL_TIME';return None
        # Check reference shapes before dereferencing them (never TypeError as
        # a surrogate for admission refusal).
        for ref_name in ('participant_refs','parent_refs'):
            if ref_name in immutable and (not isinstance(immutable[ref_name],list) or
               not all(isinstance(x,str) and bool(x.strip()) for x in immutable[ref_name])):
                self.last_refusal='INVALID_'+ref_name.upper();return None
        # Only a fully bound envelope can invoke an injected adjudicator.
        strict=immutable.get('envelope_mode')=='STRICT' 
        if strict:
            try:
                datetime.fromisoformat(causal_time)
            except (ValueError,TypeError):
                self.last_refusal='INVALID_TYPED_CAUSAL_TIME';return None
            for parent_id in immutable.get('parent_refs',[]):
                parent=self.get(parent_id)
                if not parent:
                    self.last_refusal='PARENT_EVENT_NOT_ADMITTED';return None
                try:
                    if datetime.fromisoformat(parent['causal_time'])>datetime.fromisoformat(causal_time):
                        self.last_refusal='CAUSAL_TIME_PRECEDES_PARENT';return None
                except (ValueError,TypeError):
                    self.last_refusal='UNCOMPARABLE_PARENT_CAUSAL_TIME';return None
            required=['artifact_id','artifact_digest','issuer_ref','authority_ref','release_ref','participant_refs','parent_refs','candidate_id','causal_time','source_refs']
            if any(k not in immutable or immutable[k] in (None,'') for k in required):
                self.last_refusal='INCOMPLETE_AUTHORITY_ENVELOPE';return None
            if (not explicit_source or not explicit_time or not isinstance(immutable['participant_refs'],list)
                or not immutable['participant_refs'] or not isinstance(immutable['parent_refs'],list)):
                self.last_refusal='INCOMPLETE_AUTHORITY_ENVELOPE';return None
            if self.admission_decider is None or not self.admission_decider(copy.deepcopy(immutable)):
                self.last_refusal='NO_COMPETENT_ADMISSION_WITNESS';return None
            grade='SOURCEFREE_BOUND_DECIDER_NOT_OWNER'
        else:
            # Unqualified, source-free compatibility fixtures are NEVER issued as authority.
            grade='SOURCEFREE_LEGACY_FIXTURE_NO_OWNER_AUTHORITY'
            if explicit_source and any(x.strip()=='' for x in source_refs):
                self.last_refusal='INVALID_SOURCE_REF';return None
        # Bind every present proposal field, including opaque ADP019-lineage-shaped
        # metadata, without pretending that these fields confer ADP019 authority.
        # Exact normalized preimage accompanies the event for cold restore.
        identity=copy.deepcopy(immutable)
        identity['source_refs']=source_refs
        identity['causal_time']=causal_time
        identity['admission_grade']=grade
        digest=_hash(identity)
        existing=self._by_id.get(candidate['candidate_id'])
        if existing:
            if existing['identity_digest']==digest: return copy.deepcopy(existing)
            self.last_refusal='CANDIDATE_IDENTITY_CONFLICT';return None
        event={'occurrence_id':f'OCC-{len(self._events)+1:04d}', 'candidate_id':candidate['candidate_id'],
               'content_hash':_hash(p),'identity_digest':digest,'payload':p,'state':OccurrenceState.ADMITTED.value,
               'source_refs':source_refs,'causal_time':causal_time,'artifact_id':immutable.get('artifact_id'),
               'artifact_digest':immutable.get('artifact_digest'),'issuer_ref':immutable.get('issuer_ref'),
               'authority_ref':immutable.get('authority_ref'),'release_ref':immutable.get('release_ref'),
               'participant_refs':immutable.get('participant_refs',[]),'parent_refs':immutable.get('parent_refs',[]),
               'admission_grade':grade, 'identity_preimage':identity}
        self._events.append(copy.deepcopy(event));self._by_id[event['candidate_id']]=self._events[-1]
        return copy.deepcopy(event)
    def restore_events(self,events):
        proposed=copy.deepcopy(events)
        if not isinstance(proposed,list):raise ValueError('CORRUPT_EVENT_COLLECTION')
        registry={}
        for index,e in enumerate(proposed,start=1):
            if not isinstance(e,dict) or not isinstance(e.get('candidate_id'),str):raise ValueError('CORRUPT_EVENT_IDENTITY')
            if e['candidate_id'] in registry:raise ValueError('DUPLICATED_CANDIDATE_ID')
            if (e.get('occurrence_id')!=f'OCC-{index:04d}' or e.get('state')!='ADMITTED'
                    or e.get('content_hash')!=_hash(e.get('payload'))):
                raise ValueError('CORRUPT_EVENT_INTEGRITY')
            identity=e.get('identity_preimage')
            if not isinstance(identity,dict) or e.get('identity_digest')!=_hash(identity):
                raise ValueError('CORRUPT_EVENT_IDENTITY_DIGEST')
            for k in ('candidate_id','payload','source_refs','causal_time','artifact_id','artifact_digest',
                      'issuer_ref','authority_ref','release_ref','participant_refs','parent_refs','admission_grade'):
                want=identity.get(k)
                if k in ('participant_refs','parent_refs') and want is None:want=[]
                if e.get(k)!=want:raise ValueError('CORRUPT_EVENT_PREIMAGE_BINDING')
            if identity['admission_grade'] not in ('SOURCEFREE_BOUND_DECIDER_NOT_OWNER',
                     'SOURCEFREE_LEGACY_FIXTURE_NO_OWNER_AUTHORITY'):
                raise ValueError('UNKNOWN_ADMISSION_GRADE')
            if identity.get('envelope_mode') not in (None,'STRICT'):
                raise ValueError('UNKNOWN_ENVELOPE_MODE')
            if ((identity['admission_grade']=='SOURCEFREE_BOUND_DECIDER_NOT_OWNER') !=
                (identity.get('envelope_mode')=='STRICT')):
                raise ValueError('ADMISSION_GRADE_MODE_MISMATCH')
            if _unlicensed_fields(identity) or _unlicensed_fields(e.get('payload')):
                raise ValueError('FORGED_AUTHORITY_DIRECTIVE')
            registry[e['candidate_id']]=e
        self._events=proposed
        self._by_id=registry

@dataclass
class Outbox:
    deliveries: dict[str,dict]=field(default_factory=dict)
    ledger: Optional[OccurrenceLedger]=None
    viewers: dict[str,set[str]]=field(default_factory=dict)
    revoked_viewers: dict[str,set[str]]=field(default_factory=dict)
    client_deliveries: dict[str,dict]=field(default_factory=dict)
    projection: Optional['UserProjection']=field(default=None,repr=False)
    def authorize_viewer(self,occurrence_id,viewer_id):
        if (not self.ledger or not self.ledger.get(occurrence_id)
            or not isinstance(viewer_id,str) or not viewer_id.strip()
            or viewer_id in self.revoked_viewers.get(occurrence_id,set())):return False
        self.viewers.setdefault(occurrence_id,set()).add(viewer_id);return True
    def revoke_viewer(self,occurrence_id,viewer_id):
        allowed=self.viewers.get(occurrence_id,set())
        if viewer_id not in allowed:return False
        allowed.remove(viewer_id)
        self.revoked_viewers.setdefault(occurrence_id,set()).add(viewer_id)
        if self.projection:
            offered=self.projection.opportunity.get(viewer_id,[])
            self.projection.opportunity[viewer_id]=[eid for eid in offered if eid!=occurrence_id]
        # Historical receipt remains auditable, but it cannot authorize a new
        # send, ACK, user opportunity or perception after revocation.
        return True
    def emit_to(self,occurrence_id,viewer_id):
        if not self.ledger or not self.ledger.get(occurrence_id) or viewer_id not in self.viewers.get(occurrence_id,set()):return None
        key=durable_delivery_id(occurrence_id,viewer_id)
        # A client intent requires an admitted global outbox emission intent;
        # this is still fixture state, never a renderer/client delivery grant.
        if self.emit(occurrence_id,viewer_id=viewer_id)==DeliveryState.NOT_SENT:return None
        e=self.client_deliveries.setdefault(key,{'event_id':occurrence_id,'viewer_id':viewer_id,'delivery_id':key,'state':DeliveryState.NOT_SENT.value,'attempts':0,'ack_count':0,'last_attempt_id':None})
        if e['state'] in (DeliveryState.NOT_SENT.value,DeliveryState.FAILED.value):
            e['attempts']+=1;e['last_attempt_id']=durable_attempt_id(occurrence_id,viewer_id,e['attempts'])
            e['state']=DeliveryState.ADMITTED_UNDELIVERED.value
        return copy.deepcopy(e)
    def deliver_to(self,occurrence_id,viewer_id):
        if viewer_id not in self.viewers.get(occurrence_id,set()):return None
        e=self.client_deliveries.get(durable_delivery_id(occurrence_id,viewer_id))
        if not e:return None
        if e['state']==DeliveryState.ADMITTED_UNDELIVERED.value:e['state']=DeliveryState.DELIVERED_UNACKED.value
        return copy.deepcopy(e)
    def ack_to(self,occurrence_id,viewer_id):
        if viewer_id not in self.viewers.get(occurrence_id,set()):return None
        e=self.client_deliveries.get(durable_delivery_id(occurrence_id,viewer_id))
        if not e:return None
        if e['state']==DeliveryState.DELIVERED_UNACKED.value:e['state']=DeliveryState.ACKNOWLEDGED.value;e['ack_count']+=1
        return copy.deepcopy(e)
    def fail_to(self,occurrence_id,viewer_id):
        if viewer_id not in self.viewers.get(occurrence_id,set()):return None
        e=self.client_deliveries.get(durable_delivery_id(occurrence_id,viewer_id))
        if not e:return None
        # Acknowledgment is a terminal source-free receipt; a failure callback
        # cannot erase it or fabricate a second retry opportunity.
        if e['state'] in (DeliveryState.ADMITTED_UNDELIVERED.value,
                          DeliveryState.DELIVERED_UNACKED.value):
            e['state']=DeliveryState.FAILED.value
        return copy.deepcopy(e)
    def emit(self,occurrence_id,viewer_id=None):
        if self.ledger is None or self.ledger.get(occurrence_id) is None:return DeliveryState.NOT_SENT
        admitted=self.ledger.get(occurrence_id)
        if admitted['admission_grade']=='SOURCEFREE_BOUND_DECIDER_NOT_OWNER' and viewer_id is None:return DeliveryState.NOT_SENT
        if viewer_id is not None and viewer_id not in self.viewers.get(occurrence_id,set()):return DeliveryState.NOT_SENT
        # A formerly authorized sole viewer cannot be bypassed by retrying
        # through the no-viewer legacy scalar path after revocation.
        if self.revoked_viewers.get(occurrence_id) and not self.viewers.get(occurrence_id):
            return DeliveryState.NOT_SENT
        entry=self.deliveries.setdefault(occurrence_id,{'state':DeliveryState.NOT_SENT.value,'ack_count':0,'attempts':0})
        if entry['state'] in (DeliveryState.NOT_SENT.value,DeliveryState.FAILED.value):
            entry['state']=DeliveryState.ADMITTED_UNDELIVERED.value;entry['attempts']+=1
        return DeliveryState(entry['state'])
    def _aggregate_guard(self,eid,target):
        occurrence=self.ledger.get(eid) if self.ledger else None
        if not occurrence:return False
        # Original no-viewer legacy scalars are compatibility-only; never
        # interpret them as a client receipt or human perception.
        linked=self.viewers.get(eid,set())
        if occurrence['admission_grade']=='SOURCEFREE_LEGACY_FIXTURE_NO_OWNER_AUTHORITY' and not linked and not self.revoked_viewers.get(eid):
            return True
        if not linked:return False
        if target=='deliver':
            return any(d['state'] in (DeliveryState.DELIVERED_UNACKED.value,DeliveryState.ACKNOWLEDGED.value)
                  for d in self.client_deliveries.values() if d['event_id']==eid and d['viewer_id'] in linked
                  and self.projection and self.projection.has_opportunity(d['viewer_id'],eid))
        if target=='ack':
            return any(d['state']==DeliveryState.ACKNOWLEDGED.value
                  for d in self.client_deliveries.values() if d['event_id']==eid and d['viewer_id'] in linked
                  and self.projection and self.projection.has_opportunity(d['viewer_id'],eid))
        return False
    def deliver(self,occurrence_id):
        if not self._aggregate_guard(occurrence_id,'deliver'):
            return DeliveryState.NOT_SENT
        e=self.deliveries.get(occurrence_id)
        if e and e['state']==DeliveryState.ADMITTED_UNDELIVERED.value:e['state']=DeliveryState.DELIVERED_UNACKED.value
        return DeliveryState(e['state']) if e else DeliveryState.NOT_SENT
    def ack(self,occurrence_id):
        if not self._aggregate_guard(occurrence_id,'ack'):
            return DeliveryState.NOT_SENT
        e=self.deliveries.get(occurrence_id)
        if e and e['state']==DeliveryState.DELIVERED_UNACKED.value:e['state']=DeliveryState.ACKNOWLEDGED.value;e['ack_count']+=1
        return DeliveryState(e['state']) if e else DeliveryState.NOT_SENT
    def fail(self,occurrence_id):
        e=self.deliveries.get(occurrence_id)
        # FAILED cannot replace a terminal ACK, or manufacture a failed
        # attempt out of a never-sent delivery. The original ACK remains.
        if e and e['state'] in (DeliveryState.ADMITTED_UNDELIVERED.value,
                                 DeliveryState.DELIVERED_UNACKED.value):
            e['state']=DeliveryState.FAILED.value
        return DeliveryState(e['state']) if e else DeliveryState.NOT_SENT
    def retry(self,occurrence_id):
        e=self.deliveries.get(occurrence_id)
        if e and e['state']==DeliveryState.FAILED.value:
            admitted=self.ledger.get(occurrence_id) if self.ledger else None
            if not admitted:return DeliveryState.NOT_SENT
            linked=self.viewers.get(occurrence_id,set())
            # Refuse the global bypass when the last holder of delivery
            # opportunity has been revoked, even on legacy fixtures.
            if self.revoked_viewers.get(occurrence_id) and not linked:
                return DeliveryState.NOT_SENT
            if admitted['admission_grade']=='SOURCEFREE_BOUND_DECIDER_NOT_OWNER' and not linked:
                return DeliveryState.NOT_SENT
            e['state']=DeliveryState.ADMITTED_UNDELIVERED.value;e['attempts']+=1
        return DeliveryState(e['state']) if e else DeliveryState.NOT_SENT

@dataclass
class UserProjection:
    perceived:dict[str,list[str]]=field(default_factory=dict)
    opportunity:dict[str,list[str]]=field(default_factory=dict)
    ledger:Optional[OccurrenceLedger]=None
    outbox:Optional[Outbox]=None
    perception_decider:Optional[Callable[[str,str,Any],bool]]=None
    def offer(self,user_id,occurrence_id):
        if self.ledger is None or self.ledger.get(occurrence_id) is None:return False
        admitted=self.ledger.get(occurrence_id)
        if admitted['admission_grade']=='SOURCEFREE_BOUND_DECIDER_NOT_OWNER':
            if not self.outbox or user_id not in self.outbox.viewers.get(occurrence_id,set()):return False
            d=self.outbox.client_deliveries.get(durable_delivery_id(occurrence_id,user_id))
            if not d or d['state'] not in (DeliveryState.DELIVERED_UNACKED.value,DeliveryState.ACKNOWLEDGED.value):return False
        # Prototype offer creates prospective availability, not delivery/actual perception.
        self.opportunity.setdefault(user_id,[])
        if occurrence_id in self.opportunity[user_id]:return False
        self.opportunity[user_id].append(occurrence_id)
        return True
    def perceive(self,user_id,occurrence_id,*,perception_witness=None):
        # No actual human perception owner is imported in this source-free
        # prototype. User-supplied witnesses or callback True are not proof.
        return False
    def has_opportunity(self,user_id,occurrence_id):
        if occurrence_id not in self.opportunity.get(user_id,[]):return False
        e=self.ledger.get(occurrence_id) if self.ledger else None
        if e is None:return False
        if e['admission_grade']=='SOURCEFREE_BOUND_DECIDER_NOT_OWNER':
            if not self.outbox or user_id not in self.outbox.viewers.get(occurrence_id,set()):return False
            d=self.outbox.client_deliveries.get(durable_delivery_id(occurrence_id,user_id))
            if not d or d['state'] not in (DeliveryState.DELIVERED_UNACKED.value,DeliveryState.ACKNOWLEDGED.value):return False
        return True
    def has_perceived(self,user_id,occurrence_id):
        # This prototype has no imported perception witness owner. A mutable
        # fixture dict cannot mint one, even before journal validation.
        return False

@dataclass
class OutboxPrototype:
    ledger:OccurrenceLedger=field(default_factory=OccurrenceLedger)
    outbox:Outbox=field(default_factory=Outbox)
    projection:UserProjection=field(default_factory=UserProjection)
    world_state:dict=field(default_factory=dict)
    _snapshot:dict=field(default_factory=dict)
    def __post_init__(self):
        self.outbox.ledger=self.ledger;self.outbox.projection=self.projection
        self.projection.ledger=self.ledger;self.projection.outbox=self.outbox
    def snapshot(self):
        self._snapshot=copy.deepcopy({'ledger':self.ledger.events,'outbox':self.outbox.deliveries,
             'viewers':{k:sorted(v) for k,v in self.outbox.viewers.items()},
             'revoked_viewers':{k:sorted(v) for k,v in self.outbox.revoked_viewers.items()},'client_deliveries':self.outbox.client_deliveries,
             'perceived':self.projection.perceived,'opportunity':self.projection.opportunity,'world':self.world_state})
        return copy.deepcopy(self._snapshot)
    def restore(self,snap):
        # Validate on a detached instance: failed validation must not corrupt
        # a live ledger, delivery state, projection or synthetic world fixture.
        doc=copy.deepcopy(snap)
        if not isinstance(doc,dict):raise ValueError('BAD_SNAPSHOT_SHAPE')
        staged=make_prototype()
        staged.ledger.restore_events(doc.get('ledger',[]))
        staged.outbox.deliveries=doc.get('outbox',{})
        raw_viewers=doc.get('viewers',{})
        if not isinstance(raw_viewers,dict):raise ValueError('BAD_VIEWER_SHAPE')
        if any(not isinstance(v,list) or len(v)!=len(set(v)) for v in raw_viewers.values()):
            raise ValueError('BAD_VIEWER_SHAPE')
        staged.outbox.viewers={k:set(v) for k,v in raw_viewers.items()}
        raw_revoked=doc.get('revoked_viewers',{})
        if not isinstance(raw_revoked,dict) or any(not isinstance(v,list) or len(v)!=len(set(v)) for v in raw_revoked.values()):
            raise ValueError('BAD_REVOKED_VIEWER_SHAPE')
        staged.outbox.revoked_viewers={k:set(v) for k,v in raw_revoked.items()}
        staged.outbox.client_deliveries=doc.get('client_deliveries',{})
        staged.projection.perceived=doc.get('perceived',{})
        staged.projection.opportunity=doc.get('opportunity',{})
        staged.world_state=doc.get('world',{})
        staged.validate_state()
        self.ledger._events=staged.ledger._events
        self.ledger._by_id=staged.ledger._by_id
        self.outbox.deliveries=staged.outbox.deliveries
        self.outbox.viewers=staged.outbox.viewers
        self.outbox.revoked_viewers=staged.outbox.revoked_viewers
        self.outbox.client_deliveries=staged.outbox.client_deliveries
        self.projection.perceived=staged.projection.perceived
        self.projection.opportunity=staged.projection.opportunity
        self.world_state=staged.world_state
    def validate_state(self):
        self.ledger.restore_events(self.ledger.events)
        ids={e['occurrence_id'] for e in self.ledger.events}
        if not isinstance(self.outbox.deliveries,dict) or any(eid not in ids for eid in self.outbox.deliveries):
            raise ValueError('GHOST_OUTBOX_STATE')
        if not isinstance(self.outbox.viewers,dict):raise ValueError('BAD_VIEWER_SHAPE')
        for eid,users in self.outbox.viewers.items():
            if eid not in ids or not isinstance(users,set) or not all(isinstance(x,str) and x for x in users):
                raise ValueError('GHOST_VIEWER_AUTHORIZATION')
        if not isinstance(self.outbox.revoked_viewers,dict):raise ValueError('BAD_REVOKED_VIEWER_SHAPE')
        for eid,users in self.outbox.revoked_viewers.items():
            if (eid not in ids or not isinstance(users,set) or
                    not all(isinstance(x,str) and bool(x.strip()) for x in users) or
                    users.intersection(self.outbox.viewers.get(eid,set()))):
                raise ValueError('CORRUPT_REVOKED_VIEWER')
        # Counters are not free-floating authority tokens. A journal receipt
        # cannot claim negative attempts, ACK before delivery, or impossible
        # state/count transitions even when its unkeyed digest is recomputed.
        valid_states={s.value for s in DeliveryState}
        for eid,e in self.outbox.deliveries.items():
            if not isinstance(e,dict):raise ValueError('BAD_AGGREGATE_DELIVERY')
            n=e.get('attempts');ack=e.get('ack_count');state=e.get('state')
            if (type(n) is not int or n<0 or type(ack) is not int or ack not in (0,1)
                or state not in valid_states or (n==0)!=(state==DeliveryState.NOT_SENT.value)
                or (ack==1)!=(state==DeliveryState.ACKNOWLEDGED.value)):
                raise ValueError('BAD_AGGREGATE_DELIVERY_COUNTS')
        if not isinstance(self.outbox.client_deliveries,dict):raise ValueError('BAD_CLIENT_DELIVERY_SHAPE')
        for key,d in self.outbox.client_deliveries.items():
            if not isinstance(d,dict):raise ValueError('BAD_DELIVERY_SHAPE')
            eid=d.get('event_id');viewer=d.get('viewer_id')
            # Historical receipt may outlive permission revocation, but cannot
            # be exercised or assert opportunity once authorization is revoked.
            if eid not in ids or not isinstance(viewer,str) or key!=durable_delivery_id(eid,viewer):
                raise ValueError('GHOST_CLIENT_DELIVERY')
            # Existing revoked viewer receipts remain historical evidence; a
            # fabricated delivery for a never-authorized viewer does not.
            active=self.outbox.viewers.get(eid,set())
            revoked=self.outbox.revoked_viewers.get(eid,set())
            if viewer not in active and viewer not in revoked:
                raise ValueError('UNAUTHORIZED_CLIENT_DELIVERY')
            n=d.get('attempts');ack=d.get('ack_count');state=d.get('state')
            if (d.get('delivery_id')!=key or type(n) is not int or n<0 or type(ack) is not int or ack<0 or ack>1
                    or state not in valid_states or not viewer.strip()):
                raise ValueError('BAD_DELIVERY_IDENTITY')
            expected=durable_attempt_id(eid,viewer,n) if n else None
            if d.get('last_attempt_id')!=expected:
                raise ValueError('FORGED_LAST_ATTEMPT_ID')
            if (n==0 and state!=DeliveryState.NOT_SENT.value) or (n==0 and ack!=0):
                raise ValueError('INCONSISTENT_DELIVERY_STATE')
            if (ack==1)!=(state==DeliveryState.ACKNOWLEDGED.value) or (n>0 and state==DeliveryState.NOT_SENT.value):
                raise ValueError('INCONSISTENT_ACK_STATE')
            if eid not in self.outbox.deliveries:
                raise ValueError('CLIENT_WITHOUT_OUTBOX_INTENT')
            # OUT6 legacy fixtures allow a never-sent placeholder for an ACTIVE
            # authorized viewer, but a revoked viewer cannot have historical
            # delivery evidence with zero send attempts. A forged tombstone
            # must not grant an impossible past receipt. Legitimate prior
            # deliveries (attempts >= 1) survive revocation.
            if n == 0 and viewer in revoked:
                raise ValueError('FORGED_ZERO_ATTEMPT_CLIENT_HISTORY')
        for eid,aggregate in self.outbox.deliveries.items():
            # For any viewer-bound history, a global terminal transport ACK
            # must have at least one corresponding ACKed client receipt.
            # Revocation can remove current authorization, but cannot erase
            # genuine acknowledged historical receipts from this check.
            # No-viewer legacy fixture scalar ACK remains legacy-only pending
            # OUTP L1/L2 and A1/A2 competent-owner decisions; this condition
            # does NOT require projection opportunity or assert perception.
            admitted=self.ledger.get(eid)
            historical=self.outbox.viewers.get(eid,set()) | self.outbox.revoked_viewers.get(eid,set())
            strict=admitted and admitted['admission_grade']=='SOURCEFREE_BOUND_DECIDER_NOT_OWNER'
            if aggregate['state']==DeliveryState.ACKNOWLEDGED.value and (strict or historical):
                if not any(d['event_id']==eid and d['viewer_id'] in historical
                           and d['state']==DeliveryState.ACKNOWLEDGED.value
                           and d['ack_count']==1 and d['attempts']>=1
                           for d in self.outbox.client_deliveries.values()):
                    raise ValueError('FORGED_AGGREGATE_ACK_WITHOUT_CLIENT_RECEIPT')
        for name,projection in (('opportunity',self.projection.opportunity),('perceived',self.projection.perceived)):
            if not isinstance(projection,dict):raise ValueError('BAD_PROJECTION_SHAPE')
            for user,eids in projection.items():
                if not isinstance(user,str) or not isinstance(eids,list) or len(eids)!=len(set(eids)):
                    raise ValueError('BAD_PROJECTION_RECORD')
                for eid in eids:
                    if eid not in ids:raise ValueError('GHOST_PROJECTION_STATE')
                    if name=='perceived':raise ValueError('NO_PERCEPTION_OWNER')
                    e=self.ledger.get(eid)
                    if e['admission_grade']=='SOURCEFREE_BOUND_DECIDER_NOT_OWNER':
                        if user not in self.outbox.viewers.get(eid,set()):
                            raise ValueError('UNAUTHORIZED_VIEWER_OPPORTUNITY')
                        d=self.outbox.client_deliveries.get(durable_delivery_id(eid,user))
                        if not d or d['state'] not in (DeliveryState.DELIVERED_UNACKED.value,DeliveryState.ACKNOWLEDGED.value):
                            raise ValueError('UNWITNESSED_VIEWER_OPPORTUNITY')
        if not isinstance(self.world_state,dict):raise ValueError('BAD_WORLD_STATE_SHAPE')
        # world_state here remains the explicitly non-durable legacy fixture.

def make_prototype():return OutboxPrototype()

class Journal:
    """Single-writer source-free durability experiment; no accepted owner/cross-worker law.
    One snapshot includes *both* event and outbox intent; tmp write+fsync,
    atomic same-directory rename and directory fsync. No claim for exotic filesystems.
    """
    def __init__(self,path): self.path=Path(path)
    def recover(self):
        p=make_prototype()
        if self.path.exists():
            d=json.loads(self.path.read_text())
            if d.get('schema')!='OUTBOX_F2_JOURNAL_V2':raise ValueError('UNSUPPORTED_JOURNAL_SCHEMA')
            if _hash(d.get('state'))!=d.get('state_digest'):raise ValueError('BAD_JOURNAL_DIGEST')
            if not isinstance(d['state'],dict) or d['state'].get('world'):
                raise ValueError('WORLD_STATE_REQUIRES_EXTERNAL_OWNER')
            p.restore(d['state'])
        return p
    def commit(self,p,crash_boundary=None):
        if p.world_state:raise ValueError('WORLD_STATE_REQUIRES_EXTERNAL_OWNER')
        p.validate_state()
        state=p.snapshot();receipt={'schema':'OUTBOX_F2_JOURNAL_V2','state':state,'state_digest':_hash(state)}
        self.path.parent.mkdir(parents=True,exist_ok=True)
        fd,temp=tempfile.mkstemp(prefix='.outbox-pending-',dir=str(self.path.parent))
        try:
            with os.fdopen(fd,'w',encoding='utf8') as f:
                f.write(_canonical(receipt));f.flush();os.fsync(f.fileno())
            if crash_boundary=='BEFORE_RENAME':os._exit(79)
            os.replace(temp,self.path)
            dirfd=os.open(str(self.path.parent),os.O_RDONLY)
            try:os.fsync(dirfd)
            finally:os.close(dirfd)
            if crash_boundary=='AFTER_COMMIT':os._exit(79)
        finally:
            if os.path.exists(temp):os.unlink(temp)
    def admit_and_queue(self,candidate,viewer_id=None,crash_boundary=None):
        p=self.recover();event=p.ledger.admit(candidate)
        if event is None:return None,p.ledger.last_refusal
        eid=event['occurrence_id']
        if viewer_id is not None:
            if not p.outbox.authorize_viewer(eid,viewer_id):return None,'VIEWER_NOT_AUTHORIZED'
        state=p.outbox.emit(eid,viewer_id=viewer_id)
        if state==DeliveryState.NOT_SENT:return None,'EMISSION_REFUSED'
        if viewer_id is not None:
            if p.outbox.emit_to(eid,viewer_id) is None:return None,'CLIENT_INTENT_REFUSED'
        self.commit(p,crash_boundary=crash_boundary)
        return event,None

def durable_delivery_id(occurrence_id,viewer_id):
    return 'DEL-'+_hash([occurrence_id,viewer_id])[:20]

def durable_attempt_id(occurrence_id,viewer_id,attempt):
    return 'ATT-'+_hash([occurrence_id,viewer_id,attempt])[:20]
