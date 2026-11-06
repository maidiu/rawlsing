"""Finite source-free transition experiment, NOT an ADP/CAN developmental owner.

Roots declare material conditions and permissions; later events must consume earlier
values. No endpoint or descendant enters this builder. Every computed consequence
has an actual readset. Text labels are descriptive, never capability evidence.
"""
from copy import deepcopy
from .core import h_obj, h_concat

VERSION='G15_SITUATED_TRANSITIONS_R1'
ROOTS={'ORIGIN_FAMILY','WORLD_MATERIAL','PEER_ROOT'}
ROUTES={
 'ROUTE_LOCAL_CLOSED':('INST_WORKSHOP_A',12,3),
 'ROUTE_INSTITUTIONAL':('INST_EVENING_CLASS_B',5,4),
 'ROUTE_UNCONVENTIONAL':('INST_COMMUNITY_D',6,5),
 'ROUTE_MOBILITY':('INST_TRANSIT_E',10,9),
}
EVENT_PAYLOAD_FIELDS={
 'ORIGIN_FAMILY':{'permission','role','cash','free_hours'},
 'WORLD_MATERIAL':{'permission','project_id','material_units','unit_payment','project_permit','tool_return_permit','offers'},
 'PEER_ROOT':{'permission','kinship','tool_units','goal'},'SCHOOLING':{'hours'},
 'WORK_POSITION':{'hours','wage','material_position'},
 'PROJECT':{'project','nonmother','consequential','durable_effect'},
 'PEER_PROJECT':set(),'PEER_ACTION':{'returned_units','performed'},
 'NONMOTHER_RELATIONSHIP':{'counterpart','relation_kind','nonmother','consequential','durable_effect'},
 'PRACTICE_FORMATION':{'practice','causal_event_refs'},
 'ATTITUDE_FORMATION':{'attitude','causal_event_refs'},
 'MEMORY_TRACE':{'experienced_basis_event'},'STRIVING':{'striving','causal_event_refs'},
 'ORGANISMIC_EVENT':{'rest_hours'},'ROUTE_AVAILABILITY':{'route','via'},
 'COMMISSIONED_WORK':{'place','workplace'},'ENROLLMENT':{'place','workplace'},
 'COMMUNITY_CALLOUT':{'place','workplace'},'MOBILITY_HISTORY':{'place','workplace'},
 'ENDPOINT_STATE':{'place','availability_status'},
}
FORMATION={'attitudes':('ATTITUDE_FORMATION','attitude'),
 'practices':('PRACTICE_FORMATION','practice'),'strivings':('STRIVING','striving')}


def make_event(index,kind,actor,payload,parents,owner=None):
 body=dict(effective_index=index,kind=kind,actors=[actor],owner_id=owner or actor,
           payload=deepcopy(payload),causal_parent_event_ids=list(parents),
           source_grade='SOURCEFREE_RESEARCH_INPUT')
 return dict(event_id=h_obj(body),**body)


class HistoryFault(ValueError):
 pass


