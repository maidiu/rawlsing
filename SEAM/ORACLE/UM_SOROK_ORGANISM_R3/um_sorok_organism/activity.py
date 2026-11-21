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


def record_activity_afterlife(actor, own_action, status, outcome, basis, event_ref,
                              object_delta=None, purpose_selection=None):
    """Preserve an *attempted* operation's separate objective activity courses.

    A blocked/partial attempt is historical conduct, not the absence of an
    activity. Only actor-selected project: bases may attach a proposed
    purpose. External action injection, shared means, and a successful world
    operation do not license objective fulfillment or psychic satisfaction.
    Returns audit receipts, not actor-experienced knowledge of the outcome.
    """
    if status not in ('PERFORMED', 'PARTIAL', 'BLOCKED'):
        raise ValueError('UNKNOWN_ACTIVITY_OPERATION_STATUS')
    project_ids={r.removeprefix('project:') for r in basis
                 if isinstance(r,str) and r.startswith('project:')}
    # A standalone explicit project-basis call is a *legacy caller assertion*.
    # The joined live runtime instead passes its selected-purpose receipt:
    # it is a historical error to read a pooled option's several courses as
    # several ACTUALLY ATTEMPTED ends.
    if purpose_selection is None:
        attribution='EXPLICIT_LEGACY_PROJECT_BASIS_ASSERTION'
    else:
        if not isinstance(purpose_selection,dict):
            raise ValueError('INVALID_SELECTED_PURPOSE_RECEIPT')
        ident=purpose_selection.get('project_id')
        status_kind=purpose_selection.get('status')
        if status_kind=='ACTOR_POLICY_SELECTED_PROJECT_COURSE':
            if (type(ident) is not str or project_ids!={ident}
                    or purpose_selection.get('project_ids',[ident])!=[ident]):
                raise ValueError('SELECTED_PURPOSE_NOT_IN_ACTOR_ATTEMPT_BASIS')
            project_ids={ident}
        elif status_kind=='ACTOR_POLICY_SELECTED_MULTIPLE_PROJECT_COURSES':
            refs=purpose_selection.get('project_ids')
            if (ident is not None or type(refs) is not list
                    or not 2<=len(refs)<=8
                    or any(type(x) is not str for x in refs)
                    or set(refs)!=project_ids or len(set(refs))!=len(refs)):
                raise ValueError('MULTIPLE_SELECTED_PURPOSES_MISMATCH_ATTEMPT')
            project_ids=set(refs)
        elif status_kind in (
            'EXTERNALLY_INJECTED_NO_ATTESTED_ACTOR_PURPOSE',
            'ACTOR_POLICY_NO_ATTESTED_PROJECT_PURPOSE'):
            if ident is not None or project_ids:
                raise ValueError('PURPOSE_UNKNOWN_BUT_PROJECT_ASSERTED')
            project_ids=set()
        else:raise ValueError('UNKNOWN_SELECTED_PURPOSE_STATUS')
        attribution=status_kind
        # REMONT R18 P004: a selected purpose is not merely a basis tag.
        # EVERY selected project must exist exactly once, and this exact
        # operation must be among its actual enabled means. Validate the
        # entire selection before writing even the first historical row.
        projects=actor.get('projects',[])
        for project_id in sorted(project_ids):
            matches=[p for p in projects if p.get('id')==project_id]
            if (len(matches)!=1 or own_action not in matches[0].get('means',[])):
                raise ValueError('ACTIVITY_SELECTED_MEANS_CONTRADICTION')
    # Also preflight event uniqueness for every selected project together:
    # a previously observed repeat must not append half a multi-project
    # selection before discovering the second project was duplicated.
    for project in actor.get('projects',[]):
        if project.get('id') in project_ids and any(
                h.get('event')==event_ref for h in
                project.get('operational_history',[])):
            raise ValueError('DUPLICATE_ACTIVITY_EVENT_FOR_PROJECT')
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
            'intent_attribution':attribution,
            'selected_at_actor_attempt':True if purpose_selection is not None else 'LEGACY_CALLER_ASSERTION',
            'other_eligible_project_courses_not_asserted':purpose_selection is not None,
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
