#!/usr/bin/env python3
"""Recovered R1–R3 invariants: independently reconstructed synthetic regression tests, not original test files."""
from test_r5 import fixture
from anvil import validate,outputs
import copy,json
s=fixture(); assert not validate(s),validate(s)
errors={}
def attack(name,mut,marker):
    x=copy.deepcopy(s);mut(x);a=validate(x)
    assert any(marker in k for k in a),(name,a[:10]);errors[name]=marker
attack('missing_one_of_118',lambda x:x['coverage']['K1_CAP'].pop('K1-CAP-01'),'MISSING_COVERAGE')
attack('false_historical_adoption',lambda x:x['coverage']['PYAT_PC']['PYAT-PC-R9-01'].update(adopted=True),'UNAUTHORIZED_PROPOSAL_ADOPTION')
attack('false_P4R_closure',lambda x:x['coverage']['P4R']['P4R-R01'].update(closed=True),'FALSE_P4R_CLOSURE')
attack('missing_B_independent',lambda x:x['decisions'][1]['alternatives'].pop(1),'NO_INDEPENDENT_B_ALTERNATIVE')
attack('invalid_boundary_identity',lambda x:x['boundaries']['T2'].update(contract_name='arbitrary'),'REDEFINED_BOUNDARY')
attack('broken_source_to_consumer',lambda x:x['architecture']['first_consumer_path'].pop(),'INVALID_GLOBAL_FIRST_CONSUMER_PATH')
attack('changed_type_carry',lambda x:x['architecture']['edges'][0].update(data_type='wrong_type'),'GLOBAL_TYPE_MISMATCH')
attack('incorrect_replay_or_estimate',lambda x:x['epistemic_case'].update(true_three_way_joint=False),'MISSING_TRUE_HIGH_ORDER_JOINT')
attack('fake_author_g5',lambda x:x['authority'].update(independent_review='ACCEPTED'),'AUTHOR_MINTED_INDEPENDENT_RECEIVING')
attack('false_source_rights',lambda x:x['authority'].update(source_rights_granted=True),'AUTHOR_MINTED_DOWNSTREAM_AUTHORITY')
assert len(outputs(s))==6
assert len(outputs(s)['COVERAGE_TO_DECISION.tsv'].decode().splitlines())==119
print(json.dumps({'status':'PASS_RECONSTRUCTED_SYNTHETIC_LEGACY_REGRESSIONS','count':len(errors),'errors':errors},indent=2))
