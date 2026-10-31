"""Canonical JSON identity and sealed-record validation shared by the C9P candidate.

Identity contract: a sealed record carries `hash` equal to the SHA-256 of its own
canonical JSON excluding the `hash` key. Canonical form sorts keys and uses
compact separators so any Python dict ordering yields one digest.
"""
from __future__ import annotations

import hashlib
import json
from typing import Any


class IntegrityError(ValueError):
    """A sealed record's hash did not match its recomputed digest."""


def canonical(value: Any) -> str:
    """Return the canonical JSON text for `value` with sorted keys and no spaces."""
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def digest(value: Any) -> str:
    """Return the SHA-256 hex digest of the canonical JSON text of `value`."""
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def seal(value: dict) -> dict:
    """Return a copy of `value` with a `hash` key bound to its own digest."""
    return dict(value, hash=digest(value))


def valid(value: dict) -> bool:
    """Return True when `value` carries a `hash` matching its recomputed digest."""
    if not isinstance(value, dict) or "hash" not in value:
        return False
    body = {k: v for k, v in value.items() if k != "hash"}
    return value["hash"] == digest(body)


def require_valid(value: dict, code: str) -> dict:
    """Raise `IntegrityError(code)` unless `value` is a valid sealed record."""
    if not valid(value):
        raise IntegrityError(code)
    return value
