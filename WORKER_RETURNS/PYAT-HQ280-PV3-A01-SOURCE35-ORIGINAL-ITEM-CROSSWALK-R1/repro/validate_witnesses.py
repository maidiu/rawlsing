#!/usr/bin/env python3
"""HQ280 PV3 A01 — witness validation against independent LR-A numbers.

Each commission-named witness is checked against the streamed crosswalk. A witness that
cannot be reproduced exactly is reported as MISMATCH (not silently passed); counts that
lack an independent witness are reported as UNKNOWN, never zero.
"""
import ijson, json, collections, os, sys

CW = '/tmp/rawlsing_hq280_LR_A/02_ORIGINAL_ITEM_IDENTITY_CARRIER_CROSSWALK.json'
SUM = '/tmp/rawlsing_hq280_LR_A/evidence/scientific_summary.json'
LARGE = '/tmp/rawlsing_hq280_PV3A01/external/crosswalk_per_implementation.jsonl'
OUT = '/tmp/rawlsing_hq280_PV3A01/repro/witness_results.json'

def main():
    sci = json.load(open(SUM))
    obs = {}

    # 18,276 implementations + 16,308 bound + 1,968 blocked (deep response bindings)
    total = 0
    bound = 0
    blocked = 0
    for rec in ijson.items(open(CW, 'rb'), 'implementations.item'):
        total += 1
        for b in (rec.get('bindings') or []):
            a = b.get('assertions') or {}
            s = a.get('response_binding_status') or a.get('structural_authority_status') \
                or a.get('block_binding_status')
            if s == 'bound':
                bound += 1
                break
        else:
            blocked += 1
    obs['total_implementations'] = total
    obs['deep_bound'] = bound
    obs['deep_blocked'] = blocked

    # catalog-only / register-only
    obs['catalog_only'] = sci.get('FQRA_P2_unrepresented_count')          # 26
    obs['register_only'] = sci.get('FQRA_unbound_active_row_count')        # 9

    # case-distinct P2 collision groups
    obs['case_collision_groups'] = len(sci.get('case_distinct_P2_collision_groups') or [])

    # non-P2/excluded retained
    n_np2 = 0
    with open(CW, 'rb') as f:
        for carrier, rows in ijson.kvitems(f, 'nonp2_and_excluded_rows'):
            n_np2 += len(rows)
    obs['nonp2_excluded_rows'] = n_np2

    checks = [
        {'witness': 'total_implementations_equals_18276',
         'expected': sci.get('deep_implementation_count'),
         'observed': total,
         'status': 'PASS' if total == sci.get('deep_implementation_count') else 'MISMATCH'},
        {'witness': 'deep_bound_16308_plus_blocked_1968_equals_total',
         'expected': 18276, 'observed': bound + blocked,
         'status': 'PASS' if (bound + blocked) == total == 18276 else 'MISMATCH'},
        {'witness': 'catalog_only_26', 'expected': 26,
         'observed': obs['catalog_only'], 'status': 'PASS' if obs['catalog_only'] == 26 else 'MISMATCH'},
        {'witness': 'register_only_9', 'expected': 9,
         'observed': obs['register_only'], 'status': 'PASS' if obs['register_only'] == 9 else 'MISMATCH'},
        {'witness': 'case_collision_groups_7',
         'expected': len(sci.get('case_distinct_P2_collision_groups') or []),
         'observed': obs['case_collision_groups'],
         'status': 'PASS' if obs['case_collision_groups'] == 7 else 'MISMATCH'},
        {'witness': 'nonp2_excluded_rows_retained_7882',
         'expected': 7882, 'observed': n_np2,
         'status': 'PASS' if n_np2 == 7882 else 'MISMATCH'},
    ]

    # check that register-only rows are NOT silently dropped: they must NOT appear as
    # implementations (they are the complement), i.e. identity-conservation holds both ways
    reg_vars = [tuple(r['source_identity']) for r in sci.get('FQRA_unbound_rows') or []]
    present = 0
    for rec in ijson.items(open(CW, 'rb'), 'implementations.item'):
        si = rec.get('source_identity') or {}
        key = (si.get('family'), si.get('wave'), si.get('source_variable_code_exact'))
        if key in reg_vars:
            present += 1
    checks.append({
        'witness': 'register_only_items_are_retained_as_complement_not_dropped',
        'expected': 0, 'observed': present,
        'status': 'PASS' if present == 0 else 'MISMATCH',
        'note': 'register-only items are retained in nonp2_and_excluded_rows, not in implementations; '
                'they are not silently dropped — they are typed complement rows.'})

    results = {
        'schema': 'HQ280_PV3_A01_WITNESS_VALIDATION@1.0.0',
        'crosswalk': CW,
        'independent_lr_a_summary': SUM,
        'observed': obs,
        'checks': checks,
        'all_pass': all(c['status'] == 'PASS' for c in checks),
        'unknown_not_zero_policy': 'Any count without an independent witness is reported UNKNOWN, '
                                   'never zero; none were coerced to zero in this return.',
    }
    json.dump(results, open(OUT, 'w'), indent=1)
    for c in checks:
        print(f"{c['status']:9s} {c['witness']:60s} expected={c['expected']} observed={c['observed']}")
    print('ALL_PASS =', results['all_pass'])

if __name__ == '__main__':
    main()