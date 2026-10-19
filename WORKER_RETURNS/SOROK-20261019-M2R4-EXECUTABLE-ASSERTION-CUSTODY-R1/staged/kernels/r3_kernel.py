"""M2 sourcefree candidate: no real actor, memory, CAN/ADP grant, or psychometric authority."""
from __future__ import annotations
from dataclasses import dataclass, asdict, replace
from hashlib import sha256
import json

GRADE = 'TEST_ONLY_M1_SOURCE_TIME_REPAIR_CANDIDATE_PENDING_I2'
RULE = 'M2_INTERPRETATION_SOURCE_TEMPORAL_IDENTITY@0.4.1_CANDIDATE'
RULE_CONTRACT = {'name':RULE,'clock':'no_future_read','history':'independent_fixture_witness',
                 'speech':'actual_action_plus_listener_exposure','lineage':'objective_and_consumed_source_preimages',
                 'relation':'exact_consumed_relevance_history_and_witness',
                 'counterpart':'other_actor_action_owner_bound_to_observation_and_relevance',
                 'outcome':'candidate_only','no_change':'unchanged_psychology_separate_audit'}
MODES = ('REATTRIBUTE','NARROW','GENERALIZE','REINFORCE','CONTRADICT','DIFFERENTIATE','NO_CHANGE')
STANCES = ('ACCEPT','REJECT','SUSPEND')
TEST_HISTORY_ISSUER = 'M2_TEST_ONLY_INDEPENDENT_HISTORY_REGISTRY'
TEST_SPEECH_ISSUER = 'M2_TEST_ONLY_SPEECH_ACTION_AND_EXPOSURE_REGISTRY'
TEST_RELEVANCE_ISSUER = 'M2_TEST_ONLY_OBSERVED_RELATION_CONTRAST'
TEST_EVENT_ISSUER = 'TEST_ONLY_INDEPENDENT_WORLD_FIXTURE'

class Refusal(ValueError): pass

def canonical(o): return json.dumps(o, sort_keys=True, ensure_ascii=True, separators=(',', ':'),allow_nan=False)
def digest(o): return sha256(canonical(o).encode()).hexdigest()
RULE_HASH = digest(RULE_CONTRACT)
def require(ok, reason):
    if not ok: raise Refusal(reason)

@dataclass(frozen=True)
class History:
    id: str; actor: str; time: int; activity: str; witnessed: bool; accessible: bool
    observed_action_owner: str|None=None  # explicitly attributed person for observed-other actions

@dataclass(frozen=True)
class Actor:
    id: str; history: tuple[History,...]; access: tuple[str,...]; private_project: str
    age: int=12; background: str='unspecified'

@dataclass(frozen=True)
class WorldFact:
    """Typed world predicate; no culprit, ideology or speaker motive primitives."""
    kind: str; object_ref: str; value: str; source_ref: str; owner: str=TEST_EVENT_ISSUER

@dataclass(frozen=True)
class Event:
    id: str; kind: str; time: int; observer: str; participants: tuple[str,...]
    material: tuple[str|WorldFact,...]; issuer: str=TEST_EVENT_ISSUER
    action_owner: str|None=None; action: str|None=None
    parent_event_id: str|None=None; parent_event_hash: str|None=None

@dataclass(frozen=True)
class Speech:
    id: str; event: str; speaker: str; time: int; words: str; claim_ref: str

@dataclass(frozen=True)
class HistoryWitness:
    history_id: str; history_hash: str; actor: str; observer: str; time: int
    scope: str; operation: str; issuer: str=TEST_HISTORY_ISSUER

@dataclass(frozen=True)
class SpeechAction:
    speech_id: str; speech_hash: str; speaker: str; action_event_id: str
    action_event_hash: str; observer: str; time: int; issuer: str=TEST_SPEECH_ISSUER

