#!/usr/bin/env python3
"""HQ280 PV3 A01 — carrier/instrument anti-join + topology gap derivation.

Anti-join direction is explicit and bidirectional at the governed grain:
  (a) per implementation -> which carriers FAIL to bind it (absent carrier evidence);
  (b) per carrier      -> which implementations that carrier asserts but that the
      registry/other carriers do not corroborate (unmatched, inner-join omission bait).
Nothing here confers semantic adoption; all gaps are documentary anti-joins.
"""
import ijson, json, hashlib, collections, os

CW = '/tmp/rawlsing_hq280_LR_A/02_ORIGINAL_ITEM_IDENTITY_CARRIER_CROSSWALK.json'
OUT = '/tmp/rawlsing_hq280_PV3A01'

def main():
    # first pass: enumerate the full carrier universe + per-implementation carrier sets
    per_impl_carriers = {}     # iid -> set(carriers)
    carrier_universe = set()
    fam_wave = {}
    for rec in ijson.items(open(CW, 'rb'), 'implementations.item'):
        iid = rec.get('question_implementation_id')
        si = rec.get('source_identity') or {}
        fam_wave[iid] = (si.get('family') or '~UNKNOWN', si.get('wave') or '~UNKNOWN',
                         si.get('source_variable_code_exact'))
        carriers = {b.get('carrier') for b in (rec.get('bindings') or []) if b.get('carrier')}
        carrier_universe |= carriers
        per_impl_carriers[iid] = carriers
    carrier_universe = sorted(carrier_universe)

    # anti-join (c): non-P2 and excluded rows retained (the complement that must not be dropped)
    nonp2_by_carrier = {}
    nonp2_class = collections.Counter()
    nonp2_wave_hold = collections.Counter()
    total_nonp2 = 0
    with open(CW, 'rb') as f:
        for carrier, rows in ijson.kvitems(f, 'nonp2_and_excluded_rows'):
            nonp2_by_carrier[carrier] = len(rows)
            total_nonp2 += len(rows)
            for r in rows:
                nonp2_class[r.get('classification') or 'UNKNOWN'] += 1
                if r.get('excluded_wave'):
                    nonp2_wave_hold[(carrier)] += 1

    # anti-join (a): per implementation, absent carriers
    absent_counts = collections.Counter()
    absent_by_wave = collections.defaultdict(collections.Counter)
    for iid, carriers in per_impl_carriers.items():
        absent = set(carrier_universe) - carriers
        for c in absent:
            absent_counts[c] += 1
        f, w, _ = fam_wave[iid]
        for c in absent:
            absent_by_wave[(f, w)][c] += 1
    # per-impl "is any carrier present but the majority absent" coverage tiers
    coverage = collections.Counter()
    for iid, carriers in per_impl_carriers.items():
        coverage[len(carriers)] += 1

    # anti-join (b): per carrier, its asserted implementation count vs total
    per_carrier_asserted = collections.Counter()
    for carriers in per_impl_carriers.values():
        for c in carriers:
            per_carrier_asserted[c] += 1
    total_impl = len(per_impl_carriers)
    carrier_coverage = []
    for c in carrier_universe:
        asserted = per_carrier_asserted[c]
        carrier_coverage.append({
            'carrier': c,
            'implementations_asserted': asserted,
            'implementations_total': total_impl,
            'coverage_pct': round(100.0 * asserted / total_impl, 3),
            'is_subset_of_all': asserted <= total_impl,
            'alone_inner_join_safe': asserted == total_impl,
        })

    report = {
        'schema': 'HQ280_PV3_A01_INSTRUMENT_PHYSICAL_IMPLEMENTATION_ANTIJOINS@1.0.0',
        'method': {
            'grain': 'question_implementation_id x family x wave x source_variable_code_exact',
            'antijoin_direction_a': 'implementation -> carriers that do NOT bind it',
            'antijoin_direction_b': 'carrier -> implementations it asserts vs full population',
            'semantic_adoption': 'NONE — documentary carrier-coverage only',
            'note': 'A carrier that asserts <100% is inner-join omission bait: '
                    'an inner join to that carrier silently drops implementations.',
        },
        'carrier_universe_size': len(carrier_universe),
        'total_implementations': total_impl,
        'antijoin_a_absent_carrier_counts': dict(sorted(absent_counts.items())),
        'antijoin_c_nonp2_and_excluded_rows_retained': {
            'total_rows': total_nonp2,
            'classification_counts': dict(sorted(nonp2_class.items())),
            'rows_per_carrier': dict(sorted((k, v) for k, v in nonp2_by_carrier.items() if v)),
            'excluded_wave_rows_per_carrier': dict(sorted((k, v) for k, v in nonp2_wave_hold.items() if v)),
            'note': 'These rows are the retained complement (admin/identity-conflict/wave-hold '
                    'rows) that must NOT be silently dropped; they carry no P2 implementation id '
                    'and are typed, not zero-filled.',
        },
        'carrier_coverage': carrier_coverage,
        'implementations_by_carrier_binding_count': dict(sorted(coverage.items())),
        'full_coverage_carriers': [c['carrier'] for c in carrier_coverage if c['coverage_pct'] == 100.0],
        'partial_or_zero_coverage_carriers': [
            c['carrier'] for c in carrier_coverage if c['coverage_pct'] < 100.0
        ],
        'per_wave_absent_carrier_counts': [
            {'family': f, 'wave': w, 'absent': dict(sorted(absent_by_wave[(f, w)].items()))}
            for (f, w) in sorted(absent_by_wave, key=lambda k: (k[0], k[1]))
        ],
    }
    json.dump(report, open(OUT + '/02_INSTRUMENT_PHYSICAL_IMPLEMENTATION_ANTIJOINS.json', 'w'), indent=1)
    print('carrier universe:', len(carrier_universe))
    print('non-P2/excluded rows retained:', total_nonp2, dict(sorted(nonp2_class.items())))
    print('full-coverage carriers:', len(report['full_coverage_carriers']))
    print('partial/zero carriers:', len(report['partial_or_zero_coverage_carriers']))
    print('coverage tiers (n_carriers_bound -> count):', dict(sorted(coverage.items())))
    for c in carrier_coverage:
        print(f"  {c['coverage_pct']:7.3f}%  {c['implementations_asserted']:6d}  {c['carrier']}")

if __name__ == '__main__':
    main()