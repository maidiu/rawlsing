"""Role-parameterized S39 generation and independent B performer."""
from __future__ import annotations

from typing import Any, Mapping

from .bootstrap import install

install()

from bp4.world import make_event  # noqa: E402
from candidate import digest, seal  # noqa: E402
from candidate.actor_access_response import make_actor_local_access_witness  # noqa: E402
from s39.model import FULL_RULE, generate_choice  # noqa: E402
from s39.sources import make_source  # noqa: E402

from .errors import S49Refusal

B_ACTOR_KEY = "B"
S49_GRADE = "TEST_ONLY_S49_INDEPENDENT_ACTOR_PRODUCER"
CONTROLLED_GRADE = "TEST_ONLY_S49_CONTROLLED_B_MODEL_PREMISE_NOT_OBSERVED"
MISSING_B_CONTEXT = "S49_MISSING_CURRENT_B_ACTOR_OWNED_CONTEXT"
SOURCE_OWNER_HOLD = "S49_SOURCE_OWNER_HOLD"


def _current_event(session) -> dict:
    events = session.read_events()
    if not events:
        raise S49Refusal("S49_OCCURRED_EVENT_MISSING")
    return events[-1]


def _b_state(session) -> dict:
    return dict((session.world().actor_state or {}).get(B_ACTOR_KEY) or {})


def _b_access(session, event: dict) -> dict:
    actor_id = _b_state(session).get("actor_id")
    if not actor_id:
        raise S49Refusal("S49_B_ACTOR_MISSING")
    return make_actor_local_access_witness(
        actor_id=actor_id,
        event_ref=event.get("e1_event_hash"),
        access_time=session.clock(),
        source_ref="TEST_ONLY_S49_B_ACCESS_" + str(event.get("e1_event_id")),
        access_status="ACCESSIBLE",
        scene="workshop",
        content={
            "observed_event_ref": event.get("e1_event_id"),
            "observed_event_hash": event.get("e1_event_hash"),
            "observer": "B",
        },
    )


def root_b_sources(session) -> list[dict]:
    """Actual root B context sources currently available.

    The accepted root has no B-owned S39 predicate source; do not infer one
    from material, demographics, role, or project prose.
    """
    return []


def controlled_b_sources(session) -> list[dict]:
    """Explicit controlled S39 model-premise inputs for B, never observed life."""
    actor_id = _b_state(session).get("actor_id")
    if not actor_id:
        raise S49Refusal("S49_B_ACTOR_MISSING")
    return [make_source(
        source_ref="TEST_ONLY_S49_B_OTHER_PARTY_PRIOR_REFUSAL",
        source_class="HISTORICAL_EPISODE",
        actor_id=actor_id,
        branch_id=session.branch_id,
        as_of=session.clock(),
        predicate="PRIOR_B_REFUSAL",
        value=1,
        content={
            "other_party": "A",
            "episode": "other_party_refused_before_this_controlled_model_premise",
            "observed_inner_life": False,
        },
        recruitment_mode="CAUSAL_NOT_CONSCIOUS_RECALL",
    )]


def _world_for_b(session) -> dict:
    state = _b_state(session)
    world = session.world()
    workshop = (world.resources or {}).get("workshop", {})
    return {
        "actor_present": (world.positions or {}).get("B") == "workshop",
        "object_present": True,
        "tool_available": bool(
            int(state.get("tools_remaining", 0)) > 0
            and workshop.get("tool_available") is True
        ),
        "material_available": int(state.get("material_remaining", 0)) > 0,
        "free_hours": int(state.get("free_hours", 0)) > 0,
    }


def generate_b(session, *, source_records: list[Mapping[str, Any]] | None,
               rule=FULL_RULE) -> dict:
    event = _current_event(session)
    actor_id = _b_state(session).get("actor_id")
    if not actor_id:
        raise S49Refusal("S49_B_ACTOR_MISSING")
    records = list(source_records or [])
    access = _b_access(session, event)
    c8_digest = event.get("c8_state_digest", "")
    receipt = generate_choice(
        actor_id=actor_id,
        branch_id=session.branch_id,
        event_ref=event.get("e1_event_hash"),
        event_time=int(event.get("event_time", session.clock())),
        as_of=session.clock(),
        c8_state_digest=c8_digest,
        access_witness=access,
        access_outcome="RECEIVABLE_NO_OBSERVED_UPTAKE",
        source_records=records,
        world=_world_for_b(session),
        rule=rule,
    )
    body = {
        "schema": "S49_B_ACTOR_GENERATION@1",
        "grade": S49_GRADE if records else CONTROLLED_GRADE,
        "native": False,
        "psychology_claim": False,
        "actor_id": actor_id,
        "role": "B",
        "branch_id": session.branch_id,
        "event_ref": event.get("e1_event_id"),
        "event_hash": event.get("e1_event_hash"),
        "event_time": event.get("event_time"),
        "as_of": session.clock(),
        "source_count": len(records),
        "source_refs": list(receipt.get("source_refs") or []),
        "access_witness_hash": access.get("hash", ""),
        "generation": receipt,
        "missing_context": MISSING_B_CONTEXT if not records else "",
    }
    return seal(body)


