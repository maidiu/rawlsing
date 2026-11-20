"""UM-SOROK TCO R4 integrated provisional living computational organism.

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
from .becoming import LivedDifferenceKernel
from .relational import RelationalKernel
from .parents import construct_parent, interview_readout
from .semantics import ValidatingSemanticService
from .world import IndependentWorldAuthority, COOPERATIVE, add_cue

class ConstitutiveRuntime:
    def __init__(self,db,semantic=None,world_id='w1',becoming=None,relational=None):
        self.ledger=ResearchLedger(db)
        self.semantic=semantic or ValidatingSemanticService()
        self.world_id=world_id
        self.authority=IndependentWorldAuthority(self._independent_coactor_plan)
        self.becoming=becoming or LivedDifferenceKernel()
        self.relational=relational or RelationalKernel()

    def initialize(self,parent_packets=None,child_id='nadia',child_name='Nadia'):
        world=blank_world(self.world_id)
        parents=[]
        for actor_id,name,packet in (parent_packets or []):
            person=construct_parent(actor_id,name,packet,self.semantic)
            parents.append(person)
        child=newborn(child_id,child_name)
        world['institutions']['hall_board']['members']=[parents[0]['id']] if parents else []
        self.ledger.initialize(world,parents+[child])
        for a,_,packet in (parent_packets or []):
            self.ledger.seal_source('fictional_source:'+a,'CONDITIONING_NOT_REAL_PERSON',packet)
        return {'world':self.world_id,'actors':[a['id'] for a in parents+[child]],'grade':GRADE}

    def snapshot(self,actor_id):
        _,world=self.ledger.world(self.world_id)
        _,person=self.ledger.actor(actor_id)
        return asdict(materialize(person,world))

    def see(self,actor_id):
        _,world=self.ledger.world(self.world_id)
        _,person=self.ledger.actor(actor_id)
        return asdict(actor_access(person,world,self.becoming))

    def situated(self,actor_id):
        _,world=self.ledger.world(self.world_id)
        _,person=self.ledger.actor(actor_id)
        const=materialize(person,world)
        access=actor_access(person,world,self.becoming)
        return asdict(compose(const,access,historical_kernel=self.becoming,relational_kernel=self.relational))

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
        c=materialize(actor,world);e=actor_access(actor,world,self.becoming);situated=asdict(compose(c,e,historical_kernel=self.becoming,relational_kernel=self.relational))
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
            authority='INJECTED_NOT_NATIVE_ACTOR_CHOICE'
        else:
            proposed=self.semantic.proposal('actor_attempt',{'actor':{'id':actor_id,'role':actor['role']},
                'accessible':{k:v for k,v in asdict(e).items() if k!='inaccessible_count'},'situated':situated,'options':options,
                'requesting_actor':requesting_actor,'requesting_action':requesting_action})
            action=proposed['action']
            opt=next((o for o in options if o['action']==action),None)
            if opt is None:raise ValueError('MODEL_ATTEMPT_NOT_ACTOR_ELIGIBLE')
            ok,why=eligible(actor['body'],action)
            if not ok:raise ValueError('MODEL_ACTION_BODILY_INELIGIBLE:'+why)
            # A globally eligible operation is NOT proof the actor undertook
            # all projects which happen to share that means. A policy may
            # explicitly select compatible projects; single project defaults
            # remain sourcefree hypotheses. A genuinely ambiguous selection
            # keeps the motive unresolved instead of manufacturing ownership.
            allowed_projects={b.removeprefix('project:') for b in opt.get('basis',[])
                               if isinstance(b,str) and b.startswith('project:')}
            nominated=proposed.get('project_ids')
            if nominated is None:
                nominated=sorted(allowed_projects) if len(allowed_projects)==1 else []
            if (not isinstance(nominated,list) or len(nominated)!=len(set(nominated)) or
                any(not isinstance(p,str) or p not in allowed_projects for p in nominated)):
                raise ValueError('MODEL_PROJECT_INTENTION_NOT_SUPPORTED')
            basis=[b for b in opt.get('basis',[])
                   if not (isinstance(b,str) and b.startswith('project:'))]
            basis+=['project:'+p for p in nominated]
            authority='ACTOR_SITUATED_CANDIDATE_SELECTED_SOURCEFREE'
        return Attempt(actor_id,action,means=[],basis=basis,
                       intention=authority,scene_hash=digest({'world':world,'actor':actor_id})),

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
        """An autonomous actor policy or explicitly external action injection."""
        if coactor_override is not None:raise ValueError('FORGED_COACTOR_OVERRIDE_REFUSED')
        wv,world=self.ledger.world(self.world_id)
        versions={aid:self.ledger.actor(aid)[0] for aid in self.ledger.actors()}
        actors=self.ledger.actors()
        if actor_id not in actors:raise ValueError('UNREGISTERED_ACTOR')
        principal=self._actor_plan(actor_id,world,actors,requested_action)[0]
        principal.target=target;principal.object_ref=object_ref
        return self._execute_attempt(actor_id,principal,wv,world,actors,versions)

    def _execute_attempt(self,actor_id,principal,wv,world,actors,actor_versions):
        """One world-authorized, independently coactor-resolved atomic life turn.

        A history-derived endogenous attempt uses the SAME world owner and
        afterlife as normal self-prospect. The argument is an internal planned
        attempt, not a public caller's permission to forge coactor behavior.
        """
        if actor_id!=principal.actor or actor_id not in actors:
            raise ValueError('ATTEMPT_ACTOR_IDENTITY_MISMATCH')
        # A caller never supplies another actor's response. The world owner
        # obtains it from the installed independently constituted actor policy.
        before_bodies={aid:copy(a['body']) for aid,a in actors.items()}
        before_world=copy(world)
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
            # World-owned material feasibility provenance, not an actor belief.
            # A later genesis mechanism can distinguish an actually altered
            # affordance from mere temporal B-between-failure-and-success.
            aid=row['actor'];origin=before_world['positions'].get(aid)
            previous=before_world['sites'].get(origin,{})
            current=world['sites'].get(origin,{})
            changes=[];requirements=[]
            for field in ('stock','food'):
                b=previous.get(field);a=current.get(field)
                if isinstance(a,(int,float)) and isinstance(b,(int,float)) and a!=b:
                    changes.append({'path':'sites.'+str(origin)+'.'+field,
                                    'before':b,'after':a,'delta':a-b})
            if row['action']=='REPAIR':
                req=previous.get('stock',0)
                requirements=[{'path':'sites.'+str(origin)+'.stock',
                    'required_at_least':1,'actual_before':req,
                    'satisfied':req>=1}]
            # The event summary's objective outcome describes the principal's
            # act. A coactor's separately undertaken operation must not
            # inherit that outcome as if the coactor performed the same act.
            actor_outcome=(summary['outcome'] if aid==actor_id else
                ('COACTOR_'+str(row['action'])+'_'+str(row['status'])))
            activity_effects[aid]=record_activity_afterlife(actors[aid],
                row['action'],row['status'],actor_outcome,chosen.basis,objective_ref,
                {'material_claim_ref':summary.get('material_claim_ref'),
                 'affordance_changes':changes,'affordance_requirements':requirements,
                 'material_owner':'INDEPENDENT_WORLD_RESEARCH_AUTHORITY'})
        developmental={};subjective={};historical_becoming={}
        for aid in actors:
            # Separate actor-specific view, no analyst world description in LLM input.
            access=actor_access(actors[aid],world,self.becoming)
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
            # Experimental interoceptive read-model: only this actor's own
            # present body change, never another's objective status/intent.
            pre=before_bodies[aid];post=actors[aid]['body']
            body_registration=[]
            if (post['comfort']-pre['comfort']>=.06 or
                pre['arousal']-post['arousal']>=.06):
                body_registration.append('SETTLING_PROXY')
            if pre['comfort']-post['comfort']>=.06:
                body_registration.append('DISTRESS_PROXY')
            experience={'actor':aid,'reciprocated_partner':reciprocal,
                        'ref':stable_id('experience',{'actor':aid,'event':objective_ref,
                                         'cues':personal_cues,'participated':participated,
                                         'felt_enactment':felt_enactment}),
                        'own_action':own,'status':personally_done['status'] if personally_done else 'OBSERVED',
                        'perceived_cues':personal_cues,'participated':participated,
                        'felt_enactment':felt_enactment,'felt_effect':felt_effect,
                        'interoceptive_change':body_registration,
                        'interoceptive_grade':'SOURCEFREE_NONCONCEPTUAL_BODY_PROXY',
                        'actor_access_grade':GRADE}
            subjective[aid]=copy(experience)
            lived=register_lived_activity_attempt(actors[aid],experience,
                                                activity_effects.get(aid,[]))
            changed=self.becoming.register_preconceptual(actors[aid],experience,world['clock'])
            changed+=self.becoming.register(actors[aid],experience,lived,world['clock'])
            changed+=self.becoming.propose_second_order(actors[aid],experience,lived)
            historical_becoming[aid]=changed
            # Disabled LLM proposals may truthfully produce no change.
            proposal=self.semantic.proposal('development',{'actor':{'id':aid,'role':actors[aid]['role'],
                'body':copy(actors[aid]['body']),'location':actors[aid]['location']},
                'clock':world['clock'],'experience':experience,
                'selected_constitution':asdict(compose(materialize(actors[aid],world),access,historical_kernel=self.becoming,relational_kernel=self.relational)),
                'actor_forms':copy(actors[aid]['forms']),
                'historical_formation':copy(changed),
                'lived_courses':copy(actors[aid].get('lived_course_series',{})),
                'grade':'SOURCEFREE_DEVELOPMENTAL_HYPOTHESIS'})
            developmental[aid]=admit(actors[aid],experience,objective_ref,proposal['candidates'])
        observed=subjective.get(actor_id,{})
        actual_tip={'action':principal.action,'outcome':summary['outcome'] if observed.get('perceived_cues') else 'UNKNOWN_TO_ACTOR',
                    'status':summary['status']}
        expression=self.semantic.proposal('expression',{'actor_id':actor_id,'actual':actual_tip,
               'actor_accessible':observed,
               'restriction':'NO_INNER_PSYCHIC_OMNISCIENCE'})
        payload={'attempt':principal.document(),'actor_selection_grade':principal.intention,
                 'coactor_attempt':partner.document() if partner else None,
                 'coactor_selection_grade':partner.intention if partner else None,
                 'coactor_policy_receipt':coactor_policy_receipt,
                 'objective_ref':objective_ref,'actual':summary,
                 'developmental_effects':developmental,'activity_effects':activity_effects,
                 'historical_becoming':historical_becoming,
                 'becoming_mechanism_version':self.becoming.version,
                 'relational_mechanism_version':self.relational.version,
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
            'historical_becoming_count':{aid:len(e) for aid,e in historical_becoming.items()},
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

    def continue_life(self,actor_id):
        """Actor-originated research selection of an *acquired* practical method.

        Caller chooses only WHO to advance, not action, plan, Other's consent,
        project or result. Methods must have emerged through lived actor history.
        Each operation rechecks current body, learned method, means and world.
        This is a declared imperfect deterministic research policy, not human
        psychology, not a secure adversarial-process sandbox.
        """
        actor=self.ledger.actor(actor_id)[1]
        methods=actor.get('historical_composition_methods',{})
        current=self.possible_composed_activities(actor_id)
        candidates=[p for p in current if any(m in methods for m in p['basis'])]
        if not candidates:
            return {'actor':actor_id,'attempts':[], 'reason':'NO_QUALIFIED_ACQUIRED_METHOD',
                    'sourcefree':True}
        # Deterministic policy over the actor's own methods, not a caller plan ID.
        selected=sorted(candidates,key=lambda p:p['id'])[0]
        project_ids=[b.removeprefix('project:') for b in selected['basis']
                     if b.startswith('project:')]
        if len(project_ids)!=1:raise ValueError('HISTORICAL_METHOD_PROJECT_NOT_UNIQUE')
        project_id=project_ids[0]
        attempts=[]
        for operation in selected['steps']:
            wv,world=self.ledger.world(self.world_id)
            versions={aid:self.ledger.actor(aid)[0] for aid in self.ledger.actors()}
            actors=self.ledger.actors()
            p=next((p for p in actors[actor_id]['projects'] if p['id']==project_id),None)
            if not p or operation not in p.get('means',[]):break
            # Re-evaluate current recruitability; no stale method grant.
            present=self.possible_composed_activities(actor_id)
            if selected['id'] not in {m['id'] for m in present}:break
            allowed,_=eligible(actors[actor_id]['body'],operation)
            if not allowed:break
            from .types import Attempt
            principal=Attempt(actor_id,operation,basis=['project:'+project_id,
                 'historical_method:'+selected['id']],
                 intention='ACTOR_HISTORY_DERIVED_METHOD_SELECTED_SOURCEFREE',
                 scene_hash=digest({'world':world,'actor':actor_id}))
            result=self._execute_attempt(actor_id,principal,wv,world,actors,versions)
            attempts.append(result)
            if result['status']!='PERFORMED':break
        return {'actor':actor_id,'method':selected['id'],
                'project':project_id,'attempts':attempts,'sourcefree':True,
                'selection_grade':'ACTOR_HISTORY_DERIVED_METHOD_SELECTED_SOURCEFREE',
                'no_predetermined_success':True}

    def interview(self,actor_id,instrument):
        _,a=self.ledger.actor(actor_id)
        return interview_readout(a,instrument)

    def verify(self):return self.ledger.verify_chain()
    def close(self):self.ledger.close()
