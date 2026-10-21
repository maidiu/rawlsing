"""Event-based adult project continuation; child exposure and household stay held."""
from copy import deepcopy
from .core import h_obj,S
from .history import replay_history,derive_psyche,validate_psyche
CONTINUATION_VERSION='G15_VALUE_CONTINUATION_R1'


def lab_conception_boundary():
 return dict(marker_id='LAB_CONCEPTION_BOUNDARY',marker_semantics=S.LAB_CONCEPTION_BOUNDARY,target_status='PENDING_NOT_ADMITTED_CONCEPTION',child_generated_events=0,birth_alias=False,gestation_birth_semantics='HOLD_NO_ADOPTED_BIOLOGICAL_AUTHORITY',missing_authority=['CONCEPTION_BIOLOGY_AUTHORITY_HOLD'])


def _authenticated_participation(events,state,participation,material_event,history_hash):
 """Authenticate a performed action from the source-issued receipt.

 A caller-supplied before/after, owner, permission or payment is not evidence.
 The material packet must carry the fixture-origin receipt, the action must carry
 the source-issued performed-action receipt bound to that exact material event,
 and the afterstate is recomputed from the verified material schedule.
 """
 from .joint import verify_material_source, verify_performed_action
 if not isinstance(material_event,dict):return None
 accepted,reason,payload=verify_material_source(material_event)
 if not accepted:return None
 accepted,reason=verify_performed_action(participation,material_event)
 if not accepted:return None
 if (participation.get('owner_id')!=state['actor_id']
     or participation.get('history_hash')!=history_hash
     or participation.get('status')!='PERFORMED'
     or participation.get('before')!=state):return None
 if participation.get('material_event_ref')!=material_event.get('event_id'):return None
 idx=participation.get('effective_index')
 if type(idx) is not int or idx>=1000:return None
 expected=deepcopy(state)
 expected['cash']+=payload['payment_per_actor']
 expected['free_hours']-=payload['task_hours']
 expected['completed_units']+=payload['material_units']
 if participation.get('after')!=expected:return None
 return expected


def continue_person(events,opportunity=None,participation=None,material_event=None):
 r=replay_history(events);s=deepcopy(r['state']);p=derive_psyche(events);reasons=validate_psyche(events,p,r)
 participation_refs=[]
 if participation is not None:
  # An actual performed action must be authenticated by its source-issued
  # material and action receipts and a recomputed after-state. A caller-supplied
  # after-state is not evidence; it cannot add cash or precede the clock.
  expected=_authenticated_participation(events,s,participation,material_event,r['history_hash'])
  if expected is None:return None
  s=expected
  participation_refs=[participation['event_id']]
 if any(e['effective_index']>=1000 for e in events):return None
 project=[w for w in r['value_witnesses'] if w['kind']=='PROJECT'];goal=[w for w in r['value_witnesses'] if w['kind']=='STRIVING']
 # Continuation opportunities are exact earlier world source facts. The live
 # candidate does not invent a follow-up job to fill an empty history/year.
 worlds=[e for e in events if e['kind']=='WORLD_MATERIAL' and e['event_id'] in r['admitted']]
 if not r['valid'] or reasons or not project or not goal or not worlds:return None
 w=worlds[-1];remaining=project[-1]['effect'].get('remaining_material_units',0)
 # Unused material can support continuing work; absence produces lawful NO_CHANGE.
 budget=goal[-1]['effect']['budget'];units=min(remaining,s['free_hours'],budget)
 if opportunity is not None:
  if (not isinstance(opportunity,dict) or opportunity.get('source_ref')!=w['event_id']
      or opportunity.get('permit') is not True or type(opportunity.get('units')) is not int):return None
  units=min(units,opportunity['units'])
 if units<=0:return None
 after=deepcopy(s);earned=units*w['payload']['unit_payment'];after['cash']+=earned;after['free_hours']-=units;after['completed_units']+=units
 if 'material_remaining' in after:after['material_remaining']=max(0,after['material_remaining']-units)
 body=dict(kind='PARENT_CONTINUATION',actor=s['actor_id'],owner_id=s['actor_id'],effective_index=1000,
            causal_parent_event_ids=[project[-1]['event_id'],goal[-1]['event_id'],w['event_id']]+participation_refs,
            history_hash=r['history_hash'],payload=dict(project_change=project[-1]['effect']['project'],
            goal=goal[-1]['effect']['striving'],units_performed=units,earned=earned,before=s,after=after,
            values_read=[project[-1],goal[-1],dict(event_id=w['event_id'],owner_id=w['owner_id'],path='payload',value=w['payload'])]+([dict(event_id=participation['event_id'],owner_id=participation['owner_id'],path='after',value=participation['after'])] if participation is not None else [])))
 return dict(event_id=h_obj(body),**body)


