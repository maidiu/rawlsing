"""All operative endpoint constraints have explicit, source-bound consumers."""
from .core import S
WINDOWS={'T_ENCOUNTER_LAB_WINDOW':(20,200)}


def prehistory_obligations(events,replay,ec):
 mismatches=[];witnesses=[];state=replay['state'];admitted=replay['admitted']
 constraints=ec.get('second_parent_structure_and_position_constraints',[])
 if not isinstance(constraints,list):return [dict(reason='UNISSUED_ENDPOINT_STRUCTURE',constraint=constraints)],[]
 for constraint in constraints:
  if constraint=='waged_artisan_local':
   support=[e for e in events if e['event_id'] in admitted and e['kind'] in {'WORK_POSITION','COMMISSIONED_WORK'}]
   ok=state['material_position'] in {'waged_repair','waged_finishing'} and state['place']=='INST_WORKSHOP_A' and len(support)>=2
  elif constraint=='evening_class_attendee':
   support=[e for e in events if e['event_id'] in admitted and e['kind']=='ENROLLMENT']
   ok=bool(support) and state['place']=='INST_EVENING_CLASS_B'
  else:
   mismatches.append(dict(reason='UNISSUED_ENDPOINT_STRUCTURE',constraint=constraint));continue
  witnesses.append(dict(constraint=constraint,supporting_event_ids=[e['event_id'] for e in support],value_read=dict(place=state['place'],material_position=state['material_position']),satisfied=ok))
  if not ok:mismatches.append(dict(reason='SELECTED_STRUCTURE_NOT_ENACTED',constraint=constraint))
 clock=ec.get('time_or_interval')
 if clock is not None:
  if not isinstance(clock,str) or clock not in WINDOWS:mismatches.append(dict(reason='UNISSUED_ENDPOINT_CLOCK',clock=clock))
  else:
   low,high=WINDOWS[clock]
   actual=max((e['effective_index'] for e in events if e['event_id'] in admitted),default=-1)
   if not low<=actual<=high:mismatches.append(dict(reason='PREHISTORY_CUT_OUTSIDE_SELECTED_CLOCK',have=actual,window=[low,high]))
 return mismatches,witnesses


def joint_obligations(anchor,events,relation,ec):
 from .joint import validate_joint
 witness=relation.get('objective_relation',{}).get('witness')
 actual=validate_joint(anchor,events,witness);errors=[];checks=[]
 for field,vocabulary in [('required_relation_objective_refs',{'REL_ENCOUNTER_WITNESSED'}),('conception_witness_requirements',{'ENCOUNTER_WITNESS_MIN_1'})]:
  values=ec.get(field,[])
  if not isinstance(values,list):errors.append(dict(reason='UNCLASSIFIED_JOINT_CONSTRAINT',field=field));continue
  for value in values:
   ok=isinstance(value,str) and value in vocabulary and actual
   checks.append(dict(field=field,required=value,satisfied=ok,actual_witness_ref=witness.get('event_id') if witness else None))
   if not ok:errors.append(dict(reason='REQUIRED_JOINT_WITNESS_UNRESOLVED',field=field,required=value))
 clock=ec.get('time_or_interval');window=WINDOWS.get(clock) if isinstance(clock,str) else None
 if window is None:errors.append(dict(reason='UNISSUED_ENDPOINT_CLOCK'))
 elif not witness or not window[0]<=witness['effective_index']<=window[1]:errors.append(dict(reason='JOINT_EVENT_OUTSIDE_SELECTED_CLOCK',window=window,have=witness.get('effective_index') if witness else None))
 return dict(status='SATISFIED_AT_SOURCEFREE_RESEARCH_SCOPE' if not errors else S.ENDPOINT_INFEASIBLE,checks=checks,errors=errors,clock_units='LABORATORY_EFFECTIVE_INDEX_NOT_CALENDAR_YEARS',biological_conception_admitted=False,native_grant='NOT_GRANTED')
