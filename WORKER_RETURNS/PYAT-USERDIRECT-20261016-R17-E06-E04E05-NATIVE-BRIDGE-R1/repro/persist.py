"""Store raw trace once; the values record binds its exact bytes."""
from bootstrap import ROOT
import json,hashlib
def save_products(out,trace):
 body=(json.dumps(trace,separators=(',',':'))+'\n').encode()
 path='observations/native_imports_and_calls.json'
 (ROOT/path).write_bytes(body)
 out['native_trace']=dict(path=path,sha256=hashlib.sha256(body).hexdigest(),
                         imports=trace['imports'],actual_frames=trace['actual_frames'],
                         same_concrete_C1_evidence_into_F8=trace['same_concrete_C1_evidence_into_F8'])
 (ROOT/'02_ACTUAL_NATIVE_TO_TWO_CONSUMER_PRODUCTS.json').write_text(json.dumps(out,separators=(',',':'))+'\n')
