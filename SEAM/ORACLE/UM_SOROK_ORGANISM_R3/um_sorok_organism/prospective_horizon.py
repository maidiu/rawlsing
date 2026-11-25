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
from .reflective_regulation import private_end_ground


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


def project_trial_horizons(constitution, access, candidate_actions,
                           functional_correspondences=()):
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
        private_ground=private_end_ground(constitution.memories,end,constitution.actor,
                                           access.location,constitution.clock)
        if not (end.get('origin_event') and end.get('experience_ref')
                and (end.get('actor_perceived_cue_ref') or private_ground)):
            continue
        if end.get('genesis_family')=='ACTUAL_PRIVATE_REHEARSAL' and not private_ground:
            continue
        cues = end.get('cue_terms', [])
        original_match=({x.casefold() for x in cues if type(x) is str}
                        & present) if isinstance(cues,list) else set()
        # A previously experienced but NOT DURABLY GENERALIZED functional
        # correspondence can license one attempt in a new context without
        # pretending the observer's shared label is the child's concept.
        bridge_matches=[b for b in functional_correspondences
                        if b.get('possible_end_ref')==end.get('id')]
        bridge=(bridge_matches[0] if len(bridge_matches)==1 else None)
        # The very same material object can remain accessible even if
        # learned language has not yet captured a shared 'object category'.
        # The referential match is analyst/world-qualified, NOT asserted as
        # a preverbal explicit concept.
        source_object=end.get('origin_material_object_ref')
        # The actually sensed particular Other can remain a prospective
        # address even when today's generic public care sign is absent.
        # This proves no knowledge of that Other's future willingness.
        qualified_other=end.get('addressed_party_ref')
        other_continuity=(type(qualified_other) is str
            and any(c.get('kind')=='coactor_present'
                and c.get('source_actor')==qualified_other
                for c in access.cues if type(c) is dict))
        object_continuity=(
            type(source_object) is str and
            any(c.get('material_object_ref')==source_object
                for c in access.cues if type(c) is dict))
        if source_object is not None:
            # A shared analyst token 'material_object' is not evidence that
            # this child has generalized a good from object A to object B.
            # Keep the particular source until a qualified future operation
            # can bind a different actor-recognizable correspondence.
            if not object_continuity:
                continue
        elif not original_match and bridge is None and not other_continuity and not private_ground:
            continue
        means = end.get('possible_means', [])
        if not isinstance(means, list):
            continue
        # A new means is a one-trial local possibility, not a mutation of
        # the end's durable repertoire. Only the actual issued bridge can
        # license it, and it must still be a situated eligible operation.
        bridge_operation=bridge.get('candidate_operation') if bridge else None
        if bridge_operation is not None:
            means=([*means,bridge_operation] if original_match else [bridge_operation])
        historically_perceived_other=end.get('addressed_party_ref')
        if historically_perceived_other is not None:
            if type(historically_perceived_other) is not str:
                raise ValueError('GENETIC_TRIAL_INVALID_PERSON_REFERENCE')
            # A previously perceived responder is a possible future
            # address, never a guaranteed available person or response.
            if not any(c.get('kind')=='coactor_present'
                       and c.get('source_actor')==historically_perceived_other
                       for c in access.cues if type(c) is dict):
                continue
        # The actual history of attempted means is a NEW prospective
        # distinction. Prior technical execution cannot establish that the
        # end was fulfilled or which untried alternative would fare better.
        tried = [t for t in end.get('trial_history', [])
                 if isinstance(t, dict)
                 and type(t.get('operation')) is str
                 and type(t.get('event_ref')) is str]
        tried_operations = {t['operation'] for t in tried}
        trial_history_refs = [t['id'] for t in tried if type(t.get('id')) is str]
        qualified = []
        for operation in dict.fromkeys(x for x in means if type(x) is str):
            option = op_index.get(operation)
            if not option:
                continue
            # An R34 novel-means bridge is consumed only by its own new
            # operation, never by an unrelated original-cue trial.
            op_bridge=bridge if bridge_operation in (None,operation) else None
            ident = stable_id('end_trial', {
                'actor': constitution.actor,
                'clock': constitution.clock,
                'possible_end': end['id'],
                'operation': operation,
                'functional_bridge':op_bridge.get('binding_ref') if op_bridge else None,
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
                'matching_present_terms': sorted(original_match),
                'functional_bridge_ref':op_bridge.get('binding_ref') if op_bridge else None,
                'historical_analogy_is_provisional':bool(op_bridge),
                'conditional_means_revision_ref':(
                    op_bridge.get('conditional_means_revision_ref') if op_bridge else None),
                'same_object_world_continuity_not_actor_concept':bool(object_continuity),
                'source_material_object_ref':(source_object if object_continuity else None),
                'source_qualified_addressee_ref':historically_perceived_other,
                'addressee_present_but_consent_independent':(
                    historically_perceived_other is not None),
                'present_particular_responder_continuity':bool(other_continuity),
                'other_possible_means': sorted(set(
                    x for x in means if type(x) is str and x != operation)),
                'previous_trials': len(tried),
                'actual_prior_trial_history_refs': trial_history_refs[-32:],
                'prior_mean_attempted': operation in tried_operations,
                'recognized_open_means_contrast': (
                    bool(tried_operations) and operation not in tried_operations),
                'means_contrast_grade':
                    'HISTORICALLY_DIFFERENTIATED_ATTEMPT_NOT_RESULT_COMPARISON',
                'is_means_substitution': (
                    end.get('eliciting_actor_action') not in (None, operation)),
                'actor_project_ref': None,
                'not_acquired_durable_motive': True,
                'not_conscious_intention': True,
                'not_a_world_affordance_grant': True,
                'not_a_prediction_of_objective_success': True,
                'grade': GRADE,
            }
            if private_ground:
                trial['private_rehearsal_ref']=private_ground['id']
                trial['not_current_world_sign_or_recollected_fact']=True
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
                'historically_tried_means': sorted(tried_operations),
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
    if not options_with_trial:
        return None
    unique = {(t['possible_end_ref'], t['operation']): (o,t)
              for o,t in options_with_trial}
    # A singular untried alternative for ONE previously explored possibility
    # can supply an exploratory *variation*. It is a defeasible sourcefree
    # policy, not an empirical rule that all persons prefer novelty.
    if len(unique) > 1:
        ends = {t['possible_end_ref'] for _,t in unique.values()}
        untried = [(o,t) for o,t in unique.values()
                   if t.get('recognized_open_means_contrast')]
        if len(ends) != 1 or len(untried) != 1:
            return None
        option, trial = untried[0]
    else:
        option, trial = next(iter(unique.values()))
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
    if end.get('genesis_family')=='ACTUAL_PRIVATE_REHEARSAL':
        ground=private_end_ground(actor.get('memories',[]),end,actor['id'],
                                   experience.get('location'),experience.get('clock',-1))
        if (not ground or trial.get('private_rehearsal_ref')!=ground['id']
                or (experience.get('own_practical_selection') or {}).get('possible_end_trial')!=trial):
            raise ValueError('PRIVATE_END_TRIAL_UNQUALIFIED_REHEARSAL')
    novel=trial['operation'] not in end.get('possible_means',[])
    if novel:
        matches=[b for b in actor.get('functional_bindings',[])
                 if b.get('id')==trial.get('functional_bridge_ref')
                 and b.get('actor')==actor['id']
                 and b.get('possible_end_ref')==end['id']
                 and b.get('status') in ('POSSIBLE_FUNCTIONAL_SIMILARITY_NOT_BELIEF',
                                          'ACQUIRED_CONDITIONAL_FUNCTIONAL_MEANS')
                 and b.get('scope')=='ONE_QUALIFIED_PROSPECTIVE_TRIAL'
                 and b.get('candidate_operation')==trial['operation']
                 and b.get('dissimilar_means_basis',{}).get('later_location')==experience.get('location')]
        if len(matches)!=1:
            raise ValueError('POSSIBLE_END_TRIAL_UNQUALIFIED_NOVEL_MEANS')
        binding=matches[0]
        if binding['status']=='ACQUIRED_CONDITIONAL_FUNCTIONAL_MEANS':
            if (not binding.get('revision_history')
                    or trial.get('conditional_means_revision_ref')!=binding['revision_history'][-1]['id']):
                raise ValueError('POSSIBLE_END_TRIAL_STALE_CONDITIONAL_MEANS')
        elif (trial.get('conditional_means_revision_ref') is not None
              or any(t.get('functional_bridge_ref')==binding['id']
                     for t in end.get('trial_history',[]))):
            raise ValueError('POSSIBLE_END_TRIAL_UNQUALIFIED_NOVEL_MEANS')
    if (end.get('origin_event') == event_ref or
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
        'functional_bridge_ref': trial.get('functional_bridge_ref'),
        'conditional_means_revision_ref':trial.get('conditional_means_revision_ref'),
        'means_substitution_proposed_before_event': bool(
            trial.get('is_means_substitution')),
        'experience_proves_cause': False,
        'world_success_or_motive_fulfillment': 'NOT_INFERRED',
        'untried_means_results': 'UNKNOWN_NOT_OBSERVED',
        'not_a_conscious_self_report': True,
        'grade': GRADE,
    }
    if end.get('genesis_family')=='ACTUAL_PRIVATE_REHEARSAL':
        witness['private_rehearsal_ref']=end['private_rehearsal_ref']
    end.setdefault('trial_history', []).append(witness)
    return {'kind': 'RECORD_POSSIBLE_END_TRIAL',
            'trial_history_ref': trial_id, 'possible_end': end['id'],
            'status': 'REAL_ATTEMPT_NOT_DURABLE_PROJECT', 'grade': GRADE}
