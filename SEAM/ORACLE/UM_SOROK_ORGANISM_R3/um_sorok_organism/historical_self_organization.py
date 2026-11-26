"""R19 sourcefree historically acquired pre-cue and self-organizational pressure.

The existing actor's recorded experience, constitution and developmental owner remain
authoritative. This is neither a second psyche store nor a scalar personality type.
No event, coactor consent, adult motive, cognition or material right is minted here.
"""
from .types import copy, stable_id, GRADE
from .organism import ACTIONS, eligible
from .livelihood_history import qualify_recurrent_work_orientation
from .attention_field import possible_monitoring_changes

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
    monitoring_ground = None
    if 'monitoring_basis' in proposal:
        if proposal not in possible_monitoring_changes(actor,experience,event_ref):
            raise ValueError('MONITORING_FORMATION_UNQUALIFIED')
        monitoring_ground=copy(proposal['monitoring_basis'])
    dependency_ground = None
    if 'dependency_ambivalence_basis' in proposal:
        possible=possible_dependency_ambivalence(actor,experience,event_ref)
        if proposal not in possible:
            raise ValueError('DEPENDENCY_AMBIVALENCE_UNQUALIFIED')
        dependency_ground=copy(proposal['dependency_ambivalence_basis'])
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
    if dependency_ground is not None:
        record['acquisition']='LIVED_CONTRADICTORY_PROJECT_COURSE'
        record['dependency_ambivalence_basis']=dependency_ground
        record['not_a_named_emotion_or_relationship_verdict']=True
    if monitoring_ground is not None:
        record['acquisition']='LIVED_DIRECTED_MONITORING_PRACTICE'
        record['monitoring_basis']=monitoring_ground
    prior.append(record)
    return {'kind': 'ACQUIRE_HISTORICAL_ORIENTATION', 'ref': ident,
            'status': 'PROVISIONAL_ACTOR_OWNED_NOT_MOTIVE', 'grade': GRADE}


