"""Path setup for the HQ300 C0 repair court."""
import sys
from pathlib import Path

RET = Path(__file__).resolve().parent
for p in (str(RET), str(RET / "staging" / "ns"), str(RET / "staging" / "ns" / "rawlsing_next" / "tests"),
          str(RET.parents[1]), str(RET.parents[1] / "rawlsing_next" / "tests")):
    if p not in sys.path:
        sys.path.insert(0, p)
