"""R8: preproject acquired solicitation in the existing actor expectation owner.

This is an explicitly fictional, sourcefree candidate—not a human learning law.
A body may be solicited by an experience before it can name or choose a project.
No world fact, consciousness, successful outcome, or Other's conduct is inferred.
"""
import hashlib
import json
from copy import deepcopy

GRADE = 'SOURCEFREE_RESEARCH_PROVISIONAL'
MODES = frozenset(('APPROACH', 'WITHHOLD', 'AMBIVALENT'))
# Restricted to existing low-level organismic operations. A semantic model
# cannot install competence in an operation not already available in the body.
ORIENTING_OPERATIONS = frozenset(('ORIENT', 'SIGNAL', 'WAIT', 'REST'))


def _id(tag, value):
    raw = json.dumps(value, sort_keys=True, separators=(',', ':'),
                     ensure_ascii=False, allow_nan=False)
    return tag + '_' + hashlib.sha256(raw.encode('utf8')).hexdigest()[:16]


def _received(experience):
    return {x['id']: x for x in experience.get('perceived_cues', [])
            if isinstance(x, dict) and isinstance(x.get('id'), str)}


def _tags(cue):
    terms = cue.get('tags', [])
    if not isinstance(terms, list) or any(not isinstance(t, str) for t in terms):
        raise ValueError('INVALID_ACTOR_SENSORY_TERMS')
    # Descriptors are ANALYST markers of a discriminable signal, not infant words.
    return sorted({t.strip().casefold() for t in terms if t.strip()})


def admit_preproject_anticipation(actor, experience, event_ref, candidate):
    """Owner-called after admitted actor experience; returns an actor record.

    Requires a literally received cue, explicit target operation, and a mode.
    An actor has no adult motive, concept or known world outcome as a result.
    The model's conjecture is fallible; sourcefree, actor-local, and event-bound.
    """
    if experience.get('actor') != actor.get('id') or not event_ref:
        raise ValueError('PREPROJECT_IDENTITY_MISMATCH')
    seen = _received(experience)
    cue_id = candidate.get('perceived_cue_ref')
    if cue_id not in seen:
        raise ValueError('PREPROJECT_UNEXPERIENCED_SIGN')
    action = candidate.get('possible_operation')
    if action not in ORIENTING_OPERATIONS:
        raise ValueError('PREPROJECT_UNLICENSED_OPERATION')
    mode = candidate.get('orientation_mode')
    if mode not in MODES:
        raise ValueError('PREPROJECT_INVALID_ORIENTATION')
    if not experience.get('participated') and not seen:
        raise ValueError('PREPROJECT_NO_EXPOSURE')
    cue = seen[cue_id]
    tokens = _tags(cue)
    if not tokens:
        raise ValueError('PREPROJECT_UNDIFFERENTIATED_SIGN')
    if len(tokens) > 16:
        raise ValueError('PREPROJECT_UNBOUNDED_SIGN')
    # The effect is a proposal for altered orientation, not a statement that the
    # infant consciously expected a benefit, or that a consequence occurred.
    recorded = {'id': _id('preproject', {'actor': actor['id'], 'event': event_ref,
                                       'cue': cue_id, 'operation': action}),
                'actor': actor['id'], 'origin_event': event_ref,
                'origin_experience_ref': experience.get('ref'),
                'origin_received_cue_ref': cue_id,
                'discriminant_tags': tokens, 'modality': cue.get('modality', 'unknown'),
                'possible_operation': action, 'orientation_mode': mode,
                'historical_ground_ref': event_ref,
                'project_id': None, 'acquisition': 'PREPROJECT_ORIENTING_CONTINGENCY',
                'conceptual_access': 'NONDECLARATIVE_NOT_ACTOR_PROPOSITION',
                'expectation_grade': 'PROVISIONAL_SENSORY_PRACTICAL_NOT_MOTIVE',
                'world_consequence': 'NOT_INFERRED',
                'causal_cue_interpretation': 'NOT_ESTABLISHED',
                'source_grade': GRADE, 'revisions': []}
    if any(e.get('id') == recorded['id'] for e in actor.get('expectations', [])):
        raise ValueError('PREPROJECT_DUPLICATE_ACQUISITION')
    actor.setdefault('expectations', []).append(recorded)
    return {'kind': 'ACQUIRE_PREPROJECT_ANTICIPATION', 'expectation': recorded['id'],
            'operation': action, 'not_a_motive': True, 'grade': GRADE}


def revise_preproject_anticipation(actor, experience, event_ref, candidate):
    """A later qualified sign changes orientation; world/counterfactuals remain open."""
    if actor.get('id') != experience.get('actor') or not event_ref:
        raise ValueError('PREPROJECT_IDENTITY_MISMATCH')
    identity = candidate.get('expectation_ref')
    prior = next((x for x in actor.get('expectations', [])
                  if x.get('id') == identity and
                  x.get('acquisition') == 'PREPROJECT_ORIENTING_CONTINGENCY'), None)
    if prior is None:
        raise ValueError('PREPROJECT_UNKNOWN_EXPECTATION')
    if prior['origin_event'] == event_ref:
        raise ValueError('PREPROJECT_RETROACTIVE_REVISION')
    sign = candidate.get('perceived_cue_ref')
    if sign not in _received(experience):
        raise ValueError('PREPROJECT_REVISION_UNSEEN_SIGN')
    mode = candidate.get('orientation_mode')
    if mode not in MODES:
        raise ValueError('PREPROJECT_INVALID_ORIENTATION')
    prior['revisions'].append({'event': event_ref, 'experience_ref': experience.get('ref'),
                               'perceived_cue_ref': sign,
                               'prior_mode': prior['orientation_mode'],
                               'new_mode': mode,
                               'not_world_verdict': True, 'grade': GRADE})
    prior['orientation_mode'] = mode
    return {'kind': 'REVISE_PREPROJECT_ANTICIPATION',
            'expectation': identity, 'new_mode': mode, 'grade': GRADE}


