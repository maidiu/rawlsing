"""Reuse exact WG0R transport; compare against separately frozen native fixtures."""
from collections import Counter
from dataclasses import fields,is_dataclass
from collections.abc import Mapping
from pathlib import Path
import hashlib,json,sys
R=Path(__file__).resolve().parent
sys.path.insert(0,str(R/'native'))
from rawlsing_next.tests.test_pre553_route_b_production import _fixture
from rawlsing_next.pre553_empirical_objects import semantic_hash

def material(x):
    if hasattr(x,'as_dict'):return material(x.as_dict())
    if is_dataclass(x):return {f.name:material(getattr(x,f.name)) for f in fields(x)}
    if isinstance(x,Mapping):return {k:material(v) for k,v in x.items()}
    if isinstance(x,(tuple,list)):return [material(v) for v in x]
    if isinstance(x,(set,frozenset)):return sorted((material(v) for v in x),key=repr)
    return x

def snapshot(fx):
    # Named original fixture declarations are independent of catalog enumeration.
    rows=[['QUERY',fx['raw_query'].ref.key,fx['all_p'].ref.key],
          ['QUERY',fx['weighted_query'].ref.key,fx['all_p'].ref.key],
          ['DISCOVERY',fx['discovery_authority'].ref.key,'']]
    return dict(expected_jobs=sorted(rows),projection_sha256=semantic_hash(material(fx['projection'])),
                physical_stream_sha256=semantic_hash(dict(source_sha256=fx['stream'].source_sha256,row_count=fx['stream'].row_count,cells=[material(c) for c in fx['stream'].iter_cells()])),
                catalog_sha256=semantic_hash(material(fx['catalog'])),
                source_sha256=fx['stream'].source_sha256,
                grade='TEST_ONLY_INHERITED_FIXTURE_DECLARATIONS__NOT_ORIGINAL35_E_PRE')

def freeze():
    path=R/'evidence/EXPERIMENT_EXPECTED.json'
    if path.exists():raise ValueError('REFUSE_OVERWRITE_PREFROZEN_EXPECTATIONS')
    expected={k:snapshot(_fixture(**args)) for k,args in [('positive',{}),('missing_weight',{'missing_weight':True}),('valid_empty',{'valid_empty':True})]}
    path.write_text(json.dumps(expected,sort_keys=True,indent=2)+'\n')
    print(hashlib.sha256(path.read_bytes()).hexdigest())

def verify_fixture(fx,expected):
    if snapshot(fx)!=expected:raise ValueError('FIXTURE_PREIMAGE_OR_EXPECTED_SET_CHANGED')

def verify_jobs(expected,requests,discoveries):
    actual=Counter([('QUERY',r.query_ref.key,r.predicate_ref.key) for r in requests]+[('DISCOVERY',d.ref.key,'') for d in discoveries])
    wanted=Counter(tuple(x) for x in expected['expected_jobs'])
    if actual!=wanted:raise ValueError('EXPECTED_EXECUTED_IDENTITY_MULTISET_MISMATCH')
    return dict(expected=sum(wanted.values()),actual=sum(actual.values()),missing=[],unexpected_or_duplicate=[])

def run():
    import reused_wg0r_fixture as inherited
    from rawlsing_next import pre553_route_b_production as rb
    expected=json.loads((R/'evidence/EXPERIMENT_EXPECTED.json').read_text())
    results={}
    for name,args in [('positive',{}),('missing_weight',{'missing_weight':True})]:
        fx=_fixture(**args);verify_fixture(fx,expected[name])
        req=inherited.enumerate_requests(fx['catalog']);ds=fx['catalog'].discovery_authorities
        anti=verify_jobs(expected[name],req,ds)
        receipt=inherited.run(**args)
        # Use native exact-ref parser, not string conventions, for postexecution.
        from rawlsing_next.pre553_empirical_objects import exact_ref
        observed=Counter(('QUERY',exact_ref(r['query_ref'],'query').key,exact_ref(r['predicate_ref'],'predicate').key) for r in receipt['requests'])
        observed+=Counter([('DISCOVERY',d.ref.key,'') for d in ds])
        if observed!=Counter(tuple(x) for x in expected[name]['expected_jobs']):raise ValueError('POSTEXECUTION_ANTI_JOIN')
        receipt['independent_named_fixture_anti_join']=anti
        receipt['claim_grade']='AUTHOR_REPLAY_OF_ACCEPTED_TEST_ONLY_FIXTURE__DISTINCT_REVIEW_REQUIRED'
        results[name]=receipt
    fx=_fixture(valid_empty=True);verify_fixture(fx,expected['valid_empty'])
    requests=inherited.enumerate_requests(fx['catalog']);ds=fx['catalog'].discovery_authorities
    verify_jobs(expected['valid_empty'],requests,ds)
    out=rb.execute_route_b_production(source=fx['stream'],projection=fx['projection'],runtime_catalog=fx['catalog'],i03_requests=requests,discovery_authority_ref=ds[0].ref)
    results['valid_empty']=dict(i05_receipts=[material(x) for x in out.i05_result.receipts],i03_facts=[material(f) for x in out.i03_results for f in x.facts],anti_join=verify_jobs(expected['valid_empty'],requests,ds),grade='TEST_ONLY_TYPED_EMPTY_OR_NEGATIVE_RETAINED')
    (R/'evidence/native_experiment.json').write_text(json.dumps(results,sort_keys=True,indent=2)+'\n')
    print(json.dumps({k:dict(manifest_units=len(v.get('manifest',{}).get('units',[])),anti_join=v.get('independent_named_fixture_anti_join',v.get('anti_join')),consumer_positive=v.get('consumer_positive',{}).get('semantic_fields',{}).get('adjudication_outcome'),consumer_unknown=v.get('consumer_unknown',{}).get('semantic_fields',{}).get('adjudication_outcome')) for k,v in results.items()},sort_keys=True))
if __name__=='__main__':
    if '--freeze' in sys.argv:freeze()
    else:run()
