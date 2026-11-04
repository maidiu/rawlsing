"""Explicit state separation for routing, eligibility and decline semantics.

This is a small test harness, not a production policy. It prevents an unknown
route, an ineligible route and an explicit decline from being collapsed into the
same state.
"""
from __future__ import annotations


def classify_state(route_state: str, response_code: int, response_semantics_certified: bool) -> str:
    """Classify one synthetic observation without reading respondent data.

    `route_state` must be one of UNKNOWN, ELIGIBLE or INELIGIBLE.
    """
    if route_state == "UNKNOWN":
        return "ROUTING_UNKNOWN"
    if route_state == "INELIGIBLE":
        return "ROUTED_OUT"
    if route_state == "ELIGIBLE":
        if response_code == 99:
            return "DECLINED" if response_semantics_certified else "RESPONSE_SEMANTICS_HELD"
        return "ELIGIBLE_RESPONSE"
    raise ValueError(f"unknown route_state: {route_state!r}")
