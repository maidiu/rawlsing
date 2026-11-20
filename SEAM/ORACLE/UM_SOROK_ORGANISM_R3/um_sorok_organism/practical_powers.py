"""SORACLE R12 — A historically exercised power is not an inherent trait.

Actual prior exercise can change the repertoire of *possible attempts*.  A
technical operation performed with help does NOT establish independent mastery;
when help disappears, it can instead license a modest, independently resolved
practice trial.  Solo performance is evidence of prior enactment in that
context, not of universal expertise.  World law, body, institutions and an
Other's future willingness retain independent authority.

Owner-adjacent sourcefree research organ, not native P3/CAN/PFF admission or a
scientifically measured theory of skill acquisition.
"""
from .types import copy, stable_id, GRADE
from .organism import eligible

# The physical vocabulary is inherited.  Substitution is allowed only for
# operations whose plausible component practice is already expressed by the
# existing organism, never generic applied competence for WORK or property.
PRACTICEABLE = frozenset({'SING', 'JOIN', 'MAKE_SPACE', 'PRACTICE'})
REPEATABLE = frozenset({'SING','JOIN','MAKE_SPACE','PRACTICE',
                        'SIGNAL','ASK','INSPECT','REPAIR','WORK',
                        'FEED','SIGN_FOOD_PETITION'})


def retain_exercised_power(actor, experience, objective_ref, location):
    """Preserve actor's personally undergone attempt and conditions of exercise.

    Does not attribute unperceived objective success, acquired skill, conscious
    motive, another actor's purpose, or the ability to perform in a new site.
    """
    if actor.get('id') != experience.get('actor') or type(objective_ref) is not str:
        raise ValueError('EXERCISE_ACTOR_OR_EVENT_MISMATCH')
    felt=experience.get('felt_enactment') or {}
    operation=felt.get('attempted_operation')
    if type(operation) is not str or operation not in REPEATABLE:
        return None
    if not experience.get('participated'):
        return None
    prior=actor.setdefault('power_exercises',[])
    key=stable_id('power_exercise',{'actor':actor['id'],
        'world_event':objective_ref,'operation':operation})
    if any(p.get('id')==key for p in prior):
        return {'kind':'ALREADY_RETAINED_EXERCISE','ref':key,
                'no_duplicate_history':True,'grade':GRADE}
    status=experience.get('status','UNKNOWN')
    partner=experience.get('reciprocated_partner')
    signs=[x.get('id') for x in experience.get('perceived_cues',[])
           if isinstance(x,dict) and type(x.get('id')) is str]
    # Real co-participation is not automatically a causal explanation for what
    # the actor accomplished. Its status is deliberately distinctive.
    configuration=('PERCEIVED_JOINT_PARTICIPATION' if partner and signs else
                   'NO_PERCEIVED_JOINT_PARTICIPATION')
    receipt={
        'id':key,'actor':actor['id'],'event_ref':objective_ref,
        'experience_ref':experience.get('ref'),
        'operation':operation,'encounter_location':location,
        'attempt_status_analyst_receipt':status,
        'felt_attempt':True,
        'participation_configuration':configuration,
        'coactor_as_experienced':partner if configuration==
            'PERCEIVED_JOINT_PARTICIPATION' else None,
        'personally_received_sign_refs':sorted(set(signs)),
        'independent_expertise':'NOT_ESTABLISHED',
        'dependence_on_original_sponsor':'NOT_ESTABLISHED',
        'technical_skill_generalization':'NOT_ESTABLISHED',
        'available_means_in_another_site':'NOT_ESTABLISHED',
        'objective_success_not_a_motive':'NOT_INFERRED',
        'grade':GRADE,
    }
    prior.append(receipt)
    return {'kind':'RETAIN_EXERCISED_POWER',
            'ref':key,'configuration':configuration,
            'qualified_operation':operation,
            'not_an_acquired_motive_or_mastery':True,'grade':GRADE}


def situated_exercised_repertoire(constitution, access):
    """Offer historically specific next operations, never body/work permission.

    The original partner may no longer be available. In that case assisted
    singing supplies at most an opportunity for an independent PRACTICE probe,
    not an unearned ability to realize the full prior joint performance.
    """
    if constitution.actor!=access.actor:
        raise ValueError('EXERCISE_CONSTITUTION_ACCESS_MISMATCH')
    prior=getattr(constitution,'power_exercises',[])
    present={x.get('source_actor') for x in access.cues
             if isinstance(x,dict) and x.get('kind')=='coactor_present'}
    eligible_at_site={}
    held_back=[]
    for x in prior[-512:]:
        if not isinstance(x,dict) or x.get('operation') not in REPEATABLE:
            continue
        if x.get('attempt_status_analyst_receipt')!='PERFORMED':
            # Failure can form history, not automatic future competence.
            held_back.append(x.get('id'))
            continue
        operation=x['operation']
        supported=(x.get('participation_configuration')==
                   'PERCEIVED_JOINT_PARTICIPATION')
        other=x.get('coactor_as_experienced')
        if x.get('encounter_location')!=access.location:
            held_back.append(x.get('id'))
            continue
        if supported and other not in present:
            if operation not in PRACTICEABLE:
                held_back.append(x.get('id'))
                continue
            proposed='PRACTICE'
            significance='INDEPENDENT_PRACTICE_PROBE_NOT_PRIOR_JOINT_MASTERED'
        else:
            proposed=operation
            significance=('PREVIOUSLY_EXERCISED_WITH_POSSIBLE_OTHER'
                          if supported else
                          'SITUATIONALLY_REPEATED_OPERATION_NOT_GLOBAL_MASTERY')
        allowed,_=eligible(constitution.body,proposed)
        if not allowed:
            held_back.append(x.get('id'))
            continue
        row=eligible_at_site.setdefault(proposed,{
            'action':proposed,'source_experience_refs':[],
            'support_configs':set(),'source_event_refs':[],
            'source_actor':constitution.actor,
            'location':access.location,
            'material_rights_not_granted':True,
            'independent_skill_not_inferred':True,
            'actor_motive_not_inferred':True,
            'sourcefree_grade':GRADE,
        })
        row['source_experience_refs'].append(x['experience_ref'])
        row['source_event_refs'].append(x['event_ref'])
        row['support_configs'].add(significance)
    out=[]
    for operation,row in sorted(eligible_at_site.items()):
        if operation in ('WORK','REPAIR') and access.location not in (
                'workshop','home','hall'):
            continue
        out.append({
            'action':operation,
            'basis':sorted(set(row['source_experience_refs'][-24:])),
            'source_event_refs':sorted(set(row['source_event_refs'][-24:])),
            'historical_support_statuses':sorted(row['support_configs']),
            'opportunity':'HISTORICALLY_EXERCISED_POSSIBILITY',
            'score':.115,
            'not_necessarily_a_deliberate_end':True,
            'no_automatic_motive_or_competence':True,
            'world_authority_remains_independent':True,
            'grade':GRADE,
        })
    return {'offered':out,'retained_but_unqualified_refs':sorted(set(
                    x for x in held_back if type(x) is str)),
            'readset':sorted(set(r for row in out
                        for r in row['source_event_refs'])),
            'no_a_priori_independent_mastery':True,'grade':GRADE}
