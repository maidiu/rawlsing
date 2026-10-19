import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CANDIDATE = ROOT / "candidate"
RUNTIME = CANDIDATE / "stage" / "runtime"
for path in (CANDIDATE, RUNTIME):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))
os.environ["C0P_RUNTIME"] = str(RUNTIME)