@dataclass(frozen=True)
class Exposure:
    speech_id: str; speech_hash: str; listener: str; action_event_hash: str
    witness: str; heard_time: int; issuer: str=TEST_SPEECH_ISSUER

@dataclass(frozen=True)
class Relevance:
    later_event_id: str; later_event_hash: str; earlier_event_id: str
    earlier_event_hash: str; actor: str; observed_history_id: str
    observer: str; time: int; issuer: str=TEST_RELEVANCE_ISSUER
    observed_action_owner: str|None=None  # links this receipt to the event's actual action owner

@dataclass(frozen=True)
class Scene:
    actors: tuple[Actor,...]; events: tuple[Event,...]; speech: tuple[Speech,...]
    history_witnesses: tuple[HistoryWitness,...]=()
    speech_actions: tuple[SpeechAction,...]=()
    exposures: tuple[Exposure,...]=()
    relevance: tuple[Relevance,...]=()

@dataclass(frozen=True)
class Candidate:
    id: str; actor: str; event: str; source: str|None; mode: str
    stance: str; parent: str|None; rule_hash: str=RULE_HASH

@dataclass(frozen=True)
class Interpretation:
    actor: str; event: str; version: int; previous_hash: str|None
    candidate_hash: str; source: str|None; mode: str; belief_stance: str
    affect_ref: str|None; public_action_ref: str|None
    retained_procedure_refs: tuple[str,...]; actor_memory_access: str
    rule_hash: str; provenance_refs: tuple[str,...]
    event_hash: str; original_event_id: str; original_event_hash: str
    source_preimages: tuple[tuple[str,str,str], ...]
    hash: str

@dataclass(frozen=True)
class State:
    actor: str; lineage: tuple[Interpretation,...]=(); procedure_refs: tuple[str,...]=()
    def hash(self): return digest(asdict(self))
    def psychology_hash(self): return self.hash()  # no audit receipts in this durable state

@dataclass(frozen=True)
class NoChangeAudit:
    actor: str; event_hash: str; state_before_hash: str; candidate_hash: str
    grade: str; hash: str

# Legacy atomic identifiers must be from this bounded material grammar; arbitrary
# demographic/culprit/motive text cannot enter as objective material. New facts use WorldFact.
MATERIAL_ATOMS = frozenset(('bike','garage','loss_of_transport','community_hall',
    'loss_discussion','bicycle_found_undamaged','unrelated_work','speaker_action',
    'rehearsal_room','shared_task','repair_project','unrelated_recreation'))
WORLD_FACT_VALUES = {'OBJECT_LOCATION':frozenset(('GARAGE','HALL','SHOP')),
    'RESOURCE_STATUS':frozenset(('MISSING','FOUND','DAMAGED')),
    'ACTIVITY_CONTEXT':frozenset(('REPAIR','LOCKING','DISCUSSION','SHARED_TASK','UNRELATED_WORK')),
    'OBSERVED_ACTION':frozenset(('SECURE','DELIVER','HELP','REFUSE','CHECK'))}
WITNESS_OPERATIONS = frozenset(('RELATIONAL_RECOGNITION','PROCEDURAL_PRACTICE',
    'AFFECT_EXPRESSION','PUBLIC_ACTION','INDEPENDENT_PROJECT','INDEPENDENT_PRACTICE',
    'OBSERVED_RELATIONAL_DIFFERENCE'))

def actor(scene, who):
    for a in scene.actors:
        if a.id==who: return a
    raise Refusal('UNKNOWN_ACTOR')

def objective_event_hash(e): return digest(asdict(e))

def _history_source(scene, h, operation=None):
    found=[w for w in scene.history_witnesses if w.history_id==h.id and w.actor==h.actor]
    require(len(found)==1, 'HISTORY_WITNESS_SOURCE_UNVERIFIED')
    w=found[0]
    require(w.issuer==TEST_HISTORY_ISSUER and w.history_hash==digest(asdict(h))
            and w.time==h.time and w.observer!=h.actor
            and w.observer in {a.id for a in scene.actors}
            and w.operation in WITNESS_OPERATIONS and w.scope!='',
            'HISTORY_WITNESS_SOURCE_UNVERIFIED')
    if operation: require(w.operation==operation,'HISTORY_WITNESS_WRONG_OPERATION')
    return w