def _lived_coexperience_field(witness):
    """A historical co-presence FIELD, not a privileged causal Other.

    The actor's actual source-qualified perceptual opportunity may contain
    no one, one Other, or several. All are materially possible. Distinct
    episodes can ground a bounded *situational association* when their
    received co-presence sets match. This neither claims the actor attended
    to each person, nor determines which participant caused a felt outcome.
    A multi-person household must not be erased to make dyadic math easy.
    """
    signs=witness.get('personally_perceived_sign_sources')
    if type(signs) is not list:
        return (False,())
    others=set()
    for sign in signs:
        if type(sign) is not dict:
            return (False,())
        if sign.get('kind')!='coactor_present':
            continue
        ref=sign.get('source_actor')
        if (type(ref) is not str or not ref or
                type(sign.get('cue_ref')) is not str):
            return (False,())
        others.add(ref)
    # Sorted, bounded, immutable field identity; no new inferred relation.
    # A large crowd is not an automatically learned individuated field.
    if len(others)>8:
        return (False,())
    return (True,tuple(sorted(others)))


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
    # The earlier R28 actor+operation+room match over-generalized bodily
    # orientation from one Other to another. A context is RECEIVED,
    # not a statement that the Other caused the body delta.
    qualified_field, coexperienced_others = _lived_coexperience_field(now)
    if not qualified_field:
        return []
    older = [r for r in rows
             if r['clock'] < now['clock'] and r['event_ref'] != event_ref]
    # Do not create a psychic pattern by counting different descriptions
    # of one event as multiple courses of experience.
    earlier = {}
    for row in older:
        known,others=_lived_coexperience_field(row)
        if not known or others != coexperienced_others:
            continue
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
    # A previously acquired polarity is not a lifelong veto on subsequent
    # formation. Look only at the most recent UNINTERRUPTED run of comparable
    # lived courses. Earlier opposite courses remain in actor history and
    # their acquired orientation remains operative: this is a new, possibly
    # opposed organization, NOT the erasure or automatic reversal of the old.
    # A mixed/unknown intervening course interrupts the run too; two matching
    # receipts separated by an opposite course cannot manufacture repetition.
    chronological = sorted(earlier.values(),
                           key=lambda r: (r['clock'], r['id']),
                           reverse=True)
    consecutive = []
    for row in chronological:
        if direction(row) != mode:
            break
        consecutive.append(row)
    if not consecutive:
        return []
    first = consecutive[0]
    # Existing same-polarity history is not another independent pressure.
    # But a previously inhibited organization can be reopened by NEW lived
    # courses rather than being permanently unavailable or cloned.
    matching = [r for r in actor.get('historical_orientations', [])
                if r.get('acquisition') == 'REPEATED_LIVED_BODY_COURSE'
                and r.get('actor') == actor['id']
                and r.get('operation') == action
                and r.get('location') == site
                and r.get('orientation_mode') == mode
                and r.get('lived_genesis_basis',{}).get(
                    'coexperienced_other_refs') == list(coexperienced_others)]
    reopening = None
    if matching:
        if len(matching) != 1:
            return []
        existing = matching[0]
        if _polarities(existing):
            return []
        revisions = existing.get('revisions', [])
        inhibition = revisions[-1] if revisions else {}
        cutoff = inhibition.get('clock')
        # Older unclocked revisions are retained; do not manufacture a
        # temporal ordering or reuse the events that preceded inhibition.
        if (inhibition.get('mode') != 'INHIBIT'
                or type(cutoff) is not int
                or first['clock'] <= cutoff
                or now['clock'] <= cutoff):
            return []
        reopening = existing
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
        'coexperienced_other_refs': list(coexperienced_others),
        'experienced_social_context': (
            'RECURRENT_MULTI_OR_SINGLE_COACTOR_FIELD_NOT_CAUSAL_PROOF'
            if coexperienced_others else
            'NO_OTHER_PERCEIVED_DURING_EPISODES'),
        'other_may_not_have_caused_bodily_course': True,
        'other_consent_intent_and_motive_not_inferred': True,
        'observed_bodily_course': (
            'REPEATED_ACTOR_LIVED_RELIEF' if mode == 'APPROACH'
            else 'REPEATED_ACTOR_LIVED_ADVERSE_COURSE'),
        'two_distinct_episodes_required': True,
        'consecutive_comparable_course_required': True,
        'older_opposing_orientations_not_deleted': True,
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
    if reopening is not None:
        basis['reopened_orientation_ref'] = reopening['id']
        basis['inhibition_event_ref'] = reopening['revisions'][-1]['event']
        basis['inhibition_clock'] = reopening['revisions'][-1]['clock']
        candidate['kind'] = 'REVISE_HISTORICAL_ORIENTATION'
        candidate['orientation_ref'] = reopening['id']
        candidate['revision_mode'] = 'REINSTATE'
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
    if expected['kind'] != 'ACQUIRE_LIVED_DIRECTIONAL_ORIENTATION':
        raise ValueError('LIVED_ORIENTATION_REOPEN_EXISTING_NOT_DUPLICATE')
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
    # Give the already existing pre-cue owner a source-grounded context
    # boundary; don't create a new social-learning graph or world writer.
    source['coexperienced_other_refs'] = copy(expected[
        'lived_genesis_basis']['coexperienced_other_refs'])
    source['interpretive_hypothesis_not_causal_truth'] = interpretation
    source['actor_does_not_know_objective_cause'] = True
    source['does_not_upgrade_sourcefree_to_human_science'] = True
    return {'kind': 'ACQUIRE_LIVED_DIRECTIONAL_ORIENTATION',
            'ref': emitted['ref'],
            'status': 'REPEATED_ACTOR_LIVED_PROVISIONAL_RECRUITABLE',
            'source_event_refs': copy(
                expected['lived_genesis_basis']['source_event_refs']),
            'grade': GRADE}


