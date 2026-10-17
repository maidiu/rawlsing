"""GF1F cold-process consumer replay (one fresh OS process per invocation).

Rebuilds the whole independent 2x2 universe, runs the GF1E consumer in this new
process, and writes the results plus this process pid and the imported consumer
file.  argv: <dest.json>.
"""
import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
RET = HERE.parent
RUNTIME = RET / "candidate" / "court" / "runtime_root"
sys.path[:0] = [str(RET / "repro"), str(RUNTIME)]

import gf1_pair_support_consumer as C                     # noqa: E402
from independent_relation import build_relation           # noqa: E402

oracle = json.loads((RET / "01_INDEPENDENT_FROZEN_PAIR_ORACLE.json").read_text())
results = {}
class_counts = {}
for row in oracle["universe"]:
    key = "%d%d%d%d" % (row["cells"]["00"], row["cells"]["01"],
                        row["cells"]["10"], row["cells"]["11"])
    out = C.compute_pair_support_signature(build_relation(row["cells"],
                                                          eligible=row["eligible"]))
    results[key] = out["separation_class"]
    class_counts[out["separation_class"]] = class_counts.get(out["separation_class"], 0) + 1

Path(os.path.abspath(sys.argv[1])).write_text(json.dumps(
    dict(pid=os.getpid(), consumer_file=Path(C.__file__).resolve().name,
         class_counts=class_counts, results=results),
    sort_keys=True, separators=(",", ":")) + "\n")
print("GF1F COLD", os.getpid(), class_counts)
