"""Frozen behavioral assertions for the sourcefree J/E join.

The assertions are intentionally about the actual consumer consequence:
J source/material state must reach the persisted root and the E help admission.
They do not infer psychology, native rules or human experience.
"""
from __future__ import annotations

from pathlib import Path

JOIN_POSITIVE_ASSERTION = "SOROK_JOIN_E_POSITIVE_P01"
JOIN_REFUSAL_ASSERTION = "SOROK_JOIN_E_REFUSAL_NO_TARGET_P01"
B_EVENT_ASSERTION = "SOROK_JOIN_E_B_EVENT_UPSTREAM_P01"


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


def b_event_positive(session, *, help_result: dict | None = None) -> dict:
    """Same named assertion for B's performed source and its upstream cut.

    The assertion is deliberately unchanged between the cut and restore. On an
    omitted or unavailable B source the ordinarily performed source, target,
    tool and E-help checks are false; no build/import exception is counted.
    """
    from .b_event import PERFORMED, validate_receipt

    source = session.product.source
    receipt = session.meta.get("b_performer_receipt")
    receipt_check = validate_receipt(receipt, source)
    base = positive(session, help_result=help_result)
    world = session.product._world(session.branch_id)
    checks = dict(base["checks"])
    checks.update({
        "b_disposition_performed": session.meta.get("j_b_disposition") == PERFORMED,
        "b_receipt_matches_source": receipt_check.get("ok") is True,
        "b_source_is_performed_share": (
            source.get("b_operation") == "SHARE_TOOL"
            and source.get("b_performed") is True),
        "b_clock_preserved": source.get("b_clock") == 5,
        "b_recipient_is_a": source.get("b_to_actor") == "TEST_ONLY_R31J_A",
        "branch_is_first_session": session.branch_id == "first_session",
        "canonical_product_root": (
            Path(session.product.root).resolve()
            == (Path(session.state_root) / "product").resolve()),
        "help_tool_available": (
            world.actor_state.get("A", {}).get("tools_remaining") == 1),
    })
    observed = dict(base["observed"])
    observed.update({
        "assertion": B_EVENT_ASSERTION,
        "j_b_disposition": session.meta.get("j_b_disposition"),
        "b_operation": source.get("b_operation"),
        "b_performed": source.get("b_performed"),
        "b_clock": source.get("b_clock"),
        "b_receipt": receipt_check.get("observed", {}),
    })
    return {"ok": all(checks.values()), "assertion": B_EVENT_ASSERTION,
            "checks": checks, "observed": observed}


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