def possible_counterhistory_release(actor, experience, event_ref):
    """Optional refunctioning of one existing withholding current.
    
    Two later, uninterrupted, personally lived relieving courses of the SAME
    operation and received social field can qualify suspension, not a compulsory
    new positive motive. Body change is not proof of cause or interpersonal safety.
    The original history remains; other contexts and currents remain independent.
    """
    if (experience.get('actor') != actor.get('id')
            or experience.get('participated') is not True
            or experience.get('status') != 'PERFORMED'):
        return []
    operation = experience.get('own_action')
    site = experience.get('location')
    if (operation not in ACTIONS or site != actor.get('location')
            or not eligible(actor['body'], operation)[0]):
        return []
    rows = [r for r in actor.get('lived_genesis_episodes', [])
            if r.get('actor') == actor['id'] and r.get('location') == site
            and r.get('actor_felt_attempt') == operation
            and type(r.get('clock')) is int]
    current = [r for r in rows if r.get('event_ref') == event_ref
               and r.get('experience_ref') == experience.get('ref')]
    if len(current) != 1:
        return []
    now = current[0]
    known, field = _lived_coexperience_field(now)
    if not known or not now.get('received_relief') or now.get(
            'personally_lived_adverse_course') or now.get('unfinished_own_activity'):
        return []
    earlier = [r for r in rows if r['clock'] < now['clock']
               and _lived_coexperience_field(r) == (True, field)]
    if not earlier:
        return []
    previous = max(earlier, key=lambda r: (r['clock'], r['id']))
    if (not previous.get('received_relief') or previous.get(
            'personally_lived_adverse_course') or previous.get('unfinished_own_activity')
            or previous['event_ref'] == event_ref):
        return []
    out = []
    for row in actor.get('historical_orientations', []):
        if (row.get('actor') != actor['id'] or row.get('location') != site
                or row.get('operation') != operation
                or row.get('orientation_mode') != 'WITHHOLD'
                or _polarities(row, field) != ['WITHHOLD']
                or row.get('acquisition') not in (
                    'REPEATED_LIVED_BODY_COURSE',
                    'LIVED_SOURCEFREE_PRACTICAL_ORIENTATION')):
            continue
        origins = [r for r in rows if r.get('event_ref') == row.get('origin_event')
                   and r.get('experience_ref') == row.get('origin_experience_ref')]
        if len(origins) != 1 or _lived_coexperience_field(origins[0]) != (True, field):
            continue
        if (row['acquisition'] == 'REPEATED_LIVED_BODY_COURSE'
                and row.get('coexperienced_other_refs') != list(field)):
            continue
        clocks = [origins[0]['clock']] + [x.get('clock') for x in row['revisions']]
        if any(type(c) is not int for c in clocks) or previous['clock'] <= max(clocks):
            continue
        basis = {'orientation_ref': row['id'], 'operation': operation,
                 'location': site, 'coexperienced_other_refs': list(field),
                 'origin_event_ref': row['origin_event'],
                 'source_event_refs': [previous['event_ref'], event_ref],
                 'source_experience_refs': [previous['experience_ref'], now['experience_ref']],
                 'source_episode_refs': [previous['id'], now['id']],
                 'not_recollection_or_proof_of_safety': True,
                 'not_a_new_approach_or_global_recovery': True}
        out.append({'kind': 'REVISE_HISTORICAL_ORIENTATION',
                    'orientation_ref': row['id'], 'revision_mode': 'INHIBIT',
                    'counterhistory_release_basis': basis})
    return out


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
    revision = {'event': event_ref, 'experience_ref': experience['ref'],
                'clock': experience.get('clock'),
                'source': source, 'mode': mode,
                'prior_history_retained': True, 'grade': GRADE}
    if row.get('acquisition')=='LIVED_DIRECTED_MONITORING_PRACTICE' or 'monitoring_revision_basis' in proposal:
        if proposal not in possible_monitoring_changes(actor,experience,event_ref):
            raise ValueError('MONITORING_REVISION_UNQUALIFIED')
        revision['monitoring_revision_basis']=copy(proposal['monitoring_revision_basis'])
    if 'counterhistory_release_basis' in proposal:
        possibilities = possible_counterhistory_release(actor, experience, event_ref)
        if proposal not in possibilities:
            raise ValueError('COUNTERHISTORY_RELEASE_UNQUALIFIED')
        revision['counterhistory_release_basis'] = copy(
            proposal['counterhistory_release_basis'])
    if 'lived_genesis_basis' in proposal or (
            mode == 'REINSTATE' and
            row.get('acquisition') == 'REPEATED_LIVED_BODY_COURSE'):
        possible = possible_lived_directional_orientation(
            actor, experience, event_ref)
        if len(possible) != 1 or possible[0].get('kind') != (
                'REVISE_HISTORICAL_ORIENTATION'):
            raise ValueError('LIVED_REOPEN_NO_NEW_COMPARABLE_COURSE')
        expected = possible[0]
        for field in ('kind', 'orientation_ref', 'revision_mode',
                      'operation', 'orientation_mode', 'lived_genesis_basis',
                      'perceived_cue_ref'):
            if proposal.get(field) != expected.get(field):
                raise ValueError('LIVED_REOPEN_UNLICENSED_'+field.upper())
        revision['lived_genesis_basis'] = copy(expected['lived_genesis_basis'])
        interpretation = proposal.get('interpretive_hypothesis')
        if (interpretation is not None and
                (type(interpretation) is not str or
                 not interpretation.strip() or len(interpretation) > 512)):
            raise ValueError('LIVED_REOPEN_INVALID_INTERPRETATION')
        revision['interpretive_hypothesis_not_causal_truth'] = interpretation
    row['revisions'].append(revision)
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


