import pytest
from replay_sgi1 import execute
RESULT,SUMMARY=execute()
@pytest.mark.parametrize('case',RESULT['cases'],ids=lambda c:c['case_id'])
def test_literal_original_k11_case(case):
    assert case['n_assertions']==len(case['assertion_results'])
    assert all(case['assertion_results'].values()),case['assertion_results']
    assert SUMMARY['comparison'][case['case_id']]['equal']

def test_complete_denominator_and_offline():
    assert RESULT['n_cases']==24
    assert RESULT['n_assertions']==98
    assert RESULT['n_assertions_pass']==98
    assert SUMMARY['network_attempts']==[]
