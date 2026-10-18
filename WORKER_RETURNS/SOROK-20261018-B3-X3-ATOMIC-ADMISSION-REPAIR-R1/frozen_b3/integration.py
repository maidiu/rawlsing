"""B3 research integration: events cause bounded computation, menus do not cause psyche."""
from __future__ import annotations
from copy import deepcopy
from dataclasses import asdict,replace
from pathlib import Path
import hashlib,json,sqlite3,fcntl
from contextlib import contextmanager
from sources import b2,m2,identities
from custody import prepare,admit,projected_loss,participant_from_records
import target_owner
import source_guard
@contextmanager
def locked(path):
 path=Path(str(path)+'.b3lock');path.parent.mkdir(parents=True,exist_ok=True)
 with path.open('a+b') as handle:
  fcntl.flock(handle,fcntl.LOCK_EX)
  try:yield
  finally:fcntl.flock(handle,fcntl.LOCK_UN)

GRADE='TEST_ONLY_B3_INTEGRATED_CANDIDATE_PENDING_I2'
RESPONSE_RULE='B3_SITUATED_PRACTICAL_RESPONSE@1'
def digest(x):return m2.digest(x)
def seal(x):return dict(x,hash=digest(x))
class Refusal(ValueError):pass

def require(x,reason):
 if not x:raise Refusal(reason)

# These denote attempted operations, not expected human responses. Only suggestion
# is noncausal input; every write/privilege operation needs its own destination.
FORBIDDEN={
 'demographic_psychology':'DEMOGRAPHY_TO_PSYCHOLOGY',
 'event_is_objective_without_witness':'PROPOSAL_PROMOTION',
 'private_motive_as_actor_knowledge':'OTHER_PRIVATE_MOTIVE_LEAK',
 'fabricated_actor':'FABRICATED_ACTOR','retro_child_influences_parent':'RETROCAUSAL_PARENT_HISTORY',
 'direct_other_actor_write':'CROSS_ACTOR_STATE_WRITE','self_issued_permission':'TARGET_OWNER_PERMISSION_SELF_ISSUED',
 'renderer_causes_event':'RENDERER_MUTATION','assign_culprit_group':'IDEOLOGICAL_ASSERTION_AS_OBJECTIVE_FACT',
 'force_contact_after_refusal':'COUNTERPART_REFUSAL_IGNORED','rewrite_t0':'RETROACTIVE_ORIGINAL_EVENT_MUTATION',
 'unlicensed_probability':'PROBABILITY_AUTHORITY_MISSING'}
MATERIAL_ACTS={'REPAIR_TOOLS','LATER_PROJECT','DECLINE_HELP','DECLINE_CONTACT','ALLOW_CONTACT','SHARED_TASK_CHOICE','SHARED_TASK_OVERRULE','BIKE_CARE','PUBLIC_ECHO'}
ALLOWED_ACTS=MATERIAL_ACTS|{'SPEAK','MATERIAL_LOSS','CAPABILITY_TASK_SUCCESS','CAPABILITY_TASK_FAILURE','PRACTICE_COMPLETED','RESPONSE_SELECTION'}

