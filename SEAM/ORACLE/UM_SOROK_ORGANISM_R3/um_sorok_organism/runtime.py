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
            description='',modality='visual',private_to=None,lasting_ticks=0):
        """External world fixture change, not an actor psychological event."""
        wv,world=self.ledger.world(self.world_id)
        if actor_id is not None:self.ledger.actor(actor_id)
        cue=add_cue(world,kind,tags or [kind],location=location,description=description,
                    modality=modality,private_to=private_to,source_actor=actor_id,
                    clock_offset=1,lasting_ticks=lasting_ticks)
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
                     'project_id':None,'project_ids':[],
                     'other_available_projects_not_claimed':True}
            authority='INJECTED_NOT_NATIVE_ACTOR_CHOICE'
            trial_choice=None
        else:
            proposed=self.semantic.proposal('actor_attempt',{'actor':{'id':actor_id,'role':actor['role']},
                'accessible':{k:v for k,v in asdict(e).items() if k!='inaccessible_count'},'situated':situated,'options':options,
                'requesting_actor':requesting_actor,'requesting_action':requesting_action,
                'possible_end_trials':[copy(t) for o in options
                    for t in o.get('possible_end_trials',[])],
                'trial_is_not_durable_motive':True})
            requested_trial=proposed.get('possible_end_trial_id')
            if (requested_trial is not None and
                    proposed.get('practical_option_id') is not None):
                raise ValueError('POSSIBLE_END_TRIAL_SELECTION_CONFLICT')
            trial_choice=None
            if requested_trial is not None:
                if type(requested_trial) is not str or not requested_trial:
                    raise ValueError('INVALID_POSSIBLE_END_TRIAL_ID')
                issued=[t for o in options for t in o.get('possible_end_trials',[])
                    if t.get('trial_id')==requested_trial]
                if len(issued)!=1:
                    raise ValueError('UNISSUED_OR_AMBIGUOUS_POSSIBLE_END_TRIAL')
                trial_choice=issued[0]
                if (trial_choice.get('actor')!=actor_id or
                        trial_choice.get('as_of_clock')!=world['clock']):
                    raise ValueError('FOREIGN_OR_STALE_POSSIBLE_END_TRIAL')
            action=proposed.get('action')
            if trial_choice is not None:
                if action not in (None,trial_choice['operation']):
                    raise ValueError('POSSIBLE_END_TRIAL_OPERATION_CONFLICT')
                action=trial_choice['operation']
            opt=next((o for o in options if o['action']==action),None)
            if opt is None:raise ValueError('MODEL_ATTEMPT_NOT_ACTOR_ELIGIBLE')
            ok,why=eligible(actor['body'],action)
            if not ok:raise ValueError('MODEL_ACTION_BODILY_INELIGIBLE:'+why)
            # A physical operation may serve several possible projects, but
            # their availability is NOT the actor having undertaken them all.
            raw=proposed.get('project_ids')
            if raw is not None and proposed.get('project_id') is not None:
                raise ValueError('AMBIGUOUS_SINGLE_AND_MULTI_PURPOSE_SELECTION')
            if raw is None:
                one=proposed.get('project_id')
                selected_refs=[] if one is None else [one]
            else:
                if (type(raw) is not list or not raw or len(raw)>8 or
                        any(type(ref) is not str or not ref for ref in raw) or
                        len(set(raw))!=len(raw)):
                    raise ValueError('INVALID_MULTIPLE_PROJECT_SELECTION')
                selected_refs=raw
            available={course['project_id']:course for course in opt.get('project_courses',[])}
            if trial_choice is not None and selected_refs:
                raise ValueError('PROVISIONAL_TRIAL_CANNOT_ASSERT_ESTABLISHED_PROJECT')
            if any(ref not in available for ref in selected_refs):
                raise ValueError('MODEL_SELECTED_PURPOSE_NOT_SITUATED_ELIGIBLE')
            if trial_choice is not None and not any(
                    t.get('trial_id')==trial_choice['trial_id']
                    for t in opt.get('possible_end_trials',[])):
                raise ValueError('PROVISIONAL_TRIAL_NOT_IN_SELECTED_OPERATION')
            chosen=[available[ref] for ref in selected_refs]
            if chosen:
                purpose={'status':('ACTOR_POLICY_SELECTED_PROJECT_COURSE'
                     if len(chosen)==1 else 'ACTOR_POLICY_SELECTED_MULTIPLE_PROJECT_COURSES'),
                    'project_id':chosen[0]['project_id'] if len(chosen)==1 else None,
                    'project_ids':copy(selected_refs),
                    'practical_objects':[q['object'] for q in chosen],
                    'motive_hypotheses':[q['motive_hypothesis'] for q in chosen],
                    'selection_grade':proposed.get('purpose_selection_grade',
                        'MODEL_CHOSEN_COURSE_FICTIONAL_NOT_OBSERVED_CONSCIOUS_MOTIVE'),
                    'not_claimed_fulfillment':True,
                    'other_available_projects_not_claimed':True}
                if len(chosen)==1:purpose['practical_object']=chosen[0]['object']
            else:
                purpose={'status':'ACTOR_POLICY_NO_ATTESTED_PROJECT_PURPOSE',
                    'project_id':None,'project_ids':[],
                    'selection_grade':'EXPLORATORY_OR_UNRESOLVED_END_NOT_INFERRED',
                    'other_available_projects_not_claimed':True}
            if trial_choice is not None:
                purpose={'status':'ACTOR_POLICY_PROVISIONAL_END_TRIAL_NOT_DURABLE_MOTIVE',
                         'project_id':None,'project_ids':[],
                         'possible_end_ref':trial_choice['possible_end_ref'],
                         'selection_grade':'SOURCEFREE_TRIAL_NOT_CONSCIOUS_INTENT',
                         'object_fulfillment':'NOT_INFERRED'}
            basis=[r for r in opt.get('basis',[]) if
                   not (isinstance(r,str) and r.startswith('project:'))]
            basis+=['project:'+ref for ref in selected_refs]
            authority='ACTOR_SITUATED_CANDIDATE_SELECTED_SOURCEFREE' 
        return Attempt(actor_id,action,means=[],basis=basis,
                       intention=authority,purpose_selection=purpose,
                       practical_selection=({'possible_end_trial':copy(trial_choice)}
                            if trial_choice is not None else {}),
                       scene_hash=digest({'world':world,'actor':actor_id})),

    def plan(self,actor_id,requested_action=None,target=None,object_ref=None):
        _,world=self.ledger.world(self.world_id)
        actors=self.ledger.actors()
        if actor_id not in actors:raise ValueError('UNREGISTERED_ACTOR')
        attempt=self._actor_plan(actor_id,world,actors,requested_action)[0]
        attempt.target=target;attempt.object_ref=object_ref
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
             coactor_override=None):
        """One atomic joined life transition. Coactor always uses own plan.

        coactor_override is deliberately prohibited; original R0 consent bug
        is repaired in this research implementation at the public transaction.
        """
        if coactor_override is not None:raise ValueError('FORGED_COACTOR_OVERRIDE_REFUSED')
        wv,world=self.ledger.world(self.world_id)
        actor_versions={aid:self.ledger.actor(aid)[0] for aid in self.ledger.actors()}
        actors=self.ledger.actors()
        # Private pre-event person×event computation is recorded in the
        # sealed research receipt, not in the public tip or model renderer.
        before=asdict(compose(materialize(actors[actor_id],world),
                               actor_access(actors[actor_id],world)))
        private_pre_event_psychodynamics={
            'actor':actor_id,'currents':copy(before['currents']),
            'readset':copy(before['readset']),
            'grade':'SOURCEFREE_RESEARCH_PROVISIONAL',
            'not_actor_self_knowledge':True}
        principal=self._actor_plan(actor_id,world,actors,requested_action)[0]
        principal.target=target;principal.object_ref=object_ref
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
        developmental={};subjective={}
        for aid in actors:
            # Separate actor-specific view, no analyst world description in LLM input.
            access=actor_access(actors[aid],world)
            personally_done=next((r for r in resolved['performed'] if r['actor']==aid),None)
            participated=aid in affected
            if not participated and not access.cues:continue
            personal_cues=[x for x in access.cues if x['id']==world['cues'][-1]['id']]
            if not participated and not personal_cues:continue
            own=personally_done['action'] if personally_done else ('RECEIVED_CARE' if aid in affected else None)
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
            received=[c for c in personal_cues if isinstance(c,dict)]
            if personally_done and received:
                actors[aid].setdefault('evidence_paths',[]).append({
                    'experience_ref':experience['ref'],
                    'objective_event_ref':objective_ref,
                    'own_action':personally_done['action'],
                    'selected_project_refs':copy(
                        (principal if aid==actor_id else partner).purpose_selection.get('project_ids',[])),
                    'received_cue_refs':[c.get('id') for c in received],
                    'received_cue_tags':sorted({str(t).lower() for c in received
                        for t in c.get('tags',[])}),
                    'actor_access_grade':GRADE,
                    'purpose_status':(principal if aid==actor_id else partner).purpose_selection.get('status'),
                    'selected_project_ref':(principal if aid==actor_id else partner).purpose_selection.get('project_id'),
                    'unencountered_alternatives':'UNKNOWN_NOT_OBSERVED',
                    'not_an_unperformed_counterfactual':True})
            # Actor-owned practical afterlife is separate from world objective
            # outcome. It can later be recruited, but is not motive fulfillment.
            register_lived_activity_attempt(actors[aid],experience,activity_effects.get(aid,[]))
            # Disabled LLM proposals may truthfully produce no change.
            proposal=self.semantic.proposal('development',{'actor':{'id':aid,'role':actors[aid]['role'],
                'body':copy(actors[aid]['body']),'location':actors[aid]['location']},
                'clock':world['clock'],'experience':experience,
                'selected_constitution':asdict(compose(materialize(actors[aid],world),access)),
                'actor_forms':copy(actors[aid]['forms']),
                'actor_possible_ends':copy(actors[aid].get('possible_ends',[])),
                'historical_psychodynamic_context':{'objective_event_ref':objective_ref},
                'selected_purpose_analytic_only':copy(
                    (principal if aid==actor_id else partner).purpose_selection
                    if personally_done else {}),
                'grade':'SOURCEFREE_DEVELOPMENTAL_HYPOTHESIS'})
            # The separate runtime-owned issuance is not in LLM candidates.
            # Only actually performed principal/coactor acts retain a ticket.
            actor_attempt=(principal if aid==actor_id else partner)
            issued=(actor_attempt.practical_selection.get('possible_end_trial')
                    if personally_done and actor_attempt else None)
            developmental[aid]=admit(actors[aid],experience,objective_ref,
                proposal['candidates'],issued_trial=copy(issued) if issued else None)
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
                 'coactor_attempt':partner.document() if partner else None,
                 'coactor_selection_grade':partner.intention if partner else None,
                 'coactor_policy_receipt':coactor_policy_receipt,
                 'private_pre_event_psychodynamics':private_pre_event_psychodynamics,
                 'objective_ref':objective_ref,'actual':summary,
                 'developmental_effects':developmental,'activity_effects':activity_effects,
                 'subjective_experience_refs':{aid:e['ref'] for aid,e in subjective.items()},
                 # Canonical research ledger retains each *separately keyed*
                 # access-qualified lived receipt. Do not send this audit-only
                 # material to the public expression service or other actor.
                 # Objective occurrence, actor experience, acquired afterlife
                 # are distinct and can now be independently reconstructed.
                 'private_actor_experience_receipts':copy(subjective),
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
        for action in current['steps']:
            response=self.step(actor_id,requested_action=action)
            transitions.append(response)
            if response['status'] not in ('PERFORMED','PARTIAL'):break
        return {'plan_id':plan_id,'attempts':transitions,
           'observed_actual_attempts':len(transitions),
           'grade':GRADE, 'selection_grade':'EXTERNAL_RESEARCH_PLAN_INVOCATION',
           'no_guaranteed_outcome':True}

    def interview(self,actor_id,instrument):
        _,a=self.ledger.actor(actor_id)
        return interview_readout(a,instrument)

    def verify(self):return self.ledger.verify_chain()
    def close(self):self.ledger.close()
