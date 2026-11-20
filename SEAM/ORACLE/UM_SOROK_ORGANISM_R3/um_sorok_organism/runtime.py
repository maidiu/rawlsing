"""UM-SOROK integrated provisional living computational organism R2.

One continuing world, distinct actors and bodies, acquired variable functional
psychology, contextual recruitment, independent coactivity, objective outcomes,
actor-specific experience, fictional psychological afterlife, compressed time,
and bounded public expression. NOT the protected SOROK owner implementation.
"""
from dataclasses import asdict
from pathlib import Path
from .types import newborn, blank_world, Attempt, copy, GRADE, digest, stable_id
from .storage import ResearchLedger
from .constitution import materialize, actor_access, compose
from .organism import eligible, apply_body
from .development import admit, recurring_provisional_growth
from .ordinary_life import passage
from .activity import record_activity_afterlife, register_lived_activity_attempt
from .practical_difference import start_expectation
from .lived_genesis import proposals_from_bodily_history
from .distributed_power import record_actor_participation
from .practical_powers import retain_exercised_power
from .practical_inquiry import retain_personal_notice_exposure
from .material_investments import (
    retain_personal_object_encounter, possible_object_investments)
from .unintended_goods import possible_unintended_goods
from .expectation_afterlife import source_qualified_appraisal_candidates
from .routine_sources import register_sourcefree_period_envelope
from .caregiving_practice import retain_performed_material_feeding
from .food_access_struggle import configure_food_power
from .food_power_reproduction import register_concession
from .institutional_procedure_learning import possible_institutional_learning
from .material_dependency_history import conserve_sensed_material_nonperformance
from .livelihood_history import conserve_incomplete_work
from .labor_dependency import register_work_regime
from .co_regulation_history import (
    possible_acquired_regulation, record_lived_co_regulation_response,
    possible_revision_after_nonresponse)
from .plural_care_paths import (
    conserve_lived_high_resolution_care, plural_acquisition_candidate,
    sourcequalified_reopening)
from .functional_correspondence import propose_actor_lived_correspondences
from .initiative import continue_life
from .continuity_clock import continue_to_discontinuity
from .historical_parent_bridge import render_blind_interview
from .operative_witness import freeze_operative_witness
from .parents import construct_parent, interview_readout
from .semantics import ValidatingSemanticService
from .world import IndependentWorldAuthority, COOPERATIVE, add_cue

