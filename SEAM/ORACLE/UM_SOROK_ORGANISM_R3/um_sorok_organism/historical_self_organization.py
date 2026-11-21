"""R19 sourcefree historically acquired pre-cue and self-organizational pressure.

The existing actor's recorded experience, constitution and developmental owner remain
authoritative. This is neither a second psyche store nor a scalar personality type.
No event, coactor consent, adult motive, cognition or material right is minted here.
"""
from .types import copy, stable_id, GRADE
from .organism import ACTIONS, eligible
from .livelihood_history import qualify_recurrent_work_orientation

MODES = frozenset(('APPROACH', 'WITHHOLD', 'AMBIVALENT'))
REVISIONS = frozenset(('INHIBIT', 'OPPOSE', 'REINSTATE'))
INFANT_OPERATIONS = frozenset(('ORIENT', 'SIGNAL', 'WAIT', 'REST'))


def _received(experience, proposal):
    """An actual actor experience is the only source of formation evidence."""
    cue_ref = proposal.get('perceived_cue_ref')
    cues = experience.get('perceived_cues', [])
    if type(cues) is not list:
        raise ValueError('HISTORICAL_INVALID_EXPERIENCE_CUES')
    received = {c.get('id'): c for c in cues
                if type(c) is dict and type(c.get('id')) is str}
    if cue_ref is not None:
        if type(cue_ref) is not str or cue_ref not in received:
            raise ValueError('HISTORICAL_UNEXPERIENCED_SIGN')
        cue = received[cue_ref]
        modality = cue.get('modality', 'unknown')
        if type(modality) is not str:
            raise ValueError('HISTORICAL_INVALID_MODALITY')
        return {'kind': 'ACTOR_RECEIVED_SIGNAL', 'ref': cue_ref,
                'modality': modality, 'not_a_semantic_concept': True}
    action = experience.get('own_action')
    felt = experience.get('felt_enactment') or {}
    if (experience.get('participated') is True and type(action) is str
            and action in ACTIONS and
            felt.get('attempted_operation') == action):
        return {'kind': 'ACTOR_FELT_OPERATION', 'operation': action,
                'not_an_objective_success_report': True}
    raise ValueError('HISTORICAL_NO_ACTOR_EXPERIENCED_GROUND')


def _actor_event(actor, experience, event_ref):
    if (type(event_ref) is not str or not event_ref or
            experience.get('actor') != actor.get('id') or
            type(experience.get('ref')) is not str):
        raise ValueError('HISTORICAL_ACTOR_EVENT_MISMATCH')


def _action(actor, proposed):
    action = proposed.get('operation')
    if type(action) is not str or action not in ACTIONS:
        raise ValueError('HISTORICAL_UNKNOWN_PHYSICAL_OPERATION')
    if actor.get('body', {}).get('language', 0) < .25 and action not in INFANT_OPERATIONS:
        raise ValueError('HISTORICAL_INFANT_UNEARNED_OPERATION')
    # An acquired pressure may be unable to win; it cannot install a bodily
    # operation unavailable to the organism at acquisition.
    allowed, _ = eligible(actor['body'], action)
    if not allowed:
        raise ValueError('HISTORICAL_BODILY_INELIGIBLE')
    return action