def _real_spoken_and_heard(scene, s, listener, now, evs):
    actions=[x for x in scene.speech_actions if x.speech_id==s.id]
    exposures=[x for x in scene.exposures if x.speech_id==s.id and x.listener==listener]
    require(len(actions)==1 and len(exposures)==1,'SPEAKER_ACTION_OR_ACCESS_UNVERIFIED')
    a,x=actions[0],exposures[0]
    event=evs.get(a.action_event_id)
    require(event is not None and event.kind=='ACTION' and event.action_owner==s.speaker
            and event.action=='SPEAK' and s.speaker in event.participants
            and listener in event.participants and event.observer==a.observer
            and a.observer!=s.speaker and a.observer in {v.id for v in scene.actors}
            and a.speech_hash==digest(asdict(s)) and a.action_event_hash==objective_event_hash(event)
            and a.time==event.time==s.time and a.speaker==s.speaker
            and x.issuer==a.issuer==TEST_SPEECH_ISSUER
            and x.speech_hash==a.speech_hash and x.action_event_hash==a.action_event_hash
            and x.witness!=s.speaker and x.witness in {v.id for v in scene.actors}
            and s.time <= x.heard_time <= now and s.time<=now,
            'SPEAKER_ACTION_OR_ACCESS_UNVERIFIED')
    return a,x

def validate(scene):
    ids=[x.id for x in scene.actors]
    require(len(ids)==len(set(ids)), 'ACTOR_ID_COLLISION')
    evs={x.id:x for x in scene.events}
    require(len(evs)==len(scene.events),'EVENT_ID_COLLISION')
    require(len({s.id for s in scene.speech})==len(scene.speech),'SPEECH_ID_COLLISION')
    history_ids=[]
    for a in scene.actors:
        require(a.private_project!='','ACTOR_PROJECT_MISSING')
        for h in a.history:
            require(h.actor==a.id and h.time>=0,'FOREIGN_ACTOR_HISTORY')
            history_ids.append((h.actor,h.id))
            if h.witnessed: _history_source(scene,h)
    require(len(history_ids)==len(set(history_ids)),'HISTORY_ID_COLLISION')
    for e in scene.events:
        require(e.issuer==TEST_EVENT_ISSUER,'UNOWNED_EVENT')
        require(e.observer in ids and all(x in ids for x in e.participants),'EVENT_ACTOR_UNBOUND')
        require(e.kind in ('LOSS','ACTION','PROCESS','ENCOUNTER'),'UNKNOWN_EVENT')
        for m in e.material:
            if isinstance(m,str):require(m in MATERIAL_ATOMS,'MORAL_FACT_IN_EVENT')
            elif isinstance(m,WorldFact):
                require(m.kind in WORLD_FACT_VALUES and m.value in WORLD_FACT_VALUES.get(m.kind,())
                        and m.owner==TEST_EVENT_ISSUER and m.object_ref and m.source_ref,
                        'MORAL_FACT_IN_EVENT')
            else: raise Refusal('MORAL_FACT_IN_EVENT')
        if e.kind=='PROCESS':
            parent=evs.get(e.parent_event_id)
            require(parent is not None and parent.time<e.time and parent.kind=='LOSS'
                    and e.parent_event_hash==objective_event_hash(parent),'PROCESSING_PARENT_INVALID')
        if e.action_owner:
            require(e.action_owner in e.participants and e.kind in ('ACTION','ENCOUNTER'),
                    'ACTION_OWNER_UNBOUND')
            if e.action!='SPEAK':
                a=actor(scene,e.action_owner)
                require(any(h.activity==a.private_project and h.time<e.time
                      and h.witnessed and _history_source(scene,h).operation=='INDEPENDENT_PROJECT'
                      for h in a.history),'INDEPENDENT_ACTION_HISTORY_REQUIRED')
    for s in scene.speech:
        require(s.event in evs and s.speaker in ids and s.time>=evs[s.event].time,'SPEECH_PARENT_INVALID')
        require(s.claim_ref and not s.claim_ref.startswith('objective:'),'ATTRIBUTION_LAUNDERED')
        require(any(a.speech_id==s.id for a in scene.speech_actions),
                'SPEAKER_ACTION_OR_ACCESS_UNVERIFIED')
    return evs

