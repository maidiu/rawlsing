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
        # Retain the stored project and its means, but only project currently
        # available conditional courses into recruitment. An inaccessible
        # Other or a suspended means cannot cast a project-pressure vote.
        bindings=p.get('dependency_conditional_means',{})
        if bindings:
            present={c.get('source_actor') for c in encounter.cues
                     if c.get('kind')=='coactor_present'}
            x['means']=[m for m in p.get('means',[]) if m not in bindings or (
                bindings[m].get('status','ACTIVE')=='ACTIVE'
                and bindings[m].get('location')==encounter.location
                and bindings[m].get('counterpart_ref') in present
                and any(j.get('id')==bindings[m].get('practice_ref')
                        and j.get('actor')==constitution.actor
                        and j.get('operation')==m
                        and j.get('coactor_ref')==bindings[m].get('counterpart_ref')
                        and j.get('status')=='ACQUIRED_CONDITIONAL_COORDINATION_NOT_DYAD_MASTERY'
                        for j in getattr(constitution,'joint_practices',[])))]
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
            raise ValueError('ACTIVITY_PURPOSE_BASIS_CONTRADICTION')
        ident=purpose_selection.get('project_id')
        status_kind=purpose_selection.get('status')
        if status_kind=='ACTOR_POLICY_SELECTED_PROJECT_COURSE':
            if (type(ident) is not str or project_ids!={ident}
                    or purpose_selection.get('project_ids',[ident])!=[ident]):
                raise ValueError('ACTIVITY_PURPOSE_BASIS_CONTRADICTION')
            project_ids={ident}
        elif status_kind=='ACTOR_POLICY_SELECTED_MULTIPLE_PROJECT_COURSES':
            refs=purpose_selection.get('project_ids')
            if (ident is not None or type(refs) is not list
                    or not 2<=len(refs)<=8
                    or any(type(x) is not str for x in refs)
                    or set(refs)!=project_ids or len(set(refs))!=len(refs)):
                raise ValueError('ACTIVITY_PURPOSE_BASIS_CONTRADICTION')
            project_ids=set(refs)
        elif status_kind in (
            'EXTERNALLY_INJECTED_NO_ATTESTED_ACTOR_PURPOSE',
            'ACTOR_POLICY_NO_ATTESTED_PROJECT_PURPOSE',
            # R3 issued an exploration, NOT an acquired project motive:
            # the selected event remains real activity without any falsely
            # attributed durable purpose.
            'ACTOR_POLICY_PROVISIONAL_END_TRIAL_NOT_DURABLE_MOTIVE'):
            if ident is not None or project_ids:
                raise ValueError('ACTIVITY_PURPOSE_BASIS_CONTRADICTION')
            project_ids=set()
        else:raise ValueError('ACTIVITY_PURPOSE_BASIS_CONTRADICTION')
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


