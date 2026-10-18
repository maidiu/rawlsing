"""ONECALL-C0: executable TEST-ONLY chronology and authority-boundary prototype.

No external LLM, Pyat source, CAN008/CAN011 rule or production actor is used.
All psychological inference is DEFERRED; all explicit owner effects here are
synthetic *objective* observation/material effects, never personal beliefs.
"""
from __future__ import annotations
import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path
from typing import Any

GRADE = 'BOUNDED_MOCK_OWNER_ONLY__NOT_SOROK_ACTOR_RULE'
SEED = 172901


def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False)


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode('utf-8')).hexdigest()


def fact_id(year: int, candidate_id: str) -> str:
    return f'observed:{year}:{candidate_id}'


def candidate(year: int, day: int, cid: str, action: str, **kwargs) -> dict:
    return dict(id=cid, year=year, day=day, action=action,
                possible_relevance_domains=kwargs.pop('domains', ['activity']),
                prerequisites=kwargs.pop('prerequisites', []),
                source_scope_refs=['SYNTHETIC_WORLD@1'], **kwargs)


def fixed_candidates(year: int) -> list[dict]:
    if year == 2020:
        return [
            candidate(year, 30, 'practice', 'PRACTICE_OBSERVED', domains=['skill', 'practice']),
            candidate(year, 80, 'move', 'FAMILY_MOVE', domains=['material_access']),
            candidate(year, 140, 'project', 'PROJECT_TASK', min_practice=1, domains=['competence']),
            candidate(year, 180, 'old_friend', 'FRIEND_MEETING', required_region='old_town'),
            candidate(year, 250, 'peer_contact', 'COUNTERPART_CONTACT', counterpart='peer', domains=['affiliation']),
            candidate(year, 300, 'routine', 'OBSERVED_NEUTRAL', domains=['daily_life']),
            candidate(year, 320, 'noevent', 'NO_EVENT', domains=[]),
        ]
    if year == 2021:
        return [
            candidate(year, 25, 'invented_teacher', 'TEACHER_MEETING',
                      prerequisites=['render-only:teacher-nova']),
            candidate(year, 40, 'invented_betrayal', 'ANGER_UPDATE',
                      prerequisites=['render-only:betrayal'], unauthorized_effect='CAN011_UPDATE'),
            candidate(year, 100, 'club', 'NEW_CLUB', required_region='new_town'),
            candidate(year, 150, 'speech', 'SPEECH_EXPOSURE',
                      speech_ref='speech:2021:caregiver', listener_witness=False),
            candidate(year, 210, 'quiet', 'OBSERVED_NEUTRAL', domains=['daily_life']),
            candidate(year, 260, 'covert_memory', 'OBSERVED_NEUTRAL', unauthorized_effect='ADP016_MEMORY'),
            candidate(year, 310, 'not_today', 'NO_EVENT', domains=[]),
        ]
    return []


def initial_state() -> dict:
    return dict(world=dict(region='old_town', material_version=0, cohort='SYNTHETIC_POSITION',
                           source_ref='SYNTHETIC_WORLD@1'),
                actor=dict(id='child', demographics='FIXED_SYNTHETIC_COHORT',
                           practiced_tasks=0, actor_knowledge=[], beliefs='UNISSUED', affect='UNISSUED'),
                counterparts=dict(peer=dict(project='rehearsal', available=False,
                                            independent_history=['rehearsal_reserved'])),
                events=[], current_year=2020, slow_ticks=[],
                source_grade=GRADE)


def render_input(state: dict, year: int) -> dict:
    """Only owner-committed history; render text never enters this input."""
    previous = [e['id'] for e in state['events'] if e['year'] == year-1]
    return dict(year=year, checkpoint_ref=digest(state),
                historical_event_refs=previous,
                immutable_history_hash=digest(state['events']),
                source_scope_refs=['SYNTHETIC_WORLD@1'],
                position_ref='SYNTHETIC_POSITION',
                horizon=[year, year + 1], actor_ref='child')


