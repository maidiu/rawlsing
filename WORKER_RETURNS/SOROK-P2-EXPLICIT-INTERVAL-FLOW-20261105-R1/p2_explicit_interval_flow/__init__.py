"""Additive explicit interval continuation over the shipped S45-S47 product."""

from .continuation import (
    INTERVAL_INPUT_SCHEMA,
    RESULT_SCHEMA,
    admit_continuation,
    apply_explicit_interval,
    continue_after_request,
)

__all__ = [
    "INTERVAL_INPUT_SCHEMA",
    "RESULT_SCHEMA",
    "admit_continuation",
    "apply_explicit_interval",
    "continue_after_request",
]
