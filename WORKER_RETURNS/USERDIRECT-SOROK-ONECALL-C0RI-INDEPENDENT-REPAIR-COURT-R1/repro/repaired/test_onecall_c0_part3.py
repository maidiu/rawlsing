"""ONECALL-C0 R01–R17: TEST_ONLY real executable sourcefree adversaries.

PASS here means only the named boundary against the authored mock, NOT
native Sorok F1/B3 psychological science or independent I2 acceptance.
"""
from copy import deepcopy
import subprocess
import sys
from pathlib import Path

import pytest
import onecall_c0 as oc


@pytest.fixture(scope='module')
def result():
    return oc.run()


def decisions(r):
    return {d['id']: d for d in r['causal']['decisions']}


def by_id(r, cid):
    return [x for x in r['causal']['final_state']['events'] if x['id'].endswith(':'+cid)]


def by_rejection(r):
    return {x['id']:x for x in r['causal']['proposal_rejections']}


def test_R15_same_process_replay_exact():
    a,b = oc.run(),oc.run()
    assert a['causal']['receipt_hash'] == b['causal']['receipt_hash']
    assert a['causal']['final_state'] == b['causal']['final_state']


def test_R15_external_distinct_processes():
    script = Path(oc.__file__).resolve()
    x = subprocess.run([sys.executable,str(script)],text=True,capture_output=True,check=True).stdout
    y = subprocess.run([sys.executable,str(script)],text=True,capture_output=True,check=True).stdout
    assert x == y
    assert '"causal_hash"' in x


def test_R16_model_cannot_apply_CAN011_ADP016(result):
    rejects = by_rejection(result)
    assert rejects['covert_memory']['reason'] == 'UNISSUED_PSYCHOLOGICAL_EFFECT'
    assert rejects['invented_betrayal']['reason'] == 'UNISSUED_PSYCHOLOGICAL_EFFECT'
    assert result['causal']['final_state']['actor']['beliefs'] == 'UNISSUED'


def test_R16_top_level_effect_cannot_be_launched():
    inp=oc.render_input(oc.initial_state(),2020)
    _,p=oc.mocked_artifacts(inp)
    p['CAN011_UPDATE']={'memory':'fake'}
    with pytest.raises(AssertionError,match='top-level effect'):
        oc.validate_packet(p,inp)


def test_R17_onecall_contamination_stress_selects_two_call_fallback():
    comparison=oc.mode_comparison('combined_contamination')
    assert comparison['selected_research_fallback']=='TWO_CALL'
    assert comparison['causal_equal'] is False  # audit rejects disclose contamination
    assert any(k=='extra_fabricated_teacher' for k,_ in comparison['rejected']['ONE_CALL'])
    assert not any(k=='extra_fabricated_teacher' for k,_ in comparison['rejected']['TWO_CALL'])


def test_R17_baseline_all_three_logically_equivalent():
    c=oc.mode_comparison()
    assert c['causal_equal']
    assert c['selected_research_fallback']=='ONE_CALL'
    assert c['physical_mock_invocations']=={'ONE_CALL':3,'TWO_CALL':4,'FIXED_PACKET':0}


def test_EXTRA_each_year_and_three_event_opportunities(result):
    assert [b['year'] for b in result['boundaries']] == [2020,2021,2022]
    assert len([d for d in result['causal']['decisions'] if d['year']==2020]) >= 3
    assert len([d for d in result['causal']['decisions'] if d['year']==2021]) >= 3
    assert len(result['causal']['final_state']['events']) >= 3


def test_EXTRA_candidate_unknown_referent_cannot_create_person():
    inp=oc.render_input(oc.initial_state(),2020); _,p=oc.mocked_artifacts(inp)
    p['candidates'].append(oc.candidate(2020,13,'unknown_person','TEACHER_MEETING', prerequisites=['person:invented']))
    _,items=oc.validate_packet(p,inp)
    assert 'unknown_person' not in {x['id'] for x in items}