def mocked_artifacts(inp: dict, render_variant: str = 'default') -> tuple[dict, dict]:
    """Deterministic fixture generator. It is NOT a live or purchased LLM."""
    year = inp['year']
    prev = year - 1
    observed = inp['historical_event_refs']
    text = (f'Illustration of {prev}: the child did ordinary things.'
            if render_variant == 'default' else
            f'Entirely different literary style for {prev}; not a new event.')
    # Deliberately adversarial, clearly surface-only inventions. Future claim is disallowed.
    render = dict(interval_id=str(prev), causal_checkpoint_ref=inp['checkpoint_ref'],
                  allowed_fact_refs=observed,
                  claimed_fact_refs=list(observed), text_or_scene_fragments=[text],
                  surface_inventions_only=(['render-only:teacher-nova', 'render-only:betrayal']
                                           if year == 2021 else []),
                  future_fact_claims=([fact_id(year, 'future_unoccurred')]
                                      if year == 2021 else []),
                  render_provenance=dict(provider='MOCK_NO_API', variant=render_variant))
    packet = dict(horizon=inp['horizon'], checkpoint_ref=inp['checkpoint_ref'],
                  candidates=deepcopy(fixed_candidates(year)),
                  source_scope_refs=list(inp['source_scope_refs']),
                  eligible_participant_refs=['child', 'peer', 'caregiver'],
                  model_version='MOCK_NO_MODEL', prompt_hash=digest(['fixed-prompt', year]),
                  sampling_metadata=dict(rng_stream='ONECALL_C0_TEST_SEED', seed=SEED,
                                         random_draws=0, probability_grade='NONE'),
                  uncertainty=['TEST_ONLY_NO_BEHAVIORAL_PROPENSITY'])
    return render, packet


class InvocationMock:
    def __init__(self, mode: str, variant: str):
        if mode not in ('ONE_CALL', 'TWO_CALL', 'FIXED_PACKET'):
            raise ValueError(mode)
        self.mode, self.variant = mode, variant
        self.physical_calls = 0
        self.call_log = []

    def boundary(self, inp: dict) -> tuple[dict, dict]:
        render, packet = mocked_artifacts(inp, self.variant)
        if self.mode == 'ONE_CALL' and self.variant == 'combined_contamination' and inp['year'] == 2021:
            packet['candidates'].append(candidate(2021, 55, 'extra_fabricated_teacher',
                                'TEACHER_MEETING', prerequisites=['render-only:teacher-nova']))
        if self.mode == 'ONE_CALL':
            self.physical_calls += 1
            self.call_log.append(dict(year=inp['year'], role='RETROSPECTIVE_AND_PROSPECTIVE'))
        elif self.mode == 'TWO_CALL':
            if inp['year'] > 2020:
                self.physical_calls += 1
                self.call_log.append(dict(year=inp['year'], role='RETROSPECTIVE_ONLY'))
            if packet['candidates']:
                self.physical_calls += 1
                self.call_log.append(dict(year=inp['year'], role='PROSPECTIVE_ONLY'))
        return render, packet


def validate_render(render: dict, inp: dict) -> dict:
    allowed = set(inp['historical_event_refs'])
    claimed = set(render['claimed_fact_refs'])
    assert render['causal_checkpoint_ref'] == inp['checkpoint_ref']
    assert set(render['allowed_fact_refs']) <= allowed, 'render fact grant forged'
    forbidden = sorted(claimed - allowed)
    forward = sorted(render.get('future_fact_claims', []))
    return dict(status='NONCAUSAL_VALIDATED' if not forbidden else 'RENDER_CLAIM_REJECTED',
                grounded_fact_refs=sorted(claimed & allowed),
                ungrounded_claims=forbidden,
                future_claims_rejected=forward,
                surface_inventions_only=list(render['surface_inventions_only']),
                narrative_text=render['text_or_scene_fragments'],
                causal_hash_before=inp['checkpoint_ref'],
                provenance=deepcopy(render['render_provenance']))


def validate_packet(packet: dict, inp: dict) -> tuple[dict, list[dict]]:
    assert packet['checkpoint_ref'] == inp['checkpoint_ref'], 'stale checkpoint'
    assert packet['horizon'] == inp['horizon'], 'wrong horizon'
    assert packet['source_scope_refs'] == inp['source_scope_refs'], 'source mismatch'
    assert inp.get('position_ref') == 'SYNTHETIC_POSITION', 'actor position unbound'
    prohibited_top = {'CAN011_UPDATE', 'ADP016_MEMORY', 'psychic_effects', 'selected_belief'}
    assert not prohibited_top.intersection(packet), 'unissued top-level effect'
    seen = set()
    valid, rejected = [], []
    for p in packet['candidates']:
        reason = None
        if p['id'] in seen: reason = 'DUPLICATE_CANDIDATE_ID'
        if p['year'] != inp['year'] or not 0 <= p['day'] < 365:
            reason = 'WRONG_TIME'
        if any(ref.startswith('render-only:') for ref in p.get('prerequisites', [])):
            reason = 'NARRATIVE_INVENTION_IS_NOT_A_PREREQUISITE'
        if any(ref not in inp['historical_event_refs']
               for ref in p.get('prerequisites', []) if not ref.startswith('render-only:')):
            reason = 'UNKNOWN_PREREQUISITE__CONSTRUCTOR_UNISSUED'
        if p.get('unauthorized_effect') or any(k in p for k in ('CAN011_UPDATE', 'ADP016_MEMORY', 'effects', 'psychic_delta')):
            reason = 'UNISSUED_PSYCHOLOGICAL_EFFECT'
        if p.get('source_scope_refs') != inp['source_scope_refs']:
            reason = 'SOURCE_RIGHTS_MISMATCH'
        seen.add(p['id'])
        if reason:
            rejected.append(dict(id=p['id'], status='REJECTED_PROPOSAL', reason=reason))
        else:
            valid.append(deepcopy(p))
    return dict(status='NONCAUSAL_CANDIDATES_VALIDATED', rejected=rejected,
                candidate_ids=[p['id'] for p in valid],
                proposal_checkpoint=inp['checkpoint_ref'],
                no_personal_probability=True), valid


