"""READ MODEL for the entire, possibly dormant and contradictory person; pure composition.
No psychology state is minted by materialization. This module is deliberately read-only.
"""
import math
from .types import Constitution, Situated, AccessibleEncounter, copy, GRADE
from .organism import eligible, ACTIONS
from .activity import eligible_activities, annotate_interactivity_relations
from .psychodynamics import enact_currents
from .relational_metabolism import derive_relational_metabolism
from .plans import qualified_learned_compositions
from .practical_difference import practical_alternatives
from .preproject_agency import recruit_preproject_anticipations
from .prospective_horizon import project_trial_horizons
from .attention_field import situate_attention
from .historical_self_organization import pre_cue_pressures
from .care_commitment_genesis import practiced_care_alternatives
from .cultural_mediation import cultural_object_alternatives
from .distributed_power import conditional_assistance_options
from .practical_powers import situated_exercised_repertoire
from .practical_inquiry import offer_actor_inquiry, notices_present
from .institutional_procedure_learning import annotate_notice_expectations
from .material_objects import (
    material_objects_present, can_make, object_bound_alternatives,
    material_opportunity_from_history)
from .material_investments import (
    invested_material_action_options, annotate_material_alternatives)
from .mediated_efficacy import situated_component_efficacy
from .functional_correspondence import project_functional_correspondences
from .world import (_qualified_members, _nonnegative_transfer_amount,
                    recursive_encounter_channels, project_recursive_actor_sign)
from .institutional_reproduction import current_institutional_opportunities
from .expectation_afterlife import annotate_practical_expectations, annotate_activity_affects
from .co_regulation_history import (
    recruit_co_regulation, addressed_signal_alternatives)
from .caregiving_practice import project_repeat_feeding
from .food_access_struggle import (
    live_food_petition_opportunity, offered_food_petition)
from .food_power_reproduction import (
    food_power_opportunities,COMMONS,INSTALL,MAINTAIN,SANCTION,
    OFFER,ACCEPT)
from .labor_dependency import (
    actor_work_opportunities,work_permission,situated_suspension_targets,
    ACCEPT as LABOR_ACCEPT,SUSPEND as LABOR_SUSPEND,
    RESIGN as LABOR_RESIGN,CONTRIBUTE as LABOR_FUND,DRAW as LABOR_DRAW)


def materialize(actor,world):
    world_rels=[copy(v) for v in world['relations'].values() if actor['id'] in v.get('participants',[])]
    return Constitution(actor=actor['id'],clock=world['clock'],body=copy(actor['body']),
        role=actor['role'],age_days=actor['age_days'],
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
        object_encounters=copy(actor.get('object_encounters',[])),
        material_investments=copy(actor.get('material_investments',[])),
        practice_exposures=copy(actor.get('practice_exposures',[])),
        undergone_care_periods=copy(actor.get('undergone_care_periods',[])),
        co_regulation_orientations=copy(actor.get('co_regulation_orientations',[])),
        experienced_care_events=copy(actor.get('experienced_care_events',[])),
        performed_feeding_events=copy(actor.get('performed_feeding_events',[])),
        institutional_expectations=copy(actor.get('institutional_expectations',[])),
        material_dependency_encounters=copy(actor.get(
            'material_dependency_encounters',[])),
        labor_dependency_encounters=copy(actor.get(
            'labor_dependency_encounters',[])),
        lived_genesis_episodes=copy(actor.get(
            'lived_genesis_episodes',[])),
        joint_practices=copy(actor.get('joint_practices',[])),
        care_contribution_episodes=copy(actor.get(
            'care_contribution_episodes',[])),
        care_practical_commitments=copy(actor.get(
            'care_practical_commitments',[])),
        cultural_demonstrations=copy(actor.get(
            'cultural_demonstrations',[])),
        cultural_reference_practices=copy(actor.get(
            'cultural_reference_practices',[])),
        vocal_turn_experiences=copy(actor.get(
            'vocal_turn_experiences',[])),
        vocal_coordination_practices=copy(actor.get(
            'vocal_coordination_practices',[])),
        historical_orientations=copy(actor.get('historical_orientations',[])),
        memories=copy(actor['memories']),traces=copy(actor['traces']),
        other_models=copy(actor['other_models']),self_model=copy(actor['self_model']),
        relations=world_rels,unknowns=list(actor['unknowns']),history_refs=list(actor.get('history_refs',[])))


