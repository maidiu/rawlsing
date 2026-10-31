import sys
from pathlib import Path

RET = Path(__file__).resolve().parents[1]
REPO = RET.parents[1]
for path in (str(RET), str(REPO)):
    if path not in sys.path:
        sys.path.insert(0, path)
