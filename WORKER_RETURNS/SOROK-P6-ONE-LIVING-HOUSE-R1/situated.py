"""Provisional actor interpretation over admitted P6 conduct and S46 time."""

from copy import deepcopy

from developmental_recursion.contracts import digest
from house import read_house
from actor_initiative import (
    ACTION as VISIT_ADJACENT, _select_visit, destination_affordance,
    route_from_context, visit_adjacent_room,
)
from actor_scene_context import recent_self_actions
from situated_provider import ModelUnavailable
from sourcefree_p3_bridge import qualified_p3_read


def actor_context_for(actor_id, context):
    """Project only bound, actor-local fixture fields into the model packet."""
    if (type(context) is not dict or context.get("grade") != "SOURCEFREE_FIXTURE"
            or context.get("actor_id") != actor_id):
        return None
    local = {"grade": "SOURCEFREE_FIXTURE"}
    for field in ("priority", "relationship", "current_constraint"):
        value = context.get(field)
        if isinstance(value, str) and 0 < len(value) <= 500:
            local[field] = value
    routes = context.get("routes")
    if isinstance(routes, dict):
        local["routes"] = deepcopy(routes)
    else:
        route = route_from_context(context)
        if route is not None:
            local["route"] = route
    return local


def recent_speech(session):
    """Read only speech that the world already recorded as accessible to A."""
    rows = session.product.store.perceptions(session.branch_id, "A")
    speech = []
    for row in reversed(rows):
        event = session.event(row["event_id"])
        if event is None or event["kind"] != "SPEECH" or row["clock"] != event["clock"]:
            continue
        text = event["body"].get("text")
        if isinstance(text, str):
            speech.append({"event_id": event["event_id"], "clock": event["clock"],
                           "speaker": event["actor_id"], "text": text[:500]})
        if len(speech) == 4:
            break
    return list(reversed(speech))


def decision_is_grounded(decision, cues, available_actions):
    if (type(decision) is not dict
            or set(decision) != {"attention", "interpretation", "action", "cue_event_id", "channel"}
            or decision["attention"] not in ("noticed", "vague", "misheard", "unnoticed", "uncertain")
            or not isinstance(decision["interpretation"], str)
            or len(decision["interpretation"]) > 500
            or decision["action"] not in available_actions):
        return False
    event_id, channel = decision["cue_event_id"], decision["channel"]
    if decision["attention"] in ("unnoticed", "uncertain"):
        return event_id is None and channel is None
    if decision["attention"] == "misheard" and channel != "AUDITORY":
        return False
    return any(
        event_id == cue["event_id"] and channel in cue.get("channels", [cue.get("modality")])
        and channel in ("AUDITORY", "VISUAL")
        for cue in cues
    )



# This is time since the last *interpersonal/outward* interruption, not scene
# age, subjective memory, or a claim that the workshop is acoustically silent.
QUIET_BREAK_KINDS = frozenset({
    "SPEECH", "MOVE", "PLAY_INSTRUMENT", "STOP_INSTRUMENT",
    "APPROACH", "ORIENT",
})


def interaction_quiet(session, world, house, cues):
    """Actor-qualified interpersonal quiet, NOT all-seeing world silence.

    The P6 sourcefree acoustic lane can establish a sound cue, while
    registered actor perceptions and self-performed events are separately
    authoritative. An unperceived player GO cannot reset Nadia's clock.
    """
    facts = house.get("situated_conditions", {})
    audible = (
        facts.get("grade") == "SOURCEFREE_FIXTURE"
        and facts.get("hearing") == "available"
        and (
            world.positions.get("A") == "living room"
            or (world.positions.get("A") == "workshop"
                and facts.get("sound_path") == "audible")
        )
    )
    registered = {
        row.get("event_id")
        for row in session.product.store.perceptions(session.branch_id, "A")
    }
    qualified = {
        (cue.get("event_id"), cue.get("event_hash"))
        for cue in cues if isinstance(cue, dict)
    }
    baseline = house["epoch"]
    parent = None
    for event in session.events():
        if (event.get("kind") not in QUIET_BREAK_KINDS
                or event.get("actor_id") not in ("A", session.meta["user_actor"])
                or type(event.get("clock")) is not int
                or not baseline <= event["clock"] <= world.clock):
            continue
        actor_own = event["actor_id"] == "A"
        actor_perceived = event.get("event_id") in registered
        supplied_cue = (event.get("event_id"), event.get("hash")) in qualified
        audible_instrument = (
            audible and event["kind"] in {"PLAY_INSTRUMENT", "STOP_INSTRUMENT"}
            and event.get("location") == "living room"
        )
        if not (actor_own or actor_perceived or supplied_cue or audible_instrument):
            continue
        if event["clock"] >= baseline:
            baseline = event["clock"]
            parent = event["event_id"]
    if audible and house.get("mandolin_playing"):
        return {"elapsed": 0, "status": "ACTIVE_QUALIFIED_INSTRUMENT",
                "last_break_event_id": parent}
    return {"elapsed": world.clock - baseline,
            "status": "NO_ACTOR_QUALIFIED_INTERPERSONAL_INTERRUPTION",
            "last_break_event_id": parent}



