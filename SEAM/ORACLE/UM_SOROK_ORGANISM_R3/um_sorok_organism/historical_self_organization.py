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


def possible_lived_directional_orientation(actor, experience, event_ref):
    """An acquired polarity offered BY repeated lived courses, not a label.

    Recover real actor-owned genesis witnesses already admitted by psychic_genesis.
    Two different personally attempted events, at different clocks, with
    repeated congruent bodily courses may license a *provisional proposal*.
    This proves neither that the attempted action caused the bodily change
    nor that the actor consciously believes the proposal. One adverse event,
    mixed bodily change, coactor-only relief and sourcefree analyst polarity
    are insufficient. The old hypothesis-only R19 path remains distinguishable.
    """
    if (experience.get('actor') != actor.get('id')
            or type(event_ref) is not str or not event_ref
            or type(experience.get('ref')) is not str
            or experience.get('participated') is not True):
        return []
    action = experience.get('own_action')
    if action not in ACTIONS or (experience.get('felt_enactment') or {}).get(
            'attempted_operation') != action:
        return []
    if not eligible(actor.get('body', {}), action)[0]:
        return []
    site = experience.get('location', actor.get('location'))
    if type(site) is not str or site != actor.get('location'):
        return []
    rows = [r for r in actor.get('lived_genesis_episodes', [])
            if (type(r) is dict and r.get('actor') == actor['id']
                and r.get('location') == site
                and r.get('actor_felt_attempt') == action
                and type(r.get('clock')) is int
                and type(r.get('event_ref')) is str
                and type(r.get('id')) is str)]
    current = [r for r in rows if r.get('event_ref') == event_ref
               and r.get('experience_ref') == experience['ref']]
    if len(current) != 1:
        return []
    now = current[0]
    older = [r for r in rows
             if r['clock'] < now['clock'] and r['event_ref'] != event_ref]
    # Do not create a psychic pattern by counting different descriptions
    # of one event as multiple courses of experience.
    earlier = {}
    for row in older:
        if row['event_ref'] not in earlier or (
                row['clock'], row['id']) > (
                    earlier[row['event_ref']]['clock'],
                    earlier[row['event_ref']]['id']):
            earlier[row['event_ref']] = row
    def direction(row):
        good = row.get('received_relief', {})
        bad = row.get('personally_lived_adverse_course', {})
        if type(good) is not dict or type(bad) is not dict:
            return None
        if good and not bad:
            return 'APPROACH'
        if bad and not good:
            return 'WITHHOLD'
        return None
    mode = direction(now)
    if mode is None:
        return []
    # An actually contradictory intervening lived course makes a simple
    # directional hypothesis UNDERDETERMINED, not merely less confident.
    if any(direction(row) not in (None, mode) for row in earlier.values()):
        return []
    witnessed = sorted(
        (r for r in earlier.values() if direction(r) == mode),
        key=lambda r: (r['clock'], r['id']))
    if not witnessed:
        return []
    first = witnessed[-1]
    # Prevent repeated same-valence receipts from manufacturing infinite
    # pressure. An opposite, separately acquired form may remain possible.
    if any(r.get('acquisition') == 'REPEATED_LIVED_BODY_COURSE'
           and r.get('actor') == actor['id']
           and r.get('operation') == action
           and r.get('location') == site
           and r.get('orientation_mode') == mode
           for r in actor.get('historical_orientations', [])):
        return []
    selected = [first, now]
    cue_ref = next((c.get('id') for c in experience.get('perceived_cues', [])
                    if type(c) is dict and
                    type(c.get('id')) is str and c.get('id') in
                    now.get('received_sign_refs', [])), None)
    basis = {
        'first_lived_episode_ref': first['id'],
        'later_lived_episode_ref': now['id'],
        'source_event_refs': [r['event_ref'] for r in selected],
        'source_experience_refs': [r['experience_ref'] for r in selected],
        'operation': action,
        'location': site,
        'observed_bodily_course': (
            'REPEATED_ACTOR_LIVED_RELIEF' if mode == 'APPROACH'
            else 'REPEATED_ACTOR_LIVED_ADVERSE_COURSE'),
        'two_distinct_episodes_required': True,
        'not_proof_action_caused_body_course': True,
        'not_automatic_motive_or_conscious_explanation': True,
    }
    candidate = {
        'kind': 'ACQUIRE_LIVED_DIRECTIONAL_ORIENTATION',
        'operation': action,
        'orientation_mode': mode,
        'lived_genesis_basis': basis,
        'sourcefree_provisional_not_necessary_adaptation': True,
    }
    if cue_ref is not None:
        candidate['perceived_cue_ref'] = cue_ref
    return [candidate]


def admit_lived_directional_orientation(actor, experience, event_ref, proposal):
    """Same R19 historical owner, source-validated lived genesis, one writer.

    A semantic model can choose to propose NONE or this actual licensed
    candidate. It cannot flip the valence or forge a source event, actor,
    body difference, other mind or unsupported future means.
    """
    possibilities = possible_lived_directional_orientation(
        actor, experience, event_ref)
    if len(possibilities) != 1:
        raise ValueError('LIVED_ORIENTATION_NO_REPEATED_ACTOR_COURSE')
    expected = possibilities[0]
    for field in ('kind', 'operation', 'orientation_mode',
                  'lived_genesis_basis', 'perceived_cue_ref'):
        if proposal.get(field) != expected.get(field):
            raise ValueError('LIVED_ORIENTATION_UNLICENSED_'+field.upper())
    interpretation = proposal.get('interpretive_hypothesis')
    if (interpretation is not None and
            (type(interpretation) is not str or
             not interpretation.strip() or len(interpretation) > 512)):
        raise ValueError('LIVED_ORIENTATION_INVALID_INTERPRETATION')
    emitted = acquire_orientation(actor, experience, event_ref, expected)
    source = next(r for r in actor['historical_orientations']
                  if r['id'] == emitted['ref'])
    source['acquisition'] = 'REPEATED_LIVED_BODY_COURSE'
    source['lived_genesis_basis'] = copy(expected['lived_genesis_basis'])
    source['interpretive_hypothesis_not_causal_truth'] = interpretation
    source['actor_does_not_know_objective_cause'] = True
    source['does_not_upgrade_sourcefree_to_human_science'] = True
    return {'kind': 'ACQUIRE_LIVED_DIRECTIONAL_ORIENTATION',
            'ref': emitted['ref'],
            'status': 'REPEATED_ACTOR_LIVED_PROVISIONAL_RECRUITABLE',
            'source_event_refs': copy(
                expected['lived_genesis_basis']['source_event_refs']),
            'grade': GRADE}


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
