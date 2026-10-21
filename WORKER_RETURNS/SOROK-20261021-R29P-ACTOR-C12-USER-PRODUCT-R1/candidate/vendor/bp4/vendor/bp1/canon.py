"""Canonical sealed records for BP1 sourcefree actor ledgers.

The seal is content identity, not native authority. It makes replay and
source-edge mutations detectable; it does not authenticate a native actor.
"""
from __future__ import annotations

import hashlib
import json
from typing import Any


class IntegrityError(ValueError):
    pass


def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True)


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def seal(value: dict) -> dict:
    return dict(value, hash=digest(value))


def valid(value: dict) -> bool:
    if not isinstance(value, dict) or "hash" not in value:
        return False
    body = {k: v for k, v in value.items() if k != "hash"}
    return value["hash"] == digest(body)
