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
SOURCE = 'SYNTHETIC_WORLD@1'
SOURCE_PERMISSION = 'C0R_SOURCEFREE_FIXTURE_USE@1'
MOCK_OWNER = 'ONECALL_C0_TEST_OWNER'
MOCK_RULE = 'ONECALL_C0_AUTHOR_TEST_RULE@1'
REQUIRED_GRANT = frozenset({'actor_owner','source_permission','rule_ref','objective_owner'})
RENDER_KEYS = frozenset({'interval_id','causal_checkpoint_ref','allowed_fact_refs',
 'claimed_fact_refs','text_or_scene_fragments','surface_inventions_only','future_fact_claims','render_provenance'})
PACKET_KEYS = frozenset({'horizon','checkpoint_ref','candidates','source_scope_refs',
 'eligible_participant_refs','model_version','prompt_hash','sampling_metadata','uncertainty'})
CANDIDATE_KEYS = frozenset({'id','year','day','action','possible_relevance_domains',
 'prerequisites','source_scope_refs','actor_owner','source_permission','rule_ref','objective_owner',
 'required_region','min_practice','counterpart','participants','listener_witness','speech_ref',
 'unauthorized_effect','CAN011_UPDATE','ADP016_MEMORY','effects','psychic_delta',
 'subannual_horizon_days','score','random_draw','source_rule_hash','external_issuer'})

def guard(condition, message):
    # An explicit check survives python -O; no security/custody assertion is used.
    if not condition:
        raise AssertionError(message)

def proper_str(x):
    return isinstance(x, str) and bool(x) and type(x) is str

def listed_strings(x):
    return isinstance(x,list) and all(proper_str(q) for q in x) and len(x)==len(set(x))



def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False)


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode('utf-8')).hexdigest()


def fact_id(year: int, candidate_id: str) -> str:
    return f'observed:{year}:{candidate_id}'


def candidate(year: int, day: int, cid: str, action: str, **kwargs) -> dict:
    # Explicit fixture grants, not a generated model's authority.
    owner = kwargs.pop('actor_owner', MOCK_OWNER)
    event_owner = kwargs.pop('objective_owner', MOCK_OWNER)
    permission = kwargs.pop('source_permission', SOURCE_PERMISSION)
    rule = kwargs.pop('rule_ref', MOCK_RULE)
    return dict(id=cid, year=year, day=day, action=action,
                possible_relevance_domains=kwargs.pop('domains', ['activity']),
                prerequisites=kwargs.pop('prerequisites', []),
                source_scope_refs=[SOURCE], actor_owner=owner, objective_owner=event_owner,
                source_permission=permission, rule_ref=rule, **kwargs)


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
    """Render is a validated but permanently NONCAUSAL proposal."""
    guard(isinstance(render,dict) and isinstance(inp,dict), 'render malformed')
    guard(render.get('causal_checkpoint_ref') == inp['checkpoint_ref'], 'render stale checkpoint')
    guard(listed_strings(render.get('allowed_fact_refs')), 'render malformed allowed refs')
    allowed=set(inp['historical_event_refs'])
    guard(set(render['allowed_fact_refs']) <= allowed, 'render fact grant forged')
    forbidden_schema=set(render)-RENDER_KEYS
    if forbidden_schema or not isinstance(render.get('render_provenance'),dict):
        return dict(status='RENDER_SCHEMA_REFUSED', reason='UNISSUED_RENDER_FIELD_OR_PROVENANCE',
                    unexpected_keys=sorted(forbidden_schema), grounded_fact_refs=[],
                    ungrounded_claims=[], future_claims_rejected=[],
                    surface_inventions_only=[], narrative_text=[], causal_hash_before=inp['checkpoint_ref'],
                    provenance={})
    guard(listed_strings(render.get('claimed_fact_refs')), 'render malformed claims')
    guard(listed_strings(render.get('surface_inventions_only')), 'render malformed inventions')
    guard(listed_strings(render.get('future_fact_claims')), 'render malformed future claims')
    guard(isinstance(render.get('text_or_scene_fragments'),list) and
          all(proper_str(x) for x in render['text_or_scene_fragments']), 'render malformed text')
    if set(render['render_provenance'])-{'provider','variant'} or render['render_provenance'].get('provider') != 'MOCK_NO_API':
        return dict(status='RENDER_SCHEMA_REFUSED', reason='FORGED_RENDER_PROVIDER',
                    unexpected_keys=[], grounded_fact_refs=[], ungrounded_claims=[],
                    future_claims_rejected=[], surface_inventions_only=[], narrative_text=[],
                    causal_hash_before=inp['checkpoint_ref'],provenance={})
    claimed=set(render['claimed_fact_refs'])
    forbidden=sorted(claimed-allowed)
    return dict(status='NONCAUSAL_VALIDATED' if not forbidden else 'RENDER_CLAIM_REJECTED',
                grounded_fact_refs=sorted(claimed&allowed), ungrounded_claims=forbidden,
                future_claims_rejected=sorted(render['future_fact_claims']),
                surface_inventions_only=list(render['surface_inventions_only']),
                narrative_text=render['text_or_scene_fragments'],
                causal_hash_before=inp['checkpoint_ref'],
                provenance=deepcopy(render['render_provenance']))


