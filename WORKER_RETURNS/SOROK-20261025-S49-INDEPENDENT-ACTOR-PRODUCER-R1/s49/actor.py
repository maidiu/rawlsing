"""Role-parameterized S39 generation and independent B performer."""
from __future__ import annotations

from typing import Any, Mapping

from .bootstrap import install

install()

from bp4.world import make_event  # noqa: E402
from candidate import digest, seal, valid  # noqa: E402
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
    world = session.world()
    action_event_id = event.get("action_event_id", "")
    action_event = session.event(action_event_id) if action_event_id else None
    if action_event is not None and world.positions.get(
        B_ACTOR_KEY
    ) != action_event.get("location"):
        action_event = None
    perceived = []
    if action_event_id:
        perceived = [
            row for row in session.product.store.perceptions(
                session.branch_id, B_ACTOR_KEY
            )
            if row.get("event_id") == action_event_id
        ]
    if not action_event or not perceived:
        return make_actor_local_access_witness(
            actor_id=actor_id,
            event_ref=event.get("e1_event_hash"),
            access_time=session.clock(),
            source_ref="S49_NO_OBSERVED_B_ACCESS",
            access_status="NOT_WITNESSED",
            scene="",
            content={
                "observed": False,
                "observed_event_ref": event.get("e1_event_id"),
                "observer": "B",
            },
        )
    row = perceived[-1]
    return make_actor_local_access_witness(
        actor_id=actor_id,
        event_ref=event.get("e1_event_hash"),
        access_time=int(row.get("clock", session.clock())),
        source_ref="TEST_ONLY_ADP017_S49_B_" + action_event_id,
        access_status="ACCESSIBLE",
        scene=str(action_event.get("location", "")),
        content={
            "observed_event_id": action_event_id,
            "observed_event_hash": action_event.get("hash", ""),
            "perception_clock": row.get("clock"),
            "perception_channel": row.get("channel"),
            "observer": "B",
        },
    )


def record_b_observation(session, event: dict | None = None) -> dict:
    event = event or _current_event(session)
    action_id = event.get("action_event_id", "")
    action_event = session.event(action_id) if action_id else None
    if not action_event:
        raise S49Refusal("S49_B_OBSERVATION_EVENT_MISSING")
    world = session.world()
    if world.positions.get("B") != action_event.get("location"):
        raise S49Refusal("S49_B_NOT_PRESENT_FOR_OBSERVATION")
    session._perceive_if_present(action_event, "B")
    session.product._checkpoint(session.branch_id, world.clock, world)
    rows = [
        row for row in session.product.store.perceptions(
            session.branch_id, B_ACTOR_KEY
        )
        if row.get("event_id") == action_id
    ]
    if not rows:
        raise S49Refusal("S49_B_OBSERVATION_NOT_RECORDED")
    session.meta["s49_last_b_observation"] = dict(rows[-1])
    session._save_join_meta()
    return rows[-1]


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


def _source_chain_hash(actor_id, branch_id, event_ref, event_hash, root,
                       rule_hash, access_source_ref, access_source_hash,
                       source_refs) -> str:
    return digest({
        "actor_id": actor_id,
        "branch_id": branch_id,
        "event_ref": event_ref,
        "event_hash": event_hash,
        "role": "B",
        "root_hash": root,
        "rule_content_hash": rule_hash,
        "access_source_ref": access_source_ref,
        "access_source_hash": access_source_hash,
        "source_refs": source_refs,
    })


