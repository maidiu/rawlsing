"""Research-only psychological afterlife: typed *fictional* formation and rewiring.

This is not CAN/ADP native authority. Every admitted form is actor-specific, bound
by actual experienced event, scoped, graded, and revisable. No LLM may edit an
objective world fact or another actor's state here.
"""
from .types import stable_id, copy, GRADE
from .psychodynamics import validate_tendencies
from .relational_metabolism import (
    RELATIONS, link_ref, validate_motif, admit_motif, InvalidRelationalMotif,
    qualify_lived_cross_context_revaluation,
)
from .organism import ACTIONS
from .practical_difference import validate_expected_difference, appraise_expected_difference
from .expectation_afterlife import admit_activity_affect, admit_expressive_practice
from .preproject_agency import admit_preproject_anticipation, revise_preproject_anticipation
from .reflective_regulation import acquire_reflective_regulation, admit_private_possible_end, private_end_ground
from .attention_field import received_undertaking_attention
from .practical_powers import admit_repair_technique
from .historical_self_organization import (
    acquire_orientation, revise_orientation, acquire_operative_self,
    revise_operative_self, admit_lived_directional_orientation)
from .psychic_genesis import admit_contrast_end, possible_dependency_project_takeups
from .activity import (possible_dependency_project_reorganizations,
                       possible_dependency_means_revisions)
from .joint_practice_genesis import admit_joint_practice
from .care_commitment_genesis import admit_care_commitment
from .cultural_mediation import (
    admit_cultural_reference,admit_reference_revision)
from .social_vocal_development import admit_vocal_coordination
from .prospective_horizon import record_possible_end_trial
from .unintended_goods import possible_unintended_goods, qualify_incidental_object_takeup
from .functional_correspondence import (admit_functional_correspondence,
                                         admit_functional_revision)
from .material_investments import admit_material_investment
from .co_regulation_history import (
    admit_co_regulation, admit_co_regulation_revision)
from .plural_care_paths import admit_reopening
from .institutional_procedure_learning import (
    admit_public_procedure_expectation, admit_notice_expectation, admit_notice_revision,
    qualify_lived_institutional_difference,
)
import math

class InvalidDevelopment(ValueError): pass


def _text_list(value,error):
    if not isinstance(value,list) or any(not isinstance(x,str) for x in value):
        raise InvalidDevelopment(error)
    return value

ALLOWED={'ADD_FORM','LINK_FORMS','DIFFERENTIATE','CHANGE_RECRUITMENT_SCOPE',
         'CHANGE_STRENGTH','SET_DORMANT','REACTIVATE','REORGANIZE_PROJECT',
         'TRACE','MEMORY','ACTOR_SELF_MODEL','ADD_PROJECT','CHANGE_OTHER_MODEL','LINK_ACTIVITY',
         'ACQUIRE_COMPOSITION_METHOD','ACQUIRE_RELATIONAL_MOTIF',
         'REVALUE_RELATION','REORGANIZE_RELATIONAL_MOTIF',
         'NOTICE_POSSIBLE_END','NOTICE_PRIVATE_POSSIBLE_END','TAKE_UP_POSSIBLE_END',
         'APPRAISE_EXPECTED_DIFFERENCE','ACQUIRE_ACTIVITY_AFFECT','ACQUIRE_EXPRESSIVE_PRACTICE','ACQUIRE_PREPROJECT_ANTICIPATION',
         'REVISE_PREPROJECT_ANTICIPATION','ACQUIRE_REFLECTIVE_REGULATION',
         'RECORD_POSSIBLE_END_TRIAL','ACQUIRE_FUNCTIONAL_CORRESPONDENCE',
         'REVISE_FUNCTIONAL_CORRESPONDENCE',
         'INVEST_MATERIAL_OBJECT','ACQUIRE_CO_REGULATION_ORIENTATION',
         'REVISE_CO_REGULATION_ORIENTATION',
         'ACQUIRE_HISTORICAL_ORIENTATION','ACQUIRE_LIVED_DIRECTIONAL_ORIENTATION',
         'REVISE_HISTORICAL_ORIENTATION',
         'REVISE_OPERATIVE_SELF_ORGANIZATION',
         'REOPEN_CO_REGULATION_ORIENTATION',
         'ACQUIRE_SITUATED_PUBLIC_PROCEDURE_EXPECTATION',
         'ACQUIRE_NOTICE_EXPECTATION','REVISE_NOTICE_EXPECTATION',
         'ACQUIRE_GENETIC_POSSIBLE_END',
         'ACQUIRE_CONDITIONAL_JOINT_PRACTICE',
         'ACQUIRE_COSTLY_CARE_PRACTICE',
         'ACQUIRE_SITUATED_CULTURAL_REFERENCE',
         'REVISE_SITUATED_CULTURAL_REFERENCE',
         'ACQUIRE_SOCIAL_VOCAL_COORDINATION','ACQUIRE_REPAIR_TECHNIQUE','NO_CHANGE'}
KINDS={'MEDIATOR','TENSION','PRACTICE','EXPECTATION','DISCRIMINATION','RELATIONAL_INVESTMENT'}
# The typed historic PRE-A0 relational family is supplied by the
# owner-adjacent sourcefree relational read, not redefined locally.


def validate_activity_priority(value):
    # Project importance is deliberately NOT capped at 1: existing acquired
    # purposes may have intense salience. It must, however, be a finite,
    # nonnegative number or it corrupts situated ranking and possibility.
    if (isinstance(value,bool) or not isinstance(value,(int,float)) or
            not math.isfinite(value) or value<0):
        raise InvalidDevelopment('INVALID_ACTIVITY_PRIORITY')
    return value


