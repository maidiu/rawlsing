from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
PATHS = (
    REPO / "WORKER_RETURNS/SOROK-20261025-S48-ONE-CALL-CONTINUING-TURN-R1",
    REPO / "WORKER_RETURNS/SOROK-20261025-S49-INDEPENDENT-ACTOR-PRODUCER-R1",
    REPO / "WORKER_RETURNS/SOROK-20261025-S51-SITUATED-OBJECT-RELEVANCE-R1",
    REPO / "WORKER_RETURNS/SOROK-20261025-S52-PAID-ACTIVITY-REPERTOIRE-R1",
)
for path in reversed(PATHS):
    text = str(path)
    if text not in sys.path:
        sys.path.insert(0, text)
