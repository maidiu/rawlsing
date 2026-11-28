"""SORACLE R13 — world consequences and psychic expectations run on two clocks.

An objective allocation can close now; an actor's anticipation may remain
uninterpreted through other events, be revised years later, and reshape a
situated future attempt. We compare only signs the actor could receive, never
counterfactual non-encounters. A sign produced by their own previous choice
is not independent confirmation of their theory.

First writer: existing development.admit(APPRAISE_EXPECTED_DIFFERENCE).
First reader: existing constitution practical alternatives and semantic choice.
This is a sourcefree fictional policy, not a universal preference for truth,
a measured updating law, or an imported theory of conscious reflection.
"""
from .types import GRADE, copy, stable_id


def source_qualified_appraisal_candidates(actor, experience, event_ref):
    if actor.get('id')!=experience.get('actor') or not event_ref:
        raise ValueError('APPRAISAL_FOREIGN_ACTOR_OR_EVENT')
    cues=[c for c in experience.get('perceived_cues',[])
          if type(c) is dict and type(c.get('id')) is str]
    if not cues:return []
    candidates=[]
    for exp in actor.get('expectations',[])[-128:]:
        if (type(exp) is not dict or exp.get('origin_event')==event_ref
                or not exp.get('id')):
            continue
        if exp.get('state') not in (
            'STILL_PENDING','MEANING_UNRESOLVED',
            'MATERIAL_OBSTACLE_SUSPECTED',
            'ACTOR_INTERPRETS_DISAPPOINTED',
            'ACTOR_INTERPRETS_SUPPORTED'):
            continue
        signs=exp.get('anticipated_difference',{}).get('sign_tags',[])
        if type(signs) is not list or not signs:
            continue
        wished={s.casefold() for s in signs if type(s) is str}
        matching=[c for c in cues
                  if wished & {str(t).casefold() for t in c.get('tags',[])
                               if type(t) is str}]
        for cue in matching:
            if any(x.get('perceived_cue_ref')==cue['id']
                   for x in exp.get('appraisal_history',[])):
                continue
            source_actor=cue.get('source_actor')
            # Sources of signals are not necessarily their causes; the
            # actual world and actor's inquiry must qualify every inference.
            origin=('SELF_POSITIONED_SOURCED_SIGN'
                    if source_actor==actor['id'] else
                    'OTHER_OR_WORLD_SOURCED_SIGN'
                    if type(source_actor) is str else
                    'SIGN_SOURCE_NOT_ACTOR_IDENTIFIED')
            candidates.append({
                'expectation_ref':exp['id'],
                'prior_event_ref':exp['origin_event'],
                'later_event_ref':event_ref,
                'source_perceived_cue_ref':cue['id'],
                'cue_origin_class_analyst_only':origin,
                'recognized_signal_feature_set':sorted(
                    wished & set(x.casefold() for x in cue.get('tags',[])
                                 if type(x) is str)),
                'current_interpretation':exp.get('state'),
                'possible_actor_appraisals':[
                    'MEANING_UNRESOLVED','STILL_PENDING',
                    'ACTOR_INTERPRETS_SUPPORTED',
                    'ACTOR_INTERPRETS_DISAPPOINTED',
                    'MATERIAL_OBSTACLE_SUSPECTED'],
                'self_selected_evidence_not_external_proof':True,
                'sign_is_not_causal_warrant_for_outcome':True,
                'other_unselected_paths':'UNKNOWN_NOT_OBSERVED',
                'source_grade':GRADE,
            })
    return candidates[:8]


def conservative_appraisal_proposal(candidates):
    """Fallback refuses a causal verdict while allowing actual reappraisal.

    A live semantic constructor can instead propose a fallible interpretation
    from actor-specific history, with the existing typed owner verifying that
    the claimed sign was actually received.
    """
    if len(candidates)!=1:
        return []
    row=candidates[0]
    if row['current_interpretation'] not in (
        'STILL_PENDING','MATERIAL_OBSTACLE_SUSPECTED'):
        return []
    return [{
        'kind':'APPRAISE_EXPECTED_DIFFERENCE',
        'expectation_ref':row['expectation_ref'],
        'perceived_cue_ref':row['source_perceived_cue_ref'],
        'appraisal':'MEANING_UNRESOLVED',
        'no_retroactive_objective_cause':True,
        'not_a_final_interpretation':True,
        'grade':GRADE,
    }]


