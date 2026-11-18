#!/usr/bin/env python3
"""Reload emitted typed inputs and perform one actual SourceSavedBodySink build."""
from __future__ import annotations
import json,pickle,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from rawlsing_next.pre553_source_saved_body_bridge import SourceSavedBodySink
from rawlsing_next.pre553_source_i02_handoff import build_source_i02_handoff
HERE=Path(__file__).resolve().parent
inputs=pickle.loads((HERE/'inputs'/'typed_inputs.pkl').read_bytes())
private=HERE/'estate'/'private';(HERE/'estate').mkdir(mode=0o700,exist_ok=True);private.mkdir(mode=0o700,exist_ok=True)
cert=HERE/'estate'/'direct.sqlite'
sink=SourceSavedBodySink(certificate_path=cert,authorized_private_root=private,chunk_rows=2)
handoff=build_source_i02_handoff(
 config=inputs['config'],source_path=inputs['source_path'],destination=cert,
 census=inputs['census'],inventory=inputs['inventory'],policy=inputs['policy'],
 frontier=inputs['frontier'],body_sink=sink,chunk_size=2,
)
receipt=sink.receipt
proof={'schema':'ANVIL_TESTONLY_Q2_BUILD@1','sourcefree_test_only':True,
 'destination':handoff.destination,'roots':{k:getattr(handoff.roots,k) for k in ('logical','physical','release','source','replay','universe','schema')},
 'manifest_sha256':receipt.manifest_sha256,'path':receipt.path,'i02':{k:getattr(receipt.i02,k) for k in ('logical','physical','release','source','replay','universe','schema')},'family_counts':dict(receipt.family_counts),
 'handoff_counts':dict(handoff.counts),'body_transport':dict(handoff.body_transport),'sink_stats':dict(sink.stats),
 'source_rows':handoff.row_count,'source_sha256':handoff.source_sha256}
(HERE/'proof'/'build.json').write_text(json.dumps(proof,indent=2,sort_keys=True)+'\n')
print(json.dumps({k:proof[k] for k in ('manifest_sha256','source_rows','family_counts')},sort_keys=True))
