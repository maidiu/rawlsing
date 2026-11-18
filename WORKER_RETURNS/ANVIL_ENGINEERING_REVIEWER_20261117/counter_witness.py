"""Review-only actual construction counter for prepared Batch cut1."""
from pathlib import Path
import json, tempfile

from rawlsing_next.pre553_c11_repository import C11Repository
from rawlsing_next.pre553_batch_runner import BatchManifest, BatchUnitSpec
from rawlsing_next.pre553_saved_workload_integration import execute_saved_batch
from rawlsing_next.tests.test_pre553_prepared_saved_i03 import _fixture
import rawlsing_next.pre553_source_backed_c11_facade as source_facade

def main(argv):
    proofroot = Path(argv[1]).resolve()
    tmp = Path(tempfile.mkdtemp(prefix='anvil-counter-', dir=proofroot))
    source, qa, predicate, other, queries, admission = _fixture(
        __import__('pytest').MonkeyPatch(), tmp, 'CUT1-COUNTER')
    manifest = BatchManifest(tuple(
        BatchUnitSpec('QUERY', q.ref, (admission.release_ref,))
        for q in queries.values()
    ))
    pmap = {q.ref.key: predicate.ref for q in queries.values()}
    counts = {'c11_init': 0, 'source_builder': 0}
    orig_c11 = C11Repository.__init__
    orig_builder = source_facade.build_source_backed_c11_repository
    def c11(self, *a, **k):
        counts['c11_init'] += 1
        return orig_c11(self, *a, **k)
    def builder(*a, **k):
        counts['source_builder'] += 1
        return orig_builder(*a, **k)
    C11Repository.__init__ = c11
    source_facade.build_source_backed_c11_repository = builder
    try:
        runner = execute_saved_batch(admission, manifest=manifest, predicate_ref_by_query=pmap)
    finally:
        C11Repository.__init__ = orig_c11
        source_facade.build_source_backed_c11_repository = orig_builder
    out = {'schema':'ANVIL_CUT1_COUNTER_WITNESS@1','receipt_states':[r.state for r in runner.receipts],'c11_init_calls':counts['c11_init'],'source_builder_calls':counts['source_builder'],'fixture':'sourcefree prepared fixture'}
    (proofroot/'counter_witness.json').write_text(json.dumps(out,indent=2,sort_keys=True),encoding='utf-8')
    print(json.dumps(out,indent=2,sort_keys=True))
if __name__ == '__main__':
    raise SystemExit(main(__import__('sys').argv))
