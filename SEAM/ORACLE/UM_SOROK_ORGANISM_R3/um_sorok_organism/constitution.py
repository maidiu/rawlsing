"""READ MODEL for the entire, possibly dormant and contradictory person; pure composition.
No psychology state is minted by materialization. This module is deliberately read-only.
"""
from .types import Constitution, Situated, AccessibleEncounter, copy
from .organism import eligible, ACTIONS
from .activity import eligible_activities
from .psychodynamics import enact_currents
from .relational_metabolism import derive_relational_metabolism
from .plans import qualified_learned_compositions
from .practical_difference import practical_alternatives
from .preproject_agency import recruit_preproject_anticipations
from .prospective_horizon import project_trial_horizons
from .attention_field import situate_attention
from .distributed_power import conditional_assistance_options
from .practical_powers import situated_exercised_repertoire
from .practical_inquiry import offer_actor_inquiry, notices_present
from .material_objects import (
    material_objects_present, can_make, object_bound_alternatives,
    material_opportunity_from_history)
from .functional_correspondence import project_functional_correspondences
from .world import _qualified_members
from .institutional_reproduction import current_institutional_opportunities


def materialize(actor,world):
    world_rels=[copy(v) for v in world['relations'].values() if actor['id'] in v.get('participants',[])]
    return Constitution(actor=actor['id'],clock=world['clock'],body=copy(actor['body']),
        forms=copy(actor['forms']),links=copy(actor['links']),projects=copy(actor['projects']),
        activity_links=copy(actor.get('activity_links',[])),
        composition_methods=copy(actor.get('composition_methods',[])),
        relational_motifs=copy(actor.get('relational_motifs',[])),
        possible_ends=copy(actor.get('possible_ends',[])),
        evidence_paths=copy(actor.get('evidence_paths',[])),
        expectations=copy(actor.get('expectations',[])),
        participation_history=copy(actor.get('participation_history',[])),
        functional_bindings=copy(actor.get('functional_bindings',[])),
        power_exercises=copy(actor.get('power_exercises',[])),
        notice_exposures=copy(actor.get('notice_exposures',[])),
        memories=copy(actor['memories']),traces=copy(actor['traces']),
        other_models=copy(actor['other_models']),self_model=copy(actor['self_model']),
        relations=world_rels,unknowns=list(actor['unknowns']),history_refs=list(actor.get('history_refs',[])))


def actor_access(actor,world):
    """Objective cues are never automatically the actor's concepts or memories."""
    location=world['positions'].get(actor['id'])
    cues=[]; counted=0;receipts=[]
    for x in world['cues']:
        # An event in history is not a permanently present sensory object.
        # Materially persistent signs require an explicit, bounded lifetime.
        if not (x.get('clock', -1) <= world['clock'] <= x.get('last_access_clock', -1)):
            counted+=1;continue
        if x.get('location') not in (location,'all'):
            counted+=1;continue
        sense=x.get('modality','visual')
        if sense in ('visual','auditory') and actor['body']['sensor']<x.get('threshold',.05):
            counted+=1;continue
        if x.get('private_to') not in (None,actor['id']):
            counted+=1;continue
        cues.append(copy(x));receipts.append(x['id'])
    # Co-presence is an objective present opportunity, not an assertion about
    # the other's intentions, consent, feelings, or accessible psychology.
    if actor['body']['sensor'] >= .05:
        for other,where in sorted(world['positions'].items()):
            if other!=actor['id'] and where==location:
                cues.append({'id':'presence:'+other+':'+str(world['clock']),
                    'clock':world['clock'],'kind':'coactor_present',
                    'tags':['coactor',other],'source_actor':other,'location':location,
                    'modality':'present','description':'co-present other actor'})
    # An objectively posted notice is an opportunity to inspect public
    # information, not automatic possession of its words or an explanation
    # of an earlier obstruction. Reading requires an actual later operation.
    if actor['body']['sensor'] >= .05:
        for notice in notices_present(world,location,world['clock']):
            cues.append({
                'id':'public_notice_visible:'+notice['id']+':'+str(world['clock']),
                'clock':world['clock'],
                'kind':'public_notice_visible',
                'public_notice_ref':notice['id'],
                'tags':['posted','public_notice'],
                'modality':'visual',
                'location':location,'description':'a visible posted public notice',
                'public_content_not_yet_experienced':True})
    if actor['body']['sensor'] >= .05:
        for obj in material_objects_present(world,location):
            cues.append({
                'id':'material_object_visible:'+obj['id']+':'+str(world['clock']),
                'clock':world['clock'],'kind':'material_object_present',
                'material_object_ref':obj['id'],
                'tags':['material_object','object_present'],
                'modality':'visual','location':location,
                'description':'a visible worked material object',
                'ownership_and_private_history_not_perceived':True})
    env=[]
    site=world['sites'].get(location,{})
    if (site.get('access')=='public' or actor['id'] in _qualified_members(site,'admitted','INVALID_SITE_ADMISSION')):env.append('SITE_ACCESS')
    # A publicly posted objective practice can make participation feasible
    # without implying the person already cares about this institution.
    if actor['body']['sensor'] >= .05:
        env += [v['operation'] for v in current_institutional_opportunities(
            world,actor['id'],location)]
    if any(c.get('kind')=='coactor_present' for c in cues):
        env.append('PLEDGE_CARE')
    if actor['body']['sensor'] >= .05 and can_make(world,actor['id'],location):
        env.append('MAKE_OBJECT')
    if any(x.get('kind')=='material_object_present' for x in cues):
        env.append('INSPECT')
    env+=['REST','WAIT','ORIENT','SIGNAL']
    return AccessibleEncounter(actor['id'],world['clock'],location,cues,sorted(set(env)),receipts,counted)


