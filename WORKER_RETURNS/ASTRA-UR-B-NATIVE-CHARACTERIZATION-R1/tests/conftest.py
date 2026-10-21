from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
for path in (
    ROOT, REPO,
    Path.home() / ".cache/uv/archive-v0/sFE7VO7nHEpr328Z",
    Path.home() / ".cache/uv/archive-v0/quC1M_vhOV9lE6BI",
):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))
