"""Run exact P01 owner in separate processes with preserved synthetic ledger."""
import json, sys
from pathlib import Path
from rawlsing_next.tests.test_pre553_v2_durable_consumer_integration_candidate import _fixture
from rawlsing_next import pre553_v2_durable_consumer_integration_candidate as P
from rawlsing_next.pre553_empirical_objects import ExactRef
root, output, mode = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
kwargs, calls = _fixture(root)
prior = None
if mode == 'replay':
    first = json.loads((output/'first.json').read_text())
    prior = {p['expected_work_key']: ExactRef(**p['consumer_ref']) for p in first['consumer_products']}
report = P.run_integrated(**kwargs, prior_consumer_refs=prior)
assert report['ok']
if mode == 'replay':
    assert report['consumer_products'] == first['consumer_products']
    assert report['run']['executed'] == [] and calls == []
else:
    assert len(calls) == 3
(output/(mode+'.json')).write_text(json.dumps(report, indent=2)+'\n')
(output/('expected_'+mode+'.json')).write_text(kwargs['expected'].payload_json+'\n')
print(json.dumps({'mode':mode,'ok':report['ok'],'executor_calls':len(calls),
                  'consumer_products':len(report['consumer_products']),
                  'source_occurrences':len(report['source_inventory'])}))
