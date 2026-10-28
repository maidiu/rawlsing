from __future__ import annotations
import os
import sys
from pathlib import Path

ROOT = Path(os.environ.get(
    "F0R3_SOURCE_ROOT",
    "/Users/matthewsmith/Desktop/Rawlsing_Worktrees/f0r3",
)).resolve()
S48 = ROOT / "WORKER_RETURNS/SOROK-20261025-S48-ONE-CALL-CONTINUING-TURN-R1"
S52 = ROOT / "WORKER_RETURNS/SOROK-20261025-S52-PAID-ACTIVITY-REPERTOIRE-R1"
for p in (str(S48), str(S52)):
    if p not in sys.path:
        sys.path.insert(0, p)
