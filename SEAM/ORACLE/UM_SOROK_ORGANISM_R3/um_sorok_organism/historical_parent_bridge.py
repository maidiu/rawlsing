"""SORACLE R11: evidence-constrained adult entrances and blinded interview.

Source survey joints constrain fictional adults, never identify childhood or
provide direct answer keys for later behavior. A blind operational interview
must omit questionnaire-keyed forms and the original sampled target.
SOURCEFREE: conditional inputs must be supplied by a PYAT-qualified caller.
"""
from .types import GRADE, copy, stable_id


def adult_conditioning_input(source_packet):
    """A single adult entrance, without requiring a questionnaire.

    Explicit non-survey modes are authored hypotheses, not native PYAT
    receipts. Legacy survey packets retain their original validation.
    """
    if type(source_packet) is not dict:
        raise ValueError('PARENT_WHOLE_JOINT_MISSING')
    kind=source_packet.get('input_kind','SUPPLIED_SURVEY_CONFIGURATION')
    if kind not in ('SUPPLIED_SURVEY_CONFIGURATION','SAMPLED_SURVEY_CONFIGURATION',
                    'THIN_BIOGRAPHY','AUTHORED_WORLD_HISTORY'):
        raise ValueError('PARENT_UNSUPPORTED_INPUT_KIND')
    answers=source_packet.get('answers',{})
    if type(answers) is not dict:
        raise ValueError('PARENT_WHOLE_JOINT_MISSING')
    if kind in ('THIN_BIOGRAPHY','AUTHORED_WORLD_HISTORY'):
        if answers:
            raise ValueError('PARENT_NONSURVEY_ANSWERS_AMBIGUOUS')
        if (source_packet.get('source_grade')!='EXPLICIT_FICTIONAL_HISTORICAL_INPUT'
                or type(source_packet.get('source_ref')) is not str
                or not source_packet['source_ref'].strip()
                or type(source_packet.get('biographical_context')) is not dict
                or not source_packet['biographical_context']):
            raise ValueError('PARENT_NONSURVEY_CONTEXT_UNQUALIFIED')
    elif not answers:
        raise ValueError('PARENT_NO_OBSERVED_INSTRUMENT')
    return kind,answers


def historically_conditioned_entrances(source_packet):
    kind,answers=adult_conditioning_input(source_packet)
    source=source_packet.get('source_ref','UNVERIFIED_SURVEY_INPUT')
    support=source_packet.get('conditional_support',{})
    if type(support) is not dict:
        raise ValueError('PARENT_INVALID_SUPPORT_PROFILE')
    denominators=support.get('denominators',{})
    if denominators and type(denominators) is not dict:
        raise ValueError('PARENT_INVALID_CONDITIONAL_DENOMINATORS')
    alternatives=source_packet.get('historically_supported_alternatives',[])
    if type(alternatives) is not list:
        raise ValueError('PARENT_INVALID_HISTORICAL_ALTERNATIVES')
    qualified=[]
    # Reject overflow rather than silently thinning supplied rich inputs.
    if len(alternatives)>24:
        raise ValueError('PARENT_HISTORICAL_ALTERNATIVES_CAPACITY_EXCEEDED')
    for index,alt in enumerate(alternatives):
        if type(alt) is not dict or type(alt.get('source_ref')) is not str:
            raise ValueError('PARENT_ALTERNATIVE_WITHOUT_SOURCE_WARRANT')
        if type(alt.get('historical_scope')) is not str:
            raise ValueError('PARENT_HISTORICAL_SCOPE_MISSING')
        qualified.append({
            'candidate_id':stable_id('parent_historical_entrance',
                   {'source':source,'index':index,'alternative':alt}),
            'historical_scope':alt['historical_scope'],
            'source_ref':alt['source_ref'],
            'conditional_observation_ref':alt.get('conditional_observation_ref'),
            'material_practice_constraints':copy(
                alt.get('material_practice_constraints',[])),
            'compatible_but_not_unique_biography':True,
            'not_identified_respondent_childhood':True,
            'evidence_quality':alt.get('grade','UNQUALIFIED_CANDIDATE'),
        })
    return {
        'source_ref':source,
        'input_kind':kind,
        'observed_instrument_size':len(answers),
        'biographical_context':copy(source_packet.get('biographical_context',{})),
        'survey_conditioning_state':('NO_SURVEY_SUPPLIED' if not answers
                                     else 'SUPPLIED_NOT_INDEPENDENTLY_QUALIFIED'),
        'observational_universe':source_packet.get(
            'respondent_universe','UNQUALIFIED'),
        'source_weighting':source_packet.get('weighting','NOT_PROVIDED'),
        'instrument_routing':copy(source_packet.get('routing',{})),
        'conditional_denominators':copy(denominators),
        'alternative_support':copy(support.get('alternatives',[])),
        'historically_supported_alternatives':qualified,
        'historical_specificity_loss':(
            'MISSING_HISTORICAL_BRIDGE' if not qualified else
            'MULTIPLE_UNDERIDENTIFIED_COMPATIBLE_ANTEDECENTS'),
        'fictional_prehistory_not_observed_respondent':True,
        'sampled_answers_not_an_adult_motive_algorithm':True,
        'requires_authorized_PYAT_conditioning':bool(answers),
        'native_PYAT_authority_not_issued_here':True,'grade':GRADE,
    }


