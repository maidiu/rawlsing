"""Sorok ONECALL-C0F Phase-A independent source-free falsification reference.

Frozen before access to C0 code, tests or returns. This is a *boundary oracle*,
not an implementation, a generator, a CAN008 psychology model, or an owner issuer.
The fixtures' expected outputs are never read by this reference evaluation.
"""
from __future__ import annotations
import copy
import hashlib
import json

VERSION = 'SOROK_ONECALL_C0F_BLIND_REFERENCE@1'


def canon(x):
    return json.dumps(x, sort_keys=True, separators=(',', ':'), ensure_ascii=False)


def digest(x):
    return hashlib.sha256(canon(x).encode('utf-8')).hexdigest()


def _initial(f):
    return {'location': f.get('location', 'OLD_TOWN'),
            'capacity': f.get('capacity', 0),
            'knowledge': sorted(f.get('knowledge', [])),
            'psyche': copy.deepcopy(f.get('psyche', {})),
            'ledger': copy.deepcopy(f.get('ledger', [])),
            'slow_time': f.get('now', 0)}


def run(packet):
    """Compute an independent no-LLM mock boundary over asserted authored events.

    * Never reads packet['expected'], narrative text, or a frozen oracle fixture.
    * Owner grants are explicitly *test-only simulated*; no native authority.
    * A physical world event, actor exposure, actor knowledge and durable effect
      are different decisions, not one automatic transition.
    """
    q = copy.deepcopy(packet)
    state = _initial(q)
    starting_hash = digest(state)
    now, stop = int(q.get('now', 0)), int(q.get('horizon', 365))
    committed_refs = {e['id'] for e in state['ledger'] if e.get('committed') is True and int(e['at']) <= now}
    output = q.get('output', {})
    retro = output.get('retrospective', {})
    prospective = output.get('prospective', {})
    # Rendering cannot claim an uncommitted external event as witnessed fact.
    # Surface prose and ungrounded decorative inventions remain inert.
    asserted = retro.get('asserted_fact_refs', [])
    bad_retro = sorted(set(asserted) - committed_refs)
    safe_retro = sorted(set(asserted) & committed_refs)
    render_results = ['REJECT_UNCOMMITTED_RETRO_FACT:' + v for v in bad_retro]
    if retro.get('durable_psyche_patch') or retro.get('witnessed_memory_patch'):
        render_results.append('REJECT_RENDER_TO_ACTOR_EFFECT')
    current_ledger = copy.deepcopy(state['ledger'])
    new_events = []
    outcomes = {}
    proposal_rows = prospective.get('candidates', [])
    # Equal-time candidates with an asserted dependency require its causal parent;
    # stable lexical ID is used only for independent test fixture ties.
    for ev in sorted(proposal_rows, key=lambda e: (int(e.get('at', -1)), str(e.get('id', '')))):
        eid = ev['id']
        at = int(ev.get('at', -1))
        context_refs = committed_refs | {e['id'] for e in new_events}
        if eid in outcomes or eid in context_refs:
            status = 'REFUSE_EVENT_ID_REWRITE'
        elif at <= now or at > stop:
            status = 'REFUSE_CLOCK_OUTSIDE_NEXT_INTERVAL'
        elif ev.get('origin') == 'RENDER_PROSE' or any(ref not in context_refs for ref in ev.get('requires_refs', [])):
            status = 'REFUSE_UNGROUNDED_PREREQUISITE'
        elif ev.get('actor_owner') not in (None, 'MOCK_OWNER_TEST_ONLY') or ev.get('external_issuer') == 'FORGED':
            status = 'REFUSE_FORGED_OR_FOREIGN_OWNER'
        elif ev.get('actor_owner') is None or ev.get('world_owner') is None:
            status = 'DEFER_MISSING_OWNER_AUTHORITY'
        elif ev.get('rule') == 'MISSING' or ev.get('source_permission') == 'MISSING':
            status = 'DEFER_MISSING_RULE_OR_SOURCE_PERMISSION'
        elif ev.get('score', 0) < 0:
            status = 'REFUSE_SCORE_INVALID_NO_RNG_OVERRIDE'
        elif ev.get('requires_location') not in (None, state['location']):
            status = 'INVALIDATED_CURRENT_CONTEXT'
        elif ev.get('requires_capacity', 0) > state['capacity']:
            status = 'DEFER_UNISSUED_CAPACITY_OR_LEARNING'
        elif ev.get('requires_other_consent') and ev.get('other_response') != 'CONSENT':
            status = 'REFUSE_INDEPENDENT_OTHER_PERSON'
        else:
            status = 'ADMITTED_MOCK_EXTERNAL_OCCURRENCE'
            state['slow_time'] = at
            record = {'id': eid, 'at': at, 'kind': ev.get('kind', 'ACTIVITY'), 'committed': True}
            new_events.append(record)
            # These are only mock objective/material effects from named test grants.
            if ev.get('kind') == 'MOVE':
                state['location'] = ev.get('destination', state['location'])
            if ev.get('kind') == 'PRACTICE' and ev.get('practice_owner_rule') == 'MOCK_PRACTICE_UPTAKE':
                state['capacity'] += 1
            if ev.get('exposed_to_child') is True:
                state['knowledge'] = sorted(set(state['knowledge']) | {eid})
            # No psychological outcome is ever inferred from model relevance tags.
            # Unauthorized candidate psyche patches cannot become state.
        outcomes[eid] = status
    state['ledger'] = current_ledger + new_events
    state['slow_time'] = stop
    # A no-event interval can still advance slow integration clock, not psyche.
    return {
        'dispositions': outcomes,
        'admitted_ids': [e['id'] for e in new_events],
        'render_refusals': render_results,
        'safe_render_refs': safe_retro,
        'actor_knowledge': state['knowledge'],
        'material_location': state['location'],
        'material_capacity': state['capacity'],
        'psyche': state['psyche'],
        'history_ids': [e['id'] for e in state['ledger']],
        'history_hash': digest(state['ledger']),
        'post_state_hash': digest(state),
        'pre_state_hash': starting_hash,
        'slow_time': stop,
        'physical_mock_calls': 1 if q.get('arm', 'ONE_CALL') == 'ONE_CALL' else 2 if q.get('arm') == 'TWO_CALL' else 0,
        'owner_grade': 'BOUNDED_TEST_ONLY_MOCK_NOT_CAN008_OR_WORLD_ISSUANCE',
    }


def causal_projection(result):
    """Ignore prose-only and purely physical mock invocation-count differences."""
    return {k: result[k] for k in ('dispositions', 'admitted_ids', 'actor_knowledge',
            'material_location', 'material_capacity', 'psyche', 'history_ids',
            'history_hash', 'post_state_hash', 'pre_state_hash', 'slow_time')}
