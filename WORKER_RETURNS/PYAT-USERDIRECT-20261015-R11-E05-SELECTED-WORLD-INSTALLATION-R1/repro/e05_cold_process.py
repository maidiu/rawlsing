#!/usr/bin/env python3
"""Genuine separate-process R11 E05 selected-world cold replay.

Run twice in two distinct Python processes:

    python3 repro/e05_cold_process.py <runtime> <root> <mode>

``first``  precommits nothing itself (the register is already committed in
           freezes/), verifies that freeze byte-for-byte, serves all sinks and
           records the durable receipt values.
``replay`` loads in a fresh process, re-verifies the freeze, re-serves every
           sink and asserts the selected-world receipts are bit-identical.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

RUNTIME, ROOT = Path(sys.argv[1]), Path(sys.argv[2])
MODE = sys.argv[3]
OUTPUT = ROOT / 'observations'
OUTPUT.mkdir(parents=True, exist_ok=True)
sys.path[:0] = [str(RUNTIME)]

from product.service import GenericSelectedWorldService          # noqa: E402
from product.nonparent import consume                            # noqa: E402
from product.scenario import evaluate                            # noqa: E402
from rawlsing_next.pre553_hq297_n9c_two_field_reader import (     # noqa: E402
    TestOnlyRegistry)
import e05_n9_selected_world_adapter as E                        # noqa: E402

RETURN = Path('/Users/matthewsmith/Desktop/Rawlsing/WORKER_RETURNS/'
              'PYAT-USERDIRECT-20261015-R11-E05-SELECTED-WORLD-'
              'INSTALLATION-R1')
FREEZE = RETURN / 'freezes' / '01_PRECOMMITTED_SELECTED_WORLD_EXPECTED_VALUES.json'
FIXTURE = RUNTIME / 'WORKER_RETURNS' / \
    'PYAT-R3-HQ297-N9-TWO-FIELD-VALUES-READER-R1' / \
    '02_TWO_FIELD_TESTONLY_READER_AND_ASOF.json'
SNAPSHOTS = ('CURRENT_TEST_CLOCK', 'HISTORICAL_AS_OF',
             'TYPED_PARTIAL_PRE_NCA_PUBLICATION')
PROPOSALS = [dict(scenario_id='P_INSTITUTIONAL', route='institutional'),
             dict(scenario_id='P_CIVIL', route='civil')]

frozen_bytes = FREEZE.read_bytes()
frozen = json.loads(frozen_bytes)
assert frozen['committed_root'] == hashlib.sha256(json.dumps(
    {k: v for k, v in frozen.items() if k != 'committed_root'},
    sort_keys=True, separators=(',', ':')).encode()).hexdigest(), \
    'PRECOMMITTED_ROOT_NOT_REPRODUCIBLE'
(OUTPUT / 'precommitted_before_serving.json').write_bytes(frozen_bytes)

rows = json.loads(FIXTURE.read_text())['fields']
service = GenericSelectedWorldService(structural_revision=True)
adapter = E.N9SelectedWorldAdapter(
    service=service, registry=TestOnlyRegistry(rows))

prior = None
if MODE == 'replay':
    first = json.loads((OUTPUT / 'first.json').read_text())
    prior = {k: v['receipt_hash'] for k, v in first['receipts'].items()}

receipts = {}
for label in SNAPSHOTS:
    request = E.standard_request(label=label)
    snapshot = adapter.build_snapshot(request)
    acceptance = adapter.accept(request, snapshot)
    consumers = [consume(service, snapshot)['material'],
                 evaluate(service, snapshot, PROPOSALS)['material']]
    receipt = adapter.serve(request, acceptance, snapshot, consumers=consumers)
    receipts[label] = receipt

if MODE == 'replay':
    first = json.loads((OUTPUT / 'first.json').read_text())
    assert set(receipts) == set(first['receipts'])
    for label, receipt in receipts.items():
        before = first['receipts'][label]
        assert receipt['receipt_hash'] == before['receipt_hash'], \
            'COLD_REPLAY_RECEIPT_MISMATCH:' + label
        assert receipt['receipt_payload_sha256'] == before['receipt_payload_sha256'], \
            'COLD_REPLAY_PAYLOAD_MISMATCH:' + label
        assert receipt['empirical_steps'] == before['empirical_steps']
        assert receipt['structural_values'] == before['structural_values']
        assert receipt['native_field_readset']['values_read'] == \
            before['native_field_readset']['values_read']
    assert (OUTPUT / 'precommitted_before_serving.json').read_bytes() == frozen_bytes, \
        'COLD_REPLAY_PRECOMMIT_DRIFT'

(OUTPUT / f'{MODE}.json').write_text(json.dumps(
    dict(receipts=receipts, oc05={r['policy_id']: r for r in
                                  E.installation_manifest()},
         contract=E.CONTRACT), indent=2, default=str) + '\n')

positives = [k for k, r in receipts.items() if r['state'] ==
             'SELECTED_WORLD_VALUES_SERVED']
print(json.dumps({
    'mode': MODE,
    'contract': E.CONTRACT,
    'grade': receipts['CURRENT_TEST_CLOCK']['grade'],
    'operative_N9': receipts['CURRENT_TEST_CLOCK']['operative_N9'],
    'oc05_current_applicability': {
        r['policy_id']: r['current_applicability'] for r in
        E.installation_manifest()},
    'positive_sinks': positives,
    'typed_partial_sinks': [k for k, r in receipts.items() if r['state'] !=
                            'SELECTED_WORLD_VALUES_SERVED'],
    'receipt_hashes': {k: r['receipt_hash'] for k, r in receipts.items()},
    'payload_sha256': {k: r['receipt_payload_sha256'] for k, r in
                       receipts.items()},
    'empirical_fractions': [[c['raw_probability_exact_fraction']['$exact_fraction']
                             for c in s['cells'] if c['cell'] == '1'][0]
                            for s in receipts['CURRENT_TEST_CLOCK'][
                                'empirical_steps']],
    'native_units': receipts['CURRENT_TEST_CLOCK']['native_units'],
    'gss_numerator': next(r['values']['numerator'] for r in
                          receipts['CURRENT_TEST_CLOCK'][
                              'native_field_readset']['values_read']
                          if r['role'].startswith('GSS')),
    'nca_subscriptions': next(r['values']['active_subscriptions'] for r in
                              receipts['CURRENT_TEST_CLOCK'][
                                  'native_field_readset']['values_read']
                              if r['role'].startswith('NCA')),
    'committed_register_root': frozen['committed_root'],
    'source_grade': 'SOURCEFREE_TEST_ONLY_NOT_ISSUED',
}, indent=2))
