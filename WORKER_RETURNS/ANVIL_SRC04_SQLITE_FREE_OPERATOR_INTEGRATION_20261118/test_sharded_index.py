#!/usr/bin/env python3
"""Focused capacity/exactness test for the actual sharded index path."""
from __future__ import annotations
import hashlib, json, os, shutil, sys, tempfile, time
from pathlib import Path
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE))
from streaming_estate import ShardedRefIndex,StreamRefusal
N=2626832
root=Path(tempfile.mkdtemp(prefix='anvil-shard-test-',dir=os.environ.get('TMPDIR','/tmp')))
t=time.perf_counter();idx=ShardedRefIndex(root)
try:
 for i in range(N):
  idx.add(f'urn:test:ref:{i:08d}:{hashlib.sha256(str(i).encode()).hexdigest()}')
 capacity=time.perf_counter()-t
 first=f'urn:test:ref:{N-1:08d}:{hashlib.sha256(str(N-1).encode()).hexdigest()}'
 try:
  idx.add(first);duplicate='NOT_REFUSED'
 except StreamRefusal as exc:duplicate=str(exc)
 finally:idx.close()
 out={'schema':'ANVIL_SHARDED_INDEX_TEST@1','entries':N,'shards':128,'max_open':16,'capacity_seconds':capacity,'duplicate':duplicate,'refused':duplicate=='DUPLICATE_EXACT_REF','index_bytes':sum(p.stat().st_size for p in root.rglob('*') if p.is_file()),'file_count':sum(1 for p in root.rglob('*') if p.is_file())}
 (HERE/'SHARDED_INDEX_RECEIPT.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out))
finally:
 shutil.rmtree(root,ignore_errors=True)