def annotate_practical_expectations(constitution,options):
    """A personally revised expectation modifies the *particular* course.

    No disappointment changes another project's score just because the
    projects happen to share an action name. The LLM can use this actor's
    prior appraisal to propose different attempts; fallback may choose
    another existing means but cannot assert certainty or project defeat.
    """
    known={}
    for exp in constitution.expectations[-256:]:
        if (type(exp) is dict and exp.get('project_id')
                and exp.get('state') not in (None,'STILL_PENDING')):
            known.setdefault(exp['project_id'],[]).append(exp)
    annotations=0
    for opt in options:
        for alt in opt.get('practical_alternatives',[]):
            pid=alt.get('project_id')
            records=known.get(pid,[])
            if not records:continue
            # Keep competing appraisals and evidence grades; later appraisals
            # do not rewrite older attempts into intentional prophecy.
            alt['prior_actor_appraisals']=[{
                'expectation_ref':x['id'],
                'state':x['state'],
                'appraisal_event_refs':[e.get('event') for e in
                                        x.get('appraisal_history',[])],
                'objective_success':'NOT_INFERRED',
                'not_actor_conscious_report':True,
            } for x in records[-12:]]
            alt['sourcefree_revised_future_approach']=[
                'REPEAT_OR_SUSTAIN','VARY_MEANS','WITHHOLD','SEEK_OTHER_EVIDENCE']
            alt['no_global_preference_for_novelty_or_confirmation']=True
            annotations+=1
    return {'annotated_alternative_count':annotations,
            'readset':sorted(set(
                x['id'] for group in known.values() for x in group)),
            'actor_interpretation_not_objective_event':True,'grade':GRADE}


