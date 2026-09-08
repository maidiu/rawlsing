#!/usr/bin/env python3
"""B13 committed bootstrap for byte-exact audited driver source."""
import base64,gzip,hashlib
from pathlib import Path
EXPECTED_SOURCE_SHA256="615bf0991b696b5811b3b69920b83fdacf27764c2c9a90ae158605b34c1f6a8c"
here=Path(__file__).resolve().parent
encoded="".join(p.read_text(encoding="ascii") for p in sorted((here/"DRIVER_SOURCE_CHUNKS").glob("part_*.b64")))
source=gzip.decompress(base64.b64decode(encoded))
observed=hashlib.sha256(source).hexdigest()
if observed != EXPECTED_SOURCE_SHA256:
    raise RuntimeError(f"B13_DRIVER_SOURCE_SHA256_MISMATCH__{observed}")
exec(compile(source,str(Path(__file__)),"exec"),globals(),globals())