def admit(actor,experience,event_ref,candidates,*,issued_trial=None):
    """Atomic actor-owned admission; an issued trial cannot become its own motive.

    Preserve R3's one actual trial recorder and R13/R18's separate issuer
    and durable-project protections. A semantic candidate is never a ticket.
    """
    if type(candidates) is not list or any(type(c) is not dict for c in candidates):
        raise InvalidDevelopment('INVALID_DEVELOPMENT_CANDIDATES')
    records=[c for c in candidates if c.get('kind')=='RECORD_POSSIBLE_END_TRIAL']
    if records and (issued_trial is None or len(records)!=1
                    or records[0].get('trial')!=issued_trial):
        raise InvalidDevelopment('UNISSUED_POSSIBLE_END_TRIAL')

    if issued_trial is not None:
        if (type(issued_trial) is not dict
                or issued_trial.get('actor')!=actor.get('id')):
            raise InvalidDevelopment('CURRENT_TRIAL_ISSUER_ACTOR_MISMATCH')
        # An issued exploratory operation cannot mature into a declared
        # enduring project through a synonymous generic ADD_PROJECT.
        if any(c.get('kind')=='ADD_PROJECT' for c in candidates):
            raise InvalidDevelopment('CURRENT_TRIAL_CANNOT_ACQUIRE_DURABLE_PROJECT')
        if any(c.get('kind')=='REORGANIZE_PROJECT' for c in candidates):
            raise InvalidDevelopment('CURRENT_TRIAL_CANNOT_REORGANIZE_DURABLE_PROJECT')
        if any(c.get('kind')=='TAKE_UP_POSSIBLE_END' for c in candidates):
            raise InvalidDevelopment('CURRENT_TRIAL_NOT_MATURE_MOTIVE')
        # The two inherited ticket identities are both real historical
        # issuers: R13 used "end"; R3's prospective horizon uses
        # "possible_end" plus an optional functional bridge. Keep the
        # exact grammars, not arbitrary model-rehashed ticket strings.
        identity={'actor':actor['id'],
                  'clock':issued_trial.get('as_of_clock'),
                  'operation':issued_trial.get('operation')}
        valid_ids={
            stable_id('end_trial', {**identity,
                'end':issued_trial.get('possible_end_ref')}),
            stable_id('end_trial', {**identity,
                'possible_end':issued_trial.get('possible_end_ref'),
                'functional_bridge':issued_trial.get('functional_bridge_ref')}),
        }
        if issued_trial.get('selected_offer_option_ref') is not None:
            selected=experience.get('own_practical_selection') or {}
            offer=issued_trial.get('selected_human_food_offer_ref')
            option=issued_trial['selected_offer_option_ref']
            other=issued_trial.get('offered_by_ref')
            if (issued_trial.get('operation')!='SIGNAL'
                    or any(type(x) is not str or not x for x in (offer,option,other))
                    or selected.get('option_id')!=option
                    or selected.get('selected_human_food_offer_ref')!=offer
                    or selected.get('world_request',{}).get('addressed_party_ref')!=other):
                raise InvalidDevelopment('UNISSUED_POSSIBLE_END_OFFER_TRIAL')
            base=stable_id('end_trial',{**identity,
                'possible_end':issued_trial.get('possible_end_ref'),
                'functional_bridge':issued_trial.get('functional_bridge_ref')})
            valid_ids={stable_id('end_trial_actual_offer',{
                'trial':base,'option':option,'offer':offer})}
        if (type(issued_trial.get('trial_id')) is not str
                or issued_trial['trial_id'] not in valid_ids):
            raise InvalidDevelopment('UNISSUED_POSSIBLE_END_TRIAL')
        # A physical event can be tried for at most one possible end;
        # copying it into a different end's history cannot multiply lives.
        if any(t.get('event_ref')==event_ref
               for end in actor.get('possible_ends',[])
               for t in end.get('trial_history',[]) if type(t) is dict):
            raise InvalidDevelopment('POSSIBLE_END_TRIAL_EVENT_ALREADY_CONSUMED')
        if not records:
            # A genuine sourcefree direct issuer call still records a trial;
            # runtime's explicit inserted R3 record is accepted only if it
            # matches the frozen ticket. Never record it twice.
            candidates=[{'kind':'RECORD_POSSIBLE_END_TRIAL',
                         'trial':copy(issued_trial)}]+candidates
    candidate_actor=copy(actor)
    result=_admit_in_place(candidate_actor,experience,event_ref,candidates)
    actor.clear()
    actor.update(candidate_actor)
    return result