def current_p3_actor_access(session, interval, world, house, packet, *, source_receipt=None, evidence_out=None):
    """Proof of current actor access for the optional TEST_ONLY P3 reader.

    A previously perceived MOVE or speech can inform situated interpretation,
    but cannot *by itself* activate a P3 mediator in a later interval. Outward
    cues must be exact derived matches to a committed world event and to the
    checkpointed sensory conditions. Ordinary self-actions and speech need
    current-interval actor perception, not merely a recent-history list entry.

    This is evidence provenance, not a semantic psychological trigger matcher.
    """
    from outward import sensory_candidate

    start, end = interval["start"], interval["end"]
    if type(start) is not int or type(end) is not int or start > end:
        raise ValueError("P6_P3_ACCESS_INTERVAL_INVALID")
    if evidence_out is not None and type(evidence_out) is not list:
        raise ValueError("P6_P3_ACCESS_EVIDENCE_SINK_INVALID")

    def admitted(event, basis):
        # World provenance is separate from the P3 record readset.
        # It does NOT claim that a native law matches this cue to this
        # psychological mediator, only that this world evidence was admitted.
        if evidence_out is not None:
            evidence_out.append({
                "event_id": event["event_id"], "event_hash": event["hash"],
                "clock": event["clock"], "basis": basis,
                "grade": "SOURCEFREE_TEST_ONLY",
            })
        return True

    perceived = {
        (row.get("event_id"), row.get("clock")) for row in
        session.product.store.perceptions(session.branch_id, "A")
        if isinstance(row, dict)
    }
    # This is the already-committed receipt produced by this P6 operation,
    # *not* a sourcefree sensory claim constructed by the model or its caller.
    current_outward = (
        source_receipt.get("outward_cue") if isinstance(source_receipt, dict) else None
    )
    current_performed = (
        source_receipt.get("performed") if isinstance(source_receipt, dict) else None
    )

    def world_event(row):
        if not isinstance(row, dict) or not isinstance(row.get("event_id"), str):
            return None
        event = session.event(row["event_id"])
        if (not isinstance(event, dict)
                or type(event.get("clock")) is not int
                or type(row.get("clock")) is not int
                or event["clock"] != row["clock"]
                or not start <= event["clock"] <= end
                or not isinstance(event.get("hash"), str)
                or ("event_hash" in row and event["hash"] != row["event_hash"])):
            return None
        return event

    # Only an actually *performed* outward event in this operation can
    # present a sourcefree sensory cue. Never infer a sensory producer from
    # event existence + actor perception + a caller-supplied modality:
    # the event may be real while the alleged cue is completely fabricated.
    # P6_MOVEMENT_EVIDENCE with HOLD_ACTOR_REGISTRATION_OWNER_MISSING is
    # likewise not a registered actor observation for P3/ADP purposes.
    for cue in packet["cues"]:
        event = world_event(cue)
        if event is None or cue.get("grade") != "SOURCEFREE_FIXTURE":
            continue
        if (cue == current_outward and current_performed == event
                and event.get("actor_id") == session.meta["user_actor"]
                and sensory_candidate(event, world, house) == cue):
            # The world-side source also requires an exact conduct parent.
            if any(
                ep.get("kind") == "P6_HOUSE_CONDUCT"
                and ep.get("clock") == event["clock"]
                and ep.get("body") == {
                    "event_id": event["event_id"],
                    "operation": event["kind"],
                }
                for ep in session.episodes(session.meta["user_actor"])
            ):
                return admitted(event, "P6_OUTWARD_CURRENT_OPERATION_DERIVED")

    # For near-term contextual lists, only new observations strictly after
    # this interval began may qualify. Same-clock past context is not a new
    # participant observation. Self-action helper already source-validates
    # actor ownership and actor perception; recheck at the current read cut.
    for row in packet["recent_self_actions"]:
        event = world_event(row)
        if (event is not None and event["clock"] > start
                and (event["event_id"], event["clock"]) in perceived
                and event.get("actor_id") == "A"):
            return admitted(event, "P6_ACTOR_PERCEIVED_CURRENT_SELF_ACTION")
    for row in packet["recent_speech"]:
        event = world_event(row)
        if (event is not None and event["clock"] > start
                and (event["event_id"], event["clock"]) in perceived
                and event.get("kind") == "SPEECH"
                and event.get("actor_id") == row.get("speaker")):
            return admitted(event, "P6_ACTOR_PERCEIVED_CURRENT_SPEECH")
    return False


