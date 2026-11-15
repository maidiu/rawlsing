"""Canonical identity helpers shared by the BP4 product."""
from __future__ import annotations

import hashlib
import json
from typing import Any

from bp1.canon import canonical as _bp1_canonical
from bp1.canon import digest as _bp1_digest
from bp1.canon import seal as _bp1_seal
from bp1.canon import valid as _bp1_valid

FORBIDDEN_KEYS = frozenset({
    "future_child", "future_child_personality", "future_child_outcome",
    "future_child_desired_adversity_tag", "future_child_health_outcome",
    "future_child_education_outcome", "any_field_derived_from_future_child",
})


def canonical(value: Any) -> str:
    return _bp1_canonical(value)


def digest(value: Any) -> str:
    return _bp1_digest(value)


def seal(value: dict) -> dict:
    return _bp1_seal(value)


def valid(value: Any) -> bool:
    return _bp1_valid(value)


def forbidden_key(value: Any) -> str | None:
    if isinstance(value, dict):
        for key, item in value.items():
            if isinstance(key, str) and key.lower() in FORBIDDEN_KEYS:
                return key
            found = forbidden_key(item)
            if found:
                return found
    elif isinstance(value, (list, tuple)):
        for item in value:
            found = forbidden_key(item)
            if found:
                return found
    return None


def assert_no_forbidden(value: Any) -> None:
    found = forbidden_key(value)
    if found:
        raise ValueError("FUTURE_OR_FORBIDDEN_SOURCE_FIELD:" + found)
