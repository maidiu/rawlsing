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
                       'not_actor_conscious_intent':True}
            bound_target=None
        else:
            proposed=self.semantic.proposal('actor_attempt',{'actor':{'id':actor_id,'role':actor['role']},
                'accessible':{k:v for k,v in asdict(e).items() if k!='inaccessible_count'},'situated':situated,'options':options,
                'requesting_actor':requesting_actor,'requesting_action':requesting_action})
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
            # Preserve only explicitly selected projects on Attempt; all
            # unselected courses remain in the situation, not the act's past.
            basis=[ref for ref in opt.get('basis',[])
                   if not (isinstance(ref,str) and ref.startswith('project:'))]
            basis+=['project:'+ref for ref in selected_refs]
            bound_target=(selected_alternative['world_request']['addressed_party_ref']
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
                       'not_actor_conscious_intent':True,
                       'not_premature_fulfillment':True,
                       'world_request':{
                           'operation':action,
                           'addressed_party_ref':bound_target}}
            authority='ACTOR_SITUATED_CANDIDATE_SELECTED_SOURCEFREE'
        return Attempt(actor_id,action,target=bound_target,means=[],basis=basis,
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
        attempt.object_ref=object_ref
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
        principal=self._actor_plan(actor_id,world,actors,requested_action)[0]
        if target is not None and principal.target not in (None,target):
            raise ValueError('CALLER_TARGET_CONFLICTS_WITH_ACTOR_PRACTICAL_ALTERNATIVE')
        if target is not None:principal.target=target
        principal.object_ref=object_ref
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
            personal_cues=[x for x in access.cues if x['id']==world['cues'][-1]['id']]
            if not participated and not personal_cues:continue
            own=personally_done['action'] if personally_done else ('RECEIVED_CARE' if aid in affected else None)
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
            felt_effect=(('SOMATIC_CARE_CANDIDATE' if summary['action']=='CARE'
                         else 'IMPOSED_EFFECT_UNINTERPRETED')
                         if aid in resolved['personal_effects'] and not personally_done
                         else None)
            experience={'actor':aid,'reciprocated_partner':reciprocal,
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
            developmental[aid]=admit(actors[aid],experience,objective_ref,proposal['candidates'])
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

    def verify(self):return self.ledger.verify_chain()
    def close(self):self.ledger.close()