def _polarities(row, field=None):
    mode = row['orientation_mode']
    live = set(MODES - {'AMBIVALENT'}) if mode == 'AMBIVALENT' else {mode}
    for revision in row.get('revisions', []):
        if revision['mode'] == 'INHIBIT':
            basis = revision.get('counterhistory_release_basis')
            # Repeated-course forms already recruit only in this field.
            # Earlier R19 orientations may be site-wide; do not globalize
            # counterhistory experienced in one particular social field.
            if (basis is None or row.get('acquisition') == 'REPEATED_LIVED_BODY_COURSE'
                    or (field is not None and list(field) == basis['coexperienced_other_refs'])):
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
        if row.get('acquisition')=='LIVED_DIRECTED_MONITORING_PRACTICE':
            # Attention owner alone consumes this particular orientation.
            # It is not a general motive to ORIENT.
            continue
        if row.get('acquisition')=='LIVED_CONTRADICTORY_PROJECT_COURSE':
            # Specific practical alternatives, not every occurrence of the
            # physical operation, consume this form of historical pressure.
            continue
        if row.get('acquisition') == 'REPEATED_LIVED_BODY_COURSE':
            # R29: pre-symbolic source context, not a current motive cue.
            # Do not recruit an orientation learned amid one specific
            # social field simply because the action/site repeats amid
            # a different constellation of independently acting people.
            active_others={
                c.get('source_actor') for c in access.cues
                if type(c) is dict and c.get('kind')=='coactor_present'
                and type(c.get('source_actor')) is str}
            expected_others = set(row.get('coexperienced_other_refs',[]))
            if active_others != expected_others:
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
        current_field = tuple(sorted({c.get('source_actor') for c in access.cues
            if c.get('kind') == 'coactor_present' and type(c.get('source_actor')) is str}))
        for polarity in _polarities(row, current_field):
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


