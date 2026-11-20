"""SORACLE R11 / Astra 6,7,17,19: ordinary life has discontinuities.

Routine coverage is cheap; a source-qualified deadline, expiring signal or
material interruption gets a detailed *actor-owned* opportunity. No player
chooses the action. This does not invent unperformed micro-events, pretend a
scheduling threshold was an experienced violation, or close other actors'
rights. The actual runtime/world owners still author their own transactions.
"""
from .types import GRADE

MAX_HORIZON=3650


def next_discontinuity(world, actors, horizon):
    if type(horizon) is not int or not 1<=horizon<=MAX_HORIZON:
        raise ValueError('CONTINUITY_UNSUPPORTED_HORIZON')
    clock=world.get('clock')
    if type(clock) is not int or clock < 0:
        raise ValueError('CONTINUITY_INVALID_WORLD_CLOCK')
    end=clock+horizon
    candidates=[]
    for obligation in world.get('scheduled_obligations',[]):
        if not isinstance(obligation,dict) or obligation.get('status')!='PENDING':
            continue
        due=obligation.get('due_clock')
        actor=obligation.get('responsible_actor')
        if type(due) is not int or due < 0:
            raise ValueError('CONTINUITY_INVALID_DUE_CLOCK')
        if actor not in actors:
            # A record remains objectively pending even when its bearer is
            # unavailable; inventing a substitute would be false coactivity.
            continue
        if due<=end:
            candidates.append({'at':max(clock,due),'kind':'OBLIGATION_DUE',
                'actor':actor,'source_ref':obligation.get('id'),
                'not_proof_of_broken_promise':True})
    for cue in world.get('cues',[]):
        if not isinstance(cue,dict):continue
        expiry=cue.get('last_access_clock')
        if type(expiry) is int and clock<expiry+1<=end:
            candidates.append({'at':expiry+1,'kind':'PUBLIC_SIGN_EXPIRES',
                'actor':None,'source_ref':cue.get('id'),
                'expiration_not_actor_forgetting':True})
    candidates.sort(key=lambda d:(d['at'],
                        0 if d['kind']=='OBLIGATION_DUE' else 1,
                        str(d.get('source_ref'))))
    return candidates[0] if candidates else None


def continue_to_discontinuity(runtime, horizon=30):
    """Actual period and actor step, rather than an invented diary montage.

    A due obligation gives its bearer an OCCASION, not a forced CARE action.
    The next actor attempt goes through native research actor policy and world.
    An overdue obligation with unrepresented microhistory is unresolved, not
    proof of immoral abandonment.
    """
    if type(horizon) is not int or not 1<=horizon<=MAX_HORIZON:
        raise ValueError('CONTINUITY_UNSUPPORTED_HORIZON')
    world=runtime.ledger.world(runtime.world_id)[1]
    actors=runtime.ledger.actors()
    target=next_discontinuity(world,actors,horizon)
    if target is None:
        aggregate=runtime.background(horizon)
        return {'historical_discontinuity':None,
                'ordinary_interval_receipt':aggregate['receipt'],
                'high_resolution_actor_event':None,
                'unwritten_microevents_remain_unknown':True,
                'grade':GRADE}
    advance=target['at']-world['clock']
    ordinary=None
    if advance>0:
        ordinary=runtime.background(advance)
    if target['kind']=='PUBLIC_SIGN_EXPIRES':
        return {'historical_discontinuity':target,
                'ordinary_interval_receipt':ordinary['receipt'] if ordinary else None,
                'high_resolution_actor_event':None,
                'expired_sign_not_deleted_from_history':True,
                'unwritten_microevents_remain_unknown':True,'grade':GRADE}
    # A real unsettled material obligation offers a situated initiative turn.
    # Actor may delay, refuse, fulfil, do something else or be physically
    # blocked. That independently enacted result is not the scheduler's act.
    actual=runtime.step(target['actor'])
    return {'historical_discontinuity':target,
            'ordinary_interval_receipt':ordinary['receipt'] if ordinary else None,
            'high_resolution_actor_event':actual['receipt'],
            'actor':actual['actor'],
            'attempted_operation':actual['attempt'],
            'scheduler_did_not_inject_action_or_consent':True,
            'fulfillment_not_inferred_from_elapsed_clock':True,
            'grade':GRADE}