def _tokens(cues):
    return set(v.lower() for c in cues for v in (c.get('tags',[])+[c.get('kind','')]))


def _form_in_scope(form,access):
    scope=form.get('scope',{})
    if scope.get('locations') and access.location not in scope['locations']:
        return False
    counterpart=scope.get('counterpart')
    if counterpart and not any(c.get('source_actor')==counterpart for c in access.cues):
        return False
    return True

def compose(constitution,access,limit=50):
    """Three streams: direct cue/ongoing project, acquired associative links, qualified traces.
    Does not select a motive, infer actor memory from objective facts, or claim transfer
    where the encoded form's scope prohibits it.
    """
    if constitution.actor!=access.actor:raise ValueError('ACTOR_IDENTITY_MISMATCH')
    forms=constitution.forms; cues=_tokens(access.cues)
    active={}; dormant=[]; inhibited=[]; currents=[]; disagreements=[]
    # A contextual project that is not presently recruited must NOT prime its
    # own cues. Otherwise an unseen future project bootstraps a form into the
    # present, and the form is then misrepresented as the project's cause.
    seed_projects=eligible_activities(constitution,(),access)
    project_tags=set(v.lower() for p in seed_projects for v in p.get('cue_terms',[]))
    for fid,f in forms.items():
        if f.get('lifecycle') in ('ENDED','DORMANT'):
            dormant.append(fid);continue
        if f.get('body_min',0)>constitution.body['motor']:inhibited.append(fid);continue
        if not _form_in_scope(f,access):
            dormant.append(fid);continue
        match=set(str(x).lower() for x in f.get('cues',[]))
        if match & (cues|project_tags) or f.get('always_recruitable'):
            active[fid]=copy(f)
    # P012: evidence-bounded reachability to a real fixed point, independently
    # of arbitrary link order or a three-pass depth limit. A qualifying
    # inhibitor blocks its target's ability to become a recruitment conduit;
    # it cannot first recruit a descendant and then disappear at the end.
    #
    # We use a conservative two-stage lattice: positive possible reachability,
    # then inhibitor veto by all potential qualified active sources, followed
    # by positive reachability without vetoed conduits. This may over-suppress
    # under opposing cycles; it never fabricates the affected form's action.
    seed=set(active)
    qualified={fid for fid,f in forms.items()
        if f.get('lifecycle') not in ('ENDED','DORMANT')
        and f.get('body_min',0)<=constitution.body['motor']
        and _form_in_scope(f,access)}
    valid_links=[link for link in constitution.links
        if link.get('source') in forms and link.get('target') in forms
        and (not link.get('contexts') or access.location in link['contexts'])]
    # PRE-A0's explicitly admitted relation functions must do work; not
    # merely appear in a relation-history report. Activation and suppression
    # still respect the form's own scope and bodily eligibility.
    positive=[link for link in valid_links if link.get('relation') in
              ('RECRUITS','SUPPORTS','ACTIVATES','REINFORCES')]
    negative=[link for link in valid_links if link.get('relation') in
              ('INHIBITS','SUPPRESSES')]

    def closure(start, blocked=frozenset()):
        reached=set(start)&qualified-set(blocked)
        # Monotonic form set grows at most len(qualified) times, cycles stop.
        while True:
            added={l['target'] for l in positive
                   if l['source'] in reached and l['target'] in qualified
                   and l['target'] not in blocked}
            newer=reached|added
            if len(newer)==len(reached):return reached
            reached=newer

    potentially_active=closure(seed)
    vetoed={l['target'] for l in negative if l['source'] in potentially_active}
    # Acquired configurations can recruit a third, historically existing
    # form. The bounded monotonic closure keeps new inhibitors from sneaking
    # an already vetoed conduit into the current. This is conservative under
    # contradictory loops (it may over-suppress) and is NOT a global psyche
    # optimizer, conscious retrieval manager or clinical conflict law.
    motif_seeds=set()
    motif_routes={}
    for _ in range(2*len(qualified)+2):
        reachable=closure(seed|motif_seeds,vetoed)
        projection=derive_relational_metabolism(
            constitution,access,{fid:forms[fid] for fid in reachable},vetoed)
        proposed={route['target_form'] for route in projection['recruitment_candidates']
                  if route['target_form'] in qualified}
        for route in projection['recruitment_candidates']:
            if route['target_form'] in qualified:
                motif_routes.setdefault(route['target_form'],route)
        possible=closure(seed|motif_seeds|proposed)
        next_veto=vetoed|{l['target'] for l in negative
                         if l['source'] in possible}
        next_seeds=motif_seeds|proposed
        if next_veto==vetoed and next_seeds==motif_seeds:
            break
        vetoed=next_veto;motif_seeds=next_seeds
    else:
        raise RuntimeError('RELATIONAL_RECRUITMENT_DID_NOT_CONVERGE')
    inhibited.extend(sorted(vetoed))
    active={fid:copy(forms[fid]) for fid in closure(seed|motif_seeds,vetoed)}
    relational=derive_relational_metabolism(constitution,access,active,vetoed)
    for fid,route in sorted(motif_routes.items()):
        if fid in active and fid not in closure(seed,vetoed):
            currents.append({'kind':'HISTORICALLY_RECRUITED_VIA_MOTIF',
                'ref':fid,'motif_ref':route['motif_ref'],
                'qualified_source_forms':route['source_form_refs'],
                'had_inhibited_source':bool(route['suppressed_source_refs']),
                'not_actor_conscious_retrieval':True})
    # History-made links to activities can recruit an ongoing project under
    # a new cue. Its object/motive remains separate from its possible means.
    projects=eligible_activities(constitution,active.keys(),access)
    # Trace reads are only admitted trace references, not recovered episodic memory.
    traces=[t for t in constitution.traces if set(t.get('cue_terms',[]))&(cues|project_tags)]
    for t in traces[:limit]:currents.append({'kind':'NONDECLARATIVE_TRACE','ref':t['id'],'manifestation':t.get('manifestation','uninterpreted')})
    # An earlier experienced possibility may become situatedly relevant again,
    # without instantly becoming a project, desired end, or self-narrative.
    # We read bounded historical descendants of actual actor-received cues.
    candidate_history_refs=set()
    for end in constitution.possible_ends[-128:]:
        if end.get('status')!='POSSIBLE_NOT_ACQUIRED_MOTIVE':
            continue
        qualified={str(x).lower() for x in end.get('cue_terms',[])}
        if qualified and qualified & cues:
            candidate_history_refs.add(end['id'])
            currents.append({
                'kind':'HISTORICALLY_NOTICED_POSSIBLE_END',
                'ref':end['id'],
                'possible_object_for_analytic_construction':end['possible_object'],
                'actual_origin_event':end['origin_event'],
                'not_automatically_an_active_motive':True,
                'not_necessarily_actor_self_articulated':True})
    # Seeking, avoiding, staying or leaving can change what evidence was
    # available later. Historical path receipts are NOT observations of
    # counterfactual encounters or proof of a learned causal theory.
    for previous in constitution.evidence_paths[-64:]:
        prior_tags={str(x).lower()
                    for x in previous.get('received_cue_tags',[])}
        if prior_tags and prior_tags & cues:
            candidate_history_refs.add(previous['experience_ref'])
            currents.append({
                'kind':'HISTORICAL_SIGNAL_PATH_REENCOUNTERED',
                'ref':previous['experience_ref'],
                'old_operation':previous.get('own_action'),
                'old_selected_project_refs':copy(previous.get(
                    'selected_project_refs',[])),
                'not_imputed_counterfactual':True,
                'no_automatic_belief_update':True})
    for field in constitution.relations:
        if 'REPEATED_JOINT_ACT_OBSERVED' in field.get('observed_patterns',[]):
            counterpart=[x for x in field['participants'] if x!=constitution.actor]
            if any(c.get('source_actor') in counterpart for c in access.cues):
                currents.append({'kind':'WORLD_RELATIONAL_FIELD_OBSERVATION', 'ref':field['id'],
                                 'objective_pattern':'REPEATED_JOINT_ACT_OBSERVED',
                                 'joint_capability_unproved':True,
                                 'not_personal_investment':True})
    for p in projects:
        if p.get('status','active')=='active':currents.append({'kind':'ONGOING_ACTIVITY','ref':p['id'],'object':p['object'],'motive':p.get('motive','UNSPECIFIED_ACQUIRED_MOTIVE'),
            'priority':p.get('priority',.5),'recruitment_basis':p.get('recruitment_basis',[]),
            'means':copy(p.get('means',[])),
            'latest_lived_attempt':copy(p.get('latest_lived_attempt'))})
    for fid,f in active.items():
        currents.append({'kind':f['kind'],'ref':fid,'object':f.get('object'),'actor_access':f.get('access','tacit')})
    for a in constitution.links:
        if a['relation']=='COMPETES' and a['source'] in active and a['target'] in active:
            disagreements.append({'a':a['source'],'b':a['target'],'reason':'ADMITTED_COMPETITION'})
    actions={}
    for fid,f in active.items():
        for a in f.get('enables',[]):
            status,why=eligible(constitution.body,a)
            if status:
                q=actions.setdefault(a,{'action':a,'score':.1,'basis':[],'opportunity':'ACQUIRED'})
                q['score']+=.24*f.get('strength',.5);q['basis'].append(fid)
    for p in projects:
        if p.get('status','active')!='active':continue
        for a in p.get('means',[]):
            status,why=eligible(constitution.body,a)
            if status:
                q=actions.setdefault(a,{'action':a,'score':.1,'basis':[],'opportunity':'PROJECT'})
                # A richer description of one purpose must not cast more
                # votes for the same physical operation. Project availability
                # uses a MAX ceiling, not the sum of every candidate motive.
                q['project_pressure_ceiling']=max(
                    q.get('project_pressure_ceiling',0),.4*p.get('priority',.5))
                q['basis'].append('project:'+p['id'])
                # Multiple projects may afford this *same* bodily action.
                # Their presence is candidate opportunity, NOT a claim that
                # all those purposes were selected in the impending attempt.
                q.setdefault('practical_objects',[]).append(p['object'])
                q.setdefault('motive_hypotheses',[]).append(p.get('motive','UNKNOWN'))
                q.setdefault('project_courses',[]).append({
                    'project_id':p['id'],
                    'object':p['object'],
                    'motive_hypothesis':p.get('motive','UNKNOWN'),
                    'priority':p.get('priority',.5),
                    'recruitment_basis':copy(p.get('recruitment_basis',[])),
                    'course_grade':'AVAILABLE_PURPOSE_NOT_SELECTED_INTENT'})
                q['pooled_basis_is_not_actor_selected_purpose']=True
    for q in actions.values():
        if 'project_pressure_ceiling' in q:
            q['score']+=q['project_pressure_ceiling']
            q['score_aggregation']='MAX_AVAILABLE_PROJECT_PRESSURE_NOT_SUM_OF_MOTIVES'
    # Actual prior exercise may make an operation available on a later
    # occasion without attributing the actor's motive, independent mastery,
    # a new world right, or the earlier coactor's future willingness.
    exercised=situated_exercised_repertoire(constitution,access)
    for candidate in exercised['offered']:
        action=candidate['action']
        entry=actions.setdefault(action,{
            'action':action,'score':candidate['score'],'basis':[],
            'opportunity':'HISTORICALLY_EXERCISED_POSSIBILITY'})
        entry['basis']+=['exercise:'+r for r in candidate['basis']]
        entry.setdefault('practical_exercise_sources',[]).extend(
            candidate['source_event_refs'])
        entry.setdefault('historical_support_statuses',[]).extend(
            candidate['historical_support_statuses'])
        entry['score']=max(entry['score'],candidate['score'])
    inquiry=offer_actor_inquiry(constitution,access)
    for candidate in inquiry['offered']:
        action=candidate['action']
        entry=actions.setdefault(action,{
            'action':action,'score':candidate['score'],'basis':[],
            'opportunity':'ACTOR_HISTORICAL_EVIDENCE_SEEKING'})
        entry['score']=max(entry['score'],candidate['score'])
        entry['basis']+=candidate['basis']
        entry.setdefault('candidate_notice_refs',[]).extend(
            candidate['candidate_notice_refs'])
    material=material_opportunity_from_history(constitution,access)
    for candidate in material['offers']:
        op=candidate['action']
        entry=actions.setdefault(op,{
            'action':op,'score':candidate['score'],'basis':[],
            'opportunity':'HISTORICALLY_PROPOSED_MATERIAL_COMPOSITION'})
        entry['score']=max(entry['score'],candidate['score'])
        entry['basis']+=candidate['basis']
    if 'INSPECT' in access.affordances:
        ok,_=eligible(constitution.body,'INSPECT')
        if ok:
            actions.setdefault('INSPECT',{
                'action':'INSPECT','score':.078,
                'basis':['CURRENT_MATERIAL_OBJECT_VISIBLE'],
                'opportunity':'MATERIAL_OBJECT_CAN_BE_INSPECTED_NOT_A_GOAL'})
    # Developmentally rudimentary orienting and self-preserving actions remain possible
    # even with no acquired conceptual operations.
    for a in ('WAIT','REST','ORIENT','SIGNAL'):
        status,why=eligible(constitution.body,a)
        if status:actions.setdefault(a,{'action':a,'score':.06,'basis':['organism'],'opportunity':'ORGANISM'})
    if 'PLEDGE_CARE' in access.affordances:
        status,why=eligible(constitution.body,'PLEDGE_CARE')
        if status:
            actions.setdefault('PLEDGE_CARE',{
                'action':'PLEDGE_CARE','score':.045,
                'basis':['ACTUAL_CO_PRESENT_POSSIBLE_ADDRESSEE'],
                'opportunity':'PROMISE_CAN_BE_MADE_NOT_FUTURE_FULFILLED'})
    if 'SIGN_HALL_PETITION' in access.affordances:
        status,why=eligible(constitution.body,'SIGN_HALL_PETITION')
        if status:
            actions.setdefault('SIGN_HALL_PETITION',{
                'action':'SIGN_HALL_PETITION','score':.055,
                'basis':['WORLD_PUBLISHED_INSTITUTIONAL_PROCEDURE'],
                'opportunity':'PUBLIC_RIGHT_NOT_PREASSIGNED_SOLIDARITY'})
    for a,q in actions.items():
        if a in ('WORK','REPAIR','SING','JOIN','MAKE_SPACE','OPEN_HALL') and access.location not in ('workshop','home','hall'):
            q['score']*=.45
        if a=='REST' and constitution.body['rest']<.45:q['score']+=1.0
        if a=='EAT' and constitution.body['nutrition']<.5:q['score']+=1.0
        if a=='SIGNAL' and constitution.body['comfort']<.4:q['score']+=.6
    # An inhibited form can still have an indirect, historically admitted
    # effect on another form or action. Never reinstate its direct capabilities.
    currents+=relational['currents']
    dynamics=enact_currents(constitution,access,active,actions.values(),
                             relational=relational)
    currents+=dynamics['currents']
    # Nondeclarative, historically acquired orientation can matter BEFORE an
    # explicit project exists. A read does not write new psychic content.
    preproject=recruit_preproject_anticipations(constitution,access,dynamics['candidate_actions'])
    currents+=preproject['currents']
    # These effects are *derived* from present bodily state and historically
    # acquired forms, never silently committed as an event or a new mind state.
    inhibited+=['action:'+x['action'] for x in dynamics['suspended']]
    learned=qualified_learned_compositions(constitution,access,active,projects,
                                          dynamics['candidate_actions'])
    # Meaning can be received without every sign becoming available for
    # focal, costly practical consideration. Tacit recruited psychology used
    # original access; only deliberate means/beneficiary binding uses the
    # presently nominated, scarce attentional field.
    attention=situate_attention(constitution,access)
    # Attach actor/clock/project-specific practical ALTERNATIVES beneath the
    # existing physical action grammar. Psychodynamic inhibition still acts
    # first; an inhibited operation cannot be revived by an option ID.
    for option in dynamics['candidate_actions']:
        option['practical_alternatives']=practical_alternatives(
            constitution,attention['focus_access'],option)
        # A learned relation of distributed practical power can add a real
        # future *invitation* alternative. The Other's policy remains their own.
        option['practical_alternatives']+=conditional_assistance_options(
            constitution,attention['focus_access'],option)
        option['practical_alternatives']+=object_bound_alternatives(
            constitution,attention['focus_access'],option['action'])
        if option['action']=='INSPECT' and option.get('candidate_notice_refs'):
            option['practical_alternatives'] += [
                {'option_id':'inquiry:'+constitution.actor+':'+
                  str(constitution.clock)+':'+str(ref),
                 'actor':constitution.actor,'as_of_clock':constitution.clock,
                 'operation':'INSPECT','project_id':None,
                 'grounds_status':'HISTORICALLY_FRUSTRATED_EVIDENCE_SEEKING',
                 'world_request':{'operation':'INSPECT',
                     'addressed_party_ref':None,'material_object_ref':ref},
                 'anticipated_difference':None,
                 'binding_status':'PUBLIC_POSTED_NOTICE_ACTOR_SITUATED',
                 'not_secret_world_explanation':True,
                 'grade':'SOURCEFREE_RESEARCH_PROVISIONAL'}
                for ref in option['candidate_notice_refs']]
    # The same historically noticed end can offer several ACTUAL eligible
    # operations without becoming an acquired project or being given an
    # automatic conscious object. This projection never grants capability.
    functional=project_functional_correspondences(
        constitution,attention['focus_access'])
    currents.extend({'kind':'QUALIFIED_PROVISIONAL_FUNCTIONAL_CORRESPONDENCE',
                     **copy(row)} for row in functional['active'])
    prospective=project_trial_horizons(
        constitution,attention['focus_access'],dynamics['candidate_actions'],
        functional_correspondences=functional['active'])
    currents+=prospective['currents']
    ordered=sorted(dynamics['candidate_actions'],key=lambda x:(-x['score'],x['action']))[:limit]
    return Situated(actor=constitution.actor,clock=constitution.clock,recruited=list(active.values()),
       dormant=sorted(set(dormant)),inhibited=sorted(set(inhibited)),currents=currents,
       accessible_cues=access.cues,candidate_actions=ordered,disagreements=disagreements,
       readset=sorted(set(list(active)+list(vetoed)+relational['readset']+
                           preproject['readset']+exercised['readset']+
                           material['readset']+
                           inquiry['readset']+
                           functional['readset']+
                           prospective['readset']+
                           list(candidate_history_refs)+
                           [t['id'] for t in traces]+access.access_receipts)),
       unknowns=list(constitution.unknowns),antagonisms=dynamics['antagonisms'],
       suspended_actions=dynamics['suspended'],learned_compositions=learned,
       attention_frame=attention['frame'])
