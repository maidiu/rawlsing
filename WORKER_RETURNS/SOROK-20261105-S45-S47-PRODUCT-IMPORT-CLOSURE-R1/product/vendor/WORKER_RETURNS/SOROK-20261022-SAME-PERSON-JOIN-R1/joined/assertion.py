"""Frozen behavioral assertions for the sourcefree J/E join.

The assertions are intentionally about the actual consumer consequence:
J source/material state must reach the persisted root and the E help admission.
They do not infer psychology, native rules or human experience.
"""
from __future__ import annotations

from pathlib import Path

JOIN_POSITIVE_ASSERTION = "SOROK_JOIN_E_POSITIVE_P01"
JOIN_REFUSAL_ASSERTION = "SOROK_JOIN_E_REFUSAL_NO_TARGET_P01"


def positive(session, *, help_result: dict | None = None) -> dict:
    """Return the frozen positive assertion and its observed values."""
    source = session.product.source
    root = session.product.c12_verify("root")
    branch = session.verify()
    meta = session.meta
    world = session.product._world(session.branch_id)
    checks = {
        "source_is_share": source.get("b_operation") == "SHARE_TOOL"
        and source.get("b_performed") is True,
        "source_matches_meta": source == meta.get("j_source"),
        "target_present": bool(meta.get("j_target_id")),
        "root_c12_ok": bool(root.get("ok")),
        "branch_c12_ok": bool(branch.get("ok")),
        "root_branch_present": session.product.store._branch("root") is not None,
        "material_action_is_e2_or_omit": meta.get("material_performance") in {"e2", "omit"},
        "actor_tool_state_visible": "tools_remaining" in world.actor_state.get("A", {}),
        "not_native": source.get("native") is False and meta.get("grade") == "TEST_ONLY_SOURCEFREE_NOT_NATIVE",
    }
    observed = {
        "assertion": JOIN_POSITIVE_ASSERTION,
        "source_ref": meta.get("j_source_ref"),
        "b_event_hash": source.get("b_event_hash"),
        "c8_state_digest": meta.get("j_c8_state_digest"),
        "e1_event_hash": meta.get("j_e1_event_hash"),
        "target_id": meta.get("j_target_id"),
        "tools_remaining": world.actor_state.get("A", {}).get("tools_remaining"),
        "branch_id": session.branch_id,
    }
    if help_result is not None:
        checks["help_admitted"] = bool(help_result.get("accepted"))
        observed["help_accepted"] = bool(help_result.get("accepted"))
        observed["help_strategy"] = help_result.get("strategy")
    return {"ok": all(checks.values()), "checks": checks, "observed": observed}


def cold_positive(state_root) -> dict:
    """Open a cold session and evaluate the same named positive assertion."""
    from .session import JoinedSession

    try:
        session = JoinedSession.open(Path(state_root))
    except Exception as exc:  # typed cold refusal is a behavioral negative
        return {"ok": False, "assertion": JOIN_POSITIVE_ASSERTION,
                "error": type(exc).__name__ + ":" + str(exc)}
    try:
        result = positive(session)
        result["verify"] = session.verify().get("ok")
        return result
    finally:
        session.close()


def refusal_no_target(probe: dict) -> dict:
    """Frozen negative: source refusal must not manufacture a C9 target."""
    c9 = probe.get("c9") or {}
    checks = {
        "status_is_hold": probe.get("status") == "HOLD",
        "code_is_no_target": probe.get("code") ==
        "JOIN_REFUSAL_NO_TARGET__OWNER_CONTRACT_REQUIRED",
        "source_is_refuse": (probe.get("source") or {}).get("b_operation") == "REFUSE_TOOL",
        "source_not_performed_share": (probe.get("source") or {}).get("b_performed") is True,
        "no_target_id": probe.get("target_id") == "" and c9.get("target_id") == "",
        "no_proposal": c9.get("target_reason") == "NO_PROPOSAL",
        "response_valid_empty": c9.get("response_status") == "RESPONSE_EFFECTS_VALID_EMPTY",
        "material_denied": c9.get("material_reason") == "NO_ELIGIBLE_MATERIAL_SOURCE",
        "owner_contract_present": bool((probe.get("owner_contract") or {}).get("required_decision")),
    }
    return {"ok": all(checks.values()), "assertion": JOIN_REFUSAL_ASSERTION,
            "checks": checks, "observed": {
                "source_operation": (probe.get("source") or {}).get("b_operation"),
                "c8_state_digest": probe.get("c8_state_digest"),
                "c9_target_branch": c9.get("target_branch"),
                "c9_target_reason": c9.get("target_reason"),
            }}
