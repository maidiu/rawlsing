"""Stable serialization and hashing for adapter records."""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, is_dataclass
from enum import Enum
from typing import Any

from v3.core.year_record import hash_jsonable


def _plain(value: Any) -> Any:
    if isinstance(value, Enum):
        return value.value
    if is_dataclass(value):
        return {k: _plain(v) for k, v in asdict(value).items()}
    if isinstance(value, dict):
        return {str(k): _plain(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_plain(v) for v in value]
    return value


def record_to_dict(value: Any) -> dict[str, Any]:
    """Return a JSON-compatible dict for one adapter record."""
    plain = _plain(value)
    if not isinstance(plain, dict):
        raise TypeError(f"record is not a dataclass or mapping: {type(value)!r}")
    return plain


def canonical_json(value: Any) -> str:
    """Canonical JSON used for every adapter content hash."""
    return json.dumps(_plain(value), sort_keys=True, separators=(",", ":"), default=str)


def digest(value: Any) -> str:
    """Stable SHA-256 hex digest for an adapter record."""
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def source_hash(value: Any) -> str:
    """Hash of an exact source fact; delegates to the historical V3 helper."""
    return hash_jsonable(_plain(value))


def canonical_numeric(value: Any) -> Any:
    """Normalize numeric JSON types so codec int/float coercion cannot change identity."""
    if isinstance(value, bool):
        return value
    if isinstance(value, int):
        return float(value)
    if isinstance(value, float):
        return float(value)
    if isinstance(value, dict):
        return {str(k): canonical_numeric(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [canonical_numeric(v) for v in value]
    return value


def canonical_state_hash(state: Any) -> str:
    """Durable state identity independent of codec coercion and rendered expression."""
    from v3.io.json_codec import state_to_dict

    payload = canonical_numeric(state_to_dict(state))
    payload.pop("rendered_output", None)
    return digest(payload)


def short(value: str, length: int = 12) -> str:
    return value[:length]
