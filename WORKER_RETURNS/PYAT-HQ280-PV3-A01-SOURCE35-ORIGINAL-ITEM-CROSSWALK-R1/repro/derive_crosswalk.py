#!/usr/bin/env python3
"""HQ280 PV3 A01 — deterministic streaming derivation of the All-35 original-item crosswalk.

Streams the LR-A 423MB crosswalk (memory-bounded via ijson), never loads it whole,
never touches respondent microdata, and derives:

  * per-implementation crosswalk records (admin/context/derived typed separately);
  * anti-joins across carriers (unmatched / casefold-only / conflict-bearing);
  * alias-collision and duplicate-namespace detection;
  * small per-wave counts + bounded gap samples for Git.

Large per-implementation dataset is written externally and hash-pinned, never committed.
Deterministic: stable sort keys, no wall-clock in derived content, no set iteration order.
"""
import ijson, json, hashlib, collections, os, sys, csv

CW = '/tmp/rawlsing_hq280_LR_A/02_ORIGINAL_ITEM_IDENTITY_CARRIER_CROSSWALK.json'
OUT = '/tmp/rawlsing_hq280_PV3A01'
LARGE = OUT + '/external'

NON_MEASURE_HINT = ('administrative', 'weight', 'geometry', 'id_number', 'identifier',
                    'derived', 'flag_', 'technical', 'sampling', 'cluster', 'psu')

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()

def classify_measure_role(var, p2_disposition, grain):
    """Typed role class; UNKNOWN is a legitimate retained value, never zero-filled."""
    d = (p2_disposition or '').lower()
    if 'administrative' in d:
        return 'ADMINISTRATIVE_NONMEASURE'
    if 'weight' in d or (var and 'wt' == var.lower()[-2:] and 'weight' in var.lower()):
        return 'WEIGHT_DESIGN_NONMEASURE'
    if 'derived' in d or 'index' in d:
        return 'DERIVED_NONMEASURE_OR_CONTEXT'
    if 'context' in d:
        return 'CONTEXT_NONMEASURE'
    if any(h in (var or '').lower() for h in NON_MEASURE_HINT):
        return 'NONMEASURE_OR_ADMIN_HINT'
    return 'MEASUREMENT_CANDIDATE'