def actor_only_interview_packet(actor, instrument, world=None):
    if type(actor) is not dict or actor.get('role')!='adult':
        raise ValueError('BLIND_INTERVIEW_ACTOR_NOT_ADULT')
    if type(instrument) is not list or any(type(q) is not str for q in instrument):
        raise ValueError('BLIND_INTERVIEW_INVALID_INSTRUMENT')
    retained={}
    for fid,f in actor.get('forms',{}).items():
        if type(f) is not dict:continue
        # The fallback adult constructor literally encodes the response in
        # MEDIATOR content. Removing its answer key alone is insufficient.
        if 'asserted_answer' in f or f.get('object') in instrument:
            continue
        retained[fid]=copy(f)
    operative={
        'actor_id':actor['id'],'age_days':actor.get('age_days'),
        'body':copy(actor['body']),
        'acquired_non_questionnaire_forms':retained,
        'activities':copy(actor.get('projects',[])),
        'links':[copy(l) for l in actor.get('links',[])
                 if l.get('source') in retained and l.get('target') in retained],
        'experienced_participation':copy(actor.get('participation_history',[])[-96:]),
        'functional_bindings':copy(actor.get('functional_bindings',[])[-96:]),
        'private_models':copy(actor.get('other_models',{})),
        'self_model':copy(actor.get('self_model',{})),
        'source_measurement_answers_excluded':True,
        'source_identity_excluded':True,
    }
    context=None if world is None else {
        'clock':world.get('clock'),
        'location':world.get('positions',{}).get(actor['id']),
        'material_site':copy(world.get('sites',{}).get(
            world.get('positions',{}).get(actor['id']),{})),
        'no_respondent_source_target':True,
    }
    return {'task':'blind_adult_interview','actor':operative,
            'world_context':context,'instrument':copy(instrument),
            'instruction':'INFER_FROM_FUNCTIONING_ACTOR_ONLY_NO_STORED_SURVEY_KEY',
            'sourcefree_inference_not_empirical_fidelity':True,
            'grade':GRADE}


def render_blind_interview(actor,instrument,semantic,world=None):
    packet=actor_only_interview_packet(actor,instrument,world)
    result=semantic.proposal('blind_adult_interview',packet)
    answers=result.get('responses',{})
    if type(answers) is not dict or set(answers)-set(instrument):
        raise ValueError('BLIND_INTERVIEW_INVALID_PROVIDER_RESPONSE')
    return {
        'responses':copy(answers),
        'unanswered':[q for q in instrument if q not in answers],
        'quality':'INDEPENDENT_ACTOR_ORGANIZATION_PROPOSAL_UNCALIBRATED',
        'provider_grade':getattr(semantic.provider,'grade',
                          'INJECTED_SEMANTIC_PROVIDER_UNVERIFIED'),
        'source_answers_were_unavailable_to_provider':True,
        'whole_joint_correspondence':'NOT_EVALUATED_IN_THIS_CALL',
        'grade':GRADE,
    }


