"""P5 presentation over the received, user-perceived P4 event projection."""

from collections import Counter

CHANNELS = {
    "SPEECH": "speech",
    "REPAIR": "work",
    "OFFSCREEN_REPAIR": "work",
    "INSPECT": "work",
    "ARRIVAL": "movement",
    "MOVE": "movement",
}
HISTORY_WINDOW = 12
DETAIL_BUDGET = 2


def visible_events(surface):
    return {
        row["event_id"]: row for row in surface["observations"]
        if row.get("perceived_by_user") is True and row.get("event_id")
    }


def attend(surface, history, event_id):
    """Remember an explicit choice of a perceived occurrence, once per event."""
    event = visible_events(surface).get(event_id)
    if event is None or event["kind"] not in CHANNELS:
        return None
    if event_id in history:
        return list(history)
    return [*history, event_id]


def orientation(events, history):
    """Use recent distinct choices as uncertain evidence of a reading habit."""
    recent = list(dict.fromkeys(history))[-HISTORY_WINDOW:]
    counts = Counter(
        CHANNELS[events[ref]["kind"]] for ref in recent
        if ref in events and events[ref]["kind"] in CHANNELS
    ).most_common(2)
    if not counts:
        return None
    channel, count = counts[0]
    runner_up = counts[1][1] if len(counts) == 2 else 0
    return channel if count >= 2 and count > runner_up else None


def line(event):
    # Speech is verbatim. The remaining prose is the received occurrence's
    # own observable summary, with no fallback that invents ambient activity.
    if event["kind"] == "SPEECH":
        text = event["body_public"].get("text")
        if text:
            speaker = event["actor_visible_id"]
            if speaker == "U":
                return f'You say, “{text}”'
            if speaker == "A":
                return f'Nadia says, “{text}”'
            return f'The finisher says, “{text}”' if speaker == "B" else event["summary"]
    if event["kind"] == "REPAIR" and event["actor_visible_id"] == "A":
        return "Nadia makes a repair."
    if (event["kind"] == "INSPECT" and event["actor_visible_id"] == "U"
            and event["summary"] == "The actor inspects the present material but changes nothing."):
        return "You examine the work."
    return event["summary"]


def render(surface, history, *, candidates=None, boundary=None):
    """Select detail from an already-admitted surface. Return source IDs with prose."""
    visible = visible_events(surface)
    focus = orientation(visible, history)
    refs = visible if candidates is None else dict.fromkeys(candidates)
    rows = [
        visible[ref] for ref in refs
        if ref in visible and ref != boundary and visible[ref]["kind"] in CHANNELS
    ]
    ranked = sorted(reversed(rows), key=lambda event: CHANNELS[event["kind"]] != focus)
    selected = {event["event_id"] for event in ranked[:DETAIL_BUDGET]}
    if boundary in visible:
        selected.add(boundary)
    chosen = [event for ref, event in visible.items() if ref in selected]
    return [
        {"event_id": event["event_id"], "text": text}
        for event in chosen if (text := line(event))
    ]
