from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
for path in (
    ROOT,
    ROOT / "candidate",
    ROOT / "candidate" / "vendor" / "bp2",
    ROOT / "candidate" / "vendor" / "bp4",
    ROOT / "r26e",
    ROOT / "n1",
):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))
