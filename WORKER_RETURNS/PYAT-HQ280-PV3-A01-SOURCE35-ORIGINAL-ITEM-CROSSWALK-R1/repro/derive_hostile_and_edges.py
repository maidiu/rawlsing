#!/usr/bin/env python3
"""HQ280 PV3 A01 — exact source-competence edges + hostile A01 test battery.

The three A01 hostile cases (from TASKS.json A01.hostile_cases) are executed against
the real crosswalk, not asserted:
  T1 inner-join B omission (carrier <100% coverage silently drops items)
  T2 battery-parent/child confusion (parent/child drivers vs measurement)
  T3 alias collision (casefold / question_id / driver_id collisions across carriers)
Each test yields a deterministic PASS/OBSERVED verdict + concrete examples.
"""
import ijson, json, hashlib, collections, os

CW = '/tmp/rawlsing_hq280_LR_A/02_ORIGINAL_ITEM_IDENTITY_CARRIER_CROSSWALK.json'
OUT = '/tmp/rawlsing_hq280_PV3A01'

def main():
    impls = list(ijson.items(open(CW, 'rb'), 'implementations.item'))
    total = len(impls)

    # ---- T1: inner-join omission ----
    carrier_cov = collections.Counter()
    per_impl_carriers = {}
    per_impl_var = collections.defaultdict(set)   # (fam,wave,var) -> carriers
    per_impl_qid = collections.defaultdict(set)  # question_id -> iids
    parent_child = []
    for rec in impls:
        iid = rec.get('question_implementation_id')
        si = rec.get('source_identity') or {}
        fam, wave, var = si.get('family'), si.get('wave'), si.get('source_variable_code_exact')
        carriers = {b.get('carrier') for b in (rec.get('bindings') or []) if b.get('carrier')}
        for c in carriers:
            carrier_cov[c] += 1
        per_impl_carriers[iid] = carriers
        per_impl_var[(fam, wave, (var or '').lower())].add(var)
        # battery parent/child: look at driver ids & any 'battery'/'parent' markers
        for b in (rec.get('bindings') or []):
            a = b.get('assertions') or {}
            fd = str(a.get('final_driver_id') or '')
            bl = str(a.get('final_driver_label') or '')
            if 'parent' in fd.lower() or 'child' in fd.lower() or 'battery' in fd.lower() \
               or 'battery' in bl.lower() or fd.lower().endswith('::parent') or '_parent' in fd.lower():
                parent_child.append({'iid': iid, 'carrier': b.get('carrier'), 'final_driver_id': fd,
                                     'final_driver_label': bl, 'var': var})
        for b in (rec.get('bindings') or []):
            a = b.get('assertions') or {}
            qid = a.get('question_id')
            if qid:
                per_impl_qid[str(qid)].add(iid)

    partial = {c: n for c, n in carrier_cov.items() if n < total}
    t1_omits_some = len(partial) > 0
    worst = sorted(partial.items(), key=lambda x: (x[1], x[0]))[:5]

    # ---- T2: battery parent/child ----
    t2_count = len({p['iid'] for p in parent_child})
    t2_examples = parent_child[:8]

    # ---- T3: alias collision ----
    var_case_collisions = {k: sorted(v) for k, v in per_impl_var.items() if len(v) > 1}
    qid_multi_impl = {q: sorted(v) for q, v in per_impl_qid.items() if len(v) > 1}
    t3_var_examples = [{'family': k[0], 'wave': k[1], 'variants': v}
                       for k, v in sorted(var_case_collisions.items())[:10]]
    t3_qid_examples = [{'question_id': q, 'implementation_ids': v}
                       for q, v in sorted(qid_multi_impl.items())[:10]]

    hostile = {
        'schema': 'HQ280_PV3_A01_HOSTILE_COUNT_AND_IDENTITY_TESTS@1.0.0',
        'input_crosswalk_sha256': hashlib.sha256(open(CW, 'rb').read()).hexdigest() if os.path.getsize(CW) < 1e9 else None,
        'implementations': total,
        'tests': [
            {
                'test_id': 'T1_inner_join_b_omission',
                'hostile_case': 'Inner-join B omission',
                'method': 'For each of 46 carriers, count implemented coverage; a carrier '
                          'covering <100% is omission bait under an inner join.',
                'verdict': 'OBSERVED_OMISSION_BAIT_PRESENT' if t1_omits_some else 'NONE',
                'full_coverage_carriers': sorted(c for c, n in carrier_cov.items() if n == total),
                'partial_coverage_carrier_count': len(partial),
                'lowest_coverage_examples': [
                    {'carrier': c, 'implementations': n, 'omitted_under_inner_join': total - n}
                    for c, n in worst],
                'safe_consumption': 'union-of-carriers outer join only',
            },
            {
                'test_id': 'T2_battery_parent_child_confusion',
                'hostile_case': 'Battery-parent/child confusion',
                'method': 'Flag bindings whose final_driver_id/label contains parent/child/battery '
                          'to surface battery structure as a distinct identity class from measurement.',
                'verdict': 'BATTERY_OR_PARENT_CHILD_BINDINGS_OBSERVED' if t2_count else 'NONE',
                'implementation_count_with_battery_parent_child': t2_count,
                'examples': t2_examples,
            },
            {
                'test_id': 'T3_alias_collision',
                'hostile_case': 'Alias collision',
                'method': 'Detect (family,wave,casefold var) collisions across exact spellings '
                          'and question_id -> multiple implementation_id mappings.',
                'verdict': 'COLLISIONS_OBSERVED' if (var_case_collisions or qid_multi_impl) else 'NONE',
                'var_case_collision_count': len(var_case_collisions),
                'question_id_multi_impl_count': len(qid_multi_impl),
                'var_case_collision_examples': t3_var_examples,
                'question_id_multi_impl_examples': t3_qid_examples,
            },
        ],
    }
    # fix crosswalk sha (streamed above may be large; compute once via chunk)
    h = hashlib.sha256()
    with open(CW, 'rb') as f:
        for c in iter(lambda: f.read(1 << 20), b''):
            h.update(c)
    hostile['input_crosswalk_sha256'] = h.hexdigest()
    json.dump(hostile, open(OUT + '/05_HOSTILE_COUNT_AND_IDENTITY_TESTS.json', 'w'), indent=1)

    print('T1 omission bait carriers:', len(partial), '| full-coverage:', len(hostile['tests'][0]['full_coverage_carriers']))
    print('T2 battery/parent/child impls:', t2_count)
    print('T3 var-case collisions:', len(var_case_collisions), '| qid->multi-impl:', len(qid_multi_impl))
    if t3_var_examples: print('   var example:', t3_var_examples[0])
    if t3_qid_examples: print('   qid example:', t3_qid_examples[0])
    if t2_examples: print('   battery example:', t2_examples[0])

if __name__ == '__main__':
    main()