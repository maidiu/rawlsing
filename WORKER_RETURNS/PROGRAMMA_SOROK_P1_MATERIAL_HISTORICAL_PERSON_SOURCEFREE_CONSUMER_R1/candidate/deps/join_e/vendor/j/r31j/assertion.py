"""R31J-PREC9-SOURCE-TO-C12-A0-P01 and material alternatives."""
from __future__ import annotations


def p01(observed: dict, gm01: dict) -> bool:
    source = observed.get("source_episode", {}).get("body", {}).get("gm01_source", {})
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
        and observed.get("c12_verify", {}).get("ok") is True
        and source.get("b_actor") == gm01.get("other")
        and source.get("gm01_result_hash") == gm01.get("result_hash")
        and source.get("b_operation") == "SHARE_TOOL"
        and source.get("b_performed") is True
        and bool(observed.get("c8_state_digest"))
    )


def share_omit(observed: dict) -> bool:
    return (
        observed.get("tools_before") == 1
        and observed.get("action", {}).get("status") == "NO_CHANGE"
        and observed.get("completed_after") == observed.get("completed_before")
        and observed.get("tools_after") == 1
        and observed.get("a2_other_units") == 5
        and "OFFSCREEN_REPAIR" in observed.get("a2_offscreen", [])
        and observed.get("c12_verify", {}).get("ok") is True
    )
