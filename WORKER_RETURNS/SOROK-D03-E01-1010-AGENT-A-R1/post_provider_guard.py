"""One synchronous pre-P2-write custody barrier; not a psychological rule.

This proxy does not interpret or select prospective events. The caller's
validate() must inspect source/actor state after the external model/provider
returns, before the existing RecursionCycle validates or writes an event.
If validation fails, RecursionCycle preserves its ambiguous/held call marker.
A precommit observation is NOT an atomic P3/P2 transaction or native grant.
"""
from __future__ import annotations

from typing import Any, Callable, Mapping


class GuardedProvider:
    def __init__(self, delegate: Any, validate: Callable[[], None]) -> None:
        if not callable(getattr(delegate, "call", None)):
            raise TypeError("provider must expose call")
        if not callable(validate):
            raise TypeError("custody validation callback is required")
        self._delegate = delegate
        self._validate = validate

    def call(self, request: Mapping[str, Any]) -> Mapping[str, Any]:
        response = self._delegate.call(request)
        # This MUST precede the return to RecursionCycle._parse_proposals/
        # BatchEngine; an error here makes _call HOLD, not a world event.
        self._validate()
        return response
