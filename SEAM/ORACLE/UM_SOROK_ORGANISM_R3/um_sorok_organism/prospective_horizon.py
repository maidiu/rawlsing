"""SORACLE R10 prospective-trial concept integrated into REMONT R10.

Research-grade prospective agency: an actor-owned noticed end can recruit one
already qualified operation as an experiment before an acquired project exists.
An issued trial is not the cause or outcome of world settlement; no success,
Other's consent, conscious intention, or mature motive is inferred.
"""
from .types import copy, stable_id, GRADE


def _terms(access):
    result = set()
    for cue in access.cues:
        if not isinstance(cue, dict):
            continue
        tags = cue.get('tags')
        if type(tags) is list:
            result.update(t.casefold() for t in tags if type(t) is str and t)
        if type(cue.get('kind')) is str:
            result.add(cue['kind'].casefold())
    return result


def project_trial_horizons(constitution, access, candidate_actions):
    """Read-only, actor-and-clock-qualified options over eligible operations.

    Candidate options already reflect embodied, historical and current
    psychodynamic eligibility. A trial NEVER adds an operation to the grammar.
    No private end belongs to another actor, and a *present* actor-readable
    sign is required, not merely an analyst's remembered description.
    """
    if constitution.actor != access.actor:
        raise ValueError('PROSPECTIVE_ACTOR_IDENTITY_MISMATCH')
    present = _terms(access)
    options = {o['action']: o for o in candidate_actions}
    currents, readset = [], set()
    for end in constitution.possible_ends[-128:]:
        if type(end) is not dict or end.get('status') != 'POSSIBLE_NOT_ACQUIRED_MOTIVE':
            continue
        if not (type(end.get('id')) is str and type(end.get('origin_event')) is str
                and type(end.get('experience_ref')) is str
                and type(end.get('actor_perceived_cue_ref')) is str):
            continue
        cues = end.get('cue_terms')
        if type(cues) is not list or any(type(t) is not str for t in cues):
            continue
        intersection = {t.casefold() for t in cues if t} & present
        if not intersection:
            continue
        means = end.get('possible_means')
        if type(means) is not list:
            continue
        actual_prior = [r for r in end.get('trial_history', [])
                        if type(r) is dict and type(r.get('operation')) is str
                        and type(r.get('event_ref')) is str]
        attempted = {r['operation'] for r in actual_prior}
        offered = []
        for op in dict.fromkeys(m for m in means if type(m) is str):
            opt = options.get(op)
            if opt is None:
                continue
            trial = {
                'trial_id': stable_id('end_trial', {'actor': constitution.actor,
                    'clock': constitution.clock, 'end': end['id'], 'operation': op}),
                'actor': constitution.actor,
                'as_of_clock': constitution.clock,
                'possible_end_ref': end['id'],
                'operation': op,
                'origin_event': end['origin_event'],
                'origin_experience_ref': end['experience_ref'],
                'hypothesized_difference': end.get('possible_object'),
                'matching_present_terms': sorted(intersection),
                'actual_prior_trial_history_refs': [r['id'] for r in actual_prior
                    if type(r.get('id')) is str][-32:],
                'prior_mean_attempted': op in attempted,
                'recognized_open_means_contrast': bool(attempted) and op not in attempted,
                'actor_project_ref': None,
                'not_acquired_durable_motive': True,
                'not_conscious_intention': True,
                'not_a_world_affordance_grant': True,
                'not_a_prediction_of_objective_success': True,
                'grade': GRADE,
            }
            opt.setdefault('possible_end_trials', []).append(trial)
            offered.append(op)
        if offered:
            readset.add(end['id'])
            currents.append({
                'kind': 'POSSIBLE_END_RECRUITS_PROSPECTIVE_TRIALS',
                'possible_end_ref': end['id'],
                'offered_eligible_operations': offered,
                'historically_tried_means': sorted(attempted),
                'trial_not_a_motive': True,
                'causal_outcome_unknown': True,
                'grade': GRADE,
            })
    return {'currents': currents, 'readset': sorted(readset),
            'trials_offered': sum(len(x.get('possible_end_trials', [])) for x in candidate_actions),
            'no_automatic_durable_project': True, 'grade': GRADE}