def qualify(data):
 """Validate source-owned records and actor read permissions before any write."""
 actor=data['actor'];event=data['event'];records=data['evidence'];now=data['as_of']
 require(event.get('admitted') and event['content_hash']==digest(event['content']),'OBJECTIVE_EVENT_NOT_ISSUED')
 require(event['owner']=='TEST_WORLD_REGISTRY','OBJECTIVE_EVENT_OWNER_MISSING')
 require(event['content'].get('known_culprit') is None,'CULPRIT_NOT_AUTHORIZED')
 seen={}
 for x in records:
  require(x['hash']==digest({k:v for k,v in x.items() if k!='hash'}) and x['id'] not in seen,'WITNESS_INTEGRITY')
  seen[x['id']]=x
 for op,value in data.get('proposals',{}).items():
  if value and op in FORBIDDEN:raise Refusal(FORBIDDEN[op])
  require(op in FORBIDDEN or op=='suggestion','UNREGISTERED_CAUSAL_OPERATION')
 for x in records:
  require(x['actor'] in data['actors'] and x['act'] in ALLOWED_ACTS,'WITNESS_ACTOR_OR_ACTION_UNLICENSED')
  require(x['owner']==x['actor'],'WITNESS_OWNER_MISMATCH')
  require(x['time']<=now,'FUTURE_WITNESS_RECRUITMENT')
 for s in data['utterances']:
  require(s['speaker'] in data['actors'] and s['witness'] in seen,'UNWITNESSED_SPEECH')
  x=seen[s['witness']]
  require(x['actor']==s['speaker'] and x['act']=='SPEAK','SPEECH_SPEAKER_MISMATCH')
  require(s['epistemic']=='ATTRIBUTED_CLAIM','CLAIM_TRUTH_PROMOTION')
 require(len({z['id'] for z in data['exposures']})==len(data['exposures']) and len({(z['speech_id'],z['listener']) for z in data['exposures']})==len(data['exposures']),'EXPOSURE_IDENTITY_COLLISION')
 for exposure in data['exposures']:
  spoken=next((s for s in data['utterances'] if s['id']==exposure['speech_id']),None)
  require(spoken is not None and exposure['listener']=='child' and exposure['observer'] in data['actors'] and exposure['observer']!=spoken['speaker'] and exposure['issuer']=='B3_TEST_ONLY_EXPOSURE_REGISTRY','EXPOSURE_WITNESS_INVALID')
  x=seen[spoken['witness']]
  require(exposure['speech_witness']==x['id'] and exposure['source_hash']==x['hash'] and x['time']<=exposure['time']<=now,'EXPOSURE_TIME_OR_SOURCE_INVALID')
 for ref in data['readset']:
  require(ref in seen,'READSET_MISSING_WITNESS');x=seen[ref]
  require(x['actor']==actor['id'] or x['source']=='PUBLIC_WORLD' or
   (x['act']=='SPEAK' and any(s['witness']==ref and actor['id'] in s['heard_by'] and any(z['speech_id']==s['id'] and z['listener']==actor['id'] for z in data['exposures']) for s in data['utterances'])),'OTHER_ACTOR_PRIVATE_READ')
 # Exact task observations, not a capability label or demographic proxy.
 cap=data['capability'];matched=[]
 for w in cap['witnesses']:
  x=seen.get(w['source'])
  if (x and w['actor']==actor['id'] and w['scope']==cap['scope'] and w['capability']==cap['name']
    and w['time']<=now and (not w.get('end') or now<w['end']) and x['actor']==actor['id']
    and x['source']=='OBSERVED_TASK' and x['act']=={'PRESENT':'CAPABILITY_TASK_SUCCESS','ABSENT':'CAPABILITY_TASK_FAILURE'}.get(w['outcome'])):matched.append(w['outcome'])
 if 'PRESENT' in matched and 'ABSENT' in matched:return seen,'CAPABILITY_CONTRADICTED'
 if cap['declared']=='ABSENT' and 'ABSENT' in matched:return seen,'CAPABILITY_ABSENT_SCOPED'
 if cap['declared']!='PRESENT' or 'PRESENT' not in matched:return seen,'CAPABILITY_UNQUALIFIED'
 return seen,None

