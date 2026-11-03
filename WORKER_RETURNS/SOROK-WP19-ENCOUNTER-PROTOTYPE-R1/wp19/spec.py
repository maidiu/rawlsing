"""Load the pinned S11 WP-19 consumable interface specification."""
from __future__ import annotations

import json
from pathlib import Path

RETURN = Path(__file__).resolve().parents[1]
REPO = RETURN.parents[1]
S11_RETURN = REPO / "WORKER_RETURNS" / "SOROK-S11-ENCOUNTER-EXIT-SPEC-R1"
S11_SPEC = S11_RETURN / "02_WP19_CONSUMABLE_INTERFACE.json"
S11_COMMIT = "faec7ce909c54664e85320534bdf744b9bc47d37"


def load() -> dict:
    if not S11_SPEC.is_file():
        raise FileNotFoundError(str(S11_SPEC))
    return json.loads(S11_SPEC.read_text(encoding="utf8"))


__all__ = ["REPO", "RETURN", "S11_COMMIT", "S11_SPEC", "load"]