def reconsider(session, receipt, interpret, realize=None, *, actor_context=None, provider_mode="INJECTED", psyche_owner=None, psyche_scope=None):
    """Use bounded actor-local inputs and keep interpretations in the turn receipt."""
    if interpret is None:
        return None
    interval = receipt["interval"]
    world, house = read_house(session)
    actor = world.actor_state["A"]
    if (interval["actor_id"] != actor["actor_id"] or interval["branch_id"] != session.branch_id
            or interval["root_hash"] != session.read_root()["root_hash"]
            or interval["end"] != world.clock):
        raise ValueError("P6 situated interval does not match the current actor and world")

    cues = [
        {key: row[key] for key in ("event_id", "event_hash", "clock", "performer",
                                    "origin", "destination", "modality", "basis")}
        for row in receipt.get("encounter_evidence", ())
        if row["recipient"] == "A" and row["eligibility"] == "ELIGIBLE"
    ]
    if receipt.get("outward_cue"):
        cues.append(receipt["outward_cue"])
    if actor_context is None:
        actor_context = house.get("situated_actor_context")
    local_context = actor_context_for(actor["actor_id"], actor_context)
    available_actions = ["continue"]
    if realize is not None:
        available_actions.append("speak")
    # Committed actor movement requires actor-local scene context actually
    # established in the checkpoint. A caller-supplied persona override cannot
    # authorize a world action merely by naming the same actor.
    checkpoint_context = actor_context_for(
        actor["actor_id"], house.get("situated_actor_context")
    )
    affordances = []
    if checkpoint_context is not None and checkpoint_context == local_context:
        option = destination_affordance(
            session, world, house, actor["actor_id"], checkpoint_context
        )
        if option is not None:
            available_actions.append(VISIT_ADJACENT)
            affordances.append(option)
    packet = {
        "actor": actor["actor_id"],
        "room": world.positions["A"],
        "clock": world.clock,
        "elapsed": interval["end"] - interval["start"],
        "scene_elapsed": world.clock - house["epoch"],
        "interaction_quiet": interaction_quiet(session, world, house, cues),
        "root_hash": session.read_root()["root_hash"],
        "branch_id": session.branch_id,
        "world_state_hash": digest(world.snapshot()),
        "house_source": house["source"],
        "conditions_hash": digest(house.get("situated_conditions")),
        "actor_context_hash": digest(house.get("situated_actor_context")),
        "actor_route": route_from_context(local_context, world.positions["A"]),
        "actor_route_hash": (
            digest(route_from_context(local_context, world.positions["A"]))
            if route_from_context(local_context, world.positions["A"]) is not None else None
        ),
        "action_affordances": affordances,
        "activity": {"role": actor.get("role"), "work_done": actor.get("completed_units"),
                     "material_remaining": actor.get("material_remaining"),
                     "interval_status": interval["status"]},
        "cues": cues,
        "recent_speech": recent_speech(session),
        "recent_self_actions": recent_self_actions(session),
        "actor_context": local_context,
        "available_actions": available_actions,
    }
    if psyche_owner is not None:
        if not isinstance(psyche_scope, dict):
            raise ValueError("P6_P3_SCOPE_REQUIRED")
        # A caller does not get to manufacture observation through a list
        # of near-term context. Bind the access decision to an exact event
        # receipt, and keep world hashes outside the P3 record readset.
        access_evidence = []
        observed = current_p3_actor_access(
            session, interval, world, house, packet,
            source_receipt=receipt, evidence_out=access_evidence,
        )
        p3_read = qualified_p3_read(
            psyche_owner, session,
            project=psyche_scope.get("project"),
            counterpart=psyche_scope.get("counterpart"),
            as_of=world.clock,
            interlocutor_role=psyche_scope.get("interlocutor_role"),
            relation_ref=psyche_scope.get("relation_ref"),
            obligation_refs=psyche_scope.get("obligation_refs", ()),
            actor_observed=observed,
        )
        p3_read["actor_access_evidence"] = access_evidence
        p3_read["world_readset"] = [row["event_hash"] for row in access_evidence]
        p3_read["stimulus_to_mediator_relevance"] = "UNISSUED_NATIVE_RULE"
        packet["sourcefree_p3"] = p3_read
    result = {"grade": "PROVISIONAL_MODEL_MEDIATED", "provider_mode": provider_mode,
              "packet_hash": digest(packet)}
    try:
        decision = interpret(deepcopy(packet))
    except ModelUnavailable:
        return {**result, "status": "MODEL_UNAVAILABLE"}
    if not decision_is_grounded(decision, cues, available_actions):
        return {**result, "status": "INVALID_INTERPRETATION"}

    result.update(status="INTERPRETED", decision=decision)
    if decision["action"] == VISIT_ADJACENT:
        _select_visit(session, packet, decision)
        result["movement"] = visit_adjacent_room(session, actor["actor_id"])
    elif decision["action"] == "speak":
        try:
            expressive_decision = {key: value for key, value in decision.items() if key != "interpretation"}
            text = realize(deepcopy(packet), expressive_decision)
        except ModelUnavailable:
            return {**result, "status": "EXPRESSION_UNAVAILABLE"}
        if not isinstance(text, str) or not text.strip() or len(text) > 500:
            return {**result, "status": "INVALID_EXPRESSION"}
        admission = session.product.say(text.strip(), actor="A")
        result["speech"] = admission
        if admission.get("admitted"):
            event = session.event(admission["event_id"])
            session._perceive_if_present(event, session.meta["user_actor"])
    return result