def _source_preimages(scene, *, actor_id, event_id, source, procedure_refs,
                      affect_ref, public_action_ref, evs, mode, original_event_id,
                      retained_preimages=None):
    """Snapshot precisely the source objects consumed by an interpretation.

    Only non-objective, historical *read* dependencies go here. Objective
    occurrence identities are pinned separately. Synthetic witness records are
    not accepted ADP-owner or cryptographic signatures.
    """
    own=actor(scene,actor_id)
    current=evs[event_id]
    captured=[]
    def add(kind, ref, obj):
        captured.append((kind,ref,digest(asdict(obj))))
    def history(ref, operation, kind):
        matches=[h for h in own.history if h.id==ref and h.actor==actor_id]
        require(len(matches)==1,'SOURCE_PREIMAGE_IDENTITY_COLLISION')
        h=matches[0]
        require(h.witnessed and h.time<=current.time,'SOURCE_PREIMAGE_IDENTITY_COLLISION')
        w=_history_source(scene,h,operation)
        add(kind,ref,h)
        add(kind+'_WITNESS',ref,w)
    for ref in procedure_refs:
        history(ref,'PROCEDURAL_PRACTICE','PRACTICAL_HISTORY')
    if affect_ref:
        history(affect_ref,'AFFECT_EXPRESSION','AFFECT_HISTORY')
    if public_action_ref:
        history(public_action_ref,'PUBLIC_ACTION','PUBLIC_ACTION_HISTORY')
    if source and source.startswith('history:'):
        token=source.split(':',1)[1]
        matches=[]
        for h in own.history:
            if not h.witnessed or h.time>=current.time:
                continue
            w=_history_source(scene,h)
            if w.operation=='RELATIONAL_RECOGNITION' and digest([asdict(h),asdict(w)])==token:
                matches.append((h,w))
        require(len(matches)==1,'SOURCE_PREIMAGE_IDENTITY_COLLISION')
        h,w=matches[0]
        add('RELATIONAL_HISTORY',h.id,h)
        add('RELATIONAL_HISTORY_WITNESS',h.id,w)
    elif source:
        messages=[z for z in scene.speech if z.id==source]
        require(len(messages)==1,'SOURCE_PREIMAGE_IDENTITY_COLLISION')
        utterance=messages[0]
        action,exposure=_real_spoken_and_heard(scene,utterance,actor_id,current.time,evs)
        add('HEARD_SPEECH',source,utterance)
        add('SPEAKER_ACTION_RECEIPT',source,action)
        add('LISTENER_EXPOSURE_RECEIPT',source,exposure)
    if mode in MODES and mode!='NO_CHANGE':
        choices=_relation_sources(scene,actor_id,current,evs[original_event_id])
        snapshots=[]
        for relevance,observed,witness in choices:
            ref=digest([actor_id,event_id,original_event_id,observed.id])
            snapshots.append(tuple(sorted((kind,ref,digest(asdict(obj))) for kind,obj in (
                ('RELATION_RELEVANCE',relevance),
                ('RELATION_OBSERVED_HISTORY',observed),
                ('RELATION_HISTORY_WITNESS',witness)))))
        if retained_preimages is not None:
            # Revalidate the actually consumed alternative, not a newly preferred
            # receipt. Adding unrelated/alternative evidence cannot rewrite it.
            retained=tuple(sorted(x for x in retained_preimages if x[0].startswith('RELATION_')))
            require(retained in snapshots,'SOURCE_PREIMAGE_IDENTITY_COLLISION')
            captured.extend(retained)
        else:
            require(snapshots,'SOURCE_PREIMAGE_IDENTITY_COLLISION')
            captured.extend(min(snapshots))
    return tuple(sorted(captured))

