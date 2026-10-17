import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent                    # .../PYAT-R27-T9S-.../tests
RET = HERE.parent                                         # .../PYAT-R27-T9S-...
WORKER_RETURNS = RET.parent                               # .../WORKER_RETURNS

# The T9C repaired adapter, pinned by the T9R reviewer at its phase_b subtree.
PINCAND = (WORKER_RETURNS / "PYAT-R26-T9R-INDEPENDENT-TEMPORAL-DELTA-R1"
           / "phase_b" / "pinned_candidate")

for p in (str(RET / "repro"), str(PINCAND)):
    if os.path.isdir(p) and p not in sys.path:
        sys.path.insert(0, p)

if not (PINCAND / "t9b_temporal.py").is_file():
    raise RuntimeError("pinned T9C adapter not found under T9R phase_b/pinned_candidate")
