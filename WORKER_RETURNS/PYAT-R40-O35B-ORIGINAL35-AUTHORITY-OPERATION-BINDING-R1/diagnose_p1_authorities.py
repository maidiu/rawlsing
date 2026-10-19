"""Replay a strict authority-family diagnostic, not M1's actual closure rule.

This inspects already recovered objects and invokes the native registry. It is
not a replacement for full native materialization or a learned-consumer pass.
Correction: M1 closure calls resolve_exact, not require(object_family=...). The
family failures here must not be reported as M1 authority-binding obligations.
"""
import gzip
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parents[1]))
import retained_catalog
from rawlsing_next.pre553_empirical_objects import AuthorityRef
from rawlsing_next.pre553_empirical_authority import Pre553AuthorityError


def diagnose():
    catalog = retained_catalog.build_original_scoped_catalog()
    registry = catalog.authority_registry
    snapshots = [d for d in retained_catalog.retained_documents()
                 if d['schema_id'] == 'AuthoritySnapshot']
    freeze = json.loads((HERE/'evidence/CONTINUATION_P1_FREEZE.json').read_text())
    support = json.loads((HERE/'evidence/continuation_p1_support_preimages.json').read_text())
    failures = []

    def inspect(role, doc, family):
        for raw in doc['authority_snapshot_refs']:
            ref = AuthorityRef(**raw)
            try:
                registry.require(ref, object_family=family)
            except Pre553AuthorityError as exc:
                candidates = []
                for d in snapshots:
                    fields = d['semantic_fields']
                    if all(fields[k] == raw[k] for k in raw):
                        candidates.append({
                            'public_ref': {'kind': 'AuthoritySnapshot@1.0.0',
                                           'object_id': d['object_id'],
                                           'content_hash': d['content_hash']},
                            'families': fields['governed_object_families'],
                        })
                failures.append({'role': role, 'family': family,
                                 'authority_ref': raw, 'failure': str(exc),
                                 'exact_archive_candidates': candidates})

    for role, expected in freeze['facts'].items():
        with gzip.open(HERE/'.runtime/continuation/p1'/(role+'.json.gz'), 'rt') as f:
            doc = json.load(f)
        if doc['content_hash'] != expected['hash']:
            raise ValueError('selected retained public Fact header substituted')
        inspect(role, doc, 'EmpiricalFact@1.0.0')
        del doc
    inspect('receipt', support['receipt'], 'DiscoveryResultReceipt@1.0.0')
    inspect('discovery_authority', support['discovery_authority'], 'DiscoveryAuthority@1.0.0')
    return failures


if __name__ == '__main__':
    result = diagnose()
    target = HERE/'evidence/continuation_p1_missing_authority_diagnostic.json'
    target.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({'native_require_failures': len(result),
                      'scope': 'EXACT_SELECTED_P1_RETAINED_METADATA_ONLY',
                      'new_authorities': 0}))