def _lineage_integrity(scene,state,evs):
    for index,rec in enumerate(state.lineage):
        data=asdict(rec);data.pop('hash')
        require(digest(data)==rec.hash and rec.actor==state.actor
                and rec.version==index+1,'LINEAGE_INTEGRITY_FAILURE')
        require(rec.previous_hash==(state.lineage[index-1].hash if index else None),
                'LINEAGE_PARENT_INVALID')
        original=evs.get(rec.original_event_id)
        event=evs.get(rec.event)
        require(original is not None and event is not None
                and objective_event_hash(original)==rec.original_event_hash
                and objective_event_hash(event)==rec.event_hash,
                'OBJECTIVE_EVENT_IDENTITY_COLLISION')
        try:
            exact=_source_preimages(scene,actor_id=rec.actor,event_id=rec.event,
                source=rec.source,procedure_refs=rec.retained_procedure_refs,
                affect_ref=rec.affect_ref,public_action_ref=rec.public_action_ref,evs=evs,
                mode=rec.mode,original_event_id=rec.original_event_id,
                retained_preimages=rec.source_preimages)
        except Refusal as exc:
            raise Refusal('SOURCE_PREIMAGE_IDENTITY_COLLISION') from exc
        require(exact==rec.source_preimages,'SOURCE_PREIMAGE_IDENTITY_COLLISION')
        require(rec.actor_memory_access=='NOT_GRANTED','UNISSUED_ACTOR_MEMORY')

def _relation_sources(scene,actor_id,e,orig):
    """Return the exact qualified alternatives used by the relation gate."""
    if e.kind not in ('ENCOUNTER','ACTION') or not e.action_owner or e.action_owner==actor_id:return ()
    out=[]
    for x in scene.relevance:
        if x.actor!=actor_id or x.later_event_id!=e.id or x.earlier_event_id!=orig.id:continue
        if (x.issuer!=TEST_RELEVANCE_ISSUER or x.later_event_hash!=objective_event_hash(e)
                or x.earlier_event_hash!=objective_event_hash(orig) or x.time>e.time
                or x.observed_action_owner!=e.action_owner
                or x.observer==actor_id or x.observer not in {a.id for a in scene.actors}):continue
        witness=next((h for h in actor(scene,actor_id).history if h.id==x.observed_history_id),None)
        if (witness and witness.witnessed and witness.time==e.time and x.time==e.time
                and witness.observed_action_owner==e.action_owner
                and witness.activity=='observed_counterpart_action:'+str(e.action)
                and _history_source(scene,witness).operation=='OBSERVED_RELATIONAL_DIFFERENCE'):
            out.append((x,witness,_history_source(scene,witness)))
    return tuple(out)

def _relevant(scene,state,e,evs):
    return bool(state.lineage and _relation_sources(scene,state.actor,e,
        evs[state.lineage[0].original_event_id]))

