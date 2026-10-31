from __future__ import annotations

import sys
from pathlib import Path

CANDIDATE_DIR = Path(__file__).resolve().parents[1]
REPO_ROOT = Path(__file__).resolve().parents[4]

for path in (str(CANDIDATE_DIR), str(REPO_ROOT)):
    if path not in sys.path:
        sys.path.insert(0, path)
