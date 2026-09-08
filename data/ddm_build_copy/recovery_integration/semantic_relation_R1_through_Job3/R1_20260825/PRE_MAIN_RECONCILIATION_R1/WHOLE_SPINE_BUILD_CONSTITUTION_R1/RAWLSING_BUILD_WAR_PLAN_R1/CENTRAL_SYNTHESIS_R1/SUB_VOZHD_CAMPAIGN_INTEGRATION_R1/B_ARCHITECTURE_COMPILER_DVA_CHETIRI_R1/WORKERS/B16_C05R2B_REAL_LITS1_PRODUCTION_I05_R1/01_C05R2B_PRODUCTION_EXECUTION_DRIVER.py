#!/usr/bin/env python3
"""B16 committed bootstrap for byte-exact production driver source."""
import base64,gzip,hashlib
from pathlib import Path
EXPECTED_SOURCE_SHA256="59ce6903776df5f5b17bc074b15d9ae06334a5a1c30fad91096fc3fb6a014a3f"
here=Path(__file__).resolve().parent
encoded="".join(p.read_text(encoding="ascii") for p in sorted((here/"DRIVER_SOURCE_CHUNKS").glob("part_*.b64")))
source=gzip.decompress(base64.b64decode(encoded,validate=True))
observed=hashlib.sha256(source).hexdigest()
if observed != EXPECTED_SOURCE_SHA256:
    raise RuntimeError(f"B16_DRIVER_SOURCE_SHA256_MISMATCH__{observed}")
exec(compile(source,str(Path(__file__)),"exec"),globals(),globals())
