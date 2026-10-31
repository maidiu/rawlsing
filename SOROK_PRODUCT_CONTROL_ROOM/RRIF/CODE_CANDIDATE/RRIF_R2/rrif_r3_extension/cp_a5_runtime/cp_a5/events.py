"""Sealed sourcefree CP-A5 world events.

The BP4 world accepts only its own event kinds. CP-A5 appends additional
source-owned events to the same C12 world-event table with a distinct schema;
the guarded C12 reader still verifies their hashes, sequence, clock and fork
prefix. No renderer or encounter can create one of these events.
"""
from __future__ import annotations

from bp4.canon import assert_no_forbidden, digest
from bp4.world import owner_receipt

CP_EVENT_SCHEMA = "SOROK_CP_A5_EVENT@1"
CP_EVENT_PREFIX = "TEST_ONLY_CP_A5_EVT_"
CP_GRADE = "TEST_ONLY_SOURCEFREE_CP_A5_NOT_NATIVE"


def make_cp_event(*, clock: int, kind: str, actor_id: str, location: str,
                  summary: str, body: dict, sequence: int,
                  persistent: bool = True) -> dict:
    """Create a sealed source-owned CP event with an explicit owner receipt."""
    receipt = owner_receipt(act=kind, actor_id=actor_id, clock=clock,
                            location=location)
    base = {
        "schema": CP_EVENT_SCHEMA,
        "clock": int(clock),
        "kind": kind,
        "actor_id": actor_id,
        "location": location,
        "summary": summary,
        "body": body,
        "owner_receipt": receipt,
        "persistent": bool(persistent),
        "sequence": int(sequence),
        "grade": CP_GRADE,
        "native": False,
    }
    assert_no_forbidden(base)
    event_id = CP_EVENT_PREFIX + digest(base)
    event = {"event_id": event_id, **base}
    event["hash"] = digest(event)
    return event
