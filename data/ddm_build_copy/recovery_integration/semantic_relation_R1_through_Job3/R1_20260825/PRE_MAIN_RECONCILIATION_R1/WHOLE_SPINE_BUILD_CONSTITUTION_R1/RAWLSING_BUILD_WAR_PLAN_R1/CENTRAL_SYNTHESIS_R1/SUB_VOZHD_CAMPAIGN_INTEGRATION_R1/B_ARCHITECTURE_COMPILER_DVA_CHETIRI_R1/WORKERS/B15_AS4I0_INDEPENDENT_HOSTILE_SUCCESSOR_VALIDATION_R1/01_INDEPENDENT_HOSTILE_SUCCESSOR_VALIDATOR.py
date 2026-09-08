#!/usr/bin/env python3
"""B15 committed bootstrap for byte-exact independent hostile validator source."""
import base64,gzip,hashlib
from pathlib import Path
EXPECTED_SOURCE_SHA256="c73728f7d75eea85a95eb6ab9848b73d5d9e933c9fd519685fd38ac2e0811f61"
here=Path(__file__).resolve().parent
encoded="".join(p.read_text(encoding="ascii") for p in sorted((here/"HARNESS_SOURCE_CHUNKS").glob("part_*.b64")))
source=gzip.decompress(base64.b64decode(encoded,validate=True))
observed=hashlib.sha256(source).hexdigest()
if observed != EXPECTED_SOURCE_SHA256:
    raise RuntimeError(f"B15_HARNESS_SOURCE_SHA256_MISMATCH__{observed}")
exec(compile(source,str(Path(__file__)),"exec"),globals(),globals())