def _admit_in_place(actor,experience,event_ref,candidates):
    """Mutates only the stage copy; caller commits atomically with world.

    A proposal is admissible only after an event actually occurred to which the
    actor had a qualified exposure. This is *fictional sourcefree* admission,
    not validation of an empirical human-learning law.
    """
    if experience.get('actor')!=actor['id'] or not event_ref:
        raise InvalidDevelopment('ACTOR_OR_EVENT_IDENTITY_MISMATCH')
    if not experience.get('participated') and not experience.get('perceived_cues'):
        if candidates: raise InvalidDevelopment('NO_ACTOR_EXPERIENCE')
    report=[]
    for idx,c in enumerate(candidates):
        op=c.get('kind')
        if op not in ALLOWED: raise InvalidDevelopment('UNKNOWN_PSYCHIC_OPERATION')
        if op=='NO_CHANGE':report.append({'kind':op,'status':'VALID_NO_CHANGE'});continue
        evidence={'event':event_ref,'actor':actor['id'],'experience_ref':experience['ref'],
                  'grade':GRADE,'semantic_hypothesis':True}
        if op in ('ADD_FORM','DIFFERENTIATE'):
            form=copy(c.get('form',{}))
            if form.get('kind') not in KINDS or not form.get('cues') or not isinstance(form.get('enables',[]),list):
                raise InvalidDevelopment('FORM_UNQUALIFIED')
            ident=form.get('id') or stable_id('form',{'actor':actor['id'],'event':event_ref,'index':idx,'content':form})
            if ident in actor['forms']:raise InvalidDevelopment('DUPLICATE_FORM_ID')
            validate_tendencies(form)
            if any(not isinstance(op,str) or op not in ACTIONS for op in form.get('enables',[])):
                raise InvalidDevelopment('UNSUPPORTED_ACQUIRED_OPERATION')
            form.update({'id':ident,'actor':actor['id'],'origin':[event_ref],
                         'grade':GRADE,'lifecycle':form.get('lifecycle','ACTIVE'),
                         'evidence':evidence})
            form.setdefault('scope',{})
            form.setdefault('access','tacit')
            form.setdefault('strength',.4)
            form.setdefault('body_min',0)
            actor['forms'][ident]=form
            report.append({'kind':op,'form':ident,'status':'ADMITTED_SOURCEFREE_FICTIONAL'})
        elif op=='LINK_FORMS':
            a,b=c.get('source'),c.get('target')
            if a not in actor['forms'] or b not in actor['forms'] or c.get('relation') not in RELATIONS:
                raise InvalidDevelopment('UNRESOLVED_LINK')
            _text_list(c.get('contexts',[]),'INVALID_LINK_CONTEXTS')
            link={'source':a,'target':b,'relation':c['relation'],
                  'contexts':c.get('contexts',[]),'origin':[event_ref],
                  'evidence':evidence,'grade':GRADE}
            link['id']=link_ref(link)
            if not any(link_ref(old)==link['id'] for old in actor['links']):
                actor['links'].append(link)
            report.append({'kind':op,'from':a,'to':b,'status':'ADMITTED_SOURCEFREE_FICTIONAL'})
        elif op=='ACQUIRE_RELATIONAL_MOTIF':
            try:
                motif=admit_motif(actor,c,event_ref,experience,idx)
            except InvalidRelationalMotif as exc:
                raise InvalidDevelopment(str(exc)) from exc
            actor.setdefault('relational_motifs',[]).append(motif)
            report.append({'kind':op,'motif':motif['id'],
                           'status':'ADMITTED_SOURCEFREE_RELATIONAL_FORMATION'})
        elif op=='REVALUE_RELATION':
            # The old relation remains in exact in-actor ancestry; replacement
            # changes how its endpoints become meaningful *now*, never the
            # fact that an earlier interpretation once operated.
            ident=c.get('relation_id')
            matches=[l for l in actor['links'] if link_ref(l)==ident]
            if len(matches)!=1 or c.get('new_relation') not in RELATIONS:
                raise InvalidDevelopment('UNQUALIFIED_RELATIONAL_REVALUATION')
            link=matches[0]
            contexts=c.get('contexts',link.get('contexts',[]))
            if (type(contexts) is not list or len(contexts)>20 or
                    not all(type(x) is str for x in contexts)):
                raise InvalidDevelopment('INVALID_RELATIONAL_REVALUATION_SCOPE')
            old={'relation':link['relation'],'contexts':copy(link.get('contexts',[])),
                 'event':event_ref,'prior_origin':copy(link.get('origin',[]))}
            if 'lived_institutional_difference' in c:
                # A contradiction in actually experienced public practices
                # may occasion a different *personal* relation. The model
                # chooses the new relation; the owner verifies two separately
                # lived material sources and retains both historical cuts.
                if (event_ref in link.get('origin',[]) or
                        c['new_relation']==link['relation']):
                    raise InvalidDevelopment(
                        'R24_NOT_A_LATER_RELATIONAL_REVALUATION')
                try:
                    difference=qualify_lived_institutional_difference(
                        actor,experience,event_ref,
                        c['lived_institutional_difference'])
                except ValueError as exc:
                    raise InvalidDevelopment(str(exc)) from exc
                old['lived_institutional_difference']=difference
            link.setdefault('relational_history',[]).append(old)
            link.setdefault('id',ident)
            link['relation']=c['new_relation']
            # Caller cannot replace the immutable historical source of the
            # original relation; only its current actor-specific interpretation.
            link['contexts']=copy(contexts)
            link.setdefault('changes',[]).append(evidence)
            report.append({'kind':op,'relation':ident,
                           'status':'ADMITTED_SOURCEFREE_RELATIONAL_REVALUATION'})
        elif op=='REORGANIZE_RELATIONAL_MOTIF':
            ident=c.get('motif_id')
            motifs=actor.get('relational_motifs',[])
            found=next((x for x in motifs if x.get('id')==ident),None)
            if found is None:
                raise InvalidDevelopment('UNKNOWN_RELATIONAL_MOTIF')
            # Changes to an existing learned configuration are themselves
            # historically qualified, reversible in documentary history.
            cross_context_basis=None
            if 'lived_cross_context_basis' in c:
                try:
                    cross_context_basis, changed_effects=(
                        qualify_lived_cross_context_revaluation(
                            actor,experience,event_ref,c))
                except InvalidRelationalMotif as exc:
                    raise InvalidDevelopment(str(exc)) from exc
                c={'kind':op,'motif_id':ident,'effects':changed_effects}
            update=copy(found)
            for key in ('cue_terms','locations','effects','status',
                        'witnessed_source_actor_ref'):
                if key in c:update[key]=copy(c[key])
            try:validate_motif(update,actor['forms'])
            except InvalidRelationalMotif as exc:
                raise InvalidDevelopment(str(exc)) from exc
            new_witness=update.get('witnessed_source_actor_ref')
            if (new_witness != found.get('witnessed_source_actor_ref')
                    and new_witness is not None
                    and not any(isinstance(cue,dict)
                                and cue.get('source_actor')==new_witness
                                for cue in experience.get('perceived_cues',[]))):
                raise InvalidDevelopment('MOTIF_WITNESSED_OTHER_NOT_RECEIVED')
            found.setdefault('motif_history',[]).append({
                'event':event_ref,
                'previous':{key:copy(found.get(key)) for key in
                            ('cue_terms','locations','effects','status',
                             'witnessed_source_actor_ref')},
                'experience_ref':experience['ref'],'grade':GRADE})
            if cross_context_basis is not None:
                found['motif_history'][-1]['lived_cross_context_basis']=cross_context_basis
            for key in ('cue_terms','locations','effects','status',
                        'witnessed_source_actor_ref'):
                if key in c:found[key]=copy(update[key])
            report.append({'kind':op,'motif':ident,
                           'status':'ADMITTED_SOURCEFREE_MOTIF_REORGANIZATION'})
        elif op=='LINK_ACTIVITY':
            src,dst=c.get('source'),c.get('target')
            if src not in actor['forms'] or not any(p['id']==dst for p in actor['projects']):
                raise InvalidDevelopment('UNQUALIFIED_ACTIVITY_LINK')
            _text_list(c.get('contexts',[]),'INVALID_LINK_CONTEXTS')
            link={'source':src,'target':dst,'relation':'RECRUITS_ACTIVITY',
                  'contexts':c.get('contexts',[]),'origin':[event_ref],
                  'evidence':evidence,'grade':GRADE}
            if link not in actor.setdefault('activity_links',[]):actor['activity_links'].append(link)
            report.append({'kind':op,'form':src,'activity':dst,'status':'ADMITTED_SOURCEFREE_FICTIONAL'})
        elif op=='ACQUIRE_COMPOSITION_METHOD':
            # Not a pre-installed mature faculty: a proposed new organizing
            # *method* needs actual actor-performed practice now and historically
            # acquired, separately identified means to compose. The inference
            # remains fictional / underdetermined rather than an empirical law.
            refs=c.get('source_forms');operations=c.get('operations')
            if (not isinstance(refs,list) or len(set(refs))!=2 or
                len(refs)!=2 or any(x not in actor['forms'] for x in refs)):
                raise InvalidDevelopment('COMPOSITION_NEEDS_TWO_ACQUIRED_FORMS')
            if (not isinstance(operations,list) or len(operations)!=2 or
                len(set(operations))!=2 or any(x not in ACTIONS for x in operations)):
                raise InvalidDevelopment('COMPOSITION_NOT_AN_EXISTING_TWO_MEANS')
            if not all(actor['forms'][x].get('origin') for x in refs):
                raise InvalidDevelopment('COMPOSITION_MISSING_PRACTICE_HISTORY')
            if not all(any(x in actor['forms'][fid].get('enables',[]) for fid in refs)
                       for x in operations):
                raise InvalidDevelopment('COMPOSITION_MEANS_NOT_PRACTICED')
            enacted=experience.get('felt_enactment') or {}
            if (not experience.get('participated') or experience.get('status')!='PERFORMED' or
                    enacted.get('attempted_operation') not in operations):
                raise InvalidDevelopment('COMPOSITION_NEEDS_OWN_PERFORMED_ENCOUNTER')
            if not isinstance(c.get('hypothesized_end'),str) or not c['hypothesized_end']:
                raise InvalidDevelopment('COMPOSITION_END_UNSPECIFIED')
            locs=c.get('locations',[])
            if not isinstance(locs,list) or not all(isinstance(x,str) for x in locs):
                raise InvalidDevelopment('INVALID_COMPOSITION_SCOPE')
            ident=stable_id('method',{'actor':actor['id'],'event':event_ref,'index':idx,
              'forms':sorted(refs),'operations':operations,'end':c['hypothesized_end']})
            rule={'id':ident,'source_forms':copy(refs),'operations':copy(operations),
                'hypothesized_end':c['hypothesized_end'],'locations':copy(locs),
                'status':'ACTIVE','origin':[event_ref],'experience_ref':experience['ref'],
                'grade':GRADE,'meaning':'FICTIONAL_PROVISIONAL_ACQUIRED_METHOD',
                'no_inference_of_real_human_learning_law':True}
            actor.setdefault('composition_methods',[]).append(rule)
            report.append({'kind':op,'method':ident,'status':'ADMITTED_SOURCEFREE_FICTIONAL'})
        elif op=='CHANGE_RECRUITMENT_SCOPE':
            ident=c.get('form_id')
            if ident not in actor['forms']:raise InvalidDevelopment('UNKNOWN_FORM')
            new_scope=c.get('new_scope')
            if not isinstance(new_scope,dict):raise InvalidDevelopment('BAD_SCOPE')
            validate_tendencies({'scope':new_scope})
            form=actor['forms'][ident]
            form.setdefault('prior_scopes',[]).append({'scope':copy(form.get('scope',{})),'event':event_ref})
            form['scope']=copy(new_scope)
            form.setdefault('changes',[]).append(evidence)
            report.append({'kind':op,'form':ident,'status':'ADMITTED_SOURCEFREE_FICTIONAL'})
        elif op=='CHANGE_STRENGTH':
            ident=c.get('form_id')
            if ident not in actor['forms']:raise InvalidDevelopment('UNKNOWN_FORM')
            delta=c.get('delta',0)
            if (isinstance(delta,bool) or not isinstance(delta,(int,float))
                    or not math.isfinite(delta) or abs(delta)>.35):
                raise InvalidDevelopment('UNBOUNDED_STRENGTH')
            f=actor['forms'][ident];f['strength']=round(min(1,max(0,f.get('strength',.4)+delta)),4)
            f.setdefault('changes',[]).append(evidence)
            report.append({'kind':op,'form':ident,'status':'ADMITTED_SOURCEFREE_FICTIONAL'})
        elif op in ('SET_DORMANT','REACTIVATE'):
            ident=c.get('form_id')
            if ident not in actor['forms']:raise InvalidDevelopment('UNKNOWN_FORM')
            actor['forms'][ident]['lifecycle']='DORMANT' if op=='SET_DORMANT' else 'ACTIVE'
            actor['forms'][ident].setdefault('changes',[]).append(evidence)
            report.append({'kind':op,'form':ident,'status':'ADMITTED_SOURCEFREE_FICTIONAL'})
        elif op=='ACQUIRE_SOCIAL_VOCAL_COORDINATION':
            try:
                report.append(admit_vocal_coordination(
                    actor,experience,event_ref,c))
            except ValueError as error:
                raise InvalidDevelopment(str(error)) from error
        elif op=='ACQUIRE_SITUATED_CULTURAL_REFERENCE':
            try:
                report.append(admit_cultural_reference(
                    actor,experience,event_ref,c))
            except ValueError as error:
                raise InvalidDevelopment(str(error)) from error
        elif op=='REVISE_SITUATED_CULTURAL_REFERENCE':
            try:
                report.append(admit_reference_revision(
                    actor,experience,event_ref,c))
            except ValueError as error:
                raise InvalidDevelopment(str(error)) from error
        elif op=='ACQUIRE_COSTLY_CARE_PRACTICE':
            try:
                report.append(admit_care_commitment(
                    actor,experience,event_ref,c))
            except ValueError as error:
                raise InvalidDevelopment(str(error)) from error
        elif op=='ACQUIRE_CONDITIONAL_JOINT_PRACTICE':
            try:
                report.append(admit_joint_practice(
                    actor,experience,event_ref,c))
            except ValueError as error:
                raise InvalidDevelopment(str(error)) from error
        elif op=='ACQUIRE_GENETIC_POSSIBLE_END':
            try:
                report.append(admit_contrast_end(
                    actor,experience,event_ref,c))
            except ValueError as error:
                raise InvalidDevelopment(str(error)) from error
        elif op=='ACQUIRE_EXPRESSIVE_PRACTICE':
            try:
                report.append(admit_expressive_practice(actor,experience,event_ref,c))
            except ValueError as error:
                raise InvalidDevelopment(str(error)) from error
        elif op=='ACQUIRE_REPAIR_TECHNIQUE':
            try:
                report.append(admit_repair_technique(actor,experience,event_ref,c))
            except ValueError as error:
                raise InvalidDevelopment(str(error)) from error
        elif op=='NOTICE_PRIVATE_POSSIBLE_END':
            try:
                report.append(admit_private_possible_end(actor,experience,event_ref,c))
            except ValueError as error:
                raise InvalidDevelopment(str(error)) from error
        elif op=='NOTICE_POSSIBLE_END':
            # An experience can make a *previously unchosen* consequence
            # interesting without retroactively making it the purpose of the
            # first attempt. This is only a possible future end, not a motive.
            ref=c.get('perceived_cue_ref')
            received={q.get('id') for q in experience.get('perceived_cues',[])
                      if isinstance(q,dict) and type(q.get('id')) is str}
            if type(ref) is not str or ref not in received:
                raise InvalidDevelopment('POSSIBLE_END_MUST_DERIVE_FROM_ACTOR_RECEIVED_SIGN')
            obj=c.get('possible_object')
            if type(obj) is not str or not obj.strip() or len(obj)>512:
                raise InvalidDevelopment('INVALID_POSSIBLE_END_DESCRIPTION')
            possible=c.get('possible_means',[])
            if (type(possible) is not list or not 1<=len(possible)<=8
                    or any(type(x) is not str or x not in ACTIONS for x in possible)
                    or len(set(possible))!=len(possible)):
                raise InvalidDevelopment('POSSIBLE_END_MEANS_NOT_QUALIFIED')
            cues=c.get('cue_terms',[])
            _text_list(cues,'INVALID_POSSIBLE_END_CUES')
            if len(cues)>16:raise InvalidDevelopment('POSSIBLE_END_CUES_UNBOUNDED')
            end_id=stable_id('possible_end',{'actor':actor['id'],
                'event':event_ref,'cue':ref,'index':idx,'object':obj})
            if any(e['id']==end_id for e in actor.get('possible_ends',[])):
                raise InvalidDevelopment('DUPLICATE_POSSIBLE_END')
            origin_object=c.get('origin_material_object_ref')
            if origin_object is not None and (
                    type(origin_object) is not str or
                    not any(q.get('id')==ref and
                            q.get('material_object_ref')==origin_object
                            for q in experience.get('perceived_cues',[])
                            if type(q) is dict)):
                raise InvalidDevelopment(
                    'POSSIBLE_END_OBJECT_NOT_ACTOR_RECEIVED')
            end={'id':end_id,'possible_object':obj,
                 'origin_material_object_ref':origin_object,
                 'possible_means':copy(possible),'cue_terms':copy(cues),
                 'status':'POSSIBLE_NOT_ACQUIRED_MOTIVE',
                 'origin_event':event_ref,'experience_ref':experience['ref'],
                 'actor_perceived_cue_ref':ref,
                 'eliciting_actor_action':experience.get('own_action'),
                 'initial_event_intent_not_rewritten':True,
                 'actual_consequence_not_identified_by_actor_perception':True,
                 'meaning_hypothesis_not_empirical_learning_law':True,
                 'grade':GRADE}
            if c.get('incidental_object_end_basis') is not None:
                matches=[q['incidental_object_end_basis'] for q in
                    possible_unintended_goods(actor,experience,
                        experience.get('own_practical_selection'),event_ref)
                    if q.get('incidental_object_end_basis')==c['incidental_object_end_basis']
                    and q['source_cue_ref']==ref
                    and q['world_material_object_ref']==origin_object]
                if len(matches)!=1 or any(x not in ('INSPECT','REPAIR') for x in possible):
                    raise InvalidDevelopment('INCIDENTAL_END_SOURCE_NOT_QUALIFIED')
                end['incidental_object_end_basis']=copy(matches[0])
            actor.setdefault('possible_ends',[]).append(end)
            report.append({'kind':op,'possible_end':end_id,
                           'status':'ADMITTED_PROVISIONAL_END_NOT_YET_MOTIVE'})
        elif op in ('ACQUIRE_NOTICE_EXPECTATION','REVISE_NOTICE_EXPECTATION'):
            try:
                fn=admit_notice_expectation if op=='ACQUIRE_NOTICE_EXPECTATION' else admit_notice_revision
                report.append(fn(actor,experience,event_ref,c))
            except ValueError as error:
                raise InvalidDevelopment(str(error)) from error
        elif op=='ACQUIRE_SITUATED_PUBLIC_PROCEDURE_EXPECTATION':
            try:
                report.append(admit_public_procedure_expectation(
                    actor,experience,event_ref,c))
            except ValueError as error:
                raise InvalidDevelopment(str(error)) from error
        elif op=='REOPEN_CO_REGULATION_ORIENTATION':
            try:
                report.append(admit_reopening(actor,experience,event_ref,c))
            except ValueError as error:
                raise InvalidDevelopment(str(error)) from error
        elif op=='REVISE_CO_REGULATION_ORIENTATION':
            try:
                report.append(admit_co_regulation_revision(
                    actor,experience,event_ref,c))
            except ValueError as error:
                raise InvalidDevelopment(str(error)) from error
        elif op=='ACQUIRE_CO_REGULATION_ORIENTATION':
            try:
                report.append(admit_co_regulation(
                    actor,experience,event_ref,c))
            except ValueError as error:
                raise InvalidDevelopment(str(error)) from error
        elif op=='INVEST_MATERIAL_OBJECT':
            try:
                report.append(admit_material_investment(
                    actor,experience,event_ref,c))
            except ValueError as error:
                raise InvalidDevelopment(str(error)) from error
        elif op=='REVISE_FUNCTIONAL_CORRESPONDENCE':
            try:
                report.append(admit_functional_revision(actor,experience,event_ref,c))
            except ValueError as error:
                raise InvalidDevelopment(str(error)) from error
        elif op=='ACQUIRE_FUNCTIONAL_CORRESPONDENCE':
            try:
                report.append(admit_functional_correspondence(actor,experience,event_ref,c))
            except ValueError as error:
                raise InvalidDevelopment(str(error)) from error
        elif op=='RECORD_POSSIBLE_END_TRIAL':
            # A real trial is recorded even when no LLM wishes to declare an
            # acquired motive. The developmental owner retains its afterlife.
            try:
                report.append(record_possible_end_trial(actor,experience,event_ref,c))
            except ValueError as error:
                raise InvalidDevelopment(str(error)) from error
        elif op=='TAKE_UP_POSSIBLE_END':
            ref=c.get('possible_end_ref')
            ends=[e for e in actor.get('possible_ends',[])
                  if e.get('id')==ref]
            if len(ends)!=1:
                raise InvalidDevelopment('UNKNOWN_OR_AMBIGUOUS_POSSIBLE_END')
            end=ends[0]
            if (end.get('status')!='POSSIBLE_NOT_ACQUIRED_MOTIVE'
                    or end['origin_event']==event_ref):
                raise InvalidDevelopment('POSSIBLE_END_CANNOT_RETROACTIVELY_BECOME_INTENT')
            # The second episode must remain an independently experienced
            # event. An LLM may nominate WHICH actually received cue became
            # consequential, but cannot create or retrospectively access it.
            # Absence of an explicit sign remains qualified uncertainty, not
            # an instruction to invent a conscious explanation.
            later_received={cue.get('id') for cue in experience.get('perceived_cues',[])
                if isinstance(cue,dict) and type(cue.get('id')) is str}
            if end.get('genesis_family')=='SENSED_INTERRUPTION_THEN_RELIEF':
                # A mere third event is not enough: an acquired new concern
                # must be brought into an actually *relevant* later situation.
                # The old code would accept an unrelated singleton sign as
                # sufficient to manufacture a qualitatively new project.
                if (type(experience.get('clock')) is not int
                        or type(end.get('origin_clock')) is not int
                        or experience['clock']<=end['origin_clock']):
                    raise InvalidDevelopment('GENETIC_TAKEUP_NOT_LATER_EXPERIENCE')
                qualified_signs={cue.get('id') for cue in
                    experience.get('perceived_cues',[])
                    if type(cue) is dict
                    and type(cue.get('id')) is str
                    and bool({str(t).casefold() for t in
                        cue.get('tags',[]) if type(t) is str}
                        & {str(t).casefold() for t in
                           end.get('cue_terms',[]) if type(t) is str})}
                if not qualified_signs:
                    raise InvalidDevelopment('GENETIC_TAKEUP_NO_REENCOUNTERED_SIGN')
                if (c.get('later_perceived_cue_ref') is not None
                        and c['later_perceived_cue_ref'] not in qualified_signs):
                    raise InvalidDevelopment('GENETIC_TAKEUP_UNRELATED_SIGN')
                if c.get('later_perceived_cue_ref') is None:
                    # A sourcefree inference can abstain when multiple signs
                    # compete. It cannot choose arbitrary "first" as cause.
                    if len(qualified_signs)!=1:
                        raise InvalidDevelopment('GENETIC_TAKEUP_SIGN_AMBIGUOUS')
                    c=copy(c)
                    c['later_perceived_cue_ref']=next(iter(qualified_signs))
            private_takeup=None
            if end.get('genesis_family')=='ACTUAL_PRIVATE_REHEARSAL':
                ground=private_end_ground(actor.get('memories',[]),end,actor['id'],
                                           experience.get('location'),experience.get('clock',-1))
                trials=[t for t in end.get('trial_history',[])
                        if t.get('private_rehearsal_ref')==end.get('private_rehearsal_ref')
                        and t.get('actor_experienced_status')=='PERFORMED'
                        and t.get('event_ref')!=event_ref]
                sel=experience.get('own_practical_selection') or {}
                if (not ground or not trials
                        or sel.get('status')!='ACTOR_POLICY_PRACTICAL_ATTEMPT'
                        or sel.get('selected_project_refs')!=[]
                        or sel.get('possible_end_trial') is not None
                        or experience.get('status')!='PERFORMED'
                        or experience.get('own_action') not in [t['operation'] for t in trials]
                        or not later_received):
                    raise InvalidDevelopment('PRIVATE_END_TAKEUP_REQUIRES_LATER_LIVED_COURSE')
                private_takeup={'rehearsal_ref':ground['id'],'prior_trial_ref':trials[-1]['id'],
                                'later_event_ref':event_ref}
            dependency_takeup=None
            if end.get('genesis_family')=='INTERRUPTED_ACQUIRED_SUPPORT_THEN_INDEPENDENT_RELIEF':
                matches=[p for p in possible_dependency_project_takeups(actor,experience,event_ref)
                         if p['possible_end_ref']==ref
                         and p['dependency_takeup_basis']==c.get('dependency_takeup_basis')
                         and p['later_perceived_cue_ref']==c.get('later_perceived_cue_ref')
                         and p['means']==c.get('means')]
                if len(matches)!=1:
                    raise InvalidDevelopment('DEPENDENCY_TAKEUP_NO_QUALIFIED_LATER_COURSE')
                dependency_takeup=copy(matches[0]['dependency_takeup_basis'])
            elif 'dependency_takeup_basis' in c:
                raise InvalidDevelopment('DEPENDENCY_TAKEUP_WRONG_END_FAMILY')
            claimed_later_sign=c.get('later_perceived_cue_ref')
            if (claimed_later_sign is not None and
                    (type(claimed_later_sign) is not str or
                     claimed_later_sign not in later_received)):
                raise InvalidDevelopment('TAKEUP_SIGN_NOT_ACTOR_RECEIVED')
            if claimed_later_sign is None and len(later_received)==1:
                # One received sign is a *possible contextual anchor*, not
                # proof it caused the new concern or that the actor knows why.
                claimed_later_sign=next(iter(later_received))
            incidental=None
            if end.get('incidental_object_end_basis') is not None:
                incidental=qualify_incidental_object_takeup(actor,experience,event_ref,end)
                if (incidental is None or c.get('incidental_takeup_basis')!=incidental
                        or claimed_later_sign!=incidental['later_perceived_cue_ref']):
                    raise InvalidDevelopment('INCIDENTAL_END_NEEDS_DISTINCT_LIVED_TRIAL_AND_REENCOUNTER')
            takeup_evidence={
                'later_event':event_ref,'later_experience_ref':experience['ref'],
                'actual_received_sign_refs':sorted(later_received),
                'later_received_sign_ref':claimed_later_sign,
                'sign_selection_grade':(
                    'LLM_PROPOSED_ACTOR_RECEIVED_SIGN'
                    if 'later_perceived_cue_ref' in c else
                    'SINGLE_ACTOR_RECEIVED_SIGN_PROVISIONAL'
                    if claimed_later_sign else
                    'LATER_EXPERIENCE_SIGN_UNSPECIFIED'),
                'not_a_proven_causal_significance':True,
                'not_actor_self_account':True,
                'unobserved_alternatives':'UNKNOWN_NOT_OBSERVED',
            }
            if dependency_takeup is not None:
                takeup_evidence['dependency_takeup_basis']=dependency_takeup
            if private_takeup is not None:
                takeup_evidence['private_takeup_basis']=private_takeup
            requested=c.get('means',end['possible_means'])
            if (type(requested) is not list or not requested or
                    any(type(x) is not str or x not in end['possible_means']
                        for x in requested) or len(set(requested))!=len(requested)):
                raise InvalidDevelopment('UNLICENSED_TAKEUP_MEANS')
            priority=c.get('priority',.35)
            validate_activity_priority(priority)
            project_id=stable_id('emergent_project',{
                'actor':actor['id'],'candidate':ref,'event':event_ref})
            if any(p['id']==project_id for p in actor['projects']):
                raise InvalidDevelopment('DUPLICATE_EMERGENT_PROJECT')
            project={'id':project_id,'object':end['possible_object'],
                     'motive':'EMERGENT_PROVISIONAL_END_NOT_INFERRED_FROM_INITIAL_ACT',
                     'means':copy(requested),'cue_terms':copy(end['cue_terms']),
                     'status':'active','priority':priority,
                     'contextual_only':False,
                     'origin':[end['origin_event'],event_ref],
                     'possible_end_ref':ref,
                     'takeup_evidence':copy(takeup_evidence),
                     'skill_mastery_not_inferred':True,
                     'original_attempt_purpose_not_rewritten':True,
                     'grade':GRADE}
            # A specifically experienced responder becomes an *addressed*
            # practical possibility, never an assumed beneficiary or consent.
            if end.get('addressed_party_ref') is not None:
                project['addressed_party_ref']=end['addressed_party_ref']
                project['other_future_conduct']='INDEPENDENT_NOT_PROMISED'
            if incidental is not None:
                project['material_object_ref']=incidental['source_object_ref']
                project['incidental_takeup_basis']=copy(incidental)
                project['contextual_only']=True
                takeup_evidence['incidental_takeup_basis']=copy(incidental)
                project['takeup_evidence']=copy(takeup_evidence)
            actor['projects'].append(project)
            end.setdefault('subsequent_takeup',[]).append({
                'event':event_ref,'experience_ref':experience['ref'],
                'takeup_evidence':copy(takeup_evidence),
                'project_ref':project_id,'grade':GRADE})
            end['status']='TAKEN_UP_AS_PRACTICAL_PROJECT'
            report.append({'kind':op,'project':project_id,'possible_end':ref,
                           'status':'ADMITTED_FICTIONAL_LATER_END_TAKEUP'})
        elif op=='ACQUIRE_PREPROJECT_ANTICIPATION':
            try:
                report.append(admit_preproject_anticipation(actor,experience,event_ref,c))
            except ValueError as error:
                raise InvalidDevelopment(str(error)) from error
        elif op=='REVISE_PREPROJECT_ANTICIPATION':
            try:
                report.append(revise_preproject_anticipation(actor,experience,event_ref,c))
            except ValueError as error:
                raise InvalidDevelopment(str(error)) from error
        elif op=='ACQUIRE_REFLECTIVE_REGULATION':
            try:
                receipt=acquire_reflective_regulation(actor,experience,event_ref,c,ACTIONS)
                # The new practice is read by the EXISTING recruitment and
                # psychodynamic owners, not by a parallel will controller.
                validate_tendencies(actor['forms'][receipt['form']])
                report.append(receipt)
            except ValueError as error:
                raise InvalidDevelopment(str(error)) from error
        elif op=='ACQUIRE_ACTIVITY_AFFECT':
            try:
                report.append(admit_activity_affect(actor,experience,event_ref,c))
            except ValueError as error:
                raise InvalidDevelopment(str(error)) from error
        elif op=='APPRAISE_EXPECTED_DIFFERENCE':
            try:
                report.append(appraise_expected_difference(actor,experience,event_ref,c))
            except ValueError as error:
                raise InvalidDevelopment(str(error)) from error
        elif op=='ADD_PROJECT':
            project=copy(c.get('project',{}))
            if not project.get('object') or not isinstance(project.get('means'),list):
                raise InvalidDevelopment('INVALID_NEW_PROJECT')
            if any(not isinstance(op,str) or op not in ACTIONS for op in project['means']):
                raise InvalidDevelopment('UNSUPPORTED_ACTIVITY_MEANS')
            validate_activity_priority(project.get('priority',.4))
            if 'contextual_only' in project and type(project['contextual_only']) is not bool:
                raise InvalidDevelopment('INVALID_PROJECT_CONTEXTUAL_FLAG')
            if 'expected_difference' in project:
                project['expected_difference']=validate_expected_difference(
                    project['expected_difference'])
            _text_list(project.get('cue_terms',[]),'INVALID_PROJECT_CUE_TERMS')
            ident=project.get('id') or stable_id('project',{'actor':actor['id'],'event':event_ref,'index':idx})
            if any(p['id']==ident for p in actor['projects']):
                raise InvalidDevelopment('DUPLICATE_PROJECT')
            project.update({'id':ident,'origin':[event_ref],'grade':GRADE})
            project.setdefault('motive','UNSPECIFIED_ACQUIRED_MOTIVE')
            project.setdefault('status','active')
            project.setdefault('priority',.4)
            project.setdefault('cue_terms',[])
            actor['projects'].append(project)
            report.append({'kind':op,'project':ident,'status':'ADMITTED_SOURCEFREE_FICTIONAL'})
        elif op=='REORGANIZE_PROJECT':
            ident=c.get('project_id')
            project=next((p for p in actor['projects'] if p['id']==ident),None)
            if project is None:raise InvalidDevelopment('UNKNOWN_PROJECT')
            dependency_basis=c.get('dependency_reorganization_basis')
            dependency_project=bool(project.get('takeup_evidence',{}).get('dependency_takeup_basis'))
            revision_basis=c.get('dependency_means_revision_basis')
            if revision_basis is not None:
                if c not in possible_dependency_means_revisions(actor,experience,event_ref):
                    raise InvalidDevelopment('DEPENDENCY_MEANS_REVISION_UNQUALIFIED')
                bound=project['dependency_conditional_means']['SIGNAL']
                previous=bound.get('status','ACTIVE')
                bound['status']='SUSPENDED' if revision_basis['mode']=='SUSPEND' else 'ACTIVE'
                bound.setdefault('revision_history',[]).append({
                    'event_ref':event_ref,'experience_ref':experience['ref'],
                    'previous_status':previous,'new_status':bound['status'],
                    'basis':copy(revision_basis),'grade':GRADE})
            elif dependency_basis is not None:
                if c not in possible_dependency_project_reorganizations(actor,experience,event_ref):
                    raise InvalidDevelopment('DEPENDENCY_PROJECT_REORGANIZATION_UNQUALIFIED')
                prior={k:copy(project.get(k)) for k in ('means','object','motive')}
                project.setdefault('dependency_reorganization_history',[]).append({
                    'event_ref':event_ref,'experience_ref':experience['ref'],
                    'previous':prior,'basis':copy(dependency_basis),'grade':GRADE})
                project['dependency_conditional_means']={'SIGNAL':{
                    'counterpart_ref':dependency_basis['counterpart_ref'],
                    'location':dependency_basis['location'],
                    'practice_ref':dependency_basis['practice_ref'],
                    'origin_event_ref':event_ref}}
            elif dependency_project and any(k in c for k in
                    ('means','object','motive','addressed_party_ref','dependency_conditional_means')):
                raise InvalidDevelopment('DEPENDENCY_PROJECT_MEANS_REQUIRE_LIVED_REORGANIZATION')
            if 'means' in c and (not isinstance(c['means'],list) or not all(isinstance(x,str) for x in c['means'])):
                raise InvalidDevelopment('INVALID_PROJECT_MEANS')
            if 'means' in c and any(x not in ACTIONS for x in c['means']):
                raise InvalidDevelopment('UNSUPPORTED_ACTIVITY_MEANS')
            if 'priority' in c:validate_activity_priority(c['priority'])
            if 'contextual_only' in c and type(c['contextual_only']) is not bool:
                raise InvalidDevelopment('INVALID_PROJECT_CONTEXTUAL_FLAG')
            if 'cue_terms' in c:_text_list(c['cue_terms'],'INVALID_PROJECT_CUE_TERMS')
            if 'expected_difference' in c:
                validate_expected_difference(c['expected_difference'])
            for field in ('priority','means','object','motive','status','cue_terms','contextual_only',
                          'expected_difference','addressed_party_ref'):
                if field in c:project[field]=copy(c[field])
            project.setdefault('history',[]).append(evidence)
            report.append({'kind':op,'project':ident,'status':'ADMITTED_SOURCEFREE_FICTIONAL'})
        elif op in ('TRACE','MEMORY'):
            _text_list(c.get('cue_terms',[]),'INVALID_TRACE_CUES')
            ref=stable_id('trace' if op=='TRACE' else 'memory',{'actor':actor['id'],'event':event_ref,'index':idx})
            entry={'id':ref,'origin':[event_ref],'experience':experience['ref'],
                   'grade':GRADE,'status':'NONDECLARATIVE' if op=='TRACE' else 'ACTOR_ACCESSIBLE',
                   'cue_terms':c.get('cue_terms',[]),'content':c.get('content',''),
                   'manifestation':c.get('manifestation','uninterpreted')}
            if 'undertaking_attention_ref' in c:
                receipt=received_undertaking_attention(actor,
                    experience.get('own_practical_selection'),experience)
                paths=[p for p in actor.get('evidence_paths',[])
                       if p.get('event')==event_ref and p.get('experience_ref')==experience['ref']
                       and p.get('undertaking_attention')==receipt]
                if (op!='MEMORY' or not receipt or receipt!=experience.get('undertaking_attention_receipt')
                        or c['undertaking_attention_ref']!=receipt['attention_id'] or len(paths)!=1
                        or type(entry['content']) is not str or not entry['content'].strip()
                        or len(entry['content'])>512
                        or any(m.get('undertaking_attention',{}).get('attention_id')==receipt['attention_id']
                               for m in actor['memories'])):
                    raise InvalidDevelopment('UNDERTAKING_MEMORY_UNQUALIFIED_ATTENTION')
                entry['undertaking_attention']=copy(receipt)
                entry['remembered_meaning_not_objective_future_truth']=True
            actor['traces' if op=='TRACE' else 'memories'].append(entry)
            report.append({'kind':op,'ref':ref,'status':'ADMITTED_SOURCEFREE_FICTIONAL'})
        elif op=='CHANGE_OTHER_MODEL':
            # A person may encounter an Other *directly*, or witness that
            # Other's actually performed act toward a third person. These
            # are different evidence paths, neither a license to know minds.
            other=c.get('other_ref')
            if type(other) is not str or not other or other==actor['id']:
                raise InvalidDevelopment('INVALID_OTHER_REFERENCE')
            hypothesis=c.get('hypothesis')
            if type(hypothesis) is not str or not hypothesis:
                raise InvalidDevelopment('EMPTY_RELATIONAL_HYPOTHESIS')
            about=c.get('about_relation_with_ref')
            cited=c.get('witnessed_cue_ref')
            entry={'hypothesis':hypothesis,'event':event_ref,
                   'confidence':c.get('confidence','tentative'),
                   'grade':GRADE,'not_other_objective_truth':True}
            if about is None:
                # Retain original direct reciprocal encounter gate.
                if cited is not None:
                    raise InvalidDevelopment('UNQUALIFIED_OTHER_MODEL_CUE')
                if experience.get('reciprocated_partner')!=other:
                    raise InvalidDevelopment('OTHER_NOT_ENCOUNTERED_IN_THIS_EXPERIENCE')
            else:
                if (type(about) is not str or not about or
                        about in (other,actor['id']) or
                        type(cited) is not str or not cited):
                    raise InvalidDevelopment('INVALID_THIRD_PARTY_RELATION_REFERENCE')
                observed=any(
                    type(cue) is dict and cue.get('id')==cited
                    and cue.get('source_actor')==other
                    and cue.get('actor_accessible_target_ref')==about
                    and cue.get('kind') in (
                        'performed_care','performed_feed','performed_impose')
                    and cue.get(
                        'public_person_directed_act_not_private_intention') is True
                    for cue in experience.get('perceived_cues',[]))
                if not observed:
                    raise InvalidDevelopment('THIRD_PARTY_RELATION_NOT_ACTOR_WITNESSED')
                entry.update({
                    'about_relation_with_ref':about,
                    'witnessed_cue_ref':cited,
                    'only_actor_local_interpretation_of_witnessed_act':True,
                    'not_other_private_state_or_target_consent':True})
            actor['other_models'].setdefault(other,[]).append(entry)
            report.append({'kind':op,'other_ref':other,
                           'about_relation_with_ref':about,
                           'status':'ADMITTED_SOURCEFREE_FICTIONAL'})
        elif op=='ACQUIRE_HISTORICAL_ORIENTATION':
            try:report.append(acquire_orientation(actor,experience,event_ref,c))
            except ValueError as err:raise InvalidDevelopment(str(err)) from err
        elif op=='ACQUIRE_LIVED_DIRECTIONAL_ORIENTATION':
            try:report.append(admit_lived_directional_orientation(
                actor,experience,event_ref,c))
            except ValueError as err:raise InvalidDevelopment(str(err)) from err
        elif op=='REVISE_HISTORICAL_ORIENTATION':
            try:report.append(revise_orientation(actor,experience,event_ref,c))
            except ValueError as err:raise InvalidDevelopment(str(err)) from err
        elif op=='REVISE_OPERATIVE_SELF_ORGANIZATION':
            try:report.append(revise_operative_self(actor,experience,event_ref,c))
            except ValueError as err:raise InvalidDevelopment(str(err)) from err
        elif op=='ACTOR_SELF_MODEL':
            if actor['body']['language']<.25:raise InvalidDevelopment('NO_REFLECTIVE_SELF_MODEL_CAPACITY')
            if 'operative_action' in c:
                qualified=copy(c);qualified['operation']=c['operative_action']
                try:report.append(acquire_operative_self(actor,experience,event_ref,qualified))
                except ValueError as err:raise InvalidDevelopment(str(err)) from err
            else:
                actor['self_model'].setdefault('hypotheses',[]).append({'claim':c.get('claim',''),
                    'confidence':c.get('confidence','uncertain'), 'origin':[event_ref],
                    'grade':GRADE,'does_not_operate_without_practice':True})
                report.append({'kind':op,'status':'ADMITTED_SOURCEFREE_FICTIONAL',
                               'operative':False,'not_practice_qualified':True})
    actor.setdefault('history_refs',[]).append(event_ref)
    return report