def acquire_orientation(actor, experience, event_ref, proposal):
    _actor_event(actor, experience, event_ref)
    source = _received(experience, proposal)
    action = _action(actor, proposal)
    if (actor['body']['language'] < .25 and source['kind'] ==
            'ACTOR_RECEIVED_SIGNAL' and source['modality'] not in
            ('auditory','visual','tactile','present','olfactory')):
        raise ValueError('HISTORICAL_INFANT_SENSORY_UNGROUNDED')
    mode = proposal.get('orientation_mode')
    if mode not in MODES:
        raise ValueError('HISTORICAL_INVALID_POLARITY')
    work_ground = None
    if 'recurrent_work_practice' in proposal:
        # A model cannot promote an employer's accounting decision to an
        # actor-owned work ethic, competence, permanent class identity or
        # motive. At most it proposes a revisable orientation to the
        # operation the actor has actually attempted across three occasions.
        if action != 'WORK':
            raise ValueError('R25_WORK_HISTORY_CANNOT_GRANT_OTHER_OPERATION')
        work_ground = qualify_recurrent_work_orientation(
            actor, experience, event_ref, proposal['recurrent_work_practice'])
        if proposal.get('perceived_cue_ref') != work_ground[
                'present_received_public_sign_ref']:
            raise ValueError('R25_WORK_ORIENTATION_NO_LIVED_LATEST_SIGN')
    site = experience.get('location', actor.get('location'))
    if type(site) is not str or not site or site != actor.get('location'):
        raise ValueError('HISTORICAL_UNGROUNDED_CONTEXT')
    # One actual episode is not multiple votes because it was described twice.
    ident = stable_id('historical_orientation', {
        'actor': actor['id'], 'event': event_ref, 'operation': action})
    prior = actor.setdefault('historical_orientations', [])
    if any(x.get('id') == ident for x in prior):
        raise ValueError('HISTORICAL_DUPLICATE_EPISODE')
    record = {
        'id': ident, 'actor': actor['id'], 'origin_event': event_ref,
        'origin_experience_ref': experience['ref'], 'source': source,
        'operation': action, 'orientation_mode': mode, 'location': site,
        'origin_clock': experience.get('clock'), 'revisions': [],
        'access': ('NONDECLARATIVE' if actor['body']['language'] < .25
                   else 'NOT_AUTOMATICALLY_CONSCIOUS'),
        'acquisition': 'LIVED_SOURCEFREE_PRACTICAL_ORIENTATION',
        'not_a_project_or_motive': True, 'grade': GRADE,
    }
    if work_ground is not None:
        record['recurrent_livelihood_ground'] = work_ground
        record['source_specificity'] = (
            'THREE_ACTOR_LIVED_WORK_EPISODES_NOT_EMPLOYER_PSYCHOLOGY')
        record['no_inevitable_compliance_resistance_or_conscious_theory'] = True
    prior.append(record)
    return {'kind': 'ACQUIRE_HISTORICAL_ORIENTATION', 'ref': ident,
            'status': 'PROVISIONAL_ACTOR_OWNED_NOT_MOTIVE', 'grade': GRADE}


def revise_orientation(actor, experience, event_ref, proposal):
    _actor_event(actor, experience, event_ref)
    source = _received(experience, proposal)
    ident = proposal.get('orientation_ref')
    row = next((x for x in actor.get('historical_orientations', [])
                if x.get('id') == ident and x.get('actor') == actor['id']), None)
    if row is None:
        raise ValueError('HISTORICAL_FOREIGN_OR_UNKNOWN_ORIENTATION')
    if row['origin_event'] == event_ref or any(
            r['event'] == event_ref for r in row['revisions']):
        raise ValueError('HISTORICAL_SAME_EVENT_REVISION')
    mode = proposal.get('revision_mode')
    if mode not in REVISIONS:
        raise ValueError('HISTORICAL_INVALID_REVISION')
    row['revisions'].append({'event': event_ref, 'experience_ref': experience['ref'],
                             'source': source, 'mode': mode,
                             'prior_history_retained': True, 'grade': GRADE})
    return {'kind': 'REVISE_HISTORICAL_ORIENTATION', 'ref': ident,
            'revision': mode, 'status': 'PROVISIONAL', 'grade': GRADE}


def acquire_operative_self(actor, experience, event_ref, proposal):
    """A learned self-account can become a practice only via an owned precedent."""
    _actor_event(actor, experience, event_ref)
    if actor['body']['language'] < .25:
        raise ValueError('NO_REFLECTIVE_SELF_MODEL_CAPACITY')
    action = _action(actor, proposal)
    source_id = proposal.get('source_orientation_ref')
    source = next((x for x in actor.get('historical_orientations', [])
                   if x.get('id') == source_id and x.get('actor') == actor['id']
                   and x.get('operation') == action), None)
    if source is None or source['origin_event'] == event_ref:
        raise ValueError('SELF_ORGANIZATION_NO_PRIOR_LIVED_ORIENTATION')
    if (experience.get('participated') is not True or
            experience.get('own_action') != action or
            (experience.get('felt_enactment') or {}).get(
                'attempted_operation') != action):
        raise ValueError('SELF_ORGANIZATION_NO_EXERCISED_SELF_PRACTICE')
    claim = proposal.get('claim')
    if type(claim) is not str or not claim.strip() or len(claim) > 512:
        raise ValueError('SELF_ORGANIZATION_INVALID_HYPOTHESIS')
    polarity = proposal.get('orientation_mode')
    if polarity not in MODES:
        raise ValueError('SELF_ORGANIZATION_INVALID_ORIENTATION')
    ident = stable_id('operative_self', {'actor': actor['id'],
        'source': source_id, 'later_event': event_ref, 'operation': action})
    rows = actor.setdefault('self_model', {}).setdefault('operative', [])
    if any(r.get('id') == ident for r in rows):
        raise ValueError('SELF_ORGANIZATION_DUPLICATE')
    record = {
        'id': ident, 'actor': actor['id'], 'claim': claim.strip(),
        'source_orientation_ref': source_id, 'origin_event': event_ref,
        'origin_experience_ref': experience['ref'], 'operation': action,
        'orientation_mode': polarity, 'location': experience.get(
            'location', actor.get('location')), 'revisions': [],
        'source_event': source['origin_event'],
        'not_an_objectively_true_personality': True,
        'not_an_omnipotent_executive': True,
        'grade': GRADE,
    }
    rows.append(record)
    return {'kind': 'ACTOR_SELF_MODEL', 'ref': ident,
            'status': 'OPERATIVE_HISTORICALLY_CONDITIONED_HYPOTHESIS',
            'grade': GRADE}


