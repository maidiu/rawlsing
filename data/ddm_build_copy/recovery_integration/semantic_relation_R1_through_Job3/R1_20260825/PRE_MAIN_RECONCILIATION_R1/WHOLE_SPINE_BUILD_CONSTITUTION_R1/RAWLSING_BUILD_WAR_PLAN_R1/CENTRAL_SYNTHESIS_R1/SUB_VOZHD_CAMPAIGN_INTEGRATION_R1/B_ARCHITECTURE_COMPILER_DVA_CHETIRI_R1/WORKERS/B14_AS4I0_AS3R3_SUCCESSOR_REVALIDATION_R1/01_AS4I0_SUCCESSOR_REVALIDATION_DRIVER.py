#!/usr/bin/env python3
"""B14 committed bootstrap for byte-exact audited successor revalidation adapter."""
import base64, gzip, hashlib
from pathlib import Path
EXPECTED_ADAPTER_SOURCE_SHA256="7824984d14df53700e8b8a8a97944a12fb522f5412dbe1a4e8f5ea48dcdea671"
here=Path(__file__).resolve().parent
names=["part_00.b64"]+[f"part_01_{i:02d}.b64" for i in range(7)]+["part_02.b64"]
encoded="".join((here/"DRIVER_SOURCE_CHUNKS"/name).read_text(encoding="ascii") for name in names)
source=gzip.decompress(base64.b64decode(encoded, validate=True))
observed=hashlib.sha256(source).hexdigest()
if observed != EXPECTED_ADAPTER_SOURCE_SHA256:
    raise RuntimeError(f"B14_ADAPTER_SOURCE_SHA256_MISMATCH__{observed}")
exec(compile(source,str(Path(__file__)),"exec"),globals(),globals())
