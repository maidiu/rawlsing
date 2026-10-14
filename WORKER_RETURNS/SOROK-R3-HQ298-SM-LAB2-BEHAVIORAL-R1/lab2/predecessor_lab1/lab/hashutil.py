"""Canonical semantic hashing for the lab (float-free, deterministic)."""
from __future__ import annotations

import hashlib
import json
from typing import Any


def canonicalize(value: Any) -> Any:
    if value is None or isinstance(value, (str, bool)):
        return value
    if isinstance(value, int) and not isinstance(value, bool):
        return value
    if isinstance(value, float):
        raise ValueError("float forbidden in lab semantic identity")
    if isinstance(value, dict):
        return {str(k): canonicalize(value[k]) for k in sorted(value, key=str)}
    if isinstance(value, (list, tuple)):
        return [canonicalize(v) for v in value]
    raise ValueError(f"non-canonicalizable value: {type(value).__name__}")


def canonical_json(value: Any) -> str:
    return json.dumps(canonicalize(value), sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def semantic_hash(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def bytes_of(value: Any) -> int:
    return len(canonical_json(value).encode("utf-8"))


def token_estimate(value: Any) -> int:
    """Deterministic retrieval-token estimate: ceil(bytes/4) of canonical material."""

    b = bytes_of(value)
    return (b + 3) // 4