def generate_b(session, *, source_records: list[Mapping[str, Any]] | None,
               rule=FULL_RULE,
               supplemental_reasons: list[Mapping[str, Any]] | None = None) -> dict:
    # The former generic supplemental-reason authority is intentionally inert.
    # Callers cannot append option relations or labels outside validated sources.
    _ = supplemental_reasons
    event = _current_event(session)
    actor_id = _b_state(session).get("actor_id")
    if not actor_id:
        raise S49Refusal("S49_B_ACTOR_MISSING")
    records = list(source_records or [])
    access = _b_access(session, event)
    c8_digest = event.get("c8_state_digest", "")
    if access.get("access_status") != "ACCESSIBLE":
        return seal({
            "schema": "S49_B_ACTOR_GENERATION@1",
            "grade": S49_GRADE,
            "native": False,
            "psychology_claim": False,
            "actor_id": actor_id,
            "role": "B",
            "branch_id": session.branch_id,
            "event_ref": event.get("e1_event_id"),
            "event_hash": event.get("e1_event_hash"),
            "event_time": event.get("event_time"),
            "as_of": session.clock(),
            "role": "B",
            "root_hash": session.read_root().get("root_hash", ""),
            "root_id": session.read_root().get("root_id", ""),
            "rule_content_hash": rule.content_hash,
            "access_source_ref": access.get("source_ref", ""),
            "access_source_hash": access.get("source_hash", ""),
            "source_chain_hash": _source_chain_hash(
                actor_id, session.branch_id, event.get("e1_event_id"),
                event.get("e1_event_hash"),
                session.read_root().get("root_hash", ""),
                rule.content_hash, access.get("source_ref", ""),
                access.get("source_hash", ""),
                [row.get("source_ref") for row in records],
            ),
            "source_count": len(records),
            "source_refs": [],
            "access_witness_hash": access.get("hash", ""),
            "generation": {
                "selection_status": "ACCESS_NOT_OBSERVED",
                "selected_option": "",
                "attempt_request": None,
                "source_refs": [],
                "reasons": [],
                "eligible_options": [],
                "rule": {},
            },
            "missing_context": "S49_B_ACCESS_NOT_OBSERVED",
        })
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
        "role": "B",
        "root_hash": session.read_root().get("root_hash", ""),
        "root_id": session.read_root().get("root_id", ""),
        "rule_content_hash": rule.content_hash,
        "access_source_ref": access.get("source_ref", ""),
        "access_source_hash": access.get("source_hash", ""),
        "source_chain_hash": _source_chain_hash(
            actor_id, session.branch_id, event.get("e1_event_id"),
            event.get("e1_event_hash"),
            session.read_root().get("root_hash", ""),
            rule.content_hash, access.get("source_ref", ""),
            access.get("source_hash", ""),
            [row.get("source_ref") for row in records],
        ),
        "source_count": len(records),
        "source_refs": list(receipt.get("source_refs") or []),
        "access_witness_hash": access.get("hash", ""),
        "generation": receipt,
        "missing_context": MISSING_B_CONTEXT if not records else "",
    }
    return seal(body)


def _invalid_result(session, generation_body: Mapping[str, Any], reason: str) -> dict:
    return seal({
        "schema": "S49_B_PERFORMER_RESULT@1",
        "grade": S49_GRADE,
        "native": False,
        "actor_id": "B",
        "role": "B",
        "status": "DENIED",
        "performed": False,
        "reason": reason,
        "generation_hash": generation_body.get("hash", ""),
        "option_id": "",
        "event_id": "",
        "event_hash": "",
        "target_proposals": [],
    })


def attempt_intent(session, generation_body: Mapping[str, Any]) -> dict:
    receipt = generation_body.get("generation") or {}
    request = receipt.get("attempt_request") or {}
    return seal({
        "schema": "S49_B_ATTEMPT_INTENT@1",
        "grade": S49_GRADE,
        "native": False,
        "role": "B",
        "actor_id": generation_body.get("actor_id"),
        "branch_id": generation_body.get("branch_id"),
        "root_hash": generation_body.get("root_hash"),
        "root_id": generation_body.get("root_id"),
        "event_ref": generation_body.get("event_ref"),
        "event_hash": generation_body.get("event_hash"),
        "generation_hash": generation_body.get("hash"),
        "attempt_request_hash": request.get("hash"),
        "option_id": request.get("option_id"),
        "rule_content_hash": generation_body.get("rule_content_hash"),
        "access_source_ref": generation_body.get("access_source_ref"),
        "access_source_hash": generation_body.get("access_source_hash"),
        "source_chain_hash": generation_body.get("source_chain_hash"),
    })


