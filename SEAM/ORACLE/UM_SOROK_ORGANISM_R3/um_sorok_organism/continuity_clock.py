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


def continue_to_discontinuity(runtime, horizon=30, processes=None):
    """Actual period and actor step, rather than an invented diary montage.

    A due obligation gives its bearer an OCCASION, not a forced CARE action.
    The next actor attempt goes through native research actor policy and world.
    An overdue obligation with unrepresented microhistory is unresolved, not
    proof of immoral abandonment.
    """
    if type(horizon) is not int or not 1<=horizon<=MAX_HORIZON:
        raise ValueError('CONTINUITY_UNSUPPORTED_HORIZON')
    if processes is not None and (
            type(processes) is not list or len(processes)>512):
        raise ValueError('CONTINUITY_INVALID_PERIOD_PROCESS_LIST')
    world=runtime.ledger.world(runtime.world_id)[1]
    actors=runtime.ledger.actors()
    target=next_discontinuity(world,actors,horizon)
    if target is None:
        aggregate=runtime.background(horizon,processes=processes)
        return {'historical_discontinuity':None,
                'ordinary_interval_receipt':aggregate['receipt'],
                'high_resolution_actor_event':None,
                'unwritten_microevents_remain_unknown':True,
                'grade':GRADE}
    advance=target['at']-world['clock']
    ordinary=None
    if advance>0:
        ordinary=runtime.background(advance,processes=processes)
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


