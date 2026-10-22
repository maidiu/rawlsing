"""R56-R04BYTEV r2 probe: bounded synthetic DTA/SAV read shape and O(rows) ceiling.

Each measurement runs in a fresh child process; maxrss is the process high-water mark.
"""
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path.cwd()
sys.path.insert(0, str(REPO))

import pandas as pd  # noqa: E402
import pyreadstat  # noqa: E402

CHILD = r"""
import json, resource, sys
sys.path.insert(0, '.')
from rawlsing_next.pre553_physical_decoder import decode_sav, decode_dta
path, fmt, sha = sys.argv[1], sys.argv[2], sys.argv[3]
inc = (decode_sav if fmt == 'sav' else decode_dta)(path, expected_source_sha256=sha)
before = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
cells = sum(len(batch) for batch in inc.iter_batches(1000))
after = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
print(json.dumps({"cells": cells, "maxrss_before": before, "maxrss_after": after,
                  "maxrss_delta": after - before, "source_custody": dict(inc.source_custody)}))
inc.close()
"""


def rows(count):
    base = {
        "X": [1, 0, None], "Y": [1, 0, 1], "M": ["AB", "A", ""], "O": ["AB", "BA", "AB"],
        "R": ["XY", "XZ", "XY"], "G": ["A", "B", "A"], "W": [2, 1, 3],
    }
    return {key: [values[i % 3] for i in range(count)] for key, values in base.items()}


def measure(count, fmt):
    tmp = Path(tempfile.mkdtemp(prefix=f"r04bytev-r2-shape-{fmt}-{count}-"))
    path = tmp / f"source.{fmt}"
    frame = pd.DataFrame(rows(count))
    writer = pyreadstat.write_sav if fmt == "sav" else pyreadstat.write_dta
    writer(frame, str(path))
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    result = subprocess.run(
        [sys.executable, "-c", CHILD, str(path), fmt, digest],
        cwd=REPO, capture_output=True, text=True, timeout=300,
    )
    if result.returncode != 0:
        return {"count": count, "format": fmt, "error": result.stderr[-500:]}
    data = json.loads(result.stdout)
    data.update({"count": count, "format": fmt, "file_bytes": path.stat().st_size})
    return data


if __name__ == "__main__":
    out = {}
    for fmt in ("dta", "sav"):
        out[fmt] = [measure(n, fmt) for n in (1000, 10000, 50000)]
    print(json.dumps(out, indent=2, sort_keys=True, default=str))
