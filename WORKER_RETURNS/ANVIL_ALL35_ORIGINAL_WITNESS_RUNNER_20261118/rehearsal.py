#!/usr/bin/env python3
"""Tiny sourcefree RED/GREEN rehearsal for the native sink protocol.

This uses the candidate tree's existing sourcefree fixture only.  It is not a
production source option and cannot bypass the SRC04 grant path in witness_caller.
"""
from __future__ import annotations
import json, os, subprocess, sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
CAND=Path(os.environ['ANVIL_CANDIDATE_TREE']).resolve()
sys.path.insert(0,str(CAND))
from rawlsing_next.pre553_source_i02_handoff import build_source_i02_construction_only
from rawlsing_next.pre553_source_saved_body_bridge import SourceSavedBodySink
from rawlsing_next.pre553_source_direct_parquet_estate import VerifiedDirectEstate
from rawlsing_next.pre553_source_i02_streams import ALL_FAMILIES
from rawlsing_next._pre553_external_i02_certificate import ExternalI02Roots
from rawlsing_next.tests.test_pyat960_s1e_support import source_fixture

class LegacyAdapter(SourceSavedBodySink):
    def finish(self, *, roots, manifest, counts):  # exact old defect
        return super().finish(roots=roots, manifest=manifest, counts=counts,
                              transport={})

def red(root: Path):
    fixture=source_fixture(root/'red-src')
    private=root/'red-private';private.mkdir(mode=0o700,parents=True)
    sink=LegacyAdapter(certificate_path=root/'red.sqlite',authorized_private_root=private,chunk_rows=2)
    try:
        build_source_i02_construction_only(config=fixture['config'],source_path=fixture['path'],
            destination=root/'red.sqlite',body_sink=sink,chunk_size=2)
    except Exception as exc:
        (root/'red.json').write_text(json.dumps({'status':'RED','error_type':type(exc).__name__,'error':str(exc)[:500]},indent=2)+'\n')
        print(json.dumps({'status':'RED','error_type':type(exc).__name__}))
        return 0
    raise SystemExit('RED_NOT_TRIGGERED')

def green(root: Path):
    fixture=source_fixture(root/'green-src')
    private=root/'green-private';private.mkdir(mode=0o700,parents=True)
    sink=SourceSavedBodySink(certificate_path=root/'green.sqlite',authorized_private_root=private,chunk_rows=2)
    result=build_source_i02_construction_only(config=fixture['config'],source_path=fixture['path'],
        destination=root/'green.sqlite',body_sink=sink,chunk_size=2)
    receipt=sink.receipt
    payload={'status':'GREEN_PRODUCER','producer_pid':os.getpid(),'path':receipt.path,
             'manifest_sha256':receipt.manifest_sha256,
             'i02':{k:getattr(result.roots,k) for k in ('logical','physical','release','source','replay','universe','schema')},
             'family_counts':dict(receipt.family_counts),'body_transport':dict(result.body_transport),
             'sourcefree_test_only':True,'original_source_opened':False}
    (root/'green_build.json').write_text(json.dumps(payload,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'GREEN_PRODUCER','pid':os.getpid()}))
    return 0

def green_reader(root: Path):
    b=json.loads((root/'green_build.json').read_text())
    alive=subprocess.run(['ps','-p',str(b['producer_pid']),'-o','pid='],capture_output=True,text=True).stdout.strip()
    if alive: raise SystemExit('PRODUCER_STILL_ALIVE')
    held=ExternalI02Roots(**b['i02'])
    estate=VerifiedDirectEstate(root/'green-private',exact_path=b['path'],
        independently_held_manifest_sha256=b['manifest_sha256'],
        independently_held_i02=held,current_authorizer=lambda roots: roots==held)
    counts={f:sum(1 for _ in estate.iter_family(f)) for f in ALL_FAMILIES}
    out={'status':'GREEN_READER','producer_exited_before_reader':True,'family_counts':counts,
         'sourcefree_test_only':True,'original_source_opened':False}
    (root/'green_reader.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'GREEN_READER','counts':counts}))
    return 0

if __name__=='__main__':
    if len(sys.argv)!=3: raise SystemExit('usage: rehearsal.py MODE ROOT')
    mode,root=sys.argv[1],Path(sys.argv[2]);root.mkdir(mode=0o700,parents=True,exist_ok=True)
    {'red':red,'green':green,'green-reader':green_reader}[mode](root)
