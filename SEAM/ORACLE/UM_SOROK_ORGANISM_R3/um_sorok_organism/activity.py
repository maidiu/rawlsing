"""R2: historically situated activity-object-motive-means relations.

Leontiev/Sève distinction: technical success != fulfillment of the motive; a
single performed operation can belong to multiple contradictory activities.
This is a derived and then actor-owned *research* process, not native V3.
"""
from .types import copy, stable_id, GRADE
from .distributed_power import accessible_human_counterparts
from .social_vocal_development import ordinary_vocal_actor_view, ordinary_vocal_basis_still_qualified



def _solo_vocal_sign(cue,other,location):
    """The public sign of an exercise, never the performer's private purpose."""
    return (type(cue) is dict and cue.get('kind')=='performed_sing'
            and cue.get('source_actor')==other
            and cue.get('modality')=='auditory'
            and cue.get('location')==location
            and 'solo_practice' in cue.get('tags',[])
            and type(cue.get('id')) is str)


def possible_productive_witness_reorganizations(actor,experience,event_ref):
    """A former co-performer's own undertaking may acquire a receptive means.

    A particular Other's personally heard solo vocal exercise can change what
    *this actor* does in an existing project previously enacted with them.
    No access to the Other's project, skill, initiative or private feeling.
    One offered reorganization is neither celebration nor mandatory approval.
    """
    aid=actor['id'];clock=experience.get('clock');loc=experience.get('location')
    if (experience.get('actor')!=aid or type(clock) is not int
            or type(loc) is not str or experience.get('status')!='OBSERVED'
            or experience.get('participated') is not False):return []
    signs=[c for c in experience.get('perceived_cues',[])
           if type(c.get('source_actor')) is str and c['source_actor']!=aid
           and _solo_vocal_sign(c,c['source_actor'],loc) and c.get('clock')==clock]
    if len(signs)!=1:return []
    sign=signs[0];other=sign['source_actor']
    paths=[x for x in actor.get('evidence_paths',[])
           if x.get('event')==event_ref and x.get('experience_ref')==experience.get('ref')
           and sign['id'] in x.get('received_cue_refs',[])
           and x.get('purpose_status')=='NO_ACTOR_AUTHORED_ATTEMPT']
    if len(paths)!=1:return []
    out=[]
    for p in actor.get('projects',[])[-128:]:
        if (p.get('status')!='active' or p.get('means') not in (['SING'],['SPEAK'])
                or p.get('addressed_party_ref') is not None
                or p.get('productive_witness_means') or p.get('dependency_conditional_means')
                or p.get('incidental_takeup_basis')):continue
        source_op=p['means'][0]
        matches=[]
        for h in p.get('operational_history',[]):
            if (h.get('project')!=p['id'] or h.get('operation')!=source_op
                    or h.get('performed_status')!='PERFORMED'
                    or h.get('selected_at_actor_attempt') is not True
                    or h.get('intent_attribution')!='ACTOR_POLICY_SELECTED_PROJECT_COURSE'
                    or h.get('event')==event_ref):continue
            parts=[x for x in actor.get('participation_history',[])
                   if x.get('actor')==aid and x.get('event_ref')==h.get('event')
                   and x.get('own_attempted_operation')==source_op
                   and x.get('own_status')=='PERFORMED'
                   and x.get('joint_participation_perceived') is True
                   and x.get('reciprocated_partner_actor_visible')==other
                   and type(x.get('experienced_clock')) is int
                   and x['experienced_clock']<clock]
            if len(parts)!=1:continue
            part=parts[0]
            episodes=[x for x in actor.get('lived_genesis_episodes',[])
                      if x.get('actor')==aid and x.get('event_ref')==h['event']
                      and x.get('experience_ref')==part.get('experience_ref')
                      and x.get('clock')==part['experienced_clock']
                      and x.get('location')==loc and x.get('actor_felt_attempt')==source_op
                      and x.get('selected_project_refs')==[p['id']]
                      and x.get('selected_possible_end_trial_ref') is None
                      and not x.get('unfinished_own_activity')
                      and any(((source_op=='SING' and z.get('kind')=='performed_sing'
                                and z.get('source_actor') in (aid,other))
                               or (source_op=='SPEAK' and z.get('kind')=='performed_signal'
                                   and z.get('source_actor')==other))
                              and z.get('cue_ref') in part.get('received_cue_refs',[])
                              for z in x.get('personally_perceived_sign_sources',[]))]
            if len(episodes)!=1:continue
            ep=episodes[0]
            lived=[x for x in p.get('lived_attempt_history',[])
                   if x.get('event')==h['event'] and x.get('project')==p['id']
                   and x.get('attempted_operation')==source_op
                   and set(x.get('accessible_cue_refs',[]))&set(ep.get('received_sign_refs',[]))]
            if len(lived)==1:matches.append((part,ep))
        if not matches:continue
        part,ep=max(matches,key=lambda x:(x[1]['clock'],x[1]['id']))
        basis={'actor':aid,'project_ref':p['id'],'counterpart_ref':other,'location':loc,
               'joint_event_ref':ep['event_ref'],'joint_episode_ref':ep['id'],
               'joint_participation_ref':part['id'],'solo_event_ref':event_ref,
               'solo_experience_ref':experience['ref'],'solo_sign_ref':sign['id'],
               'no_other_motive_or_approval_inferred':True}
        if source_op=='SPEAK':
            basis.update({'source_route':'ACTUAL_RESPONSIVE_SPEECH_THEN_OTHER_SOLO_SOUND',
                          'source_response_operation':source_op,
                          'no_other_acquired_capacity_or_learning_inferred':True})
        out.append({'kind':'REORGANIZE_PROJECT','project_id':p['id'],
                    'means':[source_op,'ORIENT'],'productive_witness_basis':basis})
    return out[:3]