def possible_dependency_project_reorganizations(actor,experience,event_ref):
    """A blocked acquired undertaking can be reconstituted by a lived
    alternative, including renewed cooperation with the original Other.
    The new practical relation is conditional, not a right to care.
    """
    aid=actor.get('id');clock=experience.get('clock')
    selected=experience.get('own_practical_selection') or {}
    request=selected.get('world_request') or {}
    other=experience.get('reciprocated_partner')
    if (experience.get('actor')!=aid or type(clock) is not int
            or experience.get('own_action')!='SIGNAL'
            or experience.get('status')!='PERFORMED'
            or experience.get('participated') is not True
            or selected.get('actor')!=aid
            or selected.get('status')!='ACTOR_POLICY_PRACTICAL_ATTEMPT'
            or selected.get('possible_end_trial') is not None
            or selected.get('selected_project_refs')!=[]
            or request.get('operation')!='SIGNAL'
            or type(other) is not str or other==aid
            or request.get('addressed_party_ref')!=other
            or type(selected.get('option_id')) is not str):
        return []
    episodes=actor.get('lived_genesis_episodes',[])
    current=[x for x in episodes if x.get('actor')==aid
             and x.get('event_ref')==event_ref
             and x.get('experience_ref')==experience.get('ref')
             and x.get('clock')==clock
             and x.get('actor_felt_attempt')=='SIGNAL'
             and x.get('selected_addressed_party_ref')==other
             and x.get('selected_practical_option_ref')==selected['option_id']
             and x.get('received_relief',{}).get('nutrition')
             and x.get('received_sign_refs')
             and not x.get('unfinished_own_activity')]
    if len(current)!=1:return []
    now=current[0]
    participations=[x for x in actor.get('participation_history',[])
                    if x.get('actor')==aid and x.get('event_ref')==event_ref
                    and x.get('experience_ref')==experience.get('ref')
                    and x.get('joint_participation_perceived')
                    and x.get('reciprocated_partner_actor_visible')==other
                    and x.get('own_attempted_operation')=='SIGNAL'
                    and x.get('own_status')=='PERFORMED']
    if len(participations)!=1:return []
    out=[]
    for project in actor.get('projects',[])[-128:]:
        dep=project.get('takeup_evidence',{}).get('dependency_takeup_basis')
        if (not dep or project.get('status')!='active'
                or project.get('means')!=['EAT']
                or project.get('addressed_party_ref') is not None
                or project.get('dependency_conditional_means')):continue
        practice=[x for x in actor.get('joint_practices',[])
                  if x.get('id')==dep.get('dependency_practice_ref')
                  and x.get('actor')==aid and x.get('coactor_ref')==other
                  and x.get('operation')=='SIGNAL'
                  and x.get('location')==experience.get('location')
                  and x.get('status')=='ACQUIRED_CONDITIONAL_COORDINATION_NOT_DYAD_MASTERY']
        if len(practice)!=1:continue
        # The project must actually have met the contradiction; not just
        # a failed unrelated operation or an observer's speculation.
        courses=project.get('operational_history',[])
        if not courses:continue
        course=courses[-1]
        if (course.get('project')!=project['id']
                or course.get('operation')!='EAT'
                or course.get('performed_status')!='BLOCKED'
                or course.get('selected_at_actor_attempt') is not True):continue
        lived=[x for x in project.get('lived_attempt_history',[])
               if x.get('event')==course.get('event')
               and x.get('project')==project['id']
               and x.get('attempted_operation')=='EAT'
               and x.get('accessible_cue_refs')]
        failed=[x for x in episodes if x.get('actor')==aid
                and x.get('event_ref')==course.get('event')
                and x.get('actor_felt_attempt')=='EAT'
                and x.get('unfinished_own_activity')
                and x.get('location')==now.get('location')
                and type(x.get('clock')) is int and x['clock']<clock
                and not x.get('received_relief',{}).get('nutrition')]
        if len(lived)!=1 or len(failed)!=1:continue
        basis={'practice_ref':practice[0]['id'],'counterpart_ref':other,
               'location':now['location'],'blocked_project_event_ref':course['event'],
               'blocked_episode_ref':failed[0]['id'],'renewed_episode_ref':now['id'],
               'renewed_participation_ref':participations[0]['id'],
               'renewed_event_ref':event_ref,'selected_option_ref':selected['option_id'],
               'no_future_consent_or_motive_fulfillment_inferred':True}
        out.append({'kind':'REORGANIZE_PROJECT','project_id':project['id'],
                    'means':['EAT','SIGNAL'],
                    'object':'sustain nourishment through own and conditional shared means',
                    'motive':'PROVISIONAL_REORGANIZATION_OF_NOURISHMENT_UNDERTAKING',
                    'dependency_reorganization_basis':basis})
    return out[:3]


