"""Bounded local user-phenomenal compositor.

Inputs are already-admitted objective world events and the user's actual
perception rows.  The compositor may select, omit and lexicalize; it cannot
create an event, change an utterance, expose actor-private state, or make
attention causally produce actor behaviour.
"""
from __future__ import annotations


def _label(event: dict) -> str:
    role = str(event.get("body", {}).get("public_role", ""))
    if event.get("actor_id") == "A" or role == "repair":
        return "the repair worker"
    if event.get("actor_id") == "B" or role == "finishing":
        return "the finisher"
    return "the neighbor"


def _text(event: dict) -> str:
    return str(event.get("body", {}).get("text", ""))


def compose(session, event_ids, *, attention: str = "focused") -> list[str]:
    perceived = session.user_perceived_ids()
    lines: list[str] = []
    ambient_used = False
    for event_id in event_ids:
        if event_id not in perceived:
            continue
        event = session.event(event_id)
        if not event:
            continue
        kind = event.get("kind")
        actor = event.get("actor_id")
        if kind == "SPEECH":
            text = _text(event)
            if actor == "U":
                lines.append(f'You say: "{text}"')
            else:
                line = f'{_label(event)} says: "{text}"'
                gesture = str(event.get("body", {}).get("gesture", ""))
                if gesture and attention != "distracted":
                    line += f" {gesture}"
                lines.append(line)
            continue
        if attention == "distracted":
            if not ambient_used:
                lines.append("The workshop noises continue around you.")
                ambient_used = True
            continue
        if attention == "tool_focused" and kind not in {
                "REPAIR", "INSPECT", "MOVE", "OFFSCREEN_REPAIR"}:
            continue
        if kind in {"REPAIR", "OFFSCREEN_REPAIR"}:
            lines.append(event.get("summary", "A material action is performed."))
        elif kind == "MOVE":
            lines.append(event.get("summary", "Someone moves through the workshop."))
        elif kind == "INSPECT":
            lines.append(event.get("summary", "The material is inspected."))
        elif kind == "ARRIVAL":
            lines.append(event.get("summary", "Someone arrives."))
        elif kind == "REFUSAL":
            lines.append(event.get("summary", "A boundary is made explicit."))
        elif kind == "NO_CHANGE":
            lines.append(event.get("summary", "Nothing material changes."))
    return lines