def productive_witness_signs(project,access):
    """A receptive course is local and depends on a currently receivable act.

    The older productive course stays available independently. Silence, loss
    of access or an unrelated performer cannot be treated as fresh reception.
    """
    binding=project.get('productive_witness_means')
    if not isinstance(binding,dict) or binding.get('actor')!=access.actor:return []
    if binding.get('project_ref')!=project.get('id') or binding.get('location')!=access.location:return []
    return [c for c in access.cues
            if _solo_vocal_sign(c,binding.get('counterpart_ref'),access.location)
            and c.get('clock')==access.world_clock]


def productive_witness_option(project,access,cue):
    binding=project['productive_witness_means']
    basis={'actor':access.actor,'project_ref':project['id'],'clock':access.world_clock,
           'origin_event_ref':binding['solo_event_ref'],'cue_ref':cue['id'],
           'counterpart_ref':binding['counterpart_ref'],'location':access.location}
    return {**basis,'outward_sign':copy(cue),'attention_ref':stable_id('productive_witness_attention',basis),
            'not_other_conscious_purpose_or_approval':True,'grade':GRADE}


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
        ordinary=p.get('ordinary_vocal_genesis_basis')
        if ordinary is not None and not ordinary_vocal_basis_still_qualified(
                ordinary_vocal_actor_view(constitution),ordinary,
                encounter.location,encounter.world_clock):
            # Retain acquired wanting; do not grant its same-site course in
            # every unfamiliar context or on loss of historical source.
            continue
        if p.get('incidental_takeup_basis') is not None:
            if not any(c.get('kind')=='material_object_present'
                       and c.get('material_object_ref')==p.get('material_object_ref')
                       for c in encounter.cues):
                continue
        cue_match=bool(set(t.lower() for t in p.get('cue_terms',[])) & actual_tags)
        recruiting=[link for link in constitution.activity_links
            if link.get('relation')=='RECRUITS_ACTIVITY'
            and link.get('source') in sources and link.get('target')==p['id']
            and (not link.get('contexts') or encounter.location in link['contexts'])]
        if p.get('contextual_only') and not (cue_match or recruiting or p.get('incidental_takeup_basis') is not None): continue
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
                and (bindings[m].get('counterpart_ref') in present
                     or (m=='SIGNAL' and bindings[m].get('counterpart_ref')
                         in accessible_human_counterparts(encounter)))
                and any(j.get('id')==bindings[m].get('practice_ref')
                        and j.get('actor')==constitution.actor
                        and j.get('operation')==m
                        and j.get('coactor_ref')==bindings[m].get('counterpart_ref')
                        and j.get('status')=='ACQUIRED_CONDITIONAL_COORDINATION_NOT_DYAD_MASTERY'
                        for j in getattr(constitution,'joint_practices',[])))]
        if p.get('provisioning_means_basis') and encounter.location!=p['provisioning_means_basis']['provisioning_site']:
            x['means']=[m for m in x.get('means',[]) if m not in ('WORK','BUY_FOOD')]
        if p.get('commons_provisioning_basis') and encounter.location!=p['commons_provisioning_basis']['location']:
            x['means']=[m for m in x.get('means',[]) if m!='CONTRIBUTE_FOOD_COMMONS']
        if p.get('productive_witness_means') and not productive_witness_signs(p,encounter):
            x['means']=[m for m in x.get('means',[]) if m!='ORIENT']
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
          and ((x.get('binding_status')=='NO_ADDRESSED_PARTY'
                and selected.get('binding_status')=='NO_ADDRESSED_PARTY'
                and not x.get('world_request',{}).get('material_object_ref')
                and not selected.get('world_request',{}).get('material_object_ref'))
               or _addressed_use_time_pair(selected,x))]
    if len(rows)!=1:raise ValueError('INTERACTIVITY_UNISSUED_DEFERRED_COURSE')
    x=rows[0]
    extra=({'course_relation_kind':'ADDRESSED_REPRODUCTIVE_USE_TIME',
            'selected_addressed_party_ref':selected.get('world_request',{}).get('addressed_party_ref'),
            'deferred_addressed_party_ref':x.get('world_request',{}).get('addressed_party_ref')}
           if _addressed_use_time_pair(selected,x) else {})
    return {**extra,'selected_project':selected['project_id'],'selected_operation':selected['operation'],
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
    prior=(_addressed_interactivity_history(actor,choice,event_ref,experience)
           if choice.get('course_relation_kind')=='ADDRESSED_REPRODUCTIVE_USE_TIME'
           else _interactivity_history(actor,selected,deferred,event_ref))
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
            addressed=b.get('course_relation_kind')=='ADDRESSED_REPRODUCTIVE_USE_TIME'
            def matches(x,which):
                if (x.get('project_id')!=b[which+'_project']
                        or x['operation']!=b[which+'_operation']):return False
                if not addressed:return x.get('binding_status')=='NO_ADDRESSED_PARTY'
                other=b[which+'_addressed_party_ref']
                return (x.get('world_request',{}).get('addressed_party_ref')==other
                        and x.get('binding_status')==(
                            'QUALIFIED_AS_PRESENT' if other else 'NO_ADDRESSED_PARTY'))
            left=[x for x in alts if matches(x,'selected')]
            right=[x for x in alts if matches(x,'deferred')]
            if len(left)!=1 or len(right)!=1:continue
            row={'relation_ref':rec['id'],'selected_project':b['selected_project'],
                 'deferred_project':b['deferred_project'],'selected_option_ref':left[0]['option_id'],
                 'deferred_option_ref':right[0]['option_id'],'personal_sense':rec['personal_sense'],
                 **({'course_relation_kind':b['course_relation_kind'],
                     'selected_addressed_party_ref':b['selected_addressed_party_ref'],
                     'deferred_addressed_party_ref':b['deferred_addressed_party_ref']}
                    if addressed else {}),
                 'not_an_automatic_deferral':True,'grade':GRADE}
            for x in left+right:x.setdefault('interactivity_currents',[]).append(copy(row))
            currents.append({'kind':'INTERACTIVITY_HISTORICAL_CURRENT',**copy(row)})
            readset.add(rec['id'])
    return {'currents':currents,'readset':sorted(readset)}


def own_provisioning_receipt(actor,experience,world):
    """Analytic witness to actual own performed material conduct, not mind-reading.

    World claims use the pre-transition clock; only the actor's own received
    sign licenses this reference. No token genealogy of fungible money/food.
    """
    op=experience.get('own_action'); aid=actor['id']; clock=experience.get('clock')
    if (experience.get('actor')!=aid or op not in ('WORK','BUY_FOOD')
            or experience.get('status')!='PERFORMED'
            or experience.get('participated') is not True or type(clock) is not int):
        return None
    cues=[c for c in experience.get('perceived_cues',[])
          if c.get('kind')=='performed_'+op.lower() and c.get('source_actor')==aid]
    if len(cues)!=1:return None
    claims=[c for c in world.get('material_claims',[])
            if c.get('clock')==clock-1 and c.get('site')==experience.get('location')
            and ((op=='WORK' and c.get('worker')==aid and c.get('wage',0)>0
                  and c.get('worker_control_of_output') is False)
                 or (op=='BUY_FOOD' and c.get('buyer')==aid
                     and c.get('kind')=='FOOD_PURCHASE' and c.get('price_paid',0)>0
                     and c.get('goods_transferred')==1))]
    if len(claims)!=1:return None
    return {'operation':op,'actor':aid,'clock':clock,'site':experience['location'],
            'cue_ref':cues[0]['id'],'material_claim_ref':stable_id('material_claim_witness',claims[0]),
            'not_conscious_accounting_or_earmarked_income':True}


def possible_provisioning_reorganizations(actor,experience,event_ref):
    """Prior wage and purchase can become means of a particular care project.

    Current personally enacted feeding must be independently selected for that
    project and materially performed using held food. Prior actual receipts
    qualify a semantic occasion, not proof these particular wages bought this
    exact food or that work/care have no conflicting significance.
    """
    aid=actor['id']; sel=experience.get('own_practical_selection') or {}
    refs=sel.get('selected_project_refs',[])
    if (experience.get('actor')!=aid or experience.get('own_action')!='FEED'
            or experience.get('status')!='PERFORMED'
            or experience.get('participated') is not True
            or sel.get('actor')!=aid or sel.get('status')!='ACTOR_POLICY_PRACTICAL_ATTEMPT'
            or len(refs)!=1 or sel.get('possible_end_trial') is not None):
        return []
    target=(sel.get('world_request') or {}).get('addressed_party_ref')
    feed=[x for x in actor.get('performed_feeding_events',[])
          if x.get('event_ref')==event_ref and x.get('giver')==aid
          and x.get('recipient')==target and x.get('material_food_source')=='GIVER_HELD_FOOD'
          and x.get('original_action_was_actor_selected') is True
          and x.get('applied_nutrition_change',0)>0]
    if len(feed)!=1:return []
    paths=actor.get('evidence_paths',[])
    now=[x for x in paths if x.get('event')==event_ref and
         x.get('experience_ref')==experience['ref'] and
         feed[0].get('received_action_sign_ref') in x.get('received_cue_refs',[])]
    if len(now)!=1:return []
    prior=[]
    for x in paths:
        v=x.get('own_provisioning_receipt_analytic_only') or {}
        if (v.get('actor')==aid and v.get('cue_ref') in x.get('received_cue_refs',[])
                and type(v.get('clock')) is int and v['clock']<experience['clock']
                and x.get('own_action')==v.get('operation')):
            prior.append((x,v))
    buys=[(x,v) for x,v in prior if v['operation']=='BUY_FOOD']
    if not buys:return []
    purchase,pv=max(buys,key=lambda x:x[1]['clock'])
    works=[(x,v) for x,v in prior if v['operation']=='WORK'
           and v['clock']<pv['clock'] and v['site']==pv['site']]
    if not works:return []
    work,wv=max(works,key=lambda x:x[1]['clock'])
    projects=[x for x in actor.get('projects',[]) if x.get('id')==refs[0]
              and x.get('status','active')=='active' and x.get('means') in (
                  ['FEED'],['FEED','CONTRIBUTE_FOOD_COMMONS'])
              and ('CONTRIBUTE_FOOD_COMMONS' not in x['means'] or x.get('commons_provisioning_basis'))
              and x.get('addressed_party_ref')==target
              and not x.get('provisioning_means_basis')]
    if len(projects)!=1:return []
    basis={'actor':aid,'recipient_ref':target,'work_event_ref':work['event'],
           'purchase_event_ref':purchase['event'],'feeding_event_ref':event_ref,
           'feeding_receipt_ref':feed[0]['id'],'work_claim_ref':wv['material_claim_ref'],
           'purchase_claim_ref':pv['material_claim_ref'],'provisioning_site':pv['site'],
           'not_proof_of_earmarked_money_or_motive_fulfillment':True}
    return [{'kind':'REORGANIZE_PROJECT','project_id':refs[0],
             'means':copy(projects[0]['means'])+['WORK','BUY_FOOD'],'provisioning_means_basis':basis}]


def own_commons_receipt(actor,experience,world,event_ref):
    """The existing material commons producer, actually exercised by this actor.

    A real contribution can change later practical means. The receipt is
    actor-local and analytic; no token earmarking, political ideology or
    unperformed feeding is inferred.
    """
    aid=actor['id'];clock=experience.get('clock');site=experience.get('location')
    sel=experience.get('own_practical_selection') or {}
    if (experience.get('actor')!=aid or type(clock) is not int
            or experience.get('own_action')!='CONTRIBUTE_FOOD_COMMONS'
            or experience.get('status')!='PERFORMED'
            or experience.get('participated') is not True
            or sel.get('actor')!=aid or sel.get('status')!='ACTOR_POLICY_PRACTICAL_ATTEMPT'
            or (sel.get('world_request') or {}).get('operation')!='CONTRIBUTE_FOOD_COMMONS'):
        return None
    signs=[x for x in experience.get('perceived_cues',[])
           if x.get('kind')=='performed_contribute_food_commons'
           and x.get('source_actor')==aid and x.get('clock')==clock
           and x.get('location')==site
           and x.get('description')=='INDEPENDENT_FOOD_COMMONS_ENLARGED']
    rows=[x for x in world.get('food_commons_history',[])
          if x.get('giver')==aid and x.get('site')==site and x.get('clock')==clock
          and x.get('actor_selection_source')=='ACTOR_SITUATED_CANDIDATE_SELECTED_SOURCEFREE'
          and x.get('food_debited_from_private_holdings')==1
          and x.get('food_credited_to_independent_commons')==1]
    if len(signs)!=1 or len(rows)!=1:return None
    return {'actor':aid,'event_ref':event_ref,'experience_ref':experience['ref'],
            'clock':clock,'site':site,'cue_ref':signs[0]['id'],'commons_ref':rows[0]['id'],
            'not_a_proof_of_earmarked_food_or_collective_ideology':True}


def possible_commons_provisioning_reorganizations(actor,experience,event_ref):
    """Actual blocked care, own material contribution and actual later feeding.

    The project can acquire a new *means* through its own material history,
    not because a model supplies a political slogan. Preserve the end, other
    historically acquired means, and the former unfinished activity.
    """
    aid=actor['id'];site=experience.get('location');clock=experience.get('clock')
    sel=experience.get('own_practical_selection') or {}
    refs=sel.get('selected_project_refs',[])
    if (experience.get('actor')!=aid or type(clock) is not int
            or experience.get('own_action')!='FEED' or experience.get('status')!='PERFORMED'
            or experience.get('participated') is not True
            or sel.get('actor')!=aid or sel.get('status')!='ACTOR_POLICY_PRACTICAL_ATTEMPT'
            or len(refs)!=1 or sel.get('possible_end_trial') is not None):return []
    target=(sel.get('world_request') or {}).get('addressed_party_ref')
    if type(target) is not str or target==aid:return []
    projects=[x for x in actor.get('projects',[])
              if x.get('id')==refs[0] and x.get('status','active')=='active'
              and x.get('addressed_party_ref')==target and 'FEED' in x.get('means',[])
              and 'CONTRIBUTE_FOOD_COMMONS' not in x.get('means',[])
              and not x.get('commons_provisioning_basis')]
    if len(projects)!=1:return []
    project=projects[0]
    paths=actor.get('evidence_paths',[])
    feed=[x for x in actor.get('performed_feeding_events',[])
          if x.get('event_ref')==event_ref and x.get('giver')==aid
          and x.get('recipient')==target and x.get('site')==site
          and x.get('material_food_source')=='MUTUAL_AID_FOOD'
          and x.get('original_action_was_actor_selected') is True
          and x.get('applied_nutrition_change',0)>0]
    if len(feed)!=1:return []
    now=[p for p in paths if p.get('event')==event_ref and p.get('experience_ref')==experience['ref']
         and p.get('selected_project_refs')==refs
         and p.get('practical_option_ref')==sel.get('option_id')
         and feed[0].get('received_action_sign_ref') in p.get('received_cue_refs',[])]
    if len(now)!=1:return []
    prior=[]
    for x in actor.get('material_dependency_encounters',[]):
        if (x.get('actor')!=aid or x.get('location')!=site
                or x.get('own_operation_attempted')!='FEED'
                or type(x.get('clock')) is not int or x['clock']>=clock):continue
        own=[p for p in paths if p.get('event')==x.get('event_ref')
             and p.get('experience_ref')==x.get('experience_ref')
             and p.get('selected_project_refs')==refs
             and x.get('received_nonperformance_sign_ref') in p.get('received_cue_refs',[])]
        episodes=[e for e in actor.get('lived_genesis_episodes',[])
                  if e.get('event_ref')==x.get('event_ref') and e.get('actor')==aid
                  and e.get('experience_ref')==x.get('experience_ref')
                  and e.get('selected_addressed_party_ref')==target
                  and e.get('selected_project_refs')==refs
                  and e.get('unfinished_own_activity')
                  and e.get('selected_practical_option_ref') is not None]
        if len(own)==len(episodes)==1:prior.append(x)
    if not prior:return []
    blocked=max(prior,key=lambda x:x['clock'])
    donations=[]
    for path in paths:
        x=path.get('own_commons_receipt_analytic_only',{})
        if (x.get('actor')==aid and x.get('site')==site
                and x.get('event_ref')==path.get('event')
                and x.get('experience_ref')==path.get('experience_ref')
                and x.get('cue_ref') in path.get('received_cue_refs',[])
                and type(x.get('clock')) is int and blocked['clock']<x['clock']<clock):
            donations.append(x)
    if not donations:return []
    donation=max(donations,key=lambda x:x['clock'])
    basis={'actor':aid,'location':site,'recipient_ref':target,
           'blocked_feeding_ref':blocked['id'],'blocked_event_ref':blocked['event_ref'],
           'actual_commons_ref':donation['commons_ref'],'contribution_event_ref':donation['event_ref'],
           'feeding_event_ref':event_ref,'feeding_receipt_ref':feed[0]['id'],
           'not_proof_of_earmarked_food_or_abandoned_other_means':True}
    return [{'kind':'REORGANIZE_PROJECT','project_id':project['id'],
             'means':copy(project['means'])+['CONTRIBUTE_FOOD_COMMONS'],
             'commons_provisioning_basis':basis}]


def _addressed_use_time_pair(selected,deferred):
    """The exact two alternatives coexist, neither automatically dominates.

    Extend the existing deferral owner to one actually addressed care course
    versus one nonaddressed material course. No imagined access, unavailable
    recipient, future promise or arbitrary object identity.
    """
    pair=[selected,deferred]
    care=[x for x in pair if x['operation'] in ('CARE','FEED')
          and x.get('binding_status')=='QUALIFIED_AS_PRESENT'
          and type(x.get('world_request',{}).get('addressed_party_ref')) is str]
    material=[x for x in pair if x['operation'] in (
              'CONTRIBUTE_FOOD_COMMONS','WORK','BUY_FOOD','EAT','REST')
              and x.get('binding_status')=='NO_ADDRESSED_PARTY'
              and x.get('world_request',{}).get('addressed_party_ref') is None]
    return len(care)==len(material)==1 and not any(
        x.get('world_request',{}).get('material_object_ref') for x in pair)


def _addressed_interactivity_history(actor,choice,event_ref,experience):
    """Actual reverse allocation of the same two projects is evidence of
    their distinct practical courses, not proof of conflict or priority."""
    aid=actor['id'];site=choice['location'];clock=experience.get('clock')
    if type(clock) is not int:return None
    projects={p['id']:p for p in actor.get('projects',[]) if p.get('status','active')=='active'}
    s=choice['selected_project'];d=choice['deferred_project']
    if not {s,d}<=set(projects):return None
    paths=actor.get('evidence_paths',[])
    def actual(p,project,operation):
        return (p.get('selected_project_refs')==[project]
                and p.get('own_action')==operation
                and any(x.get('event')==p.get('event') and x.get('project')==project
                        and x.get('operation')==operation and x.get('performed_status')=='PERFORMED'
                        and x.get('selected_at_actor_attempt') is True
                        for x in projects[project].get('operational_history',[])))
    current=[p for p in paths if p.get('event')==event_ref
             and p.get('experience_ref')==experience.get('ref')
             and p.get('interactivity_deferral')==choice
             and actual(p,s,choice['selected_operation'])]
    if len(current)!=1:return None
    previous=[]
    for p in paths:
        b=p.get('interactivity_deferral',{})
        if (b.get('course_relation_kind')!='ADDRESSED_REPRODUCTIVE_USE_TIME'
                or b.get('location')!=site or p.get('event')==event_ref
                or b.get('selected_project')!=d or b.get('deferred_project')!=s
                or b.get('selected_operation')!=choice['deferred_operation']
                or b.get('deferred_operation')!=choice['selected_operation']
                or b.get('selected_addressed_party_ref')!=choice['deferred_addressed_party_ref']
                or b.get('deferred_addressed_party_ref')!=choice['selected_addressed_party_ref']
                or not actual(p,d,choice['deferred_operation'])):continue
        lived=[e for e in actor.get('lived_genesis_episodes',[])
               if e.get('event_ref')==p.get('event') and e.get('actor')==aid
               and e.get('experience_ref')==p.get('experience_ref') and e.get('location')==site
               and e.get('selected_practical_option_ref')==b.get('selected_option_ref')
               and type(e.get('clock')) is int and e['clock']<clock
               and not e.get('unfinished_own_activity')]
        if len(lived)==1:previous.append((p,lived[0]))
    if not previous:return None
    p,e=max(previous,key=lambda x:x[1]['clock'])
    return {'earlier_reverse_deferral_event_ref':p['event'],
            'earlier_reverse_deferral_experience_ref':p['experience_ref'],
            'earlier_reverse_deferral_episode_ref':e['id'],
            'earlier_selected_project':d,
            'not_proof_of_foregone_outcome_or_fixed_priority':True}
