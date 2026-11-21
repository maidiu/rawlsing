"""R8 historically acquired self-regulation, not a sovereign will module.

An actual actor may acquire a *practice* for organizing later initiative. The
practice is an ordinary actor-owned form with tendencies read by the inherited
psychodynamic engine; bodily/world constraints and other currents still govern.
This candidate is fictional sourcefree psychological construction, not native
CAN/ADP theory or proof of introspective accuracy.
"""
import hashlib
import json
import math

GRADE = 'SOURCEFREE_RESEARCH_PROVISIONAL'


def _ref(name, value):
    raw = json.dumps(value, sort_keys=True, ensure_ascii=False,
                     allow_nan=False, separators=(',', ':'))
    return name + '_' + hashlib.sha256(raw.encode('utf8')).hexdigest()[:16]


def acquire_reflective_regulation(actor, experience, event_ref, proposal,
                                  allowed_actions):
    """Build a learned form after an actor's real enacted, experienced activity.

    Must depend on an actual earlier actor-owned practice or undertaking. A
    language threshold gates ONLY a reflective self-description, not agency,
    desire, primitive goal-directedness, anticipation, or nonverbal inhibition.
    Future action still requires bodily eligibility and the world's actual
    permissions; opposition is not resolved by creating this practice.
    """
    if experience.get('actor') != actor.get('id') or not event_ref:
        raise ValueError('REFLECTIVE_ACTOR_IDENTITY_MISMATCH')
    body = actor.get('body', {})
    language, regulation = body.get('language'), body.get('regulation')
    if (isinstance(language, bool) or not isinstance(language,(int,float)) or
            not math.isfinite(language) or language < .35 or
            isinstance(regulation, bool) or not isinstance(regulation,(int,float)) or
            not math.isfinite(regulation) or regulation < .20):
        raise ValueError('REFLECTIVE_CAPACITY_NOT_YET_AVAILABLE')
    enactment = experience.get('felt_enactment') or {}
    if (not experience.get('participated') or
            experience.get('status') not in ('PERFORMED','PARTIAL') or
            not experience.get('own_action') or
            enactment.get('attempted_operation') != experience['own_action']):
        raise ValueError('REFLECTIVE_NO_ENACTED_ACTOR_ACTIVITY')
    target = proposal.get('future_operation')
    if type(target) is not str or target not in allowed_actions:
        raise ValueError('REFLECTIVE_NEW_UNLICENSED_OPERATION')
    tendency = proposal.get('recruitment_polarity')
    if tendency not in ('APPROACH','WITHHOLD'):
        raise ValueError('REFLECTIVE_UNSUPPORTED_RECRUITMENT')
    # An analyst cannot fabricate a personal source merely by citing a future
    # project. It must already be owned by this particular actor.
    source = proposal.get('historical_source_ref')
    known = set(actor.get('forms', {})) | {
        p.get('id') for p in actor.get('projects', []) if isinstance(p,dict)}
    if type(source) is not str or source not in known:
        raise ValueError('REFLECTIVE_UNOWNED_HISTORICAL_SOURCE')
    seen = {c['id']: c for c in experience.get('perceived_cues', [])
            if isinstance(c,dict) and isinstance(c.get('id'), str)}
    sign_id = proposal.get('perceived_cue_ref')
    if sign_id not in seen:
        raise ValueError('REFLECTIVE_UNEXPERIENCED_SIGN')
    tags = seen[sign_id].get('tags', [])
    if (not isinstance(tags,list) or not tags or len(tags)>16 or
            any(type(t) is not str or not t.strip() for t in tags)):
        raise ValueError('REFLECTIVE_INVALID_CONTEXT_CUES')
    location = actor.get('location')
    if type(location) is not str or not location:
        raise ValueError('REFLECTIVE_NO_ACTUAL_LOCATION')
    # This is not a direct action entitlement, nor an introspectively certain
    # motive. It is a recruitable, fallible self-organizing operation.
    ident = _ref('regulation',{'actor':actor['id'],'event':event_ref,
                              'source':source,'operation':target,'polarity':tendency})
    if ident in actor.get('forms', {}):
        raise ValueError('REFLECTIVE_DUPLICATE_FORM')
    form = {'id': ident, 'actor':actor['id'], 'kind':'PRACTICE',
            'content':'self-organizing practice with respect to '+target.lower(),
            'cues':sorted(set(t.strip().casefold() for t in tags)),
            'enables':[], 'tendencies':[{'action':target,'polarity':tendency,
                                       'cue_terms':sorted(set(t.strip().casefold() for t in tags))}],
            'scope':{'locations':[location]},
            'strength':.4, 'body_min':0, 'access':'ACQUIRED_REFLECTIVE_PRACTICE',
            'lifecycle':'ACTIVE','origin':[event_ref],
            'historical_source_ref':source,
            'actor_enactment_ref':experience['ref'],
            'actor_received_cue_ref':sign_id,
            'conscious_intention':'PROVISIONAL_PRACTICE_NOT_FULL_CAUSAL_EXPLANATION',
            'does_not_override_other_currents':True,
            'does_not_grant_world_feasibility':True,
            'source_grade':GRADE}
    # Development owner commits atomically on detached actor; this helper
    # makes its only actor-local change to that staged copy.
    actor.setdefault('forms', {})[ident] = form
    return {'kind':'ACQUIRE_REFLECTIVE_REGULATION','form':ident,
            'historical_source_ref':source, 'polarity':tendency,
            'future_operation':target,'not_sovereign_agency':True,'grade':GRADE}