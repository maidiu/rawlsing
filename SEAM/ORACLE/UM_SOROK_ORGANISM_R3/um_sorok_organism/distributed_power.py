"""SORACLE R11 / Astra 2,7,8,9: distributed practical power has history.

The event owner keeps objective contributions and independent coactor decisions.
The actor keeps a narrower, source-qualified history of participating, sensing
support, being assisted and attempting an operation.  A previously participated
joint operation can make another CONDITIONAL attempt possible on a later
occasion. Neither the supporter's consent nor independent mastery is imported.

These are provisional read/programming relations, not identified psychological
learning laws or a canonical replacement for PFF / ADP / world authorities.
"""
from .types import copy, stable_id, GRADE

# Only existing world-defined cooperative operations can admit coactor
# invitations. The world authorizes each Other's contribution afresh.
COOPERATIVE_OPERATIONS = frozenset(
    ('SIGNAL','SING','PRACTICE','MAKE_SPACE','SHARE'))


def record_actor_participation(actor, experience, actual, event_ref,
                               *, body_before=None, body_after=None):
    """Record what this actor underwent, NOT what the world secretly knew.

    This routine is called only after an independently settled event and a
    qualified experience. It must not write any Other's self-understanding.
    """
    if type(actor) is not dict or type(experience) is not dict:
        raise ValueError('PARTICIPATION_REQUIRES_ACTOR_AND_EXPERIENCE')
    if actor.get('id') != experience.get('actor') or type(event_ref) is not str:
        raise ValueError('PARTICIPATION_ACTOR_OR_EVENT_MISMATCH')
    if not (experience.get('participated') or experience.get('perceived_cues')):
        return None
    own_action = experience.get('felt_enactment') or {}
    operation = own_action.get('attempted_operation')
    partner = experience.get('reciprocated_partner')
    if partner is not None and (type(partner) is not str or
                                not experience.get('perceived_cues') or not operation):
        # Objective co-presence never by itself proves experienced cooperation.
        partner = None
    signs=[c['id'] for c in experience.get('perceived_cues',[])
           if type(c) is dict and type(c.get('id')) is str]
    if not operation and not partner and not experience.get('felt_effect'):
        # Witnessing an arbitrary nearby event is not an acquired relation to
        # the act's production; experience remains retained elsewhere.
        return None
    status=experience.get('status','UNKNOWN')
    ref=stable_id('participation',{'actor':actor['id'],'event':event_ref,
        'experience':experience.get('ref'), 'operation':operation})
    if any(x.get('id')==ref for x in actor.get('participation_history',[])):
        return {'kind':'PREEXISTING_PARTICIPATION_HISTORY','ref':ref,
                'not_a_new_event':True,'grade':GRADE}
    bodily=[]
    for key in ('comfort','rest','arousal','nutrition','pain','motor'):
        if (type(body_before) is dict and type(body_after) is dict
                and type(body_before.get(key)) in (int,float)
                and type(body_after.get(key)) in (int,float)):
            bodily.append({'feature':key,'prior':body_before[key],
                           'after':body_after[key],
                           'source':'ACTUAL_ACTOR_BODY_DELTA',
                           'not_an_explanation_of_cause':True})
    record={
        'id':ref,'actor':actor['id'],'event_ref':event_ref,
        'experience_ref':experience.get('ref'),
        'own_attempted_operation':operation,'own_status':status,
        'reciprocated_partner_actor_visible':partner,
        'received_cue_refs':sorted(set(signs)),
        'felt_effect_grade':experience.get('felt_effect'),
        'bodily_differences_objective_analytic_not_actor_beliefs':bodily,
        'joint_participation_perceived':bool(partner and operation),
        'assistance_attribution':
            ('POSSIBLE_CONTINGENCY_NOT_ESTABLISHED_INDEPENDENT_SKILL'
             if partner and operation else
             'NO_ASSISTANCE_INFERENCE'),
        'unassisted_competence':'UNDETERMINED',
        'counterpart_future_readiness':'UNDETERMINED_BY_ONE_ENCOUNTER',
        'other_private_motives':'NOT_OBSERVED',
        'source_grade':GRADE,
    }
    actor.setdefault('participation_history',[]).append(record)
    return {'kind':'RETAIN_EXPERIENCED_PARTICIPATION',
            'participation_ref':ref,
            'possible_assistance_source':partner,
            'no_skill_or_love_deduction':True,'grade':GRADE}


def _present_counterparts(access):
    return {c.get('source_actor') for c in access.cues
            if type(c) is dict and c.get('kind')=='coactor_present'
            and type(c.get('source_actor')) is str}