def main():
    os.makedirs(LARGE, exist_ok=True)
    per_impl = []
    carrier_counts = collections.Counter()
    role_counts = collections.Counter()
    per_wave = collections.defaultdict(collections.Counter)
    per_wave_samples = collections.defaultdict(lambda: collections.defaultdict(list))
    join_basis = collections.Counter()
    conflict_impl = 0
    casefold_only_impl = 0
    no_binding_impl = 0
    varcase_collisions = collections.defaultdict(set)
    identity_sha_seen = collections.Counter()
    impl_id_seen = collections.Counter()
    adoption = collections.Counter()
    grain_counts = collections.Counter()
    n = 0

    for rec in ijson.items(open(CW, 'rb'), 'implementations.item'):
        n += 1
        iid = rec.get('question_implementation_id')
        si = rec.get('source_identity') or {}
        family, wave = si.get('family'), si.get('wave')
        var_exact = si.get('source_variable_code_exact')
        grain = rec.get('grain')
        p2d = rec.get('p2_disposition')
        grain_counts[grain or 'UNKNOWN'] += 1
        adoption[rec.get('current_adoption_and_operation_permission') or 'UNKNOWN'] += 1
        role = classify_measure_role(var_exact, p2d, grain)
        role_counts[role] += 1
        bindings = rec.get('bindings') or []
        if not bindings:
            no_binding_impl += 1
        carriers = sorted({b.get('carrier') for b in bindings if b.get('carrier')})
        for c in carriers:
            carrier_counts[c] += 1
        for b in bindings:
            join_basis[b.get('join_basis') or 'UNKNOWN'] += 1
        conflicts = rec.get('alternative_conflicts') or []
        casefold = rec.get('casefold_search_candidates') or []
        if conflicts:
            conflict_impl += 1
        if casefold and not bindings:
            casefold_only_impl += 1
        varcase_collisions[(family or '~UNKNOWN', wave or '~UNKNOWN', (var_exact or '').lower())].add(var_exact or '')
        identity_sha_seen[rec.get('exact_identity_sha256') or ''] += 1
        impl_id_seen[iid or ''] += 1

        # typed binding summary (identity fields only; no semantic adoption)
        bvars, bqids, btexts, bauths = set(), set(), set(), set()
        for b in bindings:
            a = b.get('assertions') or {}
            if a.get('var_name') or a.get('var_code') or a.get('source_variable_code'):
                bvars.add(a.get('var_name') or a.get('var_code') or a.get('source_variable_code'))
            if a.get('question_id'):
                bqids.add(a['question_id'])
            if a.get('exact_question_text') or a.get('question_text'):
                btexts.add((a.get('exact_question_text') or a.get('question_text'))[:200])
            if a.get('source_authority'):
                bauths.add(str(a.get('source_authority'))[:120])
        row = {
            'question_implementation_id': iid,
            'exact_identity_sha256': rec.get('exact_identity_sha256'),
            'family': family, 'wave': wave,
            'source_variable_code_exact': var_exact,
            'grain': grain,
            'p2_disposition': p2d,
            'measure_role_class': role,
            'carrier_count': len(carriers),
            'carriers': carriers,
            'binding_count': len(bindings),
            'binding_var_names': sorted(x for x in bvars if x),
            'binding_question_ids': sorted(x for x in bqids if x),
            'binding_question_text_count': len(btexts),
            'binding_source_authorities': sorted(x for x in bauths if x),
            'alternative_conflict_count': len(conflicts),
            'casefold_candidate_count': len(casefold),
            'has_any_binding': bool(bindings),
            'current_adoption': rec.get('current_adoption_and_operation_permission'),
            'identity_caveat': (rec.get('identity_caveat') or '')[:200],
        }
        per_impl.append(row)
        pw = per_wave[(family, wave)]
        pw['implementations'] += 1
        pw['role_' + role] += 1
        pw['with_bindings'] += 1 if bindings else 0
        pw['with_conflicts'] += len(conflicts)
        # bounded samples for Git
        for label, cond in (('no_binding', not bindings),
                            ('conflict', conflicts),
                            ('casefold_only', casefold and not bindings)):
            if cond and len(per_wave_samples[(family, wave)][label]) < 5:
                per_wave_samples[(family, wave)][label].append({
                    'question_implementation_id': iid,
                    'source_variable_code_exact': var_exact,
                    'measure_role_class': role})

    # duplicate namespace detection (same family+wave+casefolded var across impls)
    dup_ns = {k: sorted(v) for k, v in varcase_collisions.items() if len(v) > 1}
    dup_identity = {k: c for k, c in identity_sha_seen.items() if c > 1 and k}
    dup_impl_id = {k: c for k, c in impl_id_seen.items() if c > 1 and k}

    # deterministic order
    per_impl.sort(key=lambda r: (r['family'] or '', r['wave'] or '',
                                 r['source_variable_code_exact'] or '',
                                 r['question_implementation_id'] or ''))
    large_path = LARGE + '/crosswalk_per_implementation.jsonl'
    with open(large_path, 'w') as f:
        for r in per_impl:
            f.write(json.dumps(r, sort_keys=True, separators=(',', ':')) + '\n')

    # ---- small per-wave counts (Git) ----
    wave_rows = []
    for (family, wave) in sorted(per_wave, key=lambda k: (k[0] or '', k[1] or '')):
        c = per_wave[(family, wave)]
        samples = per_wave_samples[(family, wave)]
        wave_rows.append({
            'family': family, 'wave': wave,
            'implementations': c['implementations'],
            'with_bindings': c['with_bindings'],
            'role_counts': {k.replace('role_', ''): v for k, v in sorted(c.items()) if k.startswith('role_')},
            'alternative_conflicts_total': c['with_conflicts'],
            'gap_samples': {k: samples[k] for k in sorted(samples)},
        })

    summary = {
        'schema': 'HQ280_PV3_A01_ALL35_SOURCE_AND_ORIGINAL_ITEM_SUMMARY@1.0.0',
        'input': {
            'crosswalk_path': CW,
            'crosswalk_sha256': sha256_file(CW),
            'crosswalk_bytes': os.path.getsize(CW),
            'crosswalk_schema': 'RAWLSING_HQ280_LR_A_CROSSWALK@1.0.0',
            'lr_a_archive_sha256': 'e201e7923e1d34520dec7134a51e338b5204d55e39c3caa6a51b65888663600b',
        },
        'implementations_streamed': n,
        'distinct_implementation_ids': len([k for k in impl_id_seen if k]),
        'duplicate_implementation_ids': dup_impl_id,
        'duplicate_exact_identity_sha256': dup_identity,
        'wave_count': len(wave_rows),
        'family_count': len({w['family'] for w in wave_rows}),
        'grain_counts': dict(grain_counts),
        'measure_role_counts': dict(sorted(role_counts.items())),
        'carrier_binding_counts': dict(carrier_counts),
        'join_basis_counts': dict(join_basis),
        'implementations_with_no_binding': no_binding_impl,
        'implementations_with_alternative_conflicts': conflict_impl,
        'implementations_casefold_only_no_binding': casefold_only_impl,
        'duplicate_case_namespace_keys': len(dup_ns),
        'current_adoption_counts': dict(adoption),
        'duplicate_namespace_examples': [
            {'family': k[0], 'wave': k[1], 'var_code_lower': k[2], 'observed_exact_variants': v}
            for k, v in sorted(dup_ns.items())[:20]
        ],
        'per_wave': wave_rows,
        'large_dataset': {
            'path': large_path,
            'sha256': sha256_file(large_path),
            'bytes': os.path.getsize(large_path),
            'records': len(per_impl),
            'note': 'external data-only; hash-pinned, not committed to Git',
        },
    }
    json.dump(summary, open(OUT + '/01_ALL35_SOURCE_AND_ORIGINAL_ITEM_SUMMARY.json', 'w'), indent=1)
    print('implementations:', n, '| waves:', len(wave_rows), '| families:', summary['family_count'])
    print('no-binding:', no_binding_impl, '| conflicts:', conflict_impl, '| casefold-only:', casefold_only_impl)
    print('duplicate impl ids:', len(dup_impl_id), '| duplicate identity sha:', len(dup_identity),
          '| duplicate case namespaces:', len(dup_ns))
    print('roles:', dict(sorted(role_counts.items())))
    print('large dataset sha256:', summary['large_dataset']['sha256'])

if __name__ == '__main__':
    main()