def eligible(scene,state,event_id):
    # Check already-retained exact objective preimages before any derived-parent checks.
    snapshots={e.id:e for e in scene.events}
    for rec in state.lineage:
        original=snapshots.get(rec.original_event_id);current=snapshots.get(rec.event)
        require(original is not None and current is not None
                and objective_event_hash(original)==rec.original_event_hash
                and objective_event_hash(current)==rec.event_hash,
                'OBJECTIVE_EVENT_IDENTITY_COLLISION')
    evs=validate(scene)
    require(event_id in evs and state.actor in {a.id for a in scene.actors},'UNKNOWN_EVENT_OR_ACTOR')
    e=evs[event_id]; own=actor(scene,state.actor)
    require(state.actor in e.participants and e.id in own.access,'EVENT_NOT_ACTOR_ACCESSIBLE')
    for ref in state.procedure_refs:
        found=next((h for h in own.history if h.id==ref and h.actor==own.id and h.time<e.time),None)
        require(found is not None and found.witnessed,'PROCEDURAL_ORIGIN_UNBOUND')
        _history_source(scene,found,'PROCEDURAL_PRACTICE')
    _lineage_integrity(scene,state,evs)
    if state.lineage:
        prior=evs[state.lineage[-1].event]
        require(prior.time<e.time,'HISTORICAL_TIME_ORDER')
    parent=state.lineage[-1].hash if state.lineage else None
    out=[Candidate(digest([state.actor,objective_event_hash(e),parent,'NONE'])[:20],state.actor,e.id,None,'NO_CHANGE','SUSPEND',parent)]
    if e.kind in ('LOSS','PROCESS'):
        source_event_id=e.parent_event_id if e.kind=='PROCESS' else e.id
        for h in own.history:
            if h.time < e.time and h.witnessed:
                w=_history_source(scene,h)
                if w.operation=='RELATIONAL_RECOGNITION':
                    token=digest([asdict(h),asdict(w)])
                    out.append(Candidate(digest([state.actor,objective_event_hash(e),parent,'HISTORY',token])[:20],state.actor,e.id,'history:'+token,'PROCEDURAL_RECRUITMENT','SUSPEND',parent))
        for s in scene.speech:
            if s.event!=source_event_id or s.id not in own.access or s.time>e.time: continue
            _real_spoken_and_heard(scene,s,own.id,e.time,evs)
            for stance in STANCES:
                out.append(Candidate(digest([state.actor,objective_event_hash(e),s.id,digest(asdict(s)),stance,parent])[:20],state.actor,e.id,s.id,'RECONSIDER',stance,parent))
    if e.kind in ('ENCOUNTER','ACTION') and state.lineage and _relevant(scene,state,e,evs):
        for mode in MODES:
            if mode!='NO_CHANGE':out.append(Candidate(digest([state.actor,objective_event_hash(e),mode,parent])[:20],state.actor,e.id,None,mode,'SUSPEND',parent))
    return tuple(out)

def propose(scene,state,event_id,candidate_id,*,affect_ref=None,public_action_ref=None,model_packet=None):
    require(model_packet is None or (isinstance(model_packet,dict)
            and set(model_packet)=={'candidate_id','model_provenance'}
            and model_packet['candidate_id']==candidate_id), 'LLM_CAUSAL_AUTHORITY_FORBIDDEN')
    possibilities=eligible(scene,state,event_id)
    selected=next((x for x in possibilities if x.id==candidate_id),None)
    require(selected is not None,'CANDIDATE_NOT_ELIGIBLE')
    own=actor(scene,state.actor); event=next(e for e in scene.events if e.id==event_id)
    for ref,why in ((affect_ref,'AFFECT_EVIDENCE_MISSING'),(public_action_ref,'PUBLIC_ACTION_NOT_OWNED')):
        if ref is None:continue
        h=next((h for h in own.history if h.id==ref and h.actor==own.id),None)
        require(h is not None and h.witnessed,why)
        _history_source(scene,h,'AFFECT_EXPRESSION' if ref==affect_ref else 'PUBLIC_ACTION')
        require(h.time<=event.time,'FUTURE_AFFECT_REF' if ref==affect_ref else 'FUTURE_PUBLIC_ACTION_REF')
    root_id=(state.lineage[0].original_event_id if state.lineage else (event.parent_event_id or event.id))
    original=next(e for e in scene.events if e.id==root_id)
    return {'grade':GRADE,'actor':own.id,'event':event_id,
        'event_hash':objective_event_hash(event),'original_event_id':original.id,
        'original_event_hash':objective_event_hash(original),'candidate':asdict(selected),
        'candidate_hash':digest(asdict(selected)),'affect_ref':affect_ref,
        'public_action_ref':public_action_ref,'state_before_hash':state.hash(),
        'possible_owner_effect':'CAN011_OR_ADP016_017_UNISSUED',
        'no_actor_or_world_mutation':True,
        'source_preimages':_source_preimages(scene,actor_id=own.id,event_id=event_id,
            source=selected.source,procedure_refs=state.procedure_refs,
            affect_ref=affect_ref,public_action_ref=public_action_ref,
            evs={e.id:e for e in scene.events},mode=selected.mode,
            original_event_id=original.id)}

