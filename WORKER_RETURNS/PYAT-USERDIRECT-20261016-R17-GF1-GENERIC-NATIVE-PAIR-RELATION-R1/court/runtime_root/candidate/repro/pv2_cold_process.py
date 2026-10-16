"""Genuine separate-process PV2 cold replay through the accepted owners.

Run twice in two distinct Python processes:

    python3 repro/pv2_cold_process.py <repo> <root> <mode>

``first``  persists the precommitted register and original expected preimages
           BEFORE any Route B / I03 / I05 producer call, executes every runnable
           obligation through the real C11 / I03 / I05 / P01 owners and records
           the durable executor call counts.
``replay`` loads in a fresh process, verifies the precommitted register and the
           persisted preimages byte-for-byte, re-serves all six values and
           asserts zero additional durable executor calls.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from pathlib import Path

REPO, ROOT = Path(sys.argv[1]), Path(sys.argv[2])
MODE = sys.argv[3]
OUTPUT = ROOT / 'observations'
OUTPUT.mkdir(parents=True, exist_ok=True)

spec = importlib.util.spec_from_file_location(
    'pv2_fixture', str(REPO / 'repro' / 'pv2_sourcefree_fixture.py'))
fixture = importlib.util.module_from_spec(spec)
sys.modules['pv2_fixture'] = fixture
spec.loader.exec_module(fixture)

import pv2_original_scope_register as PV2  # noqa: E402
from rawlsing_next.pre553_empirical_objects import ExactRef  # noqa: E402

# Independently author the register from scratch in this process.
register = PV2.author_sourcefree_original_scope_register()
binding = register.binding()
register_digest = PV2.frozen_root_from_payload(binding)
assert register_digest == register.committed_root, 'REGISTER_ROOT_UNSTABLE'

frozen_path = REPO / 'freezes' / \
    '01_PRECOMMITTED_ORIGINAL_EXPECTED_SET_AND_SOURCE_IDENTITY.json'
frozen = json.loads(frozen_path.read_text())
assert frozen['committed_root'] == register.committed_root, \
    'PRECOMMITTED_REGISTER_MISMATCH'
assert PV2.frozen_root_from_payload(frozen['register_binding']) == \
    frozen['committed_root'], 'PRECOMMITTED_ROOT_NOT_REPRODUCIBLE'
(OUTPUT / 'register_before_production.json').write_text(
    json.dumps(frozen, indent=2, sort_keys=True) + '\n')

fx = fixture.pv2_sourcefree_fixture(ROOT / 'ledger')
plans, calls = fx['plans'], fx['calls']
expected = fx['expected']

# The original expected preimages must be persisted BEFORE any owner producer.
if MODE == 'first':
    (OUTPUT / 'expected_before_production.json').write_text(expected.payload_json + '\n')
else:
    assert (OUTPUT / 'expected_before_production.json').read_text() == \
        expected.payload_json + '\n', 'PRECOMMITTED_EXPECTED_PREIMAGE_MISMATCH'
    assert (OUTPUT / 'register_before_production.json').read_text() == \
        json.dumps(frozen, indent=2, sort_keys=True) + '\n', 'PRECOMMITTED_REGISTER_DRIFT'

prior = None
if MODE == 'replay':
    first = json.loads((OUTPUT / 'first.json').read_text())
    prior = {l['original_expected_work_key']: ExactRef(**l['consumer_ref'])
             for l in first['links']}

before = [len(c) for c in calls]
report = PV2.run_sourcefree_with_register(
    expected=expected, selected_scopes=plans, register=register,
    scope_metadata=tuple(fx['meta']), prior_consumer_refs=prior)
assert report['ok'] is True, report
assert len(report['links']) == 6 and len(report['nonrunnable']) == 2
assert report['pv2_role_topology_verified'] is True

if MODE == 'replay':
    assert report['links'] == first['links'], 'COLD_REPLAY_LINK_MISMATCH'
    assert report['nonrunnable'] == first['nonrunnable'], 'COLD_REPLAY_HELD_MISMATCH'
    assert report['pv2_register'] == first['pv2_register'], 'COLD_REPLAY_ROOT_MISMATCH'
    assert [len(c) for c in calls] == before, 'COLD_REPLAY_ADDITIONAL_DURABLE_CALLS'
    assert all(r['run']['executed'] == [] for r in report['owner_reports']), \
        'COLD_REPLAY_RE_EXECUTED_OWNER_UNITS'
    assert all(r['recovery']['recovery_safe'] is True for r in report['owner_reports'])
    # The persisted original inventory anchor must be identical.
    assert (OUTPUT / 'expected_before_production.json').read_text() == \
        expected.payload_json + '\n'
else:
    assert [len(c) for c in calls] == [3, 3], 'FIRST_PROCESS_DURABLE_CALLS'

(OUTPUT / f'{MODE}.json').write_text(json.dumps(report, indent=2, default=list) + '\n')

print(json.dumps({
    'mode': MODE, 'ok': report['ok'],
    'committed_register_root': report['pv2_register']['committed_root'],
    'source_inventory_root': report['pv2_register']['source_inventory_root'],
    'original_expected_work_keys': len(report['links']),
    'distinct_legacy_v2_keys': len(
        {l['legacy_expected_work_key'] for l in report['links']}),
    'distinct_field_forge_consumers': len(
        {json.dumps(l['consumer_ref'], sort_keys=True) for l in report['links']}),
    'durable_executor_calls': [len(c) for c in calls],
    'held_original_records': len(report['nonrunnable']),
    'expected_payload_sha256': hashlib.sha256(
        expected.payload_json.encode()).hexdigest(),
    'source_grade': 'SOURCEFREE_TEST_ONLY_NOT_ISSUED',
    'schema': PV2.SCHEMA}, indent=2))
