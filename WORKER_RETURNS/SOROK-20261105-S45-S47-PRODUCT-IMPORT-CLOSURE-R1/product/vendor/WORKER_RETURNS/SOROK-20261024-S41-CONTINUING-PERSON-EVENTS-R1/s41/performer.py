"""Continuation performer wrapper: current C12 inventory governs admission."""
from __future__ import annotations

from typing import Mapping

from .bootstrap import install

install()

from candidate import seal  # noqa: E402
from s40.performer import perform_generated_attempt  # noqa: E402


def _denied(*, attempt_request, generation_receipt, actor_id, branch_id, clock,
            reason):
    return seal({
        "schema": "S39_GENERATED_ATTEMPT_RESULT@1",
        "grade": "TEST_ONLY_CONSTRUCTIVE_GENERATION",
        "provenance": "TEST_ONLY_CONSTRUCTIVE_GENERATION_NOT_EXTERNALLY_OBSERVED",
        "native": False,
        "actor_id": actor_id,
        "branch_id": branch_id,
        "option_id": attempt_request["option_id"],
        "action": attempt_request["action"],
        "performer": attempt_request["performer"],
        "s36_response_kind": attempt_request["s36_response_kind"],
        "generation_receipt_hash": generation_receipt["hash"],
        "attempt_request_hash": attempt_request.get("hash", ""),
        "attempt_status": "DENIED",
        "performed": False,
        "admitted": False,
        "reason": reason,
        "world_clock": int(clock),
        "event_id": "",
        "event_hash": "",
        "event_kind": "",
        "language": None,
        "target_proposals": [],
    })


def perform_continuation_attempt(
    session,
    attempt_request: Mapping[str, object],
    *,
    generation_receipt: Mapping[str, object],
    e1_identity: Mapping[str, object],
) -> dict:
    option = attempt_request["option_id"]
    if option == "REQUEST_TOOL":
        workshop = session.world().resources.get("workshop", {})
        if workshop.get("tool_available") is not True:
            return _denied(
                attempt_request=attempt_request,
                generation_receipt=generation_receipt,
                actor_id=attempt_request["actor_id"],
                branch_id=session.branch_id,
                clock=session.clock(),
                reason="TOOL_NOT_AVAILABLE_IN_CURRENT_WORLD",
            )
    return perform_generated_attempt(
        session,
        attempt_request,
        generation_receipt=generation_receipt,
        e1_identity=e1_identity,
    )


__all__ = ["perform_continuation_attempt"]
