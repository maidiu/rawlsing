import json
import pytest
from bridge import ROOT
from f1_adapter import run_case
from f1_boundary import envelope_gate

CASES=json.loads((ROOT/'imports/F1/court/f1_frozen_court/frozen_cases.json').read_text())['cases']

@pytest.mark.parametrize('case',CASES,ids=[c['case_id'] for c in CASES])
def test_frozen_case_boundary_or_explicit_nonapplicability(case):
    result=run_case(case)
    assert result['p1_invoked'] and not result['b1_response_invoked']
    assert result['actor_state_before']==result['actor_state_after']
    assert result['world_before']==result['world_after'] and result['committed_effect_count']==0
    if case['expected_gate'] in ('DENIED','DEFERRED'):
        assert result['status']==case['expected_gate']
        assert set(case['expected_reasons_subset']).issubset(result['reasons'])
        assert result['applicability']=='B2_BOUNDARY_NEGATIVE_OR_DEFERRAL'
    else:
        assert result['status']=='NOT_APPLICABLE_TO_THIS_LAB'
        assert result['reasons']
        assert result['b2_receipt']['event_admission']=='NOT_PERFORMED'