def perform_b_attempt(session, generation_body: Mapping[str, Any]) -> dict:
    generation = generation_body.get("generation") or {}
    request = generation.get("attempt_request")
    actor_id = generation_body.get("actor_id")
    if not actor_id:
        raise S49Refusal("S49_B_ACTOR_MISSING")
    if not request:
        body = {
            "schema": "S49_B_PERFORMER_RESULT@1",
            "grade": S49_GRADE,
            "native": False,
            "actor_id": actor_id,
            "role": "B",
            "status": "NOT_ATTEMPTED",
            "performed": False,
            "reason": "NO_GENERATED_ATTEMPT",
            "event_id": "",
            "event_hash": "",
            "generation_hash": generation_body.get("hash", ""),
            "target_proposals": [],
        }
        return seal(body)
    option = request["option_id"]
    world = session.world()
    state = _b_state(session)
    if world.positions.get("B") != "workshop":
        return seal({
            "schema": "S49_B_PERFORMER_RESULT@1",
            "grade": S49_GRADE,
            "native": False,
            "actor_id": actor_id,
            "role": "B",
            "status": "DENIED",
            "performed": False,
            "reason": "B_NOT_PRESENT",
            "generation_hash": generation_body.get("hash", ""),
            "option_id": option,
            "event_id": "",
            "event_hash": "",
            "target_proposals": [],
        })
    if option == "ATTEND_OBJECT":
        event = make_event(
            clock=world.clock, kind="INSPECT", actor_id="B",
            location=world.positions["B"],
            summary="The finishing worker inspects the present material.",
            body={"changed": False, "generated": True},
            sequence=len(world.events),
        )
    elif option == "REQUEST_TOOL":
        if int(state.get("tools_remaining", 0)) < 1 or int(
            state.get("free_hours", 0)
        ) < 1:
            return seal({
                "schema": "S49_B_PERFORMER_RESULT@1",
                "grade": S49_GRADE,
                "native": False,
                "actor_id": actor_id,
                "role": "B",
                "status": "DENIED",
                "performed": False,
                "reason": "B_TOOL_OR_TIME_UNAVAILABLE",
                "generation_hash": generation_body.get("hash", ""),
                "option_id": option,
                "event_id": "",
                "event_hash": "",
                "target_proposals": [],
            })
        event = make_event(
            clock=world.clock, kind="SPEECH", actor_id="B",
            location=world.positions["B"],
            summary="The finishing worker requests the tool.",
            body={"text": "May I use the tool?", "observable": True,
                  "generated": True},
            sequence=len(world.events),
        )
    elif option == "EXPLICIT_REFUSAL":
        event = make_event(
            clock=world.clock, kind="REFUSAL", actor_id="B",
            location=world.positions["B"],
            summary="The finishing worker declines the current request.",
            body={"text": "No, not now.", "observable": True,
                  "generated": True},
            sequence=len(world.events),
        )
    else:
        return seal({
            "schema": "S49_B_PERFORMER_RESULT@1",
            "grade": S49_GRADE,
            "native": False,
            "actor_id": actor_id,
            "role": "B",
            "status": "DENIED",
            "performed": False,
            "reason": "UNKNOWN_GENERATED_OPTION",
            "generation_hash": generation_body.get("hash", ""),
            "option_id": option,
            "event_id": "",
            "event_hash": "",
            "target_proposals": [],
        })
    world.add_event(event)
    session._append_event(event, perceive=("A", "B", "U"))
    session.product._append_episode(
        session.branch_id, "B", "S49_B_ATTEMPT", world.clock,
        {
            "schema": "S49_B_PERFORMER_EPISODE@1",
            "actor_id": actor_id,
            "role": "B",
            "option_id": option,
            "event_id": event["event_id"],
            "event_hash": event["hash"],
            "generation_hash": generation_body.get("hash", ""),
        },
    )
    session.product._checkpoint(session.branch_id, world.clock, world)
    return seal({
        "schema": "S49_B_PERFORMER_RESULT@1",
        "grade": S49_GRADE,
        "native": False,
        "actor_id": actor_id,
        "role": "B",
        "status": "ADMITTED",
        "performed": True,
        "reason": "OK",
        "generation_hash": generation_body.get("hash", ""),
        "option_id": option,
        "event_id": event["event_id"],
        "event_hash": event["hash"],
        "event_kind": event["kind"],
        "world_clock": world.clock,
        "target_proposals": [],
    })


__all__ = [
    "B_ACTOR_KEY", "CONTROLLED_GRADE", "MISSING_B_CONTEXT", "S49_GRADE",
    "SOURCE_OWNER_HOLD", "controlled_b_sources", "generate_b",
    "perform_b_attempt", "root_b_sources",
]