def validate_packet(packet: dict, inp: dict) -> tuple[dict,list[dict]]:
    guard(isinstance(packet,dict) and isinstance(inp,dict), 'packet malformed')
    guard(packet.get('checkpoint_ref')==inp['checkpoint_ref'],'stale checkpoint')
    guard(packet.get('horizon')==inp['horizon'],'wrong horizon')
    guard(packet.get('source_scope_refs')==inp['source_scope_refs'],'source mismatch')
    guard(inp.get('position_ref')=='SYNTHETIC_POSITION','actor position unbound')
    guard(not {'CAN011_UPDATE','ADP016_MEMORY','psychic_effects','selected_belief'}.intersection(packet),'unissued top-level effect')
    valid,rejected=[],[]
    packet_reason=None
    if set(packet)-PACKET_KEYS: packet_reason='UNISSUED_PACKET_FIELD'
    if packet.get('model_version')!='MOCK_NO_MODEL':packet_reason='UNISSUED_MODEL_PROVENANCE'
    sm=packet.get('sampling_metadata')
    if (not isinstance(sm,dict) or sm.get('probability_grade')!='NONE' or sm.get('random_draws')!=0 or
       sm.get('rng_stream')!='ONECALL_C0_TEST_SEED' or sm.get('seed')!=SEED or set(sm)-{'rng_stream','seed','random_draws','probability_grade'}):
        packet_reason='UNISSUED_SAMPLING_PROVENANCE'
    if not (listed_strings(packet.get('eligible_participant_refs')) and
            packet['eligible_participant_refs']==['child','peer','caregiver'] and
            proper_str(packet.get('prompt_hash')) and isinstance(packet.get('uncertainty'),list) and
            isinstance(packet.get('candidates'),list)):
        packet_reason='UNQUALIFIED_PACKET_SCHEMA'
    if packet_reason:
        rejected=[dict(id=p.get('id','UNKNOWN') if isinstance(p,dict) else 'UNKNOWN',status='REJECTED_PROPOSAL',reason=packet_reason)
                  for p in packet.get('candidates',[]) if isinstance(p,dict)]
        return dict(status='PACKET_REFUSED',rejected=rejected,candidate_ids=[],proposal_checkpoint=inp['checkpoint_ref'],
                    no_personal_probability=True),[]
    seen=set(); items=packet['candidates']; ids=set()
    for p in items:
        if isinstance(p,dict) and proper_str(p.get('id')):ids.add(p['id'])
    # A proposal parent may be pending until its actual observed event; proposed != observed.
    pairs={p.get('id'):p for p in items if isinstance(p,dict)}
    for p in items:
        reason=None
        if not isinstance(p,dict):
            rejected.append(dict(id='UNKNOWN',status='REJECTED_PROPOSAL',reason='MALFORMED_CANDIDATE'));continue
        cid=p.get('id')
        if not proper_str(cid):reason='MALFORMED_CANDIDATE_ID'
        elif cid in seen:reason='DUPLICATE_CANDIDATE_ID'
        if (type(p.get('year'))!=int or type(p.get('day'))!=int or
            p.get('year')!=inp['year'] or not 0<=p['day']<365):reason='WRONG_TIME'
        if set(p)-CANDIDATE_KEYS:reason='UNISSUED_CANDIDATE_FIELD'
        if not listed_strings(p.get('source_scope_refs')) or p['source_scope_refs']!=inp['source_scope_refs']:
            reason='SOURCE_RIGHTS_MISMATCH'
        if (p.get('actor_owner')!=MOCK_OWNER or p.get('objective_owner')!=MOCK_OWNER or
            p.get('source_permission')!=SOURCE_PERMISSION or p.get('rule_ref')!=MOCK_RULE):
            reason='UNISSUED_CANDIDATE_OWNER_RULE_SOURCE'
        if 'external_issuer' in p:reason='EXTERNAL_ISSUER_UNISSUED'
        if 'rule' in p:reason='UNISSUED_CANDIDATE_FIELD'
        if 'score' in p or 'random_draw' in p:reason='UNISSUED_BEHAVIORAL_SELECTION_SCORE'
        if 'subannual_horizon_days' in p:reason='UNSUPPORTED_TEMPORAL_SCOPE'
        if not listed_strings(p.get('prerequisites')):reason='MALFORMED_PREREQUISITES'
        if not listed_strings(p.get('possible_relevance_domains')):reason='MALFORMED_RELEVANCE'
        if p.get('unauthorized_effect') or any(k in p for k in ('CAN011_UPDATE','ADP016_MEMORY','effects','psychic_delta')):
            reason='UNISSUED_PSYCHOLOGICAL_EFFECT'
        if any(q.startswith('render-only:') for q in p.get('prerequisites',[]) if isinstance(q,str)) and reason is None:
            reason='NARRATIVE_INVENTION_IS_NOT_A_PREREQUISITE'
        for q in p.get('prerequisites',[]):
            if not isinstance(q,str) or q.startswith('render-only:'):continue
            parent_id=f'observed:{inp["year"]}:'
            if q in inp['historical_event_refs']:continue
            if q.startswith(parent_id) and q[len(parent_id):] in ids:
                parent=pairs.get(q[len(parent_id):]);
                if (not isinstance(parent,dict) or type(parent.get('day'))!=int or type(p.get('day'))!=int or
                    parent['day']>=p['day']):reason='INVALID_PARENT_TIME_OR_CYCLE'
            else:reason='UNKNOWN_PREREQUISITE__CONSTRUCTOR_UNISSUED'
        if 'participants' in p:
            if not listed_strings(p['participants']) or any(x not in packet['eligible_participant_refs'] for x in p['participants']):
                reason='UNCONSTRUCTED_PARTICIPANT'
        if p.get('counterpart') and p['counterpart'] not in packet['eligible_participant_refs']:
            reason='UNCONSTRUCTED_PARTICIPANT'
        if p.get('action')=='TEACHER_MEETING' and not p.get('participants') and not any(
                q.startswith('render-only:') for q in p.get('prerequisites',[]) if isinstance(q,str)):
            reason='UNCONSTRUCTED_TEACHER'
        if proper_str(cid):seen.add(cid)
        if reason:rejected.append(dict(id=cid,status='REJECTED_PROPOSAL',reason=reason))
        else:valid.append(deepcopy(p))
    # Prune dependent children of a structurally rejected parent, to a fixed point.
    # A proposal reference does not grant its parent authority to exist.
    changed=True
    while changed:
        changed=False
        admitted_candidates={p['id'] for p in valid}
        remaining=[]
        for p in valid:
            parent_refs=[q for q in p['prerequisites'] if q.startswith(f'observed:{inp["year"]}:')]
            if any((q[len(f'observed:{inp["year"]}:'):] not in admitted_candidates)
                   and q not in inp['historical_event_refs'] for q in parent_refs):
                rejected.append(dict(id=p['id'],status='REJECTED_PROPOSAL',reason='PARENT_PROPOSAL_REJECTED'))
                changed=True
            else: remaining.append(p)
        valid=remaining
    return dict(status='NONCAUSAL_CANDIDATES_VALIDATED',rejected=rejected,
                candidate_ids=[p['id'] for p in valid],proposal_checkpoint=inp['checkpoint_ref'],
                no_personal_probability=True),valid

