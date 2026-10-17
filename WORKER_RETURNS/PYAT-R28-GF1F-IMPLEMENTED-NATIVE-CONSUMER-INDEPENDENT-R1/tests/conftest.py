import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
RET = HERE.parent
RUNTIME = RET / "candidate" / "court" / "runtime_root"
COURT_REPRO = RET / "candidate" / "court" / "repro"

for p in (str(RET / "repro"), str(COURT_REPRO), str(RUNTIME)):
    if os.path.isdir(p) and p not in sys.path:
        sys.path.insert(0, p)

if not (RUNTIME / "gf1_pair_support_consumer.py").is_file():
    raise RuntimeError("staged GF1E consumer not found under candidate/court/runtime_root")
