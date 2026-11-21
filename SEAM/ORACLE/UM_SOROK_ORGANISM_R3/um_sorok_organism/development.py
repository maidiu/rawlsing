"""Research-only psychological afterlife: typed *fictional* formation and rewiring.

This is not CAN/ADP native authority. Every admitted form is actor-specific, bound
by actual experienced event, scoped, graded, and revisable. No LLM may edit an
objective world fact or another actor's state here.
"""
from .types import stable_id, copy, GRADE
from .psychodynamics import validate_tendencies
from .relational_metabolism import (
    RELATIONS, link_ref, validate_motif, admit_motif, InvalidRelationalMotif,
)
from .organism import ACTIONS
from .practical_difference import validate_expected_difference, appraise_expected_difference
from .preproject_agency import admit_preproject_anticipation, revise_preproject_anticipation
from .reflective_regulation import acquire_reflective_regulation
from .historical_self_organization import (
    acquire_orientation, revise_orientation, acquire_operative_self,
    revise_operative_self)
from .psychic_genesis import admit_contrast_end
from .joint_practice_genesis import admit_joint_practice
from .care_commitment_genesis import admit_care_commitment
from .cultural_mediation import (
    admit_cultural_reference,admit_reference_revision)
from .social_vocal_development import admit_vocal_coordination
from .prospective_horizon import record_possible_end_trial
from .functional_correspondence import admit_functional_correspondence
from .material_investments import admit_material_investment
from .co_regulation_history import (
    admit_co_regulation, admit_co_regulation_revision)
from .plural_care_paths import admit_reopening
from .institutional_procedure_learning import admit_public_procedure_expectation
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
         'NOTICE_POSSIBLE_END','TAKE_UP_POSSIBLE_END',
         'APPRAISE_EXPECTED_DIFFERENCE','ACQUIRE_PREPROJECT_ANTICIPATION',
         'REVISE_PREPROJECT_ANTICIPATION','ACQUIRE_REFLECTIVE_REGULATION',
         'RECORD_POSSIBLE_END_TRIAL','ACQUIRE_FUNCTIONAL_CORRESPONDENCE',
         'INVEST_MATERIAL_OBJECT','ACQUIRE_CO_REGULATION_ORIENTATION',
         'REVISE_CO_REGULATION_ORIENTATION',
         'ACQUIRE_HISTORICAL_ORIENTATION','REVISE_HISTORICAL_ORIENTATION',
         'REVISE_OPERATIVE_SELF_ORGANIZATION',
         'REOPEN_CO_REGULATION_ORIENTATION',
         'ACQUIRE_SITUATED_PUBLIC_PROCEDURE_EXPECTATION',
         'ACQUIRE_GENETIC_POSSIBLE_END',
         'ACQUIRE_CONDITIONAL_JOINT_PRACTICE',
         'ACQUIRE_COSTLY_CARE_PRACTICE',
         'ACQUIRE_SITUATED_CULTURAL_REFERENCE',
         'REVISE_SITUATED_CULTURAL_REFERENCE',
         'ACQUIRE_SOCIAL_VOCAL_COORDINATION','NO_CHANGE'}
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


def admit(actor,experience,event_ref,candidates):
    """All-or-nothing psychic admission even for a multi-effect LLM proposal.

    Caller owns an actor object whose identity may be held elsewhere. Validate
    and apply on a detached candidate, then replace content only after every
    operation succeeds. A later rejected effect cannot leave an earlier
    proposed memory, project, or relationship silently installed.
    """
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
            update=copy(found)
            for key in ('cue_terms','locations','effects','status'):
                if key in c:update[key]=copy(c[key])
            try:validate_motif(update,actor['forms'])
            except InvalidRelationalMotif as exc:
                raise InvalidDevelopment(str(exc)) from exc
            found.setdefault('motif_history',[]).append({
                'event':event_ref,
                'previous':{key:copy(found.get(key)) for key in
                            ('cue_terms','locations','effects','status')},
                'experience_ref':experience['ref'],'grade':GRADE})
            for key in ('cue_terms','locations','effects','status'):
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
            actor.setdefault('possible_ends',[]).append(end)
            report.append({'kind':op,'possible_end':end_id,
                           'status':'ADMITTED_PROVISIONAL_END_NOT_YET_MOTIVE'})
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
            claimed_later_sign=c.get('later_perceived_cue_ref')
            if (claimed_later_sign is not None and
                    (type(claimed_later_sign) is not str or
                     claimed_later_sign not in later_received)):
                raise InvalidDevelopment('TAKEUP_SIGN_NOT_ACTOR_RECEIVED')
            if claimed_later_sign is None and len(later_received)==1:
                # One received sign is a *possible contextual anchor*, not
                # proof it caused the new concern or that the actor knows why.
                claimed_later_sign=next(iter(later_received))
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
            if 'means' in c and (not isinstance(c['means'],list) or not all(isinstance(x,str) for x in c['means'])):
                raise InvalidDevelopment('INVALID_PROJECT_MEANS')
            if 'means' in c and any(x not in ACTIONS for x in c['means']):
                raise InvalidDevelopment('UNSUPPORTED_ACTIVITY_MEANS')
            if 'priority' in c:validate_activity_priority(c['priority'])
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
            actor['traces' if op=='TRACE' else 'memories'].append(entry)
            report.append({'kind':op,'ref':ref,'status':'ADMITTED_SOURCEFREE_FICTIONAL'})
        elif op=='CHANGE_OTHER_MODEL':
            # What this actor expects of the Other is not the Other's actual state.
            other=c.get('other_ref')
            if not isinstance(other,str) or not other or other==actor['id']:
                raise InvalidDevelopment('INVALID_OTHER_REFERENCE')
            if experience.get('reciprocated_partner')!=other:
                raise InvalidDevelopment('OTHER_NOT_ENCOUNTERED_IN_THIS_EXPERIENCE')
            if not isinstance(c.get('hypothesis'),str) or not c.get('hypothesis'):
                raise InvalidDevelopment('EMPTY_RELATIONAL_HYPOTHESIS')
            actor['other_models'].setdefault(other,[]).append({
                'hypothesis':c['hypothesis'],'event':event_ref,
                'confidence':c.get('confidence','tentative'),
                'grade':GRADE,'not_other_objective_truth':True})
            report.append({'kind':op,'other_ref':other,'status':'ADMITTED_SOURCEFREE_FICTIONAL'})
        elif op=='ACQUIRE_HISTORICAL_ORIENTATION':
            try:report.append(acquire_orientation(actor,experience,event_ref,c))
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
    """No invented microepisodes; only coarse sourced period effects, including null.
    Repeated activity can provisionally change scope of an *existing* power if
    explicitly warranted by coverage. This is not a new social memory/event.
    """
    outputs=[]
    for proc in processes:
        if proc.get('kind')=='practice_access' and proc.get('coverage')=='AGGREGATE_MODELED':
            fid=proc.get('form_id')
            if fid in actor['forms'] and proc.get('warrants_scope_change') is True:
                old=copy(actor['forms'][fid].get('scope',{}))
                new_locations=sorted(set(old.get('locations',[])+proc.get('locations',[])))
                actor['forms'][fid]['scope']={**old,'locations':new_locations}
                actor['forms'][fid].setdefault('changes',[]).append({'period':period_ref,'grade':GRADE,
                    'type':'AGGREGATE_MODELED_SCOPE_GENERALIZATION'})
                outputs.append({'kind':'PERIOD_SCOPE_CHANGE','form':fid})
    return outputs