# This is an extension of the existing expectation/activity afterlife, not
# a universal emotion ontology. The semantic constructor supplies the
# particular meaning and may abstain, including in materially identical lives.
def possible_ordinary_project_affects(actor,experience,event_ref):
    """A personally enacted acquired concern can become felt significance.
    This route does not require that the child already reflectively judges
    a propositional expectation. The existing expectation owner supplies
    durable prospective identity; the model may abstain or differentiate
    meanings of the SAME performed act.
    """
    from .activity import (_ordinary_project_own_sing, ordinary_vocal_project_site)
    if (experience.get('actor')!=actor.get('id')
            or experience.get('own_action')!='SING'
            or experience.get('status')!='PERFORMED'
            or experience.get('participated') is not True):return []
    clock=experience.get('clock');loc=experience.get('location')
    if type(clock) is not int or type(loc) is not str:return []
    sel=experience.get('own_practical_selection') or {}
    refs=sel.get('selected_project_refs',[])
    if (len(refs)!=1 or sel.get('status')!='ACTOR_POLICY_PRACTICAL_ATTEMPT'
            or sel.get('possible_end_trial') is not None):return []
    ps=[p for p in actor.get('projects',[]) if p.get('id')==refs[0]
        and p.get('status')=='active' and p.get('ordinary_vocal_genesis_basis')]
    if len(ps)!=1:return []
    p=ps[0]
    if not ordinary_vocal_project_site(actor,p,loc,clock):return []
    current=[(x,z) for x,z in _ordinary_project_own_sing(actor,p,loc,clock)
             if x['event_ref']==event_ref and x['experience_ref']==experience.get('ref')
             and x['clock']==clock and z in {q.get('id') for q in experience.get('perceived_cues',[])}]
    if len(current)!=1:return []
    ep,sign=current[0]
    origin_site=p['ordinary_vocal_genesis_basis']['location']
    prior=_ordinary_project_own_sing(actor,p,origin_site,clock-1)
    if not prior:return []
    # One earlier actually enacted expectation is the continuing owner.
    # Do not multiply affect offers by every repeat of an identical project.
    anchors=[]
    for older,oldsign in prior:
        for exp in actor.get('expectations',[]):
            if (exp.get('actor')==actor['id'] and exp.get('project_id')==p['id']
                    and exp.get('origin_event')==older['event_ref']
                    and exp.get('origin_experience_ref')==older['experience_ref']
                    and exp.get('practical_option_id')==older['selected_practical_option_ref']
                    and 'sing' in exp.get('anticipated_difference',{}).get('sign_tags',[])):
                anchors.append((older,oldsign,exp))
    if not anchors:return []
    older,oldsign,exp=anchors[0]
    local=None
    if loc!=origin_site:
        rows=[r for r in p.get('ordinary_vocal_context_transfers',[])
              if r.get('location')==loc and r.get('local_other_ref') in {
                  c.get('source_actor') for c in experience.get('perceived_cues',[])
                  if c.get('kind')=='coactor_present'}]
        if len(rows)!=1:return []
        local=rows[0]
    # One actual current episode may occasion one first-order formulation
    # and one higher-order relation to an earlier affect. The earlier
    # organization is not overwritten by the later one.
    existing=exp.get('affective_organizations',[])
    if any(a.get('origin_event_ref')==event_ref for a in existing):return []
    target=[a for a in existing if a.get('depth')==1
            and a.get('basis',{}).get('formation_source')=='OWN_ORDINARY_PROJECT_EXERCISE'
            and a.get('basis',{}).get('location')!=loc]
    # Bounded first-draft scope: at most two first-order organizations per
    # site; an additional one may concern a particular earlier affect.
    local_count=sum(a.get('depth')==1 and a.get('basis',{}).get('location')==loc
                    and a.get('basis',{}).get('formation_source')=='OWN_ORDINARY_PROJECT_EXERCISE'
                    for a in existing)
    objects=([None] if local_count<2 else [])
    if target and not any(a.get('basis',{}).get('object_affect_ref')==target[0]['id']
                          and a.get('basis',{}).get('location')==loc for a in existing):
        objects.append(target[0]['id'])
    return [{'formation_source':'OWN_ORDINARY_PROJECT_EXERCISE',
             'expectation_ref':exp['id'],'project_ref':p['id'],
             'origin_event_ref':older['event_ref'],'origin_exercise_sign_ref':oldsign,
             'current_event_ref':event_ref,'current_experience_ref':ep['experience_ref'],
             'current_cue_ref':sign,'cue_terms':['sing'],'location':loc,
             'expressive_operation':'SING','object_affect_ref':obj,
             'source_context_other_ref':local['local_other_ref'] if local else None,
             'context_transfer_probe_event_ref':local['probe_event_ref'] if local else None,
             'not_technical_success_as_pleasure_or_conscious_self_account':True}
            for obj in objects]


