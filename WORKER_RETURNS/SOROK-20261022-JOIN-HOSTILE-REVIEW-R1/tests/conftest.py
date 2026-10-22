import os
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
DEFAULT_CANDIDATE = REPO / "WORKER_RETURNS" / "SOROK-20261022-SAME-PERSON-JOIN-R1"
CANDIDATE_ROOT = Path(
    os.environ.get("SOROK_JOIN_CANDIDATE_ROOT", str(DEFAULT_CANDIDATE))
).resolve()

if not (CANDIDATE_ROOT / "joined" / "session.py").exists():
    raise RuntimeError(f"JOIN-V candidate root not found: {CANDIDATE_ROOT}")

for path in (str(Path(__file__).parent), str(CANDIDATE_ROOT)):
    if path not in sys.path:
        sys.path.insert(0, path)
