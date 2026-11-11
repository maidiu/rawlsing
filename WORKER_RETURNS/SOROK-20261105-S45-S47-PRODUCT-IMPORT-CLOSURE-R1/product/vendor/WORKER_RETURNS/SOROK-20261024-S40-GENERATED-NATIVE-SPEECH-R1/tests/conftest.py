from __future__ import annotations

import sys
from pathlib import Path

RET = Path(__file__).resolve().parents[1]
if str(RET) not in sys.path:
    sys.path.insert(0, str(RET))
