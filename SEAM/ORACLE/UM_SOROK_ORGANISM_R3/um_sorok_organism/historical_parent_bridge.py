"""SORACLE R11: evidence-constrained adult entrances and blinded interview.

Source survey joints constrain fictional adults, never identify childhood or
provide direct answer keys for later behavior. A blind operational interview
must omit questionnaire-keyed forms and the original sampled target.
SOURCEFREE: conditional inputs must be supplied by a PYAT-qualified caller.
"""
from .types import GRADE, copy, stable_id


def historically_conditioned_entrances(source_packet):
    if type(source_packet) is not dict or type(source_packet.get('answers')) is not dict:
        raise ValueError('PARENT_WHOLE_JOINT_MISSING')
    if not source_packet['answers']:
        raise ValueError('PARENT_NO_OBSERVED_INSTRUMENT')
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
    for index,alt in enumerate(alternatives[:24]):
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
        'observed_instrument_size':len(source_packet['answers']),
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
        'requires_authorized_PYAT_conditioning':True,'grade':GRADE,
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