def conditional_assistance_options(constitution, access, option):
    """Offer a real future invitation *only* through witnessed support history.

    If the counterpart is no longer present, the dependency persists as a
    historical possibility but cannot turn into a currently realizable
    coactor choice. A new invitation triggers the Other's own separate policy.
    """
    if constitution.actor != access.actor:
        raise ValueError('ASSISTANCE_ACTOR_MISMATCH')
    operation=option.get('action')
    if operation not in COOPERATIVE_OPERATIONS:
        return []
    participants=_present_counterparts(access)
    if not participants:
        return []
    history=getattr(constitution,'participation_history',[])
    grounded={}
    for row in history[-256:]:
        if (row.get('joint_participation_perceived')
                and row.get('own_attempted_operation')==operation
                and row.get('reciprocated_partner_actor_visible') in participants
                and row.get('event_ref')):
            key=row['reciprocated_partner_actor_visible']
            grounded.setdefault(key,[]).append(row)
    offered=[]
    for counterpart,rows in sorted(grounded.items()):
        source_refs=sorted(set(r['event_ref'] for r in rows))
        # An earlier lone interruption and later genuinely reciprocated
        # cooperation can produce an actor-specific acquired practice. It is
        # stronger evidence of a *conditional way to try together* than mere
        # repetition, but it cannot supply the other's future independent act.
        practiced=[x for x in getattr(constitution,'joint_practices',[])
            if x.get('actor')==constitution.actor
            and x.get('coactor_ref')==counterpart
            and x.get('operation')==operation
            and x.get('status')==(
                'ACQUIRED_CONDITIONAL_COORDINATION_NOT_DYAD_MASTERY')
            and all(type(t) is str for t in x.get('source_participation_refs',[]))]
        qualified=practiced[-1] if practiced else None
        offered.append({
            'option_id':stable_id('conditional_assistance_option',{
                'actor':constitution.actor,'clock':constitution.clock,
                'operation':operation,'other':counterpart,'sources':source_refs}),
            'actor':constitution.actor,'as_of_clock':constitution.clock,
            'operation':operation,'project_id':None,
            'grounds_status':(
                'HISTORICALLY_ACQUIRED_CONDITIONAL_JOINT_PRACTICE'
                if qualified else
                'ACTOR_PREVIOUSLY_EXPERIENCED_CONTINGENT_COACTIVITY'),
            'acquired_joint_practice_ref':qualified['id'] if qualified else None,
            'participation_source_event_refs':source_refs,
            'supporter_actor_ref':counterpart,
            'world_request':{'operation':operation,
                             'addressed_party_ref':counterpart,
                             'material_object_ref':None},
            'binding_status':'OTHER_PRESENT_BUT_INDEPENDENT_RESPONSE_REQUIRED',
            'anticipated_difference':None,
            'beneficiary_as_apprehended':None,
            'expected_assistance':'POSSIBLE_NOT_PROMISED',
            'unassisted_competence':'NOT_INFERRED_FROM_ASSISTED_HISTORY',
            'partner_consent':'MUST_BE_INDEPENDENTLY_AUTHORED',
            'other_motive':'UNKNOWN_NOT_ATTESTED',
            'source_grade':GRADE,
            'not_an_acquired_durable_motive':True,
            'not_an_observed_future':True,
        })
    return offered


def choose_uncompelled_assistance(options, body):
    """A bounded offline *possibility*, not an invariant infant response.

    A body currently experiencing discomfort might direct a previously used
    signal toward an actually present prior respondent. Neither the body nor
    repeated care entitles it to that person's next response. If multiple
    respondents are qualified, the heuristic abstains rather than inventing
    preference. No forced cooperation is issued.
    """
    if type(body) is not dict or type(body.get('comfort')) not in (int,float):
        return None
    if not 0 <= body['comfort'] <= 1 or body['comfort'] > .45:
        return None
    if any(o.get('project_courses') for o in options):
        return None
    choices=[a for o in options if o.get('action')=='SIGNAL'
             for a in o.get('practical_alternatives',[])
             if a.get('grounds_status') in (
                'ACTOR_PREVIOUSLY_EXPERIENCED_CONTINGENT_COACTIVITY',
                'HISTORICALLY_ACQUIRED_CONDITIONAL_JOINT_PRACTICE')]
    if len(choices)==1:
        option=choices[0]
    else:
        # Multiple past respondents do not authorize an arbitrary preferred
        # caregiver. One actor-acquired, source-qualified *different* joint
        # practice may now differentiate the prospective invitation.
        practiced=[x for x in choices if x.get('grounds_status')==(
            'HISTORICALLY_ACQUIRED_CONDITIONAL_JOINT_PRACTICE')]
        if len(practiced)!=1:return None
        option=practiced[0]
    return {
        'action':'SIGNAL','project_id':None,
        'practical_option_id':option['option_id'],
        'purpose_selection_grade':
          'SOURCEFREE_NEED_CONDITIONED_CONTINGENT_INVITATION_NOT_MOTIVE',
        'semantic_grade':'SOURCEFREE_SITUATED_SUPPORT_PROPOSAL',
    }
