"""SORACLE R10: a possible end can organize a trial BEFORE becoming a motive.

Read-only prospective horizon + afterlife witness.  The owner of the acquired
possible end remains development.py/actor state.  Neither this projection nor
an LLM can grant bodily capacity, material permission, another person's consent,
or a conscious intention.  A trial is an actual attempted difference, not the
discovery that it worked.

This is an executable SOURCEFREE architectural hypothesis, not developmental
science, a clinical account, or a new canonical SOROK psyche owner.
"""
from .types import copy, stable_id, GRADE


def _present_terms(access):
    terms = set()
    for cue in access.cues:
        if not isinstance(cue, dict):
            continue
        tags = cue.get('tags', [])
        if isinstance(tags, list):
            terms.update(x.casefold() for x in tags if type(x) is str and x)
        kind = cue.get('kind')
        if type(kind) is str and kind:
            terms.add(kind.casefold())
    return terms


def project_trial_horizons(constitution, access, candidate_actions):
    """Attach *prospectable* trials to existing eligible operations.

    There is no new action and no ungrounded means creation: candidates have
    already passed organismic eligibility, context recruitment and inhibition.
    The actual owner still decides whether, why and how an act is attempted.
    A noticed possible end must have a perceived past origin and an actually
    available current cue before it can organize a trial.
    """
    if constitution.actor != access.actor:
        raise ValueError('PROSPECTIVE_ACTOR_IDENTITY_MISMATCH')
    present = _present_terms(access)
    currents, readset = [], []
    op_index = {o.get('action'): o for o in candidate_actions}
    for end in constitution.possible_ends[-128:]:
        if not isinstance(end, dict):
            continue
        if end.get('status') != 'POSSIBLE_NOT_ACQUIRED_MOTIVE':
            continue
        if not (end.get('origin_event') and end.get('experience_ref')
                and end.get('actor_perceived_cue_ref')):
            continue
        cues = end.get('cue_terms', [])
        if (not isinstance(cues, list) or not cues
                or not {x.casefold() for x in cues if type(x) is str} & present):
            continue
        means = end.get('possible_means', [])
        if not isinstance(means, list):
            continue
        qualified = []
        for operation in dict.fromkeys(x for x in means if type(x) is str):
            option = op_index.get(operation)
            if not option:
                continue
            ident = stable_id('end_trial', {
                'actor': constitution.actor,
                'clock': constitution.clock,
                'possible_end': end['id'],
                'operation': operation,
            })
            trial = {
                'trial_id': ident,
                'actor': constitution.actor,
                'as_of_clock': constitution.clock,
                'possible_end_ref': end['id'],
                'operation': operation,
                'origin_event': end['origin_event'],
                'origin_experience_ref': end['experience_ref'],
                'eliciting_actor_action': end.get('eliciting_actor_action'),
                'hypothesized_difference': end.get('possible_object'),
                'matching_present_terms': sorted(
                    {x.casefold() for x in cues if type(x) is str} & present),
                'other_possible_means': sorted(set(
                    x for x in means if type(x) is str and x != operation)),
                'previous_trials': len(end.get('trial_history', [])),
                'is_means_substitution': (
                    end.get('eliciting_actor_action') not in (None, operation)),
                'actor_project_ref': None,
                'not_acquired_durable_motive': True,
                'not_conscious_intention': True,
                'not_a_world_affordance_grant': True,
                'not_a_prediction_of_objective_success': True,
                'grade': GRADE,
            }
            option.setdefault('possible_end_trials', []).append(trial)
            qualified.append(operation)
        if qualified:
            readset.append(end['id'])
            currents.append({
                'kind': 'POSSIBLE_END_RECRUITS_PROSPECTIVE_TRIALS',
                'possible_end_ref': end['id'],
                'offered_eligible_operations': qualified,
                'origin_event': end['origin_event'],
                'trial_not_a_motive': True,
                'untried_alternatives_remain_unknown': True,
                'grade': GRADE,
            })
    return {'currents': currents, 'readset': sorted(set(readset)),
            'trials_offered': sum(len(o.get('possible_end_trials', []))
                                  for o in candidate_actions),
            'no_automatic_durable_project': True, 'grade': GRADE}


