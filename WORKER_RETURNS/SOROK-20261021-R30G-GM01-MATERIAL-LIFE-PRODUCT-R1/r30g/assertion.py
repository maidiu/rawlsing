"""Frozen R30G-GM01-C12-A0-A2-P01 assertion and alternatives."""
from __future__ import annotations


def p01(observed: dict, gm01: dict) -> bool:
    """B's performed share enables A's own performed inspection at the product."""
    return (
        observed.get("status") == "OK"
        and "ARRIVAL" in observed.get("claims", [])
        and observed.get("tools_before") == 1
        and observed.get("action", {}).get("status") == "OK"
        and observed.get("action", {}).get("admitted") is True
        and observed.get("tools_after") == 0
        and observed.get("completed_after") == observed.get("completed_before") + 1
        and observed.get("material_after") == observed.get("material_before") - 1
        and observed.get("a2_other_units") == 4
        and "OFFSCREEN_NO_CHANGE" in observed.get("a2_offscreen", [])
        and observed.get("material_start", {}).get("gm01_receipt_hash") == gm01.get("result_hash")
        and observed.get("c12_verify", {}).get("ok") is True
    )


def share_omit(observed: dict) -> bool:
    """B share leaves a feasible tool, but A does not perform; B can use it."""
    return (
        observed.get("tools_before") == 1
        and observed.get("action", {}).get("status") == "NO_CHANGE"
        and observed.get("completed_after") == observed.get("completed_before")
        and observed.get("tools_after") == 1
        and observed.get("a2_other_units") == 5
        and "OFFSCREEN_REPAIR" in observed.get("a2_offscreen", [])
    )


def deny_no_material(observed: dict) -> bool:
    """A cannot perform when B did not share and A had no prior tool."""
    return (
        observed.get("tools_before") == 0
        and observed.get("action", {}).get("status") == "DENY"
        and observed.get("action", {}).get("code") == "GM01_NO_TOOL"
        and observed.get("completed_after") == observed.get("completed_before")
        and observed.get("tools_after") == 0
        and observed.get("a2_other_units") == 4
        and "OFFSCREEN_NO_CHANGE" in observed.get("a2_offscreen", [])
    )