def possible_activity_affects(actor, experience, event_ref):
    """Offer personally grounded affective organization and higher-order objects.

    Prior actor-selected activity, actual later received appraisal sign, and
    a DISTINCT current matching encounter are necessary for this bounded
    family. Neither success nor a semantic appraisal dictates a feeling.
    Older affect is a possible object only within the same undertaking or
    the same genuinely multiply selected historical activity.
    """
    aid=actor.get('id')
    if experience.get('actor')!=aid or not event_ref:return []
    paths=actor.get('evidence_paths',[])
    by_event={}
    for index,path in enumerate(paths):
        ref=path.get('event')
        if ref in by_event:by_event[ref]=None
        else:by_event[ref]=(index,path)
    current=by_event.get(event_ref)
    if (current is None or current[1].get('experience_ref')!=experience.get('ref')
            or type(experience.get('location')) is not str):return []
    received={c['id']:c for c in experience.get('perceived_cues',[])
              if type(c) is dict and type(c.get('id')) is str
              and c['id'] in current[1].get('received_cue_refs',[])}
    if not received:return []
    projects={p['id']:p for p in actor.get('projects',[]) if p.get('status','active')=='active'}
    expectations=[e for e in actor.get('expectations',[])[-128:]
                  if e.get('actor')==aid and e.get('project_id') in projects]
    prior_affects=[]
    for exp in expectations:
        for aff in exp.get('affective_organizations',[])[-16:]:
            anchor=by_event.get(aff.get('origin_event_ref'))
            if (aff.get('actor')==aid and aff.get('expectation_ref')==exp['id']
                    and anchor is not None and anchor[0]<current[0]
                    and aff.get('depth')==1):
                prior_affects.append((exp,aff))
    offers=possible_ordinary_project_affects(actor,experience,event_ref)
    for exp in expectations:
        origin=by_event.get(exp.get('origin_event'))
        pid=exp['project_id']
        if (origin is None or origin[0]>=current[0]
                or origin[1].get('experience_ref')!=exp.get('origin_experience_ref')
                or pid not in origin[1].get('selected_project_refs',[])
                or origin[1].get('purpose_status') not in
                   ('ACTOR_POLICY_SELECTED_PROJECT_COURSE','ACTOR_POLICY_SELECTED_MULTIPLE_PROJECT_COURSES')):
            continue
        if exp.get('shared_selected_operation_ref') is not None:
            if (exp['shared_selected_operation_ref']!=origin[1].get('practical_option_ref')
                    or exp.get('shared_selected_project_refs')!=origin[1].get('selected_project_refs')):continue
        elif exp.get('practical_option_id')!=origin[1].get('practical_option_ref'):continue
        tags={str(t).casefold() for t in exp.get('anticipated_difference',{}).get('sign_tags',[])}
        if not tags:continue
        appraisals=exp.get('appraisal_history',[])
        # Latest interpretation, not arbitrary cherry-picking of older
        # appraisals after a contradictory subsequent interpretation.
        if not appraisals:continue
        appraisal=appraisals[-1]
        previous=by_event.get(appraisal.get('event'))
        sign=appraisal.get('perceived_cue_ref')
        if (previous is None or not origin[0]<previous[0]<current[0]
                or previous[1].get('experience_ref')!=appraisal.get('experience_ref')
                or sign not in previous[1].get('received_cue_refs',[])
                or sign not in appraisal.get('actual_received_sign_refs',[])
                or appraisal.get('appraisal') not in
                   ('ACTOR_INTERPRETS_SUPPORTED','ACTOR_INTERPRETS_DISAPPOINTED','MEANING_UNRESOLVED')
                or not tags.intersection(appraisal.get('appraised_sign_tags',[]))):continue
        for cue in received.values():
            matching=sorted(tags.intersection(str(t).casefold() for t in cue.get('tags',[])))
            if not matching or cue['id']==sign or cue['id'] in previous[1].get('received_cue_refs',[]):continue
            objects=[None]
            for other,aff in prior_affects:
                shared=(other.get('shared_selected_operation_ref') is not None
                        and other.get('shared_selected_operation_ref')==exp.get('shared_selected_operation_ref')
                        and other.get('origin_event')==exp.get('origin_event'))
                if other['id']==exp['id'] or shared:
                    objects.append(aff['id'])
            for target in sorted(set(x for x in objects if x is not None))+[None]:
                # An appraisal/object pair supplies at most one enduring
                # organization here. Another experienced appraisal can
                # develop another, without rewriting this one's ancestry.
                if any(a.get('basis',{}).get('appraisal_event_ref')==appraisal['event']
                       and a.get('basis',{}).get('object_affect_ref')==target
                       for a in exp.get('affective_organizations',[])):continue
                basis={'expectation_ref':exp['id'],'project_ref':pid,
                       'origin_event_ref':exp['origin_event'],
                       'appraisal_event_ref':appraisal['event'],
                       'appraisal_cue_ref':sign,'actor_appraisal':appraisal['appraisal'],
                       'current_event_ref':event_ref,'current_experience_ref':experience['ref'],
                       'current_cue_ref':cue['id'],'cue_terms':matching,
                       'location':experience['location'],'object_affect_ref':target}
                offers.append(basis)
                if len(offers)>=12:return offers
    return offers