def revise_operative_self(actor, experience, event_ref, proposal):
    _actor_event(actor, experience, event_ref)
    source = _received(experience, proposal)
    ident = proposal.get('self_organization_ref')
    row = next((r for r in actor.get('self_model', {}).get('operative', [])
                if r.get('id') == ident and r.get('actor') == actor['id']), None)
    if row is None:
        raise ValueError('SELF_ORGANIZATION_FOREIGN_OR_UNKNOWN_REF')
    if row['origin_event'] == event_ref or any(
            r['event'] == event_ref for r in row['revisions']):
        raise ValueError('SELF_ORGANIZATION_SAME_EVENT_REVISION')
    mode = proposal.get('revision_mode')
    if mode not in REVISIONS:
        raise ValueError('SELF_ORGANIZATION_INVALID_REVISION')
    row['revisions'].append({'event': event_ref, 'experience_ref': experience['ref'],
                             'mode': mode, 'source': source,
                             'previous_claim_not_erased': True, 'grade': GRADE})
    return {'kind': 'REVISE_OPERATIVE_SELF_ORGANIZATION', 'ref': ident,
            'revision': mode, 'grade': GRADE}


def _polarities(row):
    mode = row['orientation_mode']
    live = set(MODES - {'AMBIVALENT'}) if mode == 'AMBIVALENT' else {mode}
    for revision in row.get('revisions', []):
        if revision['mode'] == 'INHIBIT':
            live = set()
        elif revision['mode'] == 'REINSTATE':
            live = set(MODES - {'AMBIVALENT'}) if mode == 'AMBIVALENT' else {mode}
        elif revision['mode'] == 'OPPOSE':
            live = {'APPROACH', 'WITHHOLD'}
    return sorted(live)


def pre_cue_pressures(constitution, access):
    """Actor-owned history recruits BEFORE matching any present cue category.

    Site-specific participation is a weak sourcefree practical premise, not a
    universal drive law. An unrecognized present sign and no sign at all may
    leave this historical pressure active. No world action is created here.
    """
    if constitution.actor != access.actor:
        raise ValueError('HISTORICAL_CONSTITUTION_ACTOR_MISMATCH')
    currents = []
    seen = set()
    readset = []
    origins = {r.get('id'): r for r in
               getattr(constitution, 'historical_orientations', [])
               if type(r) is dict and type(r.get('id')) is str}
    sources = [(r, 'NONDECLARATIVE_PRACTICE') for r in
               getattr(constitution, 'historical_orientations', [])]
    sources += [(r, 'ACQUIRED_SELF_ORGANIZATION') for r in
                constitution.self_model.get('operative', [])]
    for row, family in sources:
        if type(row) is not dict or row.get('actor') != constitution.actor:
            continue
        if row.get('location') != access.location:
            continue
        if row.get('operation') not in ACTIONS:
            continue
        # Do not grant capability from psyche, self-belief, or source event.
        allowed, _ = eligible(constitution.body, row['operation'])
        if not allowed:
            continue
        source_id = row.get('id')
        if type(source_id) is not str or source_id in seen:
            continue
        seen.add(source_id)
        readset.append(source_id)
        for polarity in _polarities(row):
            currents.append({
                'kind': 'HISTORICALLY_RECRUITED_PRE_CUE_PRESSURE',
                'source_family': family, 'ref': source_id,
                'action': row['operation'], 'polarity': polarity,
                'origin_event': row['origin_event'],
                'source_modality': (row.get('source',{}).get('modality') or
                    origins.get(row.get('source_orientation_ref'),{}).get(
                        'source',{}).get('modality')),
                'source_self_claim_not_causal_truth': family == 'ACQUIRED_SELF_ORGANIZATION',
                'not_conscious_intent': True, 'not_a_new_project': True,
                'no_present_cue_required': True, 'grade': GRADE,
            })
    return {'currents': currents, 'readset': readset, 'grade': GRADE}
