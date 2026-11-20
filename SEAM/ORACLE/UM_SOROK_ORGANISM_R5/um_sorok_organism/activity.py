"""TCO R4 activity afterlife: public course != actor-owned lived course.

Integrates the independently proposed REMONT SR-P004 repair *at research grade*;
preflights mutations and preserves shared-operation/multiple-object ambiguity.
"""
from .types import copy, GRADE


def eligible_activities(constitution, recruited_form_ids, encounter):
    actual_tags={str(t).lower() for c in encounter.cues for t in c.get('tags',[])}
    sources=set(recruited_form_ids)
    result=[]
    for p in constitution.projects:
        if p.get('status','active')!='active':continue
        cue_match=bool({t.lower() for t in p.get('cue_terms',[])} & actual_tags)
        recruiting=[r for r in constitution.activity_links
                    if r.get('relation')=='RECRUITS_ACTIVITY' and r.get('source') in sources
                    and r.get('target')==p['id'] and
                    (not r.get('contexts') or encounter.location in r['contexts'])]
        if p.get('contextual_only') and not (cue_match or recruiting):continue
        x=copy(p);x['recruitment_basis']=(['ACTIVITY_CUE'] if cue_match else [])+[
            'FORM_LINK:'+r['source'] for r in recruiting]
        x['motive']=p.get('motive','UNSPECIFIED_ACQUIRED_MOTIVE')
        x['object']=p['object']
        x['latest_lived_attempt']=copy(p.get('latest_lived_attempt'))
        result.append(x)
    return result


def record_activity_afterlife(actor,own_action,status,outcome,basis,event_ref,object_delta=None):
    """Register specifically attributed actor attempts, NOT motive satisfaction.

    Existing R2 public helper conserves multi-object courses when the admitted
    basis explicitly contains more than one project. The R4 actor planner must
    NOT silently infer such multi-project intention from the action's feasibility.
    All duplicates preflight before any in-memory mutation.
    """
    if status not in ('PERFORMED','PARTIAL','BLOCKED'):
        raise ValueError('UNKNOWN_ACTIVITY_OPERATION_STATUS')
    project_ids={b.removeprefix('project:') for b in basis
                 if isinstance(b,str) and b.startswith('project:')}
    matched=[p for p in actor.get('projects',[]) if p['id'] in project_ids
             and own_action in p.get('means',[])]
    for p in matched:
        if any(h.get('event')==event_ref for h in p.get('operational_history',[])):
            raise ValueError('DUPLICATE_ACTIVITY_EVENT_FOR_PROJECT')
    # A learned organizing method may be exercised through multiple operations
    # but it is not invented anew by each operation. Keep its actual historical
    # exercise reference separately from the hypothetical purpose.
    method_refs=sorted({b.removeprefix('historical_method:') for b in basis
                         if isinstance(b,str) and b.startswith('historical_method:')})
    histories=[]
    for p in matched:
        entry={'event':event_ref,'project':p['id'],'operation':own_action,
          'performed_status':status,'operation_course':('INTERRUPTED_ATTEMPT' if status=='BLOCKED'
             else 'PARTIAL_ATTEMPT' if status=='PARTIAL' else 'PERFORMED_OPERATION'),
          'objective_outcome':outcome,'objective_outcome_access':'WORLD_AUDIT_NOT_ACTOR_KNOWLEDGE',
          'practical_object':p['object'],'motive_hypothesis':p.get('motive'),
          'object_transformation':copy(object_delta or {}),
          'object_fulfillment':'NOT_INFERRED_FROM_OPERATION',
          'motive_realized':'UNDETERMINED_BY_TECHNICAL_OUTCOME',
          'method_exercise_refs':copy(method_refs),'grade':GRADE}
        p.setdefault('operational_history',[]).append(entry);histories.append(entry)
    actor.setdefault('activity_history',[]).extend(histories)
    return histories


def register_lived_activity_attempt(actor,experience,histories):
    """Personally accessible somatic course, without importing world verdicts.

    Status here is a *provisional proprioceptive proxy* under the research
    world model. The objective cause is NEVER copied to the lived record.
    """
    felt=experience.get('felt_enactment') or {}
    if (felt.get('objective_result_not_inferred') is not True or
            felt.get('attempted_operation')!=experience.get('own_action')):
        return []
    cues=[c for c in experience.get('perceived_cues',[]) if c.get('id')]
    outputs=[]
    # preflight all project/event duplicates; no partial in-memory append.
    matches=[h for h in histories if h['operation']==experience['own_action']]
    for h in matches:
        p=next((x for x in actor.get('projects',[]) if x['id']==h['project']),None)
        if p and any(t.get('event')==h['event'] for t in p.get('lived_attempt_history',[])):
            raise ValueError('DUPLICATE_LIVED_ATTEMPT_FOR_PROJECT')
    for h in matches:
        p=next((x for x in actor.get('projects',[]) if x['id']==h['project']),None)
        if not p:continue
        course=('INTERRUPTED' if experience['status']=='BLOCKED' else
                'PARTIAL' if experience['status']=='PARTIAL' else 'CONTINUED')
        trace={'event':h['event'],'project':h['project'],'actor':actor['id'],
            'experience_ref':experience['ref'],'attempted_operation':h['operation'],
            'somatic_course':course,'somatic_course_grade':'SOURCEFREE_ENACTMENT_PROXY',
            'felt':'SOMATIC_ATTEMPT_ONLY','method_exercise_refs':copy(h.get('method_exercise_refs',[])),
            'accessible_cue_refs':[c['id'] for c in cues],
            'accessible_cue_tags':sorted({str(t).lower() for c in cues for t in c.get('tags',[])}),
            'objective_outcome':'NOT_INFERRED',
            'motive_realized':'UNDETERMINED_BY_TECHNICAL_OUTCOME',
            'practical_continuation':'OPEN_FOR_FUTURE_INTERPRETATION','grade':GRADE}
        p.setdefault('lived_attempt_history',[]).append(trace)
        p['latest_lived_attempt']=copy(trace)
        actor.setdefault('lived_activity_history',[]).append(trace)
        outputs.append(trace)
    return outputs
