"""Current-root other-actor world source proposals for S48.

The only currently supported independent other-actor operation is BP4's
owner-receipted REFUSAL. A proposal is never performed before the product
interpretation barrier; this module issues it after that barrier and then
returns the source/case used by the existing S42/S47 path.
"""
from __future__ import annotations

from .bootstrap import install

install()

import firstclass  # noqa: E402
from bp4.world import make_event, owner_receipt  # noqa: E402
from candidate import digest  # noqa: E402

from .errors import S48Refusal

CANDIDATE_ID = "OTHER_REFUSES_TOOL"
SOURCE_OPERATION = "REFUSE_TOOL"


def candidate_specs(session) -> list[dict]:
    world = session.world()
    state = dict((world.actor_state or {}).get("B") or {})
    actor_id = state.get("actor_id")
    root_ids = set(session.read_root().get("actor_ids") or [])
    if not actor_id or actor_id not in root_ids:
        return []
    if actor_id == (world.actor_state.get("A") or {}).get("actor_id"):
        return []
    if not world.owner:
        return []
    return [{
        "candidate_id": CANDIDATE_ID,
        "source_owner": actor_id,
        "source_performer_owner": world.owner,
        "source_actor": actor_id,
        "source_operation": SOURCE_OPERATION,
        "source_kind": "BP4_OWNER_RECEIPTED_REFUSAL",
        "current_clock": world.clock,
        "material_guard": "NO_MATERIAL_MUTATION",
    }]


def eligible_candidate_ids(session=None) -> list[str]:
    if session is None:
        return []
    return [row["candidate_id"] for row in candidate_specs(session)]


def issue_current_source(session, candidate_id: str) -> tuple[dict, dict, dict]:
    if candidate_id != CANDIDATE_ID:
        raise S48Refusal("S48_SOURCE_OWNER_HOLD_NO_CURRENT_OPERATION", candidate_id)
    specs = candidate_specs(session)
    if not specs:
        raise S48Refusal("S48_SOURCE_OWNER_HOLD_NO_CURRENT_OWNER")
    spec = specs[0]
    world = session.world()
    b_actor = spec["source_actor"]
    a_actor = (world.actor_state.get("A") or {}).get("actor_id")
    if not a_actor:
        raise S48Refusal("S48_SOURCE_ACTOR_A_MISSING")
    receipt = owner_receipt(
        act="REFUSAL", actor_id="B", clock=world.clock,
        location=world.positions["B"],
    )
    event = make_event(
        clock=world.clock,
        kind="REFUSAL",
        actor_id="B",
        location=world.positions["B"],
        summary="The finishing worker refuses the tool request.",
        body={
            "operation": SOURCE_OPERATION,
            "to_actor": a_actor,
            "quantity": 0,
        },
        receipt=receipt,
        sequence=len(world.events),
    )
    world.add_event(event)
    session.product._checkpoint(session.branch_id, world.clock, world)
    first = session.read_events()[0]
    source = {
        "schema": "BP2_FIRSTCLASS_B_MATERIAL_SOURCE@1",
        "b_actor": b_actor,
        "b_owner": spec["source_owner"],
        "b_event_ref": event["event_id"],
        "b_event_hash": event["hash"],
        "b_performed": True,
        "b_operation": SOURCE_OPERATION,
        "b_quantity": 0,
        "b_to_actor": a_actor,
        "b_clock": event["clock"],
        "a_e1_ref": first["e1_event_id"],
        "a_e1_hash": first["e1_event_hash"],
        "a_e1_clock": first["event_time"],
        "source_grade": "TEST_ONLY_SOURCEFREE",
        "native": False,
        "psychology_claim": False,
    }
    case = {
        "schema": "S48_CURRENT_OTHER_SOURCE_CASE@1",
        "case_id": "S48_CURRENT_OTHER_REFUSAL",
        "actor": {"actor_id": a_actor},
        "other": {"actor_id": b_actor},
        "as_of": world.clock,
        "records": [
            {
                "kind": "OTHER_PERFORMED",
                "subject": b_actor,
                "owner": spec["source_owner"],
                "ref": event["event_id"],
                "content_hash": event["hash"],
                "performed": True,
                "at": event["clock"],
                "payload": {
                    "operation": SOURCE_OPERATION,
                    "to_actor": a_actor,
                    "quantity": 0,
                },
            },
            {
                "kind": "E1_EVENT",
                "subject": a_actor,
                "owner": "TEST_ONLY_OWNER_e1",
                "ref": first["e1_event_id"],
                "content_hash": first["e1_event_hash"],
                "at": first["event_time"],
                "payload": {},
            },
        ],
    }
    validated = firstclass.validate_source(source, case)
    validated["source_performer_owner"] = spec["source_performer_owner"]
    source["source_performer_owner"] = spec["source_performer_owner"]
    validated["source_validation_hash"] = digest(validated)
    return case, validated, event


__all__ = [
    "CANDIDATE_ID", "SOURCE_OPERATION", "candidate_specs",
    "eligible_candidate_ids", "issue_current_source",
]