def evaluate(state: dict, p: dict, rules: dict) -> str:
    """Mock objective owner admits only exact currently qualified material witnesses."""
    if not isinstance(rules,dict) or not isinstance(rules.get('licensed_objective_actions'),list):
        return 'DEFERRED_MISSING_OWNER_RULE'
    if state.get('world',{}).get('source_ref')!=SOURCE:
        return 'DEFERRED_SOURCE_CURRENTNESS_MISMATCH'
    if (p.get('source_scope_refs') != [SOURCE] or p.get('source_permission')!=SOURCE_PERMISSION or
        p.get('actor_owner')!=MOCK_OWNER or p.get('objective_owner')!=MOCK_OWNER or p.get('rule_ref')!=MOCK_RULE):
        return 'DEFERRED_UNISSUED_OWNER_OR_SOURCE'
    if any(ref not in {x.get('id') for x in state['events']} for ref in p.get('prerequisites',[])):
        return 'PENDING_PARENT_NOT_ADMITTED'
    if p.get('participants') and any(x!='child' and x not in state.get('counterparts',{}) for x in p['participants']):
        return 'REFUSED_UNCONSTRUCTED_PARTICIPANT'
    if p.get('counterpart') and p['counterpart'] not in state.get('counterparts',{}):
        return 'REFUSED_UNCONSTRUCTED_COUNTERPART'
    action=p['action']
    if action=='NO_EVENT':return 'VALID_EMPTY'
    if p.get('required_region') and p['required_region']!=state['world']['region']:
        return 'INVALIDATED_MATERIAL_REGION'
    if action=='PROJECT_TASK' and state['actor']['practiced_tasks'] < p['min_practice']:
        return 'DEFERRED_MISSING_OBSERVED_PRACTICE'
    if action=='COUNTERPART_CONTACT' and not state['counterparts'][p['counterpart']]['available']:
        return 'REFUSED_INDEPENDENT_COUNTERPART'
    if action=='SPEECH_EXPOSURE' and not p.get('listener_witness'):
        return 'DEFERRED_NO_ACTOR_EXPOSURE'
    if action not in rules['licensed_objective_actions']:
        return 'DEFERRED_MISSING_OWNER_RULE'
    return 'ELIGIBLE_TEST_ONLY'


