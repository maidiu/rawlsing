#!/usr/bin/env python3
"""B53H R2 *trusted-oracle structural* verifier, NOT an executor or adoptive gate.

The caller MUST load `policy` from a protected independent CI checkout and
`result` from a trusted CI-runner-generated file, not from candidate Git content.
Even green means a structural crosswalk only, not native, scientific or N11 PASS.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
from pathlib import Path

HEX40 = re.compile(r'^[0-9a-f]{40}$')
HEX64 = re.compile(r'^[0-9a-f]{64}$')
SCHEMA = 'B53H_TRUSTED_ORACLE_PREFLIGHT@2'


def digest(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()).hexdigest()


def analyze(policy, expected_policy_sha256, result):
    failures = []
    def must(ok, cause):
        if not ok:
            failures.append(cause)
    must(bool(HEX64.fullmatch(expected_policy_sha256)), 'BAD_EXTERNALLY_PINNED_POLICY_SHA')
    must(digest(policy) == expected_policy_sha256, 'POLICY_PIN_MISMATCH')
    must(policy.get('schema') == SCHEMA, 'POLICY_SCHEMA')
    must(bool(HEX40.fullmatch(result.get('candidate_commit', ''))), 'CANDIDATE_COMMIT_MISSING')
    # Scope is governed by independent policy rather than candidate proposal.
    canonical = policy.get('original35', [])
    ids = [r.get('id') for r in canonical]
    must(len(ids) == len(set(ids)) == 35, 'TRUSTED_35_ROSTER_INVALID')
    must(sum(r.get('format') == 'SAV' for r in canonical) == 31, 'TRUSTED_31_SAV_INVALID')
    must(sum(r.get('format') == 'DTA' for r in canonical) == 4, 'TRUSTED_4_DTA_INVALID')
    listed = result.get('original35', [])
    given = [r.get('id') for r in listed]
    must(len(given) == 35 and len(set(given)) == 35 and set(given) == set(ids), 'SOURCE_ROSTER_ANTI_JOIN')
    for row in listed:
        if row.get('grade') in {'UNKNOWN', 'NO_RIGHT', 'NO_SCIENCE'}:
            must(row.get('original_u') is None and row.get('original_e_pre') is None,
                 'HOLD_AS_FALSE_ZERO_OR_PRODUCT:' + str(row.get('id')))
            must(bool(row.get('hold_reason')), 'UNEXPLAINED_HOLD:' + str(row.get('id')))
    # Trusted executor's fixture IDs and source geometries come from protected policy.
    expected = policy.get('fixtures', [])
    fixture_ids = [f.get('id') for f in expected]
    must(len(fixture_ids) >= 3 and len(set(fixture_ids)) == len(fixture_ids), 'TRUSTED_FIXTURE_UNIVERSE_INSUFFICIENT')
    shapes = set()
    classes = set()
    fmts = set()
    families = set()
    for f in expected:
        # Shape fingerprint intentionally excludes source id and variable spelling.
        shape = f.get('structural_topology')
        must(isinstance(shape, dict) and bool(shape), 'TRUSTED_SHAPE_MISSING:' + str(f.get('id')))
        if isinstance(shape, dict):
            shapes.add(digest(shape))
        fmts.add(f.get('format'))
        families.add(f.get('family'))
        classes.update(f.get('edge_classes', []))
    must(len(shapes) >= 3, 'INSUFFICIENT_GENUINE_SHAPE_DIVERSITY')
    must(len(families) >= 2 and fmts >= {'SAV', 'DTA'}, 'INSUFFICIENT_FAMILY_OR_FORMAT_DIVERSITY')
    must(set(policy.get('mandatory_edge_classes', [])) <= classes, 'REQUIRED_EDGE_CLASS_UNCOVERED')
    expected_by = {f.get('id'): f for f in expected}
    actual = result.get('fixture_runs', [])
    by_id = {f.get('id'): f for f in actual}
    must(len(actual) == len(set(f.get('id') for f in actual)) == len(expected) and
         set(by_id) == set(expected_by), 'FIXTURE_EXPECTED_ACTUAL_ANTI_JOIN')
    for ident, source in expected_by.items():
        row = by_id.get(ident, {})
        # Expected set and shape MUST be from independent policy; candidate cannot
        # define its own oracle or promote excluded operations by rehashing them.
        want = source.get('expected_operation_states', {})
        got = row.get('operation_states', {})
        must(isinstance(want, dict) and bool(want) and got == want, 'OPERATION_STATE_ANTI_JOIN:' + str(ident))
        must(row.get('frozen_pre_outcome_root') == source.get('pre_outcome_root'),
             'PRE_OUTCOME_ROOT_MISMATCH:' + str(ident))
        must(row.get('public_call_trace_id') is not None, 'GENERIC_CALL_TRACE_MISSING:' + str(ident))
        must(row.get('actual_native_c11') is True and row.get('actual_native_i03') is True,
             'NATIVE_C11_I03_UNOBSERVED:' + str(ident))
        if source.get('i05_required'):
            must(row.get('actual_native_i05') is True, 'I05_UNOBSERVED:' + str(ident))
        must(row.get('grade') == 'SOURCEFREE_TEST_ONLY', 'ORIGINAL_SCIENCE_GRADE_PROMOTED:' + str(ident))
    # Actual metamorphic tests must supply trusted runner event objects, not
    # candidate boolean assurances; this verifier still cannot authenticate them.
    metamorphic = result.get('metamorphic_events', [])
    must(any(x.get('kind') == 'RENAMING' and x.get('source_fixture') in expected_by
             and x.get('same_normalized_op_root') and x.get('same_consumer_value_root')
             and x.get('no_reserved_fixture_ids') for x in metamorphic), 'RENAMING_WITNESS_MISSING')
    must(any(x.get('kind') == 'MUTATION' and x.get('baseline') == 'PASS'
             and x.get('mutant') == 'ASSERTION_FAILED' and x.get('cold_restore') == 'PASS'
             and x.get('real_consumer_id') for x in metamorphic), 'CONSUMER_RED_RESTORE_MISSING')
    must(result.get('original_science_claim') == 'HOLD', 'SCIENTIFIC_ORIGINAL_CLAIM_ELEVATED')
    return {'status': 'REVISE' if failures else 'STRUCTURAL_CROSSWALK_READY_FOR_INDEPENDENT_NATIVE_VALIDATION',
            'failures': sorted(set(failures)),
            'limit': 'NO_NATIVE_EXECUTION_OR_ATTESTATION_VALIDATED_HERE',
            'cannot_issue': ['SOURCE_RIGHT', 'SCIENTIFIC_MEANING', 'UNIVERSAL_ACCEPT', 'N11', 'N12']}


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--trusted-policy', required=True)
    p.add_argument('--expected-policy-sha256', required=True)
    p.add_argument('--trusted-runner-result', required=True)
    a = p.parse_args()
    outcome = analyze(json.loads(Path(a.trusted_policy).read_text()), a.expected_policy_sha256,
                      json.loads(Path(a.trusted_runner_result).read_text()))
    print(json.dumps(outcome, indent=2))
    return 2 if outcome['failures'] else 0

if __name__ == '__main__':
    raise SystemExit(main())
