"""Provisional actor interpretation over admitted P6 conduct and S46 time."""

from developmental_recursion.contracts import digest


def reconsider(session, receipt, interpret, realize=None, *, actor_context=None):
    """Use bounded actor-local inputs and keep interpretations in the turn receipt."""
    if interpret is None:
        return None
    interval = receipt["interval"]
    world = session.world()
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
    packet = {
        "actor": actor["actor_id"],
        "room": world.positions["A"],
        "clock": world.clock,
        "elapsed": interval["end"] - interval["start"],
        "activity": {"role": actor.get("role"), "work_done": actor.get("completed_units"),
                     "material_remaining": actor.get("material_remaining"),
                     "interval_status": interval["status"]},
        "cues": cues,
        "actor_context": actor_context,
        "available_actions": ["continue"] if realize is None else ["continue", "speak"],
    }
    decision = interpret(packet)
    result = {"grade": "PROVISIONAL_MODEL_MEDIATED", "packet_hash": digest(packet)}
    if (type(decision) is not dict or set(decision) != {"attention", "interpretation", "action"}
            or decision["attention"] not in ("noticed", "vague", "misheard", "unnoticed", "uncertain")
            or (not cues and decision["attention"] in ("noticed", "vague", "misheard"))
            or not isinstance(decision["interpretation"], str)
            or len(decision["interpretation"]) > 500
            or decision["action"] not in packet["available_actions"]):
        return {**result, "status": "INVALID_INTERPRETATION"}

    result.update(status="INTERPRETED", decision=decision)
    if decision["action"] == "speak":
        text = realize(packet, decision)
        if not isinstance(text, str) or not text.strip() or len(text) > 500:
            return {**result, "status": "INVALID_EXPRESSION"}
        admission = session.product.say(text.strip(), actor="A")
        result["speech"] = admission
        if admission.get("admitted"):
            event = session.event(admission["event_id"])
            session._perceive_if_present(event, session.meta["user_actor"])
    return result
