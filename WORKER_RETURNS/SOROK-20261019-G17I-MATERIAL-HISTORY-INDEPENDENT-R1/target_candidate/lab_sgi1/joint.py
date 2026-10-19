"""Separately owned source-free material event and two performed adult actions.

This research observer is not an ADP010/019 issuer. No trust from a denial string,
solo co-presence, narrator, or hash prefix. Replay re-executes both actor actions.
"""
from copy import deepcopy
from .core import h_obj
from .history import replay_history,derive_psyche,validate_psyche
JOINT_OWNER='G15_INDEPENDENT_MATERIAL_OBSERVER'
JOINT_REGISTRY=dict(owner_id=JOINT_OWNER,scope='SOURCEFREE_RESEARCH_ONLY',native_grant='NOT_GRANTED',rule='TWO_PROJECT_TASK_EXCHANGE_R1')


def material_joint_opportunity(effective_index=100,permit=True,units=1):
 p=dict(owner_id=JOINT_OWNER,permission='RESEARCH_JOINT_WITNESS_ONLY',effective_index=effective_index,
        place='INST_WORKSHOP_A',material_units=units,payment_per_actor=2,task_hours=1,permit=permit)
 return dict(event_id=h_obj(p),**p)


def perform_participation(events,material):
 r=replay_history(events);s=r['state'];actor=s['actor_id']
 lawful=(r['valid'] and not validate_psyche(events,derive_psyche(events),r)
         and material.get('owner_id')==JOINT_OWNER and material.get('permission')=='RESEARCH_JOINT_WITNESS_ONLY'
         and type(material.get('effective_index')) is int and material['effective_index']>max((e['effective_index'] for e in events),default=-1)
         and material.get('place')==s['place'] and material.get('permit') is True
         and type(material.get('task_hours')) is int and 0<material['task_hours']<=s['free_hours']
         and type(material.get('material_units')) is int and material['material_units']>0
         and type(material.get('payment_per_actor')) is int and material['payment_per_actor']>0)
 source=[w for w in r['value_witnesses'] if w['kind'] in {'PROJECT','STRIVING','PRACTICE_FORMATION','COMMISSIONED_WORK'}]
 lawful=lawful and {w['kind'] for w in source}>={'PROJECT','STRIVING','PRACTICE_FORMATION','COMMISSIONED_WORK'}
 after=deepcopy(s)
 if lawful:
  after['cash']+=material['payment_per_actor'];after['free_hours']-=material['task_hours'];after['completed_units']+=material['material_units']
 action=dict(owner_id=actor,kind='PARTICIPATION_ACTION',status='PERFORMED' if lawful else 'REFUSED',
             effective_index=(material.get('effective_index',-2)+1),history_hash=r['history_hash'],material_event_ref=material.get('event_id'),
             causal_parent_event_ids=[w['event_id'] for w in source]+[material.get('event_id')],before=s,after=after,values_read=source)
 return dict(event_id=h_obj(action),**action)


def observe_joint_actions(anchor,dad_events,material):
 maternal=anchor.get('history_events',[]);a=perform_participation(maternal,material);b=perform_participation(dad_events,material)
 valid=(a['status']==b['status']=='PERFORMED' and a['owner_id']!=b['owner_id']
        and a['owner_id']==anchor.get('actor_id')
        and a['after']['completed_units']>a['before']['completed_units']
        and b['after']['completed_units']>b['before']['completed_units']
        and material.get('event_id')==h_obj({k:v for k,v in material.items() if k!='event_id'}))
 body=dict(owner_id=JOINT_OWNER,registry_hash=h_obj(JOINT_REGISTRY),kind='JOINT_TASK_WITNESS',
           status='WITNESSED' if valid else 'REFUSED',effective_index=material.get('effective_index',-3)+2,
           causal_parent_event_ids=[material.get('event_id'),a['event_id'],b['event_id']],
           material=deepcopy(material),actions=[a,b],participants=[a['owner_id'],b['owner_id']],
           maternal_history_hash=h_obj(maternal),paternal_history_hash=h_obj(dad_events))
 return dict(event_id=h_obj(body),**body)


def validate_joint(anchor,dad_events,evidence):
 if not isinstance(evidence,dict) or evidence.get('owner_id')!=JOINT_OWNER:return False
 expected=observe_joint_actions(anchor,dad_events,evidence.get('material',{}))
 return evidence==expected and expected['status']=='WITNESSED'


def observe_continued_contact(relation,continuations,material):
    """A second task contact, witnessed only after both independent continuations.
    No relationship persistence is presumed from the first contact alone.
    """
    obj=relation.get('objective_relation',{})
    participants=obj.get('participants',[])
    valid=(relation.get('relationship_committed') is True and len(participants)==2
        and len(continuations)==2 and {e['actor'] for e in continuations}==set(participants)
        and material.get('owner_id')==JOINT_OWNER and material.get('permission')=='RESEARCH_JOINT_WITNESS_ONLY'
        and material.get('event_id')==h_obj({k:v for k,v in material.items() if k!='event_id'})
        and type(material.get('effective_index')) is int
        and material['effective_index']>max([e['effective_index'] for e in continuations]+[obj.get('witness',{}).get('effective_index',-1)])
        and material.get('event_id') not in obj.get('shared_event_refs',[])
        and material.get('permit') is True)
    actions=[]
    for e in continuations:
        before=e['payload']['after'];after=deepcopy(before)
        allowed=(valid and before['place']==material.get('place')
                 and type(material.get('task_hours')) is int and 0<material['task_hours']<=before['free_hours']
                 and type(material.get('material_units')) is int and material['material_units']>0
                 and type(material.get('payment_per_actor')) is int and material['payment_per_actor']>0)
        if allowed:
            after['cash']+=material['payment_per_actor'];after['free_hours']-=material['task_hours'];after['completed_units']+=material['material_units']
        a=dict(owner_id=e['actor'],effective_index=material.get('effective_index',-2)+1,kind='CONTINUED_CONTACT_ACTION',
               status='PERFORMED' if allowed else 'REFUSED',causal_parent_event_ids=[e['event_id'],material.get('event_id')],before=before,after=after)
        actions.append(dict(event_id=h_obj(a),**a))
    body=dict(kind='WITNESSED_RELATION_CONTINUATION',owner_id=JOINT_OWNER,
        effective_index=material.get('effective_index',-3)+2,
        causal_parent_event_ids=obj.get('shared_event_refs',[])+[a['event_id'] for a in actions]+[material.get('event_id')],
        status='WITNESSED' if valid and len(actions)==2 and all(a['status']=='PERFORMED' for a in actions) else 'NO_CHANGE',
        previous_relation_ref=obj.get('relation_id'),previous_witness_refs=obj.get('shared_event_refs',[]),
        material_source=deepcopy(material),actions=actions,household_admission='NOT_GRANTED',parenthood_admission='NOT_GRANTED')
    return dict(event_id=h_obj(body),**body)


def joint_event_closure(relation,continuation):
    closure=[]
    witness=relation.get('objective_relation',{}).get('witness')
    if witness and witness.get('status')=='WITNESSED':
        material=witness['material']
        closure.extend([dict(material,causal_parent_event_ids=[]),*witness['actions'],witness])
    later=continuation.get('research_relation_continuation')
    if later and later.get('status')=='WITNESSED':
        closure.extend([dict(later['material_source'],causal_parent_event_ids=[]),*later['actions'],later])
    return closure
