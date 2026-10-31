"""Helpers for per-year simulation records.

The server writes one YearRecord per simulated year. Older callers may still
hand around legacy ``(state_dict, derived_dict)`` tuples, so this module
normalizes both shapes into the canonical record form.
"""

from __future__ import annotations

import hashlib
import json
from typing import Any


def hash_jsonable(payload: Any) -> str:
    """Stable SHA-256 hash for JSON-serializable payloads."""
    return hashlib.sha256(json.dumps(payload, sort_keys=True, default=str).encode("utf-8")).hexdigest()


def state_and_derived_from_snapshot(snapshot: Any) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    """Return (state_dict, derived_dict, record_dict) for legacy tuple or YearRecord dict snapshots."""
    if isinstance(snapshot, dict):
        record = snapshot
        state = record.get("state")
        if not isinstance(state, dict):
            state = record.get("state_after")
        if not isinstance(state, dict):
            state = record.get("state_dict")
        if not isinstance(state, dict):
            state = {}
        derived = record.get("derived")
        if not isinstance(derived, dict):
            derived = record.get("derived_after")
        if not isinstance(derived, dict):
            derived = record.get("derived_dict")
        if not isinstance(derived, dict):
            derived = {}
        if not state and "state" not in record and "state_after" not in record and "state_dict" not in record and any(
            key in record for key in ("capacity", "events_this_year", "year", "age", "rendered_output")
        ):
            state = {
                k: v
                for k, v in record.items()
                if k not in {"state", "state_after", "state_dict", "derived", "derived_after", "derived_dict"}
            }
        return state, derived, record

    if isinstance(snapshot, (list, tuple)) and len(snapshot) >= 2:
        state = snapshot[0] if isinstance(snapshot[0], dict) else {}
        derived = snapshot[1] if isinstance(snapshot[1], dict) else {}
        return state, derived, {}

    return {}, {}, {}


def normalize_year_record_snapshot(snapshot: Any) -> dict[str, Any]:
    """Return a YearRecord-like dict with at least ``state`` and ``derived`` keys."""
    state, derived, record = state_and_derived_from_snapshot(snapshot)
    normalized = dict(record) if isinstance(record, dict) else {}
    normalized.setdefault("state", state)
    normalized.setdefault("derived", derived)
    return normalized