def scene_at(data,loss,now,original_loss=None):
 """Construct only already occurred synthetic histories/actions/exposures."""
 evs=([original_loss] if original_loss is not None and original_loss.id!=loss.id else [])+[loss];histories={a:[] for a in data['actors']};witnesses=[];speeches=[];actions=[];exposures=[]
 by_id={x['id']:x for x in data['evidence'] if x['time']<=now}
 for x in by_id.values():
  if x['time']>=now:continue
  h=m2.History(x['id'],x['actor'],x['time'],x['act'],True,x['actor']=='child')
  histories[x['actor']].append(h)
  op='PROCEDURAL_PRACTICE' if x['act'] in ('BIKE_CARE','PRACTICE_COMPLETED') else 'INDEPENDENT_PRACTICE'
  if x['act'] in ('SHARED_TASK_CHOICE','SHARED_TASK_OVERRULE'):op='RELATIONAL_RECOGNITION'
  if x['act']=='LATER_PROJECT':op='INDEPENDENT_PROJECT'
  observer='caregiver' if x['actor']=='child' else 'child'
  witnesses.append(m2.HistoryWitness(h.id,digest(asdict(h)),h.actor,observer,h.time,'synthetic_observation',op))
 access=[e.id for e in evs]
 for s in data['utterances']:
  x=by_id.get(s['witness'])
  if not x:continue
  ev=m2.Event(x['id'],'ACTION',x['time'],'child',('child',s['speaker']),('speaker_action',),action_owner=s['speaker'],action='SPEAK')
  speech=m2.Speech(s['id'],s.get('event_ref',loss.id),s['speaker'],x['time'],s['claim'],x['hash'])
  evs.append(ev);speeches.append(speech)
  actions.append(m2.SpeechAction(s['id'],digest(asdict(speech)),s['speaker'],ev.id,m2.objective_event_hash(ev),'child',x['time']))
  heard=next((z for z in data['exposures'] if z['speech_id']==s['id'] and z['listener']=='child' and z['time']<=now),None)
  if heard and 'child' in s['heard_by'] and s['witness'] in data['readset']:
   exposures.append(m2.Exposure(s['id'],digest(asdict(speech)),'child',m2.objective_event_hash(ev),heard['observer'],heard['time']));access.append(s['id'])
   evs.append(m2.Event('exposure:'+heard['id'],'ACTION',heard['time'],heard['observer'],('child',s['speaker']),('speaker_action',)))
 if now>loss.time and loss.kind=='LOSS':
  process=m2.Event('process:'+str(now),'PROCESS',now,'child',('child','caregiver','peer'),('loss_discussion',),parent_event_id=loss.id,parent_event_hash=m2.objective_event_hash(loss))
  evs.append(process);access.append(process.id)
 people=tuple(m2.Actor(a,tuple(histories[a]),tuple(access) if a=='child' else (), 'LATER_PROJECT' if any(h.activity=='LATER_PROJECT' for h in histories[a]) else 'own_project:'+a) for a in data['actors'])
 return m2.Scene(people,tuple(evs),tuple(speeches),tuple(witnesses),tuple(actions),tuple(exposures)),evs[-1].id if now>loss.time and loss.kind=='LOSS' else loss.id

def response(data,admission,possibilities,middle):
 """Bounded practical affordances; no automatic affect, belief, or stance selection."""
 records=data['evidence'];now=data['as_of'];object_ref=data['event']['content']['object']
 activity=sorted((x['actor'],x['act'],x['id']) for x in records if x['act'] in MATERIAL_ACTS)
 offers=sorted(x['id'] for x in records if x['actor'] in ('caregiver','peer','later_other') and x['act'] in ('REPAIR_TOOLS','LATER_PROJECT','ALLOW_CONTACT','DECLINE_CONTACT'))
 routes=['NO_CHANGE','PRIVATE_PRACTICE']
 if any(x['act']=='REPAIR_TOOLS' for x in records):routes.append('JOINT_PRACTICAL_ACTION_POSSIBLE')
 if any(x['act']=='LATER_PROJECT' for x in records):routes.append('RECONSIDERATION_POSSIBLE')
 refused={x['actor'] for x in records if x['act']=='DECLINE_CONTACT'}
 if any(x['act']=='ALLOW_CONTACT' and x['actor'] not in refused for x in records):routes.append('CONTACT_POSSIBLE')
 if data['actor']['epistemic']['beliefs']:routes.append('BELIEF_MAY_COEXIST_WITH_DISTINCT_AFFECT')
 if any(x['act']=='PUBLIC_ECHO' for x in records):routes.append('PUBLIC_ENACTMENT_NOT_BELIEF')
 active=[x for x in middle if x['lifecycle']=='ACTIVE' and x['targets']==[object_ref]]
 # A causal contrast in enacted procedure, never an inferred emotion: an active
 # practice supplies a CHECK_LOCK option; zero qualifying history supplies none.
 actions=['CHECK_LOCK'] if active and data['event']['content']['fact']=='shared_tool_offer' else []
 return seal(dict(rule=RESPONSE_RULE,rule_source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
  event_ref=admission['admitted_event']['hash'],conditioning_hash=digest(middle),
  candidate_hashes=[digest(asdict(c)) for c in possibilities],recruited=[x['hash'] for x in active],
  uptake=[{'source':s['id'],'epistemic':'HEARD_ATTRIBUTED_ONLY'} for s in data['utterances'] if 'child' in s['heard_by'] and s['witness'] in data['readset']],
  material_actor_activity=activity,independent_offer_refs=offers,admissible_routes=sorted(set(routes)),
  practical_actions=actions,selected_affect=None,selected_belief=None,
  current_consequence='PRACTICAL_OPTION_ONLY' if actions else 'CURRENT_RESPONSE_CONSEQUENCES_VALID_EMPTY',
  actor_safe={'origin_explanation':'NOT_ACCESSIBLE','actions':actions},draws=0))