def possible_dependency_means_revisions(actor,experience,event_ref):
    """Local reversible change in a project-specific conditional means.

    Two comparable, actually lived courses after the last revision support
    optional suspension or reopening. Neither co-presence nor one refusal
    proves changed love or permanent unavailability. Unrelated operations
    are not evidence, but an intervening contrary addressed course interrupts
    the series. Keep the project, earlier practice and all receipts.
    """
    aid=actor.get('id');clock=experience.get('clock')
    sel=experience.get('own_practical_selection') or {}
    req=sel.get('world_request') or {}
    other=req.get('addressed_party_ref')
    if (experience.get('actor')!=aid or type(clock) is not int
            or experience.get('own_action')!='SIGNAL'
            or experience.get('participated') is not True
            or sel.get('actor')!=aid or sel.get('status')!='ACTOR_POLICY_PRACTICAL_ATTEMPT'
            or sel.get('possible_end_trial') is not None
            or req.get('operation')!='SIGNAL'
            or type(other) is not str or other==aid
            or type(sel.get('option_id')) is not str):
        return []
    episodes=actor.get('lived_genesis_episodes',[])
    participation=actor.get('participation_history',[])
    out=[]
    for p in actor.get('projects',[])[-128:]:
        bound=p.get('dependency_conditional_means',{}).get('SIGNAL')
        if (not bound or p.get('status')!='active' or 'SIGNAL' not in p.get('means',[])
                or bound.get('counterpart_ref')!=other
                or bound.get('location')!=experience.get('location')):continue
        status=bound.get('status','ACTIVE')
        if status not in ('ACTIVE','SUSPENDED'):continue
        mode='SUSPEND' if status=='ACTIVE' else 'REOPEN'
        if sel.get('selected_project_refs')!=([p['id']] if mode=='SUSPEND' else []):continue
        # Scope and origin must be real existing actor-owned practice.
        practice=[j for j in actor.get('joint_practices',[])
                  if j.get('id')==bound.get('practice_ref') and j.get('actor')==aid
                  and j.get('coactor_ref')==other and j.get('operation')=='SIGNAL'
                  and j.get('location')==bound['location']
                  and j.get('status')=='ACQUIRED_CONDITIONAL_COORDINATION_NOT_DYAD_MASTERY']
        if len(practice)!=1:continue
        history=bound.get('revision_history',[])
        prior_ref=history[-1]['event_ref'] if history else bound['origin_event_ref']
        origins=[e for e in episodes if e.get('event_ref')==prior_ref and e.get('actor')==aid]
        if len(origins)!=1:continue
        after=origins[0]['clock']
        # Project attribution is a separate receipt, not inferred from SIGNAL.
        courses={x['event']:x for x in p.get('operational_history',[])
                 if x.get('project')==p['id'] and x.get('operation')=='SIGNAL'
                 and x.get('selected_at_actor_attempt') is True}
        rows=[]
        for e in episodes:
            if (e.get('actor')!=aid or e.get('location')!=bound['location']
                    or e.get('actor_felt_attempt')!='SIGNAL'
                    or e.get('selected_addressed_party_ref')!=other
                    or type(e.get('selected_practical_option_ref')) is not str
                    or e.get('selection_source')!='ACTOR_SITUATED_CANDIDATE_SELECTED_SOURCEFREE'
                    or not after<e['clock']<=clock):continue
            parts=[x for x in participation if x.get('actor')==aid
                   and x.get('event_ref')==e['event_ref']
                   and x.get('experience_ref')==e['experience_ref']
                   and x.get('own_attempted_operation')=='SIGNAL']
            if len(parts)!=1:
                rows.append((e,None,None));continue
            part=parts[0]
            failed=(e.get('unfinished_own_activity') and not e.get('received_relief',{}).get('nutrition')
                    and part.get('own_status') in ('PARTIAL','BLOCKED')
                    and not part.get('joint_participation_perceived')
                    and e.get('selected_project_refs')==[p['id']]
                    and e.get('selected_possible_end_trial_ref') is None
                    and e['event_ref'] in courses
                    and courses[e['event_ref']].get('performed_status') in ('PARTIAL','BLOCKED'))
            renewed=(not e.get('unfinished_own_activity') and e.get('received_relief',{}).get('nutrition')
                     and part.get('own_status')=='PERFORMED'
                     and part.get('joint_participation_perceived')
                     and part.get('reciprocated_partner_actor_visible')==other
                     and e.get('selected_project_refs')==[]
                     and e.get('selected_possible_end_trial_ref') is None
                     and e['event_ref'] not in courses)
            rows.append((e,part,'SUSPEND' if failed else 'REOPEN' if renewed else None))
        last=rows[-2:]
        if (len(last)!=2 or any(v[2]!=mode for v in last)
                or last[-1][0]['event_ref']!=event_ref
                or last[-1][0]['experience_ref']!=experience.get('ref')
                or last[-1][0]['selected_practical_option_ref']!=sel['option_id']
                or last[0][0]['clock']>=last[1][0]['clock']):continue
        basis={'mode':mode,'practice_ref':bound['practice_ref'],'counterpart_ref':other,
               'location':bound['location'],'previous_revision_event_ref':prior_ref,
               'episode_refs':[x[0]['id'] for x in last],
               'participation_refs':[x[1]['id'] for x in last],
               'event_refs':[x[0]['event_ref'] for x in last],
               'no_relationship_or_future_consent_inference':True}
        out.append({'kind':'REORGANIZE_PROJECT','project_id':p['id'],
                    'dependency_means_revision_basis':basis})
    return out[:3]


