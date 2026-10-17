import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent                    # .../PYAT-R27-T9S-.../tests
RET = HERE.parent                                         # .../PYAT-R27-T9S-...
WORKER_RETURNS = RET.parent                               # .../WORKER_RETURNS

# Phase B candidate (T9D repaired adapter), pinned under this return's phase_b/.
# Phase A candidate (T9C) remains available for reproduction via T9S_CANDIDATE_ROOT.
PINCAND = os.environ.get("T9S_CANDIDATE_ROOT")
if PINCAND:
    PINCAND = Path(PINCAND)
else:
    PINCAND = RET / "phase_b" / "pinned_candidate"
    if not (PINCAND / "t9b_temporal.py").is_file():
        # fall back to the Phase A pinned T9C adapter under the T9R return
        PINCAND = (WORKER_RETURNS / "PYAT-R26-T9R-INDEPENDENT-TEMPORAL-DELTA-R1"
                   / "phase_b" / "pinned_candidate")

for p in (str(RET / "repro"), str(PINCAND)):
    if os.path.isdir(p) and p not in sys.path:
        sys.path.insert(0, p)

if not (PINCAND / "t9b_temporal.py").is_file():
    raise RuntimeError("pinned temporal adapter not found: " + str(PINCAND))