def fixture_grant(proposal,scope_actor):
    require(proposal['actor']==scope_actor and proposal['grade']==GRADE,'GRANT_ACTOR_SCOPE_INVALID')
    return {'issuer':'M2_TEST_FIXTURE_AUTHORIZER_ONLY','scope_actor':scope_actor,
        'proposal_hash':digest(proposal),'rule_hash':RULE_HASH}

def audit_no_change(scene,state,proposal,grant):
    """Provenance-only immutable receipt; not stored in State, no psyche change."""
    require(grant==fixture_grant(proposal,state.actor),'OWNER_PERMISSION_NOT_GRANTED')
    require(proposal['state_before_hash']==state.hash(),'STALE_LINEAGE_STATE')
    cand=proposal['candidate']; require(cand['mode']=='NO_CHANGE','NOT_A_NO_CHANGE')
    fresh=propose(scene,state,cand['event'],cand['id'],affect_ref=proposal['affect_ref'],public_action_ref=proposal['public_action_ref'])
    require(fresh==proposal,'PROPOSAL_RECOMPUTATION_FAILED')
    fields=dict(actor=state.actor,event_hash=proposal['event_hash'],state_before_hash=state.hash(),
                candidate_hash=proposal['candidate_hash'],grade='TEST_ONLY_NO_EFFECT_AUDIT')
    return NoChangeAudit(**fields,hash=digest(fields))

def append_test_only(scene,state,proposal,grant):
    require(grant==fixture_grant(proposal,state.actor),'OWNER_PERMISSION_NOT_GRANTED')
    require(proposal['state_before_hash']==state.hash(),'STALE_LINEAGE_STATE')
    c=proposal['candidate']
    require(proposal['candidate_hash']==digest(c) and c['rule_hash']==RULE_HASH,'CANDIDATE_HASH_OR_RULE')
    new=propose(scene,state,c['event'],c['id'],affect_ref=proposal['affect_ref'],public_action_ref=proposal['public_action_ref'])
    require(new==proposal,'PROPOSAL_RECOMPUTATION_FAILED')
    if c['mode']=='NO_CHANGE':
        audit_no_change(scene,state,proposal,grant)
        return state
    previous=state.lineage[-1].hash if state.lineage else None
    require(c['parent']==previous,'LINEAGE_PARENT_MISMATCH')
    fields=dict(actor=state.actor,event=c['event'],version=len(state.lineage)+1,
        previous_hash=previous,candidate_hash=proposal['candidate_hash'],source=c['source'],
        mode=c['mode'],belief_stance=c['stance'],affect_ref=proposal['affect_ref'],
        public_action_ref=proposal['public_action_ref'],retained_procedure_refs=state.procedure_refs,
        actor_memory_access='NOT_GRANTED',rule_hash=RULE_HASH,
        provenance_refs=(proposal['event_hash'],proposal['original_event_hash'],
                         proposal['candidate_hash'],grant['proposal_hash']),
        event_hash=proposal['event_hash'],original_event_id=proposal['original_event_id'],
        original_event_hash=proposal['original_event_hash'],
        source_preimages=proposal['source_preimages'])
    rec=Interpretation(**fields,hash=digest(fields))
    return replace(state,lineage=state.lineage+(rec,))