def actor_access(actor,world):
    """Objective cues are never automatically the actor's concepts or memories."""
    # P071 finite-sensor check and P067 closed historical sensory gate.
    eligible(actor['body'],'WAIT')
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
        threshold=x.get('threshold',.05)
        tags=x.get('tags',[])
        if (sense not in ('visual','auditory','tactile','olfactory') or
                not isinstance(tags,list) or
                any(not isinstance(t,str) for t in tags) or
                not isinstance(x.get('kind',''),str) or
                isinstance(threshold,bool) or not isinstance(threshold,(int,float)) or
                not math.isfinite(threshold) or not 0<=threshold<=1):
            counted+=1;continue
        if actor['body']['sensor']<threshold:
            counted+=1;continue
        if x.get('private_to') not in (None,actor['id']):
            counted+=1;continue
        projection=project_recursive_actor_sign(world,actor,x,location)
        if projection is None:
            counted+=1;continue
        cues.append(projection);receipts.append(x['id'])
    # Co-presence is an objective present opportunity, not an assertion about
    # the other's intentions, consent, feelings, or accessible psychology.
    if actor['body']['sensor'] >= .05:
        for other,where in sorted(world['positions'].items()):
            if other!=actor['id'] and where==location:
                channels=recursive_encounter_channels(
                    world,actor['id'],other,location)
                # Shared coordinates are still an objective practical fact,
                # not automatic sensory recognition of the other person.
                if channels is not None and not channels['visible']:
                    continue
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
    # A visible/held source of food is a material possibility; the actor's
    # actual ability and willingness to feed someone else remain separate.
    held=_nonnegative_transfer_amount(
        world.get('holdings',{}).get(actor['id'],{}).get('food',0),
        'INVALID_ACTOR_ACCESS_HELD_FOOD')
    site=world['sites'].get(location,{})
    shared=(site.get('shared_household_food') is True and
            _nonnegative_transfer_amount(site.get('food',0),
              'INVALID_ACTOR_ACCESS_SHARED_FOOD')>=1)
    if any(c.get('kind')=='coactor_present' for c in cues) and (
            held>=1 or shared):
        env.append('FEED')
    if actor['body']['sensor'] >= .05:
        env += [x['operation'] for x in live_food_petition_opportunity(
            world,actor,location)]
    env+=food_power_opportunities(world,actor,location)
    env+=actor_work_opportunities(world,actor,location)
    if work_permission(world,actor['id'],location)==(
            'QUALIFIED_WORK_CONTRACT_ACTIVE'):
        env.append('WORK')
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
    forms=constitution.forms
    historical=pre_cue_pressures(constitution,access)
    cues=_tokens(access.cues)
    active={}; dormant=[]; inhibited=[]; currents=copy(historical['currents']); disagreements=[]
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
    # SOURCE-JOIN P012 (R15/R18 -> richer R3): an inhibitor that has
    # itself been defeated in an acyclic inhibition graph cannot veto the
    # third form. Conservatism is retained for cyclic and support-dependent
    # configurations, where no uniquely justified winner follows.
    #
    # Keep R3's historically admitted PRE-A0 relations and extra relation
    # kinds; do not overwrite them with the older R18 constitution module.
    seed=set(active)
    qualified={fid for fid,f in forms.items()
        if f.get('lifecycle') not in ('ENDED','DORMANT')
        and f.get('body_min',0)<=constitution.body['motor']
        and _form_in_scope(f,access)}
    valid_links=[link for link in constitution.links
        if link.get('source') in forms and link.get('target') in forms
        and (not link.get('contexts') or access.location in link['contexts'])]
    positive=[link for link in valid_links if link.get('relation') in
              ('RECRUITS','SUPPORTS','ACTIVATES','REINFORCES')]
    negative=[link for link in valid_links if link.get('relation') in
              ('INHIBITS','SUPPRESSES')]

    def closure(start,blocked=frozenset()):
        reached=(set(start)&qualified)-set(blocked)
        while True:
            added={link['target'] for link in positive
                   if link['source'] in reached
                   and link['target'] in qualified
                   and link['target'] not in blocked}
            newer=reached|added
            if newer==reached:return reached
            reached=newer

    def joint_recruitment(start,blocked=frozenset()):
        """Qualified link/motif closure, with no hidden mutable actor state."""
        reached=closure(start,blocked)
        routes={}
        # Every iteration strictly adds an existing qualified form or ends.
        for _ in range(len(qualified)+1):
            projected=derive_relational_metabolism(
                constitution,access,
                {fid:forms[fid] for fid in sorted(reached)},
                set(inhibited)|set(blocked))
            proposed=set()
            for route in projected['recruitment_candidates']:
                target=route['target_form']
                if (target in qualified and target not in blocked
                        and target not in reached):
                    proposed.add(target)
                    routes.setdefault(target,route)
            following=closure(reached|proposed,blocked)
            if following==reached:return reached,routes
            reached=following
        raise RuntimeError('RELATIONAL_RECRUITMENT_DID_NOT_CONVERGE')

    potentially_active,_=joint_recruitment(seed)
    conservative_veto={link['target'] for link in negative
                       if link['source'] in potentially_active}
    # Only the graph among genuinely reachable forms can discriminate the
    # acyclic A inhibits B inhibits C case. Absent/cyclic forms cannot be
    # self-authorized as a stable victor of psychic contradiction.
    edges={fid:set() for fid in potentially_active}
    incoming={fid:0 for fid in potentially_active}
    for link in negative:
        src=link['source']; dst=link['target']
        if src in edges and dst in edges and dst not in edges[src]:
            edges[src].add(dst)
            incoming[dst]+=1
    frontier=sorted(fid for fid in edges if incoming[fid]==0)
    order=[]
    while frontier:
        node=frontier.pop(0)
        order.append(node)
        for target in sorted(edges[node]):
            incoming[target]-=1
            if incoming[target]==0:frontier.append(target)
        frontier.sort()

    vetoed=conservative_veto
    if len(order)==len(edges):
        stratified=set()
        for source in order:
            if source not in stratified:
                stratified.update(edges[source])
        # A plausible acyclic topological suppression is *not* accepted
        # unless the survivor set itself yields precisely that veto set.
        # Support-dependent inhibitors therefore cannot manufacture actions.
        surviving,_=joint_recruitment(seed,stratified)
        surviving_veto={link['target'] for link in negative
                        if link['source'] in surviving}
        if surviving_veto==stratified:
            vetoed=stratified

    inhibited.extend(sorted(vetoed))
    actual,motif_routes=joint_recruitment(seed,vetoed)
    active={fid:copy(forms[fid]) for fid in sorted(actual)}
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
    # A stable person or object co-presence is not a reencounter with the
    # earlier *signal*.  Cues made by the read model from current spatial
    # adjacency, posted notice shells or objective object visibility must
    # not be mistaken for newly received event signs after an unobserved
    # interval.  The genuinely current sensory world cue has already passed
    # actor_access's clock, place, private-owner and bodily threshold checks.
    current_event_signs=_tokens([sign for sign in access.cues
        if sign.get('kind') not in (
            'coactor_present','material_object_present',
            'public_notice_visible')])
    for previous in constitution.evidence_paths[-64:]:
        prior_tags={str(x).lower()
                    for x in previous.get('received_cue_tags',[])}
        if prior_tags and prior_tags & current_event_signs:
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
    historical_care=recruit_co_regulation(constitution,access)
    for offered in historical_care['offered']:
        entry=actions.setdefault('SIGNAL',{
            'action':'SIGNAL','score':.06,'basis':[],
            'opportunity':'HISTORICALLY_ACQUIRED_RELATIONAL_SIGNAL'})
        entry['score']=max(entry['score'],offered['score'])
        entry['basis'].append('co_regulation:'+offered['orientation_ref'])
    currents.extend({
        'kind':'HISTORICAL_CO_REGULATION_EXPECTATION_CONTRADICTED',
        'orientation_ref':r['orientation_ref'],
        'caregiver_ref':r['previous_caregiver_ref'],
        'prior_care_history_retained':True,
        'caregiver_intention_not_proved':True,'grade':r['grade']}
        for r in historical_care.get('suspended_after_contradiction',[]))
    currents.extend({
        'kind':'ACQUIRED_CO_REGULATION_MAY_RECRUIT_SIGNAL',
        'orientation_ref':r['orientation_ref'],
        'counterpart_ref':r['caregiver_ref'],
        'other_response_remains_independent':True,
        'not_a_conscious_self_report':True,
        'grade':r['grade']} for r in historical_care['offered'])
    food_collective=offered_food_petition(constitution,access)
    if food_collective is not None:
        fop=food_collective['action']
        q=actions.setdefault(fop,{
            'action':fop,'score':food_collective['score'],
            'basis':[],'opportunity':'LIVED_MATERIAL_REPRODUCTION_PUBLIC_PROCEDURE'})
        q['score']=max(q['score'],food_collective['score'])
        q['basis']+=food_collective['basis']
        q['food_collective_ground']=copy(food_collective)
        currents.append({
            'kind':'MATERIAL_REPRODUCTION_MEETS_COLLECTIVE_PROCEDURE',
            'source_notice_ref':food_collective['source_notice_exposure_ref'],
            'lived_care_refs':food_collective['lived_care_refs'],
            'obstruction_refs':food_collective['attempted_obstruction_refs'],
            'not_automatic_ideological_identification':True,
            'grade':GRADE})
    # Controlling a store and building an alternative are real world
    # affordances, not preassigned personality motives. The counter-source
    # can be recruited only when this particular actor actually attempted
    # care and encountered a nonperformance at this site.
    for action in (INSTALL,MAINTAIN,SANCTION,COMMONS,OFFER,ACCEPT):
        if action not in access.affordances or not eligible(
                constitution.body,action)[0]:
            continue
        entry=actions.setdefault(action,{
            'action':action,'score':.12,'basis':[],
            'opportunity':'SITUATED_MATERIAL_FOOD_POWER'})
        entry['basis'].append('actual_material_ability:'+action)
        if action==COMMONS:
            denied=[x for x in constitution.material_dependency_encounters
                    if x.get('own_operation_attempted')=='FEED'
                    and x.get('location')==access.location
                    and type(x.get('clock')) is int
                    and x['clock']<=constitution.clock]
            if denied:
                entry['material_counterpower_ground']={
                    'personally_sensed_incomplete_feeding_ref':
                        denied[-1]['id'],
                    'alternative_requires_own_food_not_ideology':True}
                currents.append({
                    'kind':'BLOCKED_REPRODUCTION_MAY_RECRUIT_MATERIAL_ALTERNATIVE',
                    'historical_attempt_ref':denied[-1]['id'],
                    'not_a_conscious_class_analysis':True,'grade':GRADE})
    # Accepted employment can make paid production practical. A separate
    # actually experienced failed work attempt may recruit available real
    # worker relief, without granting causal knowledge of employer intent.
    for action in ('WORK',LABOR_ACCEPT,LABOR_SUSPEND,
                   LABOR_RESIGN,LABOR_FUND,LABOR_DRAW):
        if action not in access.affordances or not eligible(
                constitution.body,action)[0]:
            continue
        entry=actions.setdefault(action,{
            'action':action,'score':.14,'basis':[],
            'opportunity':'SOURCEFREE_SITUATED_WAGE_RELATION'})
        entry['basis'].append('wage_world_opportunity:'+action)
        if action==LABOR_DRAW:
            interrupted=[x for x in constitution.labor_dependency_encounters
                if x.get('own_attempted_work')=='WORK'
                and x.get('location')==access.location
                and type(x.get('clock')) is int
                and x['clock']<=constitution.clock]
            if interrupted:
                entry['labor_relief_ground']={
                    'personal_failed_work_ref':interrupted[-1]['id'],
                    'sourcefree_fund_not_actor_ideology':True}
                currents.append({
                    'kind':'HISTORICAL_WAGE_OBSTRUCTION_AND_FUNDED_RELIEF',
                    'experienced_work_ref':interrupted[-1]['id'],
                    'employer_motive_unknown':True,'grade':GRADE})
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
        entry.setdefault('candidate_notice_grounds',{}).update({
            ref:candidate.get('source_grounds_status',
                'HISTORICALLY_FRUSTRATED_EVIDENCE_SEEKING')
            for ref in candidate['candidate_notice_refs']})
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
    invested=invested_material_action_options(constitution,access)
    currents+=invested['recruitment']['currents']
    for candidate in invested['proposals']:
        op=candidate['action']
        entry=actions.setdefault(op,{
            'action':op,'score':candidate['score'],'basis':[],
            'opportunity':'HISTORICALLY_INVESTED_VISIBLE_OBJECT'})
        entry['basis']+=candidate['basis']
        entry['score']=max(entry['score'],candidate['score'])
        entry.setdefault('object_specific_pressures',[]).append({
            'material_object_ref':candidate['object_ref'],
            'unresolved_conflict':candidate['unresolved_conflict'],
            'actor_meaning_not_world_ownership':True})
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
                             relational=relational,historical=historical)
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
    attention=situate_attention(constitution,access,historical=historical)
    # Attach actor/clock/project-specific practical ALTERNATIVES beneath the
    # existing physical action grammar. Psychodynamic inhibition still acts
    # first; an inhibited operation cannot be revived by an option ID.
    for option in dynamics['candidate_actions']:
        # A graded *component* projection can inform future practical
        # construction, without granting material permission or pretending
        # the simulated actor has a Foucauldian theory of its own powers.
        option['situated_component_facility']=situated_component_efficacy(
            {'power_exercises':constitution.power_exercises,
             'practice_exposures':constitution.practice_exposures},
             option['action'],access.location)
        option['practical_alternatives']=practical_alternatives(
            constitution,attention['focus_access'],option)
        # A learned relation of distributed practical power can add a real
        # future *invitation* alternative. The Other's policy remains their own.
        option['practical_alternatives']+=conditional_assistance_options(
            constitution,attention['focus_access'],option)
        option['practical_alternatives']+=object_bound_alternatives(
            constitution,attention['focus_access'],option['action'])
        option['practical_alternatives']+=cultural_object_alternatives(
            constitution,attention['focus_access'],option)
        option['practical_alternatives']+=addressed_signal_alternatives(
            constitution,attention['focus_access'],option)
        option['practical_alternatives']+=project_repeat_feeding(
            constitution,attention['focus_access'],option)
        option['practical_alternatives']+=practiced_care_alternatives(
            constitution,attention['focus_access'],option)
        option['practical_alternatives']+=situated_suspension_targets(
            constitution,attention['focus_access'],option)
        annotate_material_alternatives(option,invested)
        if option['action']=='INSPECT' and option.get('candidate_notice_refs'):
            option['practical_alternatives'] += [
                {'option_id':'inquiry:'+constitution.actor+':'+
                  str(constitution.clock)+':'+str(ref),
                 'actor':constitution.actor,'as_of_clock':constitution.clock,
                 'operation':'INSPECT','project_id':None,
                 'grounds_status':option.get(
                     'candidate_notice_grounds',{}).get(
                         ref,'HISTORICALLY_FRUSTRATED_EVIDENCE_SEEKING'),
                 'world_request':{'operation':'INSPECT',
                     'addressed_party_ref':None,'material_object_ref':ref},
                 'anticipated_difference':None,
                 'binding_status':'PUBLIC_POSTED_NOTICE_ACTOR_SITUATED',
                 'not_secret_world_explanation':True,
                 'grade':'SOURCEFREE_RESEARCH_PROVISIONAL'}
                for ref in option['candidate_notice_refs']]
    expectation_afterlife=annotate_practical_expectations(
        constitution,dynamics['candidate_actions'])
    affective_afterlife=annotate_activity_affects(
        constitution,attention['focus_access'],dynamics['candidate_actions'])
    currents+=affective_afterlife['currents']
    notice_afterlife=annotate_notice_expectations(constitution,access,dynamics['candidate_actions'])
    currents+=notice_afterlife['currents']
    interactivity=annotate_interactivity_relations(constitution,access,dynamics['candidate_actions'])
    currents+=interactivity['currents']
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
                           historical['readset']+preproject['readset']+exercised['readset']+
                           invested['recruitment']['readset']+
                           material['readset']+
                           historical_care['readset']+
                           ([
                             food_collective['source_notice_exposure_ref']]
                            +food_collective['lived_care_refs']
                            +food_collective['attempted_obstruction_refs']
                            if food_collective else [])+
                           inquiry['readset']+
                           functional['readset']+
                           expectation_afterlife['readset']+affective_afterlife['readset']+
                           prospective['readset']+notice_afterlife['readset']+interactivity['readset']+
                           list(candidate_history_refs)+
                           [t['id'] for t in traces]+access.access_receipts)),
       unknowns=list(constitution.unknowns),antagonisms=dynamics['antagonisms'],
       suspended_actions=dynamics['suspended'],learned_compositions=learned,
       attention_frame=attention['frame'])
