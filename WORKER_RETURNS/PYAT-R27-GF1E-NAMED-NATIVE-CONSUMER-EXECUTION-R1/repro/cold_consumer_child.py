"""GF1E cold-process consumer reconstruction.

Builds the four differential-pattern relations and computes the pair-support
signature in a fresh OS process, writing the result plus this process pid.

argv: <dest.json>
"""
import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent            # .../PYAT-R27-GF1E-.../repro
RET = HERE.parent
WORKER_RETURNS = RET.parent
GF1_RT = WORKER_RETURNS / "PYAT-USERDIRECT-20261016-R17-GF1-GENERIC-NATIVE-PAIR-RELATION-R1" / "court" / "runtime_root"

sys.path[:0] = [str(RET / "repro"), str(GF1_RT)]

from gf1e_relations import four_relations                       # noqa: E402
from gf1_pair_support_consumer import compute_pair_support_signature  # noqa: E402

dest = os.path.abspath(sys.argv[1])
results = {
    name: compute_pair_support_signature(rel)
    for name, rel in four_relations().items()
}
Path(dest).write_text(json.dumps(dict(pid=os.getpid(), results=results),
                                 sort_keys=True, separators=(",", ":")) + "\n")
print("GF1E COLD pid", os.getpid(), "classes",
      {k: v["separation_class"] for k, v in results.items()})