def seed_scene(*,child_history='cooperative',parent_history='care_work',peer_speech=True,
        child_access_peer=True,other_action='REFUSE',age=12,background='any'):
    """Provenance-bearing, entirely synthetic independently witnessed fixture."""
    child=Actor('child',(
        History('prior_recognition','child',1,child_history,True,False),
        History('old_watchful_habit','child',2,'guard_property',True,False),
        History('first_distress','child',4,'bodily_grief',True,True),
        History('public_lock_check','child',5,'lock_inspection',True,True),
        History('later_observed_counterpart','child',9,'observed_counterpart_action:'+other_action,True,True,
                observed_action_owner='other_P')),
        ('loss','parent_said')+(('peer_said',) if child_access_peer else ())+
        ('discussion','later',),'repair_bicycle',age,background)
    caregiver=Actor('caregiver',(History('care_work_history','caregiver',1,parent_history,True,False),),
        ('loss','parent_speak'),'care_work',42,background)
    peer=Actor('peer',(History('peer_debate','peer',1,'school_club',True,False),),('loss','peer_speak'),'school_club',13,background)
    other=Actor('other_P',(History('other_project','other_P',3,'own_music_project',True,False),),
        ('later',),'own_music_project',19,background)
    loss=Event('loss','LOSS',3,'child',('child','caregiver','peer'),('bike','garage','loss_of_transport'))
    parent_act=Event('parent_speak','ACTION',4,'child',('child','caregiver'),('speaker_action',),
        action_owner='caregiver',action='SPEAK')
    peer_act=Event('peer_speak','ACTION',5,'child',('child','peer'),('speaker_action',),
        action_owner='peer',action='SPEAK')
    discussion=Event('discussion','PROCESS',6,'child',('child','caregiver','peer'),
        ('loss_discussion',),parent_event_id='loss',parent_event_hash=objective_event_hash(loss))
    later=Event('later','ENCOUNTER',9,'child',('child','other_P'),('community_hall',),
        action_owner='other_P',action=other_action)
    people=(child,caregiver,peer,other);events=(loss,parent_act,peer_act,discussion,later)
    speech=[Speech('parent_said','loss','caregiver',4,'Someone could be in need.','parent_need_account')]
    if peer_speech:speech.append(Speech('peer_said','loss','peer',5,'It must be that group.','peer_group_blame'))
    ops={'prior_recognition':'RELATIONAL_RECOGNITION',
         'old_watchful_habit':'PROCEDURAL_PRACTICE','first_distress':'AFFECT_EXPRESSION',
         'public_lock_check':'PUBLIC_ACTION','later_observed_counterpart':'OBSERVED_RELATIONAL_DIFFERENCE',
         'care_work_history':'INDEPENDENT_PRACTICE',
         'peer_debate':'INDEPENDENT_PRACTICE','other_project':'INDEPENDENT_PROJECT'}
    observers={'child':'caregiver','caregiver':'peer','peer':'caregiver','other_P':'caregiver'}
    witnesses=tuple(HistoryWitness(h.id,digest(asdict(h)),a.id,observers[a.id],h.time,'actor_activity',ops[h.id])
        for a in people for h in a.history)
    acts=[];heard=[]
    for s in speech:
        act=parent_act if s.speaker=='caregiver' else peer_act
        acts.append(SpeechAction(s.id,digest(asdict(s)),s.speaker,act.id,
            objective_event_hash(act),'child',s.time))
        if s.id!='peer_said' or child_access_peer:
            heard.append(Exposure(s.id,digest(asdict(s)),'child',
                objective_event_hash(act),'child',s.time))
    relevance=(Relevance('later',objective_event_hash(later),'loss',
       objective_event_hash(loss),'child','later_observed_counterpart','caregiver',9,
       observed_action_owner='other_P'),)
    return Scene(people,events,tuple(speech),witnesses,tuple(acts),tuple(heard),relevance)
