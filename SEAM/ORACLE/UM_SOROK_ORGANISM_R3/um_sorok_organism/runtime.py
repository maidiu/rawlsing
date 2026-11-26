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
from .development import admit, recurring_provisional_growth, possible_practice_memory_access_decrease
from .reflective_regulation import offer_private_rehearsals, perform_private_rehearsal
from .attention_field import (offer_undertaking_attention, received_undertaking_attention,
    offer_correspondence_attention, settle_correspondence_attention, received_correspondence_attention,
    offer_focal_encounters, received_focal_encounter, personally_received_directed_act,
    possible_monitoring_changes)
from .ordinary_life import passage
from .activity import (record_activity_afterlife, register_lived_activity_attempt,
                        possible_productive_witness_reorganizations,
                       possible_dependency_project_reorganizations,
                       possible_dependency_means_revisions, qualify_interactivity_deferral,
                       possible_interactivity_relations)
from .practical_difference import start_selected_expectations
from .lived_genesis import proposals_from_bodily_history
from .historical_self_organization import (possible_lived_directional_orientation,
                                           possible_dependency_ambivalence,
                                           possible_counterhistory_release)
from .distributed_power import record_actor_participation
from .practical_powers import retain_exercised_power, possible_repair_technique
from .practical_inquiry import retain_personal_notice_exposure
from .material_investments import (
    retain_personal_object_encounter, possible_object_investments)
from .unintended_goods import possible_unintended_goods, qualify_incidental_object_takeup
from .expectation_afterlife import (source_qualified_appraisal_candidates,
                                    possible_activity_affects, own_vocal_reception,
                                    possible_expressive_practices)
from .routine_sources import register_sourcefree_period_envelope
from .caregiving_practice import retain_performed_material_feeding
from .food_access_struggle import configure_food_power
from .food_power_reproduction import register_concession
from .institutional_procedure_learning import (
    possible_institutional_learning, possible_lived_institutional_differences,
    possible_notice_expectations, possible_notice_revisions,
)
from .material_dependency_history import conserve_sensed_material_nonperformance
from .livelihood_history import (
    conserve_incomplete_work, possible_recurrent_work_orientation,
)
from .psychic_genesis import (
    conserve_lived_episode,possible_contrast_end,possible_dependency_project_takeups,
    possible_productive_vocal_takeups)
from .joint_practice_genesis import possible_joint_practice
from .care_commitment_genesis import (
    conserve_costly_offered_care,candidate_care_commitment)
from .cultural_mediation import (
    conserve_personally_heard_reference,
    possible_cultural_object_inquiry,possible_reference_revision)
from .social_vocal_development import (
    conserve_reciprocated_vocal_turn,possible_vocal_coordination)
from .labor_dependency import register_work_regime
from .co_regulation_history import (
    possible_acquired_regulation, record_lived_co_regulation_response,
    possible_revision_after_nonresponse)
from .plural_care_paths import (
    conserve_lived_high_resolution_care, plural_acquisition_candidate,
    sourcequalified_reopening)
from .functional_correspondence import (propose_actor_lived_correspondences,
                                        possible_functional_revisions)
from .initiative import continue_life
from .continuity_clock import continue_to_discontinuity, continue_pre_encounter, qualify_contingent_world_notice
from .historical_parent_bridge import (render_blind_interview, qualify_family_pathways,
    family_encounter_evidence, FAMILY_SOURCE, FAMILY_GRADE)
from .material_conjunction import admit_authored_structural_history
from .operative_witness import freeze_operative_witness
from .parents import construct_parent, interview_readout, select_staged_counterpart
from .semantics import ValidatingSemanticService
from .relational_metabolism import (
    possible_witnessed_third_party_relation,
    possible_lived_cross_context_revaluations)
from .world import (IndependentWorldAuthority, COOPERATIVE, add_cue,
                    register_recursive_encounter_paths, qualified_human_vocal_receipt)

def _bind_actor_trial_particular_object(alternatives, trial):
    """Choose one perceived thing, not one asserted explanation for perceiving it.

    One objective material object can be represented by an ordinary visible
    object option AND an independently acquired cultural or historical option.
    Their shared world referent is not an ambiguous physical object. For a
    source-object trial, retain the neutral visible-object binding, leaving
    the cultural alternative unselected rather than laundering its meaning
    into the actor's provisional purpose.
    """
    object_ref=trial.get('source_material_object_ref')
    if type(object_ref) is not str or not object_ref:
        raise ValueError('TRIAL_MATERIAL_OBJECT_NOT_UNIQUELY_BINDABLE')
    operation=trial.get('operation')
    matches=[a for a in alternatives if
             type(a) is dict and a.get('operation')==operation
             and a.get('project_id') is None
             and type(a.get('world_request')) is dict
             and a['world_request'].get('material_object_ref')==object_ref]
    neutral=[a for a in matches if
             a.get('grounds_status')=='PRESENT_MATERIAL_OBJECT_NOT_ASSUMED_MOTIVE'
             and a.get('binding_status')=='OBJECT_CURRENTLY_VISIBLE_NOT_EVIDENCE_OF_RIGHTS']
    if len(neutral)==1:
        return neutral[0]
    if len(matches)==1:
        return matches[0]
    raise ValueError('TRIAL_MATERIAL_OBJECT_NOT_UNIQUELY_BINDABLE')


