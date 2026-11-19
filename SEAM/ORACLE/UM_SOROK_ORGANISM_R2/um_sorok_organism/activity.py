"""R2: historically situated activity-object-motive-means relations.

Leontiev/Sève distinction: technical success != fulfillment of the motive; a
single performed operation can belong to multiple contradictory activities.
This is a derived and then actor-owned *research* process, not native V3.
"""
from .types import copy, stable_id, GRADE


def eligible_activities(constitution, recruited_form_ids, encounter):
    """A project can have its own cues or be recruited through an acquired form.

    Contextual-only projects stay dormant absent real cues or a qualified
    FORM->ACTIVITY link. Noncontextual ordinary projects remain available.
    """
    actual_tags={str(t).lower() for c in encounter.cues for t in c.get('tags',[])}
    sources=set(recruited_form_ids)
    result=[]
    for p in constitution.projects:
        if p.get('status','active')!='active': continue
        cue_match=bool(set(t.lower() for t in p.get('cue_terms',[])) & actual_tags)
        recruiting=[link for link in constitution.activity_links
            if link.get('relation')=='RECRUITS_ACTIVITY'
            and link.get('source') in sources and link.get('target')==p['id']
            and (not link.get('contexts') or encounter.location in link['contexts'])]
        if p.get('contextual_only') and not (cue_match or recruiting): continue
        x=copy(p)
        x['recruitment_basis']=['ACTIVITY_CUE'] if cue_match else []
        x['recruitment_basis'] += ['FORM_LINK:'+r['source'] for r in recruiting]
        x['motive']=p.get('motive','UNSPECIFIED_ACQUIRED_MOTIVE')
        x['object']=p['object']
        # This is an actor-accessible attempt trace, not an external verdict on
        # the project or its motive. An unfinished course remains recruitable.
        x['latest_lived_attempt']=copy(p.get('latest_lived_attempt'))
        result.append(x)
    return result


def record_activity_afterlife(actor, own_action, status, outcome, basis, event_ref, object_delta=None):
    """Preserve an *attempted* operation's separate objective activity courses.

    A blocked/partial attempt is historical conduct, not the absence of an
    activity. Only actor-selected project: bases may attach a proposed
    purpose. External action injection, shared means, and a successful world
    operation do not license objective fulfillment or psychic satisfaction.
    Returns audit receipts, not actor-experienced knowledge of the outcome.
    """
    if status not in ('PERFORMED', 'PARTIAL', 'BLOCKED'):
        raise ValueError('UNKNOWN_ACTIVITY_OPERATION_STATUS')
    project_ids={r.removeprefix('project:') for r in basis if isinstance(r,str) and r.startswith('project:')}
    histories=[]
    for project in actor.get('projects',[]):
        if project['id'] not in project_ids or own_action not in project.get('means',[]):
            continue
        # A repeated dispatch must not duplicate the same objective occurrence.
        if any(h.get('event')==event_ref for h in project.get('operational_history',[])):
            raise ValueError('DUPLICATE_ACTIVITY_EVENT_FOR_PROJECT')
        entry={'event':event_ref,'project':project['id'],
            'operation':own_action,'objective_outcome':outcome,'performed_status':status,
            'practical_object':project['object'],'motive_hypothesis':project.get('motive'),
            'object_transformation':copy(object_delta or {}),
            'operation_course':('INTERRUPTED_ATTEMPT' if status=='BLOCKED'
                 else 'PARTIAL_ATTEMPT' if status=='PARTIAL'
                 else 'PERFORMED_OPERATION'),
            'object_fulfillment':'NOT_INFERRED_FROM_OPERATION',
            'objective_outcome_access':'WORLD_AUDIT_NOT_ACTOR_KNOWLEDGE',
            'motive_realized':'UNDETERMINED_BY_TECHNICAL_OUTCOME','grade':GRADE}
        histories.append(entry)
        project.setdefault('operational_history',[]).append(entry)
    actor.setdefault('activity_history',[]).extend(histories)
    return histories


def register_lived_activity_attempt(actor, experience, histories):
    """Write a *separate* personally undergone course, without world omniscience.

    A somatically accessible attempt may leave a revisable practical trace.
    Neither an external outcome nor an inferred motive is silently admitted
    into the actor's experienced constitution. Future situated recruitment can
    consult this actor-owned trace while original objective results stay audit.
    """
    felt=experience.get('felt_enactment') or {}
    if not felt or felt.get('objective_result_not_inferred') is not True:
        return []
    if felt.get('attempted_operation')!=experience.get('own_action'):
        return []
    visible=[c.get('id') for c in experience.get('perceived_cues',[]) if c.get('id')]
    lived=[]
    for h in histories:
        if h['operation']!=experience['own_action']:
            continue
        p=next((p for p in actor.get('projects',[]) if p['id']==h['project']),None)
        if p is None:continue
        trace={'event':h['event'],'project':h['project'],
               'attempted_operation':h['operation'],'felt':'SOMATIC_ATTEMPT_ONLY',
               'accessible_cue_refs':visible,
               'objective_outcome':'NOT_INFERRED',
               'motive_realized':'UNDETERMINED_BY_TECHNICAL_OUTCOME',
               'practical_continuation':'OPEN_FOR_FUTURE_INTERPRETATION',
               'grade':GRADE}
        p.setdefault('lived_attempt_history',[]).append(trace)
        p['latest_lived_attempt']=copy(trace)
        actor.setdefault('lived_activity_history',[]).append(trace)
        lived.append(trace)
    return lived
