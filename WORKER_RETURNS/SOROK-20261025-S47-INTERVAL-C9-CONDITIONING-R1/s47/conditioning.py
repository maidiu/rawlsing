"""Compose one qualified S46 interval source for the real C9 conditioner."""
from __future__ import annotations

from .bootstrap import install

install()

from candidate.conditioning import make_conditioning_source  # noqa: E402

from .errors import S47Refusal  # noqa: E402

SOURCE_CLASS = "ResolvedStructuralContext"
SCHEMA = "S47_INTERVAL_MATERIAL_CONDITION@1"


def current_interval_source(session) -> dict | None:
    states = [
        row for row in session.read_interval_states()
        if row.get("currentness") == "CURRENT"
    ]
    if not states:
        return None
    state = states[-1]
    if hasattr(session, "_condition_revoked") and session._condition_revoked(
        state["state_id"]
    ):
        return None
    base = session.world_prerequisites()
    latest = state["segments"][-1]["world"]
    access = "granted" if base.get("material_available") else "denied"
    source_ref = "TEST_ONLY_S47_INTERVAL_" + state["state_id"]
    content = {
        "schema": SCHEMA,
        "grade": "TEST_ONLY_S47_WORLD_MATERIAL_CONDITION_NOT_NATIVE",
        "native": False,
        "psychology_claim": False,
        "condition_kind": "OBJECTIVE_BOUNDED_MATERIAL_PARTICIPATION",
        "source_owner": state.get("world_owner"),
        "source_grade": "TEST_ONLY_INSTALLED_SIMULATION_OWNER",
        "subject": session.world().actor_state.get("A", {}).get("actor_id"),
        "actor_id": session.world().actor_state.get("A", {}).get("actor_id"),
        "branch_id": session.branch_id,
        "scene": "workshop",
        "access": access,
        "as_of": int(state.get("end", session.clock())),
        "interval_state_id": state["state_id"],
        "interval_receipt_hash": state["receipt_hash"],
        "domain_issuance_id": state.get("domain_issuance_id", ""),
        "domain_issuance_hash": state.get("domain_issuance_hash", ""),
        "domain_id": state.get("domain_id", ""),
        "domain_hash": state.get("domain_hash", ""),
        "mode": state.get("domain", {}).get("mode", ""),
        "status": state.get("status"),
        "coverage": list(state.get("coverage") or []),
        "currentness": state.get("currentness"),
        "material_after_interval": bool(
            (latest.get("state_after") or {}).get("material_remaining", 0)
        ),
        "private_b_motive_included": False,
        "actor_knowledge_inferred": False,
        "actor_access_granted": False,
        "native_authority_claimed": False,
    }
    return make_conditioning_source(
        source_ref=source_ref,
        source_class=SOURCE_CLASS,
        subject=content["subject"],
        body=content,
    )


def qualify_source(session, source: dict) -> dict:
    if not isinstance(source, dict):
        raise S47Refusal("S47_SOURCE_NOT_RECORD")
    if source.get("source_class") != SOURCE_CLASS:
        raise S47Refusal("S47_SOURCE_CLASS_UNAUTHORIZED")
    content = source.get("content") or {}
    if content.get("schema") != SCHEMA:
        raise S47Refusal("S47_SOURCE_SCHEMA_MISMATCH")
    states = [
        row for row in session.read_interval_states()
        if row.get("currentness") == "CURRENT"
    ]
    if not states:
        raise S47Refusal("S47_INTERVAL_NOT_CURRENT")
    state = states[-1]
    expected_actor = session.world().actor_state.get("A", {}).get("actor_id")
    latest = state["segments"][-1]["world"]
    after = latest.get("state_after") or {}
    expected = {
        "schema": SCHEMA,
        "grade": "TEST_ONLY_S47_WORLD_MATERIAL_CONDITION_NOT_NATIVE",
        "native": False,
        "psychology_claim": False,
        "condition_kind": "OBJECTIVE_BOUNDED_MATERIAL_PARTICIPATION",
        "source_owner": state.get("world_owner"),
        "source_grade": "TEST_ONLY_INSTALLED_SIMULATION_OWNER",
        "actor_id": expected_actor,
        "subject": expected_actor,
        "branch_id": session.branch_id,
        "scene": "workshop",
        "as_of": int(state.get("end", session.clock())),
        "interval_state_id": state["state_id"],
        "interval_receipt_hash": state["receipt_hash"],
        "domain_issuance_id": state.get("domain_issuance_id", ""),
        "domain_issuance_hash": state.get("domain_issuance_hash", ""),
        "domain_id": state.get("domain_id", ""),
        "domain_hash": state.get("domain_hash", ""),
        "mode": state.get("domain", {}).get("mode", ""),
        "status": state.get("status"),
        "coverage": state.get("coverage"),
        "currentness": state.get("currentness"),
        "material_after_interval": bool(after.get("material_remaining", 0)),
        "private_b_motive_included": False,
        "actor_knowledge_inferred": False,
        "actor_access_granted": False,
        "native_authority_claimed": False,
    }
    for field, value in expected.items():
        if content.get(field) != value:
            raise S47Refusal("S47_SOURCE_" + field.upper() + "_MISMATCH")
    if source.get("source_ref") != "TEST_ONLY_S47_INTERVAL_" + state["state_id"]:
        raise S47Refusal("S47_SOURCE_REF_MISMATCH")
    if source.get("subject") != expected_actor:
        raise S47Refusal("S47_SOURCE_SUBJECT_MISMATCH")
    expected_access = "granted" if session.world_prerequisites().get(
        "material_available"
    ) else "denied"
    if content.get("access") != expected_access:
        raise S47Refusal("S47_SOURCE_ACCESS_MISMATCH")
    expected_source = make_conditioning_source(
        source_ref=source["source_ref"], source_class=SOURCE_CLASS,
        subject=expected_actor, body=dict(content),
    )
    if source.get("source_hash") != expected_source.get("source_hash"):
        raise S47Refusal("S47_SOURCE_HASH_MISMATCH")
    return source


__all__ = ["SOURCE_CLASS", "SCHEMA", "current_interval_source", "qualify_source"]