def apply_admitted(state: dict, p: dict, year: int, rules: dict) -> dict:
    """Atomic-in-function sourcefree admission: reject before ANY mutation."""
    guard(evaluate(state,p,rules)=='ELIGIBLE_TEST_ONLY','unissued admission or source mismatch')
    ident=fact_id(year,p['id'])
    guard(not any(x.get('id')==ident for x in state['events']),'duplicate existing event identity')
    guard(not any((x.get('year'),x.get('day'))>(year,p['day']) for x in state['events']),'backdated event')
    prehash=digest(state)
    old_beliefs=deepcopy(state['actor']['beliefs']);old_affect=deepcopy(state['actor']['affect'])
    action=p['action']
    # Copy before update: invalid proposals cannot leave partial state modifications.
    next_state=deepcopy(state)
    if action=='PRACTICE_OBSERVED':
        next_state['actor']['practiced_tasks']+=1
    if action=='FAMILY_MOVE':
        next_state['world']['region']='new_town';next_state['world']['material_version']+=1
    if action=='SPEECH_EXPOSURE':
        next_state['actor']['actor_knowledge'].append(p['speech_ref'])
    guard((old_beliefs,old_affect)==(next_state['actor']['beliefs'],next_state['actor']['affect']),
          'unlicensed personal psychology mutation')
    receipt=dict(id=ident,year=year,day=p['day'],action=action,actor='child',
                 objective_owner=MOCK_OWNER,grade=GRADE,source_ref=SOURCE,
                 prior_state_hash=prehash,rule_ref=MOCK_RULE)
    # Relevance stays in a DIFFERENT proposal-audit record, outside canonical event.
    receipt['hash']=digest(receipt)
    next_state['events'].append(receipt)
    state.clear();state.update(next_state)
    return receipt