def forward_continuation(anchor,dad_events,relation,contact_material=None):
 from .joint import validate_joint
 witness=relation.get('objective_relation',{}).get('witness')
 joint_valid=validate_joint(anchor,dad_events or [],witness)
 actions={a['owner_id']:a for a in witness['actions']} if joint_valid else {}
 material_event=witness.get('material') if witness else None
 mom=continue_person(anchor.get('history_events',[]),participation=actions.get(anchor['actor_id']),material_event=material_event)
 dad_actor=replay_history(dad_events or [])['state']['actor_id']
 dad=continue_person(dad_events or [],participation=actions.get(dad_actor),material_event=material_event)
 # Continuing as an adult does not depend on being in a relationship. The role
 # label here is a historical API alias, not an admitted parenthood fact.
 events=[e for e in [mom,dad] if e]
 rel_ok=False
 if relation.get('relationship_committed'):
  from .joint import validate_joint
  obj=relation.get('objective_relation',{})
  rel_ok=validate_joint(anchor,dad_events or [],obj.get('witness'))
 later=None
 if contact_material is not None:
  from .joint import observe_continued_contact
  later=observe_continued_contact(relation,events,contact_material)
 return dict(continuation_version=CONTINUATION_VERSION,continuation_events=events,
  research_relation_continuation=later,
  both_parents_continue_independently=bool(mom and dad),maternal_continuation_admitted=bool(mom),paternal_continuation_admitted=bool(dad),
  relationship_continuation_admitted=bool(later and later['status']=='WITNESSED'),previous_task_contact_resolves=rel_ok,
  parental_status='NOT_GRANTED',household_admission='NOT_GRANTED',
  paternal_continuation_requires_supplied_history=True,parent_project_change_registered_as_event=bool(events),
  care_or_absence_registered_as_event=False,no_fixed_family_labels=True,unformed_actor_continuation_minted=False,
  typed_hold=dict(hold_state='NO_RELATIONSHIP_OR_PARENTAL_CONTINUATION_OWNER_GRANT',hold_reasons=['SEPARATE_RELATIONSHIP_CONTINUATION_REQUIRED','NO_HOUSEHOLD_ADMISSION','NO_CHILD_EXPOSURE_ADMISSION']))


def child_developmental_environment_fixture(anchor,dad_events,continuation,boundary):
 # Potential context is explicit; it is never a positive child exposure or uptake.
 contexts=[]
 for e in continuation.get('continuation_events',[]):
  if e['kind']!='PARENT_CONTINUATION':continue
  contexts.append(dict(context_id=h_obj(dict(event=e['event_id'],kind='POTENTIAL_ADULT_CONTEXT')),actor=e['actor'],material_context=dict(project=e['payload']['project_change'],earned=e['payload']['earned'],cash_after=e['payload']['after']['cash']),causal_parent_events=[e['event_id']],effective_after_admission=False))
 later=continuation.get('research_relation_continuation')
 if later and later['status']=='WITNESSED':
  for context in contexts:
   action=next(a for a in later['actions'] if a['owner_id']==context['actor'])
   context['material_context']['cash_after']=action['after']['cash']
   context['causal_parent_events']+=[later['event_id'],action['event_id']]
 return dict(fixture_kind='LAB_CHILD_DEVELOPMENTAL_ENVIRONMENT_FIXTURE',fixture_id=h_obj(contexts),is_admitted_child_actor=False,is_PREV3_parent_object=False,child_generated_events=0,lab_conception_boundary=boundary['marker_id'],birth_alias=False,
  exposures=[],potential_material_contexts=contexts,exposure_changes_only_after_admission=True,personality_assigned_from_parent_profile=False,
  developmental_effects_mechanism='NOT_EXECUTED_CHILD_EXPOSURE_AND_UPTAKE_NOT_GRANTED',lab_rule='PROVISIONAL_LAB_RULE__NOT_ADOPTED')
