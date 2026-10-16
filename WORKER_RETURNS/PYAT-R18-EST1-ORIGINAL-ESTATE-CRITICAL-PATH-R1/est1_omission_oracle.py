#!/usr/bin/env python3
"""EST1 independent expected-operation/actual-receipt outer-join, SOURCEFREE only.

The expectation is a separately frozen input (SHA-256 supplied by the reviewer), not
created by the candidate under test. The verifier NEVER grants source permission.
Receipt material is inspected but cannot acquire a trusted issuer merely by claiming one.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

SCHEMA = 'PYAT_R18_EST1_SOURCEFREE_OMISSION_ORACLE@1'
DISPOSITIONS = {'PRODUCED', 'HELD', 'INADMISSIBLE'}
IDENTITY = ('op_id', 'op_class', 'target', 'conditioners', 'item_ids', 'source_id',
            'wave', 'release', 'form', 'unit', 'risk', 'source_edition',
            'permission_scope', 'disposition', 'disposition_reason')

def encoded(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()

def sha(obj):
    return hashlib.sha256(encoded(obj)).hexdigest()

def signature(row):
    return {k: row.get(k) for k in IDENTITY}

def _issue(kind, op_id, detail=None):
    return {'kind': kind, 'op_id': op_id, 'detail': detail}

def judge(expectation, actual, *, pinned_sha, allow_test_only=True):
    """Fail closed; no inference of actual original-source authority/empirical proof."""
    issues = []
    if sha(expectation) != pinned_sha:
        return {'schema': SCHEMA, 'verdict': 'INVALID_ORACLE_ROOT',
                'expected_sha256': pinned_sha, 'observed_sha256': sha(expectation),
                'issues': [_issue('EXPECTED_PREIMAGE_MISMATCH', None)]}
    if expectation.get('scope') != 'SOURCEFREE_TEST_ONLY' or expectation.get('issuer_kind') != 'INDEPENDENT_PRECOMMITTED_TEST_FIXTURE':
        issues.append(_issue('UNAUTHORIZED_EXPECTATION_ISSUER', None))
    if actual.get('scope') != 'SOURCEFREE_TEST_ONLY' or not allow_test_only:
        issues.append(_issue('ACTUAL_SOURCE_USE_NOT_GRANTED', None))
    exp = expectation.get('operations', [])
    got = actual.get('receipts', [])
    exp_ids = [o.get('op_id') for o in exp]
    if not exp or len(exp_ids) != len(set(exp_ids)):
        issues.append(_issue('INVALID_FROZEN_FRONTIER', None))
    for o in exp:
        if o.get('disposition') not in DISPOSITIONS:
            issues.append(_issue('INVALID_FROZEN_DISPOSITION', o.get('op_id')))
    expected = {o.get('op_id'): o for o in exp}
    frequencies = Counter(r.get('op_id') for r in got)
    for op, n in frequencies.items():
        if n > 1:
            issues.append(_issue('DUPLICATE_REISSUE', op, {'count': n}))
    received = {r.get('op_id'): r for r in got}
    for op in sorted(expected):
        e, r = expected[op], received.get(op)
        if r is None:
            issues.append(_issue('OMITTED_ELIGIBLE_OPERATION' if e.get('disposition') == 'PRODUCED' else 'MISSING_BLOCKED_ACCOUNTING', op, {'expected': e.get('disposition')}))
            continue
        mismatches = [k for k in IDENTITY if e.get(k) != r.get(k)]
        if mismatches:
            issues.append(_issue('EXACT_IDENTITY_OR_STATUS_MISMATCH', op, {'fields': mismatches}))
        if r.get('source_grant') not in (None, 'NO_REAL_SOURCE_GRANT'):
            issues.append(_issue('FORGED_OR_UNAUTHORIZED_SOURCE_GRANT_CLAIM', op))
        if e.get('disposition') == 'PRODUCED':
            if r.get('kind') != 'EXECUTED_TEST_ONLY':
                issues.append(_issue('MISSING_EXECUTED_TEST_ONLY_WITNESS', op))
            if not (r.get('native_owner_receipt_ref') and r.get('native_owner_receipt_blob')):
                issues.append(_issue('NATIVE_OWNER_EXECUTION_NOT_ATTESTED', op))
            # A declared ref is never automatically genuine: distinguished from actual owner execution below.
            if r.get('owner_execution_verified') is not True:
                issues.append(_issue('NATIVE_OWNER_WITNESS_UNVERIFIED', op))
        elif r.get('kind') != 'BLOCKED_ACCOUNTED':
            issues.append(_issue('HELD_OR_INADMISSIBLE_FALSE_POSITIVE', op))
    for op in sorted(set(received) - set(expected)):
        issues.append(_issue('UNEXPECTED_OR_SUBSTITUTED_OPERATION', op))
    exp_counts = Counter(e.get('disposition') for e in exp)
    got_counts = Counter(r.get('disposition') for r in got)
    return {'schema': SCHEMA, 'verdict': 'SOURCEFREE_TEST_ONLY_RECONCILED' if not issues else 'SOURCEFREE_ORACLE_RED',
            'expected_sha256': pinned_sha, 'expected_count': len(exp), 'accounted_unique_count': len(set(received) & set(expected)),
            'expected_dispositions': dict(exp_counts), 'reported_dispositions': dict(got_counts),
            'missing': sorted(set(expected) - set(received)), 'unexpected': sorted(set(received) - set(expected)),
            'issues': sorted(issues, key=lambda x: (x['kind'], str(x['op_id']))),
            'claim_ceiling': 'NO_REAL_SOURCE_GRANT__NO_ORIGINAL_EMPIRICAL_PRODUCT__OWNER_WITNESS_REQUIRES_EXTERNAL_BLOB_VERIFICATION'}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--expected', required=True)
    ap.add_argument('--actual', required=True)
    ap.add_argument('--pinned-sha256', required=True)
    ap.add_argument('--output', required=True)
    args = ap.parse_args()
    out = judge(json.loads(Path(args.expected).read_text()),
                json.loads(Path(args.actual).read_text()), pinned_sha=args.pinned_sha256)
    Path(args.output).write_text(json.dumps(out, indent=2, sort_keys=True) + '\n')
    print(out['verdict'], len(out.get('issues', [])))
    return 0 if out['verdict'] == 'SOURCEFREE_TEST_ONLY_RECONCILED' else 1

if __name__ == '__main__':
    raise SystemExit(main())