class ConstitutiveRuntime:
    def __init__(self,db,semantic=None,world_id='w1'):
        self.ledger=ResearchLedger(db)
        self.semantic=semantic or ValidatingSemanticService()
        self.world_id=world_id
        self.authority=IndependentWorldAuthority(self._independent_coactor_plan)

    @classmethod
    def with_explicit_json_llm(cls,db,*,endpoint,model,api_key,
                               allow_private_actor_data=False,
                               world_id='w1',transport=None):
        """Real opt-in semantic machinery; no implicit remote disclosure.

        This only selects a model provider. Psychic development still
        requires an actual world experience and the existing typed owner.
        """
        from .live_psychological_llm import ExplicitJSONLLMProvider
        provider=ExplicitJSONLLMProvider(
            endpoint=endpoint,model=model,api_key=api_key,
            allow_private_actor_data=allow_private_actor_data,
            transport=transport)
        return cls(db,semantic=ValidatingSemanticService(provider),
                   world_id=world_id)

    def initialize(self,parent_packets=None,child_id='nadia',child_name='Nadia',
                   *, authored_structural_history=None):
        world=blank_world(self.world_id)
        parent_packets=list(parent_packets or [])
        # World source is independent of the semantic construction of adults.
        # Validate before asking a model to construct anyone.
        if authored_structural_history is not None:
            admit_authored_structural_history(
                world,{a for a,_,_ in parent_packets}|{child_id},
                authored_structural_history)
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
        if authored_structural_history is not None:
            source_seals.append(('authored_structural_history','FICTIONAL_WORLD_CONDITIONING',
                                 authored_structural_history))
        self.ledger.initialize(world,parents+[child],source_seals=source_seals)
        return {'world':self.world_id,'actors':[a['id'] for a in parents+[child]],'grade':GRADE}

    def initialize_antecedent_adult(self,actor_id,name,packet,*,authored_structural_history=None):
        """Alternative entrance: one actually continuing adult, no precreated child."""
        world=blank_world(self.world_id)
        if authored_structural_history is not None:
            admit_authored_structural_history(world,{actor_id},authored_structural_history)
        person=construct_parent(actor_id,name,packet,self.semantic)
        seals=[('fictional_source:'+actor_id,'CONDITIONING_NOT_REAL_PERSON',packet)]
        if authored_structural_history is not None:
            seals.append(('authored_structural_history','FICTIONAL_WORLD_CONDITIONING',authored_structural_history))
        self.ledger.initialize(world,[person],source_seals=seals)
        return {'world':self.world_id,'actors':[actor_id],'grade':GRADE}

    def register_family_pathways(self,mother_id,candidates):
        version,world=self.ledger.world(self.world_id)
        mother=self.ledger.actor(mother_id)[1]
        source=qualify_family_pathways(world,mother,candidates)
        sid='family_pathways:'+mother_id
        self.ledger.seal_source(sid,FAMILY_SOURCE,source,expected_world=version)
        return {'source_seal_id':sid,'proposal_clock':source['proposal_clock'],
                'candidate_ids':[x['id'] for x in source['candidates']], 'grade':FAMILY_GRADE}

    def _family_source(self,sid):
        row=self.ledger.source(sid)
        if not row or row['category']!=FAMILY_SOURCE:raise ValueError('FAMILY_SOURCE_NOT_SEALED')
        return row['content'],digest(row)

    def _admit_family_actor(self,version,world,actor,family,kind,sid,sha):
        aid=actor['id']
        if aid in world['positions']:raise ValueError('FAMILY_ACTOR_ALREADY_PRESENT')
        world['positions'][aid]=actor['location']
        world.setdefault('accounts',{})[aid]=0.0
        world.setdefault('holdings',{})[aid]={'food':0}
        world['family_genesis']=copy(family)
        result=self.ledger.commit(self.world_id,version,world,{}, {},kind,aid,
                {'admitted_actor':aid,'source_seal_id':sid,'source_digest':sha,
                 'family_genesis':family,'no_automatic_actor_experience':True,'grade':FAMILY_GRADE},
                _family_actor=actor)
        return {'receipt':result['id'],'actor':aid,'stage':family['stage'],'grade':FAMILY_GRADE}

    def select_family_intersection(self,source_seal_id):
        version,world=self.ledger.world(self.world_id)
        source,sha=self._family_source(source_seal_id)
        mother=self.ledger.actor(source['mother'])[1]
        selected=select_staged_counterpart(world,mother,source,self.semantic)
        if selected is None:return {'status':'ABSTAINED','grade':FAMILY_GRADE}
        path,father=selected
        row={k:copy(path[k]) for k in ('id','source_ref','intersection_clock','intersection_site',
                 'conception_clock','birth_clock','child_id','child_name')}
        row.update({'mother':mother['id'],'counterpart':father['id'],'admitted_clock':world['clock'],
                    'proposal_clock':source['proposal_clock'],
                    'maternal_proposal_state_digest':source['maternal_proposal_state_digest'],
                    'maternal_selection_state_digest':stable_id('maternal_proposal',mother),
                    'prior_shared_effects':'UNKNOWN_NOT_ADMITTED'})
        family={'stage':'COUNTERPART_ADMITTED','source_seal_id':source_seal_id,
                'source_digest':sha,'selected_pathway':row,
                'not_relationship_household_consent_or_conception':True}
        return self._admit_family_actor(version,world,father,family,'FAMILY_COUNTERPART_ADMITTED',
                                        source_seal_id,sha)

    def admit_family_conception(self):
        """Explicit branch premise, not a deduction from social conduct."""
        version,world=self.ledger.world(self.world_id)
        family=world.get('family_genesis',{})
        if family.get('stage')!='COUNTERPART_ADMITTED':raise ValueError('FAMILY_NO_SELECTED_COUNTERPART')
        path=family['selected_pathway'];source,sha=self._family_source(family['source_seal_id'])
        if sha!=family['source_digest'] or world['clock']!=path['conception_clock']:
            raise ValueError('FAMILY_CONCEPTION_WRONG_SOURCE_OR_CLOCK')
        if not all(world['positions'].get(a)==path['intersection_site'] for a in (path['mother'],path['counterpart'])):
            raise ValueError('FAMILY_CONCEPTION_LOCATION_UNQUALIFIED')
        encounters=family_encounter_evidence(world,path)
        if not encounters:raise ValueError('FAMILY_NO_ACTUAL_DIRECTED_ENCOUNTER')
        family['stage']='CONCEPTION_ADMITTED'
        family['conception']={'id':stable_id('conditional_conception',path),
             'clock':world['clock'],'encounter_evidence':encounters[-1],
             'sourcefree_branch_premise_not_biological_or_consent_inference':True,
             'no_child_actor_yet':True,'grade':FAMILY_GRADE}
        result=self.ledger.commit(self.world_id,version,world,{}, {},
                'FAMILY_CONCEPTION',None,{'family_genesis':copy(family),'grade':FAMILY_GRADE})
        return {'receipt':result['id'],'stage':family['stage'],'grade':FAMILY_GRADE}

    def realize_family_birth(self):
        version,world=self.ledger.world(self.world_id)
        family=world.get('family_genesis',{})
        if family.get('stage')!='CONCEPTION_ADMITTED':raise ValueError('FAMILY_NO_ADMITTED_CONCEPTION')
        path=family['selected_pathway'];source,sha=self._family_source(family['source_seal_id'])
        if sha!=family['source_digest'] or world['clock']!=path['birth_clock']:
            raise ValueError('FAMILY_BIRTH_WRONG_SOURCE_OR_CLOCK')
        location=world['positions'][path['mother']]
        child=newborn(path['child_id'],path['child_name'],location)
        family['stage']='CHILD_BORN'
        family['birth']={'id':stable_id('conditional_birth',path),'clock':world['clock'],
            'child':child['id'],'biological_lineage_refs':[path['mother'],path['counterpart']],
            'conception_ref':family['conception']['id'],'location':location,
            'household_care_relationship_and_psyche_not_inferred':True,'grade':FAMILY_GRADE}
        return self._admit_family_actor(version,world,child,family,'FAMILY_CHILD_BORN',
                                        family['source_seal_id'],sha)

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
        # R13/P073: an explicit empty set of signs is not a missing value.
        # False, empty text, tuples and mixed types cannot be coerced into
        # a new analyst tag, thereby inventing actor-receivable evidence.
        if tags is None:
            terms=[kind]
        elif type(tags) is not list or any(type(t) is not str for t in tags):
            raise ValueError('INVALID_CUE_TAGS')
        else:
            terms=tags
        cue=add_cue(world,kind,terms,location=location,description=description,
                    modality=modality,private_to=private_to,source_actor=actor_id,
                    clock_offset=1,lasting_ticks=lasting_ticks)
        world['clock']+=1
        receipt=self.ledger.commit(self.world_id,wv,world,{}, {},'OBJECTIVE_CUE',actor_id,
            {'cue_ref':cue['id'],'issuer':'EXTERNAL_RESEARCH_FIXTURE','not_actor_memory':True})
        return {'receipt':receipt['id'],'cue':cue,'grade':GRADE}

    def offer_contingent_world_notice(self,proposal):
        """Offer a common event *candidate* into this branch's existing world.

        A system-wide calendar or live-news service can propose the same
        sourcefree notice to multiple separate continuities. No such service
        is implemented by this method. Each branch independently checks its
        present world; eligibility admits ONLY a public sensory sign, not
        scripted physical consequences, actor assent, knowledge, or emotion.
        """
        v,world=self.ledger.world(self.world_id)
        actors=self.ledger.actors()
        verdict=qualify_contingent_world_notice(world,actors,proposal)
        offer_hash=digest(proposal)
        prior=[c for c in world['cues']
               if c.get('contingent_offer_id')==proposal['offer_id']]
        if prior:
            if (len(prior)!=1 or prior[0].get('contingent_offer_hash')!=offer_hash):
                raise ValueError('CONTINGENT_NOTICE_CONFLICTING_REPLAY')
            return {'status':'ALREADY_ADMITTED_IN_THIS_WORLD',
                    'offer_id':proposal['offer_id'],'cue_ref':prior[0]['id'],
                    'clock':world['clock'],'no_second_world_event':True,
                    'grade':GRADE}
        if verdict['status']!='ELIGIBLE_SOURCEFREE_NOTICE_ONLY':
            return {**verdict,'no_world_write':True,'grade':GRADE}
        cue=add_cue(world,proposal['kind'],proposal['tags'],
                    location=proposal['location'],
                    description=proposal['description'],
                    modality='auditory',source_actor=None,
                    clock_offset=1,lasting_ticks=0)
        cue['contingent_offer_id']=proposal['offer_id']
        cue['contingent_offer_hash']=offer_hash
        cue['external_sign_only_not_verified_news_or_world_damage']=True
        world['clock']+=1
        committed=self.ledger.commit(self.world_id,v,world,{}, {},
             'SOURCEFREE_CONTINGENT_WORLD_NOTICE',None,{
                'offer_id':proposal['offer_id'],
                'proposal_hash':offer_hash,
                'cue_ref':cue['id'],
                'independent_branch_eligibility':verdict['status'],
                'world_life_not_user_or_model_autocompleted':True,
                'not_proof_of_current_real_world_event':True,
                'not_actor_perception_memory_emotion_or_consent':True,
                'grade':GRADE})
        return {'status':'ADMITTED_SOURCEFREE_NOTICE_ONLY',
                'receipt':committed['id'],'cue_ref':cue['id'],
                'clock':world['clock'],'offer_id':proposal['offer_id'],
                'no_material_consequence_inferred':True,'grade':GRADE}

    def _actor_plan(self,actor_id,world,actors,requested_action=None,requesting_actor=None,requesting_action=None,*,_principal_projection=None):
        actor=actors[actor_id]
        # Internal same-stack, same-phase result from step's pre-event audit.
        # Public plan and the independent coactor planner always read afresh.
        if _principal_projection is None:
            c=materialize(actor,world);e=actor_access(actor,world);situated=asdict(compose(c,e))
        else:
            e,situated=_principal_projection
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
            private_options=(offer_private_rehearsals(actor,world['clock'],e.location,
                [o['action'] for o in options]) if requesting_actor is None else [])
            undertaking_options=(offer_undertaking_attention(actor,world,e,
                situated.get('attention_frame',{}).get('focally_eligible_cue_refs',[]))
                if requesting_actor is None and any(o['action']=='ORIENT' for o in options) else [])
            correspondence_options=(offer_correspondence_attention(actor,world,e)
                if requesting_actor is None and any(o['action']=='ORIENT' for o in options) else [])
            focal_options=(offer_focal_encounters(actor,e,
                situated.get('attention_frame',{}).get('focally_eligible_cue_refs',[]))
                if requesting_actor is None and any(o['action']=='ORIENT' for o in options) else [])
            proposed=self.semantic.proposal('actor_attempt',{'actor':{'id':actor_id,'role':actor['role'],
                'body':copy(actor['body'])},
                'accessible':{k:v for k,v in asdict(e).items() if k!='inaccessible_count'},
                'situated':situated,'options':options,
                'practical_options':flat_alternatives,
                'possible_end_trials':flat_trials,
                'private_rehearsal_options':copy(private_options),
                'undertaking_attention_options':copy(undertaking_options),
                **({'correspondence_attention_options':correspondence_options} if correspondence_options else {}),
                **({'focal_encounter_options':focal_options} if focal_options else {}),
                'possible_end_trial_does_not_establish_motive':True,
                'selected_option_is_not_conscious_intent':True,
                'requesting_actor':requesting_actor,'requesting_action':requesting_action})
            private_choice=None
            if 'private_rehearsal_id' in proposed or 'private_rehearsal_content' in proposed:
                rows=[o for o in private_options if o['rehearsal_id']==proposed.get('private_rehearsal_id')]
                content=proposed.get('private_rehearsal_content')
                if (len(rows)!=1 or proposed.get('action')!='WAIT'
                        or any(proposed.get(k) is not None for k in
                               ('project_id','project_ids','practical_option_id','possible_end_trial_id'))
                        or type(content) is not str or not content.strip() or len(content)>512):
                    raise ValueError('PRIVATE_REHEARSAL_UNISSUED_OR_CONFLICTING_SELECTION')
                private_choice={'option':copy(rows[0]),'imagined_content':content}
            undertaking_choice=None
            if 'undertaking_attention_id' in proposed:
                rows=[o for o in undertaking_options
                      if o['attention_id']==proposed.get('undertaking_attention_id')]
                if (len(rows)!=1 or proposed.get('action')!='ORIENT' or private_choice is not None
                        or any(proposed.get(k) is not None for k in
                               ('project_id','project_ids','practical_option_id','possible_end_trial_id'))):
                    raise ValueError('UNDERTAKING_ATTENTION_UNISSUED_OR_CONFLICTING')
                undertaking_choice=copy(rows[0])
            correspondence_choice=None
            if 'correspondence_attention_id' in proposed:
                rows=[o for o in correspondence_options
                      if o['attention_id']==proposed['correspondence_attention_id']]
                if (len(rows)!=1 or proposed.get('action')!='ORIENT'
                        or private_choice is not None or undertaking_choice is not None
                        or any(proposed.get(k) is not None for k in
                               ('project_id','project_ids','practical_option_id','possible_end_trial_id',
                                'notice_expectation_ref','defer_course_option_id','interactivity_relation_ref'))):
                    raise ValueError('CORRESPONDENCE_UNISSUED_OR_CONFLICTING_SELECTION')
                correspondence_choice=copy(rows[0])
            focal_choice=None
            if 'focal_encounter_id' in proposed:
                rows=[o for o in focal_options if o['attention_id']==proposed['focal_encounter_id']]
                if (len(rows)!=1 or proposed.get('action')!='ORIENT'
                        or private_choice is not None or undertaking_choice is not None
                        or correspondence_choice is not None
                        or any(proposed.get(k) is not None for k in
                               ('project_id','project_ids','practical_option_id','possible_end_trial_id',
                                'notice_expectation_ref','defer_course_option_id','interactivity_relation_ref'))):
                    raise ValueError('FOCAL_ENCOUNTER_UNISSUED_OR_CONFLICTING_SELECTION')
                focal_choice=copy(rows[0])
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
            notice_choice=None
            if 'notice_expectation_ref' in proposed:
                rows=[x for x in opt.get('fallible_notice_expectations',[])
                      if x['expectation_ref']==proposed.get('notice_expectation_ref')]
                if (len(rows)!=1 or requesting_actor is not None or private_choice is not None
                        or undertaking_choice is not None or trial_choice is not None):
                    raise ValueError('NOTICE_EXPECTATION_UNISSUED_SELECTION')
                notice_choice=copy(rows[0])
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
            if trial_choice is not None and trial_choice.get('selected_offer_option_ref') is not None:
                qualified=[a for a in alternatives
                    if a.get('option_id')==trial_choice['selected_offer_option_ref']
                    and a.get('binding_status')=='CURRENT_HELD_FOOD_OFFER_ACCEPTANCE'
                    and a.get('human_food_offer_ref')==trial_choice['selected_human_food_offer_ref']
                    and a['world_request']['addressed_party_ref']==trial_choice['offered_by_ref']]
                if len(qualified)!=1:
                    raise ValueError('POSSIBLE_END_TRIAL_OFFER_NO_LONGER_QUALIFIED')
                selected_alternative=qualified[0]
            if trial_choice is not None and trial_choice.get(
                    'source_material_object_ref') is not None:
                selected_alternative=_bind_actor_trial_particular_object(
                    alternatives,trial_choice)
            # A project-specific addressed means may not be selected via
            # generic or multi-project dispatch when its bound option was
            # absent from focal practical alternatives.
            conditional_projects=[p for p in actor.get('projects',[])
                if p['id'] in selected_refs and action in p.get('dependency_conditional_means',{})]
            if conditional_projects and (len(selected_refs)!=1 or selected_alternative is None
                    or not selected_alternative.get('dependency_conditional_means_ref')
                    or selected_alternative.get('project_id')!=conditional_projects[0]['id']):
                raise ValueError('DEPENDENCY_MEANS_REQUIRES_BOUND_PROJECT_OPTION')
            if selected_alternative and selected_alternative.get('binding_status')=='UNBOUND_PARTY_NOT_PRESENT':
                raise ValueError('ACTOR_SELECTED_UNAVAILABLE_ADDRESSED_PARTY')
            # The selected object-specific project may not silently fall
            # back to a generic site operation, even in a multi-course act.
            object_courses=[p for p in actor.get('projects',[])
                            if p['id'] in selected_refs
                            and p.get('incidental_takeup_basis') is not None]
            if object_courses and (len(selected_refs)!=1
                    or not selected_alternative
                    or selected_alternative.get('project_id')!=object_courses[0]['id']
                    or selected_alternative['world_request'].get('material_object_ref')!=object_courses[0]['material_object_ref']):
                raise ValueError('INCIDENTAL_PROJECT_EXACT_OBJECT_SELECTION_REQUIRED')
            conditional_courses=[p for p in actor.get('projects',[])
                if p['id'] in selected_refs and action in p.get('dependency_conditional_means',{})]
            if conditional_courses and (len(selected_refs)!=1
                    or not selected_alternative
                    or selected_alternative.get('project_id')!=conditional_courses[0]['id']
                    or selected_alternative.get('dependency_conditional_means_ref')!=
                       conditional_courses[0]['dependency_conditional_means'][action]['origin_event_ref']
                    or selected_alternative['world_request'].get('addressed_party_ref')!=
                       conditional_courses[0]['dependency_conditional_means'][action]['counterpart_ref']):
                raise ValueError('DEPENDENCY_PROJECT_EXACT_CONDITIONAL_MEANS_REQUIRED')
            witness_courses=[p for p in actor.get('projects',[])
                if p['id'] in selected_refs and action=='ORIENT' and p.get('productive_witness_means')]
            if witness_courses and (len(selected_refs)!=1 or option_id is None
                    or not selected_alternative or not selected_alternative.get('productive_witness_attention')
                    or selected_alternative.get('project_id')!=witness_courses[0]['id']
                    or private_choice is not None or undertaking_choice is not None):
                raise ValueError('PRODUCTIVE_WITNESS_EXACT_RECEPTIVE_OPTION_REQUIRED')
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
            if trial_choice is not None and trial_choice.get(
                    'source_qualified_addressee_ref') is not None:
                end_target=trial_choice['source_qualified_addressee_ref']
                if (bound_target not in (None,end_target)
                        or action not in COOPERATIVE):
                    raise ValueError('GENETIC_TRIAL_ADDRESSEE_NOT_BINDABLE')
                if not any(c.get('kind')=='coactor_present'
                       and c.get('source_actor')==end_target
                       for c in e.cues):
                    raise ValueError('GENETIC_TRIAL_OTHER_NOT_PRESENT')
                bound_target=end_target
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
                       # Preserve per-purpose identity, not an unlabelled
                       # bag of projected anticipated differences. This bounded
                       # multi-course entrance is only for unaddressed,
                       # object-unbound alternatives sharing the same act.
                       'selected_expectation_courses':([
                           {'project_id':pid,'option_id':matches[0]['option_id'],
                            'anticipated_difference':copy(matches[0]['anticipated_difference'])}
                           for pid in selected_refs
                           for matches in [[a for a in alternatives
                               if a.get('project_id')==pid
                               and a.get('grounds_status')=='AVAILABLE_SINGLE_PROJECT_COURSE'
                               and a.get('binding_status')=='NO_ADDRESSED_PARTY'
                               and a.get('world_request',{}).get('material_object_ref') is None]]
                           if len(matches)==1 and matches[0].get('anticipated_difference') is not None]
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
            if (selected_alternative and selected_alternative.get('human_food_offer_ref')
                    and (proposed.get('practical_option_id')==selected_alternative['option_id']
                         or (trial_choice is not None and trial_choice.get('selected_offer_option_ref')==selected_alternative['option_id']))):
                practical['selected_human_food_offer_ref']=selected_alternative['human_food_offer_ref']
            if 'defer_course_option_id' in proposed:
                if (len(selected_refs)!=1 or requesting_actor is not None or trial_choice is not None
                        or private_choice is not None or undertaking_choice is not None):
                    raise ValueError('INTERACTIVITY_CONFLICTING_SELECTION')
                practical['interactivity_deferral']=qualify_interactivity_deferral(
                    flat_alternatives,selected_alternative,proposed['defer_course_option_id'],e.location)
            if selected_alternative and selected_alternative.get('productive_witness_attention'):
                practical['productive_witness_attention']=copy(selected_alternative['productive_witness_attention'])
            if 'interactivity_relation_ref' in proposed:
                rows=[x for x in (selected_alternative or {}).get('interactivity_currents',[])
                      if x['relation_ref']==proposed['interactivity_relation_ref']]
                if len(rows)!=1 or len(selected_refs)!=1:
                    raise ValueError('INTERACTIVITY_UNISSUED_RELATION')
                practical['interactivity_relation_analytic_only']=copy(rows[0])
            if selected_alternative and selected_alternative.get('course_historical_currents'):
                practical['course_historical_currents_analytic_only']=copy(
                    selected_alternative['course_historical_currents'])
            # Retain the exact private affective alternatives offered, not a
            # causal assertion about which affect actually decided the attempt.
            affect_courses=[{'project_id':a['project_id'],'option_id':a['option_id'],
                             'affects':copy(a['course_affective_organizations'])}
                            for a in alternatives if a.get('project_id') in selected_refs
                            and a.get('course_affective_organizations')]
            if affect_courses:
                practical['selected_course_affects_analytic_only']=affect_courses
            if notice_choice is not None:
                practical['notice_expectation']=notice_choice
            if private_choice is not None:
                practical['private_rehearsal']=private_choice
            if undertaking_choice is not None:
                practical['undertaking_attention']=undertaking_choice
            if correspondence_choice is not None:
                practical['correspondence_attention']=correspondence_choice
            if focal_choice is not None:
                practical['focal_encounter']=focal_choice
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
        principal_projection=None
        for aid,person in actors.items():
            constitution=materialize(person,world)
            encounter=actor_access(person,world)
            prior=asdict(compose(constitution,encounter))
            if aid==actor_id:
                # All audit fields below are independently copied. No world
                # or actor write, semantic call or phase transition intervenes.
                principal_projection=(encounter,prior)
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
        principal=self._actor_plan(actor_id,world,actors,requested_action,
                                   _principal_projection=principal_projection)[0]
        # No cross-phase, cross-beat or persisted projection cache.
        del principal_projection
        if principal.practical_selection.get('productive_witness_attention') is not None and (target is not None or object_ref is not None):
            raise ValueError('PRODUCTIVE_WITNESS_CANNOT_BE_EXTERNALLY_ADDRESSED')
        if principal.practical_selection.get('correspondence_attention') is not None and (target is not None or object_ref is not None):
            raise ValueError('CORRESPONDENCE_CANNOT_BE_EXTERNALLY_ADDRESSED')
        if principal.practical_selection.get('undertaking_attention') is not None and (target is not None or object_ref is not None):
            raise ValueError('UNDERTAKING_ATTENTION_CANNOT_BE_EXTERNALLY_ADDRESSED')
        if principal.practical_selection.get('focal_encounter') is not None and (target is not None or object_ref is not None):
            raise ValueError('FOCAL_ENCOUNTER_CANNOT_BE_EXTERNALLY_ADDRESSED')
        if principal.practical_selection.get('private_rehearsal') is not None and (target is not None or object_ref is not None):
            raise ValueError('PRIVATE_REHEARSAL_CANNOT_BE_EXTERNALLY_ADDRESSED')
        if target is not None and principal.target not in (None,target):
            raise ValueError('CALLER_TARGET_CONFLICTS_WITH_ACTOR_PRACTICAL_ALTERNATIVE')
        if target is not None:principal.target=target
        if object_ref is not None and principal.object_ref not in (None,object_ref):
            raise ValueError('CALLER_OBJECT_CONFLICTS_WITH_ACTOR_SELECTION')
        if object_ref is not None:principal.object_ref=object_ref
        # A caller never supplies another actor's response. The world owner
        # obtains it from the installed independently constituted actor policy.
        human_vocal = None
        if (principal.action in ('SING','SIGNAL','REFUSE') and principal.target in
                world.get('neighbor_users', {}) and requested_action is None):
            history = self.ledger.events()
            human_vocal = qualified_human_vocal_receipt(
                world, actors[actor_id], principal, history[-1] if history else None)
        if human_vocal is None:
            actual,partner,coactor_policy_receipt=self.authority.resolve(world,actors,principal)
        else:
            actual,partner,coactor_policy_receipt=self.authority.resolve(
                world,actors,principal,committed_human_event=history[-1])
        resolved=asdict(actual)
        summary=resolved['world_delta']['event']
        primary_cue_ref=world['cues'][-1]['id']
        correspondence_cue=None
        chosen_correspondence=principal.practical_selection.get('correspondence_attention')
        if chosen_correspondence is not None and summary['status']=='PERFORMED':
            correspondence_cue=settle_correspondence_attention(
                world,actors[actor_id],chosen_correspondence,summary)
            # Keep the primary public sign last for existing MII readers.
            private_cue=world['cues'].pop()
            world['cues'].insert(len(world['cues'])-1,private_cue)
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
                           if x['id']==primary_cue_ref or (correspondence_cue is not None
                               and aid==actor_id and x['id']==correspondence_cue['id'])]
            if participated:
                # The presently co-situated other can be sensed without
                # revealing their motives or private biography. The earlier
                # projection omitted this mundane evidence even from actors
                # whose living encounter just occurred in the same room.
                # Retain no cue whose sensory eligibility actor_access denied.
                personal_cues += [x for x in access.cues
                    if x.get('kind')=='coactor_present'
                    and x.get('source_actor')!=aid]
            # A deliberately selected, source-checked prior sign can have
            # been received during this orienting interval even if its
            # transient world cue expired at settlement. Never retain it
            # for a passive observer, an injected ORIENT or an unsuccessful act.
            if (aid==actor_id and requested_action is None and personally_done
                    and personally_done['action']=='ORIENT' and personally_done['status']=='PERFORMED'):
                chosen=principal.practical_selection.get('undertaking_attention')
                if chosen is not None:
                    cue=copy(chosen['outward_sign'])
                    if not any(c['id']==cue['id'] for c in personal_cues):
                        personal_cues.append(cue)
            if (aid==actor_id and requested_action is None and personally_done
                    and personally_done['action']=='ORIENT' and personally_done['status']=='PERFORMED'):
                chosen=principal.practical_selection.get('productive_witness_attention')
                if chosen is not None:
                    cue=copy(chosen['outward_sign'])
                    if not any(c['id']==cue['id'] for c in personal_cues):
                        personal_cues.append(cue)
            if (aid==actor_id and requested_action is None and personally_done
                    and personally_done['action']=='ORIENT' and personally_done['status']=='PERFORMED'):
                chosen=principal.practical_selection.get('focal_encounter')
                if chosen is not None:
                    cue=copy(chosen['outward_sign'])
                    if not any(c['id']==cue['id'] for c in personal_cues):
                        personal_cues.append(cue)
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
            if (aid == actor_id and personally_done and human_vocal is not None
                    and (summary.get('human_vocal_event_ref') or
                         summary.get('human_food_offer_event_ref') or
                         summary.get('human_food_offer_refused_event_ref')) == human_vocal['user_event_ref']
                    and personally_done['status'] == 'PERFORMED'):
                # The human act was personally accessible immediately before
                # the actor's own settlement, not an omniscient reconstruction.
                personal_cues.append(copy(human_vocal['cue']))
                if summary.get('outcome')=='JOINT_ACTIVITY_PERFORMED':
                    reciprocal = human_vocal['visitor_ref']
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
                        # Frozen only if the actor independently selected the
                        # operation. Research-forced action is not proof that
                        # the person sought that particular object.
                        'own_practical_selection':(
                            copy(actor_attempt.practical_selection)
                            if personally_done and actor_attempt is not None
                            and (aid!=actor_id or requested_action is None)
                            else None),
                        'actor_access_grade':GRADE}
            # Read the actual material owner receipt, not the model's account
            # of its own expertise. The actor need not know this causal source.
            if own=='REPAIR' and experience['own_practical_selection'] is not None:
                obj=summary.get('worked_material_object_ref')
                history=world.get('material_objects',{}).get(obj,{}).get('objective_labor_history',[])
                if history:
                    labor=history[-1]
                    if (labor.get('actor')==aid and labor.get('operation')=='REPAIR'
                            and labor.get('clock')==world['clock']
                            and labor.get('acquired_component_technique_ref')):
                        experience['performed_repair_technique_ref_analytic_only']=labor['acquired_component_technique_ref']
            attention_receipt=received_undertaking_attention(
                actors[aid],experience.get('own_practical_selection'),experience)
            if attention_receipt:
                experience['undertaking_attention_receipt']=attention_receipt
            correspondence_receipt=received_correspondence_attention(
                actors[aid],experience.get('own_practical_selection'),experience)
            if correspondence_receipt:
                experience['correspondence_attention_receipt']=correspondence_receipt
            focal_receipt=received_focal_encounter(
                actors[aid],experience.get('own_practical_selection'),experience)
            if focal_receipt:
                experience['focal_encounter_receipt']=focal_receipt
            directed_receipt=personally_received_directed_act(experience)
            subjective[aid]=copy(experience)
            if personally_done and actor_attempt is not None:
                # Anticipation is formed at the time of this actor's attempt,
                # distinct from how the world actually settled it. It can
                # remain pending after the objective event has committed.
                start_selected_expectations(actors[aid],actor_attempt.practical_selection,
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
                **({'interactivity_deferral':copy(experience['own_practical_selection']['interactivity_deferral'])}
                   if (experience.get('own_practical_selection') or {}).get('interactivity_deferral') else {}),
                **({'undertaking_attention':copy(attention_receipt)} if attention_receipt else {}),
                **({'correspondence_attention':copy(correspondence_receipt)} if correspondence_receipt else {}),
                **({'focal_encounter':copy(focal_receipt)} if focal_receipt else {}),
                **({'directed_encounter':copy(directed_receipt)} if directed_receipt else {}),
                **({'notice_expectation':copy(experience['own_practical_selection']['notice_expectation'])}
                   if (experience.get('own_practical_selection') or {}).get('notice_expectation') else {}),
                **({'own_vocal_reception':own_vocal_reception(actors[aid],experience)}
                   if own_vocal_reception(actors[aid],experience) is not None else {}),
                'received_cue_refs':[c['id'] for c in personal_cues],
                'received_cue_tags':sorted({str(tag).lower()
                    for cue in personal_cues for tag in cue.get('tags',[])}),
                'not_a_counterfactual_comparison':True,
                'unencountered_alternatives':'UNKNOWN_NOT_OBSERVED',
                'grade':GRADE})
            # Actor-owned practical afterlife is separate from world objective
            # outcome. It can later be recruited, but is not motive fulfillment.
            register_lived_activity_attempt(actors[aid],experience,activity_effects.get(aid,[]))
            conserve_lived_episode(
                actors[aid],experience,objective_ref,
                bodily_before[aid],actors[aid]['body'],
                source_selection=(
                    actor_attempt.intention if personally_done and
                    actor_attempt is not None else None))
            possible_genetic_end=possible_contrast_end(
                actors[aid],experience,objective_ref)
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
            possible_joint_practice_genesis=possible_joint_practice(
                actors[aid],experience,objective_ref)
            if personally_done and actor_attempt is not None:
                conserve_costly_offered_care(
                    actors[aid],experience,objective_ref,actor_attempt,
                    summary,bodily_before[aid],actors[aid]['body'])
            possible_care_practice=candidate_care_commitment(
                actors[aid],experience,objective_ref)
            # A person can later seek to repeat an actually exercised
            # operation or attempt to practice a formerly joint activity.
            # The source-free rule does NOT confer independent technical
            # mastery or external access rights.
            retain_exercised_power(
                actors[aid],experience,objective_ref,
                world['positions'].get(aid,actors[aid]['location']))
            retain_personal_notice_exposure(actors[aid],experience,objective_ref)
            retain_personal_object_encounter(actors[aid],experience,objective_ref)
            # A public real speaker's demonstration can enter the listener's
            # own history even when the listener did not perform the SPEAK.
            # The sign and actual object must both be personally accessible;
            # no word, education, agreement or teaching intention is inferred.
            conserve_personally_heard_reference(
                actors[aid],experience,objective_ref,world)
            cultural_reference_candidates=possible_cultural_object_inquiry(
                actors[aid],experience,objective_ref)
            cultural_revision_candidates=possible_reference_revision(
                actors[aid],experience,objective_ref)
            conserve_reciprocated_vocal_turn(
                actors[aid],experience,objective_ref)
            vocal_development_candidates=possible_vocal_coordination(
                actors[aid],experience,objective_ref)
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
            # Two *distinct* actor-lived material-public practices may give
            # a model a possible contrast, never a mandatory lesson about
            # the legitimacy of an institution, worker or authority figure.
            institutional_differences=possible_lived_institutional_differences(
                actors[aid],experience,objective_ref)
            # A later personally attempted WORK event can now give a model
            # access to a qualified recurring history of this actor's own
            # material activity. The model may propose no organization at all.
            # Future pre-cue recruitment belongs to the existing R19 owner.
            recurrent_work=possible_recurrent_work_orientation(
                actors[aid],experience,objective_ref)
            # R28 MULCH: the actor's OWN repeated bodily courses can now
            # qualify a directional historical orientation before a model
            # proposes its meaning. Neither a felt cost nor relief proves
            # action causation; a single episode or mixed history gives NONE.
            # This proposal feeds EXISTING R19 acquisition and pre-cue routing.
            lived_directional_orientation=possible_lived_directional_orientation(
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
            private_rehearsal=(perform_private_rehearsal(actors[aid],experience,objective_ref,
                actor_attempt.practical_selection,bodily_before[aid])
                if personally_done and actor_attempt is not None else None)
            proposal=self.semantic.proposal('development',{'actor':{'id':aid,'role':actors[aid]['role'],
                'body':copy(actors[aid]['body']),'location':actors[aid]['location']},
                'clock':world['clock'],'experience':experience,
                'selected_constitution':selected,
                'actor_forms':copy(actors[aid]['forms']),
                'actual_private_rehearsal_analyst_only':copy(private_rehearsal),
                'actual_undertaking_attention_analyst_only':copy(attention_receipt),
                **({'historically_possible_focal_encounter_memory': {
                        'kind':'MEMORY','focal_encounter_ref':focal_receipt['attention_id'],
                        'content_requires_actor_local_semantic_proposal':True}}
                   if focal_receipt else {}),
                **({'actual_correspondence_attention_analyst_only':copy(correspondence_receipt)} if correspondence_receipt else {}),
                **({'historically_possible_memory_access_decreases':memory_access_candidates}
                   if (memory_access_candidates:=possible_practice_memory_access_decrease(
                       actors[aid],experience,objective_ref)) else {}),
                'historically_possible_repair_techniques':copy(
                    possible_repair_technique(actors[aid],experience,objective_ref)),
                'actor_historical_orientations_analyst_only':copy(
                    actors[aid].get('historical_orientations',[])),
                'actor_self_model_analyst_only':copy(
                    actors[aid].get('self_model',{})),
                # Untried possible ends are actor-history hypotheses, not
                # automatically functioning motives or public self-knowledge.
                'actor_possible_ends':copy(actors[aid].get('possible_ends',[])),
                'historically_possible_genetic_ends':copy(possible_genetic_end),
                'historically_possible_productive_vocal_takeups':copy(
                    possible_productive_vocal_takeups(actors[aid],experience,objective_ref)),
                'historically_possible_dependency_takeups':copy(
                    possible_dependency_project_takeups(actors[aid],experience,objective_ref)),
                'historically_possible_productive_witness_reorganizations':copy(
                    possible_productive_witness_reorganizations(actors[aid],experience,objective_ref)),
                'historically_possible_dependency_project_reorganizations':copy(
                    possible_dependency_project_reorganizations(actors[aid],experience,objective_ref)),
                'historically_possible_dependency_means_revisions':copy(
                    possible_dependency_means_revisions(actors[aid],experience,objective_ref)),
                'historically_possible_dependency_ambivalence':copy(
                    possible_dependency_ambivalence(actors[aid],experience,objective_ref)),
                'historically_possible_joint_practices':copy(
                    possible_joint_practice_genesis),
                'historically_possible_care_practices':copy(
                    possible_care_practice),
                'historically_possible_cultural_references':copy(
                    cultural_reference_candidates),
                'historically_possible_cultural_revisions':copy(
                    cultural_revision_candidates),
                'historically_possible_social_vocal_development':copy(
                    vocal_development_candidates),
                'actor_personally_practiced_vocal_turns_analyst_only':copy(
                    actors[aid].get('vocal_turn_experiences',[])[-12:]),
                'actor_personally_heard_cultural_demonstrations_analyst_only':copy(
                    actors[aid].get('cultural_demonstrations',[])[-16:]),
                'actor_acquired_cultural_references_analyst_only':copy(
                    actors[aid].get('cultural_reference_practices',[])[-16:]),
                'recent_personally_lived_genesis_witnesses_analyst_only':copy(
                    actors[aid].get('lived_genesis_episodes',[])[-8:]),
                'actor_expectations_analyst_only':copy(actors[aid].get('expectations',[])),
                'historically_proposed_preproject':copy(history_genesis),
                'historically_proposed_functional':copy(functional_genesis),
                'historically_possible_functional_revisions':copy(
                    possible_functional_revisions(actors[aid],experience,objective_ref)),
                'historically_possible_material_meanings':copy(
                    material_meaning_proposals),
                'historically_possible_incidental_goods':copy(
                    possible_incidental_goods),
                'historically_possible_incidental_takeup':[
                    q for end in actors[aid].get('possible_ends',[])
                    if end.get('status')=='POSSIBLE_NOT_ACQUIRED_MOTIVE'
                    for q in [qualify_incidental_object_takeup(
                        actors[aid],experience,objective_ref,end)] if q is not None],
                'historically_possible_delayed_appraisals':copy(
                    delayed_expectation_appraisals),
                'historically_possible_expressive_practices':copy(
                    possible_expressive_practices(actors[aid],experience,objective_ref)),
                'historically_possible_interactivity_relations':copy(
                    possible_interactivity_relations(actors[aid],experience,objective_ref)),
                'historically_possible_activity_affects':copy(
                    possible_activity_affects(actors[aid],experience,objective_ref)),
                'historically_possible_co_regulation':copy(care_genesis),
                'historically_possible_plural_care':copy(plural_care_genesis),
                'historically_possible_reopened_care':copy(
                    renewed_relational_possibility),
                'actual_lived_high_resolution_care_ref':(
                    actual_lived_care['id'] if actual_lived_care else None),
                'historically_possible_co_regulation_revision':copy(
                    care_revision),
                'historically_possible_notice_expectations':copy(
                    possible_notice_expectations(actors[aid],experience,objective_ref)),
                'historically_possible_notice_revisions':copy(
                    possible_notice_revisions(actors[aid],experience,objective_ref)),
                'historically_possible_public_procedure_learning':copy(
                    institutional_learning),
                'historically_possible_institutional_relational_differences':copy(
                    institutional_differences),
                # A third person's actually witnessed treatment of another
                # may challenge this actor's inherited loyalty/identification.
                # This is an actor-local, optional semantic occasion, never
                # direct access to anyone else's private psyche.
                'historically_possible_witnessed_third_party_relations':copy(
                    possible_witnessed_third_party_relation(
                        actors[aid],experience)),
                'historically_possible_recurrent_livelihood_orientation':copy(
                    recurrent_work),
                'historically_possible_lived_directional_orientation':copy(
                    lived_directional_orientation),
                'historically_possible_counterhistory_release':copy(
                    possible_counterhistory_release(actors[aid],experience,objective_ref)),
                'historically_possible_monitoring_changes':copy(
                    possible_monitoring_changes(actors[aid],experience,objective_ref)),
                'historically_possible_lived_cross_context_revaluations':copy(
                    possible_lived_cross_context_revaluations(
                        actors[aid],experience,objective_ref)),
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
            issued_trial=None
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
                                    developmental_candidates,
                                    issued_trial=issued_trial)
        observed=subjective.get(actor_id,{})
        # A privileged world audit outcome is NOT automatically what this
        # person saw or can disclose. The event's public sign is deliberately
        # less informative than the real objective financial/material reason.
        public_sign=next((cue.get('description','EVENT_PERCEIVED') for cue in
                         observed.get('perceived_cues',[]) if cue.get('kind','').startswith('performed_')),
                         'UNKNOWN_TO_ACTOR')
        actual_tip={'action':principal.action,'outcome':public_sign,
                    'status':summary['status']}
        expression_access=copy(observed)
        expression_access.pop('performed_repair_technique_ref_analytic_only',None)
        if expression_access.get('own_practical_selection'):
            expression_access['own_practical_selection'].pop('private_rehearsal',None)
            expression_access['own_practical_selection'].pop('undertaking_attention',None)
            expression_access['own_practical_selection'].pop('focal_encounter',None)
            expression_access['own_practical_selection'].pop('productive_witness_attention',None)
            expression_access['own_practical_selection'].pop('notice_expectation',None)
            expression_access['own_practical_selection'].pop('interactivity_deferral',None)
            expression_access['own_practical_selection'].pop('interactivity_relation_analytic_only',None)
            expression_access['own_practical_selection'].pop('selected_course_affects_analytic_only',None)
            expression_access['own_practical_selection'].pop('course_historical_currents_analytic_only',None)
        expression_access.pop('undertaking_attention_receipt',None)
        expression_access.pop('focal_encounter_receipt',None)
        if correspondence_cue is not None:
            expression_access.pop('correspondence_attention_receipt',None)
            expression_access.get('own_practical_selection',{}).pop('correspondence_attention',None)
            expression_access['perceived_cues']=[c for c in expression_access.get('perceived_cues',[])
                if c.get('kind')!='opened_correspondence']
        expression=self.semantic.proposal('expression',{'actor_id':actor_id,'actual':actual_tip,
               'actor_accessible':expression_access,
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
                 'model_service_grade':getattr(
                     getattr(self.semantic,'provider',self.semantic),
                     'grade','UNSPECIFIED_SEMANTIC_ADAPTER_NO_PROVEN_GRADE'),
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

    def advance_to_discontinuity(self,horizon=30,processes=None):
        """Cover ordinary time only to the next real material interruption.

        A due commitment lets its owner initiate an independently selected
        response; no caller script forces fulfillment or another's consent.
        """
        return continue_to_discontinuity(self,horizon,processes=processes)

    def construct_pre_encounter_history(self,subject_id, target_age_days, *,
                                        horizon_days=365, autonomous_beats=2,
                                        max_segments=240, period_processes=None):
        """Run sourcefree historical becoming before any user-person meeting.

        Reuse background(), advance_to_discontinuity(), autonomous actor
        planning and the same persistent world. This is not a user-facing
        scene, parent-child gameplay, or a matured-adult-person generator.
        """
        return continue_pre_encounter(
            self, subject_id, target_age_days,
            horizon_days=horizon_days,
            autonomous_beats=autonomous_beats, max_segments=max_segments,
            period_processes=period_processes)

    def register_sourcefree_recursive_encounter_paths(self,spec):
        """Explicit finite material conditions, not actor perception or consent.

        Use the existing ledger and world owner. No NEIGHBOR visitor is
        created, and no developmental record is manufactured by registration.
        """
        version,world=self.ledger.world(self.world_id)
        source=register_recursive_encounter_paths(
            world,self.ledger.actors(),spec)
        receipt=self.ledger.commit(
            self.world_id,version,world,{}, {},
            'SOURCEFREE_RECURSIVE_ENCOUNTER_PATHS',None,{
                'source':source,'world_only_not_actor_experience':True,
                'no_automatic_perception_or_psychic_change':True,'grade':GRADE})
        return {'receipt':receipt['id'],**source}

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

    def blind_interview_evidenced(self,actor_id,question_contract):
        """No respondent answer keys; ungrounded model proposals are refused.

        The qualified PYAT instrument and blind success court are still
        separate source/owner obligations, not inferred from this interface.
        """
        from .blind_parent_probes import blind_operational_interview
        _,world=self.ledger.world(self.world_id)
        _,actor=self.ledger.actor(actor_id)
        return blind_operational_interview(
            actor,question_contract,self.semantic,world)

    def verify(self):return self.ledger.verify_chain()
    def close(self):self.ledger.close()
