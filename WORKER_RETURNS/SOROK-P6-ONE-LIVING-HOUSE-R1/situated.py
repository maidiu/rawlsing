"""Provisional actor interpretation over admitted P6 conduct and S46 time."""

from copy import deepcopy

from developmental_recursion.contracts import digest
from house import read_house
from situated_provider import ModelUnavailable


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


def reconsider(session, receipt, interpret, realize=None, *, actor_context=None, provider_mode="INJECTED"):
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
    available_actions = ("continue",) if realize is None else ("continue", "speak")
    packet = {
        "actor": actor["actor_id"],
        "room": world.positions["A"],
        "clock": world.clock,
        "elapsed": interval["end"] - interval["start"],
        "activity": {"role": actor.get("role"), "work_done": actor.get("completed_units"),
                     "material_remaining": actor.get("material_remaining"),
                     "interval_status": interval["status"]},
        "cues": cues,
        "recent_speech": recent_speech(session),
        "actor_context": actor_context_for(actor["actor_id"], actor_context),
        "available_actions": list(available_actions),
    }
    result = {"grade": "PROVISIONAL_MODEL_MEDIATED", "provider_mode": provider_mode,
              "packet_hash": digest(packet)}
    try:
        decision = interpret(deepcopy(packet))
    except ModelUnavailable:
        return {**result, "status": "MODEL_UNAVAILABLE"}
    if (type(decision) is not dict or set(decision) != {"attention", "interpretation", "action"}
            or decision["attention"] not in ("noticed", "vague", "misheard", "unnoticed", "uncertain")
            or (not cues and decision["attention"] in ("noticed", "vague", "misheard"))
            or not isinstance(decision["interpretation"], str)
            or len(decision["interpretation"]) > 500
            or decision["action"] not in available_actions):
        return {**result, "status": "INVALID_INTERPRETATION"}

    result.update(status="INTERPRETED", decision=decision)
    if decision["action"] == "speak":
        try:
            text = realize(deepcopy(packet), dict(decision))
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
