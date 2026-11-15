"""Witnessed research relation; independently situated adults, no family issuance."""
from .core import typed,S,h_obj
from .history import replay_history
from .joint import validate_joint
RELATION_VERSION='G15_JOINT_RELATION_R1'
FORMING_WITNESS_KINDS=frozenset({'JOINT_TASK_WITNESS'})

def _actual_second_parent_actor(events):
 roots=[e for e in events or [] if e.get('kind')=='ORIGIN_FAMILY']
 if len(roots)!=1:return None
 actors=roots[0].get('actors') or []
 return actors[0] if len(actors)==1 and isinstance(actors[0],str) and actors[0] else None

def reconcile(anchor,dad_events,scenario,force_mom_affectionate_dad_unknown=False):
 known=anchor.get('known_counterpart_identity_ref_or_null');dad=_actual_second_parent_actor(dad_events)
 if known and (scenario.get('candidate_kind')!='KNOWN_COUNTERPART' or dad!=known):
  return typed(S.SHARED_HISTORY_CONTRADICTION_HOLD,reason='REUSE_EXACT_ACTOR_AND_RESOLVABLE_HISTORY',mother_history_unchanged=True,unapproved_rng_draws=0)
 r=replay_history(dad_events or []);m=replay_history(anchor.get('history_events',[]));evidence=scenario.get('joint_evidence')
 reasons=[]
 if not dad_events:reasons.append('NO_SECOND_PARENT_HISTORY_SUPPLIED')
 if not dad or dad==anchor.get('actor_id'):reasons.append('SECOND_PARENT_ACTOR_IDENTITY_ABSENT_OR_REUSED')
 if not r['valid'] or not m['valid']:reasons.append('INDEPENDENT_HISTORIES_NOT_RESOLVED')
 if not validate_joint(anchor,dad_events or [],evidence):reasons.append('NO_FORMING_WITNESS_EVENT')
 if reasons:return typed(S.NOT_EXECUTED_AUTHORITY_HOLD,relationship_committed=False,hold_reasons=reasons,n_forming_witnesses=0,actor_id_minted=False,mother_history_unchanged=True,unapproved_rng_draws=0)
 relation_id=h_obj(dict(actors=sorted([anchor['actor_id'],dad]),witness=evidence['event_id']))
 # A specific task exchange earns a contact relationship. No romance/reciprocity
 # psychological state follows from this material event.
 perceived=[dict(perceiver=a,target=b,perceived_state='UNKNOWN_OR_NONRECIPROCAL',causal_basis='NO_PSYCHIC_RELATION_OWNER_GRANT') for a,b in [(anchor['actor_id'],dad),(dad,anchor['actor_id'])]]
 return dict(relation_version=RELATION_VERSION,status=S.COMMITTED,relationship_committed=True,
   science_grade='SOURCEFREE_WITNESSED_TASK_RELATION_ONLY',
   objective_relation=dict(relation_id=relation_id,participants=[anchor['actor_id'],dad],relation_kind='witnessed_task_contact',
     admission_basis='TWO_PERFORMED_PROJECT_ACTIONS_AND_SEPARATE_MATERIAL_OBSERVER',shared_event_refs=[evidence['event_id']],
     witness=evidence,maternal_history_hash=h_obj(anchor['history_events']),paternal_history_hash=h_obj(dad_events),
     single_objective_record=True),perceived_states=perceived,reciprocity_inferred=False,
   household_membership_auto=False,household_membership_requires_separate_admission=True,
   conception_is_not_relationship=True,second_parent_history_required=True,forming_witness_required=True,
   identity_reuse_check=dict(duplicate_actor_minted=False,known_counterpart_identity_ref_or_null=known),
   native_ADP015_grant='NOT_GRANTED')
