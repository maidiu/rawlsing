"""Replay the exact-ref closure rule used by native M1, without issuing rights.

Full Fact identities are verified by the real integration test. This faster
diagnostic checks authority headers and the unchanged native resolution rule.
"""
import gzip
import json
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE));sys.path.insert(0,str(HERE.parents[1]))
import retained_catalog
from retained_p1_consumer import original_p1_authorities
from rawlsing_next.pre553_empirical_objects import AuthorityRef
from rawlsing_next.pre553_empirical_authority import AuthorityRegistry,Pre553AuthorityError
from rawlsing_next.fiabc_lits_i_i03_operation_authority import historical_projection_authority_snapshot


def audit():
    catalog=retained_catalog.build_original_scoped_catalog()
    authorities=original_p1_authorities(catalog)
    # The archived object must equal the actual accepted native owner preimage.
    if authorities[-1]!=historical_projection_authority_snapshot():
        raise ValueError('archived projection snapshot differs from native historical owner')
    before=catalog.authority_registry;after=AuthorityRegistry(authorities)
    freeze=json.loads((HERE/'evidence/CONTINUATION_P1_FREEZE.json').read_text())
    support=json.loads((HERE/'evidence/continuation_p1_support_preimages.json').read_text())
    rows=[]

    def inspect(role,doc):
        missing=[];resolved=[]
        for raw in doc['authority_snapshot_refs']:
            ref=AuthorityRef(**raw)
            try:before.resolve_exact(ref)
            except Pre553AuthorityError as exc:
                missing.append({'ref':raw,'detail':str(exc)})
            snapshot=after.resolve_exact(ref).snapshot
            resolved.append({'authority_ref':raw,'public_snapshot_ref':snapshot.ref.as_dict()})
        rows.append({'role':role,'before_missing':missing,'after_resolved':resolved})

    for role,expected in freeze['facts'].items():
        with gzip.open(HERE/'.runtime/continuation/p1'/(role+'.json.gz'),'rt') as f:
            doc=json.load(f)
        if doc['content_hash']!=expected['hash']:
            raise ValueError('selected original public Fact header drift')
        inspect(role,doc)
        del doc
    inspect('receipt',support['receipt']);inspect('discovery_authority',support['discovery_authority'])
    return {'schema':'O35B_NATIVE_M1_EXACT_AUTHORITY_RESOLUTION@1',
            'actual_native_rule':'validate_object_authority_closure calls resolve_exact, not require(object_family=...)',
            'scope':'Selected retained P1 authority headers; full original Fact verification is the integration test',
            'before_snapshot_count':len(catalog.authorities),'after_snapshot_count':len(authorities),
            'append_only_snapshot':authorities[-1].ref.as_dict(),
            'matches_native_historical_owner':True,'rows':rows,
            'new_authorities_or_family_expansions':0,'raw_reads':0}


if __name__=='__main__':
    result=audit()
    (HERE/'evidence/p1_exact_authority_resolution.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'before_snapshot_count':result['before_snapshot_count'],
                      'after_snapshot_count':result['after_snapshot_count'],
                      'missing_ref_obligations_before':sum(len(r['before_missing']) for r in result['rows']),
                      'all_exact_refs_resolve_after':True,'matches_native_historical_owner':True}))