def admit_activity_affect(actor, experience, event_ref, proposal):
    allowed={'kind','basis','affect_name','personal_sense','course_orientation'}
    if (set(proposal)!=allowed or proposal['basis'] not in
            (possible_self_expression_affects(actor,experience,event_ref)
             if isinstance(proposal.get('basis'),dict)
             and proposal['basis'].get('formation_source')=='OWN_PERFORMED_EXPRESSION'
             else possible_activity_affects(actor,experience,event_ref))):
        raise ValueError('ACTIVITY_AFFECT_UNQUALIFIED_HISTORY')
    for k,limit in (('affect_name',80),('personal_sense',400)):
        v=proposal[k]
        if type(v) is not str or not v.strip() or len(v)>limit:
            raise ValueError('ACTIVITY_AFFECT_INVALID_SEMANTIC_CONTENT')
    if proposal['course_orientation'] not in ('APPROACH','WITHHOLD','NO_DIRECT_TENDENCY'):
        raise ValueError('ACTIVITY_AFFECT_INVALID_COURSE_ORIENTATION')
    b=proposal['basis']
    exp=next(e for e in actor['expectations'] if e['id']==b['expectation_ref'])
    ident=stable_id('activity_affect',{'actor':actor['id'],'basis':b})
    rec={'id':ident,'actor':actor['id'],'expectation_ref':exp['id'],
         'project_ref':b['project_ref'],'origin_event_ref':event_ref,
         'basis':copy(b),'affect_name':proposal['affect_name'],
         'personal_sense':proposal['personal_sense'],
         'course_orientation':proposal['course_orientation'],
         'depth':2 if b['object_affect_ref'] is not None else 1,
         'grade':GRADE,'fictional_semantic_construction_not_diagnosis':True,
         'not_conscious_reason_or_world_truth':True}
    exp.setdefault('affective_organizations',[]).append(rec)
    return {'kind':'ACQUIRE_ACTIVITY_AFFECT','affect_ref':ident,
            'expectation_ref':exp['id'],'grade':GRADE}


def annotate_activity_affects(constitution, access, options):
    """Recruit the actual directed, potentially opposed historical formations.

    Affective significance is scoped to the particular project course and
    currently accessible context. It grants no action, changes no eligibility
    and is never summed into a universal affect score. No disclosure follows.
    """
    tags={str(t).casefold() for cue in access.cues for t in cue.get('tags',[])}
    by_project={}
    for exp in constitution.expectations[-256:]:
        if exp.get('actor')!=constitution.actor:continue
        for aff in exp.get('affective_organizations',[]):
            b=aff.get('basis',{})
            if (aff.get('actor')!=constitution.actor or aff.get('expectation_ref')!=exp['id']
                    or aff.get('project_ref')!=exp.get('project_id')
                    or b.get('location')!=access.location):continue
            if b.get('formation_source')=='OWN_ORDINARY_PROJECT_EXERCISE':
                from .activity import ordinary_project_actor_view, ordinary_vocal_project_site
                p=next((q for q in constitution.projects if q.get('id')==exp['project_id']),None)
                other=b.get('source_context_other_ref')
                if (not p or not ordinary_vocal_project_site(ordinary_project_actor_view(constitution),
                        p,access.location,access.world_clock)
                        or (other is not None and not any(c.get('kind')=='coactor_present'
                            and c.get('source_actor')==other for c in access.cues))):continue
            elif not tags.intersection(b.get('cue_terms',[])):continue
            by_project.setdefault(exp['project_id'],[]).append(aff)
    readset=set();currents=[]
    for opt in options:
        for alt in opt.get('practical_alternatives',[]):
            rows=by_project.get(alt.get('project_id'),[])
            if not rows or alt.get('binding_status')=='UNBOUND_PARTY_NOT_PRESENT':continue
            # An affect about one's own expressive practice concerns the
            # particular expressive course, not every means of its undertaking.
            rows=[a for a in rows if a['basis'].get('formation_source') not in (
                  'OWN_PERFORMED_EXPRESSION','OWN_ORDINARY_PROJECT_EXERCISE')
                  or a['basis'].get('expressive_operation')==opt['action']]
            if not rows:continue
            # Each relation is preserved, even if no action tendency follows.
            alt['course_affective_organizations']=[copy(a) for a in rows]
            orientations={a['course_orientation'] for a in rows}
            alt['affective_course_status']=('OPPOSED_AFFECTIVE_ORIENTATIONS'
                    if {'APPROACH','WITHHOLD'}<=orientations else 'DIFFERENTIATED_AFFECTIVE_SIGNIFICANCE')
            for a in rows:
                readset.add(a['id'])
                currents.append({'kind':'ACTIVITY_AFFECT_CURRENT','ref':a['id'],
                                 'project_ref':alt['project_id'],'option_ref':alt['option_id'],
                                 'operation':opt['action'],'orientation':a['course_orientation'],
                                 'object_affect_ref':a['basis']['object_affect_ref'],
                                 'not_public_self_knowledge':True})
    return {'readset':sorted(readset),'currents':currents}