# Relations between ongoing activities are not additional universal drives.
def qualify_interactivity_deferral(alternatives, selected, deferred_id, location):
    if selected is None or selected.get('project_id') is None:
        raise ValueError('INTERACTIVITY_NO_SELECTED_COURSE')
    rows=[x for x in alternatives if x['option_id']==deferred_id
          and x.get('project_id') not in (None,selected['project_id'])
          and x['operation']!=selected['operation']
          and x.get('binding_status')=='NO_ADDRESSED_PARTY'
          and selected.get('binding_status')=='NO_ADDRESSED_PARTY'
          and not x.get('world_request',{}).get('material_object_ref')
          and not selected.get('world_request',{}).get('material_object_ref')]
    if len(rows)!=1:raise ValueError('INTERACTIVITY_UNISSUED_DEFERRED_COURSE')
    x=rows[0]
    return {'selected_project':selected['project_id'],'selected_operation':selected['operation'],
            'selected_option_ref':selected['option_id'],'deferred_project':x['project_id'],
            'deferred_operation':x['operation'],'deferred_option_ref':x['option_id'],
            'location':location,'not_a_performed_alternative_or_abandoned_motive':True}

def _interactivity_history(actor,selected,deferred,event_ref):
    paths={p['event']:p for p in actor.get('evidence_paths',[])}
    active={p['id'] for p in actor.get('projects',[]) if p.get('status','active')=='active'}
    if not {selected,deferred}<=active or selected==deferred:return None
    ex=actor.get('expectations',[])[-128:]
    for first in reversed(ex):
        if first.get('project_id')!=selected or first.get('actor')!=actor['id']:continue
        for other in reversed(ex):
            if (other.get('project_id')!=deferred or other.get('actor')!=actor['id']
                    or first.get('origin_event')!=other.get('origin_event')
                    or not first.get('shared_selected_operation_ref')
                    or first['shared_selected_operation_ref']!=other.get('shared_selected_operation_ref')):continue
            origin=paths.get(first['origin_event'],{})
            if (origin.get('purpose_status')!='ACTOR_POLICY_SELECTED_MULTIPLE_PROJECT_COURSES'
                    or not {selected,deferred}<=set(origin.get('selected_project_refs',[]))
                    or origin.get('practical_option_ref')!=first['shared_selected_operation_ref']):continue
            apps=[x.get('appraisal_history',[])[-1:] for x in (first,other)]
            if not all(apps):continue
            x,y=(v[0] for v in apps)
            if {x.get('appraisal'),y.get('appraisal')}!={'ACTOR_INTERPRETS_SUPPORTED','ACTOR_INTERPRETS_DISAPPOINTED'}:continue
            if not all(v.get('event') not in (event_ref,first['origin_event'])
                    and v.get('perceived_cue_ref') in paths.get(v.get('event'),{}).get('received_cue_refs',[])
                    and v.get('perceived_cue_ref') in v.get('actual_received_sign_refs',[])
                    for v in (x,y)):continue
            return {'shared_origin_event':first['origin_event'],
                    'selected_expectation_ref':first['id'],'deferred_expectation_ref':other['id'],
                    'selected_appraisal_event':x['event'],'deferred_appraisal_event':y['event'],
                    'selected_appraisal':x['appraisal'],'deferred_appraisal':y['appraisal']}
    return None

