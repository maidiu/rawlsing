"""Load the explicit projection/CLI adapter contract."""
from __future__ import annotations

import json
from pathlib import Path

CONTRACT_SCHEMA = "SOROK_S45_WP19_PROJECTION_CONTRACT@1"
CONTRACT_PATH = Path(__file__).resolve().parents[1] / "ADAPTER_CONTRACT.json"


def load_contract() -> dict:
    return json.loads(CONTRACT_PATH.read_text(encoding="utf8"))


__all__ = ["CONTRACT_PATH", "CONTRACT_SCHEMA", "load_contract"]