def canonical_attempt_intent(session, generation_body: Mapping[str, Any]) -> dict | None:
    rows = [
        row for row in session.product.store.episodes(session.branch_id)
        if row.get("kind") == "S49_B_ATTEMPT_INTENT"
    ]
    for row in reversed(rows):
        body = dict(row.get("body") or {})
        if body.get("generation_hash") == generation_body.get("hash"):
            return {"episode_id": row.get("episode_id"), "body": body}
    return None


def _canonical_generation(session, generation_body: Mapping[str, Any]) -> dict | None:
    target_hash = generation_body.get("hash", "")
    rows = [
        row for row in session.product.store.episodes(session.branch_id)
        if row.get("kind") == "S49_B_ACTOR_TURN"
        and (row.get("body") or {}).get("stage") == "GENERATION"
    ]
    for row in reversed(rows):
        body = dict(row.get("body") or {})
        generation = body.get("generation")
        if isinstance(generation, dict) and generation.get("hash") == target_hash:
            return body
    return None


def validate_b_generation(session, generation_body: Mapping[str, Any]) -> dict:
    if not valid(dict(generation_body)):
        raise S49Refusal("S49_GENERATION_UNSEALED")
    canonical = _canonical_generation(session, generation_body)
    if canonical is None:
        raise S49Refusal("S49_GENERATION_NOT_CANONICAL")
    if canonical.get("generation") != dict(generation_body):
        raise S49Refusal("S49_GENERATION_BODY_MISMATCH")
    actor_id = _b_state(session).get("actor_id")
    event = _current_event(session)
    root = session.read_root()
    receipt = generation_body.get("generation") or {}
    if generation_body.get("role") != "B":
        raise S49Refusal("S49_GENERATION_ROLE_MISMATCH")
    if generation_body.get("root_hash") != root.get("root_hash"):
        raise S49Refusal("S49_GENERATION_ROOT_MISMATCH")
    if generation_body.get("root_id") != root.get("root_id"):
        raise S49Refusal("S49_GENERATION_ROOT_ID_MISMATCH")
    receipt_rule = receipt.get("rule") or {}
    if (
        receipt_rule.get("rule_id") != FULL_RULE.rule_id
        or receipt_rule.get("version") != FULL_RULE.version
        or receipt_rule.get("content_hash") != FULL_RULE.content_hash
        or generation_body.get("rule_content_hash") != FULL_RULE.content_hash
    ):
        raise S49Refusal("S49_GENERATION_RULE_MISMATCH")
    if generation_body.get("source_refs") != list(receipt.get("source_refs") or []):
        raise S49Refusal("S49_GENERATION_SOURCE_REFS_MISMATCH")
    expected_chain = _source_chain_hash(
        actor_id, session.branch_id, event.get("e1_event_id"),
        event.get("e1_event_hash"),
        root.get("root_hash", ""), FULL_RULE.content_hash,
        generation_body.get("access_source_ref", ""),
        generation_body.get("access_source_hash", ""),
        generation_body.get("source_refs") or [],
    )
    if generation_body.get("source_chain_hash") != expected_chain:
        raise S49Refusal("S49_GENERATION_SOURCE_CHAIN_MISMATCH")
    if generation_body.get("event_hash") != event.get("e1_event_hash"):
        raise S49Refusal("S49_GENERATION_EVENT_HASH_MISMATCH")
    intent = canonical_attempt_intent(session, generation_body)
    if intent is None:
        raise S49Refusal("S49_ATTEMPT_INTENT_MISSING")
    expected_intent = attempt_intent(session, generation_body)
    if not valid(dict(intent["body"])):
        raise S49Refusal("S49_ATTEMPT_INTENT_UNSEALED")
    if dict(intent["body"]) != dict(expected_intent):
        raise S49Refusal("S49_ATTEMPT_INTENT_MISMATCH")
    request = (generation_body.get("generation") or {}).get("attempt_request") or {}
    if expected_intent.get("attempt_request_hash") != request.get("hash"):
        raise S49Refusal("S49_ATTEMPT_INTENT_LINK_MISMATCH")
    if expected_intent.get("option_id") != request.get("option_id"):
        raise S49Refusal("S49_ATTEMPT_INTENT_OPTION_MISMATCH")
    if generation_body.get("actor_id") != actor_id:
        raise S49Refusal("S49_GENERATION_ACTOR_MISMATCH")
    if generation_body.get("branch_id") != session.branch_id:
        raise S49Refusal("S49_GENERATION_BRANCH_MISMATCH")
    if generation_body.get("event_ref") != event.get("e1_event_id"):
        raise S49Refusal("S49_GENERATION_EVENT_MISMATCH")
    receipt = generation_body.get("generation") or {}
    request = receipt.get("attempt_request")
    if not isinstance(receipt, dict) or not valid(dict(receipt)):
        raise S49Refusal("S49_GENERATION_RECEIPT_UNSEALED")
    if receipt.get("actor_id") != actor_id or receipt.get("branch_id") != session.branch_id:
        raise S49Refusal("S49_GENERATION_RECEIPT_IDENTITY_MISMATCH")
    if receipt.get("event_ref") != event.get("e1_event_hash"):
        raise S49Refusal("S49_GENERATION_RECEIPT_EVENT_MISMATCH")
    if int(receipt.get("event_time", -1)) != int(event.get("event_time", -2)):
        raise S49Refusal("S49_GENERATION_TIME_MISMATCH")
    if int(receipt.get("as_of", -1)) < int(event.get("event_time", 0)):
        raise S49Refusal("S49_GENERATION_ASOF_MISMATCH")
    if receipt.get("selection_status") != "UNIQUE_SELECTED":
        raise S49Refusal("S49_GENERATION_NOT_SELECTED")
    if not isinstance(request, dict) or not valid(dict(request)):
        raise S49Refusal("S49_ATTEMPT_REQUEST_UNSEALED")
    if request.get("actor_id") != actor_id or request.get("branch_id") != session.branch_id:
        raise S49Refusal("S49_ATTEMPT_IDENTITY_MISMATCH")
    if request.get("event_ref") != event.get("e1_event_hash"):
        raise S49Refusal("S49_ATTEMPT_EVENT_MISMATCH")
    if request.get("option_id") != receipt.get("selected_option"):
        raise S49Refusal("S49_ATTEMPT_OPTION_MISMATCH")
    if request.get("generation_receipt_hash") not in (None, receipt.get("hash")):
        raise S49Refusal("S49_ATTEMPT_GENERATION_LINK_MISMATCH")
    access = _b_access(session, event)
    if access.get("access_status") != "ACCESSIBLE":
        raise S49Refusal("S49_ACCESS_NOT_OBSERVED")
    if generation_body.get("access_witness_hash") != access.get("hash"):
        raise S49Refusal("S49_GENERATION_ACCESS_MISMATCH")
    return canonical


