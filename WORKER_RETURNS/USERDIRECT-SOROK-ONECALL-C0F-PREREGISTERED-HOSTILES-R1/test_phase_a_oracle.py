"""Preregistered Phase A only. Never imports C0 or author results.

Tests validate a *small independent boundary reference*, not native V3,
CAN008 psychology, or the C0 implementation. Expected columns are test oracles
and never supplied to the reference evaluator.
"""
from __future__ import annotations
import copy
import json
import os
import pathlib
import subprocess
import sys
import hashlib
import pytest
from frozen_oracle import run, causal_projection, digest
from preregistered_cases import CASES

ROOT = pathlib.Path(__file__).resolve().parent

@pytest.mark.parametrize('case', CASES, ids=lambda c:c['id']+'__'+c['family'])
def test_frozen_authority_boundary(case):
    result = run(copy.deepcopy(case['input']))
    for field, expected in case['expected'].items():
        assert result[field] == expected, (case['id'],field,expected,result[field])
    assert result['owner_grade']=='BOUNDED_TEST_ONLY_MOCK_NOT_CAN008_OR_WORLD_ISSUANCE'
    assert len(result['history_ids'])==len(case['input'].get('ledger',[]))+len(result['admitted_ids'])


def _sample():
    return copy.deepcopy(next(c['input'] for c in CASES if c['id']=='A08'))


def test_fixed_packet_two_call_one_call_same_owner_projection():
    outputs=[]
    for arm in ('ONE_CALL','TWO_CALL','FIXED_PACKET'):
        packet=_sample();packet['arm']=arm;outputs.append(run(packet))
    assert [o['physical_mock_calls'] for o in outputs]==[1,2,0]
    assert causal_projection(outputs[0])==causal_projection(outputs[1])==causal_projection(outputs[2])


def test_render_wording_cannot_change_causal_checksum():
    original=_sample(); alternate=copy.deepcopy(original)
    alternate['output']['retrospective']={'text_or_scene_fragments':['A whole invented novella'],
        'surface_inventions_only':['The invented teacher returns']}
    assert causal_projection(run(original))==causal_projection(run(alternate))


def test_proposal_contamination_direction_does_not_change_retrospective_checkpoint():
    clean=_sample();bad=copy.deepcopy(clean)
    bad['output']['retrospective']['asserted_fact_refs']=['later_future_project']
    bad['output']['prospective']['candidates'].append(dict(id='later_future_project',at=340,kind='ACTIVITY',
        actor_owner='MOCK_OWNER_TEST_ONLY',world_owner='MOCK_WORLD_TEST_ONLY'))
    a,b=run(clean),run(bad)
    assert b['render_refusals']==['REJECT_UNCOMMITTED_RETRO_FACT:later_future_project']
    assert b['pre_state_hash']==a['pre_state_hash']
    assert 'later_future_project' not in b['safe_render_refs']


def test_prior_material_history_not_demographic_scalar_controls_eligibility():
    a=next(c['input'] for c in CASES if c['id']=='A04'); b=copy.deepcopy(a)
    b['demographics']={'country':'EXACT_SAME','class':'X'}
    b['output']['prospective']['candidates']=[b['output']['prospective']['candidates'][1]]
    a2=copy.deepcopy(b);a2['location']='OLD_TOWN';b['location']='NEW_TOWN'
    assert run(a2)['admitted_ids']==['old_school_friend']
    assert run(b)['dispositions']['old_school_friend']=='INVALIDATED_CURRENT_CONTEXT'


def test_demographic_priors_only_do_not_update_psyche():
    p=_sample();q=copy.deepcopy(p)
    q['demographics']={'different_population_distribution':0.9987}
    assert causal_projection(run(p))==causal_projection(run(q))


def test_other_independent_response_changes_only_actually_admitted_meeting():
    q=next(c['input'] for c in CASES if c['id']=='A05');r=copy.deepcopy(q)
    r['output']['prospective']['candidates'][0]['other_response']='CONSENT'
    assert run(q)['admitted_ids']==[]
    assert run(r)['admitted_ids']==['requested_meet']
    assert run(r)['psyche']=={}


def test_event_order_is_causal_clock_not_packet_sort():
    p=_sample();q=copy.deepcopy(p)
    q['output']['prospective']['candidates'].reverse()
    assert causal_projection(run(p))==causal_projection(run(q))


def test_no_relevance_label_writes_psychology():
    a=_sample();b=copy.deepcopy(a)
    for v in b['output']['prospective']['candidates']:
        v['possible_relevance_domains']=['inner_revelation','trauma','spiritual_breakthrough']
        v['psyche_patch']={'self_concept':'NEW'}
    assert causal_projection(run(a))==causal_projection(run(b))


def test_missing_science_even_strong_score_does_not_select():
    q=next(c['input'] for c in CASES if c['id']=='A26');p=copy.deepcopy(q)
    p['output']['prospective']['candidates'][0]['score']=100000
    assert run(p)['dispositions']['proposed_job']=='DEFER_MISSING_RULE_OR_SOURCE_PERMISSION'


def test_all_refused_does_not_force_fallback_and_slow_time_passes():
    q=next(c['input'] for c in CASES if c['id']=='A10')
    r=run(q)
    assert r['admitted_ids']==[] and r['slow_time']==365 and r['psyche']=={}


def test_cold_separate_processes_replay_exact():
    path=ROOT/'cold_replay_probe.py'
    out=[]
    for seed in ('7','947'):
        env=dict(os.environ, PYTHONHASHSEED=seed)
        cp=subprocess.run([sys.executable,'-B',str(path)],cwd=ROOT,env=env,capture_output=True,text=True)
        assert cp.returncode==0,cp.stderr
        out.append(cp.stdout)
    assert out[0]==out[1]
    obj=json.loads(out[0]);assert obj['result']['admitted_ids']==['habit_1','qualified_activity','routine_walk']


def test_distinct_packet_content_can_have_different_contamination_rate_even_identical_call_structure():
    # Two independent calls may propose different content; exact quality equality
    # is NOT an invariant. Mock counts don't show price/performance.
    safe=_sample();unsafe=copy.deepcopy(safe)
    unsafe['output']['prospective']['candidates'][1]['requires_refs']=['render_only_illusion']
    assert run(safe)['dispositions']['qualified_activity']=='ADMITTED_MOCK_EXTERNAL_OCCURRENCE'
    assert run(unsafe)['dispositions']['qualified_activity']=='REFUSE_UNGROUNDED_PREREQUISITE'


def test_frozen_case_matrix_byte_identity():
    from preregistered_cases import document
    committed=json.loads((ROOT/'01_FROZEN_HOSTILE_MATRIX.json').read_text())
    assert committed==document()
    assert committed['test_count']==32