def possible_dependency_ambivalence(actor,experience,event_ref):
    """A renewed conditional means can remain practically available while
    its actually lived history solicits opposed orientations to using it.

    The historical evidence is actor-owned material/participatory history,
    not a diagnosis of emotion, the Other's intention or a universal law.
    """
    aid=actor.get('id'); clock=experience.get('clock')
    sel=experience.get('own_practical_selection') or {}
    req=sel.get('world_request') or {}
    other=req.get('addressed_party_ref')
    refs=sel.get('selected_project_refs')
    if (experience.get('actor')!=aid or type(clock) is not int
            or experience.get('own_action')!='SIGNAL'
            or experience.get('status') not in ('PARTIAL','BLOCKED')
            or experience.get('participated') is not True
            or sel.get('actor')!=aid
            or sel.get('status')!='ACTOR_POLICY_PRACTICAL_ATTEMPT'
            or req.get('operation')!='SIGNAL' or type(other) is not str
            or type(refs) is not list or len(refs)!=1
            or type(sel.get('option_id')) is not str
            or sel.get('possible_end_trial') is not None
            or not eligible(actor['body'],'SIGNAL')[0]):return []
    ps=[p for p in actor.get('projects',[]) if p.get('id')==refs[0]]
    if len(ps)!=1:return []
    p=ps[0]; bound=p.get('dependency_conditional_means',{}).get('SIGNAL')
    if (not bound or p.get('status')!='active'
            or bound.get('status','ACTIVE')!='ACTIVE'
            or bound.get('counterpart_ref')!=other
            or bound.get('location')!=experience.get('location')):return []
    history=bound.get('revision_history',[])
    if len(history)<2:return []
    suspension,reopening=history[-2:]
    if (suspension.get('new_status')!='SUSPENDED'
            or reopening.get('new_status')!='ACTIVE'
            or suspension.get('basis',{}).get('mode')!='SUSPEND'
            or reopening.get('basis',{}).get('mode')!='REOPEN'
            or reopening.get('basis',{}).get('previous_revision_event_ref')!=suspension.get('event_ref')):return []
    episodes=actor.get('lived_genesis_episodes',[])
    parts=actor.get('participation_history',[])
    def one(eid,eref=None):
        found=[e for e in episodes if e.get('actor')==aid
               and e.get('location')==bound['location']
               and e.get('actor_felt_attempt')=='SIGNAL'
               and e.get('selected_addressed_party_ref')==other
               and e.get('selection_source')=='ACTOR_SITUATED_CANDIDATE_SELECTED_SOURCEFREE'
               and (eid is None or e.get('id')==eid)
               and (eref is None or e.get('event_ref')==eref)]
        return found[0] if len(found)==1 else None
    def witnessed(e,part_ref=None):
        found=[x for x in parts if x.get('actor')==aid
               and x.get('event_ref')==e['event_ref']
               and x.get('experience_ref')==e['experience_ref']
               and x.get('own_attempted_operation')=='SIGNAL'
               and (part_ref is None or x.get('id')==part_ref)]
        return found[0] if len(found)==1 else None
    histories=[]
    for revision,positive in ((suspension,False),(reopening,True)):
        basis=revision['basis']; ers=basis.get('episode_refs',[])
        prs=basis.get('participation_refs',[]); evs=basis.get('event_refs',[])
        if (basis.get('practice_ref')!=bound.get('practice_ref')
                or basis.get('counterpart_ref')!=other
                or basis.get('location')!=bound['location']
                or len(ers)!=2 or len(prs)!=2 or len(evs)!=2
                or revision.get('event_ref')!=evs[-1]):return []
        for er,pr,ev in zip(ers,prs,evs):
            e=one(er,ev)
            if e is None:return []
            x=witnessed(e,pr)
            if x is None:return []
            if positive:
                if (e.get('selected_project_refs')!=[]
                        or e.get('unfinished_own_activity')
                        or not e.get('received_relief',{}).get('nutrition')
                        or not x.get('joint_participation_perceived')
                        or x.get('reciprocated_partner_actor_visible')!=other
                        or x.get('own_status')!='PERFORMED'):return []
            else:
                if (e.get('selected_project_refs')!=[p['id']]
                        or not e.get('unfinished_own_activity')
                        or e.get('received_relief',{}).get('nutrition')
                        or x.get('joint_participation_perceived')
                        or x.get('own_status') not in ('PARTIAL','BLOCKED')):return []
            histories.append(e)
    now=one(None,event_ref)
    if (now is None or now.get('clock')!=clock
            or now.get('experience_ref')!=experience.get('ref')
            or now.get('selected_project_refs')!=refs
            or now.get('selected_practical_option_ref')!=sel['option_id']
            or not now.get('unfinished_own_activity')
            or now.get('received_relief',{}).get('nutrition')):return []
    part=witnessed(now)
    if (part is None or part.get('joint_participation_perceived')
            or part.get('own_status') not in ('PARTIAL','BLOCKED')):return []
    all_rows=histories+[now]
    if any(x['clock']>=y['clock'] for x,y in zip(all_rows,all_rows[1:])):return []
    courses=[c for c in p.get('operational_history',[]) if c.get('event')==event_ref
             and c.get('project')==p['id'] and c.get('operation')=='SIGNAL'
             and c.get('selected_at_actor_attempt') is True
             and c.get('performed_status') in ('PARTIAL','BLOCKED')]
    if len(courses)!=1:return []
    if any(o.get('dependency_ambivalence_basis',{}).get('project_ref')==p['id']
           and o.get('dependency_ambivalence_basis',{}).get('reopening_event_ref')==reopening['event_ref']
           for o in actor.get('historical_orientations',[])):return []
    signs=[c for c in experience.get('perceived_cues',[])
           if c.get('kind')=='performed_signal' and c.get('source_actor')==aid
           and c.get('id') in now.get('received_sign_refs',[])]
    if len(signs)!=1:return []
    basis={'project_ref':p['id'],'practice_ref':bound['practice_ref'],
           'counterpart_ref':other,'location':bound['location'],
           'suspension_event_ref':suspension['event_ref'],
           'reopening_event_ref':reopening['event_ref'],
           'approach_episode_refs':[x['id'] for x in histories[2:]],
           'withhold_episode_refs':[x['id'] for x in histories[:2]]+[now['id']],
           'latest_participation_ref':part['id'],'latest_event_ref':event_ref,
           'not_a_named_emotion_or_future_consent':True}
    return [{'kind':'ACQUIRE_HISTORICAL_ORIENTATION','operation':'SIGNAL',
             'orientation_mode':'AMBIVALENT','perceived_cue_ref':signs[0]['id'],
             'dependency_ambivalence_basis':basis}]