class Integration:
 def __init__(self,path,authority=None):
  self.authority=authority;self.path=Path(path)
  with locked(self.path):
   self.bridge=b2.Bridge(path,None if Path(path).exists() else b2.b1.initialize([]));self.db=self.bridge.store.db
   self.db.executescript('''CREATE TABLE IF NOT EXISTS b3_source (id TEXT PRIMARY KEY, body TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS b3_transition (id TEXT PRIMARY KEY, body TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS b3_response (id TEXT PRIMARY KEY, body TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS b3_clock (clock INTEGER PRIMARY KEY);
CREATE TABLE IF NOT EXISTS b3_m2_sources (id TEXT PRIMARY KEY, body TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS b3_preimage (id TEXT PRIMARY KEY, body TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS b3_audit (id TEXT PRIMARY KEY, body TEXT NOT NULL);''')
 def close(self):self.bridge.close()
 def snapshot(self):
  names=[r[0] for r in self.db.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
  return {n:self.db.execute('SELECT * FROM '+n+' ORDER BY 1').fetchall() for n in names}
 def middle(self):return [json.loads(r[0]) for r in self.db.execute('SELECT body FROM b3_transition ORDER BY id')]
 def admit_projection(self,projection,records):
  external=dict(id=projection.id,owner='TEST_WORLD_REGISTRY',time=projection.time,admitted=True,
   content={'fact':'observed_'+projection.kind.lower(),'object':'bike-child','known_culprit':None,'m2_preimage':asdict(projection)})
  external['content_hash']=digest(external['content'])
  prior=self.db.execute('SELECT body FROM b3_audit WHERE id=?',('bundle:'+projection.id,)).fetchone()
  if prior:
   bundle=json.loads(prior[0]);require(m2.canonical(bundle['witness']['external_occurrence'])==m2.canonical(external),'SOURCE_PREIMAGE_IDENTITY_COLLISION')
  else:bundle,_=prepare(self.bridge.store.state(),external,projection=projection,participant=participant_from_records(records,projection.time))
  receipt=admit(self.bridge,bundle)
  require(isinstance(receipt['event_admission'],dict),'PROJECTED_OCCURRENCE_NOT_ADMITTED')
  qualified=projected_loss(self.bridge,bundle)
  require(m2.objective_event_hash(qualified)==m2.objective_event_hash(projection),'UNQUALIFIED_M2_EVENT')
  if not prior:self.db.execute('INSERT INTO b3_audit VALUES (?,?)',('bundle:'+projection.id,m2.canonical(bundle)))
  return dict(event_id=projection.id,event_hash=m2.objective_event_hash(projection),b2_receipt=receipt)
 def run(self,data,*,owner_permission=None,registered_permissions=()):
  with locked(self.path):return self._run(data,owner_permission=owner_permission,registered_permissions=registered_permissions)
 def _run(self,data,*,owner_permission=None,registered_permissions=()):
  data=deepcopy(data);before=self.snapshot();event=data['event'];key=event['id'];initial_world_hash=digest(event)
  base=dict(case_id=data.get('case_id'),grade=GRADE,issued_production_authority=False,owner_effect_committed=False,
   selected_affect=None,asserted_culprit_group=None,imports=identities(),new_event_count=0)
  def stop(status,code):
   require(self.snapshot()==before,'REFUSAL_MUTATED_DATABASE')
   return dict(base,status=status,code=code,no_mutation=True)
  try:
   records,deferred=qualify(data)
   require(self.authority is not None and self.authority.permits(data),'SYNTHETIC_SOURCE_ISSUER_NOT_REGISTERED')
   # Prior ledger evidence is never silently repaired or converted to our mapping.
   for x in data.get('ledger',[]):
    if x['event_id']==key:
     require(x['content_hash']==event['content_hash'],'EVENT_ID_CONTENT_COLLISION')
     require(x['owner']==event['owner'],'EVENT_OWNER_REPLAY_MISMATCH')
   if deferred:return stop('DEFERRED',deferred)
   incoming={x['id']:x for x in data['evidence']}
   incoming.update({'exposure:'+z['id']:z for z in data['exposures']})
   last_clock=self.db.execute('SELECT coalesce(max(clock),0) FROM b3_clock').fetchone()[0]
   require(data['as_of']>=last_clock,'B3_TIME_REVERSED')
   for z in data['exposures']:
    old=self.db.execute('SELECT body FROM b3_preimage WHERE id=?',('exposure:'+z['id'],)).fetchone()
    require(old is not None or z['time']>=last_clock,'PAST_EXPOSURE_INSERTION')
   incoming.update({'speech:'+s['id']:{k:v for k,v in s.items() if k!='heard_by'} for s in data['utterances']})
   for sid,body in self.db.execute('SELECT id,body FROM b3_preimage'):
    require(sid in incoming and m2.canonical(incoming[sid])==body,'SOURCE_PREIMAGE_IDENTITY_COLLISION')
   previous=self.db.execute('SELECT body FROM b3_source WHERE id=?',(key,)).fetchone()
   if previous:require(json.loads(previous[0])==event,'EVENT_ID_CONTENT_COLLISION')
   bundle,loss=prepare(self.bridge.store.state(),event,participant=participant_from_records(data["evidence"],event["time"]))
   if previous:
    # Reuse the original complete B2 readset on exact reentry, rather than minting
    # a new context from a later checkpoint. Caller still must match source bytes.
    row=self.db.execute('SELECT body FROM b3_audit WHERE id=?',('bundle:'+key,)).fetchone()
    bundle=json.loads(row[0])
   admission=admit(self.bridge,bundle)
   require(isinstance(admission['event_admission'],dict),'B2_'+admission.get('reason','NOT_ADMITTED'))
   loss=projected_loss(self.bridge,bundle)
   if not previous:
    self.db.execute('INSERT INTO b3_source VALUES (?,?)',(key,m2.canonical(event)))
    self.db.execute('INSERT INTO b3_audit VALUES (?,?)',('bundle:'+key,m2.canonical(bundle)))
   # LOSS response is evaluated at its real clock before speech exists; PROCESS
   # at the later clock receives only actual admitted speaker/exposure records.
   traces=[];source_admissions=[];state=m2.State('child')
   origin=loss
   if data.get('origin_event_id'):
    parent=self.db.execute('SELECT body FROM b3_audit WHERE id=?',('bundle:'+data['origin_event_id'],)).fetchone()
    require(parent is not None,'ORIGINAL_EVENT_NOT_ADMITTED')
    origin=projected_loss(self.bridge,json.loads(parent[0]))
   for clock in sorted(set([loss.time,data['as_of']])):
    scene,process_id=scene_at(data,loss,clock,origin)
    for occurrence in sorted(scene.events,key=lambda e:(e.time,e.id)):
     if occurrence.id in (loss.id,origin.id):continue
     source_admissions.append(self.admit_projection(occurrence,data["evidence"]))
    old={sid:json.loads(body) for sid,body in self.db.execute('SELECT id,body FROM b3_m2_sources')}
    current=source_guard.check(old,scene)
    possibilities=m2.eligible(scene,state,process_id)
    for sid,body in current.items():self.db.execute('INSERT OR IGNORE INTO b3_m2_sources VALUES (?,?)',(sid,m2.canonical(body)))
    traces.append(dict(clock=clock,event=process_id,event_hash=m2.objective_event_hash(next(x for x in scene.events if x.id==process_id)),
      admitted_source_ref=admission['admitted_event']['hash'],candidates=[asdict(c) for c in possibilities],state_hash=state.hash(),
      actual_speech_ids=[s.id for s in scene.speech],exposure_ids=[e.speech_id for e in scene.exposures]))
   for sid,body in incoming.items():self.db.execute('INSERT OR IGNORE INTO b3_preimage VALUES (?,?)',(sid,m2.canonical(body)))
   middle=self.middle();r=response(data,admission,possibilities,middle)
   self.db.execute('BEGIN IMMEDIATE')
   transition=dict(status='VALID_EMPTY',code='CAN011_QUALIFIED_EFFECT_RULE_OR_PERMISSION_MISSING',before=digest(middle),after=digest(middle))
   practices=[x for x in records.values() if x['act']=='PRACTICE_COMPLETED']
   if practices and owner_permission:
    proposal=dict(actor='child',before=digest(middle),rule_hash=target_owner.RULE_HASH,time=data['as_of'],parents=[x['hash'] for x in practices])
    try:
     record=target_owner.validate(middle,event,list(records.values()),proposal,owner_permission,registered_permissions)
     self.db.execute('INSERT OR IGNORE INTO b3_transition VALUES (?,?)',(record['hash'],m2.canonical(record)))
     transition=dict(status='COMMITTED',record=record,before=digest(middle),after=digest(self.middle()),permission=owner_permission,grade='TEST_ONLY')
     base['owner_effect_committed']=True;base['independent_owner_receipt']=transition
    except target_owner.Denied as e:transition=dict(status='DENIED',code=str(e),before=digest(middle),after=digest(self.middle()))
   if transition['status']!='DENIED':self.db.execute('INSERT OR IGNORE INTO b3_response VALUES (?,?)',(r['hash'],m2.canonical(r)))
   self.db.execute('INSERT OR IGNORE INTO b3_clock VALUES (?)',(data['as_of'],))
   self.db.execute('COMMIT')
   require(digest(event)==initial_world_hash,'T0_REWRITTEN')
   base.update(status='ELIGIBLE_NONCAUSAL',code='SOURCEFREE_EVIDENCE_BOUNDARY_PASS',original_event_hash=event['content_hash'],event_world_hash_after=event['content_hash'],
    exact_replay=bool(previous or any(x['event_id']==key and x['content_hash']==event['content_hash'] for x in data.get('ledger',[]))),
    new_event_count=int(not previous),verified_evidence_refs=sorted(records),
    accessible_readset=sorted(data['readset']),material_actor_activity=r['material_actor_activity'],independent_offer_refs=r['independent_offer_refs'],admissible_routes=r['admissible_routes'],
    history_material_hash=digest(r['material_actor_activity']),admission=admission,CAN008_response=r,CAN011_transition=transition,
    M2_temporal_traces=traces,source_admissions=source_admissions,ADP016_memory='NOT_GRANTED',ADP017_access='HEARING_ONLY_NO_EPISTEMIC_WRITE',
    observed_belief_records=data['actor']['epistemic']['beliefs'],observed_affect_records=data['actor']['epistemic']['affect'],
    retained_practice=data['actor']['practice'],immutable_history={'source':event,'b2_occurrence':admission['admitted_event']['hash'],'m2_projection':m2.objective_event_hash(loss)},
    accumulated_history_refs=[digest(json.loads(x[0])) for x in self.db.execute('SELECT body FROM b3_source ORDER BY id')],
    later_meaning_effect='DEFERRED_M2_DURABLE_LINEAGE_QUARANTINED_M3_P0',
    interpretation_lineage=data.get('lineage',[]),lineage_grade='INPUT_CANDIDATE_NOT_CAUSAL_STATE',no_mutation=self.snapshot()==before)
   return base
  except (Refusal,m2.Refusal) as e:
   if self.db.in_transaction:self.db.execute('ROLLBACK')
   return stop('REFUSED',str(e))
