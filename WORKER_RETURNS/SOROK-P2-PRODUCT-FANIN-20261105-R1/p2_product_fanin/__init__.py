"""Unified TEST_ONLY P2 product throughline over the accepted base."""

from .integration import (
    GRADE,
    OPPORTUNITY_SCHEMA,
    P2ProductFanin,
    SCHEMA,
    VERIFY_SCHEMA,
    apply_explicit_interval,
)
from .runtime import load

__all__ = [
    "GRADE",
    "OPPORTUNITY_SCHEMA",
    "P2ProductFanin",
    "SCHEMA",
    "VERIFY_SCHEMA",
    "apply_explicit_interval",
    "load",
]