def select_bounded_exploratory_trial(options):
    """Conservative offline option; not a universal rule of human choice."""
    if any(o.get('project_courses') for o in options):
        return None
    entries = [(o, t) for o in options for t in o.get('possible_end_trials', [])
               if o.get('psychodynamic_status') != 'UNRESOLVED_CONTRADICTION'
               and o.get('preproject_recruitment', {}).get('status') not in
                    ('ACQUIRED_NONPROJECT_WITHHOLD', 'UNRESOLVED_PREPROJECT_CONTRADICTION')]
    unique = {(t['possible_end_ref'], t['operation']): (o,t) for o,t in entries}
    if not unique:
        return None
    if len(unique) > 1:
        ends = {t['possible_end_ref'] for _,t in unique.values()}
        untried = [(o,t) for o,t in unique.values()
                   if t.get('recognized_open_means_contrast')]
        if len(ends) != 1 or len(untried) != 1:
            return None
        _, selected = untried[0]
    else:
        _,selected = next(iter(unique.values()))
    return {'action': selected['operation'],
            'possible_end_trial_id': selected['trial_id'],
            'project_id': None,
            'semantic_grade': 'BOUNDED_SOURCEFREE_PROVISIONAL_TRIAL'}


def record_possible_end_trial(actor, experience, event_ref, trial):
    """Record an actually attempted issuer-qualified trial in staged actor state.

    IMPORTANT: callers must have already excluded all model-authored trial
    candidates and supplied an exact pre-world-issued trial from runtime.
    Called by development.admit with the privileged plan packet, never a
    general semantic provider result. The event remains objective and separate.
    """
    if (experience.get('actor') != actor.get('id') or not event_ref
            or type(trial) is not dict or trial.get('actor') != actor.get('id')):
        raise ValueError('UNISSUED_POSSIBLE_END_TRIAL')
    # Check exact issuance identity (including pre-event actor clock), not
    # merely a plausible text ID named by a developmental provider.
    clock = trial.get('as_of_clock')
    if (type(clock) is not int or clock < 0
            or type(trial.get('possible_end_ref')) is not str
            or type(trial.get('operation')) is not str
            or trial.get('trial_id') != stable_id('end_trial', {
                'actor': actor['id'], 'clock': clock,
                'end': trial['possible_end_ref'],
                'operation': trial['operation']})):
        raise ValueError('UNISSUED_POSSIBLE_END_TRIAL')
    if (type(trial.get('trial_id')) is not str or not trial['trial_id']
            or trial.get('operation') != experience.get('own_action')
            or not experience.get('participated')
            or (experience.get('felt_enactment') or {}).get('attempted_operation')
                != trial['operation']):
        raise ValueError('POSSIBLE_END_TRIAL_NOT_ACTUALLY_ATTEMPTED')
    matches = [e for e in actor.get('possible_ends', [])
               if e.get('id') == trial.get('possible_end_ref')]
    if len(matches) != 1 or matches[0].get('status') != 'POSSIBLE_NOT_ACQUIRED_MOTIVE':
        raise ValueError('POSSIBLE_END_TRIAL_NO_LIVE_END')
    end = matches[0]
    if (event_ref == end.get('origin_event')
            or trial.get('origin_event') != end.get('origin_event')
            or trial.get('origin_experience_ref') != end.get('experience_ref')
            or trial['operation'] not in end.get('possible_means', [])
            or trial.get('actor_project_ref') is not None):
        raise ValueError('POSSIBLE_END_TRIAL_INVALID_HISTORY')
    # An actor may attempt one situated end-trial per objective event, even
    # when several possible ends share the same physical means.
    if any(h.get('event_ref') == event_ref for e in actor.get('possible_ends', [])
           for h in e.get('trial_history', []) if type(h) is dict):
        raise ValueError('POSSIBLE_END_TRIAL_EVENT_ALREADY_CONSUMED')
    witnessed = [c.get('id') for c in experience.get('perceived_cues', [])
                 if type(c) is dict and type(c.get('id')) is str]
    record = {
        'id': stable_id('lived_end_trial', {'actor': actor['id'],
            'end': end['id'], 'event': event_ref, 'issued_trial': trial['trial_id']}),
        'original_situated_trial_ref': trial['trial_id'],
        'operation': trial['operation'],
        'event_ref': event_ref,
        'experience_ref': experience.get('ref'),
        'actor_experienced_status': experience.get('status'),
        'received_sign_refs': sorted(set(witnessed)),
        'eliciting_possible_end_ref': end['id'],
        'original_end_origin_event': end['origin_event'],
        'not_a_conscious_self_report': True,
        'untried_means_results': 'UNKNOWN_NOT_OBSERVED',
        'world_success_or_motive_fulfillment': 'NOT_INFERRED',
        'grade': GRADE,
    }
    end.setdefault('trial_history', []).append(record)
    return {'kind': 'RECORD_POSSIBLE_END_TRIAL', 'trial_history_ref': record['id'],
            'possible_end': end['id'],
            'status': 'REAL_ATTEMPT_NOT_DURABLE_PROJECT', 'grade': GRADE}