def slow_tick(state: dict, year: int, start: int, end: int) -> None:
    """Time passage without a synthetic event or psychological delta."""
    if end > start:
        state['slow_ticks'].append(dict(year=year, from_day=start, to_day=end,
                                        owner='TEST_CLOCK_ONLY'))


def run(mode='ONE_CALL', variant='default', rules=None, initial=None):
    owner_rules = (dict(licensed_objective_actions=[
        'PRACTICE_OBSERVED', 'FAMILY_MOVE', 'PROJECT_TASK', 'FRIEND_MEETING',
        'COUNTERPART_CONTACT', 'OBSERVED_NEUTRAL', 'NEW_CLUB', 'TEACHER_MEETING',
        'SPEECH_EXPOSURE']) if rules is None else deepcopy(rules))
    state = deepcopy(initial) if initial is not None else initial_state()
    guard(isinstance(state,dict) and isinstance(state.get('events'),list), 'invalid initial prestate')
    guard(state.get('world',{}).get('source_ref')==SOURCE, 'unissued initial source')
    guard(state.get('current_year')==2020,'UNSUPPORTED_TEMPORAL_SCOPE: only full 2020 start accepted')
    # Backward time is forbidden. The resumed fixture may include partial 2020 history.
    for evt in state['events']:
        guard(isinstance(evt,dict) and type(evt.get('year'))==int and type(evt.get('day'))==int,
              'malformed historical event cursor')
    resumed_cursor=max((e['day'] for e in state['events'] if e['year']==2020),default=-1)
    guard(not any(e['year']>2020 for e in state['events']), 'UNSUPPORTED_TEMPORAL_SCOPE: future prestate')
    llm = InvocationMock(mode, variant)
    boundaries, decisions, revalidations, all_proposals, proposal_audits = [], [], [], [], []
    for year in (2020, 2021, 2022):
        inp = render_input(state, year)
        render, packet = llm.boundary(inp)
        rend = validate_render(render, inp)
        pkt, pending = validate_packet(packet, inp)
        before = digest(state)
        guard(before == inp['checkpoint_ref'], 'checkpoint stale before scheduling')
        guard(before == rend['causal_hash_before'], 'render modified checkpoint')
        all_proposals.extend(pkt['rejected'])
        # Proposal labels are independently auditable and excluded from causal receipts.
        proposal_audits.extend(dict(year=year,id=p['id'],candidate_hash=digest(p),
                    noncausal_relevance=deepcopy(p.get('possible_relevance_domains',[])))
                    for p in packet.get('candidates',[]) if isinstance(p,dict) and proper_str(p.get('id')))
        boundaries.append(dict(year=year, checkpoint_ref=before, render=rend,
                               prospective_validation=pkt,
                               physical_calls_so_far=llm.physical_calls))
        if year == 2022: break
        last_day = resumed_cursor if year==2020 else 0
        pending.sort(key=lambda p: (p['day'], p['id']))
        while pending:
            p = pending.pop(0)
            if year==2020 and p['day']<=resumed_cursor:
                decisions.append(dict(year=year,day=p['day'],id=p['id'],status='REFUSED_ELAPSED_CURSOR',
                                      owner=MOCK_OWNER,grade=GRADE,before=digest(state),after=digest(state)))
                continue
            slow_tick(state, year, last_day, p['day'])
            last_day = p['day']
            if any(e.get('id')==fact_id(year,p['id']) for e in state['events']):
                status='REFUSED_EXISTING_EVENT_ID'
            else:
                status=evaluate(state, p, owner_rules)
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
    return dict(mode=mode, proposal_audits=proposal_audits,
                proposal_audit_hash=digest(proposal_audits), mock_physical_invocations=llm.physical_calls,
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