def project_dependency_course_currents(constitution,access,project,operation,binding):
    """Project-specific historical tensions, not a global action veto."""
    if not binding:return []
    out=[]
    for row in getattr(constitution,'historical_orientations',[]):
        if (row.get('actor')!=constitution.actor
                or row.get('acquisition')!='LIVED_CONTRADICTORY_PROJECT_COURSE'
                or row.get('operation')!=operation
                or row.get('location')!=access.location):continue
        basis=row.get('dependency_ambivalence_basis',{})
        if (basis.get('project_ref')!=project['id']
                or basis.get('practice_ref')!=binding.get('practice_ref')
                or basis.get('counterpart_ref')!=binding.get('counterpart_ref')
                or not any(c.get('kind')=='coactor_present'
                           and c.get('source_actor')==basis.get('counterpart_ref')
                           for c in access.cues)):continue
        for polarity in sorted(_polarities(row)):
            out.append({'orientation_ref':row['id'],'polarity':polarity,
                        'project_ref':project['id'],'operation':operation,
                        'counterpart_ref':basis['counterpart_ref'],
                        'origin_event_ref':row['origin_event'],
                        'source_episode_refs':copy(basis[
                            'approach_episode_refs' if polarity=='APPROACH'
                            else 'withhold_episode_refs']),
                        'not_actor_self_knowledge_or_world_outcome':True})
    return out
