#!/usr/bin/env python3
"""Reload emitted typed inputs and perform one actual SourceSavedBodySink build."""
from __future__ import annotations
import hashlib,json,os,pickle,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from rawlsing_next.pre553_source_saved_body_bridge import SourceSavedBodySink
from rawlsing_next.pre553_source_i02_handoff import build_source_i02_handoff
HERE=Path(os.environ.get('ANVIL_TESTONLY_ROOT', str(Path(__file__).resolve().parent))).resolve()
manifest_path=HERE/'inputs'/'typed_inputs_manifest.json'
manifest=json.loads(manifest_path.read_text())
if (manifest.get('schema') != 'ANVIL_TESTONLY_Q2_TYPED_INPUTS@1'
        or manifest.get('sourcefree_test_only') is not True
        or manifest.get('original_source_bodies_read') is not False
        or manifest.get('pickle_relpath') != 'inputs/typed_inputs.pkl'):
    raise SystemExit('TESTONLY_MANIFEST_REQUIRED')
pickle_path=HERE/'inputs'/'typed_inputs.pkl'
actual=hashlib.sha256(pickle_path.read_bytes()).hexdigest()
if manifest.get('pickle_sha256') != actual:
    raise SystemExit('TESTONLY_PICKLE_DIGEST_MISMATCH')
inputs=pickle.loads(pickle_path.read_bytes())
source_path=(HERE/Path(inputs['source_path'])).resolve()
if not str(source_path).startswith(str((HERE/'inputs').resolve())+os.sep):
    raise SystemExit('TESTONLY_SOURCE_OUTSIDE_TRUSTED_ROOT')
private=HERE/'estate'/'private';(HERE/'estate').mkdir(mode=0o700,exist_ok=True);private.mkdir(mode=0o700,exist_ok=True)
cert=HERE/'estate'/'direct.sqlite'
sink=SourceSavedBodySink(certificate_path=cert,authorized_private_root=private,chunk_rows=2)
handoff=build_source_i02_handoff(
 config=inputs['config'],source_path=source_path,destination=cert,
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
