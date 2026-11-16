from __future__ import annotations
import json, sys, time
from pathlib import Path
HERE=Path(__file__).resolve().parent; BASE=HERE.parent; REPO=BASE.parents[1]
sys.path[:0]=[str(REPO),str(HERE)]
from rawlsing_next._pre553_external_i02_certificate import ExternalI02Roots
from rawlsing_next.pre553_empirical_objects import exact_ref
from rawlsing_next.pre553_prepared_saved_i03 import PreparedSavedC11Admission
from rawlsing_next.pre553_carrier_execution import RuntimeObjectCatalog
from wide_fixture import build_source, build_queries
receipt=json.loads((BASE/'evidence'/'wide_estate_receipt.json').read_text())
t=time.monotonic(); source,candidate=build_source(); qa,preds,queries=build_queries(source); fixture_seconds=time.monotonic()-t
catalog=RuntimeObjectCatalog(authorities=tuple((*source['authorities'],qa)),predicates=preds,queries=queries,discovery_authorities=())
t=time.monotonic(); admission=PreparedSavedC11Admission.open(root=receipt['root'],exact_path=receipt['exact_path'],independently_held_manifest_sha256=receipt['manifest_sha256'],independently_held_i02=ExternalI02Roots(**receipt['i02']),release_ref=exact_ref(receipt['reconstructed_v1_release_ref']),runtime_catalog=catalog,current_authorizer=lambda _r: True); open_seconds=time.monotonic()-t
t=time.monotonic()
with admission.prepared_i03() as prepared:
    session_seconds=time.monotonic()-t
    q=queries[0]
    pred=next(p for p in preds if exact_ref(q.condition_predicate_ref,'condition')==p.ref)
    t=time.monotonic(); prepared.execute_i03(query_ref=q.ref,predicate_ref=pred.ref); first_query_seconds=time.monotonic()-t
out={'schema':'PYAT_P0_WIDE_OPEN@1','fixture_seconds':fixture_seconds,'cold_admission_seconds':open_seconds,'prepared_session_build_seconds':session_seconds,'first_query_seconds':first_query_seconds,'retained_bytes':receipt['retained_bytes'],'operations':len(queries)}
(BASE/'evidence'/'wide_open.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(json.dumps(out,indent=2,sort_keys=True))