def replay_history(events):
 """Validate typed, temporal, owner-bound dependencies and compute consequences.

 Partial outputs are retained for diagnostics, never admitted when errors exist.
 A stale output claim cannot supply values. A source must be in the direct typed
 parent readset, not simply somewhere in the graph.
 """
 errors=[]; admitted={}; effects={}; witnesses=[];seen=set();indices=set()
 state=dict(place=None,availability_status='unavailable',material_position=None,
            skill=0,cash=0,free_hours=0,completed_units=0,debt_units=0,
            material_remaining=0,tools_remaining=0,
            practices=[],attitudes=[],projects=[],nonmother_relations=[],
            actor_id=None,role=None,health=None)
 def fail(code,e,detail=None):
  errors.append(dict(code=code,event_id=e.get('event_id'),detail=detail))
 ordered=sorted(events,key=lambda x:x.get('effective_index',-1))
 for e in ordered:
  eid=e.get('event_id');idx=e.get('effective_index');kind=e.get('kind');p=e.get('payload',{})
  actors=e.get('actors') or [];actor=actors[0] if actors else None
  if not isinstance(actors,list) or len(actors)!=1:
   fail('SINGULAR_EVENT_REQUIRES_ONE_ACTOR',e);continue
  parents=e.get('causal_parent_event_ids') or [];readset=[]
  if not isinstance(eid,str) or not eid or eid in seen:
   fail('DUPLICATE_EVENT_ID',e);continue
  seen.add(eid)
  if type(idx) is not int or idx in indices:
   fail('DUPLICATE_EFFECTIVE_INDEX',e);continue
  indices.add(idx)
  absent=[r for r in parents if r not in admitted]
  if absent:
   for ref in absent:
    other=next((x for x in events if x.get('event_id')==ref),None)
    code='NONFORWARD_CAUSAL_PARENT' if ref==eid else 'FUTURE_CAUSAL_PARENT' if other and other.get('effective_index',-1)>=idx else 'MISSING_CAUSAL_PARENT'
    fail(code,e,ref)
   continue
  if kind not in ROOTS and not parents:
   fail('UNDECLARED_ROOT',e);continue
  if kind in ROOTS and parents:
   fail('ROOT_HAS_CAUSAL_PARENTS',e);continue
  if not isinstance(actor,str) or not actor or e.get('owner_id')!=actor:
   fail('EVENT_OWNER_IDENTITY_INVALID',e);continue
  if kind=='ORIGIN_FAMILY' and state['actor_id'] is not None:
   fail('MULTIPLE_SUBJECT_ROOTS',e);continue
  if kind not in ROOTS|{'PEER_PROJECT','PEER_ACTION'} and actor!=state['actor_id']:
   fail('ACTOR_CROSSOVER',e);continue
  def get(kinds,field=None,which=0,owner=None):
   choices=[admitted[r] for r in parents if admitted[r]['kind'] in kinds and (owner is None or admitted[r]['owner_id']==owner)]
   if len(choices)<=which: raise HistoryFault('TYPED_PARENT_REQUIRED:'+','.join(sorted(kinds)))
   src=choices[which];value=effects[src['event_id']] if field is None else effects[src['event_id']].get(field)
   readset.append(dict(event_id=src['event_id'],owner_id=src['owner_id'],path='effect'+('' if field is None else '.'+field),value=deepcopy(value)))
   return value
  def require(ok,code):
   if not ok:raise HistoryFault(code)
  def number(value,name,minimum=0):
   require(type(value) is int and minimum<=value<=1000000,'INVALID_INTEGER:'+name);return value
  if not isinstance(p,dict) or kind not in EVENT_PAYLOAD_FIELDS or set(p)!=EVENT_PAYLOAD_FIELDS[kind]:
   fail('UNCLASSIFIED_EVENT_PAYLOAD',e);continue
  before=deepcopy(state);effect={}
  try:
   if kind=='ORIGIN_FAMILY':
    require(p.get('permission')=='RESEARCH_HISTORY_ONLY' and p.get('role') in {'repair','finishing'},'ROOT_NOT_RESEARCH_AUTHORIZED')
    state.update(actor_id=actor,role=p['role'],cash=number(p.get('cash'),'cash'),free_hours=number(p.get('free_hours'),'free_hours'))
    effect=dict(role=state['role'],cash=state['cash'],free_hours=state['free_hours'])
   elif kind=='WORLD_MATERIAL':
    require(actor=='G15_WORLD' and p.get('permission')=='SOURCEFREE_MATERIAL_ONLY','WORLD_SOURCE_AUTHORITY_MISSING')
    require(p.get('project_id') in {'communal_irrigation_pump_repair','apprentice_finishing_work'},'PROJECT_ID_MISSING')
    number(p.get('material_units'),'material_units');number(p.get('unit_payment'),'unit_payment')
    require(type(p.get('project_permit')) is bool and type(p.get('tool_return_permit')) is bool,'WORLD_PERMISSION_NOT_TYPED')
    offers=p.get('offers',{})
    require(isinstance(offers,dict) and all(k in ROUTES for k in offers),'UNKNOWN_WORLD_ROUTE')
    for route,o in offers.items():
     require(set(o)=={'place','payment','travel_cost','hours','permit'},'UNCLASSIFIED_OFFER')
     require(o['place']==ROUTES[route][0] and type(o['permit']) is bool,'INVALID_WORLD_PLACE_OR_PERMISSION')
     for n in ['payment','travel_cost','hours']:number(o[n],n)
    state['material_remaining']=p['material_units']
    effect=dict(deepcopy(p),remaining_material_units=state['material_remaining'])
   elif kind=='PEER_ROOT':
    require(actor!=state['actor_id'] and p.get('permission')=='RESEARCH_HISTORY_ONLY','PEER_NOT_INDEPENDENT')
    require(p.get('kinship')=='NON_KIN','PEER_KINSHIP_NOT_ISSUED')
    state['tools_remaining']=number(p.get('tool_units'),'tool_units')
    effect=dict(peer_id=actor,tool_units=state['tools_remaining'],remaining_tools=state['tools_remaining'],goal=p.get('goal'))
   elif kind=='SCHOOLING':
    root=get({'ORIGIN_FAMILY'},owner=actor)
    hours=number(p.get('hours'),'hours',1);require(hours<=state['free_hours'],'TRAINING_TIME_UNAVAILABLE')
    state['skill']=hours//2;state['free_hours']-=hours
    effect=dict(skill=state['skill'],role=root['role'],hours=hours)
   elif kind=='WORK_POSITION':
    skill=get({'SCHOOLING','WORK_POSITION'},'skill',owner=actor)
    hours=number(p.get('hours'),'hours',1);wage=number(p.get('wage'),'wage')
    require(skill>=2 and hours<=state['free_hours'],'WORK_CAPABILITY_OR_TIME_MISSING')
    earned=hours*wage;state['cash']+=earned;state['free_hours']-=hours
    require(p.get('material_position')=='waged_'+state['role'],'UNISSUED_MATERIAL_POSITION')
    state['material_position']=p.get('material_position')
    effect=dict(skill=skill+hours//2,earned=earned,cash=state['cash'],role=state['role'],hours=hours)
    state['skill']=effect['skill']
   elif kind=='PROJECT':
    work=get({'WORK_POSITION'},owner=actor);world=get({'WORLD_MATERIAL'},owner='G15_WORLD')
    units=min(work['skill']//2,state['material_remaining'],state['free_hours'])
    require(units>0 and world['project_permit'],'PROJECT_NOT_PERFORMABLE_OR_MATERIAL_EXHAUSTED')
    expected=dict(completed_units=units,payment=units*world['unit_payment'],materials_used=units)
    require(p.get('project')==world['project_id'] and p.get('durable_effect')==expected,'PROJECT_PERFORMANCE_CLAIM_MISMATCH')
    state['cash']+=expected['payment'];state['free_hours']-=units;state['completed_units']+=units
    state['material_remaining']-=units;state['projects'].append(world['project_id'])
    effect=dict(**expected,project=world['project_id'],role=work['role'],cash=state['cash'],remaining_material_units=state['material_remaining'])
   elif kind=='PEER_PROJECT':
    root=get({'PEER_ROOT'},owner=actor);world=get({'WORLD_MATERIAL'},owner='G15_WORLD')
    require(root['goal']=='restore_shared_tools' and world['tool_return_permit'],'PEER_PROJECT_NOT_PERMITTED')
    effect=dict(peer_id=actor,tool_units=root['tool_units'],remaining_tools=state['tools_remaining'],project=root['goal'])
   elif kind=='PEER_ACTION':
    project=get({'PEER_PROJECT'},owner=actor)
    units=number(p.get('returned_units'),'returned_units',1)
    require(p.get('performed') is True,'PEER_ACTION_NOT_PERFORMED')
    require(units<=state['tools_remaining'],'PEER_TOOLS_UNAVAILABLE')
    state['tools_remaining']-=units
    effect=dict(peer_id=actor,returned_units=units,remaining_units=state['tools_remaining'],project=project['project'])
   elif kind=='NONMOTHER_RELATIONSHIP':
    project=get({'PROJECT'},owner=actor);peer=get({'PEER_ACTION'})
    cp=p.get('counterpart');require(isinstance(cp,str) and cp and cp==peer['peer_id'] and cp!=actor,'COUNTERPART_IDENTITY_MISSING_OR_WRONG')
    expected=dict(returned_units=peer['returned_units'],obligation_units=min(project['completed_units'],peer['returned_units']))
    require(p.get('durable_effect')==expected and p.get('relation_kind')=='nonkin_reciprocal_tool_work','NONKIN_PERFORMANCE_MISMATCH')
    state['debt_units']=expected['obligation_units'];state['nonmother_relations'].append(cp)
    effect=dict(**expected,counterpart=cp)
   elif kind=='PRACTICE_FORMATION':
    project=get({'PROJECT'},owner=actor);require(project['completed_units']>=2,'INSUFFICIENT_PERFORMED_PRACTICE')
    require(p.get('causal_event_refs')==parents,'PRACTICE_SOURCE_MISMATCH')
    expected='scheduled_'+project['role']+'_ledger_discipline'
    require(p.get('practice')==expected,'PRACTICE_NOT_DERIVED')
    state['practices'].append(expected);effect=dict(practice=expected,checks=project['completed_units'],role=project['role'])
   elif kind=='ATTITUDE_FORMATION':
    project=get({'PROJECT'},owner=actor);relation=get({'NONMOTHER_RELATIONSHIP'},owner=actor)
    require(p.get('causal_event_refs')==parents,'ATTITUDE_SOURCE_MISMATCH')
    require(p.get('attitude')=='reciprocity_in_work_obligations','ATTITUDE_NOT_DERIVED')
    state['attitudes'].append(p['attitude']);effect=dict(attitude=p['attitude'],reciprocity_units=min(project['completed_units'],relation['obligation_units']))
   elif kind=='MEMORY_TRACE':
    ref=p.get('experienced_basis_event');require(ref in parents,'EXPERIENCE_NOT_DIRECT_PARENT')
    require(ref in admitted and admitted[ref]['owner_id']==actor and admitted[ref]['kind'] in {'PROJECT','NONMOTHER_RELATIONSHIP','WORK_POSITION'},'EXPERIENCE_NOT_PERFORMED_BY_SUBJECT')
    effect=dict(experienced_basis_event=ref,experienced_effect=get({admitted[ref]['kind']},owner=actor))
   elif kind=='STRIVING':
    work=get({'WORK_POSITION'},owner=actor);project=get({'PROJECT'},owner=actor)
    goal='fund_'+state['role']+'_equipment'
    require(p.get('striving')==goal and p.get('causal_event_refs')==parents,'STRIVING_NOT_DERIVED')
    effect=dict(striving=goal,budget=min(work['earned'],project['payment']),role=state['role'])
   elif kind=='ORGANISMIC_EVENT':
    work=get({'WORK_POSITION'},owner=actor);rest=number(p.get('rest_hours'),'rest_hours')
    recovered=rest>=work['hours']//2;state['health']='recovered' if recovered else 'fatigued'
    effect=dict(recovered=recovered,rest_hours=rest)
   elif kind=='ROUTE_AVAILABILITY':
    work=get({'WORK_POSITION'},owner=actor);world=get({'WORLD_MATERIAL'},owner='G15_WORLD');goal=get({'STRIVING'},owner=actor)
    offer=world['offers'].get(p.get('route'));require(offer is not None,'WORLD_OFFER_ABSENT')
    effect=dict(route=p['route'],offer=offer,net=offer['payment']-offer['travel_cost'],goal=goal['striving'],skill=work['skill'])
   elif kind in {'COMMISSIONED_WORK','ENROLLMENT','COMMUNITY_CALLOUT','MOBILITY_HISTORY'}:
    work=get({'WORK_POSITION'},owner=actor);project=get({'PROJECT'},owner=actor);practice=get({'PRACTICE_FORMATION'},owner=actor)
    route=get({'ROUTE_AVAILABILITY'},owner=actor);health=get({'ORGANISMIC_EVENT'},owner=actor)
    offer=route['offer'];require(offer['permit'] and health['recovered'] and offer['hours']<=state['free_hours'] and offer['travel_cost']<=state['cash'],'ROUTE_ACTION_NOT_PERMITTED')
    require(work['skill']>=2 and project['completed_units']>=2 and practice['checks']>=2,'ROUTE_CAPABILITY_MISSING')
    require(p.get('place')==offer['place'],'ROUTE_PLACE_CLAIM_MISMATCH')
    state['cash']+=route['net'];state['free_hours']-=offer['hours'];state['place']=offer['place'];state['availability_status']='available_for_encounter'
    effect=dict(place=state['place'],route=route['route'],cash=state['cash'],free_hours=state['free_hours'],net=route['net'])
   elif kind=='ENDPOINT_STATE':
    prior=get({'COMMISSIONED_WORK','ENROLLMENT','COMMUNITY_CALLOUT','MOBILITY_HISTORY'},owner=actor)
    require(p.get('place')==prior['place'],'ENDPOINT_ASSERTION_WITHOUT_ANTECEDENT')
    require(p.get('availability_status')==state['availability_status'],'ENDPOINT_AVAILABILITY_OVERWRITE_ATTEMPT')
    effect=dict(place=state['place'],availability_status=state['availability_status'])
   else:raise HistoryFault('UNREGISTERED_EVENT_KIND:'+str(kind))
  except (HistoryFault,KeyError,TypeError,ValueError) as exc:
   state=before;fail(str(exc),e);continue
  admitted[eid]=e;effects[eid]=effect
  witnesses.append(dict(event_id=eid,kind=kind,owner_id=actor,effective_index=idx,readset=readset,before=before,after=deepcopy(state),effect=deepcopy(effect)))
 return dict(valid=not errors and bool(admitted),errors=errors,state=state,effects=effects,admitted=admitted,value_witnesses=witnesses,history_hash=h_obj(events),transition_version=VERSION)


def derive_psyche(events):
 r=replay_history(events);out={d:[] for d in FORMATION}
 for d,(kind,field) in FORMATION.items():
  for e in events:
   if e['event_id'] in r['admitted'] and e['kind']==kind:
    out[d].append({field:e['payload'][field], 'formation_event_ref':e['event_id'],
       'causal_event_refs':[e['event_id']]+e['causal_parent_event_ids'],
       'formed_value':deepcopy(r['effects'][e['event_id']])})
 return out


def validate_psyche(events,psyche,replay=None):
 r=replay or replay_history(events);expected=derive_psyche(events)
 errors=[]
 if not isinstance(psyche,dict):return ['PSYCHE_NOT_TYPED']
 for d in FORMATION:
  if not expected[d] or psyche.get(d)!=expected[d]:errors.append('PSYCHE_FORMATION_UNRESOLVED:'+d)
 return errors


class PersonHistoryBuilder:
 """An explicit finite research world, varied material inputs, forward transitions.

 The person pursues equipment finance; the peer pursues tool recovery. The most
 useful available contract is chosen from net pay under actual time/cash/permit.
 Endpoint constraints are never an input to this class.
 """
 def __init__(self,actor,seed,role='repair',material=None):
  self.actor=actor;self.seed=seed;self.role=role;self.material=material;self.events=[]
 def add(self,kind,payload,parents=(),actor=None):
  e=make_event(len(self.events),kind,actor or self.actor,payload,[x['event_id'] for x in parents]);self.events.append(e);return e
 def build(self):
  variation=int(h_obj(self.seed).split(':')[-1][:4],16)%3
  root=self.add('ORIGIN_FAMILY',dict(permission='RESEARCH_HISTORY_ONLY',role=self.role,cash=30+variation,free_hours=30))
  offers={route:dict(place=place,payment=pay,travel_cost=cost,hours=2,permit=True) for route,(place,pay,cost) in ROUTES.items()}
  world=dict(permission='SOURCEFREE_MATERIAL_ONLY',project_id=('communal_irrigation_pump_repair' if self.role=='repair' else 'apprentice_finishing_work'),material_units=5,unit_payment=2,project_permit=True,tool_return_permit=True,offers=offers)
  if self.material is not None:world=deepcopy(self.material)
  w=self.add('WORLD_MATERIAL',world,actor='G15_WORLD')
  peer_id='G15_NONKIN_'+h_obj(dict(actor=self.actor,seed=self.seed)).split(':')[-1]
  peer=self.add('PEER_ROOT',dict(permission='RESEARCH_HISTORY_ONLY',kinship='NON_KIN',tool_units=3,goal='restore_shared_tools'),actor=peer_id)
  school=self.add('SCHOOLING',dict(hours=8),[root])
  work=self.add('WORK_POSITION',dict(hours=4,wage=2,material_position='waged_'+self.role),[school])
  # These are computed proposals; replay independently recomputes and checks them.
  prior=replay_history(self.events)
  units=min(prior['state']['skill']//2,world['material_units'],prior['state']['free_hours'])
  project=self.add('PROJECT',dict(project=world['project_id'],nonmother=True,consequential=True,durable_effect=dict(completed_units=units,payment=units*world['unit_payment'],materials_used=units)),[work,w])
  pp=self.add('PEER_PROJECT',{},[peer,w],actor=peer_id)
  pa=self.add('PEER_ACTION',dict(returned_units=2,performed=True),[pp],actor=peer_id)
  rel=self.add('NONMOTHER_RELATIONSHIP',dict(counterpart=peer_id,relation_kind='nonkin_reciprocal_tool_work',nonmother=True,consequential=True,durable_effect=dict(returned_units=2,obligation_units=min(units,2))),[project,pa])
  practice=self.add('PRACTICE_FORMATION',dict(practice='scheduled_'+self.role+'_ledger_discipline',causal_event_refs=[project['event_id']]),[project])
  attitude=self.add('ATTITUDE_FORMATION',dict(attitude='reciprocity_in_work_obligations',causal_event_refs=[project['event_id'],rel['event_id']]),[project,rel])
  self.add('MEMORY_TRACE',dict(experienced_basis_event=project['event_id']),[project])
  self.add('MEMORY_TRACE',dict(experienced_basis_event=rel['event_id']),[rel])
  goal=self.add('STRIVING',dict(striving='fund_'+self.role+'_equipment',causal_event_refs=[work['event_id'],project['event_id']]),[work,project])
  health=self.add('ORGANISMIC_EVENT',dict(rest_hours=3),[work])
  available=[]
  for route,o in sorted(world['offers'].items()):
   avail=self.add('ROUTE_AVAILABILITY',dict(route=route,via=o['place']),[work,w,goal]);available.append(avail)
  # Actual prior resources choose a material opportunity. Absence is lawful.
  r=replay_history(self.events)
  lawful=[e for e in available if e['event_id'] in r['effects'] and r['effects'][e['event_id']]['offer']['permit'] and r['effects'][e['event_id']]['offer']['hours']<=r['state']['free_hours'] and r['effects'][e['event_id']]['offer']['travel_cost']<=r['state']['cash']]
  if not r['valid'] or not lawful:return self.events
  chosen=max(lawful,key=lambda e:(r['effects'][e['event_id']]['net'],e['payload']['route']))
  route=chosen['payload']['route'];kind={'ROUTE_LOCAL_CLOSED':'COMMISSIONED_WORK','ROUTE_INSTITUTIONAL':'ENROLLMENT','ROUTE_UNCONVENTIONAL':'COMMUNITY_CALLOUT','ROUTE_MOBILITY':'MOBILITY_HISTORY'}[route]
  attendance=self.add(kind,dict(place=chosen['payload']['via'],workplace=chosen['payload']['via']),[work,project,practice,chosen,health])
  self.add('ENDPOINT_STATE',dict(place=chosen['payload']['via'],availability_status='available_for_encounter'),[attendance])
  return self.events


def independent_actions(events,psyche):
 """New non-mother situations consume formed ability, motivation and peer debt.
 The returned state delta is numeric; a denied action has no performed effect.
 """
 r=replay_history(events);pe=validate_psyche(events,psyche,r);s=r['state'];probes=[]
 for pid in ['PROBE_P1_WORK_COLLECTIVE_OBLIGATION','PROBE_P2_FRIENDSHIP_CONFLICT']:
  needed='PROJECT' if pid.startswith('PROBE_P1') else 'NONMOTHER_RELATIONSHIP'
  basis=[e for e in events if e['kind']==needed and e['event_id'] in r['admitted']]
  capable=r['valid'] and not pe and bool(basis) and s['skill']>=4 and s['free_hours']>=1
  if needed=='PROJECT':
   capable=capable and s['role']=='repair' and s['completed_units']>=2
   # Concrete work and expenditure, not an authored verbal endpoint.
   delta=dict(cash=2,free_hours=-1,completed_units=1) if capable else {}
  else:
   capable=capable and s['debt_units']>0
   delta=dict(debt_units=-min(1,s['debt_units']),free_hours=-1) if capable else {}
  after=deepcopy(s)
  for k,v in delta.items():after[k]+=v
  readset=[w for w in r['value_witnesses'] if w['kind'] in {needed,'PRACTICE_FORMATION','ATTITUDE_FORMATION','STRIVING','PEER_ACTION'}]
  action=dict(status='PERFORMED' if capable else 'REFUSED',decision=('PERFORM_BOUNDED_REPAIR' if needed=='PROJECT' else 'SETTLE_ONE_PEER_OBLIGATION_UNIT') if capable else None,state_change_refs=[e['event_id'] for e in basis] if capable else [],before=deepcopy(s),after=after,delta=delta,readset=readset)
  probes.append(dict(probe_id=pid,mom_or_child_in_prompt=False,pass_=bool(capable),typed_action=action,acted_from_actor_state_without_mom_prompt=bool(capable),typed_causal_effect_record=dict(effect=delta,causal_basis_events=action['state_change_refs']),supporting_evidence=readset,generic_attitude_tags_insufficient=True,is_prose_only=False,third_party_relationship_actor_specific=bool(capable)))
  probes[-1]['pass']=probes[-1].pop('pass_')
 return dict(probes=probes,n_probes=2,n_pass=sum(x['pass'] for x in probes),heldout_independence_pass=all(x['pass'] for x in probes),probe_version=VERSION,validation_errors=r['errors']+pe)