# A historically formed manner of vocal enactment is neither the affect
# itself nor a diagnostic sign. Reuse the actual course/affect owner and
# evidence paths rather than introduce a universal emotion-to-face table.
CADENCES={'HALTING':'Speech with brief pauses.',
          'QUICKENED':'Speech in quick succession.',
          'EVEN':'Speech with an even cadence.'}

def own_vocal_reception(actor,experience):
    if (experience.get('actor')!=actor['id']
            or experience.get('own_action')!='SPEAK'
            or experience.get('status')!='PERFORMED'
            or experience.get('participated') is not True):return None
    signs=[c for c in experience.get('perceived_cues',[])
           if c.get('kind')=='performed_speak' and c.get('source_actor')==actor['id']
           and c.get('modality')=='auditory' and type(c.get('id')) is str]
    if len(signs)!=1:return None
    cue=signs[0]
    sel=experience.get('own_practical_selection') or {}
    ids=[a['id'] for row in sel.get('selected_course_affects_analytic_only',[])
         for a in row.get('affects',[]) if type(a.get('id')) is str]
    return {'cue_ref':cue['id'],'location':experience.get('location'),
            'selected_affect_refs_analytic_only':sorted(set(ids)),
            'cadence_as_sensed':cue.get('vocal_cadence','NOT_DIFFERENTIATED'),
            'not_self_explanation':True}

def _expressive_basis(actor,aff,path):
    voice=path.get('own_vocal_reception') or {}
    if (path.get('own_action')!='SPEAK'
            or path.get('purpose_status')!='ACTOR_POLICY_SELECTED_PROJECT_COURSE'
            or aff['project_ref'] not in path.get('selected_project_refs',[])
            or aff['id'] not in voice.get('selected_affect_refs_analytic_only',[])
            or voice.get('cue_ref') not in path.get('received_cue_refs',[])
            or voice.get('location')!=aff.get('basis',{}).get('location')):return None
    paths=actor.get('evidence_paths',[])
    origin=next((i for i,p in enumerate(paths)
                 if p.get('event')==aff.get('origin_event_ref')),None)
    if origin is None:return None
    current=next((i for i,p in enumerate(paths) if p.get('event')==path['event']),None)
    if current is None or current<=origin:return None
    prior=[p for p in paths[origin+1:current]
           if p.get('own_action')=='SPEAK'
           and p.get('purpose_status')=='ACTOR_POLICY_SELECTED_PROJECT_COURSE'
           and aff['project_ref'] in p.get('selected_project_refs',[])
           and aff['id'] in (p.get('own_vocal_reception') or {}).get('selected_affect_refs_analytic_only',[])
           and (p.get('own_vocal_reception') or {}).get('location')==voice['location']
           and (p.get('own_vocal_reception') or {}).get('cue_ref') in p.get('received_cue_refs',[])
           and (p.get('own_vocal_reception') or {}).get('cue_ref')!=voice['cue_ref']]
    if not prior:return None
    earlier=prior[-1]
    return {'actor':actor['id'],'affect_ref':aff['id'],'project_ref':aff['project_ref'],
            'location':voice['location'],'earlier_event_ref':earlier['event'],
            'later_event_ref':path['event'],'later_experience_ref':path['experience_ref'],
            'earlier_cue_ref':earlier['own_vocal_reception']['cue_ref'],
            'later_cue_ref':voice['cue_ref'],'grade':GRADE}

