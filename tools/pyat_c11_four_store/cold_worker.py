"""Fresh-PROCESS SQLite cold physical probe. NOT original I03 source admission.

A full body audit can be requested separately. S1/S2/S3 deliberately get
an unavailable Parquet path: a successful body read proves physical SQL
independence after source conversion.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import time

from .stores import Store, StoreFailure, canonical

def main(argv=None):
    p=argparse.ArgumentParser()
    p.add_argument("--arm",required=True,choices=("H","S1","S2","S3"))
    p.add_argument("--database",type=Path,required=True)
    p.add_argument("--estate",type=Path,required=True)
    p.add_argument("--source-identity",type=Path,required=True)
    p.add_argument("--target",required=True)
    p.add_argument("--evidence-ref",required=True)
    p.add_argument("--audit",action="store_true")
    a=p.parse_args(argv)
    identity=json.loads(a.source_identity.read_text())
    start=time.perf_counter()
    store=Store(a.arm,a.database,a.estate,create=False,source_identity=identity)
    opened=time.perf_counter()
    try:
        audit_s=None
        if a.audit:
            st=time.perf_counter()
            store.audit_families()
            audit_s=time.perf_counter()-st
        result=store.probe_query(a.target)
        # Recover at least one exact body. This must succeed for S1/S2/S3
        # without accessing original Parquet after initial build.
        body_hash=None
        oid=store.find_id(a.evidence_ref)
        if oid is None:
            raise StoreFailure("fresh-process exact evidence unavailable")
        ref,body=store.fetch_body(oid)
        if ref != a.evidence_ref:
            raise StoreFailure("fresh-process evidence identity mismatch")
        import hashlib
        body_hash=hashlib.sha256((ref+"\x00"+body).encode()).hexdigest()
        print(canonical({
            "grade":"PHYSICAL_REOPEN_NOT_SOURCE_AUTHORIZED_NATIVE_I03",
            "arm":a.arm,
            "fresh_process_open_s":opened-start,
            "full_body_audit_s":audit_s,
            "query":result,
            "one_body_sha256":body_hash,
            "elapsed_s":time.perf_counter()-start,
        }))
    finally:
        store.close()

if __name__=="__main__":
    main()
