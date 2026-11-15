"""Independent targetless performer for one generated attempt."""
from __future__ import annotations

from typing import Mapping

from .bootstrap import install

install()

from candidate import seal  # noqa: E402
from bp4.world import make_event  # noqa: E402

from .model import GRADE, PROVENANCE  # noqa: E402


def _result(*, actor_id, branch_id, attempt_request, generation_receipt_hash,
            status, performed, reason, event=None, clock):
    body = {
        "schema": "S39_GENERATED_ATTEMPT_RESULT@1",
        "grade": GRADE,
        "provenance": PROVENANCE,
        "native": False,
        "actor_id": actor_id,
        "branch_id": branch_id,
        "option_id": attempt_request["option_id"],
        "action": attempt_request["action"],
        "performer": attempt_request["performer"],
        "s36_response_kind": attempt_request["s36_response_kind"],
        "generation_receipt_hash": generation_receipt_hash,
        "attempt_request_hash": attempt_request.get("hash", ""),
        "attempt_status": status,
        "performed": bool(performed),
        "admitted": bool(performed),
        "reason": reason,
        "world_clock": int(clock),
        "event_id": event.get("event_id", "") if event else "",
        "event_hash": event.get("hash", "") if event else "",
        "event_kind": event.get("kind", "") if event else "",
        "target_proposals": [],
    }
    return seal(body)


def perform_attempt(session, attempt_request: Mapping[str, object], *,
                    generation_receipt_hash: str = "") -> dict:
    """Attempt the generated action through existing targetless session writers."""
    actor_id = attempt_request["actor_id"]
    branch_id = session.branch_id
    option = attempt_request["option_id"]
    clock = session.clock()

    if option == "ATTEND_OBJECT":
        result = session.product.inspect(actor="A")
        event_id = result.get("event_id", "")
        event = session.event(event_id) if event_id else None
        if not event:
            return _result(actor_id=actor_id, branch_id=branch_id,
                           attempt_request=attempt_request,
                           generation_receipt_hash=generation_receipt_hash,
                           status="DENIED", performed=False,
                           reason="INSPECT_NOT_ADMITTED", clock=clock)
        return _result(actor_id=actor_id, branch_id=branch_id,
                       attempt_request=attempt_request,
                       generation_receipt_hash=generation_receipt_hash,
                       status="ADMITTED", performed=True, reason="OK",
                       event=event, clock=clock)

    if option == "REQUEST_TOOL":
        tools = session.world().actor_state.get("A", {}).get("tools_remaining", 0)
        if int(tools) < 1:
            return _result(actor_id=actor_id, branch_id=branch_id,
                           attempt_request=attempt_request,
                           generation_receipt_hash=generation_receipt_hash,
                           status="DENIED", performed=False,
                           reason="TOOL_NOT_AVAILABLE", clock=clock)
        event = session._actor_say(
            "A", "May I use the tool?",
            gesture="A turns toward the bench.",
            tone="ordinary",
            episode_kind="SAY",
        )
        return _result(actor_id=actor_id, branch_id=branch_id,
                       attempt_request=attempt_request,
                       generation_receipt_hash=generation_receipt_hash,
                       status="ADMITTED", performed=True, reason="OK",
                       event=event, clock=clock)

    if option == "EXPLICIT_REFUSAL":
        world = session.world()
        event = make_event(
            clock=world.clock,
            kind="REFUSAL",
            actor_id="A",
            location=world.positions.get("A", "workshop"),
            summary="A declines the current request.",
            body={
                "text": "No, not now.",
                "observable": True,
                "generated": True,
                "generation_receipt_hash": generation_receipt_hash,
            },
            sequence=len(world.events),
        )
        world.add_event(event)
        session._append_event(event, perceive=("A",))
        session._perceive_if_present(event, "U", "B")
        session.product._append_episode(
            branch_id, "A", "DO", world.clock,
            {"action": "generated_explicit_refusal",
             "event_id": event["event_id"],
             "generation_receipt_hash": generation_receipt_hash},
        )
        session.product._checkpoint(branch_id, world.clock, world)
        return _result(actor_id=actor_id, branch_id=branch_id,
                       attempt_request=attempt_request,
                       generation_receipt_hash=generation_receipt_hash,
                       status="ADMITTED", performed=True, reason="OK",
                       event=event, clock=clock)

    return _result(actor_id=actor_id, branch_id=branch_id,
                   attempt_request=attempt_request,
                   generation_receipt_hash=generation_receipt_hash,
                   status="DENIED", performed=False,
                   reason="UNKNOWN_GENERATED_OPTION", clock=clock)


__all__ = ["perform_attempt"]