def possible_expressive_practices(actor,experience,event_ref):
    if experience.get('actor')!=actor['id']:return []
    paths=[p for p in actor.get('evidence_paths',[])
           if p.get('event')==event_ref and p.get('experience_ref')==experience.get('ref')]
    if len(paths)!=1 or own_vocal_reception(actor,experience)!=paths[0].get('own_vocal_reception'):return []
    out=[]
    for exp in actor.get('expectations',[])[-128:]:
        for aff in exp.get('affective_organizations',[])[-16:]:
            if aff.get('actor')!=actor['id'] or aff.get('expectation_ref')!=exp.get('id') or aff.get('expressive_practice'):continue
            b=_expressive_basis(actor,aff,paths[0])
            if b:out.append({'basis':b,'allowed_cadences':list(CADENCES)})
            if len(out)>=8:return out
    return out

def admit_expressive_practice(actor,experience,event_ref,proposal):
    if (set(proposal)!={'kind','basis','cadence'}
            or proposal['cadence'] not in CADENCES
            or not any(x['basis']==proposal['basis'] for x in possible_expressive_practices(actor,experience,event_ref))):
        raise ValueError('EXPRESSIVE_PRACTICE_UNQUALIFIED_HISTORY')
    b=proposal['basis']
    aff=next(a for e in actor['expectations'] for a in e.get('affective_organizations',[])
             if a['id']==b['affect_ref'])
    ident=stable_id('expressive_practice',{'basis':b,'cadence':proposal['cadence']})
    aff['expressive_practice']={'id':ident,'basis':copy(b),'cadence':proposal['cadence'],
        'not_a_universal_emotion_display_or_conscious_intention':True,'grade':GRADE}
    return {'kind':proposal['kind'],'practice_ref':ident,'grade':GRADE}

def realized_vocal_cadence(actor,attempt,location):
    """Actual world writer reads acquired history, emits only physical manner.

    No private cause, project, affect name or receipt ID enters the public cue.
    A single unambiguous acquired manner can operate without a chosen display.
    Contradictory manners are unresolved, not averaged into a diagnosis.
    """
    if (attempt.action!='SPEAK' or attempt.actor!=actor['id']
            or actor['body'].get('language',0)<.35
            or actor['body'].get('rest',0)<.12):return None
    sel=attempt.practical_selection
    if sel.get('status')!='ACTOR_POLICY_PRACTICAL_ATTEMPT' or len(sel.get('selected_project_refs',[]))!=1:return None
    recruited={a['id'] for row in sel.get('selected_course_affects_analytic_only',[])
               if row.get('project_id') in sel['selected_project_refs']
               for a in row.get('affects',[]) if type(a.get('id')) is str}
    manners=set()
    for exp in actor.get('expectations',[])[-128:]:
        for aff in exp.get('affective_organizations',[])[-16:]:
            rec=aff.get('expressive_practice')
            if (aff.get('id') not in recruited or not rec or aff.get('actor')!=actor['id']
                    or aff.get('project_ref') not in sel['selected_project_refs']
                    or rec.get('basis',{}).get('location')!=location):continue
            path=next((p for p in actor.get('evidence_paths',[])
                       if p.get('event')==rec['basis'].get('later_event_ref')),None)
            if not path or _expressive_basis(actor,aff,path)!=rec['basis']:continue
            if rec.get('cadence') in CADENCES and rec.get('id')==stable_id('expressive_practice',{'basis':rec['basis'],'cadence':rec['cadence']}):
                manners.add(rec['cadence'])
    return next(iter(manners)) if len(manners)==1 else None


