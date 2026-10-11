#!/usr/bin/env python3
"""HQ280 PV3 A01 — exact source-competence edges (source -> carrier competence matrix).

An 'edge' here is a documentary source->carrier competence relation, not an adoption or
operation-use grant. It is emitted only where the crosswalk gives an exact coordinate or
explicit implementation id binding at that carrier. Competence edges are computed per
family/wave so consumers know exactly which carriers are competent for which administered
items without inferring anything beyond the crosswalk's own assertions.
"""
import ijson, json, hashlib, collections, os

CW = '/tmp/rawlsing_hq280_LR_A/02_ORIGINAL_ITEM_IDENTITY_CARRIER_CROSSWALK.json'
OUT = '/tmp/rawlsing_hq280_PV3A01'
COMPETENT_BASES = ('EXPLICIT_IMPLEMENTATION_ID', 'EXACT_COORDINATE_CANDIDATE__VARIABLE_CASE_PRESERVED')

def main():
    edges = collections.Counter()          # (family, wave, carrier) -> count
    join = collections.defaultdict(collections.Counter)
    pop = collections.Counter()            # (family, wave) -> total impls
    for rec in ijson.items(open(CW, 'rb'), 'implementations.item'):
        si = rec.get('source_identity') or {}
        fam, wave = si.get('family') or '~UNKNOWN', si.get('wave') or '~UNKNOWN'
        pop[(fam, wave)] += 1
        for b in (rec.get('bindings') or []):
            c = b.get('carrier'); jb = b.get('join_basis') or 'UNKNOWN'
            join[(fam, wave, c)][jb] += 1
            if jb in COMPETENT_BASES:
                edges[(fam, wave, c)] += 1

    rows = []
    for (fam, wave, carrier) in sorted(edges):
        total = pop[(fam, wave)]
        comp = edges[(fam, wave, carrier)]
        rows.append({
            'family': fam, 'wave': wave, 'carrier': carrier,
            'wave_implementation_population': total,
            'exact_competence_edges': comp,
            'competence_coverage_pct': round(100.0 * comp / total, 3) if total else None,
            'join_basis_breakdown': dict(sorted(join[(fam, wave, carrier)].items())),
        })

    report = {
        'schema': 'HQ280_PV3_A01_EXACT_SOURCE_COMPETENCE_EDGES@1.0.0',
        'competent_join_bases': list(COMPETENT_BASES),
        'semantic_note': 'Edges are documentary exact-coordinate competence only; they grant '
                         'no semantic adoption, no measurement validity, and no operation use.',
        'wave_family_count': len(pop),
        'edge_rows': len(rows),
        'edges': rows,
    }
    json.dump(report, open(OUT + '/04_EXACT_SOURCE_COMPETENCE_EDGES.json', 'w'), indent=1)
    full = sum(1 for r in rows if r['competence_coverage_pct'] == 100.0)
    print('wave/family populations:', len(pop), '| edge rows:', len(rows))
    print('edge rows at 100% wave coverage:', full, '/', len(rows))

if __name__ == '__main__':
    main()