def possible_interactivity_relations(actor,experience,event_ref):
    sel=experience.get('own_practical_selection') or {}
    choice=sel.get('interactivity_deferral')
    if (not isinstance(choice,dict) or actor['id']!=experience.get('actor')
            or sel.get('actor')!=actor['id'] or sel.get('status')!='ACTOR_POLICY_PRACTICAL_ATTEMPT'
            or experience.get('participated') is not True or experience.get('status')!='PERFORMED'
            or experience.get('own_action')!=choice.get('selected_operation')
            or sel.get('selected_project_refs')!=[choice.get('selected_project')]
            or choice.get('location')!=experience.get('location')):return []
    paths=[p for p in actor.get('evidence_paths',[]) if p.get('event')==event_ref
           and p.get('experience_ref')==experience.get('ref') and p.get('interactivity_deferral')==choice]
    if len(paths)!=1:return []
    cues=[x for x in experience.get('perceived_cues',[]) if x.get('source_actor')==actor['id']
          and x.get('kind')=='performed_'+experience['own_action'].lower()
          and x.get('id') in paths[0].get('received_cue_refs',[])]
    if len(cues)!=1:return []
    selected=choice['selected_project'];deferred=choice['deferred_project']
    prior=_interactivity_history(actor,selected,deferred,event_ref)
    if not prior:return []
    p=next(p for p in actor['projects'] if p['id']==selected)
    if any(x['basis']['deferred_project']==deferred and x['basis']['location']==choice['location']
           for x in p.get('interactivity_relations',[])):return []
    return [{**copy(choice),**prior,'actor':actor['id'],'origin_event':event_ref,
             'experience_ref':experience['ref'],'received_own_sign_ref':cues[0]['id'],'grade':GRADE}]

def admit_interactivity_relation(actor,experience,event_ref,candidate):
    if (set(candidate)!={'kind','basis','personal_sense'}
            or candidate['basis'] not in possible_interactivity_relations(actor,experience,event_ref)
            or type(candidate['personal_sense']) is not str
            or not 1<=len(candidate['personal_sense'].strip())<=400):
        raise ValueError('INTERACTIVITY_RELATION_UNQUALIFIED_HISTORY')
    b=candidate['basis'];ident=stable_id('interactivity_relation',b)
    p=next(p for p in actor['projects'] if p['id']==b['selected_project'])
    p.setdefault('interactivity_relations',[]).append({'id':ident,'basis':copy(b),
        'personal_sense':candidate['personal_sense'],'status':'ACTIVE',
        'not_global_priority_or_lost_counterfactual':True,'grade':GRADE})
    return {'kind':candidate['kind'],'relation_ref':ident,'grade':GRADE}

def annotate_interactivity_relations(constitution,access,options):
    """Both activities remain possible; only their actual co-recruitment
    makes this particular relation available. No automatic winner."""
    alts=[x for o in options for x in o.get('practical_alternatives',[])]
    currents=[];readset=set()
    for p in constitution.projects[-128:]:
        for rec in p.get('interactivity_relations',[])[-16:]:
            b=rec.get('basis',{})
            if (rec.get('status')!='ACTIVE' or b.get('actor')!=constitution.actor
                    or b.get('selected_project')!=p['id'] or b.get('location')!=access.location
                    or rec.get('id')!=stable_id('interactivity_relation',b)):continue
            left=[x for x in alts if x.get('project_id')==b['selected_project']
                  and x['operation']==b['selected_operation'] and x.get('binding_status')=='NO_ADDRESSED_PARTY']
            right=[x for x in alts if x.get('project_id')==b['deferred_project']
                   and x['operation']==b['deferred_operation'] and x.get('binding_status')=='NO_ADDRESSED_PARTY']
            if len(left)!=1 or len(right)!=1:continue
            row={'relation_ref':rec['id'],'selected_project':b['selected_project'],
                 'deferred_project':b['deferred_project'],'selected_option_ref':left[0]['option_id'],
                 'deferred_option_ref':right[0]['option_id'],'personal_sense':rec['personal_sense'],
                 'not_an_automatic_deferral':True,'grade':GRADE}
            for x in left+right:x.setdefault('interactivity_currents',[]).append(copy(row))
            currents.append({'kind':'INTERACTIVITY_HISTORICAL_CURRENT',**copy(row)})
            readset.add(rec['id'])
    return {'currents':currents,'readset':sorted(readset)}