def possible_self_expression_affects(actor, experience, event_ref):
    """A person's actual received expression can become a new affective object.

    The earlier acquired affect and expressive practice are distinct from
    actual later bodily performance and its personal reception. A semantic
    proposal can form a higher-order orientation, including indifference or
    opposed significance, without claiming conscious causal understanding.
    This bounded first draft preserves parent affect, expressive practice,
    and project; it does not compel insight, shame, pride, or repression.
    """
    aid=actor.get('id')
    voice=own_vocal_reception(actor,experience)
    if not voice or voice['cadence_as_sensed'] not in CADENCES:return []
    paths=actor.get('evidence_paths',[])
    current=[(i,p) for i,p in enumerate(paths)
             if p.get('event')==event_ref and p.get('experience_ref')==experience.get('ref')]
    if len(current)!=1:return []
    i,path=current[0]
    if (path.get('own_vocal_reception')!=voice
            or path.get('own_action')!='SPEAK'
            or path.get('purpose_status')!='ACTOR_POLICY_SELECTED_PROJECT_COURSE'
            or len(path.get('selected_project_refs',[]))!=1
            or voice['cue_ref'] not in path.get('received_cue_refs',[])):
        return []
    pid=path['selected_project_refs'][0]
    if not any(p.get('id')==pid and p.get('status','active')=='active'
               for p in actor.get('projects',[])):return []
    # If distinct recruited practices could explain the same audible sign,
    # do not attribute it to a particular parent organization here.
    qualified=[]
    for exp in actor.get('expectations',[])[-128:]:
        if exp.get('actor')!=aid or exp.get('project_id')!=pid:continue
        for aff in exp.get('affective_organizations',[])[-16:]:
            rec=aff.get('expressive_practice')
            if (not rec or aff.get('depth')!=1 or aff.get('actor')!=aid
                    or aff.get('expectation_ref')!=exp['id']
                    or aff.get('project_ref')!=pid
                    or aff.get('id') not in voice['selected_affect_refs_analytic_only']
                    or rec.get('cadence')!=voice['cadence_as_sensed']
                    or aff.get('basis',{}).get('location')!=voice['location']
                    or rec.get('basis',{}).get('location')!=voice['location']):
                continue
            prior=[p for p in paths[:i] if p.get('event')==rec['basis'].get('later_event_ref')]
            if (len(prior)!=1 or _expressive_basis(actor,aff,prior[0])!=rec['basis']
                    or rec.get('id')!=stable_id('expressive_practice',
                         {'basis':rec['basis'],'cadence':rec['cadence']})
                    or voice['cue_ref'] in (rec['basis'].get('earlier_cue_ref'),
                                             rec['basis'].get('later_cue_ref'))):
                continue
            qualified.append((exp,aff,rec))
    if len(qualified)!=1:return []
    exp,aff,rec=qualified[0]
    if any(a.get('basis',{}).get('source_expressive_practice_ref')==rec['id']
           for e in actor.get('expectations',[]) for a in e.get('affective_organizations',[])):
        return []
    return [{'formation_source':'OWN_PERFORMED_EXPRESSION',
             'expectation_ref':exp['id'],'project_ref':pid,
             'origin_event_ref':exp['origin_event'],
             'parent_affect_event_ref':aff['origin_event_ref'],
             'object_affect_ref':aff['id'],
             'source_expressive_practice_ref':rec['id'],
             'practice_acquisition_event_ref':rec['basis']['later_event_ref'],
             'current_event_ref':event_ref,'current_experience_ref':experience['ref'],
             'current_cue_ref':voice['cue_ref'],
             'cadence_as_sensed':voice['cadence_as_sensed'],
             'location':voice['location'],
             'cue_terms':copy(aff['basis']['cue_terms']),
             'expressive_operation':'SPEAK',
             'not_conscious_self_explanation_or_observer_interpretation':True}]
