"""Actor-situated, activity-qualified psychological pressures (sourcefree R4).

A technical operation is not the motive or object of the activity it serves.
A tendency qualified for one audience/project/purpose does not globally prohibit
that physical operation in unrelated activities. Contradictions are retained,
not converted into a universal avoidance or moral-progress score.

These are provisional actor-acquired functional hypotheses, not clinical science.
"""
from .types import copy, GRADE
from .organism import ACTIONS

POLARITIES = {'APPROACH', 'WITHHOLD'}
CONTEXT_KEYS = ('activity_ref', 'object', 'counterpart', 'locations')


def validate_tendencies(form):
    ts = form.get('tendencies', [])
    if not isinstance(ts, list) or len(ts) > 12:
        raise ValueError('INVALID_ACQUIRED_TENDENCIES')
    for t in ts:
        if (not isinstance(t, dict) or t.get('polarity') not in POLARITIES
                or not isinstance(t.get('action'), str)
                or t.get('action') not in ACTIONS
                or not isinstance(t.get('cue_terms', []), list)
                or not all(isinstance(x, str) for x in t.get('cue_terms', []))):
            raise ValueError('INVALID_ACQUIRED_TENDENCIES')
        for key in ('activity_ref', 'object', 'counterpart'):
            if key in t and (not isinstance(t[key], str) or not t[key]):
                raise ValueError('INVALID_TENDENCY_CONTEXT')
        if 'locations' in t and (not isinstance(t['locations'], list)
                or not all(isinstance(x, str) for x in t['locations'])):
            raise ValueError('INVALID_TENDENCY_CONTEXT')


def _matches(t, option, access, cue_words):
    if t['action'] != option['action']:
        return False
    if t.get('cue_terms') and not (
            {str(v).lower() for v in t['cue_terms']} & cue_words):
        return False
    if t.get('locations') and access.location not in t['locations']:
        return False
    if t.get('activity_ref') != None and t['activity_ref'] != option.get('activity_ref'):
        return False
    if t.get('object') is not None:
        values = option.get('practical_objects', [])
        if option.get('practical_object'):
            values = values + [option['practical_object']]
        if str(t['object']).casefold() not in {str(v).casefold() for v in values}:
            return False
    if t.get('counterpart') is not None:
        partner = option.get('counterpart')
        if partner != t['counterpart']:
            return False
    return True


def _option_identity(option, index):
    return option.get('option_id') or (
        'candidate:' + str(index) + ':' + str(option['action']) +
        ':' + str(option.get('activity_ref', 'unscoped')))


def enact_currents(constitution, access, active_forms, candidates):
    """Recruit currents into distinct situated *activities*, not global action bans.

    WITHHOLD for public singing to seek Father cannot delete private singing
    or singing directed to a different concern. Legacy unqualified tendencies
    retain their deliberately broad action scope. Competing currents coexist.
    """
    cues = {str(x).lower() for c in access.cues
            for x in c.get('tags', []) + [c.get('kind', '')]}
    currents, antagonisms, suspended, updated = [], [], [], []
    body = constitution.body
    for metric, flag, threshold in (
            ('nutrition', 'HUNGER', .42),
            ('rest', 'EXHAUSTION', .4),
            ('comfort', 'DISTRESS', .35)):
        if body.get(metric, 1.0) < threshold:
            currents.append({'kind': 'ORGANISMIC_CONDITION', 'state': flag,
                'source': 'CURRENT_BODY', 'objective_body_state': metric,
                'not_a_conscious_motive': True,
                'cannot_alone_certify_an_acquired_motive': True})

    candidates = list(candidates)
    for i, proposed in enumerate(candidates):
        o = copy(proposed)
        ident = _option_identity(o, i)
        o['option_id'] = ident
        approach, withhold = [], []
        for form in active_forms.values():
            validate_tendencies(form)
            for t in form.get('tendencies', []):
                if not _matches(t, o, access, cues):
                    continue
                (approach if t['polarity'] == 'APPROACH' else withhold).append(form['id'])
                currents.append({'kind': 'ACQUIRED_ACTIVITY_CURRENT',
                    'action': o['action'], 'polarity': t['polarity'],
                    'form_ref': form['id'], 'option_id': ident,
                    'activity_ref': o.get('activity_ref'),
                    'practical_object': o.get('practical_object'),
                    'counterpart': o.get('counterpart'),
                    'tendency_context': {k: copy(t[k]) for k in CONTEXT_KEYS if k in t},
                    'grade': GRADE, 'not_universal_utility': True})
        approach, withhold = sorted(set(approach)), sorted(set(withhold))
        if approach and withhold:
            o['psychodynamic_status'] = 'UNRESOLVED_CONTRADICTION'
            o['opposed_currents'] = {'approach': approach, 'withhold': withhold}
            antagonisms.append({'option_id': ident, 'action': o['action'],
                'activity_ref': o.get('activity_ref'),
                'practical_object': o.get('practical_object'),
                'approach': approach, 'withhold': withhold,
                'resolution': 'UNDETERMINED; NO FORCED HARMONY',
                'actor': constitution.actor})
            updated.append(o)
        elif withhold:
            suspended.append({'option_id': ident, 'action': o['action'],
                'activity_ref': o.get('activity_ref'),
                'practical_object': o.get('practical_object'),
                'by_form_refs': withhold, 'status': 'SITUATED_ACQUIRED_INHIBITION',
                'still_bodily_possible': True,
                'does_not_erase_other_activities_using_same_action': True})
        else:
            if approach:
                o['psychodynamic_status'] = 'ACQUIRED_APPROACH_WITHOUT_RECORDED_COUNTERCURRENT'
                o['support_currents'] = approach
            updated.append(o)
    return {'candidate_actions': updated, 'currents': currents,
            'antagonisms': antagonisms, 'suspended': suspended, 'grade': GRADE}