def validate_normal_admission(session, source: Mapping[str, Any],
                              case: Mapping[str, Any],
                              event_time: int) -> None:
    s49_keys = [key for key in source if str(key).startswith("s49_")]
    required = {
        "s49_generation_hash", "s49_attempt_hash",
        "s49_rule_content_hash", "s49_access_source_ref",
        "s49_access_source_hash", "s49_source_chain_hash",
    }
    if not s49_keys:
        raise S49Refusal("S49_NORMAL_CONSUMER_CHAIN_MISSING")
    if not required.issubset(source):
        raise S49Refusal("S49_NORMAL_CONSUMER_CHAIN_MISSING")
    generation = None
    for row in session.product.store.episodes(session.branch_id):
        if row.get("kind") != "S49_B_ACTOR_TURN":
            continue
        body = dict(row.get("body") or {})
        value = body.get("generation")
        if (
            body.get("stage") == "GENERATION"
            and isinstance(value, dict)
            and value.get("hash") == source.get("s49_generation_hash")
        ):
            generation = value
            break
    if generation is None:
        raise S49Refusal("S49_NORMAL_CONSUMER_GENERATION_MISSING")
    validate_b_generation(session, generation)
    if generation.get("source_chain_hash") != source.get(
        "s49_source_chain_hash"
    ):
        raise S49Refusal("S49_NORMAL_CONSUMER_SOURCE_CHAIN_MISMATCH")
    if generation.get("rule_content_hash") != source.get(
        "s49_rule_content_hash"
    ) or generation.get("access_source_ref") != source.get(
        "s49_access_source_ref"
    ) or generation.get("access_source_hash") != source.get(
        "s49_access_source_hash"
    ):
        raise S49Refusal("S49_NORMAL_CONSUMER_CHAIN_MISMATCH")
    b_event = session.event(source.get("b_event_ref", ""))
    if not b_event or b_event.get("actor_id") != "B" or b_event.get(
        "kind"
    ) != "REFUSAL" or b_event.get("hash") != source.get(
        "b_event_hash"
    ) or b_event.get("clock") != source.get("b_clock"):
        raise S49Refusal("S49_NORMAL_CONSUMER_PERFORMER_MISSING")
    attempt_rows = [
        row for row in session.product.store.episodes(session.branch_id)
        if row.get("kind") == "S49_B_ACTOR_RESULT"
        and (row.get("body") or {}).get("stage") == "B_PERFORMER"
        and (row.get("body") or {}).get("generation_hash")
        == generation.get("hash")
    ]
    if len(attempt_rows) != 1:
        raise S49Refusal("S49_NORMAL_CONSUMER_PERFORMER_MISSING")
    attempt = (attempt_rows[0].get("body") or {}).get("attempt")
    if not isinstance(attempt, dict) or not valid(dict(attempt)):
        raise S49Refusal("S49_NORMAL_CONSUMER_PERFORMER_UNSEALED")
    if attempt.get("hash") != source.get("s49_attempt_hash"):
        raise S49Refusal("S49_NORMAL_CONSUMER_ATTEMPT_SUBSTITUTED")
    if attempt.get("generation_hash") != generation.get("hash"):
        raise S49Refusal("S49_NORMAL_CONSUMER_ATTEMPT_GENERATION_MISMATCH")
    if attempt.get("actor_id") != source.get("b_actor"):
        raise S49Refusal("S49_NORMAL_CONSUMER_B_ACTOR_MISMATCH")
    if attempt.get("branch_id") != session.branch_id:
        raise S49Refusal("S49_NORMAL_CONSUMER_ATTEMPT_BRANCH_MISMATCH")
    if attempt.get("event_id") != source.get("b_event_ref"):
        raise S49Refusal("S49_NORMAL_CONSUMER_B_EVENT_MISMATCH")
    if attempt.get("event_hash") != source.get("b_event_hash"):
        raise S49Refusal("S49_NORMAL_CONSUMER_B_HASH_MISMATCH")
    if attempt.get("status") != "ADMITTED" or attempt.get("performed") is not True:
        raise S49Refusal("S49_NORMAL_CONSUMER_PERFORMER_NOT_ADMITTED")
    if attempt.get("option_id") != "EXPLICIT_REFUSAL" or attempt.get(
        "event_kind"
    ) != "REFUSAL":
        raise S49Refusal("S49_NORMAL_CONSUMER_PERFORMER_KIND_MISMATCH")
    if attempt.get("world_clock") != source.get("b_clock"):
        raise S49Refusal("S49_NORMAL_CONSUMER_PERFORMER_CLOCK_MISMATCH")
    return None


def perform_b_attempt(session, generation_body: Mapping[str, Any]) -> dict:
    if (
        _canonical_generation(session, generation_body) is not None
        and canonical_attempt_intent(session, generation_body) is None
        and isinstance((generation_body.get("generation") or {}).get("attempt_request"), dict)
    ):
        session._append("S49_B_ATTEMPT_INTENT", attempt_intent(session, generation_body))
    try:
        validate_b_generation(session, generation_body)
    except S49Refusal as exc:
        return _invalid_result(session, generation_body, exc.code)
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
        "branch_id": session.branch_id,
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
    "attempt_intent", "canonical_attempt_intent", "perform_b_attempt",
    "record_b_observation", "root_b_sources", "validate_b_generation",
    "validate_normal_admission",
]
