"""Versioned successor oracle: derive expectations from explicit risk semantics.
Never imports or calls the candidate. Frozen GF1F oracle remains unchanged.
"""
import copy
import hashlib
import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
F = 'WORKER_RETURNS/PYAT-R28-GF1F-IMPLEMENTED-NATIVE-CONSUMER-INDEPENDENT-R1'
PIN = '3dcc7d7dddfff4f1be8b4293cab92e5b4275007d'
CELLS = ('00', '01', '10', '11')


def expected_class(cells, eligible):
    total = sum(cells.values())
    assert eligible >= total >= 0
    if eligible == 0:
        return 'UNDETERMINED_NO_ELIGIBLE_RISK'
    if total == 0:
        return 'UNDETERMINED_ZERO_SUPPORT_RISK'
    supports = [{t for t in ('0', '1') if cells[c + t] > 0} for c in ('0', '1')]
    if any(not row for row in supports):
        return 'UNDETERMINED_NO_ELIGIBLE_RISK'
    if all(len(row) == 1 for row in supports) and supports[0] != supports[1]:
        return 'EXACT_PAIR_SEPARATION'
    return 'NO_PAIR_SEPARATION'


def main():
    raw = subprocess.check_output(['git', 'show', PIN + ':' + F + '/01_INDEPENDENT_FROZEN_PAIR_ORACLE.json'], cwd=REPO)
    oracle = copy.deepcopy(json.loads(raw))
    oracle['schema'] = 'GF1F_CURRENT_QUALIFICATION_ORACLE@2'
    oracle['phase'] = 'USER_AUTHORIZED_CURRENT_RECONCILIATION; NOT AN INDEPENDENT PREFREEZE'
    oracle['historical_source'] = dict(commit=PIN, path=F + '/01_INDEPENDENT_FROZEN_PAIR_ORACLE.json', sha256=hashlib.sha256(raw).hexdigest())
    oracle['classification_rule'] = 'eligible=0 -> NO_ELIGIBLE_RISK; eligible>0 and total=0 -> ZERO_SUPPORT_RISK; otherwise classify explicit row supports without inventing support.'
    oracle['contract_refs'] = dict(
        GF1G_phase_a='ecd975ad5b424f952ac248dfcf1b7a83aa867a6a',
        GF1G_final='ec5dddfcb3476c01ceb8e7f5122c5e5259b936f7',
        tests=['g09 no_eligible_risk/all_zero_observed_zero', 'g10 missing states', 'g11 typed zero support', 'g14 supported empty profile'])
    for row in oracle['universe']:
        row['expected_class'] = expected_class(row['cells'], row['eligible'])
    for name, case in oracle['named_cases'].items():
        cells = {key: case[key] for key in CELLS}
        case['eligible'] = 2 if name == 'zero_supported_risk' else sum(cells.values())
        case['expected_class'] = expected_class(cells, case['eligible'])
    # Enumeration's risk=sum(cells) cannot contain positive-risk/zero-support.
    # Add it explicitly to cold coverage rather than falsely claiming coverage.
    zero = dict(cells={key: 0 for key in CELLS}, eligible=2)
    zero['expected_class'] = expected_class(zero['cells'], zero['eligible'])
    oracle['cold_extra_cases'] = [dict(case_id='0000_eligible2', **zero)]
    counts = {}
    for row in oracle['universe']:
        counts[row['expected_class']] = counts.get(row['expected_class'], 0) + 1
    oracle['class_counts'] = counts
    cold_counts = dict(counts)
    for row in oracle['cold_extra_cases']:
        cold_counts[row['expected_class']] = cold_counts.get(row['expected_class'], 0) + 1
    oracle['cold_class_counts'] = cold_counts
    (HERE / 'gf1f/01_CURRENT_PAIR_ORACLE.json').write_text(json.dumps(oracle, indent=2, sort_keys=True) + '\n')
    print('Independent-of-candidate oracle derivation:', len(oracle['universe']), 'universe cases,', sum(cold_counts.values()), 'cold cases')


if __name__ == '__main__':
    main()
