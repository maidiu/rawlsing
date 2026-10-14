"""Persist actual source-free universe variant evidence from the new test fixture."""
import importlib.util, json, sys
from pathlib import Path
from tempfile import TemporaryDirectory
from rawlsing_next import pre553_v2_durable_consumer_integration_candidate as P
repo = Path(sys.argv[1]); output = Path(sys.argv[2])
spec = importlib.util.spec_from_file_location('a04b_actual_scopes', repo/'rawlsing_next/tests/test_hq294_a04b_actual_scope_variants.py')
module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
reports = []
with TemporaryDirectory(prefix='a04b-actual-scopes-') as root:
    for ns in ('A04B-ACTUAL-NAMESPACE-A','A04B-ACTUAL-NAMESPACE-B'):
        kwargs, calls, universe = module.actual_scope_fixture(Path(root)/ns, ns)
        report = P.run_integrated(**kwargs)
        assert report['ok'] and len(calls)==2
        reports.append(dict(namespace=ns, universe_ref=universe.ref.as_dict(),
            manifest=kwargs['session'].manifest.semantic_projection(),
            expected=json.loads(kwargs['expected'].payload_json), report=report))
a,b=reports
assert a['universe_ref']!=b['universe_ref'] and a['manifest']!=b['manifest']
assert a['report']['consumer_products']!=b['report']['consumer_products']
assert {p['expected_work_key'] for p in a['report']['consumer_products']}=={p['expected_work_key'] for p in b['report']['consumer_products']}
(output/'actual_namespace_receipts.json').write_text(json.dumps(reports,indent=2)+'\n')
print(json.dumps({'actual_universes_distinct':True,'batch_manifests_distinct':True,
 'consumer_products_distinct':True,'v2_expected_keys_alias':True,'namespace_variants':2,
 'actual_consumer_products_per_variant':2,'claim_grade':'SOURCEFREE_KEY_ALIAS_GAP'}))
