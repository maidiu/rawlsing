import sys
from pathlib import Path

RETURN = Path(__file__).resolve().parents[1]
for path in (str(RETURN), str(RETURN / "vendor" / "j")):
    if path not in sys.path:
        sys.path.insert(0, path)