def evaluate(state: dict, p: dict, rules: dict) -> str:
    """Separate sourcefree owner mock: no beliefs/affect/memory writes."""
    action = p['action']
    if action == 'NO_EVENT': return 'VALID_EMPTY'
    if p.get('required_region') and p['required_region'] != state['world']['region']:
        return 'INVALIDATED_MATERIAL_REGION'
    if action == 'PROJECT_TASK' and state['actor']['practiced_tasks'] < p['min_practice']:
        return 'DEFERRED_MISSING_OBSERVED_PRACTICE'
    if action == 'COUNTERPART_CONTACT' and not state['counterparts']['peer']['available']:
        return 'REFUSED_INDEPENDENT_COUNTERPART'
    if action == 'SPEECH_EXPOSURE' and not p.get('listener_witness'):
        return 'DEFERRED_NO_ACTOR_EXPOSURE'
    if action not in rules['licensed_objective_actions']:
        return 'DEFERRED_MISSING_OWNER_RULE'
    return 'ELIGIBLE_TEST_ONLY'


def apply_admitted(state: dict, p: dict, year: int, rules: dict) -> dict:
    """Mock *objective* admission. Renderer, packet and psyche are excluded."""
    action = p['action']
    prehash = digest(state)
    old_beliefs, old_affect = state['actor']['beliefs'], state['actor']['affect']
    if action == 'PRACTICE_OBSERVED':
        # Authored toy observational threshold, not licensed CAN011 learning.
        assert 'PRACTICE_OBSERVED' in rules['licensed_objective_actions']
        state['actor']['practiced_tasks'] += 1
    if action == 'FAMILY_MOVE':
        state['world']['region'] = 'new_town'
        state['world']['material_version'] += 1
    if action == 'SPEECH_EXPOSURE':
        # Only possible if an independent listener witness was provided.
        state['actor']['actor_knowledge'].append(p['speech_ref'])
    assert (old_beliefs, old_affect) == (state['actor']['beliefs'], state['actor']['affect'])
    receipt = dict(id=fact_id(year, p['id']), year=year, day=p['day'],
                   action=action, actor='child', objective_owner='ONECALL_C0_TEST_OWNER',
                   grade=GRADE, source_ref='SYNTHETIC_WORLD@1',
                   prior_state_hash=prehash,
                   possible_relevance_not_effect=p['possible_relevance_domains'],
                   rule_ref='ONECALL_C0_AUTHOR_TEST_RULE@1')
    receipt['hash'] = digest(receipt)
    state['events'].append(receipt)
    return receipt


def slow_tick(state: dict, year: int, start: int, end: int) -> None:
    """Time passage without a synthetic event or psychological delta."""
    if end > start:
        state['slow_ticks'].append(dict(year=year, from_day=start, to_day=end,
                                        owner='TEST_CLOCK_ONLY'))


