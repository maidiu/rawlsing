#!/usr/bin/env python3
"""B16 committed bootstrap for byte-exact production driver source."""
import base64,gzip,hashlib
from pathlib import Path
EXPECTED_SOURCE_SHA256="9e638d246782b73da9d974f05cfc02bdc1748c73c3c6aa4c818940d52f6c1e77"
here=Path(__file__).resolve().parent
encoded="".join(p.read_text(encoding="ascii") for p in sorted((here/"DRIVER_SOURCE_CHUNKS").glob("part_*.b64")))
source=gzip.decompress(base64.b64decode(encoded,validate=True))
observed=hashlib.sha256(source).hexdigest()
if observed != EXPECTED_SOURCE_SHA256:
    raise RuntimeError(f"B16_DRIVER_SOURCE_SHA256_MISMATCH__{observed}")
exec(compile(source,str(Path(__file__)),"exec"),globals(),globals())