def recurring_provisional_growth(actor,period_ref,processes):
    """Admit only actor-addressed coarse-life effects, all-or-nothing.

    Modelled coverage is NOT an individual experience and may not rewrite a
    different actor merely because they possess the same reusable form ID.
    A modeled scope generalization is not an observed microepisode or a law.
    """
    staged=copy(actor)
    outputs=[]
    if not isinstance(processes,list):
        raise InvalidDevelopment('INVALID_PERIOD_PROCESSES')
    for proc in processes:
        if not isinstance(proc,dict):
            raise InvalidDevelopment('INVALID_PERIOD_PROCESS')
        if proc.get('kind')!='practice_access' or proc.get('coverage')!='AGGREGATE_MODELED':
            continue
        if proc.get('warrants_scope_change') is not True:
            continue
        # A global, unqualified activity-coverage capsule is not a licence to
        # generalize every similarly named learned form in all family members.
        claimed_actor=proc.get('actor_id')
        if not isinstance(claimed_actor,str) or not claimed_actor:
            raise InvalidDevelopment('PERIOD_PRACTICE_REQUIRES_ACTOR')
        if claimed_actor!=staged['id']:
            continue
        fid=proc.get('form_id')
        if not isinstance(fid,str) or not fid:
            raise InvalidDevelopment('INVALID_PERIOD_FORM_REF')
        if fid not in staged['forms']:
            # Evidence for an unowned form does not fabricate that form.
            continue
        locations=proc.get('locations',[])
        if (not isinstance(locations,list) or
                any(not isinstance(place,str) or not place for place in locations)):
            raise InvalidDevelopment('INVALID_PERIOD_LOCATIONS')
        form=staged['forms'][fid]
        old=copy(form.get('scope',{}))
        try:
            validate_tendencies({'scope':old})
        except ValueError as exc:
            raise InvalidDevelopment('INVALID_PRIOR_FORM_SCOPE') from exc
        old_locations=old.get('locations',[])
        novel=sorted(set(old_locations)|set(locations))
        if set(novel)==set(old_locations):
            # Period occurred, but the actor's recruitment did not change.
            continue
        form['scope']={**old,'locations':novel}
        form.setdefault('changes',[]).append({'period':period_ref,'grade':GRADE,
            'type':'AGGREGATE_MODELED_SCOPE_GENERALIZATION'})
        outputs.append({'kind':'PERIOD_SCOPE_CHANGE','form':fid})
    actor.clear()
    actor.update(staged)
    return outputs
