"""R9 sourcefree independent continuation: lived time does not wait for the user.

A scheduler chooses WHO gets an opportunity to continue; the ACTOR-OWNED
semantic/psychodynamic planner chooses WHAT to attempt. The existing world
owner settles it. This module neither invents an act nor bypasses another
person's independent decision. Scheduler ranks are not motive/agency scores.
"""
from math import isfinite

GRADE = 'SOURCEFREE_PROVISIONAL_SCHEDULER_NOT_HUMAN_VOLITION'
MAX_BEATS = 24
NEED_THRESHOLDS = {'nutrition': .42, 'rest': .40, 'comfort': .35}


def _bounded_body(actor):
    body = actor.get('body')
    if not isinstance(body, dict):
        raise ValueError('INITIATIVE_MISSING_BODY')
    for field in ('nutrition','rest','comfort','motor','sensor','language'):
        val = body.get(field)
        if isinstance(val, bool) or not isinstance(val, (float,int)) or not isfinite(val) or not 0 <= val <= 1:
            raise ValueError('INITIATIVE_INVALID_BODY_'+field.upper())
    return body


def situated_actor_opportunities(world, actors, local_counts=None):
    """Inspect actual situated bodies and material co-presence; do not assign ends.

    Urgency is only a scheduling reason to give an actor a decision occasion,
    not a claim of intended purpose. Co-presence does not grant coaction.
    """
    if not isinstance(actors, dict) or not isinstance(world, dict):
        raise ValueError('INITIATIVE_INVALID_WORLD_OR_ACTORS')
    if not isinstance(world.get('clock'), int) or world['clock'] < 0:
        raise ValueError('INITIATIVE_INVALID_CLOCK')
    positions = world.get('positions', {})
    if not isinstance(positions, dict):
        raise ValueError('INITIATIVE_INVALID_POSITIONS')
    counts = local_counts or {}
    candidates = []
    for aid, actor in sorted(actors.items()):
        if actor.get('id') != aid:
            raise ValueError('INITIATIVE_ACTOR_IDENTITY_MISMATCH')
        if aid not in positions or positions[aid] not in world.get('sites',{}):
            # Do not invent an available room or a lived opportunity.
            continue
        body = _bounded_body(actor)
        unmet = sorted(k for k,threshold in NEED_THRESHOLDS.items() if body[k] < threshold)
        cosituated = [other for other, where in positions.items()
                      if other != aid and where == positions[aid] and other in actors]
        active_projects = [p.get('id') for p in actor.get('projects', [])
                           if isinstance(p, dict) and p.get('status') == 'active'
                           and isinstance(p.get('id'), str)]
        count = counts.get(aid, 0)
        if type(count) is not int or count < 0:
            raise ValueError('INITIATIVE_INVALID_LOCAL_HISTORY')
        candidates.append({
            'actor': aid, 'as_of_clock': world['clock'], 'location': positions[aid],
            'unmet_body_conditions': unmet,
            'co_present_actor_refs': sorted(cosituated),
            'unexecuted_project_context_refs': sorted(active_projects),
            'decisions_in_this_interval': count,
            'priority_tuple': (len(unmet) > 0, -count, len(unmet)),
            'grade': GRADE, 'does_not_select_action_or_motive': True,
        })
    return candidates


def choose_next_actor(world, actors, local_counts=None):
    candidates = situated_actor_opportunities(world, actors, local_counts)
    if not candidates:
        return None
    # Material urgency offers a turn, but does not determine its action.
    # Repeated choices in the interval rotate before returning to one actor.
    candidates.sort(key=lambda c: (c['decisions_in_this_interval'],
                     -len(c['unmet_body_conditions']), c['actor']))
    return candidates[0]


def continue_life(ledger_read, actor_read, advance, beats=1, *, initial_counts=None):
    """High-resolution continuation without any player command or injected act.

    `advance(actor)` must be the existing unmodified actor-selected runtime
    step that resolves the independent world and persists objective history.
    Each beat re-reads changed world and actors. A blocked or refused act is
    still an actually settled beat. No simulated unperformed dialogue.
    """
    if type(beats) is not int or not 1 <= beats <= MAX_BEATS:
        raise ValueError('INITIATIVE_UNSUPPORTED_BEAT_BUDGET')
    if not all(callable(fn) for fn in (ledger_read, actor_read, advance)):
        raise TypeError('INITIATIVE_REQUIRES_EXISTING_OWNER_PORTS')
    # The continuing owner may supply actual committed opportunity counts.
    # Never infer motives or activities from the scheduling history.
    if initial_counts is not None and (type(initial_counts) is not dict or
            any(type(k) is not str or type(v) is not int or v<0 for k,v in initial_counts.items())):
        raise ValueError('INITIATIVE_INVALID_LOCAL_HISTORY')
    records, counts = [], dict(initial_counts or {})
    for _ in range(beats):
        world = ledger_read()
        actors = actor_read()
        decision = choose_next_actor(world, actors, counts)
        if decision is None:
            break
        aid = decision['actor']
        # No `requested_action`, beneficiary, target, consent override, or
        # privileged inner state is provided by this scheduler.
        result = advance(aid)
        if not isinstance(result, dict) or result.get('actor') != aid or not result.get('receipt'):
            raise ValueError('INITIATIVE_OWNER_RETURN_UNQUALIFIED')
        counts[aid] = counts.get(aid, 0) + 1
        records.append({
            'actor':aid, 'objective_receipt':result['receipt'],
            'previous_clock':decision['as_of_clock'],
            'new_clock':result.get('clock'),
            'body_need_priority_not_action_motive':decision['unmet_body_conditions'],
            'actor_selection':result.get('selection_grade', 'UNKNOWN'),
            'sourcefree_scheduler_not_user_injected_act': True,
            'grade':GRADE,
        })
    return {'beats_requested':beats,'beats_committed':len(records),
            'events':records,'no_player_action_injected':True,
            'unperformed_ordinary_life_not_fabricated':True,'grade':GRADE}