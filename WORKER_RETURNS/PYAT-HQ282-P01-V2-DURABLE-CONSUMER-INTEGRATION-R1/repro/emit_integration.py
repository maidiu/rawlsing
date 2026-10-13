"""Emit reproducible real source-free consumer/replay evidence."""
from pathlib import Path
from tempfile import TemporaryDirectory
import sys,json
sys.path.insert(0,str(Path(__file__).resolve().parents[3]))
from rawlsing_next.tests.test_pre553_v2_durable_consumer_integration_candidate import _fixture
from rawlsing_next import pre553_v2_durable_consumer_integration_candidate as P
from rawlsing_next.pre553_empirical_objects import ExactRef
output = Path(__file__).resolve().parent
with TemporaryDirectory(prefix='p01-sourcefree-') as directory:
    kwargs,calls = _fixture(Path(directory))
    (output/'expected_before_batch.json').write_text(kwargs['expected'].payload_json+'\n')
    first = P.run_integrated(**kwargs)
    assert first['ok'],first
    prior = {product['expected_work_key']:ExactRef(**product['consumer_ref']) for product in first['consumer_products']}
    replay = P.run_integrated(**kwargs,prior_consumer_refs=prior)
    assert replay['ok'] and replay['run']['executed'] == [] and len(calls)==3
    assert first['consumer_products']==replay['consumer_products']
    (output/'integrated_consumer_receipt.json').write_text(json.dumps(first,indent=2)+'\n')
    (output/'replay_receipt.json').write_text(json.dumps(replay,indent=2)+'\n')
    print(json.dumps({'expected_operations':3,'committed_and_consumed':3,'original_occurrences':18,
        'consumer_replay_identical':True,'durable_executor_calls_total':len(calls),'ok':True}))