def recruit_preproject_anticipations(constitution, access, options):
    """Produce currents and practical possibility, not a sovereign action choice.

    Repeated descriptions of ONE historical ground do not add votes; genuinely
    different grounds remain DISTINCT, rather than forcibly added or maxed.
    Incompatible currents are exposed as a contradiction, not resolved here.
    Only presently accessible cues recruit. No invented memory or world event.
    """
    if constitution.actor != access.actor:
        raise ValueError('PREPROJECT_ACTOR_MISMATCH')
    presented = {tag for cue in access.cues for tag in _tags(cue)}
    currents, readset = [], []
    recognized = {}
    for record in constitution.expectations:
        if record.get('acquisition') != 'PREPROJECT_ORIENTING_CONTINGENCY':
            continue
        if not presented.intersection(record.get('discriminant_tags', [])):
            continue
        operation = record.get('possible_operation')
        if operation not in ORIENTING_OPERATIONS:
            continue
        # A historical ground may be multiply described without multiplying
        # the pressure it exerts. Ambiguous copies get one conflicting group.
        ground = (operation, record.get('historical_ground_ref') or record['id'])
        recognized.setdefault(ground, []).append(record)
    qualified = {}
    for (operation, ground), records in sorted(recognized.items()):
        modes = sorted({r['orientation_mode'] for r in records})
        pol = modes[0] if len(modes) == 1 else 'AMBIVALENT'
        refs = sorted(r['id'] for r in records)
        current = {'kind': 'HISTORICALLY_ACQUIRED_PREPROJECT_SOLICITATION',
                   'operation': operation, 'orientation_mode': pol,
                   'historical_ground_ref': ground,
                   'constituent_expectation_refs': refs,
                   'multiple_descriptions_not_multiple_drives': len(records) > 1,
                   'possible_not_necessary_action': True,
                   'not_a_conscious_reason': True,
                   'grade': GRADE}
        currents.append(current)
        readset.extend(refs)
        qualified.setdefault(operation, []).append(current)
    for option in options:
        op = option.get('action')
        if op not in qualified:
            continue
        sets = qualified[op]
        approach = [c for c in sets if c['orientation_mode'] == 'APPROACH']
        withhold = [c for c in sets if c['orientation_mode'] == 'WITHHOLD']
        ambivalent = [c for c in sets if c['orientation_mode'] == 'AMBIVALENT']
        # The actor can remain capable while a current inhibits enactment.
        status = ('UNRESOLVED_PREPROJECT_CONTRADICTION' if
                  (approach and withhold) or ambivalent else
                  'ACQUIRED_NONPROJECT_APPROACH' if approach else
                  'ACQUIRED_NONPROJECT_WITHHOLD')
        option['preproject_recruitment'] = {
            'status': status,
            'ground_refs': [c['historical_ground_ref'] for c in sets],
            'source_count_distinct': len(sets),
            'no_automatic_choice_or_motive': True, 'grade': GRADE}
        option.setdefault('basis', []).extend(
            ['preproject:' + str(c['historical_ground_ref']) for c in sets])
    return {'currents': currents, 'readset': sorted(set(readset)),
            'distinct_historical_ground_count': len(recognized),
            'not_an_intent_selection': True, 'grade': GRADE}


def fallback_nonproject_orientation(options):
    """Explicitly weak fictional fallback: cannot supersede other activities.

    This intentionally only decides an otherwise UNSPECIFIED organismic
    orientation when exactly one available action has acquired solicitation.
    Contradiction, no cue, or continuing other projects => no injected choice.
    An external semantic provider may instead propose refusal/inaction.
    """
    if any(o.get('project_courses') for o in options):
        return None
    eligible = [o for o in options
                if o.get('preproject_recruitment', {}).get('status') ==
                'ACQUIRED_NONPROJECT_APPROACH' and
                o.get('action') in ('ORIENT', 'SIGNAL')]
    contested = any(o.get('preproject_recruitment', {}).get('status') ==
                    'UNRESOLVED_PREPROJECT_CONTRADICTION' for o in options)
    if len(eligible) != 1 or contested:
        return None
    return {'action': eligible[0]['action'], 'project_id': None,
            'purpose_selection_grade':
            'FICTIONAL_PREPROJECT_ORIENTATION_NOT_CONSCIOUS_INTENTION',
            'basis': ['HISTORICALLY_ACQUIRED_SENSORY_ORIENTATION'],
            'semantic_grade': 'SOURCEFREE_FALLBACK_NOT_UNIVERSAL_BEHAVIOR'}