# Selected-route first construction of SEAM/20 and SC-03. This is a
# sourcefree staged forward meeting/conception/birth path, NOT the full
# later-selection/backward-father inverse chronology.
FAMILY_GRADE='EXPLICIT_SOURCEFREE_CONDITIONAL_GENEALOGY'
FAMILY_SOURCE='FICTIONAL_FAMILY_PATHWAY_CANDIDATES'
FAMILY_FIELDS={'id','source_ref','intersection_clock','intersection_site',
               'conception_clock','birth_clock','counterpart_id','counterpart_name',
               'counterpart_packet','child_id','child_name','prior_shared_effects'}

def qualify_family_pathways(world,mother,rows):
    if (mother.get('role')!='adult' or world['positions'].get(mother['id'])!=mother['location']
            or type(rows) is not list or not 1<=len(rows)<=16):
        raise ValueError('FAMILY_PATHWAY_UNQUALIFIED_MATERNAL_SOURCE')
    known=set(world['positions']);ids=set()
    for x in rows:
        if type(x) is not dict or set(x)!=FAMILY_FIELDS:
            raise ValueError('FAMILY_PATHWAY_INVALID_FIELDS')
        if any(type(x[k]) is not str or not x[k].strip() for k in
               ('id','source_ref','intersection_site','counterpart_id','counterpart_name',
                'child_id','child_name','prior_shared_effects')):
            raise ValueError('FAMILY_PATHWAY_INVALID_IDENTITY')
        if (x['id'] in ids or x['counterpart_id'] in known or x['child_id'] in known
                or x['counterpart_id']==x['child_id'] or x['intersection_site'] not in world['sites']
                or x['prior_shared_effects']!='UNMODELED_NO_RETROACTIVE_WRITE'):
            raise ValueError('FAMILY_PATHWAY_OVERLAP_OR_IDENTITY')
        ids.add(x['id'])
        t,c,b=(x[k] for k in ('intersection_clock','conception_clock','birth_clock'))
        if (any(type(v) is not int for v in (t,c,b))
                or not world['clock']<t<c<b<=world['clock']+120*365):
            raise ValueError('FAMILY_PATHWAY_INVALID_CLOCKS')
        adult_conditioning_input(x['counterpart_packet'])
    return {'grade':FAMILY_GRADE,'mother':mother['id'],'proposal_clock':world['clock'],
            'maternal_proposal_state_digest':stable_id('maternal_proposal',mother),
            'candidates':copy(rows),'unknown_prior_shared_effects_not_denied':True,
            'not_empirical_couple_probability_or_reproductive_consent':True}

def situated_family_pathways(world,mother,source):
    if (source.get('grade')!=FAMILY_GRADE or source.get('mother')!=mother['id']
            or world['clock']<=source.get('proposal_clock',world['clock'])
            or world.get('family_genesis',{}).get('selected_pathway')):return []
    # At least one actual lived maternal attempt after proposal, not merely
    # passage of time or a narrative about her development.
    if not any(e.get('actor')==mother['id']
               and e.get('clock',-1)>source['proposal_clock']
               and e.get('own_action') is not None
               for e in mother.get('lived_genesis_episodes',[])):return []
    out=[]
    for x in source['candidates']:
        site=world['sites'][x['intersection_site']]
        if (world['clock']!=x['intersection_clock']
                or world['positions'].get(mother['id'])!=x['intersection_site']
                or x['counterpart_id'] in world['positions'] or x['child_id'] in world['positions']
                or (site.get('access')!='public' and x['counterpart_id'] not in site.get('admitted',[]))):continue
        # Do not put the other candidate's survey or private source packet
        # into the maternal semantic selection call.
        out.append({k:copy(x[k]) for k in ('id','source_ref','intersection_clock',
                        'intersection_site','conception_clock','birth_clock')})
    return out

def family_encounter_evidence(world,selected):
    """An actual directed performed act after roster admission, not a
    proof of reciprocity, sexual consent, affection or shared household."""
    pair={selected['mother'],selected['counterpart']}
    return [copy(e) for e in world.get('public_history',[])
            if e.get('clock',-1)>selected['admitted_clock']
            and e.get('clock',-1)<=world['clock']
            and e.get('status')=='PERFORMED'
            and e.get('action') in ('CARE','FEED','PLEDGE_CARE','SPEAK','SIGNAL')
            and e.get('actor') in pair and e.get('target') in pair
            and e['actor']!=e['target']]
