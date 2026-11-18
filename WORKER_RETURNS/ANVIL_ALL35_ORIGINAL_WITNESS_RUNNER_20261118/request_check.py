#!/usr/bin/env python3
"""Metadata-only equality check for the actual scoped SRC04 request."""
from __future__ import annotations
import json, os, sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
CAND=Path(os.environ['ANVIL_CANDIDATE_TREE']).resolve()
sys.path.insert(0,str(CAND));sys.path.insert(0,str(HERE))
from rawlsing_next.pre553_r157_projection_adapter import SourceConfig, source_read_request_from_config
import witness_runner as wr
import witness_caller as wc
D=HERE
pin=json.loads((D/'SRC04_WITNESS_SCOPE.json').read_text())
cfg_doc=json.loads(Path(os.environ['SRC04_CONFIG']).read_text())
scoped_doc=wr._strip_scope(cfg_doc,pin)
scoped=SourceConfig(scoped_doc)
bound,gbound=wc._grant()[1],None
# wc._grant returns gb,bound,resolver,source,trust
_,bound,resolver,source_path,trust=wc._grant()
req=source_read_request_from_config(scoped,host=bound.request.host,purpose=bound.request.purpose,
    consumer_use=bound.request.consumer_use,semantic_use_scope=bound.request.semantic_use_scope)
out={'status':'REQUEST_MATCH' if req==bound.request else 'REQUEST_MISMATCH',
     'request_equal':req==bound.request,
     'q217_slot_present':any(x['slot']['name']=='q217' for x in scoped_doc['response_slots']),
     'response_slots':len(scoped_doc['response_slots']),
     'coordinate_slots':len(scoped_doc['coordinate_slots']),
     'physical_slots':len(scoped_doc['physical_slots']),
     'request':{'source_id':req.source_id,'source_sha256':req.source_sha256,'source_format':req.source_format,'custody_locator_binding':req.custody_locator_binding,'host':req.host,'purpose':req.purpose,'consumer_use':req.consumer_use,'read_operation':req.read_operation,'physical_read_extent':req.physical_read_extent,'semantic_use_scope':list(req.semantic_use_scope),'metadata_freeze_refs':[r.as_dict() for r in req.metadata_freeze_refs]},
     'grant_ref':bound.grant_ref.as_dict(),
     'source_path_from_grant':source_path}
(D/'REQUEST_CHECK.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(json.dumps({k:out[k] for k in ('status','request_equal','q217_slot_present','response_slots','coordinate_slots')}))