class ConstitutiveRuntime:
    def __init__(self,db,semantic=None,world_id='w1'):
        self.ledger=ResearchLedger(db)
        self.semantic=semantic or ValidatingSemanticService()
        self.world_id=world_id
        self.authority=IndependentWorldAuthority(self._independent_coactor_plan)

    def initialize(self,parent_packets=None,child_id='nadia',child_name='Nadia'):
        world=blank_world(self.world_id)
        parents=[]
        for actor_id,name,packet in (parent_packets or []):
            person=construct_parent(actor_id,name,packet,self.semantic)
            parents.append(person)
        child=newborn(child_id,child_name)
        world['institutions']['hall_board']['members']=[parents[0]['id']] if parents else []
        # Source conditioning and fictional initialization share one transaction
        # and one immutable event-chain envelope. There must never be a committed
        # person with missing or unanchored source qualification.
        source_seals=[('fictional_source:'+a,'CONDITIONING_NOT_REAL_PERSON',packet)
                      for a,_,packet in (parent_packets or [])]
        self.ledger.initialize(world,parents+[child],source_seals=source_seals)
        return {'world':self.world_id,'actors':[a['id'] for a in parents+[child]],'grade':GRADE}

    def snapshot(self,actor_id):
        _,world=self.ledger.world(self.world_id)
        _,person=self.ledger.actor(actor_id)
        return asdict(materialize(person,world))

    def see(self,actor_id):
        _,world=self.ledger.world(self.world_id)
        _,person=self.ledger.actor(actor_id)
        return asdict(actor_access(person,world))

    def situated(self,actor_id):
        _,world=self.ledger.world(self.world_id)
        _,person=self.ledger.actor(actor_id)
        const=materialize(person,world)
        access=actor_access(person,world)
        return asdict(compose(const,access))

    def cue(self,actor_id=None,kind='ordinary_contact',tags=None,location='home',
            description='',modality='visual',private_to=None):
        """External world fixture change, not an actor psychological event."""
        wv,world=self.ledger.world(self.world_id)
        if actor_id is not None:self.ledger.actor(actor_id)
        cue=add_cue(world,kind,tags or [kind],location=location,description=description,
                    modality=modality,private_to=private_to,source_actor=actor_id,clock_offset=1)
        world['clock']+=1
        receipt=self.ledger.commit(self.world_id,wv,world,{}, {},'OBJECTIVE_CUE',actor_id,
            {'cue_ref':cue['id'],'issuer':'EXTERNAL_RESEARCH_FIXTURE','not_actor_memory':True})
        return {'receipt':receipt['id'],'cue':cue,'grade':GRADE}

    def _actor_plan(self,actor_id,world,actors,requested_action=None,requesting_actor=None,requesting_action=None):
        actor=actors[actor_id]
        c=materialize(actor,world);e=actor_access(actor,world);situated=asdict(compose(c,e))
        options=copy(situated['candidate_actions'])
        if requesting_actor is not None:
            valid=COOPERATIVE.get(requesting_action,set())
            opts=[o for o in options if o['action'] in valid]
            allowed,_=eligible(actor['body'],'REFUSE')
            if allowed:opts.append({'action':'REFUSE','score':.07,'basis':['independent_actor_refusal'],
                                    'opportunity':'ACTOR_RIGHT'})
            options=sorted(opts,key=lambda x:(-x['score'],x['action']))
        if requested_action is not None:
            # Injected actor conduct is disclosed, never called self-generated.
            ok,why=eligible(actor['body'],requested_action)
            if not ok: raise ValueError('ACTOR_ACTION_BODILY_INELIGIBLE:'+why)
            action=requested_action
            basis=['EXTERNAL_RESEARCH_ACTION_INJECTION']
            purpose={'status':'EXTERNALLY_INJECTED_NO_ATTESTED_ACTOR_PURPOSE',
                     'project_id':None,'selection_grade':'EXTERNAL_INJECTION',
                     'other_available_projects_not_claimed':True}
            authority='INJECTED_NOT_NATIVE_ACTOR_CHOICE'
            practical={'status':'EXTERNAL_RESEARCH_OPERATION',
                       'option_id':None,'project_id':None,
                       'anticipated_difference':None,
                       'actor_has_explicit_reason':'NOT_ESTABLISHED',
                       'conscious_availability':'NOT_INFERRED',
                       'operative_selection_witness':{
                           'policy_path':'EXTERNAL_INJECTION_NOT_ACTOR_INITIATIVE',
                           'source_grade':GRADE,
                           'historical_motive':'NOT_INFERRED'}}
            bound_target=None
        else:
            # The new selection interface offers actor-scoped *practical*
            # alternatives, not merely operation names. It also accepts the
            # older action-only policy with explicitly unresolved purposes.
            # A model policy is NOT a conscious iceberg manager.
            flat_alternatives=[copy(alt) for o in options
                               for alt in o.get('practical_alternatives',[])]
            flat_trials=[copy(t) for o in options for t in o.get('possible_end_trials',[])]
            proposed=self.semantic.proposal('actor_attempt',{'actor':{'id':actor_id,'role':actor['role'],
                'body':copy(actor['body'])},
                'accessible':{k:v for k,v in asdict(e).items() if k!='inaccessible_count'},
                'situated':situated,'options':options,
                'practical_options':flat_alternatives,
                'possible_end_trials':flat_trials,
                'possible_end_trial_does_not_establish_motive':True,
                'selected_option_is_not_conscious_intent':True,
                'requesting_actor':requesting_actor,'requesting_action':requesting_action})
            requested_option=proposed.get('practical_option_id')
            requested_trial=proposed.get('possible_end_trial_id')
            trial_choice=None
            if requested_trial is not None:
                if type(requested_trial) is not str or requested_option is not None:
                    raise ValueError('POSSIBLE_END_TRIAL_SELECTION_CONFLICT')
                matches=[t for t in flat_trials if t.get('trial_id')==requested_trial]
                if len(matches)!=1:
                    raise ValueError('UNISSUED_OR_AMBIGUOUS_POSSIBLE_END_TRIAL')
                trial_choice=matches[0]
            if requested_option is not None:
                if type(requested_option) is not str:
                    raise ValueError('INVALID_PRACTICAL_OPTION_ID')
                matches=[a for a in flat_alternatives
                         if a['option_id']==requested_option]
                if len(matches)!=1:
                    raise ValueError('UNKNOWN_OR_AMBIGUOUS_PRACTICAL_OPTION_ID')
                action=matches[0]['operation']
                if 'action' in proposed and proposed['action']!=action:
                    raise ValueError('PRACTICAL_OPTION_OPERATION_CONFLICT')
            elif trial_choice is not None:
                action=trial_choice['operation']
                if 'action' in proposed and proposed['action']!=action:
                    raise ValueError('POSSIBLE_END_TRIAL_OPERATION_CONFLICT')
            else:
                action=proposed['action']
            opt=next((o for o in options if o['action']==action),None)
            if opt is None:raise ValueError('MODEL_ATTEMPT_NOT_ACTOR_ELIGIBLE')
            ok,why=eligible(actor['body'],action)
            if not ok:raise ValueError('MODEL_ACTION_BODILY_INELIGIBLE:'+why)
            # A single operation may genuinely serve SEVERAL projects, but
            # only when the actor policy explicitly selects the particular
            # subset. Never infer multi-intent from the pooled opportunity.
            # Omission is meaningful: an exploratory act with no known end.
            raw=proposed.get('project_ids')
            if raw is not None and proposed.get('project_id') is not None:
                raise ValueError('AMBIGUOUS_SINGLE_AND_MULTI_PURPOSE_SELECTION')
            if raw is None:
                one=proposed.get('project_id')
                selected_refs=[] if one is None else [one]
            else:
                if (type(raw) is not list or not raw
                        or len(raw)>8 or len(set(map(str,raw)))!=len(raw)):
                    raise ValueError('INVALID_MULTIPLE_PROJECT_SELECTION')
                selected_refs=raw
            if any(type(ref) is not str or not ref for ref in selected_refs):
                raise ValueError('MODEL_SELECTED_PURPOSE_NOT_TEXT')
            available={p['project_id']:p for p in opt.get('project_courses',[])}
            if any(ref not in available for ref in selected_refs):
                raise ValueError('MODEL_SELECTED_PURPOSE_NOT_SITUATED_ELIGIBLE')
            if trial_choice is not None:
                if selected_refs:
                    raise ValueError('PROVISIONAL_TRIAL_CANNOT_ASSERT_ESTABLISHED_PROJECT')
                if not any(t.get('trial_id')==trial_choice['trial_id']
                           for t in opt.get('possible_end_trials',[])):
                    raise ValueError('PROVISIONAL_TRIAL_NOT_IN_SELECTED_OPERATION')
            alternatives=opt.get('practical_alternatives',[])
            option_id=proposed.get('practical_option_id')
            if option_id is not None:
                if type(option_id) is not str:
                    raise ValueError('INVALID_PRACTICAL_OPTION_ID')
                match=[a for a in alternatives if a['option_id']==option_id]
                if len(match)!=1:
                    raise ValueError('UNKNOWN_OR_AMBIGUOUS_PRACTICAL_OPTION_ID')
                selected_alternative=match[0]
                alternate_project=selected_alternative['project_id']
                if not selected_refs and alternate_project is not None:
                    selected_refs=[alternate_project]
                elif selected_refs != ([alternate_project] if alternate_project else []):
                    raise ValueError('PRACTICAL_OPTION_PURPOSE_CONFLICT')
            else:
                if len(selected_refs)==1:
                    selected_alternative=next((a for a in alternatives
                        if a['project_id']==selected_refs[0]),None)
                elif not selected_refs:
                    selected_alternative=next((a for a in alternatives
                        if a['project_id'] is None),None)
                else:
                    selected_alternative=None
            # An unintended material consequence can become a later trial
            # concerning that *particular continuing object*. Never let an
            # action-only fallback silently substitute a site-wide generic
            # repair for the actor's historically identified practical thing.
            if trial_choice is not None and trial_choice.get(
                    'source_material_object_ref') is not None:
                source_object=trial_choice['source_material_object_ref']
                material_matches=[
                    a for a in alternatives if
                    a.get('world_request',{}).get('material_object_ref')
                    ==source_object]
                if len(material_matches)!=1:
                    raise ValueError('TRIAL_MATERIAL_OBJECT_NOT_UNIQUELY_BINDABLE')
                selected_alternative=material_matches[0]
            if selected_alternative and selected_alternative.get('binding_status')=='UNBOUND_PARTY_NOT_PRESENT':
                raise ValueError('ACTOR_SELECTED_UNAVAILABLE_ADDRESSED_PARTY')
            selected=[available[ref] for ref in selected_refs]
            selection_grade=proposed.get(
                'purpose_selection_grade',
                'MODEL_CHOSEN_COURSE_FICTIONAL_NOT_OBSERVED_CONSCIOUS_MOTIVE')
            if selected:
                purpose={
                    'status':('ACTOR_POLICY_SELECTED_PROJECT_COURSE'
                              if len(selected)==1
                              else 'ACTOR_POLICY_SELECTED_MULTIPLE_PROJECT_COURSES'),
                    'project_id':selected[0]['project_id'] if len(selected)==1 else None,
                    'project_ids':copy(selected_refs),
                    'practical_objects':[p['object'] for p in selected],
                    'motive_hypotheses':[p['motive_hypothesis'] for p in selected],
                    'selection_grade':selection_grade,
                    'not_claimed_fulfillment':True,
                    'other_available_projects_not_claimed':True}
                if len(selected)==1:
                    purpose['practical_object']=selected[0]['object']
                    purpose['motive_hypothesis']=selected[0]['motive_hypothesis']
            else:
                purpose={'status':'ACTOR_POLICY_NO_ATTESTED_PROJECT_PURPOSE',
                         'project_id':None,'project_ids':[],
                         'selection_grade':'EXPLORATORY_OR_UNRESOLVED_END_NOT_INFERRED',
                         'other_available_projects_not_claimed':True}
            if trial_choice is not None:
                purpose={
                    'status':'ACTOR_POLICY_PROVISIONAL_END_TRIAL_NOT_DURABLE_MOTIVE',
                    'possible_end_ref':trial_choice['possible_end_ref'],
                    'original_event':trial_choice['origin_event'],
                    'project_id':None,'project_ids':[],
                    'selection_grade':
                        'HISTORICALLY_GROUNDED_POSSIBILITY_NOT_CONSCIOUS_REASON',
                    'object_fulfillment':'NOT_INFERRED',
                    'other_available_projects_not_claimed':True,
                }
            # Preserve only explicitly selected projects on Attempt; all
            # unselected courses remain in the situation, not the act's past.
            basis=[ref for ref in opt.get('basis',[])
                   if not (isinstance(ref,str) and ref.startswith('project:'))]
            basis+=['project:'+ref for ref in selected_refs]
            bound_target=(selected_alternative['world_request']['addressed_party_ref']
                          if selected_alternative else None)
            bound_object=(selected_alternative['world_request'].get('material_object_ref')
                          if selected_alternative else None)
            practical={'status':'ACTOR_POLICY_PRACTICAL_ATTEMPT',
                       'option_id':(selected_alternative['option_id']
                           if selected_alternative else stable_id(
                               'joint_practical_option',{'actor':actor_id,
                                'clock':world['clock'],'action':action,
                                'projects':sorted(selected_refs)})),
                       'as_of_clock':world['clock'],'actor':actor_id,
                       'selected_project_refs':copy(selected_refs),
                       'project_id':(selected_refs[0] if len(selected_refs)==1 else None),
                       'anticipated_difference':(
                           copy(selected_alternative.get('anticipated_difference'))
                           if selected_alternative else None),
                       'anticipated_differences':([
                           copy(a.get('anticipated_difference')) for a in alternatives
                           if a['project_id'] in selected_refs]
                           if len(selected_refs)>1 else []),
                       'actor_has_explicit_reason':'NOT_ESTABLISHED',
                       'conscious_availability':'NOT_INFERRED',
                       'not_premature_fulfillment':True,
                       'world_request':{
                           'operation':action,
                           'addressed_party_ref':bound_target,
                           'material_object_ref':bound_object},
                       'selected_material_object_ref':bound_object,
                       'source_co_regulation_orientation_ref':(
                           selected_alternative.get('origin_orientation_ref')
                           if selected_alternative else None),
                       'material_object_not_automatically_owned_by_actor':True}
            if trial_choice is not None:
                # Freeze actor's already issued option before the world settles.
                practical['possible_end_trial']=copy(trial_choice)
                practical['selected_trial_is_not_conscious_intention']=True
            # Freeze the exact historically acquired grounds a SOURCEFREE
            # action policy actually used, or explicitly leave it unknown.
            # The old machinery retained currents but could not say which
            # affected this occasion once the world had already settled.
            practical['operative_selection_witness']=freeze_operative_witness(
                actor_id,world['clock'],options,action,proposed,
                getattr(self.semantic.provider,'grade','INJECTED_EXTERNAL_PROVIDER'),
                selected_refs)
            authority='ACTOR_SITUATED_CANDIDATE_SELECTED_SOURCEFREE'
        return Attempt(actor_id,action,target=bound_target,
                       object_ref=(bound_object if requested_action is None else None),
                       means=[],basis=basis,
                       intention=authority,purpose_selection=purpose,
                       practical_selection=practical,
                       scene_hash=digest({'world':world,'actor':actor_id})),

    def plan(self,actor_id,requested_action=None,target=None,object_ref=None):
        _,world=self.ledger.world(self.world_id)
        actors=self.ledger.actors()
        if actor_id not in actors:raise ValueError('UNREGISTERED_ACTOR')
        attempt=self._actor_plan(actor_id,world,actors,requested_action)[0]
        if target is not None and attempt.target not in (None,target):
            raise ValueError('CALLER_TARGET_CONFLICTS_WITH_ACTOR_PRACTICAL_ALTERNATIVE')
        if target is not None:attempt.target=target
        if object_ref is not None and attempt.object_ref not in (None,object_ref):
            raise ValueError('CALLER_OBJECT_CONFLICTS_WITH_ACTOR_SELECTION')
        if object_ref is not None:attempt.object_ref=object_ref
        return attempt

    def _independent_coactor_plan(self,principal,world,actors):
        """The other actor reads their OWN acquired organization and policy.
        A requested joint activity supplies a possible invitation, not consent.
        """
        other=self._actor_plan(principal.target,world,actors,None,
                      principal.actor,principal.action)[0]
        other.target=principal.actor
        return other

    def step(self,actor_id,requested_action=None,target=None,object_ref=None,
             coactor_override=None,research_plan_context=None):
        """One atomic joined life transition. Coactor always uses own plan.

        coactor_override is deliberately prohibited; original R0 consent bug
        is repaired in this research implementation at the public transaction.
        """
        if coactor_override is not None:raise ValueError('FORGED_COACTOR_OVERRIDE_REFUSED')
        if research_plan_context is not None:
            if (requested_action is None
                    or not isinstance(research_plan_context,dict)
                    or type(research_plan_context.get('plan_id')) is not str
                    or type(research_plan_context.get('hypothesized_object')) is not str
                    or research_plan_context.get('authority')!='EXTERNAL_RESEARCH_PLAN'):
                raise ValueError('UNQUALIFIED_EXTERNAL_PLAN_CONTEXT')
        wv,world=self.ledger.world(self.world_id)
        actor_versions={aid:self.ledger.actor(aid)[0] for aid in self.ledger.actors()}
        actors=self.ledger.actors()
        # Preserve a private read of the operative psychological organization
        # BEFORE the independent world result. Even an externally injected
        # action cannot retroactively manufacture the actor's motives.
        pre_event_psychodynamics={}
        for aid,person in actors.items():
            prior=asdict(compose(materialize(person,world),actor_access(person,world)))
            pre_event_psychodynamics[aid]={
                'readset':copy(prior['readset']),
                'recruited_form_refs':[x['id'] for x in prior['recruited']],
                'inhibited_refs':copy(prior['inhibited']),
                'currents':copy(prior['currents']),
                'antagonisms':copy(prior['antagonisms']),
                'sourcefree_grade':GRADE,
                'not_an_actor_self_account':True,
            }
        # Snapshot physical state before independently authorized world settlement;
        # later psychic inference cannot retcon what this body had undergone.
        bodily_before={aid:copy(person['body']) for aid,person in actors.items()}
        principal=self._actor_plan(actor_id,world,actors,requested_action)[0]
        if target is not None and principal.target not in (None,target):
            raise ValueError('CALLER_TARGET_CONFLICTS_WITH_ACTOR_PRACTICAL_ALTERNATIVE')
        if target is not None:principal.target=target
        if object_ref is not None and principal.object_ref not in (None,object_ref):
            raise ValueError('CALLER_OBJECT_CONFLICTS_WITH_ACTOR_SELECTION')
        if object_ref is not None:principal.object_ref=object_ref
        # A caller never supplies another actor's response. The world owner
        # obtains it from the installed independently constituted actor policy.
        actual,partner,coactor_policy_receipt=self.authority.resolve(world,actors,principal)
        resolved=asdict(actual)
        summary=resolved['world_delta']['event']
        objective_ref=stable_id('objective',{'world':self.world_id,'summary':summary})
        affected=set(a['actor'] for a in resolved['performed'])
        for aid,effect in resolved['personal_effects'].items():
            affected.add(aid)
        for row in resolved['performed']:
            apply_body(actors[row['actor']],row['action'],row['status'])
        # Target of care or coercion does not become a voluntary co-performer.
        for aid in affected:
            if aid not in {r['actor'] for r in resolved['performed']}:
                apply_body(actors[aid],'WAIT','IMPOSED' if summary['action']=='IMPOSE' else 'PARTIAL')
        activity_effects={}
        for row in resolved['performed']:
            chosen=principal if row['actor']==actor_id else partner
            if chosen is None:continue
            activity_effects[row['actor']]=record_activity_afterlife(actors[row['actor']],
                row['action'],row['status'],summary['outcome'],chosen.basis,objective_ref,
                {'material_claim_ref':summary.get('material_claim_ref')},
                purpose_selection=chosen.purpose_selection)
        developmental={};subjective={};post_event_psychodynamics={}
        for aid in actors:
            # Separate actor-specific view, no analyst world description in LLM input.
            access=actor_access(actors[aid],world)
            personally_done=next((r for r in resolved['performed'] if r['actor']==aid),None)
            participated=aid in affected
            if not participated and not access.cues:continue
            personal_cues=[x for x in access.cues
                           if x['id']==world['cues'][-1]['id']]
            if participated:
                # The presently co-situated other can be sensed without
                # revealing their motives or private biography. The earlier
                # projection omitted this mundane evidence even from actors
                # whose living encounter just occurred in the same room.
                # Retain no cue whose sensory eligibility actor_access denied.
                personal_cues += [x for x in access.cues
                    if x.get('kind')=='coactor_present'
                    and x.get('source_actor')!=aid]
            if not participated and not personal_cues:continue
            own=(personally_done['action'] if personally_done else
                 ('RECEIVED_FEEDING' if aid in affected and
                  summary['action']=='FEED' else
                  'RECEIVED_CARE' if aid in affected and
                  summary['action']=='CARE' else None))
            # Only this actor's actual selection—not the pooled action
            # opportunity—may qualify an undertaken project. For a target
            # who merely suffers the act, there is no actor-authored project.
            actor_attempt=(principal if aid==actor_id else partner)
            own_selection=(copy(actor_attempt.purpose_selection)
                 if personally_done and actor_attempt is not None
                 else {'status':'NO_ACTOR_AUTHORED_ATTEMPT','project_id':None})
            reciprocal=None
            if partner and resolved['objective_description']=='JOINT_ACTIVITY_PERFORMED' and personally_done and personal_cues:
                reciprocal=partner.actor if aid==actor_id else actor_id
            # Performed action may be proprioceptively available even where its
            # outward cue occurred at the origin of a successful MOVE and the
            # actor is now elsewhere. This is *not* objective outcome knowledge.
            felt_enactment=({'attempted_operation':personally_done['action'],
                             'body_access':'SOMATIC_ATTEMPT_ONLY',
                             'objective_result_not_inferred':True}
                            if personally_done else None)
            felt_effect=(('SOMATIC_CARE_CANDIDATE' if summary['action'] in ('CARE','FEED')
                         else 'IMPOSED_EFFECT_UNINTERPRETED')
                         if aid in resolved['personal_effects'] and not personally_done
                         else None)
            experience={'actor':aid,'clock':world['clock'],
                        'location':access.location,
                        'reciprocated_partner':reciprocal,
                        'ref':stable_id('experience',{'actor':aid,'event':objective_ref,
                                         'cues':personal_cues,'participated':participated,
                                         'felt_enactment':felt_enactment}),
                        'own_action':own,'status':personally_done['status'] if personally_done else 'OBSERVED',
                        'perceived_cues':personal_cues,'participated':participated,
                        'felt_enactment':felt_enactment,'felt_effect':felt_effect,
                        'actor_access_grade':GRADE}
            subjective[aid]=copy(experience)
            if personally_done and actor_attempt is not None:
                # Anticipation is formed at the time of this actor's attempt,
                # distinct from how the world actually settled it. It can
                # remain pending after the objective event has committed.
                start_expectation(actors[aid],actor_attempt.practical_selection,
                                  experience,objective_ref)
            # An action changes the opportunities and signals subsequently
            # accessible to its author. We retain the actually received path,
            # without inventing the counterfactual evidence they did not meet.
            actors[aid].setdefault('evidence_paths',[]).append({
                'event':objective_ref,'experience_ref':experience['ref'],
                'own_action':own,'purpose_status':own_selection['status'],
                'selected_project_ref':own_selection.get('project_id'),
                'practical_option_ref':(
                    actor_attempt.practical_selection.get('option_id')
                    if personally_done and actor_attempt is not None else None),
                'pre_world_operative_policy_witness_analytic_only':(
                    copy(actor_attempt.practical_selection.get('operative_selection_witness'))
                    if personally_done and actor_attempt is not None else None),
                'provisional_end_trial_ref_analytic_only':(
                    actor_attempt.practical_selection.get('possible_end_trial',{}).get('trial_id')
                    if personally_done and actor_attempt is not None else None),
                'anticipated_difference_analytic_only':(
                    copy(actor_attempt.practical_selection.get('anticipated_difference'))
                    if personally_done and actor_attempt is not None else None),
                'selected_project_refs':copy(own_selection.get(
                    'project_ids',([own_selection['project_id']]
                        if own_selection.get('project_id') else []))),
                'received_cue_refs':[c['id'] for c in personal_cues],
                'received_cue_tags':sorted({str(tag).lower()
                    for cue in personal_cues for tag in cue.get('tags',[])}),
                'not_a_counterfactual_comparison':True,
                'unencountered_alternatives':'UNKNOWN_NOT_OBSERVED',
                'grade':GRADE})
            # Actor-owned practical afterlife is separate from world objective
            # outcome. It can later be recruited, but is not motive fulfillment.
            register_lived_activity_attempt(actors[aid],experience,activity_effects.get(aid,[]))
            retain_performed_material_feeding(
                actors[aid],experience,objective_ref,world)
            conserve_sensed_material_nonperformance(
                actors[aid],experience,objective_ref)
            conserve_incomplete_work(actors[aid],experience,objective_ref)
            # A failed, actually attempted addressed call may revise the
            # historically learned expectation of this particular source.
            # It never proves why that Other did not respond, or retroactively
            # changes the care the child previously underwent.
            if personally_done and actor_attempt is not None:
                record_lived_co_regulation_response(
                    actors[aid],experience,
                    actor_attempt.practical_selection,objective_ref,
                    bodily_before=bodily_before[aid],
                    bodily_after=actors[aid]['body'])
            # A materially real CARE occurrence can enter the recipient's
            # own high-resolution history, but only when personally received
            # and accompanied by a real bodily difference. A normal day or
            # externally explained world archive cannot invent that history.
            actual_lived_care=conserve_lived_high_resolution_care(
                actors[aid],experience,objective_ref,
                bodily_before[aid],actors[aid]['body'])
            # Objective coactor contribution remains with the world, while
            # each person's actually accessible experience can establish a
            # contingent later *possibility of seeking assistance*.
            record_actor_participation(
                actors[aid],experience,resolved,objective_ref,
                body_before=bodily_before[aid],body_after=actors[aid]['body'])
            # A person can later seek to repeat an actually exercised
            # operation or attempt to practice a formerly joint activity.
            # The source-free rule does NOT confer independent technical
            # mastery or external access rights.
            retain_exercised_power(
                actors[aid],experience,objective_ref,
                world['positions'].get(aid,actors[aid]['location']))
            retain_personal_notice_exposure(actors[aid],experience,objective_ref)
            retain_personal_object_encounter(actors[aid],experience,objective_ref)
            # A model must not invent the child's remembered language or a
            # bodily benefit. Use actual material before/after body plus a
            # sign personally received to propose—not yet admit—one modest
            # nondeclarative orientation. This is not proof of why relief arose.
            history_genesis=proposals_from_bodily_history(
                actors[aid],experience,bodily_before[aid],actors[aid]['body'])
            functional_genesis=propose_actor_lived_correspondences(
                actors[aid],experience,objective_ref)
            material_meaning_proposals=possible_object_investments(
                actors[aid],experience)
            possible_incidental_goods=possible_unintended_goods(
                actors[aid],experience,
                (actor_attempt.practical_selection
                 if personally_done and actor_attempt is not None
                 else None),objective_ref)
            delayed_expectation_appraisals=source_qualified_appraisal_candidates(
                actors[aid],experience,objective_ref)
            care_genesis=possible_acquired_regulation(
                actors[aid],experience,objective_ref)
            plural_care_genesis=plural_acquisition_candidate(
                actors[aid],experience,objective_ref)
            renewed_relational_possibility=sourcequalified_reopening(
                actors[aid],experience,objective_ref)
            care_revision=possible_revision_after_nonresponse(
                actors[aid],experience,objective_ref)
            institutional_learning=possible_institutional_learning(
                actors[aid],experience,objective_ref)
            # Disabled LLM proposals may truthfully produce no change.
            selected=asdict(compose(materialize(actors[aid],world),access))
            post_event_psychodynamics[aid]={
                'readset':copy(selected['readset']),
                'currents':copy(selected['currents']),
                'inhibited_refs':copy(selected['inhibited']),
                'antagonisms':copy(selected['antagonisms']),
                'grade':GRADE,'not_a_public_tip':True,
            }
            proposal=self.semantic.proposal('development',{'actor':{'id':aid,'role':actors[aid]['role'],
                'body':copy(actors[aid]['body']),'location':actors[aid]['location']},
                'clock':world['clock'],'experience':experience,
                'selected_constitution':selected,
                'actor_forms':copy(actors[aid]['forms']),
                # Untried possible ends are actor-history hypotheses, not
                # automatically functioning motives or public self-knowledge.
                'actor_possible_ends':copy(actors[aid].get('possible_ends',[])),
                'actor_expectations_analyst_only':copy(actors[aid].get('expectations',[])),
                'historically_proposed_preproject':copy(history_genesis),
                'historically_proposed_functional':copy(functional_genesis),
                'historically_possible_material_meanings':copy(
                    material_meaning_proposals),
                'historically_possible_incidental_goods':copy(
                    possible_incidental_goods),
                'historically_possible_delayed_appraisals':copy(
                    delayed_expectation_appraisals),
                'historically_possible_co_regulation':copy(care_genesis),
                'historically_possible_plural_care':copy(plural_care_genesis),
                'historically_possible_reopened_care':copy(
                    renewed_relational_possibility),
                'actual_lived_high_resolution_care_ref':(
                    actual_lived_care['id'] if actual_lived_care else None),
                'historically_possible_co_regulation_revision':copy(
                    care_revision),
                'historically_possible_public_procedure_learning':copy(
                    institutional_learning),
                'bodily_before_actor_analyst_only':copy(bodily_before[aid]),
                'selected_purpose_analytic_only':copy(own_selection),
                'evidence_path':copy(actors[aid].get('evidence_paths',[])[-1]),
                # The analytic model may reason from the actual *computed*
                # preceding psychic organization. The simulated actor neither
                # observes this full packet nor has to possess its vocabulary.
                # A candidate remains fictional until actor-owned typed admit.
                'historical_psychodynamic_context':{
                    'before_objective_transition':copy(pre_event_psychodynamics.get(aid,{})),
                    'after_world_before_formation':copy(post_event_psychodynamics.get(aid,{})),
                    'analyst_only_not_actor_self_knowledge':True,
                    'reconstruct_from_admitted_current_not_a_recovered_memory':True,
                    'objective_event_ref':objective_ref},
                'grade':'SOURCEFREE_DEVELOPMENTAL_HYPOTHESIS'})
            developmental_candidates=copy(proposal['candidates'])
            if personally_done and actor_attempt is not None:
                issued_trial=actor_attempt.practical_selection.get('possible_end_trial')
                if issued_trial:
                    # A trial's historical fact is not optional model narration.
                    # The same existing developmental owner records the actual
                    # attempt without claiming motive satisfaction or knowledge.
                    developmental_candidates.insert(0,{
                        'kind':'RECORD_POSSIBLE_END_TRIAL',
                        'trial':copy(issued_trial),
                    })
            developmental[aid]=admit(actors[aid],experience,objective_ref,
                                    developmental_candidates)
        observed=subjective.get(actor_id,{})
        # A privileged world audit outcome is NOT automatically what this
        # person saw or can disclose. The event's public sign is deliberately
        # less informative than the real objective financial/material reason.
        public_sign=next((cue.get('description','EVENT_PERCEIVED') for cue in
                         observed.get('perceived_cues',[]) if cue.get('kind','').startswith('performed_')),
                         'UNKNOWN_TO_ACTOR')
        actual_tip={'action':principal.action,'outcome':public_sign,
                    'status':summary['status']}
        expression=self.semantic.proposal('expression',{'actor_id':actor_id,'actual':actual_tip,
               'actor_accessible':observed,
               'restriction':'NO_INNER_PSYCHIC_OMNISCIENCE'})
        payload={'attempt':principal.document(),'actor_selection_grade':principal.intention,
                 'external_research_plan_context':copy(research_plan_context),
                 'external_plan_is_not_actor_chosen_undertaking':True,
                 'coactor_attempt':partner.document() if partner else None,
                 'coactor_selection_grade':partner.intention if partner else None,
                 'coactor_policy_receipt':coactor_policy_receipt,
                 'objective_ref':objective_ref,'actual':summary,
                 'developmental_effects':developmental,'activity_effects':activity_effects,
                 'subjective_experience_refs':{aid:e['ref'] for aid,e in subjective.items()},
                 # Canonical research ledger retains each *separately keyed*
                 # access-qualified lived receipt. Do not send this audit-only
                 # material to the public expression service or other actor.
                 # Objective occurrence, actor experience, acquired afterlife
                 # are distinct and can now be independently reconstructed.
                 'private_actor_experience_receipts':copy(subjective),
                 'private_pre_event_psychodynamics':copy(pre_event_psychodynamics),
                 'private_post_event_psychodynamics':copy(post_event_psychodynamics),
                 'relational_dynamics_are_admitted_read_projections_not_actor_claims':True,
                 'model_service_grade':getattr(self.semantic.provider,'grade','INJECTED_EXTERNAL_PROVIDER'),
                 'sourcefree':True}
        committed=self.ledger.commit(self.world_id,wv,world,actors,actor_versions,
                                     'ACTOR_LIFE_TRANSITION',actor_id,payload)
        # Expression is not granted the private formation records.
        return {'receipt':committed['id'],'clock':world['clock'],'actor':actor_id,
            'attempt':principal.action,'selection_grade':principal.intention,
            'coactor':partner.action if partner else None,'status':resolved['status'],
            'objective_outcome':resolved['objective_description'],'public_tip':expression.get('surface'),
            'developmental_effect_count':{aid:len(e) for aid,e in developmental.items()},
            'grade':GRADE}

    def continue_without_user(self,beats=1):
        """Commit bounded real actor-selected, world-resolved life while absent.

        Unlike compressed background passage, each beat is a real transaction.
        The scheduler chooses who gets the occasion, not what they intend;
        it passes no external action, target, consent or forced developmental
        proposition into the continuing organism.
        """
        return continue_life(
            lambda: self.ledger.world(self.world_id)[1],
            self.ledger.actors,
            lambda actor_id: self.step(actor_id), beats)

    def advance_to_discontinuity(self,horizon=30):
        """Cover ordinary time only to the next real material interruption.

        A due commitment lets its owner initiate an independently selected
        response; no caller script forces fulfillment or another's consent.
        """
        return continue_to_discontinuity(self,horizon)

    def register_sourcefree_food_control(self,spec):
        """Configure a fictional material institution in WORLD, not in psyche.

        The caller declares the initial sourcefree power relation.
        Subsequent changes require distinct actor-selected signatures.
        No adult or child is automatically said to comprehend this rule.
        """
        v,world=self.ledger.world(self.world_id)
        actors=self.ledger.actors()
        source=configure_food_power(world,actors,spec)
        committed=self.ledger.commit(
            self.world_id,v,world,{}, {},
            'SOURCEFREE_FOOD_ACCESS_AUTHORITY_FIXTURE',None,{
                'source':source,'world_only_not_actor_political_action':True,
                'not_native_science_or_protected_receiving':True,
                'grade':GRADE})
        return {'receipt':committed['id'],**source}

    def register_sourcefree_pantry_concession(self,spec):
        """Fixture makes a concession available, not enacted or believed."""
        version,world=self.ledger.world(self.world_id)
        actors=self.ledger.actors()
        source=register_concession(world,actors,spec)
        receipt=self.ledger.commit(
            self.world_id,version,world,{}, {},
            'SOURCEFREE_PANTRY_CONCESSION_PRECONDITION',None,{
                'source':source,'not_actor_chosen_enclosure':True,
                'no_unearned_material_rights':True,'grade':GRADE})
        return {'receipt':receipt['id'],**source}

    def register_sourcefree_work_regime(self,spec):
        """World-only wage institutional fixture, not worker consent."""
        version,world=self.ledger.world(self.world_id)
        actors=self.ledger.actors()
        registered=register_work_regime(world,actors,spec)
        receipt=self.ledger.commit(
            self.world_id,version,world,{}, {},
            'SOURCEFREE_EXISTING_WAGE_RELATION_FIXTURE',None,{
                'source':registered,
                'contract_not_automatically_accepted':True,'grade':GRADE})
        return {'receipt':receipt['id'],**registered}

    def register_historical_routine_source(self,spec):
        """Declare a bounded *research fictional* routine source before use.

        This does not certify that an actor did something, was willing,
        learned an operation, or possessed a survey respondent's history.
        Only a later source-checked compressed passage can use this envelope.
        """
        v,world=self.ledger.world(self.world_id)
        actors=self.ledger.actors()
        source=register_sourcefree_period_envelope(world,actors,spec)
        receipt=self.ledger.commit(
            self.world_id,v,world,{}, {},
            'SOURCEFREE_HISTORICAL_ROUTINE_ENVELOPE',None,{
                'source_ref':source['id'],
                'world_only_not_actor_experience':True,
                'no_automatic_effect_or_native_science':True,
                'grade':GRADE})
        return {'receipt':receipt['id'],'source_ref':source['id'],
                'grade':'EXPLICIT_SOURCEFREE_HISTORICAL_FIXTURE'}

    def background(self,days,processes=None):
        v,w=self.ledger.world(self.world_id)
        actor_versions={aid:self.ledger.actor(aid)[0] for aid in self.ledger.actors()}
        actors=self.ledger.actors()
        period=passage(w,actors,days,processes)
        deltas={aid:recurring_provisional_growth(a,period['id'],period['processes']) for aid,a in actors.items()}
        commit=self.ledger.commit(self.world_id,v,w,actors,actor_versions,'COMPRESSED_ORDINARY_LIFE',None,
                                  {'period':period,'changes':deltas,'no_unwritten_microevents':True})
        return {'receipt':commit['id'],'period':period,'effects':deltas,'grade':GRADE}

    def possible_composed_activities(self,actor_id):
        from .plans import propose_compositions
        from .types import Situated
        packet=self.situated(actor_id)
        # Composition is a derived view, not a psychical state update.
        return [asdict(x) for x in propose_compositions(Situated(**packet))]

    def perform_composed_activity(self,actor_id,plan_id):
        current=next((p for p in self.possible_composed_activities(actor_id)
                      if p['id']==plan_id),None)
        if current is None:raise ValueError('PLAN_NOT_CURRENTLY_COMPOSABLE')
        # Every step is independently resolved; prior success never guarantees
        # later feasibility, consent or material outcome.
        transitions=[]
        context={'plan_id':current['id'],
                 'hypothesized_object':current['object'],
                 'hypothetical_project_ref':current.get('project_ref'),
                 'authority':'EXTERNAL_RESEARCH_PLAN',
                 'not_actor_attested_purpose':True,
                 'not_guaranteed_success_or_future_participation':True}
        for action in current['steps']:
            response=self.step(actor_id,requested_action=action,
                               research_plan_context=context)
            transitions.append(response)
            if response['status'] not in ('PERFORMED','PARTIAL'):break
        return {'plan_id':plan_id,'attempts':transitions,
           'external_plan_hypothesized_object':current['object'],
           'external_plan_not_actor_attributed_purpose':True,
           'observed_actual_attempts':len(transitions),
           'grade':GRADE, 'selection_grade':'EXTERNAL_RESEARCH_PLAN_INVOCATION',
           'no_guaranteed_outcome':True}

    def interview(self,actor_id,instrument):
        _,a=self.ledger.actor(actor_id)
        return interview_readout(a,instrument)

    def blind_interview(self,actor_id,instrument):
        """Target-free post-constitution respondent probe (not a fidelity claim).

        Unlike the legacy direct-keyed interview, this probe supplies neither
        sampled answers nor questionnaire-mediators to the semantic call.
        """
        _,world=self.ledger.world(self.world_id)
        _,actor=self.ledger.actor(actor_id)
        return render_blind_interview(actor,instrument,self.semantic,world)

    def verify(self):return self.ledger.verify_chain()
    def close(self):self.ledger.close()
