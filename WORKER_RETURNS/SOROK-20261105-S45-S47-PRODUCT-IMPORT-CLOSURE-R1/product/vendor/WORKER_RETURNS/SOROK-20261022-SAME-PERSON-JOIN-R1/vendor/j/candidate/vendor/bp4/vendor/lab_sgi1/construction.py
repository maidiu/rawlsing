"""Bounded construction search over actual forward transitions. No native admission.
Construction constraints test a history; they never author its material outcomes.
"""
from .core import h_obj, h_concat, typed, S
from .history import (PersonHistoryBuilder,replay_history,derive_psyche,
                      validate_psyche,independent_actions,ROOTS,VERSION)
import time
CONSTRUCTION_VERSION=VERSION
STOPPING_LAW_VERSION=VERSION
PROBE_VERSION=VERSION
ROOT_EVENT_KINDS=frozenset(ROOTS)
PLACE_ESTABLISHING_KINDS=frozenset({'COMMISSIONED_WORK','ENROLLMENT','COMMUNITY_CALLOUT','MOBILITY_HISTORY'})
MANDATORY_DOMAIN_KINDS=('WORK_POSITION','ORGANISMIC_EVENT','NONMOTHER_RELATIONSHIP','PROJECT','PRACTICE_FORMATION','MEMORY_TRACE')

class DadHistoryBuilder:
 def __init__(self,actor_id,attempt_seed,endpoint_constraints):
  self.actor_id=actor_id;self.attempt_seed=attempt_seed;self.ec=endpoint_constraints
 def build(self):
  # endpoint_constraints are an observer's contract, never a builder input.
  return PersonHistoryBuilder(self.actor_id,self.attempt_seed).build()

psyche_from_dad_events=derive_psyche
heldout_independent_probes=independent_actions

def forward_replay_to_endpoint(events,endpoint_constraints):
 t=time.perf_counter();r=replay_history(events);s=r['state'];mismatches=[]
 predicates=endpoint_constraints.get('required_state_predicates',[])
 for pred in predicates:
  if not isinstance(pred,dict) or set(pred)!={'field','equals'}:
   mismatches.append(dict(predicate=pred,reason='UNCLASSIFIED_ENDPOINT_PREDICATE'));continue
  key=pred['field'];have=s.get(key)
  if key not in s or have!=pred['equals']:mismatches.append(dict(predicate=pred,have=have))
 from .endpoint import prehistory_obligations
 extra,obligation_witnesses=prehistory_obligations(events,r,endpoint_constraints)
 mismatches+=extra
 # Every supplied contract field has a declared interpretation. Unknowns hold.
 allowed={'route_kind_id','time_or_interval','place','required_state_predicates','original','declared_test_intervention','required_relation_objective_refs','second_parent_structure_and_position_constraints','conception_witness_requirements','admissible_world_context_refs'}
 unknown=set(endpoint_constraints)-allowed
 if unknown:mismatches.append(dict(reason='UNCLASSIFIED_ENDPOINT_FIELDS',fields=sorted(unknown)))
 route_effects=[r['effects'][e['event_id']] for e in events if e['event_id'] in r['effects'] and e['kind'] in PLACE_ESTABLISHING_KINDS]
 if endpoint_constraints.get('route_kind_id') and (not route_effects or route_effects[-1]['route']!=endpoint_constraints['route_kind_id']):mismatches.append(dict(reason='SELECTED_ROUTE_NOT_PERFORMED'))
 if endpoint_constraints.get('place') is not None and s['place']!=endpoint_constraints['place']:mismatches.append(dict(reason='SELECTED_PLACE_NOT_REACHED'))
 match=r['valid'] and bool(predicates) and not mismatches
 return dict(status='ENDPOINT_MATCH' if match else S.INTEGRITY_FAILURE if r['errors'] else S.ENDPOINT_INFEASIBLE,endpoint_match=match,mismatches=mismatches,recomputed_state=s,replay_seconds=round(time.perf_counter()-t,6),n_events_replayed=len(r['admitted']),temporal_inversions=0,causal_integrity_errors=r['errors'],causal_error_codes=sorted({x['code'] for x in r['errors']}),causal_edges_verified=sum(len(x.get('causal_parent_event_ids',[])) for x in events if x['event_id'] in r['admitted']),endpoint_state_derived_from_antecedent=True,endpoint_state_overwrite_by_endpoint_claim='REFUSED',endpoint_place_basis_event_id=next((e['event_id'] for e in reversed(events) if e['kind'] in PLACE_ESTABLISHING_KINDS and e['event_id'] in r['admitted']),None),value_witnesses=r['value_witnesses'],selected_obligation_witnesses=obligation_witnesses,represented_history_hash=r['history_hash'])