def run(mode='ONE_CALL', variant='default', rules=None, initial=None):
    owner_rules = rules or dict(licensed_objective_actions=[
        'PRACTICE_OBSERVED', 'FAMILY_MOVE', 'PROJECT_TASK', 'FRIEND_MEETING',
        'COUNTERPART_CONTACT', 'OBSERVED_NEUTRAL', 'NEW_CLUB', 'TEACHER_MEETING',
        'SPEECH_EXPOSURE'])
    state = deepcopy(initial) if initial is not None else initial_state()
    llm = InvocationMock(mode, variant)
    boundaries, decisions, revalidations, all_proposals = [], [], [], []
    for year in (2020, 2021, 2022):
        inp = render_input(state, year)
        render, packet = llm.boundary(inp)
        rend = validate_render(render, inp)
        pkt, pending = validate_packet(packet, inp)
        before = digest(state)
        assert before == inp['checkpoint_ref']
        assert before == rend['causal_hash_before']
        all_proposals.extend(pkt['rejected'])
        boundaries.append(dict(year=year, checkpoint_ref=before, render=rend,
                               prospective_validation=pkt,
                               physical_calls_so_far=llm.physical_calls))
        if year == 2022: break
        last_day = 0
        pending.sort(key=lambda p: (p['day'], p['id']))
        while pending:
            p = pending.pop(0)
            slow_tick(state, year, last_day, p['day'])
            last_day = p['day']
            status = evaluate(state, p, owner_rules)
            decision = dict(year=year, day=p['day'], id=p['id'],
                            status=status, owner='ONECALL_C0_TEST_OWNER',
                            grade=GRADE, before=digest(state))
            if status == 'ELIGIBLE_TEST_ONLY':
                receipt = apply_admitted(state, p, year, owner_rules)
                decision['event_ref'] = receipt['id']
                decision['event_hash'] = receipt['hash']
                decision['status'] = 'ADMITTED_TEST_ONLY'
                decision['psyche_effect_status'] = 'VALID_EMPTY__NO_CAN008_CAN011_ADP016_RULE'
            decision['after'] = digest(state)
            decisions.append(decision)
            # Revalidation after every opportunity (including refusals, valid-empty).
            # Materially invalidated futures are rejected, never silently rerolled.
            revised = []
            for future in pending:
                future_status = evaluate(state, future, owner_rules)
                revalidations.append(dict(year=year, after=p['id'], candidate=future['id'],
                                          status=future_status,
                                          owner_state_hash=digest(state)))
                if future_status.startswith('INVALIDATED_'):
                    decisions.append(dict(year=year, day=p['day'], id=future['id'],
                                          status=future_status, invalidated_by=p['id'],
                                          owner='ONECALL_C0_TEST_OWNER',
                                          grade=GRADE, before=digest(state), after=digest(state)))
                else:
                    revised.append(future)
            pending = revised
        slow_tick(state, year, last_day, 365)
        state['current_year'] = year + 1
    causal = dict(final_state=deepcopy(state), decisions=decisions,
                  revalidations=revalidations, proposal_rejections=all_proposals,
                  final_state_hash=digest(state),
                  canonical_history_hash=digest(state['events']),
                  source_grade=GRADE, rng=dict(stream='ONECALL_C0_TEST_SEED',seed=SEED,draws=0))
    causal['receipt_hash'] = digest(causal)
    return dict(mode=mode, mock_physical_invocations=llm.physical_calls,
                invocation_log=llm.call_log,
                boundaries=boundaries,
                causal=causal,
                experiment_grade=GRADE,
                money_spent='NO_EXTERNAL_PROVIDER_OR_API')


def mode_comparison(variant='default') -> dict:
    runs = {mode: run(mode, variant) for mode in ('ONE_CALL', 'TWO_CALL', 'FIXED_PACKET')}
    rejected = {k: sorted((p['id'], p['reason']) for p in r['causal']['proposal_rejections'])
                for k, r in runs.items()}
    equal = all(r['causal'] == runs['ONE_CALL']['causal'] for r in runs.values())
    fallback = 'TWO_CALL' if rejected['ONE_CALL'] != rejected['TWO_CALL'] else 'ONE_CALL'
    return dict(variant=variant, physical_mock_invocations={k:r['mock_physical_invocations']
                   for k,r in runs.items()}, causal_equal=equal, rejected=rejected,
                selected_research_fallback=fallback,
                causal_hashes={k:r['causal']['receipt_hash'] for k,r in runs.items()},
                disclaimer='C0_FIXED_PROVIDER_MOCK__NO_REAL_LLM_QUALITY_COST_INFERENCE')


def causal_equal(a: dict, b: dict) -> bool:
    return a['causal'] == b['causal']


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', choices=['ONE_CALL', 'TWO_CALL', 'FIXED_PACKET'], default='ONE_CALL')
    parser.add_argument('--variant', default='default')
    parser.add_argument('--out', type=Path)
    opts = parser.parse_args()
    result = run(opts.mode, opts.variant)
    serial = canonical(result) + '\n'
    if opts.out:
        opts.out.parent.mkdir(parents=True, exist_ok=True)
        opts.out.write_text(serial, encoding='utf-8')
    print(canonical(dict(mode=result['mode'], calls=result['mock_physical_invocations'],
                         causal_hash=result['causal']['receipt_hash'],
                         events=len(result['causal']['final_state']['events']),
                         admitted=sum(d['status']=='ADMITTED_TEST_ONLY' for d in result['causal']['decisions']),
                         refusals=sum(d['status']!='ADMITTED_TEST_ONLY' for d in result['causal']['decisions']),
                         grade=GRADE)))

if __name__ == '__main__':
    main()