def continue_pre_encounter(runtime, subject_id, target_age_days, *,
                           horizon_days=365, autonomous_beats=2,
                           max_segments=240, period_processes=None):
    """Construct historical time *before* the user encounters this person.

    This composes the EXISTING sourcefree owners: material interruptions,
    aggregate ordinary life, actor-selected activity, independent Others,
    and cold-persisted world/psyche. Neither the user nor this scheduler
    chooses the parents' or child's actions.

    Reaching a modeled age is not scientific adult-person construction, an
    adult social-role transfer, an invented diary, a first user meeting,
    or permission to disclose another actor's private history.
    """
    if type(subject_id) is not str or not subject_id:
        raise ValueError('PRE_ENCOUNTER_SUBJECT_REQUIRED')
    for value, low, high, code in (
        (target_age_days, 1, 120*365, 'PRE_ENCOUNTER_INVALID_TARGET_AGE'),
        (horizon_days, 1, MAX_HORIZON, 'PRE_ENCOUNTER_INVALID_HORIZON'),
        (autonomous_beats, 0, 24, 'PRE_ENCOUNTER_INVALID_BEAT_BUDGET'),
        (max_segments, 1, 240, 'PRE_ENCOUNTER_INVALID_SEGMENT_BUDGET'),
    ):
        if type(value) is not int or not low <= value <= high:
            raise ValueError(code)
    if period_processes is not None and (
            type(period_processes) is not list or len(period_processes)>512):
        raise ValueError('PRE_ENCOUNTER_INVALID_PERIOD_PROCESSES')
    actors = runtime.ledger.actors()
    if subject_id not in actors or actors[subject_id].get('id') != subject_id:
        raise ValueError('PRE_ENCOUNTER_UNREGISTERED_SUBJECT')
    initial = actors[subject_id].get('age_days')
    if type(initial) is not int or initial < 0:
        raise ValueError('PRE_ENCOUNTER_INVALID_SUBJECT_AGE')
    if target_age_days <= initial:
        raise ValueError('PRE_ENCOUNTER_TARGET_NOT_IN_FUTURE')
    # A finite budget is checked *before* making any persistent transition.
    # An unforeseen real discontinuity may still consume an additional segment;
    # then a complete partial-state receipt is returned without fake rollback.
    minimum = (target_age_days - initial + horizon_days - 1)//horizon_days
    if minimum > max_segments:
        raise ValueError('PRE_ENCOUNTER_SEGMENT_BUDGET_INSUFFICIENT')

    segments = []
    committed_beats = 0
    for _ in range(max_segments):
        present = runtime.ledger.actor(subject_id)[1]
        before = present['age_days']
        if before >= target_age_days:
            break
        span = min(horizon_days, target_age_days-before)
        # Material reproduction is forwarded to the existing R13 period
        # allocator, which validates exact source, location, scarce hours,
        # caregiver cost and historical interval BEFORE its own commit.
        kw = ({'processes':period_processes}
              if period_processes is not None else {})
        continuity = runtime.advance_to_discontinuity(horizon=span, **kw)
        later = runtime.ledger.actor(subject_id)[1]
        after = later.get('age_days')
        if type(after) is not int or after < before or after > before+span:
            # The existing continuity owner has already committed or refused
            # its own operation. Never silently pretend to have rolled it back.
            raise ValueError('PRE_ENCOUNTER_SOURCE_AGE_CONTRADICTION')
        entry = {
            'subject_age_before': before,
            'subject_age_after': after,
            'ordinary_interval_receipt':
                continuity.get('ordinary_interval_receipt'),
            'qualified_period_source_refs': (
                [p['source_ref'] for p in period_processes
                 if type(p) is dict and
                 type(p.get('source_ref')) is str]
                if continuity.get('ordinary_interval_receipt')
                and period_processes is not None else []),
            'material_discontinuity': continuity.get('historical_discontinuity'),
            'independently_resolved_event':
                continuity.get('high_resolution_actor_event'),
            'autonomous_event_receipts': [],
            'sourcefree_unwritten_microevents_remain_unknown': True,
        }
        if after == before:
            # A presently due unsettled obligation may give its owner an
            # actual decision turn without advancing the aggregate clock.
            # Do not rewrite its failure into a fictional missed childhood,
            # ignore a pending obligation, or loop forever on it.
            segments.append(entry)
            return _pre_encounter_receipt(
                runtime, subject_id, initial, target_age_days, segments,
                committed_beats, 'HELD_AT_UNRESOLVED_MATERIAL_DISCONTINUITY')
        if autonomous_beats:
            live = runtime.continue_without_user(beats=autonomous_beats)
            actual = live.get('events', [])
            if (live.get('no_player_action_injected') is not True or
                    live.get('beats_committed') != len(actual)):
                raise ValueError('PRE_ENCOUNTER_UNQUALIFIED_AUTONOMOUS_RETURN')
            entry['autonomous_event_receipts'] = [
                event['objective_receipt'] for event in actual]
            committed_beats += len(actual)
        segments.append(entry)

    final_age = runtime.ledger.actor(subject_id)[1]['age_days']
    status = ('HISTORICAL_AGE_CUT_REACHED'
              if final_age == target_age_days
              else 'HELD_AT_FINITE_SEGMENT_BUDGET')
    return _pre_encounter_receipt(
        runtime, subject_id, initial, target_age_days, segments,
        committed_beats, status)


def _pre_encounter_receipt(runtime, subject_id, initial, target, segments,
                           committed_beats, status):
    # Never return materialize(), situated(), the full private actor record,
    # model proposals, hidden parental relationships or a narrated scene.
    actor = runtime.ledger.actor(subject_id)[1]
    world = runtime.ledger.world(runtime.world_id)[1]
    return {
        'subject_ref': subject_id,
        'status': status,
        'initial_modeled_age_days': initial,
        'target_modeled_age_days': target,
        'last_modeled_age_days': actor['age_days'],
        'last_objective_world_clock': world['clock'],
        'aggregate_segments': len(segments),
        'autonomous_beats_committed': committed_beats,
        'historical_receipts': segments,
        'continuing_actor_role_not_reclassified': actor['role'],
        'user_visible_childhood_scenes': False,
        'no_user_action_or_other_person_consent_injected': True,
        'unwritten_events_unknown_not_simulated': True,
        'chronological_age_not_automatic_adult_psychology': True,
        'social_adult_status_not_issued': True,
        'public_first_encounter_not_issued': True,
        'private_actor_and_family_psychology_not_rendered': True,
        'sourcefree_underidentified_maturation': True,
        'partial_historical_commits_not_rolled_back': (
            status != 'HISTORICAL_AGE_CUT_REACHED'),
        'grade': GRADE,
    }