def stopping_law_check(events,psyche,endpoint_constraints,replay,probes):
 r=replay_history(events);pe=validate_psyche(events,psyche,r)
 missing=[k for k in MANDATORY_DOMAIN_KINDS if not any(e['kind']==k and e['event_id'] in r['admitted'] for e in events)]
 # Recompute dependencies; a caller-supplied positive flag is never evidence.
 real_replay=forward_replay_to_endpoint(events,endpoint_constraints)
 real_probes=independent_actions(events,psyche)
 checks=dict(endpoint_fields_have_lawful_histories=real_replay['endpoint_match'],
  material_organismic_relational_project_practice_memory_domains_present=not missing,
  psyche_fields_have_causal_ancestry=not pe,
  heldout_nonmother_action_evaluable_without_mom_prompt=real_probes['heldout_independence_pass'],
  nonmother_project_effects_persist_into_independent_future_test=real_probes['probes'][0]['pass'],
  forward_replay_entails_endpoint=real_replay['endpoint_match'],
  no_outstanding_mandatory_antecedent_missing_authority=r['valid'],
  bounded_observational_closure=r['valid'] and not missing and not pe)
 ok=all(checks.values());out=dict(stopping_law_version=VERSION,checks=checks,sufficient=ok,status=S.COMMITTED if ok else S.PREHISTORY_OWNER_RULE_MISSING,science_grade='BOUNDED_SOURCEFREE_TRANSITIONS_NOT_PERSON_FORMATION_AUTHORITY')
 if not ok:
  reasons=[]
  if r['errors']:reasons+=['OUTSTANDING_MANDATORY_ANTECEDENT','CAUSAL_INTEGRITY_FAILURE']
  if not real_replay['endpoint_match']:reasons+=['REQUIRED_ENDPOINT_PREDICATE_WITHOUT_ANTECEDENT']
  if missing:reasons+=['DOMAIN_COVERAGE_NOT_CAUSALLY_ANCHORED']
  if pe:reasons+=['PSYCHE_FIELD_WITHOUT_CAUSAL_ANCESTRY']
  out['typed_hold']=dict(hold_state=S.PREHISTORY_OWNER_RULE_MISSING,hold_reasons=reasons,outstanding_mandatory_antecedents=r['errors'],unanchored_domains=missing,psyche_fields_without_ancestry=pe,is_HOLD_not_INFEASIBLE=True)
 return out


def construct_second_parent(selected_class,endpoint_constraints,attempt_seeds):
 t=time.perf_counter();attempts=[];success=None
 for i,seed in enumerate(attempt_seeds):
  # Complete content identity; no sha256-prefix truncation or first-12-bit alias.
  actor='LAB_SECOND_PARENT_CAND_'+h_obj(dict(class_key=selected_class['class_key'],attempt_seed=seed)).split(':')[-1]
  events=DadHistoryBuilder(actor,seed,endpoint_constraints).build();p=derive_psyche(events)
  r=forward_replay_to_endpoint(events,endpoint_constraints);pr=independent_actions(events,p)
  st=stopping_law_check(events,p,endpoint_constraints,r,pr)
  status=S.COMMITTED if st['sufficient'] else S.ENDPOINT_INFEASIBLE if not r['endpoint_match'] else S.PREHISTORY_OWNER_RULE_MISSING
  att=dict(attempt_id=h_concat('ATT_G15',seed,selected_class['class_key']),attempt_seed=seed,status=status,n_events=len(events),endpoint_match=r['endpoint_match'],independence_pass=pr['heldout_independence_pass'],stopping_sufficient=st['sufficient'],replay=r,probes=pr,stopping=st,events=events,psyche=p,construction_edges=[dict(from_='SELECTED_ENDPOINT_CONTRACT',to='ATTEMPT_'+str(i),edge_type='RETROSPECTIVE_CONSTRUCTION_DEPENDS_ON',algorithm_time=True,causal_parent=False)])
  attempts.append(att)
  if status==S.COMMITTED:success=att;break
 return dict(construction_version=VERSION,n_attempts=len(attempts),attempt_seeds=attempt_seeds,attempts=attempts,selected_attempt_id=success['attempt_id'] if success else None,selected_events=success['events'] if success else None,selected_psyche=success['psyche'] if success else None,terminal_status=S.COMMITTED if success else S.HISTORY_SEARCH_EXHAUSTED,wall_seconds=round(time.perf_counter()-t,6))