def select_bounded_exploratory_trial(options):
    """Small offline policy, NOT a general theory of choosing possible ends.

    It can try one specifically recruited, bodily eligible, unopposed operation
    where no already established project is competing. A semantic model may
    select another licensed trial through the same actor-scoped identity.
    """
    if any(o.get('project_courses') for o in options):
        return None
    options_with_trial = [
        (o, t) for o in options for t in o.get('possible_end_trials', [])
        if o.get('psychodynamic_status') != 'UNRESOLVED_CONTRADICTION'
        and o.get('preproject_recruitment', {}).get('status') not in (
            'ACQUIRED_NONPROJECT_WITHHOLD', 'UNRESOLVED_PREPROJECT_CONTRADICTION')
    ]
    # Do not award the choice to a more elaborately described end.
    if len({(t['possible_end_ref'], t['operation'])
            for _, t in options_with_trial}) != 1:
        return None
    if not options_with_trial:
        return None
    option, trial = options_with_trial[0]
    return {
        'action': option['action'],
        'possible_end_trial_id': trial['trial_id'],
        'project_id': None,
        'purpose_selection_grade':
            'SOURCEFREE_TRIAL_NOT_CONSCIOUS_PURPOSE_OR_DURABLE_MOTIVE',
        'semantic_grade': 'SOURCEFREE_BOUNDED_EXPLORATION_HYPOTHESIS',
    }


def record_possible_end_trial(actor, experience, event_ref, proposal):
    """Admit an actually attempted trial into the *existing* possible end.

    Development invokes this within its atomic actor-state candidate transaction.
    Attempt provenance was frozen prior to objective world settlement, while
    the afterlife reads only the personally available experience. A successful
    operation cannot prove motive satisfaction or the causal role of a cue.
    """
    if experience.get('actor') != actor.get('id') or not event_ref:
        raise ValueError('POSSIBLE_END_TRIAL_ACTOR_MISMATCH')
    trial = proposal.get('trial')
    if type(trial) is not dict:
        raise ValueError('POSSIBLE_END_TRIAL_NOT_ISSUED')
    if trial.get('actor') != actor['id']:
        raise ValueError('POSSIBLE_END_TRIAL_FOREIGN_ACTOR')
    if trial.get('operation') != experience.get('own_action'):
        raise ValueError('POSSIBLE_END_TRIAL_ACTION_NOT_EXPERIENCED')
    felt = experience.get('felt_enactment') or {}
    if not experience.get('participated') or felt.get('attempted_operation') != trial['operation']:
        raise ValueError('POSSIBLE_END_TRIAL_NOT_ATTEMPTED')
    matches = [e for e in actor.get('possible_ends', [])
               if e.get('id') == trial.get('possible_end_ref')]
    if len(matches) != 1 or matches[0].get('status') != 'POSSIBLE_NOT_ACQUIRED_MOTIVE':
        raise ValueError('POSSIBLE_END_TRIAL_NO_LIVE_END')
    end = matches[0]
    if (end.get('origin_event') == event_ref or
            trial['operation'] not in end.get('possible_means', []) or
            trial.get('origin_event') != end['origin_event']):
        raise ValueError('POSSIBLE_END_TRIAL_INVALID_HISTORY')
    if trial.get('actor_project_ref') is not None:
        raise ValueError('POSSIBLE_END_TRIAL_NOT_A_PROJECT')
    refs = [c.get('id') for c in experience.get('perceived_cues', [])
            if isinstance(c, dict) and type(c.get('id')) is str]
    trial_id = stable_id('lived_end_trial', {
        'actor': actor['id'], 'possible_end': end['id'],
        'event': event_ref, 'option': trial.get('trial_id'),
    })
    if any(t.get('id') == trial_id for t in end.get('trial_history', [])):
        raise ValueError('POSSIBLE_END_TRIAL_ALREADY_RECORDED')
    witness = {
        'id': trial_id,
        'original_situated_trial_ref': trial['trial_id'],
        'operation': trial['operation'],
        'event_ref': event_ref,
        'experience_ref': experience.get('ref'),
        'actor_experienced_status': experience.get('status'),
        'received_sign_refs': sorted(set(refs)),
        'eliciting_possible_end_ref': end['id'],
        'original_end_origin_event': end['origin_event'],
        'means_substitution_proposed_before_event': bool(
            trial.get('is_means_substitution')),
        'experience_proves_cause': False,
        'world_success_or_motive_fulfillment': 'NOT_INFERRED',
        'untried_means_results': 'UNKNOWN_NOT_OBSERVED',
        'not_a_conscious_self_report': True,
        'grade': GRADE,
    }
    end.setdefault('trial_history', []).append(witness)
    return {'kind': 'RECORD_POSSIBLE_END_TRIAL',
            'trial_history_ref': trial_id, 'possible_end': end['id'],
            'status': 'REAL_ATTEMPT_NOT_DURABLE_PROJECT', 'grade': GRADE}
