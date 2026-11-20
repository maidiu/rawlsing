"""R8 second-order MULCH: actual lived bodily differences constrain formation.

This sourcefree, defeasible observer-side *proposal generator* does not install
new psychic fact or prove any human law. It supplies evidence-limited options to
an existing semantic service and typed developmental owner. All source events,
perceived signs and before/after body values originate outside the model.

Importantly: bodily relief is neither proof of experienced pleasure nor proof of
wanting another person, and a cue is NOT proven to have caused that relief.
"""
from math import isfinite

GRADE='SOURCEFREE_HISTORICALLY_CONDITIONED_HYPOTHESIS_NOT_HUMAN_LAW'
SENSES={'visual','auditory','tactile','olfactory','present'}


def _body_value(body,key):
    x=body.get(key)
    if isinstance(x,bool) or not isinstance(x,(float,int)) or not isfinite(x) or not 0<=x<=1:
        raise ValueError('LIVED_GENESIS_INVALID_BODY_'+key.upper())
    return float(x)


def proposals_from_bodily_history(actor,experience,before,after):
    """Propose, but never automatically commit, a minimal nonverbal anticipation.

    Require qualified physical change, received local cue, and an actor body
    with available sensation. Existing acquired same-band organization is NOT
    overwritten: subsequent development requires a separate semantic decision.
    """
    if actor.get('id') != experience.get('actor'):
        raise ValueError('LIVED_GENESIS_ACTOR_MISMATCH')
    if not (experience.get('participated') or experience.get('perceived_cues')):
        return []
    current_body=actor.get('body',{})
    if _body_value(current_body,'language') >= .25:
        return []  # This narrow fallback does not pretend to govern adult formation.
    if _body_value(current_body,'sensor') < .05:
        return []
    comfort=_body_value(after,'comfort')-_body_value(before,'comfort')
    pain=_body_value(after,'pain')-_body_value(before,'pain')
    # A high-level analyst label 'CARE' is not by itself evidence of relief.
    # These thresholds are temporary conservative sourcefree programming knobs,
    # not empirical claims about a developmental law or conscious desire.
    if comfort>=.06 and pain<=.03:
        orientation='APPROACH'
        bodily_basis='COMFORT_INCREASED_CURRENT_INTERVAL'
    elif pain>=.06 or comfort<=-.09:
        orientation='WITHHOLD'
        bodily_basis='PAIN_OR_DISCOMFORT_INCREASED_CURRENT_INTERVAL'
    else:
        return []
    if not (experience.get('felt_effect') or experience.get('felt_enactment')):
        # Mere co-present observation of someone else's bodily benefit is not
        # sufficient for this actor's own anticipation.
        return []
    current=actor.get('expectations',[])
    for cue in experience.get('perceived_cues',[]):
        if not isinstance(cue,dict):continue
        ident,modality=cue.get('id'),cue.get('modality')
        if not isinstance(ident,str) or modality not in SENSES:continue
        band='sensory:'+modality
        if any(x.get('acquisition')=='PREPROJECT_ORIENTING_CONTINGENCY' and
               x.get('possible_operation')=='ORIENT' and
               band in x.get('discriminant_tags',[])
               for x in current):
            continue
        return [{'kind':'ACQUIRE_PREPROJECT_ANTICIPATION',
                 'perceived_cue_ref':ident,
                 'possible_operation':'ORIENT',
                 'orientation_mode':orientation,
                 'historical_evidence_grade':GRADE,
                 'body_difference_basis':bodily_basis,
                 'not_a_claim_of_cause_or_conscious_reason':True}]
    return []